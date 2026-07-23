"""Task-specific checker for canonical v4 DUT 312."""
from __future__ import annotations

from ..api import Checker
from ..common.v4_topup import (
    _v4_topup_logic_high,
)


PROPERTY_IDS = (
    "P_ON_RESET_OR_WHEN_DISABLED_CLEAR",
    "P_CAPTURE_VIN_A_ON_RISING_CLK",
    "P_ESTIMATE_A_SKEW_PROXY_FROM_THE",
    "P_DRIVE_SKEW_METRIC_WITH_THE_ABSOLUTE",
    "P_ASSERT_ALARM_WHEN_SKEW_METRIC_EXCEEDS",
    "P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE",
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
    first_mismatch = ""
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
        observed_skew = float(row["skew_metric"])
        observed_mag = float(row["magnitude_metric"])
        observed_alarm = float(row["alarm"]) > 0.45
        if abs(observed_skew - expected_skew) > 0.08:
            skew_errors += 1
            if not first_mismatch:
                first_mismatch = (
                    "P_DRIVE_SKEW_METRIC_WITH_THE_ABSOLUTE "
                    f"signal=skew_metric time={float(row['time']):.6e} "
                    f"expected={expected_skew:.6g} observed={observed_skew:.6g} tolerance=0.08"
                )
        if abs(observed_mag - expected_mag) > 0.08:
            mag_errors += 1
            if not first_mismatch:
                first_mismatch = (
                    "P_DRIVE_SKEW_METRIC_WITH_THE_ABSOLUTE "
                    f"signal=magnitude_metric time={float(row['time']):.6e} "
                    f"expected={expected_mag:.6g} observed={observed_mag:.6g} tolerance=0.08"
                )
        if observed_alarm != expected_alarm:
            alarm_errors += 1
            if not first_mismatch:
                first_mismatch = (
                    "P_ASSERT_ALARM_WHEN_SKEW_METRIC_EXCEEDS "
                    f"signal=alarm time={float(row['time']):.6e} "
                    f"expected={int(expected_alarm)} observed={int(observed_alarm)} tolerance=logic"
                )
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
    summary = (
        f"v4_312 checked={checked} reset_clear={reset_clear} late_reset_clear={late_reset_clear} "
        f"late_reset_violation={late_reset_violation} "
        f"disabled_clear={disabled_clear} "
        f"high_skew={high_skew_seen} low_skew={low_skew_seen} alarm_seen={alarm_seen} "
        f"first_high_alarm_low={first_high_alarm_low_seen} "
        f"skew_errors={skew_errors} mag_errors={mag_errors} alarm_errors={alarm_errors}"
    )
    if not ok and first_mismatch:
        summary += f"; first_mismatch={first_mismatch}"
    property_mismatches = {
        "P_ON_RESET_OR_WHEN_DISABLED_CLEAR": int(
            not reset_clear
            or not late_reset_clear
            or late_reset_violation
            or not disabled_clear
        ),
        "P_CAPTURE_VIN_A_ON_RISING_CLK": skew_errors + mag_errors,
        "P_ESTIMATE_A_SKEW_PROXY_FROM_THE": skew_errors,
        "P_DRIVE_SKEW_METRIC_WITH_THE_ABSOLUTE": skew_errors + mag_errors,
        "P_ASSERT_ALARM_WHEN_SKEW_METRIC_EXCEEDS": alarm_errors,
        "P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE": 0,
    }
    summary += "; " + "; ".join(
        f"{property_id} mismatch_count={property_mismatches[property_id]}"
        for property_id in PROPERTY_IDS
    )
    return ok, summary

CHECKER_ID = "v4_312_interleaved_adc_skew_monitor"
CHECKER: Checker = check_v4_312_interleaved_adc_skew_monitor
