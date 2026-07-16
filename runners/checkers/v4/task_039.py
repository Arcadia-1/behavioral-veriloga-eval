"""Stimulus-relative checker for canonical V4 DUT 039."""
from __future__ import annotations

import math
import statistics

from ..api import Checker
from .stimulus_relative import crossings, diagnostic, event_label, pass_note, percentile, require_signals, sample


PROPERTY_IDS = (
    "P_BUNDLE_BINDING",
    "P_CLOCKED_DECISION",
    "P_DELAY_MAGNITUDE_TREND",
    "P_DELAY_CLAMP",
    "P_FALLING_RESET",
    "P_EDGE_INTERVAL_MEASUREMENT",
)


def _first_after(values: list[float], start: float, stop: float) -> float | None:
    return next((value for value in values if start < value < stop), None)


def check_cmp_delay(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {
        "time", "clk", "vinp", "vinn", "out_p", "out_n", "lp_int", "lm_int", "delay_ps", "gnd", "vdd"
    }
    error = require_signals(rows, required, "P_BUNDLE_BINDING")
    if error:
        return False, error
    vdd_values = [row["vdd"] - row["gnd"] for row in rows]
    vdd = statistics.median(vdd_values)
    if vdd <= 0.0:
        return False, diagnostic(
            "P_BUNDLE_BINDING", "invalid_trace", expected="positive_vdd",
            observed=f"median_vdd:{vdd:.4f}", event="full_trace",
        )
    threshold = 0.5 * vdd
    clk_rises = crossings(rows, "clk", threshold=threshold, direction="rising")
    clk_falls = crossings(rows, "clk", threshold=threshold, direction="falling")
    out_p_rises = crossings(rows, "out_p", threshold=threshold, direction="rising")
    out_n_rises = crossings(rows, "out_n", threshold=threshold, direction="rising")
    if len(clk_rises) < 8 or len(clk_falls) < 8:
        return False, diagnostic(
            "P_CLOCKED_DECISION", "insufficient_excitation", expected="clock_cycles>=8",
            observed=f"rises:{len(clk_rises)},falls:{len(clk_falls)}", event="full_trace",
        )

    measurements: list[tuple[float, float]] = []
    timer_checks = 0
    for index, rise in enumerate(clk_rises):
        fall = _first_after(clk_falls, rise, clk_rises[index + 1] if index + 1 < len(clk_rises) else rows[-1]["time"])
        if fall is None:
            continue
        vinp, vinn = sample(rows, "vinp", rise), sample(rows, "vinn", rise)
        if vinp is None or vinn is None:
            continue
        differential = vinp - vinn
        expected_positive = differential >= 0.0
        crossing = _first_after(out_p_rises if expected_positive else out_n_rises, rise, fall)
        label = event_label("clk_rise", index, rise)
        if crossing is None:
            return False, diagnostic(
                "P_CLOCKED_DECISION", "behavior_mismatch",
                expected="out_p_rise" if expected_positive else "out_n_rise",
                observed=f"no_decision_crossing,diff:{differential:.6g}", event=label,
            )
        measured_delay = crossing - rise
        if measured_delay < 10e-12 or measured_delay > 260e-12:
            return False, diagnostic(
                "P_DELAY_CLAMP", "behavior_mismatch", expected="decision_delay_in_[10ps,260ps]",
                observed=f"delay_ps:{measured_delay * 1e12:.3f}", event=label,
            )
        stable_probe = crossing + 0.35 * (fall - crossing)
        out_p, out_n = sample(rows, "out_p", stable_probe), sample(rows, "out_n", stable_probe)
        if out_p is None or out_n is None:
            continue
        if expected_positive:
            decision_ok = out_p > 0.75 * vdd and out_n < 0.25 * vdd
        else:
            decision_ok = out_n > 0.75 * vdd and out_p < 0.25 * vdd
        if not decision_ok:
            return False, diagnostic(
                "P_CLOCKED_DECISION", "behavior_mismatch",
                expected="complementary_decision_for_diff_sign",
                observed=f"out_p:{out_p:.3f},out_n:{out_n:.3f},diff:{differential:.6g}", event=label,
            )
        timer = sample(rows, "delay_ps", stable_probe)
        if timer is not None:
            timer_checks += 1
            measured_ps = measured_delay * 1e12
            if abs(timer - measured_ps) > max(15.0, 0.30 * measured_ps):
                return False, diagnostic(
                    "P_EDGE_INTERVAL_MEASUREMENT", "behavior_mismatch",
                    expected=f"delay_ps:{measured_ps:.3f}", observed=f"delay_ps:{timer:.3f}", event=label,
                )
        measurements.append((abs(differential), measured_delay))

    groups: dict[float, list[float]] = {}
    for differential, delay in measurements:
        if differential <= 0.0:
            continue
        bucket = round(math.log10(differential), 3)
        groups.setdefault(bucket, []).append(delay)
    trend = sorted(
        ((10.0**bucket, statistics.median(delays)) for bucket, delays in groups.items()),
        key=lambda item: item[0], reverse=True,
    )
    if len(trend) < 4 or trend[0][0] / trend[-1][0] < 500.0:
        return False, diagnostic(
            "P_DELAY_MAGNITUDE_TREND", "insufficient_excitation",
            expected="four_magnitudes_spanning>=500x",
            observed=f"groups:{len(trend)},span:{(trend[0][0] / trend[-1][0]) if len(trend) > 1 else 1.0:.1f}x",
            event="full_trace",
        )
    delays = [delay for _diff, delay in trend]
    if any(left > right + 12e-12 for left, right in zip(delays, delays[1:])) or delays[-1] - delays[0] < 15e-12:
        return False, diagnostic(
            "P_DELAY_MAGNITUDE_TREND", "behavior_mismatch",
            expected="delay_increases_as_abs_diff_decreases",
            observed="delays_ps:" + ",".join(f"{delay * 1e12:.2f}" for delay in delays), event="full_trace",
        )

    reset_checks = 0
    for index, fall in enumerate(clk_falls):
        next_rise = _first_after(clk_rises, fall, rows[-1]["time"])
        if next_rise is None:
            continue
        probe = fall + 0.35 * (next_rise - fall)
        out_p, out_n = sample(rows, "out_p", probe), sample(rows, "out_n", probe)
        if out_p is None or out_n is None:
            continue
        reset_checks += 1
        if out_p > 0.25 * vdd or out_n > 0.25 * vdd:
            return False, diagnostic(
                "P_FALLING_RESET", "behavior_mismatch", expected="both_outputs_low_after_falling_clk",
                observed=f"out_p:{out_p:.3f},out_n:{out_n:.3f}", event=event_label("clk_fall", index, fall),
            )

    mirror_error = percentile(
        [max(abs(row["out_p"] - row["lp_int"]), abs(row["out_n"] - row["lm_int"])) for row in rows],
        0.95,
    )
    if mirror_error > 0.08:
        return False, diagnostic(
            "P_BUNDLE_BINDING", "behavior_mismatch", expected="LP=DCMPP,LM=DCMPN",
            observed=f"mirror_error_p95:{mirror_error:.4f}", event="full_trace",
        )
    if timer_checks < 4 or reset_checks < 4:
        return False, diagnostic(
            "P_EDGE_INTERVAL_MEASUREMENT", "insufficient_excitation",
            expected="timer_checks>=4,reset_checks>=4",
            observed=f"timer_checks:{timer_checks},reset_checks:{reset_checks}", event="full_trace",
        )
    return True, pass_note(
        PROPERTY_IDS,
        "cmp_delay groups=" + ",".join(f"{diff:.2g}V:{delay * 1e12:.2f}ps" for diff, delay in trend),
    )


CHECKER_ID = "v4_039_propagation_delay_comparator"
CHECKER: Checker = check_cmp_delay
