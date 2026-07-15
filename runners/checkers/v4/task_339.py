"""Task-specific checker for canonical v4 DUT 339."""
from __future__ import annotations

from ..api import Checker
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

def check_v4_1037_pa_ampm_memory_tap_macro(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_1037 empty_trace"
    prev_clk = float(rows[0].get("clk", 0.0))
    prev_amp = 0.0
    checked = vout_errors = am_errors = pm_errors = valid_errors = clear_errors = 0
    reset_clear = disabled_clear = compression_seen = memory_seen = False
    for row in rows:
        t = float(row["time"])
        rst = _v4_topup_logic_high(row, "rst")
        enabled = _v4_topup_logic_high(row, "enable") and not rst
        if not enabled:
            prev_amp = 0.0
            clear = abs(row["vout"] - 0.45) < 0.08 and row["am_metric"] < 0.10 and row["pm_metric"] < 0.10 and row["valid"] < 0.10
            reset_clear = reset_clear or (rst and t < 5e-9 and clear)
            disabled_clear = disabled_clear or (t > 82e-9 and clear)
            if ((rst and t < 5e-9) or t > 82e-9) and not clear:
                clear_errors += 1
            prev_clk = float(row["clk"])
            continue
        if _v4_rising(prev_clk, float(row["clk"])):
            amp = float(row["vin"]) - 0.45
            excess = max(0.0, float(row["drive"]) - 0.55)
            gain = 1.0 / (1.0 + excess / 0.25)
            expected_vout = _v4_topup_clip01(0.45 + amp * gain + 0.2 * prev_amp)
            expected_am = 0.9 * (1.0 - gain)
            expected_pm = _v4_topup_clip01(0.45 + 0.2 * abs(amp - prev_amp))
            sample = _v4_batch001_first_after(rows, t + 0.7e-9)
            if sample is not None:
                checked += 1
                compression_seen = compression_seen or expected_am > 0.05
                memory_seen = memory_seen or expected_pm > 0.47
                if abs(float(sample["vout"]) - expected_vout) > 0.035:
                    vout_errors += 1
                if abs(float(sample["am_metric"]) - expected_am) > 0.06:
                    am_errors += 1
                if abs(float(sample["pm_metric"]) - expected_pm) > 0.06:
                    pm_errors += 1
                if not _v4_topup_logic_high(sample, "valid"):
                    valid_errors += 1
            prev_amp = amp
        prev_clk = float(row["clk"])
    ok = checked >= 6 and reset_clear and disabled_clear and compression_seen and memory_seen and vout_errors <= 1 and am_errors <= 1 and pm_errors <= 1 and valid_errors == 0 and clear_errors <= 3
    return ok, f"v4_1037 checked={checked} reset_clear={reset_clear} disabled_clear={disabled_clear} compression_seen={compression_seen} memory_seen={memory_seen} vout_errors={vout_errors} am_errors={am_errors} pm_errors={pm_errors} valid_errors={valid_errors} clear_errors={clear_errors}"

CHECKER_ID = "v4_339_pa_ampm_memory_tap_macro"
CHECKER: Checker = check_v4_1037_pa_ampm_memory_tap_macro
