"""Task-specific checker for canonical v4 DUT 119."""
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

def check_v3_sar_cdac_residue(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin", "clk", "s6", "s5", "s4", "s3", "s2", "s1", "vres"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/vin/clk/s6/s5/s4/s3/s2/s1/vres"
    events: list[tuple[float, str, float]] = [(rows[0]["time"], "sample", 0.0)]
    for edge in _v3_edge_times(rows, "clk", threshold=0.45, direction=1):
        events.append((edge, "sample", 0.0))
    events.extend((edge, "step", 0.5 * 0.9) for edge in _v3_edge_times(rows, "s6", threshold=0.45, direction=-1))
    for signal, weight in (("s5", -0.25), ("s4", -0.125), ("s3", -0.0625), ("s2", -0.03125), ("s1", -0.015625)):
        events.extend((edge, "step", weight * 0.9) for edge in _v3_edge_times(rows, signal, threshold=0.45, direction=1))
    events.sort(key=lambda item: item[0])
    if len(events) < 7:
        return False, f"too_few_cdac_events={len(events)}"
    state = rows[0]["vin"]
    checked = 0
    max_err = 0.0
    observed_values: list[float] = []
    for event_time, kind, delta in events:
        if kind == "sample":
            vin_value = sample_signal_at(rows, "vin", event_time)
            if vin_value is None:
                return False, f"missing_vin_at_event={event_time * 1e9:.3f}ns"
            state = vin_value
        else:
            state += delta
        sample_t = event_time + 0.8e-9
        if sample_t > rows[-1]["time"]:
            continue
        observed = sample_signal_at(rows, "vres", sample_t)
        if observed is None:
            return False, f"missing_vres_sample_at={sample_t * 1e9:.3f}ns"
        observed_values.append(observed)
        max_err = max(max_err, abs(observed - state))
        checked += 1
    if checked < 7:
        return False, f"too_few_cdac_checks={checked}"
    has_up_step = any(b > a + 0.30 for a, b in zip(observed_values, observed_values[1:]))
    has_down_steps = sum(1 for a, b in zip(observed_values, observed_values[1:]) if b < a - 0.01) >= 4
    if not has_up_step or not has_down_steps:
        return False, f"cdac_sequence_missing_up_or_down_steps samples={','.join(f'{v:.4f}' for v in observed_values)}"
    return max_err <= 0.010, f"checked={checked} max_error={max_err:.5f}"

CHECKER_ID = "v4_119_sar_cdac_residue"
CHECKER: Checker = check_v3_sar_cdac_residue
