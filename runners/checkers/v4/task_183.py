"""Stimulus-relative checker for canonical v4 DUT 183."""
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
    "P_INITIAL_MSB_TRIAL_CODE",
    "P_CLOCKED_RDAC_DECISION_SEQUENCE",
    "P_DECISION_POLARITY",
    "P_CALIBRATION_COMPLETION",
    "P_RDAC_OUTPUT_LEVELS",
]


def _compare_outputs(
    results: list[PropertyResult],
    probe: dict[str, float],
    codes: list[int],
    active: bool,
    *,
    time_s: float,
    primary: PropertyResult,
) -> None:
    initial, sequence, polarity, completion, levels = results
    for bit, expected_bit in enumerate(codes):
        expected = float(expected_bit)
        observed = probe[f"dc{bit}"]
        primary.compare(
            expected=expected, observed=observed, tolerance=0.08,
            time_s=time_s, label=f"dc{bit}",
        )
        levels.condition(
            min(abs(observed), abs(observed - 1.0)) <= 0.08,
            expected="logic_rail_0_or_1", observed=f"dc{bit}={observed:.6g}",
            time_s=time_s,
        )
    completion.compare(
        expected=1.0 if active else 0.0,
        observed=probe["en"], tolerance=0.08, time_s=time_s, label="en",
    )
    completion.compare(
        expected=0.0 if active else 1.0,
        observed=probe["enb"], tolerance=0.08, time_s=time_s, label="enb",
    )
    sequence.compare(
        expected=probe["vrefp"], observed=probe["cvinp"], tolerance=0.02,
        time_s=time_s, label="cvinp_tracks_vrefp",
    )
    sequence.compare(
        expected=probe["vrefn"], observed=probe["cvinn"], tolerance=0.02,
        time_s=time_s, label="cvinn_tracks_vrefn",
    )


def check_v4_foreground_rdac_calibrator(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {
        "time", "ck", "d", "vrefp", "vrefn", "cvinp", "cvinn", "en", "enb",
        *{f"dc{bit}" for bit in range(7)},
    }
    results, missing = missing_trace("v4_183", rows, required, PROPERTY_IDS)
    if missing is not None:
        return missing
    initial, sequence, polarity, completion, _levels = results
    rises = edge_times(rows, "ck", threshold=0.5, rising=True)
    settle = event_settle_delay(rises)
    codes = [0, 0, 0, 0, 0, 0, 1]
    iteration = 6
    active = True
    decisions: set[int] = set()
    initial_delay = settle
    if rises:
        initial_delay = min(initial_delay, 0.4 * (rises[0] - rows[0]["time"]))
    initial_probe = row_at_or_after(rows, rows[0]["time"] + initial_delay)
    _compare_outputs(results, initial_probe, codes, active, time_s=initial_probe["time"], primary=initial)

    for edge in rises:
        before = row_before(rows, edge)
        decision_low = int(before["d"] < 0.5)
        if iteration > 0:
            decisions.add(decision_low)
            next_bit = iteration - 1
            codes[next_bit] = 1
            if not decision_low:
                codes[iteration] = 0
            iteration -= 1
            primary = polarity
        else:
            active = False
            primary = completion
        probe_time = edge + settle
        if probe_time > rows[-1]["time"]:
            continue
        probe = row_at_or_after(rows, probe_time)
        _compare_outputs(results, probe, codes, active, time_s=probe_time, primary=primary)

    sequence.condition(
        len(rises) >= 7,
        expected="clock_rises>=7",
        observed=f"clock_rises={len(rises)}",
        time_s=rows[-1]["time"],
    )
    polarity.condition(
        decisions == {0, 1},
        expected="decision_levels=low,high",
        observed=f"decision_levels={sorted(decisions)}",
        time_s=rows[-1]["time"],
    )
    completion.condition(
        not active,
        expected="calibration_complete",
        observed=f"active={active}",
        time_s=rows[-1]["time"],
    )
    return finish(
        "v4_183",
        results,
        coverage=f"clock_rises={len(rises)} decisions={sorted(decisions)} active={active}",
    )


CHECKER_ID = "v4_183_foreground_rdac_calibrator"
CHECKER: Checker = check_v4_foreground_rdac_calibrator
