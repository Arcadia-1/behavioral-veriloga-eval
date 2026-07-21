"""Task-specific checker for canonical v4 DUT 303."""
from __future__ import annotations

from ..api import Checker
from ..common.v4_topup import (
    _v4_topup_logic_high,
    _v4_topup_near,
)
from ..common.relative_events import active_start, first_disable
from ..common.relative_events import sample_step

def check_v4_303_differential_pair_gm_limiter(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_1001 empty_trace"
    checked = polarity_errors = gain_errors = flag_errors = metric_errors = 0
    inactive_checked = inactive_errors = 0
    pos_seen = neg_seen = compressed_seen = False
    gm_gain = 4.0
    diff_limit = 120e-3
    activation = active_start(rows, enable="enable")
    disable = first_disable(rows, "enable", activation)
    guard = max(sample_step(rows) * 8.0, 0.0)
    previous_enabled = _v4_topup_logic_high(rows[0], "enable")
    control_change = float(rows[0]["time"])
    for row in rows:
        t = float(row["time"])
        enabled = _v4_topup_logic_high(row, "enable")
        if enabled != previous_enabled:
            previous_enabled = enabled
            control_change = t
        if not enabled:
            if t - control_change >= guard:
                inactive_checked += 1
                if not (
                    _v4_topup_near(row["voutp"], 0.45, 0.08)
                    and _v4_topup_near(row["voutn"], 0.45, 0.08)
                    and row["gm_metric"] < 0.12
                    and row["limit_flag"] < 0.12
                ):
                    inactive_errors += 1
            continue
        if t < activation:
            continue
        diff = float(row["vinp"]) - float(row["vinn"])
        if abs(diff) < 0.025:
            continue
        limited = diff / (1.0 + abs(diff) / diff_limit)
        sep_expected = gm_gain * limited
        sep_observed = float(row["voutp"]) - float(row["voutn"])
        gm_expected = 0.9 * diff_limit / (diff_limit + abs(diff))
        flag_expected_high = abs(diff) > diff_limit
        checked += 1
        pos_seen = pos_seen or diff > 0.0
        neg_seen = neg_seen or diff < 0.0
        compressed_seen = compressed_seen or flag_expected_high
        if sep_expected * sep_observed <= 0.0:
            polarity_errors += 1
        if abs(sep_expected - sep_observed) > 0.13:
            gain_errors += 1
        if abs(float(row["gm_metric"]) - gm_expected) > 0.18:
            metric_errors += 1
        if (float(row["limit_flag"]) > 0.45) != flag_expected_high:
            flag_errors += 1
    ok = (
        checked >= 20
        and pos_seen
        and neg_seen
        and compressed_seen
        and disable is not None
        and inactive_checked >= 8
        and inactive_errors <= max(2, inactive_checked // 50)
        and polarity_errors <= max(14, checked // 30)
        and gain_errors <= max(12, checked // 25)
        and metric_errors <= max(16, checked // 20)
        and flag_errors <= max(24, checked // 12)
    )
    diagnostics = {
        "P_WHEN_DISABLED_DRIVE_BOTH_OUTPUTS_TO": max(
            int(disable is None or inactive_checked < 8),
            inactive_errors - max(2, inactive_checked // 50),
        ),
        "P_WHEN_ENABLED_CONVERT_THE_SAMPLED_DIFFERENTIAL": int(checked < 20 or polarity_errors > max(14, checked // 30)),
        "P_SCALE_SMALL_SIGNAL_OUTPUT_SEPARATION_BY": int(gain_errors > max(12, checked // 25)),
        "P_DRIVE_GM_METRIC_AS_A_VOLTAGE": int(metric_errors > max(16, checked // 20)),
        "P_ASSERT_LIMIT_FLAG_ONLY_WHEN_COMPRESSION": int(flag_errors > max(24, checked // 12)),
        "P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE": 0,
    }
    return ok, (
        f"v4_303 checked={checked} pos={pos_seen} neg={neg_seen} compressed={compressed_seen} "
        f"disable_seen={disable is not None} inactive_checked={inactive_checked} inactive_errors={inactive_errors} "
        f"polarity_errors={polarity_errors} gain_errors={gain_errors} "
        f"metric_errors={metric_errors} flag_errors={flag_errors}; "
        + "; ".join(f"{key} mismatch_count={value}" for key, value in diagnostics.items())
    )

CHECKER_ID = "v4_303_differential_pair_gm_limiter"
CHECKER: Checker = check_v4_303_differential_pair_gm_limiter
