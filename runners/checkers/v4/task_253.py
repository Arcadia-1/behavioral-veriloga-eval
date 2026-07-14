from __future__ import annotations

from checkers.api import Checker
from checkers.common.issue109_factory import CheckResult, Row, check_continuous_factory


TASK_LABEL = 'v4_253_power_mode_clamped_mux'
SOURCE_TASK_ID = 'v3_344_power_mode_clamped_mux'
LEGACY_SYMBOL = '344-power-mode-clamped-mux'


def check_v4_253_power_mode_clamped_mux(rows: list[Row]) -> CheckResult:
    """Check v4_253_power_mode_clamped_mux: Power Mode Clamped Mux continuous mux behavior."""
    return check_continuous_factory(rows, mode='mux', task_name=TASK_LABEL)


CHECKS = {
    TASK_LABEL: check_v4_253_power_mode_clamped_mux,
    SOURCE_TASK_ID: check_v4_253_power_mode_clamped_mux,
    LEGACY_SYMBOL: check_v4_253_power_mode_clamped_mux,
}

CHECKER_ID = TASK_LABEL
CHECKER: Checker = check_v4_253_power_mode_clamped_mux
