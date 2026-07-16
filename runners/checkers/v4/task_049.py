"""Task-specific checker for canonical v4 DUT 049."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import diagnostic, pass_note, require_signals


PROPERTY_IDS = (
    "P_THERMOMETER_VALIDITY",
    "P_THERMOMETER_COUNT_TO_BINARY",
    "P_INVALID_PATTERN_REJECTED",
    "P_ZERO_AND_FULL_SCALE_BOUNDARIES",
)

INPUT_SIGNALS = tuple(f"th{i}" for i in range(256))
OUTPUT_SIGNALS = tuple(f"b{i}" for i in range(8)) + ("valid",)


def _logic_vector(row: dict[str, float], signals: tuple[str, ...]) -> tuple[int, ...]:
    return tuple(1 if row[signal] > 0.45 else 0 for signal in signals)


def _stable_probe_indices(rows: list[dict[str, float]], signals: tuple[str, ...]) -> list[int]:
    if not rows:
        return []
    probes: list[int] = []
    start = 0
    current = _logic_vector(rows[0], signals)
    for index in range(1, len(rows)):
        vector = _logic_vector(rows[index], signals)
        if vector == current:
            continue
        if rows[index - 1]["time"] - rows[start]["time"] > 0.05e-9:
            probes.append((start + index - 1) // 2)
        start = index
        current = vector
    if rows[-1]["time"] - rows[start]["time"] > 0.05e-9:
        probes.append((start + len(rows) - 1) // 2)
    return probes

def check_thermometer_to_binary_encoder_8b(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", *INPUT_SIGNALS, *OUTPUT_SIGNALS}
    missing = require_signals(rows, required, "P_THERMOMETER_COUNT_TO_BINARY")
    if missing:
        return False, missing

    probes = _stable_probe_indices(rows, INPUT_SIGNALS)
    if not probes:
        probes = [len(rows) // 2]
    checked: list[str] = []
    valid_errors = 0
    count_errors = 0
    valid_probes = 0
    invalid_seen = False
    for probe_index in probes:
        row = rows[probe_index]
        input_values = _logic_vector(row, INPUT_SIGNALS)
        output_values = _logic_vector(row, OUTPUT_SIGNALS)
        valid_probes += 1
        high = {i for i, value in enumerate(input_values) if value == 1}
        cumulative = high == set(range(len(high)))
        expected_valid = cumulative
        actual_valid = output_values[8] == 1
        if actual_valid != expected_valid:
            valid_errors += 1
        expected_code = len(high) if expected_valid else 0
        actual_code = sum((1 << bit) for bit, value in enumerate(output_values[:8]) if value)
        if actual_code != expected_code:
            count_errors += 1
        if not expected_valid:
            invalid_seen = True
        checked.append(str(expected_code) if expected_valid else "invalid")
    if valid_probes < 4:
        return False, diagnostic(
            "P_THERMOMETER_COUNT_TO_BINARY",
            "insufficient_excitation",
            expected="stable_vector_probes>=4",
            observed=f"stable_vector_probes={valid_probes}",
            event="observed_input_vector_intervals",
        )
    note = f"checked={checked} valid_errors={valid_errors} count_errors={count_errors}"
    if valid_errors:
        return False, diagnostic(
            "P_THERMOMETER_VALIDITY",
            "behavior_mismatch",
            expected="valid=1 only for cumulative thermometer patterns",
            observed=f"valid_errors={valid_errors}",
            event="stable_thermometer_vector_intervals",
        )
    if count_errors:
        return False, diagnostic(
            "P_THERMOMETER_COUNT_TO_BINARY",
            "behavior_mismatch",
            expected="binary_count==number_of_cumulative_high_inputs",
            observed=f"count_errors={count_errors}",
            event="stable_thermometer_vector_intervals",
        )
    if not invalid_seen:
        return False, diagnostic(
            "P_INVALID_PATTERN_REJECTED",
            "insufficient_excitation",
            expected="at_least_one_non_cumulative_input_pattern",
            observed=f"checked={checked}",
            event="observed_input_vector_intervals",
        )
    if not {"0", "1", "255", "invalid"}.issubset(set(checked)):
        return False, diagnostic(
            "P_ZERO_AND_FULL_SCALE_BOUNDARIES",
            "insufficient_excitation",
            expected="codes 0,1,255 plus invalid vector",
            observed=f"checked={checked}",
            event="observed_input_vector_intervals",
        )
    return True, pass_note(PROPERTY_IDS, note)

CHECKER_ID = "v4_049_thermometer_to_binary_encoder_8b"
CHECKER: Checker = check_thermometer_to_binary_encoder_8b
