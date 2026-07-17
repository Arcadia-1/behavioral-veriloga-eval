"""Stimulus-relative checker for canonical v4 DUT 016."""

from __future__ import annotations

from ..api import Checker, Row
from .stimulus_relative import diagnostic
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


def _transition_fit(rows: list[Row], start: float, stop: float) -> list[Row]:
    start_out = sample_signal(rows, "vout", start)
    target = sample_signal(rows, "vin", start + 0.5 * (stop - start))
    if start_out is None or target is None or abs(target - start_out) < 1e-6:
        return []
    low = min(start_out + 0.10 * (target - start_out), start_out + 0.90 * (target - start_out))
    high = max(start_out + 0.10 * (target - start_out), start_out + 0.90 * (target - start_out))
    fit: list[Row] = []
    for row in rows:
        if not start < row["time"] < stop:
            continue
        if low <= row["vout"] <= high:
            fit.append(row)
        elif fit:
            break
    return fit


def _sustained_excursion(
    rises: list[float],
    falls: list[float],
    *,
    trace_stop: float,
    minimum_phase_duration: float = 4.0e-9,
) -> tuple[float, float, float] | None:
    """Select a bidirectional excursion long enough to exercise periodic updates."""
    for rise_time in rises:
        fall_time = next((time_s for time_s in falls if time_s > rise_time), None)
        if fall_time is None or fall_time - rise_time < minimum_phase_duration:
            continue
        next_rise = next((time_s for time_s in rises if time_s > fall_time), trace_stop)
        if next_rise - fall_time >= minimum_phase_duration:
            return rise_time, fall_time, next_rise
    return None


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
        return False, diagnostic(
            "P_BIDIRECTIONAL_STEP_LIMIT",
            "insufficient_coverage",
            expected="sustained_rising_and_falling_excursions",
            observed=f"rises={len(rises)},falls={len(falls)}",
            event="full_trace",
        ) + f"; insufficient_excitation={coverage_missing}; {property_diagnostics(counts)}"

    time_scale = float(rows[0].get("_time_scale", 1.0))
    excursion = _sustained_excursion(
        rises,
        falls,
        trace_stop=rows[-1]["time"],
        minimum_phase_duration=4.0e-9 * time_scale,
    )
    if excursion is None:
        counts = {property_id: 1 for property_id in (
            "P_INITIAL_ZERO", "P_PERIODIC_UPDATE", "P_BIDIRECTIONAL_STEP_LIMIT",
            "P_NEAR_TARGET_SETTLE", "P_EVENTUAL_TRACKING",
        )}
        return False, diagnostic(
            "P_BIDIRECTIONAL_STEP_LIMIT",
            "insufficient_coverage",
            expected="bidirectional_phases>=4_update_periods",
            observed="no_qualifying_excursion",
            event="full_trace",
        ) + f"; insufficient_excitation=1; {property_diagnostics(counts)}"
    rise_time, fall_time, next_rise = excursion
    rising_fit = _transition_fit(rows, rise_time, fall_time)
    falling_fit = _transition_fit(rows, fall_time, next_rise)
    rising_slope = _slope(rising_fit)
    falling_slope = _slope(falling_fit)
    rate_errors = int(rising_slope is None) + int(falling_slope is None)
    if rising_slope is not None and falling_slope is not None:
        rate_errors += int(rising_slope <= 0.0) + int(falling_slope >= 0.0)
        larger_rate = max(abs(rising_slope), abs(falling_slope))
        rate_errors += int(
            larger_rate <= 0.0
            or abs(abs(rising_slope) - abs(falling_slope)) > 0.30 * larger_rate
        )

    initial = sample_signal(rows, "vout", rows[0]["time"])
    high_sample = sample_signal(rows, "vout", rise_time + 0.82 * (fall_time - rise_time))
    final_sample = sample_signal(rows, "vout", rows[-1]["time"])
    early_sample = sample_signal(rows, "vout", rise_time + 0.12 * (fall_time - rise_time))
    high_input = sample_signal(rows, "vin", rise_time + 0.5 * (fall_time - rise_time))
    start_output = sample_signal(rows, "vout", rise_time)
    final_input = rows[-1]["vin"]
    initial_error = int(initial is None or abs(initial) > 0.05)
    settle_errors = int(high_sample is None or high_input is None or abs(high_sample - high_input) > 0.08)
    settle_errors += int(final_sample is None or abs(final_sample - final_input) > 0.06)
    minimum_lag = max(
        1.25 * 0.015,
        0.20 * abs(high_input - start_output)
        if high_input is not None and start_output is not None
        else 0.0,
    )
    passthrough_errors = int(
        early_sample is None
        or high_input is None
        or abs(high_input - early_sample) < minimum_lag
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
    summary = (
        f"rise={rise_time:.3e} fall={fall_time:.3e} slopes={rising_slope}/{falling_slope} "
        f"high={high_sample} final={final_sample}{coverage}; {property_diagnostics(counts)}"
    )
    if not ok:
        failing_property = next(property_id for property_id, count in counts.items() if count)
        return False, diagnostic(
            failing_property,
            "semantic_mismatch",
            expected="public_slew_contract_satisfied",
            observed=f"mismatch_count={counts[failing_property]}",
            event=f"primary_excursion@{rise_time:.6e}s",
        ) + "; " + summary
    return True, summary


CHECKER_ID = "v4_016_slew_rate_limiter"
CHECKER: Checker = check_slew_rate_limiter
