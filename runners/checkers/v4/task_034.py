"""Task-specific checker for canonical v4 DUT 034."""
from __future__ import annotations

from checkers.api import Checker
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

def check_release_loop_filter(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "vin", "out", "metric"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/clk/rst/vin/out/metric"

    out_vals = [r["out"] for r in rows if "out" in r]
    if not out_vals:
        return False, "loop_filter_missing_out_values"
    out_min = min(out_vals)
    out_max = max(out_vals)
    if not (0.0 <= out_min <= out_max <= 0.95):
        return False, f"loop_filter_out_range=({out_min:.3f},{out_max:.3f})"

    edge_samples: list[tuple[dict[str, float], float, float]] = []
    for idx in range(1, len(rows)):
        if rows[idx - 1]["clk"] <= 0.45 < rows[idx]["clk"] and rows[idx]["rst"] <= 0.45:
            settle = settled_row_index_after_delay(rows, idx)
            edge_samples.append((rows[idx], rows[settle]["out"], rows[settle]["metric"]))
    if len(edge_samples) < 12:
        return False, f"loop_filter_too_few_edge_samples={len(edge_samples)}"

    deltas: list[tuple[dict[str, float], float, float, float]] = []
    previous_out: float | None = None
    for edge_row, out, metric in edge_samples:
        if previous_out is not None:
            deltas.append((edge_row, out - previous_out, out, metric))
        previous_out = out

    positive_deltas = [
        delta
        for edge_row, delta, out, _metric in deltas
        if edge_row["time"] < 40e-9 and edge_row["vin"] > 0.55 and 0.08 < out < 0.93
    ]
    if len(positive_deltas) < 4:
        return False, f"loop_filter_missing_positive_pi_steps={len(positive_deltas)}"
    first_pos = positive_deltas[0]
    later_pos = positive_deltas[-1]
    proportional_decay = first_pos > 0.08 and 0.0 < later_pos < first_pos * 0.65
    if not proportional_decay:
        return False, f"loop_filter_no_proportional_decay first={first_pos:.3f} later={later_pos:.3f}"

    negative_deltas = [
        delta
        for edge_row, delta, out, _metric in deltas
        if 32e-9 <= edge_row["time"] <= 50e-9 and edge_row["vin"] < 0.40 and 0.08 < out < 0.93
    ]
    negative_ok = len(negative_deltas) >= 3 and sum(1 for delta in negative_deltas if delta < -0.003) >= 3
    if not negative_ok:
        return False, f"loop_filter_missing_negative_response={len(negative_deltas)}"

    near_deadband_hold = mean_in_window(rows, "out", 48e-9, 54e-9)
    if near_deadband_hold is None or near_deadband_hold < 0.80:
        value = "missing" if near_deadband_hold is None else f"{near_deadband_hold:.3f}"
        return False, f"loop_filter_missing_integral_residual={value}"

    early_metric = mean_in_window(rows, "metric", 8e-9, 18e-9)
    late_metric = mean_in_window(rows, "metric", 24e-9, 50e-9)
    reset_metric = mean_in_window(rows, "metric", 64.5e-9, 70e-9)
    if early_metric is None or late_metric is None or reset_metric is None:
        return False, "loop_filter_missing_metric_windows"
    metric_timing = early_metric < 0.15 and late_metric > 0.65 and reset_metric < 0.15
    if not metric_timing:
        return False, (
            f"loop_filter_metric_timing early={early_metric:.3f} "
            f"late={late_metric:.3f} reset={reset_metric:.3f}"
        )

    late_reset = mean_in_window(rows, "out", 64.5e-9, 66e-9)
    after_reset = mean_in_window(rows, "out", 67e-9, 70e-9)
    if late_reset is None or after_reset is None:
        return False, "loop_filter_missing_late_reset_window"
    if abs(late_reset - 0.45) > 0.02 or abs(after_reset - 0.45) > 0.02:
        return False, f"loop_filter_reset_not_cleared late={late_reset:.3f} after={after_reset:.3f}"
    return True, (
        f"loop_filter_pi first_pos_delta={first_pos:.3f} later_pos_delta={later_pos:.3f} "
        f"negative_steps={sum(1 for delta in negative_deltas if delta < -0.003)}/{len(negative_deltas)} "
        f"integral_residual={near_deadband_hold:.3f} metric={early_metric:.3f}/{late_metric:.3f}/{reset_metric:.3f} "
        f"reset={late_reset:.3f}/{after_reset:.3f}"
    )

CHECKER_ID = "v4_034_loop_filter_abstraction"
CHECKER: Checker = check_release_loop_filter
