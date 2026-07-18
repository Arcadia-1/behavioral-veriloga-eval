#!/usr/bin/env python3
"""Run selected v4 calibration cells through an OpenAI-compatible endpoint."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
import traceback
from typing import Any


HERE = Path(__file__).resolve().parent
PACKAGE = HERE.parents[1]
REPO = PACKAGE.parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import result_protocol as RESULT_PROTOCOL  # noqa: E402

EXPORTER = PACKAGE / "operations" / "tri_form_derivation_prep" / "export_tri_form_runtime.py"
DEFAULT_RELEASE = PACKAGE / "release" / "benchmarkv4-r46"
DEFAULT_BASE_URL = "https://www.cun.ai/v1"
DEFAULT_API_KEY_ENV = "VAEVAS_API_KEY"
DIRECT_PARSER_VERSION = "v4-exact-artifact-envelope-parser-v1"
ARTIFACT_RE = re.compile(
    r'(?m)^<<<VABENCH_ARTIFACT path="([^"\r\n]+)">>>\r?\n'
    r'(.*?)'
    r'\r?\n<<<END_VABENCH_ARTIFACT>>>(?=\r?$)',
    re.DOTALL,
)
RELAXED_ARTIFACT_RE = re.compile(
    r'<<<VABENCH_ARTIFACT\s+path="([^"]+)">{2,3}\s*(.*?)\s*<<<END_VABENCH_ARTIFACT>{2,3}',
    re.DOTALL,
)
INPUT_ARTIFACT_RE = re.compile(
    r'<<<VABENCH_INPUT_ARTIFACT\s+path="([^"]+)">{2,3}\s*(.*?)\s*<<<END_VABENCH_ARTIFACT>{2,3}',
    re.DOTALL,
)
FILENAME_ARTIFACT_RE = re.compile(
    r"<<<\s*([A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*\.(?:va|scs))\s*>>>\s*(.*?)\s*<<<END_VABENCH_ARTIFACT>{2,3}",
    re.DOTALL | re.IGNORECASE,
)
FENCED_BLOCK_RE = re.compile(
    r"```(?:verilog-a|veriloga|verilog|spectre|scs)?\s*(.*?)```",
    re.DOTALL | re.IGNORECASE,
)
FILENAME_TOKEN_RE = re.compile(
    r"(?<![\w./-])([A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*\.(?:va|scs))(?![\w./-])",
    re.IGNORECASE,
)
AGENTIC = {"G2", "G3", "G4", "G5"}
FEEDBACK_SIGNAL_PREFIXES = (
    "FEEDBACK_",
    "reference:",
    "negative_",
    "security:",
    "ERROR:",
    "WARNING:",
    "Traceback",
)
PROMPT_EMBEDDED_TASK_FILES = {
    "task/instruction.md",
    "task/solver_contract.json",
    "task/public_contract.json",
}
PUBLIC_INCLUDE_RE = re.compile(
    r"\b(?:ahdl_include|include)\s+[\"']([^\"']+)[\"']", re.IGNORECASE
)
PUBLIC_ESCAPE_RE = re.compile(
    r"\b(?:shell|system|exec|spawn|unix|socket|tcp|udp|https?|ftp|curl|wget|ocean|skill|ipcBeginProcess)\b",
    re.IGNORECASE,
)


class AgentTimeoutError(TimeoutError):
    """The model endpoint exhausted the per-request wall-clock allowance."""


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def file_digest_summary(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    return {
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def read_tool_delivery_cache(runtime: Path) -> set[str]:
    path = runtime / "evidence" / "tool_delivery_cache.json"
    if not path.is_file():
        return set()
    try:
        payload = read_json(path)
    except (OSError, json.JSONDecodeError):
        return set()
    return {str(item) for item in payload.get("full_read_files") or []}


def write_tool_delivery_cache(runtime: Path, delivered: set[str]) -> None:
    write_json(runtime / "evidence" / "tool_delivery_cache.json", {
        "schema_version": "v4-tool-delivery-cache-v1",
        "full_read_files": sorted(delivered),
    })


def reference_tokens(text: str) -> int:
    return len(re.findall(r"[\w]+|[^\s\w]", text, flags=re.UNICODE))


def provider_output_usage(
    usage: dict[str, Any] | None,
    visible_text: str,
    *,
    reasoning_text: str = "",
    tool_text: str = "",
) -> dict[str, Any]:
    usage = usage or {}
    completion = usage.get("completion_tokens")
    details = usage.get("completion_tokens_details") or {}
    reasoning = details.get("reasoning_tokens", usage.get("reasoning_tokens", 0))
    if isinstance(completion, int) and completion >= 0:
        reasoning_tokens = int(reasoning) if isinstance(reasoning, int) else 0
        return {
            "output_tokens": completion,
            "reasoning_tokens": reasoning_tokens,
            "visible_tokens": max(0, completion - reasoning_tokens),
            "source": "provider_usage",
        }
    visible_estimate = reference_tokens(visible_text + tool_text)
    reasoning_estimate = reference_tokens(reasoning_text)
    return {
        "output_tokens": visible_estimate + reasoning_estimate,
        "reasoning_tokens": reasoning_estimate,
        "visible_tokens": visible_estimate,
        "source": "reference_estimate",
    }


def provider_response_metadata(response: dict[str, Any]) -> dict[str, Any]:
    """Keep stable audit fields without persisting the full provider response."""
    return {
        "response_id": response.get("id"),
        "model": response.get("model"),
        "created": response.get("created"),
        "system_fingerprint": response.get("system_fingerprint"),
    }


def model_event_hit_limit(event: dict[str, Any]) -> bool:
    if event.get("finish_reason") == "length":
        return True
    requested = event.get("requested_max_tokens")
    generated = event.get("provider_output_tokens")
    return (
        isinstance(requested, int)
        and requested > 0
        and isinstance(generated, int)
        and generated >= requested
    )


def pending_tool_calls(messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return uncheckpointed calls from the most recent assistant tool turn."""
    assistant_index = next(
        (
            index
            for index in range(len(messages) - 1, -1, -1)
            if messages[index].get("role") == "assistant"
        ),
        None,
    )
    if assistant_index is None:
        return []
    calls = list(messages[assistant_index].get("tool_calls") or [])
    handled = {
        str(message.get("tool_call_id"))
        for message in messages[assistant_index + 1:]
        if message.get("role") == "tool"
    }
    return [call for call in calls if str(call.get("id")) not in handled]


def cell_output_budget(cell: dict[str, Any]) -> int:
    value = cell.get("max_output_tokens", cell.get("max_working_tokens"))
    if not isinstance(value, int) or value <= 0:
        raise ValueError(f"invalid output-token budget for {cell.get('cell_id')}: {value!r}")
    return value


def validate_campaign_cells(cells: list[dict[str, Any]], release: Path) -> None:
    mode_specs = read_json(release / "prompt_modes" / "modes.json")["modes"]
    task_rows = read_json(release / "TASK_INDEX.json")["tasks"]
    tasks = {str(row["task_id"]): row for row in task_rows}
    seen: set[str] = set()
    for cell in cells:
        cell_id = str(cell.get("cell_id") or "")
        if not re.fullmatch(r"v4-[0-9]{3,4}-G[0-5]-r[0-9]{2,}", cell_id):
            raise ValueError(f"invalid campaign cell_id: {cell_id!r}")
        if cell_id in seen:
            raise ValueError(f"duplicate campaign cell_id: {cell_id}")
        seen.add(cell_id)

        mode = str(cell.get("mode") or "")
        if mode not in mode_specs:
            raise ValueError(f"unknown campaign mode for {cell_id}: {mode!r}")
        expected_process = str(mode_specs[mode]["process"])
        if cell.get("process") != expected_process:
            raise ValueError(f"campaign process mismatch for {cell_id}")

        task_id = str(cell.get("task_id") or "")
        task = tasks.get(task_id)
        if task is None:
            raise ValueError(f"unknown campaign task for {cell_id}: {task_id!r}")
        if str(cell.get("family_id")) != str(task["family_id"]):
            raise ValueError(f"campaign family mismatch for {cell_id}")
        if str(cell.get("form")) != str(task["form"]):
            raise ValueError(f"campaign form mismatch for {cell_id}")
        cell_output_budget(cell)


