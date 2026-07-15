"""Task-specific checker for canonical v4 DUT 333."""
from __future__ import annotations

from ..api import Checker
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
    image_min = 1e9
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
                and abs(float(row["image_metric"])) < 0.08
                and not _high(row, "calibrated")
            )
            if rst and clear:
                reset_clear = True
            if ever_enabled and (not _high(row, "enable")) and clear:
                disabled_clear = True
            if (rst or (ever_enabled and not _high(row, "enable") and disabled_clear)) and not clear:
                clear_errors += 1
            streak = 0
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
        rf = float(row["rf_in"])
        lo_i = float(row["lo_i"])
        lo_q = float(row["lo_q"])
        i_out = float(row["i_out"])
        q_out = float(row["q_out"])
        # proxy mixer polarity around vcm
        i_exp = VCM + (rf - VCM) * (1.0 if lo_i > VCM else -1.0) * 0.5
        q_exp = VCM + (rf - VCM) * (1.0 if lo_q > VCM else -1.0) * 0.5
        if abs(i_out - i_exp) > 0.25:
            mixer_errors += 1
        if abs(q_out - q_exp) > 0.25:
            mixer_errors += 1
        image = abs(float(row["image_metric"]))
        image_min = min(image_min, image)
        if image < 0.04:
            streak += 1
        else:
            streak = 0
        calibrated = _high(row, "calibrated")
        if calibrated and streak < 3:
            cal_errors += 1
        if calibrated and image > 0.06:
            cal_errors += 1
    if image_min > 1e8:
        image_min = 0.0
    ok = (
        checked >= 8
        and reset_clear
        and disabled_clear
        and mixer_errors <= max(4, checked // 2)
        and cal_errors <= 3
        and clear_errors <= 6
    )
    return ok, (
        f"v4_333 checked={checked} image_min={image_min:.3f} "
        f"mixer_errors={mixer_errors} cal_errors={cal_errors} "
        f"reset_clear={reset_clear} disabled_clear={disabled_clear} clear_errors={clear_errors}"
    )

CHECKER_ID = "v4_333_image_reject_mixer_calibration_loop"
CHECKER: Checker = check_v4_333_image_reject_mixer_calibration_loop
