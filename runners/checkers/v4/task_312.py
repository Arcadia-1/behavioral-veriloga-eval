"""Task-specific checker for canonical v4 DUT 312."""
from __future__ import annotations

from ..api import Checker
from ..common.v4_topup import (
    _v4_topup_logic_high,
)

def check_v4_312_interleaved_adc_skew_monitor(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_1010 empty_trace"
    sa = sb = 0.45
    ready_a = ready_b = False
    consecutive = 0
    checked = skew_errors = mag_errors = alarm_errors = 0
    reset_clear = late_reset_clear = late_reset_violation = disabled_clear = False
    high_skew_seen = low_skew_seen = alarm_seen = False
    first_high_alarm_low_seen = False
    saw_active = False
    previous = rows[0]
    for index, row in enumerate(rows[1:], start=1):
        clk_a_rise = (not _v4_topup_logic_high(previous, "clk_a")) and _v4_topup_logic_high(row, "clk_a")
        clk_b_rise = (not _v4_topup_logic_high(previous, "clk_b")) and _v4_topup_logic_high(row, "clk_b")
        if clk_a_rise or clk_b_rise:
            if _v4_topup_logic_high(row, "rst") or not _v4_topup_logic_high(row, "enable"):
                sa = sb = 0.45
                ready_a = ready_b = False
                consecutive = 0
            else:
                saw_active = True
                if clk_a_rise:
                    sa = float(row["vin_a"])
                    ready_a = True
                if clk_b_rise:
                    sb = float(row["vin_b"])
                    ready_b = True
        previous = row
        if index % 8 != 0:
            continue
        if _v4_topup_logic_high(row, "rst"):
            cleared = (
                row["skew_metric"] < 0.1 and row["magnitude_metric"] < 0.1 and row["alarm"] < 0.1
            )
            if saw_active:
                late_reset_clear = late_reset_clear or cleared
                late_reset_violation = late_reset_violation or not cleared
            else:
                reset_clear = reset_clear or cleared
            # The public stimulus asserts reset again after valid traffic.  A
            # reset implementation that only clears at initial_step must not
            # pass by relying on the first reset window.
            continue
        if not _v4_topup_logic_high(row, "enable"):
            disabled_clear = disabled_clear or (
                row["skew_metric"] < 0.1 and row["magnitude_metric"] < 0.1 and row["alarm"] < 0.1
            )
            consecutive = 0
            continue
        if not (ready_a and ready_b):
            continue
        expected_skew = abs(sa - sb)
        expected_mag = 0.5 * (abs(sa - 0.45) + abs(sb - 0.45))
        if expected_skew > 0.04:
            consecutive += 1
            high_skew_seen = True
        else:
            consecutive = 0
            low_skew_seen = True
        expected_alarm = consecutive >= 2
        if expected_skew > 0.04 and consecutive == 1 and row["alarm"] < 0.35:
            first_high_alarm_low_seen = True
        checked += 1
        alarm_seen = alarm_seen or row["alarm"] > 0.45
        if abs(float(row["skew_metric"]) - expected_skew) > 0.08:
            skew_errors += 1
        if abs(float(row["magnitude_metric"]) - expected_mag) > 0.08:
            mag_errors += 1
        if (float(row["alarm"]) > 0.45) != expected_alarm:
            alarm_errors += 1
    ok = (
        checked >= 20
        and reset_clear
        and late_reset_clear
        and not late_reset_violation
        and disabled_clear
        and high_skew_seen
        and low_skew_seen
        and alarm_seen
        and first_high_alarm_low_seen
        and skew_errors <= max(14, checked // 8)
        and mag_errors <= max(5, checked // 20)
        and alarm_errors <= 14
    )
    return ok, (
        f"v4_312 checked={checked} reset_clear={reset_clear} late_reset_clear={late_reset_clear} "
        f"late_reset_violation={late_reset_violation} "
        f"disabled_clear={disabled_clear} "
        f"high_skew={high_skew_seen} low_skew={low_skew_seen} alarm_seen={alarm_seen} "
        f"first_high_alarm_low={first_high_alarm_low_seen} "
        f"skew_errors={skew_errors} mag_errors={mag_errors} alarm_errors={alarm_errors}"
    )

CHECKER_ID = "v4_312_interleaved_adc_skew_monitor"
CHECKER: Checker = check_v4_312_interleaved_adc_skew_monitor
