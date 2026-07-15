"""Task-specific checker for canonical v4 DUT 014."""
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

def check_segmented_dac(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows or "time" not in rows[0] or "aout" not in rows[0]:
        return False, "missing time/aout"
    sample_times_ns = [15.0, 45.0, 75.0, 105.0, 135.0]
    expected = [0.0, 0.06, 0.12, 0.42, 0.72]
    observed: list[float] = []
    for t_ns in sample_times_ns:
        value = sample_signal(rows, "aout", t_ns * 1e-9)
        if value is None:
            return False, f"missing_sample_at={t_ns:g}ns"
        observed.append(value)
    level_ok = all(abs(got - want) <= 0.02 for got, want in zip(observed, expected))
    monotonic = all(b >= a - 1e-3 for a, b in zip(observed, observed[1:]))
    ok = level_ok and monotonic
    obs_text = ",".join(f"{value:.3f}" for value in observed)
    exp_text = ",".join(f"{value:.3f}" for value in expected)
    return ok, f"dac_levels={obs_text} expected={exp_text} monotonic={monotonic}"

CHECKER_ID = "v4_014_segmented_dac"
CHECKER: Checker = check_segmented_dac
