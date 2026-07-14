"""Task-specific checker for canonical v4 DUT 039."""
from __future__ import annotations

from checkers.api import Checker
def _sample_vector_at(times: list[float], values: list[float], time_s: float) -> float | None:
    if not times or not values or len(times) != len(values):
        return None
    first_time = times[0]
    last_time = times[-1]
    if time_s < first_time or time_s > last_time:
        return None
    if time_s == first_time:
        return values[0]
    for idx in range(1, len(times)):
        t0 = times[idx - 1]
        t1 = times[idx]
        if t0 <= time_s <= t1:
            if t1 == t0:
                return values[idx]
            alpha = (time_s - t0) / (t1 - t0)
            return values[idx - 1] + alpha * (values[idx] - values[idx - 1])
    return None

def _check_cmp_delay_vectors(times: list[float], out_p: list[float]) -> tuple[bool, str]:
    phases = [
        (0.0e-9, 4.0e-9, 10e-3),
        (4.0e-9, 8.0e-9, 1e-3),
        (8.0e-9, 12.0e-9, 0.1e-3),
        (12.0e-9, 16.0e-9, 0.01e-3),
    ]
    threshold = 0.45
    clk_rise_offset = 0.1e-9

    delays_ns: list[float] = []
    missing_high: list[str] = []
    for start_t, end_t, diff_v in phases:
        phase_samples = [value for t, value in zip(times, out_p) if start_t <= t < end_t]
        if not phase_samples or max(phase_samples) < threshold:
            missing_high.append(f"{diff_v * 1e3:.2g}mV")
            continue

        search_start = start_t + clk_rise_offset
        pre_sample = _sample_vector_at(times, out_p, search_start - 20e-12)
        if pre_sample is None or pre_sample > threshold:
            return False, f"out_p_not_low_before_clock diff={diff_v * 1e3:.2g}mV"

        crossing_t = None
        for idx, t in enumerate(times):
            if t < search_start or t >= min(end_t, search_start + 3.0e-9):
                continue
            prev = out_p[idx - 1] if idx > 0 else out_p[idx]
            if prev <= threshold and out_p[idx] > threshold:
                crossing_t = t
                break
        if crossing_t is None:
            return False, f"missing_threshold_crossing diff={diff_v * 1e3:.2g}mV"
        delays_ns.append((crossing_t - search_start) * 1e9)

    if missing_high:
        return False, f"out_p_never_high phases={','.join(missing_high)}"
    if len(delays_ns) != len(phases):
        return False, f"insufficient_delay_measurements count={len(delays_ns)}"

    monotonic = all(delays_ns[i] <= delays_ns[i + 1] + 0.015 for i in range(len(delays_ns) - 1))
    total_growth_ns = delays_ns[-1] - delays_ns[0]
    ok = monotonic and total_growth_ns >= 0.015
    return ok, (
        f"delays_ns={[round(v, 3) for v in delays_ns]} "
        f"monotonic={monotonic} total_growth_ns={total_growth_ns:.3f}"
    )

def check_cmp_delay(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "vinp", "vinn", "out_p", "out_n", "delay_ps"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/clk/vinp/vinn/out_p/out_n/delay_ps"

    times = [r["time"] for r in rows]
    out_p = [r["out_p"] for r in rows]
    return _check_cmp_delay_vectors(times, out_p)

CHECKER_ID = "v4_039_propagation_delay_comparator"
CHECKER: Checker = check_cmp_delay
