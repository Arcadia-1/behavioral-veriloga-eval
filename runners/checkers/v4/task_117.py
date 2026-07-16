"""Task-specific checker for canonical v4 DUT 117."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import crossings, diagnostic, pass_note, probe_time, require_signals, sample


PROPERTY_IDS = (
    "P_FIRST_EDGE_CAPTURE",
    "P_PREVIOUS_WINDOW_REPORT",
    "P_SIGNED_DIFFERENCE",
    "P_OUTPUT_CLIP",
    "P_WINDOW_REARM",
    "P_OUTPUT_TRANSITION",
)


def _v3_first_edge_between(edges: list[float], start_s: float, stop_s: float) -> float | None:
    for edge in edges:
        if start_s < edge < stop_s:
            return edge
    return None

def check_v3_time_diff_detector(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "vinp", "vinn", "vout"}
    missing = require_signals(rows, required, "P_PREVIOUS_WINDOW_REPORT")
    if missing:
        return False, missing

    clk_edges = crossings(rows, "clk", threshold=0.45, direction="rising")
    p_edges = crossings(rows, "vinp", threshold=0.45, direction="rising")
    n_edges = crossings(rows, "vinn", threshold=0.45, direction="rising")
    if len(clk_edges) < 3:
        return False, diagnostic(
            "P_WINDOW_REARM",
            "insufficient_events",
            expected="clk_rising_count>=3",
            observed=f"clk_rising_count={len(clk_edges)}",
            event="clk_rising_set",
        )

    max_err = 0.0
    checked = 0
    for idx, edge in enumerate(clk_edges):
        next_edge = clk_edges[idx + 1] if idx + 1 < len(clk_edges) else None
        sample_t = probe_time(rows, edge, next_edge, fraction=0.25)
        if sample_t is None:
            continue
        if idx == 0:
            expected = 0.0
        else:
            start = clk_edges[idx - 1]
            p_edge = _v3_first_edge_between(p_edges, start, edge)
            n_edge = _v3_first_edge_between(n_edges, start, edge)
            if p_edge is None or n_edge is None:
                return False, diagnostic(
                    "P_FIRST_EDGE_CAPTURE",
                    "missing_window_edge",
                    expected="vinp_rising and vinn_rising in previous clock window",
                    observed=f"vinp_present={p_edge is not None},vinn_present={n_edge is not None}",
                    event=f"clk_window[{idx - 1}]",
                )
            p_time = p_edge
            n_time = n_edge
            expected = max(-0.9, min(0.9, (p_time - n_time) * 1.0e9))
        observed = sample(rows, "vout", sample_t)
        if observed is None:
            return False, diagnostic(
                "P_OUTPUT_TRANSITION",
                "missing_sample",
                expected="vout",
                observed="unavailable",
                event=f"clk_rising[{idx}]",
            )
        err = abs(observed - expected)
        max_err = max(max_err, err)
        checked += 1
        if err > 0.10:
            return False, diagnostic(
                "P_SIGNED_DIFFERENCE",
                "time_difference_mismatch",
                expected=f"vout={expected:.4f}",
                observed=f"vout={observed:.4f},err={err:.4f}",
                event=f"clk_rising[{idx}]",
            )
    if checked < 3:
        return False, diagnostic(
            "P_PREVIOUS_WINDOW_REPORT",
            "insufficient_checks",
            expected="checked>=3",
            observed=f"checked={checked}",
            event="clk_rising_set",
        )
    return True, pass_note(PROPERTY_IDS, f"checked={checked} max_error={max_err:.5f}")

CHECKER_ID = "v4_117_time_diff_detector"
CHECKER: Checker = check_v3_time_diff_detector
