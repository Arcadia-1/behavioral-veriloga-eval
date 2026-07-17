"""Task-specific checker for canonical v4 DUT 331."""
from __future__ import annotations

from ..api import Checker
from .diagnostics import with_property_diagnostics
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

def check_v4_331_dfe_error_proxy_loop(rows: list[dict[str, float]]) -> tuple[bool, str]:
    req = {
        "time", "sample_in", "decision_clk", "rst", "enable",
        "tap_1", "tap_0", "corrected_out", "error_metric", "converged",
    }
    miss = _missing(rows, req)
    if miss:
        return False, f"v4_331 missing_signals={','.join(miss)}"
    prev_clk = float(rows[0]["decision_clk"])
    checked = corr_errors = decision_errors = conv_errors = clear_errors = 0
    reset_clear = disabled_clear = ever_enabled = False
    disable_time: float | None = None
    active_edges = 0
    decisions = 0
    error_max = 0.0
    streak = 0
    history_1 = history_0 = 0
    expected_tap_1 = expected_tap_0 = 0.0
    for row in rows:
        t = float(row["time"])
        clk = float(row["decision_clk"])
        rst = _high(row, "rst")
        enabled = _high(row, "enable") and not rst
        if not enabled:
            clear = (
                abs(float(row["corrected_out"]) - VCM) < 0.12
                and abs(float(row["error_metric"])) < 0.08
                and not _high(row, "converged")
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
            streak = 0
            history_1 = history_0 = 0
            expected_tap_1 = expected_tap_0 = 0.0
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
        sample = next((item for item in rows if float(item["time"]) >= t + 0.7e-9), rows[-1])
        sample_delta = float(row["sample_in"]) - VCM
        expected_residual = (
            sample_delta
            - expected_tap_1 * history_1
            - expected_tap_0 * history_0
        )
        expected_tap_1 = max(
            -0.18,
            min(0.18, expected_tap_1 + 0.04 * expected_residual * history_1),
        )
        expected_tap_0 = max(
            -0.12,
            min(0.12, expected_tap_0 + 0.025 * expected_residual * history_0),
        )
        expected_residual = (
            sample_delta
            - expected_tap_1 * history_1
            - expected_tap_0 * history_0
        )
        expected_corrected = max(0.0, min(VDD, VCM + expected_residual))
        decision = 1 if float(row["sample_in"]) >= VCM else -1
        history_0, history_1 = history_1, decision
        sample_enabled = _high(sample, "enable") and not _high(sample, "rst")
        if not sample_enabled:
            # A disable/reset before the observation point clears the DUT, so
            # this edge no longer has a settled enabled result to compare.
            continue
        corrected = float(sample["corrected_out"])
        err = abs(float(sample["error_metric"]))
        if err < 0.035:
            streak += 1
        else:
            streak = 0
        # Ignore the first edge after each observed enable transition while
        # the stateful proxy settles; this is relative to the submitted
        # stimulus, not a hidden absolute timestamp.  It still counts toward
        # the public consecutive-low-error convergence streak.
        if active_edges == 1:
            continue
        checked += 1
        decisions += 1
        error_max = max(error_max, err)
        tap_1 = float(sample["tap_1"]) - VCM
        tap_0 = float(sample["tap_0"]) - VCM
        if (
            abs(tap_1 - expected_tap_1) > 8e-3
            or abs(tap_0 - expected_tap_0) > 8e-3
            or abs(corrected - expected_corrected) > 0.035
        ):
            decision_errors += 1
        # corrected_out is vcm plus the residual proxy.
        if abs(err - abs(corrected - VCM)) > 0.08:
            corr_errors += 1
        converged = _high(sample, "converged")
        if converged and streak < 3:
            conv_errors += 1
        if converged and err > 0.05:
            conv_errors += 1
    ok = (
        checked >= 4
        and reset_clear
        and disabled_clear
        and corr_errors <= max(2, checked // 3)
        and decision_errors == 0
        and conv_errors == 0
        and clear_errors <= 6
    )
    return ok, (
        f"v4_331 checked={checked} decisions={decisions} error_max={error_max:.3f} "
        f"corr_errors={corr_errors} decision_errors={decision_errors} conv_errors={conv_errors} "
        f"reset_clear={reset_clear} disabled_clear={disabled_clear} clear_errors={clear_errors}"
    )

CHECKER_ID = "v4_331_dfe_error_proxy_loop"
CHECKER: Checker = with_property_diagnostics(
    check_v4_331_dfe_error_proxy_loop,
    {
        "P_ON_RESET_OR_WHEN_DISABLED_CLEAR": ("clear_errors", "!reset_clear", "!disabled_clear"),
        "P_ON_EACH_ENABLED_DECISION_CLOCK_LATCH": "decision_errors",
        "P_USE_THE_PREVIOUS_DECISION_HISTORY_TO": "decision_errors",
        "P_EXPOSE_THE_ABSOLUTE_RESIDUAL_ON_ERROR": "corr_errors",
        "P_ASSERT_CONVERGED_WHEN_THE_RESIDUAL_REMAINS": "conv_errors",
    },
)
