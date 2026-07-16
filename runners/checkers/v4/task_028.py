"""Stimulus-relative checker for canonical v4 DUT 028."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import (
    event_settle_delay,
    finish,
    missing_trace,
    rising_indices,
    row_at_or_after,
)


PROPERTY_IDS = [
    "P_COMMON_MODE_INITIAL_RESET",
    "P_GAINED_BOUNDED_TARGET",
    "P_TWO_POLE_SAMPLED_SETTLING",
    "P_LAG_METRIC",
    "P_SIGNAL_RANGE",
]


def check_higher_order_filter(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "vin", "out", "metric"}
    results, error = missing_trace(CHECKER_ID, rows, required, PROPERTY_IDS)
    if error is not None:
        return error
    by_id = {result.property_id: result for result in results}

    edges = rising_indices(rows, "clk")
    edge_times = [float(rows[index]["time"]) for index in edges]
    settle = event_settle_delay(edge_times)
    state1 = 0.45
    state2 = 0.45
    high_target_edges = 0
    low_target_edges = 0
    reset_edges = 0

    for index in edges:
        edge = rows[index]
        event_time = float(edge["time"])
        if edge["rst"] > 0.45:
            state1 = 0.45
            state2 = 0.45
            target = 0.45
            reset_edges += 1
            property_id = "P_COMMON_MODE_INITIAL_RESET"
        else:
            target = min(0.9, max(0.0, 1.8 * (edge["vin"] - 0.45) + 0.45))
            state1 += 0.18 * (target - state1)
            state2 += 0.18 * (state1 - state2)
            if target > 0.75:
                high_target_edges += 1
            if target < 0.15:
                low_target_edges += 1
            property_id = "P_GAINED_BOUNDED_TARGET"
        expected_out = min(0.9, max(0.0, state2))
        expected_metric = state1 - state2 + 0.45
        sample = row_at_or_after(rows, event_time + settle)
        by_id[property_id].compare(
            expected=expected_out,
            observed=sample["out"],
            tolerance=0.018,
            time_s=sample["time"],
            label="out",
        )
        by_id["P_TWO_POLE_SAMPLED_SETTLING"].compare(
            expected=expected_out,
            observed=sample["out"],
            tolerance=0.018,
            time_s=sample["time"],
            label="second_state",
        )
        by_id["P_LAG_METRIC"].compare(
            expected=expected_metric,
            observed=sample["metric"],
            tolerance=0.045,
            time_s=sample["time"],
            label="lag_metric",
        )
        by_id["P_SIGNAL_RANGE"].condition(
            -0.02 <= sample["out"] <= 0.92,
            expected="out_in_[0,0.9]",
            observed=f"out={sample['out']:.6g}",
            time_s=sample["time"],
            gap=max(-sample["out"], sample["out"] - 0.9, 0.0),
        )

    by_id["P_COMMON_MODE_INITIAL_RESET"].condition(
        reset_edges >= 1,
        expected="sampled_active_high_reset",
        observed=f"reset_edges={reset_edges}",
        time_s=edge_times[-1] if edge_times else 0.0,
        gap=max(0, 1 - reset_edges),
    )
    by_id["P_GAINED_BOUNDED_TARGET"].condition(
        high_target_edges >= 2 and low_target_edges >= 2,
        expected="bounded_high_and_low_targets_exercised",
        observed=f"high={high_target_edges},low={low_target_edges}",
        time_s=edge_times[-1] if edge_times else 0.0,
        gap=max(0, 2 - high_target_edges) + max(0, 2 - low_target_edges),
    )
    return finish(
        CHECKER_ID,
        results,
        coverage=(
            f"rising_edges={len(edges)} reset_edges={reset_edges} "
            f"high_targets={high_target_edges} low_targets={low_target_edges} "
            f"settle_s={settle:.6g}"
        ),
    )


CHECKER_ID = "v4_028_higher_order_filter"
CHECKER: Checker = check_higher_order_filter
