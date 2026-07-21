"""Task-specific checker for canonical v4 DUT 381."""
from __future__ import annotations

from ..api import Checker


def _level(row: dict[str, float], name: str, threshold: float = 0.45) -> bool | None:
    value = float(row.get(name, 0.0))
    if 0.1 < value < 0.8:
        return None
    return value > threshold


def _property_note(property_id: str, mismatch_count: int, expected: str, observed: str) -> str:
    return (
        f"{property_id} mismatch_count={mismatch_count} "
        f"expected={expected} observed={observed}"
    )


def _mean_period(edge_times: list[float]) -> float | None:
    if len(edge_times) < 2:
        return None
    periods = [b - a for a, b in zip(edge_times, edge_times[1:])]
    return sum(periods) / len(periods)


def _period_for_mod_bucket(rows: list[dict[str, float]], bucket: str) -> float | None:
    edge_times: list[float] = []
    previous_marker_high = _level(rows[0], "phase_marker")
    for row in rows:
        marker_high = _level(row, "phase_marker")
        if marker_high is None:
            continue
        marker_edge = previous_marker_high is not None and marker_high != previous_marker_high
        previous_marker_high = marker_high
        if not marker_edge:
            continue
        rst = _level(row, "rst")
        enable = _level(row, "enable")
        if rst is None or enable is None or not (enable and not rst):
            continue
        mod_in = float(row["mod_in"])
        if bucket == "nominal" and abs(mod_in - 0.45) <= 0.05:
            edge_times.append(float(row["time"]))
        elif bucket == "high" and mod_in >= 0.70:
            edge_times.append(float(row["time"]))
        elif bucket == "clamp" and mod_in <= -1.0:
            edge_times.append(float(row["time"]))
    return _mean_period(edge_times)


def _active_edge_times(rows: list[dict[str, float]], signal: str) -> list[float]:
    edge_times: list[float] = []
    previous_high = _level(rows[0], signal)
    for row in rows:
        high = _level(row, signal)
        if high is None:
            continue
        edge = previous_high is not None and high != previous_high
        previous_high = high
        if not edge:
            continue
        rst = _level(row, "rst")
        enable = _level(row, "enable")
        if rst is not None and enable is not None and enable and not rst:
            edge_times.append(float(row["time"]))
    return edge_times


