"""Task-specific checker for canonical v4 DUT 398."""
from __future__ import annotations

from checkers.api import Checker
def _v4_topup_clip01(value: float, low: float = 0.0, high: float = 0.9) -> float:
    return max(low, min(high, value))

def _v4_topup_logic_high(row: dict[str, float], name: str, threshold: float = 0.45) -> bool:
    return float(row.get(name, 0.0)) > threshold

def _v4_rising(prev_v: float, now_v: float, vth: float = 0.45) -> bool:
    return now_v > vth and prev_v <= vth

def _v4_batch001_first_after(rows: list[dict[str, float]], target_time: float) -> dict[str, float] | None:
    for row in rows:
        if float(row["time"]) >= target_time:
            return row
    return None

def check_v4_957_two_stage_opamp_slew_macromodel(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_957 empty_trace"
    prev_clk = float(rows[0].get("clk", 0.0))
    vout = 0.45
    settle_count = 0
    checked = vout_errors = stage1_errors = slew_errors = flag_errors = settled_errors = clear_errors = 0
    reset_clear = disabled_clear = slew_seen = clamp_seen = settled_seen = False
    for row in rows:
        t = float(row["time"])
        rst = _v4_topup_logic_high(row, "rst")
        enabled = _v4_topup_logic_high(row, "enable") and not rst
        if not enabled:
            vout = 0.45; settle_count = 0
            clear = abs(row["vout"] - 0.45) < 0.08 and abs(row["stage1_metric"] - 0.45) < 0.08 and row["slew_metric"] < 0.10 and row["clamp_flag"] < 0.10 and row["settled"] < 0.10
            reset_clear = reset_clear or (rst and t < 5e-9 and clear)
            disabled_clear = disabled_clear or (t > 86e-9 and clear)
            if ((rst and t < 5e-9) or t > 86e-9) and not clear:
                clear_errors += 1
            prev_clk = float(row["clk"])
            continue
        if _v4_rising(prev_clk, float(row["clk"])):
            diff = float(row["vinp"]) - float(row["vinn"])
            stage1 = _v4_topup_clip01(0.45 + 20.0 * diff)
            raw = 0.45 + 5.0 * (stage1 - 0.45) + (float(row["load_step"]) - 0.45) * 0.5
            target = _v4_topup_clip01(raw)
            clamped = target != raw
            move = target - vout
            if move > 0.08:
                move = 0.08
            if move < -0.08:
                move = -0.08
            vout = _v4_topup_clip01(vout + move)
            slew = abs(move)
            settle_count = settle_count + 1 if abs(target - vout) < 0.010 else 0
            sample = _v4_batch001_first_after(rows, t + 0.7e-9)
            if sample is not None:
                checked += 1
                slew_seen = slew_seen or slew > 0.02
                clamp_seen = clamp_seen or clamped
                settled_seen = settled_seen or settle_count >= 2
                if abs(float(sample["vout"]) - vout) > 0.10:
                    vout_errors += 1
                if abs(float(sample["stage1_metric"]) - stage1) > 0.10:
                    stage1_errors += 1
                if abs(float(sample["slew_metric"]) - slew) > 0.08:
                    slew_errors += 1
                if _v4_topup_logic_high(sample, "clamp_flag") != clamped:
                    flag_errors += 1
                if _v4_topup_logic_high(sample, "settled") != (settle_count >= 2):
                    settled_errors += 1
        prev_clk = float(row["clk"])
    ok = checked >= 6 and reset_clear and disabled_clear and slew_seen and clamp_seen and vout_errors <= 3 and stage1_errors <= 3 and slew_errors <= 3 and flag_errors <= 3 and settled_errors <= 3 and clear_errors <= 12
    return ok, f"v4_957 checked={checked} reset_clear={reset_clear} disabled_clear={disabled_clear} slew_seen={slew_seen} clamp_seen={clamp_seen} settled_seen={settled_seen} vout_errors={vout_errors} stage1_errors={stage1_errors} slew_errors={slew_errors} flag_errors={flag_errors} settled_errors={settled_errors} clear_errors={clear_errors}"

CHECKER_ID = "v4_398_two_stage_opamp_slew_macromodel"
CHECKER: Checker = check_v4_957_two_stage_opamp_slew_macromodel
