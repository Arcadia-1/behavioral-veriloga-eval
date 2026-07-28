from __future__ import annotations

import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runners"))

from checkers.v4.task_377 import _clock_samples


def test_clock_samples_interpolate_edge_and_settled_observation() -> None:
    rows = [
        {"time": 0.0, "clk": 0.0, "probe": 0.0},
        {"time": 1.0e-9, "clk": 0.9, "probe": 1.0},
        {"time": 2.0e-9, "clk": 0.9, "probe": 2.0},
    ]

    samples = _clock_samples(rows, "clk", settle_s=0.7e-9)

    assert len(samples) == 1
    assert samples[0]["time"] == pytest.approx(1.2e-9)
    assert samples[0]["probe"] == pytest.approx(1.2)
