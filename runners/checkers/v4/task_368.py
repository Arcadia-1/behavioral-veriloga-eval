"""Task-specific checker for canonical v4 DUT 368."""
from __future__ import annotations

from checkers.api import Checker
def _v4_topup_logic_high(row: dict[str, float], name: str, threshold: float = 0.45) -> bool:
    return float(row.get(name, 0.0)) > threshold

def _v4_rising(prev_v: float, now_v: float, vth: float = 0.45) -> bool:
    return now_v > vth and prev_v <= vth

def _v4_batch001_first_after(rows: list[dict[str, float]], target_time: float) -> dict[str, float] | None:
    for row in rows:
        if float(row["time"]) >= target_time:
            return row
    return None

def check_v4_927_tia_limiting_receiver_macro(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_927 empty_trace"
    prev_clk = float(rows[0].get("clk", 0.0))
    valid_count = 0
    checked = vout_errors = flag_errors = amp_errors = decision_errors = valid_errors = clear_errors = 0
    reset_clear = disabled_clear = limit_seen = decision_high = decision_low = valid_seen = False
    for row in rows:
        t = float(row["time"])
        rst = _v4_topup_logic_high(row, "rst")
        enabled = _v4_topup_logic_high(row, "enable") and not rst
        if not enabled:
            valid_count = 0
            clear = abs(row["vout"] - 0.45) < 0.08 and row["decision"] < 0.10 and row["limit_flag"] < 0.10 and row["valid"] < 0.10 and row["amp_metric"] < 0.10
            reset_clear = reset_clear or (rst and t < 5e-9 and clear)
            disabled_clear = disabled_clear or (t > 82e-9 and clear)
            if ((rst and t < 5e-9) or t > 82e-9) and not clear:
                clear_errors += 1
            prev_clk = float(row["clk"])
            continue
        raw = 4.0 * (float(row["vin_proxy"]) - 0.45)
        limited = max(-0.35, min(0.35, raw))
        expected_vout = 0.45 + limited
        expected_flag = abs(raw) > 0.35
        expected_amp = abs(limited)
        if _v4_rising(prev_clk, float(row["clk"])):
            expected_decision = limited >= 0.0
            decision_high = decision_high or expected_decision
            decision_low = decision_low or not expected_decision
            if expected_amp >= 0.040:
                valid_count += 1
            else:
                valid_count = 0
            expected_valid = valid_count >= 2
            valid_seen = valid_seen or expected_valid
            sample = _v4_batch001_first_after(rows, t + 0.7e-9)
            if sample is not None:
                if _v4_topup_logic_high(sample, "decision") != expected_decision:
                    decision_errors += 1
                if _v4_topup_logic_high(sample, "valid") != expected_valid:
                    valid_errors += 1
        if checked % 6 == 0:
            if abs(float(row["vout"]) - expected_vout) > 0.10:
                vout_errors += 1
            if _v4_topup_logic_high(row, "limit_flag") != expected_flag:
                flag_errors += 1
            if abs(float(row["amp_metric"]) - expected_amp) > 0.10:
                amp_errors += 1
        limit_seen = limit_seen or expected_flag
        checked += 1
        prev_clk = float(row["clk"])
    ok = checked >= 40 and reset_clear and disabled_clear and limit_seen and decision_high and decision_low and valid_seen and vout_errors <= 4 and flag_errors <= 4 and amp_errors <= 4 and decision_errors <= 2 and valid_errors == 0 and clear_errors <= 12
    return ok, f"v4_927 checked={checked} reset_clear={reset_clear} disabled_clear={disabled_clear} limit_seen={limit_seen} decision_high={decision_high} decision_low={decision_low} valid_seen={valid_seen} vout_errors={vout_errors} flag_errors={flag_errors} amp_errors={amp_errors} decision_errors={decision_errors} valid_errors={valid_errors} clear_errors={clear_errors}"

CHECKER_ID = "v4_368_tia_limiting_receiver_macro"
CHECKER: Checker = check_v4_927_tia_limiting_receiver_macro
