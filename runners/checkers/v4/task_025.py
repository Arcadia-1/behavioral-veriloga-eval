"""Task-specific checker for canonical v4 DUT 025."""
from __future__ import annotations

from checkers.api import Checker
def check_release_dac_mismatch_unit_weighting(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "b0", "b1", "b2", "b3", "out"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/b0/b1/b2/b3/out"
    weights = [1.00, 2.02, 3.96, 8.08]
    denom = sum(weights)
    sample_times = [7e-9, 15e-9, 25e-9, 35e-9]
    mismatches = 0
    details: list[str] = []
    for t in sample_times:
        row = min(rows, key=lambda r: abs(r["time"] - t))
        code_sum = sum(weights[idx] for idx, bit in enumerate(("b0", "b1", "b2", "b3")) if row[bit] > 0.45)
        expected = 0.9 * code_sum / denom
        actual = row["out"]
        delta = abs(actual - expected)
        details.append(f"{t * 1e9:.0f}ns:{actual:.4f}/{expected:.4f}")
        if delta > 0.0015:
            mismatches += 1
    if mismatches:
        return False, f"dac_weight_mismatches={mismatches} {' '.join(details)}"
    return True, f"dac_weight_samples {' '.join(details)}"

CHECKER_ID = "v4_025_dac_mismatch_unit_weighting_model"
CHECKER: Checker = check_release_dac_mismatch_unit_weighting
