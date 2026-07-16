"""Task-specific checker for canonical v4 DUT 120."""
from __future__ import annotations

from collections.abc import Callable

from ..api import Checker
from .stimulus_relative import diagnostic, pass_note, require_signals


PROPERTY_IDS = (
    "P_DB_AMPLITUDE_RATIO",
    "P_POLARITY_PRESERVATION",
    "P_MONOTONIC_ATTENUATION",
    "P_CONTINUOUS_RESPONSE",
)


def _check_affine_transfer_coverage(
    rows: list[dict[str, float]],
    *,
    required: set[str],
    output: str,
    expected_fn: Callable[[dict[str, float]], float],
    drive_fn: Callable[[dict[str, float]], float],
    label: str,
    tolerance: float,
    min_span: float,
) -> tuple[bool, str]:
    missing = require_signals(rows, required, "P_DB_AMPLITUDE_RATIO")
    if missing:
        return False, missing

    checked = 0
    max_err = 0.0
    worst: tuple[float, float, float] | None = None
    first_drive = drive_fn(rows[0])
    drive_min = drive_max = previous_drive = first_drive
    saw_rise = saw_fall = False
    for row in rows:
        drive = drive_fn(row)
        expected = expected_fn(row)
        error = abs(row[output] - expected)
        if error >= max_err:
            max_err = error
            worst = (row["time"], row[output], expected)
        saw_rise = saw_rise or drive - previous_drive > 1e-5
        saw_fall = saw_fall or drive - previous_drive < -1e-5
        drive_min = min(drive_min, drive)
        drive_max = max(drive_max, drive)
        previous_drive = drive
        checked += 1
    if checked < 20:
        return False, diagnostic(
            "P_CONTINUOUS_RESPONSE",
            "insufficient_checks",
            expected="checked>=20",
            observed=f"checked={checked}",
            event=f"{label}_trace",
        )
    if drive_max - drive_min < min_span or not (saw_rise and saw_fall):
        return False, diagnostic(
            "P_MONOTONIC_ATTENUATION",
            "insufficient_drive_coverage",
            expected=f"span>={min_span:.3f},rise=True,fall=True",
            observed=f"span={drive_max - drive_min:.3f},rise={saw_rise},fall={saw_fall}",
            event=f"{label}_trace",
        )
    if max_err > tolerance:
        assert worst is not None
        _time_s, observed, expected = worst
        return False, diagnostic(
            "P_DB_AMPLITUDE_RATIO",
            "attenuation_mismatch",
            expected=f"{output}={expected:.4f}",
            observed=f"{output}={observed:.4f},max_err={max_err:.4f}",
            event=f"{label}_worst_observed_sample",
        )
    detail = f"checked={checked} range={drive_min:.3f}:{drive_max:.3f} rise={saw_rise} fall={saw_fall} max_err={max_err:.4f}"
    return True, pass_note(PROPERTY_IDS, detail)

def check_v3_attenuator_gain(rows: list[dict[str, float]]) -> tuple[bool, str]:
    return _check_affine_transfer_coverage(
        rows,
        required={"time", "vin", "vout"},
        output="vout",
        expected_fn=lambda row: 0.5 * row["vin"],
        drive_fn=lambda row: row["vin"],
        label="attenuator_gain",
        tolerance=0.015,
        min_span=0.35,
    )

CHECKER_ID = "v4_120_attenuator_gain"
CHECKER: Checker = check_v3_attenuator_gain
