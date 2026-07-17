"""Task-specific checker for canonical v4 DUT 333."""
from __future__ import annotations

from bisect import bisect_left

from ..api import Checker
from .diagnostics import with_property_diagnostics
VCM = 0.45
VTH = 0.45

def _high(row: dict[str, float], name: str, thr: float = VTH) -> bool:
    return float(row.get(name, 0.0)) > thr

def _rising(prev: float, now: float, thr: float = VTH) -> bool:
    return now > thr and prev <= thr

def _missing(rows: list[dict[str, float]], required: set[str]) -> list[str]:
    if not rows:
        return sorted(required)
    return sorted(required - set(rows[0].keys()))

def check_v4_333_image_reject_mixer_calibration_loop(rows: list[dict[str, float]]) -> tuple[bool, str]:
    req = {
        "time", "rf_in", "lo_i", "lo_q", "clk", "rst", "enable",
        "i_out", "q_out", "image_metric", "calibrated",
    }
    miss = _missing(rows, req)
    if miss:
        return False, f"v4_333 missing_signals={','.join(miss)}"
    prev_clk = float(rows[0]["clk"])
    checked = mixer_errors = cal_errors = clear_errors = 0
    reset_clear = disabled_clear = ever_enabled = False
    disable_time: float | None = None
    active_edges = 0
    image_min = 1e9
    streak = 0
    gain_trim = VCM
    phase_trim = VCM
    direction = 1
    times = [float(row["time"]) for row in rows]

    def mix(row: dict[str, float], gain: float, phase: float) -> tuple[float, float, float]:
        x = float(row["rf_in"]) - VCM
        si = 1.0 if float(row["lo_i"]) > VTH else -1.0
        sq = 1.0 if float(row["lo_q"]) > VTH else -1.0
        g = 0.8 * (gain - VCM)
        p = 0.6 * (phase - VCM)
        i = x * si * (1.0 - g)
        q = -x * sq * (1.0 + g) - p * x * si
        return (
            max(0.0, min(0.9, VCM + i)),
            max(0.0, min(0.9, VCM + q)),
            max(0.0, min(0.9, 0.5 * abs(i + q))),
        )
    for row in rows:
        t = float(row["time"])
        clk = float(row["clk"])
        rst = _high(row, "rst")
        enabled = _high(row, "enable") and not rst
        if not enabled:
            clear = (
                abs(float(row["i_out"]) - VCM) < 0.12
                and abs(float(row["q_out"]) - VCM) < 0.12
                and abs(float(row["image_metric"])) < 0.08
                and not _high(row, "calibrated")
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
            gain_trim = VCM
            phase_trim = VCM
            direction = 1
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
        _, _, sampled_image = mix(row, gain_trim, phase_trim)
        image_min = min(image_min, sampled_image)
        if sampled_image < 0.04:
            streak += 1
            gain_trim = VCM + 0.5 * (gain_trim - VCM)
            phase_trim = VCM + 0.5 * (phase_trim - VCM)
        else:
            streak = 0
            gain_trim = max(VCM - 0.18, min(VCM + 0.18, gain_trim + direction * 18e-3))
            phase_trim = max(VCM - 0.18, min(VCM + 0.18, phase_trim - direction * 9e-3))
            direction = -direction
        expected_calibrated = streak >= 3
        sample_index = min(len(rows) - 1, bisect_left(times, t + 0.7e-9))
        sample = rows[sample_index]
        if _high(sample, "rst") or not _high(sample, "enable"):
            continue
        checked += 1
        i_exp, q_exp, _ = mix(sample, gain_trim, phase_trim)
        if abs(float(sample["i_out"]) - i_exp) > 0.08:
            mixer_errors += 1
        if abs(float(sample["q_out"]) - q_exp) > 0.08:
            mixer_errors += 1
        if abs(float(sample["image_metric"]) - sampled_image) > 0.08:
            mixer_errors += 1
        calibrated = _high(sample, "calibrated")
        if calibrated != expected_calibrated:
            cal_errors += 1
    if image_min > 1e8:
        image_min = 0.0
    ok = (
        checked >= 8
        and reset_clear
        and disabled_clear
        and mixer_errors == 0
        and cal_errors == 0
        and clear_errors <= 6
    )
    return ok, (
        f"v4_333 checked={checked} image_min={image_min:.3f} "
        f"mixer_errors={mixer_errors} cal_errors={cal_errors} "
        f"reset_clear={reset_clear} disabled_clear={disabled_clear} clear_errors={clear_errors}"
    )

CHECKER_ID = "v4_333_image_reject_mixer_calibration_loop"
CHECKER: Checker = with_property_diagnostics(
    check_v4_333_image_reject_mixer_calibration_loop,
    {
        "P_ON_RESET_OR_WHEN_DISABLED_CLEAR": ("clear_errors", "!reset_clear", "!disabled_clear"),
        "P_ON_EACH_ENABLED_RISING_CLK_EDGE": "mixer_errors",
        "P_GENERATE_I_AND_Q_OUTPUTS_USING": "mixer_errors",
        "P_UPDATE_A_SIMPLE_GAIN_PHASE_CORRECTION": "mixer_errors",
        "P_ASSERT_CALIBRATED_AFTER_THREE_CONSECUTIVE_UPDA": "cal_errors",
    },
)
