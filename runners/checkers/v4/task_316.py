"""Task-specific checker for canonical v4 DUT 316."""
from __future__ import annotations

from ..api import Checker
from ..common.v4_topup import (
    _v4_topup_clip01,
    _v4_topup_logic_high,
    _v4_rising,
)
from .diagnostics import with_property_diagnostics

def check_v4_316_residue_amplifier_gain_calibration(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_1014 empty_trace"

    def settled(index: int) -> bool:
        """Avoid fixed time windows; wait for the current clock result to settle."""
        if index < 2:
            return False
        names = (
            "rst", "cal_en", "gain_0", "gain_1", "gain_2",
            "vout", "error_metric", "locked",
        )
        for current in range(index - 1, index + 1):
            previous = rows[current - 1]
            row = rows[current]
            if any(abs(float(row[name]) - float(previous[name])) > 1e-4 for name in names):
                return False
        return True

    def clock_period() -> float:
        rises: list[float] = []
        previous = float(rows[0].get("clk", 0.0))
        for row in rows[1:]:
            now = float(row["clk"])
            if now > 0.45 and previous <= 0.45:
                rises.append(float(row["time"]))
            previous = now
        periods = [right - left for left, right in zip(rises, rises[1:]) if right > left]
        return sorted(periods)[len(periods) // 2] if periods else 1.0

    period = clock_period()
    checked = vout_errors = metric_errors = clear_errors = lock_errors = 0
    codes_seen: set[int] = set()
    reset_clear = disabled_clear = high_code_seen = locked_seen = error_reduced = False
    first_active_error = None
    last_active_error = None
    saw_active = False
    active_rises = 0
    previous_clk = float(rows[0].get("clk", 0.0))
    last_rise = None
    for index, row in enumerate(rows):
        t = float(row["time"])
        rst = _v4_topup_logic_high(row, "rst")
        enabled = _v4_topup_logic_high(row, "cal_en") and not rst
        clk = float(row.get("clk", 0.0))
        if _v4_topup_logic_high(row, "cal_en") and not rst and _v4_rising(previous_clk, clk):
            active_rises += 1
            last_rise = t
        previous_clk = clk
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
            stable = settled(index)
            if rst and stable and clear:
                reset_clear = True
            if saw_active and not rst and not _v4_topup_logic_high(row, "cal_en") and stable and clear:
                disabled_clear = True
            if stable and ((rst) or (saw_active and not _v4_topup_logic_high(row, "cal_en"))) and not clear:
                clear_errors += 1
            continue
        saw_active = True
        if last_rise is None or t - last_rise < 0.24 * period or not settled(index):
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
        if locked and active_rises < 3:
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
CHECKER: Checker = with_property_diagnostics(
    check_v4_316_residue_amplifier_gain_calibration,
    {
        "P_ON_RESET_CLEAR_GAIN_CODE_OUTPUT": (
            "clear_errors", "!reset_clear", "!disabled_clear",
        ),
        "P_WHILE_CAL_EN_IS_HIGH_COMPARE": "metric_errors",
        "P_INCREMENT_OR_DECREMENT_THE_GAIN_CODE": (
            "!high_code_seen", "!error_reduced",
        ),
        "P_DRIVE_VOUT_AS_A_CLAMPED_RESIDUE": "vout_errors",
        "P_ASSERT_LOCKED_AFTER_THREE_CONSECUTIVE_UPDATES": (
            "lock_errors", "!locked_seen",
        ),
        "P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE": (),
    },
)
