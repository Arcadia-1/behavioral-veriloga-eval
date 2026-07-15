"""Task-specific checker for canonical v4 DUT 037."""
from __future__ import annotations

from ..api import Checker
def mean_in_window(rows: list[dict[str, float]], key: str, start: float, stop: float) -> float | None:
    values = [r[key] for r in rows if start <= r["time"] <= stop and key in r]
    if not values:
        return None
    return sum(values) / len(values)

def check_precision_rectifier_envelope_detector(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "vin", "rect", "env", "metric"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/clk/rst/vin/rect/env/metric"

    reset_rect = mean_in_window(rows, "rect", 0.5e-9, 2.0e-9)
    reset_env = mean_in_window(rows, "env", 0.5e-9, 2.0e-9)
    pos_rect = mean_in_window(rows, "rect", 7.0e-9, 10.0e-9)
    center_rect = mean_in_window(rows, "rect", 15.0e-9, 17.0e-9)
    neg_rect = mean_in_window(rows, "rect", 22.0e-9, 26.0e-9)
    peak_env = mean_in_window(rows, "env", 43.0e-9, 48.0e-9)
    hold_env = mean_in_window(rows, "env", 56.0e-9, 64.0e-9)
    hold_rect = mean_in_window(rows, "rect", 56.0e-9, 64.0e-9)
    hold_metric = mean_in_window(rows, "metric", 56.0e-9, 64.0e-9)
    required_windows = (
        reset_rect,
        reset_env,
        pos_rect,
        center_rect,
        neg_rect,
        peak_env,
        hold_env,
        hold_rect,
        hold_metric,
    )
    if None in required_windows:
        return False, "rectifier_missing_sample_windows"
    assert reset_rect is not None
    assert reset_env is not None
    assert pos_rect is not None
    assert center_rect is not None
    assert neg_rect is not None
    assert peak_env is not None
    assert hold_env is not None
    assert hold_rect is not None
    assert hold_metric is not None

    if abs(reset_rect - 0.45) > 0.10 or abs(reset_env - 0.45) > 0.10:
        return False, f"rectifier_reset_common_mode rect={reset_rect:.3f} env={reset_env:.3f}"
    if pos_rect < 0.62:
        return False, f"rectifier_positive_half_not_rectified={pos_rect:.3f}"
    if neg_rect < 0.62:
        return False, f"rectifier_negative_half_not_rectified={neg_rect:.3f}"
    if abs(center_rect - 0.45) > 0.08:
        return False, f"rectifier_center_not_common_mode={center_rect:.3f}"
    if peak_env < 0.74:
        return False, f"rectifier_envelope_peak_too_low={peak_env:.3f}"
    if hold_env < hold_rect + 0.10 or hold_metric < 0.35:
        return False, (
            "rectifier_envelope_hold_missing "
            f"env={hold_env:.3f} rect={hold_rect:.3f} metric={hold_metric:.3f}"
        )

    post = [r for r in rows if r["rst"] <= 0.45 and r["time"] > 3e-9]
    if not post:
        return False, "rectifier_no_post_reset_rows"
    below_rect = sum(1 for r in post if r["env"] + 0.06 < r["rect"])
    if below_rect > max(2, len(post) // 20):
        return False, f"rectifier_envelope_below_rect_count={below_rect}"

    selected = [r for r in post if 5e-9 <= r["time"] <= 30e-9 or 40e-9 <= r["time"] <= 68e-9]
    errors = [abs(r["rect"] - min(0.9, 0.45 + abs(r["vin"] - 0.45))) for r in selected]
    if errors:
        p90 = sorted(errors)[int(0.90 * (len(errors) - 1))]
        if p90 > 0.09:
            return False, f"rectifier_rect_abs_tracking_p90={p90:.3f}"

    return True, (
        "precision_rectifier_envelope_detector "
        f"pos/neg={pos_rect:.3f}/{neg_rect:.3f} env_peak={peak_env:.3f} "
        f"hold={hold_env:.3f}/{hold_rect:.3f}"
    )

CHECKER_ID = "v4_037_precision_rectifier_envelope_detector"
CHECKER: Checker = check_precision_rectifier_envelope_detector
