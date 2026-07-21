"""Stimulus-relative checker for canonical v4 DUT 153."""
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
    "P_CLOCKED_SIX_BIT_WEIGHTED_CODE",
    "P_COMPLEMENTARY_DIFFERENTIAL_OUTPUTS",
    "P_OUTPUT_SWING_SCALE",
)
DIN = tuple(f"din{bit}" for bit in range(6))
SIGNALS = {"time", "clks", "voutp", "voutn"} | set(DIN)
WEIGHTS = {f"din{bit}": 2.0 ** -(bit + 1) for bit in range(6)}
VTH = 0.75
VCM = 0.75
REFP = 0.925
REFN = 0.575
VALUE_TOL = 0.015


def _expected(rows: list[Row], event_t: float, threshold: float) -> tuple[float, float] | None:
    yp = VCM / 64.0
    yn = VCM / 64.0
    for signal, weight in WEIGHTS.items():
        bit = logic_at(rows, signal, event_t, threshold=threshold)
        if bit is None:
            return None
        yp += weight * (REFP if bit else REFN)
        yn += weight * (REFN if bit else REFP)
    return yp, yn


def check_v3_differential_dac_calc_6b(rows: list[Row]) -> tuple[bool, str]:
    missing = require_signals(rows, SIGNALS, "P_CLOCKED_SIX_BIT_WEIGHTED_CODE")
    if missing:
        return False, missing

    clk_threshold = logic_threshold(rows, ("clks",), default_high=2.0 * VTH)
    bit_threshold = logic_threshold(rows, DIN, default_high=2.0 * VTH)
    clk_edges = crossings(rows, "clks", threshold=clk_threshold, direction="rising")
    if len(clk_edges) < 4:
        return False, diagnostic(
            "P_CLOCKED_SIX_BIT_WEIGHTED_CODE",
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
    max_value_error = 0.0
    max_cm_error = 0.0
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
        yp = sample(rows, "voutp", probe_t)
        yn = sample(rows, "voutn", probe_t)
        label = event_label("clks_rise", index, edge_t)
        if expected is None or yp is None or yn is None:
            return False, diagnostic(
                "P_CLOCKED_SIX_BIT_WEIGHTED_CODE",
                "invalid_trace",
                expected="sampled_inputs_and_outputs",
                observed="missing_sample",
                event=label,
            )
        expected_yp, expected_yn = expected
        bits = tuple(
            logic_at(rows, signal, edge_t, threshold=bit_threshold) for signal in DIN
        )
        din3_only_seen = din3_only_seen or bits == (0, 0, 0, 1, 0, 0)
        value_error = max(abs(yp - expected_yp), abs(yn - expected_yn))
        cm_error = abs(0.5 * (yp + yn) - VCM)
        max_value_error = max(max_value_error, value_error)
        max_cm_error = max(max_cm_error, cm_error)
        checked += 1
        if value_error > VALUE_TOL:
            return False, diagnostic(
                "P_CLOCKED_SIX_BIT_WEIGHTED_CODE",
                "value_mismatch",
                expected=f"voutp={expected_yp:.5f},voutn={expected_yn:.5f}",
                observed=f"voutp={yp:.5f},voutn={yn:.5f}",
                event=label,
            )
        if cm_error > 0.015:
            return False, diagnostic(
                "P_COMPLEMENTARY_DIFFERENTIAL_OUTPUTS",
                "common_mode_mismatch",
                expected=f"common_mode={VCM:.5f}",
                observed=f"common_mode={0.5 * (yp + yn):.5f}",
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
            held_yp = sample(rows, "voutp", hold_probe)
            held_yn = sample(rows, "voutn", hold_probe)
            if held_yp is None or held_yn is None:
                return False, diagnostic(
                    "P_CLOCKED_SIX_BIT_WEIGHTED_CODE",
                    "invalid_trace",
                    expected="held_differential_output_sample",
                    observed="missing_sample",
                    event=label,
                )
            hold_error = max(
                abs(held_yp - expected_yp), abs(held_yn - expected_yn)
            )
            max_value_error = max(max_value_error, hold_error)
            hold_checked += 1
            if hold_error > VALUE_TOL:
                return False, diagnostic(
                    "P_CLOCKED_SIX_BIT_WEIGHTED_CODE",
                    "hold_mismatch",
                    expected=(
                        f"held_voutp={expected_yp:.5f},held_voutn={expected_yn:.5f}"
                    ),
                    observed=f"voutp={held_yp:.5f},voutn={held_yn:.5f}",
                    event=label,
                )

    if checked < 4 or hold_checked < 3 or not din3_only_seen:
        return False, diagnostic(
            "P_CLOCKED_SIX_BIT_WEIGHTED_CODE",
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
        f"checked={checked} hold_checked={hold_checked} din3_only_seen={din3_only_seen} "
        f"max_value_error={max_value_error:.5f} max_cm_error={max_cm_error:.5f}",
    )


CHECKER_ID = "v4_153_differential_dac_calc_6b"
CHECKER: Checker = bind_properties(check_v3_differential_dac_calc_6b, PROPERTY_IDS)
