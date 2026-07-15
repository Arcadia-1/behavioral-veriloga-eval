"""Task-specific checker for canonical v4 DUT 086."""
from __future__ import annotations

from ..api import Checker
DEFAULT_EDGE_SETTLE_DELAY_S = 1.2e-10

def mean_in_window(rows: list[dict[str, float]], key: str, start: float, stop: float) -> float | None:
    values = [r[key] for r in rows if start <= r["time"] <= stop and key in r]
    if not values:
        return None
    return sum(values) / len(values)

def settled_row_index_after_delay(
    rows: list[dict[str, float]],
    start_idx: int,
    settle_delay_s: float = DEFAULT_EDGE_SETTLE_DELAY_S,
) -> int:
    settle_time = rows[start_idx]["time"] + settle_delay_s
    settle = start_idx
    while settle + 1 < len(rows) and rows[settle]["time"] < settle_time:
        settle += 1
    return settle

def edge_settled_values(
    rows: list[dict[str, float]],
    key: str,
    *,
    clk_key: str = "clk",
    rst_key: str = "rst",
    settle_delay_s: float | None = None,
) -> list[tuple[dict[str, float], float]]:
    values: list[tuple[dict[str, float], float]] = []
    for idx in range(1, len(rows)):
        if rows[idx - 1][clk_key] <= 0.45 < rows[idx][clk_key] and rows[idx].get(rst_key, 0.0) <= 0.45:
            settle = settled_row_index_after_delay(
                rows,
                idx,
                DEFAULT_EDGE_SETTLE_DELAY_S if settle_delay_s is None else settle_delay_s,
            )
            values.append((rows[idx], rows[settle][key]))
    return values

