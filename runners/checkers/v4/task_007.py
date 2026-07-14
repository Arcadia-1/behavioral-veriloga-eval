"""Task-specific checker for canonical v4 DUT 007."""
from __future__ import annotations

from checkers.api import Checker
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

    vin_pre = sample_signal(rows, "vin", 10.0e-9)
    vin_post = sample_signal(rows, "vin", 30.0e-9)
    vin_late = sample_signal(rows, "vin", 150.0e-9)
    if vin_pre is None or vin_post is None or vin_late is None:
        return False, "missing_vin_step_samples"
    input_step = vin_pre < 0.10 and vin_post > 0.72 and vin_late > 0.72

    sample_times_ns = [30.0, 50.0, 90.0, 150.0]
    samples: list[float] = []
    for t_ns in sample_times_ns:
        value = sample_signal(rows, "vout", t_ns * 1e-9)
        if value is None:
            return False, f"missing_sample_at={t_ns:g}ns"
        samples.append(value)

    monotonic = samples[0] < samples[1] < samples[2] <= samples[3] + 0.03
    response_fast_enough = samples[1] > 0.55 and samples[2] > 0.70 and samples[3] > 0.76
    not_instant = samples[0] < 0.45
    post_rows = [r for r in rows if r.get("time", 0.0) >= 22.0e-9 and "vout" in r]
    bounded = bool(post_rows) and -0.03 <= min(r["vout"] for r in post_rows) <= max(r["vout"] for r in post_rows) <= 0.88
    ok = input_step and monotonic and response_fast_enough and not_instant and bounded
    values = ",".join(f"{value:.3f}" for value in samples)
    return ok, (
        f"lowpass_samples={values} input_step={input_step} monotonic={monotonic} "
        f"response_fast_enough={response_fast_enough} not_instant={not_instant} "
        f"bounded={bounded}"
    )

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

    initial_samples = [sample_signal_at(rows, "vout", time_ns * 1e-9) for time_ns in (1.0, 10.0)]
    initial_ok = all(value is not None and abs(value) <= 0.02 for value in initial_samples)
    end_time = rows[-1]["time"]
    y = 0.0
    update_period = 0.5e-9
    update_time = 0.0
    update_index = 0
    schedule_errors: list[tuple[float, float, float]] = []
    while update_time + 0.45e-9 <= end_time:
        vin = sample_signal_at(rows, "vin", update_time)
        if vin is None:
            break
        y = y + 0.025 * (vin - y)
        if update_index % 10 == 0:
            observed = sample_signal_at(rows, "vout", update_time + 0.45e-9)
            if observed is not None:
                error = abs(observed - y)
                schedule_errors.append((update_time, observed, error))
        update_index += 1
        update_time = update_index * update_period

    failing_schedule = [item for item in schedule_errors if item[2] > 0.035]
    max_schedule_error = max((item[2] for item in schedule_errors), default=float("inf"))
    schedule_ok = len(schedule_errors) >= 20 and not failing_schedule
    return base_ok and initial_ok and schedule_ok, (
        f"{base_note} initial_samples={initial_samples} initial_ok={initial_ok} "
        f"schedule_checks={len(schedule_errors)} schedule_failures={len(failing_schedule)} "
        f"max_schedule_error={max_schedule_error:.4f}"
        + (
            " schedule_detail="
            + ";".join(
                f"{time_s * 1e9:.3f}ns_observed={observed:.3f}_error={error:.4f}"
                for time_s, observed, error in failing_schedule[:5]
            )
            if failing_schedule
            else ""
        )
    )

check_vbm1_first_order_lowpass = check_first_order_lowpass

CHECKER_ID = "v4_007_first_order_lowpass"
CHECKER: Checker = check_v4_first_order_lowpass
