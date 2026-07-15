"""Task-specific checker for canonical v4 DUT 090."""
from __future__ import annotations

from ..api import Checker
def check_v3_dither_adder(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"vres_p", "vres_n", "dpn", "vout_p", "vout_n"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing vres_p/vres_n/dpn/vout_p/vout_n"

    high: list[float] = []
    low: list[float] = []
    cm_errors: list[float] = []
    guard_s = 2.5e-10
    last_dpn_transition = -1.0e99
    prev_dpn: float | None = None
    for row in rows:
        cur_dpn = row["dpn"]
        cur_time = row.get("time")
        if cur_time is not None:
            if cur_time <= guard_s:
                prev_dpn = cur_dpn
                continue
            crossed_threshold = (
                prev_dpn is not None
                and (prev_dpn - 0.45) * (cur_dpn - 0.45) <= 0.0
                and prev_dpn != cur_dpn
            )
            if crossed_threshold:
                last_dpn_transition = cur_time
            if cur_time - last_dpn_transition <= guard_s:
                prev_dpn = cur_dpn
                continue
        prev_dpn = cur_dpn
        vin_diff = row["vres_p"] - row["vres_n"]
        out_diff = row["vout_p"] - row["vout_n"]
        dither_diff = out_diff - vin_diff
        if cur_dpn > 0.45:
            high.append(dither_diff)
        else:
            low.append(dither_diff)
        in_cm = 0.5 * (row["vres_p"] + row["vres_n"])
        out_cm = 0.5 * (row["vout_p"] + row["vout_n"])
        cm_errors.append(abs(out_cm - in_cm))

    if len(high) < 20 or len(low) < 20:
        return False, f"insufficient_dpn_states high={len(high)} low={len(low)}"
    high_mean = sum(high) / len(high)
    low_mean = sum(low) / len(low)
    high_err = sum(abs(value - high_mean) for value in high) / len(high)
    low_err = sum(abs(value - low_mean) for value in low) / len(low)
    cm_max = max(cm_errors) if cm_errors else float("inf")
    symmetry_err = abs(high_mean + low_mean)
    ok = (
        0.020 <= high_mean <= 0.040
        and -0.040 <= low_mean <= -0.020
        and symmetry_err <= 0.002
        and high_err <= 0.003
        and low_err <= 0.003
        and cm_max <= 0.003
    )
    return ok, (
        f"dither_high={high_mean:.4f} dither_low={low_mean:.4f} "
        f"symmetry_err={symmetry_err:.4f} high_err={high_err:.4f} "
        f"low_err={low_err:.4f} cm_max={cm_max:.4f}"
    )

CHECKER_ID = "v4_090_dither_adder"
CHECKER: Checker = check_v3_dither_adder
