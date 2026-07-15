"""Task-specific checker for canonical v4 DUT 317."""
from __future__ import annotations

from ..api import Checker
from ..common.v4_topup import (
    _v4_topup_logic_high,
)

def check_v4_317_capacitor_mismatch_calibration_engine(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_1015 empty_trace"
    checked = metric_errors = clear_errors = done_errors = 0
    codes_seen: set[int] = set()
    reset_clear = disabled_clear = monotonic_up = high_code_seen = done_seen = False
    last_code = None
    for row in rows:
        t = float(row["time"])
        rst = _v4_topup_logic_high(row, "rst")
        enabled = _v4_topup_logic_high(row, "enable") and not rst
        code = (
            (1 if _v4_topup_logic_high(row, "cal_0") else 0)
            + (2 if _v4_topup_logic_high(row, "cal_1") else 0)
            + (4 if _v4_topup_logic_high(row, "cal_2") else 0)
            + (8 if _v4_topup_logic_high(row, "cal_3") else 0)
        )
        metric = float(row["correction_metric"])
        done = _v4_topup_logic_high(row, "done")
        if not enabled:
            clear = code == 0 and metric < 0.03 and not done
            if rst and t < 5e-9 and clear:
                reset_clear = True
            if t > 82e-9 and not _v4_topup_logic_high(row, "enable") and clear:
                disabled_clear = True
            if ((rst and t < 5e-9) or t > 82e-9) and not clear:
                clear_errors += 1
            continue
        if t < 12e-9 or any(edge <= t <= edge + 1.2e-9 for edge in [5e-9, 10e-9, 15e-9, 20e-9, 25e-9, 30e-9, 35e-9, 40e-9, 45e-9, 50e-9, 55e-9, 60e-9, 65e-9, 70e-9]):
            continue
        checked += 1
        codes_seen.add(code)
        if last_code is not None and code >= last_code and code > 0:
            monotonic_up = True
        last_code = code
        if code >= 8:
            high_code_seen = True
        if abs(metric - 0.006 * code) > 0.015:
            metric_errors += 1
        if t > 50e-9 and done:
            done_seen = True
        if t < 35e-9 and done:
            done_errors += 1
    ok = (
        checked >= 40
        and reset_clear
        and disabled_clear
        and monotonic_up
        and high_code_seen
        and done_seen
        and len(codes_seen) >= 5
        and metric_errors <= max(6, checked // 20)
        and done_errors <= 2
        and clear_errors <= 4
    )
    return ok, (
        f"v4_317 checked={checked} codes={sorted(codes_seen)} reset_clear={reset_clear} "
        f"disabled_clear={disabled_clear} monotonic_up={monotonic_up} high_code_seen={high_code_seen} "
        f"done_seen={done_seen} metric_errors={metric_errors} done_errors={done_errors} clear_errors={clear_errors}"
    )

CHECKER_ID = "v4_317_capacitor_mismatch_calibration_engine"
CHECKER: Checker = check_v4_317_capacitor_mismatch_calibration_engine
