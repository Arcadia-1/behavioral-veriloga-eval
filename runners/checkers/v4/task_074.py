"""Behavioral checker for v4 task 074 sampled true-RMS-to-DC converter."""
from __future__ import annotations

import math

from ..api import Checker
from .stimulus_relative import crossings, diagnostic, pass_note, require_signals, sample


PROPERTY_IDS = (
    "P_DIFFERENTIAL_RMS",
    "P_FOUR_SAMPLE_WINDOW",
    "P_ENABLE_FREEZE",
    "P_ASYNC_RESET",
    "P_VALID_PULSE",
    "P_OUTPUT_HOLD",
)

WINDOW_SIZE = 4
LOGIC_THRESHOLD = 0.45
LOGIC_HIGH = 0.9


def _probe_after_edge(
    rows: list[dict[str, float]], edge: float, next_edge: float | None
) -> float | None:
    stop = rows[-1]["time"] if next_edge is None else next_edge
    interval = stop - edge
    if interval <= 0.3e-9:
        return None
    return edge + min(0.4e-9, 0.2 * interval)


def check_sampled_true_rms_to_dc(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {
        "time",
        "vinp",
        "vinn",
        "clk",
        "reset",
        "enable",
        "rms_out",
        "valid",
    }
    missing = require_signals(rows, required, "P_DIFFERENTIAL_RMS")
    if missing:
        return False, missing

    initial_error = max(abs(rows[0]["rms_out"]), abs(rows[0]["valid"]))
    if initial_error > 0.06:
        return False, diagnostic(
            "P_ASYNC_RESET",
            "initial_state_mismatch",
            expected="rms_out=0,valid=0",
            observed=f"initial_error={initial_error:.4f}",
            event="initial_step",
        )

    clk_edges = crossings(rows, "clk", threshold=LOGIC_THRESHOLD, direction="rising")
    reset_edges = crossings(rows, "reset", threshold=LOGIC_THRESHOLD, direction="rising")
    if len(clk_edges) < 12:
        return False, diagnostic(
            "P_FOUR_SAMPLE_WINDOW",
            "insufficient_events",
            expected="clk_rising_count>=12",
            observed=f"clk_rising_count={len(clk_edges)}",
            event="clk_rising_set",
        )

    square_sum = 0.0
    sample_count = 0
    expected_rms = 0.0
    expected_valid = False
    reset_index = 0
    previous_clk = rows[0]["time"]
    accepted_values: list[float] = []
    completed_windows = 0
    disabled_edges = 0
    checked_edges = 0
    hold_checks = 0
    max_rms_error = 0.0

    for index, edge in enumerate(clk_edges):
        while reset_index < len(reset_edges) and reset_edges[reset_index] <= edge:
            if reset_edges[reset_index] > previous_clk:
                square_sum = 0.0
                sample_count = 0
                expected_rms = 0.0
                expected_valid = False
            reset_index += 1

        reset = sample(rows, "reset", edge)
        enable = sample(rows, "enable", edge)
        vinp = sample(rows, "vinp", edge)
        vinn = sample(rows, "vinn", edge)
        if None in (reset, enable, vinp, vinn):
            return False, diagnostic(
                "P_DIFFERENTIAL_RMS",
                "missing_sample",
                expected="reset,enable,vinp,vinn_at_clk_edge",
                observed="unavailable",
                event=f"clk_rising[{index}]",
            )
        assert reset is not None and enable is not None and vinp is not None and vinn is not None

        if reset > LOGIC_THRESHOLD:
            square_sum = 0.0
            sample_count = 0
            expected_rms = 0.0
            expected_valid = False
        else:
            expected_valid = False
            if enable > LOGIC_THRESHOLD:
                differential = vinp - vinn
                accepted_values.append(differential)
                square_sum += differential * differential
                sample_count += 1
                if sample_count == WINDOW_SIZE:
                    expected_rms = math.sqrt(square_sum / WINDOW_SIZE)
                    expected_valid = True
                    square_sum = 0.0
                    sample_count = 0
                    completed_windows += 1
            else:
                disabled_edges += 1

        next_edge = clk_edges[index + 1] if index + 1 < len(clk_edges) else None
        probe = _probe_after_edge(rows, edge, next_edge)
        if probe is None:
            previous_clk = edge
            continue
        observed_rms = sample(rows, "rms_out", probe)
        observed_valid = sample(rows, "valid", probe)
        if observed_rms is None or observed_valid is None:
            return False, diagnostic(
                "P_OUTPUT_HOLD",
                "missing_sample",
                expected="rms_out,valid_after_clk_edge",
                observed="unavailable",
                event=f"clk_rising[{index}]",
            )
        rms_error = abs(observed_rms - expected_rms)
        valid_target = LOGIC_HIGH if expected_valid else 0.0
        valid_error = abs(observed_valid - valid_target)
        max_rms_error = max(max_rms_error, rms_error)
        checked_edges += 1
        if rms_error > 0.012:
            return False, diagnostic(
                "P_DIFFERENTIAL_RMS",
                "rms_mismatch",
                expected=f"rms_out={expected_rms:.5f}",
                observed=f"rms_out={observed_rms:.5f},err={rms_error:.5f}",
                event=f"clk_rising[{index}]",
            )
        if valid_error > 0.08:
            return False, diagnostic(
                "P_VALID_PULSE",
                "valid_mismatch",
                expected=f"valid={valid_target:.3f}",
                observed=f"valid={observed_valid:.3f},err={valid_error:.3f}",
                event=f"clk_rising[{index}]",
            )

        if next_edge is not None:
            hold_probe = edge + 0.75 * (next_edge - edge)
            held_rms = sample(rows, "rms_out", hold_probe)
            held_valid = sample(rows, "valid", hold_probe)
            if held_rms is None or held_valid is None:
                return False, diagnostic(
                    "P_OUTPUT_HOLD",
                    "missing_sample",
                    expected="interedge_output_samples",
                    observed="unavailable",
                    event=f"clk_interval[{index}]",
                )
            reset_during_hold = any(edge < reset_edge <= hold_probe for reset_edge in reset_edges)
            hold_rms_target = 0.0 if reset_during_hold else expected_rms
            hold_valid_target = 0.0 if reset_during_hold else valid_target
            hold_checks += 1
            if abs(held_rms - hold_rms_target) > 0.012 or abs(held_valid - hold_valid_target) > 0.08:
                return False, diagnostic(
                    "P_OUTPUT_HOLD",
                    "interedge_change",
                    expected=f"rms_out={hold_rms_target:.5f},valid={hold_valid_target:.3f}",
                    observed=f"rms_out={held_rms:.5f},valid={held_valid:.3f}",
                    event=f"clk_interval[{index}]",
                )
        previous_clk = edge

    reset_checks = 0
    for index, edge in enumerate(reset_edges):
        probe = edge + 0.4e-9
        if probe >= rows[-1]["time"]:
            continue
        rms_after_reset = sample(rows, "rms_out", probe)
        valid_after_reset = sample(rows, "valid", probe)
        if rms_after_reset is None or valid_after_reset is None:
            continue
        reset_checks += 1
        if abs(rms_after_reset) > 0.012 or abs(valid_after_reset) > 0.08:
            return False, diagnostic(
                "P_ASYNC_RESET",
                "reset_clear_mismatch",
                expected="rms_out=0,valid=0_after_async_reset",
                observed=f"rms_out={rms_after_reset:.5f},valid={valid_after_reset:.3f}",
                event=f"reset_rising[{index}]",
            )

    if completed_windows < 2 or disabled_edges < 1 or reset_checks < 1:
        return False, diagnostic(
            "P_FOUR_SAMPLE_WINDOW",
            "insufficient_contract_coverage",
            expected="completed_windows>=2,disabled_edges>=1,async_resets>=1",
            observed=(
                f"completed_windows={completed_windows},disabled_edges={disabled_edges},"
                f"async_resets={reset_checks}"
            ),
            event="full_trace",
        )
    if not any(value > 0.02 for value in accepted_values) or not any(
        value < -0.02 for value in accepted_values
    ):
        return False, diagnostic(
            "P_DIFFERENTIAL_RMS",
            "insufficient_input_coverage",
            expected="accepted_positive_and_negative_differential_samples",
            observed=f"sample_range={min(accepted_values):.4f}:{max(accepted_values):.4f}",
            event="accepted_sample_set",
        )

    return True, pass_note(
        PROPERTY_IDS,
        f"checked_edges={checked_edges} completed_windows={completed_windows} "
        f"disabled_edges={disabled_edges} async_resets={reset_checks} "
        f"hold_checks={hold_checks} max_rms_error={max_rms_error:.5f}",
    )


CHECKER_ID = "v4_074_sampled_true_rms_to_dc_converter"
CHECKER: Checker = check_sampled_true_rms_to_dc
