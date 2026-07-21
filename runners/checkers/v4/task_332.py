"""Task-specific checker for canonical v4 DUT 332."""
from __future__ import annotations

from ..api import Checker
from .diagnostics import with_property_diagnostics
from ..common.relative_events import rising_edges, sample_after_event
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

    expected_streak = 0
    oracle_checked = oracle_errors = phase_errors = output_errors = balanced_errors = 0
    for edge_time in rising_edges(rows, "clk"):
        edge_index = next(
            (index for index, row in enumerate(rows) if float(row["time"]) >= edge_time),
            None,
        )
        if edge_index is None:
            continue
        stimulus = rows[max(0, edge_index - 1)]
        active = _high(stimulus, "enable") and not _high(stimulus, "rst")
        if not active:
            expected_streak = 0
            continue
        i_sample = max(0.0, min(VDD, float(stimulus["i_in"])))
        q_sample = max(0.0, min(VDD, float(stimulus["q_in"])))
        i_dev = i_sample - VCM
        q_dev = q_sample - VCM
        max_dev = max(abs(i_dev), abs(q_dev))
        scale = 0.22 / max_dev if max_dev > 0.22 else 1.0
        expected_i = max(0.0, min(VDD, VCM + i_dev * scale))
        expected_q = max(0.0, min(VDD, VCM + q_dev * scale))
        expected_amp = abs(abs(i_dev) - abs(q_dev))
        expected_phase = abs(i_dev + q_dev)
        if expected_amp < 45e-3 and expected_phase < 60e-3:
            expected_streak += 1
        else:
            expected_streak = 0
        post = sample_after_event(
            rows,
            edge_time,
            clock_signal="clk",
            fraction_of_period=0.20,
        )
        if post is None:
            continue
        if not _high(post, "enable") or _high(post, "rst"):
            expected_streak = 0
            continue
        output_bad = (
            abs(float(post["i_out"]) - expected_i) > 0.07
            or abs(float(post["q_out"]) - expected_q) > 0.07
        )
        phase_bad = abs(float(post["phase_error_metric"]) - expected_phase) > 0.07
        balanced_bad = _high(post, "balanced") != (expected_streak >= 2)
        oracle_checked += 1
        output_errors += int(output_bad)
        phase_errors += int(phase_bad)
        balanced_errors += int(balanced_bad)
        if (
            output_bad
            or abs(float(post["amp_error_metric"]) - expected_amp) > 0.07
            or phase_bad
            or balanced_bad
        ):
            oracle_errors += 1
    prev_clk = float(rows[0]["clk"])
    checked = norm_errors = bal_errors = clear_errors = 0
    reset_clear = disabled_clear = ever_enabled = False
    disable_time: float | None = None
    reset_time: float | None = None
    active_edges = 0
    amp_max = phase_max = 0.0
    streak = 0
    for row in rows:
        t = float(row["time"])
        clk = float(row["clk"])
        rst = _high(row, "rst")
        enabled = _high(row, "enable") and not rst
        if not enabled:
            if rst and reset_time is None:
                reset_time = t
            reset_ready = (
                rst
                and reset_time is not None
                and t >= reset_time + 0.7e-9
            )
            clear = (
                abs(float(row["i_out"]) - VCM) < 0.12
                and abs(float(row["q_out"]) - VCM) < 0.12
                and abs(float(row["amp_error_metric"])) < 0.08
                and abs(float(row["phase_error_metric"])) < 0.08
                and not _high(row, "balanced")
            )
            if reset_ready and clear:
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
            if (reset_ready or disabled_ready) and not clear:
                clear_errors += 1
            streak = 0
            active_edges = 0
            prev_clk = clk
            continue
        ever_enabled = True
        reset_time = None
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
        checked >= 6
        and oracle_checked >= 6
        and oracle_errors == 0
        and reset_clear
        and disabled_clear
        and norm_errors <= max(3, checked // 3)
        and bal_errors <= 3
        and clear_errors <= 6
    )
    return ok, (
        f"v4_332 checked={checked} amp_max={amp_max:.3f} phase_max={phase_max:.3f} "
        f"oracle_checked={oracle_checked} oracle_errors={oracle_errors} output_errors={output_errors} "
        f"phase_errors={phase_errors} balanced_errors={balanced_errors} norm_errors={norm_errors} bal_errors={bal_errors} "
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
