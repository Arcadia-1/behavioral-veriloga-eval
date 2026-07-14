"""Task-specific checker for canonical v4 DUT 021."""
from __future__ import annotations

from checkers.api import Checker
DEFAULT_EDGE_SETTLE_DELAY_S = 1.2e-10

def check_release_calibration_loop(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "out"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/clk/rst/out"
    input_key = "vin" if "vin" in rows[0] else "err" if "err" in rows[0] else None
    if input_key is None:
        return False, "missing vin/err input"

    reset_rows = [r for r in rows if r["rst"] > 0.45 and r["time"] < 3e-9]
    post_rows = [r for r in rows if r["rst"] <= 0.45 and r["time"] > 3e-9]
    if len(post_rows) < 10:
        return False, f"too_few_post_reset_rows={len(post_rows)}"

    reset_mean = sum(r["out"] for r in reset_rows) / len(reset_rows) if reset_rows else rows[0]["out"]
    out_vals = [r["out"] for r in post_rows]
    out_min = min(out_vals)
    out_max = max(out_vals)
    out_span = out_max - out_min
    if not (0.0 <= out_min <= out_max <= 0.95):
        return False, f"out_range=({out_min:.3f},{out_max:.3f})"
    if abs(reset_mean - 0.45) > 0.12:
        return False, f"reset_trim_mean={reset_mean:.3f}"
    # EVAS and Spectre can land on opposite sides of the exact 0.120 V boundary
    # from transition sampling granularity while producing the same trim sequence.
    if out_span < 0.12 - 1e-6:
        return False, f"trim_span_too_small={out_span:.3f}"

    edge_idx = [
        idx for idx in range(1, len(rows))
        if rows[idx - 1]["clk"] <= 0.45 < rows[idx]["clk"] and rows[idx]["rst"] <= 0.45
    ]
    directional_checks = 0
    directional_matches = 0
    prev_out: float | None = None
    for idx in edge_idx:
        settle = min(idx + 3, len(rows) - 1)
        current_out = rows[settle]["out"]
        if prev_out is None:
            prev_out = current_out
            continue
        errv = rows[idx][input_key] - 0.45
        delta = current_out - prev_out
        prev_out = current_out
        if abs(errv) <= 0.08:
            continue
        if current_out < 0.08 or current_out > 0.82 or prev_out < 0.08 or prev_out > 0.82:
            continue
        directional_checks += 1
        if (errv > 0.0 and delta > 0.004) or (errv < 0.0 and delta < -0.004):
            directional_matches += 1
    if directional_checks < 3:
        return False, f"too_few_directional_trim_checks={directional_checks}"
    if directional_matches < directional_checks - 1:
        return False, f"trim_direction_mismatches={directional_checks - directional_matches}/{directional_checks}"

    return True, (
        f"release_calibration_loop reset={reset_mean:.3f} span={out_span:.3f} "
        f"direction={directional_matches}/{directional_checks}"
    )

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

def check_release_deadband_calibration(rows: list[dict[str, float]]) -> tuple[bool, str]:
    ok, note = check_release_calibration_loop(rows)
    if not ok:
        return ok, note
    samples = edge_settled_values(rows, "out", settle_delay_s=0.12e-9)
    hold_checks = hold_ok = 0
    previous: float | None = None
    for edge_row, out in samples:
        if previous is None:
            previous = out
            continue
        errv = edge_row.get("vin", edge_row.get("err", 0.45)) - 0.45
        delta = abs(out - previous)
        previous = out
        if abs(errv) <= 0.055 and edge_row["time"] < 60e-9:
            hold_checks += 1
            if delta <= 0.025:
                hold_ok += 1
    if hold_checks < 2:
        return False, f"deadband_missing_hold_samples={hold_checks}"
    if hold_ok < hold_checks:
        return False, f"deadband_hold_mismatches={hold_checks - hold_ok}/{hold_checks}"
    return True, f"{note}; deadband_hold={hold_ok}/{hold_checks}"

CHECKER_ID = "v4_021_calibration_deadband_controller"
CHECKER: Checker = check_release_deadband_calibration
