from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCORE_CAMPAIGN = (
    ROOT
    / "benchmark-vabench-release-v4"
    / "operations"
    / "calibration_pilot"
    / "score_campaign.py"
)


def load_score_campaign():
    spec = importlib.util.spec_from_file_location("score_campaign_under_test", SCORE_CAMPAIGN)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_result(run_root: Path) -> Path:
    result = run_root / "v4-001-G0-r00" / "evidence" / "campaign_result.json"
    result.parent.mkdir(parents=True)
    result.write_text(
        json.dumps(
            {
                "cell": {
                    "cell_id": "v4-001-G0-r00",
                    "family_id": "001",
                    "task_id": "v4-001",
                    "form": "testbench",
                    "mode": "G0",
                },
                "events": [],
                "finished_at": "2026-07-13T00:00:01+00:00",
                "output_tokens": 17,
                "started_at": "2026-07-13T00:00:00+00:00",
                "status": "submitted",
                "working_tokens": 17,
            }
        )
        + "\n",
        encoding="utf-8",
    )
    return result


def test_score_campaign_resolves_workspace_relative_runtime_and_judge_command(
    tmp_path: Path, monkeypatch
) -> None:
    module = load_score_campaign()
    run_root = tmp_path / "behavioral-veriloga-eval" / "results" / "score-smoke" / "run"
    write_result(run_root)
    fake_adapter = (
        tmp_path
        / "behavioral-veriloga-eval"
        / "benchmark-vabench-release-v4"
        / "operations"
        / "calibration_pilot"
        / "fake_adapter.py"
    )
    fake_adapter.parent.mkdir(parents=True)
    fake_adapter.write_text("# fake\n", encoding="utf-8")

    captured: dict[str, object] = {}

    def fake_command_result(command: str, runtime: Path, timeout_s: int) -> dict[str, object]:
        captured["command"] = command
        captured["runtime"] = runtime
        captured["timeout_s"] = timeout_s
        return {"returncode": 0, "stdout": "ok\n", "stderr": "", "elapsed_s": 0.0}

    monkeypatch.setattr(module.RUNNER, "command_result", fake_command_result)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "score_campaign.py",
            "--campaign-output",
            "behavioral-veriloga-eval/results/score-smoke/run",
            "--judge-kind",
            "feedback_evas",
            "--judge-command",
            "python3 behavioral-veriloga-eval/benchmark-vabench-release-v4/operations/calibration_pilot/fake_adapter.py",
            "--output",
            "behavioral-veriloga-eval/results/score-smoke/run/SCORE.json",
        ],
    )

    assert module.main() == 0

    runtime = captured["runtime"]
    assert isinstance(runtime, Path)
    assert runtime.is_absolute()
    assert runtime == run_root / "v4-001-G0-r00"
    command = str(captured["command"])
    assert str(fake_adapter.resolve()) in command
    report = json.loads((run_root / "SCORE.json").read_text(encoding="utf-8"))
    assert report["judge_statuses"] == {"pass": 1}


def test_score_campaign_resolves_readme_repo_relative_judge_command(
    tmp_path: Path, monkeypatch
) -> None:
    module = load_score_campaign()
    run_root = tmp_path / "run"
    write_result(run_root)
    captured: dict[str, object] = {}

    def fake_command_result(command: str, runtime: Path, timeout_s: int) -> dict[str, object]:
        captured["command"] = command
        captured["runtime"] = runtime
        return {"returncode": 0, "stdout": "ok\n", "stderr": "", "elapsed_s": 0.0}

    monkeypatch.setattr(module.RUNNER, "command_result", fake_command_result)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "score_campaign.py",
            "--campaign-output",
            "run",
            "--judge-kind",
            "feedback_evas",
            "--judge-command",
            "python3 benchmark-vabench-release-v4/operations/calibration_pilot/feedback_adapter.py",
        ],
    )

    assert module.main() == 0

    command = str(captured["command"])
    assert str(
        ROOT
        / "benchmark-vabench-release-v4"
        / "operations"
        / "calibration_pilot"
        / "feedback_adapter.py"
    ) in command


def test_score_campaign_requires_final_spectre_judge_command(tmp_path: Path, monkeypatch) -> None:
    module = load_score_campaign()
    run_root = tmp_path / "run"
    write_result(run_root)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "score_campaign.py",
            "--campaign-output",
            "run",
            "--judge-kind",
            "final_spectre",
        ],
    )

    try:
        module.main()
    except SystemExit as exc:
        assert "--judge-kind final_spectre requires --judge-command" in str(exc)
    else:
        raise AssertionError("final_spectre without a judge command should fail")
