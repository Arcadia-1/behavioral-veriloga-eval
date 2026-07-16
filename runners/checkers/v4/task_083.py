"""Task-specific checker for canonical v4 DUT 083."""
from __future__ import annotations

from collections.abc import Callable

from ..api import Checker
from .stimulus_relative import crossings, diagnostic, event_label, pass_note, require_signals


PROPERTY_IDS = [
    "P_RESET_COMMON_MODE",
    "P_BOUNDED_PREAMP",
    "P_FIRST_FILTER_STAGE",
    "P_SECOND_FILTER_STAGE",
    "P_CASCADE_LAG",
    "P_SETTLE_STATUS",
]


def mean_value(rows: list[dict[str, float]], key: str) -> float | None:
    values = [r[key] for r in rows if key in r]
    if not values:
        return None
    return sum(values) / len(values)


def contiguous_segments(
    rows: list[dict[str, float]],
    predicate: Callable[[dict[str, float]], bool],
    *,
    min_len: int = 3,
) -> list[list[dict[str, float]]]:
    segments: list[list[dict[str, float]]] = []
    current: list[dict[str, float]] = []
    for row in rows:
        if predicate(row):
            current.append(row)
        elif current:
            if len(current) >= min_len:
                segments.append(current)
            current = []
    if len(current) >= min_len:
        segments.append(current)
    return segments


def middle(rows: list[dict[str, float]], start_fraction: float, stop_fraction: float) -> list[dict[str, float]]:
    if len(rows) < 4:
        return rows
    start = min(len(rows) - 1, max(0, int(len(rows) * start_fraction)))
    stop = min(len(rows), max(start + 1, int(len(rows) * stop_fraction)))
    return rows[start:stop]


def fail(property_id: str, expected: str, observed: str, event: str) -> tuple[bool, str]:
    return False, diagnostic(
        property_id,
        "behavior_mismatch",
        expected=expected,
        observed=observed,
        event=event,
    )


