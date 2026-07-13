"""Task-specific checker for canonical v4 DUT 044."""
from __future__ import annotations

from checkers.api import Checker
DEFAULT_EDGE_SETTLE_DELAY_S = 1.2e-10

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

def check_release_sar_calibration_fsm(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "vin", "out", "metric"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/clk/rst/vin/out/metric"

    reset_rows = [r for r in rows if r["rst"] > 0.45 and r["time"] < 3e-9]
    reset_mean = sum(r["out"] for r in reset_rows) / len(reset_rows) if reset_rows else rows[0]["out"]
    if abs(reset_mean - 0.45) > 0.12:
        return False, f"sar_cal_reset_mean={reset_mean:.3f}"

    post_rows = [r for r in rows if r["rst"] <= 0.45 and r["time"] > 3e-9]
    if len(post_rows) < 10:
        return False, f"sar_cal_too_few_post_reset_rows={len(post_rows)}"
    out_vals = [r["out"] for r in post_rows]
    out_min = min(out_vals)
    out_max = max(out_vals)
    if not (0.0 <= out_min <= out_max <= 0.95):
        return False, f"sar_cal_out_range=({out_min:.3f},{out_max:.3f})"
    out_span = out_max - out_min
    if out_span < 0.12:
        return False, f"sar_cal_trim_span_too_small={out_span:.3f}"

    samples = [
        (edge, out)
        for edge, out in edge_settled_values(rows, "out")
        if edge["time"] < 45e-9 and edge.get("metric", 0.0) < 0.45
    ]
    deltas = [samples[0][1] - reset_mean] if samples else []
    deltas.extend(samples[idx][1] - samples[idx - 1][1] for idx in range(1, len(samples)))
    active_deltas = [abs(d) for d in deltas if abs(d) > 0.015]
    if len(active_deltas) < 4:
        return False, f"sar_cal_too_few_active_steps={len(active_deltas)}"
    if active_deltas[-1] > 0.60 * active_deltas[0]:
        return False, f"sar_cal_step_not_halving first={active_deltas[0]:.3f} last={active_deltas[-1]:.3f}"

    direction_checks = direction_ok = 0
    for idx, (edge_row, out) in enumerate(samples):
        previous = reset_mean if idx == 0 else samples[idx - 1][1]
        delta = out - previous
        errv = edge_row["vin"] - 0.45
        if abs(delta) <= 0.004 or abs(errv) <= 0.005:
            continue
        direction_checks += 1
        if (errv > 0.0 and delta > 0.0) or (errv < 0.0 and delta < 0.0):
            direction_ok += 1
    if direction_checks < 3:
        return False, f"sar_cal_too_few_direction_checks={direction_checks}"
    if direction_ok < direction_checks - 1:
        return False, f"sar_cal_direction_mismatches={direction_checks - direction_ok}/{direction_checks}"

    metric_values = [r.get("metric", 0.0) for r in rows if r["time"] > 20e-9]
    if metric_values and max(metric_values) <= 0.45:
        return False, "sar_cal_done_never_asserted"
    return True, (
        f"sar_cal reset={reset_mean:.3f} span={out_span:.3f} "
        f"direction={direction_ok}/{direction_checks}; sar_step_first_last={active_deltas[0]:.3f}/{active_deltas[-1]:.3f}"
    )

CHECKER_ID = "v4_044_successive_approximation_calibration_search_fsm"
CHECKER: Checker = check_release_sar_calibration_fsm
