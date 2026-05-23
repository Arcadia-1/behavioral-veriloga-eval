from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "benchmark-vabench-release-v1"
IMPORT_REPORT = PACKAGE / "reports" / "dual_rerun_import.json"
DUAL_REPORT = PACKAGE / "reports" / "dual_certification.json"


def test_dual_rerun_import_records_fresh_ct05_summary() -> None:
    report = json.loads(IMPORT_REPORT.read_text(encoding="utf-8"))
    summary_path = ROOT / report["summary"]
    summary = json.loads(summary_path.read_text(encoding="utf-8"))

    assert summary["status"] == "complete"
    assert summary["tasks_total"] == report["summary_tasks_total"]
    assert report["status"] == "partial_imported"
    assert report["stale_summary"] is True
    assert report["summary_tasks_total"] == summary["tasks_total"]
    assert report["current_queue_count"] == 0
    assert report["imported_primary_result_count"] == 46
    assert report["imported_pass_count"] == 46
    assert report["imported_fail_count"] == 0
    assert "partially imported by exact entry/form match" in report["reason"]


def test_current_dual_certification_is_complete_after_ct02_rerun() -> None:
    dual = json.loads(DUAL_REPORT.read_text(encoding="utf-8"))

    assert dual["status"] == "pass"
    assert dual["simulator_rerun"] is True
    assert dual["dual_certified_release_task_count"] == 249
    assert dual["dual_pending_release_task_count"] == 0
    assert dual["dual_failed_release_task_count"] == 0
    assert dual["evas_pass_spectre_fail_count"] == 0
