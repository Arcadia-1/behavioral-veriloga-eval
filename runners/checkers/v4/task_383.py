"""Task-specific checker for canonical v4 DUT 383."""
from __future__ import annotations

from statistics import median

from ..api import Checker


REQUIRED_SIGNALS = {"time", "enable", "rst", "osc_out", "period_metric", "valid"}
VTH = 0.45
LOW_TOL = 0.12
HIGH_TOL = 0.65
NOMINAL_PERIOD = 20e-9


def _level(row: dict[str, float], name: str, threshold: float = VTH) -> bool | None:
    value = float(row.get(name, 0.0))
    if 0.1 < value < 0.8:
        return None
    return value > threshold


def _property_note(property_id: str, mismatch_count: int, expected: str, observed: str) -> str:
    return (
        f"{property_id} mismatch_count={mismatch_count} "
        f"expected={expected} observed={observed}"
    )


def _missing_columns(rows: list[dict[str, float]]) -> str | None:
    if not rows:
        return _property_note("P_TRACE_CONTRACT", 1, "non_empty_trace", "empty_trace")
    missing = sorted(REQUIRED_SIGNALS - set(rows[0]))
    if missing:
        return _property_note("P_TRACE_CONTRACT", len(missing), "required_public_traces", ",".join(missing))
    return None


def _enabled(row: dict[str, float]) -> bool:
    enable = _level(row, "enable")
    rst = _level(row, "rst")
    return enable is True and rst is False


def _clear_outputs(row: dict[str, float]) -> bool:
    return (
        float(row["osc_out"]) < LOW_TOL
        and float(row["period_metric"]) < LOW_TOL
        and float(row["valid"]) < LOW_TOL
    )


def _segments(rows: list[dict[str, float]], enabled: bool) -> list[list[dict[str, float]]]:
    groups: list[list[dict[str, float]]] = []
    current: list[dict[str, float]] = []
    for row in rows:
        if _enabled(row) == enabled:
            current.append(row)
        elif current:
            groups.append(current)
            current = []
    if current:
        groups.append(current)
    return groups


def _span(rows: list[dict[str, float]]) -> float:
    return float(rows[-1]["time"]) - float(rows[0]["time"])


def _edge_times(rows: list[dict[str, float]]) -> tuple[list[float], list[float]]:
    edges: list[float] = []
    rises: list[float] = []
    last = float(rows[0]["osc_out"]) > VTH
    for row in rows[1:]:
        cur = float(row["osc_out"]) > VTH
        if cur != last:
            t = float(row["time"])
            edges.append(t)
            if cur:
                rises.append(t)
        last = cur
    return edges, rises


