from __future__ import annotations

from ..api import Checker
from .family_271_280_diagnostics import bind_properties
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
    # The public tr parameter permits 50 ps output smoothing. Ignore the input
    # breakpoint and its immediate settling interval; all scored samples remain
    # steady-state contract checks.
    return check_continuous(rows, "mux", TASK_LABEL, settle_time_s=100e-12)


CHECKS = {
    TASK_LABEL: check_v4_277_calibration_bit_select_flag,
    SOURCE_TASK_ID: check_v4_277_calibration_bit_select_flag,
    "403-calibration-bit-select-flag": check_v4_277_calibration_bit_select_flag,
}

CHECKER_ID = TASK_LABEL
CHECKER: Checker = bind_properties(check_v4_277_calibration_bit_select_flag, (
    "P_MEASURE_ANALOG_INPUTS_RELATIVE_TO_THE",
    "P_USE_THE_TWO_CONTROL_LEVELS_AS",
))
