"""Stimulus-relative checker for canonical v4 DUT 015."""

from __future__ import annotations

from ..api import Checker, Row
from .trace_utils import plateau_sample_index, property_diagnostics, stable_logic_plateaus


BITS = ["code_0", "code_1", "code_2", "code_3"]


def check_simple_binary_dac_4b(rows: list[Row]) -> tuple[bool, str]:
    required = {"time", "aout", "vref", "vss", *BITS}
    missing = sorted(required - (set(rows[0]) if rows else set()))
    if missing:
        return False, "missing_columns=" + ",".join(missing)

    plateaus = stable_logic_plateaus(rows, BITS, minimum_duration_s=1e-9)
    observations: list[tuple[int, float, float]] = []
    for start, end, vector in plateaus:
        row = rows[plateau_sample_index(rows, start, end)]
        code = sum(bit << index for index, bit in enumerate(vector))
        expected = row["vss"] + (row["vref"] - row["vss"]) * code / 15.0
        observations.append((code, row["aout"], expected))

    unique = {code for code, _, _ in observations}
    missing_codes = set(range(16)) - unique
    level_errors = sum(abs(observed - expected) > 0.025 for _, observed, expected in observations)
    endpoints = sum(
        abs(observed - expected) > 0.025
        for code, observed, expected in observations
        if code in {0, 15}
    ) + int(0 not in unique) + int(15 not in unique)
    ordered = sorted({code: observed for code, observed, _ in observations}.items())
    monotonic_errors = sum(right + 0.003 < left for (_, left), (_, right) in zip(ordered, ordered[1:]))
    counts = {
        "P_BINARY_WEIGHTS": level_errors + len(missing_codes),
        "P_ENDPOINTS": endpoints,
        "P_LINEAR_MONOTONIC_MAPPING": level_errors + monotonic_errors,
        "P_CONTINUOUS_UPDATE": level_errors + len(missing_codes),
    }
    ok = len(unique) == 16 and all(count == 0 for count in counts.values())
    coverage = "" if not missing_codes else f" insufficient_excitation_missing_codes={sorted(missing_codes)}"
    levels = ",".join(f"{code}:{observed:.3f}/{expected:.3f}" for code, observed, expected in observations)
    return ok, f"levels={levels}{coverage}; {property_diagnostics(counts)}"


CHECKER_ID = "v4_015_binary_weighted_voltage_dac"
CHECKER: Checker = check_simple_binary_dac_4b
