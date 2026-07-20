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
    input_edges = sorted(
        crossings(rows, "vin", threshold=0.45, direction="rising")
        + crossings(rows, "vin", threshold=0.45, direction="falling")
    )
    output_edges = sorted(
        crossings(rows, "vout", threshold=0.45, direction="rising")
        + crossings(rows, "vout", threshold=0.45, direction="falling")
    )
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

    wide_matches = 0
    early_errors = 0
    delays: list[float] = []
    for edge_index, in_edge in enumerate(input_edges, start=1):
        rst_at_edge = sample(rows, "rst", in_edge)
        enable_at_edge = sample(rows, "enable", in_edge)
        if rst_at_edge is None or enable_at_edge is None or rst_at_edge > 0.45 or enable_at_edge <= 0.45:
            continue
        before = sample(rows, "vout", max(rows[0]["time"], in_edge + 0.45e-9))
        if before is None:
            continue
        in_after = sample(rows, "vin", min(rows[-1]["time"], in_edge + 0.70e-9))
        if in_after is None:
            continue
        stable_after = sample(rows, "vin", min(rows[-1]["time"], in_edge + 1.40e-9))
        if stable_after is None:
            continue
        is_wide = (in_after > 0.45) == (stable_after > 0.45)
        later_edges = [out_edge for out_edge in output_edges if 0.8e-9 <= out_edge - in_edge <= 3.2e-9]
        if is_wide and later_edges:
            wide_matches += 1
            delays.append(later_edges[0] - in_edge)
        if later_edges and abs(before - (0.9 if in_after > 0.45 else 0.0)) < 0.12 and later_edges[0] - in_edge < 0.8e-9:
            early_errors += 1

    rejected_seen = any(row["rejected"] > 0.45 for row in rows)
    valid_seen = any(row["edge_valid"] > 0.45 for row in rows)
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
        wide_matches >= 2
        and early_errors == 0
        and rejected_seen
        and valid_seen
        and disabled_clears
        and 1.7e-9 <= min_delay <= 3.2e-9
        and max_delay <= 3.4e-9
    )
    summary = (
        f"input_edges={len(input_edges)} output_edges={len(output_edges)} "
        f"wide_matches={wide_matches} delay_range=({min_delay:.3e},{max_delay:.3e}) "
        f"rejected={rejected_seen} valid={valid_seen} disabled_clears={disabled_clears} early_errors={early_errors}"
    )
    if not ok:
        return False, diagnostic(
            "P_DELAYED_EDGE_EMISSION",
            "semantic_mismatch",
            expected="wide_matches>=2,delay=1.7..3.4ns,rejected_valid_disabled_clear,no_early",
            observed=summary.replace(" ", "_"),
            event="full_trace",
        )
    return True, pass_note(PROPERTIES, summary)

CHECKER_ID = "v4_064_edge_delay_line_with_deglitch"
CHECKER: Checker = check_v4_edge_delay_line_with_deglitch
