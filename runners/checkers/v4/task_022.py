"""Task-specific checker for canonical v4 DUT 022."""
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

def check_release_charge_pump(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "up", "dn", "vctrl", "metric"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/clk/rst/up/dn/vctrl/metric"

    ctrl_vals = [r["vctrl"] for r in rows]
    ctrl_min = min(ctrl_vals)
    ctrl_max = max(ctrl_vals)
    if not (0.0 <= ctrl_min <= ctrl_max <= 0.95):
        return False, f"charge_pump_vctrl_range=({ctrl_min:.3f},{ctrl_max:.3f})"

    reset_vals = [r["vctrl"] for r in rows if r["rst"] > 0.45 and r["time"] <= 3.0e-9]
    if not reset_vals:
        return False, "charge_pump_missing_reset_window"
    reset_mean = sum(reset_vals) / len(reset_vals)
    if abs(reset_mean - 0.45) > 0.12:
        return False, f"charge_pump_reset_mean={reset_mean:.3f}"
    ctrl_span = ctrl_max - ctrl_min
    if ctrl_span < 0.12:
        return False, f"charge_pump_vctrl_span_too_small={ctrl_span:.3f}"

    samples = edge_settled_values(rows, "vctrl")
    up_checks = down_checks = up_ok = down_ok = 0
    previous: float | None = None
    for edge_row, ctrl in samples:
        if previous is None:
            previous = ctrl
            continue
        previous_out = previous
        delta = ctrl - previous_out
        previous = ctrl
        if edge_row["time"] > 60e-9:
            continue
        if ctrl < 0.08 or ctrl > 0.82 or previous_out < 0.08 or previous_out > 0.82:
            continue
        up_high = edge_row["up"] > 0.45
        dn_high = edge_row["dn"] > 0.45
        if up_high and not dn_high:
            up_checks += 1
            if delta > 0.004:
                up_ok += 1
        elif dn_high and not up_high:
            down_checks += 1
            if delta < -0.004:
                down_ok += 1
    if up_checks < 2 or down_checks < 2:
        return False, f"charge_pump_missing_polarity_windows up={up_checks} down={down_checks}"
    if up_ok < up_checks - 1 or down_ok < down_checks - 1:
        return False, f"charge_pump_polarity up={up_ok}/{up_checks} down={down_ok}/{down_checks}"
    return True, (
        f"release_charge_pump reset={reset_mean:.3f} span={ctrl_span:.3f} "
        f"polarity up={up_ok}/{up_checks} down={down_ok}/{down_checks}"
    )

CHECKER_ID = "v4_022_charge_pump_abstraction"
CHECKER: Checker = check_release_charge_pump
