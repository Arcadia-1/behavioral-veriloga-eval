"""Task-specific checker for canonical v4 DUT 270."""
from __future__ import annotations

from checkers.api import Checker
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

def check_v3_374_sampled_error_update_monitor(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "sample", "target", "coef", "out", "err_metric", "progress"}
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0].keys())) if rows else sorted(required)
        return False, "missing_columns=" + ",".join(missing)
    times = [row["time"] for row in rows]
    clk_edges = _threshold_crossings([row["clk"] for row in rows], times, threshold=0.45, direction="rising")
    if len(clk_edges) < 8:
        return False, f"too_few_sampled_error_edges={len(clk_edges)}"
    min_period = min((b - a for a, b in zip(clk_edges, clk_edges[1:])), default=1.0e-9)
    output_delay = min(0.42e-9, 0.42 * min_period)
    stable_count = 0
    checked = 0
    max_err = 0.0
    reset_errors = corrected_errors = metric_errors = progress_errors = 0
    saw_reset = saw_progress_high = saw_progress_low = saw_coeff_change = saw_target_change = saw_high_error = False
    first_coef: float | None = None
    first_target: float | None = None
    for edge_t in clk_edges:
        output_t = edge_t + output_delay
        if output_t >= times[-1] - 0.05e-9:
            continue
        inputs = _v3_values_at(rows, ("rst", "sample", "target", "coef"), edge_t + 1.0e-12)
        outputs = _v3_values_at(rows, ("out", "err_metric", "progress"), output_t)
        if inputs is None or outputs is None:
            continue
        if first_coef is None:
            first_coef = inputs["coef"]
        if first_target is None:
            first_target = inputs["target"]
        coeff = min(1.0, max(0.0, inputs["coef"] / 0.9))
        err_v = inputs["target"] - inputs["sample"]
        if inputs["rst"] > 0.45:
            stable_count = 0
            out_expected = err_expected = progress_expected = 0.0
            saw_reset = True
        else:
            corrected = inputs["sample"] + coeff * err_v
            out_expected = min(0.9, max(0.0, corrected))
            err_expected = 0.9 * min(1.0, max(0.0, abs(err_v) / 0.50))
            if abs(err_v) <= 0.040:
                stable_count = min(stable_count + 1, 3)
            else:
                stable_count = 0
            progress_expected = 0.9 * min(1.0, max(0.0, stable_count / 3.0))
        out_err = abs(outputs["out"] - out_expected)
        metric_err = abs(outputs["err_metric"] - err_expected)
        progress_err = abs(outputs["progress"] - progress_expected)
        max_err = max(max_err, out_err, metric_err, progress_err)
        if inputs["rst"] > 0.45:
            reset_errors += sum(err > 0.10 for err in (out_err, metric_err, progress_err))
        else:
            corrected_errors += int(out_err > 0.10)
            metric_errors += int(metric_err > 0.10)
            progress_errors += int(progress_err > 0.10)
        saw_progress_high = saw_progress_high or progress_expected > 0.70
        saw_progress_low = saw_progress_low or progress_expected < 0.15
        saw_high_error = saw_high_error or err_expected > 0.45
        saw_coeff_change = saw_coeff_change or abs(inputs["coef"] - first_coef) > 0.05
        saw_target_change = saw_target_change or abs(inputs["target"] - first_target) > 0.05
        checked += 1
    if checked < 8:
        return False, f"insufficient_sampled_error_samples={checked}"
    if not (saw_reset and saw_progress_high and saw_progress_low and saw_coeff_change and saw_target_change and saw_high_error):
        return False, "insufficient_sampled_error_coverage"
    ok = max_err <= 0.10
    detail = f"samples={checked} max_err={max_err:.4f}"
    if not ok:
        detail = f"sampled_error_update_error={max_err:.4f}"
    return ok, (
        f"{detail}; P_RESET_CLEARS_STATE_AND_OBSERVABLES mismatch_count={reset_errors}; "
        f"P_CORRECTED_OUTPUT_USES_SAMPLE_TARGET_AND_COEF mismatch_count={corrected_errors}; "
        f"P_ERROR_METRIC_REPORTS_ABSOLUTE_ERROR mismatch_count={metric_errors}; "
        f"P_PROGRESS_COUNTS_CONSECUTIVE_IN_WINDOW_SAMPLES mismatch_count={progress_errors}"
    )

CHECKER_ID = "v4_270_sampled_error_update_monitor"
CHECKER: Checker = check_v3_374_sampled_error_update_monitor
