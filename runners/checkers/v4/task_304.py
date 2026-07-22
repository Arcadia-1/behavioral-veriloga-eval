"""Task-specific checker for canonical v4 DUT 304."""
from __future__ import annotations

from ..api import Checker
from ..common.v4_topup import (
    _v4_topup_clip01,
    _v4_topup_near,
)
from .trace_utils import sample_signal


_NOMINAL_STOP = 78e-9
_TICK = 500e-12
_PROBE_OFFSETS = (300e-12, 450e-12)


def _timer_events(rows: list[dict[str, float]]) -> list[tuple[float, tuple[float, ...]]]:
    start = float(rows[0]["time"])
    stop = float(rows[-1]["time"])
    duration = stop - start
    if duration <= 0.0:
        return []

    scale = duration / _NOMINAL_STOP
    tick = _TICK * scale
    offsets = tuple(offset * scale for offset in _PROBE_OFFSETS)
    events: list[tuple[float, tuple[float, ...]]] = []
    index = 0
    while True:
        event_time = start + index * tick
        probes = tuple(event_time + offset for offset in offsets)
        if not probes or probes[-1] > stop + tick * 1e-6:
            break
        events.append((event_time, probes))
        index += 1
    return events

def check_v4_304_common_gate_tia_front_end(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_1002 empty_trace"
    checked = hold_checked = gain_errors = polarity_errors = metric_errors = overload_errors = 0
    inactive_checked = inactive_errors = 0
    high_bias_seen = low_bias_seen = overload_seen = False
    active_seen = disable_seen = False
    rz_gain = 3.0
    bias_min = 0.3
    for event_time, probe_times in _timer_events(rows):
        enable = sample_signal(rows, "enable", event_time)
        rst = sample_signal(rows, "rst", event_time)
        vin_proxy = sample_signal(rows, "vin_proxy", event_time)
        bias = sample_signal(rows, "bias", event_time)
        if None in (enable, rst, vin_proxy, bias):
            continue
        enabled = enable > 0.45 and rst <= 0.45
        disable_seen = disable_seen or (active_seen and not enabled)
        if not enabled:
            inactive_checked += 1
            event_bad = False
            for probe_time in probe_times:
                vout = sample_signal(rows, "vout", probe_time)
                metric = sample_signal(rows, "transimpedance_metric", probe_time)
                overload = sample_signal(rows, "overload", probe_time)
                if None in (vout, metric, overload):
                    event_bad = True
                    continue
                hold_checked += 1
                if not (
                    _v4_topup_near(vout, 0.45, 0.08)
                    and metric < 0.15
                    and overload < 0.15
                ):
                    event_bad = True
            inactive_errors += int(event_bad)
            continue
        active_seen = True
        gain_scale = _v4_topup_clip01((bias - bias_min) / (0.45 - bias_min))
        if gain_scale < 0.35:
            gain_scale = 0.35
        effective_gain = rz_gain * gain_scale
        raw_target = 0.45 + effective_gain * (vin_proxy - 0.45)
        expected_vout = _v4_topup_clip01(raw_target)
        expected_metric = _v4_topup_clip01(0.9 * effective_gain / rz_gain)
        expected_overload = raw_target > 0.9 or raw_target < 0.0
        checked += 1
        high_bias_seen = high_bias_seen or bias > 0.55
        low_bias_seen = low_bias_seen or bias < 0.32
        overload_seen = overload_seen or expected_overload
        polarity_bad = gain_bad = metric_bad = overload_bad = False
        for probe_time in probe_times:
            vout = sample_signal(rows, "vout", probe_time)
            metric = sample_signal(rows, "transimpedance_metric", probe_time)
            overload = sample_signal(rows, "overload", probe_time)
            if None in (vout, metric, overload):
                polarity_bad = gain_bad = metric_bad = overload_bad = True
                continue
            hold_checked += 1
            if (vin_proxy - 0.45) * (vout - 0.45) < -0.01:
                polarity_bad = True
            if abs(vout - expected_vout) > 0.14:
                gain_bad = True
            if abs(metric - expected_metric) > 0.18:
                metric_bad = True
            if (overload > 0.45) != expected_overload:
                overload_bad = True
        polarity_errors += int(polarity_bad)
        gain_errors += int(gain_bad)
        metric_errors += int(metric_bad)
        overload_errors += int(overload_bad)
    ok = (
        checked >= 8
        and high_bias_seen
        and low_bias_seen
        and overload_seen
        and disable_seen
        and inactive_checked >= 8
        and inactive_errors == 0
        and polarity_errors == 0
        and gain_errors == 0
        and metric_errors == 0
        and overload_errors == 0
    )
    diagnostics = {
        "P_ON_RESET_OR_WHEN_DISABLED_DRIVE": max(
            int(not disable_seen or inactive_checked < 8),
            inactive_errors,
        ),
        "P_TREAT_VIN_PROXY_AS_A_VOLTAGE": polarity_errors,
        "P_GENERATE_AN_OUTPUT_DEVIATION_AROUND_VCM": gain_errors,
        "P_REDUCE_EFFECTIVE_GAIN_WHEN_BIAS_FALLS": int(not (high_bias_seen and low_bias_seen)),
        "P_ASSERT_OVERLOAD_WHEN_THE_UNCLAMPED_OUTPUT": overload_errors,
        "P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE": 0,
    }
    return ok, (
        f"v4_304 checked_events={checked} hold_probes={hold_checked} high_bias={high_bias_seen} low_bias={low_bias_seen} "
        f"overload={overload_seen} disable_seen={disable_seen} inactive_checked={inactive_checked} "
        f"inactive_errors={inactive_errors} polarity_errors={polarity_errors} "
        f"gain_errors={gain_errors} metric_errors={metric_errors} overload_errors={overload_errors}; "
        + "; ".join(f"{key} mismatch_count={value}" for key, value in diagnostics.items())
    )

CHECKER_ID = "v4_304_common_gate_tia_front_end"
CHECKER: Checker = check_v4_304_common_gate_tia_front_end
