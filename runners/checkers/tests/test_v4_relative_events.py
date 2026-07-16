from __future__ import annotations

from runners.checkers.common.relative_events import (
    active_start,
    event_period,
    relative_rows,
    rising_edges,
)


def _clock_rows(scale: float = 1.0, shift: float = 0.0) -> list[dict[str, float]]:
    # The waveform has the same observed stimulus events under translation and
    # uniform scaling; only the time coordinate changes.
    base = [
        (0.0, 0.0, 0.0),
        (1.0, 0.0, 0.0),
        (1.1, 0.9, 0.0),
        (2.0, 0.9, 0.0),
        (2.1, 0.0, 0.0),
        (3.0, 0.0, 0.0),
        (3.1, 0.9, 0.9),
        (4.0, 0.9, 0.9),
        (4.1, 0.0, 0.9),
        (5.0, 0.0, 0.9),
    ]
    return [
        {"time": shift + scale * t, "clk": clk, "enable": enable}
        for t, clk, enable in base
    ]


def test_observed_edges_and_period_are_shift_scale_invariant() -> None:
    base = _clock_rows()
    transformed = _clock_rows(scale=7.0, shift=13.0)
    base_edges = rising_edges(base, "clk")
    transformed_edges = rising_edges(transformed, "clk")
    assert len(base_edges) == len(transformed_edges)
    assert event_period(transformed, "clk") == 7.0 * event_period(base, "clk")
    base_start = base_edges[0]
    transformed_start = transformed_edges[0]
    assert transformed_start == 13.0 + 7.0 * base_start


def test_relative_windows_and_active_start_ignore_time_origin() -> None:
    base = _clock_rows()
    transformed = _clock_rows(scale=3.5, shift=21.0)
    assert len(relative_rows(base, 0.2, 0.8)) == len(relative_rows(transformed, 0.2, 0.8))
    assert active_start(transformed, enable="enable") == 21.0 + 3.5 * active_start(base, enable="enable")
