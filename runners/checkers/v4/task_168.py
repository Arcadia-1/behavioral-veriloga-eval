"""Stimulus-relative checker for canonical v4 DUT 168."""
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
    "P_THRESHOLDED_4BIT_CODE",
    "P_OFFSET_PLUS_SCALED_TRIM",
    "P_EVENT_UPDATED_OUTPUT",
)
DIN = ("din0", "din1", "din2", "din3")
SIGNALS = {"time", "dout"} | set(DIN)


def _code(rows: list[Row], time_s: float, threshold: float) -> int | None:
    bits: list[int] = []
    for signal in ("din3", "din2", "din1", "din0"):
        bit = logic_at(rows, signal, time_s, threshold=threshold)
        if bit is None:
            return None
        bits.append(bit)
    return 8 * bits[0] + 4 * bits[1] + 2 * bits[2] + bits[3]


def check_v3_dac_ideal_4b_offset(rows: list[Row]) -> tuple[bool, str]:
    missing = require_signals(rows, SIGNALS, "P_THRESHOLDED_4BIT_CODE")
    if missing:
        return False, missing

    threshold = logic_threshold(rows, DIN, default_high=1.0)
    probes = stable_probe_times(rows, DIN, threshold=threshold)
    if len(probes) < 4:
        return False, diagnostic(
            "P_EVENT_UPDATED_OUTPUT",
            "coverage",
            expected="at_least_4_stable_code_windows",
            observed=f"windows={len(probes)}",
            event="full_trace",
        )

    scaling = 32.0 * 10.0 / 9.0
    codes: list[int] = []
    max_error = 0.0
    for index, probe_t in enumerate(probes):
        code = _code(rows, probe_t, threshold)
        observed = sample(rows, "dout", probe_t)
        event = f"stable_window[{index}]@{probe_t:.6e}s"
        if code is None or observed is None:
            return False, diagnostic(
                "P_THRESHOLDED_4BIT_CODE",
                "invalid_trace",
                expected="sampled_code_and_dout",
                observed="missing_sample",
                event=event,
            )
        expected = 0.239 + code / scaling
        error = abs(observed - expected)
        max_error = max(max_error, error)
        codes.append(code)
        if error > 0.025:
            return False, diagnostic(
                "P_OFFSET_PLUS_SCALED_TRIM",
                "value_mismatch",
                expected=f"dout={expected:.5f}",
                observed=f"dout={observed:.5f}",
                event=event,
            )
    if len(set(codes)) < 4 or max(codes) < 14:
        return False, diagnostic(
            "P_EVENT_UPDATED_OUTPUT",
            "coverage",
            expected="four_distinct_codes_including_full_scale",
            observed=f"codes={codes}",
            event="full_trace",
        )
    return True, pass_note(PROPERTY_IDS, f"codes={codes} max_error={max_error:.5f}")


CHECKER_ID = "v4_168_dac_ideal_4b_offset"
CHECKER: Checker = bind_properties(check_v3_dac_ideal_4b_offset, PROPERTY_IDS)
