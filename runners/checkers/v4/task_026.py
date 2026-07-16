"""Stimulus-relative checker for canonical v4 DUT 026."""
from __future__ import annotations

from statistics import median

from ..api import Checker
from .stimulus_relative import finish, missing_trace, row_at_or_after


PROPERTY_IDS = [
    "P_TIMER_INCREMENT",
    "P_MODULO_WRAP",
    "P_PHASE_RAIL_SCALING",
    "P_PHASE_DERIVED_CLOCK",
    "P_PARAMETERIZED_PERIOD",
]


def _normalized_phase(row: dict[str, float]) -> float:
    span = row["VDD"] - row["VSS"]
    if span <= 1e-12:
        return 0.0
    return (row["phase_out"] - row["VSS"]) / span


def _phase_transition_groups(rows: list[dict[str, float]]) -> list[list[int]]:
    changed = [
        index
        for index in range(1, len(rows))
        if abs(_normalized_phase(rows[index]) - _normalized_phase(rows[index - 1])) > 0.002
    ]
    groups: list[list[int]] = []
    for index in changed:
        if not groups or index - groups[-1][-1] > 3:
            groups.append([index])
        else:
            groups[-1].append(index)
    return groups


def check_phase_accumulator_timer_wrap(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "VDD", "VSS", "clk_out", "phase_out"}
    results, error = missing_trace(CHECKER_ID, rows, required, PROPERTY_IDS)
    if error is not None:
        return error
    by_id = {result.property_id: result for result in results}

    groups = _phase_transition_groups(rows)
    event_times = [float(rows[group[0]]["time"]) for group in groups]
    plateaus: list[tuple[float, dict[str, float]]] = []
    for position, group in enumerate(groups):
        start = float(rows[group[-1]]["time"])
        stop = (
            float(rows[groups[position + 1][0]]["time"])
            if position + 1 < len(groups)
            else float(rows[-1]["time"])
        )
        sample = row_at_or_after(rows, start + 0.50 * max(0.0, stop - start))
        plateaus.append((_normalized_phase(sample), sample))

    initial_phase = _normalized_phase(rows[max(0, groups[0][0] - 1)]) if groups else 0.0
    phases = [initial_phase, *(phase for phase, _ in plateaus)]
    increments = [
        (current - previous) % 1.0
        for previous, current in zip(phases, phases[1:])
    ]
    useful_increments = [value for value in increments if value > 0.01]
    inferred_step = median(useful_increments) if useful_increments else 0.0
    step_tolerance = max(0.025, 0.12 * inferred_step)

    for (phase, sample), increment in zip(plateaus, increments):
        by_id["P_TIMER_INCREMENT"].compare(
            expected=inferred_step,
            observed=increment,
            tolerance=step_tolerance,
            time_s=sample["time"],
            label="normalized_increment",
        )
        by_id["P_PHASE_RAIL_SCALING"].condition(
            -0.025 <= phase <= 1.025,
            expected="normalized_phase_in_[0,1)",
            observed=f"normalized_phase={phase:.6g}",
            time_s=sample["time"],
            gap=max(-phase, phase - 1.0, 0.0),
        )
        expected_clk = sample["VDD"] if phase < 0.5 else sample["VSS"]
        by_id["P_PHASE_DERIVED_CLOCK"].compare(
            expected=expected_clk,
            observed=sample["clk_out"],
            tolerance=0.06,
            time_s=sample["time"],
            label="derived_clk",
        )

    wraps = sum(
        1 for previous, current in zip(phases, phases[1:]) if current < previous - 0.25
    )
    by_id["P_MODULO_WRAP"].condition(
        wraps >= 2 and all(-0.025 <= phase <= 1.025 for phase in phases),
        expected="at_least_2_bounded_wraps",
        observed=f"wraps={wraps}",
        time_s=event_times[-1] if event_times else 0.0,
        gap=max(0, 2 - wraps),
    )

    spacings = [right - left for left, right in zip(event_times, event_times[1:])]
    cadence = median(spacings) if spacings else 0.0
    cadence_error = max((abs(value - cadence) for value in spacings), default=float("inf"))
    cadence_tolerance = 0.08 * cadence if cadence > 0.0 else 0.0
    by_id["P_PARAMETERIZED_PERIOD"].condition(
        len(spacings) >= 4
        and 0.01 < inferred_step < 1.0
        and cadence > 0.0
        and cadence_error <= cadence_tolerance,
        expected="stable_positive_timer_cadence_and_step",
        observed=(
            f"events={len(event_times)},cadence={cadence:.6g},"
            f"max_gap_error={cadence_error:.6g},step={inferred_step:.6g}"
        ),
        time_s=event_times[-1] if event_times else 0.0,
        gap=cadence_error,
    )
    return finish(
        CHECKER_ID,
        results,
        coverage=(
            f"timer_events={len(event_times)} wraps={wraps} "
            f"inferred_step={inferred_step:.6g} cadence_s={cadence:.6g}"
        ),
    )


CHECKER_ID = "v4_026_digital_phase_accumulator_with_modulo_wrap"
CHECKER: Checker = check_phase_accumulator_timer_wrap
