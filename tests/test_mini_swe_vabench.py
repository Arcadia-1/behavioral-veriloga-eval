from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import shutil
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
MODULE = (
    ROOT
    / "benchmark-vabench-release-v4"
    / "operations"
    / "calibration_pilot"
    / "mini_swe_vabench.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location("mini_swe_vabench_test", MODULE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class FakeProvider:
    model = "test-model"

    def __init__(self, commands: list[str | None]) -> None:
        self.commands = list(commands)
        self.calls: list[dict] = []

    def complete(self, messages, max_tokens, tools, *, timeout_s):
        command = self.commands.pop(0)
        self.calls.append(
            {
                "messages": messages,
                "max_tokens": max_tokens,
                "tools": tools,
                "timeout_s": timeout_s,
            }
        )
        message = {"role": "assistant", "content": "I will inspect the task first."}
        if command is not None:
            message["tool_calls"] = [
                {
                    "id": f"call-{len(self.calls)}",
                    "type": "function",
                    "function": {
                        "name": "bash",
                        "arguments": json.dumps({"command": command}),
                    },
                }
            ]
        return {
            "id": f"response-{len(self.calls)}",
            "model": self.model,
            "choices": [
                {
                    "finish_reason": "tool_calls",
                    "message": message,
                }
            ],
            "usage": {"completion_tokens": 7},
        }


def usage_parser(usage, _visible, **_kwargs):
    return {
        "output_tokens": int(usage["completion_tokens"]),
        "reasoning_tokens": 0,
        "visible_tokens": int(usage["completion_tokens"]),
        "source": "provider_usage",
    }


def response_metadata(response):
    return {"response_id": response["id"], "model": response["model"]}


def artifact_gate(runtime: Path) -> dict:
    artifact = runtime / "public" / "submission" / "model.va"
    passed = artifact.is_file() and not artifact.is_symlink()
    return {
        "passed": passed,
        "diagnostics": [] if passed else ["missing:model.va"],
        "artifact_sha256": {"model.va": "test-hash"} if passed else {},
    }


def test_mini_swe_bash_episode_runs_feedback_reads_output_and_submits(tmp_path: Path) -> None:
    module = load_module()
    runtime = tmp_path / "runtime"
    (runtime / "public" / "task").mkdir(parents=True)
    (runtime / "public" / "submission").mkdir(parents=True)
    (runtime / "evaluator").mkdir(parents=True)
    (runtime / "public" / "task" / "instruction.md").write_text("public task")
    (runtime / "evaluator" / "secret.txt").write_text("sealed")
    provider = FakeProvider(
        [
            "vabench feedback run",
            "cat evas-output/run-0001/summary.json",
            "printf 'module model; endmodule\\n' > submission/model.va",
            "vabench-submit",
        ]
    )

    result = module.run_mini_swe_episode(
        runtime=runtime,
        prompt="Generate model.va.",
        client=provider,
        per_turn_max_tokens=4096,
        agent_timeout_s=30,
        request_timeout_s=10,
        tool_timeout_s=10,
        sandbox_backend="none",
        feedback_runner=lambda _runtime, _timeout, _case: {
            "returncode": 1,
            "stdout": "FEEDBACK_BEHAVIOR_FAIL\nP_DELAY expected=2 observed=3\n",
            "stderr": "",
            "elapsed_s": 0.1,
        },
        submission_gate=artifact_gate,
        usage_parser=usage_parser,
        response_metadata=response_metadata,
        trajectory_path=runtime / "evidence" / "trajectory.json",
    )

    assert result["submitted"] is True
    assert result["exit_status"] == "Submitted"
    assert result["output_tokens"] == 28
    assert result["model_calls"] == 4
    assert [row["kind"] for row in result["commands"]] == [
        "vabench-feedback-run",
        "bash",
        "bash",
        "vabench-submit",
    ]
    assert result["scaffold"] == "mini-swe-agent-2.4.5-vabench-bash-v1"
    assert (runtime / "public" / "submission" / "model.va").is_file()
    run_dir = runtime / "public" / "evas-output" / "run-0001"
    assert json.loads((run_dir / "summary.json").read_text())["status"] == "fail"
    assert "P_DELAY" in (run_dir / "stdout.log").read_text()
    assert (runtime / "evidence" / "trajectory.json").is_file()


def test_sandbox_cannot_read_sibling_evaluator(tmp_path: Path) -> None:
    if shutil.which("sandbox-exec") is None:
        pytest.skip("sandbox-exec is only available on supported macOS runners")
    module = load_module()
    runtime = tmp_path / "runtime"
    (runtime / "public" / "task").mkdir(parents=True)
    (runtime / "public" / "submission").mkdir(parents=True)
    (runtime / "evaluator").mkdir(parents=True)
    (runtime / "evaluator" / "secret.txt").write_text("sealed")
    environment = module.VaBenchBashEnvironment(
        runtime,
        timeout_s=5,
        sandbox_backend="sandbox-exec",
        feedback_runner=lambda _runtime, _timeout, _case: {},
        submission_gate=artifact_gate,
    )

    result = environment.execute({"command": "cat ../evaluator/secret.txt"})

    assert result["returncode"] != 0
    assert "sealed" not in result["output"]


def test_sandbox_profile_keeps_evas_output_read_only(tmp_path: Path) -> None:
    module = load_module()
    workspace = tmp_path / "runtime" / "public"
    profile = module._sandbox_profile(workspace)

    write_rule = next(
        line for line in profile.splitlines() if line.startswith("(allow file-write*")
    )
    assert str(workspace / "submission") in write_rule
    assert str(workspace / ".tmp") in write_rule
    assert str(workspace / "evas-output") not in write_rule


def test_bubblewrap_argv_mounts_only_the_public_workspace(tmp_path: Path) -> None:
    module = load_module()
    runtime = tmp_path / "runtime"
    workspace = runtime / "public"
    argv = module._bubblewrap_argv("/usr/bin/bwrap", workspace, "pwd")

    assert "--unshare-net" in argv
    assert [str(workspace), "/workspace"] == argv[
        argv.index("--ro-bind", argv.index("--dir")) + 1 :
        argv.index("--ro-bind", argv.index("--dir")) + 3
    ]
    assert str(runtime / "evaluator") not in argv
    assert [str(workspace / "submission"), "/workspace/submission"] == argv[
        argv.index("--bind") + 1 : argv.index("--bind") + 3
    ]
    assert str(workspace / "evas-output") not in argv


def test_auto_selects_bubblewrap_on_linux(monkeypatch: pytest.MonkeyPatch) -> None:
    module = load_module()
    monkeypatch.setattr(module.platform, "system", lambda: "Linux")
    monkeypatch.setattr(
        module.shutil,
        "which",
        lambda name: "/usr/bin/bwrap" if name == "bwrap" else None,
    )

    assert module.default_sandbox_backend() == "bubblewrap"


def test_bubblewrap_isolates_evaluator_and_feedback_output(tmp_path: Path) -> None:
    if shutil.which("bwrap") is None:
        pytest.skip("bubblewrap is not installed on this host")
    module = load_module()
    runtime = tmp_path / "runtime"
    (runtime / "public" / "task").mkdir(parents=True)
    (runtime / "public" / "submission").mkdir(parents=True)
    (runtime / "public" / "evas-output").mkdir(parents=True)
    (runtime / "evaluator").mkdir(parents=True)
    (runtime / "evaluator" / "secret.txt").write_text("sealed")
    environment = module.VaBenchBashEnvironment(
        runtime,
        timeout_s=5,
        sandbox_backend="bubblewrap",
        feedback_runner=lambda _runtime, _timeout, _case: {},
        submission_gate=artifact_gate,
    )

    environment.preflight()
    hidden = environment.execute({"command": "cat ../evaluator/secret.txt"})
    readonly = environment.execute(
        {"command": "printf tampered > evas-output/model-created.log"}
    )
    writable = environment.execute(
        {"command": "printf candidate > submission/model.va"}
    )

    assert hidden["returncode"] != 0
    assert "sealed" not in hidden["output"]
    assert readonly["returncode"] != 0
    assert not (runtime / "public" / "evas-output" / "model-created.log").exists()
    assert writable["returncode"] == 0
    assert (runtime / "public" / "submission" / "model.va").read_text() == "candidate"


def test_sandbox_cannot_modify_evas_output(tmp_path: Path) -> None:
    if shutil.which("sandbox-exec") is None:
        pytest.skip("sandbox-exec is only available on supported macOS runners")
    module = load_module()
    runtime = tmp_path / "runtime"
    (runtime / "public" / "task").mkdir(parents=True)
    (runtime / "public" / "submission").mkdir(parents=True)
    (runtime / "public" / "evas-output").mkdir(parents=True)
    environment = module.VaBenchBashEnvironment(
        runtime,
        timeout_s=5,
        sandbox_backend="sandbox-exec",
        feedback_runner=lambda _runtime, _timeout, _case: {},
        submission_gate=artifact_gate,
    )

    result = environment.execute(
        {"command": "printf tampered > evas-output/model-created.log"}
    )

    assert result["returncode"] != 0
    assert not (runtime / "public" / "evas-output" / "model-created.log").exists()


def test_missing_feedback_returncode_is_a_failure(tmp_path: Path) -> None:
    module = load_module()
    runtime = tmp_path / "runtime"
    (runtime / "public" / "task").mkdir(parents=True)
    (runtime / "public" / "submission").mkdir(parents=True)
    environment = module.VaBenchBashEnvironment(
        runtime,
        timeout_s=5,
        sandbox_backend="none",
        feedback_runner=lambda _runtime, _timeout, _case: {
            "stdout": "unavailable",
            "stderr": "",
        },
        submission_gate=artifact_gate,
    )

    result = environment.execute({"command": "vabench feedback run"})

    summary = json.loads(
        (runtime / "public" / "evas-output" / "run-0001" / "summary.json").read_text()
    )
    assert result["returncode"] == -1
    assert summary["returncode"] == -1
    assert summary["status"] == "fail"


def test_mini_swe_reprompts_after_missing_bash_call_and_counts_telemetry(
    tmp_path: Path,
) -> None:
    module = load_module()
    runtime = tmp_path / "runtime"
    (runtime / "public" / "task").mkdir(parents=True)
    (runtime / "public" / "submission").mkdir(parents=True)
    provider = FakeProvider(
        [
            None,
            "printf 'module model; endmodule\\n' > submission/model.va",
            "vabench-submit",
        ]
    )

    result = module.run_mini_swe_episode(
        runtime=runtime,
        prompt="Generate model.va.",
        client=provider,
        per_turn_max_tokens=4096,
        agent_timeout_s=30,
        request_timeout_s=10,
        tool_timeout_s=10,
        sandbox_backend="none",
        feedback_runner=lambda _runtime, _timeout, _case: {},
        submission_gate=artifact_gate,
        usage_parser=usage_parser,
        response_metadata=response_metadata,
        trajectory_path=runtime / "evidence" / "trajectory.json",
    )

    assert result["submitted"] is True
    assert result["model_calls"] == 3
    assert result["output_tokens"] == 21
    trajectory = json.loads((runtime / "evidence" / "trajectory.json").read_text())
    assert any(
        (message.get("extra") or {}).get("interrupt_type") == "FormatError"
        for message in trajectory["messages"]
    )
