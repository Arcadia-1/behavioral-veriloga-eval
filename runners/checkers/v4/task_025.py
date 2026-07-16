"""Stimulus-relative checker for canonical v4 DUT 025."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import bit_code, event_settle_delay, finish, missing_trace, row_at_or_after


PROPERTY_IDS = [
    "P_ZERO_AND_FULL_SCALE",
    "P_NONIDEAL_WEIGHT_SUM",
    "P_LOGIC_THRESHOLD",
    "P_BOUNDED_OUTPUT",
    "P_MISMATCH_OBSERVABILITY",
]
BITS = ["b0", "b1", "b2", "b3"]
WEIGHTS = [1.00, 2.02, 3.96, 8.08]
WEIGHT_SUM = sum(WEIGHTS)


def _expected_output(row: dict[str, float]) -> float:
    active_weight = sum(
        weight for signal, weight in zip(BITS, WEIGHTS) if row[signal] > 0.45
    )
    return 0.9 * active_weight / WEIGHT_SUM


def check_dac_mismatch_unit_weighting(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "out", *BITS}
    results, error = missing_trace(CHECKER_ID, rows, required, PROPERTY_IDS)
    if error is not None:
        return error
    by_id = {result.property_id: result for result in results}

    change_indices = [0]
    previous_code = bit_code(rows[0], BITS)
    for index, row in enumerate(rows[1:], start=1):
        code = bit_code(row, BITS)
        if code != previous_code:
            change_indices.append(index)
            previous_code = code
    event_times = [float(rows[index]["time"]) for index in change_indices]
    settle = event_settle_delay(event_times, fraction=0.10)
    sampled_codes: set[int] = set()
    endpoint_codes: set[int] = set()
    threshold_cases = 0
    mismatch_cases = 0

    for position, index in enumerate(change_indices):
        start = float(rows[index]["time"])
        stop = (
            float(rows[change_indices[position + 1]]["time"])
            if position + 1 < len(change_indices)
            else float(rows[-1]["time"])
        )
        if stop - start <= settle:
            continue
        sample = row_at_or_after(rows, min(stop, start + max(settle, 0.35 * (stop - start))))
        code = bit_code(sample, BITS)
        expected = _expected_output(sample)
        sampled_codes.add(code)
        by_id["P_NONIDEAL_WEIGHT_SUM"].compare(
            expected=expected,
            observed=sample["out"],
            tolerance=0.0015,
            time_s=sample["time"],
            label=f"code_{code}_out",
        )
        by_id["P_BOUNDED_OUTPUT"].condition(
            -0.002 <= sample["out"] <= 0.902,
            expected="out_in_[0,0.9]",
            observed=f"out={sample['out']:.6g}",
            time_s=sample["time"],
            gap=max(-sample["out"], sample["out"] - 0.9, 0.0),
        )
        if code in {0, 15}:
            endpoint_codes.add(code)
            by_id["P_ZERO_AND_FULL_SCALE"].compare(
                expected=0.0 if code == 0 else 0.9,
                observed=sample["out"],
                tolerance=0.004,
                time_s=sample["time"],
                label=f"endpoint_code_{code}",
            )
        if any(0.45 < sample[signal] < 0.70 for signal in BITS):
            threshold_cases += 1
            by_id["P_LOGIC_THRESHOLD"].compare(
                expected=expected,
                observed=sample["out"],
                tolerance=0.0015,
                time_s=sample["time"],
                label="threshold_case_out",
            )
        ideal = 0.9 * code / 15.0
        if abs(expected - ideal) >= 0.0018:
            mismatch_cases += 1
            by_id["P_MISMATCH_OBSERVABILITY"].compare(
                expected=expected,
                observed=sample["out"],
                tolerance=0.0015,
                time_s=sample["time"],
                label="nonideal_weight_out",
            )

    by_id["P_ZERO_AND_FULL_SCALE"].condition(
        endpoint_codes == {0, 15},
        expected="zero_and_full_scale_exercised",
        observed=f"endpoint_codes={sorted(endpoint_codes)}",
        time_s=rows[-1]["time"],
        gap=2 - len(endpoint_codes),
    )
    by_id["P_LOGIC_THRESHOLD"].condition(
        threshold_cases > 0,
        expected="near_threshold_high_exercised",
        observed=f"cases={threshold_cases}",
        time_s=rows[-1]["time"],
        gap=1 if threshold_cases == 0 else 0,
    )
    by_id["P_MISMATCH_OBSERVABILITY"].condition(
        mismatch_cases > 0,
        expected="nonideal_distinguishing_pattern_exercised",
        observed=f"cases={mismatch_cases}",
        time_s=rows[-1]["time"],
        gap=1 if mismatch_cases == 0 else 0,
    )
    return finish(
        CHECKER_ID,
        results,
        coverage=(
            f"patterns={len(sampled_codes)} endpoint_codes={sorted(endpoint_codes)} "
            f"threshold_cases={threshold_cases} mismatch_cases={mismatch_cases}"
        ),
    )


CHECKER_ID = "v4_025_dac_mismatch_unit_weighting_model"
CHECKER: Checker = check_dac_mismatch_unit_weighting
