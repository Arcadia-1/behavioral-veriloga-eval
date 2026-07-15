"""Task-specific checker for canonical v4 DUT 303."""
from __future__ import annotations

from ..api import Checker
from ..common.v4_topup import (
    _v4_topup_logic_high,
    _v4_topup_near,
)

def check_v4_303_differential_pair_gm_limiter(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_1001 empty_trace"
    checked = polarity_errors = gain_errors = flag_errors = metric_errors = 0
    pos_seen = neg_seen = compressed_seen = disabled_clear = False
    gm_gain = 4.0
    diff_limit = 120e-3
    for row in rows:
        t = float(row["time"])
        if t < 7e-9:
            continue
        enabled = _v4_topup_logic_high(row, "enable")
        if not enabled:
            if t > 52e-9 and _v4_topup_near(row["voutp"], 0.45, 0.08) and _v4_topup_near(row["voutn"], 0.45, 0.08) and row["gm_metric"] < 0.12 and row["limit_flag"] < 0.12:
                disabled_clear = True
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
        and disabled_clear
        and polarity_errors <= max(14, checked // 30)
        and gain_errors <= max(12, checked // 25)
        and metric_errors <= max(16, checked // 20)
        and flag_errors <= max(24, checked // 12)
    )
    return ok, (
        f"v4_303 checked={checked} pos={pos_seen} neg={neg_seen} compressed={compressed_seen} "
        f"disabled_clear={disabled_clear} polarity_errors={polarity_errors} gain_errors={gain_errors} "
        f"metric_errors={metric_errors} flag_errors={flag_errors}"
    )

CHECKER_ID = "v4_303_differential_pair_gm_limiter"
CHECKER: Checker = check_v4_303_differential_pair_gm_limiter
