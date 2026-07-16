"""Small stimulus-relative trace helpers shared by V4 task checkers."""

from __future__ import annotations

from statistics import median

from ..api import Row


def sample_signal(rows: list[Row], signal: str, time_s: float) -> float | None:
    if not rows or "time" not in rows[0] or signal not in rows[0]:
        return None
    if time_s < rows[0]["time"] or time_s > rows[-1]["time"]:
        return None
    for index in range(1, len(rows)):
        previous = rows[index - 1]
        current = rows[index]
        t0 = previous["time"]
        t1 = current["time"]
        if not t0 <= time_s <= t1:
            continue
        if t1 == t0:
            return current[signal]
        alpha = (time_s - t0) / (t1 - t0)
        return previous[signal] + alpha * (current[signal] - previous[signal])
    return rows[-1][signal]


def threshold_crossings(
    rows: list[Row],
    signal: str,
    *,
    threshold: float = 0.45,
    direction: int = 0,
) -> list[float]:
    crossings: list[float] = []
    for index in range(1, len(rows)):
        previous = rows[index - 1]
        current = rows[index]
        v0 = previous[signal]
        v1 = current[signal]
        rising = v0 < threshold <= v1
        falling = v0 >= threshold > v1
        if (direction > 0 and not rising) or (direction < 0 and not falling):
            continue
        if direction == 0 and not (rising or falling):
            continue
        if v1 == v0:
            crossings.append(current["time"])
            continue
        alpha = (threshold - v0) / (v1 - v0)
        crossings.append(previous["time"] + alpha * (current["time"] - previous["time"]))
    return crossings


def median_step(rows: list[Row]) -> float:
    steps = [
        rows[index]["time"] - rows[index - 1]["time"]
        for index in range(1, len(rows))
        if rows[index]["time"] > rows[index - 1]["time"]
    ]
    return median(steps) if steps else 0.0


def stable_logic_plateaus(
    rows: list[Row],
    signals: list[str],
    *,
    threshold: float = 0.45,
    minimum_duration_s: float = 1e-9,
) -> list[tuple[int, int, tuple[int, ...]]]:
    """Return inclusive row ranges whose digital stimulus vector is stable."""
    if not rows:
        return []

    def vector(row: Row) -> tuple[int, ...]:
        return tuple(int(row[signal] > threshold) for signal in signals)

    plateaus: list[tuple[int, int, tuple[int, ...]]] = []
    start = 0
    current = vector(rows[0])
    for index in range(1, len(rows)):
        candidate = vector(rows[index])
        if candidate == current:
            continue
        if rows[index - 1]["time"] - rows[start]["time"] >= minimum_duration_s:
            plateaus.append((start, index - 1, current))
        start = index
        current = candidate
    if rows[-1]["time"] - rows[start]["time"] >= minimum_duration_s:
        plateaus.append((start, len(rows) - 1, current))
    return plateaus


def plateau_sample_index(
    rows: list[Row], start: int, end: int, *, fraction: float = 0.75
) -> int:
    """Pick a pre-boundary sample at a relative position in the plateau."""
    if end <= start:
        return end
    target = rows[start]["time"] + fraction * (rows[end]["time"] - rows[start]["time"])
    return min(range(start, end + 1), key=lambda index: abs(rows[index]["time"] - target))


def property_diagnostics(counts: dict[str, int]) -> str:
    return "; ".join(
        f"{property_id} mismatch_count={int(count)}"
        for property_id, count in counts.items()
    )
