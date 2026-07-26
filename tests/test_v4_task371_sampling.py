from __future__ import annotations

import csv
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
RUNNERS = ROOT / "runners"
if str(RUNNERS) not in sys.path:
    sys.path.insert(0, str(RUNNERS))

from checkers.v4.task_371 import CHECKER, _clock_samples


ARCHIVED_CASES = (
    ROOT.parents[1]
    / "_experiment_runs"
    / "r52-deepseek-family001-400-threeform-threearm-20260726"
    / "spectre-audit-behavior"
    / "cells"
    / "v4-871-G2-r00-agentic"
    / "a455b373b963624bdd9b2816ad19b5ac3fcf809b305528e79b81a77554b05a8d"
    / "cases"
)


def _load_rows(csv_path: Path) -> list[dict[str, float]]:
    if not csv_path.is_file():
        pytest.skip(f"archived v4-871 Spectre trace is not available: {csv_path}")
    with csv_path.open(newline="", encoding="utf-8") as handle:
        return [
            {name: float(value) for name, value in row.items()}
            for row in csv.DictReader(handle)
        ]


@pytest.mark.parametrize(
    ("rows", "supply_active"),
    (
        (
            [
                {"time": 3.000000000e-6, "clk": 0.0, "vdd_sense": 0.0},
                {"time": 3.000000500e-6, "clk": 0.4500000003, "vdd_sense": 0.000045},
                {"time": 3.000001000e-6, "clk": 0.9, "vdd_sense": 0.000090},
                {"time": 3.010000000e-6, "clk": 0.9, "vdd_sense": 0.9},
            ],
            False,
        ),
        (
            [
                {"time": 3.000000000e-6, "clk": 0.0, "vdd_sense": 0.0},
                {"time": 3.002501250e-6, "clk": 0.450225, "vdd_sense": 0.2251125},
                {"time": 3.003710162e-6, "clk": 0.667829, "vdd_sense": 0.333914584},
            ],
            False,
        ),
        (
            [
                {"time": 70.000000000e-6, "clk": 0.0, "vdd_sense": 0.9},
                {"time": 70.000000500e-6, "clk": 0.4500000003, "vdd_sense": 0.89998},
                {"time": 70.000001000e-6, "clk": 0.9, "vdd_sense": 0.89996},
                {"time": 70.010000000e-6, "clk": 0.9, "vdd_sense": 0.5},
            ],
            True,
        ),
        (
            [
                {"time": 70.000000000e-6, "clk": 0.0, "vdd_sense": 0.9},
                {"time": 70.002501250e-6, "clk": 0.450225, "vdd_sense": 0.79995},
                {"time": 70.003750625e-6, "clk": 0.6751125, "vdd_sense": 0.749975},
            ],
            True,
        ),
    ),
)
def test_clock_samples_use_the_last_observation_within_the_settle_window(
    rows: list[dict[str, float]], supply_active: bool
) -> None:
    samples = _clock_samples(rows, "clk")

    assert len(samples) == 1
    assert any(samples[0] is row for row in rows)
    assert (samples[0]["vdd_sense"] >= 0.72) is supply_active


def test_archived_spectre_reference_passes_and_all_mutations_remain_rejected() -> None:
    reference_ok, reference_note = CHECKER(
        _load_rows(ARCHIVED_CASES / "reference" / "tran_spectre.csv")
    )
    assert reference_ok, reference_note

    mutation_dirs = sorted(
        path for path in ARCHIVED_CASES.iterdir() if path.name.startswith("neg_")
    )
    assert len(mutation_dirs) == 5
    for mutation_dir in mutation_dirs:
        mutation_ok, mutation_note = CHECKER(
            _load_rows(mutation_dir / "tran_spectre.csv")
        )
        assert not mutation_ok, (
            f"v4-871 unexpectedly accepted {mutation_dir.name}: {mutation_note}"
        )
