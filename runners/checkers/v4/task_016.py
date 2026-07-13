"""Task-specific checker for canonical v4 DUT 016."""
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

def check_slew_rate_limiter(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin", "vout"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/vin/vout"

    vin_pre = sample_signal(rows, "vin", 10.0e-9)
    vin_high = sample_signal(rows, "vin", 80.0e-9)
    vin_low = sample_signal(rows, "vin", 150.0e-9)
    if vin_pre is None or vin_high is None or vin_low is None:
        return False, "missing_vin_step_samples"
    input_sequence = vin_pre < 0.10 and vin_high > 0.72 and 0.05 <= vin_low <= 0.18

    sample_times_ns = [40.0, 80.0, 100.0, 120.0, 150.0]
    samples: list[float] = []
    for t_ns in sample_times_ns:
        value = sample_signal(rows, "vout", t_ns * 1e-9)
        if value is None:
            return False, f"missing_sample_at={t_ns:g}ns"
        samples.append(value)

    rising_limited = 0.20 <= samples[0] <= 0.40
    high_reached = samples[1] > 0.74
    falling_limited = samples[2] > samples[3] > samples[4] and samples[2] > 0.65 and 0.34 <= samples[3] <= 0.58
    low_reached = abs(samples[4] - 0.10) <= 0.05
    not_passthrough = samples[0] < vin_high - 0.30 and samples[2] > vin_low + 0.45
    ok = input_sequence and rising_limited and high_reached and falling_limited and low_reached and not_passthrough
    values = ",".join(f"{value:.3f}" for value in samples)
    return ok, (
        f"slew_samples={values} input_sequence={input_sequence} "
        f"rising_limited={rising_limited} high_reached={high_reached} "
        f"falling_limited={falling_limited} low_reached={low_reached} "
        f"not_passthrough={not_passthrough}"
    )

CHECKER_ID = "v4_016_slew_rate_limiter"
CHECKER: Checker = check_slew_rate_limiter
