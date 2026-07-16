"""Task-specific checker for canonical v4 DUT 112."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import crossings, diagnostic, max_signal_value, pass_note, probe_time, require_signals, sample


PROPERTY_IDS = (
    "P_RISING_EDGE_LATCH",
    "P_OFFSET_DECISION",
    "P_INTEREDGE_HOLD",
    "P_DELAY_AND_SMOOTHING",
)


def check_v3_latched_comparator_delay(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "vinp", "vinn", "dout"}
    missing = require_signals(rows, required, "P_RISING_EDGE_LATCH")
    if missing:
        return False, missing

    vdd = max_signal_value(rows, ["clk", "dout"], default=0.9)
    clk_edges = crossings(rows, "clk", threshold=0.5 * vdd, direction="rising")
    if len(clk_edges) < 4:
        return False, diagnostic(
            "P_RISING_EDGE_LATCH",
            "insufficient_events",
            expected="clk_rising_count>=4",
            observed=f"clk_rising_count={len(clk_edges)}",
            event="clk_rising_set",
        )

    checked = 0
    max_err = 0.0
    decisions: list[int] = []
    for index, edge in enumerate(clk_edges):
        next_edge = clk_edges[index + 1] if index + 1 < len(clk_edges) else None
        probe = probe_time(rows, edge, next_edge, fraction=0.25)
        if probe is None:
            continue
        vinp = sample(rows, "vinp", edge)
        vinn = sample(rows, "vinn", edge)
        dout = sample(rows, "dout", probe)
        if vinp is None or vinn is None or dout is None:
            return False, diagnostic(
                "P_OFFSET_DECISION",
                "missing_sample",
                expected="vinp,vinn,dout",
                observed="unavailable",
                event=f"clk_rising[{index}]",
            )
        expected = vdd if vinp > vinn else 0.0
        decision = 1 if expected > 0.5 * vdd else 0
        decisions.append(decision)
        err = abs(dout - expected)
        max_err = max(max_err, err)
        checked += 1
        if err > 0.08:
            return False, diagnostic(
                "P_DELAY_AND_SMOOTHING",
                "latched_decision_mismatch",
                expected=f"dout={expected:.4f}",
                observed=f"dout={dout:.4f},err={err:.4f}",
                event=f"clk_rising[{index}]",
            )

    if checked < 4:
        return False, diagnostic(
            "P_INTEREDGE_HOLD",
            "insufficient_checks",
            expected="checked>=4",
            observed=f"checked={checked}",
            event="clk_rising_set",
        )
    if set(decisions) != {0, 1}:
        return False, diagnostic(
            "P_OFFSET_DECISION",
            "insufficient_decision_coverage",
            expected="decisions=0,1",
            observed="decisions=" + ",".join(str(value) for value in sorted(set(decisions))),
            event="clk_rising_set",
        )
    return True, pass_note(PROPERTY_IDS, f"checked={checked} max_err={max_err:.5f} decisions=0,1")

CHECKER_ID = "v4_112_latched_comparator_delay"
CHECKER: Checker = check_v3_latched_comparator_delay
