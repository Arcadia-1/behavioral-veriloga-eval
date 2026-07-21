"""Task-specific checker for canonical v4 DUT 089."""
from __future__ import annotations

import csv
from pathlib import Path

from ..api import Checker

def _csv_header_indices(csv_path: Path) -> tuple[list[str], dict[str, int]]:
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, [])
    return header, {name: idx for idx, name in enumerate(header)}

def _csv_required_indices(csv_path: Path, required: set[str]) -> tuple[dict[str, int] | None, list[str]]:
    header, index = _csv_header_indices(csv_path)
    missing = sorted(required - set(header))
    if missing:
        return None, missing
    return {name: index[name] for name in required}, []

def _float_at(row: list[str], index: int, default: float = 0.0) -> float:
    try:
        return float(row[index])
    except (IndexError, TypeError, ValueError):
        return default

def _stream_cross_interval_163p333_csv(csv_path: Path) -> tuple[float, list[str]]:
    required = {"time", "vdd", "vss", "a", "b", "delay_out", "seen_out"}
    indices, _missing = _csv_required_indices(csv_path, required)
    if indices is None:
        return 0.0, ["missing time/vdd/vss/a/b/delay_out/seen_out"]
    assert indices is not None

    supply_span = 0.0
    vss_level = 0.0
    observed_seen_hi = float("-inf")
    prev_a: float | None = None
    prev_b: float | None = None
    a_t: float | None = None
    b_t: float | None = None
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            time_value = _float_at(row, indices["time"])
            a = _float_at(row, indices["a"])
            b = _float_at(row, indices["b"])
            vdd = _float_at(row, indices["vdd"])
            vss_level = _float_at(row, indices["vss"])
            observed_seen_hi = max(observed_seen_hi, _float_at(row, indices["seen_out"]))
            supply_span = max(supply_span, vdd - vss_level)
            threshold = vss_level + 0.5 * (vdd - vss_level)
            if prev_a is not None and a_t is None and prev_a <= threshold < a:
                a_t = time_value
            if prev_b is not None and a_t is not None and b_t is None and time_value > a_t and prev_b <= threshold < b:
                b_t = time_value
            prev_a = a
            prev_b = b
    if a_t is None or b_t is None:
        return 0.0, [f"missing_input_edges a={a_t is not None} b={b_t is not None}"]
    if supply_span < 0.2:
        return 0.0, [f"invalid_supply_span={supply_span:.3f}"]

    seen_th = vss_level + 0.5 * supply_span
    first_seen_time: float | None = None
    seen_delay_values: list[float] = []
    settled_delay_values: list[float] = []
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            time_value = _float_at(row, indices["time"])
            seen = _float_at(row, indices["seen_out"])
            if seen <= seen_th:
                continue
            if first_seen_time is None:
                first_seen_time = time_value
            delay = _float_at(row, indices["delay_out"])
            seen_delay_values.append(delay)
            if time_value >= first_seen_time + 0.2e-9:
                settled_delay_values.append(delay)

    if first_seen_time is None:
        return 0.0, ["seen_out_no_logic_high_samples"]
    if len(settled_delay_values) < 3:
        settled_delay_values = seen_delay_values
    tail_count = min(len(settled_delay_values), max(5, len(settled_delay_values) // 3))
    tail = sorted(settled_delay_values[-tail_count:])
    if not tail:
        return 0.0, ["no_post_seen_delay_samples"]
    delay_level = tail[len(tail) // 2]
    seen_rail_error = abs(observed_seen_hi - (vss_level + supply_span))
    delay_ps = (delay_level - vss_level) / supply_span * 200.0
    expected_ps = (b_t - a_t) * 1.0e12
    err_ps = abs(delay_ps - expected_ps)
    ok = 0.0 < expected_ps < 500.0 and err_ps <= 15.0 and seen_rail_error <= 0.08
    return (1.0 if ok else 0.0), [
        f"delay_ps={delay_ps:.3f} expected_ps={expected_ps:.3f} "
        f"err_ps={err_ps:.3f} supply_span={supply_span:.3f} "
        f"seen_rail_error={seen_rail_error:.3f} post_seen_samples={len(settled_delay_values)}"
    ]

def rising_edges(values: list[float], times: list[float], threshold: float = 0.45) -> list[float]:
    edges: list[float] = []
    for i in range(1, len(values)):
        if values[i - 1] < threshold <= values[i]:
            edges.append(times[i])
    return edges

def check_cross_interval_163p333(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vdd", "vss", "a", "b", "delay_out", "seen_out"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/vdd/vss/a/b/delay_out/seen_out"
    supply_spans = [r["vdd"] - r["vss"] for r in rows]
    supply_span = sum(supply_spans) / len(supply_spans)
    vss_level = sum(r["vss"] for r in rows) / len(rows)
    if supply_span < 0.2 or max(supply_spans) - min(supply_spans) > 0.02:
        return False, f"invalid_supply_span={supply_span:.3f}"
    threshold = vss_level + 0.5 * supply_span
    times = [r["time"] for r in rows]
    a_edges = rising_edges([r["a"] for r in rows], times, threshold=threshold)
    b_edges = rising_edges([r["b"] for r in rows], times, threshold=threshold)
    if not a_edges or not b_edges:
        return False, f"missing_input_edges a={len(a_edges)} b={len(b_edges)}"
    a_t = a_edges[0]
    b_t = next((edge for edge in b_edges if edge > a_t), None)
    if b_t is None:
        return False, "missing_b_edge_after_a"

    seen_hi = max(r["seen_out"] for r in rows)
    seen_rail_error = abs(seen_hi - (vss_level + supply_span))
    if seen_rail_error > 0.08:
        return False, f"seen_out_high_not_supply_rail error={seen_rail_error:.3f}"

    seen_th = vss_level + 0.5 * supply_span
    seen_rows = [r for r in rows if r["seen_out"] > seen_th]
    if not seen_rows:
        return False, "seen_out_no_logic_high_samples"
    # The event happens late in a short run. Averaging the final 30% of the
    # whole waveform incorrectly includes pre-event zeros, so measure the
    # settled delay level only after seen_out has asserted.
    settle_start = seen_rows[0]["time"] + 0.2e-9
    settled_rows = [r for r in seen_rows if r["time"] >= settle_start]
    if len(settled_rows) < 3:
        settled_rows = seen_rows
    tail_count = min(len(settled_rows), max(5, len(settled_rows) // 3))
    tail = sorted(r["delay_out"] for r in settled_rows[-tail_count:])
    if not tail:
        return False, "no_post_seen_delay_samples"
    delay_level = tail[len(tail) // 2]
    delay_ps = (delay_level - vss_level) / supply_span * 200.0
    expected_ps = (b_t - a_t) * 1.0e12
    err_ps = abs(delay_ps - expected_ps)
    ok = 0.0 < expected_ps < 500.0 and err_ps <= 15.0
    return ok, (
        f"delay_ps={delay_ps:.3f} expected_ps={expected_ps:.3f} "
        f"err_ps={err_ps:.3f} supply_span={supply_span:.3f} "
        f"seen_rail_error={seen_rail_error:.3f} post_seen_samples={len(settled_rows)}"
    )

CHECKER_ID = "v4_089_edge_crossing_interval_timer"
CHECKER: Checker = check_cross_interval_163p333
STREAMING_CHECKER = _stream_cross_interval_163p333_csv
