"""Task-specific checker for canonical v4 DUT 304."""
from __future__ import annotations

from ..api import Checker
from ..common.v4_topup import (
    _v4_topup_clip01,
    _v4_topup_logic_high,
    _v4_topup_near,
)
from ..common.relative_events import active_start, first_disable

def check_v4_304_common_gate_tia_front_end(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_1002 empty_trace"
    checked = gain_errors = polarity_errors = metric_errors = overload_errors = 0
    high_bias_seen = low_bias_seen = overload_seen = disabled_clear = False
    rz_gain = 3.0
    bias_min = 0.3
    activation = active_start(rows, enable="enable", reset="rst")
    disable = first_disable(rows, "enable", activation)
    for row in rows:
        t = float(row["time"])
        if t < activation:
            continue
        enabled = _v4_topup_logic_high(row, "enable") and not _v4_topup_logic_high(row, "rst")
        if not enabled:
            if (disable is None or t >= disable) and _v4_topup_near(row["vout"], 0.45, 0.08) and row["transimpedance_metric"] < 0.15 and row["overload"] < 0.15:
                disabled_clear = True
            continue
        gain_scale = _v4_topup_clip01((float(row["bias"]) - bias_min) / (0.45 - bias_min))
        if gain_scale < 0.35:
            gain_scale = 0.35
        effective_gain = rz_gain * gain_scale
        raw_target = 0.45 + effective_gain * (float(row["vin_proxy"]) - 0.45)
        expected_vout = _v4_topup_clip01(raw_target)
        expected_metric = _v4_topup_clip01(0.9 * effective_gain / rz_gain)
        expected_overload = raw_target > 0.9 or raw_target < 0.0
        checked += 1
        high_bias_seen = high_bias_seen or float(row["bias"]) > 0.55
        low_bias_seen = low_bias_seen or float(row["bias"]) < 0.32
        overload_seen = overload_seen or expected_overload
        if (float(row["vin_proxy"]) - 0.45) * (float(row["vout"]) - 0.45) < -0.01:
            polarity_errors += 1
        if abs(float(row["vout"]) - expected_vout) > 0.14:
            gain_errors += 1
        if abs(float(row["transimpedance_metric"]) - expected_metric) > 0.18:
            metric_errors += 1
        if (float(row["overload"]) > 0.45) != expected_overload:
            overload_errors += 1
    ok = (
        checked >= 8
        and high_bias_seen
        and low_bias_seen
        and overload_seen
        and disabled_clear
        and polarity_errors <= max(6, checked // 80)
        and gain_errors <= max(16, checked // 25)
        and metric_errors <= max(16, checked // 25)
        and overload_errors <= max(20, checked // 20)
    )
    diagnostics = {
        "P_ON_RESET_OR_WHEN_DISABLED_DRIVE": int(not disabled_clear),
        "P_TREAT_VIN_PROXY_AS_A_VOLTAGE": int(polarity_errors > max(6, checked // 80)),
        "P_GENERATE_AN_OUTPUT_DEVIATION_AROUND_VCM": int(gain_errors > max(16, checked // 25)),
        "P_REDUCE_EFFECTIVE_GAIN_WHEN_BIAS_FALLS": int(not (high_bias_seen and low_bias_seen)),
        "P_ASSERT_OVERLOAD_WHEN_THE_UNCLAMPED_OUTPUT": int(overload_errors > max(20, checked // 20)),
        "P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE": 0,
    }
    return ok, (
        f"v4_304 checked={checked} high_bias={high_bias_seen} low_bias={low_bias_seen} "
        f"overload={overload_seen} disabled_clear={disabled_clear} polarity_errors={polarity_errors} "
        f"gain_errors={gain_errors} metric_errors={metric_errors} overload_errors={overload_errors}; "
        + "; ".join(f"{key} mismatch_count={value}" for key, value in diagnostics.items())
    )

CHECKER_ID = "v4_304_common_gate_tia_front_end"
CHECKER: Checker = check_v4_304_common_gate_tia_front_end
