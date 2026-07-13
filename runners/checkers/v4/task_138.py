"""Task-specific checker for canonical v4 DUT 138."""
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

def check_v3_voltage_controlled_gain_amplifier(rows: list[dict[str, float]]) -> tuple[bool, str]:
    regions: set[str] = set()

    def expected(row: dict[str, float]) -> float:
        target = 1.5 * (row["vctrl_p"] - row["vctrl_n"]) * ((row["vin_p"] - row["vin_n"]) - 0.05) + 0.5
        if target < 0.1:
            regions.add("low")
            return 0.1
        if target > 0.9:
            regions.add("high")
            return 0.9
        regions.add("linear")
        return target

    ok, detail = _v3_formula_check(
        rows,
        required={"time", "vin_p", "vin_n", "vctrl_p", "vctrl_n", "vout"},
        output="vout",
        expected_fn=expected,
        tol=0.025,
        min_checked=20,
    )
    if not ok:
        return ok, detail
    if regions != {"low", "linear", "high"}:
        return False, f"insufficient_vcga_regions={sorted(regions)}"
    return True, f"{detail} regions={sorted(regions)}"

CHECKER_ID = "v4_138_voltage_controlled_gain_amplifier"
CHECKER: Checker = check_v3_voltage_controlled_gain_amplifier
