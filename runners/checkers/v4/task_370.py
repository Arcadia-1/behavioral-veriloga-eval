"""Task-specific checker for canonical v4 DUT 370."""
from __future__ import annotations

from checkers.api import Checker
def _v4_topup_clip01(value: float, low: float = 0.0, high: float = 0.9) -> float:
    return max(low, min(high, value))

def _v4_topup_logic_high(row: dict[str, float], name: str, threshold: float = 0.45) -> bool:
    return float(row.get(name, 0.0)) > threshold

def _v4_code_from_bits(row: dict[str, float], bits: list[str]) -> int:
    return sum((1 << idx) for idx, bit in enumerate(bits) if _v4_topup_logic_high(row, bit))

def _v4_rising(prev_v: float, now_v: float, vth: float = 0.45) -> bool:
    return now_v > vth and prev_v <= vth

def _v4_batch001_first_after(rows: list[dict[str, float]], target_time: float) -> dict[str, float] | None:
    for row in rows:
        if float(row["time"]) >= target_time:
            return row
    return None

def check_v4_929_opamp_feedback_settling_monitor(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_929 empty_trace"
    prev_clk = float(rows[0].get("clk", 0.0))
    vout = 0.45
    settle_count = 0
    checked = vout_errors = err_errors = settled_errors = clear_errors = 0
    reset_clear = disabled_clear = settled_seen = move_seen = False
    for row in rows:
        t = float(row["time"])
        rst = _v4_topup_logic_high(row, "rst")
        enabled = _v4_topup_logic_high(row, "enable") and not rst
        if not enabled:
            vout = 0.45; settle_count = 0
            clear = abs(row["vout"] - 0.45) < 0.08 and abs(row["error_metric"] - 0.45) < 0.08 and row["settled"] < 0.10
            reset_clear = reset_clear or (rst and t < 5e-9 and clear)
            disabled_clear = disabled_clear or (t > 82e-9 and clear)
            if ((rst and t < 5e-9) or t > 82e-9) and not clear:
                clear_errors += 1
            prev_clk = float(row["clk"])
            continue
        if _v4_rising(prev_clk, float(row["clk"])):
            code = _v4_code_from_bits(row, ["gain_0", "gain_1", "gain_2"])
            target = _v4_topup_clip01(0.45 + (1.0 + 0.5 * code) * (float(row["vin"]) - 0.45))
            old = vout
            vout = _v4_topup_clip01(vout + 0.3 * (target - vout))
            err = target - vout
            settle_count = settle_count + 1 if abs(err) < 0.040 else 0
            sample = _v4_batch001_first_after(rows, t + 0.7e-9)
            if sample is not None:
                checked += 1
                move_seen = move_seen or abs(vout - old) > 0.01
                expected_settled = settle_count >= 3
                settled_seen = settled_seen or expected_settled
                if abs(float(sample["vout"]) - vout) > 0.10:
                    vout_errors += 1
                if abs(float(sample["error_metric"]) - (err + 0.45)) > 0.12:
                    err_errors += 1
                if _v4_topup_logic_high(sample, "settled") != expected_settled:
                    settled_errors += 1
        prev_clk = float(row["clk"])
    ok = checked >= 6 and reset_clear and disabled_clear and move_seen and settled_seen and vout_errors <= 1 and err_errors <= 1 and settled_errors <= 1 and clear_errors <= 12
    return ok, f"v4_929 checked={checked} reset_clear={reset_clear} disabled_clear={disabled_clear} move_seen={move_seen} settled_seen={settled_seen} vout_errors={vout_errors} err_errors={err_errors} settled_errors={settled_errors} clear_errors={clear_errors}"

CHECKER_ID = "v4_370_opamp_feedback_settling_monitor"
CHECKER: Checker = check_v4_929_opamp_feedback_settling_monitor
