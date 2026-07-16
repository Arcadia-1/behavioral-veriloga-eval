"""Task-specific checker for canonical v4 DUT 119."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import crossings, diagnostic, pass_note, probe_time, require_signals, sample


PROPERTY_IDS = (
    "P_INPUT_SAMPLE",
    "P_S6_HALF_ADD",
    "P_BINARY_SUBTRACTIONS",
    "P_EDGE_POLARITY",
    "P_ACCUMULATED_STATE",
    "P_OUTPUT_TRANSITION",
)


def check_v3_sar_cdac_residue(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin", "clk", "s6", "s5", "s4", "s3", "s2", "s1", "vres"}
    missing = require_signals(rows, required, "P_ACCUMULATED_STATE")
    if missing:
        return False, missing

    events: list[tuple[float, str, float]] = [(rows[0]["time"], "sample", 0.0)]
    for edge in crossings(rows, "clk", threshold=0.45, direction="rising"):
        events.append((edge, "sample", 0.0))
    events.extend((edge, "step", 0.5 * 0.9) for edge in crossings(rows, "s6", threshold=0.45, direction="falling"))
    for signal, weight in (("s5", -0.25), ("s4", -0.125), ("s3", -0.0625), ("s2", -0.03125), ("s1", -0.015625)):
        events.extend((edge, "step", weight * 0.9) for edge in crossings(rows, signal, threshold=0.45, direction="rising"))
    events.sort(key=lambda item: item[0])
    if len(events) < 7:
        return False, diagnostic(
            "P_EDGE_POLARITY",
            "insufficient_events",
            expected="events>=7",
            observed=f"events={len(events)}",
            event="cdac_event_set",
        )

    state = rows[0]["vin"]
    checked = 0
    max_err = 0.0
    observed_values: list[float] = []
    for index, (event_time, kind, delta) in enumerate(events):
        if kind == "sample":
            vin_value = sample(rows, "vin", event_time)
            if vin_value is None:
                return False, diagnostic(
                    "P_INPUT_SAMPLE",
                    "missing_sample",
                    expected="vin",
                    observed="unavailable",
                    event=f"cdac_event[{index}]",
                )
            state = vin_value
        else:
            state += delta
        next_event_time = events[index + 1][0] if index + 1 < len(events) else None
        sample_t = probe_time(rows, event_time, next_event_time, fraction=0.25)
        if sample_t is None:
            continue
        observed = sample(rows, "vres", sample_t)
        if observed is None:
            return False, diagnostic(
                "P_OUTPUT_TRANSITION",
                "missing_sample",
                expected="vres",
                observed="unavailable",
                event=f"cdac_event[{index}]",
            )
        observed_values.append(observed)
        err = abs(observed - state)
        max_err = max(max_err, err)
        checked += 1
        if err > 0.010:
            property_id = "P_INPUT_SAMPLE" if kind == "sample" else "P_ACCUMULATED_STATE"
            return False, diagnostic(
                property_id,
                "residue_state_mismatch",
                expected=f"vres={state:.5f}",
                observed=f"vres={observed:.5f},err={err:.5f}",
                event=f"cdac_event[{index}]",
            )
    if checked < 7:
        return False, diagnostic(
            "P_ACCUMULATED_STATE",
            "insufficient_checks",
            expected="checked>=7",
            observed=f"checked={checked}",
            event="cdac_event_set",
        )
    has_up_step = any(b > a + 0.30 for a, b in zip(observed_values, observed_values[1:]))
    has_down_steps = sum(1 for a, b in zip(observed_values, observed_values[1:]) if b < a - 0.01) >= 4
    if not has_up_step or not has_down_steps:
        return False, diagnostic(
            "P_BINARY_SUBTRACTIONS",
            "sequence_coverage_mismatch",
            expected="one_up_step_and_four_down_steps",
            observed=f"up_step={has_up_step},down_step_count={sum(1 for a, b in zip(observed_values, observed_values[1:]) if b < a - 0.01)}",
            event="cdac_event_set",
        )
    return True, pass_note(PROPERTY_IDS, f"checked={checked} max_error={max_err:.5f}")

CHECKER_ID = "v4_119_sar_cdac_residue"
CHECKER: Checker = check_v3_sar_cdac_residue
