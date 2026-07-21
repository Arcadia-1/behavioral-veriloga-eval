"""Task-specific checker for canonical v4 DUT 066."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import crossings, diagnostic, event_label, pass_note, require_signals, sample


PROPERTIES = (
    "P_RISING_SELECTION",
    "P_FALLING_SELECTION",
    "P_OPPOSITE_EDGE_REJECTION",
    "P_BOUNDED_PULSE",
    "P_OUTPUT_LEVELS",
)


def check_configurable_polarity_edge_detector(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "sig", "rise_en", "pulse"}
    invalid = require_signals(rows, required, "P_RISING_SELECTION")
    if invalid:
        return False, invalid
    edge_times: list[float] = []
    signal_edges = sorted(
        (edge_t, "rising") for edge_t in crossings(rows, "sig", threshold=0.45, direction="rising")
    ) + sorted(
        (edge_t, "falling") for edge_t in crossings(rows, "sig", threshold=0.45, direction="falling")
    )
    for edge_t, direction in sorted(signal_edges):
        rise_en = sample(rows, "rise_en", edge_t)
        if rise_en is None:
            continue
        if (direction == "rising" and rise_en > 0.45) or (direction == "falling" and rise_en <= 0.45):
            edge_times.append(edge_t)
    missed = 0
    level_errors = 0
    failures: list[str] = []
    for edge_index, edge_t in enumerate(edge_times, start=1):
        pulse_rows = [row for row in rows if edge_t <= row["time"] <= edge_t + 3e-9]
        peak = max((row["pulse"] for row in pulse_rows), default=0.0)
        if peak < 0.75:
            missed += 1
            failures.append(
                diagnostic(
                    "P_OUTPUT_LEVELS" if peak > 0.45 else "P_BOUNDED_PULSE",
                    "semantic_mismatch",
                    expected="pulse_peak_in_[0.75,1.05]V_after_selected_edge",
                    observed=f"pulse_peak={peak:.3f}",
                    event=event_label("selected_sig_edge", edge_index, edge_t),
                )
            )
        level_errors += sum(row["pulse"] > 1.05 or row["pulse"] < -0.15 for row in pulse_rows)
    false_pulses = 0
    for row in rows:
        if row["pulse"] <= 0.45:
            continue
        if not any(edge_t <= row["time"] <= edge_t + 4e-9 for edge_t in edge_times):
            false_pulses += 1
    if false_pulses:
        failures.append(
            diagnostic(
                "P_OPPOSITE_EDGE_REJECTION",
                "semantic_mismatch",
                expected="no_pulse_without_selected_edge",
                observed=f"false_pulses={false_pulses}",
                event="full_trace",
            )
        )
    if failures:
        return False, " ".join(failures[:5])
    summary = (
        f"events={len(edge_times)} missed={missed} "
        f"false_pulses={false_pulses} level_errors={level_errors}"
    )
    ok = len(edge_times) >= 3 and missed == 0 and false_pulses == 0 and level_errors == 0
    if not ok:
        return False, diagnostic(
            "P_RISING_SELECTION",
            "insufficient_coverage",
            expected="selected_edges>=3,no_misses,no_false_pulses",
            observed=summary.replace(" ", "_"),
            event="full_trace",
        )
    return True, pass_note(PROPERTIES, summary)

CHECKER_ID = "v4_066_configurable_polarity_edge_detector"
CHECKER: Checker = check_configurable_polarity_edge_detector
