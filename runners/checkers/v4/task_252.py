from __future__ import annotations

from ..api import Checker
from ..common.issue109_factory import CheckResult, Row, check_continuous_factory
from .factory_property_diagnostics import append_continuous_property_diagnostics


TASK_LABEL = 'v4_252_supply_qualified_window_flag'
SOURCE_TASK_ID = 'v3_343_supply_qualified_window_flag'
LEGACY_SYMBOL = '343-supply-qualified-window-flag'


def check_v4_252_supply_qualified_window_flag(rows: list[Row]) -> CheckResult:
    """Check v4_252_supply_qualified_window_flag: Supply Qualified Window Flag continuous window behavior."""
    ok, note = check_continuous_factory(rows, mode='window', task_name=TASK_LABEL)
    return ok, append_continuous_property_diagnostics(
        rows,
        note,
        mode='window',
        normalization_property_id='P_MEASURE_ANALOG_INPUTS_RELATIVE_TO_THE',
        function_property_id='P_WHEN_VALID_DRIVE_OUT_VHI_CLIP01',
    )


CHECKS = {
    TASK_LABEL: check_v4_252_supply_qualified_window_flag,
    SOURCE_TASK_ID: check_v4_252_supply_qualified_window_flag,
    LEGACY_SYMBOL: check_v4_252_supply_qualified_window_flag,
}

CHECKER_ID = TASK_LABEL
CHECKER: Checker = check_v4_252_supply_qualified_window_flag
