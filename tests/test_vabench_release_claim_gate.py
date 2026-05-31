from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "benchmark-vabench-release-v1" / "reports" / "claim_gate.json"


def test_claim_gate_records_allowed_and_blocked_paper_claims() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    claims = {item["id"]: item for item in report["claims"]}

    assert report["status"] == "in_progress"
    assert report["claim_count"] == 9
    assert report["allowed_claim_count"] == 7
    assert report["blocked_claim_count"] == 2

    assert claims["C1_coverage_target_defined"]["allowed"] is True
    assert claims["C2_source_assets_static_clean"]["allowed"] is True
    assert claims["C3_imported_dual_subset_clean"]["allowed"] is True
    assert claims["C4_full_release_dual_certified"]["allowed"] is True
    assert claims["C5_score_denominator_enabled"]["allowed"] is True
    assert claims["C8_l0_conformance_separate"]["allowed"] is True
    assert claims["C9_release_package_complete"]["allowed"] is True

    assert claims["C6_speed_debug_claim"]["allowed"] is False
    assert claims["C7_model_baseline_claim"]["allowed"] is False


def test_claim_gate_prevents_subset_evidence_from_being_overclaimed() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    claims = {item["id"]: item for item in report["claims"]}

    subset = claims["C3_imported_dual_subset_clean"]
    full = claims["C4_full_release_dual_certified"]
    complete = claims["C9_release_package_complete"]

    assert subset["numbers"]["dual_certified_forms"] == 271
    assert subset["numbers"]["evas_pass_spectre_fail_count"] == 0
    assert subset["numbers"]["imported_dual_pending_forms"] == 0
    assert subset["numbers"]["current_dual_pending_forms"] == 0
    assert subset["notes"] == []

    assert full["allowed"] is True
    assert full["numbers"]["current_dual_pending_forms"] == 0
    assert full["numbers"]["imported_dual_pending_forms"] == 0
    assert full["numbers"]["fresh_dual_rerun_queue_forms"] == 0
    assert full["numbers"]["bridge_status"] == "ready"
    assert full["numbers"]["bridge_required_for_current_claim"] is False
    assert full["required_before_allowed"] == []
    assert report["blocked_completion_required_claim_ids"] == [
        "C6_speed_debug_claim",
        "C7_model_baseline_claim",
    ]
    assert complete["allowed"] is True


def test_claim_gate_lists_source_reports_and_policy() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    source_reports = report["source_reports"]

    assert source_reports["dual_certification"].endswith("dual_certification.json")
    assert source_reports["paper_artifacts"].endswith("paper_artifacts.json")
    assert source_reports["score_denominator_manifest"].endswith("score_denominator_manifest.json")
    assert any("Blocked claims must not appear" in item for item in report["claim_policy"])
