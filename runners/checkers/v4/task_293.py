"""Task-specific checker for canonical v4 DUT 293."""
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

def check_v3_candidate_bias_reference_settling_window_monitor(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "ref", "target", "valid", "err_metric", "settle_mon"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing reference settling window monitor signals"
    times = [row["time"] for row in rows]
    clk_edges = _threshold_crossings([row["clk"] for row in rows], times, threshold=0.45, direction="rising")
    if len(clk_edges) < 8:
        return False, f"too_few_reference_settling_clk_edges={len(clk_edges)}"
    min_period = min((b - a for a, b in zip(clk_edges, clk_edges[1:])), default=1.0e-9)
    output_delay = min(0.45e-9, 0.45 * min_period)
    settle_count = 0
    checked = 0
    max_err = 0.0
    valid_high = valid_low = reset_seen = metric_high = target_changed = out_of_window_clear = False
    first_target: float | None = None
    for edge_t in clk_edges:
        output_t = edge_t + output_delay
        if output_t >= times[-1] - 0.05e-9:
            continue
        input_values = {
            name: sample_signal_at(rows, name, edge_t + 1.0e-12)
            for name in ("rst", "ref", "target")
        }
        output_values = {
            name: sample_signal_at(rows, name, output_t)
            for name in ("valid", "err_metric", "settle_mon")
        }
        if any(value is None for value in input_values.values()) or any(value is None for value in output_values.values()):
            continue
        prior_count = settle_count
        if first_target is None:
            first_target = input_values["target"]
        target_changed = target_changed or abs(input_values["target"] - first_target) > 0.05
        err_v = abs(input_values["ref"] - input_values["target"])
        metric_expected = min(1.0, max(0.0, err_v / 0.20)) * 0.9
        if input_values["rst"] > 0.45:
            settle_count = 0
            reset_seen = True
        elif err_v <= 0.035:
            settle_count = min(settle_count + 1, 3)
        else:
            settle_count = 0
        valid_expected = 0.9 if settle_count >= 3 else 0.0
        settle_expected = 0.9 * settle_count / 3.0
        max_err = max(
            max_err,
            abs(output_values["valid"] - valid_expected),
            abs(output_values["err_metric"] - metric_expected),
            abs(output_values["settle_mon"] - settle_expected),
        )
        valid_high = valid_high or valid_expected > 0.45
        valid_low = valid_low or valid_expected < 0.45
        metric_high = metric_high or metric_expected > 0.45
        out_of_window_clear = out_of_window_clear or (err_v > 0.035 and prior_count > 0 and settle_count == 0)
        checked += 1
    if checked < 10:
        return False, f"insufficient_reference_settling_samples={checked}"
    if not (valid_high and valid_low and reset_seen and metric_high and target_changed and out_of_window_clear):
        return False, "insufficient_reference_settling_coverage"
    if max_err > 0.10:
        return False, f"reference_settling_error={max_err:.4f}"
    return True, f"samples={checked} max_err={max_err:.4f}"

CHECKER_ID = "v4_293_reference_settling_window_monitor"
CHECKER: Checker = check_v3_candidate_bias_reference_settling_window_monitor
