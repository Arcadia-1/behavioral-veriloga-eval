"""Stimulus-relative checker for canonical v4 DUT 182."""
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
    "P_RESET_SELECTS_DIN0",
    "P_FALLING_CLOCK_UPDATE_SAMPLE",
    "P_UPDATE_LOW_HOLDS_STATE",
    "P_SELECT_DECODE_AND_OUTPUT_TIMING",
]


def _selected_input(row: dict[str, float]) -> tuple[int, float]:
    code = int(row["dsel0"] > 0.45) + 2 * int(row["dsel1"] > 0.45)
    return code, row[f"din{code}"]


def check_v4_clocked_mux4_sampler(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {
        "time", "dsel0", "dsel1", "din0", "din1", "din2", "din3",
        "update", "rst", "clks", "dout",
    }
    results, missing = missing_trace("v4_182", rows, required, PROPERTY_IDS)
    if missing is not None:
        return missing
    reset_result, sample_result, hold_result, decode_result = results
    clock_falls = edge_times(rows, "clks", threshold=0.45, rising=False)
    reset_rises = edge_times(rows, "rst", threshold=0.45, rising=True)
    event_times = sorted(set(clock_falls + reset_rises))
    settle = event_settle_delay(event_times)

    initial_expected = rows[0]["din0"]
    initial_probe = row_at_or_after(rows, rows[0]["time"] + settle)
    reset_result.compare(
        expected=initial_expected,
        observed=initial_probe["dout"],
        tolerance=0.04,
        time_s=initial_probe["time"],
        label="initial_din0",
    )
    held = initial_expected
    selected_codes: set[int] = set()
    reset_checks = 1
    sample_checks = 0
    hold_checks = 0
    for event_time in event_times:
        before = row_before(rows, event_time)
        is_reset_rise = any(abs(event_time - value) <= 1e-15 for value in reset_rises)
        is_clock_fall = any(abs(event_time - value) <= 1e-15 for value in clock_falls)
        property_result = decode_result
        if is_reset_rise or (is_clock_fall and before["rst"] > 0.45):
            held = before["din0"]
            property_result = reset_result
            reset_checks += 1
        elif is_clock_fall and before["update"] > 0.45:
            code, held = _selected_input(before)
            selected_codes.add(code)
            property_result = sample_result
            sample_checks += 1
        elif is_clock_fall:
            property_result = hold_result
            hold_checks += 1
        else:
            continue
        probe_time = event_time + settle
        if probe_time > rows[-1]["time"]:
            continue
        observed = row_at_or_after(rows, probe_time)["dout"]
        property_result.compare(
            expected=held,
            observed=observed,
            tolerance=0.04,
            time_s=probe_time,
            label="dout",
        )
        decode_result.compare(
            expected=held,
            observed=observed,
            tolerance=0.04,
            time_s=probe_time,
            label="selected_input",
        )

    reset_result.condition(
        reset_checks >= 2,
        expected="reset_checks>=2",
        observed=f"reset_checks={reset_checks}",
        time_s=rows[-1]["time"],
    )
    sample_result.condition(
        sample_checks >= 4 and selected_codes == {0, 1, 2, 3},
        expected="update_samples>=4_codes=0,1,2,3",
        observed=f"samples={sample_checks}_codes={sorted(selected_codes)}",
        time_s=rows[-1]["time"],
    )
    hold_result.condition(
        hold_checks >= 1,
        expected="update_low_holds>=1",
        observed=f"holds={hold_checks}",
        time_s=rows[-1]["time"],
    )
    return finish(
        "v4_182",
        results,
        coverage=(
            f"clock_falls={len(clock_falls)} reset_checks={reset_checks} "
            f"samples={sample_checks} holds={hold_checks} codes={sorted(selected_codes)}"
        ),
    )


CHECKER_ID = "v4_182_clocked_mux4_sampler"
CHECKER: Checker = check_v4_clocked_mux4_sampler
