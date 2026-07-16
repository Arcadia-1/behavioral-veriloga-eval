"""Task-specific checker for canonical v4 DUT 317."""
from __future__ import annotations

from ..api import Checker
from ..common.v4_topup import (
    _v4_topup_logic_high,
    _v4_rising,
)

def check_v4_317_capacitor_mismatch_calibration_engine(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_1015 empty_trace"

    def settled(index: int) -> bool:
        """Use local signal stability instead of absolute clock timestamps."""
        if index < 2:
            return False
        names = (
            "rst", "enable", "cal_0", "cal_1", "cal_2", "cal_3",
            "correction_metric", "done",
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
    checked = metric_errors = clear_errors = done_errors = 0
    codes_seen: set[int] = set()
    reset_clear = disabled_clear = monotonic_up = high_code_seen = done_seen = False
    last_code = None
    saw_active = False
    active_rises = 0
    previous_clk = float(rows[0].get("clk", 0.0))
    last_rise = None
    for index, row in enumerate(rows):
        t = float(row["time"])
        rst = _v4_topup_logic_high(row, "rst")
        enabled = _v4_topup_logic_high(row, "enable") and not rst
        clk = float(row.get("clk", 0.0))
        if _v4_topup_logic_high(row, "enable") and not rst and _v4_rising(previous_clk, clk):
            active_rises += 1
            last_rise = t
        previous_clk = clk
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
            stable = settled(index)
            if rst and stable and clear:
                reset_clear = True
            if saw_active and not rst and not _v4_topup_logic_high(row, "enable") and stable and clear:
                disabled_clear = True
            if stable and (rst or (saw_active and not _v4_topup_logic_high(row, "enable"))) and not clear:
                clear_errors += 1
            continue
        saw_active = True
        if last_rise is None or t - last_rise < 0.24 * period or not settled(index):
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
        if active_rises >= 8 and done:
            done_seen = True
        if active_rises < 8 and done:
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
