"""Task-specific checker for canonical v4 DUT 082."""
from __future__ import annotations

from checkers.api import Checker
def mean_in_window(rows: list[dict[str, float]], key: str, start: float, stop: float) -> float | None:
    values = [r[key] for r in rows if start <= r["time"] <= stop and key in r]
    if not values:
        return None
    return sum(values) / len(values)

def check_agc_receiver_leveling_loop(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "vin", "out", "metric", "gain_mon", "rssi_mon"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/clk/rst/vin/out/metric/gain_mon/rssi_mon"

    def amp_mean(start: float, stop: float) -> float | None:
        val = mean_in_window(rows, "out", start, stop)
        if val is None:
            return None
        return abs(val - 0.45)

    low_amp = amp_mean(12.0e-9, 20.0e-9)
    overload_amp = amp_mean(24.0e-9, 30.0e-9)
    settled_amp = amp_mean(44.0e-9, 54.0e-9)
    settled_metric = mean_in_window(rows, "metric", 44.0e-9, 54.0e-9)
    low_gain = mean_in_window(rows, "gain_mon", 12.0e-9, 20.0e-9)
    settled_gain = mean_in_window(rows, "gain_mon", 44.0e-9, 54.0e-9)
    low_rssi = mean_in_window(rows, "rssi_mon", 12.0e-9, 20.0e-9)
    overload_rssi = mean_in_window(rows, "rssi_mon", 24.0e-9, 30.0e-9)
    settled_rssi = mean_in_window(rows, "rssi_mon", 44.0e-9, 54.0e-9)
    if None in (low_amp, overload_amp, settled_amp, settled_metric, low_gain, settled_gain, low_rssi, overload_rssi, settled_rssi):
        return False, "agc_missing_sample_windows"
    assert low_amp is not None
    assert overload_amp is not None
    assert settled_amp is not None
    assert settled_metric is not None
    assert low_gain is not None
    assert settled_gain is not None
    assert low_rssi is not None
    assert overload_rssi is not None
    assert settled_rssi is not None

    if overload_amp <= settled_amp + 0.08:
        return False, f"agc_gain_not_reduced overload={overload_amp:.3f} settled={settled_amp:.3f}"
    if not (0.10 <= settled_amp <= 0.24):
        return False, f"agc_settled_amplitude_wrong={settled_amp:.3f}"
    if low_amp < 0.08:
        return False, f"agc_low_input_not_amplified={low_amp:.3f}"
    if settled_metric < 0.45:
        return False, f"agc_lock_metric_low={settled_metric:.3f}"
    if overload_rssi <= low_rssi + 0.20 or overload_rssi <= settled_rssi + 0.15:
        return False, (
            f"agc_rssi_monitor_not_overload_sensitive low/overload/settled="
            f"{low_rssi:.3f}/{overload_rssi:.3f}/{settled_rssi:.3f}"
        )
    if settled_gain >= low_gain - 0.10:
        return False, f"agc_gain_monitor_not_reduced low={low_gain:.3f} settled={settled_gain:.3f}"
    return True, (
        f"agc_receiver_leveling_loop amp_low/overload/settled={low_amp:.3f}/{overload_amp:.3f}/{settled_amp:.3f} "
        f"gain={low_gain:.3f}->{settled_gain:.3f} rssi={low_rssi:.3f}/{overload_rssi:.3f}/{settled_rssi:.3f}"
    )

CHECKER_ID = "v4_082_agc_receiver_leveling_loop"
CHECKER: Checker = check_agc_receiver_leveling_loop
