"""Task-specific checker for canonical v4 DUT 089."""
from __future__ import annotations

import csv
from pathlib import Path

from ..api import Checker

BASE_SIGNALS = ("vdd", "vss", "a", "b", "delay_out", "seen_out")


def _signal(base: str, label: str) -> str:
    return base if not label else f"{base}_{label}"


def _ref(rows: list[dict[str, float]], base: str, label: str) -> float | None:
    name = _signal(base, label)
    if not rows or name not in rows[0]:
        return None
    values = [float(row[name]) for row in rows if name in row]
    return sum(values) / len(values) if values else None


def _groups_from_columns(columns: set[str]) -> list[str]:
    groups: list[str] = []
    if {"time", *BASE_SIGNALS}.issubset(columns):
        groups.append("")
    for column in sorted(columns):
        if not column.startswith("delay_out_"):
            continue
        label = column[len("delay_out_") :]
        if all(_signal(base, label) in columns for base in BASE_SIGNALS):
            groups.append(label)
    return groups


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
    header, header_indices = _csv_header_indices(csv_path)
    groups = _groups_from_columns(set(header))
    if not groups:
        return 0.0, ["missing time/vdd/vss/a/b/delay_out/seen_out grouped trace"]
    required = {"time"}
    for label in groups:
        required.update(_signal(base, label) for base in BASE_SIGNALS)
        for ref_base in ("vth_ref", "scale_ps_ref", "tedge_ps_ref"):
            ref_name = _signal(ref_base, label)
            if ref_name in header_indices:
                required.add(ref_name)
    indices, _missing = _csv_required_indices(csv_path, required)
    if indices is None:
        return 0.0, ["missing grouped interval timer columns"]
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


