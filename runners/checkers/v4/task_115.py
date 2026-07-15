"""Task-specific checker for canonical v4 DUT 115."""
from __future__ import annotations

from ..api import Checker
def _threshold_crossings(
    values: list[float],
    times: list[float],
    *,
    threshold: float = 0.0,
    direction: str,
) -> list[float]:
    edges: list[float] = []
    for idx in range(1, len(values)):
        v0 = values[idx - 1]
        v1 = values[idx]
        if direction == "rising":
            hit = v0 <= threshold < v1
        elif direction == "falling":
            hit = v0 >= threshold > v1
        else:
            raise ValueError(f"unsupported direction={direction!r}")
        if not hit:
            continue
        t0 = times[idx - 1]
        t1 = times[idx]
        if v1 == v0:
            edges.append(t1)
        else:
            alpha = (threshold - v0) / (v1 - v0)
            edges.append(t0 + alpha * (t1 - t0))
    return edges

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

def check_v3_two_bit_counter_marker(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clkin", "mc"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/clkin/mc"
    vth = 0.5 * _max_signal_value(rows, ["clkin", "mc"], default=1.0)
    rises = _edge_times_for_signal(rows, "clkin", threshold=vth, direction="rising")
    if len(rises) < 4:
        return False, f"too_few_counter_edges={len(rises)}"
    count = 0
    checked = 0
    saw_marker_high = False
    saw_marker_low_after_high = False
    failures: list[str] = []
    for edge_t in rises:
        if count == 3:
            count = 0
            expected = 1.0
        else:
            count += 1
            expected = 0.0
        probe_t = _event_probe_time(rows, edge_t, delay_s=0.30e-9)
        if probe_t is None:
            continue
        observed = sample_signal_at(rows, "mc", probe_t)
        if observed is None:
            continue
        checked += 1
        if expected > 0.5:
            saw_marker_high = True
        elif saw_marker_high:
            saw_marker_low_after_high = True
        if abs(observed - expected) > 0.08:
            failures.append(f"mc@{probe_t * 1e9:.2f}ns={observed:.3f} expected={expected:.1f}")
    if checked < 4:
        return False, f"too_few_counter_checks={checked}"
    if not saw_marker_high:
        return False, "marker_high_never_observed"
    if len(rises) >= 5 and not saw_marker_low_after_high:
        return False, "marker_did_not_return_low"
    if failures:
        return False, " ".join(failures[:5])
    return True, f"edges={len(rises)} checked={checked} marker_return_low={saw_marker_low_after_high}"

def _max_signal_value(
    rows: list[dict[str, float]],
    signals: list[str],
    *,
    default: float,
) -> float:
    values: list[float] = []
    for row in rows:
        for signal in signals:
            value = row.get(signal)
            if value is not None:
                values.append(value)
    return max(values) if values else default

def _edge_times_for_signal(
    rows: list[dict[str, float]],
    signal: str,
    *,
    threshold: float,
    direction: str,
) -> list[float]:
    times = [row["time"] for row in rows if "time" in row and signal in row]
    values = [row[signal] for row in rows if "time" in row and signal in row]
    if len(times) < 2:
        return []
    return _threshold_crossings(values, times, threshold=threshold, direction=direction)

def _event_probe_time(
    rows: list[dict[str, float]],
    event_time_s: float,
    *,
    delay_s: float = 0.18e-9,
) -> float | None:
    if not rows:
        return None
    last_time = rows[-1].get("time")
    if last_time is None:
        return None
    probe_time = event_time_s + delay_s
    if probe_time <= last_time:
        return probe_time
    fallback = last_time - 0.02e-9
    return fallback if fallback > event_time_s else None

CHECKER_ID = "v4_115_two_bit_counter_marker"
CHECKER: Checker = check_v3_two_bit_counter_marker
