"""Task-specific checker for canonical v4 DUT 197."""
from __future__ import annotations

from ..api import Checker, Row
from .trace_utils import plateau_sample_index, property_diagnostics, stable_logic_plateaus

INPUTS = ["din0", "din1", "din2", "din3", "din4", "din5", "din6"]
WEIGHTS = (0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0)
PROPERTIES = {
    "P_INPUT_THRESHOLDING": 0,
    "P_WEIGHTED_CODE_SUM": 0,
    "P_NORMALIZED_SINGLE_ENDED_OUTPUT": 0,
    "P_MONOTONIC_CODE_RESPONSE": 0,
}


def _expected_code(vector: tuple[int, ...]) -> float:
    return sum(weight for bit, weight in zip(vector, WEIGHTS) if bit) / 32.0


def check_v3_single_adc_7b_weighted(rows: list[Row]) -> tuple[bool, str]:
    required = {"time", *INPUTS, "dout"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing single adc 7b weighted signals"

    span = rows[-1]["time"] - rows[0]["time"]
    min_duration = max(span * 0.03, 1e-12)
    plateaus = stable_logic_plateaus(
        rows,
        INPUTS,
        threshold=0.45,
        minimum_duration_s=min_duration,
    )
    if len(plateaus) < 3:
        return (
            False,
            "insufficient_excitation single_adc_7b_weighted "
            f"plateaus={len(plateaus)} required>=3",
        )

    counts = dict(PROPERTIES)
    observations: list[tuple[float, float, tuple[int, ...]]] = []
    max_err = 0.0
    tol = 0.018

    for start, end, vector in plateaus:
        sample_index = plateau_sample_index(rows, start, end, fraction=0.7)
        observed = rows[sample_index]["dout"]
        expected = _expected_code(vector)
        err = abs(observed - expected)
        max_err = max(max_err, err)
        observations.append((expected, observed, vector))
        if err > tol:
            counts["P_WEIGHTED_CODE_SUM"] += 1
            counts["P_NORMALIZED_SINGLE_ENDED_OUTPUT"] += 1
            counts["P_INPUT_THRESHOLDING"] += 1

    distinct_codes = {round(expected, 9) for expected, _, _ in observations}
    if len(distinct_codes) < 3:
        return (
            False,
            "insufficient_excitation single_adc_7b_weighted "
            f"distinct_codes={len(distinct_codes)} required>=3",
        )

    for (prev_expected, prev_observed, _), (expected, observed, _) in zip(
        sorted(observations), sorted(observations)[1:]
    ):
        if expected > prev_expected and observed + tol < prev_observed:
            counts["P_MONOTONIC_CODE_RESPONSE"] += 1

    expected_span = max(expected for expected, _, _ in observations) - min(
        expected for expected, _, _ in observations
    )
    observed_span = max(observed for _, observed, _ in observations) - min(
        observed for _, observed, _ in observations
    )
    if expected_span > 0 and abs(observed_span - expected_span) > tol:
        counts["P_MONOTONIC_CODE_RESPONSE"] += 1

    ok = all(count == 0 for count in counts.values())
    return (
        ok,
        f"{property_diagnostics(counts)}; plateaus={len(plateaus)}; "
        f"distinct_codes={len(distinct_codes)}; max_err={max_err:.6g}",
    )


CHECKER_ID = "v4_197_single_adc_7b_weighted"
CHECKER: Checker = check_v3_single_adc_7b_weighted
