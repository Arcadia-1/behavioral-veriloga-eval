"""Task-specific checker for canonical v4 DUT 381."""
from __future__ import annotations

from ..api import Checker


F0 = 10.0e6
KVCO = 5.0e6
VCM = 0.45
MIN_FREQUENCY = 1.0e6
VALID_TRANSITION_GRACE = 2.0e-9


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


def _mod_bucket(mod_in: float) -> str | None:
    if abs(mod_in - VCM) <= 0.05:
        return "nominal"
    if mod_in >= 0.70:
        return "high"
    if mod_in <= -1.0:
        return "clamp"
    return None


def _expected_period(mod_in: float) -> float:
    frequency = max(MIN_FREQUENCY, F0 + KVCO * (mod_in - VCM))
    return 1.0 / frequency


def _active_edge_times(
    rows: list[dict[str, float]], signal: str, *, rising_only: bool = False
) -> list[float]:
    edge_times: list[float] = []
    previous_high = _level(rows[0], signal)
    for row in rows[1:]:
        high = _level(row, signal)
        if high is None:
            continue
        edge = previous_high is not None and high != previous_high
        rising = previous_high is False and high is True
        previous_high = high
        if not edge or (rising_only and not rising):
            continue
        rst = _level(row, "rst")
        enable = _level(row, "enable")
        if rst is not None and enable is not None and enable and not rst:
            edge_times.append(float(row["time"]))
    return edge_times


def _period_samples(rows: list[dict[str, float]]) -> dict[str, list[tuple[float, float]]]:
    samples: dict[str, list[tuple[float, float]]] = {
        "nominal": [],
        "high": [],
        "clamp": [],
    }
    previous_marker_high = _level(rows[0], "phase_marker")
    previous_event: tuple[float, float, str, int] | None = None
    segment = 0
    was_active = False
    for row in rows[1:]:
        rst = _level(row, "rst")
        enable = _level(row, "enable")
        active = rst is not None and enable is not None and enable and not rst
        if active and not was_active:
            segment += 1
            previous_event = None
        if not active:
            previous_event = None
        was_active = active

        marker_high = _level(row, "phase_marker")
        if marker_high is None:
            continue
        marker_rise = previous_marker_high is False and marker_high is True
        previous_marker_high = marker_high
        if not active or not marker_rise:
            continue

        time = float(row["time"])
        mod_in = float(row["mod_in"])
        bucket = _mod_bucket(mod_in)
        if bucket is None:
            previous_event = None
            continue
        if previous_event is not None:
            previous_time, previous_mod, previous_bucket, previous_segment = previous_event
            if previous_bucket == bucket and previous_segment == segment:
                measured = time - previous_time
                expected = 0.5 * (_expected_period(previous_mod) + _expected_period(mod_in))
                if measured > 0.0:
                    samples[bucket].append((measured, expected))
        previous_event = (time, mod_in, bucket, segment)
    return samples


