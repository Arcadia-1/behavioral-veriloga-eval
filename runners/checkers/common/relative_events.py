"""Stimulus-relative event helpers for v4 trace checkers.

The helpers deliberately derive timing from the sampled control waveforms.  A
checker can therefore be run on a translated or uniformly time-scaled trace
without changing the answer, while still reporting the observed event times in
its diagnostic string.
"""
from __future__ import annotations

from statistics import median
from typing import Iterable


def trace_bounds(rows: list[dict[str, float]]) -> tuple[float, float, float]:
    if not rows:
        return 0.0, 0.0, 0.0
    start = float(rows[0]["time"])
    end = float(rows[-1]["time"])
    return start, end, max(0.0, end - start)


def positive_steps(rows: list[dict[str, float]]) -> list[float]:
    return [
        float(now["time"]) - float(prev["time"])
        for prev, now in zip(rows, rows[1:])
        if float(now["time"]) > float(prev["time"])
    ]


def sample_step(rows: list[dict[str, float]]) -> float:
    steps = positive_steps(rows)
    return float(median(steps)) if steps else 0.0


def logic_edges(
    rows: list[dict[str, float]],
    signal: str,
    *,
    threshold: float = 0.45,
    rising: bool = True,
) -> list[float]:
    edges: list[float] = []
    for previous, row in zip(rows, rows[1:]):
        before = float(previous.get(signal, 0.0))
        after = float(row.get(signal, 0.0))
        crossed = before <= threshold < after if rising else before > threshold >= after
        if crossed:
            edges.append(float(row["time"]))
    return edges


def rising_edges(rows: list[dict[str, float]], signal: str, threshold: float = 0.45) -> list[float]:
    return logic_edges(rows, signal, threshold=threshold, rising=True)


def falling_edges(rows: list[dict[str, float]], signal: str, threshold: float = 0.45) -> list[float]:
    return logic_edges(rows, signal, threshold=threshold, rising=False)


def first_event_after(events: Iterable[float], target: float) -> float | None:
    return next((event for event in events if event >= target), None)


def first_rising_after(rows: list[dict[str, float]], signal: str, target: float = float("-inf")) -> float | None:
    return first_event_after(rising_edges(rows, signal), target)


def first_falling_after(rows: list[dict[str, float]], signal: str, target: float = float("-inf")) -> float | None:
    return first_event_after(falling_edges(rows, signal), target)


def active_start(
    rows: list[dict[str, float]],
    *,
    enable: str | None = None,
    reset: str | None = None,
    auxiliary: str | None = None,
) -> float:
    """Return the first observed time at which a DUT can be active."""
    events: list[float] = []
    for signal in (enable, auxiliary):
        if signal:
            edge = first_rising_after(rows, signal)
            if edge is not None:
                events.append(edge)
    if reset:
        edge = first_falling_after(rows, reset)
        if edge is not None:
            events.append(edge)
    if not events:
        return trace_bounds(rows)[0]
    return max(events)


def first_disable(rows: list[dict[str, float]], signal: str, after: float) -> float | None:
    return first_falling_after(rows, signal, after)


def latest_assertion(rows: list[dict[str, float]], signal: str) -> float | None:
    events = rising_edges(rows, signal)
    return events[-1] if events else None


def rows_between(
    rows: list[dict[str, float]], start: float, end: float | None = None
) -> list[dict[str, float]]:
    return [
        row for row in rows
        if float(row["time"]) >= start and (end is None or float(row["time"]) <= end)
    ]


def relative_rows(rows: list[dict[str, float]], lo: float, hi: float) -> list[dict[str, float]]:
    start, _, duration = trace_bounds(rows)
    if duration <= 0.0:
        return []
    return rows_between(rows, start + lo * duration, start + hi * duration)


def event_period(rows: list[dict[str, float]], signal: str) -> float:
    events = rising_edges(rows, signal)
    periods = [b - a for a, b in zip(events, events[1:]) if b > a]
    return float(median(periods)) if periods else max(sample_step(rows), 0.0)


def sample_after_event(
    rows: list[dict[str, float]],
    event_time: float,
    *,
    clock_signal: str | None = None,
    fraction_of_period: float = 0.2,
) -> dict[str, float] | None:
    """Pick a post-event sample using the observed clock period, not nanoseconds."""
    period = event_period(rows, clock_signal) if clock_signal else sample_step(rows) * 4.0
    delay = max(sample_step(rows) * 3.0, period * fraction_of_period)
    target = event_time + delay
    return next((row for row in rows if float(row["time"]) >= target), None)


def period_step_anchor(rows: list[dict[str, float]], signal: str) -> float | None:
    """Find a reference-clock period change from observed edges."""
    events = rising_edges(rows, signal)
    periods = [b - a for a, b in zip(events, events[1:]) if b > a]
    if len(periods) < 4:
        return None
    baseline = float(median(periods[: max(2, len(periods) // 4)]))
    for index, period in enumerate(periods):
        if abs(period - baseline) > max(sample_step(rows) * 3.0, baseline * 0.02):
            return events[index + 1]
    return None


def weighted_logic_high_fraction(
    rows: list[dict[str, float]], signal: str, threshold: float = 0.45
) -> float:
    if len(rows) < 2:
        return 0.0
    total = 0.0
    high = 0.0
    for previous, row in zip(rows, rows[1:]):
        dt = float(row["time"]) - float(previous["time"])
        if dt <= 0.0:
            continue
        total += dt
        if 0.5 * (float(previous.get(signal, 0.0)) + float(row.get(signal, 0.0))) > threshold:
            high += dt
    return high / total if total else 0.0