def safe_relative(raw: str) -> Path:
    path = Path(raw.replace("\\", "/"))
    if not path.parts or path.is_absolute() or ".." in path.parts:
        raise ValueError(f"unsafe relative path: {raw!r}")
    return path


def submission_relative(raw: str) -> Path:
    """Normalize the public path spellings exposed by the agent prompt and tools."""
    path = safe_relative(raw)
    if path.parts[:2] == ("public", "submission"):
        path = Path(*path.parts[2:])
    elif path.parts[0] == "submission":
        path = Path(*path.parts[1:])
    if not path.parts:
        raise ValueError(f"submission path names no artifact: {raw!r}")
    return path


def load_key(path: str | None, env_name: str) -> str:
    value = os.environ.get(env_name, "").strip()
    if value:
        return value
    if path:
        value = Path(path).expanduser().read_text(encoding="utf-8").strip()
        if value:
            return value
    raise SystemExit(f"missing credential: set {env_name} or use --api-key-file")


class OpenAICompatible:
    def __init__(
        self,
        *,
        base_url: str,
        model: str,
        api_key: str,
        timeout_s: int,
        temperature: float,
        stream: bool = False,
    ):
        self.endpoint = base_url.rstrip("/")
        if not self.endpoint.endswith("/chat/completions"):
            self.endpoint += "/chat/completions" if self.endpoint.endswith("/v1") else "/v1/chat/completions"
        self.model = model
        self.api_key = api_key
        self.timeout_s = timeout_s
        self.temperature = temperature
        self.stream = stream

    def _redact(self, text: str) -> str:
        return text.replace(self.api_key, "<redacted-provider-credential>") if self.api_key else text

    def complete(self, messages: list[dict[str, Any]], max_tokens: int, tools: list[dict[str, Any]] | None) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": self.temperature,
        }
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"
        if self.stream:
            payload["stream"] = True
            return self._complete_stream(payload)
        completed = None
        for attempt in range(1, 4):
            with tempfile.TemporaryDirectory(prefix="v4_provider_") as td:
                root = Path(td)
                payload_path = root / "payload.json"
                header_path = root / "headers.txt"
                payload_path.write_text(json.dumps(payload), encoding="utf-8")
                header_path.write_text(
                    f"Authorization: Bearer {self.api_key}\nContent-Type: application/json\n",
                    encoding="utf-8",
                )
                header_path.chmod(0o600)
                try:
                    completed = subprocess.run(
                        [
                            "curl", "-sS", "--max-time", str(self.timeout_s),
                            self.endpoint, "-H", f"@{header_path}",
                            "--data-binary", f"@{payload_path}",
                        ],
                        text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                        timeout=self.timeout_s + 5, check=False,
                    )
                except subprocess.TimeoutExpired as exc:
                    raise AgentTimeoutError(
                        f"provider request exceeded {self.timeout_s}s"
                    ) from exc
            if completed.returncode == 0:
                break
            if attempt < 3:
                time.sleep(2 * attempt)
        assert completed is not None
        if completed.returncode == 28:
            raise AgentTimeoutError(
                f"provider request exceeded {self.timeout_s}s after 3 attempts"
            )
        if completed.returncode != 0:
            raise RuntimeError(
                f"provider transport failed after 3 attempts rc={completed.returncode}: "
                f"{self._redact(completed.stderr[-2000:])}"
            )
        try:
            response = json.loads(completed.stdout)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "provider returned non-JSON response "
                f"status=transport_ok stdout_len={len(completed.stdout)} "
                f"stderr_len={len(completed.stderr)} "
                f"stdout_tail={self._redact(completed.stdout[-2000:])!r} "
                f"stderr_tail={self._redact(completed.stderr[-2000:])!r}"
            ) from exc
        if response.get("error"):
            error = self._redact(json.dumps(response["error"])[:2000])
            raise RuntimeError(f"provider error: {error}")
        return response

    def _curl_payload(self, payload: dict[str, Any]) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory(prefix="v4_provider_") as td:
            root = Path(td)
            payload_path = root / "payload.json"
            header_path = root / "headers.txt"
            payload_path.write_text(json.dumps(payload), encoding="utf-8")
            header_path.write_text(
                f"Authorization: Bearer {self.api_key}\nContent-Type: application/json\n",
                encoding="utf-8",
            )
            header_path.chmod(0o600)
            try:
                return subprocess.run(
                    [
                        "curl", "-sS", "--no-buffer", "--max-time", str(self.timeout_s),
                        self.endpoint, "-H", f"@{header_path}",
                        "--data-binary", f"@{payload_path}",
                    ],
                    text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    timeout=self.timeout_s + 5, check=False,
                )
            except subprocess.TimeoutExpired as exc:
                raise AgentTimeoutError(
                    f"provider streaming request exceeded {self.timeout_s}s"
                ) from exc

    def _complete_stream(self, payload: dict[str, Any]) -> dict[str, Any]:
        completed = None
        for attempt in range(1, 4):
            completed = self._curl_payload(payload)
            if completed.returncode == 0:
                break
            if attempt < 3:
                time.sleep(2 * attempt)
        assert completed is not None
        if completed.returncode == 28:
            raise AgentTimeoutError(
                f"provider streaming request exceeded {self.timeout_s}s after 3 attempts"
            )
        if completed.returncode != 0:
            raise RuntimeError(
                f"provider streaming transport failed after 3 attempts rc={completed.returncode}: "
                f"{self._redact(completed.stderr[-2000:])}"
            )
        try:
            return parse_openai_sse_response(completed.stdout, completed.stderr)
        except RuntimeError as exc:
            raise RuntimeError(self._redact(str(exc))) from None


