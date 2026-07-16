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


def positive_step_times(rows: list[dict[str, float]]) -> list[float]:
    vin_values = [row["vin"] for row in rows]
    threshold = min(vin_values) + 0.5 * (max(vin_values) - min(vin_values))
    return [
        current["time"]
        for previous, current in zip(rows, rows[1:])
        if previous["vin"] < threshold <= current["vin"]
    ]


def check_first_order_lowpass(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin", "vout"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/vin/vout"

    vin_values = [row["vin"] for row in rows]
    vin_low = min(vin_values)
    vin_high = max(vin_values)
    vin_span = vin_high - vin_low
    if vin_span < 0.20:
        return False, (
            "input_step_too_small; first_mismatch=P_STEP_MONOTONICITY signal=vin "
            f"expected=positive_step>=0.2 observed={vin_span:.6g} tolerance=0"
        )
    step_times = positive_step_times(rows)
    if len(step_times) != 1:
        return False, (
            f"input_step_count={len(step_times)}; "
            "first_mismatch=P_STEP_MONOTONICITY signal=vin "
            f"expected=one_positive_step observed={len(step_times)} tolerance=0"
        )
    step_time = step_times[0]
    start_time = rows[0]["time"]
    end_time = rows[-1]["time"]
    response_window = end_time - step_time
    prehistory = step_time - start_time
    if response_window <= 0.0 or prehistory <= 0.0:
        return False, "missing_vin_step_samples"
    vin_pre = sample_signal(rows, "vin", step_time - 0.25 * prehistory)
    vin_post = sample_signal(rows, "vin", step_time + 0.10 * response_window)
    vin_late = sample_signal(rows, "vin", step_time + 0.90 * response_window)
    if vin_pre is None or vin_post is None or vin_late is None:
        return False, "missing_vin_step_samples"
    step_amplitude = vin_late - vin_pre
    stimulus_tolerance = max(0.02, 0.08 * abs(step_amplitude))
    input_step = (
        step_amplitude >= 0.20
        and vin_post >= vin_pre + 0.80 * step_amplitude
        and abs(vin_late - vin_post) <= stimulus_tolerance
    )

    vout_pre = sample_signal(rows, "vout", step_time - 0.10 * prehistory)
    if vout_pre is None:
        return False, "missing_vout_pre_step_sample"
    response_span = vin_late - vout_pre
    if response_span <= 0.10:
        return False, (
            "response_span_too_small; first_mismatch=P_LOW_PASS_RESPONSE signal=vout "
            f"expected=response_span>0.1 observed={response_span:.6g} tolerance=0"
        )

    sample_times = [step_time + fraction * response_window for fraction in (0.08, 0.22, 0.50, 0.92)]
    samples: list[float] = []
    for time_s in sample_times:
        value = sample_signal(rows, "vout", time_s)
        if value is None:
            return False, f"missing_sample_at={time_s * 1e9:.3f}ns"
        samples.append(value)

    normalized = [(value - vout_pre) / response_span for value in samples]
    normalized_slack = max(0.01, 0.03 / response_span)
    monotonic = (
        normalized[0] < normalized[1] < normalized[2]
        and normalized[2] <= normalized[3] + normalized_slack
    )
    response_fast_enough = normalized[1] > 0.6875 and normalized[2] > 0.875 and normalized[3] > 0.95
    not_instant = normalized[0] < 0.5625
    post_rows = [
        r
        for r in rows
        if r.get("time", 0.0) >= step_time and "vout" in r and "vin" in r
    ]
    min_vout = min((r["vout"] for r in post_rows), default=float("nan"))
    max_vout = max((r["vout"] for r in post_rows), default=float("nan"))
    input_floor = min((r["vin"] for r in post_rows), default=float("nan"))
    input_ceiling = max((r["vin"] for r in post_rows), default=float("nan"))
    bound_tolerance = max(0.03, 0.05 * abs(step_amplitude))
    bounded = (
        bool(post_rows)
        and min(vout_pre, input_floor) - bound_tolerance <= min_vout
        and max_vout <= input_ceiling + bound_tolerance
    )
    ok = input_step and monotonic and response_fast_enough and not_instant and bounded
    values = ",".join(f"{value:.3f}" for value in samples)
    normalized_values = ",".join(f"{value:.3f}" for value in normalized)
    note = (
        f"lowpass_samples={values} normalized_samples={normalized_values} "
        f"step_amplitude={step_amplitude:.6g} input_step={input_step} monotonic={monotonic} "
        f"response_fast_enough={response_fast_enough} not_instant={not_instant} "
        f"bounded={bounded} input_ceiling={input_ceiling:.6g} max_vout={max_vout:.6g}"
    )
    if not input_step:
        note += (
            "; first_mismatch=P_STEP_MONOTONICITY signal=vin "
            f"expected=stable_positive_step>=0.2 observed={step_amplitude:.6g} "
            f"tolerance={stimulus_tolerance:.6g}"
        )
    elif not not_instant:
        note += (
            "; first_mismatch=P_LOW_PASS_RESPONSE signal=vout "
            "expected=normalized_sample0<0.5625 "
            f"observed={normalized[0]:.6g} tolerance=0"
        )
    elif not monotonic:
        note += (
            "; first_mismatch=P_STEP_MONOTONICITY signal=vout "
            f"expected=monotonic_normalized_response observed={normalized_values} "
            f"tolerance={normalized_slack:.6g}"
        )
    elif not response_fast_enough:
        note += (
            "; first_mismatch=P_LOW_PASS_RESPONSE signal=vout "
            "expected=normalized_samples[1:]>0.6875,0.875,0.95 and sample0<0.5625 "
            f"observed={normalized_values} tolerance=0"
        )
    elif not bounded:
        note += (
            "; first_mismatch=P_STEP_MONOTONICITY signal=vout "
            f"time={end_time:.6e} expected<={input_ceiling + bound_tolerance:.6g} "
            f"observed={max_vout:.6g} tolerance={bound_tolerance:.6g}"
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

    step_times = positive_step_times(rows)
    if len(step_times) != 1:
        return False, base_note
    start_time = rows[0]["time"]
    step_time = step_times[0]
    initial_window = min(step_time - start_time, 400e-12)
    initial_samples = [
        sample_signal_at(rows, "vout", start_time + fraction * initial_window)
        for fraction in (0.25, 0.75)
    ]
    initial_ok = all(value is not None and abs(value) <= 0.02 for value in initial_samples)
    note = f"{base_note} initial_samples={initial_samples} initial_ok={initial_ok}"
    if base_ok and not initial_ok:
        note += (
            "; first_mismatch=P_INITIAL_STATE signal=vout "
            f"time={start_time + 0.75 * initial_window:.6e} expected=0 "
            f"observed={initial_samples[-1]} tolerance=0.02"
        )
    return base_ok and initial_ok, note


check_vbm1_first_order_lowpass = check_first_order_lowpass

CHECKER_ID = "v4_007_first_order_lowpass"
CHECKER: Checker = check_v4_first_order_lowpass
