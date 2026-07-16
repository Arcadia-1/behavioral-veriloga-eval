"""Task-specific checker for canonical v4 DUT 104."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import structured_result


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

def check_v3_sample_hold(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin", "vout", "vclk"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/vin/vout/vclk"
    vth = 0.5 * _max_signal_value(rows, ["vclk"], default=0.9)
    edge_times = _edge_times_for_signal(rows, "vclk", threshold=vth, direction="rising")
    if len(edge_times) < 2:
        return False, f"too_few_sample_clock_edges={len(edge_times)}"

    errors: list[float] = []
    held_spans: list[float] = []
    for edge_t in edge_times:
        probe_t = edge_t + 1.0e-9
        if probe_t > rows[-1]["time"]:
            continue
        vin_edge = sample_signal_at(rows, "vin", edge_t)
        vout_settled = sample_signal_at(rows, "vout", probe_t)
        if vin_edge is None or vout_settled is None:
            return False, f"missing_sample_near_edge={edge_t * 1e9:.3f}ns"
        errors.append(abs(vout_settled - vin_edge))

    for start_edge, stop_edge in zip(edge_times, edge_times[1:]):
        start_t = start_edge + 2.0e-9
        stop_t = stop_edge - 2.0e-9
        if stop_t <= start_t:
            continue
        values = [sample_signal_at(rows, "vout", t) for t in (start_t, 0.5 * (start_t + stop_t), stop_t)]
        if any(value is None for value in values):
            return False, f"missing_hold_window_sample={start_t * 1e9:.3f}-{stop_t * 1e9:.3f}ns"
        numeric = [float(value) for value in values if value is not None]
        held_spans.append(max(numeric) - min(numeric))
    if len(errors) < 2:
        return False, f"too_few_sample_checks={len(errors)}"
    if not held_spans:
        return False, "no_interedge_hold_window"
    max_error = max(errors)
    max_hold_span = max(held_spans)
    ok = max_error <= 0.025 and max_hold_span <= 0.025
    return ok, f"edges={len(edge_times)} max_sample_error={max_error:.4f} max_hold_span={max_hold_span:.4f}"

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

CHECKER_ID = "v4_104_sample_and_hold_ideal"
PROPERTY_IDS = (
    "P_RISING_EDGE_CAPTURE",
    "P_INTEREDGE_HOLD",
    "P_NO_FALLING_EDGE_CAPTURE",
    "P_UNITY_SAMPLE_GAIN",
    "P_PARAMETERIZED_THRESHOLD",
)
CHECKER: Checker = structured_result(check_v3_sample_hold, PROPERTY_IDS)
