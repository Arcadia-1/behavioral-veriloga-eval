"""Stimulus-relative checker for canonical V4 DUT 032."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import close, crossings, diagnostic, event_label, pass_note, probe_time, require_signals, sample


PROPERTY_IDS = (
    "P_INITIAL_AND_RESET_COMMON_MODE",
    "P_SMALL_SIGNAL_GAIN",
    "P_POSITIVE_COMPRESSION",
    "P_NEGATIVE_COMPRESSION",
    "P_FINAL_OUTPUT_CLAMP",
    "P_CLOCKED_HOLD",
)


def _transfer(vin: float) -> tuple[float, float, str, bool]:
    linear = 0.45 + 2.2 * (vin - 0.45)
    if linear > 0.76:
        raw, metric, region = 0.76 + 0.28 * (linear - 0.76), 0.8, "positive"
    elif linear < 0.14:
        raw, metric, region = 0.14 + 0.28 * (linear - 0.14), 0.8, "negative"
    else:
        raw, metric, region = linear, 0.1, "linear"
    return min(0.86, max(0.04, raw)), metric, region, not 0.04 <= raw <= 0.86


def check_lna_gain_compression_macro(rows: list[dict[str, float]]) -> tuple[bool, str]:
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
        rst, vin = sample(rows, "rst", edge), sample(rows, "vin", edge)
        out, metric = sample(rows, "out", probe), sample(rows, "metric", probe)
        if None in (rst, vin, out, metric):
            continue
        assert rst is not None and vin is not None and out is not None and metric is not None
        label = event_label("clk_rise", index, edge)
        if rst > 0.45:
            expected_out, expected_metric = 0.45, 0.0
            property_id = "P_INITIAL_AND_RESET_COMMON_MODE"
            covered.add("reset")
        else:
            expected_out, expected_metric, region, clamped = _transfer(vin)
            property_id = {
                "linear": "P_SMALL_SIGNAL_GAIN",
                "positive": "P_POSITIVE_COMPRESSION",
                "negative": "P_NEGATIVE_COMPRESSION",
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
                values = (
                    sample(rows, "out", early), sample(rows, "out", late),
                    sample(rows, "metric", early), sample(rows, "metric", late),
                )
                if None not in values:
                    a, b, c, d = values
                    assert a is not None and b is not None and c is not None and d is not None
                    hold_checks += 1
                    if abs(a - b) > 0.035 or abs(c - d) > 0.10:
                        return False, diagnostic(
                            "P_CLOCKED_HOLD", "behavior_mismatch", expected="held_between_clk_rises",
                            observed=f"out:{a:.4f}->{b:.4f},metric:{c:.3f}->{d:.3f}", event=label,
                        )
    out_min, out_max = min(row["out"] for row in rows), max(row["out"] for row in rows)
    if out_min < 0.02 or out_max > 0.88:
        return False, diagnostic(
            "P_FINAL_OUTPUT_CLAMP", "behavior_mismatch", expected="out_in_[0.04,0.86]",
            observed=f"out_range:{out_min:.4f}..{out_max:.4f}", event="full_trace",
        )
    missing = sorted({"reset", "linear", "positive", "negative", "clamp"} - covered)
    if missing or hold_checks == 0:
        return False, diagnostic(
            "P_FINAL_OUTPUT_CLAMP" if "clamp" in missing else "P_CLOCKED_HOLD",
            "insufficient_excitation", expected="reset,linear,positive,negative,clamp,hold",
            observed="missing:" + ",".join(missing + ([] if hold_checks else ["hold"])), event="full_trace",
        )
    return True, pass_note(PROPERTY_IDS, f"lna edge_checks={len(edges)} hold_checks={hold_checks}")


CHECKER_ID = "v4_032_lna_gain_compression_macro"
CHECKER: Checker = check_lna_gain_compression_macro
