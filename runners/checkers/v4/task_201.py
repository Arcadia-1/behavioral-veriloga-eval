"""Task-specific checker for canonical v4 DUT 201."""
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


def check_v3_cdac_6b_stage1_up(rows: list[dict[str, float]]) -> tuple[bool, str]:
    bits = [f"dctrl{bit}" for bit in range(6)]
    required = {"time", "vin", "clks", "vres", *bits}
    property_ids = ["P_AT_INITIALIZATION_AND_ON_EACH_FALLING"]
    results, missing = missing_trace("v4_201", rows, required, property_ids)
    if missing is not None:
        return missing
    behavior = results[0]
    events: list[tuple[float, str, float]] = []
    for edge in edge_times(rows, "clks", threshold=0.5, rising=False):
        events.append((edge, "sample", 0.0))
    for bit, weight in enumerate((0.015625, 0.03125, 0.0625, 0.125, 0.25, 0.5)):
        for edge in edge_times(rows, f"dctrl{bit}", threshold=0.5, rising=True):
            events.append((edge, f"dctrl{bit}", weight))
    events.sort()
    settle = event_settle_delay([event[0] for event in events], minimum_s=5e-11)
    expected = float(rows[0]["vin"])
    controls_seen: set[str] = set()
    sample_events = 0
    sampled_values: list[float] = []

    initial_probe = row_at_or_after(rows, rows[0]["time"] + settle)
    behavior.compare(expected=expected, observed=initial_probe["vres"], tolerance=0.03,
                     time_s=initial_probe["time"], label="initial_vres")
    for index, (edge, kind, weight) in enumerate(events):
        stimulus = row_before(rows, edge)
        if kind == "sample":
            expected = float(stimulus["vin"])
            sample_events += 1
            sampled_values.append(expected)
        else:
            expected += weight
            controls_seen.add(kind)
        next_edge = events[index + 1][0] if index + 1 < len(events) else rows[-1]["time"]
        probe_time = min(edge + settle, edge + 0.4 * max(0.0, next_edge - edge))
        if probe_time <= edge or probe_time > rows[-1]["time"]:
            continue
        probe = row_at_or_after(rows, probe_time)
        behavior.compare(expected=expected, observed=probe["vres"], tolerance=0.03,
                         time_s=probe_time, label=kind)

    required_controls = {f"dctrl{bit}" for bit in range(6)}
    behavior.condition(
        sample_events >= 2
        and max(sampled_values, default=0.0) - min(sampled_values, default=0.0) >= 0.05
        and required_controls.issubset(controls_seen),
        expected="two_changed_falling_samples_and_all_six_control_weights",
        observed=(
            f"sample_events={sample_events}_sampled_values={sampled_values}"
            f"_controls={sorted(controls_seen)}"
            f"_missing_controls={sorted(required_controls - controls_seen)}"
        ),
        time_s=rows[-1]["time"],
    )
    return finish(
        "v4_201", results,
        coverage=f"events={len(events)} sample_events={sample_events} controls={sorted(controls_seen)}",
    )

CHECKER_ID = "v4_201_cdac_6b_stage1_up"
CHECKER: Checker = check_v3_cdac_6b_stage1_up
