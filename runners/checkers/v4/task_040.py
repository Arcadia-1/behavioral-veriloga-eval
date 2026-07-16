"""Stimulus-relative checker for canonical V4 DUT 040."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import close, crossings, diagnostic, event_label, pass_note, probe_time, require_signals, sample


PROPERTY_IDS = (
    "P_RESET_REFERENCE",
    "P_INPUT_CLAMP",
    "P_PTAT_TREND",
    "P_CTAT_PTAT_AVERAGE",
    "P_REFERENCE_BOUNDS",
)


def check_ptat_ctat_reference_generator(rows: list[dict[str, float]]) -> tuple[bool, str]:
    error = require_signals(rows, {"time", "clk", "rst", "vin", "out", "metric"}, "P_INPUT_CLAMP")
    if error:
        return False, error
    edges = crossings(rows, "clk", threshold=0.45, direction="rising")
    if len(edges) < 5:
        return False, diagnostic(
            "P_PTAT_TREND", "insufficient_excitation", expected="clk_rise_count>=5",
            observed=f"clk_rise_count={len(edges)}", event="full_trace",
        )
    covered: set[str] = set()
    metrics: list[tuple[float, float]] = []
    checked = 0
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
            property_id = "P_RESET_REFERENCE"
            covered.add("reset")
        else:
            clamped_vin = min(0.9, max(0.0, vin))
            expected_out = 0.48
            expected_metric = 0.18 + 0.34 * clamped_vin
            property_id = "P_CTAT_PTAT_AVERAGE"
            metrics.append((clamped_vin, metric))
            if vin < 0.0:
                covered.add("below_range")
            elif vin > 0.9:
                covered.add("above_range")
            else:
                covered.add("nominal")
        checked += 1
        if not close(out, expected_out, 0.035):
            return False, diagnostic(
                property_id, "behavior_mismatch", expected=f"out:{expected_out:.3f}",
                observed=f"out:{out:.3f},vin:{vin:.3f}", event=label,
            )
        if not close(metric, expected_metric, 0.055):
            return False, diagnostic(
                "P_PTAT_TREND", "behavior_mismatch", expected=f"metric:{expected_metric:.3f}",
                observed=f"metric:{metric:.3f},vin:{vin:.3f}", event=label,
            )
    out_min, out_max = min(row["out"] for row in rows), max(row["out"] for row in rows)
    if out_min < -0.02 or out_max > 0.92:
        return False, diagnostic(
            "P_REFERENCE_BOUNDS", "behavior_mismatch", expected="out_in_[0,0.9]",
            observed=f"out_range:{out_min:.3f}..{out_max:.3f}", event="full_trace",
        )
    if metrics:
        ordered = sorted(metrics)
        if ordered[-1][1] <= ordered[0][1] + 0.20:
            return False, diagnostic(
                "P_PTAT_TREND", "behavior_mismatch", expected="metric_increases_with_clamped_vin",
                observed=f"metric:{ordered[0][1]:.3f}->{ordered[-1][1]:.3f}", event="full_trace",
            )
    missing = sorted({"reset", "below_range", "nominal", "above_range"} - covered)
    if missing:
        return False, diagnostic(
            "P_INPUT_CLAMP", "insufficient_excitation",
            expected="reset,below_range,nominal,above_range",
            observed="missing:" + ",".join(missing), event="full_trace",
        )
    return True, pass_note(PROPERTY_IDS, f"ptat_ctat edge_checks={checked}")


CHECKER_ID = "v4_040_ptat_ctat_reference_generator"
CHECKER: Checker = check_ptat_ctat_reference_generator
