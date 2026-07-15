"""Task-specific checker for canonical v4 DUT 131."""
from __future__ import annotations

from ..api import Checker
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

def check_v3_limiting_differential_amplifier(rows: list[dict[str, float]]) -> tuple[bool, str]:
    regions: set[str] = set()

    def expected(row: dict[str, float]) -> float:
        target = 0.2 + 3.0 * ((row["sigin_p"] - row["sigin_n"]) - 0.05)
        if target < -0.4:
            regions.add("low")
            return -0.4
        if target > 0.8:
            regions.add("high")
            return 0.8
        regions.add("linear")
        return target

    ok, detail = _v3_formula_check(
        rows,
        required={"time", "sigin_p", "sigin_n", "sigout"},
        output="sigout",
        expected_fn=expected,
        tol=0.02,
        min_checked=20,
    )
    if not ok:
        return ok, detail
    if regions != {"low", "linear", "high"}:
        return False, f"insufficient_limiting_diffamp_regions={sorted(regions)}"
    return True, f"{detail} regions={sorted(regions)}"

CHECKER_ID = "v4_131_limiting_differential_amplifier"
CHECKER: Checker = check_v3_limiting_differential_amplifier
