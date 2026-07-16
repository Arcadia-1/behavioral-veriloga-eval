"""Task-specific checker for canonical v4 DUT 111."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import crossings, diagnostic, max_signal_value, pass_note, require_signals, sample


PROPERTY_IDS = (
    "P_RISING_TRIP_CAPTURE",
    "P_FALLING_TRIP_CAPTURE",
    "P_HYSTERESIS_WIDTH_SIGN",
    "P_VALID_AFTER_BOTH_DIRECTIONS",
)


def check_v3_hysteresis_trip_characterizer(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin", "cmp_out", "trip_rise", "trip_fall", "hyst_width", "valid"}
    missing = require_signals(rows, required, "P_RISING_TRIP_CAPTURE")
    if missing:
        return False, missing

    vdd = max_signal_value(rows, ["cmp_out", "valid"], default=0.9)
    rises = crossings(rows, "cmp_out", threshold=0.5 * vdd, direction="rising")
    falls = crossings(rows, "cmp_out", threshold=0.5 * vdd, direction="falling")
    if len(rises) < 2 or len(falls) < 2:
        return False, diagnostic(
            "P_VALID_AFTER_BOTH_DIRECTIONS",
            "insufficient_events",
            expected="rise_count>=2,fall_count>=2",
            observed=f"rise_count={len(rises)},fall_count={len(falls)}",
            event="cmp_crossing_set",
        )

    rise_t = rises[-1]
    fall_t = falls[-1]
    expected_rise = sample(rows, "vin", rise_t)
    expected_fall = sample(rows, "vin", fall_t)
    final_t = rows[-1]["time"]
    trip_rise = sample(rows, "trip_rise", final_t)
    trip_fall = sample(rows, "trip_fall", final_t)
    hyst_width = sample(rows, "hyst_width", final_t)
    valid = sample(rows, "valid", final_t)
    if None in (expected_rise, expected_fall, trip_rise, trip_fall, hyst_width, valid):
        return False, diagnostic(
            "P_RISING_TRIP_CAPTURE",
            "missing_sample",
            expected="trip_rise,trip_fall,hyst_width,valid",
            observed="unavailable",
            event="final_observed_state",
        )

    assert expected_rise is not None
    assert expected_fall is not None
    assert trip_rise is not None
    assert trip_fall is not None
    assert hyst_width is not None
    assert valid is not None

    expected_width = expected_rise - expected_fall
    rise_err = abs(trip_rise - expected_rise)
    fall_err = abs(trip_fall - expected_fall)
    width_err = abs(hyst_width - expected_width)
    valid_ok = valid > 0.7 * vdd
    width_ok = expected_width > 0.015
    ok = valid_ok and width_ok and rise_err <= 0.004 and fall_err <= 0.004 and width_err <= 0.004
    detail = (
        f"rise_err={rise_err:.5f} fall_err={fall_err:.5f} "
        f"width_err={width_err:.5f} valid={valid_ok} width_positive={width_ok} "
        f"rise_events={len(rises)} fall_events={len(falls)}"
    )
    if not ok:
        return False, diagnostic(
            "P_HYSTERESIS_WIDTH_SIGN",
            "trip_measurement_mismatch",
            expected="rise_err<=0.004,fall_err<=0.004,width_err<=0.004,valid=True,width_positive=True",
            observed=detail,
            event="last_observed_trip_pair",
        )
    return True, pass_note(PROPERTY_IDS, detail)

CHECKER_ID = "v4_111_hysteresis_trip_characterizer"
CHECKER: Checker = check_v3_hysteresis_trip_characterizer
