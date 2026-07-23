"""Task-specific checker for canonical v4 DUT 077."""
from __future__ import annotations

from bisect import bisect_right
import math

from ..api import Checker
from .stimulus_relative import diagnostic, pass_note, require_signals


PROPERTY_IDS = (
    "P_PERIODIC_UPDATE",
    "P_SAMPLE_HOLD",
    "P_ADDITIVE_OUTPUT",
    "P_DETERMINISTIC_SEQUENCE",
    "P_ZERO_MEAN_DITHER",
)

SEQUENCE = (-1.0, -0.5, 0.0, 0.5, 1.0, 0.5, 0.0, -0.5)
TRACE_CASES = (
    ("default", "vout_default", 0.01, 0.5e-9),
    ("override", "vout_override", 0.037, 0.8e-9),
)
TRANSITION_GUARD_FRACTION = 0.12
LEVEL_TOLERANCE_FRACTION = 0.06
MIN_COMPLETE_INTERVALS = 24
MAX_COMPLETE_INTERVALS = 128
STABLE_PROBE_PHASES = (TRANSITION_GUARD_FRACTION, 0.5, 0.88)


def _invalid_trace(category: str, observed: str) -> tuple[bool, str]:
    return False, diagnostic(
        "P_ADDITIVE_OUTPUT",
        category,
        expected="finite_complete_ordered_trace",
        observed=observed,
        event="full_trace",
    )


