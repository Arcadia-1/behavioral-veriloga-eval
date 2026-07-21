"""Stimulus-relative checker for canonical v4 DUT 170."""
from __future__ import annotations

from ..api import Checker, Row
from .batch17_stimulus_relative import (
    bind_properties,
    crossings,
    diagnostic,
    event_label,
    logic_threshold,
    max_signal_value,
    pass_note,
    require_signals,
    sample,
)


PROPERTY_IDS = (
    "P_CLOCK_ARMED_MEASUREMENT",
    "P_DECISION_DELAY_CAPTURE",
    "P_ABSOLUTE_OVERDRIVE_METRIC",
    "P_POLARITY_AND_VALID_FLAG",
)
SIGNALS = {
    "time",
    "clk",
    "vinp",
    "vinn",
    "outp",
    "outn",
    "delay_ps",
    "overdrive_mv",
    "polarity",
    "valid",
}


def _event_probe_time(rows: list[Row], event_time_s: float, *, delay_s: float = 0.08e-9) -> float | None:
    if not rows:
        return None
    probe_t = event_time_s + delay_s
    if probe_t <= rows[-1]["time"]:
        return probe_t
    fallback = rows[-1]["time"] - 0.02e-9
    return fallback if fallback > event_time_s else None


def check_v3_comparator_delay_overdrive_meter(rows: list[Row]) -> tuple[bool, str]:
    missing = require_signals(rows, SIGNALS, "P_CLOCK_ARMED_MEASUREMENT")
    if missing:
        return False, missing

    vdd = max_signal_value(rows, ("clk", "outp", "outn", "valid", "polarity"), default=0.9)
    threshold = logic_threshold(rows, ("clk", "outp", "outn"), default_high=vdd)
    clk_rises = crossings(rows, "clk", threshold=threshold, direction="rising")
    out_events: list[tuple[float, str]] = [
        (edge_t, "outp")
        for edge_t in crossings(rows, "outp", threshold=threshold, direction="rising")
    ]
    out_events.extend(
        (edge_t, "outn")
        for edge_t in crossings(rows, "outn", threshold=threshold, direction="rising")
    )
    out_events.sort()
    if len(clk_rises) < 4 or len(out_events) < 4:
        return False, diagnostic(
            "P_CLOCK_ARMED_MEASUREMENT",
            "coverage",
            expected="at_least_4_clk_and_output_events",
            observed=f"clk={len(clk_rises)} out={len(out_events)}",
            event="full_trace",
        )

    checked = 0
    max_delay_err = 0.0
    max_overdrive_err = 0.0
    saw_outp = False
    saw_outn = False
    failures: list[str] = []

    for index, clk_t in enumerate(clk_rises):
        next_clk = clk_rises[index + 1] if index + 1 < len(clk_rises) else rows[-1]["time"] + 1e-12
        event = next(((t, name) for t, name in out_events if clk_t + 1e-13 < t < next_clk), None)
        if event is None:
            continue
        event_t, out_name = event
        probe_t = _event_probe_time(rows, event_t)
        if probe_t is None:
            continue

        armed_probe_t = clk_t + 0.5 * (event_t - clk_t)
        armed_valid = sample(rows, "valid", armed_probe_t)
        if armed_valid is None:
            return False, diagnostic(
                "P_CLOCK_ARMED_MEASUREMENT",
                "invalid_trace",
                expected="valid_low_between_arm_and_decision",
                observed="missing_sample",
                event=event_label("valid", checked, armed_probe_t),
            )
        if armed_valid > 0.2 * vdd:
            failures.append(
                diagnostic(
                    "P_CLOCK_ARMED_MEASUREMENT",
                    "value_mismatch",
                    expected=f"valid<={0.2 * vdd:.3f}_while_armed",
                    observed=f"valid={armed_valid:.3f}",
                    event=event_label("valid", checked, armed_probe_t),
                )
            )

        vinp = sample(rows, "vinp", clk_t + 1e-12)
        vinn = sample(rows, "vinn", clk_t + 1e-12)
        delay_s = sample(rows, "delay_ps", probe_t)
        overdrive_v = sample(rows, "overdrive_mv", probe_t)
        polarity = sample(rows, "polarity", probe_t)
        valid = sample(rows, "valid", probe_t)
        label = event_label(out_name, checked, event_t)
        if None in (vinp, vinn, delay_s, overdrive_v, polarity, valid):
            return False, diagnostic(
                "P_DECISION_DELAY_CAPTURE",
                "invalid_trace",
                expected="measurement_samples",
                observed="missing_sample",
                event=label,
            )
        assert vinp is not None
        assert vinn is not None
        assert delay_s is not None
        assert overdrive_v is not None
        assert polarity is not None
        assert valid is not None

        delay_ps = 1.0e12 * delay_s
        overdrive_mv = 1.0e3 * overdrive_v
        expected_delay_ps = 1.0e12 * (event_t - clk_t)
        expected_overdrive_mv = 1.0e3 * abs(vinp - vinn)
        expected_polarity = vdd if out_name == "outp" else 0.0
        saw_outp = saw_outp or out_name == "outp"
        saw_outn = saw_outn or out_name == "outn"
        delay_err = abs(delay_ps - expected_delay_ps)
        overdrive_err = abs(overdrive_mv - expected_overdrive_mv)
        polarity_err = abs(polarity - expected_polarity)
        max_delay_err = max(max_delay_err, delay_err)
        max_overdrive_err = max(max_overdrive_err, overdrive_err)
        checked += 1

        if delay_err > 4.0:
            failures.append(
                diagnostic(
                    "P_DECISION_DELAY_CAPTURE",
                    "value_mismatch",
                    expected=f"delay_ps={expected_delay_ps:.3f}",
                    observed=f"delay_ps={delay_ps:.3f}",
                    event=label,
                )
            )
        if overdrive_err > 1.5:
            failures.append(
                diagnostic(
                    "P_ABSOLUTE_OVERDRIVE_METRIC",
                    "value_mismatch",
                    expected=f"overdrive_mv={expected_overdrive_mv:.3f}",
                    observed=f"overdrive_mv={overdrive_mv:.3f}",
                    event=label,
                )
            )
        if polarity_err > 0.08 or valid < 0.7 * vdd:
            failures.append(
                diagnostic(
                    "P_POLARITY_AND_VALID_FLAG",
                    "value_mismatch",
                    expected=f"polarity={expected_polarity:.3f},valid>={0.7 * vdd:.3f}",
                    observed=f"polarity={polarity:.3f},valid={valid:.3f}",
                    event=label,
                )
            )

    if checked < 4:
        return False, diagnostic(
            "P_DECISION_DELAY_CAPTURE",
            "coverage",
            expected="at_least_4_checked_decisions",
            observed=f"checked={checked}",
            event="full_trace",
        )
    if not (saw_outp and saw_outn):
        return False, diagnostic(
            "P_POLARITY_AND_VALID_FLAG",
            "coverage",
            expected="both_output_polarities",
            observed=f"outp={saw_outp},outn={saw_outn}",
            event="full_trace",
        )
    if failures:
        return False, "; ".join(failures[:3])
    return True, pass_note(
        PROPERTY_IDS,
        f"checked={checked} max_delay_err_ps={max_delay_err:.3f} max_overdrive_err_mv={max_overdrive_err:.3f}",
    )


CHECKER_ID = "v4_170_comparator_delay_overdrive_meter"
CHECKER: Checker = bind_properties(check_v3_comparator_delay_overdrive_meter, PROPERTY_IDS)
