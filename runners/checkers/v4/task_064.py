"""Task-specific checker for canonical v4 DUT 064."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import (
    crossings,
    diagnostic,
    event_label,
    pass_note,
    probe_time,
    require_signals,
    sample,
)


PROPERTIES = (
    "P_RESET_DISABLE_CLEAR",
    "P_STABLE_EDGE_QUALIFICATION",
    "P_DELAYED_EDGE_EMISSION",
    "P_NARROW_GLITCH_REJECTION",
    "P_VALID_EMISSION_PULSE",
    "P_BIDIRECTIONAL_LEVELS",
    "P_PARAMETER_OVERRIDE",
)

def check_v4_edge_delay_line_with_deglitch(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin", "rst", "enable", "vout", "edge_valid", "rejected"}
    invalid = require_signals(rows, required, "P_RESET_DISABLE_CLEAR")
    if invalid:
        return False, invalid
    reset_rows = [row for row in rows if row["rst"] > 0.45]
    if reset_rows:
        reset_peak = max(max(row["vout"], row["edge_valid"], row["rejected"]) for row in reset_rows)
        if reset_peak > 0.16:
            return False, diagnostic(
                "P_RESET_DISABLE_CLEAR",
                "semantic_mismatch",
                expected="outputs<=0.16_during_reset",
                observed=f"max_output={reset_peak:.3f}",
                event="rst_high",
            )
    input_events = sorted(
        [(time_s, 1) for time_s in crossings(rows, "vin", threshold=0.45, direction="rising")]
        + [(time_s, -1) for time_s in crossings(rows, "vin", threshold=0.45, direction="falling")]
    )
    output_events = sorted(
        [(time_s, 1) for time_s in crossings(rows, "vout", threshold=0.45, direction="rising")]
        + [(time_s, -1) for time_s in crossings(rows, "vout", threshold=0.45, direction="falling")]
    )
    input_edges = [time_s for time_s, _ in input_events]
    output_edges = [time_s for time_s, _ in output_events]
    if len(input_edges) < 5:
        return False, diagnostic(
            "P_STABLE_EDGE_QUALIFICATION",
            "insufficient_coverage",
            expected="input_edges>=5",
            observed=f"input_edges={len(input_edges)}",
            event="full_trace",
        )
    if len(output_edges) < 2:
        return False, diagnostic(
            "P_DELAYED_EDGE_EMISSION",
            "insufficient_coverage",
            expected="output_edges>=2",
            observed=f"output_edges={len(output_edges)}",
            event="full_trace",
        )

    qualified_events: list[tuple[float, int]] = []
    narrow_events: list[tuple[float, float]] = []
    skip_as_narrow_reversal: set[int] = set()
    for index, (in_edge, direction) in enumerate(input_events):
        if index in skip_as_narrow_reversal:
            continue
        next_edge = input_events[index + 1][0] if index + 1 < len(input_events) else rows[-1]["time"]
        rst_at_edge = sample(rows, "rst", in_edge)
        enable_at_edge = sample(rows, "enable", in_edge)
        if rst_at_edge is None or enable_at_edge is None or rst_at_edge > 0.45 or enable_at_edge <= 0.45:
            continue
        if next_edge - in_edge < 0.75e-9:
            narrow_events.append((in_edge, next_edge))
            skip_as_narrow_reversal.add(index + 1)
            continue
        enable_at_emit = sample(rows, "enable", min(rows[-1]["time"], in_edge + 3.4e-9))
        rst_at_emit = sample(rows, "rst", min(rows[-1]["time"], in_edge + 3.4e-9))
        if enable_at_emit is not None and rst_at_emit is not None and enable_at_emit > 0.45 and rst_at_emit <= 0.45:
            qualified_events.append((in_edge, direction))

    matched_output_indices: set[int] = set()
    delays: list[float] = []
    valid_misses = 0
    for in_edge, direction in qualified_events:
        match = next(
            (
                (index, out_edge)
                for index, (out_edge, out_direction) in enumerate(output_events)
                if index not in matched_output_indices
                and out_direction == direction
                and 1.7e-9 <= out_edge - in_edge <= 3.4e-9
            ),
            None,
        )
        if match is None:
            continue
        output_index, out_edge = match
        matched_output_indices.add(output_index)
        delays.append(out_edge - in_edge)
        if not any(
            out_edge - 0.2e-9 <= row["time"] <= out_edge + 1.0e-9
            and row["edge_valid"] > 0.45
            for row in rows
        ):
            valid_misses += 1

    rejected_misses = sum(
        not any(
            reverse_edge - 0.2e-9 <= row["time"] <= reverse_edge + 1.5e-9
            and row["rejected"] > 0.45
            for row in rows
        )
        for _, reverse_edge in narrow_events
    )
    disabled_clears = False
    enable_falls = crossings(rows, "enable", threshold=0.45, direction="falling")
    enable_rises = crossings(rows, "enable", threshold=0.45, direction="rising")
    for disable_index, disable_t in enumerate(enable_falls, start=1):
        next_enable = next((rise for rise in enable_rises if rise > disable_t), None)
        clear_t = probe_time(rows, disable_t, next_enable, fraction=0.35)
        clear_vout = sample(rows, "vout", clear_t) if clear_t is not None else None
        if clear_vout is not None and clear_vout < 0.2:
            disabled_clears = True
            break
    min_delay = min(delays, default=0.0)
    max_delay = max(delays, default=0.0)
    ok = (
        len(qualified_events) >= 4
        and len(matched_output_indices) == len(qualified_events)
        and len(matched_output_indices) == len(output_events)
        and valid_misses == 0
        and len(narrow_events) >= 1
        and rejected_misses == 0
        and disabled_clears
        and 1.7e-9 <= min_delay <= 3.2e-9
        and max_delay <= 3.4e-9
    )
    summary = (
        f"input_edges={len(input_edges)} output_edges={len(output_edges)} "
        f"qualified={len(qualified_events)} matched={len(matched_output_indices)} "
        f"narrow={len(narrow_events)} rejected_misses={rejected_misses} "
        f"valid_misses={valid_misses} delay_range=({min_delay:.3e},{max_delay:.3e}) "
        f"disabled_clears={disabled_clears}"
    )
    if not ok:
        return False, diagnostic(
            "P_DELAYED_EDGE_EMISSION",
            "semantic_mismatch",
            expected="every_qualified_edge_matched_once,each_valid,narrow_rejected,disabled_clear",
            observed=summary.replace(" ", "_"),
            event="full_trace",
        )
    return True, pass_note(PROPERTIES, summary)

CHECKER_ID = "v4_064_edge_delay_line_with_deglitch"
CHECKER: Checker = check_v4_edge_delay_line_with_deglitch
