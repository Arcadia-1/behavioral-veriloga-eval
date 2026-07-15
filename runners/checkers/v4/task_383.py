"""Task-specific checker for canonical v4 DUT 383."""
from __future__ import annotations

from ..api import Checker
def _v4_topup_logic_high(row: dict[str, float], name: str, threshold: float = 0.45) -> bool:
    return float(row.get(name, 0.0)) > threshold

def check_v4_942_fixed_frequency_oscillator_source(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_942 empty_trace"
    checked = metric_errors = clear_errors = 0
    reset_clear = disabled_clear = osc_activity = valid_seen = reenable_seen = False
    osc_vals: list[float] = []
    prev_osc = float(rows[0].get("osc_out", 0.0))
    first_reenable_rise: float | None = None
    for row in rows[::6]:
        t = float(row["time"])
        rst = _v4_topup_logic_high(row, "rst")
        enabled = _v4_topup_logic_high(row, "enable") and not rst
        if not enabled:
            clear = row["osc_out"] < 0.12 and row["period_metric"] < 0.08 and row["valid"] < 0.10
            reset_clear = reset_clear or (rst and t < 5e-9 and clear)
            disabled_clear = disabled_clear or (54e-9 < t < 64e-9 and clear)
            if ((rst and t < 5e-9) or (54e-9 < t < 64e-9)) and not clear:
                clear_errors += 1
            continue
        reenable_seen = reenable_seen or t > 64e-9
        osc_vals.append(float(row["osc_out"]))
        if t > 64e-9 and first_reenable_rise is None and prev_osc < 0.30 and float(row["osc_out"]) > 0.65:
            first_reenable_rise = t
        valid_seen = valid_seen or _v4_topup_logic_high(row, "valid")
        checked += 1
        if abs(float(row["period_metric"]) - 0.45) > 0.10 and t > 12e-9:
            metric_errors += 1
        prev_osc = float(row["osc_out"])
    osc_activity = bool(osc_vals) and max(osc_vals) > 0.65 and min(osc_vals) < 0.20
    restart_timing_ok = first_reenable_rise is not None and 72e-9 <= first_reenable_rise <= 77e-9
    ok = checked >= 12 and reset_clear and disabled_clear and reenable_seen and restart_timing_ok and osc_activity and valid_seen and metric_errors <= 4 and clear_errors <= 4
    first_rise_note = "none" if first_reenable_rise is None else f"{first_reenable_rise:.3e}"
    return ok, f"v4_942 checked={checked} reset_clear={reset_clear} disabled_clear={disabled_clear} reenable_seen={reenable_seen} restart_timing_ok={restart_timing_ok} first_reenable_rise={first_rise_note} osc_activity={osc_activity} valid_seen={valid_seen} metric_errors={metric_errors} clear_errors={clear_errors}"

CHECKER_ID = "v4_383_fixed_frequency_oscillator_source"
CHECKER: Checker = check_v4_942_fixed_frequency_oscillator_source
