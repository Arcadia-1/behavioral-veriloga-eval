from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "benchmark-vabench-release-v1" / "reports" / "score_denominator_manifest.json"


def test_score_denominator_enables_frozen_certified_content_rows() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    summary = report["summary"]

    assert report["status"] == "score_enabled"
    assert summary["planned_entry_count"] == 75
    assert summary["release_form_count"] == 259
    assert summary["content_denominator_entry_count"] == 74
    assert summary["content_excluded_entry_count"] == 1
    assert summary["content_denominator_form_count"] == 255
    assert summary["content_excluded_form_count"] == 4
    assert summary["certified_entry_count"] == summary["planned_entry_count"]
    assert summary["certified_form_count"] == summary["release_form_count"]
    assert summary["benchmark_score_enabled_entry_count"] == 74
    assert summary["benchmark_score_enabled_form_count"] == 255
    assert summary["scored_entry_count"] == 74
    assert summary["scored_form_count"] == 255
    assert summary["l0_conformance_counted_in_denominator"] == 0
    assert report["claim_rule"]["score_claim_allowed"] is True


def test_score_denominator_records_why_rows_are_excluded() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    summary = report["summary"]

    entry_reasons = summary["entry_exclusion_reason_counts"]
    form_reasons = summary["form_exclusion_reason_counts"]
    assert entry_reasons["benchmark_score_disabled"] == 1
    assert entry_reasons["content_denominator_excluded:duplicate_strongarm_clocked_comparator"] == 1
    assert "content_denominator_excluded:duplicate_l2_gold_kernel" not in entry_reasons
    assert "entry_missing_required_forms" not in entry_reasons
    assert "entry_not_fully_certified" not in entry_reasons
    assert form_reasons["benchmark_score_disabled"] == 4
    assert form_reasons["content_denominator_excluded:duplicate_strongarm_clocked_comparator"] == 4
    assert "content_denominator_excluded:duplicate_l2_gold_kernel" not in form_reasons
    assert "task_evas:pending" not in form_reasons
    assert "task_spectre:pending" not in form_reasons
