"""Stimulus-relative checker for canonical v4 DUT 012."""

from __future__ import annotations

from ..api import Checker, Row
from .trace_utils import (
    property_diagnostics,
    stable_logic_plateaus,
    threshold_crossings,
)


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
    plateaus = stable_logic_plateaus(active, bits, minimum_duration_s=0.0)
    segment_notes: list[str] = []
    tested_ratios: list[int] = []
    period_errors = 0
    period_coverage_errors = 0
    duty_errors = 0
    odd_duty_coverage_errors = 0
    lock_errors = 0
    code_changes = 0
    previous_vector: tuple[int, ...] | None = None

    for begin, end, vector in plateaus:
        ratio = sum((1 << index) * bit for index, bit in enumerate(vector)) or 1
        changed = previous_vector is not None and vector != previous_vector
        code_changes += int(changed)
        previous_vector = vector
        segment = active[begin : end + 1]
        in_rises = threshold_crossings(segment, "clk_in", direction=1)
        minimum_edges = max(8, 2 * ratio + 3)
        if len(in_rises) < minimum_edges:
            segment_notes.append(f"ratio={ratio}:short({len(in_rises)})")
            continue

        # A ratio change resets divider phase and lock.  Analyze only after
        # one complete new-ratio period so boundary transitions cannot be
        # mistaken for steady-state behavior while short valid tests still
        # retain enough cycles for period measurement.
        settle_edge = in_rises[min(len(in_rises) - 1, ratio + 1)]
        steady = [row for row in segment if row["time"] >= settle_edge]
        steady_in_rises = threshold_crossings(steady, "clk_in", direction=1)
        out_rises = threshold_crossings(steady, "clk_out", direction=1)
        out_falls = threshold_crossings(steady, "clk_out", direction=-1)
        output_transitions = sorted(out_rises + out_falls)
        periods = [
            sum(left < edge <= right for edge in steady_in_rises)
            for left, right in zip(out_rises, out_rises[1:])
        ]
        phases = [
            sum(left < edge <= right for edge in steady_in_rises)
            for left, right in zip(output_transitions, output_transitions[1:])
        ]
        tested_ratios.append(ratio)
        period_errors += sum(interval != ratio for interval in periods)
        period_coverage_errors += int(len(periods) < 2)

        if ratio > 1:
            allowed_phases = {max(1, ratio // 2), ratio - ratio // 2}
            duty_errors += sum(interval not in allowed_phases for interval in phases)
            if ratio % 2:
                odd_duty_coverage_errors += int(
                    not allowed_phases.issubset(set(phases))
                )

        lock_rises = threshold_crossings(segment, "lock", direction=1)
        lock_errors += int(segment[-1]["lock"] <= 0.45)
        if changed and ratio > 1:
            lock_errors += int(not lock_rises)
        segment_notes.append(
            f"ratio={ratio}:in={len(in_rises)},out={len(out_rises)},"
            f"period_err={sum(interval != ratio for interval in periods)}"
        )

    distinct_ratios = set(tested_ratios)
    ratio_coverage_missing = (
        int(not reset_segments)
        + int(not distinct_ratios)
        + int(not any(ratio > 1 for ratio in distinct_ratios))
    )
    odd_coverage_missing = int(not any(ratio > 1 and ratio % 2 for ratio in distinct_ratios))
    reacquire_coverage_missing = int(code_changes == 0 and len(reset_segments) < 2)
    coverage_missing = (
        ratio_coverage_missing
        + period_coverage_errors
        + odd_coverage_missing
        + odd_duty_coverage_errors
        + reacquire_coverage_missing
    )
    counts = {
        "P_RESET": reset_errors + int(not reset_segments),
        "P_RATIO_DECODE": period_errors + ratio_coverage_missing,
        "P_DIVIDED_PERIOD": period_errors + period_coverage_errors,
        "P_ODD_RATIO_DUTY": duty_errors + odd_coverage_missing + odd_duty_coverage_errors,
        "P_LOCK_REACQUIRE": lock_errors + reacquire_coverage_missing,
    }
    ok = coverage_missing == 0 and all(count == 0 for count in counts.values())
    coverage = "" if coverage_missing == 0 else f" insufficient_excitation={coverage_missing}"
    return ok, (
        f"ratios={tested_ratios} reset_segments={len(reset_segments)} "
        f"code_changes={code_changes} segments={segment_notes}{coverage}; "
        f"{property_diagnostics(counts)}"
    )


CHECKER_ID = "v4_012_clock_divider"
CHECKER: Checker = check_v4_clock_divider
