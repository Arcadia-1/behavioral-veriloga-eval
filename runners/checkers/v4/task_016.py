"""Stimulus-relative checker for canonical v4 DUT 016."""

from __future__ import annotations

from ..api import Checker, Row
from .trace_utils import property_diagnostics, sample_signal, threshold_crossings


def _slope(rows: list[Row]) -> float | None:
    if len(rows) < 4:
        return None
    origin = rows[0]["time"]
    xs = [row["time"] - origin for row in rows]
    ys = [row["vout"] for row in rows]
    xbar = sum(xs) / len(xs)
    ybar = sum(ys) / len(ys)
    denominator = sum((x - xbar) ** 2 for x in xs)
    return None if denominator <= 0 else sum((x - xbar) * (y - ybar) for x, y in zip(xs, ys)) / denominator


def check_slew_rate_limiter(rows: list[Row]) -> tuple[bool, str]:
    required = {"time", "vin", "vout"}
    missing = sorted(required - (set(rows[0]) if rows else set()))
    if missing:
        return False, "missing_columns=" + ",".join(missing)

    vin_min = min(row["vin"] for row in rows)
    vin_max = max(row["vin"] for row in rows)
    threshold = 0.5 * (vin_min + vin_max)
    rises = threshold_crossings(rows, "vin", threshold=threshold, direction=1)
    falls = threshold_crossings(rows, "vin", threshold=threshold, direction=-1)
    coverage_missing = int(not rises) + int(not falls)
    if not rises or not falls:
        counts = {property_id: coverage_missing for property_id in (
            "P_INITIAL_ZERO", "P_PERIODIC_UPDATE", "P_BIDIRECTIONAL_STEP_LIMIT",
            "P_NEAR_TARGET_SETTLE", "P_EVENTUAL_TRACKING",
        )}
        return False, f"insufficient_excitation={coverage_missing}; {property_diagnostics(counts)}"

    rise_time = rises[0]
    fall_time = next((time_s for time_s in falls if time_s > rise_time), falls[-1])
    rising_fit = [row for row in rows if rise_time < row["time"] < fall_time and 0.10 <= row["vout"] <= 0.68]
    falling_fit = [row for row in rows if row["time"] > fall_time and 0.20 <= row["vout"] <= 0.70]
    rising_slope = _slope(rising_fit)
    falling_slope = _slope(falling_fit)
    target_rate = 0.015 / 1e-9
    rate_errors = int(rising_slope is None) + int(falling_slope is None)
    if rising_slope is not None:
        rate_errors += abs(rising_slope - target_rate) > 0.23 * target_rate
    if falling_slope is not None:
        rate_errors += abs(falling_slope + target_rate) > 0.23 * target_rate

    initial = sample_signal(rows, "vout", rows[0]["time"])
    high_sample = sample_signal(rows, "vout", rise_time + 0.82 * (fall_time - rise_time))
    final_sample = sample_signal(rows, "vout", rows[-1]["time"])
    early_sample = sample_signal(rows, "vout", rise_time + 0.12 * (fall_time - rise_time))
    high_input = sample_signal(rows, "vin", rise_time + 0.5 * (fall_time - rise_time))
    final_input = rows[-1]["vin"]
    initial_error = int(initial is None or abs(initial) > 0.05)
    settle_errors = int(high_sample is None or high_input is None or abs(high_sample - high_input) > 0.08)
    settle_errors += int(final_sample is None or abs(final_sample - final_input) > 0.06)
    passthrough_errors = int(
        early_sample is None or high_input is None or early_sample >= high_input - 0.25
    )
    coverage_missing += int(len(rising_fit) < 4) + int(len(falling_fit) < 4)
    counts = {
        "P_INITIAL_ZERO": initial_error,
        "P_PERIODIC_UPDATE": rate_errors + coverage_missing,
        "P_BIDIRECTIONAL_STEP_LIMIT": rate_errors + passthrough_errors,
        "P_NEAR_TARGET_SETTLE": settle_errors,
        "P_EVENTUAL_TRACKING": settle_errors,
    }
    ok = coverage_missing == 0 and all(count == 0 for count in counts.values())
    coverage = "" if coverage_missing == 0 else f" insufficient_excitation={coverage_missing}"
    return ok, (
        f"rise={rise_time:.3e} fall={fall_time:.3e} slopes={rising_slope}/{falling_slope} "
        f"high={high_sample} final={final_sample}{coverage}; {property_diagnostics(counts)}"
    )


CHECKER_ID = "v4_016_slew_rate_limiter"
CHECKER: Checker = check_slew_rate_limiter
