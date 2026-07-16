"""Task-specific checker for canonical v4 DUT 046."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import diagnostic, pass_note, require_signals


PROPERTY_IDS = (
    "P_RESET_FAULT",
    "P_UPPER_TRIP_ASSERT",
    "P_HYSTERESIS_HOLD",
    "P_BROWNOUT_CLEAR",
    "P_STATUS_DISTINCTION",
)


def _mean(values: list[float]) -> float | None:
    return sum(values) / len(values) if values else None

def check_uvlo_brownout_detector(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "vin", "out", "metric"}
    missing = require_signals(rows, required, "P_UPPER_TRIP_ASSERT")
    if missing:
        return False, missing

    initial_values: list[float] = []
    power_good_values: list[float] = []
    hysteresis_values: list[float] = []
    brownout_values: list[float] = []
    lower_hold_values: list[float] = []
    recovered_values: list[float] = []
    seen_high = False
    seen_brownout = False
    for row in rows:
        if row["rst"] > 0.45:
            continue
        vin = row["vin"]
        if not seen_high:
            if vin <= 0.53:
                initial_values.append(row["out"])
                continue
            if vin >= 0.66:
                seen_high = True
                power_good_values.append(row["out"])
                continue
        elif not seen_brownout:
            if vin >= 0.66:
                power_good_values.append(row["out"])
                continue
            if 0.56 <= vin <= 0.60:
                hysteresis_values.append(row["out"])
                continue
            if vin <= 0.54:
                seen_brownout = True
                brownout_values.append(row["out"])
                continue
        else:
            if vin <= 0.54:
                brownout_values.append(row["out"])
                continue
            if 0.60 <= vin <= 0.64:
                lower_hold_values.append(row["out"])
                continue
            if vin >= 0.66:
                recovered_values.append(row["out"])

    initial_low = _mean(initial_values)
    power_good = _mean(power_good_values)
    hysteresis_hold = _mean(hysteresis_values)
    brownout_low = _mean(brownout_values)
    lower_threshold_hold = _mean(lower_hold_values)
    recovered = _mean(recovered_values)
    if None in (initial_low, power_good, hysteresis_hold, brownout_low, lower_threshold_hold, recovered):
        return False, diagnostic(
            "P_STATUS_DISTINCTION",
            "insufficient_excitation",
            expected="initial,upper,hysteresis,brownout,lower_hold,recovered_regions",
            observed=(
                f"initial={len(initial_values)},upper={len(power_good_values)},"
                f"hysteresis={len(hysteresis_values)},brownout={len(brownout_values)},"
                f"lower_hold={len(lower_hold_values)},recovered={len(recovered_values)}"
            ),
            event="observed_vin_sequence",
        )
    assert initial_low is not None
    assert power_good is not None
    assert hysteresis_hold is not None
    assert brownout_low is not None
    assert lower_threshold_hold is not None
    assert recovered is not None

    if initial_low > 0.20:
        return False, diagnostic(
            "P_RESET_FAULT",
            "behavior_mismatch",
            expected="initial_out<=0.20",
            observed=f"initial_out={initial_low:.3f}",
            event="pre_upper_trip_region",
        )
    if power_good < 0.65 or hysteresis_hold < 0.65:
        return False, diagnostic(
            "P_HYSTERESIS_HOLD",
            "behavior_mismatch",
            expected="power_good>=0.65,hysteresis_hold>=0.65",
            observed=f"power_good={power_good:.3f},hysteresis_hold={hysteresis_hold:.3f}",
            event="after_upper_trip_before_brownout",
        )
    if brownout_low > 0.20 or lower_threshold_hold > 0.20:
        return False, diagnostic(
            "P_BROWNOUT_CLEAR",
            "behavior_mismatch",
            expected="brownout<=0.20,lower_hold<=0.20",
            observed=f"brownout={brownout_low:.3f},lower_hold={lower_threshold_hold:.3f}",
            event="after_brownout_before_recovery",
        )
    if recovered < 0.65:
        return False, diagnostic(
            "P_UPPER_TRIP_ASSERT",
            "behavior_mismatch",
            expected="recovered>=0.65",
            observed=f"recovered={recovered:.3f}",
            event="second_upper_trip_region",
        )
    return True, pass_note(PROPERTY_IDS, (
        "uvlo_brownout_detector "
        f"pgood={power_good:.3f} hold={hysteresis_hold:.3f}/{lower_threshold_hold:.3f} "
        f"recover={recovered:.3f}"
    ))

CHECKER_ID = "v4_046_uvlo_brownout_detector"
CHECKER: Checker = check_uvlo_brownout_detector
