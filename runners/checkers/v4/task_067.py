"""Task-specific checker for canonical v4 DUT 067."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import crossings, diagnostic, event_label, pass_note, require_signals, sample
import math


PROPERTIES = (
    "P_STROBE_UPDATE",
    "P_IDEAL_CODE",
    "P_OBSERVED_CODE",
    "P_ABSOLUTE_ERROR",
    "P_MAX_RETENTION",
    "P_METRIC_SCALE",
)

def check_v3_501_adc_static_linearity_monitor(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vsample", "vin", "d2", "d1", "d0", "maxerr"}
    invalid = require_signals(rows, required, "P_STROBE_UPDATE")
    if invalid:
        return False, invalid
    sample_edges = crossings(rows, "vsample", threshold=0.45, direction="rising")
    if len(sample_edges) < 5:
        return False, diagnostic(
            "P_STROBE_UPDATE",
            "insufficient_coverage",
            expected="sample_edges>=5",
            observed=f"sample_edges={len(sample_edges)}",
            event="full_trace",
        )
    expected_max = 0
    checked = 0
    max_err = 0.0
    observed_metrics: list[float] = []
    failures: list[str] = []
    for edge_index, edge_t in enumerate(sample_edges, start=1):
        sample_t = edge_t + 0.10e-9
        vin = sample(rows, "vin", edge_t + 1e-12)
        if vin is None:
            continue
        clipped = min(1.0, max(0.0, vin))
        ideal = int(math.floor(8.0 * clipped))
        ideal = max(0, min(7, ideal))
        observed_code = 0
        for bit, signal in enumerate(("d0", "d1", "d2")):
            value = sample(rows, signal, edge_t + 1e-12)
            if value is None:
                failures.append(
                    diagnostic(
                        "P_OBSERVED_CODE",
                        "missing_probe",
                        expected=signal,
                        observed="none",
                        event=event_label("sample_edge", edge_index, edge_t),
                    )
                )
                continue
            observed_code += (1 << bit) if value > 0.45 else 0
        expected_max = max(expected_max, abs(observed_code - ideal))
        metric = sample(rows, "maxerr", sample_t)
        if metric is None:
            return False, diagnostic(
                "P_METRIC_SCALE",
                "missing_probe",
                expected="maxerr",
                observed="none",
                event=event_label("sample_edge", edge_index, edge_t),
            )
        observed_metrics.append(metric)
        max_err = max(max_err, abs(metric - expected_max))
        checked += 1
    if checked < 5:
        return False, diagnostic(
            "P_STROBE_UPDATE",
            "insufficient_coverage",
            expected="checked_samples>=5",
            observed=f"checked_samples={checked}",
            event="full_trace",
        )
    if any(observed_metrics[idx] + 0.03 < observed_metrics[idx - 1] for idx in range(1, len(observed_metrics))):
        return False, diagnostic(
            "P_MAX_RETENTION",
            "semantic_mismatch",
            expected="maxerr_nondecreasing",
            observed=f"metrics={','.join(f'{value:.3f}' for value in observed_metrics)}",
            event="sample_edges",
        )
    if expected_max < 2:
        return False, diagnostic(
            "P_ABSOLUTE_ERROR",
            "insufficient_coverage",
            expected="absolute_error>=2_lsb",
            observed=f"absolute_error={expected_max}",
            event="sample_edges",
        )
    if failures:
        return False, " ".join(failures[:5])
    if max_err > 0.08:
        return False, diagnostic(
            "P_METRIC_SCALE",
            "semantic_mismatch",
            expected=f"running_max_code_error={expected_max}",
            observed=f"max_err={max_err:.4f}",
            event="sample_edges",
        )
    return True, pass_note(PROPERTIES, f"samples={checked} expected_max={expected_max} max_err={max_err:.4f}")

CHECKER_ID = "v4_067_adc_static_linearity_monitor"
CHECKER: Checker = check_v3_501_adc_static_linearity_monitor
