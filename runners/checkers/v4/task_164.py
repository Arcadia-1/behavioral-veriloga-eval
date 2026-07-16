"""Stimulus-relative checker for canonical v4 DUT 164."""
from __future__ import annotations

from ..api import Checker, Row
from .batch17_stimulus_relative import (
    bind_properties,
    diagnostic,
    logic_at,
    logic_threshold,
    pass_note,
    require_signals,
    sample,
    stable_probe_times,
)


PROPERTY_IDS = (
    "P_THRESHOLD_CODE_DETECTION",
    "P_WEIGHTED_GROUP_SUM",
    "P_SCALED_SCALAR_OUTPUT",
)
DIN = tuple(f"din{bit}" for bit in range(7))
SIGNALS = {"time", "dout"} | set(DIN)
WEIGHTS = {
    "din6": 16.0 / 32.0,
    "din5": 8.0 / 32.0,
    "din4": 4.0 / 32.0,
    "din3": 2.0 / 32.0,
    "din2": 1.0 / 32.0,
    "din1": 0.5 / 32.0,
    "din0": 0.25 / 32.0,
}


def _expected(rows: list[Row], time_s: float, threshold: float) -> float | None:
    total = 0.0
    for signal, weight in WEIGHTS.items():
        bit = logic_at(rows, signal, time_s, threshold=threshold)
        if bit is None:
            return None
        total += weight * bit
    return total


def check_v3_ideal_adc_out_7bits(rows: list[Row]) -> tuple[bool, str]:
    missing = require_signals(rows, SIGNALS, "P_THRESHOLD_CODE_DETECTION")
    if missing:
        return False, missing

    threshold = logic_threshold(rows, DIN, default_high=0.9)
    probes = stable_probe_times(rows, DIN, threshold=threshold)
    if len(probes) < 3:
        return False, diagnostic(
            "P_THRESHOLD_CODE_DETECTION",
            "coverage",
            expected="at_least_3_stable_input_windows",
            observed=f"windows={len(probes)}",
            event="full_trace",
        )

    max_error = 0.0
    expected_values: list[float] = []
    for index, probe_t in enumerate(probes):
        expected = _expected(rows, probe_t, threshold)
        observed = sample(rows, "dout", probe_t)
        event = f"stable_window[{index}]@{probe_t:.6e}s"
        if expected is None or observed is None:
            return False, diagnostic(
                "P_SCALED_SCALAR_OUTPUT",
                "invalid_trace",
                expected="sampled_inputs_and_dout",
                observed="missing_sample",
                event=event,
            )
        expected_values.append(round(expected, 6))
        error = abs(observed - expected)
        max_error = max(max_error, error)
        if error > 0.02:
            return False, diagnostic(
                "P_SCALED_SCALAR_OUTPUT",
                "value_mismatch",
                expected=f"dout={expected:.5f}",
                observed=f"dout={observed:.5f}",
                event=event,
            )
    if len(set(expected_values)) < 3:
        return False, diagnostic(
            "P_WEIGHTED_GROUP_SUM",
            "coverage",
            expected="at_least_3_distinct_codes",
            observed=f"codes={expected_values}",
            event="full_trace",
        )
    return True, pass_note(PROPERTY_IDS, f"checked={len(probes)} max_error={max_error:.5f}")


CHECKER_ID = "v4_164_ideal_adc_out_7bits"
CHECKER: Checker = bind_properties(check_v3_ideal_adc_out_7bits, PROPERTY_IDS)
