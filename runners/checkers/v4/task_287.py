from __future__ import annotations

from checkers.api import Checker
from checkers.common.issue109_split import check_clocked


TASK_LABEL = "v4_287_edge_delay_qualified_driver"
SOURCE_TASK_ID = "v3_453_edge_delay_qualified_driver"
TRACE_SIGNALS = ("time", "clk", "rst", "in0", "in1", "in2", "in3", "ctrl0", "ctrl1", "vdd", "vss", "en", "out", "flag", "metric")
PROPERTIES = (
    "rising-clock qualified decision driver",
    "valid sample drives out and flag high only when x0 > x1",
    "metric is the bounded absolute decision margin abs(x0-x1)",
)


def check_v4_287_edge_delay_qualified_driver(rows: list[dict[str, float]]) -> tuple[bool, str]:
    return check_clocked(rows, "edge", TASK_LABEL)


CHECKS = {
    TASK_LABEL: check_v4_287_edge_delay_qualified_driver,
    SOURCE_TASK_ID: check_v4_287_edge_delay_qualified_driver,
    "453-edge-delay-qualified-driver": check_v4_287_edge_delay_qualified_driver,
}

CHECKER_ID = TASK_LABEL
CHECKER: Checker = check_v4_287_edge_delay_qualified_driver
