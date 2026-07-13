"""Task-specific checker for canonical v4 DUT 310."""
from __future__ import annotations

from checkers.api import Checker
from checkers.common.v4_topup import (
    _v4_topup_logic_high,
    _v4_topup_near,
    _v4_topup_span,
)

def check_v4_1008_bootstrapped_sampler_charge_metric(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_1008 empty_trace"
    active_rows = [row for row in rows if row["time"] > 8e-9 and _v4_topup_logic_high(row, "enable") and not _v4_topup_logic_high(row, "rst")]
    disabled_clear = any(
        row["time"] > 58e-9
        and not _v4_topup_logic_high(row, "enable")
        and _v4_topup_near(row["vhold"], 0.45, 0.08)
        and row["boot_metric"] < 0.15
        and row["droop_flag"] < 0.15
        for row in rows
    )
    if len(active_rows) < 20:
        return False, f"v4_1008 too_few_active_rows={len(active_rows)}"
    high_hold_seen = any(row["vhold"] > 0.65 for row in active_rows)
    low_hold_seen = any(row["vhold"] < 0.25 for row in active_rows)
    high_input_hold_seen = any(row["vin"] > 0.75 and row["vhold"] > 0.60 for row in active_rows)
    low_input_hold_seen = any(row["vin"] < 0.18 and row["vhold"] < 0.32 for row in active_rows)
    rail_metric_seen = any(abs(row["vin"] - 0.45) > 0.25 and row["boot_metric"] > 0.35 for row in active_rows)
    cm_metric_low_seen = any(abs(row["vin"] - 0.45) < 0.08 and row["boot_metric"] < 0.22 for row in active_rows)
    droop_seen = any(row["droop_flag"] > 0.45 for row in active_rows)
    range_ok = _v4_topup_span(active_rows, "vhold") > 0.35 and _v4_topup_span(active_rows, "boot_metric") > 0.25
    ok = (
        disabled_clear
        and high_hold_seen
        and low_hold_seen
        and high_input_hold_seen
        and low_input_hold_seen
        and rail_metric_seen
        and cm_metric_low_seen
        and droop_seen
        and range_ok
    )
    return ok, (
        f"v4_1008 active_rows={len(active_rows)} disabled_clear={disabled_clear} high_hold={high_hold_seen} "
        f"low_hold={low_hold_seen} high_input_hold={high_input_hold_seen} low_input_hold={low_input_hold_seen} "
        f"rail_metric={rail_metric_seen} cm_metric_low={cm_metric_low_seen} "
        f"droop={droop_seen} range_ok={range_ok}"
    )

CHECKER_ID = "v4_1008_bootstrapped_sampler_charge_metric"
CHECKER: Checker = check_v4_1008_bootstrapped_sampler_charge_metric