def check_v4_942_fixed_frequency_oscillator_source(rows: list[dict[str, float]]) -> tuple[bool, str]:
    missing = _missing_columns(rows)
    if missing:
        return False, missing
    rows = sorted(rows, key=lambda row: float(row["time"]))

    enabled_segments = [seg for seg in _segments(rows, True) if _span(seg) >= 0.9 * NOMINAL_PERIOD]
    disabled_segments = [seg for seg in _segments(rows, False) if _span(seg) >= 2e-9]
    reset_segments = [
        seg for seg in disabled_segments if any(_level(row, "rst") is True for row in seg)
    ]
    pure_disable_segments = [
        seg
        for seg in disabled_segments
        if any(_level(row, "enable") is False for row in seg)
        and not any(_level(row, "rst") is True for row in seg)
    ]

    clear_errors = sum(
        1
        for seg in disabled_segments
        for row in seg
        if float(row["time"]) >= float(seg[0]["time"]) + 1.0e-9 and not _clear_outputs(row)
    )
    all_edges: list[float] = []
    edge_intervals: list[float] = []
    segment_errors = valid_errors = restart_errors = 0
    metric_samples: list[float] = []
    osc_high_seen = osc_low_seen = False

    for seg in enabled_segments:
        start = float(seg[0]["time"])
        end = float(seg[-1]["time"])
        edges, rises = _edge_times(seg)
        all_edges.extend(edges)
        edge_intervals.extend(b - a for a, b in zip(edges, edges[1:]) if b > a)
        osc_values = [float(row["osc_out"]) for row in seg]
        osc_high_seen = osc_high_seen or max(osc_values) > HIGH_TOL
        osc_low_seen = osc_low_seen or min(osc_values) < LOW_TOL
        if len(edges) < 3 or len(rises) < 2:
            segment_errors += 1
        if any((b - a) > 12.5e-9 for a, b in zip(edges, edges[1:])):
            segment_errors += 1
        if rises and abs((rises[0] - start) - NOMINAL_PERIOD / 2.0) > 2.5e-9:
            restart_errors += 1
        elif not rises:
            restart_errors += 1

        early_valid = [
            row
            for row in seg
            if float(row["time"]) <= start + 0.9 * NOMINAL_PERIOD
            and _level(row, "valid") is True
        ]
        late_rows = [row for row in seg if float(row["time"]) >= start + 1.1 * NOMINAL_PERIOD]
        late_valid_low = [row for row in late_rows if _level(row, "valid") is not True]
        if early_valid or late_valid_low:
            valid_errors += 1
        metric_samples.extend(float(row["period_metric"]) for row in late_rows)
        if end - start < 1.4 * NOMINAL_PERIOD:
            segment_errors += 1

    half_period_errors = sum(1 for dt in edge_intervals if not 8.0e-9 <= dt <= 12.0e-9)
    measured_period = 2.0 * median(edge_intervals) if edge_intervals else 0.0
    expected_metric = min(0.9, max(0.0, measured_period / NOMINAL_PERIOD * 0.45)) if measured_period else 0.0
    if metric_samples:
        metric_mid = median(metric_samples)
        metric_span = max(metric_samples) - min(metric_samples)
        metric_stable = metric_span <= 0.08
        metric_errors = sum(1 for value in metric_samples if abs(value - expected_metric) > 0.10)
    else:
        metric_mid = 0.0
        metric_span = 0.0
        metric_stable = False
        metric_errors = 1

    notes = [
        _property_note(
            "P_RESET_DISABLE_CLEAR",
            clear_errors + int(len(reset_segments) < 2) + int(len(pure_disable_segments) < 2),
            "repeat_reset_and_disable_clear_outputs",
            (
                f"reset_segments={len(reset_segments)},disable_segments={len(pure_disable_segments)},"
                f"clear_errors={clear_errors}"
            ),
        ),
        _property_note(
            "P_PERIODIC_OSCILLATION",
            segment_errors + half_period_errors + int(len(edge_intervals) < 8),
            "multiple_edges_per_enabled_window_with_10ns_half_period",
            f"enabled_segments={len(enabled_segments)},edges={len(all_edges)},half_period_errors={half_period_errors}",
        ),
        _property_note(
            "P_VALID_AFTER_COMPLETE_CYCLE",
            valid_errors,
            "valid_low_before_first_complete_cycle_and_high_after",
            f"valid_errors={valid_errors}",
        ),
        _property_note(
            "P_RESTART_PHASE",
            restart_errors,
            "first_edge_restarts_one_half_period_after_each_enable",
            f"restart_errors={restart_errors}",
        ),
        _property_note(
            "P_PERIOD_METRIC",
            metric_errors + int(not metric_stable),
            "stable_metric_matches_measured_period",
            f"metric_mid={metric_mid:.3f},metric_span={metric_span:.3f},expected={expected_metric:.3f}",
        ),
        _property_note(
            "P_OSCILLATOR_LEVELS",
            int(not osc_high_seen) + int(not osc_low_seen),
            "osc_out_reaches_low_and_high",
            f"low={osc_low_seen},high={osc_high_seen}",
        ),
    ]
    ok = all("mismatch_count=0" in note for note in notes)
    return ok, "; ".join(notes)


CHECKER_ID = "v4_383_fixed_frequency_oscillator_source"
CHECKER: Checker = check_v4_942_fixed_frequency_oscillator_source
