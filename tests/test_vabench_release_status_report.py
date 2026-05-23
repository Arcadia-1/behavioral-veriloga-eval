from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "benchmark-vabench-release-v1"
REPORT = PACKAGE / "reports" / "release_status.json"
ENTRY_SCHEMA = ROOT / "schemas" / "vabench-release-entry.schema.json"


def release_entries() -> list[dict[str, object]]:
    return [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((PACKAGE / "tasks").glob("CT*/vbr1_*/release_entry.json"))
    ]


def test_release_entry_schema_covers_generated_seed_skeletons() -> None:
    schema = json.loads(ENTRY_SCHEMA.read_text(encoding="utf-8"))
    required = set(schema["required"])

    entries = release_entries()
    assert len(entries) == 72
    for entry in entries:
        assert required <= set(entry)
        assert entry["benchmark"] == "vabench-release-v1"
        assert entry["level"] in {"L1", "L2"}
        assert entry["counts"]["model_capability"] is False
        assert entry["counts"]["l0_conformance"] is False
        assert entry["counts"]["benchmark_score"] is True
        if entry["release_tasks"]:
            assert entry["certification"]["static"] == "pass"
        else:
            assert entry["certification"]["static"] == "fail"
            assert "source_materialization" in entry["release_blockers"]
        assert entry["certification"]["evas"] in {"pass", "pending"}
        assert entry["certification"]["spectre"] in {"pass", "pending"}
        assert entry["certification"]["evidence"] == "benchmark-vabench-release-v1/reports/dual_certification.json"
        assert all(release_task["static_status"] == "pass" for release_task in entry["release_tasks"])
        assert all((ROOT / release_task["static_evidence"]).exists() for release_task in entry["release_tasks"])
        assert all((ROOT / release_task["static_result"]).exists() for release_task in entry["release_tasks"])
        assert all(release_task["evas_status"] in {"pass", "pending"} for release_task in entry["release_tasks"])
        assert all(release_task["spectre_status"] in {"pass", "pending"} for release_task in entry["release_tasks"])
        assert all((ROOT / release_task["dual_evidence"]).exists() for release_task in entry["release_tasks"])
        for release_task in entry["release_tasks"]:
            assert release_task["asset_materialized"] is True
            assert (ROOT / release_task["prompt"]).exists()
            assert (ROOT / release_task["meta"]).exists()
            assert (ROOT / release_task["checks"]).exists()
            assert release_task["gold"]


def test_release_status_report_is_conservative() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))

    assert report["planned_entries"] == 72
    assert report["level_counts"] == {"L1": 56, "L2": 16}
    assert report["source_linked_entry_count"] == 72
    assert report["source_linked_seed_count"] == 24
    assert report["asset_materialized_entry_count"] == 72
    assert report["fully_materialized_seed_count"] == 24
    assert report["asset_integrity_status"] == "pass"
    assert report["asset_integrity_issue_count"] == 0
    assert report["asset_integrity_warning_count"] == 0
    assert report["static_certification_status"] == "pass"
    assert report["static_certified_release_task_count"] == 245
    assert report["static_failed_release_task_count"] == 0
    assert report["static_certified_entry_count"] == 72
    assert report["dual_certification_status"] == "pass"
    assert report["dual_certified_release_task_count"] == 245
    assert report["dual_failed_release_task_count"] == 0
    assert report["dual_pending_release_task_count"] == 0
    assert report["dual_pass_materialized_entry_count"] == 72
    assert report["dual_pending_materialized_entry_count"] == 0
    assert report["dual_failed_materialized_entry_count"] == 0
    assert report["fully_certified_entry_count"] == 72
    assert report["source_equivalence_blocked_release_task_count"] == 0
    assert report["source_equivalence_failure_count"] == 0
    assert report["evas_pass_spectre_fail_count"] == 0
    assert report["dual_simulator_rerun"] is True
    assert report["l0_conformance_case_count"] == 4
    assert report["l0_conformance_benchmark_coverage_count"] == 0
    assert report["l0_conformance_model_capability_count"] == 0
    assert report["l0_conformance_broad_parity_denominator_count"] == 0
    assert report["seed_entries_all_forms_present"] == 24
    assert report["selected_entries_without_package_dir"] == []
    assert report["certified_release_entries"] == 72
    assert report["scored_release_entries"] == 72
    assert report["score_denominator_status"] == "score_enabled"
    assert report["score_claim_allowed"] is True
    assert report["scored_release_forms"] == 245
    assert report["speed_debug_status"] == "measured_subset"
    assert report["speed_claim_allowed"] is False
    assert report["speed_timed_rows"] == 4
    assert report["baseline_status"] == "ready_for_baseline_runs"
    assert report["baseline_claim_allowed"] is False
    assert report["claim_gate_status"] == "in_progress"
    assert report["allowed_claim_count"] == 7
    assert report["blocked_claim_count"] == 2
    assert report["dual_rerun_import_status"] == "partial_imported"
    assert report["stop_condition"]["ready_to_score"] is True
