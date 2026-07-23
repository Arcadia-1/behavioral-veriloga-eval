"""Task-specific checker for canonical v4 DUT 195."""
from __future__ import annotations

from statistics import median

from ..api import Checker, Row
from .trace_utils import property_diagnostics

SIGNALS = ["rst", "s", "nc", "res", "conv"]
PROPERTIES = {
    "P_PERIODIC_16NS_FRAME": 0,
    "P_RESET_AND_SAMPLE_WINDOWS": 0,
    "P_NONOVERLAP_AND_RESIDUE_WINDOWS": 0,
    "P_CONVERSION_OUTPUT_TIMING": 0,
}
EXPECTED_WINDOWS = {
    "rst": [(0.0, 0.2, "P_RESET_AND_SAMPLE_WINDOWS")],
    "s": [
        (1.0, 1.8, "P_RESET_AND_SAMPLE_WINDOWS"),
        (9.0, 9.8, "P_RESET_AND_SAMPLE_WINDOWS"),
    ],
    "nc": [
        (2.0, 2.25, "P_NONOVERLAP_AND_RESIDUE_WINDOWS"),
        (10.0, 10.25, "P_NONOVERLAP_AND_RESIDUE_WINDOWS"),
    ],
    "res": [
        (3.0, 3.25, "P_NONOVERLAP_AND_RESIDUE_WINDOWS"),
        (4.5, 4.75, "P_NONOVERLAP_AND_RESIDUE_WINDOWS"),
        (6.0, 6.25, "P_NONOVERLAP_AND_RESIDUE_WINDOWS"),
        (7.5, 7.75, "P_NONOVERLAP_AND_RESIDUE_WINDOWS"),
    ],
    "conv": [
        (3.0, 7.0, "P_CONVERSION_OUTPUT_TIMING"),
        (11.0, 15.0, "P_CONVERSION_OUTPUT_TIMING"),
    ],
}
SIGNAL_LEVEL_PROPERTY = {
    "rst": "P_RESET_AND_SAMPLE_WINDOWS",
    "s": "P_RESET_AND_SAMPLE_WINDOWS",
    "nc": "P_NONOVERLAP_AND_RESIDUE_WINDOWS",
    "res": "P_NONOVERLAP_AND_RESIDUE_WINDOWS",
    "conv": "P_CONVERSION_OUTPUT_TIMING",
}
TIMING_TOLERANCE_FRACTION = 0.015
PERIOD_TOLERANCE_FRACTION = 0.03
TRACE_COVERAGE_EPSILON_FRACTION = 1e-6
# The sibling DUT/bugfix canonical decks stop at 12 ns, where ten complete
# windows are observable.  Coverage counts only complete physical windows;
# v4-695's longer canonical deck observes the remaining conversion edge too.
MIN_CHECKED_WINDOWS = 10


def _high_intervals(rows: list[Row], signal: str, threshold: float) -> list[tuple[float, float]]:
    intervals: list[tuple[float, float]] = []
    is_high = rows[0][signal] >= threshold
    start = rows[0]["time"] if is_high else None
    for index in range(1, len(rows)):
        previous = rows[index - 1]
        current = rows[index]
        t0 = previous["time"]
        t1 = current["time"]
        v0 = previous[signal]
        v1 = current[signal]
        if v0 < threshold <= v1:
            if v1 == v0:
                start = t1
            else:
                alpha = (threshold - v0) / (v1 - v0)
                start = t0 + alpha * (t1 - t0)
            is_high = True
        elif v0 >= threshold > v1:
            if start is None:
                start = t0
            if v1 == v0:
                end = t1
            else:
                alpha = (threshold - v0) / (v1 - v0)
                end = t0 + alpha * (t1 - t0)
            intervals.append((start, end))
            start = None
            is_high = False
    if is_high and start is not None:
        intervals.append((start, rows[-1]["time"]))
    return intervals


def _overlap(a: tuple[float, float], b: tuple[float, float]) -> float:
    return max(0.0, min(a[1], b[1]) - max(a[0], b[0]))


def _best_interval(
    intervals: list[tuple[float, float]],
    expected: tuple[float, float],
    tolerance: float,
) -> tuple[float, float] | None:
    expanded = (expected[0] - tolerance, expected[1] + tolerance)
    candidates = [interval for interval in intervals if _overlap(interval, expanded) > 0.0]
    if not candidates:
        return None
    return max(candidates, key=lambda interval: _overlap(interval, expanded))


