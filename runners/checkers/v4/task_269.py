"""Task-specific checker for canonical v4 DUT 269."""
from __future__ import annotations

from ..api import Checker
from .family_261_270_diagnostics import bind_properties


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

def _v3_uniform_sample_times(
    rows: list[dict[str, float]],
    *,
    start_s: float = 0.75e-9,
    step_s: float = 0.75e-9,
    end_margin_s: float = 0.25e-9,
) -> list[float]:
    if not rows:
        return []
    start = max(rows[0]["time"] + start_s, rows[0]["time"])
    stop = rows[-1]["time"] - end_margin_s
    times: list[float] = []
    t = start
    while t <= stop:
        times.append(t)
        t += step_s
    return times

def _v3_values_at(
    rows: list[dict[str, float]],
    names: tuple[str, ...],
    time_s: float,
) -> dict[str, float] | None:
    values = {name: sample_signal_at(rows, name, time_s) for name in names}
    if any(value is None for value in values.values()):
        return None
    return {name: float(value) for name, value in values.items() if value is not None}

def check_v3_373_saturation_recovery_limiter(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin", "en", "out", "sat", "recovery_metric"}
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0].keys())) if rows else sorted(required)
        return False, "missing_columns=" + ",".join(missing)
    vlo = 0.12
    vlimit = 0.78
    vhi = 0.9
    checked = 0
    max_err = 0.0
    out_errors = sat_errors = metric_errors = clear_errors = 0
    saw_low_clip = saw_high_clip = saw_linear = saw_disabled = saw_metric = False
    for time_s in _v3_uniform_sample_times(rows):
        values = _v3_values_at(rows, ("vin", "en", "out", "sat", "recovery_metric"), time_s)
        if values is None:
            continue
        raw = values["vin"]
        enabled = values["en"] > 0.45
        limited = min(vlimit, max(vlo, raw))
        clipped = abs(raw - limited) > 1.0e-9
        out_expected = limited if enabled else 0.0
        sat_expected = vhi if enabled and clipped else 0.0
        metric_expected = vhi * min(1.0, max(0.0, abs(raw - limited) / (vlimit - vlo))) if enabled else 0.0
        out_err = abs(values["out"] - out_expected)
        sat_err = abs(values["sat"] - sat_expected)
        metric_err = abs(values["recovery_metric"] - metric_expected)
        max_err = max(max_err, out_err, sat_err, metric_err)
        out_errors += int(out_err > 0.085)
        sat_errors += int(sat_err > 0.085)
        metric_errors += int(metric_err > 0.085)
        if not enabled:
            clear_errors += sum(err > 0.085 for err in (out_err, sat_err, metric_err))
        saw_low_clip = saw_low_clip or (enabled and raw < vlo)
        saw_high_clip = saw_high_clip or (enabled and raw > vlimit)
        saw_linear = saw_linear or (enabled and vlo < raw < vlimit)
        saw_disabled = saw_disabled or (not enabled)
        saw_metric = saw_metric or metric_expected > 0.05
        checked += 1
    if checked < 10:
        return False, f"insufficient_saturation_limiter_samples={checked}"
    if not (saw_low_clip and saw_high_clip and saw_linear and saw_disabled and saw_metric):
        return False, "insufficient_saturation_limiter_coverage"
    ok = max_err <= 0.085
    detail = f"samples={checked} max_err={max_err:.4f}"
    if not ok:
        detail = f"saturation_limiter_error={max_err:.4f}"
    return ok, (
        f"{detail}; P_CLAMP_THE_ENABLED_INPUT_BETWEEN_THE mismatch_count={out_errors}; "
        f"P_DRIVE_A_SATURATION_FLAG_WHEN_EITHER mismatch_count={sat_errors}; "
        f"P_CLEAR_OUTPUT_FLAG_AND_RECOVERY_METRIC mismatch_count={clear_errors}; "
        f"P_COMPUTE_LIMITED_CLAMP_V_VIN_VLO mismatch_count={out_errors}; "
        f"P_DRIVE_SAT_VHI_WHEN_ENABLED_AND mismatch_count={sat_errors}; "
        f"P_DRIVE_THE_RECOVERY_METRIC_AS mismatch_count={metric_errors}"
    )

CHECKER_ID = "v4_269_saturation_recovery_limiter"
CHECKER: Checker = bind_properties(check_v3_373_saturation_recovery_limiter, (
    "P_CLAMP_THE_ENABLED_INPUT_BETWEEN_THE",
    "P_DRIVE_A_SATURATION_FLAG_WHEN_EITHER",
    "P_CLEAR_OUTPUT_FLAG_AND_RECOVERY_METRIC",
    "P_COMPUTE_LIMITED_CLAMP_V_VIN_VLO",
    "P_DRIVE_SAT_VHI_WHEN_ENABLED_AND",
    "P_DRIVE_THE_RECOVERY_METRIC_AS",
))
