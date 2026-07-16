"""Task-specific checker for canonical v4 DUT 150."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import crossings, probe_time, require_signals, sample


def check_v3_cyclic_decoder_12bit(rows: list[dict[str, float]]) -> tuple[bool, str]:
    bit_names = [f"d{index}" for index in range(12)]
    invalid = require_signals(rows, {"time", "clks", "dout", *bit_names}, "P_UNSIGNED_DECODE")
    if invalid:
        return False, invalid
    edges = crossings(rows, "clks", threshold=0.55, direction="rising")
    if len(edges) < 3:
        return False, f"insufficient_excitation clock_rising_edges={len(edges)}"

    mismatches = 0
    codes: set[int] = set()
    for index, edge in enumerate(edges):
        values = [sample(rows, name, edge) for name in bit_names]
        if any(value is None for value in values):
            return False, f"missing_input_sample edge={index}"
        code = sum(1 << bit for bit, value in enumerate(values) if value is not None and value > 0.55)
        codes.add(code)
        expected = code / 4095.0 - 0.5
        next_edge = edges[index + 1] if index + 1 < len(edges) else None
        probe = probe_time(rows, edge, next_edge, fraction=0.25)
        observed = sample(rows, "dout", probe) if probe is not None else None
        if observed is None or abs(observed - expected) > 0.02:
            mismatches += 1

    if len(codes) < 3:
        return False, f"insufficient_excitation distinct_input_codes={len(codes)}"
    return mismatches == 0, (
        f"clock_rising_edges={len(edges)} distinct_input_codes={len(codes)} "
        f"mismatch_count={mismatches}"
    )


CHECKER_ID = "v4_150_cyclic_decoder_12bit"
CHECKER: Checker = check_v3_cyclic_decoder_12bit
