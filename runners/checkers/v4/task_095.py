"""Task-specific checker for canonical v4 DUT 095."""
from __future__ import annotations

from ..api import Checker
def mean_in_window(rows: list[dict[str, float]], key: str, start: float, stop: float) -> float | None:
    values = [r[key] for r in rows if start <= r["time"] <= stop and key in r]
    if not values:
        return None
    return sum(values) / len(values)

def check_ldo_load_step_recovery_flow(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "vin", "out", "metric", "load_mon", "ctrl_mon"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/clk/rst/vin/out/metric/load_mon/ctrl_mon"

    pre_step = mean_in_window(rows, "out", 10.0e-9, 15.0e-9)
    early_droop = mean_in_window(rows, "out", 18.0e-9, 22.0e-9)
    late_recovery = mean_in_window(rows, "out", 34.0e-9, 40.0e-9)
    light_recovery = mean_in_window(rows, "out", 52.0e-9, 60.0e-9)
    second_droop = mean_in_window(rows, "out", 64.0e-9, 68.0e-9)
    late_metric = mean_in_window(rows, "metric", 34.0e-9, 40.0e-9)
    pre_load = mean_in_window(rows, "load_mon", 10.0e-9, 15.0e-9)
    heavy_load = mean_in_window(rows, "load_mon", 18.0e-9, 22.0e-9)
    light_load = mean_in_window(rows, "load_mon", 52.0e-9, 60.0e-9)
    second_load = mean_in_window(rows, "load_mon", 64.0e-9, 68.0e-9)
    pre_ctrl = mean_in_window(rows, "ctrl_mon", 10.0e-9, 15.0e-9)
    heavy_ctrl = mean_in_window(rows, "ctrl_mon", 18.0e-9, 22.0e-9)
    light_ctrl = mean_in_window(rows, "ctrl_mon", 52.0e-9, 60.0e-9)
    second_ctrl = mean_in_window(rows, "ctrl_mon", 64.0e-9, 68.0e-9)
    if None in (
        pre_step,
        early_droop,
        late_recovery,
        light_recovery,
        second_droop,
        late_metric,
        pre_load,
        heavy_load,
        light_load,
        second_load,
        pre_ctrl,
        heavy_ctrl,
        light_ctrl,
        second_ctrl,
    ):
        return False, "ldo_flow_missing_sample_windows"
    assert pre_step is not None
    assert early_droop is not None
    assert late_recovery is not None
    assert light_recovery is not None
    assert second_droop is not None
    assert late_metric is not None
    assert pre_load is not None
    assert heavy_load is not None
    assert light_load is not None
    assert second_load is not None
    assert pre_ctrl is not None
    assert heavy_ctrl is not None
    assert light_ctrl is not None
    assert second_ctrl is not None

    if not (0.56 <= pre_step <= 0.66):
        return False, f"ldo_flow_pre_step_regulation_wrong={pre_step:.3f}"
    if early_droop >= pre_step - 0.04:
        return False, f"ldo_flow_no_transient_droop pre={pre_step:.3f} early={early_droop:.3f}"
    if late_recovery <= early_droop + 0.045:
        return False, f"ldo_flow_no_closed_loop_recovery early={early_droop:.3f} late={late_recovery:.3f}"
    if light_recovery <= late_recovery:
        return False, f"ldo_flow_light_load_not_higher light={light_recovery:.3f} late={late_recovery:.3f}"
    if second_droop >= light_recovery - 0.035:
        return False, f"ldo_flow_second_step_no_droop second={second_droop:.3f} light={light_recovery:.3f}"
    if late_metric < 0.65:
        return False, f"ldo_flow_recovery_metric_low={late_metric:.3f}"
    if heavy_load <= pre_load + 0.45 or light_load >= heavy_load - 0.35 or second_load <= light_load + 0.35:
        return False, (
            f"ldo_flow_load_monitor_wrong pre/heavy/light/second="
            f"{pre_load:.3f}/{heavy_load:.3f}/{light_load:.3f}/{second_load:.3f}"
        )
    if heavy_ctrl <= pre_ctrl + 0.12:
        return False, f"ldo_flow_ctrl_no_heavy_load_response pre={pre_ctrl:.3f} heavy={heavy_ctrl:.3f}"
    if light_ctrl >= heavy_ctrl - 0.08:
        return False, f"ldo_flow_ctrl_not_reduced_at_light_load light={light_ctrl:.3f} heavy={heavy_ctrl:.3f}"
    if second_ctrl <= light_ctrl + 0.08:
        return False, f"ldo_flow_ctrl_no_second_step_response second={second_ctrl:.3f} light={light_ctrl:.3f}"
    return True, (
        "ldo_load_step_recovery_flow "
        f"pre/early/late/light/second={pre_step:.3f}/{early_droop:.3f}/"
        f"{late_recovery:.3f}/{light_recovery:.3f}/{second_droop:.3f} "
        f"load={pre_load:.3f}/{heavy_load:.3f}/{light_load:.3f}/{second_load:.3f} "
        f"ctrl={pre_ctrl:.3f}/{heavy_ctrl:.3f}/{light_ctrl:.3f}/{second_ctrl:.3f}"
    )

CHECKER_ID = "v4_095_ldo_load_step_recovery"
CHECKER: Checker = check_ldo_load_step_recovery_flow
