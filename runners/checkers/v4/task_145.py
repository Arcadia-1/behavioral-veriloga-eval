"""Task-specific checker for canonical v4 DUT 145."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import crossings, probe_time, require_signals, sample


def check_v3_divide_by_eight_clock(rows: list[dict[str, float]]) -> tuple[bool, str]:
    invalid = require_signals(rows, {"time", "vin", "rst", "en", "vout"}, "P_DIVIDE_BY_EIGHT")
    if invalid:
        return False, invalid
    edges = crossings(rows, "vin", threshold=0.45, direction="rising")
    if len(edges) < 6:
        return False, f"insufficient_excitation vin_rising_edges={len(edges)}"

    count = 0
    output_high = True
    mismatches = 0
    saw_reset_high = saw_reset_low = saw_enable_high = saw_enable_low = False
    for index, edge in enumerate(edges):
        rst = sample(rows, "rst", edge)
        enable = sample(rows, "en", edge)
        if rst is None or enable is None:
            return False, f"missing_control_sample edge={index}"
        reset_high = rst > 0.45
        enable_high = enable > 0.45
        saw_reset_high |= reset_high
        saw_reset_low |= not reset_high
        saw_enable_high |= enable_high
        saw_enable_low |= not enable_high
        if reset_high:
            count = 0
            output_high = True
        elif enable_high:
            count = (count + 1) % 8
            output_high = count < 4

        next_edge = edges[index + 1] if index + 1 < len(edges) else None
        probe = probe_time(rows, edge, next_edge, fraction=0.25)
        observed = sample(rows, "vout", probe) if probe is not None else None
        expected = 0.9 if output_high else 0.0
        if observed is None or abs(observed - expected) > 0.08:
            mismatches += 1

    coverage = saw_reset_high and saw_reset_low and saw_enable_high and saw_enable_low
    if not coverage:
        return False, (
            "insufficient_excitation "
            f"reset_high={saw_reset_high} reset_low={saw_reset_low} "
            f"enable_high={saw_enable_high} enable_low={saw_enable_low}"
        )
    return mismatches == 0, f"vin_rising_edges={len(edges)} mismatch_count={mismatches}"


CHECKER_ID = "v4_145_divide_by_eight_clock"
CHECKER: Checker = check_v3_divide_by_eight_clock
