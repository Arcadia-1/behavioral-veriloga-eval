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


def test_mini_swe_bash_episode_runs_direct_evas_reads_output_and_submits(
    tmp_path: Path,
) -> None:
    module = load_module()
    runtime = tmp_path / "runtime"
    (runtime / "public" / "task").mkdir(parents=True)
    (runtime / "public" / "task" / "instruction.md").write_text("public task")
    (runtime / "public" / "task" / "visible_test.scs").write_text("tran tran stop=1n")
    (runtime / "public" / "submission").mkdir(parents=True)
    (runtime / "evaluator").mkdir(parents=True)
    (runtime / "evaluator" / "secret.txt").write_text("sealed")
    fake_evas = tmp_path / "fake-evas"
    fake_evas.write_text(
        "#!/bin/bash\n"
        "if [[ $1 == --version || $1 == --help ]]; then echo 'evas-test 1.0'; exit 0; fi\n"
        "while (($#)); do\n"
        "  if [[ $1 == -o ]]; then shift; output=$1; fi\n"
        "  shift\n"
        "done\n"
        "mkdir -p \"$output\"\n"
        "printf 'time,vout\\n0,0\\n' > \"$output/tran.csv\"\n"
    )
    fake_evas.chmod(0o755)
    provider = FakeProvider(
        [
            "which evas && evas --help",
            "printf 'module model; endmodule\\n' > public/submission/model.va",
            (
                "evas simulate public/task/visible_test.scs "
                "-o /tmp/vabench-visible/evas-output --spectre-strict 2>&1 | tail -20"
            ),
            "cat public/evas-output/tran.csv",
            "which vabench-submit && vabench-submit",
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
        evas_command=str(fake_evas),
        submission_gate=artifact_gate,
        usage_parser=usage_parser,
        response_metadata=response_metadata,
        trajectory_path=runtime / "evidence" / "trajectory.json",
    )

    assert result["submitted"] is True
    assert result["exit_status"] == "Submitted"
    assert result["output_tokens"] == 35
    assert result["model_calls"] == 5
    assert [row["returncode"] for row in result["evas_invocations"]] == [0, 0]
    assert [row["status"] for row in result["evas_invocations"]] == [
        "succeeded",
        "succeeded",
    ]
    assert "VABENCH_EVAS:" not in json.dumps(result["messages"])
    assert [row["kind"] for row in result["commands"]] == [
        "bash",
        "bash",
        "bash",
        "bash",
        "bash-submit",
    ]
    assert result["scaffold"] == "mini-swe-agent-2.4.5-vabench-direct-evas-v2"
    assert (runtime / "public" / "submission" / "model.va").is_file()
    assert "time,vout" in (
        runtime / "public" / "evas-output" / "tran.csv"
    ).read_text()
    assert (runtime / "evidence" / "trajectory.json").is_file()


def test_sandbox_cannot_read_sibling_evaluator(tmp_path: Path) -> None:
    if shutil.which("sandbox-exec") is None:
        pytest.skip("sandbox-exec is only available on supported macOS runners")
    module = load_module()
    runtime = tmp_path / "runtime"
    (runtime / "public" / "task").mkdir(parents=True)
    (runtime / "public" / "task" / "instruction.md").write_text("public task")
    (runtime / "public" / "submission").mkdir(parents=True)
    (runtime / "evaluator").mkdir(parents=True)
    (runtime / "evaluator" / "secret.txt").write_text("sealed")
    environment = module.VaBenchBashEnvironment(
        runtime,
        timeout_s=5,
        sandbox_backend="sandbox-exec",
        evas_command="/usr/bin/true",
        submission_gate=artifact_gate,
    )

    environment.preflight()
    result = environment.execute({"command": "cat ../evaluator/secret.txt"})

    assert result["returncode"] != 0
    assert "sealed" not in result["output"]


def test_macos_sandbox_executes_pinned_external_evas(tmp_path: Path) -> None:
    if shutil.which("sandbox-exec") is None:
        pytest.skip("sandbox-exec is only available on supported macOS runners")
    module = load_module()
    runtime = tmp_path / "runtime"
    (runtime / "public" / "task").mkdir(parents=True)
    (runtime / "public" / "task" / "instruction.md").write_text("public task")
    external = tmp_path / "tool-runtime" / "evas"
    external.parent.mkdir()
    external.write_text("#!/bin/bash\necho 'evas-external 1.0'\n")
    external.chmod(0o755)
    environment = module.VaBenchBashEnvironment(
        runtime,
        timeout_s=5,
        sandbox_backend="sandbox-exec",
        evas_command=str(external),
        submission_gate=artifact_gate,
    )

    environment.preflight()
    result = environment.execute({"command": "which evas && evas --version"})

    assert result["returncode"] == 0
    assert "public/.tools/evas" in result["output"]
    assert "evas-external 1.0" in result["output"]


def test_direct_evas_timeout_is_recorded_without_leaking_control_markers(
    tmp_path: Path,
) -> None:
    module = load_module()
    runtime = tmp_path / "runtime"
    (runtime / "public" / "task").mkdir(parents=True)
    slow_evas = tmp_path / "slow-evas"
    slow_evas.write_text("#!/bin/bash\nsleep 2\n", encoding="utf-8")
    slow_evas.chmod(0o755)
    environment = module.VaBenchBashEnvironment(
        runtime,
        timeout_s=1.0,
        sandbox_backend="none",
        evas_command=str(slow_evas),
        submission_gate=artifact_gate,
    )

    result = environment.execute({"command": "evas 2>&1 | tail -20"})

    assert result["returncode"] == -1
    assert "VABENCH_EVAS:" not in result["output"]
    assert len(environment.evas_invocations) == 1
    assert environment.evas_invocations[0]["status"] == "timed_out"
    assert environment.evas_invocations[0]["returncode"] is None


def test_sandbox_profile_allows_only_candidate_and_evas_scratch_writes(
    tmp_path: Path,
) -> None:
    module = load_module()
    workspace = tmp_path / "runtime" / "public"
    profile = module._sandbox_profile(workspace)

    write_rule = next(
        line for line in profile.splitlines() if line.startswith("(allow file-write*")
    )
    assert str(workspace / "submission") in write_rule
    assert str(workspace / ".tmp") in write_rule
    assert str(workspace / "evas-output") in write_rule


def test_bubblewrap_argv_mounts_only_the_public_workspace(tmp_path: Path) -> None:
    module = load_module()
    runtime = tmp_path / "runtime"
    workspace = runtime / "public"
    argv = module._bubblewrap_argv("/usr/bin/bwrap", runtime, [], "pwd")

    assert "--unshare-net" in argv
    assert [str(workspace), "/workspace/public"] == argv[
        argv.index("--ro-bind", argv.index("--dir")) + 1 :
        argv.index("--ro-bind", argv.index("--dir")) + 3
    ]
    assert str(runtime / "evaluator") not in argv
    assert [str(workspace / "submission"), "/workspace/public/submission"] == argv[
        argv.index("--bind") + 1 : argv.index("--bind") + 3
    ]
    assert [str(workspace / "evas-output"), "/workspace/public/evas-output"] in [
        argv[index + 1 : index + 3]
        for index, word in enumerate(argv)
        if word == "--bind"
    ]


def test_auto_selects_bubblewrap_on_linux(monkeypatch: pytest.MonkeyPatch) -> None:
    module = load_module()
    monkeypatch.setattr(module.platform, "system", lambda: "Linux")
    monkeypatch.setattr(
        module.shutil,
        "which",
        lambda name: "/usr/bin/bwrap" if name == "bwrap" else None,
    )

    assert module.default_sandbox_backend() == "bubblewrap"


def test_bubblewrap_isolates_evaluator_and_allows_direct_evas_output(
    tmp_path: Path,
) -> None:
    if shutil.which("bwrap") is None:
        pytest.skip("bubblewrap is not installed on this host")
    module = load_module()
    runtime = tmp_path / "runtime"
    (runtime / "public" / "task").mkdir(parents=True)
    (runtime / "public" / "task" / "instruction.md").write_text("public task")
    (runtime / "public" / "submission").mkdir(parents=True)
    (runtime / "public" / "evas-output").mkdir(parents=True)
    (runtime / "evaluator").mkdir(parents=True)
    (runtime / "evaluator" / "secret.txt").write_text("sealed")
    external = tmp_path / "tool-runtime" / "evas"
    external.parent.mkdir()
    external.write_text("#!/bin/bash\necho 'evas-external 1.0'\n")
    external.chmod(0o755)
    environment = module.VaBenchBashEnvironment(
        runtime,
        timeout_s=5,
        sandbox_backend="bubblewrap",
        evas_command=str(external),
        submission_gate=artifact_gate,
    )

    environment.preflight()
    hidden = environment.execute({"command": "cat ../evaluator/secret.txt"})
    direct_evas = environment.execute(
        {"command": "command -v evas && evas --version"}
    )
    scratch = environment.execute(
        {"command": "printf waveform > public/evas-output/model-created.log"}
    )
    writable = environment.execute(
        {"command": "printf candidate > public/submission/model.va"}
    )

    assert hidden["returncode"] != 0
    assert "sealed" not in hidden["output"]
    assert direct_evas["returncode"] == 0
    assert "evas-external 1.0" in direct_evas["output"]
    assert scratch["returncode"] == 0
    assert (runtime / "public" / "evas-output" / "model-created.log").read_text() == "waveform"
    assert writable["returncode"] == 0
    assert (runtime / "public" / "submission" / "model.va").read_text() == "candidate"


def test_sandbox_can_write_direct_evas_output_but_not_task(tmp_path: Path) -> None:
    if shutil.which("sandbox-exec") is None:
        pytest.skip("sandbox-exec is only available on supported macOS runners")
    module = load_module()
    runtime = tmp_path / "runtime"
    (runtime / "public" / "task").mkdir(parents=True)
    (runtime / "public" / "task" / "instruction.md").write_text("public task")
    (runtime / "public" / "submission").mkdir(parents=True)
    (runtime / "public" / "evas-output").mkdir(parents=True)
    environment = module.VaBenchBashEnvironment(
        runtime,
        timeout_s=5,
        sandbox_backend="sandbox-exec",
        evas_command="/usr/bin/true",
        submission_gate=artifact_gate,
    )

    scratch = environment.execute(
        {"command": "printf waveform > public/evas-output/model-created.log"}
    )
    task_write = environment.execute(
        {"command": "printf tampered > public/task/instruction.md"}
    )

    assert scratch["returncode"] == 0
    assert task_write["returncode"] != 0
    assert (runtime / "public" / "evas-output" / "model-created.log").read_text() == "waveform"
    assert (runtime / "public" / "task" / "instruction.md").read_text() == "public task"


def test_direct_evas_must_exist_before_the_first_model_call(tmp_path: Path) -> None:
    module = load_module()
    runtime = tmp_path / "runtime"
    (runtime / "public" / "task").mkdir(parents=True)
    (runtime / "public" / "submission").mkdir(parents=True)
    with pytest.raises(ValueError, match="EVAS executable is unavailable"):
        module.VaBenchBashEnvironment(
            runtime,
            timeout_s=5,
            sandbox_backend="none",
            evas_command="definitely-not-an-evas-executable",
            submission_gate=artifact_gate,
        )


def test_direct_evas_runtime_cannot_mount_private_task_assets(tmp_path: Path) -> None:
    module = load_module()
    runtime = tmp_path / "runtime"
    (runtime / "public" / "task").mkdir(parents=True)
    private_tool = runtime / "evaluator" / "evas"
    private_tool.parent.mkdir()
    private_tool.write_text("#!/bin/bash\nexit 0\n")
    private_tool.chmod(0o755)

    with pytest.raises(ValueError, match="inside the private task runtime"):
        module.VaBenchBashEnvironment(
            runtime,
            timeout_s=5,
            sandbox_backend="none",
            evas_command=str(private_tool),
            submission_gate=artifact_gate,
        )


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
            "printf 'module model; endmodule\\n' > public/submission/model.va",
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
        evas_command="/usr/bin/true",
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
