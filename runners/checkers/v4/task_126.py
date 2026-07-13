"""Task-specific checker for canonical v4 DUT 126."""
from __future__ import annotations

from checkers.api import Checker
def check_v3_absolute_value(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "sigin", "sigout"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing absolute value signals"
    max_err = 0.0
    checked = 0
    for row in rows:
        if row.get("time", 0.0) < 0.2e-9:
            continue
        err = abs(row["sigout"] - abs(row["sigin"]))
        max_err = max(max_err, err)
        checked += 1
    if checked == 0:
        return False, "no_absolute_value_rows_checked"
    return max_err <= 0.02, f"checked={checked} max_abs_error={max_err:.5f}"

CHECKER_ID = "v4_126_absolute_value"
CHECKER: Checker = check_v3_absolute_value
