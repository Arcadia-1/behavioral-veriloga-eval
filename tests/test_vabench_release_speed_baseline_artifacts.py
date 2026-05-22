from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "benchmark-vabench-release-v1"
SPEED = PACKAGE / "reports" / "speed_debug_artifact.json"
BASELINE = PACKAGE / "reports" / "baseline_artifact.json"


def test_speed_debug_artifact_records_full_timing_without_allowing_speed_claim() -> None:
    report = json.loads(SPEED.read_text(encoding="utf-8"))

    assert report["status"] == "measured"
    assert report["claim_allowed"] is False
    assert report["reason"] == "Timing exists, but this slice does not show an EVAS speedup over Spectre."
    assert report["measurement_scope"]["summary"] == (
        "results/vabench-release-v1-dual-rerun-speed-remaining-fix9-20260521/summary.json"
    )
    assert report["measurement_scope"]["summary_selection"]["source"] == (
        "merged_complete_timing_summaries"
    )
    assert report["measurement_scope"]["summary_selection"]["imported_summary_rejected_reason"] == (
        "imported summary is a dry-run sample"
    )
    selected = report["measurement_scope"]["summary_selection"]["selected_summaries"]
    assert "results/vabench-release-v1-dual-rerun-20260516-full-after-fixes/summary.json" in selected
    assert "results/vabench-release-v1-dual-rerun-speed-remaining-20260521/summary.json" in selected
    assert "results/vabench-release-v1-dual-rerun-speed-remaining-fix9-20260521/summary.json" in selected
    assert report["measurement_scope"]["planned_primary_rerun_rows"] == 277
    assert report["measurement_scope"]["planned_staged_bundles"] == 0
    assert report["measurement_scope"]["timed_rows"] == 277
    assert report["measurement_scope"]["timed_scored_form_count"] == 255
    assert report["measurement_scope"]["scored_form_count"] == 255
    assert report["measurement_scope"]["missing_scored_form_count"] == 0
    assert report["measurement_scope"]["timed_unscored_form_count"] == 22
    assert report["measurement_scope"]["full_score_denominator_timed"] is True
    assert report["measurement_scope"]["stale_summary_rejected"] is False
    assert report["measurement_plan"]["status"] == "measured_or_ready_to_import"
    assert report["measurement_plan"]["primary_queue_rows"] == 0
    assert report["measurement_plan"]["staged_bundle_count"] == 0
    assert report["measurement_plan"]["bundle_variant_counts"] == {}
    assert report["measurement_plan"]["bundle_expected_result_counts"] == {}
    assert report["measurement_plan"]["claim_blockers"] == []
    assert report["timing_totals"]["evas_wall_time_s"] > 1300
    assert report["timing_totals"]["spectre_wall_time_s"] > 1200
    assert report["timing_totals"]["spectre_over_evas_speedup"] < 1.0
    assert report["timing_totals"]["spectre_reported_total_elapsed_s"] > 200
    assert report["timing_distribution"]["wrapper_ratio"]["rows_evas_faster"] == 246
    assert report["timing_distribution"]["wrapper_ratio"]["rows_evas_slower"] == 31
    assert report["timing_distribution"]["wrapper_ratio"]["median"] > 4.0
    assert "dual_rerun_staging_manifest.json for per-bundle staging blockers" in report["debug_triage_order"]
    assert any("every scored release form" in item for item in report["required_to_claim"])


def test_baseline_artifact_is_ready_for_baselines_after_score_enablement() -> None:
    report = json.loads(BASELINE.read_text(encoding="utf-8"))

    assert report["status"] == "ready_for_baseline_runs"
    assert report["claim_allowed"] is False
    assert report["scored_release_entries"] == 74
    assert report["scored_release_forms"] == 255
    assert report["score_denominator_status"] == "score_enabled"
    assert report["dual_pending_release_task_count"] == 0
    assert report["baseline_summary_count"] == 0
    assert report["execution_plan"]["status"] == "ready_for_baseline_runs"
    assert report["execution_plan"]["blocked_by"] == []
    assert "EVAS/Spectre release certification is pending" not in report["execution_plan"]["blocked_by"]
    assert report["execution_plan"]["denominator_preview"]["planned_entries"] == 75
    assert report["execution_plan"]["denominator_preview"]["release_forms"] == 259
    assert report["baseline_protocol"]["result_schema_contract"]["spectre_is_final_judge"] is True
    assert report["baseline_protocol"]["result_schema_contract"]["unscored_rows_excluded"] is True
    assert "prompt_only_generation" in report["baseline_protocol"]["minimal_lanes"]
    assert any("score_denominator_manifest.json" in item for item in report["required_to_claim"])
    assert any("Spectre as the final judge" in item for item in report["required_to_claim"])
