"""Task-specific checker for canonical v4 DUT 298."""
from __future__ import annotations

from ..api import Checker
def sample_signal_at(rows: list[dict[str, float]], signal: str, time_s: float) -> float | None:
    if not rows or "time" not in rows[0] or signal not in rows[0]:
        return None
    first_time = rows[0]["time"]
    last_time = rows[-1].get("time")
    if last_time is None or time_s < first_time or time_s > last_time:
        return None
    if time_s == first_time:
        return rows[0].get(signal)
    for idx in range(1, len(rows)):
        prev = rows[idx - 1]
        cur = rows[idx]
        t0 = prev.get("time")
        t1 = cur.get("time")
        if t0 is None or t1 is None:
            continue
        if t0 <= time_s <= t1:
            v0 = prev.get(signal)
            v1 = cur.get(signal)
            if v0 is None or v1 is None:
                return None
            if t1 == t0:
                return v1
            alpha = (time_s - t0) / (t1 - t0)
            return v0 + alpha * (v1 - v0)
    return None

def check_v3_candidate_afe_differential_common_mode_window_monitor(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vip", "vin", "vcm_ref", "en", "diff_ok", "cm_ok", "valid", "diff_metric", "cm_metric"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing differential common mode window monitor signals"
    end_t = rows[-1]["time"]
    sample_t = 0.75e-9
    checked = 0
    max_err = 0.0
    valid_high = valid_low = diff_fail = cm_fail = enable_low = negative_diff = ref_changed = False
    first_ref: float | None = None
    while sample_t < end_t - 0.2e-9:
        values = {name: sample_signal_at(rows, name, sample_t) for name in required if name != "time"}
        if any(value is None for value in values.values()):
            sample_t += 1.0e-9
            continue
        if first_ref is None:
            first_ref = values["vcm_ref"]
        vdiff = values["vip"] - values["vin"]
        vcm = 0.5 * (values["vip"] + values["vin"])
        diff_abs = abs(vdiff)
        cm_err = abs(vcm - values["vcm_ref"])
        enabled = values["en"] > 0.45
        diff_valid = enabled and diff_abs <= 0.30
        cm_valid = enabled and cm_err <= 0.080
        valid_expected = diff_valid and cm_valid
        diff_expected = 0.9 if diff_valid else 0.0
        cm_expected = 0.9 if cm_valid else 0.0
        full_expected = 0.9 if valid_expected else 0.0
        diff_metric_expected = min(1.0, max(0.0, diff_abs / 0.45)) * 0.9
        cm_metric_expected = min(1.0, max(0.0, cm_err / 0.160)) * 0.9
        max_err = max(
            max_err,
            abs(values["diff_ok"] - diff_expected),
            abs(values["cm_ok"] - cm_expected),
            abs(values["valid"] - full_expected),
            abs(values["diff_metric"] - diff_metric_expected),
            abs(values["cm_metric"] - cm_metric_expected),
        )
        valid_high = valid_high or full_expected > 0.45
        valid_low = valid_low or full_expected < 0.45
        diff_fail = diff_fail or (enabled and diff_abs > 0.30 and cm_err <= 0.080)
        cm_fail = cm_fail or (enabled and diff_abs <= 0.30 and cm_err > 0.080)
        enable_low = enable_low or (not enabled)
        negative_diff = negative_diff or (vdiff < -0.05)
        ref_changed = ref_changed or abs(values["vcm_ref"] - first_ref) > 0.04
        checked += 1
        sample_t += 1.0e-9
    if checked < 10:
        return False, f"insufficient_diff_cm_samples={checked}"
    if not (valid_high and valid_low and diff_fail and cm_fail and enable_low and negative_diff and ref_changed):
        return False, "insufficient_diff_cm_coverage"
    if max_err > 0.08:
        return False, f"diff_cm_monitor_error={max_err:.4f}"
    return True, f"samples={checked} max_err={max_err:.4f}"

CHECKER_ID = "v4_298_differential_common_mode_window_monitor"
CHECKER: Checker = check_v3_candidate_afe_differential_common_mode_window_monitor
