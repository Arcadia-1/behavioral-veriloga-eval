"""Stimulus-relative checker for canonical V4 DUT 036."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import close, crossings, diagnostic, event_label, pass_note, probe_time, require_signals, sample


PROPERTY_IDS = (
    "P_RESET_ASSERTED_UNSAFE",
    "P_DELAYED_RELEASE",
    "P_RELEASE_STATUS",
    "P_FAULT_REASSERTION",
    "P_VOLTAGE_CODED_LEVELS",
)


def check_power_on_reset_detector(rows: list[dict[str, float]]) -> tuple[bool, str]:
    error = require_signals(rows, {"time", "clk", "rst", "vin", "out", "metric"}, "P_RESET_ASSERTED_UNSAFE")
    if error:
        return False, error

    clock_edges = crossings(rows, "clk", threshold=0.45, direction="rising")
    rst_edges = crossings(rows, "rst", threshold=0.45, direction="rising") + crossings(
        rows, "rst", threshold=0.45, direction="falling"
    )
    vin_edges = crossings(rows, "vin", threshold=0.62, direction="rising") + crossings(
        rows, "vin", threshold=0.62, direction="falling"
    )
    if len(clock_edges) < 8:
        return False, diagnostic(
            "P_DELAYED_RELEASE", "insufficient_excitation", expected="clk_rise_count>=8",
            observed=f"clk_rise_count={len(clock_edges)}", event="full_trace",
        )
    events: list[tuple[float, str]] = [(rows[0]["time"], "initial")]
    events.extend((time_s, "clock") for time_s in clock_edges)
    events.extend((time_s, "fault") for time_s in rst_edges)
    events.extend((time_s, "fault") for time_s in vin_edges)
    events.sort(key=lambda item: (item[0], 0 if item[1] == "fault" else 1))

    release_count = 0
    safe_epochs = 0
    released_epochs = 0
    fault_reassertions = 0
    previously_unsafe = True
    checked = 0
    for index, (event_time, kind) in enumerate(events):
        next_time = events[index + 1][0] if index + 1 < len(events) else None
        condition_probe = probe_time(rows, event_time, next_time, fraction=0.02)
        output_probe = probe_time(rows, event_time, next_time, fraction=0.35)
        if condition_probe is None or output_probe is None:
            continue
        rst = sample(rows, "rst", condition_probe)
        vin = sample(rows, "vin", condition_probe)
        if rst is None or vin is None:
            continue
        unsafe = rst > 0.45 or vin < 0.62
        if unsafe:
            if not previously_unsafe:
                fault_reassertions += 1
            release_count = 0
            expected_out, expected_metric = 0.9, 0.0
            property_id = "P_RESET_ASSERTED_UNSAFE" if index == 0 else "P_FAULT_REASSERTION"
        else:
            if previously_unsafe:
                safe_epochs += 1
            if kind == "clock":
                release_count += 1
            if release_count >= 4:
                expected_out, expected_metric = 0.0, 0.9
                property_id = "P_RELEASE_STATUS"
                released_epochs = max(released_epochs, safe_epochs)
            else:
                expected_out = 0.9
                expected_metric = 0.2 if release_count > 0 else 0.0
                property_id = "P_DELAYED_RELEASE"
        previously_unsafe = unsafe
        out, metric = sample(rows, "out", output_probe), sample(rows, "metric", output_probe)
        if out is None or metric is None:
            continue
        checked += 1
        label = event_label(kind, index, event_time)
        if not close(out, expected_out, 0.08) or not close(metric, expected_metric, 0.10):
            return False, diagnostic(
                property_id, "behavior_mismatch",
                expected=f"out:{expected_out:.2f},metric:{expected_metric:.2f}",
                observed=f"out:{out:.3f},metric:{metric:.3f},vin:{vin:.3f},rst:{rst:.3f},count:{release_count}",
                event=label,
            )

    invalid_levels = [
        row for row in rows
        if not (-0.08 <= row["out"] <= 0.98 and -0.08 <= row["metric"] <= 0.98)
    ]
    if invalid_levels:
        row = invalid_levels[0]
        return False, diagnostic(
            "P_VOLTAGE_CODED_LEVELS", "behavior_mismatch", expected="out,metric_in_[0,0.9]",
            observed=f"out:{row['out']:.3f},metric:{row['metric']:.3f}", event=f"trace@{row['time']:.6e}s",
        )
    missing = []
    if safe_epochs < 2:
        missing.append("initial_release_and_recovery")
    if released_epochs < 2:
        missing.append("four_edge_release_twice")
    if fault_reassertions < 1:
        missing.append("brownout_or_reset_reassertion")
    if missing:
        return False, diagnostic(
            "P_FAULT_REASSERTION", "insufficient_excitation",
            expected="unsafe,release_delay,brownout,recovery", observed="missing:" + ",".join(missing),
            event="full_trace",
        )
    return True, pass_note(PROPERTY_IDS, f"por event_checks={checked} safe_epochs={safe_epochs}")


CHECKER_ID = "v4_036_power_on_reset_detector"
CHECKER: Checker = check_power_on_reset_detector
