"""Task-specific checker for canonical v4 DUT 232."""
from __future__ import annotations

from checkers.api import Checker
def check_v3_safe_analog_divider(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "signumer", "sigdenom", "sigout"}
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0])) if rows else sorted(required)
        return False, "missing_safe_divider_columns=" + ",".join(missing)
    regions = {
        "normal_positive": False,
        "guard_nonnegative": False,
        "guard_negative": False,
        "normal_negative": False,
    }
    checked = 0
    max_err = 0.0
    worst: tuple[float, float, float, float] | None = None
    for row in rows:
        if row["time"] < 0.10e-9:
            continue
        denominator = row["sigdenom"]
        if denominator >= 0.2:
            guarded = denominator
            regions["normal_positive"] = True
        elif denominator >= 0.0:
            guarded = 0.2
            regions["guard_nonnegative"] = True
        elif denominator > -0.2:
            guarded = -0.2
            regions["guard_negative"] = True
        else:
            guarded = denominator
            regions["normal_negative"] = True
        expected = row["signumer"] / guarded
        error = abs(row["sigout"] - expected)
        if error >= max_err:
            max_err = error
            worst = (row["time"], denominator, row["sigout"], expected)
        checked += 1
    if checked < 20:
        return False, f"insufficient_safe_divider_samples={checked}"
    missing_regions = sorted(name for name, seen in regions.items() if not seen)
    if missing_regions:
        return False, "missing_safe_divider_regions=" + ",".join(missing_regions)
    if max_err > 0.05:
        assert worst is not None
        time_s, denominator, observed, expected = worst
        return False, (
            f"safe_divider_error@{time_s * 1e9:.3f}ns denom={denominator:.4f} "
            f"observed={observed:.4f} expected={expected:.4f} max_err={max_err:.4f}"
        )
    return True, f"checked={checked} regions={sorted(regions)} max_err={max_err:.4f}"

CHECKER_ID = "v4_232_safe_analog_divider"
CHECKER: Checker = check_v3_safe_analog_divider
