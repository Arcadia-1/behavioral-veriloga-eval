"""Task-specific checker for canonical v4 DUT 041."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import diagnostic, pass_note, require_signals


PROPERTY_IDS = (
    "P_RESET_COMMON_MODE",
    "P_LO_POLARITY",
    "P_DOWNCONVERSION_TRANSFER",
    "P_ACTIVE_METRIC",
    "P_OUTPUT_CLAMP",
)


def _mean_where(
    rows: list[dict[str, float]], key: str, predicate
) -> float | None:
    values = [row[key] for row in rows if predicate(row)]
    return sum(values) / len(values) if values else None


def _interp(a: dict[str, float], b: dict[str, float], time_s: float, field: str) -> float:
    t0 = a["time"]
    t1 = b["time"]
    if t1 <= t0:
        return a[field]
    frac = max(0.0, min(1.0, (time_s - t0) / (t1 - t0)))
    return a[field] + frac * (b[field] - a[field])


def _mean_selected(
    rows: list[dict[str, float]],
    key: str,
    *,
    clk_high: bool,
    vin_high: bool,
) -> float | None:
    total = 0.0
    duration = 0.0
    for row, nxt in zip(rows, rows[1:]):
        left = row["time"]
        right = nxt["time"]
        if right <= left:
            continue
        mid = 0.5 * (left + right)
        rst_mid = _interp(row, nxt, mid, "rst")
        clk_mid = _interp(row, nxt, mid, "clk")
        vin_mid = _interp(row, nxt, mid, "vin")
        if rst_mid > 0.45:
            continue
        if clk_high and clk_mid <= 0.75:
            continue
        if (not clk_high) and clk_mid >= 0.15:
            continue
        if vin_high and vin_mid <= 0.55:
            continue
        if (not vin_high) and vin_mid >= 0.38:
            continue
        value_left = _interp(row, nxt, left, key)
        value_right = _interp(row, nxt, right, key)
        total += 0.5 * (value_left + value_right) * (right - left)
        duration += right - left
    if duration <= 0.0:
        return None
    return total / duration

def check_rf_mixer_downconverter_macro(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "vin", "out", "metric"}
    missing = require_signals(rows, required, "P_DOWNCONVERSION_TRANSFER")
    if missing:
        return False, missing

    pos_hi = _mean_selected(rows, "out", clk_high=True, vin_high=True)
    pos_lo = _mean_selected(rows, "out", clk_high=False, vin_high=True)
    neg_hi = _mean_selected(rows, "out", clk_high=True, vin_high=False)
    neg_lo = _mean_selected(rows, "out", clk_high=False, vin_high=False)
    active_metric = _mean_where(rows, "metric", lambda row: row["rst"] <= 0.45)
    if None in (pos_hi, pos_lo, neg_hi, neg_lo, active_metric):
        return False, diagnostic(
            "P_DOWNCONVERSION_TRANSFER",
            "insufficient_excitation",
            expected="clk_high/clk_low at high and low vin after reset",
            observed="missing_observable_event_bin",
            event="observed_clk_vin_regions",
        )
    assert pos_hi is not None
    assert pos_lo is not None
    assert neg_hi is not None
    assert neg_lo is not None
    assert active_metric is not None

    if pos_hi <= 0.58 or pos_lo >= 0.34:
        return False, diagnostic(
            "P_LO_POLARITY",
            "behavior_mismatch",
            expected="high_vin:out_hi>0.58,out_lo<0.34",
            observed=f"out_hi={pos_hi:.3f},out_lo={pos_lo:.3f}",
            event="high_vin_clk_polarity",
        )
    if neg_hi >= 0.34 or neg_lo <= 0.56:
        return False, diagnostic(
            "P_LO_POLARITY",
            "behavior_mismatch",
            expected="low_vin:out_hi<0.34,out_lo>0.56",
            observed=f"out_hi={neg_hi:.3f},out_lo={neg_lo:.3f}",
            event="low_vin_clk_polarity",
        )
    if active_metric < 0.40:
        return False, diagnostic(
            "P_ACTIVE_METRIC",
            "behavior_mismatch",
            expected="metric_mean>=0.40",
            observed=f"metric_mean={active_metric:.3f}",
            event="post_reset_trace",
        )
    return True, pass_note(PROPERTY_IDS, (
        "rf_mixer_downconverter_macro "
        f"pos={pos_hi:.3f}/{pos_lo:.3f} neg={neg_hi:.3f}/{neg_lo:.3f}"
    ))

CHECKER_ID = "v4_041_rf_mixer_downconverter_macro"
CHECKER: Checker = check_rf_mixer_downconverter_macro
