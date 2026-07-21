"""Task-specific checker for canonical v4 DUT 068."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import crossings, diagnostic, pass_note, require_signals


PROPERTIES = (
    "P_PERIOD",
    "P_DUTY_CYCLE",
    "P_PHASE_OFFSETS",
    "P_PHASE_STABILITY",
    "P_OUTPUT_LEVELS",
)

def check_multiphase_clock_generator_4ph(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vss", "clk0", "clk90", "clk180", "clk270"}
    invalid = require_signals(rows, required, "P_PERIOD")
    if invalid:
        return False, invalid
    clocks = ("clk0", "clk90", "clk180", "clk270")
    relative_rows = [
        {
            **row,
            **{col: row[col] - row["vss"] for col in clocks},
        }
        for row in rows
    ]
    lows = {col: min(row[col] for row in relative_rows) for col in clocks}
    highs = {col: max(row[col] for row in relative_rows) for col in clocks}
    spans = {col: highs[col] - lows[col] for col in clocks}
    reference_low = sum(lows.values()) / len(clocks)
    reference_high = sum(highs.values()) / len(clocks)
    reference_span = reference_high - reference_low
    if reference_span < 0.2 or abs(reference_low) > 0.05:
        return False, diagnostic(
            "P_OUTPUT_LEVELS",
            "invalid_logic_rails",
            expected="common_0V_low_and_parameterized_nontrivial_high_rail",
            observed=f"low={reference_low:.4f},span={reference_span:.4f}",
            event="full_trace",
        )
    rail_tolerance = max(0.04, 0.08 * reference_span)
    rail_errors = [
        f"{col}={lows[col]:.3f}:{highs[col]:.3f}"
        for col in clocks
        if spans[col] < 0.2
        or abs(lows[col] - reference_low) > rail_tolerance
        or abs(highs[col] - reference_high) > rail_tolerance
    ]
    if rail_errors:
        return False, diagnostic(
            "P_OUTPUT_LEVELS",
            "inconsistent_phase_rails",
            expected="all_phases_share_low_and_high_rails",
            observed=";".join(rail_errors),
            event="full_trace",
        )

    threshold = 0.5 * (reference_low + reference_high)
    rises = {
        col: crossings(relative_rows, col, threshold=threshold, direction="rising")
        for col in clocks
    }
    falls = {
        col: crossings(relative_rows, col, threshold=threshold, direction="falling")
        for col in clocks
    }
    if any(len(rises[col]) < 4 or len(falls[col]) < 4 for col in clocks):
        return False, diagnostic(
            "P_PERIOD",
            "insufficient_coverage",
            expected="at_least_four_rising_and_falling_edges_per_phase",
            observed=",".join(
                f"{col}=rise{len(rises[col])}/fall{len(falls[col])}" for col in clocks
            ),
            event="full_trace",
        )

    duty_errors: list[str] = []
    period_errors: list[str] = []
    for col in clocks:
        periods = [b - a for a, b in zip(rises[col], rises[col][1:])]
        for index, period in enumerate(periods):
            if abs(period - 20e-9) > 1.0e-9:
                period_errors.append(f"{col}[{index}]={period * 1e9:.3f}ns")
        for index, rise in enumerate(rises[col][:-1]):
            fall = next((value for value in falls[col] if rise < value < rises[col][index + 1]), None)
            if fall is None:
                duty_errors.append(f"{col}[{index}]=missing_fall")
                continue
            duty = (fall - rise) / (rises[col][index + 1] - rise)
            if abs(duty - 0.5) > 0.08:
                duty_errors.append(f"{col}[{index}]={duty:.3f}")
    if duty_errors:
        return False, diagnostic(
            "P_DUTY_CYCLE",
            "duty_cycle_mismatch",
            expected="duty=0.50+/-0.08",
            observed=";".join(duty_errors[:6]),
            event="complete_clock_cycles",
        )
    if period_errors:
        return False, diagnostic(
            "P_PERIOD",
            "period_mismatch",
            expected="period=20ns+/-1ns",
            observed=";".join(period_errors[:6]),
            event="all_observed_cycles",
        )

    phase_errors: list[str] = []
    for base_index, base in enumerate(rises["clk0"]):
        targets = [base + 5e-9, base + 10e-9, base + 15e-9]
        cols = ["clk90", "clk180", "clk270"]
        for col, target in zip(cols, targets):
            if target > rows[-1]["time"]:
                continue
            error = min(abs(t - target) for t in rises[col])
            if error > 1.0e-9:
                phase_errors.append(f"clk0[{base_index}]->{col}:{error * 1e9:.3f}ns")
    summary = (
        f"edge_counts={ {k: (len(rises[k]), len(falls[k])) for k in clocks} } "
        f"phase_errors={len(phase_errors)} duty_errors=0 period_errors=0 "
        f"common_rails={reference_low:.3f}:{reference_high:.3f}"
    )
    if phase_errors:
        return False, diagnostic(
            "P_PHASE_OFFSETS",
            "semantic_mismatch",
            expected="period=20ns,phase_offsets=5/10/15ns",
            observed=";".join(phase_errors[:6]),
            event="all_observable_clk0_edges",
        )
    return True, pass_note(PROPERTIES, summary)

CHECKER_ID = "v4_068_multiphase_clock_generator_4ph"
CHECKER: Checker = check_multiphase_clock_generator_4ph
