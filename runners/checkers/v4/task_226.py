"""Task-specific checker for canonical v4 DUT 226."""
from __future__ import annotations

from checkers.api import Checker
def check_v3_level_shifter_offset(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "sigin", "sigout"}
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0])) if rows else sorted(required)
        return False, "missing_level_shifter_columns=" + ",".join(missing)
    checked = 0
    max_err = 0.0
    worst: tuple[float, float, float] | None = None
    input_min = input_max = rows[0]["sigin"]
    saw_rise = saw_fall = False
    previous = rows[0]["sigin"]
    for row in rows:
        if row["time"] < 0.10e-9:
            previous = row["sigin"]
            continue
        expected = row["sigin"] + 0.35
        error = abs(row["sigout"] - expected)
        if error >= max_err:
            max_err = error
            worst = (row["time"], row["sigout"], expected)
        delta = row["sigin"] - previous
        saw_rise = saw_rise or delta > 0.05
        saw_fall = saw_fall or delta < -0.05
        input_min = min(input_min, row["sigin"])
        input_max = max(input_max, row["sigin"])
        previous = row["sigin"]
        checked += 1
    if checked < 20:
        return False, f"insufficient_level_shifter_samples={checked}"
    if input_max - input_min < 0.50 or not (saw_rise and saw_fall):
        return False, (
            f"insufficient_level_shifter_coverage range={input_min:.3f}:{input_max:.3f} "
            f"rise={saw_rise} fall={saw_fall}"
        )
    if max_err > 0.025:
        assert worst is not None
        time_s, observed, expected = worst
        return False, (
            f"level_shift_error@{time_s * 1e9:.3f}ns observed={observed:.4f} "
            f"expected={expected:.4f} max_err={max_err:.4f}"
        )
    return True, (
        f"checked={checked} input_range={input_min:.3f}:{input_max:.3f} "
        f"rise={saw_rise} fall={saw_fall} max_err={max_err:.4f}"
    )

CHECKER_ID = "v4_226_level_shifter_offset"
CHECKER: Checker = check_v3_level_shifter_offset
