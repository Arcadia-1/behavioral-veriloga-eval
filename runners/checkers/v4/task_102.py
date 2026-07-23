"""Task-specific checker for canonical v4 DUT 102."""
from __future__ import annotations

import math

from ..api import Checker
from .stimulus_relative import (
    crossings,
    diagnostic,
    event_settle_delay,
    pass_note,
    require_signals,
    sample,
)


CHECKER_ID = "v4_102_clocked_sine_source"
PROPERTY_IDS = (
    "P_RESET_COMMON_MODE",
    "P_RISING_EDGE_SAMPLE",
    "P_SAMPLED_SINE",
    "P_REFERENCE_SIDE_COMMON_MODE",
    "P_INTEREDGE_HOLD",
    "P_SEEDED_REPEATABILITY",
)

_POSITIVE_OUTPUTS = ("vinp", "vinp_seed_b", "vinp_seed_alt", "vinp_sigma0")
_NEGATIVE_OUTPUTS = ("vinn", "vinn_seed_b", "vinn_seed_alt", "vinn_sigma0")
_REQUIRED = {
    "time",
    "clk",
    "rst_n",
    "vamp_p",
    "vamp_n",
    *_POSITIVE_OUTPUTS,
    *_NEGATIVE_OUTPUTS,
}
_AMPLITUDE = 0.02
_FREQUENCY_HZ = 1.0e6
_SAME_SEED_TOLERANCE = 2.5e-4
_SIGMA_ZERO_TOLERANCE = 1.5e-3
_MIN_SEED_SEPARATION = 1.0e-3
_MIN_NOISE_RESIDUAL = 1.0e-3


def _failure(
    property_id: str,
    category: str,
    *,
    expected: str,
    observed: str,
    event: str,
) -> tuple[bool, str]:
    return False, diagnostic(
        property_id,
        category,
        expected=expected,
        observed=observed,
        event=event,
    )


def _max_signal_value(
    rows: list[dict[str, float]],
    signals: tuple[str, ...],
    *,
    default: float,
) -> float:
    values = [row[signal] for row in rows for signal in signals if signal in row]
    return max(values, default=default)


