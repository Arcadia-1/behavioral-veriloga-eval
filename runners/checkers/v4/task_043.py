"""Task-specific checker for canonical v4 DUT 043."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import diagnostic, pass_note, percentile, require_signals


PROPERTY_IDS = (
    "P_RESET_NEUTRAL",
    "P_HYSTERESIS_STATE_UPDATE",
    "P_GAINED_LIMITER_TRANSFER",
    "P_OUTPUT_LIMITS",
    "P_STATE_METRIC",
)


def _mean(values: list[float]) -> float | None:
    return sum(values) / len(values) if values else None

def check_release_soft_hysteretic_limiter(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "vin", "out", "metric"}
    missing = require_signals(rows, required, "P_GAINED_LIMITER_TRANSFER")
    if missing:
        return False, missing

    active_rows = [row for row in rows if row["rst"] <= 0.45]
    high_out: list[float] = []
    low_out: list[float] = []
    high_memory_out: list[float] = []
    low_memory_out: list[float] = []
    high_metric_values: list[float] = []
    low_metric_values: list[float] = []
    high_memory_metric_values: list[float] = []
    low_memory_metric_values: list[float] = []
    state: str | None = None
    for row in active_rows:
        vin = row["vin"]
        if vin >= 0.72:
            state = "high"
            high_out.append(row["out"])
            high_metric_values.append(row["metric"])
            continue
        if vin <= 0.25:
            state = "low"
            low_out.append(row["out"])
            low_metric_values.append(row["metric"])
            continue
        if 0.35 <= vin <= 0.60 and state == "high":
            high_memory_out.append(row["out"])
            high_memory_metric_values.append(row["metric"])
        elif 0.35 <= vin <= 0.60 and state == "low":
            low_memory_out.append(row["out"])
            low_memory_metric_values.append(row["metric"])

    high_limited = _mean(high_out)
    low_limited = _mean(low_out)
    high_memory = _mean(high_memory_out)
    low_memory = _mean(low_memory_out)
    high_metric = _mean(high_metric_values)
    low_metric = _mean(low_metric_values)
    high_memory_metric = _mean(high_memory_metric_values)
    low_memory_metric = _mean(low_memory_metric_values)
    if None in (
        high_limited,
        low_limited,
        high_memory,
        low_memory,
        high_metric,
        low_metric,
        high_memory_metric,
        low_memory_metric,
    ):
        return False, diagnostic(
            "P_HYSTERESIS_STATE_UPDATE",
            "insufficient_excitation",
            expected="high,low,high-memory,low-memory vin regions after reset",
            observed=(
                f"high={len(high_out)},low={len(low_out)},"
                f"high_memory={len(high_memory_out)},low_memory={len(low_memory_out)}"
            ),
            event="observed_vin_regions",
        )
    assert high_limited is not None
    assert low_limited is not None
    assert high_memory is not None
    assert low_memory is not None
    assert high_metric is not None
    assert low_metric is not None
    assert high_memory_metric is not None
    assert low_memory_metric is not None

    if len(active_rows) < 10:
        return False, diagnostic(
            "P_RESET_NEUTRAL",
            "insufficient_excitation",
            expected="post_reset_rows>=10",
            observed=f"post_reset_rows={len(active_rows)}",
            event="rst.low",
        )
    out_min = min(r["out"] for r in active_rows)
    out_max = max(r["out"] for r in active_rows)
    metric_span = max(r["metric"] for r in active_rows) - min(r["metric"] for r in active_rows)
    if not (-0.02 <= out_min <= out_max <= 0.92):
        return False, diagnostic(
            "P_OUTPUT_LIMITS",
            "behavior_mismatch",
            expected="out_range_within_-0.02..0.92",
            observed=f"out_range={out_min:.3f}..{out_max:.3f}",
            event="rst.low",
        )
    if high_limited > 0.84 or high_limited < 0.70:
        return False, diagnostic(
            "P_GAINED_LIMITER_TRANSFER",
            "behavior_mismatch",
            expected="0.70<=high_limited<=0.84",
            observed=f"high_limited={high_limited:.3f}",
            event="vin.high_region",
        )
    if low_limited < 0.08 or low_limited > 0.22:
        return False, diagnostic(
            "P_GAINED_LIMITER_TRANSFER",
            "behavior_mismatch",
            expected="0.08<=low_limited<=0.22",
            observed=f"low_limited={low_limited:.3f}",
            event="vin.low_region",
        )
    if high_memory <= low_memory + 0.10:
        return False, diagnostic(
            "P_HYSTERESIS_STATE_UPDATE",
            "behavior_mismatch",
            expected="high_memory>low_memory+0.10",
            observed=f"high_memory={high_memory:.3f},low_memory={low_memory:.3f}",
            event="deadband_after_extreme",
        )
    high_metric_stable = percentile(high_metric_values, 0.75)
    low_metric_stable = percentile(low_metric_values, 0.25)
    if (
        high_metric_stable < 0.58
        or high_memory_metric < 0.58
        or low_metric_stable > 0.32
        or low_memory_metric > 0.32
    ):
        return False, diagnostic(
            "P_STATE_METRIC",
            "behavior_mismatch",
            expected="metric_high>=0.58 and metric_low<=0.32",
            observed=(
                f"high={high_metric_stable:.3f}/{high_memory_metric:.3f},"
                f"low={low_metric_stable:.3f}/{low_memory_metric:.3f}"
            ),
            event="state_regions",
        )
    if metric_span < 0.30:
        return False, diagnostic(
            "P_STATE_METRIC",
            "behavior_mismatch",
            expected="metric_span>=0.30",
            observed=f"metric_span={metric_span:.3f}",
            event="rst.low",
        )
    return True, pass_note(PROPERTY_IDS, (
        "release_soft_hysteretic_limiter "
        f"limited={low_limited:.3f}/{high_limited:.3f} "
        f"memory={low_memory:.3f}/{high_memory:.3f} metric_span={metric_span:.3f}"
    ))

CHECKER_ID = "v4_043_soft_hysteretic_limiter"
CHECKER: Checker = check_release_soft_hysteretic_limiter
