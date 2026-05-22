from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "benchmark-vabench-release-v1"
REPORT = PACKAGE / "reports" / "static_certification.json"
RESULT_SCHEMA = ROOT / "schemas" / "vabench-release-result.schema.json"


def test_static_certification_report_passes_all_materialized_release_forms() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))

    assert report["status"] == "pass"
    assert report["static_certified_release_task_count"] == 259
    assert report["static_failed_release_task_count"] == 0
    assert report["static_certified_entry_count"] == 75
    assert report["entry_count"] == 75
    assert report["issue_count"] == 0


def test_static_evidence_keeps_evas_and_spectre_pending() -> None:
    evidence_paths = sorted((PACKAGE / "evidence" / "static").glob("*/*/evidence.json"))

    assert len(evidence_paths) == 259
    for path in evidence_paths:
        evidence = json.loads(path.read_text(encoding="utf-8"))
        assert evidence["static"] == "pass"
        assert evidence["evas"] == "pending"
        assert evidence["spectre"] == "pending"
        assert evidence["verdict"] == "not_certified"
        assert evidence["checks"]["failures"] == []


def test_static_results_use_static_backend_without_scoring_rows() -> None:
    result_paths = sorted((PACKAGE / "evidence" / "static").glob("*/*/result.json"))

    assert len(result_paths) == 259
    for path in result_paths:
        result = json.loads(path.read_text(encoding="utf-8"))
        assert result["backend"] == "static"
        assert result["status"] == "PASS"
        assert result["scores"]["failure_count"] == 0


def test_release_result_schema_allows_static_backend() -> None:
    schema = json.loads(RESULT_SCHEMA.read_text(encoding="utf-8"))

    assert "static" in schema["properties"]["backend"]["enum"]
    assert "FAIL_STATIC" in schema["properties"]["status"]["enum"]
    assert "PENDING" in schema["properties"]["status"]["enum"]
