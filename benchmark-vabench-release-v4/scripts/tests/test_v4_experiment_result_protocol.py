from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys

import jsonschema
import pytest


ROOT = Path(__file__).resolve().parents[3]
PILOT = ROOT / "benchmark-vabench-release-v4" / "operations" / "calibration_pilot"
SCHEMA = ROOT / "schemas" / "vabench-experiment-result.schema.json"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PROTOCOL = load_module("v4_result_protocol_test", PILOT / "result_protocol.py")
RUNNER = load_module("v4_campaign_runner_test", PILOT / "run_campaign.py")
SCORER = load_module("v4_campaign_scorer_test", PILOT / "score_campaign.py")


def runtime_with_submission(tmp_path: Path) -> Path:
    runtime = tmp_path / "runtime"
    (runtime / "evaluator").mkdir(parents=True)
    (runtime / "public" / "submission").mkdir(parents=True)
    (runtime / "evaluator" / "score_policy.json").write_text(
        json.dumps({"candidate_artifacts": ["candidate.va"]}), encoding="utf-8"
    )
    (runtime / "evaluator" / "visible_test.scs").write_text("tran tran stop=1n\n")
    (runtime / "public" / "submission" / "candidate.va").write_text(
        "module candidate; endmodule\n", encoding="utf-8"
    )
    return runtime


@pytest.mark.parametrize("mode", [f"G{index}" for index in range(6)])
def test_all_modes_preserve_raw_final_and_artifact_snapshot(
    tmp_path: Path, mode: str
) -> None:
    runtime = runtime_with_submission(tmp_path)
    gate = RUNNER.submission_artifact_gate(runtime)
    replay = PROTOCOL.trusted_replay(
        None,
        None,
        PROTOCOL.hash_test_tree(runtime / "evaluator"),
        {"available": True, "version_output": "evas 1.2.3", "sha256": "a" * 64},
    )
    message = {"role": "assistant", "content": f"final output for {mode}"}
    record = PROTOCOL.build_experiment_result(
        cell={"cell_id": f"v4-001-{mode}-r01", "task_id": "v4-001", "mode": mode},
        model_status="completed",
        messages=[{"role": "user", "content": "task"}, message],
        artifact_gate=gate,
        runtime=runtime,
        replay=replay,
    )

    # The system image ships an older jsonschema package; this schema uses a
    # Draft 7-compatible subset even though its public declaration is 2020-12.
    jsonschema.Draft7Validator(json.loads(SCHEMA.read_text())).validate(record)
    assert record["schema_version"] == "vabench-experiment-result-v2"
    assert (
        record["failure_taxonomy"]["schema_version"]
        == "vabench-failure-taxonomy-v1"
    )
    assert record["model_execution"]["raw_final_output"]["message"] == message
    artifact = record["final_submission"]["artifacts"][0]
    snapshot = runtime / artifact["snapshot_path"]
    original = snapshot.read_bytes()
    (runtime / "public" / "submission" / "candidate.va").write_text("changed\n")
    assert snapshot.read_bytes() == original


@pytest.mark.parametrize(
    "status",
    ["compile_failure", "runtime_failure", "behavior_failure"],
)
def test_structured_replay_preserves_failure_stage(status: str) -> None:
    replay = PROTOCOL.trusted_replay(
        {"execution_status": "completed", "returncode": 7},
        {"status": status, "diagnostics": ["specific failure"]},
        {"file_count": 1, "tree_sha256": "b" * 64, "files": []},
        {"available": True, "version_output": "evas test"},
    )
    assert replay["status"] == status


