"""Task-specific checker for canonical v4 DUT 321."""
from __future__ import annotations

from checkers.api import Checker
VCM = 0.45
VDD = 0.9
VTH = 0.45

def _high(row: dict[str, float], name: str, thr: float = VTH) -> bool:
    return float(row.get(name, 0.0)) > thr

def _rising(prev: float, now: float, thr: float = VTH) -> bool:
    return now > thr and prev <= thr

def _missing(rows: list[dict[str, float]], required: set[str]) -> list[str]:
    if not rows:
        return sorted(required)
    return sorted(required - set(rows[0].keys()))

def check_v4_321_charge_pump_pulse_balancer(rows: list[dict[str, float]]) -> tuple[bool, str]:
    req = {"time", "up", "dn", "clk", "rst", "enable", "vctrl", "imbalance_metric", "balanced"}
    miss = _missing(rows, req)
    if miss:
        return False, f"v4_321 missing_signals={','.join(miss)}"
    prev_clk = float(rows[0]["clk"])
    prev_row = rows[0]
    checked = step_errors = metric_errors = balance_errors = clear_errors = 0
    reset_clear = disabled_clear = ever_enabled = False
    ever_enabled = sample_pending = False
    pending_up = pending_dn = False
    expected_vctrl = VCM
    expected_imbalance = 0.0
    up_only = dn_only = hold = 0
    vctrl_min = 1e9
    vctrl_max = -1e9
    for row in rows:
        clk = float(row["clk"])
        rst = _high(row, "rst")
        enabled = _high(row, "enable") and not rst
        vctrl = float(row["vctrl"])
        if not enabled:
            clear = (
                abs(float(row["imbalance_metric"])) < 0.08
                and not _high(row, "balanced")
                and abs(vctrl - VCM) < 0.12
            )
            if rst and clear:
                reset_clear = True
            if ever_enabled and (not _high(row, "enable")) and clear:
                disabled_clear = True
            if (rst or (ever_enabled and not _high(row, "enable") and disabled_clear)) and not clear:
                clear_errors += 1
            expected_vctrl = VCM
            expected_imbalance = 0.0
            sample_pending = False
            prev_clk = clk
            prev_row = row
            continue
        ever_enabled = True
        if _rising(prev_clk, clk):
            sample_pending = True
            pending_up = _high(row, "up")
            pending_dn = _high(row, "dn")
        elif sample_pending and prev_clk > VTH and clk <= VTH:
            sample_pending = False
            checked += 1
            if pending_up and not pending_dn:
                up_only += 1
                expected_vctrl = min(VDD, expected_vctrl + 0.02)
                expected_imbalance += 0.02
            elif pending_dn and not pending_up:
                dn_only += 1
                expected_vctrl = max(0.0, expected_vctrl - 0.02)
                expected_imbalance -= 0.02
            else:
                hold += 1
            observed_vctrl = float(prev_row["vctrl"])
            metric = abs(float(prev_row["imbalance_metric"]))
            balanced = _high(prev_row, "balanced")
            if abs(observed_vctrl - expected_vctrl) > 0.012:
                step_errors += 1
            expected_metric = abs(expected_imbalance)
            if abs(metric - expected_metric) > 0.012:
                metric_errors += 1
            if balanced != (expected_metric <= 0.03):
                balance_errors += 1
            vctrl_min = min(vctrl_min, observed_vctrl)
            vctrl_max = max(vctrl_max, observed_vctrl)
        prev_clk = clk
        prev_row = row
    ok = (
        checked >= 8
        and reset_clear
        and disabled_clear
        and up_only >= 1
        and dn_only >= 1
        and hold >= 1
        and step_errors <= 1
        and metric_errors <= 1
        and balance_errors <= 1
        and vctrl_min >= -0.05
        and vctrl_max <= 0.95
    )
    clear_mismatches = int(not reset_clear) + int(not disabled_clear)
    return ok, (
        f"v4_321 checked={checked} up_only={up_only} dn_only={dn_only} hold={hold} "
        f"reset_clear={reset_clear} disabled_clear={disabled_clear} "
        f"step_errors={step_errors} metric_errors={metric_errors} balance_errors={balance_errors} "
        f"clear_errors={clear_errors} vctrl_range=[{vctrl_min:.3f},{vctrl_max:.3f}]; "
        f"P_ON_RESET_OR_WHEN_DISABLED_DRIVE mismatch_count={clear_mismatches}; "
        f"P_ON_EACH_RISING_CLK_EDGE_OBSERVE mismatch_count={step_errors}; "
        f"P_INCREASE_VCTRL_FOR_UP_ONLY_DECREASE mismatch_count={step_errors}; "
        f"P_DRIVE_IMBALANCE_METRIC_FROM_THE_ACCUMULATED mismatch_count={metric_errors}; "
        f"P_ASSERT_BALANCED_ONLY_WHEN_THE_RECENT mismatch_count={balance_errors}"
    )

CHECKER_ID = "v4_321_charge_pump_pulse_balancer"
CHECKER: Checker = check_v4_321_charge_pump_pulse_balancer