def check_v4_940_fm_vco_modulation_source(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, _property_note("P_TRACE_CONTRACT", 1, "non_empty_trace", "empty_trace")

    checked = metric_errors = clear_errors = lower_clamp_errors = 0
    reset_clear = disabled_clear = low_metric = high_metric = lower_clamp_seen = valid_seen = False
    osc_vals: list[float] = []
    marker_vals: list[float] = []
    metric_vals: list[float] = []
    for row in rows:
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
        freq = max(MIN_FREQUENCY, F0 + KVCO * (float(row["mod_in"]) - VCM))
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

    valid_early_errors = valid_hold_errors = valid_late_errors = 0
    active_segment_started = False
    first_cycle_time: float | None = None
    valid_high_after_grace = False
    previous_marker_high = _level(rows[0], "phase_marker")
    for row in rows:
        rst = _level(row, "rst")
        enable = _level(row, "enable")
        if rst is None or enable is None:
            continue
        active = enable and not rst
        marker_high = _level(row, "phase_marker")
        marker_rise = (
            marker_high is not None
            and previous_marker_high is False
            and marker_high is True
        )
        if marker_high is not None:
            previous_marker_high = marker_high
        if not active:
            if active_segment_started and first_cycle_time is not None and not valid_high_after_grace:
                valid_late_errors += 1
            active_segment_started = False
            first_cycle_time = None
            valid_high_after_grace = False
            continue
        if not active_segment_started:
            active_segment_started = True
            first_cycle_time = None
            valid_high_after_grace = False
        if marker_rise and first_cycle_time is None:
            first_cycle_time = float(row["time"])
        valid_high = _level(row, "valid")
        if valid_high is None:
            continue
        if first_cycle_time is None:
            valid_early_errors += int(valid_high)
            continue
        if float(row["time"]) - first_cycle_time <= VALID_TRANSITION_GRACE:
            continue
        if valid_high:
            valid_high_after_grace = True
        else:
            valid_hold_errors += 1
    if active_segment_started and first_cycle_time is not None and not valid_high_after_grace:
        valid_late_errors += 1

    osc_activity = bool(osc_vals) and max(osc_vals) > 0.65 and min(osc_vals) < 0.20
    marker_activity = bool(marker_vals) and max(marker_vals) > 0.65 and min(marker_vals) < 0.20
    metric_span = (max(metric_vals) - min(metric_vals)) if metric_vals else 0.0
    coverage_errors = int(not low_metric) + int(not high_metric) + int(not lower_clamp_seen) + int(metric_span < 0.055)
    activity_errors = int(not osc_activity) + int(not marker_activity)

    marker_edge_times = _active_edge_times(rows, "phase_marker", rising_only=True)
    osc_edge_times = _active_edge_times(rows, "osc_out")
    marker_alignment_errors = sum(
        1
        for marker_time in marker_edge_times
        if not osc_edge_times or min(abs(marker_time - osc_time) for osc_time in osc_edge_times) > 2.0e-9
    )
    alignment_errors = marker_alignment_errors + int(not marker_edge_times) + int(not osc_edge_times)

    period_samples = _period_samples(rows)
    measured_periods: dict[str, float | None] = {}
    expected_periods: dict[str, float | None] = {}
    period_scales: dict[str, float | None] = {}
    for bucket, samples in period_samples.items():
        if not samples:
            measured_periods[bucket] = expected_periods[bucket] = period_scales[bucket] = None
            continue
        measured = sum(sample[0] for sample in samples) / len(samples)
        expected = sum(sample[1] for sample in samples) / len(samples)
        measured_periods[bucket] = measured
        expected_periods[bucket] = expected
        period_scales[bucket] = measured / expected
    available_scales = [scale for scale in period_scales.values() if scale is not None]
    reference_scale = sum(available_scales) / len(available_scales) if available_scales else None
    period_model_errors = sum(scale is None for scale in period_scales.values())
    if reference_scale is not None:
        period_model_errors += sum(
            abs(scale / reference_scale - 1.0) > 0.18
            for scale in available_scales
        )
    nominal_period = measured_periods["nominal"]
    high_period = measured_periods["high"]
    clamp_period = measured_periods["clamp"]
    period_order_errors = int(
        nominal_period is None
        or high_period is None
        or clamp_period is None
        or not (high_period < nominal_period * 0.92 and clamp_period > nominal_period * 4.0)
    )

    valid_errors = valid_early_errors + valid_hold_errors + valid_late_errors + int(not valid_seen)
    ok = (
        checked >= 72
        and reset_clear
        and disabled_clear
        and coverage_errors == 0
        and activity_errors == 0
        and alignment_errors == 0
        and period_order_errors == 0
        and period_model_errors == 0
        and valid_errors == 0
        and metric_errors <= 24
        and lower_clamp_errors <= 18
        and clear_errors <= 24
    )
    notes = [
        _property_note(
            "P_RESET_DISABLE_CLEAR",
            max(0, clear_errors - 24) + int(not reset_clear) + int(not disabled_clear),
            "clear_on_reset_and_disable",
            f"reset_clear={reset_clear},disabled_clear={disabled_clear},raw_clear_errors={clear_errors}",
        ),
        _property_note("P_FREQUENCY_TRANSFER", max(0, metric_errors - 24), "freq_metric=f(mod_in)", f"checked={checked},raw_errors={metric_errors}"),
        _property_note("P_METRIC_COVERAGE", coverage_errors, "low_high_lower_clamp_and_span", f"span={metric_span:.6g},lower_clamp_seen={lower_clamp_seen}"),
        _property_note("P_LOWER_CLAMP", max(0, lower_clamp_errors - 18), "freq_metric_tracks_1MHz_lower_clamp", f"raw_errors={lower_clamp_errors}"),
        _property_note("P_OSCILLATOR_ACTIVITY", int(not osc_activity), "osc_out_has_low_high_activity", str(osc_activity)),
        _property_note("P_PHASE_MARKER_ACTIVITY", int(not marker_activity), "phase_marker_has_low_high_activity", str(marker_activity)),
        _property_note("P_PHASE_MARKER_ALIGNMENT", alignment_errors, "marker_rise_aligned_with_osc_edge", f"marker_rises={len(marker_edge_times)},osc_edges={len(osc_edge_times)},misaligned={marker_alignment_errors}"),
        _property_note("P_PERIOD_ORDERING", period_order_errors, "high_mod_period<nominal_period<clamp_period", f"high={high_period},nominal={nominal_period},clamp={clamp_period}"),
        _property_note("P_PERIOD_MODEL", period_model_errors, "measured_over_expected_period_scale_consistent_across_modulation", f"measured={measured_periods},expected={expected_periods},scales={period_scales}"),
        _property_note("P_VALID_AFTER_ENABLE", valid_errors, "valid_low_until_first_cycle_then_continuously_high", f"seen={valid_seen},early={valid_early_errors},hold={valid_hold_errors},late={valid_late_errors}"),
    ]
    return ok, "; ".join(notes)


CHECKER_ID = "v4_381_fm_vco_modulation_source"
CHECKER: Checker = check_v4_940_fm_vco_modulation_source