def test_behavior_failure_preserves_structured_failure_taxonomy() -> None:
    replay = PROTOCOL.trusted_replay(
        {"execution_status": "completed", "returncode": 7},
        {
            "status": "behavior_failure",
            "diagnostics": ["slew_limit violated"],
            "failure_taxonomy": {
                "primary_class": "property",
                "secondary_classes": ["functional"],
                "stage": "property_check",
                "responsibility": "candidate",
                "retryable": False,
                "case_ids": ["corner-fast"],
                "property_ids": ["slew_limit"],
                "mutation_ids": [],
            },
        },
        {"file_count": 1, "tree_sha256": "b" * 64, "files": []},
        {"available": True, "version_output": "evas test"},
    )

    assert replay["status"] == "behavior_failure"
    assert replay["failure_taxonomy"] == {
        "schema_version": "vabench-failure-taxonomy-v1",
        "primary_class": "property",
        "secondary_classes": ["functional"],
        "stage": "property_check",
        "responsibility": "candidate",
        "retryable": False,
        "case_ids": ["corner-fast"],
        "property_ids": ["slew_limit"],
        "mutation_ids": [],
    }


@pytest.mark.parametrize(
    ("failure_class", "stage"),
    [
        ("functional", "functional_check"),
        ("mutation_survival", "mutation_check"),
        ("property", "property_check"),
    ],
)
def test_behavior_failure_accepts_analysis_classes(
    failure_class: str, stage: str
) -> None:
    replay = PROTOCOL.trusted_replay(
        {"execution_status": "completed", "returncode": 7},
        {
            "status": "behavior_failure",
            "failure_taxonomy": {
                "primary_class": failure_class,
                "stage": stage,
                "responsibility": "candidate",
                "retryable": False,
            },
        },
        {"file_count": 1, "tree_sha256": "b" * 64, "files": []},
        {"available": True, "version_output": "evas test"},
    )

    assert replay["status"] == "behavior_failure"
    assert replay["failure_taxonomy"]["primary_class"] == failure_class
    assert replay["failure_taxonomy"]["stage"] == stage


def test_experiment_result_uses_final_replay_failure_taxonomy(
    tmp_path: Path,
) -> None:
    runtime = runtime_with_submission(tmp_path)
    replay = PROTOCOL.trusted_replay(
        {"execution_status": "completed", "returncode": 7},
        {
            "status": "behavior_failure",
            "failure_taxonomy": {
                "primary_class": "mutation_survival",
                "stage": "mutation_check",
                "responsibility": "candidate",
                "retryable": False,
                "mutation_ids": ["stuck-high"],
            },
        },
        PROTOCOL.hash_test_tree(runtime / "evaluator"),
        {"available": True, "version_output": "evas test"},
    )
    record = PROTOCOL.build_experiment_result(
        cell={"cell_id": "v4-001-G2-r01", "task_id": "v4-001", "mode": "G2"},
        model_status="completed",
        messages=[],
        artifact_gate=RUNNER.submission_artifact_gate(runtime),
        runtime=runtime,
        replay=replay,
    )

    assert record["failure_taxonomy"] == replay["failure_taxonomy"]
    assert record["failure_taxonomy"]["mutation_ids"] == ["stuck-high"]
    jsonschema.Draft7Validator(json.loads(SCHEMA.read_text())).validate(record)


@pytest.mark.parametrize(
    ("command", "adapter_result", "expected_class", "expected_stage"),
    [
        (
            {"execution_status": "completed", "returncode": 2},
            {"status": "compile_failure"},
            "compile",
            "compilation",
        ),
        (
            {"execution_status": "completed", "returncode": 3},
            {"status": "runtime_failure"},
            "runtime",
            "simulation",
        ),
        (
            {"execution_status": "completed", "returncode": 4},
            {"status": "behavior_failure"},
            "behavior_unspecified",
            "behavior_check",
        ),
        (
            {"execution_status": "timeout", "returncode": None},
            None,
            "timeout",
            "simulation",
        ),
        (
            {"execution_status": "completed", "returncode": 0},
            {"status": "passed"},
            None,
            "completed",
        ),
    ],
)
def test_replay_derives_default_failure_taxonomy(
    command: dict,
    adapter_result: dict | None,
    expected_class: str | None,
    expected_stage: str,
) -> None:
    replay = PROTOCOL.trusted_replay(
        command,
        adapter_result,
        {"file_count": 1, "tree_sha256": "b" * 64, "files": []},
        {"available": True, "version_output": "evas test"},
    )

    assert replay["failure_taxonomy"]["primary_class"] == expected_class
    assert replay["failure_taxonomy"]["stage"] == expected_stage


