"""Task-specific checker for canonical v4 DUT 381."""
from __future__ import annotations

from checkers.api import Checker
def _v4_topup_logic_high(row: dict[str, float], name: str, threshold: float = 0.45) -> bool:
    return float(row.get(name, 0.0)) > threshold

def check_v4_940_fm_vco_modulation_source(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_940 empty_trace"
    checked = metric_errors = clear_errors = 0
    reset_clear = disabled_clear = low_metric = high_metric = osc_activity = marker_activity = valid_seen = False
    osc_vals: list[float] = []
    marker_vals: list[float] = []
    metric_vals: list[float] = []
    for row in rows[::6]:
        t = float(row["time"])
        rst = _v4_topup_logic_high(row, "rst")
        enabled = _v4_topup_logic_high(row, "enable") and not rst
        if not enabled:
            clear = row["osc_out"] < 0.12 and row["freq_metric"] < 0.08 and row["phase_marker"] < 0.12 and row["valid"] < 0.10
            reset_clear = reset_clear or (rst and t < 5e-9 and clear)
            disabled_clear = disabled_clear or (t > 82e-9 and clear)
            if ((rst and t < 5e-9) or t > 82e-9) and not clear:
                clear_errors += 1
            continue
        freq = max(1.0e6, 10.0e6 + 5.0e6 * (float(row["mod_in"]) - 0.45))
        expected_metric = min(0.9, max(0.0, freq / 20.0e6 * 0.9))
        low_metric = low_metric or expected_metric < 0.45
        high_metric = high_metric or expected_metric > 0.45
        osc_vals.append(float(row["osc_out"]))
        marker_vals.append(float(row["phase_marker"]))
        if 14e-9 < t < 80e-9:
            metric_vals.append(float(row["freq_metric"]))
        valid_seen = valid_seen or _v4_topup_logic_high(row, "valid")
        checked += 1
        if abs(float(row["freq_metric"]) - expected_metric) > 0.10:
            metric_errors += 1
    osc_activity = bool(osc_vals) and max(osc_vals) > 0.65 and min(osc_vals) < 0.20
    marker_activity = bool(marker_vals) and max(marker_vals) > 0.65 and min(marker_vals) < 0.20
    metric_span = (max(metric_vals) - min(metric_vals)) if metric_vals else 0.0
    ok = checked >= 12 and reset_clear and disabled_clear and low_metric and high_metric and metric_span >= 0.055 and osc_activity and marker_activity and valid_seen and metric_errors <= 4 and clear_errors <= 4
    return ok, f"v4_940 checked={checked} reset_clear={reset_clear} disabled_clear={disabled_clear} low_metric={low_metric} high_metric={high_metric} metric_span={metric_span:.3g} osc_activity={osc_activity} marker_activity={marker_activity} valid_seen={valid_seen} metric_errors={metric_errors} clear_errors={clear_errors}"

CHECKER_ID = "v4_381_fm_vco_modulation_source"
CHECKER: Checker = check_v4_940_fm_vco_modulation_source
