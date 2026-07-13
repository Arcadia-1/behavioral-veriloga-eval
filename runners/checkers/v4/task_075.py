"""Task-specific checker for canonical v4 DUT 075."""
from __future__ import annotations

from checkers.api import Checker
def check_peak_detector(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin", "rst", "vout"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/vin/rst/vout"

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
        if stop - start < 8.0e-9:
            continue
        span_rows = [row for row in rows if start + 1.0e-9 <= row["time"] <= stop - 1.0e-9]
        if len(span_rows) < 4:
            continue
        expected_peak = max(row["vin"] for row in span_rows)
        tail_rows = span_rows[-max(3, len(span_rows) // 5):]
        observed_peak = sum(row["vout"] for row in tail_rows) / len(tail_rows)
        peak_checks += 1
        err = abs(observed_peak - expected_peak)
        peak_notes.append(f"{observed_peak:.3f}/{expected_peak:.3f}")
        if err <= 0.06:
            peak_ok += 1

    if clear_checks < 1 or clear_ok < clear_checks:
        return False, f"reset_clear={clear_ok}/{clear_checks}"
    if peak_checks < 2 or peak_ok < peak_checks:
        return False, f"peak_hold={peak_ok}/{peak_checks} values={peak_notes}"
    return True, f"reset_clear={clear_ok}/{clear_checks} peak_hold={peak_ok}/{peak_checks} values={peak_notes}"

def check_v4_peak_detector(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin", "rst", "vout"}
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0].keys())) if rows else sorted(required)
        return False, "missing_columns=" + ",".join(missing[:12])
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
        return False, "peak_reset_not_observable observed=reset_rows:0 expected=>0 window=full_trace"
    reset_peak = max(row["vout"] for row in reset_rows)
    if reset_peak > 0.12:
        return False, f"peak_reset_clear observed=vout_peak:{reset_peak:.3f} expected<=0.12 window=rst_high"
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
        prev_vout = segment[0]["vout"]
        for row in segment[1:]:
            if row["vout"] + 0.04 < prev_vout:
                failures.append(
                    f"monotonic_hold observed=vout:{prev_vout:.3f}->{row['vout']:.3f} "
                    f"expected=nondecreasing window={row['time'] * 1e9:.3f}ns"
                )
                break
            prev_vout = row["vout"]
        prev_vout = segment[0]["vout"]
        for row in segment[:: max(1, len(segment) // 40)]:
            expected_peak = max(expected_peak, row["vin"])
            err = max(0.0, row["vout"] - expected_peak)
            max_err = max(max_err, err)
            if err > 0.08:
                failures.append(
                    f"peak_above_observed_input observed=vout:{row['vout']:.3f} "
                    f"expected<=peak_so_far:{expected_peak:.3f} window={row['time'] * 1e9:.3f}ns"
                )
            prev_vout = row["vout"]
            checks += 1
    if checks < 12:
        failures.append(f"insufficient_peak_checks observed={checks} expected>=12 window=non_reset_segments")
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
                f"output_smoothing observed=max_step:{max_step:.3f} expected<=0.40 "
                f"window={step_time * 1e9:.3f}ns"
            )
    return True, f"{base_note} reset_peak={reset_peak:.3f} monotonic_checks={checks} max_err={max_err:.4f}"

check_vbm1_peak_detector = check_peak_detector

CHECKER_ID = "v4_075_peak_detector"
CHECKER: Checker = check_v4_peak_detector
