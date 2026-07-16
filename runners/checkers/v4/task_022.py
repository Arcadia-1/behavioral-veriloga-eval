"""Stimulus-relative checker for canonical v4 DUT 022."""
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
    "P_RESET_MIDSCALE",
    "P_UP_ONLY_STEP",
    "P_DN_ONLY_STEP",
    "P_HOLD_CASES",
    "P_CONTROL_CLAMP",
    "P_SAMPLED_HOLD",
]


def check_charge_pump_abstraction(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "up", "dn", "vctrl", "metric"}
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
            expected_metric = 0.45
            property_id = "P_RESET_MIDSCALE"
        else:
            up = edge["up"] > 0.45
            down = edge["dn"] > 0.45
            if up and not down:
                state += 0.06
                expected_metric = 0.75
                property_id = "P_UP_ONLY_STEP"
            elif down and not up:
                state -= 0.06
                expected_metric = 0.15
                property_id = "P_DN_ONLY_STEP"
            else:
                expected_metric = 0.45
                property_id = "P_HOLD_CASES"
        state = min(0.85, max(0.05, state))
        sample = row_at_or_after(rows, event_time + settle)
        by_id[property_id].compare(
            expected=state,
            observed=sample["vctrl"],
            tolerance=0.018,
            time_s=sample["time"],
            label="vctrl",
        )
        by_id[property_id].compare(
            expected=expected_metric,
            observed=sample["metric"],
            tolerance=0.055,
            time_s=sample["time"],
            label="metric",
        )
        by_id["P_CONTROL_CLAMP"].condition(
            0.032 <= sample["vctrl"] <= 0.868,
            expected="vctrl_in_[0.05,0.85]",
            observed=f"vctrl={sample['vctrl']:.6g}",
            time_s=sample["time"],
            gap=max(0.05 - sample["vctrl"], sample["vctrl"] - 0.85, 0.0),
        )

    for left, right in zip(edge_times, edge_times[1:]):
        spacing = right - left
        if spacing <= 2.5 * settle:
            continue
        early = row_at_or_after(rows, left + max(settle, 0.30 * spacing))
        late = row_at_or_after(rows, left + 0.78 * spacing)
        by_id["P_SAMPLED_HOLD"].compare(
            expected=early["vctrl"],
            observed=late["vctrl"],
            tolerance=0.012,
            time_s=late["time"],
            label="held_vctrl",
        )

    return finish(
        CHECKER_ID,
        results,
        coverage=f"rising_edges={len(edges)} settle_s={settle:.6g}",
    )


CHECKER_ID = "v4_022_charge_pump_abstraction"
CHECKER: Checker = check_charge_pump_abstraction
