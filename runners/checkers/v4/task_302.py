"""Task-specific checker for canonical v4 DUT 302."""
from __future__ import annotations

from bisect import bisect_right
import csv
from pathlib import Path
from statistics import median

from ..api import Checker
from ..common.relative_events import (
    rows_between,
    trace_bounds,
    weighted_logic_high_fraction,
)


def _rising_edges(rows: list[dict[str, float]], signal: str, threshold: float = 0.45) -> list[float]:
    edges: list[float] = []
    for previous, row in zip(rows, rows[1:]):
        before = float(previous.get(signal, 0.0))
        after = float(row.get(signal, 0.0))
        if before < threshold <= after:
            edges.append(float(row["time"]))
    return edges


def _period_step_anchor_from_edges(edges: list[float]) -> float | None:
    periods = [b - a for a, b in zip(edges, edges[1:]) if b > a]
    if len(periods) < 4:
        return None
    baseline = float(median(periods[: max(2, len(periods) // 4)]))
    for index, period in enumerate(periods):
        # Detect a physical period change independently of how densely a
        # simulator samples the trace.  Using sample_step here let a coarse
        # Spectre trace hide the declared 2.5% reference-clock step.
        if abs(period - baseline) > max(1e-15, baseline * 0.02):
            return edges[index + 1]
    return None


def _fractional_edge_metrics(
    ref_edges: list[float],
    fb_edges: list[float],
    dco_edges: list[float],
) -> tuple[dict[str, object] | None, str | None]:
    if len(ref_edges) < 5 or len(fb_edges) < 4 or len(dco_edges) < 20:
        return None, (
            f"not_enough_edges ref={len(ref_edges)} fb={len(fb_edges)} "
            f"dco={len(dco_edges)}"
        )

    step_anchor = _period_step_anchor_from_edges(ref_edges)
    if step_anchor is None:
        step_anchor = ref_edges[len(ref_edges) // 2]

    post_ref_edges = [time_s for time_s in ref_edges if time_s >= step_anchor]
    post_fb_edges = [time_s for time_s in fb_edges if time_s >= step_anchor]
    ref_tracking_edges = post_ref_edges[-4:] if len(post_ref_edges) >= 4 else ref_edges[-4:]
    fb_tracking_edges = post_fb_edges[-4:] if len(post_fb_edges) >= 4 else fb_edges[-4:]
    if len(ref_tracking_edges) < 3 or len(fb_tracking_edges) < 3:
        return None, (
            f"not_enough_tracking_edges ref={len(ref_tracking_edges)} "
            f"fb={len(fb_tracking_edges)}"
        )

    ref_periods = [b - a for a, b in zip(ref_tracking_edges, ref_tracking_edges[1:])]
    fb_periods = [b - a for a, b in zip(fb_tracking_edges, fb_tracking_edges[1:])]
    ref_period = sum(ref_periods) / len(ref_periods)
    fb_period = sum(fb_periods) / len(fb_periods)
    if ref_period <= 0.0 or fb_period <= 0.0:
        return None, "non_positive_period"
    freq_ratio = ref_period / fb_period

    dco_counts = [
        bisect_right(dco_edges, stop_t) - bisect_right(dco_edges, start_t)
        for start_t, stop_t in zip(fb_edges, fb_edges[1:])
    ]
    if len(dco_counts) < 3:
        return None, f"not_enough_dco_count_windows={len(dco_counts)}"
    avg_dco_per_fb = sum(dco_counts) / len(dco_counts)
    if not (14.5 <= avg_dco_per_fb <= 16.1):
        return None, (
            "dco_edges_per_fb_period_out_of_range "
            f"avg={avg_dco_per_fb:.3f} counts={dco_counts}"
        )
    if min(dco_counts) >= 16 or max(dco_counts) <= 15:
        return None, f"fractional_short_count_not_observed counts={dco_counts}"

    return {
        "step_anchor": step_anchor,
        "ref_period": ref_period,
        "freq_ratio": freq_ratio,
        "dco_counts": dco_counts,
        "avg_dco_per_fb": avg_dco_per_fb,
    }, None


def _fractional_lock_windows(
    metrics: dict[str, object],
    trace_start: float,
    trace_end: float,
) -> dict[str, tuple[float, float | None]]:
    step_anchor = float(metrics["step_anchor"])
    ref_period = float(metrics["ref_period"])
    disturb_end = min(trace_end, step_anchor + 3.0 * ref_period)
    reacquire_target = step_anchor + 3.0 * ref_period
    reacquire_start = min(
        reacquire_target,
        max(step_anchor, trace_end - 2.0 * ref_period),
    )
    return {
        "pre": (trace_start, step_anchor),
        "disturb": (step_anchor, disturb_end),
        "post": (reacquire_start, None),
    }


def _central_bounds(values: list[float]) -> tuple[float, float]:
    if not values:
        return 0.0, 0.0
    ordered = sorted(float(value) for value in values)
    if len(ordered) < 20:
        return ordered[0], ordered[-1]
    lower_index = max(0, int(0.05 * (len(ordered) - 1)))
    upper_index = min(len(ordered) - 1, int(0.95 * (len(ordered) - 1)))
    return ordered[lower_index], ordered[upper_index]


def _fractional_result(
    *,
    metrics: dict[str, object],
    ref_edges: list[float],
    dco_edges: list[float],
    lock_edges: list[float],
    lock_fractions: dict[str, float],
    post_start: float,
    vctrl_min: float,
    vctrl_max: float,
    vctrl_in_range: bool,
) -> tuple[bool, str]:
    step_anchor = float(metrics["step_anchor"])
    freq_ratio = float(metrics["freq_ratio"])
    dco_counts = list(metrics["dco_counts"])
    avg_dco_per_fb = float(metrics["avg_dco_per_fb"])

    pre_lock_frac = lock_fractions["pre"]
    post_lock_frac = lock_fractions["post"]
    pre_lock_edges = [time_s for time_s in lock_edges if time_s < step_anchor]
    post_lock_edges = [time_s for time_s in lock_edges if time_s >= post_start]
    disturb_low_frac = 1.0 - lock_fractions["disturb"]

    vctrl_span = vctrl_max - vctrl_min

    ok = (
        (bool(pre_lock_edges) or pre_lock_frac >= 0.20)
        and disturb_low_frac >= 0.20
        and (bool(post_lock_edges) or post_lock_frac >= 0.20)
        and 0.95 <= freq_ratio <= 1.05
        and vctrl_in_range
        and vctrl_span >= 0.01
    )
    diagnostics = {
        "P_USE_REF_CLK_AS_THE_REFERENCE": int(len(ref_edges) < 5),
        "P_GENERATE_A_BEHAVIORAL_DCO_CLOCK_ON": int(len(dco_edges) < 20),
        "P_GENERATE_FB_CLK_BY_TOGGLING_IT": int(not (14.5 <= avg_dco_per_fb <= 16.1 and min(dco_counts) < 16 and max(dco_counts) > 15)),
        "P_UPDATE_A_BOUNDED_CONTROL_VOLTAGE_MONITOR": int(not vctrl_in_range),
        "P_DRIVE_LOCK_HIGH_AFTER_STABLE_TRACKING": int(not ((pre_lock_edges or pre_lock_frac >= 0.20) and (post_lock_edges or post_lock_frac >= 0.20) and disturb_low_frac >= 0.20)),
    }
    return ok, (
        f"pre_lock_edges={len(pre_lock_edges)} pre_lock_frac={pre_lock_frac:.3f} "
        f"disturb_lock_low_frac={disturb_low_frac:.3f} "
        f"post_lock_edges={len(post_lock_edges)} post_lock_frac={post_lock_frac:.3f} "
        f"tracking_freq_ratio={freq_ratio:.4f} step_anchor={step_anchor:.4e} "
        f"dco_counts={dco_counts[:8]} avg_dco_per_fb={avg_dco_per_fb:.3f} "
        f"vctrl_min={vctrl_min:.3f} vctrl_max={vctrl_max:.3f} vctrl_span={vctrl_span:.3f}; "
        + "; ".join(f"{key} mismatch_count={value}" for key, value in diagnostics.items())
    )


def check_v3_505_fractional_n_divider_accumulator_flow(
    rows: list[dict[str, float]],
) -> tuple[bool, str]:
    required = {"time", "ref_clk", "fb_clk", "dco_clk", "lock", "vctrl_mon"}
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0].keys())) if rows else sorted(required)
        return False, "missing_columns=" + ",".join(missing)

    ref_edges = _rising_edges(rows, "ref_clk")
    fb_edges = _rising_edges(rows, "fb_clk")
    dco_edges = _rising_edges(rows, "dco_clk")
    metrics, error = _fractional_edge_metrics(ref_edges, fb_edges, dco_edges)
    if metrics is None:
        assert error is not None
        return False, error

    trace_start, trace_end, _ = trace_bounds(rows)
    windows = _fractional_lock_windows(metrics, trace_start, trace_end)
    lock_fractions = {
        name: weighted_logic_high_fraction(
            rows_between(rows, start, end),
            "lock",
            0.45,
        )
        for name, (start, end) in windows.items()
    }
    vctrl_vals = [row["vctrl_mon"] for row in rows]
    vctrl_central_min, vctrl_central_max = _central_bounds(vctrl_vals)
    return _fractional_result(
        metrics=metrics,
        ref_edges=ref_edges,
        dco_edges=dco_edges,
        lock_edges=_rising_edges(rows, "lock"),
        lock_fractions=lock_fractions,
        post_start=windows["post"][0],
        vctrl_min=vctrl_central_min,
        vctrl_max=vctrl_central_max,
        vctrl_in_range=all(-1e-6 <= value <= 0.95 for value in vctrl_vals),
    )


def _stream_lock_fractions(
    csv_path: Path,
    columns: dict[str, str],
    windows: dict[str, tuple[float, float | None]],
) -> dict[str, float]:
    totals = {name: 0.0 for name in windows}
    highs = {name: 0.0 for name in windows}
    previous_time: float | None = None
    previous_lock: float | None = None
    with csv_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            try:
                time_s = float(row[columns["time"]])
                lock = float(row[columns["lock"]])
            except (KeyError, TypeError, ValueError):
                continue
            if previous_time is not None and previous_lock is not None:
                dt = time_s - previous_time
                if dt > 0.0:
                    for name, (start, end) in windows.items():
                        if previous_time < start or (end is not None and time_s > end):
                            continue
                        totals[name] += dt
                        if 0.5 * (previous_lock + lock) > 0.45:
                            highs[name] += dt
            previous_time = time_s
            previous_lock = lock
    return {
        name: highs[name] / totals[name] if totals[name] else 0.0
        for name in windows
    }


def _stream_fractional_n_divider_accumulator_flow(
    csv_path: Path,
) -> tuple[float, list[str]]:
    required = {"time", "ref_clk", "fb_clk", "dco_clk", "lock", "vctrl_mon"}
    with csv_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        columns = {str(name).lower(): str(name) for name in (reader.fieldnames or [])}
        missing = sorted(required - set(columns))
        if missing:
            return 0.0, ["missing_columns=" + ",".join(missing)]

        ref_edges: list[float] = []
        fb_edges: list[float] = []
        dco_edges: list[float] = []
        lock_edges: list[float] = []
        previous: dict[str, float] | None = None
        trace_start: float | None = None
        trace_end: float | None = None
        vctrl_min = float("inf")
        vctrl_max = float("-inf")
        vctrl_values: list[float] = []
        vctrl_in_range = True
        for row in reader:
            try:
                current = {
                    name: float(row[column])
                    for name, column in columns.items()
                    if name in required
                }
            except (TypeError, ValueError):
                continue
            if set(current) != required:
                continue
            time_s = current["time"]
            if trace_start is None:
                trace_start = time_s
            trace_end = time_s
            vctrl = current["vctrl_mon"]
            vctrl_min = min(vctrl_min, vctrl)
            vctrl_max = max(vctrl_max, vctrl)
            vctrl_values.append(vctrl)
            vctrl_in_range = vctrl_in_range and -1e-6 <= vctrl <= 0.95
            if previous is not None:
                for signal, edges in (
                    ("ref_clk", ref_edges),
                    ("fb_clk", fb_edges),
                    ("dco_clk", dco_edges),
                    ("lock", lock_edges),
                ):
                    if previous[signal] < 0.45 <= current[signal]:
                        edges.append(time_s)
            previous = current

    if trace_start is None or trace_end is None:
        return 0.0, ["missing_columns=" + ",".join(sorted(required))]
    metrics, error = _fractional_edge_metrics(ref_edges, fb_edges, dco_edges)
    if metrics is None:
        assert error is not None
        return 0.0, [error]

    windows = _fractional_lock_windows(metrics, trace_start, trace_end)
    lock_fractions = _stream_lock_fractions(csv_path, columns, windows)
    vctrl_central_min, vctrl_central_max = _central_bounds(vctrl_values)
    ok, note = _fractional_result(
        metrics=metrics,
        ref_edges=ref_edges,
        dco_edges=dco_edges,
        lock_edges=lock_edges,
        lock_fractions=lock_fractions,
        post_start=windows["post"][0],
        vctrl_min=vctrl_central_min,
        vctrl_max=vctrl_central_max,
        vctrl_in_range=vctrl_in_range,
    )
    return (1.0 if ok else 0.0), [note]

CHECKER_ID = "v4_302_fractional_n_divider_accumulator_flow"
CHECKER: Checker = check_v3_505_fractional_n_divider_accumulator_flow
STREAMING_CHECKER = _stream_fractional_n_divider_accumulator_flow
