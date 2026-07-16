"""Stimulus-relative checker for canonical v4 DUT 014."""

from __future__ import annotations

from ..api import Checker, Row
from .trace_utils import plateau_sample_index, property_diagnostics, stable_logic_plateaus


BITS = ["b0", "b1", "t0", "t1", "t2"]
PROPERTIES = (
    "P_SEGMENT_WEIGHTS",
    "P_CODE_MONOTONICITY",
    "P_ENDPOINTS",
    "P_RAIL_RELATIVE_MAPPING",
)


def check_segmented_dac(rows: list[Row]) -> tuple[bool, str]:
    required = {"time", "aout", "vref", "vss", *BITS}
    missing = sorted(required - (set(rows[0]) if rows else set()))
    if missing:
        return False, "missing_columns=" + ",".join(missing)

    plateaus = stable_logic_plateaus(rows, BITS, minimum_duration_s=1e-9)
    observations: list[tuple[int, float, float, float]] = []
    for start, end, vector in plateaus:
        index = plateau_sample_index(rows, start, end)
        row = rows[index]
        code = vector[0] + 2 * vector[1] + 4 * sum(vector[2:])
        expected = row["vss"] + (row["vref"] - row["vss"]) * code / 15.0
        observations.append((code, row["aout"], expected, row["time"]))

    unique_codes = {code for code, *_ in observations}
    coverage_missing = max(0, 5 - len(unique_codes)) + int(0 not in unique_codes) + int(15 not in unique_codes)
    level_errors = sum(abs(observed - expected) > 0.025 for _, observed, expected, _ in observations)
    endpoint_errors = sum(
        abs(observed - expected) > 0.025
        for code, observed, expected, _ in observations
        if code in {0, 15}
    ) + int(0 not in unique_codes) + int(15 not in unique_codes)
    ordered = sorted({code: observed for code, observed, _, _ in observations}.items())
    monotonic_errors = sum(right + 0.003 < left for (_, left), (_, right) in zip(ordered, ordered[1:]))
    # The expected-value comparison already exercises the observed local rails;
    # keep a separate range diagnostic for clearer feedback.
    rail_errors = sum(
        observed < min(rows[plateau_sample_index(rows, start, end)]["vss"], rows[plateau_sample_index(rows, start, end)]["vref"]) - 0.025
        or observed > max(rows[plateau_sample_index(rows, start, end)]["vss"], rows[plateau_sample_index(rows, start, end)]["vref"]) + 0.025
        for (start, end, _), (_, observed, _, _) in zip(plateaus, observations)
    )

    counts = {
        "P_SEGMENT_WEIGHTS": level_errors + coverage_missing,
        "P_CODE_MONOTONICITY": monotonic_errors + int(len(unique_codes) < 3),
        "P_ENDPOINTS": endpoint_errors,
        "P_RAIL_RELATIVE_MAPPING": level_errors + rail_errors,
    }
    ok = bool(observations) and all(count == 0 for count in counts.values())
    coverage = "" if coverage_missing == 0 else f" insufficient_excitation={coverage_missing}"
    levels = ",".join(f"{code}:{observed:.3f}/{expected:.3f}" for code, observed, expected, _ in observations)
    return ok, f"levels={levels} unique_codes={sorted(unique_codes)}{coverage}; {property_diagnostics(counts)}"


CHECKER_ID = "v4_014_segmented_dac"
CHECKER: Checker = check_segmented_dac
