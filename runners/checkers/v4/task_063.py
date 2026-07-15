"""Task-specific checker for canonical v4 DUT 063."""
from __future__ import annotations

from ..api import Checker
def _logic_bits_to_int(row: dict[str, float], prefix: str, width: int, vth: float = 0.45) -> int:
    return sum((1 << bit) for bit in range(width) if row[f"{prefix}{bit}"] > vth)

def check_settling_window_detector(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin", "target", "tol", "settled", *{f"t_code{i}" for i in range(8)}}
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0].keys())) if rows else sorted(required)
        return False, "missing_columns=" + ",".join(missing[:12])
    hold = 20e-9
    flags = [abs(row["vin"] - row["target"]) <= row["tol"] + 1e-12 for row in rows]
    intervals: list[tuple[float, float]] = []
    start: float | None = rows[0]["time"] if flags[0] else None
    for idx in range(1, len(rows)):
        if flags[idx] and not flags[idx - 1]:
            start = rows[idx]["time"]
        elif flags[idx - 1] and not flags[idx] and start is not None:
            intervals.append((start, rows[idx]["time"]))
            start = None
    if start is not None:
        intervals.append((start, rows[-1]["time"]))

    long_intervals = [(a, b) for a, b in intervals if b - a >= hold + 2e-9]
    if not long_intervals:
        return False, f"no_long_settling_interval intervals={intervals}"

    errors = 0
    settled_seen = False
    early_seen = False
    reset_seen = len(intervals) >= 2
    samples: list[tuple[float, dict[str, float]]] = []
    t = 2.5e-9
    while t <= rows[-1]["time"] + 1e-15:
        samples.append((t, min(rows, key=lambda row: abs(row["time"] - t))))
        t += 2.5e-9

    for sample_t, row in samples:
        actual_settled = row["settled"] > 0.45
        in_allowed_settled_region = any((entry + hold + 1e-9) <= sample_t <= (exit_t - 1e-9) for entry, exit_t in long_intervals)
        in_early_region = any((entry + 1e-9) <= sample_t < (entry + hold - 1e-9) for entry, exit_t in long_intervals)
        if actual_settled and in_early_region:
            early_seen = True
            errors += 1
        if actual_settled and not any((entry + hold - 1e-9) <= sample_t <= (exit_t + 1e-9) for entry, exit_t in long_intervals):
            errors += 1
        if in_allowed_settled_region:
            if not actual_settled:
                errors += 1
            else:
                settled_seen = True
                entry = next(entry for entry, exit_t in long_intervals if (entry + hold + 1e-9) <= sample_t <= (exit_t - 1e-9))
                expected_code = max(0, min(255, int(round(entry / 1e-9))))
                actual_code = _logic_bits_to_int(row, "t_code", 8)
                if abs(actual_code - expected_code) > 1:
                    errors += 1
    return errors == 0 and settled_seen and reset_seen and not early_seen, (
        f"errors={errors} intervals={[(round(a/1e-9,1), round(b/1e-9,1)) for a,b in long_intervals]} "
        f"settled_seen={settled_seen} reset_seen={reset_seen} early_seen={early_seen}"
    )

CHECKER_ID = "v4_063_settling_window_detector"
CHECKER: Checker = check_settling_window_detector
