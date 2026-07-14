"""Task-specific checker for canonical v4 DUT 237."""
from __future__ import annotations

from checkers.api import Checker
import math

def check_v3_smooth_absolute_value(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "sigin", "sigout"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing smooth absolute value signals"
    smooth = 0.05
    max_err = 0.0
    checked = 0
    positive = negative = near_zero = 0
    for row in rows:
        if row.get("time", 0.0) < 0.2e-9:
            continue
        sigin = row["sigin"]
        expected = sigin * math.tanh(sigin / smooth)
        max_err = max(max_err, abs(row["sigout"] - expected))
        checked += 1
        if sigin > 0.10:
            positive += 1
        elif sigin < -0.10:
            negative += 1
        else:
            near_zero += 1
    if checked < 20 or positive == 0 or negative == 0 or near_zero == 0:
        return False, (
            f"insufficient_smooth_abs_coverage checked={checked} "
            f"positive={positive} negative={negative} near_zero={near_zero}"
        )
    return max_err <= 0.008, (
        f"checked={checked} positive={positive} negative={negative} "
        f"near_zero={near_zero} max_smooth_abs_error={max_err:.5f}"
    )

CHECKER_ID = "v4_237_absolute_value"
CHECKER: Checker = check_v3_smooth_absolute_value
