"""Task-specific checker for canonical v4 DUT 236."""
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

def check_v3_285_dual_track_sample_hold(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin", "clk", "vout", "phase"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/vin/clk/vout/phase"

    times = [r["time"] for r in rows]
    last_t = times[-1]
    rising = _threshold_crossings([r["clk"] for r in rows], times, threshold=0.45, direction="rising")
    falling = _threshold_crossings([r["clk"] for r in rows], times, threshold=0.45, direction="falling")
    if len(rising) < 3 or len(falling) < 3:
        return False, f"too_few_clk_edges rise={len(rising)} fall={len(falling)}"

    tick = 0.5e-9
    alpha_in = 0.45
    alpha_out = 0.55
    stage_in = 0.0
    stage_out = 0.0
    ref_errors: list[float] = []
    t = 0.0
    while t <= last_t - 0.20e-9:
        vin = sample_signal_at(rows, "vin", t)
        clk = sample_signal_at(rows, "clk", t)
        if vin is None or clk is None:
            t += tick
            continue
        if clk > 0.45:
            stage_out = stage_out + alpha_out * (stage_in - stage_out)
        else:
            stage_in = stage_in + alpha_in * (vin - stage_in)
        if stage_in < 0.0:
            stage_in = 0.0
        if stage_in > 0.9:
            stage_in = 0.9
        if stage_out < 0.0:
            stage_out = 0.0
        if stage_out > 0.9:
            stage_out = 0.9
        observed = sample_signal_at(rows, "vout", t + 0.15e-9)
        if observed is not None and t > 1.0e-9:
            ref_errors.append(abs(observed - stage_out))
        t += tick

    if len(ref_errors) < 20:
        return False, f"too_few_reference_samples={len(ref_errors)}"
    mean_ref_err = sum(ref_errors) / len(ref_errors)
    max_ref_err = max(ref_errors)

    phase_high_hits = 0
    phase_low_hits = 0
    hold_windows = 0
    hold_failures = 0
    tracking_windows = 0
    for rise_t in rising:
        fall_t = next((ft for ft in falling if ft > rise_t + 0.2e-9), None)
        if fall_t is None:
            continue
        phase_hi = mean_in_window(rows, "phase", rise_t + 0.5e-9, fall_t - 0.5e-9)
        if phase_hi is not None and phase_hi > 0.60:
            phase_high_hits += 1
        out_vals_hi = [r["vout"] for r in rows if rise_t + 0.5e-9 <= r["time"] <= fall_t - 0.5e-9]
        if out_vals_hi and max(out_vals_hi) - min(out_vals_hi) > 0.035:
            tracking_windows += 1

    for fall_t in falling:
        next_rise = next((rt for rt in rising if rt > fall_t + 0.2e-9), None)
        if next_rise is None or next_rise - fall_t <= 1.5e-9:
            continue
        phase_lo = mean_in_window(rows, "phase", fall_t + 0.5e-9, next_rise - 0.5e-9)
        if phase_lo is not None and phase_lo < 0.25:
            phase_low_hits += 1
        out_vals_lo = [r["vout"] for r in rows if fall_t + 0.8e-9 <= r["time"] <= next_rise - 0.8e-9]
        if len(out_vals_lo) >= 3:
            hold_windows += 1
            if max(out_vals_lo) - min(out_vals_lo) > 0.060:
                hold_failures += 1

    ok = (
        mean_ref_err <= 0.035
        and max_ref_err <= 0.12
        and phase_high_hits >= 3
        and phase_low_hits >= 2
        and tracking_windows >= 2
        and hold_windows >= 2
        and hold_failures == 0
    )
    return ok, (
        f"dual_track_sample_hold mean_ref_err={mean_ref_err:.3f} max_ref_err={max_ref_err:.3f} "
        f"phase_hi={phase_high_hits} phase_lo={phase_low_hits} "
        f"tracking_windows={tracking_windows} hold_windows={hold_windows} "
        f"hold_failures={hold_failures}"
    )

CHECKER_ID = "v4_236_dual_track_sample_hold"
CHECKER: Checker = check_v3_285_dual_track_sample_hold