def check_v4_940_fm_vco_modulation_source(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, _property_note("P_TRACE_CONTRACT", 1, "non_empty_trace", "empty_trace")
    checked = metric_errors = clear_errors = lower_clamp_errors = valid_early_errors = valid_late_errors = 0
    reset_clear = disabled_clear = low_metric = high_metric = lower_clamp_seen = osc_activity = marker_activity = valid_seen = False
    osc_vals: list[float] = []
    marker_vals: list[float] = []
    metric_vals: list[float] = []
    for row in rows[::6]:
        rst = _level(row, "rst")
        enable = _level(row, "enable")
        if rst is None or enable is None:
            continue
        enabled = enable and not rst
        if not enabled:
            clear = row["osc_out"] < 0.12 and row["freq_metric"] < 0.08 and row["phase_marker"] < 0.12 and row["valid"] < 0.10
            if rst and clear:
                reset_clear = True
            if not rst and not enable and clear:
                disabled_clear = True
            if clear is False:
                clear_errors += 1
            continue
        freq = max(1.0e6, 10.0e6 + 5.0e6 * (float(row["mod_in"]) - 0.45))
        expected_metric = min(0.9, max(0.0, freq / 20.0e6 * 0.9))
        low_metric = low_metric or expected_metric < 0.45
        high_metric = high_metric or expected_metric > 0.45
        if expected_metric <= 0.06:
            lower_clamp_seen = True
            if abs(float(row["freq_metric"]) - expected_metric) > 0.025:
                lower_clamp_errors += 1
        osc_vals.append(float(row["osc_out"]))
        marker_vals.append(float(row["phase_marker"]))
        metric_vals.append(float(row["freq_metric"]))
        valid_seen = valid_seen or bool(_level(row, "valid"))
        checked += 1
        if abs(float(row["freq_metric"]) - expected_metric) > 0.10:
            metric_errors += 1
    marker_alignment_errors = 0
    marker_edges = osc_edges = 0
    previous_osc_high = float(rows[0].get("osc_out", 0.0)) > 0.65
    previous_marker_high = float(rows[0].get("phase_marker", 0.0)) > 0.65
    active_segment_started = False
    cycle_seen_in_segment = False
    valid_seen_after_cycle = False
    for row in rows:
        rst = _level(row, "rst")
        enable = _level(row, "enable")
        if rst is None or enable is None:
            continue
        if not (enable and not rst):
            previous_osc_high = float(row["osc_out"]) > 0.65
            previous_marker_high = float(row["phase_marker"]) > 0.65
            if active_segment_started and cycle_seen_in_segment and not valid_seen_after_cycle:
                valid_late_errors += 1
            active_segment_started = False
            cycle_seen_in_segment = False
            valid_seen_after_cycle = False
            continue
        if not active_segment_started:
            active_segment_started = True
            cycle_seen_in_segment = False
            valid_seen_after_cycle = False
        osc_high = float(row["osc_out"]) > 0.65
        marker_high = float(row["phase_marker"]) > 0.65
        osc_edge = previous_osc_high != osc_high
        marker_edge = previous_marker_high != marker_high
        if osc_edge:
            osc_edges += 1
        if marker_edge:
            marker_edges += 1
            cycle_seen_in_segment = True
            if not osc_edge:
                marker_alignment_errors += 1
        valid_high = _level(row, "valid")
        if valid_high and not cycle_seen_in_segment:
            valid_early_errors += 1
        if cycle_seen_in_segment and valid_high:
            valid_seen_after_cycle = True
        previous_osc_high = osc_high
        previous_marker_high = marker_high
    if active_segment_started and cycle_seen_in_segment and not valid_seen_after_cycle:
        valid_late_errors += 1
    osc_activity = bool(osc_vals) and max(osc_vals) > 0.65 and min(osc_vals) < 0.20
    marker_activity = bool(marker_vals) and max(marker_vals) > 0.65 and min(marker_vals) < 0.20
    metric_span = (max(metric_vals) - min(metric_vals)) if metric_vals else 0.0
    coverage_errors = int(not low_metric) + int(not high_metric) + int(not lower_clamp_seen) + int(metric_span < 0.055)
    activity_errors = int(not osc_activity) + int(not marker_activity)
    marker_edge_times = _active_edge_times(rows, "phase_marker")
    osc_edge_times = _active_edge_times(rows, "osc_out")
    marker_edges = len(marker_edge_times)
    osc_edges = len(osc_edge_times)
    marker_alignment_errors = sum(
        1
        for marker_time in marker_edge_times
        if not osc_edge_times or min(abs(marker_time - osc_time) for osc_time in osc_edge_times) > 2.0e-9
    )
    alignment_errors = marker_alignment_errors + int(marker_edges == 0) + int(osc_edges == 0)
    nominal_period = _period_for_mod_bucket(rows, "nominal")
    high_period = _period_for_mod_bucket(rows, "high")
    clamp_period = _period_for_mod_bucket(rows, "clamp")
    period_order_errors = 0
    if nominal_period is None or high_period is None or clamp_period is None:
        period_order_errors += 1
    else:
        period_order_errors += int(not (high_period < nominal_period * 0.92))
        period_order_errors += int(not (clamp_period > nominal_period * 4.0))
    valid_errors = valid_early_errors + valid_late_errors + int(not valid_seen)
    ok = (
        checked >= 12
        and reset_clear
        and disabled_clear
        and coverage_errors == 0
        and activity_errors == 0
        and alignment_errors == 0
        and period_order_errors == 0
        and valid_errors == 0
        and metric_errors <= 4
        and lower_clamp_errors <= 3
        and clear_errors <= 4
    )
    notes = [
        _property_note(
            "P_RESET_DISABLE_CLEAR",
            max(0, clear_errors - 4) + int(not reset_clear) + int(not disabled_clear),
            "clear_on_reset_and_disable",
            f"reset_clear={reset_clear},disabled_clear={disabled_clear},raw_clear_errors={clear_errors}",
        ),
        _property_note("P_FREQUENCY_TRANSFER", max(0, metric_errors - 4), "freq_metric=f(mod_in)", f"checked={checked},raw_errors={metric_errors}"),
        _property_note("P_METRIC_COVERAGE", coverage_errors, "low_high_lower_clamp_and_span", f"span={metric_span:.6g},lower_clamp_seen={lower_clamp_seen}"),
        _property_note("P_LOWER_CLAMP", max(0, lower_clamp_errors - 3), "freq_metric_tracks_1MHz_lower_clamp", f"raw_errors={lower_clamp_errors}"),
        _property_note("P_OSCILLATOR_ACTIVITY", int(not osc_activity), "osc_out_has_low_high_activity", str(osc_activity)),
        _property_note("P_PHASE_MARKER_ACTIVITY", int(not marker_activity), "phase_marker_has_low_high_activity", str(marker_activity)),
        _property_note("P_PHASE_MARKER_ALIGNMENT", alignment_errors, "marker_edge_aligned_with_osc_edge", f"marker_edges={marker_edges},osc_edges={osc_edges},misaligned={marker_alignment_errors}"),
        _property_note("P_PERIOD_ORDERING", period_order_errors, "high_mod_period<nominal_period<clamp_period", f"high={high_period},nominal={nominal_period},clamp={clamp_period}"),
        _property_note("P_VALID_AFTER_ENABLE", valid_errors, "valid_low_until_first_cycle_then_asserted", f"seen={valid_seen},early={valid_early_errors},late={valid_late_errors}"),
    ]
    return ok, "; ".join(notes)

CHECKER_ID = "v4_381_fm_vco_modulation_source"
CHECKER: Checker = check_v4_940_fm_vco_modulation_source
