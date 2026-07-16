"""Stimulus-relative checker for canonical v4 DUT 023."""
from __future__ import annotations

import math

from ..api import Checker
from .stimulus_relative import (
    bit_code,
    event_settle_delay,
    finish,
    missing_trace,
    rising_indices,
    row_at_or_after,
)


PROPERTY_IDS = [
    "P_RISING_EDGE_QUANTIZATION",
    "P_CODE_CLAMP",
    "P_BINARY_RAIL_ENCODING",
    "P_CODE_MONOTONICITY",
    "P_SAMPLE_HOLD",
]
BITS = ["dout0", "dout1", "dout2"]


def check_clocked_adc_quantizer(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "vin", "vdd", "vss", *BITS}
    results, error = missing_trace(CHECKER_ID, rows, required, PROPERTY_IDS)
    if error is not None:
        return error
    by_id = {result.property_id: result for result in results}

    edges = rising_indices(rows, "clk")
    edge_times = [float(rows[index]["time"]) for index in edges]
    settle = event_settle_delay(edge_times)
    expected_codes: list[int] = []
    observed_codes: list[int] = []
    sampled_vin: list[float] = []

    for index in edges:
        edge = rows[index]
        event_time = float(edge["time"])
        rail_span = float(edge["vdd"] - edge["vss"])
        if rail_span <= 0.2:
            by_id["P_BINARY_RAIL_ENCODING"].condition(
                False,
                expected="positive_local_rail_span",
                observed=f"rail_span={rail_span:.6g}",
                time_s=event_time,
                gap=0.2 - rail_span,
            )
            continue
        normalized = 8.0 * (float(edge["vin"]) - edge["vss"]) / rail_span
        expected_code = min(7, max(0, math.floor(normalized)))
        sample = row_at_or_after(rows, event_time + settle)
        observed_code = bit_code(sample, BITS)
        expected_codes.append(expected_code)
        observed_codes.append(observed_code)
        sampled_vin.append(float(edge["vin"]))

        by_id["P_RISING_EDGE_QUANTIZATION"].condition(
            observed_code == expected_code,
            expected=f"code={expected_code}",
            observed=f"code={observed_code}",
            time_s=sample["time"],
            gap=abs(observed_code - expected_code),
        )
        if normalized <= 0.5 or normalized >= 7.5:
            by_id["P_CODE_CLAMP"].condition(
                observed_code == expected_code,
                expected=f"endpoint_code={expected_code}",
                observed=f"code={observed_code}",
                time_s=sample["time"],
                gap=abs(observed_code - expected_code),
            )
        for bit_index, signal in enumerate(BITS):
            expected_rail = sample["vdd"] if expected_code & (1 << bit_index) else sample["vss"]
            by_id["P_BINARY_RAIL_ENCODING"].compare(
                expected=expected_rail,
                observed=sample[signal],
                tolerance=0.04,
                time_s=sample["time"],
                label=signal,
            )

    for previous_vin, current_vin, previous_code, current_code, event_time in zip(
        sampled_vin,
        sampled_vin[1:],
        observed_codes,
        observed_codes[1:],
        edge_times[1:],
    ):
        if current_vin + 1e-6 < previous_vin:
            continue
        by_id["P_CODE_MONOTONICITY"].condition(
            current_code >= previous_code,
            expected=f"code>={previous_code}",
            observed=f"code={current_code}",
            time_s=event_time,
            gap=max(0, previous_code - current_code),
        )

    for left, right in zip(edge_times, edge_times[1:]):
        spacing = right - left
        if spacing <= 2.5 * settle:
            continue
        early = row_at_or_after(rows, left + max(settle, 0.30 * spacing))
        late = row_at_or_after(rows, left + 0.78 * spacing)
        early_code = bit_code(early, BITS)
        late_code = bit_code(late, BITS)
        by_id["P_SAMPLE_HOLD"].condition(
            early_code == late_code,
            expected=f"held_code={early_code}",
            observed=f"code={late_code}",
            time_s=late["time"],
            gap=abs(late_code - early_code),
        )

    by_id["P_RISING_EDGE_QUANTIZATION"].condition(
        len(set(expected_codes)) == 8,
        expected="all_8_uniform_bins_exercised",
        observed=f"bins={len(set(expected_codes))}",
        time_s=edge_times[-1] if edge_times else 0.0,
        gap=8 - len(set(expected_codes)),
    )
    return finish(
        CHECKER_ID,
        results,
        coverage=(
            f"rising_edges={len(edges)} expected_bins={len(set(expected_codes))} "
            f"settle_s={settle:.6g}"
        ),
    )


CHECKER_ID = "v4_023_clocked_adc_quantizer"
CHECKER: Checker = check_clocked_adc_quantizer
