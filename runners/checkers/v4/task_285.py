from __future__ import annotations

from ..api import Checker
from ..common.issue109_split import check_continuous


TASK_LABEL = "v4_285_configurable_startup_policy"
SOURCE_TASK_ID = "v3_433_configurable_startup_policy"
TRACE_SIGNALS = ("time", "in0", "in1", "in2", "in3", "ctrl0", "ctrl1", "vdd", "vss", "en", "out", "flag", "metric")
PROPERTIES = (
    "continuous startup policy over normalized x0",
    "flag asserts only inside the x0 startup window and when c0 qualifies policy",
    "metric reports bounded distance from the window center",
)


def check_v4_285_configurable_startup_policy(rows: list[dict[str, float]]) -> tuple[bool, str]:
    return check_continuous(rows, "window", TASK_LABEL)


CHECKS = {
    TASK_LABEL: check_v4_285_configurable_startup_policy,
    SOURCE_TASK_ID: check_v4_285_configurable_startup_policy,
    "433-configurable-startup-policy": check_v4_285_configurable_startup_policy,
}

CHECKER_ID = TASK_LABEL
CHECKER: Checker = check_v4_285_configurable_startup_policy
