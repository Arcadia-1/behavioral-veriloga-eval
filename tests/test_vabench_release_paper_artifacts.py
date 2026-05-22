from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "benchmark-vabench-release-v1" / "reports" / "paper_artifacts.json"


def test_paper_artifacts_report_is_claim_gated() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))

    assert report["status"] == "in_progress"
    gates = report["claim_gates"]
    assert gates["can_claim_release_assets_materialized"] is True
    assert gates["can_claim_top_level_coverage_plan"] is True
    assert gates["can_claim_release_package_complete"] is True
    assert gates["can_claim_scored_benchmark"] is True
    assert gates["can_claim_zero_evas_pass_spectre_fail_on_imported_release_evidence"] is True
    assert gates["can_claim_speedup"] is False
    assert gates["can_claim_model_baseline"] is False
    assert "release entries are not scored yet" not in gates["blocking_conditions"]
    assert "selected source design pending" not in gates["blocking_conditions"]
    assert "release entries with missing required forms remain unscored" not in gates["blocking_conditions"]
    assert "selected EVAS/Spectre rerun pending" not in gates["blocking_conditions"]
    if report["parity_summary"]["latest_dual_rerun_attempt_status"] == "blocked":
        assert any(
            item.startswith("EVAS/Spectre rerun blocked:")
            for item in gates["blocking_conditions"]
        )
    assert any(
        item.startswith("external blocker report active:")
        for item in gates["blocking_conditions"]
    )


def test_paper_artifacts_summarize_coverage_and_parity_without_overclaiming() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    coverage = report["coverage_summary"]
    parity = report["parity_summary"]
    gap = report["certification_gap_summary"]
    remaining = report["remaining_counts"]

    assert coverage["planned_entries"] == 75
    assert coverage["level_counts"] == {"L1": 60, "L2": 15}
    assert coverage["source_linked_entry_count"] == 75
    assert coverage["asset_materialized_entry_count"] == 75
    assert coverage["dual_certified_release_task_count"] == 259
    assert coverage["fully_certified_entry_count"] == 75
    assert coverage["scored_release_entries"] == 74
    assert coverage["scored_release_forms"] == 255
    assert coverage["certification_matrix_status"] == "complete"
    assert coverage["score_denominator_status"] == "score_enabled"
    assert coverage["claim_status"] == "score_enabled"

    assert parity["dual_failed_release_task_count"] == 0
    assert parity["evas_pass_spectre_fail_count"] == 0
    assert parity["main120_gold_evas"]["pass_count"] == 120
    assert parity["main120_gold_evas"]["total_tasks"] == 120
    assert parity["main120_gold_spectre"]["pass_count"] == 120
    assert parity["main120_gold_spectre"]["total_tasks"] == 120
    assert parity["l0_conformance_case_count"] == 4
    assert parity["l0_counts_in_benchmark_denominator"] == 0
    assert parity["dual_rerun_staging_status"] == "complete"
    assert parity["dual_rerun_queue_rows_with_ready_primary_bundle"] == 0
    assert parity["dual_rerun_ready_bundle_count"] == 0
    assert parity["latest_dual_rerun_attempt_status"] == "dry_run"

    assert gap["assets_materialized"] is True
    assert gap["static_certification_complete"] is True
    assert gap["fresh_dual_rerun_queue_ready"] is True
    assert gap["fresh_dual_rerun_queue_count"] == 0
    assert gap["fresh_dual_rerun_ready_bundle_count"] == 0
    assert gap["dual_pending_release_task_count"] == 0
    assert gap["bridge_ready"] in {True, False}
    assert gap["bridge_required_for_certification"] is False
    assert gap["external_blockers_status"] == "pending"
    assert gap["external_blocked_count"] == 0
    assert gap["external_pending_count"] >= 1
    assert gap["stale_rerun_summary_rejected"] is False
    assert gap["import_status"] == "imported"

    assert remaining == {
        "source_design_pending_entry_count": 0,
        "selected_rerun_pending_form_count": 0,
        "source_equivalence_blocked_form_count": 0,
        "missing_required_form_entry_count": 0,
        "current_seed_missing_form_entry_count": 0,
    }


def test_speed_artifact_has_full_timing_while_claim_stays_blocked() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))

    speed = report["speed_debug_summary"]
    baseline = report["baseline_summary"]
    assert speed["status"] == "measured"
    assert speed["claim_allowed"] is False
    assert speed["reason"] == "Timing exists, but this slice does not show an EVAS speedup over Spectre."
    assert speed["measurement_scope"]["timed_rows"] == 277
    assert speed["measurement_scope"]["timed_scored_form_count"] == 255
    assert speed["measurement_scope"]["missing_scored_form_count"] == 0
    assert speed["measurement_scope"]["full_score_denominator_timed"] is True
    assert speed["timing_totals"]["spectre_over_evas_speedup"] < 1.0
    assert baseline["status"] == "ready_for_baseline_runs"
    assert baseline["claim_allowed"] is False
    assert baseline["current_scored_release_entries"] == 74
    assert baseline["current_scored_release_forms"] == 255
    assert baseline["score_denominator_status"] == "score_enabled"
