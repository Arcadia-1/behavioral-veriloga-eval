"""Task-specific checker for canonical v4 DUT 099."""
from __future__ import annotations

from checkers.api import Checker
def mean_in_window(rows: list[dict[str, float]], key: str, start: float, stop: float) -> float | None:
    values = [r[key] for r in rows if start <= r["time"] <= stop and key in r]
    if not values:
        return None
    return sum(values) / len(values)

def check_reference_startup_enable_flow(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "out", "metric"}
    has_legacy_vin = bool(rows and "vin" in rows[0])
    if has_legacy_vin:
        required.add("vin")
    else:
        required.update({"vdd_in", "en"})
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0].keys())) if rows else sorted(required)
        return False, f"missing_columns={','.join(missing)}"

    supply_off = mean_in_window(rows, "out", 5.0e-9, 9.0e-9)
    pre_enable = mean_in_window(rows, "out", 15.0e-9, 22.0e-9)
    startup_ref = mean_in_window(rows, "out", 39.0e-9, 52.0e-9)
    startup_metric = mean_in_window(rows, "metric", 39.0e-9, 52.0e-9)
    dip_reset = mean_in_window(rows, "out", 57.0e-9, 61.0e-9)
    recovered_metric = mean_in_window(rows, "metric", 74.0e-9, 79.0e-9)
    if has_legacy_vin:
        pre_supply = pre_vin = mean_in_window(rows, "vin", 15.0e-9, 22.0e-9)
        startup_supply = startup_vin = mean_in_window(rows, "vin", 39.0e-9, 52.0e-9)
        dip_supply = dip_vin = mean_in_window(rows, "vin", 57.0e-9, 61.0e-9)
        pre_en = 0.0
        startup_en = 0.9
    else:
        pre_supply = mean_in_window(rows, "vdd_in", 15.0e-9, 22.0e-9)
        startup_supply = mean_in_window(rows, "vdd_in", 39.0e-9, 52.0e-9)
        dip_supply = mean_in_window(rows, "vdd_in", 57.0e-9, 61.0e-9)
        pre_en = mean_in_window(rows, "en", 15.0e-9, 22.0e-9)
        startup_en = mean_in_window(rows, "en", 39.0e-9, 52.0e-9)
        pre_vin = pre_supply
        startup_vin = startup_supply
        dip_vin = dip_supply
    if None in (
        supply_off,
        pre_enable,
        startup_ref,
        startup_metric,
        dip_reset,
        recovered_metric,
        pre_supply,
        startup_supply,
        dip_supply,
        pre_en,
        startup_en,
    ):
        return False, "ref_startup_missing_sample_windows"
    assert supply_off is not None
    assert pre_enable is not None
    assert startup_ref is not None
    assert startup_metric is not None
    assert dip_reset is not None
    assert recovered_metric is not None
    assert pre_supply is not None
    assert startup_supply is not None
    assert dip_supply is not None
    assert pre_en is not None
    assert startup_en is not None

    if supply_off > 0.08:
        return False, f"ref_startup_supply_off_not_low={supply_off:.3f}"
    if pre_enable > 0.12:
        return False, f"ref_startup_ignores_enable={pre_enable:.3f}"
    if has_legacy_vin:
        assert pre_vin is not None
        if not (0.32 < pre_vin < 0.55):
            return False, f"ref_startup_pre_enable_vin_wrong={pre_vin:.3f}"
    elif pre_supply <= 0.55 or pre_en >= 0.20:
        return False, f"ref_startup_pre_enable_inputs_wrong supply={pre_supply:.3f} en={pre_en:.3f}"
    if startup_ref < 0.48 or startup_ref > 0.60:
        return False, f"ref_startup_wrong_reference={startup_ref:.3f}"
    if startup_metric < 0.65:
        return False, f"ref_startup_valid_metric_low={startup_metric:.3f}"
    if startup_supply <= 0.55 or startup_en <= 0.55:
        return False, f"ref_startup_enable_window_inputs_low supply={startup_supply:.3f} en={startup_en:.3f}"
    if dip_reset > 0.10:
        return False, f"ref_startup_supply_dip_not_reset={dip_reset:.3f}"
    if dip_supply >= 0.32:
        return False, f"ref_startup_dip_supply_high={dip_supply:.3f}"
    if recovered_metric < 0.45:
        return False, f"ref_startup_no_recovery_metric={recovered_metric:.3f}"
    return True, (
        "reference_startup_enable_flow "
        f"pre_enable={pre_enable:.3f} startup={startup_ref:.3f} "
        f"metric={startup_metric:.3f}->{recovered_metric:.3f} dip={dip_reset:.3f}"
    )

CHECKER_ID = "v4_099_reference_startup_enable_flow"
CHECKER: Checker = check_reference_startup_enable_flow
