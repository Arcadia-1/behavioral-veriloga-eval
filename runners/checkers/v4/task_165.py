"""Stimulus-relative checker for canonical v4 DUT 165."""
from __future__ import annotations

from ..api import Checker, Row
from .batch17_stimulus_relative import (
    bind_properties,
    crossings,
    diagnostic,
    event_label,
    logic_at,
    logic_threshold,
    max_signal_value,
    pass_note,
    probe_time,
    require_signals,
    sample,
)


PROPERTY_IDS = (
    "P_READY_CLOCKED_SAMPLING",
    "P_BINARY_BIT_ORDER",
    "P_VDD_SCALED_DAC_OUTPUT",
)
DIN = ("din1", "din2", "din3", "din4")
SIGNALS = {"time", "rdy", "aout"} | set(DIN)
WEIGHTS = {
    "din4": 0.5,
    "din3": 0.25,
    "din2": 0.125,
    "din1": 0.0625,
}


def _expected(rows: list[Row], event_t: float, threshold: float, vdd: float) -> float | None:
    code = 0.0
    for signal, weight in WEIGHTS.items():
        bit = logic_at(rows, signal, event_t, threshold=threshold)
        if bit is None:
            return None
        code += weight * bit
    return vdd * code


def check_v3_va_lx_dac_ideal_4b(rows: list[Row]) -> tuple[bool, str]:
    missing = require_signals(rows, SIGNALS, "P_READY_CLOCKED_SAMPLING")
    if missing:
        return False, missing

    rdy_threshold = logic_threshold(rows, ("rdy",), default_high=1.8)
    din_threshold = logic_threshold(rows, DIN, default_high=1.8)
    vdd = max_signal_value(rows, DIN, default=1.8)
    rdy_edges = crossings(rows, "rdy", threshold=rdy_threshold, direction="rising")
    if len(rdy_edges) < 3:
        return False, diagnostic(
            "P_READY_CLOCKED_SAMPLING",
            "coverage",
            expected="at_least_3_rdy_rises",
            observed=f"rdy_rises={len(rdy_edges)}",
            event="full_trace",
        )

    checked = 0
    max_error = 0.0
    for index, edge_t in enumerate(rdy_edges):
        next_edge = rdy_edges[index + 1] if index + 1 < len(rdy_edges) else None
        probe_t = probe_time(rows, edge_t, next_edge, fraction=0.25)
        if probe_t is None:
            continue
        expected = _expected(rows, edge_t, din_threshold, vdd)
        observed = sample(rows, "aout", probe_t)
        label = event_label("rdy_rise", index, edge_t)
        if expected is None or observed is None:
            return False, diagnostic(
                "P_VDD_SCALED_DAC_OUTPUT",
                "invalid_trace",
                expected="sampled_inputs_and_aout",
                observed="missing_sample",
                event=label,
            )
        error = abs(observed - expected)
        max_error = max(max_error, error)
        checked += 1
        if error > 0.03:
            return False, diagnostic(
                "P_VDD_SCALED_DAC_OUTPUT",
                "value_mismatch",
                expected=f"aout={expected:.5f}",
                observed=f"aout={observed:.5f}",
                event=label,
            )

    if checked < 3:
        return False, diagnostic(
            "P_READY_CLOCKED_SAMPLING",
            "coverage",
            expected="at_least_3_checked_rdy_rises",
            observed=f"checked={checked}",
            event="full_trace",
        )
    return True, pass_note(PROPERTY_IDS, f"checked={checked} max_error={max_error:.5f}")


CHECKER_ID = "v4_165_va_lx_dac_ideal_4b"
CHECKER: Checker = bind_properties(check_v3_va_lx_dac_ideal_4b, PROPERTY_IDS)
