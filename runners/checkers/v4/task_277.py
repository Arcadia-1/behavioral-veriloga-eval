from __future__ import annotations

from ..api import Checker
from ..common.issue109_split import check_continuous


TASK_LABEL = "v4_277_calibration_bit_select_flag"
SOURCE_TASK_ID = "v3_403_calibration_bit_select_flag"
TRACE_SIGNALS = ("time", "in0", "in1", "in2", "in3", "ctrl0", "ctrl1", "vdd", "vss", "en", "out", "flag", "metric")
PROPERTIES = (
    "continuous local-rail normalization",
    "ctrl1/ctrl0 select x0/x1/x2/x3 with explicit scalar mux behavior",
    "metric is the voltage-coded select index divided by three",
)


def check_v4_277_calibration_bit_select_flag(rows: list[dict[str, float]]) -> tuple[bool, str]:
    return check_continuous(rows, "mux", TASK_LABEL)


CHECKS = {
    TASK_LABEL: check_v4_277_calibration_bit_select_flag,
    SOURCE_TASK_ID: check_v4_277_calibration_bit_select_flag,
    "403-calibration-bit-select-flag": check_v4_277_calibration_bit_select_flag,
}

CHECKER_ID = TASK_LABEL
CHECKER: Checker = check_v4_277_calibration_bit_select_flag