def _transition_span_ps(
    rows: list[dict[str, float]],
    signal: str,
    low: float,
    high: float,
) -> float | None:
    span = high - low
    if span <= 0.0:
        return None
    lo_th = low + 0.2 * span
    hi_th = low + 0.8 * span
    spans: list[float] = []
    start: float | None = None
    for left, right in zip(rows, rows[1:]):
        lv = float(left[signal])
        rv = float(right[signal])
        if lv <= lo_th < rv:
            frac = (lo_th - lv) / (rv - lv)
            start = float(left["time"]) + frac * (float(right["time"]) - float(left["time"]))
        elif lv >= hi_th > rv:
            frac = (lv - hi_th) / (lv - rv)
            start = float(left["time"]) + frac * (float(right["time"]) - float(left["time"]))
        if start is None:
            continue
        if lv <= hi_th < rv:
            frac = (hi_th - lv) / (rv - lv)
            stop = float(left["time"]) + frac * (float(right["time"]) - float(left["time"]))
            spans.append(abs(stop - start) * 1.0e12)
            start = None
        elif lv >= lo_th > rv:
            frac = (lv - lo_th) / (lv - rv)
            stop = float(left["time"]) + frac * (float(right["time"]) - float(left["time"]))
            spans.append(abs(stop - start) * 1.0e12)
            start = None
    if not spans:
        return None
    spans.sort()
    return spans[len(spans) // 2]


def _check_group(rows: list[dict[str, float]], label: str) -> tuple[bool, str]:
    required = {"time", *{_signal(base, label) for base in BASE_SIGNALS}}
    if not rows or not required.issubset(rows[0]):
        return False, f"missing grouped interval timer signals instance={label or 'legacy'}"
    vdd = _signal("vdd", label)
    vss = _signal("vss", label)
    a = _signal("a", label)
    b = _signal("b", label)
    delay_out = _signal("delay_out", label)
    seen_out = _signal("seen_out", label)
    supply_spans = [r[vdd] - r[vss] for r in rows]
    supply_span = sum(supply_spans) / len(supply_spans)
    vss_level = sum(r[vss] for r in rows) / len(rows)
    if supply_span < 0.2 or max(supply_spans) - min(supply_spans) > 0.02:
        return False, f"invalid_supply_span={supply_span:.3f} instance={label or 'legacy'}"
    vth_ref = _ref(rows, "vth_ref", label)
    scale_ps_ref = _ref(rows, "scale_ps_ref", label) or 200.0
    tedge_ps_ref = _ref(rows, "tedge_ps_ref", label)
    threshold = vss_level + (vth_ref if vth_ref is not None else 0.5 * supply_span)
    times = [r["time"] for r in rows]
    a_edges = rising_edges([r[a] for r in rows], times, threshold=threshold)
    b_edges = rising_edges([r[b] for r in rows], times, threshold=threshold)
    if len(a_edges) < 2 or len(b_edges) < 2:
        return False, f"missing_input_edges a={len(a_edges)} b={len(b_edges)} instance={label or 'legacy'}"

    seen_hi = max(r[seen_out] for r in rows)
    seen_rail_error = abs(seen_hi - (vss_level + supply_span))
    if seen_rail_error > 0.08:
        return False, f"seen_out_high_not_supply_rail error={seen_rail_error:.3f} instance={label or 'legacy'}"
    if tedge_ps_ref is not None and tedge_ps_ref >= 45.0:
        observed_tedge = _transition_span_ps(rows, seen_out, vss_level, vss_level + supply_span)
        if observed_tedge is None or observed_tedge < max(25.0, 0.45 * tedge_ps_ref):
            return False, (
                f"tedge_smoothing_too_fast instance={label or 'legacy'} "
                f"expected_span_ps>={max(25.0, 0.45 * tedge_ps_ref):.3f} "
                f"observed_span_ps={observed_tedge if observed_tedge is not None else 'missing'}"
            )

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
        clear_guard = max(0.03e-9, 2.5 * (tedge_ps_ref or 20.0) * 1.0e-12)
        pre_capture_rows = [
            r for r in rows
            if a_t + clear_guard <= r["time"] < b_t - 0.03e-9
        ]
        if pre_capture_rows and max(r[seen_out] for r in pre_capture_rows) > seen_th:
            return False, f"seen_out_not_cleared_after_a cycle={cycle_index} instance={label or 'legacy'}"

        window_end = next_a - 0.05e-9 if next_a is not None else rows[-1]["time"]
        capture_rows = [
            r for r in rows
            if b_t + 0.2e-9 <= r["time"] <= window_end and r[seen_out] > seen_th
        ]
        if len(capture_rows) < 3:
            return False, f"seen_out_no_logic_high_samples cycle={cycle_index} instance={label or 'legacy'}"
        tail_count = min(len(capture_rows), max(5, len(capture_rows) // 3))
        tail = sorted(r[delay_out] for r in capture_rows[-tail_count:])
        delay_level = tail[len(tail) // 2]
        delay_ps = (delay_level - vss_level) / supply_span * scale_ps_ref
        expected_ps = (b_t - a_t) * 1.0e12
        err_ps = abs(delay_ps - expected_ps)
        if not (0.0 < expected_ps < 500.0 and err_ps <= 15.0):
            return False, (
                f"delay_ps={delay_ps:.3f} expected_ps={expected_ps:.3f} "
                f"err_ps={err_ps:.3f} cycle={cycle_index} instance={label or 'legacy'}"
            )
        cycle_notes.append(
            f"{label or 'legacy'}:cycle{cycle_index}:delay_ps={delay_ps:.3f},expected_ps={expected_ps:.3f},err_ps={err_ps:.3f}"
        )
        checked_cycles += 1
    if checked_cycles < 2:
        return False, f"insufficient_measurement_cycles={checked_cycles} instance={label or 'legacy'}"
    return True, (
        " ".join(cycle_notes)
        + f" instance={label or 'legacy'} supply_span={supply_span:.3f} scale_ps={scale_ps_ref:.3f} seen_rail_error={seen_rail_error:.3f}"
    )


def check_cross_interval_163p333(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "missing time/vdd/vss/a/b/delay_out/seen_out"
    groups = _groups_from_columns(set(rows[0]))
    if not groups:
        return False, "missing time/vdd/vss/a/b/delay_out/seen_out grouped trace"
    notes: list[str] = []
    for label in groups:
        passed, detail = _check_group(rows, label)
        if not passed:
            return False, detail
        notes.append(detail)
    if len(groups) < 2 and any(name.startswith("vth_ref_") for name in rows[0]):
        return False, f"insufficient_parameter_override_coverage instances={groups}"
    return True, " ".join(notes)

CHECKER_ID = "v4_089_edge_crossing_interval_timer"
CHECKER: Checker = check_cross_interval_163p333
STREAMING_CHECKER = _stream_cross_interval_163p333_csv
