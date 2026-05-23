from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "benchmark-vabench-release-v1"
SPEED = PACKAGE / "reports" / "speed_debug_artifact.json"
BASELINE = PACKAGE / "reports" / "baseline_artifact.json"


def test_speed_debug_artifact_records_subset_timing_without_release_speed_claim() -> None:
    report = json.loads(SPEED.read_text(encoding="utf-8"))

    assert report["status"] == "measured_subset"
    assert report["claim_allowed"] is False
    assert "Timing exists for a subset only" in report["reason"]
    assert report["measurement_scope"]["summary"] == (
        "results/vabench-release-v1-dual-rerun-ct06-split-20260524-r5-l2/summary.json"
    )
    assert report["measurement_scope"]["summary_selection"]["source"] == "dual_rerun_import"
    assert report["measurement_scope"]["planned_primary_rerun_rows"] == 4
    assert report["measurement_scope"]["planned_staged_bundles"] == 0
    assert report["measurement_scope"]["timed_rows"] == 4
    assert report["measurement_scope"]["timed_scored_form_count"] == 4
    assert report["measurement_scope"]["scored_form_count"] == 245
    assert report["measurement_scope"]["missing_scored_form_count"] == 241
    assert report["measurement_scope"]["timed_unscored_form_count"] == 0
    assert report["measurement_scope"]["full_score_denominator_timed"] is False
    assert report["measurement_scope"]["stale_summary_rejected"] is False
    assert report["measurement_plan"]["status"] == "measured_or_ready_to_import"
    assert report["measurement_plan"]["primary_queue_rows"] == 0
    assert report["measurement_plan"]["staged_bundle_count"] == 0
    assert report["measurement_plan"]["bundle_variant_counts"] == {}
    assert report["measurement_plan"]["bundle_expected_result_counts"] == {}
    assert report["measurement_plan"]["claim_blockers"] == []
    assert report["timing_totals"]["evas_wall_time_s"] > 0
    assert report["timing_totals"]["spectre_wall_time_s"] > 0
    assert "dual_rerun_staging_manifest.json for per-bundle staging blockers" in report["debug_triage_order"]
    assert any("every scored release form" in item for item in report["required_to_claim"])


def test_baseline_artifact_is_ready_after_current_dual_certification() -> None:
    report = json.loads(BASELINE.read_text(encoding="utf-8"))

    assert report["status"] == "ready_for_baseline_runs"
    assert report["claim_allowed"] is False
    assert report["scored_release_entries"] == 72
    assert report["scored_release_forms"] == 245
    assert report["score_denominator_status"] == "score_enabled"
    assert report["dual_pending_release_task_count"] == 0
    assert report["baseline_summary_count"] == 0
    assert report["execution_plan"]["status"] == "ready_for_baseline_runs"
    assert report["execution_plan"]["blocked_by"] == []
    assert report["execution_plan"]["denominator_preview"]["planned_entries"] == 72
    assert report["execution_plan"]["denominator_preview"]["release_forms"] == 245
    assert report["baseline_protocol"]["result_schema_contract"]["spectre_is_final_judge"] is True
    assert report["baseline_protocol"]["result_schema_contract"]["unscored_rows_excluded"] is True
    assert "prompt_only_generation" in report["baseline_protocol"]["minimal_lanes"]
    assert any("score_denominator_manifest.json" in item for item in report["required_to_claim"])
    assert any("Spectre as the final judge" in item for item in report["required_to_claim"])
