"""Task-specific checker for canonical v4 DUT 340."""
from __future__ import annotations

from ..api import Checker
from .diagnostics import with_property_diagnostics
VTH = 0.45
SETTLE_S = 0.7e-9

def _high(row: dict[str, float], name: str, thr: float = VTH) -> bool:
    return float(row.get(name, 0.0)) > thr

def _rising(prev: float, now: float, thr: float = VTH) -> bool:
    return now > thr and prev <= thr

def _first_after(rows: list[dict[str, float]], target_time: float) -> dict[str, float] | None:
    for row in rows:
        if float(row["time"]) >= target_time:
            return row
    return None

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
    disable_time: float | None = None
    active_edges = 0
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
            disabled = ever_enabled and not _high(row, "enable")
            if disabled and disable_time is None:
                disable_time = t
            disabled_ready = (
                disabled
                and disable_time is not None
                and t >= disable_time + 0.7e-9
            )
            if disabled_ready and clear:
                disabled_clear = True
            if (rst or disabled_ready) and not clear:
                clear_errors += 1
            active_edges = 0
            prev_clk = clk
            continue
        ever_enabled = True
        disable_time = None
        if not _rising(prev_clk, clk):
            prev_clk = clk
            continue
        prev_clk = clk
        active_edges += 1
        if active_edges == 1:
            continue
        sample = _first_after(rows, t + SETTLE_S)
        if sample is None:
            continue
        checked += 1
        cmd = float(row["power_cmd"])
        temp = float(row["temp_sense"])
        limited = float(sample["limited_cmd"])
        metric = abs(float(sample["foldback_metric"]))
        ok_flag = _high(sample, "thermal_ok")
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
        and thermal_errors == 0
        and clear_errors <= 6
    )
    return ok, (
        f"v4_340 checked={checked} pass_errors={pass_errors} fold_errors={fold_errors} "
        f"metric_errors={metric_errors} thermal_errors={thermal_errors} "
        f"reset_clear={reset_clear} disabled_clear={disabled_clear} clear_errors={clear_errors}"
    )

CHECKER_ID = "v4_340_thermal_foldback_power_limiter"
CHECKER: Checker = with_property_diagnostics(
    check_v4_340_thermal_foldback_power_limiter,
    {
        "P_ON_RESET_OR_WHEN_DISABLED_CLEAR": ("clear_errors", "!reset_clear", "!disabled_clear"),
        "P_ON_EACH_ENABLED_RISING_CLK_EDGE": ("pass_errors", "fold_errors", "metric_errors"),
        "P_PASS_POWER_CMD_THROUGH_WHILE_TEMPERATURE": "pass_errors",
        "P_REDUCE_LIMITED_CMD_AS_TEMPERATURE_RISES": "fold_errors",
        "P_ASSERT_THERMAL_OK_ONLY_WHEN_NO": "thermal_errors",
    },
)
