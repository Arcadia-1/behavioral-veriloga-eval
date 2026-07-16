"""Task-specific checker for canonical v4 DUT 176."""
from __future__ import annotations

from ..api import Checker
from .batch18_diagnostics import bind_properties
def _stable_bits_tuple(row: dict[str, float], bit_names: list[str]) -> tuple[int, ...] | None:
    bits = [_stable_voltage_bit(row, signal) for signal in bit_names]
    if any(bit is None for bit in bits):
        return None
    return tuple(int(bit) for bit in bits if bit is not None)

def check_v3_weighted_decoder_7b5(rows: list[dict[str, float]]) -> tuple[bool, str]:
    bit_names = [f"d{i}" for i in range(9)]
    required = {"time", "aout7b", "aout7b5", "aout8b", *bit_names}
    if not rows or not required.issubset(rows[0]):
        return False, "missing weighted decoder outputs"
    ladder_weights = [1.0, 2.0, 4.0, 8.0, 8.0, 16.0, 32.0, 64.0]
    denom = 2.0 * (sum(ladder_weights) + 1.0)
    last_bits: tuple[int, ...] | None = None
    settle_until = 0.0
    checked = 0
    observed_codes: set[tuple[int, ...]] = set()
    max_err = 0.0
    worst_code = ""
    for row in rows:
        t = row.get("time")
        if t is None:
            continue
        bits = _stable_bits_tuple(row, bit_names)
        if bits is None:
            continue
        observed_codes.add(bits)
        if last_bits is None or bits != last_bits:
            last_bits = bits
            settle_until = t + 0.08e-9
            continue
        if t < settle_until:
            continue
        bipolar = [1.0 if bit else -1.0 for bit in bits]
        paired_lsb = 1.0 if bits[0] and bits[1] else -1.0 if not bits[0] and not bits[1] else 0.0
        expected = {
            "aout7b": sum(weight * bipolar[idx + 1] for idx, weight in enumerate(ladder_weights)) / denom,
            "aout8b": (0.5 * bipolar[0] + sum(weight * bipolar[idx + 1] for idx, weight in enumerate(ladder_weights))) / denom,
            "aout7b5": (paired_lsb + sum(weight * bipolar[idx + 2] for idx, weight in enumerate(ladder_weights[1:]))) / denom,
        }
        err = max(abs(row[name] - value) for name, value in expected.items())
        if err > max_err:
            max_err = err
            worst_code = "".join(str(bit) for bit in bits)
        checked += 1
    if checked < 20 or len(observed_codes) < 2:
        return False, (
            f"insufficient_weighted_decoder_excitation rows={checked} "
            f"codes={len(observed_codes)}"
        )
    return max_err <= 0.025, f"checked={checked} max_weighted7b5_error={max_err:.5f} worst_code={worst_code}"

def _stable_voltage_bit(row: dict[str, float], signal: str) -> int | None:
    value = row.get(signal)
    if value is None:
        return None
    if value <= 0.15:
        return 0
    if value >= 0.75:
        return 1
    return None

CHECKER_ID = "v4_176_weighted_decoder_7b5"
CHECKER: Checker = bind_properties(check_v3_weighted_decoder_7b5, (
    "P_SHARED_272_DENOMINATOR", "P_SEVEN_BIT_OUTPUT",
    "P_SEVEN_HALF_BIT_OUTPUT", "P_EIGHT_BIT_OUTPUT",
))