def check_release_complete_calibration_loop(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "vin", "out", "metric", "trim_mon", "residual_mon"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/clk/rst/vin/out/metric/trim_mon/residual_mon"

    reset_spans: list[tuple[float, float]] = []
    release_times: list[float] = []
    span_start = rows[0]["time"]
    in_reset = rows[0]["rst"] > 0.45
    for prev, cur in zip(rows, rows[1:]):
        cur_reset = cur["rst"] > 0.45
        if cur_reset != in_reset:
            if in_reset:
                reset_spans.append((span_start, cur["time"]))
                release_times.append(cur["time"])
            span_start = cur["time"]
            in_reset = cur_reset
    if in_reset:
        reset_spans.append((span_start, rows[-1]["time"]))

    def in_reset_guard(t: float, after: float = 2.0e-9) -> bool:
        return any(start <= t <= stop + after for start, stop in reset_spans)

    first_release = release_times[0] if release_times else 3.0e-9
    post_rows = [
        r
        for r in rows
        if r["rst"] <= 0.45 and r["time"] > first_release + 1.0e-9 and not in_reset_guard(r["time"])
    ]
    if len(post_rows) < 10:
        return False, f"complete_cal_loop_too_few_post_reset_rows={len(post_rows)}"

    reset_rows = [r for r in rows if r["rst"] > 0.45]
    reset_mean = sum(r["out"] for r in reset_rows) / len(reset_rows) if reset_rows else rows[0]["out"]
    if abs(reset_mean - 0.45) > 0.06:
        return False, f"complete_cal_loop_reset_mean={reset_mean:.3f}"

    out_vals = [r["out"] for r in post_rows]
    metric_vals = [r["metric"] for r in post_rows]
    vin_vals = [r["vin"] for r in post_rows]
    out_min = min(out_vals)
    out_max = max(out_vals)
    metric_min = min(metric_vals)
    metric_max = max(metric_vals)
    vin_span = max(vin_vals) - min(vin_vals)
    out_span = out_max - out_min
    if not (0.0 <= out_min <= out_max <= 0.95):
        return False, f"complete_cal_loop_out_range=({out_min:.3f},{out_max:.3f})"
    if not (0.0 <= metric_min <= metric_max <= 0.95):
        return False, f"complete_cal_loop_metric_range=({metric_min:.3f},{metric_max:.3f})"
    if vin_span < 0.35:
        return False, f"complete_cal_loop_input_span_too_small={vin_span:.3f}"
    if out_span < 0.05:
        return False, f"complete_cal_loop_out_span_too_small={out_span:.3f}"

    correction_checks = correction_ok = positive_checks = negative_checks = 0
    for edge_row, out in edge_settled_values(rows, "out"):
        if in_reset_guard(edge_row["time"]):
            continue
        raw_err = edge_row["vin"] - 0.45
        out_err = out - 0.45
        if abs(raw_err) <= 0.09:
            continue
        correction_checks += 1
        if raw_err > 0.0:
            positive_checks += 1
        else:
            negative_checks += 1
        if abs(out_err) <= max(0.075, abs(raw_err) - 0.06):
            correction_ok += 1
    if correction_checks < 8 or positive_checks < 2 or negative_checks < 2:
        return False, (
            f"complete_cal_loop_insufficient_error_windows total={correction_checks} "
            f"pos={positive_checks} neg={negative_checks}"
        )
    if correction_ok < correction_checks - 2:
        return False, f"complete_cal_loop_uncorrected_samples={correction_checks - correction_ok}/{correction_checks}"

    trim_vals = [r["trim_mon"] for r in post_rows]
    residual_vals = [r["residual_mon"] for r in post_rows]
    trim_min = min(trim_vals)
    trim_max = max(trim_vals)
    residual_min = min(residual_vals)
    residual_max = max(residual_vals)
    if not (0.0 <= trim_min <= trim_max <= 0.95):
        return False, f"complete_cal_loop_trim_range=({trim_min:.3f},{trim_max:.3f})"
    if not (0.0 <= residual_min <= residual_max <= 0.95):
        return False, f"complete_cal_loop_residual_range=({residual_min:.3f},{residual_max:.3f})"
    if trim_max - trim_min < 0.12:
        return False, f"complete_cal_loop_trim_span_too_small={trim_max - trim_min:.3f}"

    trim_samples = edge_settled_values(rows, "trim_mon")
    residual_samples = edge_settled_values(rows, "residual_mon")
    trim_checks = trim_ok = residual_ok = 0
    for (edge_row, trim_v), (_res_edge_row, residual_v) in zip(trim_samples, residual_samples):
        if in_reset_guard(edge_row["time"]):
            continue
        raw_err = edge_row["vin"] - 0.45
        if abs(raw_err) <= 0.09:
            continue
        trim_checks += 1
        if (raw_err > 0.0 and trim_v < 0.435) or (raw_err < 0.0 and trim_v > 0.465):
            trim_ok += 1
        residual_err = abs(residual_v - 0.45)
        if residual_err <= max(0.075, abs(raw_err) * 0.85):
            residual_ok += 1
    if trim_checks < 8:
        return False, f"complete_cal_loop_insufficient_trim_windows={trim_checks}"
    if trim_ok < trim_checks - 2:
        return False, f"complete_cal_loop_trim_not_opposing_error={trim_checks - trim_ok}/{trim_checks}"
    if residual_ok < trim_checks - 2:
        return False, f"complete_cal_loop_residual_not_reduced={trim_checks - residual_ok}/{trim_checks}"

    converged_metrics = [r["metric"] for r in post_rows if abs(r["out"] - 0.45) <= 0.08]
    if len(converged_metrics) < 5:
        return False, f"complete_cal_loop_too_few_converged_samples={len(converged_metrics)}"
    converged_metric_mean = sum(converged_metrics) / len(converged_metrics)
    if converged_metric_mean < 0.70:
        return False, f"complete_cal_loop_metric_not_high_when_converged={converged_metric_mean:.3f}"

    reset_recovery_checks = reset_recovery_ok = 0
    for release_t in release_times:
        after_reset = mean_in_window(rows, "out", release_t + 0.8e-9, release_t + 3.0e-9)
        if after_reset is None:
            continue
        reset_recovery_checks += 1
        if abs(after_reset - 0.45) <= 0.12:
            reset_recovery_ok += 1
    if reset_recovery_checks < 1:
        return False, "complete_cal_loop_missing_reset_recovery_window"
    if reset_recovery_ok < reset_recovery_checks:
        return False, f"complete_cal_loop_reset_recovery={reset_recovery_ok}/{reset_recovery_checks}"

    return True, (
        f"complete_cal_loop reset={reset_mean:.3f} vin_span={vin_span:.3f} out_span={out_span:.3f} "
        f"correction={correction_ok}/{correction_checks} trim={trim_ok}/{trim_checks} "
        f"residual={residual_ok}/{trim_checks} metric={converged_metric_mean:.3f} "
        f"reset_recovery={reset_recovery_ok}/{reset_recovery_checks}"
    )

CHECKER_ID = "v4_086_complete_calibration_loop"
CHECKER: Checker = check_release_complete_calibration_loop
