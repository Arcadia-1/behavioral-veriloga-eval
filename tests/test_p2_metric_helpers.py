from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runners"))

from p2_metric_helpers import (  # noqa: E402
    count_logic_edges,
    time_weighted_high_fraction,
    time_weighted_mean,
    within_tolerance,
)


def test_time_weighted_high_fraction_ignores_saved_row_density() -> None:
    rows = [
        {"time": 0.0, "out": 0.0},
        {"time": 1.0, "out": 1.0},
        {"time": 2.0, "out": 1.0},
        {"time": 2.1, "out": 1.0},
        {"time": 2.2, "out": 1.0},
        {"time": 3.0, "out": 0.0},
        {"time": 4.0, "out": 0.0},
    ]

    row_fraction = sum(1 for row in rows if row["out"] > 0.5) / len(rows)

    assert row_fraction != time_weighted_high_fraction(rows, "out", 0.5)
    assert time_weighted_high_fraction(rows, "out", 0.5) == 0.525


def test_edge_count_and_window_mean_are_stable_contract_metrics() -> None:
    rows = [
        {"time": 0.0, "sig": 0.0, "vout": 0.0},
        {"time": 1.0, "sig": 1.0, "vout": 1.0},
        {"time": 2.0, "sig": 0.0, "vout": 3.0},
        {"time": 4.0, "sig": 1.0, "vout": 3.0},
    ]

    assert count_logic_edges(rows, "sig", 0.5, direction="rising") == 2
    assert count_logic_edges(rows, "sig", 0.5, direction="falling") == 1
    assert time_weighted_mean(rows, "vout", 1.0, 4.0) == 8.0 / 3.0
    assert within_tolerance(1.003, 1.0, abs_tol=0.005)
    assert not within_tolerance(1.010, 1.0, abs_tol=0.005)
