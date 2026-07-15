"""Task-specific checker for canonical v4 DUT 116."""
from __future__ import annotations

from ..api import Checker
def check_v3_max_detector_hold(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin", "vout"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/vin/vout"
    running_max = rows[0]["vin"]
    stride = max(1, len(rows) // 240)
    checked = 0
    max_err = 0.0
    input_dropped_after_peak = False
    previous_vout = rows[0]["vout"]
    monotone_ok = True
    for idx, row in enumerate(rows):
        running_max = max(running_max, row["vin"])
        if row["vin"] < running_max - 0.05:
            input_dropped_after_peak = True
        if row["vout"] < previous_vout - 0.01:
            monotone_ok = False
        previous_vout = row["vout"]
        if idx % stride == 0:
            max_err = max(max_err, abs(row["vout"] - running_max))
            checked += 1
    if checked < 20:
        return False, f"too_few_max_hold_samples={checked}"
    if not monotone_ok:
        return False, "max_detector_output_not_monotonic"
    if not input_dropped_after_peak:
        return False, "max_detector_missing_hold_after_input_drop"
    return max_err <= 0.03, f"checked={checked} max_error={max_err:.5f} monotonic_hold=True"

CHECKER_ID = "v4_116_max_detector_hold"
CHECKER: Checker = check_v3_max_detector_hold
