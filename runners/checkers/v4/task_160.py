"""Task-specific checker for canonical v4 DUT 160."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import normalize_affine_time
from .trace_utils import sample_signal, threshold_crossings

def check_v3_divide_by_8_9_switch(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clkin", "mc", "out"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing divide-by-8/9 signals"
    rows = normalize_affine_time(rows, [
        ("clkin", 0.6, "rising", 1.025, 0),
        ("clkin", 0.6, "rising", 3.025, 1),
    ])
    if rows is None:
        return False, "missing_clock_stimulus_edges"
    edges = threshold_crossings(rows, "clkin", threshold=0.6, direction=1)
    if len(edges) < 8:
        return False, f"insufficient_clock_edges={len(edges)} expected>=8"

    pre_edge_time = rows[0]["time"] + 0.5 * (edges[0] - rows[0]["time"])
    pre_edge_out = sample_signal(rows, "out", pre_edge_time)
    if pre_edge_out is None:
        return False, "missing_initial_out_sample"
    if abs(pre_edge_out) > 0.08:
        return False, (
            f"first_mismatch=P_DIVIDER_DUTY_WINDOW signal=out time={pre_edge_time:.6e} "
            f"expected=0 observed={pre_edge_out:.6g} tolerance=0.08"
        )

    samples: list[tuple[int, float, float, int]] = []
    for index, edge in enumerate(edges):
        next_edge = edges[index + 1] if index + 1 < len(edges) else rows[-1]["time"]
        if next_edge <= edge:
            continue
        sample_time = edge + 0.25 * (next_edge - edge)
        observed = sample_signal(rows, "out", sample_time)
        mc = sample_signal(rows, "mc", edge)
        if observed is None or mc is None:
            return False, f"missing_edge_sample_at={sample_time:.6e}"
        samples.append((index + 1, sample_time, observed, 9 if mc > 0.6 else 8))

    phase_failures: dict[int, list[tuple[int, float, float, float]]] = {}
    for first_count in range(4):
        count = first_count
        failures: list[tuple[int, float, float, float]] = []
        for sample_index, (edge_index, sample_time, observed, modulus) in enumerate(samples):
            if sample_index:
                count = (count + 1) % modulus
            expected = 1.2 if count < 4 else 0.0
            if abs(observed - expected) > 0.08:
                failures.append((edge_index, sample_time, expected, observed))
        if not failures:
            return True, (
                f"checked={len(samples)} initial_high_window_count={first_count} "
                "modulus_sequence=stimulus_relative"
            )
        phase_failures[first_count] = failures

    best_phase, best_failures = min(
        phase_failures.items(), key=lambda item: (len(item[1]), item[0])
    )
    edge_index, sample_time, expected, observed = best_failures[0]
    return False, (
        "first_mismatch=P_MODULUS_SWITCHING_ON_MC_EDGES signal=out "
        f"event=clkin_rise[{edge_index}] time={sample_time:.6e} "
        f"expected={expected:.6g} observed={observed:.6g} tolerance=0.08 "
        f"best_initial_high_window_count={best_phase} "
        f"mismatch_count={len(best_failures)}"
    )

CHECKER_ID = "v4_160_divide_by_8_9_switch"
CHECKER: Checker = check_v3_divide_by_8_9_switch
