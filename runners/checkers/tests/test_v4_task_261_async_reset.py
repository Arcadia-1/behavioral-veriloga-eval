from __future__ import annotations

from runners.checkers.v4.task_261 import (
    check_v4_261_falling_edge_calibration_sampler,
)


def _rows_with_between_edge_reset() -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    falling_edges = {1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0}
    for step in range(0, 151):
        time_ns = step * 0.05
        cycle = int(time_ns)
        phase = time_ns - cycle
        clk = 0.9 if phase < 0.5 else 0.0
        rst = 0.9 if 3.20 <= time_ns < 3.70 else 0.0
        en = 0.0 if 5.0 <= time_ns < 6.0 else 0.9
        decision = cycle % 2 == 0
        out = 0.9 if decision else 0.0
        metric = 0.72 if decision else 0.54
        if rst > 0.45 or en < 0.45:
            out = 0.0
            metric = 0.0
        rows.append(
            {
                "time": time_ns * 1e-9,
                "clk": clk,
                "rst": rst,
                "en": en,
                "in0": 0.82 if decision else 0.10,
                "in1": 0.10 if decision else 0.70,
                "in2": 0.20,
                "in3": 0.30,
                "ctrl0": 0.0,
                "ctrl1": 0.0,
                "vdd": 0.9,
                "vss": 0.0,
                "out": out,
                "flag": out,
                "metric": metric,
            }
        )
    assert len(falling_edges) == 7
    return rows


def test_async_reset_between_falling_edges_counts_as_reset_coverage() -> None:
    passed, diagnostic = check_v4_261_falling_edge_calibration_sampler(
        _rows_with_between_edge_reset()
    )

    assert passed, diagnostic
    assert "samples=7" in diagnostic
