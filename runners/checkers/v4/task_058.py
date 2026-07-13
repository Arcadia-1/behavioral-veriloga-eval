"""Task-specific checker for canonical v4 DUT 058."""
from __future__ import annotations

from checkers.api import Checker
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

def check_masked_config_update_32b(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", *{f"old{i}" for i in range(32)}, *{f"new{i}" for i in range(32)}, *{f"mask{i}" for i in range(32)}, *{f"out{i}" for i in range(32)}}
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0].keys())) if rows else sorted(required)
        return False, "missing_columns=" + ",".join(missing[:12])
    errors = 0
    for row in _sample_rows_every_10ns(rows):
        for idx in range(32):
            expected = row[f"new{idx}"] > 0.45 if row[f"mask{idx}"] > 0.45 else row[f"old{idx}"] > 0.45
            if (row[f"out{idx}"] > 0.45) != expected:
                errors += 1
    return errors == 0, f"bit_errors={errors}"

CHECKER_ID = "v4_058_masked_config_update_32b"
CHECKER: Checker = check_masked_config_update_32b
