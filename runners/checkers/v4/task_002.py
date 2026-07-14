"""Task-specific checker for canonical v4 DUT 002."""
from __future__ import annotations

from checkers.api import Checker
def rising_edges(values: list[float], times: list[float], threshold: float = 0.45) -> list[float]:
    edges: list[float] = []
    for i in range(1, len(values)):
        if values[i - 1] < threshold <= values[i]:
            edges.append(times[i])
    return edges

def sample_signal_at(rows: list[dict[str, float]], signal: str, time_s: float) -> float | None:
    if not rows or "time" not in rows[0] or signal not in rows[0]:
        return None
    first_time = rows[0]["time"]
    last_time = rows[-1].get("time")
    if last_time is None or time_s < first_time or time_s > last_time:
        return None
    if time_s == first_time:
        return rows[0].get(signal)
    for idx in range(1, len(rows)):
        prev = rows[idx - 1]
        cur = rows[idx]
        t0 = prev.get("time")
        t1 = cur.get("time")
        if t0 is None or t1 is None:
            continue
        if t0 <= time_s <= t1:
            v0 = prev.get(signal)
            v1 = cur.get(signal)
            if v0 is None or v1 is None:
                return None
            if t1 == t0:
                return v1
            alpha = (time_s - t0) / (t1 - t0)
            return v0 + alpha * (v1 - v0)
    return None

def check_v3_cdac_feedback_dac(rows: list[dict[str, float]]) -> tuple[bool, str]:
    """V3 CDAC: verify sampled binary code, calibration offset, polarity, and common-mode."""
    required = {"time", "clk", "cal0", "cal1", "vdac_p", "vdac_n"} | {f"d{i}" for i in range(10)}
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0].keys())) if rows else sorted(required)
        return False, "missing_columns=" + ",".join(missing[:16])

    times = [r["time"] for r in rows]
    clk_edges = rising_edges([r["clk"] for r in rows], times)
    if len(clk_edges) < 8:
        return False, f"clk_edges={len(clk_edges)}"

    checked = 0
    mismatches = 0
    max_diff_error = 0.0
    max_cm_error = 0.0
    effective_codes: list[int] = []
    actual_diffs: list[float] = []
    cal_codes: set[int] = set()
    main_codes: set[int] = set()

    for edge_t in clk_edges:
        sample_t = edge_t + 0.8e-9
        vdac_p = sample_signal_at(rows, "vdac_p", sample_t)
        vdac_n = sample_signal_at(rows, "vdac_n", sample_t)
        if vdac_p is None or vdac_n is None:
            continue

        main_code = 0
        missing_input = False
        for bit in range(10):
            value = sample_signal_at(rows, f"d{bit}", edge_t)
            if value is None:
                missing_input = True
                break
            if value > 0.45:
                main_code |= 1 << bit
        cal0 = sample_signal_at(rows, "cal0", edge_t)
        cal1 = sample_signal_at(rows, "cal1", edge_t)
        if missing_input or cal0 is None or cal1 is None:
            continue

        cal_code = (1 if cal0 > 0.45 else 0) | (2 if cal1 > 0.45 else 0)
        effective_code = main_code + 32 * cal_code
        expected_diff = 0.6 * ((effective_code / 1023.0) - 0.5)
        actual_diff = vdac_p - vdac_n
        diff_error = abs(actual_diff - expected_diff)
        cm_error = abs(0.5 * (vdac_p + vdac_n) - 0.45)

        checked += 1
        main_codes.add(main_code)
        cal_codes.add(cal_code)
        effective_codes.append(effective_code)
        actual_diffs.append(actual_diff)
        max_diff_error = max(max_diff_error, diff_error)
        max_cm_error = max(max_cm_error, cm_error)
        if diff_error > 0.025 or cm_error > 0.020:
            mismatches += 1

    if checked < 8:
        return False, f"settled_samples={checked}"
    if not {0, 1, 2, 3}.issubset(cal_codes):
        return False, f"cal_coverage={sorted(cal_codes)}"
    if not ({0, 1023}.issubset(main_codes) and any(450 <= code <= 573 for code in main_codes)):
        return False, f"main_code_coverage={sorted(main_codes)[:12]}"

    monotonic_errors = 0
    ordered = sorted(zip(effective_codes, actual_diffs), key=lambda item: item[0])
    for (_, prev_diff), (_, cur_diff) in zip(ordered, ordered[1:]):
        if cur_diff + 0.015 < prev_diff:
            monotonic_errors += 1

    diff_span = max(actual_diffs) - min(actual_diffs) if actual_diffs else 0.0
    ok = mismatches == 0 and monotonic_errors == 0 and diff_span > 0.55 and max_cm_error <= 0.020
    return ok, (
        f"samples={checked} main_codes={len(main_codes)} cal_codes={sorted(cal_codes)} "
        f"mismatches={mismatches} monotonic_errors={monotonic_errors} "
        f"diff_span={diff_span:.4f} max_diff_error={max_diff_error:.4f} "
        f"max_cm_error={max_cm_error:.4f}"
    )

