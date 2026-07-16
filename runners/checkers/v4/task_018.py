"""Stimulus-relative checker for canonical v4 DUT 018."""

from __future__ import annotations

from collections import defaultdict

from ..api import Checker, Row
from .trace_utils import plateau_sample_index, property_diagnostics, stable_logic_plateaus


SEGMENTS = [f"seg{index}" for index in range(15)]


def check_vbm1_thermometer_dac_15seg(rows: list[Row]) -> tuple[bool, str]:
    required = {"time", "aout", "vref", "vss", *SEGMENTS}
    missing = sorted(required - (set(rows[0]) if rows else set()))
    if missing:
        return False, "missing_columns=" + ",".join(missing)

    plateaus = stable_logic_plateaus(rows, SEGMENTS, minimum_duration_s=1e-9)
    observations: list[tuple[int, tuple[int, ...], float, float]] = []
    for start, end, vector in plateaus:
        # The public 500 ps response must already be settled near the start of
        # each multi-nanosecond plateau; sampling only at the end hides slow
        # implementations that violate that contract.
        row = rows[plateau_sample_index(rows, start, end, fraction=0.20)]
        count = sum(vector)
        expected = row["vss"] + (row["vref"] - row["vss"]) * count / 15.0
        observations.append((count, vector, row["aout"], expected))

    counts_seen = {count for count, _, _, _ in observations}
    masks_by_count: dict[int, set[tuple[int, ...]]] = defaultdict(set)
    for count, vector, _, _ in observations:
        masks_by_count[count].add(vector)
    permutation_pairs = sum(len(masks) - 1 for masks in masks_by_count.values() if len(masks) > 1)
    level_errors = sum(abs(observed - expected) > 0.025 for _, _, observed, expected in observations)
    endpoint_errors = sum(
        abs(observed - expected) > 0.025
        for count, _, observed, expected in observations
        if count in {0, 15}
    ) + int(0 not in counts_seen) + int(15 not in counts_seen)
    ordered = sorted({count: observed for count, _, observed, _ in observations}.items())
    monotonic_errors = sum(right + 0.003 < left for (_, left), (_, right) in zip(ordered, ordered[1:]))
    coverage_missing = int(len(counts_seen) < 5) + int(permutation_pairs < 1)
    counts = {
        "P_ZERO_SCALE": int(0 not in counts_seen) + endpoint_errors,
        "P_FULL_SCALE": int(15 not in counts_seen) + endpoint_errors,
        "P_UNIT_ELEMENT_WEIGHT": level_errors + coverage_missing,
        "P_PERMUTATION_INVARIANCE": level_errors + int(permutation_pairs < 1),
        "P_COUNT_MONOTONICITY": monotonic_errors + int(len(counts_seen) < 3),
    }
    ok = bool(observations) and all(count == 0 for count in counts.values())
    coverage = "" if coverage_missing == 0 else f" insufficient_excitation={coverage_missing}"
    levels = ",".join(f"{count}:{observed:.3f}/{expected:.3f}" for count, _, observed, expected in observations)
    return ok, (
        f"levels={levels} counts={sorted(counts_seen)} permutation_pairs={permutation_pairs}{coverage}; "
        f"{property_diagnostics(counts)}"
    )


CHECKER_ID = "v4_018_unit_element_thermometer_dac"
CHECKER: Checker = check_vbm1_thermometer_dac_15seg
