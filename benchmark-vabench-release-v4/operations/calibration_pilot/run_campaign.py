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
from submission_normalization import normalize_submission_layout  # noqa: E402

EXPORTER = PACKAGE / "operations" / "tri_form_derivation_prep" / "export_tri_form_runtime.py"
DEFAULT_RELEASE = PACKAGE / "release" / "tri-form-v4-1200-final"
DEFAULT_BASE_URL = "https://www.cun.ai/v1"
DEFAULT_API_KEY_ENV = "VAEVAS_API_KEY"
ARTIFACT_RE = re.compile(
    r'<<<VABENCH_ARTIFACT\s+path="([^"]+)">>>\s*(.*?)\s*<<<END_VABENCH_ARTIFACT>>>',
    re.DOTALL,
)
RELAXED_ARTIFACT_RE = re.compile(
    r'<<<VABENCH_ARTIFACT\s+path="([^"]+)">{2,3}\s*(.*?)\s*<<<END_VABENCH_ARTIFACT>{2,3}',
    re.DOTALL,
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


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def reference_tokens(text: str) -> int:
    return len(re.findall(r"[\w]+|[^\s\w]", text, flags=re.UNICODE))


def provider_output_usage(usage: dict[str, Any] | None, visible_text: str) -> dict[str, Any]:
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
    estimated = reference_tokens(visible_text)
    return {
        "output_tokens": estimated,
        "reasoning_tokens": 0,
        "visible_tokens": estimated,
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


def cell_output_budget(cell: dict[str, Any]) -> int:
    value = cell.get("max_output_tokens", cell.get("max_working_tokens"))
    if not isinstance(value, int) or value <= 0:
        raise ValueError(f"invalid output-token budget for {cell.get('cell_id')}: {value!r}")
    return value


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
    def __init__(self, *, base_url: str, model: str, api_key: str, timeout_s: int, temperature: float):
        self.endpoint = base_url.rstrip("/")
        if not self.endpoint.endswith("/chat/completions"):
            self.endpoint += "/chat/completions" if self.endpoint.endswith("/v1") else "/v1/chat/completions"
        self.model = model
        self.api_key = api_key
        self.timeout_s = timeout_s
        self.temperature = temperature

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
                completed = subprocess.run(
                    [
                        "curl", "-sS", "--max-time", str(self.timeout_s),
                        self.endpoint, "-H", f"@{header_path}",
                        "--data-binary", f"@{payload_path}",
                    ],
                    text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    timeout=self.timeout_s + 5, check=False,
                )
            if completed.returncode == 0:
                break
            if attempt < 3:
                time.sleep(2 * attempt)
        assert completed is not None
        if completed.returncode != 0:
            raise RuntimeError(
                f"provider transport failed after 3 attempts rc={completed.returncode}: "
                f"{completed.stderr[-2000:]}"
            )
        try:
            response = json.loads(completed.stdout)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "provider returned non-JSON response "
                f"status=transport_ok stdout_len={len(completed.stdout)} "
                f"stderr_len={len(completed.stderr)} "
                f"stdout_tail={completed.stdout[-2000:]!r} "
                f"stderr_tail={completed.stderr[-2000:]!r}"
            ) from exc
        if response.get("error"):
            raise RuntimeError(f"provider error: {json.dumps(response['error'])[:2000]}")
        return response


TOOLS = [
    {"type": "function", "function": {"name": "list_files", "description": "List readable task files and writable submission files.", "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {"name": "read_file", "description": "Read a public task or submission text file.", "parameters": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}}},
    {"type": "function", "function": {"name": "write_file", "description": "Create or replace a submission file.", "parameters": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}}, "required": ["path", "content"]}}},
    {"type": "function", "function": {"name": "feedback", "description": "Run the shared public feedback service on the current submission.", "parameters": {"type": "object", "properties": {"channels": {"type": "array", "items": {"type": "string"}}}}}},
    {"type": "function", "function": {"name": "finalize", "description": "Finalize the current submission.", "parameters": {"type": "object", "properties": {}}}},
]