def test_incompatible_adapter_failure_taxonomy_is_infrastructure_failure() -> None:
    replay = PROTOCOL.trusted_replay(
        {"execution_status": "completed", "returncode": 7},
        {
            "status": "behavior_failure",
            "failure_taxonomy": {
                "primary_class": "compile",
                "stage": "compilation",
                "responsibility": "candidate",
                "retryable": False,
            },
        },
        {"file_count": 1, "tree_sha256": "b" * 64, "files": []},
        {"available": True, "version_output": "evas test"},
    )

    assert replay["status"] == "infrastructure_failure"
    assert replay["failure_taxonomy"]["primary_class"] == "infrastructure"
    assert replay["failure_taxonomy"]["retryable"] is True
    assert "invalid_failure_taxonomy" in replay["diagnostics"]
    assert (
        replay["adapter_result"]["failure_taxonomy"]["primary_class"]
        == "compile"
    )


@pytest.mark.parametrize(
    "override",
    [
        {"stage": "compilation"},
        {"responsibility": "system"},
        {"retryable": True},
    ],
)
def test_inconsistent_behavior_failure_metadata_is_rejected(
    override: dict,
) -> None:
    taxonomy = {
        "primary_class": "property",
        "stage": "property_check",
        "responsibility": "candidate",
        "retryable": False,
    }
    taxonomy.update(override)
    replay = PROTOCOL.trusted_replay(
        {"execution_status": "completed", "returncode": 7},
        {
            "status": "behavior_failure",
            "failure_taxonomy": taxonomy,
        },
        {"file_count": 1, "tree_sha256": "b" * 64, "files": []},
        {"available": True, "version_output": "evas test"},
    )

    assert replay["status"] == "infrastructure_failure"
    assert "invalid_failure_taxonomy" in replay["diagnostics"]


def test_unstructured_nonzero_replay_is_not_behavior_failure() -> None:
    replay = PROTOCOL.trusted_replay(
        {"execution_status": "completed", "returncode": 1},
        None,
        {"file_count": 0, "tree_sha256": "c" * 64, "files": []},
        {"available": False},
    )
    assert replay["status"] == "infrastructure_failure"
    assert "missing_structured" in replay["diagnostics"][0]


def test_complete_workspace_at_timeout_awaits_replay(tmp_path: Path) -> None:
    runtime = runtime_with_submission(tmp_path)
    record = PROTOCOL.build_experiment_result(
        cell={"cell_id": "v4-001-G4-r01", "task_id": "v4-001", "mode": "G4"},
        model_status="agent_timeout",
        messages=[{"role": "assistant", "content": "partial final"}],
        artifact_gate=RUNNER.submission_artifact_gate(runtime),
        runtime=runtime,
        replay=PROTOCOL.trusted_replay(
            None,
            None,
            PROTOCOL.hash_test_tree(runtime / "evaluator"),
            {"available": False},
        ),
    )
    assert record["outcome"] == "not_scored"
    assert record["score_eligible"] is False
    assert record["score"] is None
    jsonschema.Draft7Validator(json.loads(SCHEMA.read_text())).validate(record)


def test_agent_resource_exhaustion_has_no_score(tmp_path: Path) -> None:
    runtime = runtime_with_submission(tmp_path)
    record = PROTOCOL.build_experiment_result(
        cell={"cell_id": "v4-001-G4-r01", "task_id": "v4-001", "mode": "G4"},
        model_status="agent_resource_exhausted",
        messages=[{"role": "assistant", "content": "oversized workspace"}],
        artifact_gate=RUNNER.submission_artifact_gate(runtime),
        runtime=runtime,
        replay=PROTOCOL.trusted_replay(
            None,
            None,
            PROTOCOL.hash_test_tree(runtime / "evaluator"),
            {"available": False},
        ),
    )
    assert record["outcome"] == "agent_resource_exhausted"
    assert record["score_eligible"] is False
    assert record["score"] is None
    jsonschema.Draft7Validator(json.loads(SCHEMA.read_text())).validate(record)


