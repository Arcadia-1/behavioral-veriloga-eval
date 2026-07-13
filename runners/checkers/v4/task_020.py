"""Task-specific checker for canonical v4 DUT 020."""
from __future__ import annotations

from checkers.api import Checker
def mean_in_window(rows: list[dict[str, float]], key: str, start: float, stop: float) -> float | None:
    values = [r[key] for r in rows if start <= r["time"] <= stop and key in r]
    if not values:
        return None
    return sum(values) / len(values)

def check_bandgap_reference_macro_model(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "vin", "out", "metric"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/clk/rst/vin/out/metric"

    pre_start = mean_in_window(rows, "out", 4.0e-9, 7.5e-9)
    nominal_ref = mean_in_window(rows, "out", 27.0e-9, 36.0e-9)
    high_supply_ref = mean_in_window(rows, "out", 55.0e-9, 63.0e-9)
    brownout_ref = mean_in_window(rows, "out", 67.0e-9, 70.0e-9)
    valid_metric = mean_in_window(rows, "metric", 30.0e-9, 62.0e-9)
    if None in (pre_start, nominal_ref, high_supply_ref, brownout_ref, valid_metric):
        return False, "bandgap_missing_sample_windows"
    assert pre_start is not None
    assert nominal_ref is not None
    assert high_supply_ref is not None
    assert brownout_ref is not None
    assert valid_metric is not None

    if pre_start > 0.08:
        return False, f"bandgap_reference_not_held_low_pre_start={pre_start:.3f}"
    if not (0.50 <= nominal_ref <= 0.60):
        return False, f"bandgap_reference_nominal_wrong={nominal_ref:.3f}"
    line_delta = abs(high_supply_ref - nominal_ref)
    if line_delta > 0.065:
        return False, f"bandgap_line_regulation_too_large={line_delta:.3f}"
    if brownout_ref > 0.12:
        return False, f"bandgap_brownout_not_reset={brownout_ref:.3f}"
    if valid_metric < 0.65:
        return False, f"bandgap_valid_metric_low={valid_metric:.3f}"
    return True, (
        "bandgap_reference_macro_model "
        f"ref={nominal_ref:.3f}/{high_supply_ref:.3f} line_delta={line_delta:.3f} "
        f"brownout={brownout_ref:.3f}"
    )

CHECKER_ID = "v4_020_bandgap_reference_macro_model"
CHECKER: Checker = check_bandgap_reference_macro_model
