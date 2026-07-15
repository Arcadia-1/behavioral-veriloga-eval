"""Task-specific checker for canonical v4 DUT 271."""
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

def _v3_values_at(
    rows: list[dict[str, float]],
    names: tuple[str, ...],
    time_s: float,
) -> dict[str, float] | None:
    values = {name: sample_signal_at(rows, name, time_s) for name in names}
    if any(value is None for value in values.values()):
        return None
    return {name: float(value) for name, value in values.items() if value is not None}

def check_v3_375_windowed_event_rate_monitor(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "event_in", "gate", "rate", "average"}
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0].keys())) if rows else sorted(required)
        return False, "missing_columns=" + ",".join(missing)
    times = [row["time"] for row in rows]
    clk_edges = _threshold_crossings([row["clk"] for row in rows], times, threshold=0.45, direction="rising")
    if len(clk_edges) < 8:
        return False, f"too_few_event_rate_edges={len(clk_edges)}"
    min_period = min((b - a for a, b in zip(clk_edges, clk_edges[1:])), default=1.0e-9)
    output_delay = min(0.42e-9, 0.42 * min_period)
    event_count = 0
    sample_count = 0
    checked = 0
    max_err = 0.0
    saw_reset = saw_gate_clear = saw_event_high = saw_event_low = saw_rate_high = saw_average_mid = False
    for edge_t in clk_edges:
        output_t = edge_t + output_delay
        if output_t >= times[-1] - 0.05e-9:
            continue
        inputs = _v3_values_at(rows, ("rst", "event_in", "gate"), edge_t + 1.0e-12)
        outputs = _v3_values_at(rows, ("rate", "average"), output_t)
        if inputs is None or outputs is None:
            continue
        prior_samples = sample_count
        if inputs["rst"] > 0.45 or inputs["gate"] <= 0.45:
            event_count = 0
            sample_count = 0
            rate_expected = average_expected = 0.0
            saw_reset = saw_reset or inputs["rst"] > 0.45
            saw_gate_clear = saw_gate_clear or (inputs["gate"] <= 0.45 and prior_samples > 0)
        else:
            sample_count += 1
            if inputs["event_in"] > 0.45:
                event_count += 1
                saw_event_high = True
            else:
                saw_event_low = True
            rate_expected = 0.9 * min(1.0, max(0.0, event_count / 5.0))
            average_expected = 0.9 * min(1.0, max(0.0, event_count / sample_count))
        max_err = max(max_err, abs(outputs["rate"] - rate_expected), abs(outputs["average"] - average_expected))
        saw_rate_high = saw_rate_high or rate_expected > 0.50
        saw_average_mid = saw_average_mid or 0.20 < average_expected < 0.80
        checked += 1
    if checked < 8:
        return False, f"insufficient_event_rate_samples={checked}"
    if not (saw_reset and saw_gate_clear and saw_event_high and saw_event_low and saw_rate_high and saw_average_mid):
        return False, "insufficient_event_rate_coverage"
    if max_err > 0.10:
        return False, f"event_rate_monitor_error={max_err:.4f}"
    return True, f"samples={checked} max_err={max_err:.4f}"

CHECKER_ID = "v4_271_windowed_event_rate_monitor"
CHECKER: Checker = check_v3_375_windowed_event_rate_monitor