@pytest.mark.parametrize(
    ("model_status", "expected_class", "expected_stage", "expected_responsibility"),
    [
        ("completed", "invalid", "artifact_gate", "candidate"),
        ("agent_timeout", "timeout", "model_execution", "model"),
        (
            "agent_resource_exhausted",
            "resource_exhaustion",
            "model_execution",
            "model",
        ),
        ("provider_failure", "infrastructure", "model_execution", "system"),
        ("runner_failure", "infrastructure", "model_execution", "system"),
    ],
)
def test_terminal_result_classifies_non_replay_failures(
    tmp_path: Path,
    model_status: str,
    expected_class: str,
    expected_stage: str,
    expected_responsibility: str,
) -> None:
    runtime = runtime_with_submission(tmp_path)
    (runtime / "public" / "submission" / "candidate.va").unlink()
    record = PROTOCOL.build_experiment_result(
        cell={"cell_id": "v4-001-G2-r01", "task_id": "v4-001", "mode": "G2"},
        model_status=model_status,
        messages=[],
        artifact_gate=RUNNER.submission_artifact_gate(runtime),
        runtime=runtime,
        replay=PROTOCOL.trusted_replay(
            None,
            None,
            PROTOCOL.hash_test_tree(runtime / "evaluator"),
            {"available": False},
        ),
    )

    taxonomy = record["failure_taxonomy"]
    assert taxonomy["primary_class"] == expected_class
    assert taxonomy["stage"] == expected_stage
    assert taxonomy["responsibility"] == expected_responsibility


def test_provider_failure_is_not_reported_as_no_submission(tmp_path: Path) -> None:
    runtime = runtime_with_submission(tmp_path)
    (runtime / "public" / "submission" / "candidate.va").unlink()
    record = PROTOCOL.build_experiment_result(
        cell={"cell_id": "v4-001-G0-r01", "task_id": "v4-001", "mode": "G0"},
        model_status="provider_failure",
        messages=[],
        artifact_gate=RUNNER.submission_artifact_gate(runtime),
        runtime=runtime,
        replay=PROTOCOL.trusted_replay(
            None, None, PROTOCOL.hash_test_tree(runtime / "evaluator"), {"available": False}
        ),
    )
    assert record["outcome"] == "infrastructure_failure"
    assert record["score"] is None


def test_command_timeout_is_recorded_without_exception(tmp_path: Path) -> None:
    runtime = runtime_with_submission(tmp_path)
    result = RUNNER.command_result(
        f'{sys.executable} -c "import time; time.sleep(2)"', runtime, 1
    )
    assert result["execution_status"] == "timeout"
    assert result["returncode"] is None


def test_trusted_replay_reads_adapter_result_and_evas_identity(tmp_path: Path) -> None:
    runtime = runtime_with_submission(tmp_path)
    final_submission = PROTOCOL.snapshot_submission(
        runtime, RUNNER.submission_artifact_gate(runtime)
    )
    adapter = tmp_path / "adapter.py"
    adapter.write_text(
        "import json, os, pathlib\n"
        "candidate = pathlib.Path(os.environ['VABENCH_SUBMISSION_DIR']) / 'candidate.va'\n"
        "status = 'behavior_failure' if candidate.is_file() else 'infrastructure_failure'\n"
        "json.dump({'status': status, 'diagnostics': ['mismatch']}, "
        "open(os.environ['VABENCH_TRUSTED_REPLAY_RESULT'], 'w'))\n"
        "raise SystemExit(30)\n",
        encoding="utf-8",
    )
    replay = RUNNER.run_trusted_replay(
        runtime, f"{sys.executable} {adapter}", 5, sys.executable, final_submission
    )
    assert replay["status"] == "behavior_failure"
    assert replay["submission_tree_sha256"] == final_submission["tree_sha256"]
    assert replay["test_manifest"]["file_count"] == 2
    assert replay["evas_identity"]["available"] is True


