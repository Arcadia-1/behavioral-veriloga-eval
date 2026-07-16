from __future__ import annotations

from ..api import Checker
from ..common.issue109_factory import CheckResult, Row, check_continuous_factory
from .factory_property_diagnostics import append_continuous_property_diagnostics


TASK_LABEL = 'v4_253_power_mode_clamped_mux'
SOURCE_TASK_ID = 'v3_344_power_mode_clamped_mux'
LEGACY_SYMBOL = '344-power-mode-clamped-mux'


def check_v4_253_power_mode_clamped_mux(rows: list[Row]) -> CheckResult:
    """Check v4_253_power_mode_clamped_mux: Power Mode Clamped Mux continuous mux behavior."""
    ok, note = check_continuous_factory(rows, mode='mux', task_name=TASK_LABEL)
    return ok, append_continuous_property_diagnostics(
        rows,
        note,
        mode='mux',
        normalization_property_id='P_MEASURE_ANALOG_INPUTS_RELATIVE_TO_THE',
        function_property_id='P_USE_THE_TWO_CONTROL_LEVELS_AS',
    )


CHECKS = {
    TASK_LABEL: check_v4_253_power_mode_clamped_mux,
    SOURCE_TASK_ID: check_v4_253_power_mode_clamped_mux,
    LEGACY_SYMBOL: check_v4_253_power_mode_clamped_mux,
}

CHECKER_ID = TASK_LABEL
CHECKER: Checker = check_v4_253_power_mode_clamped_mux
