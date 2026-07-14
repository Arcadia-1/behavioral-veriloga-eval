"""Task-specific checker for canonical v4 DUT 114."""
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

def check_v3_analog_mux_threshold(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin1", "vin2", "vsel", "vout"}
    modes: set[int] = set()

    def expected(row: dict[str, float]) -> float:
        mode = 1 if row["vsel"] > 0.45 else 0
        modes.add(mode)
        return row["vin1"] if mode else row["vin2"]

    ok, detail = _v3_formula_check(
        rows,
        required=required,
        output="vout",
        expected_fn=expected,
        stable_fn=lambda row: abs(row["vsel"] - 0.45) > 0.05,
        tol=0.035,
        min_checked=20,
    )
    if not ok:
        return ok, detail
    if modes != {0, 1}:
        return False, f"insufficient_mux_selection_coverage={sorted(modes)}"
    return True, detail + " modes=0,1"

CHECKER_ID = "v4_114_analog_mux_threshold"
CHECKER: Checker = check_v3_analog_mux_threshold
