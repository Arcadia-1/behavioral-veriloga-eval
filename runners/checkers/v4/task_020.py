"""Stimulus-relative checker for canonical v4 DUT 020."""

from __future__ import annotations

from ..api import Checker, Row
from .trace_utils import property_diagnostics, sample_signal, threshold_crossings


def check_bandgap_reference_macro_model(rows: list[Row]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "vin", "out", "metric"}
    missing = sorted(required - (set(rows[0]) if rows else set()))
    if missing:
        return False, "missing_columns=" + ",".join(missing)

    edges = threshold_crossings(rows, "clk", direction=1)
    expected = 0.0
    settling_errors = metric_errors = clamp_errors = hold_errors = 0
    reset_events = brownout_events = startup_events = valid_events = 0
    checked = 0
    details: list[str] = []
    for index, edge in enumerate(edges):
        next_edge = edges[index + 1] if index + 1 < len(edges) else rows[-1]["time"]
        if next_edge <= edge:
            continue
        rst = sample_signal(rows, "rst", edge)
        vin = sample_signal(rows, "vin", edge)
        if rst is None or vin is None:
            continue
        if rst > 0.45 or vin < 0.58:
            expected = 0.0
            expected_metric = 0.0
            reset_events += int(rst > 0.45)
            brownout_events += int(rst <= 0.45 and vin < 0.58)
        else:
            target = min(max(0.55 + 0.020 * (vin - 0.75), 0.0), vin - 0.05)
            expected += 0.35 * (target - expected)
            expected = min(max(expected, 0.0), 0.9)
            expected_metric = 0.9 if expected > 0.48 else 0.2
            startup_events += int(expected_metric == 0.2)
            valid_events += int(expected_metric == 0.9)

        early_time = edge + 0.36 * (next_edge - edge)
        late_time = edge + 0.76 * (next_edge - edge)
        observed = sample_signal(rows, "out", early_time)
        metric = sample_signal(rows, "metric", early_time)
        late = sample_signal(rows, "out", late_time)
        if observed is None or metric is None or late is None:
            continue
        checked += 1
        settling_errors += abs(observed - expected) > 0.055
        metric_errors += abs(metric - expected_metric) > 0.10
        clamp_errors += observed < -0.035 or observed > min(0.935, max(0.0, vin - 0.015))
        hold_errors += abs(late - observed) > 0.025
        if len(details) < 8:
            details.append(f"{observed:.3f}/{expected:.3f}:{metric:.2f}/{expected_metric:.1f}")

    coverage_missing = (
        int(checked < 20)
        + int(reset_events < 1)
        + int(brownout_events < 1)
        + int(startup_events < 1)
        + int(valid_events < 1)
    )
    counts = {
        "P_RESET_AND_BROWNOUT": settling_errors + metric_errors + int(reset_events < 1) + int(brownout_events < 1),
        "P_CLOCKED_FIRST_ORDER_SETTLING": settling_errors + coverage_missing,
        "P_TARGET_AND_OUTPUT_CLAMPS": clamp_errors,
        "P_VALIDITY_ENCODING": metric_errors + int(startup_events < 1) + int(valid_events < 1),
        "P_CLOCKED_HOLD": hold_errors,
    }
    ok = coverage_missing == 0 and all(count == 0 for count in counts.values())
    coverage = "" if coverage_missing == 0 else f" insufficient_excitation={coverage_missing}"
    return ok, (
        f"checked={checked} reset={reset_events} brownout={brownout_events} startup={startup_events} "
        f"valid={valid_events} samples={','.join(details)}{coverage}; {property_diagnostics(counts)}"
    )


CHECKER_ID = "v4_020_bandgap_reference_macro_model"
CHECKER: Checker = check_bandgap_reference_macro_model
