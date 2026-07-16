"""Task-specific checker for canonical v4 DUT 129."""
from __future__ import annotations

from ..api import Checker
def check_v3_polynomial_differential_vcvs(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "inp", "inn", "outp", "outn"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/inp/inn/outp/outn"
    stride = max(1, len(rows) // 240)
    checked = 0
    max_err = 0.0
    max_cm_error = 0.0
    saw_positive = False
    saw_negative = False
    for row in rows[::stride]:
        vid = row["inp"] - row["inn"]
        saw_positive = saw_positive or vid > 0.05
        saw_negative = saw_negative or vid < -0.05
        vod = (2.0 * vid + vid * vid * vid) / 2.0
        if vod > 0.3:
            vod = 0.3
        if vod < -0.3:
            vod = -0.3
        expected_p = 0.5 + vod
        expected_n = 0.5 - vod
        max_err = max(max_err, abs(row["outp"] - expected_p), abs(row["outn"] - expected_n))
        outp = row["outp"]
        outn = row["outn"]
        max_cm_error = max(max_cm_error, abs(0.5 * (outp + outn) - 0.5))
        checked += 1
    if checked < 20:
        return False, f"too_few_vcvs_samples={checked}"
    if not (saw_positive and saw_negative):
        return False, f"insufficient_vcvs_polarity positive={saw_positive} negative={saw_negative}"
    ok = max_err <= 0.035 and max_cm_error <= 0.02
    return ok, f"checked={checked} max_error={max_err:.5f} max_cm_error={max_cm_error:.5f}"

CHECKER_ID = "v4_129_polynomial_differential_vcvs"
CHECKER: Checker = check_v3_polynomial_differential_vcvs
