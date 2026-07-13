from __future__ import annotations

from checkers.api import Checker
from checkers.common.issue109_factory import CheckResult, Row, check_clocked_factory


TASK_LABEL = 'v4_267_clocked_power_ready_sampler'
SOURCE_TASK_ID = 'v3_359_clocked_power_ready_sampler'
LEGACY_SYMBOL = '359-clocked-power-ready-sampler'


def check_v4_267_clocked_power_ready_sampler(rows: list[Row]) -> CheckResult:
    """Check v4_267_clocked_power_ready_sampler: Clocked Power Ready Sampler clocked counter behavior."""
    return check_clocked_factory(rows, mode='counter', edge=1, task_name=TASK_LABEL)


CHECKS = {
    TASK_LABEL: check_v4_267_clocked_power_ready_sampler,
    SOURCE_TASK_ID: check_v4_267_clocked_power_ready_sampler,
    LEGACY_SYMBOL: check_v4_267_clocked_power_ready_sampler,
}

CHECKER_ID = TASK_LABEL
CHECKER: Checker = check_v4_267_clocked_power_ready_sampler
