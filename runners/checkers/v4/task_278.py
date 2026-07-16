from __future__ import annotations

from ..api import Checker
from .family_271_280_diagnostics import bind_properties
from ..common.issue109_split import check_continuous


TASK_LABEL = "v4_278_lane_mask_replication_driver"
SOURCE_TASK_ID = "v3_406_lane_mask_replication_driver"
TRACE_SIGNALS = ("time", "in0", "in1", "in2", "in3", "ctrl0", "ctrl1", "vdd", "vss", "en", "out", "flag", "metric")
PROPERTIES = (
    "continuous local-rail normalization",
    "count x0..x3 values above 0.50 as a lane mask population",
    "out and metric both encode count/4, flag asserts only when count >= 3",
)


def check_v4_278_lane_mask_replication_driver(rows: list[dict[str, float]]) -> tuple[bool, str]:
    return check_continuous(rows, "reduction", TASK_LABEL)


CHECKS = {
    TASK_LABEL: check_v4_278_lane_mask_replication_driver,
    SOURCE_TASK_ID: check_v4_278_lane_mask_replication_driver,
    "406-lane-mask-replication-driver": check_v4_278_lane_mask_replication_driver,
}

CHECKER_ID = TASK_LABEL
CHECKER: Checker = bind_properties(check_v4_278_lane_mask_replication_driver, (
    "P_MEASURE_ANALOG_INPUTS_RELATIVE_TO_THE",
    "P_COUNT_THE_NUMBER_OF_NORMALIZED_INPUTS",
))
