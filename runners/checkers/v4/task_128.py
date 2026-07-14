"""Task-specific checker for canonical v4 DUT 128."""
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

def check_v3_safe_voltage_divider(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "signumer", "sigdenom", "sigout"}
    guarded = 0
    negative_guarded = 0

    def expected(row: dict[str, float]) -> float:
        nonlocal guarded, negative_guarded
        denominator = row["sigdenom"]
        if abs(denominator) < 0.25:
            guarded += 1
            if denominator < 0:
                negative_guarded += 1
            denominator = 0.25 if denominator >= 0 else -0.25
        return 2.0 * row["signumer"] / denominator

    ok, detail = _v3_formula_check(
        rows,
        required=required,
        output="sigout",
        expected_fn=expected,
        tol=0.05,
        min_checked=20,
    )
    if not ok:
        return ok, detail
    if guarded == 0 or negative_guarded == 0:
        return False, f"insufficient_guard_coverage guarded={guarded} negative_guarded={negative_guarded}"
    return True, f"{detail} guarded={guarded} negative_guarded={negative_guarded}"

CHECKER_ID = "v4_128_safe_voltage_divider"
CHECKER: Checker = check_v3_safe_voltage_divider
