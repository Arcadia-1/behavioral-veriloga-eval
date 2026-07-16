"""Task-specific checker for canonical v4 DUT 090."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import crossings, diagnostic, event_label, pass_note, require_signals


PROPERTY_IDS = [
    "P_POSITIVE_DITHER",
    "P_NEGATIVE_DITHER",
    "P_SYMMETRIC_SPLIT",
    "P_COMMON_MODE_PRESERVATION",
    "P_PARAMETER_OVERRIDE",
]


def _mean_abs_error(values: list[float], target: float) -> float:
    return sum(abs(value - target) for value in values) / len(values)


def _state_rows(
    rows: list[dict[str, float]],
    *,
    threshold: float,
    high: bool,
) -> list[dict[str, float]]:
    transition_times = sorted(
        crossings(rows, "dpn", threshold=threshold, direction="rising")
        + crossings(rows, "dpn", threshold=threshold, direction="falling")
    )
    if len(rows) < 2:
        return []
    positive_steps = [
        cur["time"] - prev["time"]
        for prev, cur in zip(rows, rows[1:])
        if cur["time"] > prev["time"]
    ]
    median_step = sorted(positive_steps)[len(positive_steps) // 2] if positive_steps else 0.0
    transition_gaps = [b - a for a, b in zip(transition_times, transition_times[1:]) if b > a]
    state_gap = min(transition_gaps) if transition_gaps else rows[-1]["time"] - rows[0]["time"]
    guard_s = max(2.0 * median_step, 0.01 * state_gap)
    selected: list[dict[str, float]] = []
    segment_start = rows[0]["time"]
    boundaries = transition_times + [rows[-1]["time"]]
    for index, segment_stop in enumerate(boundaries):
        segment = [
            row
            for row in rows
            if segment_start + guard_s <= row["time"] <= segment_stop - guard_s
        ]
        if segment:
            segment_is_high = sum(row["dpn"] for row in segment) / len(segment) > threshold
            if segment_is_high is high:
                selected.extend(segment)
        segment_start = segment_stop
        if index < len(transition_times):
            segment_start = transition_times[index]
    return selected


def check_v3_dither_adder(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vres_p", "vres_n", "dpn", "vout_p", "vout_n"}
    missing = require_signals(rows, required, "P_POSITIVE_DITHER")
    if missing:
        return False, missing

    high: list[float] = []
    low: list[float] = []
    cm_errors: list[float] = []
    for state_high, bucket in ((True, high), (False, low)):
        for row in _state_rows(rows, threshold=0.45, high=state_high):
            vin_diff = row["vres_p"] - row["vres_n"]
            out_diff = row["vout_p"] - row["vout_n"]
            bucket.append(out_diff - vin_diff)
            in_cm = 0.5 * (row["vres_p"] + row["vres_n"])
            out_cm = 0.5 * (row["vout_p"] + row["vout_n"])
            cm_errors.append(abs(out_cm - in_cm))

    first_transition = next(
        iter(
            sorted(
                crossings(rows, "dpn", threshold=0.45, direction="rising")
                + crossings(rows, "dpn", threshold=0.45, direction="falling")
            )
        ),
        rows[0]["time"],
    )
    if len(high) < 20 or len(low) < 20:
        return False, diagnostic(
            "P_PARAMETER_OVERRIDE",
            "invalid_trace",
            expected="at_least_20_settled_rows_per_dpn_state",
            observed=f"high={len(high)},low={len(low)}",
            event=event_label("dpn_transition", 0, first_transition),
        )
    high_mean = sum(high) / len(high)
    low_mean = sum(low) / len(low)
    high_err = _mean_abs_error(high, high_mean)
    low_err = _mean_abs_error(low, low_mean)
    cm_max = max(cm_errors) if cm_errors else float("inf")
    symmetry_err = abs(high_mean + low_mean)
    if not (0.020 <= high_mean <= 0.040):
        return False, diagnostic(
            "P_POSITIVE_DITHER",
            "behavior_mismatch",
            expected="0.020<=positive_dither<=0.040",
            observed=f"positive_dither={high_mean:.4f}",
            event=event_label("dpn_high_region", 0, first_transition),
        )
    if not (-0.040 <= low_mean <= -0.020):
        return False, diagnostic(
            "P_NEGATIVE_DITHER",
            "behavior_mismatch",
            expected="-0.040<=negative_dither<=-0.020",
            observed=f"negative_dither={low_mean:.4f}",
            event=event_label("dpn_low_region", 0, rows[0]["time"]),
        )
    if symmetry_err > 0.002:
        return False, diagnostic(
            "P_SYMMETRIC_SPLIT",
            "behavior_mismatch",
            expected="positive_dither_plus_negative_dither<=0.002",
            observed=f"symmetry_err={symmetry_err:.4f}",
            event=event_label("dpn_transition", 0, first_transition),
        )
    if high_err > 0.003 or low_err > 0.003:
        return False, diagnostic(
            "P_PARAMETER_OVERRIDE",
            "behavior_mismatch",
            expected="state_dither_error<=0.003",
            observed=f"high_err={high_err:.4f},low_err={low_err:.4f}",
            event=event_label("dpn_transition", 0, first_transition),
        )
    if cm_max > 0.003:
        return False, diagnostic(
            "P_COMMON_MODE_PRESERVATION",
            "behavior_mismatch",
            expected="common_mode_error<=0.003",
            observed=f"cm_max={cm_max:.4f}",
            event=event_label("full_trace", 0, rows[0]["time"]),
        )
    return True, pass_note(
        PROPERTY_IDS,
        f"dither_high={high_mean:.4f} dither_low={low_mean:.4f} "
        f"symmetry_err={symmetry_err:.4f} high_err={high_err:.4f} "
        f"low_err={low_err:.4f} cm_max={cm_max:.4f}",
    )


CHECKER_ID = "v4_090_dither_adder"
CHECKER: Checker = check_v3_dither_adder
