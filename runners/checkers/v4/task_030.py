"""Stimulus-relative checker for canonical v4 DUT 030."""
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
    "P_INITIAL_AND_RESET_STATE",
    "P_LOAD_TARGET",
    "P_FIRST_ORDER_REGULATION",
    "P_REGULATED_OUTPUT_CLAMP",
    "P_ERROR_METRIC",
    "P_CLOCKED_HOLD",
]


def check_ldo_regulator_macro_model(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "vin", "out", "metric"}
    results, error = missing_trace(CHECKER_ID, rows, required, PROPERTY_IDS)
    if error is not None:
        return error
    by_id = {result.property_id: result for result in results}

    edges = rising_indices(rows, "clk")
    edge_times = [float(rows[index]["time"]) for index in edges]
    settle = event_settle_delay(edge_times)
    state = 0.60
    reset_edges = 0
    loads: set[float] = set()
    rising_updates = 0
    falling_updates = 0

    for index in edges:
        edge = rows[index]
        event_time = float(edge["time"])
        previous_state = state
        if edge["rst"] > 0.45:
            state = 0.60
            expected_metric = 0.9
            target = 0.60
            reset_edges += 1
            property_id = "P_INITIAL_AND_RESET_STATE"
        else:
            load = min(0.9, max(0.0, float(edge["vin"])))
            loads.add(round(load, 4))
            target = 0.62 - 0.055 * load
            state += 0.35 * (target - state)
            state = min(0.75, max(0.25, state))
            expected_metric = min(0.9, max(0.0, 0.9 - 4.0 * abs(state - target)))
            if state > previous_state + 1e-6:
                rising_updates += 1
            if state < previous_state - 1e-6:
                falling_updates += 1
            property_id = "P_LOAD_TARGET"
        sample = row_at_or_after(rows, event_time + settle)
        by_id[property_id].compare(
            expected=state,
            observed=sample["out"],
            tolerance=0.016,
            time_s=sample["time"],
            label="regulated_out",
        )
        by_id["P_FIRST_ORDER_REGULATION"].compare(
            expected=state,
            observed=sample["out"],
            tolerance=0.016,
            time_s=sample["time"],
            label="first_order_out",
        )
        by_id["P_ERROR_METRIC"].compare(
            expected=expected_metric,
            observed=sample["metric"],
            tolerance=0.055,
            time_s=sample["time"],
            label="error_metric",
        )
        by_id["P_REGULATED_OUTPUT_CLAMP"].condition(
            0.232 <= sample["out"] <= 0.768,
            expected="out_in_[0.25,0.75]",
            observed=f"out={sample['out']:.6g}",
            time_s=sample["time"],
            gap=max(0.25 - sample["out"], sample["out"] - 0.75, 0.0),
        )

    for left, right in zip(edge_times, edge_times[1:]):
        spacing = right - left
        if spacing <= 2.5 * settle:
            continue
        early = row_at_or_after(rows, left + max(settle, 0.30 * spacing))
        late = row_at_or_after(rows, left + 0.78 * spacing)
        by_id["P_CLOCKED_HOLD"].compare(
            expected=early["out"],
            observed=late["out"],
            tolerance=0.010,
            time_s=late["time"],
            label="held_out",
        )
        by_id["P_CLOCKED_HOLD"].compare(
            expected=early["metric"],
            observed=late["metric"],
            tolerance=0.025,
            time_s=late["time"],
            label="held_metric",
        )

    by_id["P_INITIAL_AND_RESET_STATE"].condition(
        reset_edges >= 1,
        expected="sampled_active_high_reset",
        observed=f"reset_edges={reset_edges}",
        time_s=edge_times[-1] if edge_times else 0.0,
        gap=max(0, 1 - reset_edges),
    )
    by_id["P_LOAD_TARGET"].condition(
        len(loads) >= 3,
        expected="at_least_3_distinct_loads",
        observed=f"loads={sorted(loads)}",
        time_s=edge_times[-1] if edge_times else 0.0,
        gap=max(0, 3 - len(loads)),
    )
    by_id["P_FIRST_ORDER_REGULATION"].condition(
        rising_updates >= 1 and falling_updates >= 1,
        expected="rising_and_falling_regulation_exercised",
        observed=f"rising={rising_updates},falling={falling_updates}",
        time_s=edge_times[-1] if edge_times else 0.0,
        gap=max(0, 1 - rising_updates) + max(0, 1 - falling_updates),
    )
    return finish(
        CHECKER_ID,
        results,
        coverage=(
            f"rising_edges={len(edges)} reset_edges={reset_edges} loads={len(loads)} "
            f"rising_updates={rising_updates} falling_updates={falling_updates} "
            f"settle_s={settle:.6g}"
        ),
    )


CHECKER_ID = "v4_030_ldo_regulator_macro_model"
CHECKER: Checker = check_ldo_regulator_macro_model