def check_release_amplifier_filter_chain(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {
        "time",
        "clk",
        "rst",
        "vin",
        "out",
        "metric",
        "preamp_mon",
        "filt1_mon",
        "filt2_mon",
        "settle_metric",
    }
    missing = require_signals(rows, required, "P_RESET_COMMON_MODE")
    if missing:
        return False, missing

    reset_releases = crossings(rows, "rst", threshold=0.45, direction="falling")
    release_t = reset_releases[0] if reset_releases else rows[0]["time"]
    active_rows = [row for row in rows if row["time"] >= release_t and row["rst"] <= 0.45]
    high_segments = contiguous_segments(active_rows, lambda row: row["vin"] >= 0.75)
    if not high_segments:
        return False, diagnostic(
            "P_CASCADE_LAG",
            "invalid_trace",
            expected="observable_high_input_segment",
            observed="segments=0",
            event=event_label("reset_release", 0, release_t),
        )
    high_segment = high_segments[0]
    high_start = high_segment[0]["time"]
    high_stop = high_segment[-1]["time"]
    mid_segments = contiguous_segments(
        [row for row in active_rows if row["time"] > high_stop],
        lambda row: abs(row["vin"] - 0.45) <= 0.04,
    )
    low_segments = contiguous_segments(
        [row for row in active_rows if row["time"] > high_stop],
        lambda row: row["vin"] <= 0.20,
    )
    if not mid_segments or not low_segments:
        return False, diagnostic(
            "P_SETTLE_STATUS",
            "invalid_trace",
            expected="observable_mid_and_low_input_segments_after_high",
            observed=f"mid={len(mid_segments)},low={len(low_segments)}",
            event=event_label("high_input", 0, high_start),
        )

    early_high_rows = middle(high_segment, 0.05, 0.30)
    late_high_rows = middle(high_segment, 0.70, 0.98)
    mid_rows = middle(mid_segments[0], 0.25, 0.80)
    low_rows = middle(low_segments[0], 0.55, 0.98)

    early_high_out = mean_value(early_high_rows, "out")
    late_high_out = mean_value(late_high_rows, "out")
    early_high_metric = mean_value(early_high_rows, "metric")
    late_high_metric = mean_value(late_high_rows, "metric")
    mid_metric = mean_value(mid_rows, "metric")
    low_metric = mean_value(low_rows, "metric")
    early_high_preamp = mean_value(early_high_rows, "preamp_mon")
    late_high_preamp = mean_value(late_high_rows, "preamp_mon")
    low_preamp = mean_value(low_rows, "preamp_mon")
    early_high_filt1 = mean_value(early_high_rows, "filt1_mon")
    late_high_filt1 = mean_value(late_high_rows, "filt1_mon")
    early_high_filt2 = mean_value(early_high_rows, "filt2_mon")
    late_high_filt2 = mean_value(late_high_rows, "filt2_mon")
    low_filt2 = mean_value(low_rows, "filt2_mon")
    settle_low = mean_value(early_high_rows, "settle_metric")
    settle_high = mean_value(late_high_rows, "settle_metric")
    low_out = mean_value(low_rows, "out")
    if None in (
        early_high_out,
        late_high_out,
        early_high_metric,
        late_high_metric,
        mid_metric,
        low_metric,
        early_high_preamp,
        late_high_preamp,
        low_preamp,
        early_high_filt1,
        late_high_filt1,
        early_high_filt2,
        late_high_filt2,
        low_filt2,
        settle_low,
        settle_high,
        low_out,
    ):
        return False, diagnostic(
            "P_CASCADE_LAG",
            "invalid_trace",
            expected="complete_segment_metrics",
            observed="missing_metric_sample",
            event=event_label("high_input", 0, high_start),
        )
    assert early_high_out is not None
    assert late_high_out is not None
    assert early_high_metric is not None
    assert late_high_metric is not None
    assert mid_metric is not None
    assert low_metric is not None
    assert early_high_preamp is not None
    assert late_high_preamp is not None
    assert low_preamp is not None
    assert early_high_filt1 is not None
    assert late_high_filt1 is not None
    assert early_high_filt2 is not None
    assert late_high_filt2 is not None
    assert low_filt2 is not None
    assert settle_low is not None
    assert settle_high is not None
    assert low_out is not None

    post_rows = active_rows
    if len(post_rows) < 10:
        return False, diagnostic(
            "P_RESET_COMMON_MODE",
            "invalid_trace",
            expected="at_least_10_post_reset_rows",
            observed=f"post_reset_rows={len(post_rows)}",
            event=event_label("reset_release", 0, release_t),
        )
    out_vals = [r["out"] for r in post_rows]
    metric_vals = [r["metric"] for r in post_rows]
    preamp_vals = [r["preamp_mon"] for r in post_rows]
    filt1_vals = [r["filt1_mon"] for r in post_rows]
    filt2_vals = [r["filt2_mon"] for r in post_rows]
    settle_vals = [r["settle_metric"] for r in post_rows]
    if not (-0.02 <= min(out_vals) <= max(out_vals) <= 0.92):
        return fail("P_SECOND_FILTER_STAGE", "out_range_within_rails", f"range={min(out_vals):.3f}..{max(out_vals):.3f}", event_label("post_reset", 0, release_t))
    if not (-0.02 <= min(metric_vals) <= max(metric_vals) <= 0.92):
        return fail("P_BOUNDED_PREAMP", "metric_range_within_rails", f"range={min(metric_vals):.3f}..{max(metric_vals):.3f}", event_label("post_reset", 0, release_t))
    if not (-0.02 <= min(preamp_vals) <= max(preamp_vals) <= 0.92):
        return fail("P_BOUNDED_PREAMP", "preamp_range_within_rails", f"range={min(preamp_vals):.3f}..{max(preamp_vals):.3f}", event_label("post_reset", 0, release_t))
    if not (-0.02 <= min(filt1_vals) <= max(filt1_vals) <= 0.92):
        return fail("P_FIRST_FILTER_STAGE", "filt1_range_within_rails", f"range={min(filt1_vals):.3f}..{max(filt1_vals):.3f}", event_label("post_reset", 0, release_t))
    if not (-0.02 <= min(filt2_vals) <= max(filt2_vals) <= 0.92):
        return fail("P_SECOND_FILTER_STAGE", "filt2_range_within_rails", f"range={min(filt2_vals):.3f}..{max(filt2_vals):.3f}", event_label("post_reset", 0, release_t))
    if early_high_metric < 0.84 or late_high_metric < 0.84 or low_metric > 0.08:
        return fail("P_BOUNDED_PREAMP", "metric_tracks_high_then_low_input", f"early={early_high_metric:.3f},late={late_high_metric:.3f},low={low_metric:.3f}", event_label("high_input", 0, high_start))
    if (
        abs(early_high_metric - early_high_preamp) > 0.04
        or abs(late_high_metric - late_high_preamp) > 0.04
        or abs(low_metric - low_preamp) > 0.04
    ):
        return fail("P_BOUNDED_PREAMP", "preamp_monitor_matches_metric", f"early={early_high_metric:.3f}/{early_high_preamp:.3f},late={late_high_metric:.3f}/{late_high_preamp:.3f},low={low_metric:.3f}/{low_preamp:.3f}", event_label("high_input", 0, high_start))
    if abs(mid_metric - 0.45) > 0.08:
        return fail("P_RESET_COMMON_MODE", "mid_metric_common_mode", f"mid_metric={mid_metric:.3f}", event_label("mid_input", 0, mid_rows[0]["time"]))
    if late_high_out <= early_high_out + 0.09:
        return fail("P_CASCADE_LAG", "late_high_out>early_high_out+0.09", f"early={early_high_out:.3f},late={late_high_out:.3f}", event_label("high_input", 0, high_start))
    if early_high_metric - early_high_out < 0.12:
        return fail("P_CASCADE_LAG", "early_metric-output_gap>=0.12", f"gap={early_high_metric - early_high_out:.3f}", event_label("high_input", 0, high_start))
    if early_high_filt1 <= early_high_filt2 + 0.05:
        return fail("P_FIRST_FILTER_STAGE", "filt1_leads_filt2_on_high_step", f"f1={early_high_filt1:.3f},f2={early_high_filt2:.3f}", event_label("high_input", 0, high_start))
    if (
        abs(early_high_out - early_high_filt2) > 0.04
        or abs(late_high_out - late_high_filt2) > 0.04
        or abs(low_out - low_filt2) > 0.04
    ):
        return fail("P_SECOND_FILTER_STAGE", "output_matches_second_filter_state", f"early={early_high_out:.3f}/{early_high_filt2:.3f},late={late_high_out:.3f}/{late_high_filt2:.3f},low={low_out:.3f}/{low_filt2:.3f}", event_label("high_input", 0, high_start))
    if max(settle_vals) < 0.75 or min(settle_vals) > 0.25:
        return fail("P_SETTLE_STATUS", "settle_metric_voltage_coded", f"range={min(settle_vals):.3f}..{max(settle_vals):.3f}", event_label("post_reset", 0, release_t))
    if settle_low > 0.35 or settle_high < 0.65:
        return fail("P_SETTLE_STATUS", "settle_metric_recovers_during_high_step", f"early={settle_low:.3f},late={settle_high:.3f}", event_label("high_input", 0, high_start))
    if low_out > 0.35:
        return fail("P_SECOND_FILTER_STAGE", "low_input_output_falls", f"low_out={low_out:.3f}", event_label("low_input", 0, low_rows[0]["time"]))
    return True, pass_note(
        PROPERTY_IDS,
        "release_amplifier_filter_chain "
        f"metric_high_low={early_high_metric:.3f}/{low_metric:.3f} high_window={high_start:.3e}..{high_stop:.3e} "
        f"out_lag={early_high_out:.3f}->{late_high_out:.3f} "
        f"settle={settle_low:.3f}->{settle_high:.3f}"
    )

CHECKER_ID = "v4_083_amplifier_filter_chain"
CHECKER: Checker = check_release_amplifier_filter_chain