def test_score_report_does_not_turn_agent_timeout_into_test_zero(tmp_path: Path) -> None:
    runtime = runtime_with_submission(tmp_path)
    (runtime / "public" / "submission" / "candidate.va").unlink()
    result_path = runtime / "evidence" / "campaign_result.json"
    result_path.parent.mkdir(parents=True)
    experiment = PROTOCOL.build_experiment_result(
        cell={"cell_id": "v4-001-G5-r01", "task_id": "v4-001", "mode": "G5"},
        model_status="agent_timeout",
        messages=[],
        artifact_gate=RUNNER.submission_artifact_gate(runtime),
        runtime=runtime,
        replay=PROTOCOL.trusted_replay(
            None, None, PROTOCOL.hash_test_tree(runtime / "evaluator"), {"available": False}
        ),
    )
    result_path.write_text(json.dumps({
        "cell": {
            "cell_id": "v4-001-G5-r01",
            "family_id": "001",
            "task_id": "v4-001",
            "form": "dut",
            "mode": "G5",
        },
        "status": "agent_timeout",
        "experiment_result": experiment,
        "events": [],
    }))
    row = SCORER.evaluate_cell(result_path, None, 5)
    assert row["judge_status"] == "agent_timeout"
    assert row["outcome"] == "agent_timeout"
    assert row["failure_class"] == "timeout"
    assert row["failure_stage"] == "model_execution"
    assert experiment["score"] is None


def test_score_summary_aggregates_structured_failure_taxonomy() -> None:
    def row(
        arm: str,
        judge_status: str,
        failure_class: str | None,
        stage: str,
    ) -> dict:
        return {
            "form": "testbench",
            "mode": "G2",
            "experimental_arm": arm,
            "submission_status": "submitted",
            "judge_status": judge_status,
            "failure_class": failure_class,
            "failure_stage": stage,
            "failure_responsibility": (
                "none" if failure_class is None else "candidate"
            ),
            "failure_retryable": False,
            "failure_taxonomy": {
                "secondary_classes": (
                    ["functional"] if failure_class == "property" else []
                ),
                "case_ids": (
                    ["corner-fast"] if failure_class == "property" else []
                ),
                "property_ids": (
                    ["slew_limit"] if failure_class == "property" else []
                ),
                "mutation_ids": (
                    ["stuck-high"]
                    if failure_class == "mutation_survival"
                    else []
                ),
            },
            "incidents": [],
            "output_tokens": 1,
            "episode_elapsed_s": 1.0,
            "telemetry": {},
            "evas_usage": {},
        }

    report = SCORER.summarize(
        [
            row("Agentic", "behavior_failure", "property", "property_check"),
            row(
                "Agentic",
                "behavior_failure",
                "mutation_survival",
                "mutation_check",
            ),
            row("Agent-No-EVAS", "compile_failure", "compile", "compilation"),
            row("OneShot", "passed", None, "completed"),
        ],
        "final_spectre",
    )

    assert report["schema_version"] == "v4-calibration-score-report-v2"
    assert report["failure_classes"] == {
        "compile": 1,
        "mutation_survival": 1,
        "property": 1,
    }
    assert report["failure_stages"] == {
        "compilation": 1,
        "mutation_check": 1,
        "property_check": 1,
    }
    assert report["failure_breakdown"]["arm:Agentic"] == {
        "mutation_survival": 1,
        "property": 1,
    }
    assert report["failure_breakdown"]["arm:Agent-No-EVAS"] == {"compile": 1}
    assert report["secondary_failure_classes"] == {"functional": 1}
    assert report["failed_case_ids"] == {"corner-fast": 1}
    assert report["failed_property_ids"] == {"slew_limit": 1}
    assert report["failed_mutation_ids"] == {"stuck-high": 1}
