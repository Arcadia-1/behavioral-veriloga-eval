"""Task-specific checker for canonical v4 DUT 007."""
from __future__ import annotations

from ..api import Checker
def sample_signal(rows: list[dict[str, float]], signal: str, time_s: float) -> float | None:
    if not rows or signal not in rows[0] or "time" not in rows[0]:
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
    return rows[-1].get(signal)

def check_first_order_lowpass(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin", "vout"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/vin/vout"

    step_times = [
        current["time"]
        for previous, current in zip(rows, rows[1:])
        if previous["vin"] < 0.4 <= current["vin"]
    ]
    if len(step_times) != 1:
        return False, f"input_step_count={len(step_times)}"
    step_time = step_times[0]
    end_time = rows[-1]["time"]
    response_window = end_time - step_time
    vin_pre = sample_signal(rows, "vin", step_time - 0.05 * response_window)
    vin_post = sample_signal(rows, "vin", step_time + 0.10 * response_window)
    vin_late = sample_signal(rows, "vin", step_time + 0.90 * response_window)
    if vin_pre is None or vin_post is None or vin_late is None:
        return False, "missing_vin_step_samples"
    input_step = vin_pre < 0.10 and vin_post > 0.72 and vin_late > 0.72

    sample_times = [step_time + fraction * response_window for fraction in (0.08, 0.22, 0.50, 0.92)]
    samples: list[float] = []
    for time_s in sample_times:
        value = sample_signal(rows, "vout", time_s)
        if value is None:
            return False, f"missing_sample_at={time_s * 1e9:.3f}ns"
        samples.append(value)

    monotonic = samples[0] < samples[1] < samples[2] <= samples[3] + 0.03
    response_fast_enough = samples[1] > 0.55 and samples[2] > 0.70 and samples[3] > 0.76
    not_instant = samples[0] < 0.45
    post_rows = [
        r
        for r in rows
        if r.get("time", 0.0) >= step_time and "vout" in r and "vin" in r
    ]
    min_vout = min((r["vout"] for r in post_rows), default=float("nan"))
    max_vout = max((r["vout"] for r in post_rows), default=float("nan"))
    input_ceiling = max((r["vin"] for r in post_rows), default=float("nan"))
    bounded = bool(post_rows) and -0.03 <= min_vout <= max_vout <= input_ceiling + 0.03
    ok = input_step and monotonic and response_fast_enough and not_instant and bounded
    values = ",".join(f"{value:.3f}" for value in samples)
    note = (
        f"lowpass_samples={values} input_step={input_step} monotonic={monotonic} "
        f"response_fast_enough={response_fast_enough} not_instant={not_instant} "
        f"bounded={bounded} input_ceiling={input_ceiling:.6g} max_vout={max_vout:.6g}"
    )
    if not bounded:
        note += (
            "; first_mismatch=P_STEP_MONOTONICITY signal=vout "
            f"time={end_time:.6e} expected<={input_ceiling + 0.03:.6g} "
            f"observed={max_vout:.6g} tolerance=0.03"
        )
    return ok, note

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

def check_v4_first_order_lowpass(rows: list[dict[str, float]]) -> tuple[bool, str]:
    base_ok, base_note = check_vbm1_first_order_lowpass(rows)
    required = {"time", "vin", "vout"}
    if not rows or not required.issubset(rows[0]):
        return False, base_note

    step_times = [
        current["time"]
        for previous, current in zip(rows, rows[1:])
        if previous["vin"] < 0.4 <= current["vin"]
    ]
    if len(step_times) != 1:
        return False, base_note
    start_time = rows[0]["time"]
    step_time = step_times[0]
    initial_samples = [
        sample_signal_at(rows, "vout", start_time + fraction * (step_time - start_time))
        for fraction in (0.25, 0.75)
    ]
    initial_ok = all(value is not None and abs(value) <= 0.02 for value in initial_samples)
    return base_ok and initial_ok, f"{base_note} initial_samples={initial_samples} initial_ok={initial_ok}"

check_vbm1_first_order_lowpass = check_first_order_lowpass

CHECKER_ID = "v4_007_first_order_lowpass"
CHECKER: Checker = check_v4_first_order_lowpass
