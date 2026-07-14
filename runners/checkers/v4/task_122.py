"""Task-specific checker for canonical v4 DUT 122."""
from __future__ import annotations

from checkers.api import Checker
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

def check_v3_differential_deadband(rows: list[dict[str, float]]) -> tuple[bool, str]:
    regions: set[str] = set()

    def expected(row: dict[str, float]) -> float:
        diff = row["sigin_p"] - row["sigin_n"]
        if diff < -0.2:
            regions.add("below")
            return diff + 0.25
        if diff > 0.2:
            regions.add("above")
            return diff - 0.15
        regions.add("inside")
        return 0.05

    ok, detail = _v3_formula_check(
        rows,
        required={"time", "sigin_p", "sigin_n", "sigout"},
        output="sigout",
        expected_fn=expected,
        tol=0.015,
        min_checked=20,
    )
    if not ok:
        return ok, detail
    if regions != {"below", "inside", "above"}:
        return False, f"insufficient_diff_deadband_region_coverage={sorted(regions)}"
    return True, f"{detail} regions={sorted(regions)}"

CHECKER_ID = "v4_122_differential_deadband"
CHECKER: Checker = check_v3_differential_deadband
