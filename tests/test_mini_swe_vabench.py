from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import shutil
import shlex
import subprocess
import sys
import threading
import time

import pytest


ROOT = Path(__file__).resolve().parents[1]
MODULE = (
    ROOT
    / "benchmark-vabench-release-v4"
    / "operations"
    / "calibration_pilot"
    / "mini_swe_vabench.py"
)
PUBLIC_RUNTIME = (
    ROOT / "benchmark-vabench-release-v4" / "public-agent-runtime" / "run.sh"
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
    assert result["scaffold"] == "mini-swe-agent-2.4.5-vabench-docker-evas-v3"
    assert (runtime / "public" / "submission" / "model.va").is_file()
    assert "time,vout" in (
        runtime / "public" / "evas-output" / "tran.csv"
    ).read_text()
    assert (runtime / "evidence" / "trajectory.json").is_file()


def test_mini_swe_agent_no_evas_uses_same_scaffold_without_evas(
    tmp_path: Path,
) -> None:
    module = load_module()
    runtime = tmp_path / "runtime"
    (runtime / "public" / "task").mkdir(parents=True)
    (runtime / "public" / "task" / "instruction.md").write_text("public task")
    (runtime / "public" / "submission").mkdir(parents=True)
    provider = FakeProvider(
        [
            "command -v evas || true",
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
        evas_command="",
        executable_feedback=False,
        submission_gate=artifact_gate,
        usage_parser=usage_parser,
        response_metadata=response_metadata,
        trajectory_path=runtime / "evidence" / "trajectory.json",
    )

    assert result["submitted"] is True
    assert result["scaffold"] == module.MINI_SWE_SCAFFOLD_ID
    assert result["executable_feedback"] is False
    assert result["evas_invocations"] == []
    assert "EVAS execution is not available" in json.dumps(result["messages"])
    first_observation = provider.calls[1]["messages"][-1]["content"]
    assert "<output>\n\n</output>" in first_observation
    assert (runtime / "public" / "submission" / "model.va").is_file()


def test_mini_swe_exposes_skill_package_lazily_and_records_lookup_command(
    tmp_path: Path,
) -> None:
    module = load_module()
    runtime = tmp_path / "runtime"
    (runtime / "public" / "task").mkdir(parents=True)
    (runtime / "public" / "task" / "instruction.md").write_text("public task")
    (runtime / "public" / "submission").mkdir(parents=True)
    skill = runtime / "public" / "skills" / "veriloga"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("---\nname: veriloga\n---\n# Language\n")
    tree_sha = module._skill_tree_sha(skill)
    (runtime / "public" / "skills" / "SNAPSHOT_MANIFEST.json").write_text(
        json.dumps({
            "schema_version": "v4-runtime-skill-manifest-v1",
            "skills": {
                "veriloga": {
                    "skill_file": "public/skills/veriloga/SKILL.md",
                    "tree_sha256": tree_sha,
                }
            },
        }) + "\n"
    )
    (runtime / "MODEL_ACCESS_POLICY.json").write_text(
        json.dumps({
            "mounts": [
                "public/task:ro",
                "public/submission:rw",
                "public/work:rw",
                "public/skills:ro",
            ],
            "available_skills": {
                "veriloga": {"tree_sha256": tree_sha},
            },
        }) + "\n",
        encoding="utf-8",
    )
    provider = FakeProvider([
        "sed -n '1,80p' public/skills/veriloga/SKILL.md",
        "printf 'module model; endmodule\\n' > public/submission/model.va",
        "vabench-submit",
    ])

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

    assert set(result["available_skills"]) == {"veriloga"}
    assert len(result["skill_command_events"]) == 1
    assert result["skill_command_events"][0]["returncode"] == 0
    assert "command" not in result["skill_command_events"][0]


def test_mini_swe_rejects_an_undeclared_skills_directory(tmp_path: Path) -> None:
    module = load_module()
    runtime = tmp_path / "runtime"
    (runtime / "public" / "task").mkdir(parents=True)
    (runtime / "public" / "submission").mkdir(parents=True)
    (runtime / "public" / "skills" / "veriloga").mkdir(parents=True)
    (runtime / "MODEL_ACCESS_POLICY.json").write_text(
        json.dumps({
            "mounts": [
                "public/task:ro",
                "public/submission:rw",
                "public/work:rw",
            ],
            "available_skills": {},
        }),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="not authorized"):
        module.VaBenchBashEnvironment(
            runtime,
            timeout_s=5,
            sandbox_backend="none",
            evas_command="/usr/bin/true",
            submission_gate=artifact_gate,
        )


def test_docker_backend_runs_shell_in_shared_environment_and_cleans_up(
    tmp_path: Path,
) -> None:
    module = load_module()
    runtime = tmp_path / "runtime"
    (runtime / "public" / "task").mkdir(parents=True)
    (runtime / "public" / "task" / "instruction.md").write_text("public task")
    (runtime / "public" / "submission").mkdir(parents=True)
    (runtime / "public" / "skills" / "veriloga").mkdir(parents=True)
    (runtime / "public" / "skills" / "veriloga" / "SKILL.md").write_text(
        "---\nname: veriloga\n---\n", encoding="utf-8"
    )
    skill = runtime / "public" / "skills" / "veriloga"
    tree_sha = module._skill_tree_sha(skill)
    (runtime / "public" / "skills" / "SNAPSHOT_MANIFEST.json").write_text(
        json.dumps({
            "schema_version": "v4-runtime-skill-manifest-v1",
            "skills": {
                "veriloga": {
                    "skill_file": "public/skills/veriloga/SKILL.md",
                    "tree_sha256": tree_sha,
                }
            },
        }),
        encoding="utf-8",
    )
    (runtime / "MODEL_ACCESS_POLICY.json").write_text(
        json.dumps({
            "mounts": [
                "public/task:ro",
                "public/submission:rw",
                "public/work:rw",
                "public/skills:ro",
            ],
            "available_skills": {
                "veriloga": {"tree_sha256": tree_sha},
            },
        }),
        encoding="utf-8",
    )
    log = tmp_path / "docker.log"
    fake_docker = tmp_path / "docker"
    fake_docker.write_text(
        "#!/bin/sh\n"
        f"printf '%s\\n' \"$*\" >> {str(log)!r}\n"
        "case \"$1 $2\" in\n"
        "  'image inspect') echo 'sha256:shared-environment' ;;\n"
        "  'create --name') echo 'vabench-test-container' ;;\n"
        "  'exec -i') echo 'hello from shared docker' ;;\n"
        "esac\n",
        encoding="utf-8",
    )
    fake_docker.chmod(0o755)
    environment = module.VaBenchBashEnvironment(
        runtime,
        timeout_s=5,
        sandbox_backend="docker",
        evas_command="",
        docker_command=str(fake_docker),
        docker_image="vabench-agent-runtime:test-commit",
        submission_gate=artifact_gate,
    )

    environment.preflight()
    result = environment.execute({"command": "printf hello"})
    serialized = environment.serialize()
    environment.close()

    assert result["returncode"] == 0
    assert "hello from shared docker" in result["output"]
    assert serialized["info"]["config"]["environment"]["image_id"] == (
        "sha256:shared-environment"
    )
    calls = log.read_text(encoding="utf-8")
    assert "--network=none" in calls
    assert "dst=/workspace/public/task,readonly" in calls
    assert "dst=/workspace/public/skills,readonly" in calls
    assert "dst=/workspace/public/submission" in calls
    assert "dst=/workspace/work" in calls
    assert "exec -i" in calls
    assert "/usr/bin/timeout --signal=TERM --kill-after=1s" in calls
    assert "rm -f" in calls


def test_docker_preflight_retries_one_timeout_with_configured_deadline(
    tmp_path: Path,
) -> None:
    module = load_module()
    runtime = tmp_path / "runtime"
    (runtime / "public" / "task").mkdir(parents=True)
    (runtime / "public" / "task" / "instruction.md").write_text("public task")
    (runtime / "public" / "submission").mkdir(parents=True)
    marker = tmp_path / "first-exec"
    fake_docker = tmp_path / "docker"
    fake_docker.write_text(
        "#!/bin/sh\n"
        "case \"$1 $2\" in\n"
        "  'image inspect') echo 'sha256:shared-environment' ;;\n"
        "  'create --name') echo 'vabench-test-container' ;;\n"
        "  'exec -i')\n"
        f"    if [ ! -e {shlex.quote(str(marker))} ]; then\n"
        f"      : > {shlex.quote(str(marker))}\n"
        "      sleep 1\n"
        "    fi\n"
        "    ;;\n"
        "esac\n",
        encoding="utf-8",
    )
    fake_docker.chmod(0o755)
    environment = module.VaBenchBashEnvironment(
        runtime,
        timeout_s=5,
        sandbox_backend="docker",
        evas_command="",
        docker_command=str(fake_docker),
        docker_image="vabench-agent-runtime:test-commit",
        preflight_timeout_s=0.1,
        preflight_attempts=2,
        submission_gate=artifact_gate,
    )

    try:
        environment.preflight()
        serialized = environment.serialize()["info"]["config"]["environment"]
    finally:
        environment.close()

    assert serialized["preflight_timeout_s"] == 0.1
    assert serialized["preflight_attempts"] == 2
    assert serialized["preflight_attempts_used"] == 2


def test_docker_startup_limiter_serializes_only_preflight(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    module = load_module()
    limiter = threading.BoundedSemaphore(1)
    active = 0
    maximum_active = 0
    lock = threading.Lock()

    def fake_ensure(_self) -> None:
        nonlocal active, maximum_active
        if _self._docker_container is not None:
            return
        with lock:
            active += 1
            maximum_active = max(maximum_active, active)
        _self._docker_container = "vabench-test-container"
        time.sleep(0.03)

    def fake_probe(*_args, **_kwargs):
        nonlocal active
        time.sleep(0.03)
        with lock:
            active -= 1
        return subprocess.CompletedProcess([], 0, "")

    monkeypatch.setattr(module.VaBenchBashEnvironment, "_ensure_docker_container", fake_ensure)
    monkeypatch.setattr(module.subprocess, "run", fake_probe)
    environments = []
    for index in range(2):
        runtime = tmp_path / f"runtime-{index}"
        (runtime / "public" / "task").mkdir(parents=True)
        (runtime / "public" / "task" / "instruction.md").write_text("public task")
        (runtime / "public" / "submission").mkdir(parents=True)
        environments.append(
            module.VaBenchBashEnvironment(
                runtime,
                timeout_s=5,
                sandbox_backend="docker",
                evas_command="",
                docker_image="vabench-agent-runtime:test-commit",
                startup_limiter=limiter,
                submission_gate=artifact_gate,
            )
        )

    threads = [threading.Thread(target=environment.preflight) for environment in environments]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert maximum_active == 1
    assert limiter.acquire(blocking=False)
    limiter.release()


def test_public_runtime_mounts_a_spaced_skill_path_as_one_readonly_argument(
    tmp_path: Path,
) -> None:
    task = tmp_path / "task input"
    submission = tmp_path / "submission output"
    work = tmp_path / "work output"
    skills = tmp_path / "skill packages"
    for directory in (task, submission, work, skills):
        directory.mkdir()
    log = tmp_path / "docker-arguments.log"
    fake_docker = tmp_path / "fake-docker"
    fake_docker.write_text(
        "#!/bin/sh\n"
        f"printf '%s\\n' \"$@\" > {shlex.quote(str(log))}\n",
        encoding="utf-8",
    )
    fake_docker.chmod(0o755)
    env = os.environ.copy()
    env.update({
        "DOCKER": str(fake_docker),
        "VABENCH_SKILLS_DIR": str(skills),
    })

    subprocess.run(
        [str(PUBLIC_RUNTIME), str(task), str(submission), str(work), "/bin/true"],
        cwd=ROOT,
        env=env,
        check=True,
    )

    arguments = log.read_text(encoding="utf-8").splitlines()
    skill_mounts = [
        argument
        for argument in arguments
        if "dst=/workspace/public/skills" in argument
    ]
    assert skill_mounts == [
        f"--mount=type=bind,src={skills.resolve()},dst=/workspace/public/skills,readonly"
    ]


def test_bash_output_capture_is_bounded(tmp_path: Path) -> None:
    module = load_module()
    runtime = tmp_path / "runtime"
    (runtime / "public" / "task").mkdir(parents=True)
    (runtime / "public" / "submission").mkdir(parents=True)
    environment = module.VaBenchBashEnvironment(
        runtime,
        timeout_s=10,
        sandbox_backend="none",
        evas_command="/usr/bin/true",
        submission_gate=artifact_gate,
    )

    result = environment.execute(
        {"command": "yes x | head -c 2097152; printf 'TAIL-SENTINEL\\n'"}
    )

    assert result["returncode"] == 0
    assert result["output_total_bytes"] > module.COMMAND_OUTPUT_CAPTURE_BYTES
    assert result["output_captured_bytes"] == module.COMMAND_OUTPUT_CAPTURE_BYTES
    assert result["output_truncated_bytes"] > 0
    assert len(result["output"].encode()) < 13_000
    assert "TAIL-SENTINEL" in result["output"]
    assert "omitted" in result["output"]


def test_workspace_quota_is_reported_as_resource_exhaustion(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    module = load_module()
    monkeypatch.setattr(module, "SUBMISSION_QUOTA_BYTES", 8)
    runtime = tmp_path / "runtime"
    (runtime / "public" / "task").mkdir(parents=True)
    (runtime / "public" / "submission").mkdir(parents=True)
    environment = module.VaBenchBashEnvironment(
        runtime,
        timeout_s=10,
        sandbox_backend="none",
        evas_command="/usr/bin/true",
        submission_gate=artifact_gate,
    )

    result = environment.execute(
        {"command": "printf 123456789 > public/submission/extra.va"}
    )

    assert result["returncode"] == 125
    assert result["exception_info"] == "agent workspace quota exceeded"
    assert result["resources"]["exceeded"] == ["submission"]
    assert environment.commands[-1]["resources"]["submission_bytes"] == 9


def test_shared_docker_image_executes_real_adapter_contract(tmp_path: Path) -> None:
    if os.environ.get("VABENCH_TEST_DOCKER_RUNTIME") != "1":
        pytest.skip("real shared-image test is enabled by public-agent-runtime CI")
    module = load_module()
    runtime = tmp_path / "runtime"
    (runtime / "public" / "task").mkdir(parents=True)
    (runtime / "public" / "task" / "instruction.md").write_text("public task")
    (runtime / "public" / "submission").mkdir(parents=True)
    environment = module.VaBenchBashEnvironment(
        runtime,
        timeout_s=30,
        sandbox_backend="docker",
        evas_command="",
        docker_image=os.environ.get(
            "VABENCH_TEST_DOCKER_IMAGE", module.DEFAULT_DOCKER_IMAGE
        ),
        candidate_artifacts=["model.va"],
        submission_gate=artifact_gate,
    )
    try:
        environment.preflight()
        result = environment.execute(
            {
                "command": (
                    "printf 'module model; endmodule\\n' > public/submission/model.va "
                    "&& evas --version --format json"
                )
            }
        )
        serialized = environment.serialize()["info"]["config"]["environment"]
    finally:
        environment.close()

    assert result["returncode"] == 0
    assert '"package_version":"0.8.5"' in result["output"].replace(" ", "")
    assert serialized["image_id"].startswith("sha256:")
    assert (runtime / "public" / "submission" / "model.va").is_file()
    assert len(environment.evas_invocations) == 1
    assert len(environment.evas_invocations[0]["candidate_tree_sha256"]) == 64
    assert environment.evas_invocations[0][
        "candidate_tree_schema_version"
    ] == module.CANDIDATE_TREE_SCHEMA_VERSION


def test_shared_no_evas_image_has_no_evas_capability(tmp_path: Path) -> None:
    if os.environ.get("VABENCH_TEST_DOCKER_RUNTIME") != "1":
        pytest.skip("real shared-image test is enabled by public-agent-runtime CI")
    module = load_module()
    runtime = tmp_path / "runtime"
    (runtime / "public" / "task").mkdir(parents=True)
    (runtime / "public" / "task" / "instruction.md").write_text("public task")
    (runtime / "public" / "submission").mkdir(parents=True)
    environment = module.VaBenchBashEnvironment(
        runtime,
        timeout_s=30,
        sandbox_backend="docker",
        evas_command="",
        executable_feedback=False,
        docker_image=os.environ.get(
            "VABENCH_TEST_NO_EVAS_DOCKER_IMAGE",
            module.DEFAULT_NO_EVAS_DOCKER_IMAGE,
        ),
        submission_gate=artifact_gate,
    )
    try:
        environment.preflight()
        result = environment.execute(
            {
                "command": (
                    "! command -v evas && "
                    "python3 -c 'import importlib.util; "
                    "assert importlib.util.find_spec(\"evas\") is None' && "
                    "printf 'module model; endmodule\\n' > public/submission/model.va"
                )
            }
        )
        serialized = environment.serialize()["info"]["config"]["environment"]
    finally:
        environment.close()

    assert result["returncode"] == 0
    assert serialized["executable_feedback"] is False
    assert serialized["image_id"].startswith("sha256:")
    assert (runtime / "public" / "submission" / "model.va").is_file()


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


def test_consecutive_evas_calls_record_the_same_candidate_tree_hash(
    tmp_path: Path,
) -> None:
    module = load_module()
    runtime = tmp_path / "runtime"
    (runtime / "public" / "task").mkdir(parents=True)
    submission = runtime / "public" / "submission"
    submission.mkdir(parents=True)
    (submission / "model.va").write_text(
        "module model; endmodule\n", encoding="utf-8"
    )
    environment = module.VaBenchBashEnvironment(
        runtime,
        timeout_s=5,
        sandbox_backend="none",
        evas_command="/usr/bin/true",
        candidate_artifacts=["model.va"],
        submission_gate=artifact_gate,
    )

    result = environment.execute({"command": "evas --version && evas --version"})

    assert result["returncode"] == 0
    assert len(environment.evas_invocations) == 2
    hashes = [
        invocation["candidate_tree_sha256"]
        for invocation in environment.evas_invocations
    ]
    assert len(hashes[0]) == 64
    assert hashes == [hashes[0], hashes[0]]


def test_compound_command_hashes_candidate_at_each_evas_start(
    tmp_path: Path,
) -> None:
    module = load_module()
    runtime = tmp_path / "runtime"
    (runtime / "public" / "task").mkdir(parents=True)
    (runtime / "public" / "submission").mkdir(parents=True)
    environment = module.VaBenchBashEnvironment(
        runtime,
        timeout_s=5,
        sandbox_backend="none",
        evas_command="/usr/bin/true",
        candidate_artifacts=["model.va"],
        submission_gate=artifact_gate,
    )

    result = environment.execute(
        {
            "command": (
                "printf A > public/submission/model.va; "
                "evas --version; "
                "printf B > public/submission/model.va; "
                "evas --version"
            )
        }
    )

    assert result["returncode"] == 0
    hashes = [
        invocation["candidate_tree_sha256"]
        for invocation in environment.evas_invocations
    ]
    assert len(hashes) == 2
    assert hashes[0] != hashes[1]


def test_multi_file_candidate_hash_changes_when_one_declared_artifact_changes(
    tmp_path: Path,
) -> None:
    module = load_module()
    runtime = tmp_path / "runtime"
    (runtime / "public" / "task").mkdir(parents=True)
    submission = runtime / "public" / "submission"
    submission.mkdir(parents=True)
    (submission / "model.va").write_text("model-a", encoding="utf-8")
    (submission / "support.va").write_text("support-a", encoding="utf-8")
    environment = module.VaBenchBashEnvironment(
        runtime,
        timeout_s=5,
        sandbox_backend="none",
        evas_command="/usr/bin/true",
        candidate_artifacts=["support.va", "model.va"],
        submission_gate=artifact_gate,
    )

    result = environment.execute(
        {
            "command": (
                "evas --version; "
                "printf support-b > public/submission/support.va; "
                "evas --version"
            )
        }
    )

    assert result["returncode"] == 0
    first, second = environment.evas_invocations
    assert first["candidate_tree_sha256"] != second["candidate_tree_sha256"]

    mirror_runtime = tmp_path / "mirror-runtime"
    (mirror_runtime / "public" / "task").mkdir(parents=True)
    mirror_submission = mirror_runtime / "public" / "submission"
    mirror_submission.mkdir(parents=True)
    (mirror_submission / "model.va").write_text("model-a", encoding="utf-8")
    (mirror_submission / "support.va").write_text(
        "support-a", encoding="utf-8"
    )
    mirror = module.VaBenchBashEnvironment(
        mirror_runtime,
        timeout_s=5,
        sandbox_backend="none",
        evas_command="/usr/bin/true",
        candidate_artifacts=["model.va", "support.va"],
        submission_gate=artifact_gate,
    )
    mirror.execute({"command": "evas --version"})
    assert (
        first["candidate_tree_sha256"]
        == mirror.evas_invocations[0]["candidate_tree_sha256"]
    )


def test_rewriting_declared_artifact_with_same_bytes_preserves_candidate_hash(
    tmp_path: Path,
) -> None:
    module = load_module()
    runtime = tmp_path / "runtime"
    (runtime / "public" / "task").mkdir(parents=True)
    submission = runtime / "public" / "submission"
    submission.mkdir(parents=True)
    (submission / "model.va").write_bytes(b"same-bytes")
    environment = module.VaBenchBashEnvironment(
        runtime,
        timeout_s=5,
        sandbox_backend="none",
        evas_command="/usr/bin/true",
        candidate_artifacts=["model.va"],
        submission_gate=artifact_gate,
    )

    result = environment.execute(
        {
            "command": (
                "evas --version; "
                "printf same-bytes > public/submission/model.va; "
                "evas --version"
            )
        }
    )

    assert result["returncode"] == 0
    first, second = environment.evas_invocations
    assert first["candidate_tree_sha256"] == second["candidate_tree_sha256"]


def test_empty_and_missing_declared_artifacts_have_stable_hashes(
    tmp_path: Path,
) -> None:
    module = load_module()

    def run_twice(name: str, artifacts: list[str]) -> list[str]:
        runtime = tmp_path / name
        (runtime / "public" / "task").mkdir(parents=True)
        (runtime / "public" / "submission").mkdir(parents=True)
        environment = module.VaBenchBashEnvironment(
            runtime,
            timeout_s=5,
            sandbox_backend="none",
            evas_command="/usr/bin/true",
            candidate_artifacts=artifacts,
            submission_gate=artifact_gate,
        )
        result = environment.execute(
            {"command": "evas --version && evas --version"}
        )
        assert result["returncode"] == 0
        return [
            invocation["candidate_tree_sha256"]
            for invocation in environment.evas_invocations
        ]

    missing_hashes = run_twice("missing", ["model.va"])
    empty_hashes = run_twice("empty", [])

    assert missing_hashes[0] == missing_hashes[1]
    assert empty_hashes[0] == empty_hashes[1]
    assert missing_hashes[0] != empty_hashes[0]


def test_candidate_hash_excludes_work_evas_output_and_private_assets(
    tmp_path: Path,
) -> None:
    module = load_module()
    runtime = tmp_path / "runtime"
    (runtime / "public" / "task").mkdir(parents=True)
    submission = runtime / "public" / "submission"
    submission.mkdir(parents=True)
    (submission / "model.va").write_text("candidate", encoding="utf-8")
    private = runtime / "evaluator" / "secret.txt"
    private.parent.mkdir(parents=True)
    private.write_text("private-a", encoding="utf-8")
    environment = module.VaBenchBashEnvironment(
        runtime,
        timeout_s=5,
        sandbox_backend="none",
        evas_command="/usr/bin/true",
        candidate_artifacts=["model.va"],
        submission_gate=artifact_gate,
    )
    work_file = runtime / "public" / "work" / "scratch.txt"
    output_file = runtime / "public" / "evas-output" / "tran.csv"
    work_file.write_text("work-a", encoding="utf-8")
    output_file.write_text("output-a", encoding="utf-8")

    first = environment.execute({"command": "evas --version"})
    private.write_text("private-b", encoding="utf-8")
    work_file.write_text("work-b", encoding="utf-8")
    output_file.write_text("output-b", encoding="utf-8")
    second = environment.execute({"command": "evas --version"})

    assert first["returncode"] == second["returncode"] == 0
    first_invocation, second_invocation = environment.evas_invocations
    assert (
        first_invocation["candidate_tree_sha256"]
        == second_invocation["candidate_tree_sha256"]
    )
    assert not any(
        "waveform" in key or "log" in key
        for key in first_invocation
    )


def test_candidate_hash_does_not_follow_symlinks_into_private_assets(
    tmp_path: Path,
) -> None:
    module = load_module()
    runtime = tmp_path / "runtime"
    (runtime / "public" / "task").mkdir(parents=True)
    submission = runtime / "public" / "submission"
    submission.mkdir(parents=True)
    private = runtime / "evaluator" / "secret.txt"
    private.parent.mkdir(parents=True)
    private.write_text("private-a", encoding="utf-8")
    (submission / "model.va").symlink_to(private)
    environment = module.VaBenchBashEnvironment(
        runtime,
        timeout_s=5,
        sandbox_backend="none",
        evas_command="/usr/bin/true",
        candidate_artifacts=["model.va"],
        submission_gate=artifact_gate,
    )

    environment.execute({"command": "evas --version"})
    private.write_text("private-b", encoding="utf-8")
    environment.execute({"command": "evas --version"})

    first, second = environment.evas_invocations
    assert first["candidate_tree_sha256"] == second["candidate_tree_sha256"]


@pytest.mark.parametrize(
    "candidate_path",
    ["../evaluator/secret.txt", "/absolute/model.va"],
)
def test_candidate_hash_rejects_paths_outside_declared_submission_root(
    tmp_path: Path,
    candidate_path: str,
) -> None:
    module = load_module()
    runtime = tmp_path / "runtime"
    (runtime / "public" / "task").mkdir(parents=True)

    with pytest.raises(ValueError, match="unsafe candidate artifact path"):
        module.VaBenchBashEnvironment(
            runtime,
            timeout_s=5,
            sandbox_backend="none",
            evas_command="/usr/bin/true",
            candidate_artifacts=[candidate_path],
            submission_gate=artifact_gate,
        )


def test_waveform_cli_and_agentic_wave_arm_are_not_exposed(
    tmp_path: Path,
) -> None:
    module = load_module()
    runtime = tmp_path / "runtime"
    (runtime / "public" / "task").mkdir(parents=True)
    environment = module.VaBenchBashEnvironment(
        runtime,
        timeout_s=5,
        sandbox_backend="none",
        evas_command="/usr/bin/true",
        candidate_artifacts=["model.va"],
        submission_gate=artifact_gate,
    )
    executable_tools = sorted(
        path.name
        for path in environment.tools_dir.iterdir()
        if path.is_file() and os.access(path, os.X_OK)
    )
    campaign_sources = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (
            MODULE.parent / "build_campaign.py",
            MODULE.parent / "run_campaign.py",
        )
    )

    assert executable_tools == ["evas", "vabench-submit"]
    assert "vabench-waveform" not in (
        module.SYSTEM_PROMPT + module.BASH_CONTRACT + campaign_sources
    )
    assert "Agentic-Wave" not in campaign_sources


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


def test_auto_selects_shared_docker_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    module = load_module()
    monkeypatch.setattr(
        module.shutil,
        "which",
        lambda name: "/usr/bin/docker" if name == "docker" else None,
    )

    assert module.default_sandbox_backend() == "docker"


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