def parse_openai_sse_response(stdout: str, stderr: str = "") -> dict[str, Any]:
    content_parts: list[str] = []
    reasoning_parts: list[str] = []
    tool_calls_by_index: dict[int, dict[str, Any]] = {}
    finish_reason = None
    usage = None
    metadata: dict[str, Any] = {"object": "chat.completion"}
    chunk_count = 0
    for raw in stdout.splitlines():
        line = raw.strip()
        if not line or line.startswith(":"):
            continue
        if not line.startswith("data:"):
            continue
        data = line.removeprefix("data:").strip()
        if data == "[DONE]":
            continue
        try:
            chunk = json.loads(data)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "provider returned malformed streaming JSON "
                f"stdout_len={len(stdout)} stderr_len={len(stderr)} "
                f"line_tail={line[-1000:]!r} stderr_tail={stderr[-2000:]!r}"
            ) from exc
        chunk_count += 1
        for key in ("id", "model", "created", "system_fingerprint"):
            if chunk.get(key) is not None:
                metadata[key] = chunk.get(key)
        if chunk.get("usage") is not None:
            usage = chunk.get("usage")
        choices = chunk.get("choices") or []
        if not choices:
            continue
        choice = choices[0]
        if choice.get("finish_reason") is not None:
            finish_reason = choice.get("finish_reason")
        delta = choice.get("delta") or {}
        if delta.get("content") is not None:
            content_parts.append(str(delta.get("content") or ""))
        if delta.get("reasoning_content") is not None:
            reasoning_parts.append(str(delta.get("reasoning_content") or ""))
        for tool_delta in delta.get("tool_calls") or []:
            index = int(tool_delta.get("index", 0))
            call = tool_calls_by_index.setdefault(
                index,
                {"id": "", "type": "function", "function": {"name": "", "arguments": ""}},
            )
            if tool_delta.get("id"):
                call["id"] = str(tool_delta["id"])
            if tool_delta.get("type"):
                call["type"] = str(tool_delta["type"])
            function_delta = tool_delta.get("function") or {}
            if function_delta.get("name") is not None:
                call["function"]["name"] += str(function_delta.get("name") or "")
            if function_delta.get("arguments") is not None:
                call["function"]["arguments"] += str(function_delta.get("arguments") or "")
    if chunk_count == 0:
        raise RuntimeError(
            "provider returned empty streaming response "
            f"stdout_len={len(stdout)} stderr_len={len(stderr)} stdout_tail={stdout[-2000:]!r} "
            f"stderr_tail={stderr[-2000:]!r}"
        )
    message: dict[str, Any] = {
        "role": "assistant",
        "content": "".join(content_parts),
    }
    if reasoning_parts:
        message["reasoning_content"] = "".join(reasoning_parts)
    tool_calls = [tool_calls_by_index[index] for index in sorted(tool_calls_by_index)]
    if tool_calls:
        message["tool_calls"] = tool_calls
    response = {
        **metadata,
        "choices": [{"index": 0, "message": message, "finish_reason": finish_reason}],
        "usage": usage,
        "streaming_chunk_count": chunk_count,
    }
    return response


TOOLS = [
    {"type": "function", "function": {"name": "list_files", "description": "List readable task files and writable submission files.", "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {"name": "read_file", "description": "Read a public task or submission text file.", "parameters": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}}},
    {"type": "function", "function": {"name": "write_file", "description": "Create or replace a submission file.", "parameters": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}}, "required": ["path", "content"]}}},
    {"type": "function", "function": {"name": "run_evas", "description": "Run EVAS against the task-local visible test. Testbench tasks require one public case name from evas_runtime.json.", "parameters": {"type": "object", "properties": {"case": {"type": "string"}}, "additionalProperties": False}}},
    {"type": "function", "function": {"name": "finalize", "description": "Finalize the current submission.", "parameters": {"type": "object", "properties": {}}}},
]


def command_result(
    command: str,
    runtime: Path,
    timeout_s: int,
    submission_dir: Path | None = None,
) -> dict[str, Any]:
    effective_submission = submission_dir or runtime / "public" / "submission"
    env = os.environ.copy()
    env.update({
        "VABENCH_RUNTIME_DIR": str(runtime),
        "VABENCH_PUBLIC_DIR": str(runtime / "public"),
        "VABENCH_SUBMISSION_DIR": str(effective_submission),
        "VABENCH_FINAL_SUBMISSION_DIR": str(effective_submission),
        "VABENCH_EVALUATOR_DIR": str(runtime / "evaluator"),
        "VABENCH_TRUSTED_REPLAY_RESULT": str(
            runtime / "evidence" / "trusted_replay_result.json"
        ),
    })
    started = time.monotonic()
    try:
        completed = subprocess.run(
            shlex.split(command), cwd=REPO, env=env, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout_s, check=False,
        )
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout.decode(errors="replace") if isinstance(exc.stdout, bytes) else exc.stdout
        stderr = exc.stderr.decode(errors="replace") if isinstance(exc.stderr, bytes) else exc.stderr
        return {
            "execution_status": "timeout",
            "returncode": None,
            "stdout": (stdout or "")[-12000:],
            "stderr": (stderr or "")[-4000:],
            "elapsed_s": time.monotonic() - started,
        }
    except OSError as exc:
        return {
            "execution_status": "launch_error",
            "returncode": None,
            "stdout": "",
            "stderr": str(exc)[:4000],
            "elapsed_s": time.monotonic() - started,
        }
    return {
        "execution_status": "completed",
        "returncode": completed.returncode,
        "stdout": completed.stdout[-12000:],
        "stderr": completed.stderr[-4000:],
        "elapsed_s": time.monotonic() - started,
    }


