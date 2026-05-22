from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "benchmark-vabench-release-v1"
REPORT = PACKAGE / "reports" / "remaining_work.json"


def test_remaining_work_report_separates_pending_causes() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))

    assert report["status"] == "in_progress"
    assert report["ready_to_score"] is True
    assert report["planned_entries"] == 75
    assert report["source_linked_entry_count"] == 75
    assert report["asset_materialized_entry_count"] == 75
    assert report["dual_failed_release_task_count"] == 0
    assert report["evas_pass_spectre_fail_count"] == 0
    assert report["scored_release_entries"] == 74
    assert report["source_design_pending_entry_count"] == 0
    assert report["selected_rerun_pending_form_count"] == 0
    assert report["source_equivalence_blocked_form_count"] == 0
    assert report["fresh_dual_rerun_queue_form_count"] == 0
    assert "fresh EVAS/Spectre rerun" in report["source_equivalence_resolution_policy"]
    assert report["missing_required_form_entry_count"] == 0
    assert report["current_seed_missing_form_entry_count"] == 0


def test_remaining_work_report_names_actionable_queues() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))

    source_pending = {row["entry_id"] for row in report["source_design_pending_entries"]}
    source_equivalence = {row["entry_id"] for row in report["source_equivalence_blocked_forms"]}
    missing_required = {row["entry_id"] for row in report["missing_required_form_entries"]}
    seed_missing = {row["entry_id"] for row in report["current_seed_missing_forms"]}

    assert source_pending == set()
    assert source_equivalence == set()
    assert seed_missing == set()
    assert missing_required == set()


def test_remaining_work_next_queue_only_lists_active_work() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    queue = report["next_queue"]

    assert all("Design release-ready source tasks" not in item for item in queue)
    assert not any("fresh dual certification queue" in item for item in queue)
    assert not any("source-equivalence blocked historical imports" in item for item in queue)
    assert not any("missing required forms" in item for item in queue)
    assert not any("benchmark_score" in item for item in queue)
    assert queue == ["No remaining release work is known from current reports."]
