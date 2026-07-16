"""Task-specific checker for canonical v4 DUT 048."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import diagnostic, pass_note, require_signals


PROPERTY_IDS = (
    "P_ENABLE_GATES_OUTPUTS",
    "P_BINARY_TO_THERMOMETER_COUNT",
    "P_THERMOMETER_CUMULATIVE_ORDER",
    "P_ZERO_AND_FULL_SCALE_BOUNDARIES",
)

INPUT_SIGNALS = tuple(f"b{i}" for i in range(8)) + ("en",)
OUTPUT_SIGNALS = tuple(f"th{i}" for i in range(256))


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

def check_bin_to_thermometer_decoder_8b(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", *INPUT_SIGNALS, *OUTPUT_SIGNALS}
    missing = require_signals(rows, required, "P_BINARY_TO_THERMOMETER_COUNT")
    if missing:
        return False, missing

    probes = _stable_probe_indices(rows, INPUT_SIGNALS)
    if not probes:
        probes = [len(rows) // 2]

    checked_codes: list[int] = []
    enable_low_ok = True
    cumulative_errors = 0
    count_errors = 0
    boundary_seen = set()
    valid_probes = 0
    for probe_index in probes:
        row = rows[probe_index]
        input_values = _logic_vector(row, INPUT_SIGNALS)
        output_values = _logic_vector(row, OUTPUT_SIGNALS)
        valid_probes += 1
        bits = input_values[:8]
        enabled = input_values[8] == 1
        code = sum((1 << bit) for bit, value in enumerate(bits) if value)
        expected_count = code if enabled else 0
        actual_high = {i for i, value in enumerate(output_values) if value == 1}
        expected_high = set(range(expected_count))
        if actual_high != expected_high:
            if len(actual_high) != expected_count:
                count_errors += 1
            else:
                cumulative_errors += 1
        if not enabled and actual_high:
            enable_low_ok = False
        checked_codes.append(code if enabled else -1)
        if enabled and code in {0, 1, 255}:
            boundary_seen.add(code)

    if valid_probes < 4:
        return False, diagnostic(
            "P_BINARY_TO_THERMOMETER_COUNT",
            "insufficient_excitation",
            expected="stable_vector_probes>=4",
            observed=f"stable_vector_probes={valid_probes}",
            event="observed_input_vector_intervals",
        )
    ok = (
        enable_low_ok
        and count_errors == 0
        and cumulative_errors == 0
        and {0, 1, 255}.issubset(boundary_seen)
        and -1 in checked_codes
    )
    note = (
        f"checked={checked_codes} boundary_seen={sorted(boundary_seen)} "
        f"enable_low_ok={enable_low_ok} count_errors={count_errors} "
        f"cumulative_errors={cumulative_errors}"
    )
    if not enable_low_ok:
        return False, diagnostic(
            "P_ENABLE_GATES_OUTPUTS",
            "behavior_mismatch",
            expected="all thermometer outputs low when en=0",
            observed="enabled_output_seen_when_disabled",
            event="en.low_interval",
        )
    if count_errors:
        return False, diagnostic(
            "P_BINARY_TO_THERMOMETER_COUNT",
            "behavior_mismatch",
            expected="popcount(th)==binary_code_when_enabled",
            observed=f"count_errors={count_errors}",
            event="stable_input_vector_intervals",
        )
    if cumulative_errors:
        return False, diagnostic(
            "P_THERMOMETER_CUMULATIVE_ORDER",
            "behavior_mismatch",
            expected="th[0:code) high and th[code:] low",
            observed=f"cumulative_errors={cumulative_errors}",
            event="stable_input_vector_intervals",
        )
    if not {0, 1, 255}.issubset(boundary_seen) or -1 not in checked_codes:
        return False, diagnostic(
            "P_ZERO_AND_FULL_SCALE_BOUNDARIES",
            "insufficient_excitation",
            expected="enabled codes 0,1,255 plus disabled vector",
            observed=f"checked={checked_codes},boundary_seen={sorted(boundary_seen)}",
            event="observed_input_vector_intervals",
        )
    return ok, pass_note(PROPERTY_IDS, note)

CHECKER_ID = "v4_048_bin_to_thermometer_decoder_8b"
CHECKER: Checker = check_bin_to_thermometer_decoder_8b
