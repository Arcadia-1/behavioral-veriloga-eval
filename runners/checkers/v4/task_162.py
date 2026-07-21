"""Stimulus-relative checker for canonical v4 DUT 162."""
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
    "P_THERMOMETER_COUNT",
    "P_FOUR_STAGE_ALIGNMENT",
    "P_BINARY_OUTPUT_ORDER",
    "P_EVENT_HELD_OUTPUTS",
)
DIN = tuple(f"din{bit}" for bit in range(8))
DOUT = tuple(f"dout{bit}" for bit in range(4))
SIGNALS = {"time", "clk"} | set(DIN) | set(DOUT)


def _thermometer_count(rows: list[Row], event_t: float, threshold: float) -> int | None:
    count = 0
    for signal in DIN:
        bit = logic_at(rows, signal, event_t, threshold=threshold)
        if bit is None:
            return None
        count += bit
    return count


def check_v3_flash_data_align_pipeline(rows: list[Row]) -> tuple[bool, str]:
    missing = require_signals(rows, SIGNALS, "P_THERMOMETER_COUNT")
    if missing:
        return False, missing

    clk_threshold = logic_threshold(rows, ("clk",), default_high=0.9)
    din_threshold = logic_threshold(rows, DIN, default_high=0.9)
    clk_edges = crossings(rows, "clk", threshold=clk_threshold, direction="rising")
    if len(clk_edges) < 9:
        return False, diagnostic(
            "P_FOUR_STAGE_ALIGNMENT",
            "coverage",
            expected="at_least_9_clk_rises",
            observed=f"clk_rises={len(clk_edges)}",
            event="full_trace",
        )

    counts: list[int] = []
    for index, edge_t in enumerate(clk_edges):
        count = _thermometer_count(rows, edge_t, din_threshold)
        if count is None:
            return False, diagnostic(
                "P_THERMOMETER_COUNT",
                "invalid_trace",
                expected="sampled_din_bits",
                observed="missing_sample",
                event=event_label("clk_rise", index, edge_t),
            )
        counts.append(count)

    checked = 0
    max_error = 0.0
    upper_patterns_observed: set[tuple[int, int, int]] = set()
    for index, edge_t in enumerate(clk_edges[4:], start=4):
        next_edge = clk_edges[index + 1] if index + 1 < len(clk_edges) else None
        probe_t = probe_time(rows, edge_t, next_edge, fraction=0.25)
        if probe_t is None:
            continue
        expected_code = counts[index - 4]
        sampled_input_t = clk_edges[index - 4]
        upper_values = tuple(
            logic_at(rows, signal, sampled_input_t, threshold=din_threshold)
            for signal in DIN[5:]
        )
        if any(bit is None for bit in upper_values):
            return False, diagnostic(
                "P_THERMOMETER_COUNT",
                "invalid_trace",
                expected="sampled_din5_din6_din7",
                observed="missing_sample",
                event=event_label("clk_rise", index - 4, sampled_input_t),
            )
        upper_patterns_observed.add(tuple(int(bit) for bit in upper_values))
        label = event_label("clk_rise", index, edge_t)
        for bit, signal in enumerate(DOUT):
            observed = sample(rows, signal, probe_t)
            if observed is None:
                return False, diagnostic(
                    "P_BINARY_OUTPUT_ORDER",
                    "invalid_trace",
                    expected=f"{signal}_sample",
                    observed="missing_sample",
                    event=label,
                )
            expected = 1.0 if (expected_code >> bit) & 1 else 0.0
            error = abs(observed - expected)
            max_error = max(max_error, error)
            if error > 0.12:
                return False, diagnostic(
                    "P_BINARY_OUTPUT_ORDER",
                    "value_mismatch",
                    expected=f"{signal}={expected:.1f}",
                    observed=f"{signal}={observed:.4f}",
                    event=label,
                )
        interval_stop = rows[-1]["time"] if next_edge is None else next_edge
        margin = 0.02 * (interval_stop - edge_t)
        hold_rows = [
            row for row in rows
            if edge_t + margin <= row["time"] <= interval_stop - margin
        ]
        for row in hold_rows:
            for bit, signal in enumerate(DOUT):
                expected = 1.0 if (expected_code >> bit) & 1 else 0.0
                observed = row[signal]
                error = abs(observed - expected)
                max_error = max(max_error, error)
                if error > 0.12:
                    return False, diagnostic(
                        "P_EVENT_HELD_OUTPUTS",
                        "hold_mismatch",
                        expected=f"{signal}={expected:.1f}_through_interval",
                        observed=f"{signal}={observed:.4f}",
                        event=f"{label}@{row['time']:.6e}s",
                    )
        checked += 1

    if checked < 5:
        return False, diagnostic(
            "P_FOUR_STAGE_ALIGNMENT",
            "coverage",
            expected="at_least_5_delayed_outputs",
            observed=f"checked={checked}",
            event="full_trace",
        )
    required_upper_patterns = {(1, 0, 0), (0, 1, 0), (0, 0, 1)}
    if not required_upper_patterns.issubset(upper_patterns_observed):
        return False, diagnostic(
            "P_THERMOMETER_COUNT",
            "coverage",
            expected="independent_one_hot_din5_din6_din7_checked_delayed_samples",
            observed=f"patterns={sorted(upper_patterns_observed)}",
            event="checked_input_samples",
        )
    return True, pass_note(PROPERTY_IDS, f"checked={checked} max_error={max_error:.5f}")


CHECKER_ID = "v4_162_flash_data_align_pipeline"
CHECKER: Checker = bind_properties(check_v3_flash_data_align_pipeline, PROPERTY_IDS)
