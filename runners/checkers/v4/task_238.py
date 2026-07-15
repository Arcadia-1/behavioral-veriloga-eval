"""Task-specific checker for canonical v4 DUT 238."""
from __future__ import annotations

from ..api import Checker
def check_v3_deadband_voltage(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "sigin", "sigout"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing deadband voltage signals"
    max_err = 0.0
    checked = 0
    below = inside = above = 0
    for row in rows:
        if row["time"] < 0.15e-9:
            continue
        sigin = row["sigin"]
        if sigin < -0.25:
            expected = sigin + 0.25
            below += 1
        elif sigin > 0.25:
            expected = sigin - 0.25
            above += 1
        else:
            expected = 0.0
            inside += 1
        max_err = max(max_err, abs(row["sigout"] - expected))
        checked += 1
    if checked < 20 or below == 0 or inside == 0 or above == 0:
        return False, f"insufficient_deadband_voltage_coverage checked={checked} below={below} inside={inside} above={above}"
    return max_err <= 0.025, f"checked={checked} below={below} inside={inside} above={above} max_err={max_err:.5f}"

CHECKER_ID = "v4_238_deadband_voltage"
CHECKER: Checker = check_v3_deadband_voltage
