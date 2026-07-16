"""Task-specific checker for canonical v4 DUT 082."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import crossings, diagnostic, event_label, pass_note, require_signals


PROPERTY_IDS = [
    "P_RESET_STATE",
    "P_CLOCKED_GAIN_LOOP",
    "P_OUTPUT_ENVELOPE",
    "P_GAIN_DIRECTION_AND_BOUNDS",
    "P_DEADBAND_HOLD",
    "P_SETTLING_METRIC",
]


def mean_value(rows: list[dict[str, float]], key: str) -> float | None:
    values = [r[key] for r in rows if key in r]
    if not values:
        return None
    return sum(values) / len(values)


def trimmed_region(rows: list[dict[str, float]], start_fraction: float = 0.25) -> list[dict[str, float]]:
    if len(rows) < 4:
        return rows
    start = min(len(rows) - 1, max(0, int(len(rows) * start_fraction)))
    stop = max(start + 1, int(len(rows) * 0.95))
    return rows[start:stop]


def check_agc_receiver_leveling_loop(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "vin", "out", "metric", "gain_mon", "rssi_mon"}
    missing = require_signals(rows, required, "P_RESET_STATE")
    if missing:
        return False, missing

    reset_releases = crossings(rows, "rst", threshold=0.45, direction="falling")
    release_t = reset_releases[0] if reset_releases else rows[0]["time"]
    active_rows = [row for row in rows if row["time"] >= release_t and row["rst"] <= 0.45]
    overload_rows = [row for row in active_rows if row["vin"] >= 0.65]
    if len(active_rows) < 10 or len(overload_rows) < 4:
        return False, diagnostic(
            "P_CLOCKED_GAIN_LOOP",
            "invalid_trace",
            expected="post_reset_low_and_overload_input_regions",
            observed=f"active_rows={len(active_rows)},overload_rows={len(overload_rows)}",
            event=event_label("reset_release", 0, release_t),
        )

    overload_start = overload_rows[0]["time"]
    overload_stop = overload_rows[-1]["time"]
    low_rows = [
        row
        for row in active_rows
        if row["time"] < overload_start and 0.49 <= row["vin"] <= 0.62
    ]
    settled_rows = [
        row
        for row in active_rows
        if row["time"] > overload_stop and 0.49 <= row["vin"] <= 0.62
    ]
    low_rows = trimmed_region(low_rows)
    overload_rows = trimmed_region(overload_rows)
    settled_rows = trimmed_region(settled_rows)
    if len(low_rows) < 4 or len(overload_rows) < 4 or len(settled_rows) < 4:
        return False, diagnostic(
            "P_OUTPUT_ENVELOPE",
            "invalid_trace",
            expected="observable_low_overload_settled_regions",
            observed=f"low={len(low_rows)},overload={len(overload_rows)},settled={len(settled_rows)}",
            event=event_label("overload", 0, overload_start),
        )

    def amp_mean(region: list[dict[str, float]]) -> float | None:
        val = mean_value(region, "out")
        if val is None:
            return None
        return abs(val - 0.45)

    low_amp = amp_mean(low_rows)
    overload_amp = amp_mean(overload_rows)
    settled_amp = amp_mean(settled_rows)
    settled_metric = mean_value(settled_rows, "metric")
    low_gain = mean_value(low_rows, "gain_mon")
    settled_gain = mean_value(settled_rows, "gain_mon")
    low_rssi = mean_value(low_rows, "rssi_mon")
    overload_rssi = mean_value(overload_rows, "rssi_mon")
    settled_rssi = mean_value(settled_rows, "rssi_mon")
    if None in (low_amp, overload_amp, settled_amp, settled_metric, low_gain, settled_gain, low_rssi, overload_rssi, settled_rssi):
        return False, diagnostic(
            "P_OUTPUT_ENVELOPE",
            "invalid_trace",
            expected="complete_observable_region_metrics",
            observed="missing_metric_sample",
            event=event_label("overload", 0, overload_start),
        )
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
        return False, diagnostic(
            "P_GAIN_DIRECTION_AND_BOUNDS",
            "behavior_mismatch",
            expected="overload_amplitude>settled_amplitude+0.08",
            observed=f"overload={overload_amp:.3f},settled={settled_amp:.3f}",
            event=event_label("post_overload", 0, overload_stop),
        )
    if not (0.10 <= settled_amp <= 0.24):
        return False, diagnostic(
            "P_OUTPUT_ENVELOPE",
            "behavior_mismatch",
            expected="0.10<=settled_amplitude<=0.24",
            observed=f"settled={settled_amp:.3f}",
            event=event_label("settled_region", 0, settled_rows[0]["time"]),
        )
    if low_amp < 0.08:
        return False, diagnostic(
            "P_OUTPUT_ENVELOPE",
            "behavior_mismatch",
            expected="low_input_amplitude>=0.08",
            observed=f"low={low_amp:.3f}",
            event=event_label("low_input", 0, low_rows[0]["time"]),
        )
    if settled_metric < 0.45:
        return False, diagnostic(
            "P_SETTLING_METRIC",
            "behavior_mismatch",
            expected="settled_metric>=0.45",
            observed=f"settled_metric={settled_metric:.3f}",
            event=event_label("settled_region", 0, settled_rows[0]["time"]),
        )
    if overload_rssi <= low_rssi + 0.20 or overload_rssi <= settled_rssi + 0.15:
        return False, diagnostic(
            "P_CLOCKED_GAIN_LOOP",
            "behavior_mismatch",
            expected="overload_rssi>low_rssi+0.20_and_overload_rssi>settled_rssi+0.15",
            observed=f"low={low_rssi:.3f},overload={overload_rssi:.3f},settled={settled_rssi:.3f}",
            event=event_label("overload", 0, overload_start),
        )
    if settled_gain >= low_gain - 0.10:
        return False, diagnostic(
            "P_GAIN_DIRECTION_AND_BOUNDS",
            "behavior_mismatch",
            expected="settled_gain<low_gain-0.10",
            observed=f"low={low_gain:.3f},settled={settled_gain:.3f}",
            event=event_label("settled_region", 0, settled_rows[0]["time"]),
        )
    return True, pass_note(
        PROPERTY_IDS,
        f"agc_receiver_leveling_loop amp_low/overload/settled={low_amp:.3f}/{overload_amp:.3f}/{settled_amp:.3f} "
        f"gain={low_gain:.3f}->{settled_gain:.3f} rssi={low_rssi:.3f}/{overload_rssi:.3f}/{settled_rssi:.3f}"
    )

CHECKER_ID = "v4_082_agc_receiver_leveling_loop"
CHECKER: Checker = check_agc_receiver_leveling_loop
