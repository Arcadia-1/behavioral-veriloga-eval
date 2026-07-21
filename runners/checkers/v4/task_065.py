"""Task-specific checker for canonical v4 DUT 065."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import crossings, diagnostic, pass_note, require_signals


PROPERTIES = (
    "P_ENABLED_HIGH",
    "P_DISABLED_LOW",
    "P_ENABLE_GATING",
    "P_OUTPUT_LEVELS",
)

def check_enable_gated_clock_pulse(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "en", "pulse"}
    invalid = require_signals(rows, required, "P_ENABLE_GATING")
    if invalid:
        return False, invalid
    errors = 0
    level_errors = 0
    saw_high = False
    saw_blocked = False
    edge_times = (
        crossings(rows, "clk", threshold=0.45, direction="rising")
        + crossings(rows, "clk", threshold=0.45, direction="falling")
        + crossings(rows, "en", threshold=0.45, direction="rising")
        + crossings(rows, "en", threshold=0.45, direction="falling")
    )
    for row in rows[:: max(1, len(rows) // 400)]:
        if any(abs(row["time"] - t) < 0.3e-9 for t in edge_times):
            continue
        if 0.1 < row["clk"] < 0.8 or 0.1 < row["en"] < 0.8:
            continue
        expected = row["en"] > 0.45 and row["clk"] > 0.45
        actual = row["pulse"] > 0.45
        if actual != expected:
            errors += 1
        if expected:
            level_errors += int(not 0.75 <= row["pulse"] <= 1.05)
        else:
            level_errors += int(abs(row["pulse"]) > 0.15)
        saw_high = saw_high or actual
        saw_blocked = saw_blocked or (row["clk"] > 0.45 and row["en"] <= 0.45 and not actual)
    summary = (
        f"errors={errors} level_errors={level_errors} "
        f"saw_high={saw_high} saw_blocked={saw_blocked}"
    )
    ok = errors == 0 and level_errors == 0 and saw_high and saw_blocked
    if not ok:
        return False, diagnostic(
            "P_OUTPUT_LEVELS" if level_errors else "P_ENABLE_GATING",
            "semantic_mismatch",
            expected="pulse_equals_clk_and_enable_at_0.0/0.9V,with_blocked_case",
            observed=summary.replace(" ", "_"),
            event="observable_stable_points",
        )
    return True, pass_note(PROPERTIES, summary)

CHECKER_ID = "v4_065_enable_gated_clock_pulse"
CHECKER: Checker = check_enable_gated_clock_pulse