def _v4_edge_times(
    rows: list[dict[str, float]], signal: str, *, rising: bool, threshold: float = 0.45
) -> list[float]:
    times: list[float] = []
    for previous, current in zip(rows, rows[1:]):
        before = previous[signal]
        after = current[signal]
        if rising and before < threshold <= after:
            times.append(current["time"])
        elif not rising and before > threshold >= after:
            times.append(current["time"])
    return times

def _v4_hold_spans(
    rows: list[dict[str, float]],
    signal: str,
    edge_times: list[float],
    *,
    settle_s: float,
    guard_s: float,
) -> list[tuple[float, float, float]]:
    spans: list[tuple[float, float, float]] = []
    for start, stop in zip(edge_times, edge_times[1:]):
        window_start = start + settle_s
        window_stop = stop - guard_s
        values = [
            row[signal]
            for row in rows
            if window_start <= row["time"] <= window_stop
        ]
        if len(values) >= 2:
            spans.append((window_start, window_stop, max(values) - min(values)))
    return spans

def check_v4_cdac_feedback_dac(rows: list[dict[str, float]]) -> tuple[bool, str]:
    base_ok, base_note = check_v3_cdac_feedback_dac(rows)
    required = {"time", "clk", "vdac_p", "vdac_n"}
    if not rows or not required.issubset(rows[0]):
        return False, base_note

    clock_edges = _v4_edge_times(rows, "clk", rising=True)
    p_spans = _v4_hold_spans(
        rows, "vdac_p", clock_edges, settle_s=0.25e-9, guard_s=0.20e-9
    )
    n_spans = _v4_hold_spans(
        rows, "vdac_n", clock_edges, settle_s=0.25e-9, guard_s=0.20e-9
    )
    violations = [
        (start, stop, max(p_span, n_span))
        for (start, stop, p_span), (_, _, n_span) in zip(p_spans, n_spans)
        if max(p_span, n_span) > 0.012
    ]
    max_hold_span = max((max(p[2], n[2]) for p, n in zip(p_spans, n_spans)), default=0.0)
    hold_ok = len(p_spans) >= 6 and not violations
    return base_ok and hold_ok, (
        f"{base_note} hold_intervals={len(p_spans)} hold_violations={len(violations)} "
        f"max_hold_span={max_hold_span:.4f}"
        + (
            " hold_detail="
            + ";".join(
                f"{start * 1e9:.3f}-{stop * 1e9:.3f}ns:{span:.4f}"
                for start, stop, span in violations[:4]
            )
            if violations
            else ""
        )
    )

CHECKER_ID = "v4_002_capacitive_weighted_sar_feedback_dac"
CHECKER: Checker = check_v4_cdac_feedback_dac