def _finite(value: object) -> bool:
    try:
        return math.isfinite(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return False


def _validate_rows(
    rows: list[dict[str, float]], required: set[str]
) -> tuple[bool, str]:
    for row_index, row in enumerate(rows):
        missing = sorted(required - set(row))
        if missing:
            return _invalid_trace(
                "invalid_trace",
                f"row={row_index},missing={','.join(missing)}",
            )
        for signal in sorted(required):
            if not _finite(row[signal]):
                return _invalid_trace(
                    "nonfinite_trace_value",
                    f"row={row_index},signal={signal}",
                )

    for row_index, (left, right) in enumerate(zip(rows, rows[1:]), start=1):
        step = right["time"] - left["time"]
        if not _finite(step):
            return _invalid_trace("nonfinite_derived_time_step", f"row={row_index}")
        if step < 0.0:
            return _invalid_trace("unordered_trace", f"row={row_index}")
    return True, ""


def _interpolate(
    rows: list[dict[str, float]],
    times: list[float],
    signal: str,
    target: float,
) -> float:
    right = bisect_right(times, target)
    if right == 0:
        return rows[0][signal]
    left = right - 1
    if times[left] == target or right == len(rows):
        return rows[left][signal]

    t0 = times[left]
    t1 = times[right]
    if t1 == t0:
        return rows[right][signal]
    alpha = (target - t0) / (t1 - t0)
    return rows[left][signal] + alpha * (rows[right][signal] - rows[left][signal])


def _interpolate_within_interval(
    rows: list[dict[str, float]],
    times: list[float],
    signal: str,
    target: float,
    stop: float,
) -> float:
    right = bisect_right(times, target)
    if right == 0 or right == len(rows):
        return _interpolate(rows, times, signal, target)
    left = right - 1
    if times[left] == target:
        return rows[left][signal]
    if times[right] >= stop:
        # The row at ``stop`` belongs to the next timer interval.  A sparse
        # trace must not smear that update backwards into the held interval.
        return rows[left][signal]
    return _interpolate(rows, times, signal, target)


def _check_parameter_case(
    rows: list[dict[str, float]],
    *,
    label: str,
    output: str,
    sigma: float,
    dt: float,
) -> tuple[bool, str]:
    horizon_ratio = rows[-1]["time"] / dt
    if not _finite(horizon_ratio):
        return _invalid_trace("nonfinite_derived_horizon", f"case={label}")
    complete_intervals = math.floor(horizon_ratio + 1e-9)
    if complete_intervals < MIN_COMPLETE_INTERVALS:
        return False, diagnostic(
            "P_PERIODIC_UPDATE",
            f"{label}_insufficient_coverage",
            expected=f"complete_intervals>={MIN_COMPLETE_INTERVALS}",
            observed=f"complete_intervals={complete_intervals}",
            event=label,
        )
    if complete_intervals > MAX_COMPLETE_INTERVALS:
        return _invalid_trace(
            "unexpected_trace_horizon",
            f"case={label},complete_intervals={complete_intervals}",
        )

    tolerance = max(1e-6, LEVEL_TOLERANCE_FRACTION * sigma)
    if not _finite(tolerance):
        return _invalid_trace("nonfinite_derived_tolerance", f"case={label}")

    interval_levels: list[float] = []
    max_level_error = 0.0
    max_hold_span = 0.0
    sample_cursor = 0
    times = [row["time"] for row in rows]
    for interval in range(complete_intervals):
        start = interval * dt
        stable_start = start + TRANSITION_GUARD_FRACTION * dt
        stop = (interval + 1) * dt
        if not all(_finite(value) for value in (start, stable_start, stop)):
            return _invalid_trace(
                "nonfinite_derived_interval_boundary",
                f"case={label},interval={interval}",
            )

        while (
            sample_cursor + 1 < len(rows)
            and rows[sample_cursor + 1]["time"] <= start + 1e-15
        ):
            sample_cursor += 1
        sampled_vin = rows[sample_cursor]["vin_i"]
        if not _finite(sampled_vin):
            return _invalid_trace(
                "nonfinite_derived_sampled_vin",
                f"case={label},interval={interval}",
            )

        stable = [
            (row_index, row["time"], row[output] - sampled_vin)
            for row_index, row in enumerate(rows)
            if stable_start <= row["time"] < stop
        ]
        stable.extend(
            (
                -1,
                probe_time,
                _interpolate_within_interval(
                    rows,
                    times,
                    output,
                    probe_time,
                    stop,
                )
                - sampled_vin,
            )
            for probe_time in (
                start + phase * dt for phase in STABLE_PROBE_PHASES
            )
        )
        if any(not _finite(value) for _, _, value in stable):
            return _invalid_trace(
                "nonfinite_derived_noise",
                f"case={label},interval={interval}",
            )

        expected = sigma * SEQUENCE[interval % len(SEQUENCE)]
        if not _finite(expected):
            return _invalid_trace(
                "nonfinite_derived_expected_level",
                f"case={label},interval={interval}",
            )
        stable_values = [value for _, _, value in stable]
        hold_span = max(stable_values) - min(stable_values)
        if not _finite(hold_span):
            return _invalid_trace(
                "nonfinite_derived_hold_span",
                f"case={label},interval={interval}",
            )
        max_hold_span = max(max_hold_span, hold_span)

        for row_index, stable_time, value in stable:
            level_error = abs(value - expected)
            if not _finite(level_error):
                return _invalid_trace(
                    "nonfinite_derived_level_error",
                    f"row={row_index},signal={output}",
                )
            max_level_error = max(max_level_error, level_error)
            if level_error > tolerance:
                location = (
                    f"row={row_index}"
                    if row_index >= 0
                    else f"time={stable_time:.4e}"
                )
                return False, diagnostic(
                    "P_SAMPLE_HOLD",
                    f"{label}_level_or_hold_mismatch",
                    expected="public_level_throughout_stable_interval",
                    observed=f"interval={interval},{location}",
                    event=label,
                )

        interval_level = _interpolate_within_interval(
            rows,
            times,
            output,
            start + 0.5 * dt,
            stop,
        ) - sampled_vin
        if not _finite(interval_level):
            return _invalid_trace(
                "nonfinite_derived_interval_level",
                f"case={label},interval={interval}",
            )
        interval_levels.append(interval_level)

    amplitude = max(abs(value) for value in interval_levels)
    amplitude_error = abs(amplitude - sigma)
    if not _finite(amplitude) or not _finite(amplitude_error):
        return _invalid_trace("nonfinite_derived_amplitude", f"case={label}")
    if amplitude_error > tolerance:
        return False, diagnostic(
            "P_ADDITIVE_OUTPUT",
            f"{label}_sigma_mismatch",
            expected=f"sigma={sigma:.6g}",
            observed=f"amplitude={amplitude:.6g}",
            event=label,
        )

    normalized = [value / sigma for value in interval_levels]
    if not all(_finite(value) for value in normalized):
        return _invalid_trace("nonfinite_derived_normalized_level", f"case={label}")
    sequence_errors = [
        abs(value - SEQUENCE[index % len(SEQUENCE)])
        for index, value in enumerate(normalized)
    ]
    if not all(_finite(value) for value in sequence_errors):
        return _invalid_trace("nonfinite_derived_sequence_error", f"case={label}")
    sequence_error = max(sequence_errors)
    if sequence_error > LEVEL_TOLERANCE_FRACTION:
        return False, diagnostic(
            "P_DETERMINISTIC_SEQUENCE",
            f"{label}_sequence_or_dt_mismatch",
            expected=f"public_sequence_at_dt={dt:.4e}",
            observed=f"max_normalized_error={sequence_error:.4f}",
            event=label,
        )

    cycle_means = []
    for start in range(0, len(normalized) - 7, 8):
        cycle_mean = math.fsum(normalized[start : start + 8]) / 8
        if not _finite(cycle_mean):
            return _invalid_trace("nonfinite_derived_cycle_mean", f"case={label}")
        cycle_means.append(cycle_mean)
    if not cycle_means or max(abs(value) for value in cycle_means) > 0.04:
        return False, diagnostic(
            "P_ZERO_MEAN_DITHER",
            f"{label}_cycle_mean_mismatch",
            expected="each_eight_sample_mean=0",
            observed="cycle_mean_out_of_tolerance",
            event=label,
        )

    detail = (
        f"{label}:intervals={complete_intervals},sigma={amplitude:.6g},dt={dt:.4e},"
        f"level_error={max_level_error:.6g},hold_span={max_hold_span:.6g},"
        f"sequence_error={sequence_error:.4f}"
    )
    return True, detail


def check_noise_gen(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin_i", *(output for _, output, _, _ in TRACE_CASES)}
    missing = require_signals(rows, required, "P_ADDITIVE_OUTPUT")
    if missing is not None:
        return False, missing
    valid, detail = _validate_rows(rows, required)
    if not valid:
        return False, detail

    details = []
    for label, output, sigma, dt in TRACE_CASES:
        passed, detail = _check_parameter_case(
            rows,
            label=label,
            output=output,
            sigma=sigma,
            dt=dt,
        )
        if not passed:
            return False, detail
        details.append(detail)
    return True, pass_note(PROPERTY_IDS, " ".join(details))


CHECKER_ID = "v4_077_dither_noise_like_deterministic_source"
CHECKER: Checker = check_noise_gen
