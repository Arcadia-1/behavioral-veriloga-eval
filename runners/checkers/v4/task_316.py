"""Task-specific checker for canonical v4 DUT 316."""
from __future__ import annotations

from bisect import bisect_left

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

    def clock_period() -> float:
        rises: list[float] = []
        previous = float(rows[0].get("clk", 0.0))
        for row in rows[1:]:
            now = float(row["clk"])
            if now > 0.45 and previous <= 0.45:
                rises.append(float(row["time"]))
            previous = now
        periods = [right - left for left, right in zip(rises, rises[1:]) if right > left]
        return sorted(periods)[len(periods) // 2] if periods else 1e-9

    period = clock_period()
    settle_window = min(1e-9, max(0.35e-9, 0.10 * period))
    times = [float(row["time"]) for row in rows]
    checked = code_errors = vout_errors = metric_errors = clear_errors = lock_errors = 0
    codes_seen: set[int] = set()
    reset_clear = late_reset_clear = disabled_clear = high_code_seen = locked_seen = decrement_seen = False
    first_active_error = None
    last_active_error = None
    expected_code = 0
    lock_streak = 0
    ever_enabled = False
    inactive_kind: str | None = None
    inactive_start = float(rows[0].get("time", 0.0))
    previous_clk = float(rows[0].get("clk", 0.0))
    for row in rows:
        rst = _v4_topup_logic_high(row, "rst")
        enabled = _v4_topup_logic_high(row, "cal_en") and not rst
        row_time = float(row["time"])
        clk = float(row.get("clk", 0.0))
        code = (
            (1 if _v4_topup_logic_high(row, "gain_0") else 0)
            + (2 if _v4_topup_logic_high(row, "gain_1") else 0)
            + (4 if _v4_topup_logic_high(row, "gain_2") else 0)
        )
        vout = float(row["vout"])
        metric = float(row["error_metric"])
        locked = _v4_topup_logic_high(row, "locked")
        if not enabled:
            next_inactive_kind = (
                "reset"
                if rst
                else "disabled"
                if ever_enabled and not _v4_topup_logic_high(row, "cal_en")
                else None
            )
            if next_inactive_kind != inactive_kind:
                inactive_kind = next_inactive_kind
                inactive_start = row_time
            clear = code == 0 and abs(vout - 0.45) < 0.08 and metric < 0.08 and not locked
            if rst and clear:
                reset_clear = True
                if ever_enabled:
                    late_reset_clear = True
            if ever_enabled and not rst and not _v4_topup_logic_high(row, "cal_en") and clear:
                disabled_clear = True
            if (
                next_inactive_kind is not None
                and row_time - inactive_start >= settle_window
                and not clear
            ):
                clear_errors += 1
            expected_code = 0
            lock_streak = 0
            previous_clk = clk
            continue
        inactive_kind = None
        ever_enabled = True
        if not _v4_rising(previous_clk, clk):
            previous_clk = clk
            continue
        previous_clk = clk
        edge_time = float(row["time"])
        sample_index = min(len(rows) - 1, bisect_left(times, edge_time + 0.24 * period))
        sample = rows[sample_index]
        if _v4_topup_logic_high(sample, "rst") or not _v4_topup_logic_high(sample, "cal_en"):
            continue
        pre_vout = _v4_topup_clip01(
            0.45 + (2.0 + 0.25 * expected_code) * (float(row["vin"]) - 0.45)
        )
        signed_error = float(row["residue_ref"]) - pre_vout
        err = abs(signed_error)
        if signed_error > 0.015:
            expected_code = min(7, expected_code + 1)
        elif signed_error < -0.015:
            if expected_code > 0:
                decrement_seen = True
            expected_code = max(0, expected_code - 1)
        lock_streak = lock_streak + 1 if err <= 0.015 else 0
        expected_locked = lock_streak >= 3
        observed_code = (
            (1 if _v4_topup_logic_high(sample, "gain_0") else 0)
            + (2 if _v4_topup_logic_high(sample, "gain_1") else 0)
            + (4 if _v4_topup_logic_high(sample, "gain_2") else 0)
        )
        expected_vout = _v4_topup_clip01(
            0.45 + (2.0 + 0.25 * expected_code) * (float(sample["vin"]) - 0.45)
        )
        checked += 1
        codes_seen.add(observed_code)
        if observed_code != expected_code:
            code_errors += 1
        if abs(float(sample["vout"]) - expected_vout) > 0.08:
            vout_errors += 1
        if abs(float(sample["error_metric"]) - err) > 0.03:
            metric_errors += 1
        if first_active_error is None:
            first_active_error = err
        last_active_error = err
        if observed_code >= 4:
            high_code_seen = True
        observed_locked = _v4_topup_logic_high(sample, "locked")
        if observed_locked:
            locked_seen = True
        if observed_locked != expected_locked:
            lock_errors += 1
    error_reduced = (
        first_active_error is not None
        and last_active_error is not None
        and last_active_error + 0.01 < first_active_error
    )
    ok = (
        checked >= 8
        and reset_clear
        and late_reset_clear
        and disabled_clear
        and locked_seen
        and decrement_seen
        and error_reduced
        and code_errors == 0
        and vout_errors == 0
        and metric_errors == 0
        and lock_errors == 0
        and clear_errors == 0
    )
    return ok, (
        f"v4_316 checked={checked} codes={sorted(codes_seen)} reset_clear={reset_clear} "
        f"late_reset_clear={late_reset_clear} disabled_clear={disabled_clear} "
        f"high_code_seen={high_code_seen} locked_seen={locked_seen} decrement_seen={decrement_seen} "
        f"error_reduced={error_reduced} code_errors={code_errors} "
        f"vout_errors={vout_errors} metric_errors={metric_errors} "
        f"lock_errors={lock_errors} clear_errors={clear_errors} settle_window={settle_window:.6g}"
    )

CHECKER_ID = "v4_316_residue_amplifier_gain_calibration"
CHECKER: Checker = with_property_diagnostics(
    check_v4_316_residue_amplifier_gain_calibration,
    {
        "P_ON_RESET_CLEAR_GAIN_CODE_OUTPUT": (
            "clear_errors", "!reset_clear", "!late_reset_clear", "!disabled_clear",
        ),
        "P_WHILE_CAL_EN_IS_HIGH_COMPARE": "metric_errors",
        "P_INCREMENT_OR_DECREMENT_THE_GAIN_CODE": (
            "code_errors", "!decrement_seen", "!error_reduced",
        ),
        "P_DRIVE_VOUT_AS_A_CLAMPED_RESIDUE": "vout_errors",
        "P_ASSERT_LOCKED_AFTER_THREE_CONSECUTIVE_UPDATES": (
            "lock_errors", "!locked_seen",
        ),
        "P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE": (),
    },
)
