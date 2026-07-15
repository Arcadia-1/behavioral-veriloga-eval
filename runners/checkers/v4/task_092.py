"""Task-specific checker for canonical v4 DUT 092."""
from __future__ import annotations

from ..api import Checker
def check_v3_fixed_gain_amplifier(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"vin_p", "vin_n", "vout_p", "vout_n"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing vin_p/vin_n/vout_p/vout_n"

    gains: list[float] = []
    cm_errors: list[float] = []
    for row in rows:
        vin_diff = row["vin_p"] - row["vin_n"]
        if abs(vin_diff) < 0.015:
            continue
        out_diff = row["vout_p"] - row["vout_n"]
        gains.append(out_diff / vin_diff)
        cm_errors.append(abs(0.5 * (row["vout_p"] + row["vout_n"]) - 0.45))

    if len(gains) < 20:
        return False, f"insufficient_nonzero_input_samples={len(gains)}"
    gain_mean = sum(gains) / len(gains)
    gain_err = sum(abs(value - gain_mean) for value in gains) / len(gains)
    cm_max = max(cm_errors) if cm_errors else float("inf")
    ok = 4.5 <= gain_mean <= 5.6 and gain_err <= 0.08 and cm_max <= 0.006
    return ok, f"gain={gain_mean:.3f} gain_err={gain_err:.4f} cm_max={cm_max:.4f}"

CHECKER_ID = "v4_092_fixed_gain_amplifier"
CHECKER: Checker = check_v3_fixed_gain_amplifier
