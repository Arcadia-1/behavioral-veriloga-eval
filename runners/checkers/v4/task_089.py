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
    rows: list[dict[str, float]] = []
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            rows.append({name: _float_at(row, indices[name]) for name in required})
    passed, detail = check_cross_interval_163p333(rows)
    return (1.0 if passed else 0.0), [detail]

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
    if len(a_edges) < 2 or len(b_edges) < 2:
        return False, f"missing_input_edges a={len(a_edges)} b={len(b_edges)}"

    seen_hi = max(r["seen_out"] for r in rows)
    seen_rail_error = abs(seen_hi - (vss_level + supply_span))
    if seen_rail_error > 0.08:
        return False, f"seen_out_high_not_supply_rail error={seen_rail_error:.3f}"

    seen_th = vss_level + 0.5 * supply_span
    cycle_notes: list[str] = []
    checked_cycles = 0
    for cycle_index, a_t in enumerate(a_edges):
        next_a = a_edges[cycle_index + 1] if cycle_index + 1 < len(a_edges) else None
        b_after_a = [
            edge for edge in b_edges
            if edge > a_t and (next_a is None or edge < next_a)
        ]
        if not b_after_a:
            return False, f"missing_b_edge_after_a cycle={cycle_index}"
        b_t = b_after_a[0]
        pre_capture_rows = [
            r for r in rows
            if a_t + 0.03e-9 <= r["time"] < b_t - 0.03e-9
        ]
        if pre_capture_rows and max(r["seen_out"] for r in pre_capture_rows) > seen_th:
            return False, f"seen_out_not_cleared_after_a cycle={cycle_index}"

        window_end = next_a - 0.05e-9 if next_a is not None else rows[-1]["time"]
        capture_rows = [
            r for r in rows
            if b_t + 0.2e-9 <= r["time"] <= window_end and r["seen_out"] > seen_th
        ]
        if len(capture_rows) < 3:
            return False, f"seen_out_no_logic_high_samples cycle={cycle_index}"
        tail_count = min(len(capture_rows), max(5, len(capture_rows) // 3))
        tail = sorted(r["delay_out"] for r in capture_rows[-tail_count:])
        delay_level = tail[len(tail) // 2]
        delay_ps = (delay_level - vss_level) / supply_span * 200.0
        expected_ps = (b_t - a_t) * 1.0e12
        err_ps = abs(delay_ps - expected_ps)
        if not (0.0 < expected_ps < 500.0 and err_ps <= 15.0):
            return False, (
                f"delay_ps={delay_ps:.3f} expected_ps={expected_ps:.3f} "
                f"err_ps={err_ps:.3f} cycle={cycle_index}"
            )
        cycle_notes.append(
            f"cycle{cycle_index}:delay_ps={delay_ps:.3f},expected_ps={expected_ps:.3f},err_ps={err_ps:.3f}"
        )
        checked_cycles += 1
    if checked_cycles < 2:
        return False, f"insufficient_measurement_cycles={checked_cycles}"
    return True, (
        " ".join(cycle_notes)
        + f" supply_span={supply_span:.3f} seen_rail_error={seen_rail_error:.3f}"
    )

CHECKER_ID = "v4_089_edge_crossing_interval_timer"
CHECKER: Checker = check_cross_interval_163p333
STREAMING_CHECKER = _stream_cross_interval_163p333_csv
