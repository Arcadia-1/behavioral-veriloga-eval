"""Task-specific checker for canonical v4 DUT 132."""
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

def check_v3_analog_multiplier(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "sigin1", "sigin2", "sigout"}
    has_negative_product = False

    def expected(row: dict[str, float]) -> float:
        nonlocal has_negative_product
        product = 2.0 * row["sigin1"] * row["sigin2"]
        has_negative_product = has_negative_product or product < -0.05
        return product

    ok, detail = _v3_formula_check(
        rows,
        required=required,
        output="sigout",
        expected_fn=expected,
        tol=0.025,
        min_checked=20,
    )
    if not ok:
        return ok, detail
    if not has_negative_product:
        return False, "multiplier_missing_negative_product_coverage"
    return True, detail

CHECKER_ID = "v4_132_analog_multiplier"
CHECKER: Checker = check_v3_analog_multiplier
