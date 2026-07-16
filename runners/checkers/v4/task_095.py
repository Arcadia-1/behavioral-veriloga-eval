"""Task-specific checker for canonical v4 DUT 095."""
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
    "P_RESET_REGULATION_STATE",
    "P_BOUNDED_LOAD_AND_TARGET",
    "P_CONTROL_MONITOR",
    "P_HEAVY_LOAD_DROOP",
    "P_LIGHT_LOAD_KICK",
    "P_RECOVERY_AND_SETTLING",
]


def _after(intervals: list[tuple[float, float]], time_s: float) -> list[tuple[float, float]]:
    return [interval for interval in intervals if interval[0] > time_s]


def _event(interval: tuple[float, float], label: str) -> str:
    return event_label(label, 0, interval[0])

def check_ldo_load_step_recovery_flow(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "vin", "out", "metric", "load_mon", "ctrl_mon"}
    missing = require_signals(rows, required, "P_BOUNDED_LOAD_AND_TARGET")
    if missing:
        return False, missing

    active = [row for row in rows if row["rst"] <= 0.45]
    heavy_intervals = intervals_where(active, lambda row: row["vin"] > 0.55)
    light_intervals = intervals_where(active, lambda row: row["vin"] < 0.35)
    if len(heavy_intervals) < 2 or len(light_intervals) < 2:
        return False, diagnostic(
            "P_BOUNDED_LOAD_AND_TARGET",
            "missing_load_plateaus",
            expected="two_heavy_and_two_light_load_plateaus",
            observed=f"heavy:{len(heavy_intervals)},light:{len(light_intervals)}",
            event="vin_plateaus",
        )

    pre_interval = light_intervals[0]
    first_heavy = heavy_intervals[0]
    later_lights = _after(light_intervals, first_heavy[0])
    if not later_lights:
        return False, diagnostic(
            "P_LIGHT_LOAD_KICK",
            "missing_light_load_return",
            expected="light_plateau_after_first_heavy_load",
            observed="light_after_heavy:none",
            event=_event(first_heavy, "heavy_load"),
        )
    light_interval = later_lights[0]
    later_heavies = _after(heavy_intervals, light_interval[0])
    if not later_heavies:
        return False, diagnostic(
            "P_HEAVY_LOAD_DROOP",
            "missing_second_heavy_load",
            expected="second_heavy_plateau_after_light_load",
            observed="second_heavy:none",
            event=_event(light_interval, "light_load"),
        )
    second_heavy = later_heavies[0]

    pre_step = mean_in_inner_interval(rows, "out", pre_interval, 0.55, 0.95)
    early_droop = mean_in_inner_interval(rows, "out", first_heavy, 0.08, 0.25)
    late_recovery = mean_in_inner_interval(rows, "out", first_heavy, 0.70, 0.92)
    light_recovery = mean_in_inner_interval(rows, "out", light_interval, 0.50, 0.90)
    second_droop = mean_in_inner_interval(rows, "out", second_heavy, 0.10, 0.35)
    late_metric = mean_in_inner_interval(rows, "metric", first_heavy, 0.70, 0.92)
    pre_load = mean_in_inner_interval(rows, "load_mon", pre_interval, 0.55, 0.95)
    heavy_load = mean_in_inner_interval(rows, "load_mon", first_heavy, 0.08, 0.25)
    light_load = mean_in_inner_interval(rows, "load_mon", light_interval, 0.50, 0.90)
    second_load = mean_in_inner_interval(rows, "load_mon", second_heavy, 0.10, 0.35)
    pre_ctrl = mean_in_inner_interval(rows, "ctrl_mon", pre_interval, 0.55, 0.95)
    heavy_ctrl = mean_in_inner_interval(rows, "ctrl_mon", first_heavy, 0.08, 0.25)
    light_ctrl = mean_in_inner_interval(rows, "ctrl_mon", light_interval, 0.50, 0.90)
    second_ctrl = mean_in_inner_interval(rows, "ctrl_mon", second_heavy, 0.10, 0.35)
    if None in (
        pre_step,
        early_droop,
        late_recovery,
        light_recovery,
        second_droop,
        late_metric,
        pre_load,
        heavy_load,
        light_load,
        second_load,
        pre_ctrl,
        heavy_ctrl,
        light_ctrl,
        second_ctrl,
    ):
        return False, diagnostic(
            "P_RECOVERY_AND_SETTLING",
            "missing_observable_plateau_samples",
            expected="samples_inside_load_plateaus",
            observed="one_or_more_plateau_windows_empty",
            event="vin_plateaus",
        )
    assert pre_step is not None
    assert early_droop is not None
    assert late_recovery is not None
    assert light_recovery is not None
    assert second_droop is not None
    assert late_metric is not None
    assert pre_load is not None
    assert heavy_load is not None
    assert light_load is not None
    assert second_load is not None
    assert pre_ctrl is not None
    assert heavy_ctrl is not None
    assert light_ctrl is not None
    assert second_ctrl is not None

    if not (0.56 <= pre_step <= 0.66):
        return False, diagnostic(
            "P_RESET_REGULATION_STATE",
            "pre_step_regulation_wrong",
            expected="out_between_0.56_and_0.66",
            observed=f"out:{pre_step:.3f}",
            event=_event(pre_interval, "pre_load"),
        )
    if early_droop >= pre_step - 0.04:
        return False, diagnostic(
            "P_HEAVY_LOAD_DROOP",
            "no_transient_droop",
            expected="early_heavy_out_below_pre_by_0.04",
            observed=f"pre:{pre_step:.3f},early:{early_droop:.3f}",
            event=_event(first_heavy, "heavy_load"),
        )
    if late_recovery <= early_droop + 0.040:
        return False, diagnostic(
            "P_RECOVERY_AND_SETTLING",
            "no_closed_loop_recovery",
            expected="late_heavy_out_above_early_by_0.040",
            observed=f"early:{early_droop:.3f},late:{late_recovery:.3f}",
            event=_event(first_heavy, "heavy_load"),
        )
    if light_recovery <= late_recovery:
        return False, diagnostic(
            "P_LIGHT_LOAD_KICK",
            "light_load_not_higher",
            expected="light_load_recovery_above_heavy_recovery",
            observed=f"light:{light_recovery:.3f},heavy_late:{late_recovery:.3f}",
            event=_event(light_interval, "light_load"),
        )
    if second_droop >= light_recovery - 0.035:
        return False, diagnostic(
            "P_HEAVY_LOAD_DROOP",
            "second_step_no_droop",
            expected="second_heavy_out_below_light_by_0.035",
            observed=f"second:{second_droop:.3f},light:{light_recovery:.3f}",
            event=_event(second_heavy, "second_heavy_load"),
        )
    if late_metric < 0.65:
        return False, diagnostic(
            "P_RECOVERY_AND_SETTLING",
            "recovery_metric_low",
            expected="late_recovery_metric_above_0.65",
            observed=f"metric:{late_metric:.3f}",
            event=_event(first_heavy, "heavy_load"),
        )
    if heavy_load <= pre_load + 0.45 or light_load >= heavy_load - 0.35 or second_load <= light_load + 0.35:
        return False, diagnostic(
            "P_BOUNDED_LOAD_AND_TARGET",
            "load_monitor_wrong",
            expected="load_monitor_tracks_light_heavy_light_heavy_sequence",
            observed=f"load:{pre_load:.3f}/{heavy_load:.3f}/{light_load:.3f}/{second_load:.3f}",
            event="vin_plateaus",
        )
    if heavy_ctrl <= pre_ctrl + 0.12:
        return False, diagnostic(
            "P_CONTROL_MONITOR",
            "no_heavy_load_response",
            expected="heavy_ctrl_above_pre_ctrl_by_0.12",
            observed=f"pre:{pre_ctrl:.3f},heavy:{heavy_ctrl:.3f}",
            event=_event(first_heavy, "heavy_load"),
        )
    if light_ctrl >= heavy_ctrl - 0.08:
        return False, diagnostic(
            "P_CONTROL_MONITOR",
            "not_reduced_at_light_load",
            expected="light_ctrl_below_heavy_ctrl_by_0.08",
            observed=f"light:{light_ctrl:.3f},heavy:{heavy_ctrl:.3f}",
            event=_event(light_interval, "light_load"),
        )
    if second_ctrl <= light_ctrl + 0.08:
        return False, diagnostic(
            "P_CONTROL_MONITOR",
            "no_second_step_response",
            expected="second_ctrl_above_light_ctrl_by_0.08",
            observed=f"second:{second_ctrl:.3f},light:{light_ctrl:.3f}",
            event=_event(second_heavy, "second_heavy_load"),
        )
    return True, pass_note(
        PROPERTY_IDS,
        "ldo_load_step_recovery_flow "
        f"pre/early/late/light/second={pre_step:.3f}/{early_droop:.3f}/"
        f"{late_recovery:.3f}/{light_recovery:.3f}/{second_droop:.3f} "
        f"load={pre_load:.3f}/{heavy_load:.3f}/{light_load:.3f}/{second_load:.3f} "
        f"ctrl={pre_ctrl:.3f}/{heavy_ctrl:.3f}/{light_ctrl:.3f}/{second_ctrl:.3f}",
    )

CHECKER_ID = "v4_095_ldo_load_step_recovery"
CHECKER: Checker = check_ldo_load_step_recovery_flow
