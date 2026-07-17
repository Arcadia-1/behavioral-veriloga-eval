"""Stimulus-relative checker for canonical v4 DUT 012."""

from __future__ import annotations

from ..api import Checker, Row
from .trace_utils import property_diagnostics, threshold_crossings


def check_v4_clock_divider(rows: list[Row]) -> tuple[bool, str]:
    bits = [f"div_code_{index}" for index in range(8)]
    required = {"time", "clk_in", "rst_n", "clk_out", "lock", *bits}
    missing = sorted(required - (set(rows[0]) if rows else set()))
    if missing:
        return False, "missing_columns=" + ",".join(missing)

    reset_segments: list[tuple[int, int]] = []
    start: int | None = None
    for index, row in enumerate(rows):
        low = row["rst_n"] < 0.2
        if low and start is None:
            start = index
        elif not low and start is not None:
            reset_segments.append((start, index - 1))
            start = None
    if start is not None:
        reset_segments.append((start, len(rows) - 1))

    reset_errors = 0
    for begin, end in reset_segments:
        settle = begin + max(1, (end - begin) // 3)
        reset_errors += sum(max(row["clk_out"], row["lock"]) > 0.12 for row in rows[settle : end + 1])

    analysis_start = reset_segments[-1][1] + 1 if reset_segments else len(rows)
    active = rows[analysis_start:]
    ratio = (
        sum(
            (1 << index)
            for index, bit in enumerate(bits)
            if active and active[-1][bit] > 0.45
        )
        or 1
    )
    in_rises = threshold_crossings(active, "clk_in", direction=1) if active else []
    out_rises = threshold_crossings(active, "clk_out", direction=1) if active else []
    out_falls = threshold_crossings(active, "clk_out", direction=-1) if active else []
    output_transitions = sorted(out_rises + out_falls)

    period_intervals = [
        sum(left < edge <= right for edge in in_rises)
        for left, right in zip(out_rises, out_rises[1:])
    ]
    period_errors = sum(interval != ratio for interval in period_intervals)
    phase_intervals = [
        sum(left < edge <= right for edge in in_rises)
        for left, right in zip(output_transitions, output_transitions[1:])
    ]
    allowed_phases = {max(1, ratio // 2), max(1, ratio - ratio // 2)}
    duty_errors = sum(interval not in allowed_phases for interval in phase_intervals)
    duty_coverage = ratio % 2 == 0 or allowed_phases.issubset(set(phase_intervals))
    lock_high = bool(active) and active[-1]["lock"] > 0.45
    lock_edges = threshold_crossings(active, "lock", direction=1) if active else []
    lock_errors = int(not lock_high) + int(len(out_rises) >= 2 and not lock_edges)

    coverage_missing = (
        int(not reset_segments)
        + int(len(in_rises) < max(8, 2 * ratio))
        + int(len(out_rises) < 3)
        + int(not duty_coverage)
    )
    counts = {
        "P_RESET": reset_errors + int(not reset_segments),
        "P_RATIO_DECODE": period_errors + coverage_missing,
        "P_DIVIDED_PERIOD": period_errors + int(len(period_intervals) < 2),
        "P_ODD_RATIO_DUTY": duty_errors + int(not duty_coverage),
        "P_LOCK_REACQUIRE": lock_errors + int(len(reset_segments) < 2),
    }
    ok = coverage_missing == 0 and all(count == 0 for count in counts.values())
    coverage = "" if coverage_missing == 0 else f" insufficient_excitation={coverage_missing}"
    return ok, (
        f"ratio={ratio} reset_segments={len(reset_segments)} in_rises={len(in_rises)} "
        f"out_rises={len(out_rises)} periods={period_intervals} phases={phase_intervals} "
        f"lock_edges={len(lock_edges)}{coverage}; {property_diagnostics(counts)}"
    )


CHECKER_ID = "v4_012_clock_divider"
CHECKER: Checker = check_v4_clock_divider
