"""Stimulus-relative checker for canonical v4 DUT 166."""
from __future__ import annotations

from ..api import Checker, Row
from .batch17_stimulus_relative import (
    bind_properties,
    crossings,
    diagnostic,
    event_label,
    logic_threshold,
    pass_note,
    probe_time,
    require_signals,
    sample,
)


PROPERTY_IDS = (
    "P_FALLING_CLOCK_SAMPLE",
    "P_CONTROL_STEP_WEIGHTS",
    "P_RETAINED_RESIDUE_OUTPUT",
)
SIGNALS = {"time", "vin", "clks", "dctrl1", "dctrl2", "dctrl3", "vres"}
CONTROL_STEPS = {"dctrl3": 0.5, "dctrl2": 0.25, "dctrl1": 0.125}


def check_v3_l2_cdac_4b_residue(rows: list[Row]) -> tuple[bool, str]:
    missing = require_signals(rows, SIGNALS, "P_FALLING_CLOCK_SAMPLE")
    if missing:
        return False, missing

    threshold = logic_threshold(rows, ("clks", "dctrl1", "dctrl2", "dctrl3"), default_high=1.0)
    falling_edges = crossings(rows, "clks", threshold=threshold, direction="falling")
    rising_edges = crossings(rows, "clks", threshold=threshold, direction="rising")
    discriminating_edges = 0
    for falling_t in falling_edges:
        preceding_rise = next(
            (rising_t for rising_t in reversed(rising_edges) if rising_t < falling_t),
            None,
        )
        if preceding_rise is None:
            continue
        vin_at_rise = sample(rows, "vin", preceding_rise)
        vin_at_fall = sample(rows, "vin", falling_t)
        if (
            vin_at_rise is not None
            and vin_at_fall is not None
            and abs(vin_at_fall - vin_at_rise) > 0.05
        ):
            discriminating_edges += 1
    if len(falling_edges) < 2 or discriminating_edges < 1:
        return False, diagnostic(
            "P_FALLING_CLOCK_SAMPLE",
            "coverage",
            expected="at_least_2_falling_edges_and_vin_change_between_rise_and_fall",
            observed=(
                f"falling_edges={len(falling_edges)} "
                f"edge_discriminating_cycles={discriminating_edges}"
            ),
            event="full_trace",
        )
    events: list[tuple[float, str]] = [
        (edge_t, "clks_fall")
        for edge_t in falling_edges
    ]
    for signal in CONTROL_STEPS:
        events.extend(
            (edge_t, signal)
            for edge_t in crossings(rows, signal, threshold=threshold, direction="rising")
        )
    events.sort()
    if len(events) < 4:
        return False, diagnostic(
            "P_CONTROL_STEP_WEIGHTS",
            "coverage",
            expected="falling_clock_plus_3_control_events",
            observed=f"events={len(events)}",
            event="full_trace",
        )

    state = sample(rows, "vin", rows[0]["time"])
    if state is None:
        return False, diagnostic(
            "P_FALLING_CLOCK_SAMPLE",
            "invalid_trace",
            expected="initial_vin_sample",
            observed="missing_sample",
            event="initial_step",
        )

    checked = 0
    max_error = 0.0
    for index, (event_t, kind) in enumerate(events):
        next_event = events[index + 1][0] if index + 1 < len(events) else None
        if kind == "clks_fall":
            sampled_vin = sample(rows, "vin", event_t)
            if sampled_vin is None:
                return False, diagnostic(
                    "P_FALLING_CLOCK_SAMPLE",
                    "invalid_trace",
                    expected="vin_at_falling_clock",
                    observed="missing_sample",
                    event=event_label(kind, index, event_t),
                )
            state = sampled_vin
        else:
            state += CONTROL_STEPS[kind]

        probe_t = probe_time(rows, event_t, next_event, fraction=0.25)
        if probe_t is None:
            continue
        observed = sample(rows, "vres", probe_t)
        label = event_label(kind, index, event_t)
        if observed is None:
            return False, diagnostic(
                "P_RETAINED_RESIDUE_OUTPUT",
                "invalid_trace",
                expected="vres_sample",
                observed="missing_sample",
                event=label,
            )
        error = abs(observed - state)
        max_error = max(max_error, error)
        checked += 1
        if error > 0.03:
            property_id = (
                "P_FALLING_CLOCK_SAMPLE"
                if kind == "clks_fall"
                else "P_CONTROL_STEP_WEIGHTS"
            )
            return False, diagnostic(
                property_id,
                "value_mismatch",
                expected=f"vres={state:.5f}",
                observed=f"vres={observed:.5f}",
                event=label,
            )

    if checked < 4:
        return False, diagnostic(
            "P_CONTROL_STEP_WEIGHTS",
            "coverage",
            expected="at_least_4_checked_events",
            observed=f"checked={checked}",
            event="full_trace",
        )
    return True, pass_note(PROPERTY_IDS, f"checked={checked} max_error={max_error:.5f}")


CHECKER_ID = "v4_166_l2_cdac_4b_residue"
CHECKER: Checker = bind_properties(check_v3_l2_cdac_4b_residue, PROPERTY_IDS)