def check_v3_clocked_sine_source(
    rows: list[dict[str, float]],
) -> tuple[bool, str]:
    missing = require_signals(rows, _REQUIRED, "P_SEEDED_REPEATABILITY")
    if missing is not None:
        return False, missing
    for row_index, row in enumerate(rows):
        for signal in _REQUIRED:
            if not math.isfinite(float(row[signal])):
                return _failure(
                    "P_SAMPLED_SINE",
                    "nonfinite_trace_value",
                    expected="finite_public_trace",
                    observed=f"row={row_index},signal={signal}",
                    event="full_trace",
                )

    vdd = _max_signal_value(rows, ("clk", "rst_n"), default=0.9)
    vth = 0.5 * vdd
    common_mode = 0.5 * vdd
    reset_rows = [row for row in rows if row["rst_n"] < vth]
    reset_cm_err = max(
        (
            abs(row[signal] - common_mode)
            for row in reset_rows
            for signal in (*_POSITIVE_OUTPUTS, *_NEGATIVE_OUTPUTS)
        ),
        default=float("inf"),
    )
    if reset_cm_err > 0.025:
        return _failure(
            "P_RESET_COMMON_MODE",
            "reset_common_mode_mismatch",
            expected="all_source_outputs_at_vdd_over_2",
            observed=f"max_error={reset_cm_err:.6g}",
            event="reset_window",
        )

    reference_err = max(
        (
            abs(row[signal] - common_mode)
            for row in rows
            for signal in _NEGATIVE_OUTPUTS
        ),
        default=float("inf"),
    )
    if reference_err > 0.015:
        return _failure(
            "P_REFERENCE_SIDE_COMMON_MODE",
            "reference_common_mode_mismatch",
            expected="all_reference_outputs_at_vdd_over_2",
            observed=f"max_error={reference_err:.6g}",
            event="full_trace",
        )

    all_edges = crossings(rows, "clk", threshold=vth, direction="rising")
    settle = event_settle_delay(all_edges, fraction=0.08, maximum_s=1.5e-9)
    edges = []
    for edge in all_edges:
        reset = sample(rows, "rst_n", edge + settle)
        if reset is not None and reset >= vth:
            edges.append(edge)
    if len(edges) < 20:
        return _failure(
            "P_RISING_EDGE_SAMPLE",
            "insufficient_active_clock_edges",
            expected="active_edges>=20",
            observed=f"active_edges={len(edges)}",
            event="clock_edge_set",
        )

    sampled: dict[str, list[float]] = {signal: [] for signal in _POSITIVE_OUTPUTS}
    hold_errors: list[float] = []
    repeat_errors: list[float] = []
    alternate_seed_differences: list[float] = []
    sigma_zero_errors: list[float] = []
    noise_residuals: list[float] = []
    for edge_index, (left, right) in enumerate(zip(edges, edges[1:])):
        probe = left + settle
        hold_probe = right - settle
        if hold_probe <= probe:
            continue
        values: dict[str, float] = {}
        for signal in (*_POSITIVE_OUTPUTS, *_NEGATIVE_OUTPUTS):
            value = sample(rows, signal, probe)
            held = sample(rows, signal, hold_probe)
            if value is None or held is None:
                break
            values[signal] = value
            hold_errors.append(abs(held - value))
        else:
            for signal in _POSITIVE_OUTPUTS:
                sampled[signal].append(values[signal])
            repeat_errors.append(
                max(
                    abs(values["vinp"] - values["vinp_seed_b"]),
                    abs(values["vinn"] - values["vinn_seed_b"]),
                )
            )
            alternate_seed_differences.append(
                abs(
                    (values["vinp"] - values["vinn"])
                    - (values["vinp_seed_alt"] - values["vinn_seed_alt"])
                )
            )
            expected_sigma_zero = common_mode + _AMPLITUDE * math.sin(
                2.0 * math.pi * _FREQUENCY_HZ * left
            )
            sigma_zero_errors.append(
                abs(values["vinp_sigma0"] - expected_sigma_zero)
            )
            noise_residuals.append(
                abs(values["vinp"] - values["vinp_sigma0"])
            )

    checked_windows = len(sampled["vinp"])
    if checked_windows < 15:
        return _failure(
            "P_INTEREDGE_HOLD",
            "insufficient_sample_hold_windows",
            expected="checked_windows>=15",
            observed=f"checked_windows={checked_windows}",
            event="clock_window_set",
        )

    max_hold_err = max(hold_errors, default=float("inf"))
    if max_hold_err > 0.004:
        return _failure(
            "P_INTEREDGE_HOLD",
            "interedge_hold_mismatch",
            expected="max_hold_error<=0.004",
            observed=f"max_hold_error={max_hold_err:.6g}",
            event="clock_window_set",
        )

    source_span = max(sampled["vinp"]) - min(sampled["vinp"])
    if source_span < 0.025:
        return _failure(
            "P_SAMPLED_SINE",
            "sampled_source_span_too_small",
            expected="source_span>=0.025",
            observed=f"source_span={source_span:.6g}",
            event="active_sample_set",
        )

    max_repeat_error = max(repeat_errors, default=float("inf"))
    if max_repeat_error > _SAME_SEED_TOLERANCE:
        return _failure(
            "P_SEEDED_REPEATABILITY",
            "same_seed_sequence_mismatch",
            expected=f"max_error<={_SAME_SEED_TOLERANCE:.6g}",
            observed=f"max_error={max_repeat_error:.6g}",
            event="same_seed_instances",
        )

    max_alternate_difference = max(alternate_seed_differences, default=0.0)
    if max_alternate_difference < _MIN_SEED_SEPARATION:
        return _failure(
            "P_SEEDED_REPEATABILITY",
            "alternate_seed_has_no_effect",
            expected=f"max_difference>={_MIN_SEED_SEPARATION:.6g}",
            observed=f"max_difference={max_alternate_difference:.6g}",
            event="alternate_seed_instance",
        )

    max_sigma_zero_error = max(sigma_zero_errors, default=float("inf"))
    if max_sigma_zero_error > _SIGMA_ZERO_TOLERANCE:
        return _failure(
            "P_SEEDED_REPEATABILITY",
            "sigma_zero_did_not_remove_perturbation",
            expected=f"max_sine_error<={_SIGMA_ZERO_TOLERANCE:.6g}",
            observed=f"max_sine_error={max_sigma_zero_error:.6g}",
            event="sigma_zero_instance",
        )

    max_noise_residual = max(noise_residuals, default=0.0)
    if max_noise_residual < _MIN_NOISE_RESIDUAL:
        return _failure(
            "P_SEEDED_REPEATABILITY",
            "nonzero_sigma_has_no_perturbation",
            expected=f"max_residual>={_MIN_NOISE_RESIDUAL:.6g}",
            observed=f"max_residual={max_noise_residual:.6g}",
            event="nonzero_sigma_instance",
        )

    vin_diff = [row["vinp"] - row["vinn"] for row in rows if row["rst_n"] >= vth]
    vamp_diff = [
        row["vamp_p"] - row["vamp_n"] for row in rows if row["rst_n"] >= vth
    ]
    mean_in = sum(vin_diff) / len(vin_diff)
    mean_out = sum(vamp_diff) / len(vamp_diff)
    std_in = (sum((value - mean_in) ** 2 for value in vin_diff) / len(vin_diff)) ** 0.5
    std_out = (
        sum((value - mean_out) ** 2 for value in vamp_diff) / len(vamp_diff)
    ) ** 0.5
    gain = std_out / std_in if std_in > 1e-12 else 0.0
    if gain <= 4.0:
        return _failure(
            "P_SAMPLED_SINE",
            "downstream_gain_too_small",
            expected="downstream_gain>4",
            observed=f"downstream_gain={gain:.6g}",
            event="composed_gain_flow",
        )

    detail = (
        f"active_edges={len(edges)} checked_windows={checked_windows} "
        f"reset_cm_err={reset_cm_err:.5f} reference_err={reference_err:.5f} "
        f"source_span={source_span:.5f} max_hold_err={max_hold_err:.5f} "
        f"same_seed_err={max_repeat_error:.6g} "
        f"alternate_seed_diff={max_alternate_difference:.6g} "
        f"sigma_zero_err={max_sigma_zero_error:.6g} "
        f"noise_residual={max_noise_residual:.6g} downstream_gain={gain:.2f}"
    )
    return True, pass_note(PROPERTY_IDS, detail)


CHECKER: Checker = check_v3_clocked_sine_source
