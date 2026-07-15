"""Task-specific checker for canonical v4 DUT 124."""
from __future__ import annotations

from ..api import Checker
import math

def check_v3_smooth_comparator_tanh(rows: list[dict[str, float]]) -> tuple[bool, str]:
    return _check_source_tanh_transfer(rows, high=0.9, low=0.0, offset=0.0, slope=20.0, tol=0.025)

def _check_source_tanh_transfer(
    rows: list[dict[str, float]],
    *,
    high: float,
    low: float,
    offset: float,
    slope: float,
    tol: float,
) -> tuple[bool, str]:
    required = {"time", "sigin", "sigref", "sigout"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing source tanh comparator signals"
    max_err = 0.0
    checked = 0
    for row in rows:
        if row["time"] < 0.05e-9:
            continue
        expected = (
            0.5 * (high - low) * math.tanh(slope * (row["sigin"] - row["sigref"] - offset))
            + 0.5 * (high + low)
        )
        err = abs(row["sigout"] - expected)
        max_err = max(max_err, err)
        checked += 1
    if checked < 20:
        return False, f"insufficient_tanh_rows={checked}"
    return max_err <= tol, f"checked={checked} max_tanh_error={max_err:.5f}"

CHECKER_ID = "v4_124_smooth_comparator_tanh"
CHECKER: Checker = check_v3_smooth_comparator_tanh
