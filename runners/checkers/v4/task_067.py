"""Task-specific checker for canonical v4 DUT 067."""
from __future__ import annotations

from ..api import Checker
import math

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

def check_v3_501_adc_static_linearity_monitor(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vsample", "vin", "d2", "d1", "d0", "maxerr"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing adc static linearity monitor signals"
    times = [row["time"] for row in rows]
    sample_edges = _threshold_crossings(
        [row["vsample"] for row in rows],
        times,
        threshold=0.45,
        direction="rising",
    )
    if len(sample_edges) < 5:
        return False, f"too_few_linearity_sample_edges={len(sample_edges)}"
    expected_max = 0
    checked = 0
    max_err = 0.0
    observed_metrics: list[float] = []
    failures: list[str] = []
    for edge_t in sample_edges:
        sample_t = edge_t + 0.10e-9
        vin = sample_signal_at(rows, "vin", edge_t + 1e-12)
        if vin is None:
            continue
        clipped = min(1.0, max(0.0, vin))
        ideal = int(math.floor(8.0 * clipped))
        ideal = max(0, min(7, ideal))
        observed_code = 0
        for bit, signal in enumerate(("d0", "d1", "d2")):
            value = sample_signal_at(rows, signal, edge_t + 1e-12)
            if value is None:
                failures.append(f"missing_{signal}@{edge_t * 1e9:.2f}ns")
                continue
            observed_code += (1 << bit) if value > 0.45 else 0
        expected_max = max(expected_max, abs(observed_code - ideal))
        metric = sample_signal_at(rows, "maxerr", sample_t)
        if metric is None:
            return False, f"missing_maxerr@{sample_t * 1e9:.2f}ns"
        observed_metrics.append(metric)
        max_err = max(max_err, abs(metric - expected_max))
        checked += 1
    if checked < 5:
        return False, f"insufficient_linearity_monitor_samples={checked}"
    if any(observed_metrics[idx] + 0.03 < observed_metrics[idx - 1] for idx in range(1, len(observed_metrics))):
        return False, f"maxerr_not_monotonic observed={observed_metrics} expected=nondecreasing window=sample_edges"
    if expected_max < 2:
        return False, f"stimulus_did_not_exercise_two_lsb_error observed={expected_max} expected>=2 window=sample_edges"
    if failures:
        return False, " ".join(failures[:5])
    if max_err > 0.08:
        return False, (
            f"maxerr_metric_error observed=max_err:{max_err:.4f},metrics:{observed_metrics} "
            f"expected=running_max_code_error:{expected_max} window=sample_edges"
        )
    return True, f"samples={checked} expected_max={expected_max} max_err={max_err:.4f}"

CHECKER_ID = "v4_067_adc_static_linearity_monitor"
CHECKER: Checker = check_v3_501_adc_static_linearity_monitor
