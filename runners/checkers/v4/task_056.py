"""Task-specific checker for canonical v4 DUT 056."""
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

def _check_bus_equal(
    rows: list[dict[str, float]],
    input_prefix: str,
    output_prefix: str,
    width: int,
    enable_col: str | None = None,
    invert_enable: bool = False,
) -> tuple[bool, str]:
    required = {"time", *{f"{input_prefix}{i}" for i in range(width)}, *{f"{output_prefix}{i}" for i in range(width)}}
    if enable_col:
        required.add(enable_col)
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0].keys())) if rows else sorted(required)
        return False, "missing_columns=" + ",".join(missing[:12])
    errors = 0
    checked = 0
    for row in _sample_rows_every_10ns(rows):
        enabled = True
        if enable_col:
            en_high = row[enable_col] > 0.45
            enabled = (not en_high) if invert_enable else en_high
        for idx in range(width):
            expected_high = enabled and row[f"{input_prefix}{idx}"] > 0.45
            actual_high = row[f"{output_prefix}{idx}"] > 0.45
            if actual_high != expected_high:
                errors += 1
        checked += 1
    return errors == 0 and checked >= 3, f"checked={checked} bit_errors={errors}"

def check_config_latch_32b_clocked(rows: list[dict[str, float]]) -> tuple[bool, str]:
    return _check_bus_equal(rows, "d", "q", 32, "en")

CHECKER_ID = "v4_056_config_latch_32b_clocked"
CHECKER: Checker = check_config_latch_32b_clocked
