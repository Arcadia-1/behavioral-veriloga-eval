"""Task-specific checker for canonical v4 DUT 376."""
from __future__ import annotations

from checkers.api import Checker
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

def _v4_missing_columns(rows: list[dict[str, float]], required: set[str]) -> str | None:
    if not rows:
        return "missing_columns=" + ",".join(sorted(required)[:16])
    missing = sorted(required - set(rows[0].keys()))
    if missing:
        return "missing_columns=" + ",".join(missing[:16])
    return None

def _v4_clip(value: float, lo: float = 0.0, hi: float = 0.9) -> float:
    return max(lo, min(hi, value))

def _v4_close(actual: float, expected: float, tol: float = 0.07) -> bool:
    return abs(actual - expected) <= tol

def check_v4_pwm_ramp_modulator_front_end(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "enable", "vctrl", "ramp_out", "pwm_out", "cycle_start", "duty_metric"}
    missing = _v4_missing_columns(rows, required)
    if missing:
        return False, missing
    ramp = 0.0
    errors = 0
    checked = 0
    wraps = 0
    highs = 0
    lows = 0
    for edge_t in _rising_times(rows, "clk"):
        edge_row = min(rows, key=lambda row: abs(row["time"] - edge_t))
        sample = _sample_after(rows, edge_t, 0.8e-9)
        if edge_row["rst"] > 0.45 or edge_row["enable"] <= 0.45:
            ramp = 0.0
            expected_pwm = 0.0
            expected_cycle = 0.0
            expected_duty = 0.0
        else:
            expected_cycle = 0.0
            if ramp >= 0.9 - 0.15 / 2.0:
                ramp = 0.0
                expected_cycle = 0.9
                wraps += 1
            else:
                ramp += 0.15
            expected_pwm = 0.9 if edge_row["vctrl"] > ramp else 0.0
            expected_duty = _v4_clip(edge_row["vctrl"])
            highs += int(expected_pwm > 0.45)
            lows += int(expected_pwm <= 0.45)
        if not _v4_close(sample["ramp_out"], ramp, 0.06):
            errors += 1
        if (sample["pwm_out"] > 0.45) != (expected_pwm > 0.45):
            errors += 1
        if (sample["cycle_start"] > 0.45) != (expected_cycle > 0.45):
            errors += 1
        if not _v4_close(sample["duty_metric"], expected_duty, 0.06):
            errors += 1
        checked += 1
    ok = errors == 0 and checked >= 8 and wraps >= 2 and highs > 0 and lows > 0
    return ok, f"v4_pwm_ramp checked={checked} wraps={wraps} highs={highs} lows={lows} errors={errors}"

CHECKER_ID = "v4_376_pwm_ramp_modulator_front_end"
CHECKER: Checker = check_v4_pwm_ramp_modulator_front_end
