"""Stimulus-relative checker for canonical v4 DUT 189."""
from __future__ import annotations

import math

from ..api import Checker
from .stimulus_relative import PropertyResult, finish, median_step, missing_trace


PROPERTY_IDS = [
    "P_ANALOG_INPUT_ROUNDING",
    "P_LOW_FOUR_BIT_MAPPING",
    "P_CONTINUOUS_CODE_UPDATE",
    "P_TRIM_OUTPUT_LEVELS",
]


def _code_plateaus(rows: list[dict[str, float]]) -> list[tuple[int, int, int]]:
    plateaus: list[tuple[int, int, int]] = []
    start = 0
    code = math.floor(rows[0]["ain"] + 0.5)
    for index, row in enumerate(rows[1:], start=1):
        current = math.floor(row["ain"] + 0.5)
        if current == code:
            continue
        plateaus.append((start, index - 1, code))
        start = index
        code = current
    plateaus.append((start, len(rows) - 1, code))
    return plateaus


def check_v4_trim_ctrl_4bit(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "ain", "dout0", "dout1", "dout2", "dout3"}
    results, missing = missing_trace("v4_189", rows, required, PROPERTY_IDS)
    if missing is not None:
        return missing
    rounding, mapping, continuous, levels = results
    step = median_step(rows)
    settled: list[tuple[dict[str, float], int]] = []
    for start, stop, code in _code_plateaus(rows):
        duration = rows[stop]["time"] - rows[start]["time"]
        if stop <= start or duration < max(4.0 * step, 30e-12):
            continue
        probe = start + max(1, int(0.75 * (stop - start)))
        settled.append((rows[min(probe, stop)], code))

    distinct_codes = {code for _, code in settled}
    settled_inputs = [row["ain"] for row, _ in settled]
    below_half = any(0.45 <= (value - math.floor(value)) < 0.5 for value in settled_inputs)
    at_or_above_half = any(0.5 <= (value - math.floor(value)) <= 0.55 for value in settled_inputs)
    wrap_covered = any(16 <= code <= 31 for code in distinct_codes)
    for row, code in settled:
        time_s = row["time"]
        for bit in range(4):
            observed = row[f"dout{bit}"]
            expected = 0.9 if ((code >> bit) & 1) else 0.0
            rounding.compare(
                expected=expected,
                observed=observed,
                tolerance=0.08,
                time_s=time_s,
                label=f"rounded_code_bit{bit}",
            )
            mapping.compare(
                expected=expected,
                observed=observed,
                tolerance=0.08,
                time_s=time_s,
                label=f"dout{bit}",
            )
            levels.condition(
                min(abs(observed), abs(observed - 0.9)) <= 0.08,
                expected="logic_rail_0_or_0.9",
                observed=f"dout{bit}={observed:.6g}",
                time_s=time_s,
                gap=min(abs(observed), abs(observed - 0.9)),
            )

    continuous.condition(
        len(settled) >= 8 and len(distinct_codes) >= 8,
        expected="settled_plateaus>=8_distinct_codes>=8",
        observed=f"plateaus={len(settled)}_codes={sorted(distinct_codes)}",
        time_s=rows[-1]["time"],
        gap=float(max(0, 8 - len(distinct_codes))),
    )
    rounding.condition(
        below_half and at_or_above_half,
        expected="fractional_inputs_below_and_at_or_above_half",
        observed=f"below_half={below_half}_at_or_above_half={at_or_above_half}",
        time_s=rows[-1]["time"],
    )
    mapping.condition(
        wrap_covered,
        expected="rounded_code_wrap_16_to_31_covered",
        observed=f"codes={sorted(distinct_codes)}",
        time_s=rows[-1]["time"],
    )
    for result in (rounding, mapping, levels):
        result.require_coverage(4)
    return finish(
        "v4_189",
        results,
        coverage=(
            f"plateaus={len(settled)} distinct_codes={sorted(distinct_codes)} "
            f"below_half={below_half} at_or_above_half={at_or_above_half} "
            f"wrap_covered={wrap_covered}"
        ),
    )


CHECKER_ID = "v4_189_trim_ctrl_4bit"
CHECKER: Checker = check_v4_trim_ctrl_4bit
