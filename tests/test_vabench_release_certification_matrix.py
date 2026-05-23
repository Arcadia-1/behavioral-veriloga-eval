from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "benchmark-vabench-release-v1" / "reports"
REPORT = REPORTS / "certification_matrix.json"
ENTRY_CSV = REPORTS / "certification_matrix_entries.csv"
FORM_CSV = REPORTS / "certification_matrix_forms.csv"


def test_certification_matrix_summarizes_entry_and_form_status() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    summary = report["summary"]

    assert report["status"] == "complete"
    assert summary["entry_count"] == 73
    assert summary["form_count"] == 249
    assert summary["fully_certified_entry_count"] == 73
    assert summary["pending_entry_count"] == 0
    assert summary["certified_form_count"] == 249
    assert summary["pending_form_count"] == 0
    assert summary["fresh_dual_rerun_pending_form_count"] == 0
    assert summary["source_equivalence_blocked_form_count"] == 0
    assert summary["dual_failure_form_count"] == 0
    assert summary["evas_pass_spectre_fail_count"] == 0
    assert summary["scored_entry_count"] == 73
    assert summary["scored_form_count"] == 245


def test_certification_matrix_exposes_pending_causes_without_overclaiming() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    summary = report["summary"]

    assert summary["entry_pending_cause_counts"] == {"fully_certified": 73}
    assert summary["form_pending_cause_counts"] == {
        "certified": 249,
    }
    assert summary["form_disposition_counts"] == {
        "none": 249,
    }
    assert any("does not create new simulator evidence" in item for item in report["claim_boundary"])
    assert any("remain excluded from score" in item for item in report["claim_boundary"])


def test_certification_matrix_lists_source_equivalence_blockers() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    blocked = {
        (row["release_entry_id"], row["form"])
        for row in report["source_equivalence_blocked_forms"]
    }

    assert blocked == set()


def test_certification_matrix_writes_entry_and_form_csvs() -> None:
    entry_rows = list(csv.DictReader(ENTRY_CSV.open(encoding="utf-8")))
    form_rows = list(csv.DictReader(FORM_CSV.open(encoding="utf-8")))

    assert len(entry_rows) == 73
    assert len(form_rows) == 249
    assert sum(row["entry_status"] == "fully_certified" for row in entry_rows) == 73
    assert sum(row["pending_cause"] == "certified" for row in form_rows) == 249
    assert sum(row["pending_cause"] == "fresh_dual_rerun_pending" for row in form_rows) == 0
    assert sum(row["counted_in_score"] == "True" for row in form_rows) == 245
    assert sum(row["counted_in_score"] == "False" for row in form_rows) == 4
