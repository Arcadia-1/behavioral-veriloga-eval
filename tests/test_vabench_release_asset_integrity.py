from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "benchmark-vabench-release-v1" / "reports" / "asset_integrity.json"


def test_release_asset_integrity_has_no_blocking_issues() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))

    assert report["status"] == "pass"
    assert report["audited_release_task_count"] == 271
    assert report["issue_count"] == 0
    assert report["form_counts"] == {
        "bugfix": 54,
        "dut": 59,
        "e2e": 79,
        "tb": 79,
    }


def test_release_asset_integrity_has_no_prompt_or_checker_warnings() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))

    assert all(task["status"] == "pass" for task in report["task_reports"])
    assert report["warning_count"] == 0
    assert not any(task["warnings"] for task in report["task_reports"])
