"""Stimulus-relative checker for canonical v4 DUT 156."""
from __future__ import annotations

from ..api import Checker, Row
from .batch17_stimulus_relative import (
    all_crossings,
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
    "P_CLOCKED_SEVEN_BIT_WEIGHTED_SUM",
    "P_MSB_AND_TERMINATION_CONTRIBUTIONS",
    "P_REFERENCE_ENDPOINTS_AND_SCALE",
)
DIN = tuple(f"din{bit}" for bit in range(7))
SIGNALS = {"time", "clks", "vout"} | set(DIN)
WEIGHTS = {f"din{bit}": 2.0 ** -(bit + 1) for bit in range(7)}
VTH = 0.75
REFP = 5.0
REFN = 1.0


def _expected(rows: list[Row], event_t: float, threshold: float) -> float | None:
    total = REFN / 128.0
    for signal, weight in WEIGHTS.items():
        bit = logic_at(rows, signal, event_t, threshold=threshold)
        if bit is None:
            return None
        total += weight * (REFP if bit else REFN)
    return total


def check_v3_dac_5v_weighted_7b(rows: list[Row]) -> tuple[bool, str]:
    missing = require_signals(rows, SIGNALS, "P_CLOCKED_SEVEN_BIT_WEIGHTED_SUM")
    if missing:
        return False, missing

    clk_threshold = logic_threshold(rows, ("clks",), default_high=0.9)
    bit_threshold = logic_threshold(rows, DIN, default_high=0.9)
    clk_edges = crossings(rows, "clks", threshold=clk_threshold, direction="rising")
    if len(clk_edges) < 4:
        return False, diagnostic(
            "P_CLOCKED_SEVEN_BIT_WEIGHTED_SUM",
            "coverage",
            expected="at_least_4_clk_rises",
            observed=f"clk_rises={len(clk_edges)}",
            event="full_trace",
        )

    input_edges = sorted(
        edge_t
        for signal in DIN
        for edge_t in all_crossings(rows, signal, threshold=bit_threshold)
    )
    max_error = 0.0
    checked = 0
    hold_checked = 0
    din3_only_seen = False
    for index, edge_t in enumerate(clk_edges):
        next_edge = (
            clk_edges[index + 1] if index + 1 < len(clk_edges) else rows[-1]["time"]
        )
        probe_t = probe_time(
            rows, edge_t, next_edge, fraction=0.25, minimum_delay_s=1.2e-9
        )
        if probe_t is None:
            continue
        expected = _expected(rows, edge_t, bit_threshold)
        observed = sample(rows, "vout", probe_t)
        label = event_label("clks_rise", index, edge_t)
        if expected is None or observed is None:
            return False, diagnostic(
                "P_CLOCKED_SEVEN_BIT_WEIGHTED_SUM",
                "invalid_trace",
                expected="sampled_inputs_and_vout",
                observed="missing_sample",
                event=label,
            )
        error = abs(observed - expected)
        bits = tuple(
            logic_at(rows, signal, edge_t, threshold=bit_threshold) for signal in DIN
        )
        din3_only_seen = din3_only_seen or bits == (0, 0, 0, 1, 0, 0, 0)
        max_error = max(max_error, error)
        checked += 1
        if error > 0.04:
            return False, diagnostic(
                "P_CLOCKED_SEVEN_BIT_WEIGHTED_SUM",
                "value_mismatch",
                expected=f"vout={expected:.5f}",
                observed=f"vout={observed:.5f}",
                event=label,
            )

        changes = [
            change_t
            for change_t in input_edges
            if edge_t + 0.1e-9 < change_t < next_edge - 0.1e-9
        ]
        if changes:
            last_change = max(changes)
            hold_probe = last_change + 0.75 * (next_edge - last_change)
            held = sample(rows, "vout", hold_probe)
            if held is None:
                return False, diagnostic(
                    "P_CLOCKED_SEVEN_BIT_WEIGHTED_SUM",
                    "invalid_trace",
                    expected="held_vout_sample",
                    observed="missing_sample",
                    event=label,
                )
            hold_error = abs(held - expected)
            max_error = max(max_error, hold_error)
            hold_checked += 1
            if hold_error > 0.04:
                return False, diagnostic(
                    "P_CLOCKED_SEVEN_BIT_WEIGHTED_SUM",
                    "hold_mismatch",
                    expected=f"held_vout={expected:.5f}",
                    observed=f"vout={held:.5f}",
                    event=label,
                )

    if checked < 4 or hold_checked < 3 or not din3_only_seen:
        return False, diagnostic(
            "P_CLOCKED_SEVEN_BIT_WEIGHTED_SUM",
            "coverage",
            expected="4_clocked_codes_3_interclock_hold_checks_and_din3_only_code",
            observed=(
                f"checked={checked} hold_checked={hold_checked} "
                f"din3_only_seen={din3_only_seen}"
            ),
            event="full_trace",
        )
    return True, pass_note(
        PROPERTY_IDS,
        f"checked={checked} hold_checked={hold_checked} "
        f"din3_only_seen={din3_only_seen} max_error={max_error:.5f}",
    )


CHECKER_ID = "v4_156_dac_5v_weighted_7b"
CHECKER: Checker = bind_properties(check_v3_dac_5v_weighted_7b, PROPERTY_IDS)
