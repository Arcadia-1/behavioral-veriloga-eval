"""Task-specific checker for canonical v4 DUT 043."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import (
    edge_times,
    event_settle_delay,
    finish,
    missing_trace,
    row_at_or_after,
    row_before,
)


PROPERTY_IDS = (
    "P_RESET_NEUTRAL",
    "P_HYSTERESIS_STATE_UPDATE",
    "P_GAINED_LIMITER_TRANSFER",
    "P_OUTPUT_LIMITS",
    "P_STATE_METRIC",
)


def check_release_soft_hysteretic_limiter(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "vin", "out", "metric"}
    results, missing = missing_trace("v4_043", rows, required, list(PROPERTY_IDS))
    if missing is not None:
        return missing
    reset, state_update, transfer, limits, metric = results
    rises = edge_times(rows, "clk", threshold=0.45, rising=True)
    settle = event_settle_delay(rises)
    hysteresis = 0.0
    regions: set[str] = set()
    memory_regions: set[str] = set()

    for edge in rises:
        stimulus = row_before(rows, edge)
        probe_time = edge + settle
        if probe_time > rows[-1]["time"]:
            continue
        probe = row_at_or_after(rows, probe_time)
        if stimulus["rst"] > 0.45:
            hysteresis = 0.0
            expected_out = expected_metric = 0.45
            reset.compare(expected=expected_out, observed=probe["out"], tolerance=0.08,
                          time_s=probe_time, label="reset_out")
            reset.compare(expected=expected_metric, observed=probe["metric"], tolerance=0.08,
                          time_s=probe_time, label="reset_metric")
            continue

        vin = float(stimulus["vin"])
        previous_hysteresis = hysteresis
        if vin > 0.62:
            hysteresis = 0.08
            regions.add("high")
        elif vin < 0.38:
            hysteresis = -0.08
            regions.add("low")
        elif previous_hysteresis > 0:
            memory_regions.add("high")
        elif previous_hysteresis < 0:
            memory_regions.add("low")
        expected_out = min(0.82, max(0.10, 1.8 * (vin - 0.45) + 0.45 + hysteresis))
        expected_metric = 0.45 + 2.0 * hysteresis
        state_update.compare(expected=expected_metric, observed=probe["metric"], tolerance=0.08,
                             time_s=probe_time, label="state_metric")
        transfer.compare(expected=expected_out, observed=probe["out"], tolerance=0.08,
                         time_s=probe_time, label="held_out")
        limits.condition(0.08 <= probe["out"] <= 0.84,
                         expected="0.10<=out<=0.82", observed=f"out={probe['out']:.6g}",
                         time_s=probe_time)
        metric.compare(expected=expected_metric, observed=probe["metric"], tolerance=0.08,
                       time_s=probe_time, label="metric")

    state_update.condition(
        regions == {"high", "low"} and memory_regions == {"high", "low"},
        expected="high_low_and_both_memory_regions",
        observed=f"regions={sorted(regions)}_memory={sorted(memory_regions)}",
        time_s=rows[-1]["time"],
    )
    reset.require_coverage(2)
    for result in (transfer, limits, metric):
        result.require_coverage(4)
    return finish(
        "v4_043", results,
        coverage=f"clock_rises={len(rises)} regions={sorted(regions)} memory={sorted(memory_regions)}",
    )

CHECKER_ID = "v4_043_soft_hysteretic_limiter"
CHECKER: Checker = check_release_soft_hysteretic_limiter
