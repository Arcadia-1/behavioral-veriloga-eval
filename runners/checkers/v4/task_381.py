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

def check_v4_940_fm_vco_modulation_source(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, _property_note("P_TRACE_CONTRACT", 1, "non_empty_trace", "empty_trace")
    checked = metric_errors = clear_errors = 0
    reset_clear = disabled_clear = low_metric = high_metric = osc_activity = marker_activity = valid_seen = False
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
        osc_vals.append(float(row["osc_out"]))
        marker_vals.append(float(row["phase_marker"]))
        metric_vals.append(float(row["freq_metric"]))
        valid_seen = valid_seen or bool(_level(row, "valid"))
        checked += 1
        if abs(float(row["freq_metric"]) - expected_metric) > 0.10:
            metric_errors += 1
    marker_alignment_errors = 0
    marker_rises = osc_rises = 0
    previous_osc_high = float(rows[0].get("osc_out", 0.0)) > 0.65
    previous_marker_high = float(rows[0].get("phase_marker", 0.0)) > 0.65
    for row in rows:
        rst = _level(row, "rst")
        enable = _level(row, "enable")
        if rst is None or enable is None:
            continue
        if not (enable and not rst):
            previous_osc_high = float(row["osc_out"]) > 0.65
            previous_marker_high = float(row["phase_marker"]) > 0.65
            continue
        osc_high = float(row["osc_out"]) > 0.65
        marker_high = float(row["phase_marker"]) > 0.65
        osc_rise = not previous_osc_high and osc_high
        marker_rise = not previous_marker_high and marker_high
        if osc_rise:
            osc_rises += 1
        if marker_rise:
            marker_rises += 1
            if not osc_rise:
                marker_alignment_errors += 1
        previous_osc_high = osc_high
        previous_marker_high = marker_high
    osc_activity = bool(osc_vals) and max(osc_vals) > 0.65 and min(osc_vals) < 0.20
    marker_activity = bool(marker_vals) and max(marker_vals) > 0.65 and min(marker_vals) < 0.20
    metric_span = (max(metric_vals) - min(metric_vals)) if metric_vals else 0.0
    coverage_errors = int(not low_metric) + int(not high_metric) + int(metric_span < 0.055)
    activity_errors = int(not osc_activity) + int(not marker_activity)
    alignment_errors = marker_alignment_errors + int(marker_rises == 0) + int(osc_rises == 0)
    ok = (
        checked >= 12
        and reset_clear
        and disabled_clear
        and coverage_errors == 0
        and activity_errors == 0
        and alignment_errors == 0
        and valid_seen
        and metric_errors <= 4
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
        _property_note("P_METRIC_COVERAGE", coverage_errors, "low_high_and_span", f"span={metric_span:.6g}"),
        _property_note("P_OSCILLATOR_ACTIVITY", int(not osc_activity), "osc_out_has_low_high_activity", str(osc_activity)),
        _property_note("P_PHASE_MARKER_ACTIVITY", int(not marker_activity), "phase_marker_has_low_high_activity", str(marker_activity)),
        _property_note("P_PHASE_MARKER_ALIGNMENT", alignment_errors, "marker_rise_aligned_with_osc_rise", f"marker_rises={marker_rises},osc_rises={osc_rises},misaligned={marker_alignment_errors}"),
        _property_note("P_VALID_AFTER_ENABLE", int(not valid_seen), "valid_asserted_when_active", str(valid_seen)),
    ]
    return ok, "; ".join(notes)

CHECKER_ID = "v4_381_fm_vco_modulation_source"
CHECKER: Checker = check_v4_940_fm_vco_modulation_source
