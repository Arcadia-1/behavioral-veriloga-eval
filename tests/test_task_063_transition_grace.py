from __future__ import annotations

import csv
from pathlib import Path
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
RUNNERS = ROOT / "runners"
if str(RUNNERS) not in sys.path:
    sys.path.insert(0, str(RUNNERS))

from checkers.v4.registry import load_checker


EXPERIMENT = (
    ROOT.parents[1]
    / "_experiment_runs"
    / "r52-deepseek-family001-400-threeform-threearm-20260726"
)
ARCHIVED_SPECTRE_TRACE = (
    EXPERIMENT
    / "spectre-audit-pass/cells/v4-063-G2-r00-noevas"
    / "389aa6536a11c7bc0045a941c129ec6105a926b29759c5aea9acce60408b93b9"
    / "cases/score/tran_spectre.csv"
)


def _load_rows(csv_path: Path) -> list[dict[str, float]]:
    if not csv_path.is_file():
        pytest.skip(f"archived Spectre CSV is not available: {csv_path}")
    with csv_path.open(newline="", encoding="utf-8") as handle:
        return [
            {name: float(value) for name, value in row.items()}
            for row in csv.DictReader(handle)
        ]


def _row(
    time_s: float,
    *,
    vin: float,
    settled: float,
    code: int = 0,
) -> dict[str, float]:
    row = {
        "time": time_s,
        "vin": vin,
        "target": 0.5,
        "tol": 0.05,
        "settled": settled,
    }
    row.update(
        {
            f"t_code{bit}": 0.9 if code & (1 << bit) else 0.0
            for bit in range(8)
        }
    )
    return row


def _valid_transition_trace() -> list[dict[str, float]]:
    return [
        _row(0.0, vin=0.7, settled=0.0),
        _row(10e-9, vin=0.51, settled=0.0, code=10),
        _row(20e-9, vin=0.51, settled=0.0, code=10),
        _row(30e-9, vin=0.51, settled=0.9, code=10),
        _row(35e-9, vin=0.51, settled=0.9, code=10),
        _row(49e-9, vin=0.51, settled=0.9, code=10),
        _row(50e-9, vin=0.7, settled=0.9, code=10),
        _row(50e-9 + 10e-12, vin=0.7, settled=0.45),
        _row(50e-9 + 20e-12, vin=0.7, settled=0.0),
        _row(55e-9, vin=0.7, settled=0.0),
        _row(70e-9, vin=0.7, settled=0.0),
    ]


def test_task063_exit_transition_grace_accepts_20ps_tail() -> None:
    checker = load_checker("v4_063_settling_window_detector")
    assert checker is not None

    passed, detail = checker(_valid_transition_trace())

    assert passed, detail


def test_task063_archived_spectre_transition_tail_is_accepted() -> None:
    checker = load_checker("v4_063_settling_window_detector")
    assert checker is not None

    passed, detail = checker(_load_rows(ARCHIVED_SPECTRE_TRACE))

    assert passed, detail


def test_task063_wide_tolerance_mutation_remains_rejected() -> None:
    rows = [
        _row(0.0, vin=0.7, settled=0.0),
        _row(5e-9, vin=0.58, settled=0.0),
        _row(15e-9, vin=0.58, settled=0.0),
        _row(26e-9, vin=0.58, settled=0.9),
        _row(35e-9, vin=0.7, settled=0.0),
        _row(50e-9, vin=0.51, settled=0.0, code=50),
        _row(60e-9, vin=0.51, settled=0.0, code=50),
        _row(72e-9, vin=0.51, settled=0.9, code=50),
        _row(80e-9, vin=0.51, settled=0.9, code=50),
        _row(90e-9, vin=0.7, settled=0.0),
        _row(95e-9, vin=0.7, settled=0.0),
        _row(110e-9, vin=0.7, settled=0.0),
    ]

    checker = load_checker("v4_063_settling_window_detector")
    assert checker is not None
    passed, detail = checker(rows)

    assert not passed
    assert "property_id=P_WINDOW_DEFINITION" in detail
    assert "settled=low_outside_tolerance_window" in detail


def test_task063_long_outside_high_remains_rejected() -> None:
    rows = _valid_transition_trace()
    for row in rows:
        if row["time"] == 55e-9:
            row["settled"] = 0.9

    checker = load_checker("v4_063_settling_window_detector")
    assert checker is not None
    passed, detail = checker(rows)

    assert not passed
    assert "property_id=P_WINDOW_DEFINITION" in detail
    assert "settled=low_outside_tolerance_window" in detail
