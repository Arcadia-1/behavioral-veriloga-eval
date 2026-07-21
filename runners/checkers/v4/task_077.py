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

SEQUENCE = (-1.0, -0.5, 0.0, 0.5, 1.0, 0.5, 0.0, -0.5)
TRACE_CASES = (
    ("default", "vout_default", 0.01, 0.5e-9),
    ("override", "vout_override", 0.037, 0.8e-9),
)


def _sample_near(
    rows: list[dict[str, float]],
    noises: list[float],
    target_time: float,
    dt: float,
) -> tuple[float, float] | None:
    index = min(range(len(rows)), key=lambda item: abs(rows[item]["time"] - target_time))
    distance = abs(rows[index]["time"] - target_time)
    if distance > 0.12 * dt:
        return None
    return noises[index], distance


def _check_parameter_case(
    rows: list[dict[str, float]],
    *,
    label: str,
    output: str,
    sigma: float,
    dt: float,
) -> tuple[bool, str]:
    noises = [row[output] - row["vin_i"] for row in rows]
    early: list[float] = []
    late: list[float] = []
    max_sample_distance = 0.0
    for interval in range(24):
        pair = []
        for phase in (0.30, 0.70):
            sampled = _sample_near(rows, noises, (interval + phase) * dt, dt)
            if sampled is None:
                return False, diagnostic(
                    "P_PERIODIC_UPDATE",
                    f"{label}_insufficient_time_resolution",
                    expected=f"samples_within_0.12_dt_for_{output}",
                    observed=f"interval={interval} phase={phase:.2f}",
                    event=label,
                )
            value, distance = sampled
            pair.append(value)
            max_sample_distance = max(max_sample_distance, distance)
        early.append(pair[0])
        late.append(pair[1])

    amplitude = max(abs(value) for value in early + late)
    amplitude_tolerance = max(1e-6, 0.06 * sigma)
    if abs(amplitude - sigma) > amplitude_tolerance:
        return False, diagnostic(
            "P_ADDITIVE_OUTPUT",
            f"{label}_sigma_mismatch",
            expected=f"sigma={sigma:.6g}",
            observed=f"amplitude={amplitude:.6g}",
            event=label,
        )

    normalized = [value / sigma for value in late]
    sequence_error = max(
        abs(value - SEQUENCE[index % len(SEQUENCE)])
        for index, value in enumerate(normalized)
    )
    if sequence_error > 0.08:
        return False, diagnostic(
            "P_DETERMINISTIC_SEQUENCE",
            f"{label}_sequence_or_dt_mismatch",
            expected=f"public_sequence_at_dt={dt:.4e}",
            observed=f"max_normalized_error={sequence_error:.4f}",
            event=label,
        )

    hold_error = max(abs(first - second) for first, second in zip(early, late))
    if hold_error > amplitude_tolerance:
        return False, diagnostic(
            "P_SAMPLE_HOLD",
            f"{label}_interinterval_variation",
            expected="piecewise_constant_between_updates",
            observed=f"max_hold_error={hold_error:.6g}",
            event=label,
        )

    cycle_means = [sum(normalized[start : start + 8]) / 8 for start in (0, 8, 16)]
    if max(abs(value) for value in cycle_means) > 0.04:
        return False, diagnostic(
            "P_ZERO_MEAN_DITHER",
            f"{label}_cycle_mean_mismatch",
            expected="each_eight_sample_mean=0",
            observed="cycle_means=" + ",".join(f"{value:.4f}" for value in cycle_means),
            event=label,
        )

    detail = (
        f"{label}:sigma={amplitude:.6g},dt={dt:.4e},"
        f"sequence_error={sequence_error:.4f},hold_error={hold_error:.6g},"
        f"sample_distance={max_sample_distance:.3e}"
    )
    return True, detail


def check_noise_gen(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin_i", *(output for _, output, _, _ in TRACE_CASES)}
    missing = require_signals(rows, required, "P_ADDITIVE_OUTPUT")
    if missing is not None:
        return False, missing

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
