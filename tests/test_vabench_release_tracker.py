from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRACKER = ROOT / "docs" / "VABENCH_RELEASE_TRACKER.csv"


def test_release_tracker_has_expected_top_level_counts() -> None:
    rows = list(csv.DictReader(TRACKER.open(encoding="utf-8")))

    assert len(rows) == 75
    assert Counter(row["level"] for row in rows) == {"L1": 60, "L2": 15}
    assert Counter(row["package_status"] for row in rows) == {
        "current_l1_seed": 27,
        "current_l1_seed_with_review": 1,
        "selected_l1_addition": 32,
        "selected_l2_target": 15,
    }


def test_release_tracker_does_not_score_uncertified_rows() -> None:
    rows = list(csv.DictReader(TRACKER.open(encoding="utf-8")))

    assert rows
    assert {row["certification_status"] for row in rows} == {"not_certified"}
    assert {row["evas_status"] for row in rows} == {"pending"}
    assert {row["spectre_status"] for row in rows} == {"pending"}
