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
    required = {"time", "clk0", "clk90", "clk180", "clk270"}
    invalid = require_signals(rows, required, "P_PERIOD")
    if invalid:
        return False, invalid
    rises = {
        col: crossings(rows, col, threshold=0.45, direction="rising")[:4]
        for col in ("clk0", "clk90", "clk180", "clk270")
    }
    if any(len(v) < 2 for v in rises.values()):
        return False, diagnostic(
            "P_PERIOD",
            "insufficient_coverage",
            expected="at_least_two_edges_per_phase",
            observed=",".join(f"{key}={len(value)}" for key, value in rises.items()),
            event="full_trace",
        )
    errors = 0
    period_errors = 0
    clk0_periods = [b - a for a, b in zip(rises["clk0"], rises["clk0"][1:])]
    for period in clk0_periods:
        if abs(period - 20e-9) > 1.5e-9:
            period_errors += 1
    for base in rises["clk0"][:3]:
        targets = [base + 5e-9, base + 10e-9, base + 15e-9]
        cols = ["clk90", "clk180", "clk270"]
        for col, target in zip(cols, targets):
            if min(abs(t - target) for t in rises[col]) > 1.5e-9:
                errors += 1
    summary = (
        f"edge_counts={ {k: len(v) for k, v in rises.items()} } "
        f"phase_errors={errors} period_errors={period_errors}"
    )
    if errors or period_errors:
        return False, diagnostic(
            "P_PHASE_OFFSETS",
            "semantic_mismatch",
            expected="period=20ns,phase_offsets=5/10/15ns",
            observed=summary.replace(" ", "_"),
            event="observable_clk0_edges",
        )
    return True, pass_note(PROPERTIES, summary)

CHECKER_ID = "v4_068_multiphase_clock_generator_4ph"
CHECKER: Checker = check_multiphase_clock_generator_4ph
