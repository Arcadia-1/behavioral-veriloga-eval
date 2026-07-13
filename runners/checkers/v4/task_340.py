"""Task-specific checker for canonical v4 DUT 340."""
from __future__ import annotations

from checkers.api import Checker
VTH = 0.45

def _high(row: dict[str, float], name: str, thr: float = VTH) -> bool:
    return float(row.get(name, 0.0)) > thr

def _rising(prev: float, now: float, thr: float = VTH) -> bool:
    return now > thr and prev <= thr

def _missing(rows: list[dict[str, float]], required: set[str]) -> list[str]:
    if not rows:
        return sorted(required)
    return sorted(required - set(rows[0].keys()))

def check_v4_340_thermal_foldback_power_limiter(rows: list[dict[str, float]]) -> tuple[bool, str]:
    req = {
        "time", "power_cmd", "temp_sense", "clk", "rst", "enable",
        "limited_cmd", "foldback_metric", "thermal_ok",
    }
    miss = _missing(rows, req)
    if miss:
        return False, f"v4_340 missing_signals={','.join(miss)}"
    prev_clk = float(rows[0]["clk"])
    checked = pass_errors = fold_errors = thermal_errors = metric_errors = clear_errors = 0
    reset_clear = disabled_clear = ever_enabled = False
    trip = 0.65
    for row in rows:
        t = float(row["time"])
        clk = float(row["clk"])
        rst = _high(row, "rst")
        enabled = _high(row, "enable") and not rst
        if not enabled:
            clear = (
                abs(float(row["limited_cmd"])) < 0.12
                and abs(float(row["foldback_metric"])) < 0.08
                and not _high(row, "thermal_ok")
            )
            if rst and clear:
                reset_clear = True
            if ever_enabled and (not _high(row, "enable")) and clear:
                disabled_clear = True
            if (rst or (ever_enabled and not _high(row, "enable") and disabled_clear)) and not clear:
                clear_errors += 1
            prev_clk = clk
            continue
        ever_enabled = True
        if not _rising(prev_clk, clk):
            prev_clk = clk
            continue
        prev_clk = clk
        if t < 8e-9:
            continue
        checked += 1
        cmd = float(row["power_cmd"])
        temp = float(row["temp_sense"])
        limited = float(row["limited_cmd"])
        metric = abs(float(row["foldback_metric"]))
        ok_flag = _high(row, "thermal_ok")
        if temp < trip - 0.02:
            if abs(limited - cmd) > 0.06:
                pass_errors += 1
            if metric > 0.05:
                metric_errors += 1
            if not ok_flag and metric < 0.03:
                # tolerate delayed thermal_ok
                pass
        elif temp > trip + 0.02:
            if limited > cmd - 0.03:
                fold_errors += 1
            if abs(metric - abs(cmd - limited)) > 0.08:
                metric_errors += 1
            if ok_flag:
                thermal_errors += 1
        if ok_flag and metric > 0.05:
            thermal_errors += 1
    ok = (
        checked >= 8
        and reset_clear
        and disabled_clear
        and pass_errors <= max(2, checked // 4)
        and fold_errors <= max(2, checked // 4)
        and metric_errors <= max(3, checked // 3)
        and thermal_errors <= max(2, checked // 4)
        and clear_errors <= 6
    )
    return ok, (
        f"v4_340 checked={checked} pass_errors={pass_errors} fold_errors={fold_errors} "
        f"metric_errors={metric_errors} thermal_errors={thermal_errors} "
        f"reset_clear={reset_clear} disabled_clear={disabled_clear} clear_errors={clear_errors}"
    )

CHECKER_ID = "v4_340_thermal_foldback_power_limiter"
CHECKER: Checker = check_v4_340_thermal_foldback_power_limiter
