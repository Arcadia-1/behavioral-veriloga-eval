"""Task-specific checker for canonical v4 DUT 133."""
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

def check_v3_three_way_threshold_mux(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "sigin1", "sigin2", "sigin3", "cntrlp", "cntrlm", "sigout"}
    regions: set[str] = set()

    def expected(row: dict[str, float]) -> float:
        ctrl = row["cntrlp"] - row["cntrlm"]
        if ctrl < -0.2:
            regions.add("low")
            return row["sigin1"]
        if ctrl <= 0.2:
            regions.add("mid")
            return row["sigin2"]
        regions.add("high")
        return row["sigin3"]

    ok, detail = _v3_formula_check(
        rows,
        required=required,
        output="sigout",
        expected_fn=expected,
        stable_fn=lambda row: min(abs((row["cntrlp"] - row["cntrlm"]) + 0.2), abs((row["cntrlp"] - row["cntrlm"]) - 0.2)) > 0.03,
        tol=0.03,
        min_checked=20,
    )
    if not ok:
        return ok, detail
    if regions != {"low", "mid", "high"}:
        return False, f"insufficient_threshold_mux_regions={sorted(regions)}"
    return True, detail + " regions=low,mid,high"

CHECKER_ID = "v4_133_three_way_threshold_mux"
CHECKER: Checker = check_v3_three_way_threshold_mux
