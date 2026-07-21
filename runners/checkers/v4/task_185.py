"""Stimulus-relative checker for canonical v4 DUT 185."""
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
    "P_RESET_LOADS_DEFAULT_WORD",
    "P_SHIFT_ON_SCKI_TRANSITIONS",
    "P_SHIFT_DIRECTION_AND_SDI_INSERTION",
    "P_SDO_EXPOSES_SHIFTED_OUT_BIT",
    "P_OUTPUT_RAIL_LEVELS",
]
DEFAULT_BITS = [0, 1, 0, 0, 1, 1, 0, 1]


def check_v4_spi_shift_mux(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {
        "time", "scki", "sdi", "rst", "sdo", "scko",
        *{f"out{bit}" for bit in range(8)},
    }
    results, missing = missing_trace("v4_185", rows, required, PROPERTY_IDS)
    if missing is not None:
        return missing
    reset_result, shift_result, direction_result, sdo_result, levels_result = results
    rises = edge_times(rows, "scki", threshold=0.45, rising=True)
    falls = edge_times(rows, "scki", threshold=0.45, rising=False)
    reset_rises = edge_times(rows, "rst", threshold=0.45, rising=True)
    events = sorted(
        [(time_s, "rise") for time_s in rises]
        + [(time_s, "fall") for time_s in falls]
        + [(time_s, "reset") for time_s in reset_rises]
    )
    settle = event_settle_delay([time_s for time_s, _ in events])
    bits = list(DEFAULT_BITS)
    sdi_values: set[int] = set()
    reset_checks = 0
    reset_clock_checks = 0
    shift_checks = 0

    initial_probe = row_at_or_after(rows, rows[0]["time"] + settle)
    for bit, expected_bit in enumerate(bits):
        reset_result.compare(
            expected=0.9 * expected_bit,
            observed=initial_probe[f"out{bit}"],
            tolerance=0.08,
            time_s=initial_probe["time"],
            label=f"initial_out{bit}",
        )
    reset_checks += 1

    for event_time, kind in events:
        before = row_before(rows, event_time)
        if kind == "reset" or before["rst"] > 0.45:
            bits = list(DEFAULT_BITS)
            result = reset_result
            reset_checks += 1
            if kind in {"rise", "fall"}:
                reset_clock_checks += 1
        else:
            incoming = int(before["sdi"] > 0.45)
            sdi_values.add(incoming)
            bits = [incoming, *bits[:7]]
            result = shift_result
            shift_checks += 1
        probe_time = event_time + settle
        if probe_time > rows[-1]["time"]:
            continue
        probe = row_at_or_after(rows, probe_time)
        for bit, expected_bit in enumerate(bits):
            expected = 0.9 * expected_bit
            result.compare(
                expected=expected,
                observed=probe[f"out{bit}"],
                tolerance=0.08,
                time_s=probe_time,
                label=f"out{bit}",
            )
            direction_result.compare(
                expected=expected,
                observed=probe[f"out{bit}"],
                tolerance=0.08,
                time_s=probe_time,
                label=f"shifted_out{bit}",
            )
            levels_result.condition(
                min(abs(probe[f"out{bit}"]), abs(probe[f"out{bit}"] - 0.9)) <= 0.08,
                expected="logic_rail_0_or_0.9",
                observed=f"out{bit}={probe[f'out{bit}']:.6g}",
                time_s=probe_time,
            )
        sdo_result.compare(
            expected=0.9 * bits[7],
            observed=probe["sdo"],
            tolerance=0.08,
            time_s=probe_time,
            label="sdo_out7",
        )
        if kind in {"rise", "fall"}:
            expected_scko = 0.9 if kind == "rise" else 0.0
            shift_result.compare(
                expected=expected_scko,
                observed=probe["scko"],
                tolerance=0.08,
                time_s=probe_time,
                label="scko",
            )

    reset_result.condition(
        reset_checks >= 2,
        expected="initial_plus_reset_reload",
        observed=f"reset_checks={reset_checks}",
        time_s=rows[-1]["time"],
    )
    reset_result.condition(
        reset_clock_checks >= 2,
        expected="clock_edges_while_reset_high>=2",
        observed=f"reset_clock_checks={reset_clock_checks}",
        time_s=rows[-1]["time"],
    )
    shift_result.condition(
        shift_checks >= 4 and bool(rises) and bool(falls),
        expected="shift_checks>=4_with_both_edges",
        observed=f"shifts={shift_checks}_rises={len(rises)}_falls={len(falls)}",
        time_s=rows[-1]["time"],
    )
    direction_result.condition(
        sdi_values == {0, 1},
        expected="sdi_values=0,1",
        observed=f"sdi_values={sorted(sdi_values)}",
        time_s=rows[-1]["time"],
    )
    return finish(
        "v4_185",
        results,
        coverage=(
            f"rises={len(rises)} falls={len(falls)} shifts={shift_checks} "
            f"reset_checks={reset_checks} reset_clock_checks={reset_clock_checks} "
            f"sdi={sorted(sdi_values)}"
        ),
    )


CHECKER_ID = "v4_185_spi_shift_mux"
CHECKER: Checker = check_v4_spi_shift_mux
