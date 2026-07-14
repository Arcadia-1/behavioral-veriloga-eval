"""Task-specific checker for canonical v4 DUT 059."""
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

def check_edge_interval_tdc_8b(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "start", "stop", "valid", *{f"code{i}" for i in range(8)}}
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0].keys())) if rows else sorted(required)
        return False, "missing_columns=" + ",".join(missing[:12])
    starts = _rising_times(rows, "start")
    stops = _rising_times(rows, "stop")
    errors = 0
    checked: list[int] = []
    for start_t, stop_t in zip(starts, stops):
        expected = max(0, min(255, int(round((stop_t - start_t) / 1e-9))))
        row = _sample_after(rows, stop_t, 0.20e-9)
        actual = _logic_bits_to_int(row, "code", 8)
        if row["valid"] <= 0.45 or abs(actual - expected) > 1:
            errors += 1
        checked.append(expected)
    return errors == 0 and len(checked) >= 3 and len(set(checked)) >= 3, f"checked={checked} errors={errors}"

CHECKER_ID = "v4_059_edge_interval_tdc_8b"
CHECKER: Checker = check_edge_interval_tdc_8b
