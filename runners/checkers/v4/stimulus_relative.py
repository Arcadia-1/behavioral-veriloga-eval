"""Small primitives for stimulus-relative V4 waveform checkers.

These helpers deliberately derive probe locations from observed events.  They
must not encode a particular public or private deck's absolute schedule.
"""
from __future__ import annotations

from collections.abc import Iterable


Row = dict[str, float]


def diagnostic(
    property_id: str,
    category: str,
    *,
    expected: str,
    observed: str,
    event: str,
) -> str:
    """Return the stable, redaction-safe feedback shape used by V4 checkers."""

    return (
        f"property_id={property_id} category={category} "
        f"expected={expected} observed={observed} event={event}"
    )


def require_signals(rows: list[Row], signals: Iterable[str], property_id: str) -> str | None:
    required = set(signals)
    if not rows:
        return diagnostic(
            property_id,
            "invalid_trace",
            expected="nonempty_trace",
            observed="empty_trace",
            event="full_trace",
        )
    missing = sorted(required - set(rows[0]))
    if missing:
        return diagnostic(
            property_id,
            "invalid_trace",
            expected="signals:" + ",".join(sorted(required)),
            observed="missing:" + ",".join(missing),
            event="full_trace",
        )
    return None


def sample(rows: list[Row], signal: str, time_s: float) -> float | None:
    """Linearly interpolate one public signal at ``time_s``."""

    if not rows or signal not in rows[0] or time_s < rows[0]["time"] or time_s > rows[-1]["time"]:
        return None
    if time_s == rows[0]["time"]:
        return rows[0][signal]
    for left, right in zip(rows, rows[1:]):
        t0 = left["time"]
        t1 = right["time"]
        if not (t0 <= time_s <= t1):
            continue
        if t1 == t0:
            return right[signal]
        alpha = (time_s - t0) / (t1 - t0)
        return left[signal] + alpha * (right[signal] - left[signal])
    return None


def nearest_row(rows: list[Row], time_s: float) -> Row | None:
    if not rows:
        return None
    return min(rows, key=lambda row: abs(row["time"] - time_s))


def logic_bits_to_int(row: Row, prefix: str, width: int, threshold: float = 0.45) -> int:
    return sum((1 << bit) for bit in range(width) if row[f"{prefix}{bit}"] > threshold)


def crossings(
    rows: list[Row],
    signal: str,
    *,
    threshold: float,
    direction: str,
) -> list[float]:
    """Return interpolated threshold-crossing times from the observed trace."""

    edges: list[float] = []
    for left, right in zip(rows, rows[1:]):
        v0 = left[signal]
        v1 = right[signal]
        if direction == "rising":
            hit = v0 <= threshold < v1
        elif direction == "falling":
            hit = v0 >= threshold > v1
        else:
            raise ValueError(f"unsupported crossing direction: {direction}")
        if not hit:
            continue
        if v1 == v0:
            edges.append(right["time"])
            continue
        alpha = (threshold - v0) / (v1 - v0)
        edges.append(left["time"] + alpha * (right["time"] - left["time"]))
    return edges


def probe_time(
    rows: list[Row],
    event_time: float,
    next_event_time: float | None,
    *,
    fraction: float = 0.25,
) -> float | None:
    """Choose a settled probe as a fraction of the observed event interval."""

    stop = rows[-1]["time"]
    interval_stop = stop if next_event_time is None else min(stop, next_event_time)
    if interval_stop <= event_time:
        return None
    return event_time + fraction * (interval_stop - event_time)


def event_label(kind: str, index: int, time_s: float) -> str:
    return f"{kind}[{index}]@{time_s:.6e}s"


def close(observed: float, expected: float, tolerance: float) -> bool:
    return abs(observed - expected) <= tolerance


def percentile(values: list[float], fraction: float) -> float:
    if not values:
        raise ValueError("percentile requires at least one value")
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, int(fraction * (len(ordered) - 1))))
    return ordered[index]


def pass_note(property_ids: Iterable[str], summary: str) -> str:
    diagnostics = "; ".join(f"{property_id} mismatch_count=0" for property_id in property_ids)
    return f"{summary}; {diagnostics}"
