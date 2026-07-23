"""Task-specific checker for canonical v4 DUT 102."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import structured_result


def check_v3_clocked_sine_source(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst_n", "vinp", "vinn", "vamp_p", "vamp_n"}
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - (set(rows[0]) if rows else set()))
        return False, f"missing_clocked_sine_signals={','.join(missing)}"

    vdd = _max_signal_value(rows, ["clk", "rst_n"], default=0.9)
    vth = 0.5 * vdd
    common_mode = 0.5 * vdd
    reset_rows = [row for row in rows if row["rst_n"] < vth]
    reset_cm_err = max(
        (max(abs(row["vinp"] - common_mode), abs(row["vinn"] - common_mode)) for row in reset_rows),
        default=float("inf"),
    )
    reference_err = max((abs(row["vinn"] - common_mode) for row in rows), default=float("inf"))

    edges: list[float] = []
    previous = rows[0]
    for row in rows[1:]:
        if previous["clk"] < vth <= row["clk"] and row["rst_n"] >= vth:
            edges.append(row["time"])
        previous = row
    if len(edges) < 20:
        return False, f"too_few_active_clock_edges={len(edges)}"

    sampled: list[float] = []
    hold_errors: list[float] = []
    for left, right in zip(edges, edges[1:]):
        after_edge = sample_signal_at(rows, "vinp", left + 1.5e-9)
        before_next = sample_signal_at(rows, "vinp", right - 1.5e-9)
        if after_edge is None or before_next is None:
            continue
        sampled.append(after_edge)
        hold_errors.append(abs(before_next - after_edge))
    if len(sampled) < 15:
        return False, f"insufficient_sample_hold_windows={len(sampled)}"

    source_span = max(sampled) - min(sampled)
    max_hold_err = max(hold_errors, default=float("inf"))
    vin_diff = [row["vinp"] - row["vinn"] for row in rows if row["rst_n"] >= vth]
    vamp_diff = [row["vamp_p"] - row["vamp_n"] for row in rows if row["rst_n"] >= vth]
    mean_in = sum(vin_diff) / len(vin_diff)
    mean_out = sum(vamp_diff) / len(vamp_diff)
    std_in = (sum((value - mean_in) ** 2 for value in vin_diff) / len(vin_diff)) ** 0.5
    std_out = (sum((value - mean_out) ** 2 for value in vamp_diff) / len(vamp_diff)) ** 0.5
    gain = std_out / std_in if std_in > 1e-12 else 0.0

    ok = (
        reset_cm_err <= 0.025
        and reference_err <= 0.015
        and source_span >= 0.025
        and max_hold_err <= 0.004
        and gain > 4.0
    )
    return ok, (
        f"active_edges={len(edges)} reset_cm_err={reset_cm_err:.5f} "
        f"reference_err={reference_err:.5f} source_span={source_span:.5f} "
        f"max_hold_err={max_hold_err:.5f} downstream_gain={gain:.2f}"
    )

def sample_signal_at(rows: list[dict[str, float]], signal: str, time_s: float) -> float | None:
    if not rows or "time" not in rows[0] or signal not in rows[0]:
        return None
    first_time = rows[0]["time"]
    last_time = rows[-1].get("time")
    if last_time is None or time_s < first_time or time_s > last_time:
        return None
    if time_s == first_time:
        return rows[0].get(signal)
    for idx in range(1, len(rows)):
        prev = rows[idx - 1]
        cur = rows[idx]
        t0 = prev.get("time")
        t1 = cur.get("time")
        if t0 is None or t1 is None:
            continue
        if t0 <= time_s <= t1:
            v0 = prev.get(signal)
            v1 = cur.get(signal)
            if v0 is None or v1 is None:
                return None
            if t1 == t0:
                return v1
            alpha = (time_s - t0) / (t1 - t0)
            return v0 + alpha * (v1 - v0)
    return None

def _max_signal_value(
    rows: list[dict[str, float]],
    signals: list[str],
    *,
    default: float,
) -> float:
    values: list[float] = []
    for row in rows:
        for signal in signals:
            value = row.get(signal)
            if value is not None:
                values.append(value)
    return max(values) if values else default

CHECKER_ID = "v4_102_clocked_sine_source"
PROPERTY_IDS = (
    "P_RESET_COMMON_MODE",
    "P_RISING_EDGE_SAMPLE",
    "P_SAMPLED_SINE",
    "P_REFERENCE_SIDE_COMMON_MODE",
    "P_INTEREDGE_HOLD",
    "P_SEEDED_REPEATABILITY",
)
CHECKER: Checker = structured_result(check_v3_clocked_sine_source, PROPERTY_IDS)
