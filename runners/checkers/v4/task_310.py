"""Task-specific checker for canonical v4 DUT 310."""
from __future__ import annotations

from ..api import Checker
from ..common.v4_topup import (
    _v4_topup_clip01,
    _v4_topup_logic_high,
)
from ..common.relative_events import event_period, rising_edges, sample_after_event, sample_step

def check_v4_310_bootstrapped_sampler_charge_metric(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_1008 empty_trace"
    edges = rising_edges(rows, "clk")
    period = event_period(rows, "clk")
    guard = max(period * 0.15, sample_step(rows) * 3.0)
    active_edges = inactive_edges = 0
    clear_errors = capture_errors = metric_errors = early_flag_errors = 0
    hold_checked = hold_errors = direction_errors = 0
    late_flag_windows = late_flag_missing = 0
    high_input_hold_seen = low_input_hold_seen = False
    rail_metric_seen = cm_metric_low_seen = droop_seen = False

    for index, edge in enumerate(edges):
        edge_index = next((i for i, row in enumerate(rows) if float(row["time"]) >= edge), None)
        edge_row = rows[max(0, edge_index - 1)] if edge_index is not None else None
        post = sample_after_event(rows, edge, clock_signal="clk", fraction_of_period=0.15)
        if edge_row is None or post is None:
            continue
        active = _v4_topup_logic_high(edge_row, "enable") and not _v4_topup_logic_high(edge_row, "rst")
        if not active:
            inactive_edges += 1
            if (
                abs(float(post["vhold"]) - 0.45) > 0.08
                or float(post["boot_metric"]) > 0.15
                or float(post["droop_flag"]) > 0.15
            ):
                clear_errors += 1
            continue

        active_edges += 1
        captured = float(edge_row["vin"])
        expected_metric = _v4_topup_clip01(2.0 * abs(captured - 0.45))
        if abs(float(post["vhold"]) - captured) > 0.08:
            capture_errors += 1
        if abs(float(post["boot_metric"]) - expected_metric) > 0.12:
            metric_errors += 1
        if float(post["droop_flag"]) > 0.45:
            early_flag_errors += 1
        high_input_hold_seen = high_input_hold_seen or (captured > 0.75 and float(post["vhold"]) > 0.60)
        low_input_hold_seen = low_input_hold_seen or (captured < 0.18 and float(post["vhold"]) < 0.32)
        rail_metric_seen = rail_metric_seen or (abs(captured - 0.45) > 0.25 and float(post["boot_metric"]) > 0.35)
        cm_metric_low_seen = cm_metric_low_seen or (abs(captured - 0.45) < 0.08 and float(post["boot_metric"]) < 0.22)

        next_edge = edges[index + 1] if index + 1 < len(edges) else float(rows[-1]["time"])
        late_rows: list[dict[str, float]] = []
        for hold_row in rows:
            hold_time = float(hold_row["time"])
            if hold_time < edge + guard or hold_time >= next_edge - sample_step(rows) * 2.0:
                continue
            if not _v4_topup_logic_high(hold_row, "enable") or _v4_topup_logic_high(hold_row, "rst"):
                continue
            hold_checked += 1
            held = float(hold_row["vhold"])
            if abs(held - captured) > 0.08:
                hold_errors += 1
            if (held - captured) * (captured - 0.45) > 5e-3:
                direction_errors += 1
            held_metric = _v4_topup_clip01(2.0 * abs(held - 0.45))
            if abs(float(hold_row["boot_metric"]) - held_metric) > 0.12:
                metric_errors += 1
            if hold_time >= edge + 0.75 * period:
                late_rows.append(hold_row)
        if late_rows:
            late_flag_windows += 1
            late_high = any(float(row["droop_flag"]) > 0.45 for row in late_rows)
            droop_seen = droop_seen or late_high
            if not late_high:
                late_flag_missing += 1

    allowed_hold_errors = max(6, hold_checked // 50)
    allowed_metric_errors = max(6, hold_checked // 50)
    ok = (
        active_edges >= 6
        and inactive_edges >= 1
        and high_input_hold_seen
        and low_input_hold_seen
        and rail_metric_seen
        and cm_metric_low_seen
        and droop_seen
        and clear_errors == 0
        and capture_errors <= 1
        and early_flag_errors == 0
        and hold_checked >= 20
        and hold_errors <= allowed_hold_errors
        and direction_errors <= allowed_hold_errors
        and metric_errors <= allowed_metric_errors
        and late_flag_windows >= 2
        and late_flag_missing <= 1
    )
    diagnostics = {
        "P_ON_RESET_OR_WHEN_DISABLED_CLEAR": int(inactive_edges < 1) + clear_errors,
        "P_ON_EACH_RISING_CLK_EDGE_WHILE": int(active_edges < 6) + max(0, capture_errors - 1),
        "P_EXPOSE_A_BOOT_METRIC_THAT_INCREASES": int(not rail_metric_seen or not cm_metric_low_seen) + max(0, metric_errors - allowed_metric_errors),
        "P_BETWEEN_SAMPLES_HOLD_VHOLD_AND_APPLY": max(0, hold_errors - allowed_hold_errors) + max(0, direction_errors - allowed_hold_errors),
        "P_ASSERT_DROOP_FLAG_WHEN_ACCUMULATED_HOLD": early_flag_errors + late_flag_missing + int(not droop_seen),
        "P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE": 0,
    }
    return ok, (
        f"v4_310 active_edges={active_edges} inactive_edges={inactive_edges} clear_errors={clear_errors} "
        f"capture_errors={capture_errors} "
        f"hold_checked={hold_checked} hold_errors={hold_errors} direction_errors={direction_errors} "
        f"metric_errors={metric_errors} early_flag_errors={early_flag_errors} late_flag_windows={late_flag_windows} "
        f"late_flag_missing={late_flag_missing} high_input_hold={high_input_hold_seen} low_input_hold={low_input_hold_seen} "
        f"rail_metric={rail_metric_seen} cm_metric_low={cm_metric_low_seen} droop={droop_seen}; "
        + "; ".join(f"{key} mismatch_count={value}" for key, value in diagnostics.items())
    )

CHECKER_ID = "v4_310_bootstrapped_sampler_charge_metric"
CHECKER: Checker = check_v4_310_bootstrapped_sampler_charge_metric
