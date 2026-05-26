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

    assert report["status"] == "partial"
    assert summary["entry_count"] == 64
    assert summary["form_count"] == 219
    assert summary["fully_certified_entry_count"] == 63
    assert summary["pending_entry_count"] == 1
    assert summary["certified_form_count"] == 217
    assert summary["pending_form_count"] == 2
    assert summary["fresh_dual_rerun_pending_form_count"] == 2
    assert summary["source_equivalence_blocked_form_count"] == 0
    assert summary["dual_failure_form_count"] == 0
    assert summary["evas_pass_spectre_fail_count"] == 0
    assert summary["scored_entry_count"] == 51
    assert summary["scored_form_count"] == 184


def test_certification_matrix_exposes_pending_causes_without_overclaiming() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    summary = report["summary"]

    assert summary["entry_pending_cause_counts"] == {
            "fresh_dual_rerun_pending": 1,
            "fully_certified": 63,
    }
    assert summary["form_pending_cause_counts"] == {
            "certified": 217,
            "fresh_dual_rerun_pending": 2,
    }
    assert summary["form_disposition_counts"] == {
            "fresh_dual_rerun_required": 2,
            "none": 217,
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

    assert len(entry_rows) == 64
    assert len(form_rows) == 219
    assert sum(row["entry_status"] == "pending" for row in entry_rows) == 1
    assert sum(row["entry_status"] == "fully_certified" for row in entry_rows) == 63
    assert sum(row["pending_cause"] == "certified" for row in form_rows) == 217
    assert sum(row["pending_cause"] == "fresh_dual_rerun_pending" for row in form_rows) == 2
    assert sum(row["counted_in_score"] == "True" for row in form_rows) == 184
    assert sum(row["counted_in_score"] == "False" for row in form_rows) == 35
