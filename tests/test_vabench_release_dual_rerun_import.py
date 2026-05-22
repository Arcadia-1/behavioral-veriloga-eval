from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "benchmark-vabench-release-v1"
IMPORT_REPORT = PACKAGE / "reports" / "dual_rerun_import.json"
DUAL_REPORT = PACKAGE / "reports" / "dual_certification.json"


def test_dual_rerun_import_accepts_fresh_targeted_summary() -> None:
    report = json.loads(IMPORT_REPORT.read_text(encoding="utf-8"))
    summary_path = ROOT / report["summary"]
    summary = json.loads(summary_path.read_text(encoding="utf-8"))

    assert summary["status"] in {"complete", "dry_run"}
    assert summary["tasks_total"] == 3
    assert report["status"] == "imported"
    assert report["stale_summary"] is False
    assert report["summary_tasks_total"] == summary["tasks_total"]
    assert report["current_queue_count"] == 0
    assert report["imported_primary_result_count"] == 0
    assert report["imported_fail_count"] == 0
    assert report["merged_dual_certified_release_task_count"] == 259
    assert report["merged_dual_pending_release_task_count"] == 0
    assert "dual_certification.json already reflects imported fresh rerun evidence" in report["reason"]


def test_fresh_targeted_import_promotes_full_dual_certification() -> None:
    dual = json.loads(DUAL_REPORT.read_text(encoding="utf-8"))

    assert dual["status"] == "pass"
    assert dual["simulator_rerun"] is True
    assert dual["dual_certified_release_task_count"] == 259
    assert dual["dual_pending_release_task_count"] == 0
    assert dual["dual_failed_release_task_count"] == 0
    assert dual["evas_pass_spectre_fail_count"] == 0
