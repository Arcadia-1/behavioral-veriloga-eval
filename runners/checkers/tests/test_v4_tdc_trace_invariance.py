from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from runners.checkers.v4.task_179 import check_v3_tdc_ideal_edge_delta


EVENTS = (
    (1.00e-9, "samp", 0.0),
    (1.20e-9, "inp", 0.0),
    (1.25e-9, "inn", -0.5),
    (2.00e-9, "samp", 0.0),
    (2.24e-9, "inn", 0.0),
    (2.28e-9, "inp", 0.4),
)


def _logic_pulse(time_s: float, event_time: float) -> float:
    return 0.9 if event_time <= time_s < event_time + 20e-12 else 0.0


def _tdc_rows(*, grid_s: float, wrong_scale: bool = False) -> list[dict[str, float]]:
    times = {index * grid_s for index in range(int(3.0e-9 / grid_s) + 1)}
    for event_time, _, _ in EVENTS:
        times.update((event_time - 2e-12, event_time, event_time + 2e-12, event_time + 20e-12))

    rows: list[dict[str, float]] = []
    for time_s in sorted(time for time in times if time >= 0.0):
        expected = 0.0
        for event_time, signal, value in EVENTS:
            if signal != "samp" and value and time_s >= event_time:
                expected = value
        if wrong_scale:
            expected *= 0.5
        rows.append(
            {
                "time": time_s,
                "samp": max(
                    _logic_pulse(time_s, event_time)
                    for event_time, signal, _ in EVENTS
                    if signal == "samp"
                ),
                "inp": max(
                    _logic_pulse(time_s, event_time)
                    for event_time, signal, _ in EVENTS
                    if signal == "inp"
                ),
                "inn": max(
                    _logic_pulse(time_s, event_time)
                    for event_time, signal, _ in EVENTS
                    if signal == "inn"
                ),
                "vout": expected,
            }
        )
    return rows


def test_tdc_physical_delta_is_invariant_to_adaptive_sample_density() -> None:
    dense_ok, dense_note = check_v3_tdc_ideal_edge_delta(_tdc_rows(grid_s=2e-12))
    sparse_ok, sparse_note = check_v3_tdc_ideal_edge_delta(_tdc_rows(grid_s=17e-12))

    assert dense_ok, dense_note
    assert sparse_ok, sparse_note
    assert "measured_deltas=[-0.5, 0.4]" in dense_note
    assert "measured_deltas=[-0.5, 0.4]" in sparse_note
    assert "full_range_s=1e-10" in sparse_note


def test_tdc_wrong_full_range_scale_remains_rejected_on_sparse_grid() -> None:
    ok, note = check_v3_tdc_ideal_edge_delta(
        _tdc_rows(grid_s=17e-12, wrong_scale=True)
    )

    assert not ok, note
    assert "P_FULL_RANGE_SCALE mismatch_count=" in note
    assert "first_mismatch" in note
