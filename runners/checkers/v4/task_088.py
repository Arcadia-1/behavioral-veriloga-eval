"""Task-specific checker for canonical v4 DUT 088."""
from __future__ import annotations

import csv
from pathlib import Path

from ..api import Checker
from .stimulus_relative import crossings, diagnostic, event_label, pass_note, require_signals


PROPERTY_IDS = [
    "P_REFERENCE_PERIOD_STEP",
    "P_DCO_FREQUENCY_CONTROL",
    "P_FEEDBACK_DIVISION",
    "P_BOUNDED_TRACKING_CONTROL",
    "P_INITIAL_LOCK_ACQUISITION",
    "P_DISTURBANCE_UNLOCK",
    "P_LATE_REACQUISITION",
]


def _median(values: list[float]) -> float:
    ordered = sorted(values)
    return ordered[len(ordered) // 2]


def _mean(values: list[float]) -> float:
    return sum(values) / len(values)


def _periods(edges: list[float]) -> list[float]:
    return [b - a for a, b in zip(edges, edges[1:]) if b > a]


def _tail_period(edges: list[float], *, after: float, min_edges: int = 5) -> tuple[float | None, int]:
    tail_edges = [edge for edge in edges if edge > after]
    if len(tail_edges) < min_edges:
        tail_edges = edges[-min(len(edges), max(min_edges, 8)) :]
    periods = _periods(tail_edges[-min(len(tail_edges), 8) :])
    if not periods:
        return None, len(tail_edges)
    return _mean(periods), len(tail_edges)


def _reference_step(ref_edges: list[float]) -> tuple[float, float, float, float] | None:
    periods = _periods(ref_edges)
    if len(periods) < 12:
        return None
    changes = [abs(periods[idx + 1] - periods[idx]) for idx in range(len(periods) - 1)]
    step_idx = max(range(len(changes)), key=lambda idx: changes[idx])
    pre_slice = periods[max(0, step_idx - 8) : step_idx + 1]
    post_slice = periods[step_idx + 1 : min(len(periods), step_idx + 10)]
    if not pre_slice or not post_slice:
        return None
    pre_period = _median(pre_slice)
    post_period = _median(post_slice)
    if pre_period <= 0.0 or post_period <= 0.0:
        return None
    rel_change = abs(post_period - pre_period) / max(pre_period, post_period)
    return ref_edges[step_idx + 1], pre_period, post_period, rel_change


def _logic_high_fraction(
    rows: list[dict[str, float]],
    signal: str,
    threshold: float,
    start: float,
    stop: float,
) -> float:
    if stop <= start:
        return 0.0
    high_dt = 0.0
    total_dt = 0.0
    for prev, cur in zip(rows, rows[1:]):
        t0 = prev["time"]
        t1 = cur["time"]
        left = max(start, t0)
        right = min(stop, t1)
        if right <= left:
            continue
        total_dt += right - left
        if 0.5 * (prev[signal] + cur[signal]) > threshold:
            high_dt += right - left
    return high_dt / total_dt if total_dt > 0.0 else 0.0


def _check_cppll_freq_step_reacquire(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "ref_clk", "fb_clk", "lock", "vctrl_mon"}
    missing = require_signals(rows, required, "P_REFERENCE_PERIOD_STEP")
    if missing:
        return False, missing

    vth = 0.45
    ref_edges = crossings(rows, "ref_clk", threshold=vth, direction="rising")
    fb_edges = crossings(rows, "fb_clk", threshold=vth, direction="rising")
    if len(ref_edges) < 12 or len(fb_edges) < 12:
        return False, diagnostic(
            "P_REFERENCE_PERIOD_STEP",
            "invalid_trace",
            expected="at_least_12_ref_and_fb_edges",
            observed=f"ref={len(ref_edges)},fb={len(fb_edges)}",
            event="full_trace",
        )

    step = _reference_step(ref_edges)
    if step is None:
        return False, diagnostic(
            "P_REFERENCE_PERIOD_STEP",
            "behavior_mismatch",
            expected="observable_reference_period_step",
            observed="period_step_not_detected",
            event="ref_clk_edges",
        )
    step_t, pre_period, post_period, rel_change = step
    if rel_change < 0.005:
        return False, diagnostic(
            "P_REFERENCE_PERIOD_STEP",
            "behavior_mismatch",
            expected="reference_period_relative_change>=0.005",
            observed=f"relative_change={rel_change:.4f}",
            event=event_label("ref_period_step", 0, step_t),
        )

    late_after = step_t + 6.0 * post_period
    ref_late_period, ref_late_edges = _tail_period(ref_edges, after=late_after)
    fb_late_period, fb_late_edges = _tail_period(fb_edges, after=late_after)
    if ref_late_period is None or fb_late_period is None:
        return False, diagnostic(
            "P_FEEDBACK_DIVISION",
            "invalid_trace",
            expected="late_ref_and_fb_periods_after_reference_step",
            observed=f"ref_late_edges={ref_late_edges},fb_late_edges={fb_late_edges}",
            event=event_label("ref_period_step", 0, step_t),
        )
    freq_ratio = ref_late_period / fb_late_period

    lock_rises = crossings(rows, "lock", threshold=vth, direction="rising")
    lock_falls = crossings(rows, "lock", threshold=vth, direction="falling")
    pre_stop = max(rows[0]["time"], step_t - pre_period)
    pre_lock_high = _logic_high_fraction(rows, "lock", vth, rows[0]["time"], pre_stop)
    disturb_start = next((edge for edge in lock_falls if edge >= step_t - pre_period), None)
    if disturb_start is None:
        disturb_start = next(
            (
                row["time"]
                for row in rows
                if row["time"] >= step_t and row["lock"] <= vth
            ),
            None,
        )
    if disturb_start is None:
        return False, diagnostic(
            "P_DISTURBANCE_UNLOCK",
            "behavior_mismatch",
            expected="lock_low_event_after_reference_step",
            observed="no_lock_low_event",
            event=event_label("ref_period_step", 0, step_t),
        )
    relock_time = next(
        (edge for edge in lock_rises if edge > disturb_start + 0.5 * post_period),
        None,
    )
    disturb_stop = (
        relock_time
        if relock_time is not None
        else min(rows[-1]["time"], disturb_start + 12.0 * post_period)
    )
    disturb_low_frac = 1.0 - _logic_high_fraction(rows, "lock", vth, disturb_start, disturb_stop)
    relock_fall = (
        next(
            (
                edge
                for edge in lock_falls
                if relock_time is not None and edge > relock_time + 0.25 * post_period
            ),
            None,
        )
        if relock_time is not None
        else None
    )
    relock_stop = (
        min(rows[-1]["time"], relock_time + 12.0 * post_period)
        if relock_time is not None and relock_fall is None
        else relock_fall
    )
    relock_high_duration = (
        max(0.0, relock_stop - relock_time)
        if relock_time is not None and relock_stop is not None
        else 0.0
    )

    vctrl_vals = [row["vctrl_mon"] for row in rows]
    vctrl_min = min(vctrl_vals)
    vctrl_max = max(vctrl_vals)
    vctrl_span = vctrl_max - vctrl_min
    vctrl_in_range = all(-1e-6 <= value <= 0.95 for value in vctrl_vals)

    if pre_lock_high < 0.60:
        return False, diagnostic(
            "P_INITIAL_LOCK_ACQUISITION",
            "behavior_mismatch",
            expected="pre_step_lock_high_fraction>=0.60",
            observed=f"pre_lock_high={pre_lock_high:.3f}",
            event=event_label("pre_step_window", 0, rows[0]["time"]),
        )
    if disturb_low_frac < 0.25:
        return False, diagnostic(
            "P_DISTURBANCE_UNLOCK",
            "behavior_mismatch",
            expected="post_step_lock_low_fraction>=0.25",
            observed=f"disturb_low_frac={disturb_low_frac:.3f}",
            event=event_label("lock_disturbance", 0, disturb_start),
        )
    if relock_time is None or relock_high_duration < 0.5 * post_period:
        return False, diagnostic(
            "P_LATE_REACQUISITION",
            "behavior_mismatch",
            expected="observable_relock_with_high_duration>=0.5_post_period",
            observed=f"relock_time={relock_time},high_duration={relock_high_duration:.3e}",
            event=event_label("lock_disturbance", 0, disturb_start),
        )
    if not (0.97 <= freq_ratio <= 1.03):
        return False, diagnostic(
            "P_FEEDBACK_DIVISION",
            "behavior_mismatch",
            expected="0.97<=late_ref_to_fb_period_ratio<=1.03",
            observed=f"freq_ratio={freq_ratio:.4f}",
            event=event_label("late_tracking", 0, late_after),
        )
    if not vctrl_in_range or vctrl_span < 0.02:
        return False, diagnostic(
            "P_BOUNDED_TRACKING_CONTROL",
            "behavior_mismatch",
            expected="vctrl_in_range_and_span>=0.02",
            observed=f"vctrl_min={vctrl_min:.3f},vctrl_max={vctrl_max:.3f},span={vctrl_span:.3f}",
            event=event_label("full_trace", 0, rows[0]["time"]),
        )

    return True, pass_note(
        PROPERTY_IDS,
        f"cppll_freq_step step_t={step_t:.3e} period={pre_period:.3e}->{post_period:.3e} "
        f"freq_ratio={freq_ratio:.4f} disturb_low_frac={disturb_low_frac:.3f} "
        f"initial_lock_high={pre_lock_high:.3f} relock_time={relock_time:.3e} "
        f"relock_high_duration={relock_high_duration:.3e} vctrl_span={vctrl_span:.3f}",
    )


def _stream_cppll_freq_step_reacquire_csv(csv_path: Path) -> tuple[float, list[str]]:
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fields = set(reader.fieldnames or [])
        required = {"time", "ref_clk", "fb_clk", "lock", "vctrl_mon"}
        missing = sorted(required - fields)
        if missing:
            return 0.0, [
                diagnostic(
                    "P_REFERENCE_PERIOD_STEP",
                    "invalid_trace",
                    expected="signals:" + ",".join(sorted(required)),
                    observed="missing:" + ",".join(missing),
                    event="full_trace",
                )
            ]
        rows = [
            {
                "time": float(row.get("time", 0.0) or 0.0),
                "ref_clk": float(row.get("ref_clk", 0.0) or 0.0),
                "fb_clk": float(row.get("fb_clk", 0.0) or 0.0),
                "lock": float(row.get("lock", 0.0) or 0.0),
                "vctrl_mon": float(row.get("vctrl_mon", 0.0) or 0.0),
            }
            for row in reader
        ]
    ok, note = _check_cppll_freq_step_reacquire(rows)
    return (1.0 if ok else 0.0), [note]


def check_cppll_freq_step_reacquire(rows: list[dict[str, float]]) -> tuple[bool, str]:
    return _check_cppll_freq_step_reacquire(rows)


CHECKER_ID = "v4_088_cppll_tracking_reacquire_timer"
CHECKER: Checker = check_cppll_freq_step_reacquire
STREAMING_CHECKER = _stream_cppll_freq_step_reacquire_csv
