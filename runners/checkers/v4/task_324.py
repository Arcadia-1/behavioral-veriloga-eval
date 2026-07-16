"""Task-specific checker for canonical v4 DUT 324."""
from __future__ import annotations

from ..api import Checker
def _v4_topup_logic_high(row: dict[str, float], name: str, threshold: float = 0.45) -> bool:
    return float(row.get(name, 0.0)) > threshold

def check_v4_1022_duty_cycle_window_monitor(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_1022 empty_trace"
    prev_clk = float(rows[0].get("clk_in", 0.0))
    last_rise = None
    last_fall = None
    expected_duty = None
    update_time = -1.0
    checked = metric_errors = window_errors = valid_errors = clear_errors = 0
    reset_clear = disabled_clear = high_duty_seen = low_duty_seen = in_window_seen = out_window_seen = False
    ever_enabled = False
    for row in rows:
        t = float(row["time"])
        clk = float(row["clk_in"])
        rst = _v4_topup_logic_high(row, "rst")
        enabled = _v4_topup_logic_high(row, "enable") and not rst
        if not enabled:
            last_rise = None
            last_fall = None
            expected_duty = None
            clear = abs(float(row["duty_metric"])) < 0.08 and not _v4_topup_logic_high(row, "in_window") and not _v4_topup_logic_high(row, "valid")
            disabled = ever_enabled and not _v4_topup_logic_high(row, "enable")
            if rst and clear:
                reset_clear = True
            if disabled and clear:
                disabled_clear = True
            if ((rst and reset_clear) or (disabled and disabled_clear)) and not clear:
                clear_errors += 1
            prev_clk = clk
            continue
        ever_enabled = True
        if prev_clk <= 0.45 and clk > 0.45:
            if last_rise is not None and last_fall is not None and last_rise < last_fall < t:
                expected_duty = (last_fall - last_rise) / (t - last_rise)
                update_time = t
                if expected_duty >= 0.6:
                    high_duty_seen = True
                if expected_duty <= 0.35:
                    low_duty_seen = True
            last_rise = t
        if prev_clk > 0.45 and clk <= 0.45:
            last_fall = t
        prev_clk = clk
        if expected_duty is None or t < update_time + 0.7e-9:
            continue
        checked += 1
        expected_metric = 0.9 * expected_duty
        min_f = max(0.0, min(1.0, float(row["duty_min"]) / 0.9))
        max_f = max(0.0, min(1.0, float(row["duty_max"]) / 0.9))
        expected_window = min_f <= expected_duty <= max_f
        in_window_seen = in_window_seen or expected_window
        out_window_seen = out_window_seen or (not expected_window)
        if abs(float(row["duty_metric"]) - expected_metric) > 0.08:
            metric_errors += 1
        if _v4_topup_logic_high(row, "in_window") != expected_window:
            window_errors += 1
        if not _v4_topup_logic_high(row, "valid"):
            valid_errors += 1
    metric_budget = max(6, checked // 12)
    window_budget = max(6, checked // 12)
    valid_budget = 3
    clear_budget = 4
    ok = (
        checked >= 40
        and reset_clear
        and disabled_clear
        and high_duty_seen
        and low_duty_seen
        and in_window_seen
        and out_window_seen
        and metric_errors <= metric_budget
        and window_errors <= window_budget
        and valid_errors <= valid_budget
        and clear_errors <= clear_budget
    )
    return ok, (
        f"v4_1022 checked={checked} reset_clear={reset_clear} disabled_clear={disabled_clear} "
        f"high_duty_seen={high_duty_seen} low_duty_seen={low_duty_seen} in_window_seen={in_window_seen} "
        f"out_window_seen={out_window_seen} metric_errors={metric_errors} window_errors={window_errors} "
        f"valid_errors={valid_errors} clear_errors={clear_errors}; "
        f"P_ON_RESET_OR_WHEN_DISABLED_CLEAR mismatch_count={max(0, clear_errors - clear_budget) + int(not reset_clear) + int(not disabled_clear)}; "
        f"P_MEASURE_HIGH_AND_LOW_INTERVALS_OVER mismatch_count={int(not high_duty_seen) + int(not low_duty_seen)}; "
        f"P_DRIVE_DUTY_METRIC_AS_THE_MEASURED mismatch_count={max(0, metric_errors - metric_budget)}; "
        f"P_ASSERT_IN_WINDOW_ONLY_WHEN_THE mismatch_count={max(0, window_errors - window_budget)}; "
        f"P_ASSERT_VALID_AFTER_A_COMPLETE_HIGH mismatch_count={max(0, valid_errors - valid_budget)}"
    )

CHECKER_ID = "v4_324_duty_cycle_window_monitor"
CHECKER: Checker = check_v4_1022_duty_cycle_window_monitor