def command_result(command: str, runtime: Path, timeout_s: int) -> dict[str, Any]:
    env = os.environ.copy()
    env.update({
        "VABENCH_RUNTIME_DIR": str(runtime),
        "VABENCH_PUBLIC_DIR": str(runtime / "public"),
        "VABENCH_SUBMISSION_DIR": str(runtime / "public" / "submission"),
        "VABENCH_EVALUATOR_DIR": str(runtime / "evaluator"),
    })
    started = time.monotonic()
    completed = subprocess.run(
        shlex.split(command), cwd=REPO, env=env, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout_s, check=False,
    )
    return {
        "returncode": completed.returncode,
        "stdout": completed.stdout[-12000:],
        "stderr": completed.stderr[-4000:],
        "elapsed_s": time.monotonic() - started,
    }


def execute_tool(name: str, arguments: dict[str, Any], runtime: Path, feedback_command: str | None, timeout_s: int) -> tuple[str, bool]:
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
        return path.read_text(encoding="utf-8"), False
    if name == "write_file":
        relative = submission_relative(str(arguments["path"]))
        path = submission / relative
        path.resolve().relative_to(submission.resolve())
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(str(arguments["content"]), encoding="utf-8")
        return json.dumps({"written": relative.as_posix(), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}), False
    if name == "feedback":
        if not feedback_command:
            return json.dumps({"status": "unavailable", "reason": "feedback command not configured"}), False
        return json.dumps(command_result(feedback_command, runtime, timeout_s)), False
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


def exact_envelope_mapping(text: str, expected: list[str]) -> dict[str, str] | None:
    matches = list(ARTIFACT_RE.finditer(text))
    mapping = validated_artifact_mapping(
        [(match.group(1), match.group(2)) for match in matches], expected
    )
    if mapping is None:
        return None
    outside = ARTIFACT_RE.sub("", text)
    return mapping if not outside.strip() else None


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
        path.write_text(mapping[relative].rstrip() + "\n", encoding="utf-8")
        saved.append(relative)
    return saved


def parse_direct_artifacts(text: str, runtime: Path) -> tuple[dict[str, str] | None, str]:
    expected = expected_candidate_artifacts(runtime)
    if not expected:
        return None, "missing_candidate_artifact_contract"

    mapping = exact_envelope_mapping(text, expected)
    protocol = "exact_artifact_envelope"
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
    mapping, protocol = parse_direct_artifacts(text, runtime)
    if mapping is None:
        return [], protocol
    return write_artifact_mapping(mapping, runtime), protocol


def direct_protocol_compliant(protocol: str) -> bool:
    return protocol == "exact_artifact_envelope"


def extract_direct(text: str, runtime: Path) -> list[str]:
    return extract_direct_with_protocol(text, runtime)[0]


def submission_complete(runtime: Path) -> bool:
    expected = [Path(item) for item in expected_candidate_artifacts(runtime)]
    submission = runtime / "public" / "submission"
    return bool(expected) and all((submission / path).is_file() for path in expected)


