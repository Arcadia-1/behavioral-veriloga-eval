"""Task-specific checker for canonical v4 DUT 077."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import diagnostic, pass_note, require_signals


PROPERTY_IDS = (
    "P_PERIODIC_UPDATE",
    "P_SAMPLE_HOLD",
    "P_ADDITIVE_OUTPUT",
    "P_DETERMINISTIC_SEQUENCE",
    "P_ZERO_MEAN_DITHER",
)


def check_noise_gen(rows: list[dict[str, float]]) -> tuple[bool, str]:
    missing = require_signals(rows, {"time", "vin_i", "vout_o"}, "P_ADDITIVE_OUTPUT")
    if missing is not None:
        return False, missing
    noises = [r["vout_o"] - r["vin_i"] for r in rows]
    amplitude = max(abs(value) for value in noises)
    if amplitude <= 1e-6:
        return False, diagnostic(
            "P_DETERMINISTIC_SEQUENCE",
            "zero_amplitude",
            expected="nonzero_sigma_sequence",
            observed=f"max_abs={amplitude:.4g}",
            event="full_trace",
        )

    # Compress the trace into held levels. This recovers sigma and dt from the
    # public outputs, so legal parameter overrides are not mistaken for an
    # incorrect implementation.
    level_tolerance = max(1e-7, 0.10 * amplitude)
    levels: list[tuple[float, float]] = [(rows[0]["time"], noises[0])]
    for row, noise in zip(rows[1:], noises[1:]):
        if abs(noise - levels[-1][1]) > level_tolerance:
            levels.append((row["time"], noise))
    if len(levels) < 17:
        return False, diagnostic(
            "P_PERIODIC_UPDATE",
            "insufficient_coverage",
            expected="at_least_two_complete_eight_level_periods",
            observed=f"held_levels={len(levels)}",
            event="full_trace",
        )

    expected = (-1.0, -0.5, 0.0, 0.5, 1.0, 0.5, 0.0, -0.5)
    normalized = [value / amplitude for _, value in levels[:17]]
    sequence_error = max(
        abs(value - expected[index % len(expected)])
        for index, value in enumerate(normalized)
    )
    if sequence_error > 0.12:
        return False, diagnostic(
            "P_DETERMINISTIC_SEQUENCE",
            "sequence_mismatch",
            expected="[-1,-.5,0,.5,1,.5,0,-.5]_times_sigma_repeated",
            observed=f"max_normalized_error={sequence_error:.4f}",
            event="first_seventeen_held_levels",
        )

    update_intervals = [
        later[0] - earlier[0]
        for earlier, later in zip(levels[1:16], levels[2:17])
    ]
    sorted_intervals = sorted(update_intervals)
    inferred_dt = sorted_intervals[len(sorted_intervals) // 2]
    if inferred_dt <= 0 or max(abs(value - inferred_dt) for value in update_intervals) > 0.15 * inferred_dt:
        return False, diagnostic(
            "P_PERIODIC_UPDATE",
            "irregular_update_interval",
            expected="stable_parameterized_dt",
            observed=f"inferred_dt={inferred_dt:.4e}",
            event="first_two_sequence_periods",
        )

    max_hold_error = 0.0
    for index, (start, level) in enumerate(levels[:16]):
        stop = levels[index + 1][0]
        interior = [
            noise
            for row, noise in zip(rows, noises)
            if start <= row["time"] < stop
        ]
        if interior:
            max_hold_error = max(max_hold_error, max(abs(value - level) for value in interior))
    if max_hold_error > level_tolerance:
        return False, diagnostic(
            "P_SAMPLE_HOLD",
            "interinterval_variation",
            expected="piecewise_constant_between_updates",
            observed=f"max_hold_error={max_hold_error:.4g}",
            event="first_sixteen_intervals",
        )

    cycle_means = [sum(normalized[start : start + 8]) / 8 for start in (0, 8)]
    if max(abs(value) for value in cycle_means) > 0.06:
        return False, diagnostic(
            "P_ZERO_MEAN_DITHER",
            "cycle_mean_mismatch",
            expected="each_eight_sample_mean=0",
            observed=f"cycle_means={cycle_means[0]:.4f},{cycle_means[1]:.4f}",
            event="complete_sequence_periods",
        )
    note = (
        f"levels={len(levels)} inferred_sigma={amplitude:.4g} inferred_dt={inferred_dt:.4e} "
        f"max_sequence_error={sequence_error:.4f} max_hold_error={max_hold_error:.4g}"
    )
    return True, pass_note(PROPERTY_IDS, note)

CHECKER_ID = "v4_077_dither_noise_like_deterministic_source"
CHECKER: Checker = check_noise_gen
