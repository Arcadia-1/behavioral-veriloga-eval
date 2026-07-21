"""Stimulus-relative checker for canonical v4 DUT 159."""
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
    require_signals,
    sample,
)


PROPERTY_IDS = (
    "P_CLOCKED_FIFTEEN_TAP_COUNT",
    "P_FULL_TAP_COVERAGE",
    "P_FRACTION_NORMALIZATION_AND_GAIN",
)
TAPS = tuple(f"dt{index}" for index in range(15))
SIGNALS = {"time", "clks", "dout"} | set(TAPS)


def _count(rows: list[Row], event_t: float, threshold: float) -> int | None:
    bits = [logic_at(rows, signal, event_t, threshold=threshold) for signal in TAPS]
    if any(bit is None for bit in bits):
        return None
    return sum(bit for bit in bits if bit is not None)


def check_v3_ref_flash_15level_decoder(rows: list[Row]) -> tuple[bool, str]:
    missing = require_signals(rows, SIGNALS, "P_CLOCKED_FIFTEEN_TAP_COUNT")
    if missing:
        return False, missing

    clk_threshold = logic_threshold(rows, ("clks",), default_high=0.9)
    tap_threshold = logic_threshold(rows, TAPS, default_high=0.9)
    clk_edges = crossings(rows, "clks", threshold=clk_threshold, direction="rising")
    if len(clk_edges) < 4:
        return False, diagnostic(
            "P_CLOCKED_FIFTEEN_TAP_COUNT",
            "coverage",
            expected="at_least_4_clk_rises",
            observed=f"clk_rises={len(clk_edges)}",
            event="full_trace",
        )

    tap_edges = sorted(
        edge_t
        for signal in TAPS
        for edge_t in all_crossings(rows, signal, threshold=tap_threshold)
    )
    checked = 0
    hold_checked = 0
    max_error = 0.0
    for index, edge_t in enumerate(clk_edges):
        next_edge = clk_edges[index + 1] if index + 1 < len(clk_edges) else rows[-1]["time"]
        expected_count = _count(rows, edge_t, tap_threshold)
        label = event_label("clks_rise", index, edge_t)
        if expected_count is None:
            return False, diagnostic(
                "P_CLOCKED_FIFTEEN_TAP_COUNT",
                "invalid_trace",
                expected="sampled_tap_inputs",
                observed="missing_sample",
                event=label,
            )
        expected = expected_count / 15.0
        value_probe = min(edge_t + 1.8e-9, edge_t + 0.25 * (next_edge - edge_t))
        if value_probe <= edge_t or value_probe > rows[-1]["time"]:
            continue
        observed = sample(rows, "dout", value_probe)
        if observed is None:
            return False, diagnostic(
                "P_FRACTION_NORMALIZATION_AND_GAIN",
                "invalid_trace",
                expected="dout_sample",
                observed="missing_sample",
                event=label,
            )
        error = abs(observed - expected)
        max_error = max(max_error, error)
        checked += 1
        if error > 0.025:
            return False, diagnostic(
                "P_FRACTION_NORMALIZATION_AND_GAIN",
                "value_mismatch",
                expected=f"dout={expected:.5f}",
                observed=f"dout={observed:.5f}",
                event=label,
            )

        changes = [change_t for change_t in tap_edges if edge_t + 0.1e-9 < change_t < next_edge - 0.1e-9]
        if changes:
            last_change = max(changes)
            hold_probe = last_change + 0.5 * (next_edge - last_change)
            held = sample(rows, "dout", hold_probe)
            if held is None:
                return False, diagnostic(
                    "P_CLOCKED_FIFTEEN_TAP_COUNT",
                    "invalid_trace",
                    expected="held_dout_sample",
                    observed="missing_sample",
                    event=label,
                )
            hold_error = abs(held - expected)
            max_error = max(max_error, hold_error)
            hold_checked += 1
            if hold_error > 0.025:
                return False, diagnostic(
                    "P_CLOCKED_FIFTEEN_TAP_COUNT",
                    "hold_mismatch",
                    expected=f"held_dout={expected:.5f}",
                    observed=f"dout={held:.5f}",
                    event=label,
                )

    if checked < 4 or hold_checked < 3:
        return False, diagnostic(
            "P_FULL_TAP_COVERAGE",
            "coverage",
            expected="4_clocked_codes_and_3_interclock_hold_checks",
            observed=f"checked={checked} hold_checked={hold_checked}",
            event="full_trace",
        )
    return True, pass_note(
        PROPERTY_IDS,
        f"checked={checked} hold_checked={hold_checked} max_error={max_error:.5f}",
    )


CHECKER_ID = "v4_159_ref_flash_15level_decoder"
CHECKER: Checker = bind_properties(check_v3_ref_flash_15level_decoder, PROPERTY_IDS)
