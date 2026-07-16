"""Task-specific checker for canonical v4 DUT 305."""
from __future__ import annotations

from ..api import Checker
from ..common.v4_topup import (
    _v4_topup_clip01,
    _v4_topup_logic_high,
    _v4_topup_near,
)
from ..common.relative_events import active_start, first_disable

def check_v4_305_capacitive_feedback_amplifier_macro(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_1003 empty_trace"
    checked = sample_errors = gain_errors = settled_errors = 0
    codes_seen: set[int] = set()
    disabled_clear = settled_seen = False
    activation = active_start(rows, enable="enable", reset="rst")
    disable = first_disable(rows, "enable", activation)
    for row in rows:
        t = float(row["time"])
        if t < activation:
            continue
        active = _v4_topup_logic_high(row, "enable") and not _v4_topup_logic_high(row, "rst")
        if not active:
            if (disable is None or t >= disable) and _v4_topup_near(row["vout"], 0.45, 0.08) and row["sampled_metric"] < 0.15 and row["settled"] < 0.15:
                disabled_clear = True
            continue
        code = int(_v4_topup_logic_high(row, "gain_0")) + 2 * int(_v4_topup_logic_high(row, "gain_1"))
        expected_gain = 1.0 + 0.75 * code
        expected_vout = _v4_topup_clip01(0.45 + expected_gain * (float(row["sampled_metric"]) - 0.45))
        codes_seen.add(code)
        checked += 1
        if abs(float(row["sampled_metric"]) - float(row["vin"])) > 0.18:
            sample_errors += 1
        if abs(float(row["vout"]) - expected_vout) > 0.16:
            gain_errors += 1
        if abs(float(row["vout"]) - expected_vout) < 0.04:
            settled_seen = settled_seen or float(row["settled"]) > 0.45
        elif float(row["settled"]) > 0.45:
            settled_errors += 1
    ok = (
        checked >= 8
        and len(codes_seen) >= 3
        and disabled_clear
        and settled_seen
        and sample_errors <= max(24, checked // 6)
        and gain_errors <= max(32, checked // 4)
        and settled_errors <= max(8, checked // 12)
    )
    diagnostics = {
        "P_ON_RESET_OR_WHEN_DISABLED_DRIVE": int(not disabled_clear),
        "P_ON_EACH_RISING_CLK_EDGE_WHILE": int(sample_errors > max(24, checked // 6)),
        "P_DRIVE_SAMPLED_METRIC_WITH_THE_HELD": int(sample_errors > max(24, checked // 6)),
        "P_MOVE_VOUT_TOWARD_VCM_GAIN_SAMPLE": int(gain_errors > max(32, checked // 4)),
        "P_ASSERT_SETTLED_AFTER_THE_OUTPUT_HAS": int(not settled_seen or settled_errors > max(8, checked // 12)),
        "P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE": 0,
    }
    return ok, (
        f"v4_305 checked={checked} codes={sorted(codes_seen)} disabled_clear={disabled_clear} "
        f"settled_seen={settled_seen} sample_errors={sample_errors} gain_errors={gain_errors} "
        f"settled_errors={settled_errors}; "
        + "; ".join(f"{key} mismatch_count={value}" for key, value in diagnostics.items())
    )

CHECKER_ID = "v4_305_capacitive_feedback_amplifier_macro"
CHECKER: Checker = check_v4_305_capacitive_feedback_amplifier_macro
