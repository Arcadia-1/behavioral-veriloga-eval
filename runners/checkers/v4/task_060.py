"""Task-specific checker for canonical v4 DUT 060."""
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

def _falling_times(rows: list[dict[str, float]], col: str, vth: float = 0.45) -> list[float]:
    times: list[float] = []
    last = rows[0][col] > vth
    for row in rows[1:]:
        cur = row[col] > vth
        if last and not cur:
            times.append(row["time"])
        last = cur
    return times

def _sample_after(rows: list[dict[str, float]], t: float, delay: float = 5e-9) -> dict[str, float]:
    target = t + delay
    return min(rows, key=lambda row: abs(row["time"] - target))

def check_duty_cycle_meter_8b(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk_in", "valid", *{f"duty{i}" for i in range(8)}}
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0].keys())) if rows else sorted(required)
        return False, "missing_columns=" + ",".join(missing[:12])
    rises = _rising_times(rows, "clk_in")
    falls = _falling_times(rows, "clk_in")
    errors = 0
    checked: list[int] = []
    for first_rise, second_rise in zip(rises, rises[1:]):
        falls_in_cycle = [t for t in falls if first_rise < t < second_rise]
        if not falls_in_cycle:
            continue
        high_time = falls_in_cycle[0] - first_rise
        period = second_rise - first_rise
        expected = max(0, min(255, int(round(255.0 * high_time / period))))
        row = _sample_after(rows, second_rise)
        actual = _logic_bits_to_int(row, "duty", 8)
        if row["valid"] <= 0.45 or abs(actual - expected) > 1:
            errors += 1
        checked.append(expected)
    return errors == 0 and len(checked) >= 3 and len(set(checked)) >= 2, f"checked={checked} errors={errors}"

CHECKER_ID = "v4_060_duty_cycle_meter_8b"
CHECKER: Checker = check_duty_cycle_meter_8b
