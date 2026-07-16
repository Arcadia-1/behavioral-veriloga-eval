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
    first_mismatch: str | None = None
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
        early_rst = sample_signal(rows, "rst", early_time)
        early_vin = sample_signal(rows, "vin", early_time)
        late_rst = sample_signal(rows, "rst", late_time)
        late_vin = sample_signal(rows, "vin", late_time)
        if any(
            value is None
            for value in (observed, metric, late, early_rst, early_vin, late_rst, late_vin)
        ):
            continue
        checked += 1
        settling_failed = abs(observed - expected) > 0.055
        metric_failed = abs(metric - expected_metric) > 0.10
        clamp_ceiling = min(0.935, max(0.0, vin - 0.015))
        clamp_failed = observed < -0.035 or observed > clamp_ceiling
        early_forced_low = early_rst > 0.45 or early_vin < 0.58
        late_forced_low = late_rst > 0.45 or late_vin < 0.58
        hold_failed = early_forced_low == late_forced_low and abs(late - observed) > 0.025
        settling_errors += settling_failed
        metric_errors += metric_failed
        clamp_errors += clamp_failed
        hold_errors += hold_failed
        if first_mismatch is None and settling_failed:
            property_id = (
                "P_RESET_AND_BROWNOUT"
                if rst > 0.45 or vin < 0.58
                else "P_CLOCKED_FIRST_ORDER_SETTLING"
            )
            first_mismatch = (
                f"first_mismatch={property_id} signal=out time={early_time:.6e} "
                f"expected={expected:.6g} observed={observed:.6g} tolerance=0.055"
            )
        if first_mismatch is None and metric_failed:
            property_id = (
                "P_RESET_AND_BROWNOUT"
                if rst > 0.45 or vin < 0.58
                else "P_VALIDITY_ENCODING"
            )
            first_mismatch = (
                f"first_mismatch={property_id} signal=metric time={early_time:.6e} "
                f"expected={expected_metric:.6g} observed={metric:.6g} tolerance=0.1"
            )
        if first_mismatch is None and clamp_failed:
            first_mismatch = (
                "first_mismatch=P_TARGET_AND_OUTPUT_CLAMPS signal=out "
                f"time={early_time:.6e} expected=[-0.035,{clamp_ceiling:.6g}] "
                f"observed={observed:.6g} tolerance=0"
            )
        if first_mismatch is None and hold_failed:
            first_mismatch = (
                "first_mismatch=P_CLOCKED_HOLD signal=out "
                f"time={late_time:.6e} expected={observed:.6g} "
                f"observed={late:.6g} tolerance=0.025"
            )
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
    if first_mismatch is None and coverage_missing:
        coverage_checks = (
            ("P_CLOCKED_FIRST_ORDER_SETTLING", "checked", 20, checked),
            ("P_RESET_AND_BROWNOUT", "reset_events", 1, reset_events),
            ("P_RESET_AND_BROWNOUT", "brownout_events", 1, brownout_events),
            ("P_VALIDITY_ENCODING", "startup_events", 1, startup_events),
            ("P_VALIDITY_ENCODING", "valid_events", 1, valid_events),
        )
        for property_id, signal, expected_count, observed_count in coverage_checks:
            if observed_count < expected_count:
                first_mismatch = (
                    f"first_mismatch={property_id} signal={signal} "
                    f"expected=>={expected_count} observed={observed_count} tolerance=0"
                )
                break
    mismatch_detail = "" if first_mismatch is None else f"; {first_mismatch}"
    return ok, (
        f"checked={checked} reset={reset_events} brownout={brownout_events} startup={startup_events} "
        f"valid={valid_events} samples={','.join(details)}{coverage}; {property_diagnostics(counts)}"
        f"{mismatch_detail}"
    )


CHECKER_ID = "v4_020_bandgap_reference_macro_model"
CHECKER: Checker = check_bandgap_reference_macro_model
