"""Task-specific checker for canonical v4 DUT 200."""
from __future__ import annotations

from statistics import median

from ..api import Checker, Row
from .trace_utils import median_step, property_diagnostics, sample_signal, threshold_crossings

BITS = ["din1", "din2", "din3", "din4"]
WEIGHTS = (0.5, 1.0, 2.0, 4.0)
PROPERTIES = {
    "P_FIRST_READY_EDGE_ARMS_ONLY": 0,
    "P_READY_SAMPLES_FOUR_BITS": 0,
    "P_SWITCHED_WEIGHT_DENOMINATOR": 0,
    "P_BIPOLAR_CDAC_OUTPUT": 0,
}


def _expected_aout(rows: list[Row], time_s: float, vdd: float, vth: float) -> float | None:
    switched = 0.0
    for signal, weight in zip(BITS, WEIGHTS):
        value = sample_signal(rows, signal, time_s)
        if value is None:
            return None
        if value > vth:
            switched += weight
    return switched / 8.5 * 2.0 * vdd - vdd


def check_v3_l2_cdac_4b_switch(rows: list[Row]) -> tuple[bool, str]:
    required = {"time", "rdy", *BITS, "aout"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing l2 cdac 4b switch signals"

    vdd = max(max(row[signal] for row in rows) for signal in ("rdy", *BITS))
    if vdd < 0.8:
        return False, f"insufficient_excitation l2_cdac_4b_switch rail_hi={vdd:.4g}"
    vth = 0.5 * vdd
    ready_edges = threshold_crossings(rows, "rdy", threshold=vth, direction=1)
    if len(ready_edges) < 3:
        return (
            False,
            "insufficient_excitation l2_cdac_4b_switch "
            f"ready_edges={len(ready_edges)} required>=3",
        )

    periods = [
        ready_edges[index] - ready_edges[index - 1]
        for index in range(1, len(ready_edges))
        if ready_edges[index] > ready_edges[index - 1]
    ]
    period = median(periods) if periods else rows[-1]["time"] - rows[0]["time"]
    settle = max(median_step(rows) * 5.0, min(period * 0.08, period * 0.25))
    tol = 0.045
    counts = dict(PROPERTIES)
    checked_edges = 0
    max_err = 0.0

    first_sample_time = ready_edges[0] + settle
    first_value = sample_signal(rows, "aout", first_sample_time)
    if first_value is None:
        return False, "missing_aout_after_first_ready_edge"
    first_err = abs(first_value - 0.0)
    max_err = max(max_err, first_err)
    if first_err > tol:
        counts["P_FIRST_READY_EDGE_ARMS_ONLY"] += 1
        counts["P_BIPOLAR_CDAC_OUTPUT"] += 1

    distinct_codes: set[tuple[int, ...]] = set()
    for index, edge in enumerate(ready_edges[1:], start=1):
        sample_times = [edge + settle]
        if index + 1 < len(ready_edges):
            sample_times.append(edge + 0.5 * (ready_edges[index + 1] - edge))
        for sample_time in sample_times:
            if sample_time > rows[-1]["time"]:
                continue
            expected = _expected_aout(rows, edge + settle * 0.25, vdd, vth)
            observed = sample_signal(rows, "aout", sample_time)
            if expected is None or observed is None:
                continue
            bits = tuple(
                int((sample_signal(rows, signal, edge + settle * 0.25) or 0.0) > vth)
                for signal in BITS
            )
            distinct_codes.add(bits)
            checked_edges += 1
            err = abs(observed - expected)
            max_err = max(max_err, err)
            if err > tol:
                counts["P_READY_SAMPLES_FOUR_BITS"] += 1
                counts["P_SWITCHED_WEIGHT_DENOMINATOR"] += 1
                counts["P_BIPOLAR_CDAC_OUTPUT"] += 1

    if checked_edges < 2 or len(distinct_codes) < 2:
        return (
            False,
            "insufficient_excitation l2_cdac_4b_switch "
            f"checked_edges={checked_edges} distinct_codes={len(distinct_codes)}",
        )

    ok = all(count == 0 for count in counts.values())
    return (
        ok,
        f"{property_diagnostics(counts)}; ready_edges={len(ready_edges)}; "
        f"checked_edges={checked_edges}; distinct_codes={len(distinct_codes)}; "
        f"max_err={max_err:.6g}",
    )


CHECKER_ID = "v4_200_l2_cdac_4b_switch"
CHECKER: Checker = check_v3_l2_cdac_4b_switch
