"""Task-specific checker for canonical v4 DUT 099."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import (
    diagnostic,
    event_label,
    intervals_where,
    mean_in_inner_interval,
    pass_note,
    require_signals,
)

PROPERTY_IDS = [
    "P_SUPPLY_AND_ENABLE_MONITORS",
    "P_RESET_OR_BROWNOUT",
    "P_DISABLED_REFERENCE",
    "P_ENABLED_SETTLING",
    "P_STARTUP_VALIDITY",
    "P_BROWNOUT_RECOVERY",
]


def _after(intervals: list[tuple[float, float]], time_s: float) -> list[tuple[float, float]]:
    return [interval for interval in intervals if interval[0] > time_s]


def _event(interval: tuple[float, float], label: str) -> str:
    return event_label(label, 0, interval[0])

def check_reference_startup_enable_flow(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "out", "metric"}
    has_legacy_vin = bool(rows and "vin" in rows[0] and "vdd_in" not in rows[0])
    if has_legacy_vin:
        required.add("vin")
    else:
        required.update({"vdd_in", "en"})
    missing = require_signals(rows, required, "P_SUPPLY_AND_ENABLE_MONITORS")
    if missing:
        return False, missing

    supply_key = "vin" if has_legacy_vin else "vdd_in"
    active = [row for row in rows if row["rst"] <= 0.45]
    if has_legacy_vin:
        disabled_intervals = intervals_where(active, lambda row: 0.32 < row[supply_key] < 0.55)
        enabled_intervals = intervals_where(active, lambda row: row[supply_key] > 0.55)
    else:
        disabled_intervals = intervals_where(active, lambda row: row[supply_key] > 0.55 and row["en"] <= 0.20)
        enabled_intervals = intervals_where(active, lambda row: row[supply_key] > 0.55 and row["en"] > 0.55)
    low_supply_intervals = intervals_where(active, lambda row: row[supply_key] <= 0.32)
    if not low_supply_intervals or not disabled_intervals or not enabled_intervals:
        return False, diagnostic(
            "P_SUPPLY_AND_ENABLE_MONITORS",
            "missing_startup_intervals",
            expected="supply_low_disabled_enabled_intervals",
            observed=(
                f"supply_low:{len(low_supply_intervals)},"
                f"disabled:{len(disabled_intervals)},enabled:{len(enabled_intervals)}"
            ),
            event="supply_enable_intervals",
        )

    off_interval = low_supply_intervals[0]
    disabled_interval = disabled_intervals[0]
    startup_interval = enabled_intervals[0]
    brownout_candidates = _after(low_supply_intervals, startup_interval[0])
    if not brownout_candidates:
        return False, diagnostic(
            "P_BROWNOUT_RECOVERY",
            "missing_brownout_interval",
            expected="supply_low_interval_after_startup",
            observed="brownout:none",
            event=_event(startup_interval, "startup_enabled"),
        )
    brownout_interval = brownout_candidates[0]
    recovery_candidates = _after(enabled_intervals, brownout_interval[0])
    if not recovery_candidates:
        return False, diagnostic(
            "P_BROWNOUT_RECOVERY",
            "missing_recovery_interval",
            expected="enabled_supply_interval_after_brownout",
            observed="recovery:none",
            event=_event(brownout_interval, "brownout"),
        )
    recovery_interval = recovery_candidates[0]

    supply_off = mean_in_inner_interval(rows, "out", off_interval, 0.45, 0.90)
    pre_enable = mean_in_inner_interval(rows, "out", disabled_interval, 0.35, 0.90)
    startup_ref = mean_in_inner_interval(rows, "out", startup_interval, 0.50, 0.92)
    startup_metric = mean_in_inner_interval(rows, "metric", startup_interval, 0.50, 0.92)
    dip_reset = mean_in_inner_interval(rows, "out", brownout_interval, 0.25, 0.75)
    recovered_metric = mean_in_inner_interval(rows, "metric", recovery_interval, 0.55, 0.95)
    pre_supply = mean_in_inner_interval(rows, supply_key, disabled_interval, 0.35, 0.90)
    startup_supply = mean_in_inner_interval(rows, supply_key, startup_interval, 0.50, 0.92)
    dip_supply = mean_in_inner_interval(rows, supply_key, brownout_interval, 0.25, 0.75)
    if has_legacy_vin:
        pre_en = 0.0
        startup_en = 0.9
    else:
        pre_en = mean_in_inner_interval(rows, "en", disabled_interval, 0.35, 0.90)
        startup_en = mean_in_inner_interval(rows, "en", startup_interval, 0.50, 0.92)
    if None in (
        supply_off,
        pre_enable,
        startup_ref,
        startup_metric,
        dip_reset,
        recovered_metric,
        pre_supply,
        startup_supply,
        dip_supply,
        pre_en,
        startup_en,
    ):
        return False, diagnostic(
            "P_ENABLED_SETTLING",
            "missing_observable_interval_samples",
            expected="samples_inside_supply_enable_intervals",
            observed="one_or_more_interval_windows_empty",
            event="supply_enable_intervals",
        )
    assert supply_off is not None
    assert pre_enable is not None
    assert startup_ref is not None
    assert startup_metric is not None
    assert dip_reset is not None
    assert recovered_metric is not None
    assert pre_supply is not None
    assert startup_supply is not None
    assert dip_supply is not None
    assert pre_en is not None
    assert startup_en is not None

    if supply_off > 0.08:
        return False, diagnostic(
            "P_RESET_OR_BROWNOUT",
            "supply_off_not_low",
            expected="out_below_0.08_when_supply_off",
            observed=f"out:{supply_off:.3f}",
            event=_event(off_interval, "supply_off"),
        )
    if pre_enable > 0.12:
        return False, diagnostic(
            "P_DISABLED_REFERENCE",
            "ignores_enable",
            expected="out_below_0.12_before_enable",
            observed=f"out:{pre_enable:.3f}",
            event=_event(disabled_interval, "disabled"),
        )
    if has_legacy_vin:
        if not (0.32 < pre_supply < 0.55):
            return False, diagnostic(
                "P_SUPPLY_AND_ENABLE_MONITORS",
                "pre_enable_vin_wrong",
                expected="legacy_vin_between_0.32_and_0.55",
                observed=f"vin:{pre_supply:.3f}",
                event=_event(disabled_interval, "disabled"),
            )
    elif pre_supply <= 0.55 or pre_en >= 0.20:
        return False, diagnostic(
            "P_SUPPLY_AND_ENABLE_MONITORS",
            "pre_enable_inputs_wrong",
            expected="supply_high_and_enable_low_before_startup",
            observed=f"supply:{pre_supply:.3f},en:{pre_en:.3f}",
            event=_event(disabled_interval, "disabled"),
        )
    if startup_ref < 0.48 or startup_ref > 0.60:
        return False, diagnostic(
            "P_ENABLED_SETTLING",
            "wrong_reference",
            expected="settled_reference_between_0.48_and_0.60",
            observed=f"out:{startup_ref:.3f}",
            event=_event(startup_interval, "startup_enabled"),
        )
    if startup_metric < 0.65:
        return False, diagnostic(
            "P_STARTUP_VALIDITY",
            "valid_metric_low",
            expected="startup_metric_above_0.65",
            observed=f"metric:{startup_metric:.3f}",
            event=_event(startup_interval, "startup_enabled"),
        )
    if startup_supply <= 0.55 or startup_en <= 0.55:
        return False, diagnostic(
            "P_SUPPLY_AND_ENABLE_MONITORS",
            "enable_window_inputs_low",
            expected="supply_and_enable_high_during_startup",
            observed=f"supply:{startup_supply:.3f},en:{startup_en:.3f}",
            event=_event(startup_interval, "startup_enabled"),
        )
    if dip_reset > 0.10:
        return False, diagnostic(
            "P_RESET_OR_BROWNOUT",
            "supply_dip_not_reset",
            expected="out_below_0.10_during_brownout",
            observed=f"out:{dip_reset:.3f}",
            event=_event(brownout_interval, "brownout"),
        )
    if dip_supply >= 0.32:
        return False, diagnostic(
            "P_SUPPLY_AND_ENABLE_MONITORS",
            "dip_supply_high",
            expected="brownout_supply_below_0.32",
            observed=f"supply:{dip_supply:.3f}",
            event=_event(brownout_interval, "brownout"),
        )
    if recovered_metric < 0.45:
        return False, diagnostic(
            "P_BROWNOUT_RECOVERY",
            "no_recovery_metric",
            expected="recovered_metric_above_0.45",
            observed=f"metric:{recovered_metric:.3f}",
            event=_event(recovery_interval, "recovery"),
        )
    return True, pass_note(
        PROPERTY_IDS,
        "reference_startup_enable_flow "
        f"pre_enable={pre_enable:.3f} startup={startup_ref:.3f} "
        f"metric={startup_metric:.3f}->{recovered_metric:.3f} dip={dip_reset:.3f}",
    )

CHECKER_ID = "v4_099_reference_startup_enable_flow"
CHECKER: Checker = check_reference_startup_enable_flow
