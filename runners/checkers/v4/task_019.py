"""Stimulus-relative checker for canonical v4 DUT 019."""

from __future__ import annotations

from statistics import median

from ..api import Checker, Row
from .trace_utils import property_diagnostics, threshold_crossings


def _slope(points: list[tuple[float, float]]) -> float | None:
    if len(points) < 8:
        return None
    origin = points[0][0]
    xs = [time_s - origin for time_s, _ in points]
    ys = [value for _, value in points]
    xbar = sum(xs) / len(xs)
    ybar = sum(ys) / len(ys)
    denominator = sum((x - xbar) ** 2 for x in xs)
    return None if denominator <= 0 else sum((x - xbar) * (y - ybar) for x, y in zip(xs, ys)) / denominator


def check_vco_phase_integrator(rows: list[Row]) -> tuple[bool, str]:
    required = {"time", "vctrl", "phase", "clk"}
    missing = sorted(required - (set(rows[0]) if rows else set()))
    if missing:
        return False, "missing_columns=" + ",".join(missing)

    unwrapped: list[tuple[float, float, float]] = []
    wraps = 0
    previous = rows[0]["phase"]
    for row in rows:
        phase = row["phase"]
        # A smoothed wrap can be represented by several small downward trace
        # steps, so detect the observable midscale crossing rather than one
        # large adjacent-row jump.
        if previous >= 0.5 and phase < 0.5:
            wraps += 1
        unwrapped.append((row["time"], phase + wraps, row["vctrl"]))
        previous = phase

    control_min = min(row["vctrl"] for row in rows)
    control_max = max(row["vctrl"] for row in rows)
    threshold = 0.5 * (control_min + control_max)
    control_steps = threshold_crossings(rows, "vctrl", threshold=threshold, direction=1)
    split = control_steps[0] if control_steps else rows[-1]["time"]
    guard = max(2e-9, 0.02 * (rows[-1]["time"] - rows[0]["time"]))
    low_points = [(time_s, value) for time_s, value, control in unwrapped if rows[0]["time"] + guard <= time_s <= split - guard and control < threshold]
    high_points = [(time_s, value) for time_s, value, control in unwrapped if split + guard <= time_s <= rows[-1]["time"] - guard and control > threshold]
    low_slope = _slope(low_points)
    high_slope = _slope(high_points)
    low_control = median(control for _, _, control in unwrapped if control < threshold) if any(control < threshold for _, _, control in unwrapped) else 0.0
    high_control = median(control for _, _, control in unwrapped if control > threshold) if any(control > threshold for _, _, control in unwrapped) else 0.0
    expected_low = (0.03 + 0.09 * low_control) / 1e-9
    expected_high = (0.03 + 0.09 * high_control) / 1e-9
    slope_errors = int(low_slope is None) + int(high_slope is None)
    if low_slope is not None:
        slope_errors += abs(low_slope - expected_low) > 0.18 * expected_low
    if high_slope is not None:
        slope_errors += abs(high_slope - expected_high) > 0.18 * expected_high

    clock_toggles = len(threshold_crossings(rows, "clk", direction=0))
    toggle_errors = abs(clock_toggles - wraps)
    phase_min = min(row["phase"] for row in rows)
    phase_max = max(row["phase"] for row in rows)
    range_errors = int(phase_min < -0.04) + int(phase_max >= 1.04) + int(phase_max < 0.75)
    rate_errors = int(low_slope is None or high_slope is None or high_slope <= 1.45 * low_slope)
    coverage_missing = int(not control_steps) + int(len(low_points) < 8) + int(len(high_points) < 8) + int(wraps < 3)
    counts = {
        "P_PERIODIC_PHASE_UPDATE": slope_errors + coverage_missing,
        "P_WRAPPED_PHASE_RANGE": range_errors,
        "P_WRAP_TOGGLES_CLOCK": toggle_errors + int(wraps < 3),
        "P_CONTROLLED_EDGE_RATE": rate_errors + int(not control_steps),
    }
    ok = coverage_missing == 0 and all(count == 0 for count in counts.values())
    coverage = "" if coverage_missing == 0 else f" insufficient_excitation={coverage_missing}"
    return ok, (
        f"wraps={wraps} clock_toggles={clock_toggles} phase_range={phase_min:.3f}/{phase_max:.3f} "
        f"slopes={low_slope}/{high_slope} expected={expected_low:.3e}/{expected_high:.3e}{coverage}; "
        f"{property_diagnostics(counts)}"
    )


CHECKER_ID = "v4_019_vco_phase_integrator"
CHECKER: Checker = check_vco_phase_integrator
