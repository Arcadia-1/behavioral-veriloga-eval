from __future__ import annotations

from checkers.api import Checker
from checkers.common.issue109_split import check_continuous


TASK_LABEL = "v4_288_calibration_quadrant_mapper"
SOURCE_TASK_ID = "v3_454_calibration_quadrant_mapper"
TRACE_SIGNALS = ("time", "in0", "in1", "in2", "in3", "ctrl0", "ctrl1", "vdd", "vss", "en", "out", "flag", "metric")
PROPERTIES = (
    "continuous quadrant selection from ctrl1/ctrl0",
    "selects x0/x1/x2/x3 without multidimensional array state",
    "out, flag, and metric expose selected quadrant value and index",
)


def check_v4_288_calibration_quadrant_mapper(rows: list[dict[str, float]]) -> tuple[bool, str]:
    return check_continuous(rows, "mux", TASK_LABEL)


CHECKS = {
    TASK_LABEL: check_v4_288_calibration_quadrant_mapper,
    SOURCE_TASK_ID: check_v4_288_calibration_quadrant_mapper,
    "454-calibration-quadrant-mapper": check_v4_288_calibration_quadrant_mapper,
}

CHECKER_ID = TASK_LABEL
CHECKER: Checker = check_v4_288_calibration_quadrant_mapper
