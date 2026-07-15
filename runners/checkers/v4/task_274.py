"""Task-specific checker for canonical v4 DUT 274."""
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

def check_v3_378_rail_normalized_metric_mapper(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "meas", "vdd", "vss", "en", "norm", "valid"}
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0].keys())) if rows else sorted(required)
        return False, "missing_columns=" + ",".join(missing)
    checked = 0
    max_err = 0.0
    saw_vss_offset = saw_enable_low = saw_span_low = saw_span_high = saw_valid = saw_invalid_window = False
    saw_clip_low = saw_clip_high = False
    for time_s in _v3_uniform_sample_times(rows):
        values = _v3_values_at(rows, ("meas", "vdd", "vss", "en", "norm", "valid"), time_s)
        if values is None:
            continue
        span = values["vdd"] - values["vss"]
        local_meas = values["meas"] - values["vss"]
        enabled = values["en"] > 0.45
        if enabled and span >= 0.60:
            norm_expected = 0.9 * min(1.0, max(0.0, local_meas / span))
        else:
            norm_expected = 0.0
        valid_expected = 0.9 if (enabled and 0.60 <= span <= 1.20 and 0.0 <= local_meas <= span) else 0.0
        max_err = max(max_err, abs(values["norm"] - norm_expected), abs(values["valid"] - valid_expected))
        saw_vss_offset = saw_vss_offset or abs(values["vss"]) > 0.025
        saw_enable_low = saw_enable_low or (not enabled)
        saw_span_low = saw_span_low or (span < 0.60)
        saw_span_high = saw_span_high or (span > 1.20)
        saw_valid = saw_valid or valid_expected > 0.45
        saw_invalid_window = saw_invalid_window or (enabled and span >= 0.60 and (local_meas < 0.0 or local_meas > span))
        saw_clip_low = saw_clip_low or (enabled and span >= 0.60 and local_meas < 0.0)
        saw_clip_high = saw_clip_high or (enabled and span >= 0.60 and local_meas > span)
        checked += 1
    if checked < 10:
        return False, f"insufficient_rail_norm_samples={checked}"
    if not (saw_vss_offset and saw_enable_low and saw_span_low and saw_span_high and saw_valid and saw_invalid_window and saw_clip_low and saw_clip_high):
        return False, "insufficient_rail_norm_coverage"
    if max_err > 0.08:
        return False, f"rail_normalized_metric_error={max_err:.4f}"
    return True, f"samples={checked} max_err={max_err:.4f}"

CHECKER_ID = "v4_274_rail_normalized_metric_mapper"
CHECKER: Checker = check_v3_378_rail_normalized_metric_mapper
