from __future__ import annotations

from ..api import Checker
from ..common.issue109_split import check_continuous


TASK_LABEL = "v4_279_explicit_sar_slice_router"
SOURCE_TASK_ID = "v3_415_explicit_sar_slice_router"
TRACE_SIGNALS = ("time", "in0", "in1", "in2", "in3", "ctrl0", "ctrl1", "vdd", "vss", "en", "out", "flag", "metric")
PROPERTIES = (
    "continuous local-rail normalization",
    "ctrl1/ctrl0 implement explicit SAR slice select over x0..x3",
    "out is 0.88*selected+0.04 clipped to vhi, flag and metric expose selected slice",
)


def check_v4_279_explicit_sar_slice_router(rows: list[dict[str, float]]) -> tuple[bool, str]:
    return check_continuous(rows, "mux", TASK_LABEL)


CHECKS = {
    TASK_LABEL: check_v4_279_explicit_sar_slice_router,
    SOURCE_TASK_ID: check_v4_279_explicit_sar_slice_router,
    "415-explicit-sar-slice-router": check_v4_279_explicit_sar_slice_router,
}

CHECKER_ID = TASK_LABEL
CHECKER: Checker = check_v4_279_explicit_sar_slice_router
