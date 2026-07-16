"""Stimulus-relative checker for canonical v4 DUT 161."""
from __future__ import annotations

from ..api import Checker, Row
from .batch17_stimulus_relative import (
    bind_properties,
    crossings,
    diagnostic,
    event_label,
    logic_at,
    logic_threshold,
    pass_note,
    probe_time,
    require_signals,
    sample,
)


PROPERTY_IDS = (
    "P_CLOCKED_CODE_SAMPLING",
    "P_WEIGHTED_REDUNDANT_CODE",
    "P_OFFSET_MIDRISE_OUTPUT",
    "P_OUTPUT_SMOOTH_HOLD",
)
SIGNALS = {"time", "clk", "vout"} | {f"D{bit}" for bit in range(11)}
BIT_WEIGHTS = {
    "D10": 512,
    "D9": 256,
    "D8": 128,
    "D7": 64,
    "D6": 64,
    "D5": 32,
    "D4": 16,
    "D3": 8,
    "D2": 4,
    "D1": 2,
    "D0": 1,
}


def _expected_vout(rows: list[Row], event_t: float, threshold: float) -> float | None:
    code = -32
    for signal, weight in BIT_WEIGHTS.items():
        bit = logic_at(rows, signal, event_t, threshold=threshold)
        if bit is None:
            return None
        code += weight * bit
    return (code + 0.5) * (1.8 / 1024.0) - 0.9


def check_v3_dac_restore_10bit_offset(rows: list[Row]) -> tuple[bool, str]:
    property_id = "P_OFFSET_MIDRISE_OUTPUT"
    missing = require_signals(rows, SIGNALS, property_id)
    if missing:
        return False, missing

    clk_threshold = logic_threshold(rows, ("clk",), default_high=0.9)
    bit_threshold = logic_threshold(rows, BIT_WEIGHTS, default_high=0.9)
    clk_edges = crossings(rows, "clk", threshold=clk_threshold, direction="rising")
    if len(clk_edges) < 3:
        return False, diagnostic(
            "P_CLOCKED_CODE_SAMPLING",
            "coverage",
            expected="at_least_3_clk_rises",
            observed=f"clk_rises={len(clk_edges)}",
            event="full_trace",
        )

    max_error = 0.0
    checked = 0
    for index, edge_t in enumerate(clk_edges):
        next_edge = clk_edges[index + 1] if index + 1 < len(clk_edges) else None
        probe_t = probe_time(rows, edge_t, next_edge, fraction=0.25)
        if probe_t is None:
            continue
        expected = _expected_vout(rows, edge_t, bit_threshold)
        observed = sample(rows, "vout", probe_t)
        label = event_label("clk_rise", index, edge_t)
        if expected is None or observed is None:
            return False, diagnostic(
                property_id,
                "invalid_trace",
                expected="sampled_inputs_and_vout",
                observed="missing_sample",
                event=label,
            )
        error = abs(observed - expected)
        max_error = max(max_error, error)
        checked += 1
        if error > 0.025:
            return False, diagnostic(
                property_id,
                "value_mismatch",
                expected=f"vout={expected:.5f}",
                observed=f"vout={observed:.5f}",
                event=label,
            )

    if checked < 3:
        return False, diagnostic(
            property_id,
            "coverage",
            expected="at_least_3_checked_clk_rises",
            observed=f"checked={checked}",
            event="full_trace",
        )
    return True, pass_note(PROPERTY_IDS, f"checked={checked} max_error={max_error:.5f}")


CHECKER_ID = "v4_161_dac_restore_10bit_offset"
CHECKER: Checker = bind_properties(check_v3_dac_restore_10bit_offset, PROPERTY_IDS)
