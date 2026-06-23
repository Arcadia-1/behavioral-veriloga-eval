from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "benchmark-vabench-release-v1"
IMPORT_REPORT = PACKAGE / "reports" / "dual_rerun_import.json"
DUAL_REPORT = PACKAGE / "reports" / "dual_certification.json"


def test_dual_rerun_import_records_current_external_queue_import() -> None:
    report = json.loads(IMPORT_REPORT.read_text(encoding="utf-8"))

    assert report["status"] == "imported"
    assert report["stale_summary"] is False
    assert report["summary_tasks_total"] == 8
    assert report["current_queue_count"] == 0
    assert report["imported_primary_result_count"] == 0
    assert report["imported_pass_count"] == 0
    assert report["imported_pending_count"] == 0
    assert report["imported_fail_count"] == 0
    assert report["merged_dual_certified_release_task_count"] == 271
    assert report["merged_dual_pending_release_task_count"] == 0
    assert report["merged_dual_failed_release_task_count"] == 0
    assert report["merged_evas_pass_spectre_fail_count"] == 0
    assert "No current dual rerun queue remains" in report["reason"]


def test_current_dual_certification_is_complete_after_full_reruns() -> None:
    dual = json.loads(DUAL_REPORT.read_text(encoding="utf-8"))

    assert dual["status"] == "pass"
    assert dual["simulator_rerun"] is True
    assert dual["dual_certified_release_task_count"] == 271
    assert dual["dual_pending_release_task_count"] == 0
    assert dual["dual_failed_release_task_count"] == 0
    assert dual["evas_pass_spectre_fail_count"] == 0
    pending = [row for row in dual["task_reports"] if row["status"] == "pending"]
    assert pending == []
