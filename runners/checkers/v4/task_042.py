"""Task-specific checker for canonical v4 DUT 042."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import crossings, diagnostic, pass_note, require_signals, sample


PROPERTY_IDS = (
    "P_SAMPLE_CAPTURE",
    "P_HOLD_BETWEEN_EVENTS",
    "P_PERIODIC_DROOP",
    "P_RESET_CLEAR",
    "P_SMOOTH_OUTPUT",
)

def check_release_vin_sampled_droop_hold(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "sample", "rst", "vin", "vout"}
    missing = require_signals(rows, required, "P_SAMPLE_CAPTURE")
    if missing:
        return False, missing

    all_sample_edges = crossings(rows, "sample", threshold=0.45, direction="rising")
    sample_edges = [
        edge_t
        for edge_t in all_sample_edges
        if (sample(rows, "rst", edge_t) or 0.0) < 0.45
        and (sample(rows, "rst", edge_t + 1.20e-9) or 0.0) < 0.45
    ]
    if len(sample_edges) < 3:
        return False, diagnostic(
            "P_SAMPLE_CAPTURE",
            "insufficient_excitation",
            expected="active_sample_edges>=3",
            observed=(
                f"active_sample_edges={len(sample_edges)},"
                f"all_sample_edges={len(all_sample_edges)}"
            ),
            event="sample.rising while rst.low",
        )

    expected: list[float] = []
    observed: list[float] = []
    errors: list[float] = []
    for edge_t in sample_edges[:3]:
        want = sample(rows, "vin", edge_t + 0.05e-9)
        got = sample(rows, "vout", edge_t + 1.20e-9)
        if want is None or got is None:
            return False, diagnostic(
                "P_SAMPLE_CAPTURE",
                "invalid_trace",
                expected="vin/vout observable after sample edge",
                observed="missing_interpolated_sample",
                event=f"sample_edge@{edge_t:.6e}s",
            )
        expected.append(want)
        observed.append(got)
        errors.append(abs(got - want))

    max_err = max(errors)
    expected_span = max(expected) - min(expected)
    observed_span = max(observed) - min(observed)
    sample_match = max_err <= 0.045 and expected_span >= 0.35 and observed_span >= 0.30

    reset_edges = crossings(rows, "rst", threshold=0.45, direction="rising")
    hold_windows: list[tuple[float, float]] = []
    for edge_t in sample_edges:
        boundaries = [
            boundary
            for boundary in (*sample_edges, *reset_edges, rows[-1]["time"])
            if boundary > edge_t
        ]
        if boundaries:
            hold_windows.append((edge_t, min(boundaries)))
    hold_edge, hold_end = max(hold_windows, key=lambda window: window[1] - window[0])
    droop_start_t = hold_edge + 2.0e-9
    droop_end_t = hold_end - 2.0e-9
    droop_values = [r["vout"] for r in rows if droop_start_t <= r["time"] <= droop_end_t]
    if len(droop_values) < 8:
        return False, diagnostic(
            "P_PERIODIC_DROOP",
            "insufficient_excitation",
            expected="droop_samples>=8",
            observed=f"droop_samples={len(droop_values)}",
            event="longest_active_hold_window",
        )
    droop = droop_values[0] - droop_values[-1]
    upward_steps = sum(1 for a, b in zip(droop_values[:-1], droop_values[1:]) if b - a > 0.004)
    droop_ok = 0.04 <= droop <= 0.45 and upward_steps <= max(1, len(droop_values) // 10)

    reset_t = reset_edges[0] if reset_edges else 125.0e-9
    reset_sample = sample(rows, "vout", reset_t + 8.0e-9)
    reset_clear = reset_sample is not None and reset_sample < 0.05

    ok = sample_match and droop_ok and reset_clear
    exp_text = ",".join(f"{value:.3f}" for value in expected)
    obs_text = ",".join(f"{value:.3f}" for value in observed)
    note = (
        f"vin_samples={exp_text} held_samples={obs_text} "
        f"max_sample_err={max_err:.3f} expected_span={expected_span:.3f} "
        f"observed_span={observed_span:.3f} droop={droop:.3f} "
        f"upward_steps={upward_steps} reset_clear={reset_clear}"
    )
    if not sample_match:
        return False, diagnostic(
            "P_SAMPLE_CAPTURE",
            "behavior_mismatch",
            expected="max_sample_err<=0.045,spans_exercised",
            observed=f"max_sample_err={max_err:.3f},expected_span={expected_span:.3f},observed_span={observed_span:.3f}",
            event="sample.rising",
        )
    if not droop_ok:
        return False, diagnostic(
            "P_PERIODIC_DROOP",
            "behavior_mismatch",
            expected="0.04<=droop<=0.45 and limited upward steps",
            observed=f"droop={droop:.3f},upward_steps={upward_steps}",
            event="post_second_sample_hold",
        )
    if not reset_clear:
        observed = "missing" if reset_sample is None else f"{reset_sample:.3f}"
        return False, diagnostic(
            "P_RESET_CLEAR",
            "behavior_mismatch",
            expected="vout<0.05 after reset",
            observed=f"vout={observed}",
            event=f"reset_edge@{reset_t:.6e}s",
        )
    return ok, pass_note(PROPERTY_IDS, note)

CHECKER_ID = "v4_042_sample_and_hold_with_droop_leakage"


def check(rows: list[dict[str, float]]) -> tuple[bool, str]:
    passed, note = check_release_vin_sampled_droop_hold(rows)
    return passed, f"{note} properties_checked={','.join(PROPERTY_IDS)}"


CHECKER: Checker = check
