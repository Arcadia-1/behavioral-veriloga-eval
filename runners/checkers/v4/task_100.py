"""Stimulus-relative checker for canonical v4 DUT 100."""
from __future__ import annotations

import math

from ..api import Checker
from .stimulus_relative import (
    PropertyResult,
    edge_times,
    finish,
    missing_trace,
    sample,
)


PROPERTY_IDS = [
    "P_APERTURE_CAPTURE",
    "P_SUPPLY_CLAMPED_SAMPLE",
    "P_COARSE_DECISION",
    "P_VALID_PULSE",
    "P_LOW_PHASE_DROOP",
    "P_NO_TRACK_THROUGH",
]
APERTURE_S = 200e-12
VALID_WIDTH_S = 2e-9
DROOP_TAU_S = 90e-9


def check_v4_sample_hold_droop_front_end(
    rows: list[dict[str, float]],
) -> tuple[bool, str]:
    required = {"time", "vdd", "vss", "vin", "clk", "vout", "valid", "coarse"}
    results, missing = missing_trace("v4_100", rows, required, PROPERTY_IDS)
    if missing is not None:
        return missing
    aperture, clamped, coarse_result, valid_result, droop_result, hold_result = results
    time_scale = float(rows[0].get("_time_scale", 1.0))
    aperture_delay = APERTURE_S * time_scale
    valid_width = VALID_WIDTH_S * time_scale
    droop_tau = DROOP_TAU_S * time_scale
    rises = edge_times(rows, "clk", threshold=0.45, rising=True)
    falls = edge_times(rows, "clk", threshold=0.45, rising=False)
    aperture_sensitive = 0
    sampled_below = sampled_above = 0
    clamp_events = 0

    for edge in rises:
        capture_time = edge + aperture_delay
        probe_time = capture_time + 0.20e-9 * time_scale
        low_time = capture_time + valid_width + 0.80e-9 * time_scale
        if low_time > rows[-1]["time"]:
            continue
        vin_edge = sample(rows, "vin", edge)
        vin_capture = sample(rows, "vin", capture_time)
        vdd = sample(rows, "vdd", capture_time)
        vss = sample(rows, "vss", capture_time)
        observed = sample(rows, "vout", probe_time)
        coarse = sample(rows, "coarse", probe_time)
        valid_high = sample(rows, "valid", probe_time)
        valid_low = sample(rows, "valid", low_time)
        if None in (vin_edge, vin_capture, vdd, vss, observed, coarse, valid_high, valid_low):
            continue
        assert vin_edge is not None and vin_capture is not None
        assert vdd is not None and vss is not None and observed is not None
        assert coarse is not None and valid_high is not None and valid_low is not None
        expected = min(vdd, max(vss, vin_capture))
        if vin_capture < vss or vin_capture > vdd:
            clamp_events += 1
        sampled_below += int(expected <= 0.45)
        sampled_above += int(expected > 0.45)
        if abs(vin_capture - vin_edge) > 0.12:
            aperture_sensitive += 1
        aperture.compare(
            expected=expected, observed=observed, tolerance=0.055,
            time_s=probe_time, label="aperture_vout",
        )
        clamped.compare(
            expected=expected, observed=observed, tolerance=0.055,
            time_s=probe_time, label="clamped_vout",
        )
        coarse_result.compare(
            expected=vdd if expected > 0.45 else vss,
            observed=coarse, tolerance=0.08,
            time_s=probe_time, label="coarse",
        )
        valid_result.compare(
            expected=vdd, observed=valid_high, tolerance=0.08,
            time_s=probe_time, label="valid_high",
        )
        valid_result.compare(
            expected=vss, observed=valid_low, tolerance=0.08,
            time_s=low_time, label="valid_low",
        )

    low_windows = 0
    for fall in falls:
        next_rise = next((rise for rise in rises if rise > fall), None)
        if next_rise is None or next_rise - fall < 3e-9:
            continue
        margin = min(0.5e-9 * time_scale, 0.05 * (next_rise - fall))
        start_time = fall + margin
        stop_time = next_rise - margin
        start = sample(rows, "vout", start_time)
        stop = sample(rows, "vout", stop_time)
        if start is None or stop is None or start < 0.10:
            continue
        expected_stop = start * math.exp(-(stop_time - start_time) / droop_tau)
        tolerance = max(0.035, 0.12 * start)
        droop_result.compare(
            expected=expected_stop, observed=stop, tolerance=tolerance,
            time_s=stop_time, label="drooped_vout",
        )
        hold_result.compare(
            expected=expected_stop, observed=stop, tolerance=tolerance,
            time_s=stop_time, label="held_not_tracking",
        )
        low_windows += 1

    aperture.condition(
        len(rises) >= 6 and aperture_sensitive >= 1,
        expected="rising_edges>=6_aperture_sensitive>=1",
        observed=f"rises={len(rises)}_aperture_sensitive={aperture_sensitive}",
        time_s=rows[-1]["time"],
    )
    coarse_result.condition(
        sampled_below >= 2 and sampled_above >= 2,
        expected="samples_below>=2_above>=2",
        observed=f"below={sampled_below}_above={sampled_above}",
        time_s=rows[-1]["time"],
    )
    droop_result.condition(
        low_windows >= 2,
        expected="droop_windows>=2",
        observed=f"droop_windows={low_windows}",
        time_s=rows[-1]["time"],
    )
    return finish(
        "v4_100",
        results,
        coverage=(
            f"rises={len(rises)} falls={len(falls)} aperture_sensitive={aperture_sensitive} "
            f"below={sampled_below} above={sampled_above} clamps={clamp_events} "
            f"droop_windows={low_windows}"
        ),
    )


CHECKER_ID = "v4_100_sample_hold_droop_front_end"
CHECKER: Checker = check_v4_sample_hold_droop_front_end
