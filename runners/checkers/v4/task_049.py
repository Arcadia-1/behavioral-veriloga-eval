"""Task-specific checker for canonical v4 DUT 049."""
from __future__ import annotations

from ..api import Checker
def _sample_rows_every_10ns(rows: list[dict[str, float]]) -> list[dict[str, float]]:
    # Formal utility testbenches hold each vector for a 10 ns window. Sample
    # mid-window to avoid transition edges and PWL update times.
    max_time = rows[-1]["time"]
    times = [row["time"] for row in rows]
    samples: list[dict[str, float]] = []
    sample_t = 5e-9
    while sample_t <= max_time + 1e-15:
        idx = min(range(len(times)), key=lambda i: abs(times[i] - sample_t))
        samples.append(rows[idx])
        sample_t += 10e-9
    return samples

def _logic_bits_to_int(row: dict[str, float], prefix: str, width: int, vth: float = 0.45) -> int:
    return sum((1 << bit) for bit in range(width) if row[f"{prefix}{bit}"] > vth)

def check_thermometer_to_binary_encoder_8b(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "valid", *{f"th{i}" for i in range(256)}, *{f"b{i}" for i in range(8)}}
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0].keys())) if rows else sorted(required)
        return False, "missing_columns=" + ",".join(missing[:12])
    samples = _sample_rows_every_10ns(rows)
    checked: list[str] = []
    valid_errors = 0
    count_errors = 0
    for row in samples:
        high = {i for i in range(256) if row[f"th{i}"] > 0.45}
        cumulative = high == set(range(len(high)))
        expected_valid = cumulative
        actual_valid = row["valid"] > 0.45
        if actual_valid != expected_valid:
            valid_errors += 1
        expected_code = len(high) if expected_valid else 0
        actual_code = _logic_bits_to_int(row, "b", 8)
        if actual_code != expected_code:
            count_errors += 1
        checked.append(str(expected_code) if expected_valid else "invalid")
    return valid_errors == 0 and count_errors == 0 and {"0", "1", "255", "invalid"}.issubset(set(checked)), (
        f"checked={checked} valid_errors={valid_errors} count_errors={count_errors}"
    )

CHECKER_ID = "v4_049_thermometer_to_binary_encoder_8b"
CHECKER: Checker = check_thermometer_to_binary_encoder_8b
