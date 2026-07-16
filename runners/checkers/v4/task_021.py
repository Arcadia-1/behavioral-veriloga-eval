"""Stimulus-relative checker for canonical v4 DUT 021."""
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
    "P_INITIAL_AND_RESET_TARGET",
    "P_POSITIVE_ERROR_STEP",
    "P_NEGATIVE_ERROR_STEP",
    "P_DEADBAND_HOLD",
    "P_OUTPUT_CLAMP",
    "P_BETWEEN_EDGE_HOLD",
]


def check_calibration_deadband_controller(
    rows: list[dict[str, float]],
) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "vin", "out", "metric"}
    results, error = missing_trace(CHECKER_ID, rows, required, PROPERTY_IDS)
    if error is not None:
        return error
    by_id = {result.property_id: result for result in results}

    edges = rising_indices(rows, "clk")
    edge_times = [float(rows[index]["time"]) for index in edges]
    settle = event_settle_delay(edge_times)
    state = 0.45

    for index in edges:
        edge = rows[index]
        event_time = float(edge["time"])
        if edge["rst"] > 0.45:
            state = 0.45
            expected_metric = 0.0
            property_id = "P_INITIAL_AND_RESET_TARGET"
        else:
            error_v = float(edge["vin"]) - 0.45
            if error_v > 0.05:
                state += 0.06
                expected_metric = 0.9
                property_id = "P_POSITIVE_ERROR_STEP"
            elif error_v < -0.05:
                state -= 0.06
                expected_metric = 0.9
                property_id = "P_NEGATIVE_ERROR_STEP"
            else:
                expected_metric = 0.0
                property_id = "P_DEADBAND_HOLD"
        state = min(0.85, max(0.05, state))
        sample = row_at_or_after(rows, event_time + settle)
        by_id[property_id].compare(
            expected=state,
            observed=sample["out"],
            tolerance=0.018,
            time_s=sample["time"],
            label="out",
        )
        by_id[property_id].compare(
            expected=expected_metric,
            observed=sample["metric"],
            tolerance=0.075,
            time_s=sample["time"],
            label="metric",
        )
        by_id["P_OUTPUT_CLAMP"].condition(
            0.032 <= sample["out"] <= 0.868,
            expected="out_in_[0.05,0.85]",
            observed=f"out={sample['out']:.6g}",
            time_s=sample["time"],
            gap=max(0.05 - sample["out"], sample["out"] - 0.85, 0.0),
        )

    for left, right in zip(edge_times, edge_times[1:]):
        spacing = right - left
        if spacing <= 2.5 * settle:
            continue
        early = row_at_or_after(rows, left + max(settle, 0.30 * spacing))
        late = row_at_or_after(rows, left + 0.78 * spacing)
        by_id["P_BETWEEN_EDGE_HOLD"].compare(
            expected=early["out"],
            observed=late["out"],
            tolerance=0.012,
            time_s=late["time"],
            label="held_out",
        )

    return finish(
        CHECKER_ID,
        results,
        coverage=f"rising_edges={len(edges)} settle_s={settle:.6g}",
    )


CHECKER_ID = "v4_021_calibration_deadband_controller"
CHECKER: Checker = check_calibration_deadband_controller
