"""Task-specific checker for canonical v4 DUT 071."""
from __future__ import annotations

from ..api import Checker
def _threshold_crossings(
    values: list[float],
    times: list[float],
    *,
    threshold: float = 0.0,
    direction: str,
) -> list[float]:
    edges: list[float] = []
    for idx in range(1, len(values)):
        v0 = values[idx - 1]
        v1 = values[idx]
        if direction == "rising":
            hit = v0 <= threshold < v1
        elif direction == "falling":
            hit = v0 >= threshold > v1
        else:
            raise ValueError(f"unsupported direction={direction!r}")
        if not hit:
            continue
        t0 = times[idx - 1]
        t1 = times[idx]
        if v1 == v0:
            edges.append(t1)
        else:
            alpha = (threshold - v0) / (v1 - v0)
            edges.append(t0 + alpha * (t1 - t0))
    return edges

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

def mean_in_window(rows: list[dict[str, float]], key: str, start: float, stop: float) -> float | None:
    values = [r[key] for r in rows if start <= r["time"] <= stop and key in r]
    if not values:
        return None
    return sum(values) / len(values)

def check_acquisition_limited_sample_hold(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "sample", "rst", "vin", "vout", "metric"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/sample/rst/vin/vout/metric"

    times = [r["time"] for r in rows]
    sample_vals = [r["sample"] for r in rows]
    rising = _threshold_crossings(sample_vals, times, threshold=0.45, direction="rising")
    falling = _threshold_crossings(sample_vals, times, threshold=0.45, direction="falling")
    if len(rising) < 3 or len(falling) < 3:
        return False, f"too_few_sample_windows rise={len(rising)} fall={len(falling)}"

    reset_rows = [r for r in rows if r["rst"] > 0.45]
    if not reset_rows:
        return False, "missing_reset_window"
    reset_mean = sum(r["vout"] for r in reset_rows) / len(reset_rows)
    if abs(reset_mean - 0.45) > 0.08:
        return False, f"acq_hold_reset_out={reset_mean:.3f}"

    finite_windows = 0
    settling_windows = 0
    metric_track_hits = 0
    metric_hold_hits = 0
    hold_windows = 0
    hold_failures = 0
    max_late_error = 0.0
    for idx, rise_t in enumerate(rising):
        fall_t = next((t for t in falling if t > rise_t + 0.2e-9), None)
        if fall_t is None:
            continue
        if mean_in_window(rows, "rst", rise_t + 0.2e-9, fall_t - 0.2e-9) is None:
            continue
        duration = fall_t - rise_t
        if duration < 1.5e-9:
            continue
        early_t = rise_t + min(1.2e-9, duration * 0.30)
        late_t = fall_t - min(0.6e-9, duration * 0.20)
        early_vin = sample_signal_at(rows, "vin", early_t)
        early_vout = sample_signal_at(rows, "vout", early_t)
        late_vin = sample_signal_at(rows, "vin", late_t)
        late_vout = sample_signal_at(rows, "vout", late_t)
        track_metric = mean_in_window(rows, "metric", early_t, late_t)
        if None in (early_vin, early_vout, late_vin, late_vout, track_metric):
            return False, f"acq_hold_missing_window_at={rise_t:.3e}"
        assert early_vin is not None and early_vout is not None
        assert late_vin is not None and late_vout is not None and track_metric is not None
        early_error = abs(early_vout - early_vin)
        late_error = abs(late_vout - late_vin)
        max_late_error = max(max_late_error, late_error)
        if early_error > 0.07:
            finite_windows += 1
        if late_error + 0.02 < early_error:
            settling_windows += 1
        if track_metric > 0.60:
            metric_track_hits += 1

        next_rise = rising[idx + 1] if idx + 1 < len(rising) else None
        if next_rise is not None and next_rise - fall_t > 1.5e-9:
            hold_start = fall_t + 0.8e-9
            hold_stop = next_rise - 0.8e-9
            hold_vals = [r["vout"] for r in rows if hold_start <= r["time"] <= hold_stop]
            hold_metric = mean_in_window(rows, "metric", hold_start, hold_stop)
            if len(hold_vals) >= 3 and hold_metric is not None:
                hold_windows += 1
                if max(hold_vals) - min(hold_vals) > 0.055:
                    hold_failures += 1
                if hold_metric < 0.25:
                    metric_hold_hits += 1

    ok = (
        finite_windows >= 1
        and settling_windows >= 2
        and hold_windows >= 2
        and hold_failures == 0
        and metric_track_hits >= 2
        and metric_hold_hits >= 2
        and max_late_error <= 0.14
    )
    return ok, (
        "acquisition_limited_sample_hold "
        f"finite_windows={finite_windows} settling_windows={settling_windows} "
        f"hold_windows={hold_windows} hold_failures={hold_failures} "
        f"metric={metric_track_hits}/{metric_hold_hits} "
        f"max_late_error={max_late_error:.3f}"
    )

CHECKER_ID = "v4_071_acquisition_limited_sample_and_hold"
CHECKER: Checker = check_acquisition_limited_sample_hold
