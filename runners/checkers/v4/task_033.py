"""Stimulus-relative checker for canonical V4 DUT 033."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import close, crossings, diagnostic, event_label, pass_note, probe_time, require_signals, sample


PROPERTY_IDS = (
    "P_RESET_BASELINE",
    "P_CLOCKED_MAGNITUDE_SAMPLE",
    "P_RSSI_BINS",
    "P_OUTPUT_BOUNDS",
    "P_AMPLITUDE_METRIC",
)


def _transfer(vin: float) -> tuple[float, float, int]:
    amp = abs(vin - 0.45)
    if amp < 0.035:
        out, bin_index = 0.12, 0
    elif amp < 0.11:
        out, bin_index = 0.30, 1
    elif amp < 0.22:
        out, bin_index = 0.54, 2
    else:
        out, bin_index = 0.72, 3
    return out, min(0.9, 3.0 * amp), bin_index


def check_log_rssi_power_detector(rows: list[dict[str, float]]) -> tuple[bool, str]:
    error = require_signals(rows, {"time", "clk", "rst", "vin", "out", "metric"}, "P_CLOCKED_MAGNITUDE_SAMPLE")
    if error:
        return False, error
    edges = crossings(rows, "clk", threshold=0.45, direction="rising")
    if len(edges) < 5:
        return False, diagnostic(
            "P_CLOCKED_MAGNITUDE_SAMPLE", "insufficient_excitation", expected="clk_rise_count>=5",
            observed=f"clk_rise_count={len(edges)}", event="full_trace",
        )
    bins: set[int] = set()
    reset_seen = False
    polarity: set[str] = set()
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
            expected_out, expected_metric = 0.12, 0.0
            reset_seen = True
            out_property = "P_RESET_BASELINE"
        else:
            expected_out, expected_metric, bin_index = _transfer(vin)
            bins.add(bin_index)
            if vin > 0.455:
                polarity.add("positive")
            elif vin < 0.445:
                polarity.add("negative")
            out_property = "P_RSSI_BINS"
        if not close(out, expected_out, 0.045):
            return False, diagnostic(
                out_property, "behavior_mismatch", expected=f"out:{expected_out:.3f}",
                observed=f"out:{out:.3f},vin:{vin:.4f}", event=label,
            )
        if not close(metric, expected_metric, 0.09):
            return False, diagnostic(
                "P_AMPLITUDE_METRIC", "behavior_mismatch", expected=f"metric:{expected_metric:.3f}",
                observed=f"metric:{metric:.3f},vin:{vin:.4f}", event=label,
            )
        if next_edge is not None:
            early = probe_time(rows, edge, next_edge, fraction=0.32)
            late = probe_time(rows, edge, next_edge, fraction=0.82)
            if early is not None and late is not None:
                a, b = sample(rows, "out", early), sample(rows, "out", late)
                c, d = sample(rows, "metric", early), sample(rows, "metric", late)
                if None not in (a, b, c, d):
                    assert a is not None and b is not None and c is not None and d is not None
                    hold_checks += 1
                    if abs(a - b) > 0.04 or abs(c - d) > 0.10:
                        return False, diagnostic(
                            "P_CLOCKED_MAGNITUDE_SAMPLE", "behavior_mismatch",
                            expected="held_between_clk_rises",
                            observed=f"out:{a:.3f}->{b:.3f},metric:{c:.3f}->{d:.3f}", event=label,
                        )
    out_min, out_max = min(row["out"] for row in rows), max(row["out"] for row in rows)
    if out_min < 0.06 or out_max > 0.84:
        return False, diagnostic(
            "P_OUTPUT_BOUNDS", "behavior_mismatch", expected="out_in_[0.08,0.82]",
            observed=f"out_range:{out_min:.3f}..{out_max:.3f}", event="full_trace",
        )
    missing = []
    if not reset_seen:
        missing.append("reset")
    if len(bins) < 4:
        missing.append(f"rssi_bins:{sorted(bins)}")
    if len(polarity) < 2:
        missing.append("both_input_polarities")
    if hold_checks == 0:
        missing.append("clocked_hold")
    if missing:
        return False, diagnostic(
            "P_RSSI_BINS", "insufficient_excitation", expected="reset,4_bins,both_polarities,hold",
            observed="missing:" + ",".join(missing), event="full_trace",
        )
    return True, pass_note(PROPERTY_IDS, f"rssi edge_checks={len(edges)} bins={sorted(bins)}")


CHECKER_ID = "v4_033_log_rssi_power_detector"
CHECKER: Checker = check_log_rssi_power_detector
