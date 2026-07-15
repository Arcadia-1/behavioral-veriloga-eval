"""Task-specific checker for canonical v4 DUT 009."""
from __future__ import annotations

from ..api import Checker
def rising_edges(values: list[float], times: list[float], threshold: float = 0.45) -> list[float]:
    edges: list[float] = []
    for i in range(1, len(values)):
        if values[i - 1] < threshold <= values[i]:
            edges.append(times[i])
    return edges

def check_v3_009_lock_detector(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "ref_clk", "fb_clk", "rst_n", "lock"}
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0].keys())) if rows else sorted(required)
        return False, "missing_columns=" + ",".join(missing)

    times = [r["time"] for r in rows]
    ref_edges = rising_edges([r["ref_clk"] for r in rows], times, threshold=0.45)
    fb_edges = rising_edges([r["fb_clk"] for r in rows], times, threshold=0.45)
    if len(ref_edges) < 8 or len(fb_edges) < 8:
        return False, f"too_few_edges ref={len(ref_edges)} fb={len(fb_edges)}"

    events: list[tuple[float, bool, bool]] = []
    for ref_t in ref_edges:
        rst = sample_signal_at(rows, "rst_n", ref_t)
        if rst is None or rst <= 0.45:
            continue
        nearest_fb = min((abs(fb_t - ref_t) for fb_t in fb_edges), default=1.0)
        aligned = nearest_fb <= 2.0e-9
        lock_after = sample_signal_at(rows, "lock", ref_t + 0.8e-9)
        events.append((ref_t, aligned, bool(lock_after is not None and lock_after > 0.45)))

    streak = 0
    good_lock_after_three = 0
    early_locks = 0
    mismatch_clears = 0
    mismatch_failures = 0
    for ref_t, aligned, lock_high in events:
        if aligned:
            streak += 1
            if streak >= 3 and lock_high:
                good_lock_after_three += 1
            if streak < 3 and lock_high:
                early_locks += 1
        else:
            if lock_high:
                mismatch_failures += 1
            else:
                mismatch_clears += 1
            streak = 0

    reset_sample_times = (1e-9, 58e-9, 59e-9, 95e-9, 99e-9, 102e-9)
    reset_samples = [sample_signal_at(rows, "lock", t) for t in reset_sample_times]
    reset_low = all(value is not None and value < 0.45 for value in reset_samples)
    final_lock = sample_signal_at(rows, "lock", max(times) - 1e-9)
    final_lock_low = final_lock is not None and final_lock < 0.45

    ok = (
        reset_low
        and early_locks == 0
        and mismatch_failures == 0
        and mismatch_clears >= 1
        and good_lock_after_three >= 2
        and final_lock_low
    )
    aligned_count = sum(1 for _, aligned, _ in events if aligned)
    mismatch_count = sum(1 for _, aligned, _ in events if not aligned)
    return ok, (
        f"events={len(events)} aligned={aligned_count} mismatch={mismatch_count} "
        f"good_lock_after_three={good_lock_after_three} early_locks={early_locks} "
        f"mismatch_clears={mismatch_clears} mismatch_failures={mismatch_failures} "
        f"reset_low={reset_low} final_lock_low={final_lock_low}"
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

CHECKER_ID = "v4_009_lock_detector"
CHECKER: Checker = check_v3_009_lock_detector