def argv_result(argv: list[str], runtime: Path, timeout_s: int) -> dict[str, Any]:
    """Run one operator-selected executable with benchmark-controlled arguments."""
    started = time.monotonic()
    try:
        completed = subprocess.run(
            argv,
            cwd=runtime,
            env=os.environ.copy(),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout_s,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout.decode(errors="replace") if isinstance(exc.stdout, bytes) else exc.stdout
        stderr = exc.stderr.decode(errors="replace") if isinstance(exc.stderr, bytes) else exc.stderr
        return {
            "execution_status": "timeout",
            "returncode": None,
            "stdout": (stdout or "")[-12000:],
            "stderr": (stderr or "")[-4000:],
            "elapsed_s": time.monotonic() - started,
        }
    except OSError as exc:
        return {
            "execution_status": "launch_error",
            "returncode": None,
            "stdout": "",
            "stderr": str(exc)[:4000],
            "elapsed_s": time.monotonic() - started,
        }
    return {
        "execution_status": "completed",
        "returncode": completed.returncode,
        "stdout": completed.stdout[-12000:],
        "stderr": completed.stderr[-4000:],
        "elapsed_s": time.monotonic() - started,
    }


def confined_path(root: Path, relative: str) -> Path:
    path = root / safe_relative(relative)
    path.resolve().relative_to(root.resolve())
    return path


def validate_public_testbench(candidate: Path) -> None:
    if candidate.is_symlink() or candidate.stat().st_size > 1_000_000:
        raise ValueError("candidate testbench must be a regular file no larger than 1 MB")
    text = candidate.read_text(encoding="utf-8")
    uncommented = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
    uncommented = "\n".join(line.split("//", 1)[0] for line in uncommented.splitlines())
    if PUBLIC_ESCAPE_RE.search(uncommented):
        raise ValueError("candidate testbench contains a forbidden process or network escape")
    includes = PUBLIC_INCLUDE_RE.findall(uncommented)
    if not includes:
        raise ValueError("candidate testbench must include its public DUT fixture")
    for raw in includes:
        include = Path(raw.replace("\\", "/"))
        if include.is_absolute() or ".." in include.parts:
            raise ValueError("candidate testbench include escapes the public DUT fixture")
        if not include.parts or include.parts[0] != "dut":
            raise ValueError("candidate testbench includes must remain below ./dut")


def run_public_evas(
    runtime: Path,
    arguments: dict[str, Any],
    timeout_s: int,
    evas_command: str,
) -> dict[str, Any]:
    """Execute only the fixed public EVAS contract, never an agent-supplied command."""
    public = runtime / "public"
    task = public / "task"
    submission = public / "submission"
    contract_path = task / "evas_runtime.json"
    if not contract_path.is_file():
        return {"status": "unavailable", "reason": "public EVAS runtime contract is missing"}
    contract = read_json(contract_path)
    if contract.get("working_directory") != "runtime_package_root":
        raise ValueError("unsupported EVAS working directory")
    executable = shlex.split(evas_command)
    if not executable:
        raise ValueError("empty EVAS executable command")

    schema_version = str(contract.get("schema_version") or "")
    requested_case = arguments.get("case")
    if schema_version == "r45-direct-evas-runtime-v1":
        if requested_case not in (None, ""):
            raise ValueError("DUT and bugfix visible tests do not accept a case")
        if contract.get("command") != (
            "evas simulate public/task/visible_test.scs -o "
            "public/submission/evas-output --spectre-strict"
        ):
            raise ValueError("unrecognized public EVAS command contract")
        deck = confined_path(runtime, "public/task/visible_test.scs")
        output = confined_path(submission, "evas-output")
        if not deck.is_file():
            raise FileNotFoundError("visible_test.scs is missing")
        argv = [*executable, "simulate", str(deck), "-o", str(output), "--spectre-strict"]
        result = argv_result(argv, runtime, timeout_s)
        result.update({
            "status": "pass" if result.get("returncode") == 0 else "fail",
            "case": None,
            "test": "public/task/visible_test.scs",
        })
        return result

    if schema_version != "r45-direct-evas-testbench-suite-v1":
        raise ValueError(f"unsupported public EVAS runtime schema: {schema_version!r}")
    if contract.get("fixture_policy") != "read_only_and_identical_for_visible_and_final_replay":
        raise ValueError("unsupported public fixture policy")
    if contract.get("candidate") != "public/submission/testbench.scs":
        raise ValueError("unrecognized testbench candidate path")
    case = str(requested_case or "")
    cases = {
        str(row.get("case")): str(row.get("dut_root"))
        for row in contract.get("cases") or []
        if isinstance(row, dict)
    }
    expected_cases = {"reference", *(f"mutation_{index:02d}" for index in range(1, 6))}
    if set(cases) != expected_cases:
        raise ValueError("public EVAS testbench suite must contain reference plus five mutations")
    if case not in cases:
        raise ValueError(f"unknown public EVAS case: {case!r}; choose one of {sorted(cases)}")
    if not re.fullmatch(r"reference|mutation_0[1-5]", case):
        raise ValueError("public EVAS case name is outside the fixed suite")
    candidate = confined_path(submission, "testbench.scs")
    if not candidate.is_file():
        raise FileNotFoundError("submission/testbench.scs is missing")
    validate_public_testbench(candidate)
    fixture = confined_path(task, cases[case])
    fixture.resolve().relative_to((task / "visible_fixtures").resolve())
    if not fixture.is_dir():
        raise FileNotFoundError(f"public fixture is missing for {case}")

    run_dir = confined_path(submission, f"runs/{case}")
    if run_dir.exists():
        shutil.rmtree(run_dir)
    run_dir.mkdir(parents=True)
    shutil.copy2(candidate, run_dir / "testbench.scs")
    shutil.copytree(fixture, run_dir / "dut")
    output = confined_path(submission, f"evas-output/{case}")
    argv = [
        *executable,
        "simulate",
        str(run_dir / "testbench.scs"),
        "-o",
        str(output),
        "--spectre-strict",
    ]
    result = argv_result(argv, runtime, timeout_s)
    result.update({
        "status": "pass" if result.get("returncode") == 0 else "fail",
        "case": case,
        "test": f"submission/runs/{case}/testbench.scs",
    })
    return result


def load_trusted_replay_adapter_result(runtime: Path) -> dict[str, Any] | None:
    path = runtime / "evidence" / "trusted_replay_result.json"
    if not path.is_file():
        return None
    try:
        value = read_json(path)
    except (OSError, json.JSONDecodeError):
        return {"status": "infrastructure_failure", "diagnostics": ["invalid_result_json"]}
    if not isinstance(value, dict):
        return {
            "status": "infrastructure_failure",
            "diagnostics": ["trusted_replay_result_must_be_an_object"],
        }
    return value


def run_trusted_replay(
    runtime: Path,
    command: str | None,
    timeout_s: int,
    evas_command: str,
    final_submission: dict[str, Any] | None = None,
) -> dict[str, Any]:
    result_path = runtime / "evidence" / "trusted_replay_result.json"
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.unlink(missing_ok=True)
    test_manifest = RESULT_PROTOCOL.hash_test_tree(runtime / "evaluator")
    identity = RESULT_PROTOCOL.evas_identity(shlex.split(evas_command))
    submission_dir = runtime / "evidence" / "final_submission"
    command_record = (
        command_result(command, runtime, timeout_s, submission_dir) if command else None
    )
    adapter_result = load_trusted_replay_adapter_result(runtime) if command else None
    return RESULT_PROTOCOL.trusted_replay(
        command_record,
        adapter_result,
        test_manifest,
        identity,
        (final_submission or {}).get("tree_sha256"),
    )


def attach_experiment_result(
    result: dict[str, Any],
    runtime: Path,
    messages: list[dict[str, Any]],
    args: argparse.Namespace,
    model_status: str,
) -> None:
    gate = submission_artifact_gate(runtime)
    final_submission = RESULT_PROTOCOL.snapshot_submission(runtime, gate)
    replay = run_trusted_replay(
        runtime,
        args.final_judge_command if gate["passed"] else None,
        args.judge_timeout_s,
        args.evas_command,
        final_submission,
    )
    result["experiment_result"] = RESULT_PROTOCOL.build_experiment_result(
        cell=result.get("cell") or {},
        model_status=model_status,
        messages=messages,
        artifact_gate=gate,
        runtime=runtime,
        replay=replay,
        final_submission=final_submission,
    )
    if replay.get("command") is not None:
        result["final_judge"] = replay["command"]


def compact_text_lines(text: str, *, limit: int = 24) -> list[str]:
    """Keep high-signal feedback lines without echoing simulator counters.

    Feedback stdout can include thousands of low-level simulator timing and
    instrumentation lines.  Returning all of that to the model repeatedly burns
    the working-token budget without materially improving repairs.  Keep the
    public oracle summaries, validation diagnostics, and concrete errors.
    """
    semantic: list[str] = []
    errors: list[str] = []
    markers: list[str] = []
    seen: set[str] = set()
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line in seen:
            continue
        seen.add(line)
        lowered = line.lower()
        clipped = line[:1000]
        if re.fullmatch(r"required_trace_missing_node_count\s*=\s*0", lowered):
            continue
        if (
            re.search(r"\bP_[A-Z0-9_]+\b", line)
            or any(
                token in lowered
                for token in (
                    "mismatch",
                    "expected=",
                    "observed=",
                    "failure_detail=",
                    "failures=",
                    "missing_",
                    "metric_gap=",
                    "tolerance=",
                    "checked=",
                    "coverage=",
                )
            )
            or line.startswith("reference:")
            or re.match(r"negative_[0-9]+:", line)
        ):
            semantic.append(clipped)
        elif (
            "simulation failed" in lowered
            or "failed to compile" in lowered
            or "failed to parse" in lowered
            or "parse error" in lowered
            or "syntax error" in lowered
            or "invalid source" in lowered
            or "missing required" in lowered
            or "timed out" in lowered
            or "rustsimprogram rejection:" in lowered
            or "not_lowered" in lowered
            or re.search(r"\b[A-Za-z_][A-Za-z0-9_]*(?:Error|Exception):", line)
            or re.search(r"(^|\s)(error|fatal|panic|exception)(\s|:|\[)", lowered)
            or any(
                token in lowered
                for token in (
                    "unexpected token",
                    "unknown parameter",
                    "unknown instance",
                    "unsupported construct",
                    "unresolved reference",
                    "no such file",
                )
            )
        ):
            errors.append(clipped)
        elif line.startswith(FEEDBACK_SIGNAL_PREFIXES):
            markers.append(clipped)

    selected: list[str] = []
    for group in (semantic, errors, markers):
        for line in group:
            if line not in selected:
                selected.append(line)
            if len(selected) >= limit:
                return selected
    if selected:
        return selected
    tail = [line.strip() for line in text.splitlines() if line.strip()]
    return [line[:1000] for line in tail[-min(limit, 6):]]


def compact_feedback_result(result: dict[str, Any]) -> dict[str, Any]:
    stdout = str(result.get("stdout") or "")
    stderr = str(result.get("stderr") or "")
    lines = compact_text_lines("\n".join(part for part in (stdout, stderr) if part))
    markers = [line for line in lines if line.startswith("FEEDBACK_")]
    compact: dict[str, Any] = {
        "schema_version": "v4-feedback-tool-result-compact-v1",
        "returncode": result.get("returncode"),
        "elapsed_s": result.get("elapsed_s"),
        "status": "pass" if result.get("returncode") == 0 else "fail",
        "markers": markers[-4:],
        "diagnostics": lines,
        "stdout_chars": len(stdout),
        "stderr_chars": len(stderr),
        "compacted": True,
    }
    if stderr:
        compact["stderr_excerpt"] = compact_text_lines(stderr, limit=12)
    return compact


def execute_tool(
    name: str,
    arguments: dict[str, Any],
    runtime: Path,
    timeout_s: int,
    evas_command: str,
) -> tuple[str, bool]:
    public = runtime / "public"
    submission = public / "submission"
    if name == "list_files":
        rows = []
        for root, label in ((public / "task", "task"), (submission, "submission")):
            rows.extend(f"{label}/{p.relative_to(root).as_posix()}" for p in sorted(root.rglob("*")) if p.is_file())
        return json.dumps({"files": rows}), False
    if name == "read_file":
        relative = safe_relative(str(arguments["path"]))
        if relative.parts[:2] == ("public", "task"):
            relative = Path("task", *relative.parts[2:])
        elif relative.parts[:2] == ("public", "submission"):
            relative = Path("submission", *relative.parts[2:])
        elif relative.parts[0] not in {"task", "submission"}:
            relative = Path("submission") / relative
        path = public / relative
        path.resolve().relative_to(public.resolve())
        relative_key = relative.as_posix()
        if relative_key in PROMPT_EMBEDDED_TASK_FILES:
            summary = file_digest_summary(path)
            return json.dumps({
                "status": "already_in_initial_prompt",
                "path": relative_key,
                "note": (
                    "This immutable task file was included verbatim in the initial prompt; "
                    "use that copy instead of spending another tool-result round on it."
                ),
                **summary,
            }), False
        immutable_task_file = relative.parts[:1] == ("task",)
        if immutable_task_file:
            delivered = read_tool_delivery_cache(runtime)
            if relative_key in delivered:
                summary = file_digest_summary(path)
                return json.dumps({
                    "status": "already_provided_in_this_episode",
                    "path": relative_key,
                    "note": "This read-only task file was already returned earlier in the conversation.",
                    **summary,
                }), False
        text = path.read_text(encoding="utf-8")
        if immutable_task_file:
            delivered = read_tool_delivery_cache(runtime)
            delivered.add(relative_key)
            write_tool_delivery_cache(runtime, delivered)
        return text, False
    if name == "write_file":
        relative = submission_relative(str(arguments["path"]))
        path = submission / relative
        path.resolve().relative_to(submission.resolve())
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(str(arguments["content"]), encoding="utf-8")
        return json.dumps({"written": relative.as_posix(), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}), False
    if name == "run_evas":
        return json.dumps(run_public_evas(runtime, arguments, timeout_s, evas_command)), False
    if name == "finalize":
        return json.dumps({"status": "finalized"}), True
    raise ValueError(f"unknown tool: {name}")


def expected_candidate_artifacts(runtime: Path) -> list[str]:
    policy_path = runtime / "evaluator" / "score_policy.json"
    if not policy_path.is_file():
        return []
    policy = read_json(policy_path)
    return [safe_relative(str(item)).as_posix() for item in policy.get("candidate_artifacts") or []]


def validated_artifact_mapping(
    pairs: list[tuple[str, str]], expected: list[str]
) -> dict[str, str] | None:
    if not pairs or not expected:
        return None
    mapping: dict[str, str] = {}
    expected_set = set(expected)
    for raw, content in pairs:
        try:
            relative = safe_relative(raw).as_posix()
        except ValueError:
            return None
        if relative not in expected_set or relative in mapping:
            return None
        mapping[relative] = content
    return mapping if set(mapping) == expected_set else None


def last_complete_artifact_bundle(
    pairs: list[tuple[str, str]], expected: list[str]
) -> tuple[dict[str, str] | None, bool]:
    """Select the last complete ordered label bundle without reading semantics."""
    expected_set = set(expected)
    current: dict[str, str] = {}
    complete: dict[str, str] | None = None
    saw_restart = False
    for raw, content in pairs:
        try:
            relative = safe_relative(raw).as_posix()
        except ValueError:
            return None, saw_restart
        if relative not in expected_set or not content.strip():
            return None, saw_restart
        if relative in current:
            current = {}
            saw_restart = True
        current[relative] = content
        if set(current) == expected_set:
            if complete is not None:
                saw_restart = True
            complete = dict(current)
            current = {}
    return complete, saw_restart


def exact_envelope_mapping(
    text: str, expected: list[str]
) -> tuple[dict[str, str] | None, list[str]]:
    diagnostics: list[str] = []
    matches = list(ARTIFACT_RE.finditer(text))
    if not matches:
        return None, ["no_exact_artifact_blocks"]

    outside_parts: list[str] = []
    cursor = 0
    for match in matches:
        outside_parts.append(text[cursor:match.start()])
        cursor = match.end()
    outside_parts.append(text[cursor:])
    if any(part.strip() for part in outside_parts):
        diagnostics.append("non_whitespace_outside_artifact_blocks")

    observed: list[str] = []
    mapping: dict[str, str] = {}
    expected_set = set(expected)
    for match in matches:
        raw, content = match.group(1), match.group(2)
        try:
            relative = safe_relative(raw).as_posix()
        except ValueError:
            diagnostics.append(f"unsafe_artifact_path:{raw}")
            continue
        observed.append(relative)
        if raw != relative:
            diagnostics.append(f"noncanonical_artifact_path:{raw}")
        elif relative not in expected_set:
            diagnostics.append(f"undeclared_artifact_path:{relative}")
        elif relative in mapping:
            diagnostics.append(f"duplicate_artifact_path:{relative}")
        else:
            mapping[relative] = content
        if "<<<VABENCH_ARTIFACT" in content or "<<<END_VABENCH_ARTIFACT" in content:
            diagnostics.append(f"ambiguous_artifact_marker:{relative}")

    missing = [relative for relative in expected if relative not in mapping]
    diagnostics.extend(f"missing_artifact_path:{relative}" for relative in missing)
    if observed != expected:
        diagnostics.append("artifact_blocks_not_in_canonical_order")
    if diagnostics:
        return None, diagnostics
    return mapping, []


def artifact_label(line: str, expected: list[str]) -> str | None:
    matches: set[str] = set()
    for token in FILENAME_TOKEN_RE.findall(line):
        try:
            candidate = safe_relative(token).as_posix()
        except ValueError:
            continue
        for item in expected:
            if candidate == item or Path(candidate).name == Path(item).name:
                matches.add(item)
    return next(iter(matches)) if len(matches) == 1 else None


def leading_comment_label(content: str, expected: list[str]) -> tuple[str | None, bool]:
    labels: set[str] = set()
    for line in content.splitlines():
        if not line.strip():
            continue
        if not re.match(r"^\s*//", line):
            break
        label = artifact_label(line, expected)
        if label:
            labels.add(label)
    return (next(iter(labels)), False) if len(labels) == 1 else (None, len(labels) > 1)


def split_labeled_fenced_sections(
    content: str, expected: list[str]
) -> tuple[dict[str, str] | None, bool, bool]:
    lines = content.splitlines()
    labels: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        if not re.match(r"^\s*//", line):
            continue
        label = artifact_label(line, expected)
        if label:
            labels.append((index, label))
    if len(labels) < 2:
        return None, False, bool(labels)
    if any(line.strip() for line in lines[:labels[0][0]]):
        return None, False, True
    pairs: list[tuple[str, str]] = []
    for offset, (start, label) in enumerate(labels):
        stop = labels[offset + 1][0] if offset + 1 < len(labels) else len(lines)
        body = "\n".join(lines[start + 1:stop]).strip()
        if not body:
            return None, False, True
        pairs.append((label, body))
    mapping, restarted = last_complete_artifact_bundle(pairs, expected)
    return mapping, restarted, True


def labeled_fenced_mapping(text: str, expected: list[str]) -> tuple[dict[str, str] | None, str]:
    blocks = list(FENCED_BLOCK_RE.finditer(text))
    if len(blocks) == 1:
        sections, restarted, saw_sections = split_labeled_fenced_sections(
            blocks[0].group(1), expected
        )
        if sections is not None:
            protocol = "last_complete_labeled_bundle" if restarted else "labeled_sections_in_fenced_block"
            return sections, protocol
        if saw_sections:
            return None, "incomplete_labeled_bundle"

    pairs: list[tuple[str, str]] = []
    previous_end = 0
    for block in blocks:
        content = block.group(1)
        prefix_lines = [line for line in text[previous_end:block.start()].splitlines() if line.strip()]
        prefix_label = artifact_label(prefix_lines[-1], expected) if prefix_lines else None
        inline_label, inline_ambiguous = leading_comment_label(content, expected)
        if inline_ambiguous:
            return None, "ambiguous_labeled_artifacts"
        labels = {label for label in (prefix_label, inline_label) if label}
        if len(labels) != 1:
            return None, "ambiguous_labeled_artifacts" if labels else "unparsed"
        label = next(iter(labels))
        if not content.strip():
            return None, "unparsed"
        pairs.append((label, content))
        previous_end = block.end()
    mapping, restarted = last_complete_artifact_bundle(pairs, expected)
    if mapping is not None:
        protocol = "last_complete_labeled_bundle" if restarted else "labeled_fenced_blocks"
        return mapping, protocol
    return None, "incomplete_labeled_bundle" if pairs else "unparsed"


def write_artifact_mapping(mapping: dict[str, str], runtime: Path) -> list[str]:
    submission = runtime / "public" / "submission"
    saved: list[str] = []
    for relative in sorted(mapping):
        path = submission / relative
        path.resolve().relative_to(submission.resolve())
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(mapping[relative], encoding="utf-8")
        saved.append(relative)
    return saved


def parse_direct_artifacts_detailed(
    text: str, runtime: Path
) -> tuple[dict[str, str] | None, str, list[str]]:
    expected = expected_candidate_artifacts(runtime)
    if not expected:
        return None, "invalid_exact_artifact_envelope", ["missing_candidate_artifact_contract"]

    mapping, diagnostics = exact_envelope_mapping(text, expected)
    if mapping is None:
        return None, "invalid_exact_artifact_envelope", diagnostics
    return mapping, "exact_artifact_envelope", []


def parse_direct_artifacts(text: str, runtime: Path) -> tuple[dict[str, str] | None, str]:
    mapping, protocol, _diagnostics = parse_direct_artifacts_detailed(text, runtime)
    return mapping, protocol


def parse_recoverable_direct_artifacts(
    text: str, runtime: Path
) -> tuple[dict[str, str] | None, str]:
    """Classify deterministic historical recoveries without changing live scoring."""
    expected = expected_candidate_artifacts(runtime)
    if not expected:
        return None, "missing_candidate_artifact_contract"

    mapping, protocol = parse_direct_artifacts(text, runtime)
    if mapping is None:
        exact_pairs = ARTIFACT_RE.findall(text)
        mapping, restarted = last_complete_artifact_bundle(exact_pairs, expected)
        if mapping is not None:
            protocol = "last_complete_labeled_bundle" if restarted else "noncanonical_artifact_envelope"
    if mapping is None:
        mapping, restarted = last_complete_artifact_bundle(
            RELAXED_ARTIFACT_RE.findall(text), expected
        )
        if mapping is not None:
            protocol = "last_complete_labeled_bundle" if restarted else "normalized_artifact_envelope"
    if mapping is None and len(expected) == 1:
        mapping, restarted = last_complete_artifact_bundle(
            FILENAME_ARTIFACT_RE.findall(text), expected
        )
        if mapping is not None:
            protocol = "last_complete_labeled_bundle" if restarted else "normalized_filename_artifact_envelope"
    if mapping is None and len(expected) == 1:
        mapping, restarted = last_complete_artifact_bundle(
            INPUT_ARTIFACT_RE.findall(text), expected
        )
        if mapping is not None:
            protocol = "last_complete_labeled_bundle" if restarted else "normalized_input_artifact_envelope"
    if mapping is None:
        mapping, protocol = labeled_fenced_mapping(text, expected)
    if mapping is None:
        blocks = FENCED_BLOCK_RE.findall(text)
        if len(expected) == 1 and len(blocks) == 1:
            mapping = {expected[0]: blocks[0]}
            protocol = "single_artifact_fenced_block"
    if mapping is None:
        return None, protocol
    return mapping, protocol


def extract_direct_with_protocol(text: str, runtime: Path) -> tuple[list[str], str]:
    mapping, protocol, _diagnostics = parse_direct_artifacts_detailed(text, runtime)
    if mapping is None:
        return [], protocol
    return write_artifact_mapping(mapping, runtime), protocol


def extract_recoverable_direct_with_protocol(
    text: str, runtime: Path
) -> tuple[list[str], str]:
    mapping, protocol = parse_recoverable_direct_artifacts(text, runtime)
    if mapping is None:
        return [], protocol
    return write_artifact_mapping(mapping, runtime), protocol


def direct_protocol_compliant(protocol: str) -> bool:
    return protocol == "exact_artifact_envelope"


def extract_direct(text: str, runtime: Path) -> list[str]:
    return extract_direct_with_protocol(text, runtime)[0]


def submission_artifact_gate(runtime: Path) -> dict[str, Any]:
    expected = expected_candidate_artifacts(runtime)
    expected_set = set(expected)
    submission = runtime / "public" / "submission"
    diagnostics: list[str] = []
    actual: set[str] = set()
    allowed_directories: set[str] = set()
    for raw in expected:
        parent = Path(raw).parent
        while parent != Path("."):
            allowed_directories.add(parent.as_posix())
            parent = parent.parent

    if not expected:
        diagnostics.append("missing_candidate_artifact_contract")
    if len(expected_set) != len(expected):
        diagnostics.append("duplicate_candidate_artifact_contract")
    if not submission.is_dir():
        diagnostics.append("missing_submission_directory")
    else:
        for path in sorted(submission.rglob("*")):
            relative = path.relative_to(submission).as_posix()
            if path.is_symlink():
                diagnostics.append(f"symlink_not_allowed:{relative}")
            elif path.is_file():
                actual.add(relative)
            elif path.is_dir():
                if relative not in allowed_directories:
                    diagnostics.append(f"undeclared_directory:{relative}")
            else:
                diagnostics.append(f"non_regular_artifact:{relative}")

    diagnostics.extend(
        f"missing_artifact_path:{relative}" for relative in sorted(expected_set - actual)
    )
    diagnostics.extend(
        f"undeclared_artifact_path:{relative}" for relative in sorted(actual - expected_set)
    )
    passed = not diagnostics
    artifacts = {
        relative: hashlib.sha256((submission / relative).read_bytes()).hexdigest()
        for relative in expected
        if passed
    }
    return {
        "schema_version": "v4-submission-artifact-gate-v1",
        "passed": passed,
        "expected_artifacts": expected,
        "observed_artifacts": sorted(actual),
        "artifact_sha256": artifacts,
        "diagnostics": diagnostics,
    }


def submission_complete(runtime: Path) -> bool:
    return bool(submission_artifact_gate(runtime)["passed"])


def extract_direct_submission(text: str, runtime: Path) -> dict[str, Any]:
    mapping, protocol, diagnostics = parse_direct_artifacts_detailed(text, runtime)
    saved = write_artifact_mapping(mapping, runtime) if mapping is not None else []
    gate = submission_artifact_gate(runtime) if mapping is not None else None
    compliant = bool(mapping is not None and gate and gate["passed"])
    return {
        "saved_files": saved,
        "extraction_protocol": protocol,
        "submission_protocol_compliant": compliant,
        "response_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "response_parser_version": DIRECT_PARSER_VERSION,
        "parse_diagnostics": diagnostics,
        "artifact_gate": gate,
        "artifact_sha256": dict((gate or {}).get("artifact_sha256") or {}),
    }


def gate_agentic_submission(runtime: Path, result: dict[str, Any]) -> bool:
    gate = submission_artifact_gate(runtime)
    result["artifact_gate"] = gate
    result["artifact_sha256"] = gate["artifact_sha256"]
    result["submission_protocol_compliant"] = bool(gate["passed"])
    return bool(gate["passed"])


def export_runtime(cell: dict[str, Any], release: Path, output: Path) -> None:
    subprocess.run([
        sys.executable, str(EXPORTER), "--release", str(release), "--task", cell["task_id"],
        "--mode", cell["mode"], "--output", str(output), "--working-token-budget",
        str(cell_output_budget(cell)), "--force",
    ], cwd=REPO, check=True, stdout=subprocess.DEVNULL)


def run_cell(cell: dict[str, Any], args: argparse.Namespace, client: OpenAICompatible | None) -> dict[str, Any]:
    runtime = args.output / cell["cell_id"]
    result_path = runtime / "evidence" / "campaign_result.json"
    if args.resume and result_path.is_file():
        previous = read_json(result_path)
        if previous.get("status") in {
            "submitted", "submitted_at_budget", "invalid_submission", "budget_exhausted"
        }:
            if "experiment_result" not in previous:
                checkpoint_path = runtime / "evidence" / "conversation_checkpoint.json"
                checkpoint = read_json(checkpoint_path) if checkpoint_path.is_file() else {}
                attach_experiment_result(
                    previous, runtime, list(checkpoint.get("messages") or []), args, "completed"
                )
                write_json(result_path, previous)
            return previous
    conversation_path = runtime / "evidence" / "conversation_checkpoint.json"
    if not (args.resume and conversation_path.is_file()):
        export_runtime(cell, args.release, runtime)
    prompt_path = runtime / ("agent_prompt.txt" if cell["mode"] in AGENTIC else "direct_prompt.txt")
    prompt = prompt_path.read_text(encoding="utf-8")
    result: dict[str, Any] = {"cell": cell, "started_at": now(), "runtime": str(runtime), "status": "prepared"}
    if args.dry_run:
        result["finished_at"] = now()
        write_json(runtime / "evidence" / "campaign_result.json", result)
        return result
    assert client is not None
    if args.resume and conversation_path.is_file():
        checkpoint = read_json(conversation_path)
        if checkpoint.get("cell_id") != cell["cell_id"]:
            raise ValueError("conversation checkpoint cell_id does not match the campaign cell")
        result["started_at"] = str(checkpoint.get("started_at") or result["started_at"])
        messages = list(checkpoint["messages"])
        output_tokens = int(checkpoint.get("output_tokens", checkpoint.get("working_tokens", 0)))
        events = list(checkpoint["events"])
        finalized = bool(checkpoint.get("finalized"))
    else:
        messages = [{"role": "user", "content": prompt}]
        output_tokens = 0
        events = []
        finalized = False

    output_budget = cell_output_budget(cell)

    def save_conversation() -> None:
        write_json(conversation_path, {
            "schema_version": "v4-calibration-conversation-checkpoint-v1",
            "cell_id": cell["cell_id"], "messages": messages,
            "started_at": result["started_at"],
            "output_tokens": output_tokens, "working_tokens": output_tokens, "events": events,
            "finalized": finalized, "updated_at": now(),
        })

    def current_turn_hit_limit() -> bool:
        last_model = next(
            (event for event in reversed(events) if event.get("type") == "model"),
            {},
        )
        return model_event_hit_limit(last_model) or output_tokens >= output_budget

    def process_tool_calls(calls: list[dict[str, Any]]) -> None:
        nonlocal finalized
        for call in calls:
            function = call["function"]
            try:
                arguments = json.loads(function.get("arguments") or "{}")
                text, done = execute_tool(
                    function["name"],
                    arguments,
                    runtime,
                    args.tool_timeout_s,
                    args.evas_command,
                )
            except Exception as exc:  # Model tool mistakes are episode evidence, not runner failures.
                text = json.dumps({
                    "status": "tool_error",
                    "tool": function.get("name"),
                    "error_type": type(exc).__name__,
                    "error": str(exc)[:2000],
                })
                done = False
            delivered = reference_tokens(text)
            events.append({"type": "tool", "name": function["name"], "reference_tokens": delivered})
            write_json(runtime / "evidence" / "campaign_checkpoint.json", {
                "cell_id": cell["cell_id"], "output_tokens": output_tokens,
                "working_tokens": output_tokens,
                "event_count": len(events), "events": events, "updated_at": now(),
            })
            messages.append({"role": "tool", "tool_call_id": call["id"], "content": text})
            finalized = finalized or done
            save_conversation()

    if cell["mode"] not in AGENTIC and len(messages) > 1:
        content = str(messages[-1].get("content") or "")
        direct_submission = extract_direct_submission(content, runtime)
        complete = bool(direct_submission["submission_protocol_compliant"])
        result.update({
            "status": (
                "submitted_at_budget" if complete and current_turn_hit_limit()
                else "submitted" if complete
                else "budget_exhausted" if current_turn_hit_limit()
                else "invalid_submission"
            ),
            "finished_at": now(),
            "output_tokens": output_tokens,
            "working_tokens": output_tokens,
            "events": events,
            "recovered_from_checkpoint": True,
            **direct_submission,
        })
        attach_experiment_result(result, runtime, messages, args, "completed")
        write_json(runtime / "evidence" / "campaign_result.json", result)
        return result
    if cell["mode"] in AGENTIC and args.resume:
        pending = pending_tool_calls(messages)
        if pending:
            process_tool_calls(pending)
        elif messages and messages[-1].get("role") == "assistant":
            complete = gate_agentic_submission(runtime, result)
            result["status"] = (
                "submitted_at_budget" if complete and current_turn_hit_limit()
                else "submitted" if complete
                else "budget_exhausted" if current_turn_hit_limit()
                else "invalid_submission"
            )
        if finalized:
            complete = gate_agentic_submission(runtime, result)
            result["status"] = (
                "submitted_at_budget" if complete and current_turn_hit_limit()
                else "submitted" if complete
                else "invalid_submission"
            )
    while output_tokens < output_budget and not finalized and result.get("status") == "prepared":
        remaining = output_budget - output_tokens
        started = time.monotonic()
        response = client.complete(messages, remaining, TOOLS if cell["mode"] in AGENTIC else None)
        response_choice = response["choices"][0]
        choice = response_choice["message"]
        elapsed = time.monotonic() - started
        content = str(choice.get("content") or "")
        reasoning_content = str(choice.get("reasoning_content") or "")
        response_tool_calls = choice.get("tool_calls") or []
        tool_text = json.dumps(response_tool_calls, sort_keys=True) if response_tool_calls else ""
        usage = provider_output_usage(
            response.get("usage"),
            content,
            reasoning_text=reasoning_content,
            tool_text=tool_text,
        )
        output_tokens += int(usage["output_tokens"])
        model_event = {
            "type": "model",
            "elapsed_s": elapsed,
            "requested_max_tokens": remaining,
            "finish_reason": response_choice.get("finish_reason"),
            "provider_output_tokens": usage["output_tokens"],
            "provider_reasoning_tokens": usage["reasoning_tokens"],
            "provider_visible_tokens": usage["visible_tokens"],
            "provider_token_source": usage["source"],
            "reference_tokens": reference_tokens(content),
            "provider_usage": response.get("usage"),
            "provider_response": provider_response_metadata(response),
        }
        events.append(model_event)
        write_json(runtime / "evidence" / "campaign_checkpoint.json", {
            "cell_id": cell["cell_id"], "output_tokens": output_tokens,
            "working_tokens": output_tokens,
            "event_count": len(events), "events": events, "updated_at": now(),
        })
        messages.append(choice)
        save_conversation()
        if cell["mode"] not in AGENTIC:
            direct_submission = extract_direct_submission(content, runtime)
            complete = bool(direct_submission["submission_protocol_compliant"])
            hit_limit = model_event_hit_limit(model_event) or output_tokens >= output_budget
            result.update({
                "status": (
                    "submitted_at_budget" if complete and hit_limit
                    else "submitted" if complete
                    else "budget_exhausted" if hit_limit
                    else "invalid_submission"
                ),
                **direct_submission,
            })
            break
        calls = choice.get("tool_calls") or []
        if not calls:
            hit_limit = model_event_hit_limit(model_event) or output_tokens >= output_budget
            complete = gate_agentic_submission(runtime, result)
            result["status"] = (
                "submitted_at_budget" if complete and hit_limit
                else "submitted" if complete
                else "budget_exhausted" if hit_limit
                else "invalid_submission"
            )
            break
        process_tool_calls(calls)
        if finalized:
            complete = gate_agentic_submission(runtime, result)
            result["status"] = (
                "submitted_at_budget" if complete and current_turn_hit_limit()
                else "submitted" if complete
                else "invalid_submission"
            )
    if result.get("status") == "prepared":
        complete = gate_agentic_submission(runtime, result) if cell["mode"] in AGENTIC else False
        result["status"] = "submitted_at_budget" if complete else "budget_exhausted"
    result.update({
        "finished_at": now(),
        "output_tokens": output_tokens,
        "working_tokens": output_tokens,
        "output_token_budget": output_budget,
        "events": events,
    })
    attach_experiment_result(result, runtime, messages, args, "completed")
    write_json(runtime / "evidence" / "campaign_result.json", result)
    return result


def run_cell_preserving_failure(
    cell: dict[str, Any], args: argparse.Namespace, client: OpenAICompatible | None
) -> dict[str, Any]:
    try:
        return run_cell(cell, args, client)
    except Exception as exc:  # Preserve failed paid episodes for audit and resume diagnosis.
        runtime = args.output / cell["cell_id"]
        error = str(exc)[:4000]
        trace = traceback.format_exc()[-12000:]
        if client is not None:
            error = client._redact(error)
            trace = client._redact(trace)
        failure = {
            "cell": cell,
            "status": "agent_timeout" if isinstance(exc, AgentTimeoutError) else "runner_error",
            "error_type": type(exc).__name__,
            "error": error,
            "traceback": trace,
            "finished_at": now(),
        }
        checkpoint_path = runtime / "evidence" / "conversation_checkpoint.json"
        checkpoint = read_json(checkpoint_path) if checkpoint_path.is_file() else {}
        model_status = (
            "agent_timeout"
            if isinstance(exc, AgentTimeoutError)
            else "provider_failure"
            if isinstance(exc, RuntimeError) and "provider" in str(exc).lower()
            else "runner_failure"
        )
        attach_experiment_result(
            failure, runtime, list(checkpoint.get("messages") or []), args, model_status
        )
        write_json(runtime / "evidence" / "campaign_result.json", failure)
        return failure


def stored_results(output: Path) -> list[dict[str, Any]]:
    return [
        read_json(path)
        for path in sorted(output.glob("v4-*/evidence/campaign_result.json"))
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--campaign", type=Path, required=True)
    parser.add_argument("--release", type=Path, default=DEFAULT_RELEASE)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--api-key-file")
    parser.add_argument("--api-key-env", default=DEFAULT_API_KEY_ENV)
    parser.add_argument("--cell")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--request-timeout-s", type=int, default=600)
    parser.add_argument("--tool-timeout-s", type=int, default=120)
    parser.add_argument("--judge-timeout-s", type=int, default=600)
    parser.add_argument("--final-judge-command")
    parser.add_argument(
        "--evas-command",
        default="evas",
        help="EVAS executable used by the restricted visible-test tool and recorded for trusted replay identity.",
    )
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--stream", action="store_true", help="Use OpenAI-compatible SSE streaming responses.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    args.campaign = args.campaign.resolve()
    args.release = args.release.resolve()
    args.output = args.output.resolve()
    campaign = read_json(args.campaign)
    expected_release_hash = str(campaign.get("release_manifest_sha256") or "")
    observed_release_hash = hashlib.sha256((args.release / "MANIFEST.json").read_bytes()).hexdigest()
    if expected_release_hash != observed_release_hash:
        raise SystemExit(
            "campaign release manifest does not match --release: "
            f"expected={expected_release_hash or '<missing>'} observed={observed_release_hash}"
        )
    cells = list(campaign["cells"])
    validate_campaign_cells(cells, args.release)
    if args.cell:
        cells = [row for row in cells if row["cell_id"] == args.cell]
    if args.limit is not None:
        cells = cells[:args.limit]
    if not cells:
        raise SystemExit("no matching campaign cells")
    if args.workers < 1:
        raise SystemExit("--workers must be at least 1")
    if min(args.request_timeout_s, args.tool_timeout_s, args.judge_timeout_s) < 1:
        raise SystemExit("request, tool, and judge timeouts must be positive")
    key = "" if args.dry_run else load_key(args.api_key_file, args.api_key_env)
    if not args.dry_run:
        os.environ.pop(args.api_key_env, None)
    client = None if args.dry_run else OpenAICompatible(
        base_url=args.base_url, model=campaign["model"], api_key=key,
        timeout_s=args.request_timeout_s, temperature=args.temperature, stream=args.stream,
    )
    args.output.mkdir(parents=True, exist_ok=True)
    if args.workers == 1:
        results = [run_cell_preserving_failure(cell, args, client) for cell in cells]
    else:
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            results = list(pool.map(lambda cell: run_cell_preserving_failure(cell, args, client), cells))
    all_results = stored_results(args.output)
    summary = {"schema_version": "v4-calibration-run-summary-v1", "campaign": str(args.campaign), "dry_run": args.dry_run, "result_count": len(all_results), "statuses": {}}
    for row in all_results:
        status = row["status"]
        summary["statuses"][status] = summary["statuses"].get(status, 0) + 1
    write_json(args.output / "SUMMARY.json", summary)
    print(json.dumps(summary, indent=2))
    return 1 if summary["statuses"].get("runner_error") else 0


if __name__ == "__main__":
    raise SystemExit(main())
