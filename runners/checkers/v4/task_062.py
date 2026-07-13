"""Task-specific checker for canonical v4 DUT 062."""
from __future__ import annotations

from checkers.api import Checker
def _logic_bits_to_int(row: dict[str, float], prefix: str, width: int, vth: float = 0.45) -> int:
    return sum((1 << bit) for bit in range(width) if row[f"{prefix}{bit}"] > vth)

def _rising_times(rows: list[dict[str, float]], col: str, vth: float = 0.45) -> list[float]:
    times: list[float] = []
    last = rows[0][col] > vth
    for row in rows[1:]:
        cur = row[col] > vth
        if not last and cur:
            times.append(row["time"])
        last = cur
    return times

def _sample_after(rows: list[dict[str, float]], t: float, delay: float = 5e-9) -> dict[str, float]:
    target = t + delay
    return min(rows, key=lambda row: abs(row["time"] - target))

def check_ready_valid_latency_counter_12b(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "valid_i", "ready_i", "done", *{f"lat{i}" for i in range(12)}}
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0].keys())) if rows else sorted(required)
        return False, "missing_columns=" + ",".join(missing[:12])
    rise_rows = [_sample_after(rows, t, 1e-9) for t in _rising_times(rows, "clk")]
    active = False
    count = 0
    errors = 0
    checked: list[int] = []
    for row in rise_rows:
        valid = row["valid_i"] > 0.45
        ready = row["ready_i"] > 0.45
        if valid and not active:
            active = True
            count = 0
        elif active and not ready:
            count += 1
        if active and ready:
            expected = count
            actual = _logic_bits_to_int(row, "lat", 12)
            if row["done"] <= 0.45 or actual != expected:
                errors += 1
            checked.append(expected)
            active = False
    return errors == 0 and len(checked) >= 2 and max(checked, default=0) > 0, f"checked={checked} errors={errors}"

CHECKER_ID = "v4_062_latency_counter_ready_valid_12b"
CHECKER: Checker = check_ready_valid_latency_counter_12b
