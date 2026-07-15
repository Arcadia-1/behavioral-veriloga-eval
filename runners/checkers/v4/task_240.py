"""Task-specific checker for canonical v4 DUT 240."""
from __future__ import annotations

from ..api import Checker
import math

def check_v3_limiting_diffamp(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "sigin_p", "sigin_n", "sigout"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing limiting diffamp signals"
    max_err = 0.0
    checked = 0
    low_soft = linear = high_soft = 0
    limit = 0.75
    gain = 4.0
    for row in rows:
        if row["time"] < 0.15e-9:
            continue
        raw = gain * (row["sigin_p"] - row["sigin_n"])
        expected = limit * math.tanh(raw / limit)
        if raw <= -limit:
            low_soft += 1
        elif raw >= limit:
            high_soft += 1
        else:
            linear += 1
        max_err = max(max_err, abs(row["sigout"] - expected))
        checked += 1
    if checked < 20 or low_soft == 0 or linear == 0 or high_soft == 0:
        return False, (
            f"insufficient_smooth_limiting_diffamp_coverage checked={checked} "
            f"low={low_soft} linear={linear} high={high_soft}"
        )
    return max_err <= 0.03, (
        f"checked={checked} low={low_soft} linear={linear} "
        f"high={high_soft} max_err={max_err:.5f}"
    )

def check_v3_smooth_limiting_diffamp(rows: list[dict[str, float]]) -> tuple[bool, str]:
    return check_v3_limiting_diffamp(rows)

CHECKER_ID = "v4_240_limiting_diffamp"
CHECKER: Checker = check_v3_smooth_limiting_diffamp
