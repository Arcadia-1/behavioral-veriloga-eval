from __future__ import annotations

import json
from pathlib import Path

from runners.vabench_release_paths import release_form_dir


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "benchmark-vabench-release-v1"
REPORT = PACKAGE / "reports" / "schema_validation.json"
TASK_SYNC = PACKAGE / "reports" / "release_task_manifest_sync.json"


def test_release_schema_validation_covers_all_release_json_surfaces() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    groups = {item["schema"]: item for item in report["validations"]}

    assert report["status"] == "pass"
    assert report["issue_count"] == 0
    assert report["count_issue_count"] == 0
    assert groups["package_manifest"]["file_count"] == 1
    assert groups["evaluator_contract"]["file_count"] == 1
    assert groups["speed_debug_artifact"]["file_count"] == 1
    assert groups["baseline_artifact"]["file_count"] == 1
    assert groups["paper_artifacts"]["file_count"] == 1
    assert groups["claim_gate"]["file_count"] == 1
    assert groups["score_denominator"]["file_count"] == 1
    assert groups["dual_rerun_queue"]["file_count"] == 1
    assert groups["dual_rerun_staging"]["file_count"] == 1
    assert groups["dual_rerun_import"]["file_count"] == 1
    assert groups["bridge_diagnostics"]["file_count"] == 1
    assert groups["external_blockers"]["file_count"] == 1
    assert groups["finish_readiness"]["file_count"] == 1
    assert groups["completion_audit"]["file_count"] == 1
    assert groups["finish_after_bridge_attempt"]["file_count"] in {0, 1}
    assert groups["conformance_manifest"]["file_count"] == 1
    assert groups["artifact_index"]["file_count"] == 1
    assert groups["checksum_manifest"]["file_count"] == 1
    assert groups["paper_tables"]["file_count"] == 1
    assert groups["release_task_manifest_sync"]["file_count"] == 1
    assert groups["release_status"]["file_count"] == 1
    assert groups["asset_integrity"]["file_count"] == 1
    assert groups["static_certification"]["file_count"] == 1
    assert groups["dual_certification"]["file_count"] == 1
    assert groups["certification_matrix"]["file_count"] == 1
    assert groups["remaining_work"]["file_count"] == 1
    assert groups["release_entry"]["file_count"] == 86
    assert groups["release_task"]["file_count"] == 300
    assert groups["evidence"]["file_count"] == 542
    assert groups["result"]["file_count"] == 813


def test_release_task_manifest_sync_writes_one_manifest_per_materialized_form() -> None:
    report = json.loads(TASK_SYNC.read_text(encoding="utf-8"))
    manifests = sorted(PACKAGE.glob("tasks/*/vbr1_*/forms/*/release_task.json"))

    assert report["status"] == "pass"
    assert report["release_task_manifest_count"] == 271
    assert len(manifests) == 271
    sample = json.loads(manifests[0].read_text(encoding="utf-8"))
    assert sample["benchmark"] == "vabench-release-v1"
    assert sample["domain"] == "voltage"
    enabled = 0
    disabled = 0
    for manifest in manifests:
        payload = json.loads(manifest.read_text(encoding="utf-8"))
        assert payload["track"] in {"core", "support"}
        assert payload["difficulty"] in {"D1", "D2", "D3"}
        assert isinstance(payload["counts"]["benchmark_score"], bool)
        enabled += int(payload["counts"]["benchmark_score"] is True)
        disabled += int(payload["counts"]["benchmark_score"] is False)
    assert enabled == 236
    assert disabled == 35


def test_designed_release_prompts_define_public_port_contracts() -> None:
    prompt = (
        release_form_dir(PACKAGE / "tasks", "vbr1_l1_loop_filter_abstraction", "dut") / "prompt.md"
    ).read_text(encoding="utf-8")

    assert "Public port contract:" in prompt
    assert "module loop_filter_abstraction(clk, rst, vin, out, metric);" in prompt
    assert "input clk, rst, vin;" in prompt
    assert "output out, metric;" in prompt
    assert "electrical clk, rst, vin, out, metric" in prompt
    assert "Saved waveform columns:" in prompt


def test_designed_bugfix_meta_separates_public_input_from_reference_solution() -> None:
    meta = json.loads(
        (release_form_dir(PACKAGE / "tasks", "vbr1_l1_loop_filter_abstraction", "bugfix") / "meta.json").read_text(
            encoding="utf-8"
        )
    )

    assert meta["inputs"] == ["prompt.md", "gold/dut_buggy.va"]
    assert meta["artifacts"] == ["dut_fixed.va"]
    assert meta["public_inputs"] == ["prompt.md", "gold/dut_buggy.va"]
    assert meta["submission_artifacts"] == ["dut_fixed.va"]
    assert meta["private_reference_artifacts"] == ["gold/dut_fixed.va"]

    release_task = json.loads(
        (
            release_form_dir(PACKAGE / "tasks", "vbr1_l1_loop_filter_abstraction", "bugfix") / "release_task.json"
        ).read_text(encoding="utf-8")
    )
    artifacts = release_task["artifacts"]
    assert artifacts["public_inputs"] == ["prompt.md", "gold/dut_buggy.va"]
    assert artifacts["submission_artifacts"] == ["dut_fixed.va"]
    assert artifacts["private_reference_artifacts"] == ["gold/dut_fixed.va"]
