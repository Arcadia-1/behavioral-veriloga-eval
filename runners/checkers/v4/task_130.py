"""Task-specific checker for canonical v4 DUT 130."""
from __future__ import annotations

from checkers.api import Checker
def check_v3_differential_gain_driver(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "sigin_p", "sigin_n", "sigout_p", "sigout_n", "sigref"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/sigin_p/sigin_n/sigout_p/sigout_n/sigref"
    stride = max(1, len(rows) // 240)
    checked = 0
    max_err = 0.0
    regions: set[str] = set()
    for row in rows[::stride]:
        diff = row["sigin_p"] - row["sigin_n"]
        if diff < -0.03:
            regions.add("negative")
        elif diff > 0.03:
            regions.add("positive")
        else:
            regions.add("zero")
        expected_p = row["sigref"] + diff
        expected_n = row["sigref"] - diff
        max_err = max(max_err, abs(row["sigout_p"] - expected_p), abs(row["sigout_n"] - expected_n))
        checked += 1
    if checked < 20:
        return False, f"too_few_differential_gain_samples={checked}"
    if max_err > 0.02:
        return False, f"checked={checked} max_error={max_err:.5f}"
    if regions != {"negative", "zero", "positive"}:
        return False, f"insufficient_differential_gain_regions={sorted(regions)}"
    return True, f"checked={checked} max_error={max_err:.5f} regions={sorted(regions)}"

CHECKER_ID = "v4_130_differential_gain_driver"
CHECKER: Checker = check_v3_differential_gain_driver
