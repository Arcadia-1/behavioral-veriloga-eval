"""Task-specific checker for canonical v4 DUT 070."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import diagnostic, pass_note, require_signals, sample


PROPERTIES = (
    "P_NOMINAL_CLOCK",
    "P_SEED_DECODE",
    "P_EDGE_MODULATION",
    "P_REPEATABILITY",
    "P_TIMING_BOUNDS",
    "P_OUTPUT_LEVELS",
)

def check_deterministic_jittered_clock(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "jitter_en", "clk_out", *{f"seed{i}" for i in range(8)}}
    invalid = require_signals(rows, required, "P_NOMINAL_CLOCK")
    if invalid:
        return False, invalid
    out_min = min(row["clk_out"] for row in rows)
    out_max = max(row["clk_out"] for row in rows)
    swing = out_max - out_min
    if swing < 0.10:
        return False, diagnostic(
            "P_OUTPUT_LEVELS",
            "semantic_mismatch",
            expected="clk_out_swing>=0.10",
            observed=f"clk_out_range={out_min:.3f}..{out_max:.3f}",
            event="full_trace",
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
        return False, diagnostic(
            "P_NOMINAL_CLOCK",
            "insufficient_coverage",
            expected="transitions>=16",
            observed=f"transitions={len(transitions)}",
            event="full_trace",
        )
    if out_min < -0.05 or out_min > 0.15 or out_max < 0.72 or out_max > 1.02:
        return False, diagnostic(
            "P_OUTPUT_LEVELS",
            "semantic_mismatch",
            expected="low=0.0,high=0.9",
            observed=f"low={out_min:.3f},high={out_max:.3f}",
            event="full_trace",
        )

    half_periods = [(b - a) / 1e-9 for a, b in zip(transitions, transitions[1:])]
    enabled_periods: list[tuple[int, float]] = []
    disabled_periods: list[tuple[int, float]] = []
    formula_failures: list[str] = []
    for index, (edge_t, half_period_ns) in enumerate(zip(transitions, half_periods), start=1):
        enabled = sample(rows, "jitter_en", edge_t)
        if enabled is None:
            continue
        if enabled <= 0.45:
            disabled_periods.append((index, half_period_ns))
            continue
        enabled_periods.append((index, half_period_ns))
        seed = 0
        for bit in range(8):
            value = sample(rows, f"seed{bit}", edge_t)
            if value is not None and value > 0.45:
                seed |= 1 << bit
        expected_ns = 10.0 + (((seed + 3 * index) % 5) - 2) * 0.8
        if abs(half_period_ns - expected_ns) > 0.18:
            formula_failures.append(
                diagnostic(
                    "P_EDGE_MODULATION",
                    "semantic_mismatch",
                    expected=f"half_period_ns={expected_ns:.3f}",
                    observed=f"half_period_ns={half_period_ns:.3f},seed={seed}",
                    event=f"edge{index}",
                )
            )

    bounds_failures = [
        (index, period) for index, period in enabled_periods if period < 8.22 or period > 11.78
    ]
    if bounds_failures:
        index, period = bounds_failures[0]
        return False, diagnostic(
            "P_TIMING_BOUNDS",
            "semantic_mismatch",
            expected="half_period_ns=8.4..11.6",
            observed=f"half_period_ns={period:.3f},mismatch_count={len(bounds_failures)}",
            event=f"edge{index}",
        )
    nominal_failures = [
        (index, period) for index, period in disabled_periods if abs(period - 10.0) > 0.18
    ]
    if nominal_failures:
        index, period = nominal_failures[0]
        return False, diagnostic(
            "P_NOMINAL_CLOCK",
            "semantic_mismatch",
            expected="half_period_ns=10.000",
            observed=f"half_period_ns={period:.3f},mismatch_count={len(nominal_failures)}",
            event=f"edge{index}",
        )
    unique_enabled = {round(period, 1) for _, period in enabled_periods}
    if len(enabled_periods) >= 5 and len(unique_enabled) < 3:
        return False, diagnostic(
            "P_EDGE_MODULATION",
            "semantic_mismatch",
            expected="unique_enabled_half_periods>=3",
            observed=f"unique_enabled_half_periods={sorted(unique_enabled)}",
            event="jitter_en_high",
        )

    repeat_failures: list[tuple[int, float, float]] = []
    enabled_by_index = {index: period for index, period in enabled_periods}
    for index, period in enabled_periods:
        repeated = enabled_by_index.get(index + 5)
        if repeated is not None and abs(repeated - period) > 0.18:
            repeat_failures.append((index, period, repeated))
    if repeat_failures:
        index, first, repeated = repeat_failures[0]
        return False, diagnostic(
            "P_REPEATABILITY",
            "semantic_mismatch",
            expected="edge_i_equals_edge_i_plus_5",
            observed=f"edge{index}={first:.3f}ns,edge{index + 5}={repeated:.3f}ns,mismatch_count={len(repeat_failures)}",
            event="constant_seed",
        )
    if formula_failures:
        return False, " ".join(formula_failures[:5])
    return True, pass_note(PROPERTIES, (
        f"jitter_clock_contract_pass transitions={len(transitions)} enabled_intervals={len(enabled_periods)} "
        f"disabled_intervals={len(disabled_periods)} output_range={out_min:.3f}..{out_max:.3f}"
    ))

CHECKER_ID = "v4_070_jittered_clock_source_deterministic"
CHECKER: Checker = check_deterministic_jittered_clock
