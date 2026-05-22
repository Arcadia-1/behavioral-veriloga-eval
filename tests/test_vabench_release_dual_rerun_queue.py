from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "benchmark-vabench-release-v1"
REPORT = PACKAGE / "reports" / "dual_rerun_queue.json"
REPORT_CSV = PACKAGE / "reports" / "dual_rerun_queue.csv"


def test_dual_rerun_queue_tracks_all_pending_release_forms() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))

    assert report["status"] == "complete"
    assert report["queue_count"] == 0
    assert report["ready_count"] == report["queue_count"]
    assert report["blocked_count"] == 0
    assert sum(report["reason_counts"].values()) == report["queue_count"]
    assert sum(report["form_counts"].values()) == report["queue_count"]
    assert all(row["evas_status"] == "pending" for row in report["rows"])
    assert all(row["spectre_status"] == "pending" for row in report["rows"])


def test_dual_rerun_queue_has_machine_readable_csv_and_gold_links() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    rows = list(csv.DictReader(REPORT_CSV.open(encoding="utf-8")))

    assert len(rows) == report["queue_count"]
    assert all((ROOT / row["evidence"]).exists() for row in rows)
    for row in report["rows"]:
        assert row["ready_for_dual_rerun"] is True
        assert row["gold"]
        assert all((ROOT / path).exists() for path in row["gold"])
