"""Stimulus-relative checker for canonical V4 DUT 037."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import close, crossings, diagnostic, event_label, pass_note, percentile, probe_time, require_signals, sample


PROPERTY_IDS = (
    "P_FULL_WAVE_RECTIFICATION",
    "P_RESET_ENVELOPE",
    "P_PEAK_ATTACK",
    "P_BOUNDED_DECAY",
    "P_ENVELOPE_LAG_METRIC",
)


def _rect(vin: float) -> float:
    return min(0.9, 0.45 + abs(vin - 0.45))


def check_precision_rectifier_envelope_detector(rows: list[dict[str, float]]) -> tuple[bool, str]:
    error = require_signals(
        rows, {"time", "clk", "rst", "vin", "rect", "env", "metric"}, "P_FULL_WAVE_RECTIFICATION"
    )
    if error:
        return False, error

    edges = crossings(rows, "clk", threshold=0.45, direction="rising")
    if len(edges) < 6:
        return False, diagnostic(
            "P_PEAK_ATTACK", "insufficient_excitation", expected="clk_rise_count>=6",
            observed=f"clk_rise_count={len(edges)}", event="full_trace",
        )

    rect_errors = [abs(row["rect"] - _rect(row["vin"])) for row in rows]
    rect_p90 = percentile(rect_errors, 0.90)
    if rect_p90 > 0.055:
        return False, diagnostic(
            "P_FULL_WAVE_RECTIFICATION", "behavior_mismatch", expected="rect=0.45+abs(vin-0.45),clipped",
            observed=f"rect_error_p90:{rect_p90:.4f}", event="full_trace",
        )

    env_state = 0.45
    reset_seen = False
    attack_count = 0
    decay_count = 0
    lag_high_seen = False
    checked = 0
    for index, edge in enumerate(edges):
        next_edge = edges[index + 1] if index + 1 < len(edges) else None
        probe = probe_time(rows, edge, next_edge)
        if probe is None:
            continue
        rst, vin_at_edge = sample(rows, "rst", edge), sample(rows, "vin", edge)
        if rst is None or vin_at_edge is None:
            continue
        rect_at_edge = _rect(vin_at_edge)
        previous_env = env_state
        if rst > 0.45:
            env_state = 0.45
            property_id = "P_RESET_ENVELOPE"
            reset_seen = True
        elif rect_at_edge > env_state:
            env_state = rect_at_edge
            property_id = "P_PEAK_ATTACK"
            attack_count += 1
        else:
            env_state = max(0.45, rect_at_edge, env_state - 0.018)
            property_id = "P_BOUNDED_DECAY"
            if env_state < previous_env - 0.005:
                decay_count += 1
        vin_probe = sample(rows, "vin", probe)
        env, metric = sample(rows, "env", probe), sample(rows, "metric", probe)
        if None in (vin_probe, env, metric):
            continue
        assert vin_probe is not None and env is not None and metric is not None
        rect_probe = _rect(vin_probe)
        expected_metric = 0.9 if env_state - rect_probe > 0.030 else 0.0
        lag_high_seen |= expected_metric > 0.5
        checked += 1
        label = event_label("clk_rise", index, edge)
        if not close(env, env_state, 0.055):
            return False, diagnostic(
                property_id, "behavior_mismatch", expected=f"env:{env_state:.4f}",
                observed=f"env:{env:.4f},rect_edge:{rect_at_edge:.4f}", event=label,
            )
        if not close(metric, expected_metric, 0.12):
            return False, diagnostic(
                "P_ENVELOPE_LAG_METRIC", "behavior_mismatch", expected=f"metric:{expected_metric:.1f}",
                observed=f"metric:{metric:.3f},env:{env:.3f},rect:{rect_probe:.3f}", event=label,
            )
    polarities = {
        "positive" if row["vin"] > 0.47 else "negative"
        for row in rows
        if row["vin"] > 0.47 or row["vin"] < 0.43
    }
    missing = []
    if not reset_seen:
        missing.append("reset")
    if attack_count == 0:
        missing.append("peak_attack")
    if decay_count == 0:
        missing.append("bounded_decay")
    if not lag_high_seen:
        missing.append("lag_metric_high")
    if polarities != {"positive", "negative"}:
        missing.append("both_rectifier_polarities")
    if missing:
        return False, diagnostic(
            "P_FULL_WAVE_RECTIFICATION", "insufficient_excitation",
            expected="reset,both_polarities,attack,decay,lag", observed="missing:" + ",".join(missing),
            event="full_trace",
        )
    return True, pass_note(
        PROPERTY_IDS,
        f"rectifier edge_checks={checked} attack={attack_count} decay={decay_count} rect_p90={rect_p90:.4f}",
    )


CHECKER_ID = "v4_037_precision_rectifier_envelope_detector"
CHECKER: Checker = check_precision_rectifier_envelope_detector
