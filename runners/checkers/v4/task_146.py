"""Task-specific checker for canonical v4 DUT 146."""
from __future__ import annotations

from checkers.api import Checker
def _v3_missing_columns(rows: list[dict[str, float]], required: set[str]) -> str | None:
    if not rows:
        return "empty_waveform"
    missing = sorted(required - set(rows[0]))
    if missing:
        return "missing_columns=" + ",".join(missing)
    return None

def check_v3_flash_thermometer_centered_sum(rows: list[dict[str, float]]) -> tuple[bool, str]:
    bit_names = [f"b{idx}" for idx in range(8)]
    required = {"time", "dout", *bit_names}
    missing = _v3_missing_columns(rows, required)
    if missing:
        return False, missing

    max_error = 0.0
    checked = 0
    stride = max(1, len(rows) // 60)
    for row in rows[::stride]:
        bits = [row[name] for name in bit_names]
        if not all(bit <= 0.10 or bit >= 0.80 for bit in bits):
            continue
        ones = sum(1 for bit in bits if bit > 0.45)
        expected = 0.1125 * (ones - 4.0)
        max_error = max(max_error, abs(row["dout"] - expected))
        checked += 1
    if checked < 8:
        return False, f"too_few_stable_thermometer_samples={checked}"
    return max_error <= 0.02, f"checked={checked} max_error={max_error:.5f}"

CHECKER_ID = "v4_146_flash_thermometer_centered_sum"
CHECKER: Checker = check_v3_flash_thermometer_centered_sum
