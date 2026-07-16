"""Stimulus-relative checker for canonical v4 DUT 013."""

from __future__ import annotations

from statistics import median

from ..api import Checker, Row
from .trace_utils import property_diagnostics, stable_logic_plateaus


def _slope(rows: list[Row], signal: str) -> float | None:
    if len(rows) < 4:
        return None
    origin = rows[0]["time"]
    xs = [row["time"] - origin for row in rows]
    ys = [row[signal] for row in rows]
    xbar = sum(xs) / len(xs)
    ybar = sum(ys) / len(ys)
    denominator = sum((x - xbar) ** 2 for x in xs)
    if denominator <= 0.0:
        return None
    return sum((x - xbar) * (y - ybar) for x, y in zip(xs, ys)) / denominator


def check_resettable_integrator(rows: list[Row]) -> tuple[bool, str]:
    required = {"time", "vin", "rst", "vout"}
    missing = sorted(required - (set(rows[0]) if rows else set()))
    if missing:
        return False, "missing_columns=" + ",".join(missing)

    plateaus = stable_logic_plateaus(rows, ["rst"], minimum_duration_s=2e-9)
    reset_segments = [(start, end) for start, end, state in plateaus if state == (1,)]
    active_segments = [(start, end) for start, end, state in plateaus if state == (0,)]
    reset_errors = 0
    for start, end in reset_segments:
        settled = start + max(1, 2 * (end - start) // 3)
        reset_errors += sum(abs(row["vout"]) > 0.05 for row in rows[settled : end + 1])

    slopes: list[float] = []
    slope_errors = 0
    monotonic_errors = 0
    restart_seen = False
    for segment_index, (start, end) in enumerate(active_segments):
        segment = rows[start : end + 1]
        fit = [row for row in segment if 0.06 <= row["vout"] <= 0.72]
        measured = _slope(fit, "vout")
        if measured is not None:
            slopes.append(measured)
            expected = 1.0e9 * median(row["vin"] for row in fit)
            slope_errors += abs(measured - expected) > max(0.22 * abs(expected), 2.5e5)
        else:
            slope_errors += 1
        monotonic_errors += sum(
            right["vout"] + 0.012 < left["vout"]
            for left, right in zip(segment, segment[1:])
        )
        if segment_index > 0 and max(row["vout"] for row in segment) > 0.08:
            restart_seen = True

    initial_error = int(abs(rows[0]["vout"]) > 0.05)
    maximum = max(row["vout"] for row in rows)
    minimum = min(row["vout"] for row in rows)
    clamp_errors = int(maximum < 0.80) + int(maximum > 0.90) + int(minimum < -0.04)
    coverage_missing = (
        int(len(reset_segments) < 2)
        + int(len(active_segments) < 2)
        + int(len(slopes) < 2)
        + int(not restart_seen)
        + int(maximum < 0.80)
    )
    counts = {
        "P_INITIAL_ZERO": initial_error,
        "P_TIMER_INTEGRATION": slope_errors + int(len(slopes) < 2),
        "P_ACTIVE_HIGH_RESET": reset_errors + int(len(reset_segments) < 2) + int(not restart_seen),
        "P_ACCUMULATOR_CLAMP": clamp_errors,
        "P_EVENT_HOLD": monotonic_errors,
    }
    ok = coverage_missing == 0 and all(count == 0 for count in counts.values())
    coverage = "" if coverage_missing == 0 else f" insufficient_excitation={coverage_missing}"
    return ok, (
        f"reset_segments={len(reset_segments)} active_segments={len(active_segments)} "
        f"slopes={[round(value, 1) for value in slopes]} range={minimum:.3f}/{maximum:.3f} "
        f"restart_seen={restart_seen}{coverage}; {property_diagnostics(counts)}"
    )


CHECKER_ID = "v4_013_resettable_integrator"
CHECKER: Checker = check_resettable_integrator
