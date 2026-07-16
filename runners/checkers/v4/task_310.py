"""Task-specific checker for canonical v4 DUT 310."""
from __future__ import annotations

from ..api import Checker
from ..common.v4_topup import (
    _v4_topup_logic_high,
    _v4_topup_near,
    _v4_topup_span,
)
from ..common.relative_events import active_start, first_disable

def check_v4_310_bootstrapped_sampler_charge_metric(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_1008 empty_trace"
    activation = active_start(rows, enable="enable", reset="rst")
    disable = first_disable(rows, "enable", activation)
    active_rows = [row for row in rows if row["time"] >= activation and _v4_topup_logic_high(row, "enable") and not _v4_topup_logic_high(row, "rst")]
    disabled_clear = any(
        disable is not None and row["time"] >= disable
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
    diagnostics = {
        "P_ON_RESET_OR_WHEN_DISABLED_CLEAR": int(not disabled_clear),
        "P_ON_EACH_RISING_CLK_EDGE_WHILE": int(not (high_input_hold_seen and low_input_hold_seen)),
        "P_EXPOSE_A_BOOT_METRIC_THAT_INCREASES": int(not rail_metric_seen or not cm_metric_low_seen),
        "P_BETWEEN_SAMPLES_HOLD_VHOLD_AND_APPLY": int(not (high_hold_seen and low_hold_seen)),
        "P_ASSERT_DROOP_FLAG_WHEN_ACCUMULATED_HOLD": int(not droop_seen),
        "P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE": 0,
    }
    return ok, (
        f"v4_310 active_rows={len(active_rows)} disabled_clear={disabled_clear} high_hold={high_hold_seen} "
        f"low_hold={low_hold_seen} high_input_hold={high_input_hold_seen} low_input_hold={low_input_hold_seen} "
        f"rail_metric={rail_metric_seen} cm_metric_low={cm_metric_low_seen} "
        f"droop={droop_seen} range_ok={range_ok}; "
        + "; ".join(f"{key} mismatch_count={value}" for key, value in diagnostics.items())
    )

CHECKER_ID = "v4_310_bootstrapped_sampler_charge_metric"
CHECKER: Checker = check_v4_310_bootstrapped_sampler_charge_metric
