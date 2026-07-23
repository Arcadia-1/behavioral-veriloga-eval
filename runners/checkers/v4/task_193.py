"""Task-specific checker for canonical v4 DUT 193."""
from __future__ import annotations

from ..api import Checker, Row
from .trace_utils import median_step, property_diagnostics, sample_signal, threshold_crossings

PUBLIC_TON_S = 120e-12
PROPERTIES = {
    "P_LEADING_EDGE_DIRECTION": 0,
    "P_RESET_OVERLAP_WINDOW": 0,
    "P_CLEAR_AFTER_RESET_WINDOW": 0,
    "P_PFD_OUTPUT_LEVELS": 0,
}


def _rail_bounds(rows: list[Row]) -> tuple[float, float]:
    high = max(row["vdd"] for row in rows)
    low = min(row["gnd"] for row in rows)
    return high, low


def _check_outputs(
    rows: list[Row],
    counts: dict[str, int],
    time_s: float,
    *,
    up_high: bool,
    dn_high: bool,
    property_id: str,
    high: float,
    low: float,
    tol: float,
) -> float | None:
    up = sample_signal(rows, "up", time_s)
    dn = sample_signal(rows, "dn", time_s)
    if up is None or dn is None:
        counts[property_id] += 1
        return None
    expected_up = high if up_high else low
    expected_dn = high if dn_high else low
    max_err = max(abs(up - expected_up), abs(dn - expected_dn))
    if abs(up - expected_up) > tol or abs(dn - expected_dn) > tol:
        counts[property_id] += 1
        counts["P_PFD_OUTPUT_LEVELS"] += 1
    return max_err


def _has_complete_input_pulse(rows: list[Row], threshold: float) -> bool:
    for signal in ("in1", "in2"):
        rises = threshold_crossings(rows, signal, threshold=threshold, direction=1)
        falls = threshold_crossings(rows, signal, threshold=threshold, direction=-1)
        for rise in rises:
            if any(event_time > rise for event_time in falls):
                return True
    return False


def _fall_start_after(
    rows: list[Row],
    signal: str,
    after_s: float,
    high: float,
    low: float,
) -> tuple[float, float] | None:
    span = high - low
    high_falls = threshold_crossings(
        rows, signal, threshold=low + 0.8 * span, direction=-1
    )
    low_falls = threshold_crossings(
        rows, signal, threshold=low + 0.2 * span, direction=-1
    )
    high_crossing = next((time_s for time_s in high_falls if time_s > after_s), None)
    if high_crossing is None:
        return None
    low_crossing = next(
        (time_s for time_s in low_falls if time_s >= high_crossing), None
    )
    if low_crossing is None:
        return None
    slew_20_80 = low_crossing - high_crossing
    fall_start = high_crossing - slew_20_80 / 3.0
    return fall_start, slew_20_80


def _edge_pairs(
    rows: list[Row], threshold: float, reset_window_s: float
) -> list[tuple[str, float, float]]:
    events = sorted(
        [
            *[(time_s, "in1") for time_s in threshold_crossings(rows, "in1", threshold=threshold, direction=1)],
            *[(time_s, "in2") for time_s in threshold_crossings(rows, "in2", threshold=threshold, direction=1)],
        ]
    )
    pairs: list[tuple[str, float, float]] = []
    armed_signal: str | None = None
    armed_time = 0.0
    suppress_until = rows[0]["time"]
    for event_time, signal in events:
        if event_time < suppress_until:
            continue
        if armed_signal is None:
            armed_signal = signal
            armed_time = event_time
            continue
        if signal == armed_signal:
            armed_time = event_time
            continue
        pairs.append((armed_signal, armed_time, event_time))
        armed_signal = None
        suppress_until = event_time + reset_window_s
    return pairs


