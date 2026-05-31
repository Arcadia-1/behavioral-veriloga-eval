#!/usr/bin/env python3
from __future__ import annotations

from collections.abc import Sequence


Row = dict[str, float]


def _sorted_rows(rows: Sequence[Row]) -> list[Row]:
    return sorted((row for row in rows if "time" in row), key=lambda row: row["time"])


def _interp(rows: Sequence[Row], signal: str, time_s: float) -> float | None:
    ordered = _sorted_rows(rows)
    if not ordered:
        return None
    if signal not in ordered[0]:
        return None
    if time_s <= ordered[0]["time"]:
        return ordered[0].get(signal)
    for idx in range(1, len(ordered)):
        left = ordered[idx - 1]
        right = ordered[idx]
        t0 = left["time"]
        t1 = right["time"]
        if t0 <= time_s <= t1:
            v0 = left.get(signal)
            v1 = right.get(signal)
            if v0 is None or v1 is None:
                return None
            if t1 == t0:
                return v1
            alpha = (time_s - t0) / (t1 - t0)
            return v0 + alpha * (v1 - v0)
    return ordered[-1].get(signal)


def _window_points(rows: Sequence[Row], signal: str, start: float, stop: float) -> list[tuple[float, float]]:
    if stop <= start:
        return []
    ordered = _sorted_rows(rows)
    points: list[tuple[float, float]] = []
    for t in (start, stop):
        value = _interp(ordered, signal, t)
        if value is not None:
            points.append((t, value))
    for row in ordered:
        t = row["time"]
        value = row.get(signal)
        if start < t < stop and value is not None:
            points.append((t, value))
    return sorted(set(points))


def count_logic_edges(
    rows: Sequence[Row],
    signal: str,
    threshold: float,
    *,
    direction: str = "rising",
) -> int:
    """Count threshold crossings independent of saved-row density."""
    if direction not in {"rising", "falling", "both"}:
        raise ValueError(f"unsupported direction: {direction}")
    ordered = [row for row in _sorted_rows(rows) if signal in row]
    count = 0
    for idx in range(1, len(ordered)):
        prev = ordered[idx - 1][signal]
        cur = ordered[idx][signal]
        rising = prev < threshold <= cur
        falling = prev > threshold >= cur
        if direction == "rising" and rising:
            count += 1
        elif direction == "falling" and falling:
            count += 1
        elif direction == "both" and (rising or falling):
            count += 1
    return count


def time_weighted_high_fraction(
    rows: Sequence[Row],
    signal: str,
    threshold: float,
    *,
    start: float | None = None,
    stop: float | None = None,
) -> float:
    """Return high-time / elapsed-time, not high-rows / total-rows."""
    ordered = _sorted_rows(rows)
    if len(ordered) < 2:
        return 0.0
    t_start = ordered[0]["time"] if start is None else start
    t_stop = ordered[-1]["time"] if stop is None else stop
    points = _window_points(ordered, signal, t_start, t_stop)
    if len(points) < 2:
        return 0.0
    high_dt = 0.0
    for idx in range(1, len(points)):
        t0, v0 = points[idx - 1]
        t1, v1 = points[idx]
        dt = t1 - t0
        if dt <= 0.0:
            continue
        if v0 > threshold and v1 > threshold:
            high_dt += dt
        elif v0 <= threshold and v1 <= threshold:
            continue
        elif v1 != v0:
            crossing = t0 + ((threshold - v0) / (v1 - v0)) * dt
            if v0 <= threshold < v1:
                high_dt += t1 - crossing
            elif v0 > threshold >= v1:
                high_dt += crossing - t0
    total_dt = points[-1][0] - points[0][0]
    return high_dt / total_dt if total_dt > 0.0 else 0.0


def time_weighted_mean(rows: Sequence[Row], signal: str, start: float, stop: float) -> float | None:
    """Trapezoidal mean over a time window."""
    points = _window_points(rows, signal, start, stop)
    if len(points) < 2:
        return None
    area = 0.0
    for idx in range(1, len(points)):
        t0, v0 = points[idx - 1]
        t1, v1 = points[idx]
        dt = t1 - t0
        if dt > 0.0:
            area += 0.5 * (v0 + v1) * dt
    total_dt = points[-1][0] - points[0][0]
    return area / total_dt if total_dt > 0.0 else None


def within_tolerance(observed: float, expected: float, *, abs_tol: float, rel_tol: float = 0.0) -> bool:
    return abs(observed - expected) <= max(abs_tol, rel_tol * abs(expected))
