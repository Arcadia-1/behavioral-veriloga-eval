"""Task-specific checker for canonical v4 DUT 073."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import diagnostic, pass_note, probe_time, require_signals, sample


PROPERTY_IDS = (
    "P_CLOCKED_UPDATE",
    "P_DISABLE_RESET",
    "P_TRIM_TARGET",
    "P_SETTLING",
    "P_MONOTONIC_TRIM",
    "P_ENABLE_METRIC",
)


def _rising_edges(rows: list[dict[str, float]], signal: str, threshold: float = 0.45) -> list[float]:
    edges: list[float] = []
    for left, right in zip(rows, rows[1:]):
        if left[signal] <= threshold < right[signal]:
            edges.append(right["time"])
    return edges


def _target(vin: float) -> float:
    raw = 0.28 + 0.55 * ((vin - 0.25) / 0.65)
    return min(0.82, max(0.28, raw))


def _event(index: int) -> str:
    return f"clk_rise[{index}]"


def check_bias_voltage_generator_with_enable_trim(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "vin", "out", "metric"}
    missing = require_signals(rows, required, "P_CLOCKED_UPDATE")
    if missing is not None:
        return False, missing

    edges = _rising_edges(rows, "clk")
    if len(edges) < 6:
        return False, diagnostic(
            "P_CLOCKED_UPDATE",
            "missing_event",
            expected="clk_rises>=6",
            observed=f"clk_rises:{len(edges)}",
            event="full_trace",
        )

    expected_state = 0.0
    disabled_checks = 0
    enabled_checks = 0
    settling_checks = 0
    metric_enabled = 0
    metric_disabled = 0
    enabled_observations: list[tuple[float, float, float]] = []

    for idx, edge_t in enumerate(edges):
        next_edge_t = edges[idx + 1] if idx + 1 < len(edges) else None
        check_t = probe_time(rows, edge_t, next_edge_t, fraction=0.35)
        if check_t is None:
            continue
        rst = sample(rows, "rst", edge_t)
        vin = sample(rows, "vin", edge_t)
        out = sample(rows, "out", check_t)
        metric = sample(rows, "metric", check_t)
        if None in (rst, vin, out, metric):
            return False, diagnostic(
                "P_CLOCKED_UPDATE",
                "invalid_trace",
                expected="sampled_clk_update",
                observed="missing_probe",
                event=_event(idx),
            )
        assert rst is not None and vin is not None and out is not None and metric is not None

        if rst > 0.45 or vin < 0.25:
            expected_state = 0.0
            disabled_checks += 1
            if out > 0.09:
                return False, diagnostic(
                    "P_DISABLE_RESET",
                    "value_mismatch",
                    expected="out<=0.09",
                    observed=f"out:{out:.3f}",
                    event=_event(idx),
                )
            if metric <= 0.18:
                metric_disabled += 1
            continue

        target = _target(vin)
        previous_state = expected_state
        expected_state = previous_state + 0.45 * (target - previous_state)
        enabled_checks += 1
        enabled_observations.append((target, out, vin))
        if abs(out - expected_state) <= 0.08:
            settling_checks += 1
        else:
            return False, diagnostic(
                "P_SETTLING",
                "value_mismatch",
                expected=f"out:{expected_state:.3f}",
                observed=f"out:{out:.3f}",
                event=_event(idx),
            )
        if metric >= 0.55:
            metric_enabled += 1

    if disabled_checks < 2:
        return False, diagnostic(
            "P_DISABLE_RESET",
            "missing_event",
            expected="disabled_updates>=2",
            observed=f"disabled_updates:{disabled_checks}",
            event="clk_rises",
        )
    if enabled_checks < 4 or settling_checks < 4:
        return False, diagnostic(
            "P_SETTLING",
            "missing_event",
            expected="settling_updates>=4",
            observed=f"settling_updates:{settling_checks}",
            event="enabled_clk_rises",
        )
    if metric_enabled < 3 or metric_disabled < 2:
        return False, diagnostic(
            "P_ENABLE_METRIC",
            "value_mismatch",
            expected="enabled_metric>=3,disabled_metric>=2",
            observed=f"enabled_metric:{metric_enabled},disabled_metric:{metric_disabled}",
            event="clk_rises",
        )

    lower = min(enabled_observations, key=lambda item: item[0])
    higher = max(enabled_observations, key=lambda item: item[0])
    if higher[0] <= lower[0] + 0.10 or higher[1] <= lower[1] + 0.08:
        return False, diagnostic(
            "P_MONOTONIC_TRIM",
            "value_mismatch",
            expected="higher_trim_output>lower_trim_output",
            observed=f"low:{lower[1]:.3f},high:{higher[1]:.3f}",
            event="enabled_clk_rises",
        )

    return True, pass_note(
        PROPERTY_IDS,
        (
            "bias_voltage_generator_with_enable_trim "
            f"enabled_updates={enabled_checks} disabled_updates={disabled_checks} "
            f"settling_updates={settling_checks}"
        ),
    )


CHECKER_ID = "v4_073_bias_voltage_generator_with_enable_trim"
CHECKER: Checker = check_bias_voltage_generator_with_enable_trim
