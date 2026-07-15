"""Task-specific checker for canonical v4 DUT 084."""
from __future__ import annotations

from ..api import Checker
import math

def rising_edges(values: list[float], times: list[float], threshold: float = 0.45) -> list[float]:
    edges: list[float] = []
    for i in range(1, len(values)):
        if values[i - 1] < threshold <= values[i]:
            edges.append(times[i])
    return edges

def check_bbpd_data_edge_alignment(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"clk", "data", "up", "dn"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing clk/data/up/dn"

    vth = 0.45
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
        f"overlap_frac={overlap_frac:.4f}"
    )

CHECKER_ID = "v4_084_bbpd_data_edge_alignment"
CHECKER: Checker = check_bbpd_data_edge_alignment
