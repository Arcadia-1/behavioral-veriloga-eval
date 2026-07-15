from __future__ import annotations

from ..api import Checker
from ..common.issue109_factory import CheckResult, Row, check_continuous_factory


TASK_LABEL = 'v4_268_mode_selected_bias_driver'
SOURCE_TASK_ID = 'v3_360_mode_selected_bias_driver'
LEGACY_SYMBOL = '360-mode-selected-bias-driver'


def check_v4_268_mode_selected_bias_driver(rows: list[Row]) -> CheckResult:
    """Check v4_268_mode_selected_bias_driver: Mode Selected Bias Driver continuous mux behavior."""
    return check_continuous_factory(rows, mode='mux', task_name=TASK_LABEL)


CHECKS = {
    TASK_LABEL: check_v4_268_mode_selected_bias_driver,
    SOURCE_TASK_ID: check_v4_268_mode_selected_bias_driver,
    LEGACY_SYMBOL: check_v4_268_mode_selected_bias_driver,
}

CHECKER_ID = TASK_LABEL
CHECKER: Checker = check_v4_268_mode_selected_bias_driver
