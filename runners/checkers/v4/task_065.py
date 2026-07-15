"""Task-specific checker for canonical v4 DUT 065."""
from __future__ import annotations

from ..api import Checker
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

def check_enable_gated_clock_pulse(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "en", "pulse"}
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0].keys())) if rows else sorted(required)
        return False, "missing_columns=" + ",".join(missing[:12])
    errors = 0
    saw_high = False
    saw_blocked = False
    edge_times = _rising_times(rows, "clk") + _falling_times(rows, "clk") + _rising_times(rows, "en") + _falling_times(rows, "en")
    for row in rows[:: max(1, len(rows) // 400)]:
        if any(abs(row["time"] - t) < 0.3e-9 for t in edge_times):
            continue
        if 0.1 < row["clk"] < 0.8 or 0.1 < row["en"] < 0.8 or 0.1 < row["pulse"] < 0.8:
            continue
        expected = row["en"] > 0.45 and row["clk"] > 0.45
        actual = row["pulse"] > 0.45
        if actual != expected:
            errors += 1
        saw_high = saw_high or actual
        saw_blocked = saw_blocked or (row["clk"] > 0.45 and row["en"] <= 0.45 and not actual)
    return errors == 0 and saw_high and saw_blocked, f"errors={errors} saw_high={saw_high} saw_blocked={saw_blocked}"

CHECKER_ID = "v4_065_enable_gated_clock_pulse"
CHECKER: Checker = check_enable_gated_clock_pulse
