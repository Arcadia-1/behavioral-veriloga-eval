"""Stimulus-relative checker for canonical v4 DUT 167."""
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
    "P_MODULO8_COUNTER",
    "P_INCREMENT_BEFORE_SELECTION",
    "P_ANALOG_CHANNEL_MUX",
    "P_COUNTER_MONITOR_LEVEL",
)
INPUTS = tuple(f"in{index}" for index in range(8))
SIGNALS = {"time", "clk", "out", "count_x"} | set(INPUTS)


def check_v3_ideal_clkmux_8channel(rows: list[Row]) -> tuple[bool, str]:
    missing = require_signals(rows, SIGNALS, "P_MODULO8_COUNTER")
    if missing:
        return False, missing

    threshold = logic_threshold(rows, ("clk",), default_high=1.0)
    clk_edges = crossings(rows, "clk", threshold=threshold, direction="rising")
    if len(clk_edges) < 6:
        return False, diagnostic(
            "P_INCREMENT_BEFORE_SELECTION",
            "coverage",
            expected="at_least_6_clk_rises",
            observed=f"clk_rises={len(clk_edges)}",
            event="full_trace",
        )

    count = 0
    checked = 0
    max_out_error = 0.0
    max_count_error = 0.0
    for index, edge_t in enumerate(clk_edges):
        count = (count + 1) % 8
        next_edge = clk_edges[index + 1] if index + 1 < len(clk_edges) else None
        probe_t = probe_time(rows, edge_t, next_edge, fraction=0.25)
        if probe_t is None:
            continue
        expected_out = sample(rows, f"in{count}", edge_t)
        observed_out = sample(rows, "out", probe_t)
        observed_count = sample(rows, "count_x", probe_t)
        label = event_label("clk_rise", index, edge_t)
        if expected_out is None or observed_out is None or observed_count is None:
            return False, diagnostic(
                "P_ANALOG_CHANNEL_MUX",
                "invalid_trace",
                expected="selected_input_out_count",
                observed="missing_sample",
                event=label,
            )
        out_error = abs(observed_out - expected_out)
        count_error = abs(observed_count - float(count))
        max_out_error = max(max_out_error, out_error)
        max_count_error = max(max_count_error, count_error)
        checked += 1
        if out_error > 0.08:
            return False, diagnostic(
                "P_ANALOG_CHANNEL_MUX",
                "value_mismatch",
                expected=f"out={expected_out:.5f}",
                observed=f"out={observed_out:.5f}",
                event=label,
            )
        if count_error > 0.08:
            return False, diagnostic(
                "P_COUNTER_MONITOR_LEVEL",
                "value_mismatch",
                expected=f"count_x={count}",
                observed=f"count_x={observed_count:.5f}",
                event=label,
            )

    if checked < 6:
        return False, diagnostic(
            "P_INCREMENT_BEFORE_SELECTION",
            "coverage",
            expected="at_least_6_checked_clk_rises",
            observed=f"checked={checked}",
            event="full_trace",
        )
    return True, pass_note(
        PROPERTY_IDS,
        f"checked={checked} max_out_error={max_out_error:.5f} max_count_error={max_count_error:.5f}",
    )


CHECKER_ID = "v4_167_ideal_clkmux_8channel"
CHECKER: Checker = bind_properties(check_v3_ideal_clkmux_8channel, PROPERTY_IDS)
