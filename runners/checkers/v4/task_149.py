"""Task-specific checker for canonical v4 DUT 149."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import crossings, probe_time, require_signals, sample


def check_v3_dual_modulus_divider_16_17(rows: list[dict[str, float]]) -> tuple[bool, str]:
    invalid = require_signals(rows, {"time", "fin", "mc", "fout"}, "P_MC_SELECTS_MODULUS")
    if invalid:
        return False, invalid
    edges = crossings(rows, "fin", threshold=0.5, direction="rising")
    if len(edges) < 34:
        return False, f"insufficient_excitation fin_rising_edges={len(edges)}"

    count = 0
    output_high = False
    mismatches = 0
    saw_mod16 = saw_mod17 = False
    for index, edge in enumerate(edges):
        mc = sample(rows, "mc", edge)
        if mc is None:
            return False, f"missing_mc_sample edge={index}"
        mod17 = mc > 0.5
        saw_mod17 |= mod17
        saw_mod16 |= not mod17
        if count == 15:
            if mod17:
                count = 16
            else:
                count = 0
                output_high = True
        elif count == 16:
            count = 0
            output_high = True
        elif count == 8:
            count += 1
            output_high = False
        else:
            count += 1

        next_edge = edges[index + 1] if index + 1 < len(edges) else None
        probe = probe_time(rows, edge, next_edge, fraction=0.25)
        observed = sample(rows, "fout", probe) if probe is not None else None
        expected = 1.0 if output_high else 0.0
        if observed is None or abs(observed - expected) > 0.08:
            mismatches += 1

    if not (saw_mod16 and saw_mod17):
        return False, f"insufficient_excitation mod16={saw_mod16} mod17={saw_mod17}"
    return mismatches == 0, f"fin_rising_edges={len(edges)} mismatch_count={mismatches}"


CHECKER_ID = "v4_149_dual_modulus_divider_16_17"
CHECKER: Checker = check_v3_dual_modulus_divider_16_17
