#!/usr/bin/env python3
"""Pinned mini-SWE-agent adapter for vaBench bash-only episodes.

The benchmark harness owns task selection, runtime export, scoring, and
telemetry.  This module owns only the model -> bash -> observation loop used
by G2--G5.  Evaluator assets never enter the model-visible shell sandbox.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import secrets
import shlex
import shutil
import subprocess
import time
from types import SimpleNamespace
from typing import Any, Callable


MINI_SWE_AGENT_VERSION = "2.4.5"
MINI_SWE_SCAFFOLD_ID = "mini-swe-agent-2.4.5-vabench-direct-evas-v2"
BASH_TOOL = {
    "type": "function",
    "function": {
        "name": "bash",
        "description": "Execute a bash command in the isolated vaBench public workspace.",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "The bash command to execute."}
            },
            "required": ["command"],
            "additionalProperties": False,
        },
    },
}

SYSTEM_PROMPT = (
    "You are a behavioral Verilog-A engineer operating in an isolated shell. "
    "Use the bash tool to inspect the public task, create or edit only declared "
    "artifacts under public/submission/, invoke the pinned EVAS executable directly "
    "when useful, inspect its public output yourself, and submit."
)

BASH_CONTRACT = r"""
<vabench_bash_contract>
This is an interactive bash-only episode. Every assistant turn must contain at
least one bash tool call.

Workspace:
- public/task/ is read-only public task material.
- public/skill/ is an optional read-only reusable skill/reference tree in skill-enabled modes.
- public/submission/ is the only writable candidate-artifact directory.
- public/evas-output/ is writable simulator scratch and is never scored.
- evaluator, gold implementations, checker source, private mutations, and final
  score cases are not mounted in this shell.

Commands:
- Use ordinary non-interactive shell commands to inspect public/task/ and edit
  public/submission/.
- `evas` is a real, pinned executable in PATH. `evas --help`, pipes, redirection,
  and compound shell commands behave normally.
- Follow public/task/evas_runtime.json and invoke `evas` directly. The sandboxed
  launcher confines its documented `/tmp/vabench-visible/evas-output` destination
  to public/evas-output/; inspect logs and tran.csv there yourself.
- `vabench-submit` is a real command in PATH. Run it after every declared artifact
  is complete. A rejected submission returns diagnostics and the episode continues.

