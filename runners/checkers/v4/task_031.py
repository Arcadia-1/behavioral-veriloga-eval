"""Stimulus-relative checker for canonical V4 DUT 031."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import close, crossings, diagnostic, event_label, pass_note, probe_time, require_signals, sample


PROPERTY_IDS = (
    "P_INITIAL_AND_RESET_COMMON_MODE",
    "P_LINEAR_REGION",
    "P_POSITIVE_LIMITING",
    "P_NEGATIVE_LIMITING",
    "P_OUTPUT_CLAMP",
    "P_CLOCKED_HOLD",
)


def _transfer(vin: float) -> tuple[float, float, str, bool]:
    x = vin - 0.45
    unclamped: float
    if x > 0.09:
        unclamped, metric, region = 0.73 + 0.45 * (x - 0.09), 0.85, "positive"
    elif x < -0.09:
        unclamped, metric, region = 0.17 + 0.45 * (x + 0.09), 0.85, "negative"
    else:
        unclamped, metric, region = 0.45 + 1.7 * x, 0.0, "linear"
    return min(0.86, max(0.04, unclamped)), metric, region, not 0.04 <= unclamped <= 0.86


def check_limiting_amplifier_frontend(rows: list[dict[str, float]]) -> tuple[bool, str]:
    error = require_signals(rows, {"time", "clk", "rst", "vin", "out", "metric"}, "P_CLOCKED_HOLD")
    if error:
        return False, error
    edges = crossings(rows, "clk", threshold=0.45, direction="rising")
    if len(edges) < 4:
        return False, diagnostic(
            "P_CLOCKED_HOLD", "insufficient_excitation", expected="clk_rise_count>=4",
            observed=f"clk_rise_count={len(edges)}", event="full_trace",
        )

    covered: set[str] = set()
    hold_checks = 0
    for index, edge in enumerate(edges):
        next_edge = edges[index + 1] if index + 1 < len(edges) else None
        probe = probe_time(rows, edge, next_edge)
        if probe is None:
            continue
        rst = sample(rows, "rst", edge)
        vin = sample(rows, "vin", edge)
        out = sample(rows, "out", probe)
        metric = sample(rows, "metric", probe)
        if None in (rst, vin, out, metric):
            continue
        assert rst is not None and vin is not None and out is not None and metric is not None
        label = event_label("clk_rise", index, edge)
        if rst > 0.45:
            expected_out, expected_metric, property_id = 0.45, 0.0, "P_INITIAL_AND_RESET_COMMON_MODE"
            covered.add("reset")
        else:
            expected_out, expected_metric, region, clamped = _transfer(vin)
            property_id = {
                "linear": "P_LINEAR_REGION",
                "positive": "P_POSITIVE_LIMITING",
                "negative": "P_NEGATIVE_LIMITING",
            }[region]
            covered.add(region)
            if clamped:
                covered.add("clamp")
        if not close(out, expected_out, 0.012) or not close(metric, expected_metric, 0.10):
            return False, diagnostic(
                property_id, "behavior_mismatch",
                expected=f"out:{expected_out:.4f},metric:{expected_metric:.3f}",
                observed=f"out:{out:.4f},metric:{metric:.3f},vin:{vin:.4f}", event=label,
            )

        if next_edge is not None:
            early = probe_time(rows, edge, next_edge, fraction=0.32)
            late = probe_time(rows, edge, next_edge, fraction=0.82)
            if early is not None and late is not None:
                early_out, late_out = sample(rows, "out", early), sample(rows, "out", late)
                early_metric, late_metric = sample(rows, "metric", early), sample(rows, "metric", late)
                if None not in (early_out, late_out, early_metric, late_metric):
                    hold_checks += 1
                    assert early_out is not None and late_out is not None
                    assert early_metric is not None and late_metric is not None
                    if abs(early_out - late_out) > 0.035 or abs(early_metric - late_metric) > 0.10:
                        return False, diagnostic(
                            "P_CLOCKED_HOLD", "behavior_mismatch", expected="held_between_clk_rises",
                            observed=f"out:{early_out:.4f}->{late_out:.4f},metric:{early_metric:.3f}->{late_metric:.3f}",
                            event=label,
                        )

    out_min = min(row["out"] for row in rows)
    out_max = max(row["out"] for row in rows)
    if out_min < 0.02 or out_max > 0.88:
        return False, diagnostic(
            "P_OUTPUT_CLAMP", "behavior_mismatch", expected="out_in_[0.04,0.86]",
            observed=f"out_range:{out_min:.4f}..{out_max:.4f}", event="full_trace",
        )
    missing = sorted({"reset", "linear", "positive", "negative", "clamp"} - covered)
    if missing or hold_checks == 0:
        return False, diagnostic(
            "P_OUTPUT_CLAMP" if "clamp" in missing else "P_CLOCKED_HOLD",
            "insufficient_excitation", expected="reset,linear,positive,negative,clamp,hold",
            observed="missing:" + ",".join(missing + ([] if hold_checks else ["hold"])), event="full_trace",
        )
    return True, pass_note(PROPERTY_IDS, f"limiter edge_checks={len(edges)} hold_checks={hold_checks}")


CHECKER_ID = "v4_031_limiting_amplifier"
CHECKER: Checker = check_limiting_amplifier_frontend
