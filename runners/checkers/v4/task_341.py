"""Task-specific checker for canonical v4 DUT 341."""
from __future__ import annotations

from ..api import Checker
def _v4_topup_clip01(value: float, low: float = 0.0, high: float = 0.9) -> float:
    return max(low, min(high, value))

def _v4_topup_logic_high(row: dict[str, float], name: str, threshold: float = 0.45) -> bool:
    return float(row.get(name, 0.0)) > threshold

def _v4_rising(prev_v: float, now_v: float, vth: float = 0.45) -> bool:
    return now_v > vth and prev_v <= vth

def _v4_batch001_first_after(rows: list[dict[str, float]], target_time: float) -> dict[str, float] | None:
    for row in rows:
        if float(row["time"]) >= target_time:
            return row
    return None

def check_v4_1039_buck_soft_start_ramp_controller(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_1039 empty_trace"
    prev_clk = float(rows[0].get("clk", 0.0))
    soft_ref = 0.0
    ramp_step = 40e-3
    ramp_tol = 5e-3
    checked = soft_errors = metric_errors = done_errors = clear_errors = step_errors = clamp_errors = 0
    reset_clear = disabled_clear = done_seen = not_done_seen = ramp_seen = target_drop_seen = False
    previous_active_soft: float | None = None
    disabled_start: float | None = None
    for row in rows:
        t = float(row["time"])
        rst = _v4_topup_logic_high(row, "rst")
        enabled = _v4_topup_logic_high(row, "enable") and not rst
        if not enabled:
            if not rst and disabled_start is None:
                disabled_start = t
            soft_ref = 0.0
            previous_active_soft = None
            clear = row["soft_ref"] < 0.10 and row["ramp_metric"] < 0.10 and row["done"] < 0.10
            reset_clear = reset_clear or (rst and t < 3.5e-9 and clear)
            disabled_settled = (not rst) and disabled_start is not None and (t - disabled_start) > 1.0e-9
            disabled_clear = disabled_clear or (disabled_settled and clear)
            if ((rst and t > 0.5e-9) or disabled_settled) and not clear:
                clear_errors += 1
            prev_clk = float(row["clk"])
            continue
        disabled_start = None
        if _v4_rising(prev_clk, float(row["clk"])):
            target = _v4_topup_clip01(float(row["target_ref"]))
            if soft_ref > target:
                soft_ref = target
                target_drop_seen = True
            elif target - soft_ref <= ramp_tol:
                soft_ref = target
            else:
                before = soft_ref
                soft_ref = min(target, soft_ref + ramp_step)
                if soft_ref - before > ramp_step + 0.010:
                    step_errors += 1
            expected_metric = max(0.0, target - soft_ref)
            expected_done = expected_metric <= ramp_tol
            sample = _v4_batch001_first_after(rows, t + 0.7e-9)
            if sample is not None:
                checked += 1
                observed_soft = float(sample["soft_ref"])
                observed_metric = float(sample["ramp_metric"])
                observed_done = _v4_topup_logic_high(sample, "done")
                done_seen = done_seen or expected_done
                not_done_seen = not_done_seen or not expected_done
                ramp_seen = ramp_seen or expected_metric > 0.03
                if observed_soft - target > 0.045:
                    clamp_errors += 1
                if previous_active_soft is not None and target >= previous_active_soft and observed_soft + 0.02 < previous_active_soft and expected_metric > ramp_tol:
                    step_errors += 1
                previous_active_soft = observed_soft
                if abs(observed_soft - soft_ref) > 0.055:
                    soft_errors += 1
                if abs(observed_metric - expected_metric) > 0.060:
                    metric_errors += 1
                if observed_done != expected_done:
                    done_errors += 1
        prev_clk = float(row["clk"])
    ok = (
        checked >= 8
        and reset_clear
        and disabled_clear
        and done_seen
        and not_done_seen
        and ramp_seen
        and target_drop_seen
        and soft_errors <= 1
        and metric_errors <= 1
        and done_errors <= 1
        and clear_errors <= 3
        and step_errors <= 1
        and clamp_errors <= 1
    )
    return ok, (
        f"v4_1039 checked={checked} reset_clear={reset_clear} disabled_clear={disabled_clear} "
        f"done_seen={done_seen} not_done_seen={not_done_seen} ramp_seen={ramp_seen} "
        f"target_drop_seen={target_drop_seen} soft_errors={soft_errors} metric_errors={metric_errors} "
        f"done_errors={done_errors} clear_errors={clear_errors} step_errors={step_errors} "
        f"clamp_errors={clamp_errors}"
    )

CHECKER_ID = "v4_341_buck_soft_start_ramp_controller"
CHECKER: Checker = check_v4_1039_buck_soft_start_ramp_controller
