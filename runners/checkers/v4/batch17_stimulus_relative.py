"""Compatibility primitives scoped to the repaired V4 batch 17 checkers."""
from __future__ import annotations

from collections.abc import Iterable

from ..api import Checker, Row
from .stimulus_relative import (
    crossings,
    diagnostic,
    event_label,
    max_signal_value,
    pass_note,
    require_signals,
    sample,
)


def logic_threshold(
    rows: list[Row], signals: Iterable[str], *, default_high: float = 0.9
) -> float:
    return 0.5 * max_signal_value(rows, signals, default=default_high)


def logic_at(
    rows: list[Row], signal: str, time_s: float, *, threshold: float
) -> int | None:
    value = sample(rows, signal, time_s)
    if value is None:
        return None
    return int(value > threshold)


def all_crossings(
    rows: list[Row],
    signal: str,
    *,
    threshold: float,
    directions: tuple[str, ...] = ("rising", "falling"),
) -> list[float]:
    edges = [
        edge
        for direction in directions
        for edge in crossings(rows, signal, threshold=threshold, direction=direction)
    ]
    return sorted(edges)


def stable_probe_times(
    rows: list[Row],
    signals: Iterable[str],
    *,
    threshold: float,
    settle_s: float = 0.3e-9,
) -> list[float]:
    if not rows:
        return []
    first_t = rows[0]["time"]
    last_t = rows[-1]["time"]
    cuts = [first_t, last_t]
    for signal in signals:
        cuts.extend(all_crossings(rows, signal, threshold=threshold))
    cuts = sorted({time_s for time_s in cuts if first_t <= time_s <= last_t})
    return [
        0.5 * (start_t + end_t)
        for start_t, end_t in zip(cuts, cuts[1:])
        if end_t - start_t > 2.0 * settle_s
    ]


def probe_time(
    rows: list[Row],
    event_time: float,
    next_event_time: float | None,
    *,
    fraction: float = 0.25,
    minimum_delay_s: float = 0.08e-9,
) -> float | None:
    if not rows:
        return None
    interval_stop = (
        rows[-1]["time"]
        if next_event_time is None
        else min(rows[-1]["time"], next_event_time)
    )
    if interval_stop <= event_time:
        return None
    target = event_time + max(
        minimum_delay_s, fraction * (interval_stop - event_time)
    )
    if target <= interval_stop:
        return target
    fallback = interval_stop - 0.02e-9
    return fallback if fallback > event_time else None


def bind_properties(checker: Checker, property_ids: Iterable[str]) -> Checker:
    property_tuple = tuple(property_ids)

    def wrapped(rows: list[Row]) -> tuple[bool, str]:
        passed, note = checker(rows)
        return passed, f"{note}; checked_property_ids={','.join(property_tuple)}"

    wrapped.__name__ = checker.__name__
    wrapped.__doc__ = checker.__doc__
    wrapped.__module__ = checker.__module__
    return wrapped