def _infer_period_and_origin(intervals: dict[str, list[tuple[float, float]]]) -> tuple[float, float]:
    rst_starts = [start for start, _ in intervals["rst"]]
    s_starts = [start for start, _ in intervals["s"]]
    candidates: list[float] = []
    candidates.extend(
        rst_starts[index] - rst_starts[index - 1]
        for index in range(1, len(rst_starts))
        if rst_starts[index] > rst_starts[index - 1]
    )
    candidates.extend(
        2.0 * (s_starts[index] - s_starts[index - 1])
        for index in range(1, len(s_starts))
        if s_starts[index] > s_starts[index - 1]
    )
    period = median(candidates) if candidates else 16e-9
    origin = rst_starts[0] if rst_starts else (s_starts[0] - period / 16.0)
    return period, origin


def check_v3_clock_sample_1600n_sequencer(rows: list[Row]) -> tuple[bool, str]:
    required = {"time", *SIGNALS}
    if not rows or not required.issubset(rows[0]):
        return False, "missing clock sample 1600n sequencer signals"

    rail_hi = max(max(row[signal] for row in rows) for signal in SIGNALS)
    if rail_hi < 0.85:
        return (
            False,
            "insufficient_excitation clock_sample_1600n_sequencer "
            f"rail_hi={rail_hi:.4g}",
        )
    threshold = 0.5 * rail_hi
    intervals = {
        signal: _high_intervals(rows, signal, threshold)
        for signal in SIGNALS
    }
    if not intervals["s"] or not intervals["conv"]:
        return (
            False,
            "insufficient_excitation clock_sample_1600n_sequencer "
            f"s_intervals={len(intervals['s'])} conv_intervals={len(intervals['conv'])}",
        )

    period, origin = _infer_period_and_origin(intervals)
    tolerance = period * TIMING_TOLERANCE_FRACTION
    coverage_epsilon = max(1e-15, period * TRACE_COVERAGE_EPSILON_FRACTION)
    counts = dict(PROPERTIES)
    checked = 0
    max_timing_err = 0.0
    trace_start = rows[0]["time"]
    trace_end = rows[-1]["time"]

    for signal in SIGNALS:
        signal_high = max(row[signal] for row in rows)
        if intervals[signal] and signal_high < 0.85:
            counts[SIGNAL_LEVEL_PROPERTY[signal]] += 1

    if abs(period - 16e-9) > PERIOD_TOLERANCE_FRACTION * 16e-9:
        counts["P_PERIODIC_16NS_FRAME"] += 1

    frame = origin
    while frame <= trace_end + coverage_epsilon:
        for signal, windows in EXPECTED_WINDOWS.items():
            for start_ns, end_ns, property_id in windows:
                expected_start = frame + period * (start_ns / 16.0)
                expected_end = frame + period * (end_ns / 16.0)
                if (
                    expected_start < trace_start - coverage_epsilon
                    or expected_end > trace_end + coverage_epsilon
                ):
                    continue
                observed = _best_interval(
                    intervals[signal],
                    (expected_start, expected_end),
                    tolerance,
                )
                checked += 1
                if observed is None:
                    counts[property_id] += 1
                    continue
                if expected_start >= trace_start + tolerance:
                    start_err = abs(observed[0] - expected_start)
                    max_timing_err = max(max_timing_err, start_err)
                    if start_err > tolerance:
                        counts[property_id] += 1
                if expected_end <= trace_end - tolerance:
                    end_err = abs(observed[1] - expected_end)
                    max_timing_err = max(max_timing_err, end_err)
                    if end_err > tolerance:
                        counts[property_id] += 1
        frame += period

    if checked < MIN_CHECKED_WINDOWS:
        return (
            False,
            "insufficient_excitation clock_sample_1600n_sequencer "
            f"checked_windows={checked}",
        )

    ok = all(count == 0 for count in counts.values())
    return (
        ok,
        f"{property_diagnostics(counts)}; checked_windows={checked}; "
        f"frame_period_ns={period * 1e9:.6g}; max_timing_err_ns={max_timing_err * 1e9:.6g}",
    )


CHECKER_ID = "v4_195_clock_sample_1600n_sequencer"
CHECKER: Checker = check_v3_clock_sample_1600n_sequencer
