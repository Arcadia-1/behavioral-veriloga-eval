"""Task-specific checker for canonical v4 DUT 050."""
from __future__ import annotations

import math

from ..api import Checker
from .stimulus_relative import (
    diagnostic,
    pass_note,
    require_signals,
    stimulus_change_intervals,
    time_outside_intervals,
)


PROPERTY_IDS = (
    "P_DC_INPUT_CLAMP",
    "P_3BIT_QUANTIZATION",
    "P_MONOTONIC_CODE_COVERAGE",
)


def _expected_code(vin: float) -> int:
    clipped = min(1.0, max(0.0, vin))
    code = int(math.floor(8.0 * clipped))
    return max(0, min(7, code))


def _is_stable_quantization_point(vin: float) -> bool:
    clipped = min(1.0, max(0.0, vin))
    for boundary in (step / 8.0 for step in range(1, 8)):
        if abs(clipped - boundary) < 0.01:
            return False
    return True


def _observed_code(row: dict[str, float]) -> int:
    return (
        (4 if row["d2"] > 0.45 else 0)
        + (2 if row["d1"] > 0.45 else 0)
        + (1 if row["d0"] > 0.45 else 0)
    )


def _representative_rows(rows: list[dict[str, float]]) -> list[dict[str, float]]:
    # Partition by semantic input-code regions rather than requiring repeated
    # raw vin rows.  Spectre may emit only a handful of points on a DC ramp,
    # while EVAS publishes many rows for the same eight quantization regions.
    ordered = sorted(rows, key=lambda item: item["time"])
    change_intervals = stimulus_change_intervals(ordered, ("vin",))
    stable = [
        row
        for row in ordered
        if _is_stable_quantization_point(row["vin"])
        and time_outside_intervals(row["time"], change_intervals, margin_s=40e-12)
    ]
    if len(stable) < 6:
        stable = [
            row
            for row in ordered
            if _is_stable_quantization_point(row["vin"])
        ]
    if not stable:
        return []

    selected: list[dict[str, float]] = []
    start = 0
    for index in range(1, len(stable) + 1):
        if index < len(stable) and _expected_code(stable[index]["vin"]) == _expected_code(
            stable[index - 1]["vin"]
        ):
            continue
        segment = stable[start:index]
        vin_min = min(row["vin"] for row in segment)
        vin_max = max(row["vin"] for row in segment)
        # Two semantic probes per represented code catch half-LSB rounding
        # faults without making coverage depend on the simulator's row count.
        for fraction in (0.25, 0.75):
            target = vin_min + fraction * (vin_max - vin_min)
            sample = min(segment, key=lambda row: abs(row["vin"] - target))
            if not selected or sample is not selected[-1]:
                selected.append(sample)
        start = index
    return selected

def check_v3_498_dc_aware_adc3bit(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin", "d2", "d1", "d0"}
    missing = require_signals(rows, required, "P_3BIT_QUANTIZATION")
    if missing:
        return False, missing

    samples = _representative_rows(rows)
    checked = 0
    codes: list[int] = []
    clamp_failures: list[str] = []
    failures: list[str] = []
    for row in samples:
        vin = row["vin"]
        code = _expected_code(vin)
        observed = _observed_code(row)
        if observed != code:
            failure = f"t={row['time']:.6e}s vin={vin:.3f} expected_code={code} observed_code={observed}"
            if vin < 0.0 or vin > 1.0:
                clamp_failures.append(failure)
            else:
                failures.append(failure)
        codes.append(code)
        checked += 1
    if checked < 6:
        return False, diagnostic(
            "P_3BIT_QUANTIZATION",
            "insufficient_excitation",
            expected="stable_input_code_samples>=6",
            observed=f"stable_input_code_samples={checked}",
            event="vin_plateaus",
        )
    if min(codes) != 0 or max(codes) != 7 or len(set(codes)) < 5:
        return False, diagnostic(
            "P_MONOTONIC_CODE_COVERAGE",
            "insufficient_excitation",
            expected="codes_span_0_to_7_with_at_least_5_unique_codes",
            observed=f"codes={codes}",
            event="vin_plateaus",
        )
    if clamp_failures:
        return False, diagnostic(
            "P_DC_INPUT_CLAMP",
            "behavior_mismatch",
            expected="out_of_range_inputs_saturate_to_clipped_endpoint_codes",
            observed=";".join(clamp_failures[:3]),
            event="vin_plateaus",
        )
    if failures:
        return False, diagnostic(
            "P_3BIT_QUANTIZATION",
            "behavior_mismatch",
            expected="d2d1d0=floor(8*clamp(vin,0,1))",
            observed=";".join(failures[:3]),
            event="vin_plateaus",
        )
    return True, pass_note(PROPERTY_IDS, f"dc_adc_samples={checked} codes={codes}")

CHECKER_ID = "v4_050_dc_aware_adc3bit"
CHECKER: Checker = check_v3_498_dc_aware_adc3bit