def check_v3_pfd_tdomain_reset_window(rows: list[Row]) -> tuple[bool, str]:
    required = {"time", "in1", "in2", "up", "dn", "vdd", "gnd"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing pfd tdomain reset window signals"

    high, low = _rail_bounds(rows)
    if high - low < 0.5:
        return False, f"insufficient_excitation pfd_tdomain_reset_window rail_span={high - low:.4g}"

    threshold = low + 0.5 * (high - low)
    if not _has_complete_input_pulse(rows, threshold):
        return (
            False,
            "insufficient_excitation pfd_tdomain_reset_window "
            "complete_input_pulses=0",
        )
    reset_window_s = PUBLIC_TON_S
    pairs = _edge_pairs(rows, threshold, reset_window_s)
    if not pairs:
        return (
            False,
            "insufficient_excitation pfd_tdomain_reset_window "
            "opposite input edge pairs=0",
        )

    counts = dict(PROPERTIES)
    tol = max(0.08, 0.12 * (high - low))
    step = median_step(rows)
    settle = max(step * 5.0, 0.25 * reset_window_s)
    max_err = 0.0
    max_reset_err = 0.0
    max_fall_slew = 0.0
    max_timing_tol = 0.0
    checked = 0

    for leading_signal, leading_time, second_time in pairs:
        gap = second_time - leading_time
        if gap <= settle * 2.0:
            counts["P_LEADING_EDGE_DIRECTION"] += 1
            continue

        direction_time = min(leading_time + max(settle, gap * 0.25), second_time - settle)
        err = _check_outputs(
            rows,
            counts,
            direction_time,
            up_high=leading_signal == "in1",
            dn_high=leading_signal == "in2",
            property_id="P_LEADING_EDGE_DIRECTION",
            high=high,
            low=low,
            tol=tol,
        )
        if err is not None:
            max_err = max(max_err, err)
            checked += 1

        overlap_time = second_time + 0.5 * reset_window_s
        if overlap_time <= rows[-1]["time"]:
            err = _check_outputs(
                rows,
                counts,
                overlap_time,
                up_high=True,
                dn_high=True,
                property_id="P_RESET_OVERLAP_WINDOW",
                high=high,
                low=low,
                tol=tol,
            )
            if err is not None:
                max_err = max(max_err, err)
                checked += 1

        clear_estimates = [
            _fall_start_after(rows, signal, second_time, high, low)
            for signal in ("up", "dn")
        ]
        if any(estimate is None for estimate in clear_estimates):
            counts["P_CLEAR_AFTER_RESET_WINDOW"] += 1
            counts["P_PFD_OUTPUT_LEVELS"] += 1
            continue
        up_estimate, dn_estimate = clear_estimates
        assert up_estimate is not None and dn_estimate is not None
        up_clear, up_slew = up_estimate
        dn_clear, dn_slew = dn_estimate
        fall_slew = max(up_slew, dn_slew)
        timing_tol = max(
            2.0 * step,
            min(0.5 * fall_slew + step, 0.15 * reset_window_s),
        )
        max_fall_slew = max(max_fall_slew, fall_slew)
        max_timing_tol = max(max_timing_tol, timing_tol)
        common_clear = 0.5 * (up_clear + dn_clear)
        observed_window = common_clear - second_time
        reset_err = abs(observed_window - reset_window_s)
        max_reset_err = max(max_reset_err, reset_err)
        if (
            reset_err > timing_tol
            or abs(up_clear - dn_clear) > timing_tol
            or abs(up_slew - dn_slew) > timing_tol
        ):
            counts["P_CLEAR_AFTER_RESET_WINDOW"] += 1
        checked += 1

    if checked < 3:
        return (
            False,
            "insufficient_excitation pfd_tdomain_reset_window "
            f"pairs={len(pairs)} checked_windows={checked}",
        )

    ok = all(count == 0 for count in counts.values())
    return (
        ok,
        f"{property_diagnostics(counts)}; pairs={len(pairs)}; "
        f"checked_windows={checked}; max_err={max_err:.6g}; "
        f"max_reset_err_s={max_reset_err:.6g}; "
        f"max_fall_slew_20_80_s={max_fall_slew:.6g}; "
        f"max_timing_tol_s={max_timing_tol:.6g}",
    )


CHECKER_ID = "v4_193_pfd_tdomain_reset_window"
CHECKER: Checker = check_v3_pfd_tdomain_reset_window