Do not access the network, leave the workspace, create symlinks, or modify public/task/.
</vabench_bash_contract>
""".strip()


class MiniSweAgentUnavailable(RuntimeError):
    """Raised when the pinned mini-SWE-agent package is unavailable or mismatched."""


def load_mini_swe() -> tuple[type, type, type, Callable[..., list[dict[str, Any]]]]:
    # mini-SWE creates its global config directory at import time. Pin it to a
    # benchmark-owned temporary location instead of depending on user config.
    os.environ["MSWEA_SILENT_STARTUP"] = "1"
    os.environ["MSWEA_GLOBAL_CONFIG_DIR"] = "/tmp/vabench-mini-swe-agent"
    try:
        import minisweagent
        from minisweagent.agents.default import DefaultAgent
        from minisweagent.exceptions import FormatError, Submitted
        from minisweagent.models.utils.actions_toolcall import (
            format_toolcall_observation_messages,
        )
    except ImportError as exc:
        raise MiniSweAgentUnavailable(
            "mini-SWE-agent is required for G2-G5; install the pinned agentic extra"
        ) from exc
    if str(minisweagent.__version__) != MINI_SWE_AGENT_VERSION:
        raise MiniSweAgentUnavailable(
            "mini-SWE-agent version mismatch: "
            f"expected={MINI_SWE_AGENT_VERSION} observed={minisweagent.__version__}"
        )
    return DefaultAgent, Submitted, FormatError, format_toolcall_observation_messages


def _json_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _sandbox_profile(
    workspace: Path, extra_read_roots: list[Path] | None = None
) -> str:
    escaped = str(workspace).replace('"', '\\"')
    runtime = str(workspace.parent).replace('"', '\\"')
    home = str(Path.home().resolve()).replace('"', '\\"')
    submission = str(workspace / "submission").replace('"', '\\"')
    temporary = str(workspace / ".tmp").replace('"', '\\"')
    rules = [
        "(version 1)",
        # Recent macOS releases abort some system binaries under a strict
        # file-read allowlist because their runtime dependencies are not a
        # stable public interface. Retain system execution capability, then
        # seal user data, temporary data, and the private runtime explicitly.
        "(allow default)",
        "(deny network*)",
        f'(deny file-read* (subpath "{home}"))',
        '(deny file-read* (subpath "/private/tmp") '
        '(subpath "/private/var/folders"))',
        f'(deny file-read* (subpath "{runtime}"))',
        f'(allow file-read* (subpath "{escaped}"))',
        # Traversal metadata is required for executing a pinned interpreter
        # below denied home/tmp trees. File contents and directory enumeration
        # remain denied outside explicit roots.
        f'(allow file-read-metadata (subpath "{home}") '
        '(subpath "/private/tmp") (subpath "/private/var/folders"))',
        "(deny file-write*)",
        f'(allow file-write* (subpath "{submission}") (subpath "{temporary}") '
        f'(subpath "{escaped}/evas-output") '
        '(literal "/dev/null") (literal "/dev/tty"))',
    ]
    for root in extra_read_roots or []:
        readable = str(root).replace('"', '\\"')
        selector = "literal" if root.is_file() else "subpath"
        rules.insert(-2, f'(allow file-read* ({selector} "{readable}"))')
    return "\n".join(rules)


def _bubblewrap_system_mounts() -> list[str]:
    mounts: list[str] = []
    for raw in ("/usr", "/bin", "/sbin", "/lib", "/lib64"):
        path = Path(raw)
        if path.is_symlink():
            mounts.extend(["--symlink", os.readlink(path), raw])
        elif path.exists():
            mounts.extend(["--ro-bind", raw, raw])
    return mounts


def _bubblewrap_parent_dirs(path: Path) -> list[str]:
    parents: list[Path] = []
    current = path.parent
    while current != current.parent:
        if str(current) in {"/usr", "/bin", "/sbin", "/lib", "/lib64"}:
            break
        parents.append(current)
        current = current.parent
    argv: list[str] = []
    for parent in reversed(parents):
        argv.extend(["--dir", str(parent)])
    return argv


def _bubblewrap_argv(
    executable: str,
    runtime: Path,
    extra_read_roots: list[Path],
    command: str,
) -> list[str]:
    workspace = runtime / "public"
    extra_mounts: list[str] = []
    created: set[str] = set()
    for root in extra_read_roots:
        parent_dirs = _bubblewrap_parent_dirs(root)
        for index in range(0, len(parent_dirs), 2):
            parent_args = parent_dirs[index : index + 2]
            if parent_args[1] not in created:
                extra_mounts.extend(parent_args)
                created.add(parent_args[1])
        extra_mounts.extend(["--ro-bind", str(root), str(root)])
    return [
        executable,
        "--die-with-parent",
        "--new-session",
        "--unshare-user",
        "--unshare-ipc",
        "--unshare-pid",
        "--unshare-net",
        "--unshare-uts",
        "--proc",
        "/proc",
        "--dev",
        "/dev",
        *_bubblewrap_system_mounts(),
        *extra_mounts,
        "--dir",
        "/workspace",
        "--ro-bind",
        str(workspace),
        "/workspace/public",
        "--bind",
        str(workspace / "submission"),
        "/workspace/public/submission",
        "--bind",
        str(workspace / "evas-output"),
        "/workspace/public/evas-output",
        "--bind",
        str(workspace / ".tmp"),
        "/workspace/public/.tmp",
        "--chdir",
        "/workspace/public",
        "--clearenv",
        "--setenv",
        "PATH",
        "/workspace/public/.tools:/usr/bin:/bin:/usr/sbin:/sbin",
        "--setenv",
        "HOME",
        "/workspace/public",
        "--setenv",
        "TMPDIR",
        "/workspace/public/.tmp",
        "--setenv",
        "VABENCH_EVAS_OUTPUT_ROOT",
        "/workspace/public/evas-output",
        "--setenv",
        "VABENCH_SUBMIT_SENTINEL",
        "/workspace/public/.tmp/submission-request",
        "--setenv",
        "LANG",
        "C.UTF-8",
        "--setenv",
        "LC_ALL",
        "C.UTF-8",
        "/bin/bash",
        "-c",
        command,
    ]


@dataclass
class BashEnvironmentConfig:
    cwd: str
    timeout: float
    sandbox_backend: str


class VaBenchBashEnvironment:
    """One bash tool over the model-visible public workspace.

    EVAS and submission are exposed as discoverable shell executables. Commands
    execute in an OS sandbox with no network and no read access to evaluator data.
    """

    def __init__(
        self,
        runtime: Path,
        *,
        timeout_s: float,
        sandbox_backend: str,
        evas_command: str,
        deadline_monotonic: float | None = None,
        submission_gate: Callable[[Path], dict[str, Any]],
    ) -> None:
        self.runtime = runtime.resolve()
        self.workspace = (self.runtime / "public").resolve()
        self.submission_gate = submission_gate
        self.deadline_monotonic = deadline_monotonic
        self.config = BashEnvironmentConfig(
            cwd=str(self.workspace), timeout=float(timeout_s), sandbox_backend=sandbox_backend
        )
        self.workspace.joinpath("submission").mkdir(parents=True, exist_ok=True)
        self.workspace.joinpath("evas-output").mkdir(parents=True, exist_ok=True)
        self.workspace.joinpath(".tmp").mkdir(parents=True, exist_ok=True)
        self.tools_dir = self.workspace / ".tools"
        self.tools_dir.mkdir(parents=True, exist_ok=True)
        public_alias = self.workspace / "public"
        if not public_alias.exists() and not public_alias.is_symlink():
            public_alias.symlink_to(".", target_is_directory=True)
        self.submit_sentinel = self.workspace / ".tmp" / "submission-request"
        self.evas_command = evas_command
        self._evas_telemetry_token = secrets.token_hex(16)
        self.evas_invocations: list[dict[str, Any]] = []
        self._install_shell_tools()
        self.commands: list[dict[str, Any]] = []
        self._submitted_exception: type | None = None

    def _install_shell_tools(self) -> None:
        base = shlex.split(self.evas_command)
        if not base:
            raise ValueError("empty EVAS executable command")
        executable = shutil.which(base[0])
        if executable is None:
            raise ValueError(f"EVAS executable is unavailable: {base[0]}")
        base[0] = str(Path(executable).resolve())
        self.evas_read_roots = self._evas_read_roots(Path(base[0]), base[1:])
        if any(
            root == self.runtime or self.runtime in root.parents
            for root in self.evas_read_roots
        ):
            raise ValueError("EVAS executable runtime is inside the private task runtime")
        evas_wrapper = self.tools_dir / "evas"
        telemetry_prefix = f"VABENCH_EVAS:{self._evas_telemetry_token}"
        evas_wrapper.write_text(
            "#!/bin/bash\n"
            "set -e\n"
            "invocation_id=\"${BASHPID:-$$}-${RANDOM}\"\n"
            f"telemetry_prefix={shlex.quote(telemetry_prefix)}\n"
            "printf '\\036%s:%s:START\\n' \"$telemetry_prefix\" \"$invocation_id\" >&9\n"
            "finish_telemetry() {\n"
            "  rc=$?\n"
            "  printf '\\036%s:%s:END:%s\\n' \"$telemetry_prefix\" \"$invocation_id\" \"$rc\" >&9\n"
            "}\n"
            "trap finish_telemetry EXIT\n"
            "args=()\n"
            "while (($#)); do\n"
            "  if [[ $1 == -o ]]; then\n"
            "    shift\n"
            "    [[ $# -gt 0 ]] || { echo 'evas: -o requires a path' >&2; exit 2; }\n"
            "    output=$1\n"
            "    if [[ $output == /tmp/vabench-visible/evas-output* ]]; then\n"
            "      suffix=${output#/tmp/vabench-visible/evas-output}\n"
            "      output=${VABENCH_EVAS_OUTPUT_ROOT}${suffix}\n"
            "      echo \"VABENCH_EVAS_OUTPUT=$output\" >&2\n"
            "    elif [[ $output == public/submission/evas-output* ]]; then\n"
            "      suffix=${output#public/submission/evas-output}\n"
            "      output=${VABENCH_EVAS_OUTPUT_ROOT}${suffix}\n"
            "      echo \"VABENCH_EVAS_OUTPUT=$output\" >&2\n"
            "    fi\n"
            "    args+=(\"-o\" \"$output\")\n"
            "  else\n"
            "    args+=(\"$1\")\n"
            "  fi\n"
            "  shift\n"
            "done\n"
            "set +e\n"
            f"{shlex.join(base)} \"${{args[@]}}\"\n"
            "exit $?\n",
            encoding="utf-8",
        )
        evas_wrapper.chmod(0o755)
        submit = self.tools_dir / "vabench-submit"
        submit.write_text(
            "#!/bin/bash\n"
            "set -e\n"
            ": > \"${VABENCH_SUBMIT_SENTINEL:?}\"\n",
            encoding="utf-8",
        )
        submit.chmod(0o755)

    @staticmethod
    def _evas_read_roots(executable: Path, arguments: list[str]) -> list[Path]:
        system_roots = tuple(
            Path(root) for root in ("/usr", "/bin", "/sbin", "/lib", "/lib64")
        )

        def system_path(path: Path) -> bool:
            return any(path == root or root in path.parents for root in system_roots)

        roots: list[Path] = []
        venv = executable.parent.parent
        roots.append(venv if (venv / "pyvenv.cfg").is_file() else executable)
        roots.extend(
            path
            for argument in arguments
            if (path := Path(argument)).is_absolute() and path.is_file()
        )
        try:
            first_line = executable.read_text(encoding="utf-8", errors="ignore").splitlines()[0]
        except (OSError, IndexError):
            first_line = ""
        if first_line.startswith("#!"):
            interpreter = Path(first_line[2:].strip().split()[0])
            if interpreter.is_absolute():
                resolved = interpreter.resolve()
                if not system_path(resolved):
                    roots.append(resolved.parent.parent)
        unique: list[Path] = []
        for root in roots:
            resolved = root.resolve()
            if not system_path(resolved) and resolved not in unique:
                unique.append(resolved)
        return unique

    def bind_submitted_exception(self, exception_type: type) -> None:
        self._submitted_exception = exception_type

    def _remaining_command_timeout_s(self) -> float:
        if self.deadline_monotonic is None:
            return self.config.timeout
        return max(
            0.1,
            min(self.config.timeout, self.deadline_monotonic - time.monotonic()),
        )

    def get_template_vars(self, **kwargs: Any) -> dict[str, Any]:
        return {"workspace": str(self.workspace), **kwargs}

    def serialize(self) -> dict[str, Any]:
        return {
            "info": {
                "config": {
                    "environment": {
                        "cwd": str(self.workspace),
                        "timeout": self.config.timeout,
                        "sandbox_backend": self.config.sandbox_backend,
                        "network": False,
                        "evaluator_mounted": False,
                    }
                },
                "commands": self.commands,
            }
        }

    def preflight(self) -> None:
        """Fail before the first model call if the requested isolation is unusable."""
        if self.config.sandbox_backend == "none":
            return
        # ``test -r`` checks Unix permission bits and can still report a path as
        # readable when sandbox-exec would deny the actual filesystem access.
        # Probe a real directory read so macOS and namespace-based backends are
        # validated against the isolation property we rely on.
        argv = self._sandbox_argv(
            "test -r public/task/instruction.md "
            "&& command -v evas >/dev/null "
            "&& evas --version >/dev/null "
            "&& ! /bin/ls ../evaluator >/dev/null 2>&1"
        )
        probe = subprocess.run(
            argv,
            cwd=self.workspace,
            env=self._shell_env(),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=min(10.0, self._remaining_command_timeout_s()),
            check=False,
        )
        if probe.returncode != 0:
            diagnostic = probe.stdout.strip()[:2000] or f"returncode={probe.returncode}"
            if "RTM_NEWADDR" in diagnostic or "unprivileged user namespaces" in diagnostic:
                diagnostic += (
                    " | Linux host policy blocked secure user/network namespaces. "
                    "On Ubuntu 24.04, use the distro system /usr/bin/bwrap with its "
                    "targeted AppArmor userns profile; do not disable network isolation."
                )
            raise RuntimeError(
                "mini-SWE sandbox preflight failed before the first model call: "
                + diagnostic
            )

    def _sandbox_argv(self, command: str) -> list[str]:
        command = "exec 9>&1\n" + command
        backend = self.config.sandbox_backend
        if backend == "sandbox-exec":
            executable = shutil.which("sandbox-exec")
            if not executable:
                raise RuntimeError("sandbox-exec backend requested but unavailable")
            return [
                executable,
                "-p",
                _sandbox_profile(self.workspace, self.evas_read_roots),
                "/bin/bash",
                "-c",
                command,
            ]
        if backend == "bubblewrap":
            executable = shutil.which("bwrap")
            if not executable:
                raise RuntimeError("bubblewrap backend requested but bwrap is unavailable")
            return _bubblewrap_argv(
                executable, self.runtime, self.evas_read_roots, command
            )
        if backend == "none":
            return ["/bin/bash", "-c", command]
        raise RuntimeError(f"unsupported mini-SWE sandbox backend: {backend}")

    def _submit(self) -> dict[str, Any]:
        gate = self.submission_gate(self.runtime)
        if not gate.get("passed"):
            return {
                "output": json.dumps(
                    {"status": "submission_rejected", "diagnostics": gate.get("diagnostics") or []},
                    sort_keys=True,
                ),
                "returncode": 2,
                "exception_info": "",
            }
        if self._submitted_exception is None:
            raise RuntimeError("mini-SWE-agent Submitted exception was not bound")
        manifest = {
            "status": "submitted",
            "artifact_sha256": gate.get("artifact_sha256") or {},
        }
        raise self._submitted_exception(
            {
                "role": "exit",
                "content": json.dumps(manifest, sort_keys=True),
                "extra": {"exit_status": "Submitted", "submission": json.dumps(manifest, sort_keys=True)},
            }
        )

    def _shell_env(self) -> dict[str, str]:
        return {
            "PATH": f"{self.tools_dir}:/usr/bin:/bin:/usr/sbin:/sbin",
            "HOME": str(self.workspace),
            "TMPDIR": str(self.workspace / ".tmp"),
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "VABENCH_EVAS_OUTPUT_ROOT": str(self.workspace / "evas-output"),
            "VABENCH_SUBMIT_SENTINEL": str(self.submit_sentinel),
        }

    def _run_sandboxed(self, command: str) -> dict[str, Any]:
        env = self._shell_env()
        argv = self._sandbox_argv(command)
        started = time.monotonic()
        try:
            completed = subprocess.run(
                argv,
                cwd=self.workspace,
                env=env,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=self._remaining_command_timeout_s(),
                check=False,
            )
            elapsed_s = time.monotonic() - started
            output = self._record_evas_invocations(
                completed.stdout,
                command=command,
                elapsed_s=elapsed_s,
                command_timed_out=False,
            )
            return {
                "output": output,
                "returncode": completed.returncode,
                "exception_info": "",
                "elapsed_s": elapsed_s,
            }
        except subprocess.TimeoutExpired as exc:
            output = exc.stdout.decode(errors="replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
            elapsed_s = time.monotonic() - started
            output = self._record_evas_invocations(
                output,
                command=command,
                elapsed_s=elapsed_s,
                command_timed_out=True,
            )
            return {
                "output": output,
                "returncode": -1,
                "exception_info": "bash command timed out within the episode wall-time limit",
                "elapsed_s": elapsed_s,
            }

    def _record_evas_invocations(
        self,
        output: str,
        *,
        command: str,
        elapsed_s: float,
        command_timed_out: bool,
    ) -> str:
        marker = re.compile(
            rf"\x1eVABENCH_EVAS:{re.escape(self._evas_telemetry_token)}:"
            r"(?P<invocation_id>[^:\r\n]+):(?P<event>START|END)(?::(?P<returncode>-?\d+))?\r?\n?"
        )
        active: dict[str, dict[str, Any]] = {}
        order: list[str] = []
        for match in marker.finditer(output):
            invocation_id = match.group("invocation_id")
            if match.group("event") == "START":
                if invocation_id not in active:
                    active[invocation_id] = {
                        "invocation_id": invocation_id,
                        "shell_command": command,
                        "shell_elapsed_s": elapsed_s,
                    }
                    order.append(invocation_id)
                continue
            row = active.get(invocation_id)
            if row is None:
                continue
            returncode = int(match.group("returncode") or 0)
            row["returncode"] = returncode
            row["status"] = "succeeded" if returncode == 0 else "failed"
        for invocation_id in order:
            row = active[invocation_id]
            if "status" not in row:
                row["returncode"] = None
                row["status"] = "timed_out" if command_timed_out else "interrupted"
            self.evas_invocations.append(row)
        return marker.sub("", output)

    def execute(self, action: dict[str, Any], cwd: str = "") -> dict[str, Any]:
        del cwd
        command = str(action.get("command") or "")
        started = time.monotonic()
        kind = "bash"
        try:
            output = self._run_sandboxed(command)
            if self.submit_sentinel.is_file():
                self.submit_sentinel.unlink(missing_ok=True)
                kind = "bash-submit"
                output = self._submit()
        except Exception:
            self.commands.append(
                {
                    "command": command,
                    "kind": kind,
                    "returncode": 0 if kind == "bash-submit" else -1,
                    "elapsed_s": time.monotonic() - started,
                }
            )
            raise
        self.commands.append(
            {
                "command": command,
                "kind": kind,
                "returncode": output.get("returncode"),
                "elapsed_s": output.get("elapsed_s", time.monotonic() - started),
            }
        )
        return output


class VaBenchMiniModel:
    def __init__(
        self,
        client: Any,
        *,
        per_turn_max_tokens: int,
        request_timeout_s: float,
        deadline_monotonic: float,
        usage_parser: Callable[..., dict[str, Any]],
        response_metadata: Callable[[dict[str, Any]], dict[str, Any]],
    ) -> None:
        self.client = client
        self.per_turn_max_tokens = per_turn_max_tokens
        self.request_timeout_s = request_timeout_s
        self.deadline_monotonic = deadline_monotonic
        self.usage_parser = usage_parser
        self.response_metadata = response_metadata
        self.config = SimpleNamespace(model_name=client.model)
        self.events: list[dict[str, Any]] = []
        self.total_output_tokens = 0
        self._format_observations: Callable[..., list[dict[str, Any]]] | None = None
        self._format_error: type | None = None

    def bind_mini_swe_protocol(
        self,
        formatter: Callable[..., list[dict[str, Any]]],
        format_error: type,
    ) -> None:
        self._format_observations = formatter
        self._format_error = format_error

    def get_template_vars(self, **kwargs: Any) -> dict[str, Any]:
        return {"model_name": self.client.model, **kwargs}

    def format_message(self, *, role: str, content: str, extra: dict[str, Any] | None = None, **kwargs: Any) -> dict[str, Any]:
        return {"role": role, "content": content, "extra": extra or {}, **kwargs}

    def query(self, messages: list[dict[str, Any]], **kwargs: Any) -> dict[str, Any]:
        del kwargs
        remaining = max(0.1, self.deadline_monotonic - time.monotonic())
        timeout_s = min(float(self.request_timeout_s), remaining)
        provider_messages = [
            {key: value for key, value in message.items() if key in {"role", "content", "tool_call_id", "tool_calls"}}
            for message in messages
            if message.get("role") != "exit"
        ]
        started = time.monotonic()
        response = self.client.complete(
            provider_messages,
            self.per_turn_max_tokens,
            [BASH_TOOL],
            timeout_s=timeout_s,
        )
        choice_row = response["choices"][0]
        choice = dict(choice_row["message"])
        content = str(choice.get("content") or "")
        reasoning = str(choice.get("reasoning_content") or "")
        calls = list(choice.get("tool_calls") or [])
        usage = self.usage_parser(
            response.get("usage"),
            content,
            reasoning_text=reasoning,
            tool_text=json.dumps(calls, sort_keys=True) if calls else "",
        )
        self.total_output_tokens += int(usage["output_tokens"])
        event = {
            "type": "model",
            "elapsed_s": time.monotonic() - started,
            "requested_max_tokens": self.per_turn_max_tokens,
            "finish_reason": choice_row.get("finish_reason"),
            "provider_output_tokens": usage["output_tokens"],
            "provider_reasoning_tokens": usage["reasoning_tokens"],
            "provider_visible_tokens": usage["visible_tokens"],
            "provider_token_source": usage["source"],
            "provider_usage": response.get("usage"),
            "provider_response": self.response_metadata(response),
        }
        # Count every completed provider call, including responses that mini-SWE
        # subsequently rejects as malformed. Token accounting is telemetry only.
        self.events.append(event)
        actions: list[dict[str, Any]] = []
        if not calls:
            if self._format_error is None:
                raise RuntimeError("mini-SWE-agent FormatError was not bound")
            raise self._format_error(
                {
                    "role": "user",
                    "content": (
                        "No tool calls found in the response. Every response MUST "
                        "include at least one bash tool call."
                    ),
                    "extra": {"interrupt_type": "FormatError"},
                }
            )
        for call in calls:
            function = call.get("function") or {}
            if function.get("name") != "bash":
                if self._format_error is None:
                    raise RuntimeError("mini-SWE-agent FormatError was not bound")
                raise self._format_error(
                    {
                        "role": "user",
                        "content": f"Unknown tool {function.get('name')!r}; use bash.",
                        "extra": {"interrupt_type": "FormatError"},
                    }
                )
            try:
                arguments = json.loads(function.get("arguments") or "{}")
            except json.JSONDecodeError as exc:
                if self._format_error is None:
                    raise RuntimeError("mini-SWE-agent FormatError was not bound") from exc
                raise self._format_error(
                    {
                        "role": "user",
                        "content": f"Invalid bash tool arguments: {exc}.",
                        "extra": {"interrupt_type": "FormatError"},
                    }
                ) from exc
            if not isinstance(arguments, dict) or not isinstance(arguments.get("command"), str):
                if self._format_error is None:
                    raise RuntimeError("mini-SWE-agent FormatError was not bound")
                raise self._format_error(
                    {
                        "role": "user",
                        "content": "The bash tool requires a string command argument.",
                        "extra": {"interrupt_type": "FormatError"},
                    }
                )
            actions.append({"command": arguments["command"], "tool_call_id": str(call.get("id") or "")})
        choice["extra"] = {"actions": actions, "cost": 0.0, "provider_event": event}
        return choice

    def format_observation_messages(
        self, message: dict[str, Any], outputs: list[dict[str, Any]], template_vars: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        if self._format_observations is None:
            raise RuntimeError("mini-SWE-agent observation formatter was not bound")
        return self._format_observations(
            actions=list((message.get("extra") or {}).get("actions") or []),
            outputs=outputs,
            observation_template=(
                "<returncode>{{ output.returncode }}</returncode>\n"
                "{% if output.exception_info %}<exception>{{ output.exception_info }}</exception>\n{% endif %}"
                "<output>\n{{ output.output[:12000] }}\n</output>"
            ),
            template_vars=template_vars or {},
        )

    def serialize(self) -> dict[str, Any]:
        return {
            "info": {
                "model": self.client.model,
                "provider_output_tokens": self.total_output_tokens,
                "provider_events": self.events,
            }
        }


def run_mini_swe_episode(
    *,
    runtime: Path,
    prompt: str,
    client: Any,
    per_turn_max_tokens: int,
    agent_timeout_s: float,
    request_timeout_s: float,
    tool_timeout_s: float,
    sandbox_backend: str,
    evas_command: str,
    submission_gate: Callable[[Path], dict[str, Any]],
    usage_parser: Callable[..., dict[str, Any]],
    response_metadata: Callable[[dict[str, Any]], dict[str, Any]],
    trajectory_path: Path,
) -> dict[str, Any]:
    DefaultAgent, Submitted, FormatError, observation_formatter = load_mini_swe()
    started = time.monotonic()
    deadline = started + float(agent_timeout_s)
    environment = VaBenchBashEnvironment(
        runtime,
        timeout_s=min(float(tool_timeout_s), float(agent_timeout_s)),
        sandbox_backend=sandbox_backend,
        evas_command=evas_command,
        deadline_monotonic=deadline,
        submission_gate=submission_gate,
    )
    environment.preflight()
    environment.bind_submitted_exception(Submitted)
    model = VaBenchMiniModel(
        client,
        per_turn_max_tokens=per_turn_max_tokens,
        request_timeout_s=request_timeout_s,
        deadline_monotonic=deadline,
        usage_parser=usage_parser,
        response_metadata=response_metadata,
    )
    model.bind_mini_swe_protocol(observation_formatter, FormatError)
    agent = DefaultAgent(
        model,
        environment,
        system_template=SYSTEM_PROMPT,
        instance_template="{{task}}",
        step_limit=0,
        cost_limit=0.0,
        wall_time_limit_seconds=max(1, int(agent_timeout_s)),
        # Keep malformed-turn recovery available without introducing another
        # episode cutoff. Submission, provider/context failure, and wall time
        # remain the only terminal conditions.
        max_consecutive_format_errors=0,
        output_path=trajectory_path,
    )
    task = prompt.rstrip() + "\n\n" + BASH_CONTRACT
    outcome = agent.run(task)
    gate = submission_gate(runtime)
    serialized = agent.serialize()
    explicit_submission = outcome.get("exit_status") == "Submitted"
    return {
        "scaffold": MINI_SWE_SCAFFOLD_ID,
        "scaffold_version": MINI_SWE_AGENT_VERSION,
        "bash_tool_schema_sha256": _json_digest(BASH_TOOL),
        "system_prompt_sha256": hashlib.sha256(SYSTEM_PROMPT.encode()).hexdigest(),
        "bash_contract_sha256": hashlib.sha256(BASH_CONTRACT.encode()).hexdigest(),
        "exit_status": outcome.get("exit_status"),
        "submission": outcome.get("submission", ""),
        "submitted": bool(explicit_submission and gate.get("passed")),
        "artifact_complete": bool(gate.get("passed")),
        "artifact_gate": gate,
        "artifact_sha256": gate.get("artifact_sha256") or {},
        "output_tokens": model.total_output_tokens,
        "events": model.events,
        "commands": environment.commands,
        "evas_invocations": environment.evas_invocations,
        "model_calls": len(model.events),
        "messages": list(serialized.get("messages") or []),
        "agent_elapsed_s": time.monotonic() - started,
        "trajectory_format": serialized.get("trajectory_format"),
        "sandbox_backend": sandbox_backend,
        "network": False,
        "evaluator_mounted": False,
    }


def default_sandbox_backend() -> str:
    if platform.system() == "Darwin" and shutil.which("sandbox-exec"):
        return "sandbox-exec"
    if platform.system() == "Linux" and shutil.which("bwrap"):
        return "bubblewrap"
    raise RuntimeError(
        "no supported secure bash sandbox found; install bubblewrap on Linux/WSL2, "
        "use macOS sandbox-exec, or explicitly select --mini-swe-sandbox none only "
        "for local tests"
    )
