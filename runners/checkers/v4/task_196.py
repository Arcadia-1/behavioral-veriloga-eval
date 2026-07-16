"""Task-specific checker for canonical v4 DUT 196."""
from __future__ import annotations

from ..api import Checker, Row
from .trace_utils import property_diagnostics

PROPERTIES = {
    "P_POSITIVE_LO_GAIN_PATH": 0,
    "P_NEGATIVE_LO_CHOP_PATH": 0,
    "P_CONTINUOUS_TRACKING": 0,
}


def check_v3_phase_detector_chopper(rows: list[Row]) -> tuple[bool, str]:
    required = {"time", "vlocal_osc", "vin_rf", "vif"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing phase detector chopper signals"

    counts = dict(PROPERTIES)
    checked = 0
    positive_samples = 0
    negative_samples = 0
    max_err = 0.0
    gain = 1.25
    tol = 0.025

    for row in rows:
        lo = row["vlocal_osc"]
        if abs(lo) < 0.05:
            continue
        expected = gain * row["vin_rf"] if lo > 0.0 else -gain * row["vin_rf"]
        err = abs(row["vif"] - expected)
        max_err = max(max_err, err)
        checked += 1
        if lo > 0.0:
            positive_samples += 1
            if err > tol:
                counts["P_POSITIVE_LO_GAIN_PATH"] += 1
        else:
            negative_samples += 1
            if err > tol:
                counts["P_NEGATIVE_LO_CHOP_PATH"] += 1
        if err > tol:
            counts["P_CONTINUOUS_TRACKING"] += 1

    if positive_samples < 5 or negative_samples < 5:
        return (
            False,
            "insufficient_excitation phase_detector_chopper "
            f"positive_samples={positive_samples} negative_samples={negative_samples}",
        )

    ok = all(count == 0 for count in counts.values())
    return (
        ok,
        f"{property_diagnostics(counts)}; checked={checked}; "
        f"positive_samples={positive_samples}; negative_samples={negative_samples}; "
        f"max_err={max_err:.6g}",
    )


CHECKER_ID = "v4_196_phase_detector_chopper"
CHECKER: Checker = check_v3_phase_detector_chopper
