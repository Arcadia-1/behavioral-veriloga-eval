"""Stimulus-relative checker for canonical V4 DUT 038."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import close, crossings, diagnostic, event_label, pass_note, percentile, probe_time, require_signals, sample


PROPERTY_IDS = (
    "P_RESET_UNITY",
    "P_SAMPLED_GAIN_SELECT",
    "P_COMMON_MODE_GAIN",
    "P_OUTPUT_CLAMP",
    "P_CLIP_METRIC",
)


def check_programmable_gain_amplifier(rows: list[dict[str, float]]) -> tuple[bool, str]:
    error = require_signals(
        rows, {"time", "clk", "rst", "gain_sel", "vin", "out", "metric"}, "P_SAMPLED_GAIN_SELECT"
    )
    if error:
        return False, error
    reset_rows = [row for row in rows if row["rst"] > 0.70]
    if not reset_rows:
        return False, diagnostic(
            "P_RESET_UNITY", "insufficient_excitation", expected="active_reset_interval",
            observed="reset_rows:0", event="full_trace",
        )
    reset_out_error = percentile([abs(row["out"] - 0.45) for row in reset_rows], 0.90)
    reset_metric_error = percentile([abs(row["metric"]) for row in reset_rows], 0.90)
    if reset_out_error > 0.05 or reset_metric_error > 0.10:
        return False, diagnostic(
            "P_RESET_UNITY", "behavior_mismatch", expected="out:0.45,metric:0_during_reset",
            observed=f"out_error_p90:{reset_out_error:.3f},metric_error_p90:{reset_metric_error:.3f}",
            event="active_reset_interval",
        )
    edges = crossings(rows, "clk", threshold=0.45, direction="rising")
    if len(edges) < 6:
        return False, diagnostic(
            "P_SAMPLED_GAIN_SELECT", "insufficient_excitation", expected="clk_rise_count>=6",
            observed=f"clk_rise_count={len(edges)}", event="full_trace",
        )

    gain = 1.0
    covered: set[str] = {"reset"}
    checked = 0
    for index, edge in enumerate(edges):
        next_edge = edges[index + 1] if index + 1 < len(edges) else None
        rst_edge = sample(rows, "rst", edge)
        gain_sel = sample(rows, "gain_sel", edge)
        if rst_edge is None or gain_sel is None:
            continue
        if rst_edge > 0.45:
            gain = 1.0
            covered.add("reset")
        else:
            gain = 2.4 if gain_sel > 0.45 else 0.8
            covered.add("high_gain" if gain > 1.0 else "low_gain")
        fractions = (0.32, 0.68) if next_edge is not None else (0.35,)
        for probe_index, fraction in enumerate(fractions):
            probe = probe_time(rows, edge, next_edge, fraction=fraction)
            if probe is None:
                continue
            rst, vin = sample(rows, "rst", probe), sample(rows, "vin", probe)
            out, metric = sample(rows, "out", probe), sample(rows, "metric", probe)
            if None in (rst, vin, out, metric):
                continue
            assert rst is not None and vin is not None and out is not None and metric is not None
            if rst > 0.45:
                expected_out, expected_metric = 0.45, 0.0
                property_id = "P_RESET_UNITY"
                covered.add("reset")
            else:
                raw = 0.45 + gain * (vin - 0.45)
                expected_out = min(0.9, max(0.0, raw))
                expected_metric = 0.9 if raw < 0.0 or raw > 0.9 else 0.0
                property_id = "P_COMMON_MODE_GAIN"
                if raw > 0.9:
                    covered.add("positive_clip")
                elif raw < 0.0:
                    covered.add("negative_clip")
                else:
                    covered.add("unclipped")
            checked += 1
            label = event_label(f"clk_interval_probe_{probe_index}", index, probe)
            if not close(out, expected_out, 0.055):
                return False, diagnostic(
                    "P_OUTPUT_CLAMP" if expected_out in {0.0, 0.9} else property_id,
                    "behavior_mismatch", expected=f"out:{expected_out:.4f},sampled_gain:{gain:.1f}",
                    observed=f"out:{out:.4f},vin:{vin:.4f},gain_sel:{gain_sel:.3f}", event=label,
                )
            if not close(metric, expected_metric, 0.12):
                return False, diagnostic(
                    "P_CLIP_METRIC", "behavior_mismatch", expected=f"metric:{expected_metric:.1f}",
                    observed=f"metric:{metric:.3f},out:{out:.3f},vin:{vin:.3f}", event=label,
                )
    out_min, out_max = min(row["out"] for row in rows), max(row["out"] for row in rows)
    if out_min < -0.03 or out_max > 0.93:
        return False, diagnostic(
            "P_OUTPUT_CLAMP", "behavior_mismatch", expected="out_in_[0,0.9]",
            observed=f"out_range:{out_min:.4f}..{out_max:.4f}", event="full_trace",
        )
    missing = sorted(
        {"reset", "low_gain", "high_gain", "unclipped", "positive_clip", "negative_clip"} - covered
    )
    if missing:
        return False, diagnostic(
            "P_SAMPLED_GAIN_SELECT", "insufficient_excitation",
            expected="reset,low_gain,high_gain,unclipped,both_clamps",
            observed="missing:" + ",".join(missing), event="full_trace",
        )
    return True, pass_note(PROPERTY_IDS, f"pga interval_checks={checked}")


CHECKER_ID = "v4_038_programmable_gain_amplifier"
CHECKER: Checker = check_programmable_gain_amplifier
