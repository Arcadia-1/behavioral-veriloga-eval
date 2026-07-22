"""Task-specific checker for canonical v4 DUT 379."""
from __future__ import annotations

from ..api import Checker
def _rising_times(rows: list[dict[str, float]], col: str, vth: float = 0.45) -> list[float]:
    times: list[float] = []
    last = rows[0][col] > vth
    for row in rows[1:]:
        cur = row[col] > vth
        if not last and cur:
            times.append(row["time"])
        last = cur
    return times

def _sample_after(rows: list[dict[str, float]], t: float, delay: float = 5e-9) -> dict[str, float]:
    target = t + delay
    return min(rows, key=lambda row: abs(row["time"] - target))

def _v4_missing_columns(rows: list[dict[str, float]], required: set[str]) -> str | None:
    if not rows:
        return "missing_columns=" + ",".join(sorted(required)[:16])
    missing = sorted(required - set(rows[0].keys()))
    if missing:
        return "missing_columns=" + ",".join(missing[:16])
    return None

def _v4_close(actual: float, expected: float, tol: float = 0.07) -> bool:
    return abs(actual - expected) <= tol

def check_v4_periodic_sampler_aperture_metric(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin", "clk", "rst", "sample_en", "vhold", "aperture_metric", "valid"}
    missing = _v4_missing_columns(rows, required)
    if missing:
        return False, missing
    hold = 0.0
    metric = 0.0
    valid = False
    errors = 0
    checked = 0
    disabled_hold_checks = 0
    metric_nonzero = False
    for edge_t in _rising_times(rows, "clk"):
        edge_row = min(rows, key=lambda row: abs(row["time"] - edge_t))
        old_hold = hold
        if edge_row["rst"] > 0.45:
            hold = 0.0
            metric = 0.0
            valid = False
        elif edge_row["sample_en"] > 0.45:
            metric = min(0.9, 0.5 * abs(edge_row["vin"] - old_hold))
            hold = edge_row["vin"]
            valid = True
            metric_nonzero = metric_nonzero or metric > 0.03
        else:
            disabled_hold_checks += 1
        sample = _sample_after(rows, edge_t, 0.8e-9)
        if not _v4_close(sample["vhold"], hold, 0.06):
            errors += 1
        if not _v4_close(sample["aperture_metric"], metric, 0.06):
            errors += 1
        if (sample["valid"] > 0.45) != valid:
            errors += 1
        checked += 1
    ok = errors == 0 and checked >= 8 and disabled_hold_checks >= 1 and metric_nonzero
    return ok, (
        f"v4_periodic_sampler checked={checked} disabled_hold_checks={disabled_hold_checks} "
        f"metric_nonzero={metric_nonzero} errors={errors}"
    )

CHECKER_ID = "v4_379_periodic_sampler_aperture_metric"
CHECKER: Checker = check_v4_periodic_sampler_aperture_metric
