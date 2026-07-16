"""Task-specific checker for canonical v4 DUT 052."""
from __future__ import annotations

import math

from ..api import Checker
from .stimulus_relative import Row, diagnostic, event_label, pass_note, require_signals


WIDTH = 16
VTH = 0.45
LOW_MAX = 0.18
HIGH_MIN = 0.72
VIN_STABLE_TOL = 1e-6
PROPERTIES = (
    "P_PREFIX_CODE",
    "P_ORDERED_ACTIVATION",
    "P_UNIFORM_SEGMENTS",
    "P_INPUT_CLIPPING",
    "P_OUTPUT_LEVELS",
)


def _expected_code(vin: float) -> int:
    clipped = min(1.0, max(0.0, vin))
    return max(0, min(WIDTH, int(math.floor(WIDTH * clipped))))


def _logic_bits(row: Row) -> list[int] | None:
    bits: list[int] = []
    for bit in range(WIDTH):
        value = row[f"t{bit}"]
        if LOW_MAX < value < HIGH_MIN:
            return None
        bits.append(1 if value > VTH else 0)
    return bits


def _samples_from_vin_segments(rows: list[Row], *, require_repeated_vin: bool) -> list[tuple[int, Row, list[int]]]:
    """Pick one settled observable row from each stable input plateau."""

    samples: list[tuple[int, Row, list[int]]] = []
    start = 0
    last_key: tuple[int, tuple[int, ...]] | None = None
    for index in range(1, len(rows) + 1):
        if index < len(rows) and abs(rows[index]["vin"] - rows[index - 1]["vin"]) <= VIN_STABLE_TOL:
            continue
        segment = rows[start:index]
        selected: tuple[int, Row, list[int]] | None = None
        if not require_repeated_vin or len(segment) > 1:
            for row in reversed(segment):
                bits = _logic_bits(row)
                if bits is not None:
                    selected = (_expected_code(row["vin"]), row, bits)
                    break
        if selected is not None:
            key = (selected[0], tuple(selected[2]))
            if key != last_key:
                samples.append(selected)
                last_key = key
        start = index
    return samples


def _stable_code_samples(rows: list[Row]) -> list[tuple[int, Row, list[int]]]:
    samples = _samples_from_vin_segments(rows, require_repeated_vin=True)
    if samples:
        return samples
    return _samples_from_vin_segments(rows, require_repeated_vin=False)


def check_v3_497_thermometer_bus_encoder(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin", *{f"t{i}" for i in range(WIDTH)}}
    missing = require_signals(rows, required, "P_PREFIX_CODE")
    if missing:
        return False, missing
    samples = _stable_code_samples(rows)
    if len(samples) < 4:
        return False, diagnostic(
            "P_UNIFORM_SEGMENTS",
            "insufficient_coverage",
            expected="stable_code_samples>=4",
            observed=f"stable_code_samples={len(samples)}",
            event="full_trace",
        )

    checked = 0
    previous_code: int | None = None
    seen_codes: set[int] = set()
    max_level_error = 0
    for sample_index, (code, row, bits) in enumerate(samples):
        expected = [1 if bit < code else 0 for bit in range(WIDTH)]
        if bits != expected:
            return False, diagnostic(
                "P_UNIFORM_SEGMENTS",
                "wrong_segment_count",
                expected=f"active_count={code}",
                observed=f"active_count={sum(bits)}",
                event=event_label("vin_code_segment", sample_index),
            )
        if any(bits[bit] < bits[bit + 1] for bit in range(WIDTH - 1)):
            return False, diagnostic(
                "P_PREFIX_CODE",
                "non_prefix_order",
                expected="contiguous_prefix",
                observed="higher_segment_without_lower_segment",
                event=event_label("vin_code_segment", sample_index),
            )
        if previous_code is not None and row["vin"] >= samples[sample_index - 1][1]["vin"] and code < previous_code:
            return False, diagnostic(
                "P_ORDERED_ACTIVATION",
                "non_monotonic_count",
                expected="active_count_non_decreasing",
                observed=f"previous={previous_code},current={code}",
                event=event_label("vin_code_segment", sample_index),
            )
        for bit, expected_bit in enumerate(expected):
            value = row[f"t{bit}"]
            if expected_bit and value < HIGH_MIN:
                max_level_error += 1
            elif not expected_bit and value > LOW_MAX:
                max_level_error += 1
        seen_codes.add(code)
        previous_code = code
        checked += 1

    if max_level_error:
        return False, diagnostic(
            "P_OUTPUT_LEVELS",
            "rail_level_error",
            expected="inactive<=0.18_active>=0.72",
            observed=f"rail_errors={max_level_error}",
            event="stable_code_segments",
        )
    if len(seen_codes) < 4 or 0 not in seen_codes or WIDTH not in seen_codes:
        return False, diagnostic(
            "P_INPUT_CLIPPING",
            "insufficient_endpoint_coverage",
            expected="code0_and_code16_plus_two_midcodes",
            observed="codes=" + ",".join(str(code) for code in sorted(seen_codes)),
            event="full_trace",
        )
    return True, pass_note(PROPERTIES, f"thermometer_samples={checked}")

CHECKER_ID = "v4_052_thermometer_bus_encoder"
CHECKER: Checker = check_v3_497_thermometer_bus_encoder
