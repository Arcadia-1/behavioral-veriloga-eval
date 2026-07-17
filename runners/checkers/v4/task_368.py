"""Task-specific checker for canonical v4 DUT 368."""
from __future__ import annotations

from ..api import Checker
from .diagnostics import with_property_diagnostics

SETTLE = 7.0e-10

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
    time_scale = float(rows[0].get("_time_scale", 1.0))
    prev_clk = float(rows[0].get("clk", 0.0))
    valid_count = 0
    checked = vout_errors = flag_errors = amp_errors = decision_errors = valid_errors = clear_errors = 0
    reset_clear = disabled_clear = limit_seen = decision_high = decision_low = valid_seen = False
    ever_enabled = False
    stable_samples = 0
    last_input_change = float(rows[0]["time"])
    previous_inputs = {
        name: float(rows[0][name]) for name in ("vin_proxy", "rst", "enable")
    }
    for row in rows:
        t = float(row["time"])
        current_inputs = {
            name: float(row[name]) for name in ("vin_proxy", "rst", "enable")
        }
        if any(
            abs(current_inputs[name] - previous_inputs[name]) > 1.0e-9
            for name in current_inputs
        ):
            last_input_change = t
        previous_inputs = current_inputs
        stable = t - last_input_change >= time_scale * SETTLE
        rst = _v4_topup_logic_high(row, "rst")
        enabled = _v4_topup_logic_high(row, "enable") and not rst
        if not enabled:
            valid_count = 0
            if stable:
                clear = abs(row["vout"] - 0.45) < 0.08 and row["decision"] < 0.10 and row["limit_flag"] < 0.10 and row["valid"] < 0.10 and row["amp_metric"] < 0.10
                disabled = ever_enabled and not _v4_topup_logic_high(row, "enable")
                reset_clear = reset_clear or (rst and clear)
                disabled_clear = disabled_clear or (disabled and clear)
                if (rst or disabled) and not clear:
                    clear_errors += 1
            prev_clk = float(row["clk"])
            continue
        ever_enabled = True
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
            sample = _v4_batch001_first_after(rows, t + time_scale * 0.7e-9)
            if sample is not None:
                if _v4_topup_logic_high(sample, "decision") != expected_decision:
                    decision_errors += 1
                if _v4_topup_logic_high(sample, "valid") != expected_valid:
                    valid_errors += 1
        if stable:
            stable_samples += 1
        if stable and stable_samples % 6 == 0:
            if abs(float(row["vout"]) - expected_vout) > 0.10:
                vout_errors += 1
            if _v4_topup_logic_high(row, "limit_flag") != expected_flag:
                flag_errors += 1
            if abs(float(row["amp_metric"]) - expected_amp) > 0.10:
                amp_errors += 1
            checked += 1
            limit_seen = limit_seen or expected_flag
        prev_clk = float(row["clk"])
    ok = checked >= 40 and reset_clear and disabled_clear and limit_seen and decision_high and decision_low and valid_seen and vout_errors <= 4 and flag_errors <= 4 and amp_errors <= 4 and decision_errors <= 2 and valid_errors == 0 and clear_errors <= 12
    return ok, f"v4_927 checked={checked} reset_clear={reset_clear} disabled_clear={disabled_clear} limit_seen={limit_seen} decision_high={decision_high} decision_low={decision_low} valid_seen={valid_seen} vout_errors={vout_errors} flag_errors={flag_errors} amp_errors={amp_errors} decision_errors={decision_errors} valid_errors={valid_errors} clear_errors={clear_errors}"

CHECKER_ID = "v4_368_tia_limiting_receiver_macro"
CHECKER: Checker = with_property_diagnostics(
    check_v4_927_tia_limiting_receiver_macro,
    {
        "P_ON_RESET_OR_WHEN_ENABLE_IS": (
            "clear_errors",
            "!reset_clear",
            "!disabled_clear",
        ),
        "P_TREAT_VIN_PROXY_AS_A_VOLTAGE": "vout_errors",
        "P_APPLY_GAIN_TO_THE_DEVIATION_FROM": (
            "vout_errors",
            "amp_errors",
        ),
        "P_ASSERT_LIMIT_FLAG_WHEN_THE_UNCLAMPED": (
            "flag_errors",
            "!limit_seen",
        ),
        "P_ON_EACH_RISING_CLK_EDGE_DRIVE": (
            "decision_errors",
            "!decision_high",
            "!decision_low",
        ),
        "P_ASSERT_VALID_WHEN_AMP_METRIC_IS": (
            "valid_errors",
            "!valid_seen",
        ),
    },
)
