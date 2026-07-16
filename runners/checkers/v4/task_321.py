"""Checker for the clocked charge-pump pulse balancer."""

from __future__ import annotations

from ..api import Checker, Row


VCM = 0.45
VDD = 0.9
VTH = 0.45
PUMP_STEP = 0.02
BALANCE_TOL = 0.03


def _high(row: Row, name: str) -> bool:
    return float(row[name]) > VTH


def _rising(previous: float, current: float) -> bool:
    return previous <= VTH < current


def check_charge_pump_pulse_balancer(rows: list[Row]) -> tuple[bool, str]:
    required = {
        "time",
        "up",
        "dn",
        "clk",
        "rst",
        "enable",
        "vctrl",
        "imbalance_metric",
        "balanced",
    }
    missing = sorted(required - (set(rows[0]) if rows else set()))
    if missing:
        return False, "v4_321 missing_signals=" + ",".join(missing)

    previous_clk = float(rows[0]["clk"])
    previous_row = rows[0]
    expected_vctrl = VCM
    expected_imbalance = 0.0
    pending_sample: tuple[bool, bool] | None = None
    checked = 0
    up_only = 0
    dn_only = 0
    holds = 0
    step_errors = 0
    metric_errors = 0
    balance_errors = 0
    reset_clear = False
    disabled_clear = False
    ever_enabled = False

    for row in rows:
        clk = float(row["clk"])
        reset = _high(row, "rst")
        enabled = _high(row, "enable") and not reset
        if not enabled:
            clear = (
                abs(float(row["vctrl"]) - VCM) <= 0.08
                and abs(float(row["imbalance_metric"])) <= 0.05
                and not _high(row, "balanced")
            )
            reset_clear |= reset and clear
            disabled_clear |= ever_enabled and not _high(row, "enable") and clear
            expected_vctrl = VCM
            expected_imbalance = 0.0
            pending_sample = None
            previous_clk = clk
            previous_row = row
            continue

        ever_enabled = True
        if _rising(previous_clk, clk):
            pending_sample = (_high(row, "up"), _high(row, "dn"))
        elif pending_sample is not None and previous_clk > VTH >= clk:
            up, dn = pending_sample
            pending_sample = None
            checked += 1
            if up and not dn:
                up_only += 1
                expected_vctrl = min(VDD, expected_vctrl + PUMP_STEP)
                expected_imbalance += PUMP_STEP
            elif dn and not up:
                dn_only += 1
                expected_vctrl = max(0.0, expected_vctrl - PUMP_STEP)
                expected_imbalance -= PUMP_STEP
            else:
                holds += 1

            observed_vctrl = float(previous_row["vctrl"])
            observed_metric = float(previous_row["imbalance_metric"])
            observed_balanced = _high(previous_row, "balanced")
            expected_metric = abs(expected_imbalance)
            step_errors += abs(observed_vctrl - expected_vctrl) > 0.012
            metric_errors += abs(observed_metric - expected_metric) > 0.012
            balance_errors += observed_balanced != (expected_metric <= BALANCE_TOL)

        previous_clk = clk
        previous_row = row

    coverage_ok = (
        checked >= 5
        and reset_clear
        and disabled_clear
        and up_only > 0
        and dn_only > 0
        and holds > 0
    )
    ok = coverage_ok and step_errors <= 1 and metric_errors <= 1 and balance_errors <= 1
    return ok, (
        f"v4_321 checked={checked} up_only={up_only} dn_only={dn_only} holds={holds} "
        f"reset_clear={reset_clear} disabled_clear={disabled_clear} "
        f"step_errors={step_errors} metric_errors={metric_errors} "
        f"balance_errors={balance_errors}; "
        f"P_ON_RESET_OR_WHEN_DISABLED_DRIVE mismatch_count={int(not reset_clear) + int(not disabled_clear)}; "
        f"P_ON_EACH_RISING_CLK_EDGE_OBSERVE mismatch_count={step_errors}; "
        f"P_INCREASE_VCTRL_FOR_UP_ONLY_DECREASE mismatch_count={step_errors}; "
        f"P_DRIVE_IMBALANCE_METRIC_FROM_THE_ACCUMULATED mismatch_count={metric_errors}; "
        f"P_ASSERT_BALANCED_ONLY_WHEN_THE_RECENT mismatch_count={balance_errors}"
    )


CHECKER_ID = "v4_321_charge_pump_pulse_balancer"
CHECKER: Checker = check_charge_pump_pulse_balancer
