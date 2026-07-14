"""Task-specific checker for canonical v4 DUT 046."""
from __future__ import annotations

from checkers.api import Checker
def mean_in_window(rows: list[dict[str, float]], key: str, start: float, stop: float) -> float | None:
    values = [r[key] for r in rows if start <= r["time"] <= stop and key in r]
    if not values:
        return None
    return sum(values) / len(values)

def check_uvlo_brownout_detector(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "vin", "out", "metric"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/clk/rst/vin/out/metric"

    initial_low = mean_in_window(rows, "out", 5.0e-9, 9.0e-9)
    power_good = mean_in_window(rows, "out", 18.0e-9, 26.0e-9)
    hysteresis_hold = mean_in_window(rows, "out", 33.0e-9, 41.0e-9)
    brownout_low = mean_in_window(rows, "out", 48.0e-9, 53.0e-9)
    lower_threshold_hold = mean_in_window(rows, "out", 59.0e-9, 65.0e-9)
    recovered = mean_in_window(rows, "out", 72.0e-9, 78.0e-9)
    if None in (initial_low, power_good, hysteresis_hold, brownout_low, lower_threshold_hold, recovered):
        return False, "uvlo_missing_sample_windows"
    assert initial_low is not None
    assert power_good is not None
    assert hysteresis_hold is not None
    assert brownout_low is not None
    assert lower_threshold_hold is not None
    assert recovered is not None

    if initial_low > 0.20:
        return False, f"uvlo_initial_power_good_high={initial_low:.3f}"
    if power_good < 0.65 or hysteresis_hold < 0.65:
        return False, f"uvlo_hysteresis_hold_failed good={power_good:.3f} hold={hysteresis_hold:.3f}"
    if brownout_low > 0.20 or lower_threshold_hold > 0.20:
        return False, f"uvlo_brownout_or_lower_hold_failed brownout={brownout_low:.3f} hold={lower_threshold_hold:.3f}"
    if recovered < 0.65:
        return False, f"uvlo_not_recovered={recovered:.3f}"
    return True, (
        "uvlo_brownout_detector "
        f"pgood={power_good:.3f} hold={hysteresis_hold:.3f}/{lower_threshold_hold:.3f} "
        f"recover={recovered:.3f}"
    )

CHECKER_ID = "v4_046_uvlo_brownout_detector"
CHECKER: Checker = check_uvlo_brownout_detector
