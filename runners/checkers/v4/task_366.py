"""Task-specific checker for canonical v4 DUT 366."""
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

def check_v4_925_polyphase_quadrature_filter_macro(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_925 empty_trace"
    prev_clk = float(rows[0].get("clk", 0.0))
    i_state = q_state = 0.45
    count = 0
    checked = i_errors = q_errors = amp_errors = phase_errors = valid_errors = clear_errors = 0
    reset_clear = disabled_clear = iq_separated = valid_seen = False
    for row in rows:
        t = float(row["time"])
        rst = _v4_topup_logic_high(row, "rst")
        enabled = _v4_topup_logic_high(row, "enable") and not rst
        if not enabled:
            i_state = q_state = 0.45; count = 0
            clear = abs(row["i_out"] - 0.45) < 0.08 and abs(row["q_out"] - 0.45) < 0.08 and row["amp_metric"] < 0.10 and row["phase_metric"] < 0.10 and row["valid"] < 0.10
            reset_clear = reset_clear or (rst and t < 5e-9 and clear)
            disabled_clear = disabled_clear or (t > 82e-9 and clear)
            if ((rst and t < 5e-9) or t > 82e-9) and not clear:
                clear_errors += 1
            prev_clk = float(row["clk"])
            continue
        if _v4_rising(prev_clk, float(row["clk"])):
            old_i = i_state
            i_state = i_state + 0.25 * (float(row["vin"]) - i_state)
            q_state = q_state + 0.25 * (old_i - q_state)
            count += 1
            expected_amp = min(0.9, abs(i_state - q_state) * 2.0)
            expected_phase = 0.65 if i_state >= q_state else 0.25
            expected_valid = count >= 4
            sample = _v4_batch001_first_after(rows, t + 0.7e-9)
            if sample is not None:
                checked += 1
                iq_separated = iq_separated or abs(i_state - q_state) > 0.025
                valid_seen = valid_seen or expected_valid
                if abs(float(sample["i_out"]) - i_state) > 0.08:
                    i_errors += 1
                if abs(float(sample["q_out"]) - q_state) > 0.08:
                    q_errors += 1
                if abs(float(sample["amp_metric"]) - expected_amp) > 0.10:
                    amp_errors += 1
                if abs(float(sample["phase_metric"]) - expected_phase) > 0.10:
                    phase_errors += 1
                if _v4_topup_logic_high(sample, "valid") != expected_valid:
                    valid_errors += 1
        prev_clk = float(row["clk"])
    ok = checked >= 6 and reset_clear and disabled_clear and iq_separated and valid_seen and i_errors <= 2 and q_errors <= 2 and amp_errors <= 2 and phase_errors <= 2 and valid_errors <= 1 and clear_errors <= 12
    return ok, f"v4_925 checked={checked} reset_clear={reset_clear} disabled_clear={disabled_clear} iq_separated={iq_separated} valid_seen={valid_seen} i_errors={i_errors} q_errors={q_errors} amp_errors={amp_errors} phase_errors={phase_errors} valid_errors={valid_errors} clear_errors={clear_errors}"

CHECKER_ID = "v4_366_polyphase_quadrature_filter_macro"
CHECKER: Checker = check_v4_925_polyphase_quadrature_filter_macro
