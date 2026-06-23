from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "benchmark-vabench-release-v1"
MANIFEST = PACKAGE / "MANIFEST.json"
MANIFEST_CSV = PACKAGE / "MANIFEST.csv"
MANIFEST_MD = PACKAGE / "MANIFEST.md"


def test_package_manifest_indexes_all_entries_and_forms_after_certification() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    summary = manifest["summary"]

    assert manifest["status"] == "in_progress"
    assert manifest["package_root"] == "benchmark-vabench-release-v1"
    assert summary["planned_entry_count"] == 86
    assert summary["entry_count"] == 86
    assert summary["form_count"] == 300
    assert summary["track_entry_counts"] == {"core": 73, "support": 13}
    assert summary["track_form_counts"] == {"core": 265, "support": 35}
    assert summary["difficulty_entry_counts"] == {"D1": 10, "D2": 50, "D3": 26}
    assert summary["content_denominator_entry_count"] == 73
    assert summary["content_excluded_entry_count"] == 13
    assert summary["content_denominator_form_count"] == 265
    assert summary["content_excluded_form_count"] == 35
    assert summary["certified_entry_count"] == 86
    assert summary["certified_form_count"] == 300
    assert summary["pending_entry_count"] == 0
    assert summary["pending_form_count"] == 0
    assert sum(summary["entry_status_counts"].values()) == summary["entry_count"]
    assert sum(summary["form_status_counts"].values()) == summary["form_count"]
    assert summary["scored_entry_count"] == 73
    assert summary["scored_form_count"] == 265
    assert summary["support_scored_entry_count"] == 0
    assert summary["support_scored_form_count"] == 0
    assert summary["l0_conformance_case_count"] == 4
    assert summary["l0_conformance_counted_in_denominator"] == 0


def test_package_manifest_form_rows_link_assets_evidence_and_score_status() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    forms = manifest["forms"]

    assert len(forms) == 300
    assert all(row["release_task_manifest"].endswith("release_task.json") for row in forms)
    assert all(row["prompt"].endswith("prompt.md") for row in forms)
    assert all(row["meta"].endswith("meta.json") for row in forms)
    assert all(row["checks"].endswith("checks.yaml") for row in forms)
    assert all(row["gold_count"] >= 1 for row in forms)
    assert all(row["static"] == "pass" for row in forms)
    assert sum(row["track"] == "core" for row in forms) == 265
    assert sum(row["track"] == "support" for row in forms) == 35
    assert sum(row["counted_in_score"] is True for row in forms) == 265
    assert sum(row["counted_in_score"] is False for row in forms) == 35
    assert sum(row["content_denominator_included"] is True for row in forms) == 265
    assert sum(row["content_denominator_included"] is False for row in forms) == 35
    assert all(row["release_entry_id"] != "vbr1_l1_clocked_comparator" for row in forms)
    summary = manifest["summary"]
    assert sum(1 for row in forms if row["certification"] == "certified") == summary["certified_form_count"]
    assert sum(1 for row in forms if row["certification"] == "pending") == summary["pending_form_count"]
    assert sum(1 for row in forms if row["certification"] == "failed") == summary["form_status_counts"].get("failed", 0)


def test_package_manifest_csv_and_markdown_are_written() -> None:
    assert MANIFEST_CSV.exists()
    assert MANIFEST_MD.exists()
    with MANIFEST_CSV.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 300
    assert {"task_id", "release_entry_id", "form", "track", "difficulty", "certification", "counted_in_score"} <= set(rows[0])
    text = MANIFEST_MD.read_text(encoding="utf-8")
    assert "vaBench Release Package Manifest" in text
    assert "not simulator" in text


def test_package_manifest_declares_claim_boundary_and_source_reports() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    assert manifest["reports"]["claim_gate"].endswith("claim_gate.json")
    assert manifest["reports"]["score_denominator"].endswith("score_denominator_manifest.json")
    assert manifest["reports"]["finish_readiness"].endswith("finish_readiness.json")
    assert any("not simulator certification evidence" in item for item in manifest["claim_boundary"])
    assert any("counted_in_score=false" in item for item in manifest["claim_boundary"])
    assert any("counted_in_score=false" in item for item in manifest["claim_boundary"])
