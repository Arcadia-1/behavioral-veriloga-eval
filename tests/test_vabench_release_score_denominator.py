from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "benchmark-vabench-release-v1" / "reports" / "score_denominator_manifest.json"


def test_score_denominator_enables_frozen_certified_content_rows() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    summary = report["summary"]

    assert report["status"] == "score_enabled"
    assert summary["planned_entry_count"] == 79
    assert summary["release_form_count"] == 271
    assert summary["track_entry_counts"] == {"core": 66, "support": 13}
    assert summary["track_form_counts"] == {"core": 236, "support": 35}
    assert summary["difficulty_entry_counts"] == {"D1": 10, "D2": 49, "D3": 20}
    assert summary["content_denominator_entry_count"] == 66
    assert summary["content_excluded_entry_count"] == 13
    assert summary["content_denominator_form_count"] == 236
    assert summary["content_excluded_form_count"] == 35
    assert summary["certified_entry_count"] == 79
    assert summary["certified_form_count"] == 271
    assert summary["benchmark_score_enabled_entry_count"] == 66
    assert summary["benchmark_score_enabled_form_count"] == 236
    assert summary["scored_entry_count"] == 66
    assert summary["scored_form_count"] == 236
    assert summary["core_scored_entry_count"] == 66
    assert summary["core_scored_form_count"] == 236
    assert summary["support_scored_entry_count"] == 0
    assert summary["support_scored_form_count"] == 0
    assert summary["l0_conformance_counted_in_denominator"] == 0
    assert report["claim_rule"]["score_claim_allowed"] is True


def test_score_denominator_records_why_rows_are_excluded() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    summary = report["summary"]

    entry_reasons = summary["entry_exclusion_reason_counts"]
    form_reasons = summary["form_exclusion_reason_counts"]
    assert entry_reasons == {
        "benchmark_score_disabled": 13,
        "content_denominator_excluded:support_suite_not_core_circuit_score": 13,
    }
    assert "content_denominator_excluded:duplicate_l2_gold_kernel" not in entry_reasons
    assert "entry_missing_required_forms" not in entry_reasons
    assert "entry_blocker:fresh_dual_validation" not in entry_reasons
    assert form_reasons == {
        "benchmark_score_disabled": 35,
        "content_denominator_excluded:support_suite_not_core_circuit_score": 35,
    }
    assert "content_denominator_excluded:duplicate_l2_gold_kernel" not in form_reasons
