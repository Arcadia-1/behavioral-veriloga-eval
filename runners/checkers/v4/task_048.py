"""Task-specific checker for canonical v4 DUT 048."""
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

def check_bin_to_thermometer_decoder_8b(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "en", *{f"b{i}" for i in range(8)}, *{f"th{i}" for i in range(256)}}
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0].keys())) if rows else sorted(required)
        return False, "missing_columns=" + ",".join(missing[:12])

    vth = 0.45
    samples = _sample_rows_every_10ns(rows)

    checked_codes: list[int] = []
    enable_low_ok = True
    cumulative_errors = 0
    count_errors = 0
    boundary_seen = set()
    for row in samples:
        code = sum((1 << bit) for bit in range(8) if row[f"b{bit}"] > vth)
        enabled = row["en"] > vth
        expected_count = code if enabled else 0
        actual_high = {i for i in range(256) if row[f"th{i}"] > vth}
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

    ok = (
        enable_low_ok
        and count_errors == 0
        and cumulative_errors == 0
        and {0, 1, 255}.issubset(boundary_seen)
        and -1 in checked_codes
    )
    return ok, (
        f"checked={checked_codes} boundary_seen={sorted(boundary_seen)} "
        f"enable_low_ok={enable_low_ok} count_errors={count_errors} "
        f"cumulative_errors={cumulative_errors}"
    )

CHECKER_ID = "v4_048_bin_to_thermometer_decoder_8b"
CHECKER: Checker = check_bin_to_thermometer_decoder_8b
