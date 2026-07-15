"""Task-specific checker for canonical v4 DUT 316."""
from __future__ import annotations

from ..api import Checker
from ..common.v4_topup import (
    _v4_topup_clip01,
    _v4_topup_logic_high,
)

def check_v4_316_residue_amplifier_gain_calibration(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_1014 empty_trace"
    checked = vout_errors = metric_errors = clear_errors = lock_errors = 0
    codes_seen: set[int] = set()
    reset_clear = disabled_clear = high_code_seen = locked_seen = error_reduced = False
    first_active_error = None
    last_active_error = None
    for row in rows:
        t = float(row["time"])
        rst = _v4_topup_logic_high(row, "rst")
        enabled = _v4_topup_logic_high(row, "cal_en") and not rst
        code = (
            (1 if _v4_topup_logic_high(row, "gain_0") else 0)
            + (2 if _v4_topup_logic_high(row, "gain_1") else 0)
            + (4 if _v4_topup_logic_high(row, "gain_2") else 0)
        )
        vout = float(row["vout"])
        metric = float(row["error_metric"])
        locked = _v4_topup_logic_high(row, "locked")
        if not enabled:
            clear = code == 0 and abs(vout - 0.45) < 0.08 and metric < 0.08 and not locked
            if rst and t < 5e-9 and clear:
                reset_clear = True
            if t > 82e-9 and not _v4_topup_logic_high(row, "cal_en") and clear:
                disabled_clear = True
            if ((rst and t < 5e-9) or t > 82e-9) and not clear:
                clear_errors += 1
            continue
        if t < 12e-9 or any(edge <= t <= edge + 1.2e-9 for edge in [5e-9, 10e-9, 15e-9, 20e-9, 25e-9, 30e-9, 35e-9, 40e-9, 45e-9, 50e-9, 55e-9, 60e-9, 65e-9, 70e-9]):
            continue
        expected = _v4_topup_clip01(0.45 + (2.0 + 0.25 * code) * (float(row["vin"]) - 0.45))
        err = abs(float(row["residue_ref"]) - vout)
        checked += 1
        codes_seen.add(code)
        if abs(vout - expected) > 0.08:
            vout_errors += 1
        if abs(metric - err) > 0.08:
            metric_errors += 1
        if first_active_error is None:
            first_active_error = err
        last_active_error = err
        if code >= 4:
            high_code_seen = True
        if locked and t < 35e-9:
            lock_errors += 1
        if locked:
            locked_seen = True
            if err > 0.08:
                lock_errors += 1
    if first_active_error is not None and last_active_error is not None:
        error_reduced = last_active_error + 0.04 < first_active_error
    ok = (
        checked >= 40
        and reset_clear
        and disabled_clear
        and high_code_seen
        and locked_seen
        and error_reduced
        and vout_errors <= max(6, checked // 20)
        and metric_errors <= max(6, checked // 20)
        and lock_errors <= 2
        and clear_errors <= 4
    )
    return ok, (
        f"v4_316 checked={checked} codes={sorted(codes_seen)} reset_clear={reset_clear} "
        f"disabled_clear={disabled_clear} high_code_seen={high_code_seen} locked_seen={locked_seen} "
        f"error_reduced={error_reduced} vout_errors={vout_errors} metric_errors={metric_errors} "
        f"lock_errors={lock_errors} clear_errors={clear_errors}"
    )

CHECKER_ID = "v4_316_residue_amplifier_gain_calibration"
CHECKER: Checker = check_v4_316_residue_amplifier_gain_calibration
