"""Task-specific checker for canonical v4 DUT 139."""
from __future__ import annotations

from ..api import Checker
def check_v3_ideal_differential_opamp(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vinp", "vinn", "voutp", "voutn"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/vinp/vinn/voutp/voutn"
    stride = max(1, len(rows) // 240)
    checked = 0
    max_err = 0.0
    max_cm_error = 0.0
    signed_gain_coverage = {"pos": False, "neg": False}
    for row in rows[::stride]:
        diff = 2.0 * (row["vinp"] - row["vinn"])
        expected_p = 0.5 + diff
        expected_n = 0.5 - diff
        signed_gain_coverage["pos"] = signed_gain_coverage["pos"] or diff > 0.05
        signed_gain_coverage["neg"] = signed_gain_coverage["neg"] or diff < -0.05
        max_err = max(max_err, abs(row["voutp"] - expected_p), abs(row["voutn"] - expected_n))
        voutp = row["voutp"]
        voutn = row["voutn"]
        max_cm_error = max(max_cm_error, abs(0.5 * (voutp + voutn) - 0.5))
        checked += 1
    if checked < 20:
        return False, f"too_few_opamp_samples={checked}"
    if not all(signed_gain_coverage.values()):
        return False, f"insufficient_signed_gain_coverage={signed_gain_coverage}"
    ok = max_err <= 0.035 and max_cm_error <= 0.02
    return ok, f"checked={checked} max_error={max_err:.5f} max_cm_error={max_cm_error:.5f}"

CHECKER_ID = "v4_139_ideal_differential_opamp"
CHECKER: Checker = check_v3_ideal_differential_opamp
