from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from runners.checkers.v4.task_022 import check_charge_pump_abstraction


NS = 1e-9


def _rows(*, hold_glitch: bool = False, ignore_reset: bool = False) -> list[dict[str, float]]:
    edge_times = (5.0, 25.0, 45.0, 65.0, 85.0, 105.0)
    rows: list[dict[str, float]] = []
    for index in range(241):
        time_ns = 0.5 * index
        clk = 0.0
        for edge_ns in edge_times:
            if edge_ns <= time_ns < edge_ns + 4.0:
                clk = 0.9
        rst = 0.9 if time_ns < 9.0 or time_ns >= 95.0 else 0.0
        up = 0.9 if 20.0 <= time_ns < 29.0 else 0.0
        dn = 0.9 if 40.0 <= time_ns < 49.0 or 80.0 <= time_ns < 89.0 else 0.0
        if time_ns < 5.0:
            vctrl = 0.45
        elif time_ns < 25.0:
            vctrl = 0.45
        elif time_ns < 45.0:
            vctrl = 0.51
        elif time_ns < 85.0:
            vctrl = 0.45
        elif time_ns < 95.0:
            vctrl = 0.39
        else:
            vctrl = 0.39 if ignore_reset else 0.45
        if hold_glitch and 73.0 <= time_ns < 82.0:
            vctrl = 0.55
        metric = 0.45
        if 25.0 <= time_ns < 45.0:
            metric = 0.75
        elif 45.0 <= time_ns < 65.0 or 85.0 <= time_ns < 95.0:
            metric = 0.15
        rows.append(
            {
                "time": time_ns * NS,
                "clk": clk,
                "rst": rst,
                "up": up,
                "dn": dn,
                "vctrl": vctrl,
                "metric": metric,
            }
        )
    return rows


def test_sampled_hold_interval_ends_at_asynchronous_reset() -> None:
    ok, note = check_charge_pump_abstraction(_rows())
    assert ok, note


def test_sampled_hold_violation_without_reset_remains_rejected() -> None:
    ok, note = check_charge_pump_abstraction(_rows(hold_glitch=True))
    assert not ok
    assert "P_SAMPLED_HOLD" in note


def test_asynchronous_reset_that_does_not_clear_remains_rejected() -> None:
    ok, note = check_charge_pump_abstraction(_rows(ignore_reset=True))
    assert not ok
    assert "P_RESET_MIDSCALE" in note
