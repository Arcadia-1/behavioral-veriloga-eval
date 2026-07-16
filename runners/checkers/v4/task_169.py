"""Stimulus-relative checker for canonical v4 DUT 169."""
from __future__ import annotations

from ..api import Checker, Row
from .batch17_stimulus_relative import (
    bind_properties,
    diagnostic,
    logic_threshold,
    pass_note,
    require_signals,
    sample,
    stable_probe_times,
)


PROPERTY_IDS = (
    "P_DIFFERENTIAL_INPUT_POLARITY",
    "P_KPHI_GAIN_SCALE",
    "P_CONTINUOUS_ANALOG_TRACKING",
)
SIGNALS = {"time", "in1", "in2", "out"}


def check_v3_linear_pfd_gain(rows: list[Row]) -> tuple[bool, str]:
    missing = require_signals(rows, SIGNALS, "P_DIFFERENTIAL_INPUT_POLARITY")
    if missing:
        return False, missing

    threshold = logic_threshold(rows, ("in1", "in2"), default_high=1.0)
    probes = stable_probe_times(rows, ("in1", "in2"), threshold=threshold)
    if len(probes) < 3:
        return False, diagnostic(
            "P_CONTINUOUS_ANALOG_TRACKING",
            "coverage",
            expected="at_least_3_stable_input_windows",
            observed=f"windows={len(probes)}",
            event="full_trace",
        )

    max_error = 0.0
    polarities: set[int] = set()
    for index, probe_t in enumerate(probes):
        in1 = sample(rows, "in1", probe_t)
        in2 = sample(rows, "in2", probe_t)
        observed = sample(rows, "out", probe_t)
        event = f"stable_window[{index}]@{probe_t:.6e}s"
        if in1 is None or in2 is None or observed is None:
            return False, diagnostic(
                "P_CONTINUOUS_ANALOG_TRACKING",
                "invalid_trace",
                expected="in1_in2_out_samples",
                observed="missing_sample",
                event=event,
            )
        expected = 2.03 * (in1 - in2)
        polarities.add(1 if expected > 0.0 else -1 if expected < 0.0 else 0)
        error = abs(observed - expected)
        max_error = max(max_error, error)
        if error > 0.02:
            return False, diagnostic(
                "P_KPHI_GAIN_SCALE",
                "value_mismatch",
                expected=f"out={expected:.5f}",
                observed=f"out={observed:.5f}",
                event=event,
            )
    if not ({-1, 1} <= polarities):
        return False, diagnostic(
            "P_DIFFERENTIAL_INPUT_POLARITY",
            "coverage",
            expected="positive_and_negative_differential_windows",
            observed=f"polarities={sorted(polarities)}",
            event="full_trace",
        )
    return True, pass_note(PROPERTY_IDS, f"checked={len(probes)} max_error={max_error:.5f}")


CHECKER_ID = "v4_169_linear_pfd_gain"
CHECKER: Checker = bind_properties(check_v3_linear_pfd_gain, PROPERTY_IDS)
