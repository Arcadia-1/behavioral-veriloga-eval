from __future__ import annotations

from checkers.api import Checker
from checkers.common.issue109_factory import CheckResult, Row, check_clocked_factory


TASK_LABEL = 'v4_262_resettable_phase_toggle_monitor'
SOURCE_TASK_ID = 'v3_353_resettable_phase_toggle_monitor'
LEGACY_SYMBOL = '353-resettable-phase-toggle-monitor'


def check_v4_262_resettable_phase_toggle_monitor(rows: list[Row]) -> CheckResult:
    """Check v4_262_resettable_phase_toggle_monitor: Resettable Phase Toggle Monitor clocked toggle behavior."""
    return check_clocked_factory(rows, mode='toggle', edge=1, task_name=TASK_LABEL)


CHECKS = {
    TASK_LABEL: check_v4_262_resettable_phase_toggle_monitor,
    SOURCE_TASK_ID: check_v4_262_resettable_phase_toggle_monitor,
    LEGACY_SYMBOL: check_v4_262_resettable_phase_toggle_monitor,
}

CHECKER_ID = TASK_LABEL
CHECKER: Checker = check_v4_262_resettable_phase_toggle_monitor
