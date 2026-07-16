"""Task-specific checker for canonical v4 DUT 374."""
from __future__ import annotations

from ..api import Checker
def _v4_topup_logic_high(row: dict[str, float], name: str, threshold: float = 0.45) -> bool:
    return float(row.get(name, 0.0)) > threshold

def _v4_rising(prev_v: float, now_v: float, vth: float = 0.45) -> bool:
    return now_v > vth and prev_v <= vth

def _v4_first_after(rows: list[dict[str, float]], target_time: float) -> dict[str, float] | None:
    for row in rows:
        if float(row["time"]) >= target_time:
            return row
    return None

def check_v4_374_crystal_oscillator_startup_monitor(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_933 empty_trace"
    prev_clk = float(rows[0].get("clk_ref", 0.0))
    amp = 0.0
    periods = 0
    checked = amp_errors = done_errors = valid_errors = osc_errors = clear_errors = 0
    reset_clear = disabled_clear = ramp_seen = done_seen = valid_seen = osc_activity = False
    reset_seen = enabled_seen = False
    osc_vals: list[float] = []
    expected_osc_high = False
    for row in rows:
        rst = _v4_topup_logic_high(row, "rst")
        enabled = _v4_topup_logic_high(row, "enable") and not rst
        if not enabled:
            amp = 0.0; periods = 0
            expected_osc_high = False
            clear = row["osc_out"] < 0.12 and row["amp_metric"] < 0.08 and row["valid"] < 0.10 and row["startup_done"] < 0.10
            if rst:
                reset_seen = True
                reset_clear = reset_clear or clear
                if not clear:
                    clear_errors += 1
            elif enabled_seen:
                # The first low-enable sample is the observed disable event;
                # accept the DUT's natural settling latency and require a
                # cleared state somewhere in the remaining disabled window.
                disabled_clear = disabled_clear or clear
            prev_clk = float(row["clk_ref"])
            continue
        enabled_seen = True
        osc_vals.append(float(row["osc_out"]))
        if _v4_rising(prev_clk, float(row["clk_ref"])):
            old_amp = amp
            amp = min(0.3, amp + 0.040)
            if amp > 0.0:
                expected_osc_high = not expected_osc_high
            expected_done = amp >= 0.3 - 1e-6
            if expected_done:
                periods += 1
            expected_valid = periods >= 2 and expected_done
            ramp_seen = ramp_seen or amp > old_amp
            done_seen = done_seen or expected_done
            valid_seen = valid_seen or expected_valid
            sample = _v4_first_after(rows, float(row["time"]) + 0.7e-9)
            if sample is not None:
                checked += 1
                if abs(float(sample["amp_metric"]) - amp) > 0.06:
                    amp_errors += 1
                if _v4_topup_logic_high(sample, "startup_done") != expected_done:
                    done_errors += 1
                if _v4_topup_logic_high(sample, "valid") != expected_valid:
                    valid_errors += 1
                if _v4_topup_logic_high(sample, "osc_out") != expected_osc_high:
                    osc_errors += 1
        prev_clk = float(row["clk_ref"])
    osc_activity = bool(osc_vals) and max(osc_vals) > 0.65 and min(osc_vals) < 0.20
    ok = checked >= 8 and reset_seen and reset_clear and enabled_seen and disabled_clear and ramp_seen and done_seen and valid_seen and osc_activity and amp_errors <= 2 and done_errors <= 1 and valid_errors <= 1 and osc_errors <= 1 and clear_errors <= 4
    return ok, f"v4_374 checked={checked} reset_seen={reset_seen} reset_clear={reset_clear} disabled_clear={disabled_clear} ramp_seen={ramp_seen} done_seen={done_seen} valid_seen={valid_seen} osc_activity={osc_activity} amp_errors={amp_errors} done_errors={done_errors} valid_errors={valid_errors} osc_errors={osc_errors} clear_errors={clear_errors}"

CHECKER_ID = "v4_374_crystal_oscillator_startup_monitor"
CHECKER: Checker = check_v4_374_crystal_oscillator_startup_monitor
