"""Stimulus-relative checker for canonical v4 DUT 184."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import (
    PropertyResult,
    edge_times,
    event_settle_delay,
    finish,
    missing_trace,
    row_at_or_after,
    row_before,
)


PROPERTY_IDS = [
    "P_TWO_PHASE_CLOCKED_FLOW",
    "P_REFERENCE_AND_CODE_INITIALIZATION",
    "P_RDAC_REFINEMENT_SEQUENCE",
    "P_OFFSET_SEARCH_BISECTION",
]


def _expected_outputs(vin: float, vref: float, codes: list[int]) -> dict[str, float]:
    values = {
        "vinp": 0.6 + 0.5 * vin,
        "vinn": 0.6 - 0.5 * vin,
        "vrefp": 0.6 + 0.5 * vref,
        "vrefn": 0.6 - 0.5 * vref,
    }
    values.update({f"dc{bit}": float(value) for bit, value in enumerate(codes)})
    return values


def _compare(
    result: PropertyResult,
    probe: dict[str, float],
    expected: dict[str, float],
    *,
    time_s: float,
) -> None:
    for signal, target in expected.items():
        result.compare(
            expected=target,
            observed=probe[signal],
            tolerance=0.025 if signal.startswith("v") else 0.08,
            time_s=time_s,
            label=signal,
        )


def check_v4_offset_rdac_search_flow(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {
        "time", "ck", "d", "vinp", "vinn", "vrefp", "vrefn",
        *{f"dc{bit}" for bit in range(7)},
    }
    results, missing = missing_trace("v4_184", rows, required, PROPERTY_IDS)
    if missing is not None:
        return missing
    flow_result, init_result, refinement_result, offset_result = results
    rises = edge_times(rows, "ck", threshold=0.5, rising=True)
    settle = event_settle_delay(rises)
    lsb = 1.0 / 16.0
    vref = -17.0 / 2.0 * lsb
    vin = vref
    step = 0.04
    state = 1
    iteration = 6
    offset_phase = False
    codes = [0, 0, 0, 0, 0, 0, 1]
    decisions: set[int] = set()
    offset_steps = 0
    phase_transitions = 0

    initial_delay = settle
    if rises:
        initial_delay = min(initial_delay, 0.4 * (rises[0] - rows[0]["time"]))
    initial_probe = row_at_or_after(rows, rows[0]["time"] + initial_delay)
    _compare(init_result, initial_probe, _expected_outputs(vin, vref, codes), time_s=initial_probe["time"])

    for edge in rises:
        decision = int(row_before(rows, edge)["d"] < 0.5)
        decisions.add(decision)
        if not offset_phase:
            if iteration > 0:
                next_bit = iteration - 1
                codes[next_bit] = 1
                if not decision:
                    codes[iteration] = 0
                iteration -= 1
                primary = refinement_result
            else:
                offset_phase = True
                iteration = 0
                step = 0.04
                phase_transitions += 1
                primary = flow_result
        elif iteration == 8:
            iteration = 6
            step = 0.04
            offset_phase = False
            phase_transitions += 1
            primary = flow_result
        else:
            if state != decision and step > 0.0:
                step /= 2.0
            state = decision
            vin += (2 * state - 1) * step
            iteration += 1
            offset_steps += 1
            if iteration == 8:
                vref += lsb
                vin = vref
                codes = [0, 0, 0, 0, 0, 0, 1]
            primary = offset_result
        probe_time = edge + settle
        if probe_time > rows[-1]["time"]:
            continue
        probe = row_at_or_after(rows, probe_time)
        expected = _expected_outputs(vin, vref, codes)
        _compare(primary, probe, expected, time_s=probe_time)
        _compare(flow_result, probe, expected, time_s=probe_time)

    flow_result.condition(
        phase_transitions >= 2,
        expected="enter_and_exit_offset_phase",
        observed=f"phase_transitions={phase_transitions}",
        time_s=rows[-1]["time"],
    )
    refinement_result.condition(
        len(rises) >= 17 and decisions == {0, 1},
        expected="clock_rises>=17_decisions=low,high",
        observed=f"clock_rises={len(rises)}_decisions={sorted(decisions)}",
        time_s=rows[-1]["time"],
    )
    offset_result.condition(
        offset_steps >= 8,
        expected="offset_steps>=8",
        observed=f"offset_steps={offset_steps}",
        time_s=rows[-1]["time"],
    )
    return finish(
        "v4_184",
        results,
        coverage=(
            f"clock_rises={len(rises)} decisions={sorted(decisions)} "
            f"offset_steps={offset_steps} phase_transitions={phase_transitions}"
        ),
    )


CHECKER_ID = "v4_184_offset_rdac_search_flow"
CHECKER: Checker = check_v4_offset_rdac_search_flow
