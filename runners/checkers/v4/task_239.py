"""Task-specific checker for canonical v4 DUT 239."""
from __future__ import annotations

from ..api import Checker
def check_v3_deadband_diffamp(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "sigin_p", "sigin_n", "sigout"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing deadband diffamp signals"
    max_err = 0.0
    checked = 0
    below = inside = above = 0
    for row in rows:
        if row["time"] < 0.15e-9:
            continue
        diff = row["sigin_p"] - row["sigin_n"]
        if diff < -0.1:
            expected = 2.0 * (diff + 0.1) + 0.02
            below += 1
        elif diff > 0.1:
            expected = 3.0 * (diff - 0.1) + 0.02
            above += 1
        else:
            expected = 0.02
            inside += 1
        max_err = max(max_err, abs(row["sigout"] - expected))
        checked += 1
    if checked < 20 or below == 0 or inside == 0 or above == 0:
        return False, f"insufficient_deadband_diffamp_coverage checked={checked} below={below} inside={inside} above={above}"
    return max_err <= 0.04, f"checked={checked} below={below} inside={inside} above={above} max_err={max_err:.5f}"

CHECKER_ID = "v4_239_deadband_diffamp"
CHECKER: Checker = check_v3_deadband_diffamp
