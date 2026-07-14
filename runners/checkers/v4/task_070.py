"""Task-specific checker for canonical v4 DUT 070."""
from __future__ import annotations

from checkers.api import Checker
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

def check_deterministic_jittered_clock(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "jitter_en", "clk_out", *{f"seed{i}" for i in range(8)}}
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0].keys())) if rows else sorted(required)
        return False, "missing_columns=" + ",".join(missing[:12])
    out_min = min(row["clk_out"] for row in rows)
    out_max = max(row["clk_out"] for row in rows)
    swing = out_max - out_min
    if swing < 0.10:
        return False, (
            f"jitter_clock_edges observed=0 expected>=16 window=full_trace "
            f"output_range={out_min:.3f}..{out_max:.3f}"
        )

    edge_threshold = out_min + 0.5 * swing
    transitions: list[float] = []
    last_high = rows[0]["clk_out"] > edge_threshold
    for row in rows[1:]:
        high = row["clk_out"] > edge_threshold
        if high != last_high:
            transitions.append(row["time"])
        last_high = high
    if len(transitions) < 16:
        return False, f"jitter_clock_edges observed={len(transitions)} expected>=16 window=full_trace"
    if out_min < -0.05 or out_min > 0.15 or out_max < 0.72 or out_max > 1.02:
        return False, (
            f"jitter_clock_level observed=low:{out_min:.3f},high:{out_max:.3f} "
            "expected=low:0.0,high:0.9 window=full_trace"
        )

    half_periods = [(b - a) / 1e-9 for a, b in zip(transitions, transitions[1:])]
    enabled_periods: list[tuple[int, float]] = []
    disabled_periods: list[tuple[int, float]] = []
    formula_failures: list[str] = []
    for index, (edge_t, half_period_ns) in enumerate(zip(transitions, half_periods), start=1):
        enabled = sample_signal_at(rows, "jitter_en", edge_t)
        if enabled is None:
            continue
        if enabled <= 0.45:
            disabled_periods.append((index, half_period_ns))
            continue
        enabled_periods.append((index, half_period_ns))
        seed = 0
        for bit in range(8):
            value = sample_signal_at(rows, f"seed{bit}", edge_t)
            if value is not None and value > 0.45:
                seed |= 1 << bit
        expected_ns = 10.0 + (((seed + 3 * index) % 5) - 2) * 0.8
        if abs(half_period_ns - expected_ns) > 0.18:
            formula_failures.append(
                f"jitter_clock_formula observed={half_period_ns:.3f}ns expected={expected_ns:.3f}ns "
                f"window=edge{index} seed={seed}"
            )

    bounds_failures = [
        (index, period) for index, period in enabled_periods if period < 8.22 or period > 11.78
    ]
    if bounds_failures:
        index, period = bounds_failures[0]
        return False, (
            f"jitter_clock_bounds observed={period:.3f}ns expected=8.4..11.6ns "
            f"window=edge{index} mismatch_count={len(bounds_failures)}"
        )
    nominal_failures = [
        (index, period) for index, period in disabled_periods if abs(period - 10.0) > 0.18
    ]
    if nominal_failures:
        index, period = nominal_failures[0]
        return False, (
            f"jitter_clock_nominal observed={period:.3f}ns expected=10.000ns "
            f"window=edge{index} mismatch_count={len(nominal_failures)}"
        )
    unique_enabled = {round(period, 1) for _, period in enabled_periods}
    if len(enabled_periods) >= 5 and len(unique_enabled) < 3:
        return False, (
            f"jitter_clock_modulation observed=unique_half_periods:{sorted(unique_enabled)} "
            "expected>=3 window=jitter_en_high"
        )

    repeat_failures: list[tuple[int, float, float]] = []
    enabled_by_index = {index: period for index, period in enabled_periods}
    for index, period in enabled_periods:
        repeated = enabled_by_index.get(index + 5)
        if repeated is not None and abs(repeated - period) > 0.18:
            repeat_failures.append((index, period, repeated))
    if repeat_failures:
        index, first, repeated = repeat_failures[0]
        return False, (
            f"jitter_clock_repeatability observed=edge{index}:{first:.3f}ns,edge{index + 5}:{repeated:.3f}ns "
            f"expected=equal window=constant_seed mismatch_count={len(repeat_failures)}"
        )
    if formula_failures:
        return False, " ".join(formula_failures[:5])
    return True, (
        f"jitter_clock_contract_pass transitions={len(transitions)} enabled_intervals={len(enabled_periods)} "
        f"disabled_intervals={len(disabled_periods)} output_range={out_min:.3f}..{out_max:.3f}"
    )

CHECKER_ID = "v4_070_jittered_clock_source_deterministic"
CHECKER: Checker = check_deterministic_jittered_clock
