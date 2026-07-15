"""Task-specific checker for canonical v4 DUT 143."""
from __future__ import annotations

from ..api import Checker
def sample_signal_at(rows: list[dict[str, float]], signal: str, time_s: float) -> float | None:
    if not rows or "time" not in rows[0] or signal not in rows[0]:
        return None
    first_time = rows[0]["time"]
    last_time = rows[-1].get("time")
    if last_time is None or time_s < first_time or time_s > last_time:
        return None
    if time_s == first_time:
        return rows[0].get(signal)
    for idx in range(1, len(rows)):
        prev = rows[idx - 1]
        cur = rows[idx]
        t0 = prev.get("time")
        t1 = cur.get("time")
        if t0 is None or t1 is None:
            continue
        if t0 <= time_s <= t1:
            v0 = prev.get(signal)
            v1 = cur.get(signal)
            if v0 is None or v1 is None:
                return None
            if t1 == t0:
                return v1
            alpha = (time_s - t0) / (t1 - t0)
            return v0 + alpha * (v1 - v0)
    return None

def _v3_edge_times(
    rows: list[dict[str, float]],
    signal: str,
    *,
    threshold: float,
    direction: int,
) -> list[float]:
    edges: list[float] = []
    for idx in range(1, len(rows)):
        prev = rows[idx - 1]
        cur = rows[idx]
        v0 = prev.get(signal)
        v1 = cur.get(signal)
        t0 = prev.get("time")
        t1 = cur.get("time")
        if v0 is None or v1 is None or t0 is None or t1 is None:
            continue
        crossed = (v0 < threshold <= v1) if direction > 0 else (v0 > threshold >= v1)
        if not crossed:
            continue
        if v1 == v0:
            edges.append(t1)
        else:
            frac = (threshold - v0) / (v1 - v0)
            edges.append(t0 + frac * (t1 - t0))
    return edges

def check_v3_two_period_sample_delay(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "update", "ain", "aout"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/update/ain/aout"
    edges = _v3_edge_times(rows, "update", threshold=0.5, direction=1)
    if len(edges) < 4:
        return False, f"too_few_update_edges={len(edges)}"
    prev_sample = 0.0
    max_err = 0.0
    checked = 0
    for edge in edges:
        expected = prev_sample
        new_sample = sample_signal_at(rows, "ain", edge)
        if new_sample is None:
            return False, f"missing_ain_at_update={edge * 1e9:.3f}ns"
        prev_sample = new_sample
        sample_t = edge + 1.0e-9
        if sample_t > rows[-1]["time"]:
            continue
        observed = sample_signal_at(rows, "aout", sample_t)
        if observed is None:
            return False, f"missing_aout_sample_at={sample_t * 1e9:.3f}ns"
        max_err = max(max_err, abs(observed - expected))
        checked += 1
    if checked < 4:
        return False, f"too_few_delay_checks={checked}"
    return max_err <= 0.035, f"checked={checked} max_error={max_err:.5f}"

CHECKER_ID = "v4_143_two_period_sample_delay"
CHECKER: Checker = check_v3_two_period_sample_delay
