"""Stimulus-relative checker for canonical v4 DUT 173."""
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
    "P_SAMPLE_CLOCK_RESET",
    "P_SARREADY_SERIAL_ACCUMULATION",
    "P_BINARY_WEIGHT_ORDER",
    "P_BIPOLAR_OUTPUT_MAPPING",
]


def check_v4_dac_serial_accumulator(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk_sample", "clk_sarready", "data", "out"}
    results, missing = missing_trace("v4_173", rows, required, PROPERTY_IDS)
    if missing is not None:
        return missing
    reset_result, accumulation_result, weight_result, bipolar_result = results
    sample_falls = edge_times(rows, "clk_sample", threshold=0.55, rising=False)
    serial_falls = edge_times(rows, "clk_sarready", threshold=0.55, rising=False)
    events = sorted(
        [(time_s, "sample") for time_s in sample_falls]
        + [(time_s, "serial") for time_s in serial_falls]
    )
    settle = event_settle_delay([time_s for time_s, _ in events])
    state = 0.0
    counter = 1
    frame_bits: list[list[int]] = [[]]
    initial_probe = row_at_or_after(rows, rows[0]["time"] + settle)
    bipolar_result.compare(
        expected=-1.1,
        observed=initial_probe["out"],
        tolerance=0.04,
        time_s=initial_probe["time"],
        label="initial_bipolar_zero",
    )
    for event_time, kind in events:
        before = row_before(rows, event_time)
        if kind == "sample":
            state = 0.0
            counter = 1
            frame_bits.append([])
            target = -1.1
            result = reset_result
        else:
            if counter > 4:
                continue
            bit = int(before["data"] > 0.55)
            frame_bits[-1].append(bit)
            state += bit / (2.0 ** counter)
            counter += 1
            target = state * 2.2 - 1.1
            result = accumulation_result
        probe_time = event_time + settle
        if probe_time > rows[-1]["time"]:
            continue
        observed = row_at_or_after(rows, probe_time)["out"]
        result.compare(
            expected=target,
            observed=observed,
            tolerance=0.04,
            time_s=probe_time,
            label="out",
        )
        bipolar_result.compare(
            expected=target,
            observed=observed,
            tolerance=0.04,
            time_s=probe_time,
            label="bipolar_out",
        )
        if kind == "serial":
            weight_result.compare(
                expected=target,
                observed=observed,
                tolerance=0.04,
                time_s=probe_time,
                label=f"serial_weight_{counter - 1}",
            )

    complete_frames = [bits for bits in frame_bits if len(bits) >= 4]
    observed_bits = [bit for bits in frame_bits for bit in bits]
    reset_result.condition(
        len(sample_falls) >= 2,
        expected="sample_resets>=2",
        observed=f"sample_resets={len(sample_falls)}",
        time_s=rows[-1]["time"],
    )
    accumulation_result.condition(
        len(serial_falls) >= 5,
        expected="serial_falls>=5",
        observed=f"serial_falls={len(serial_falls)}",
        time_s=rows[-1]["time"],
    )
    weight_result.condition(
        bool(complete_frames) and set(observed_bits) == {0, 1},
        expected="complete_4bit_frame_with_zero_and_one",
        observed=f"frames={frame_bits}",
        time_s=rows[-1]["time"],
    )
    return finish(
        "v4_173",
        results,
        coverage=(
            f"sample_falls={len(sample_falls)} serial_falls={len(serial_falls)} "
            f"frames={frame_bits}"
        ),
    )


CHECKER_ID = "v4_173_dac_serial_accumulator"
CHECKER: Checker = check_v4_dac_serial_accumulator
