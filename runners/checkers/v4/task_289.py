from __future__ import annotations

from checkers.api import Checker
from checkers.common.issue109_split import check_clocked


TASK_LABEL = "v4_289_iterative_decay_estimator"
SOURCE_TASK_ID = "v3_458_iterative_decay_estimator"
TRACE_SIGNALS = ("time", "clk", "rst", "in0", "in1", "in2", "in3", "ctrl0", "ctrl1", "vdd", "vss", "en", "out", "flag", "metric")
PROPERTIES = (
    "clocked iterative decay state replaces recursive helper behavior",
    "state update is clip01(0.62*state + 0.32*aux)",
    "flag asserts when state exceeds 0.58 and metric reports aux",
)


def check_v4_289_iterative_decay_estimator(rows: list[dict[str, float]]) -> tuple[bool, str]:
    return check_clocked(rows, "accum", TASK_LABEL)


CHECKS = {
    TASK_LABEL: check_v4_289_iterative_decay_estimator,
    SOURCE_TASK_ID: check_v4_289_iterative_decay_estimator,
    "458-iterative-decay-estimator": check_v4_289_iterative_decay_estimator,
}

CHECKER_ID = TASK_LABEL
CHECKER: Checker = check_v4_289_iterative_decay_estimator
