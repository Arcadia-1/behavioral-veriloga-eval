"""Task-specific checker for canonical v4 DUT 084."""
from __future__ import annotations

import math

from ..api import Checker
from .stimulus_relative import sample

def rising_edges(values: list[float], times: list[float], threshold: float = 0.45) -> list[float]:
    edges: list[float] = []
    for i in range(1, len(values)):
        if values[i - 1] < threshold <= values[i]:
            edges.append(times[i])
    return edges

def check_bbpd_data_edge_alignment(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vdd", "vss", "clk", "data", "up", "dn", "retimed_data"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/vdd/vss/clk/data/up/dn/retimed_data"

    supply_spans = [row["vdd"] - row["vss"] for row in rows]
    supply_span = sum(supply_spans) / len(supply_spans)
    vss = sum(row["vss"] for row in rows) / len(rows)
    vdd = vss + supply_span
    if supply_span < 0.2 or max(supply_spans) - min(supply_spans) > 0.02:
        return False, f"invalid_supply_span={supply_span:.3f}"
    vth = vss + 0.5 * supply_span
    times = [r["time"] for r in rows]
    clk_vals = [r["clk"] for r in rows]
    up = [r["up"] for r in rows]
    dn = [r["dn"] for r in rows]
    data = [r["data"] for r in rows]

    clk_edges = rising_edges(clk_vals, times, threshold=vth)
    if len(clk_edges) < 4:
        return False, f"too_few_clk_edges={len(clk_edges)}"
    clk_periods = [b - a for a, b in zip(clk_edges, clk_edges[1:]) if b > a]
    clk_period = sorted(clk_periods)[len(clk_periods) // 2] if clk_periods else 20e-9
    if clk_period <= 0:
        return False, f"bad_clk_period={clk_period:.3e}"

    retimed_checks = 0
    retimed_max_error = 0.0
    retimed_decisions: set[int] = set()
    for index, edge_t in enumerate(clk_edges):
        next_edge = clk_edges[index + 1] if index + 1 < len(clk_edges) else rows[-1]["time"]
        if next_edge - edge_t < 1.0e-9:
            continue
        captured = sample(rows, "data", edge_t)
        if captured is None:
            continue
        expected = vdd if captured > vth else vss
        retimed_decisions.add(1 if expected > vth else 0)
        for fraction in (0.25, 0.70):
            probe_t = edge_t + fraction * (next_edge - edge_t)
            observed = sample(rows, "retimed_data", probe_t)
            if observed is None:
                return False, f"missing_retimed_data_probe@{probe_t:.3e}"
            error = abs(observed - expected)
            retimed_max_error = max(retimed_max_error, error)
            retimed_checks += 1
            if error > max(0.04, 0.09 * supply_span):
                return False, (
                    f"retimed_data_mismatch edge={index} fraction={fraction:.2f} "
                    f"observed={observed:.4f} expected={expected:.4f}"
                )
    if retimed_checks < 6 or retimed_decisions != {0, 1}:
        return False, (
            f"insufficient_retimed_coverage checks={retimed_checks} "
            f"decisions={sorted(retimed_decisions)}"
        )

    data_edges = [
        times[i]
        for i in range(1, len(rows))
        if ((data[i - 1] <= vth < data[i]) or (data[i - 1] >= vth > data[i]))
    ]
    if len(data_edges) < 6:
        return False, f"too_few_data_edges={len(data_edges)}"

    overlap = sum(1 for r in rows if r["up"] > vth and r["dn"] > vth)
    overlap_frac = overlap / max(len(rows), 1)
    if overlap_frac > 0.02:
        return False, f"overlap_frac={overlap_frac:.4f}"

    def clock_neighbors(edge_t: float) -> tuple[float, float]:
        first = clk_edges[0]
        periods_from_first = math.floor((edge_t - first) / clk_period)
        prev_clk = first + periods_from_first * clk_period
        if prev_clk > edge_t:
            prev_clk -= clk_period
        next_clk = prev_clk + clk_period
        return prev_clk, next_clk

    def pulse_seen(signal: str, start: float, stop: float) -> bool:
        return any(row[signal] > vth for row in rows if start <= row["time"] <= stop)

    counts = {"up": 0, "dn": 0, "none": 0}
    hits = {"up": 0, "dn": 0, "none": 0}
    deadzone = 0.8e-9
    pulse_window = 1.6e-9
    checked = 0
    for edge_t in data_edges:
        prev_clk, next_clk = clock_neighbors(edge_t)
        dist_prev = edge_t - prev_clk
        dist_next = next_clk - edge_t
        if dist_next < dist_prev and dist_next > deadzone:
            expected = "up"
        elif dist_prev < dist_next and dist_prev > deadzone:
            expected = "dn"
        else:
            expected = "none"
        up_hit = pulse_seen("up", edge_t, edge_t + pulse_window)
        dn_hit = pulse_seen("dn", edge_t, edge_t + pulse_window)
        counts[expected] += 1
        checked += 1
        if expected == "up" and up_hit and not dn_hit:
            hits["up"] += 1
        elif expected == "dn" and dn_hit and not up_hit:
            hits["dn"] += 1
        elif expected == "none" and not up_hit and not dn_hit:
            hits["none"] += 1

    if checked < 6:
        return False, f"too_few_checked_edges={checked}"
    if counts["up"] < 2 or hits["up"] < counts["up"]:
        return False, f"up_hits={hits['up']}/{counts['up']}"
    if counts["dn"] < 2 or hits["dn"] < counts["dn"]:
        return False, f"dn_hits={hits['dn']}/{counts['dn']}"
    if counts["none"] and hits["none"] < counts["none"]:
        return False, f"deadzone_suppression={hits['none']}/{counts['none']}"

    return True, (
        f"data_edges={len(data_edges)} clk_period={clk_period:.3e} "
        f"up={hits['up']}/{counts['up']} dn={hits['dn']}/{counts['dn']} "
        f"none={hits['none']}/{counts['none']} "
        f"overlap_frac={overlap_frac:.4f} retimed_checks={retimed_checks} "
        f"retimed_max_error={retimed_max_error:.4f} supply_span={supply_span:.3f}"
    )

CHECKER_ID = "v4_084_bbpd_data_edge_alignment"
CHECKER: Checker = check_bbpd_data_edge_alignment
