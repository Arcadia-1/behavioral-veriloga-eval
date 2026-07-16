"""Task-specific checker for canonical v4 DUT 116."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import diagnostic, pass_note, require_signals


PROPERTY_IDS = (
    "P_INITIAL_INPUT",
    "P_CAPTURE_NEW_MAX",
    "P_HOLD_ON_FALL",
    "P_MONOTONE_OUTPUT",
    "P_RUNNING_MAX",
)


def check_v3_max_detector_hold(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin", "vout"}
    missing = require_signals(rows, required, "P_RUNNING_MAX")
    if missing:
        return False, missing

    running_max = rows[0]["vin"]
    stride = max(1, len(rows) // 240)
    checked = 0
    max_err = 0.0
    input_dropped_after_peak = False
    previous_vout = rows[0]["vout"]
    monotone_ok = True
    for idx, row in enumerate(rows):
        running_max = max(running_max, row["vin"])
        if row["vin"] < running_max - 0.05:
            input_dropped_after_peak = True
        if row["vout"] < previous_vout - 0.01:
            monotone_ok = False
        previous_vout = row["vout"]
        if idx % stride == 0:
            max_err = max(max_err, abs(row["vout"] - running_max))
            checked += 1
    if checked < 20:
        return False, diagnostic(
            "P_RUNNING_MAX",
            "insufficient_checks",
            expected="checked>=20",
            observed=f"checked={checked}",
            event="trace_observation_set",
        )
    if not monotone_ok:
        return False, diagnostic(
            "P_MONOTONE_OUTPUT",
            "monotonicity_mismatch",
            expected="vout_monotone_non_decreasing",
            observed="vout_drop_detected",
            event="trace_observation_set",
        )
    if not input_dropped_after_peak:
        return False, diagnostic(
            "P_HOLD_ON_FALL",
            "insufficient_stimulus_coverage",
            expected="vin_falls_below_previous_max",
            observed="hold_window_missing",
            event="trace_observation_set",
        )
    detail = f"checked={checked} max_error={max_err:.5f} monotonic_hold=True"
    if max_err > 0.03:
        return False, diagnostic(
            "P_RUNNING_MAX",
            "running_max_mismatch",
            expected="max_error<=0.03000",
            observed=detail,
            event="trace_observation_set",
        )
    return True, pass_note(PROPERTY_IDS, detail)

CHECKER_ID = "v4_116_max_detector_hold"
CHECKER: Checker = check_v3_max_detector_hold
