"""Task-specific checker for canonical v4 DUT 135."""
from __future__ import annotations

from ..api import Checker
import math

def _v3_formula_check(
    rows: list[dict[str, float]],
    *,
    required: set[str],
    output: str,
    expected_fn,
    tol: float,
    min_checked: int,
    max_rows: int = 240,
    stable_fn=None,
) -> tuple[bool, str]:
    if not rows or not required.issubset(rows[0]):
        return False, "missing " + "/".join(sorted(required))
    stride = max(1, len(rows) // max_rows)
    checked = 0
    max_err = 0.0
    for row in rows[::stride]:
        if stable_fn is not None and not stable_fn(row):
            continue
        expected = expected_fn(row)
        if expected is None:
            continue
        observed = row.get(output)
        if observed is None:
            return False, f"missing_{output}_sample"
        max_err = max(max_err, abs(observed - expected))
        checked += 1
    if checked < min_checked:
        return False, f"too_few_formula_samples={checked}"
    return max_err <= tol, f"checked={checked} max_error={max_err:.5f}"

def check_v3_logarithmic_amplifier(rows: list[dict[str, float]]) -> tuple[bool, str]:
    regions: set[str] = set()

    def expected(row: dict[str, float]) -> float:
        adjusted = row["sigin"] - 0.2
        magnitude = abs(adjusted)
        if magnitude < 0.1:
            regions.add("floored")
            magnitude = 0.1
        elif adjusted < 0:
            regions.add("negative")
        else:
            regions.add("positive")
        return math.log(magnitude)

    ok, detail = _v3_formula_check(
        rows,
        required={"time", "sigin", "sigout"},
        output="sigout",
        expected_fn=expected,
        tol=0.035,
        min_checked=20,
    )
    if not ok:
        return ok, detail
    if regions != {"floored", "negative", "positive"}:
        return False, f"insufficient_logamp_regions={sorted(regions)}"
    return True, f"{detail} regions={sorted(regions)}"

CHECKER_ID = "v4_135_logarithmic_amplifier"
CHECKER: Checker = check_v3_logarithmic_amplifier