def normalize_agentic_submission(runtime: Path, result: dict[str, Any]) -> bool:
    expected = expected_candidate_artifacts(runtime)
    normalization = normalize_submission_layout(
        runtime / "public" / "submission", expected
    )
    if normalization is not None:
        result["submission_layout_normalization"] = normalization
        result["submission_protocol_compliant"] = False
    complete = submission_complete(runtime)
    if complete and normalization is None:
        result["submission_protocol_compliant"] = True
    return complete


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
            "output_tokens": output_tokens, "working_tokens": output_tokens, "events": events,
            "finalized": finalized, "updated_at": now(),
        })

    if cell["mode"] not in AGENTIC and len(messages) > 1:
        content = str(messages[-1].get("content") or "")
        saved, extraction_protocol = extract_direct_with_protocol(content, runtime)
        result.update({
            "status": "submitted" if saved and submission_complete(runtime) else "invalid_submission",
            "saved_files": saved,
            "extraction_protocol": extraction_protocol,
            "submission_protocol_compliant": direct_protocol_compliant(extraction_protocol),
            "finished_at": now(),
            "output_tokens": output_tokens,
            "working_tokens": output_tokens,
            "events": events,
            "recovered_from_checkpoint": True,
        })
        write_json(runtime / "evidence" / "campaign_result.json", result)
        return result
    while output_tokens < output_budget and not finalized:
        remaining = output_budget - output_tokens
        started = time.monotonic()
        response = client.complete(messages, remaining, TOOLS if cell["mode"] in AGENTIC else None)
        response_choice = response["choices"][0]
        choice = response_choice["message"]
        elapsed = time.monotonic() - started
        content = str(choice.get("content") or "")
        usage = provider_output_usage(response.get("usage"), content)
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
            saved, extraction_protocol = extract_direct_with_protocol(content, runtime)
            hit_limit = model_event_hit_limit(model_event) or output_tokens >= output_budget
            result.update({
                "status": (
                    "submitted_at_budget" if saved and submission_complete(runtime) and hit_limit
                    else "submitted" if saved and submission_complete(runtime)
                    else "budget_exhausted" if hit_limit
                    else "invalid_submission"
                ),
                "saved_files": saved,
                "extraction_protocol": extraction_protocol,
                "submission_protocol_compliant": direct_protocol_compliant(extraction_protocol),
            })
            break
        calls = choice.get("tool_calls") or []
        if not calls:
            hit_limit = model_event_hit_limit(model_event) or output_tokens >= output_budget
            complete = normalize_agentic_submission(runtime, result)
            result["status"] = (
                "submitted_at_budget" if complete and hit_limit
                else "submitted" if complete
                else "budget_exhausted" if hit_limit
                else "invalid_submission"
            )
            break
        for call in calls:
            function = call["function"]
            try:
                arguments = json.loads(function.get("arguments") or "{}")
                text, done = execute_tool(function["name"], arguments, runtime, args.feedback_command, args.tool_timeout_s)
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
        if finalized:
            result["status"] = "submitted" if normalize_agentic_submission(runtime, result) else "invalid_submission"
    if result.get("status") == "prepared":
        complete = normalize_agentic_submission(runtime, result) if cell["mode"] in AGENTIC else submission_complete(runtime)
        result["status"] = "submitted_at_budget" if complete else "budget_exhausted"
    result.update({
        "finished_at": now(),
        "output_tokens": output_tokens,
        "working_tokens": output_tokens,
        "output_token_budget": output_budget,
        "events": events,
    })
    if args.final_judge_command:
        result["final_judge"] = command_result(args.final_judge_command, runtime, args.judge_timeout_s)
    write_json(runtime / "evidence" / "campaign_result.json", result)
    return result


def run_cell_preserving_failure(
    cell: dict[str, Any], args: argparse.Namespace, client: OpenAICompatible | None
) -> dict[str, Any]:
    try:
        return run_cell(cell, args, client)
    except Exception as exc:  # Preserve failed paid episodes for audit and resume diagnosis.
        runtime = args.output / cell["cell_id"]
        failure = {
            "cell": cell,
            "status": "runner_error",
            "error_type": type(exc).__name__,
            "error": str(exc)[:4000],
            "traceback": traceback.format_exc()[-12000:],
            "finished_at": now(),
        }
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
    parser.add_argument("--feedback-command")
    parser.add_argument("--final-judge-command")
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    args.campaign = args.campaign.resolve()
    args.release = args.release.resolve()
    args.output = args.output.resolve()
    campaign = read_json(args.campaign)
    cells = list(campaign["cells"])
    if args.cell:
        cells = [row for row in cells if row["cell_id"] == args.cell]
    if args.limit is not None:
        cells = cells[:args.limit]
    if not cells:
        raise SystemExit("no matching campaign cells")
    if args.workers < 1:
        raise SystemExit("--workers must be at least 1")
    key = "" if args.dry_run else load_key(args.api_key_file, args.api_key_env)
    client = None if args.dry_run else OpenAICompatible(
        base_url=args.base_url, model=campaign["model"], api_key=key,
        timeout_s=args.request_timeout_s, temperature=args.temperature,
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
