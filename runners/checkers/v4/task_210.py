"""Task-specific checker for canonical v4 DUT 210."""
from __future__ import annotations

from checkers.api import Checker
def rising_edges(values: list[float], times: list[float], threshold: float = 0.45) -> list[float]:
    edges: list[float] = []
    for i in range(1, len(values)):
        if values[i - 1] < threshold <= values[i]:
            edges.append(times[i])
    return edges

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

def check_v3_sample_hold_5v_clock(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin", "vclk", "vout"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing sample hold 5v clock signals"
    threshold = 0.5 * _max_signal_value(rows, ["vclk"], default=5.0)
    rising_edges = _edge_times_for_signal(rows, "vclk", threshold=threshold, direction="rising")
    if len(rising_edges) < 3:
        return False, f"too_few_sample_hold_edges={len(rising_edges)}"
    sample_errors: list[float] = []
    hold_errors: list[float] = []
    nontracking_windows = 0
    for idx, edge_t in enumerate(rising_edges):
        vin_edge = sample_signal_at(rows, "vin", edge_t + 1e-12)
        probe_t = _event_probe_time(rows, edge_t, delay_s=0.12e-9)
        if vin_edge is None or probe_t is None:
            return False, f"missing_sample_edge={edge_t * 1e9:.3f}ns"
        vout_edge = sample_signal_at(rows, "vout", probe_t)
        if vout_edge is None:
            return False, f"missing_vout_after_edge={edge_t * 1e9:.3f}ns"
        sample_errors.append(abs(vout_edge - vin_edge))
        if idx + 1 >= len(rising_edges):
            continue
        start = edge_t + 0.20e-9
        stop = rising_edges[idx + 1] - 0.15e-9
        if stop <= start:
            continue
        hold_t = start + 0.55 * (stop - start)
        vout_hold = sample_signal_at(rows, "vout", hold_t)
        if vout_hold is None:
            continue
        hold_errors.append(abs(vout_hold - vin_edge))
        vin_values = [row["vin"] for row in rows if start <= row["time"] <= stop]
        vout_values = [row["vout"] for row in rows if start <= row["time"] <= stop]
        if vin_values and vout_values:
            if max(vin_values) - min(vin_values) > 0.20 and max(vout_values) - min(vout_values) < 0.08:
                nontracking_windows += 1
    max_sample_err = max(sample_errors) if sample_errors else 1e9
    max_hold_err = max(hold_errors) if hold_errors else 1e9
    ok = max_sample_err <= 0.05 and max_hold_err <= 0.06 and nontracking_windows >= 1
    return ok, (
        f"edges={len(rising_edges)} max_sample_err={max_sample_err:.4f} "
        f"max_hold_err={max_hold_err:.4f} nontracking={nontracking_windows}"
    )

CHECKER_ID = "v4_210_sample_hold_5v_clock"
CHECKER: Checker = check_v3_sample_hold_5v_clock
