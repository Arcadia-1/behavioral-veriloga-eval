from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runners"))

from checkers.common.issue109_factory import check_clocked_output_hold


def _clocked_rows(
    *,
    inter_edge_glitch: bool,
    continuous_tracking: bool = False,
) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for step in range(1601):
        time_ns = step / 100.0
        phase = (time_ns - 0.21) % 1.0
        clk = 0.9 if phase < 0.42 else 0.0
        rst = 0.9 if time_ns < 1.25 or 9.05 <= time_ns < 10.05 else 0.0
        en = 0.0 if 6.85 <= time_ns < 7.85 else 0.9
        in0 = 0.20 if time_ns < 4.5 else 0.70
        out = in0 if continuous_tracking else 0.0
        flag = out
        metric = 0.0
        if inter_edge_glitch and rst < 0.45 and clk < 0.45:
            out = 0.9 - out
            flag = 0.9 - flag
            metric = 0.9 - metric
        rows.append({
            "time": time_ns * 1e-9,
            "clk": clk,
            "rst": rst,
            "in0": in0,
            "in1": 0.70,
            "in2": 0.42,
            "in3": 0.12,
            "ctrl0": 0.9,
            "ctrl1": 0.0,
            "vdd": 0.9,
            "vss": 0.0,
            "en": en,
            "out": out,
            "flag": flag,
            "metric": metric,
        })
    return rows


def test_clocked_outputs_hold_between_update_edges() -> None:
    assert check_clocked_output_hold(
        _clocked_rows(inter_edge_glitch=False), edge=1, task_name="test"
    )[0]


def test_clocked_outputs_reject_inter_edge_glitches() -> None:
    ok, note = check_clocked_output_hold(
        _clocked_rows(inter_edge_glitch=True), edge=1, task_name="test"
    )
    assert not ok
    assert "inter_edge_hold_error" in note


def test_clocked_outputs_reject_continuous_input_tracking() -> None:
    ok, note = check_clocked_output_hold(
        _clocked_rows(inter_edge_glitch=False, continuous_tracking=True),
        edge=1,
        task_name="test",
    )
    assert not ok
    assert "inter_edge_hold_error" in note
