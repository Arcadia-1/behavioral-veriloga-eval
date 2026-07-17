"""Task-specific checker for canonical v4 DUT 075."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import diagnostic, pass_note, require_signals


PROPERTY_IDS = (
    "P_INITIAL_ZERO",
    "P_SAMPLED_MEASUREMENT",
    "P_MAX_RETENTION",
    "P_MONOTONIC_HOLD",
    "P_RESET_CLEAR",
    "P_OUTPUT_SMOOTHING",
)


def check_peak_detector(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin", "rst", "vout"}
    missing = require_signals(rows, required, "P_SAMPLED_MEASUREMENT")
    if missing is not None:
        return False, missing

    vth = 0.45
    times = [row["time"] for row in rows]
    inactive_spans: list[tuple[float, float]] = []
    reset_spans: list[tuple[float, float]] = []
    span_start = times[0]
    in_reset = rows[0]["rst"] > vth
    for prev, cur in zip(rows, rows[1:]):
        cur_reset = cur["rst"] > vth
        if cur_reset != in_reset:
            span_end = cur["time"]
            if in_reset:
                reset_spans.append((span_start, span_end))
            else:
                inactive_spans.append((span_start, span_end))
            span_start = cur["time"]
            in_reset = cur_reset
    if in_reset:
        reset_spans.append((span_start, times[-1]))
    else:
        inactive_spans.append((span_start, times[-1]))

    clear_checks = clear_ok = 0
    for start, stop in reset_spans:
        vals = [row["vout"] for row in rows if start + 1.0e-9 <= row["time"] <= stop - 0.3e-9]
        if vals:
            clear_checks += 1
            if max(vals) < 0.08:
                clear_ok += 1

    peak_checks = peak_ok = 0
    peak_notes: list[str] = []
    for start, stop in inactive_spans:
        # Four 500 ps sample periods are sufficient to exercise capture and
        # retention; reset-separated custom decks need not use gold's span.
        if stop - start < 2.0e-9:
            continue
        margin = min(0.1e-9, 0.05 * (stop - start))
        span_rows = [row for row in rows if start + margin <= row["time"] <= stop - margin]
        if len(span_rows) < 4:
            continue
        expected_peak = max(row["vin"] for row in span_rows)
        observed_peak = max(row["vout"] for row in span_rows)
        peak_checks += 1
        err = abs(observed_peak - expected_peak)
        peak_notes.append(f"{observed_peak:.3f}/{expected_peak:.3f}")
        if err <= 0.06:
            peak_ok += 1

    if clear_checks < 1 or clear_ok < clear_checks:
        return False, diagnostic(
            "P_RESET_CLEAR",
            "value_mismatch",
            expected=f"reset_clear:{clear_checks}/{clear_checks}",
            observed=f"reset_clear:{clear_ok}/{clear_checks}",
            event="rst_high_segments",
        )
    if peak_checks < 2 or peak_ok < peak_checks:
        return False, diagnostic(
            "P_MAX_RETENTION",
            "value_mismatch",
            expected=f"peak_hold:{peak_checks}/{peak_checks}",
            observed=f"peak_hold:{peak_ok}/{peak_checks}",
            event="non_reset_segments",
        )
    return True, f"reset_clear={clear_ok}/{clear_checks} peak_hold={peak_ok}/{peak_checks} values={peak_notes}"

def check_v4_peak_detector(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin", "rst", "vout"}
    missing = require_signals(rows, required, "P_SAMPLED_MEASUREMENT")
    if missing is not None:
        return False, missing
    base_ok, base_note = check_vbm1_peak_detector(rows)
    if not base_ok:
        return False, base_note
    reset_rows: list[dict[str, float]] = []
    reset_start: float | None = rows[0]["time"] if rows[0]["rst"] > 0.45 else None
    for row in rows:
        if row["rst"] > 0.45:
            if reset_start is None:
                reset_start = row["time"]
            if row["time"] - reset_start >= 1.20e-9:
                reset_rows.append(row)
        else:
            reset_start = None
    if not reset_rows:
        return False, diagnostic(
            "P_RESET_CLEAR",
            "missing_event",
            expected="reset_rows>0",
            observed="reset_rows:0",
            event="full_trace",
        )
    reset_peak = max(row["vout"] for row in reset_rows)
    if reset_peak > 0.12:
        return False, diagnostic(
            "P_RESET_CLEAR",
            "value_mismatch",
            expected="vout_peak<=0.12",
            observed=f"vout_peak:{reset_peak:.3f}",
            event="rst_high",
        )
    segments: list[list[dict[str, float]]] = []
    current: list[dict[str, float]] = []
    for row in rows:
        if row["rst"] > 0.45:
            if current:
                segments.append(current)
                current = []
        else:
            current.append(row)
    if current:
        segments.append(current)
    checks = 0
    max_err = 0.0
    failures: list[str] = []
    for segment in segments:
        if len(segment) < 4:
            continue
        expected_peak = 0.0
        held_vout = segment[0]["vout"]
        for row in segment[1:]:
            if row["vout"] + 0.04 < held_vout:
                failures.append(
                    diagnostic(
                        "P_MONOTONIC_HOLD",
                        "value_mismatch",
                        expected="nondecreasing_vout",
                        observed=f"vout:{held_vout:.3f}->{row['vout']:.3f}",
                        event="non_reset_segment",
                    )
                )
                break
            held_vout = max(held_vout, row["vout"])
        for row in segment[:: max(1, len(segment) // 40)]:
            expected_peak = max(expected_peak, row["vin"])
            err = max(0.0, row["vout"] - expected_peak)
            max_err = max(max_err, err)
            if err > 0.08:
                failures.append(
                    diagnostic(
                        "P_SAMPLED_MEASUREMENT",
                        "value_mismatch",
                        expected=f"vout<=peak_so_far:{expected_peak:.3f}",
                        observed=f"vout:{row['vout']:.3f}",
                        event="non_reset_segment",
                    )
                )
            checks += 1
    if checks < 12:
        failures.append(
            diagnostic(
                "P_MAX_RETENTION",
                "missing_event",
                expected="peak_checks>=12",
                observed=f"peak_checks:{checks}",
                event="non_reset_segments",
            )
        )
    if failures:
        return False, " ".join(failures[:5])
    non_reset_steps = [
        (rows[idx]["time"], rows[idx]["vout"] - rows[idx - 1]["vout"])
        for idx in range(1, len(rows))
        if rows[idx]["rst"] <= 0.45 and rows[idx - 1]["rst"] <= 0.45
    ]
    if non_reset_steps:
        step_time, max_step = max(non_reset_steps, key=lambda item: item[1])
        if max_step > 0.40:
            return False, (
                diagnostic(
                    "P_OUTPUT_SMOOTHING",
                    "value_mismatch",
                    expected="max_step<=0.40",
                    observed=f"max_step:{max_step:.3f}",
                    event="non_reset_step",
                )
            )
    return True, pass_note(
        PROPERTY_IDS,
        f"{base_note} reset_peak={reset_peak:.3f} monotonic_checks={checks} max_err={max_err:.4f}",
    )

check_vbm1_peak_detector = check_peak_detector

CHECKER_ID = "v4_075_peak_detector"
CHECKER: Checker = check_v4_peak_detector
