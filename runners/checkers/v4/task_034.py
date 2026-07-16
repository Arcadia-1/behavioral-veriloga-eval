"""Stimulus-relative checker for canonical V4 DUT 034."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import close, crossings, diagnostic, event_label, pass_note, probe_time, require_signals, sample


PROPERTY_IDS = (
    "P_RESET_STATE",
    "P_SIGNED_UPDATE",
    "P_STEP_HALVING",
    "P_DEADBAND_HOLD",
    "P_PROPORTIONAL_CLAMP",
    "P_LOCK_COUNT_METRIC",
)


def check_release_loop_filter(rows: list[dict[str, float]]) -> tuple[bool, str]:
    error = require_signals(rows, {"time", "clk", "rst", "vin", "out", "metric"}, "P_SIGNED_UPDATE")
    if error:
        return False, error
    edges = crossings(rows, "clk", threshold=0.45, direction="rising")
    if len(edges) < 8:
        return False, diagnostic(
            "P_SIGNED_UPDATE", "insufficient_excitation", expected="clk_rise_count>=8",
            observed=f"clk_rise_count={len(edges)}", event="full_trace",
        )

    state, step, integral, accepted = 0.45, 0.20, 0.0, 0
    reset_seen = False
    deadband_seen = False
    positive_seen = False
    negative_seen = False
    max_accepted = 0
    checked = 0
    for index, edge in enumerate(edges):
        next_edge = edges[index + 1] if index + 1 < len(edges) else None
        rst, vin = sample(rows, "rst", edge), sample(rows, "vin", edge)
        probe = probe_time(rows, edge, next_edge)
        if None in (rst, vin) or probe is None:
            continue
        assert rst is not None and vin is not None
        err = vin - 0.45
        label = event_label("clk_rise", index, edge)
        if rst > 0.45:
            state, step, integral, accepted = 0.45, 0.20, 0.0, 0
            expected_metric = 0.0
            property_id = "P_RESET_STATE"
            reset_seen = True
        elif abs(err) > 0.05:
            state += step if err > 0.0 else -step
            state = min(0.85, max(0.05, state))
            integral += 0.04 * err
            step *= 0.5
            accepted += 1
            max_accepted = max(max_accepted, accepted)
            expected_metric = 0.9 if accepted >= 4 else 0.0
            positive_seen |= err > 0.0
            negative_seen |= err < 0.0
            property_id = "P_SIGNED_UPDATE" if accepted <= 1 else "P_STEP_HALVING"
        else:
            expected_metric = 0.9 if accepted >= 4 else 0.0
            property_id = "P_DEADBAND_HOLD"
            deadband_seen = True
        expected_out = state + integral
        out, metric = sample(rows, "out", probe), sample(rows, "metric", probe)
        if None in (out, metric):
            continue
        assert out is not None and metric is not None
        checked += 1
        if not close(out, expected_out, 0.045):
            return False, diagnostic(
                property_id, "behavior_mismatch", expected=f"out:{expected_out:.4f}",
                observed=f"out:{out:.4f},vin:{vin:.4f},accepted:{accepted}", event=label,
            )
        if not close(metric, expected_metric, 0.10):
            return False, diagnostic(
                "P_LOCK_COUNT_METRIC", "behavior_mismatch", expected=f"metric:{expected_metric:.3f}",
                observed=f"metric:{metric:.3f},accepted:{accepted}", event=label,
            )

    out_min, out_max = min(row["out"] for row in rows), max(row["out"] for row in rows)
    if out_min < -0.02 or out_max > 0.98:
        return False, diagnostic(
            "P_PROPORTIONAL_CLAMP", "behavior_mismatch", expected="bounded_proportional_state",
            observed=f"out_range:{out_min:.4f}..{out_max:.4f}", event="full_trace",
        )
    missing = []
    if not reset_seen:
        missing.append("reset")
    if not deadband_seen:
        missing.append("deadband")
    if not positive_seen:
        missing.append("positive_update")
    if not negative_seen:
        missing.append("negative_update")
    if max_accepted < 4:
        missing.append("four_accepted_updates")
    if missing:
        return False, diagnostic(
            "P_SIGNED_UPDATE", "insufficient_excitation",
            expected="reset,deadband,positive,negative,four_updates",
            observed="missing:" + ",".join(missing), event="full_trace",
        )
    return True, pass_note(PROPERTY_IDS, f"loop_filter edge_checks={checked} max_accepted={max_accepted}")


CHECKER_ID = "v4_034_loop_filter_abstraction"
CHECKER: Checker = check_release_loop_filter
