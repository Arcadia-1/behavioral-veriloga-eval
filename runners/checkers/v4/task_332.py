"""Task-specific checker for canonical v4 DUT 332."""
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

def check_v4_332_polyphase_iq_balance_monitor(rows: list[dict[str, float]]) -> tuple[bool, str]:
    req = {
        "time", "i_in", "q_in", "clk", "rst", "enable",
        "i_out", "q_out", "amp_error_metric", "phase_error_metric", "balanced",
    }
    miss = _missing(rows, req)
    if miss:
        return False, f"v4_332 missing_signals={','.join(miss)}"
    prev_clk = float(rows[0]["clk"])
    checked = norm_errors = bal_errors = clear_errors = 0
    reset_clear = disabled_clear = ever_enabled = False
    disable_time: float | None = None
    active_edges = 0
    amp_max = phase_max = 0.0
    streak = 0
    for row in rows:
        t = float(row["time"])
        clk = float(row["clk"])
        rst = _high(row, "rst")
        enabled = _high(row, "enable") and not rst
        if not enabled:
            clear = (
                abs(float(row["i_out"]) - VCM) < 0.12
                and abs(float(row["q_out"]) - VCM) < 0.12
                and abs(float(row["amp_error_metric"])) < 0.08
                and abs(float(row["phase_error_metric"])) < 0.08
                and not _high(row, "balanced")
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
        # Let the first edge in each observed enable window establish state.
        if active_edges == 1:
            continue
        checked += 1
        i_out = float(row["i_out"])
        q_out = float(row["q_out"])
        if not (0.0 - 0.05 <= i_out <= VDD + 0.05 and 0.0 - 0.05 <= q_out <= VDD + 0.05):
            norm_errors += 1
        amp = abs(float(row["amp_error_metric"]))
        phase = abs(float(row["phase_error_metric"]))
        amp_max = max(amp_max, amp)
        phase_max = max(phase_max, phase)
        i_in = float(row["i_in"])
        q_in = float(row["q_in"])
        expected_amp = abs(abs(i_in - VCM) - abs(q_in - VCM))
        if abs(amp - expected_amp) > 0.10:
            norm_errors += 1
        if amp < 0.08 and phase < 0.08:
            streak += 1
        else:
            streak = 0
        balanced = _high(row, "balanced")
        if balanced and streak < 2:
            bal_errors += 1
        if balanced and (amp > 0.12 or phase > 0.12):
            bal_errors += 1
    ok = (
        checked >= 8
        and reset_clear
        and disabled_clear
        and norm_errors <= max(3, checked // 3)
        and bal_errors <= 3
        and clear_errors <= 6
    )
    return ok, (
        f"v4_332 checked={checked} amp_max={amp_max:.3f} phase_max={phase_max:.3f} "
        f"norm_errors={norm_errors} bal_errors={bal_errors} "
        f"reset_clear={reset_clear} disabled_clear={disabled_clear} clear_errors={clear_errors}"
    )

CHECKER_ID = "v4_332_polyphase_iq_balance_monitor"
CHECKER: Checker = with_property_diagnostics(
    check_v4_332_polyphase_iq_balance_monitor,
    {
        "P_ON_RESET_OR_WHEN_DISABLED_DRIVE": ("clear_errors", "!reset_clear", "!disabled_clear"),
        "P_ON_EACH_ENABLED_RISING_CLK_EDGE": "norm_errors",
        "P_DRIVE_CORRECTED_I_Q_OUTPUTS_WITH": "norm_errors",
        "P_EXPOSE_AMPLITUDE_AND_PHASE_ERROR_PROXIES": "norm_errors",
        "P_ASSERT_BALANCED_ONLY_WHEN_BOTH_METRICS": "bal_errors",
    },
)
