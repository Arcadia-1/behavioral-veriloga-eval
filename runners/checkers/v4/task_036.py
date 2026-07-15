"""Task-specific checker for canonical v4 DUT 036."""
from __future__ import annotations

from ..api import Checker
def mean_in_window(rows: list[dict[str, float]], key: str, start: float, stop: float) -> float | None:
    values = [r[key] for r in rows if start <= r["time"] <= stop and key in r]
    if not values:
        return None
    return sum(values) / len(values)

def check_power_on_reset_detector(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "vin", "out", "metric"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/clk/rst/vin/out/metric"

    initial_reset = mean_in_window(rows, "out", 4.0e-9, 7.0e-9)
    delayed_reset = mean_in_window(rows, "out", 10.0e-9, 13.0e-9)
    released = mean_in_window(rows, "out", 22.0e-9, 38.0e-9)
    brownout_immediate = mean_in_window(rows, "out", 45.0e-9, 45.8e-9)
    brownout_reset = mean_in_window(rows, "out", 46.2e-9, 52.0e-9)
    recovered = mean_in_window(rows, "out", 65.0e-9, 76.0e-9)
    released_metric = mean_in_window(rows, "metric", 22.0e-9, 38.0e-9)
    if None in (initial_reset, delayed_reset, released, brownout_immediate, brownout_reset, recovered, released_metric):
        return False, "por_missing_sample_windows"
    assert initial_reset is not None
    assert delayed_reset is not None
    assert released is not None
    assert brownout_immediate is not None
    assert brownout_reset is not None
    assert recovered is not None
    assert released_metric is not None

    if initial_reset < 0.65:
        return False, f"por_initial_not_asserted={initial_reset:.3f}"
    if delayed_reset < 0.65:
        return False, f"por_no_release_delay={delayed_reset:.3f}"
    if released > 0.20:
        return False, f"por_not_released={released:.3f}"
    if brownout_immediate < 0.65:
        return False, f"por_brownout_not_immediate={brownout_immediate:.3f}"
    if brownout_reset < 0.65:
        return False, f"por_brownout_not_asserted={brownout_reset:.3f}"
    if recovered > 0.20 or released_metric < 0.65:
        return False, f"por_recovery_wrong recovered={recovered:.3f} metric={released_metric:.3f}"
    return True, (
        "power_on_reset_detector "
        f"reset={initial_reset:.3f}->{released:.3f} brownout={brownout_immediate:.3f}/{brownout_reset:.3f}"
    )

CHECKER_ID = "v4_036_power_on_reset_detector"
CHECKER: Checker = check_power_on_reset_detector
