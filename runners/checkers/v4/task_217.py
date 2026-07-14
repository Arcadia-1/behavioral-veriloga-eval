"""Task-specific checker for canonical v4 DUT 217."""
from __future__ import annotations

from checkers.api import Checker
def _threshold_crossings(
    values: list[float],
    times: list[float],
    *,
    threshold: float = 0.0,
    direction: str,
) -> list[float]:
    edges: list[float] = []
    for idx in range(1, len(values)):
        v0 = values[idx - 1]
        v1 = values[idx]
        if direction == "rising":
            hit = v0 <= threshold < v1
        elif direction == "falling":
            hit = v0 >= threshold > v1
        else:
            raise ValueError(f"unsupported direction={direction!r}")
        if not hit:
            continue
        t0 = times[idx - 1]
        t1 = times[idx]
        if v1 == v0:
            edges.append(t1)
        else:
            alpha = (threshold - v0) / (v1 - v0)
            edges.append(t0 + alpha * (t1 - t0))
    return edges

def _max_signal_value(
    rows: list[dict[str, float]],
    signals: list[str],
    *,
    default: float,
) -> float:
    values: list[float] = []
    for row in rows:
        for signal in signals:
            value = row.get(signal)
            if value is not None:
                values.append(value)
    return max(values) if values else default

def _v3_away_from_edges(row_time: float, edge_times: list[float], margin_s: float = 80e-12) -> bool:
    return all(abs(row_time - edge_time) > margin_s for edge_time in edge_times)

def check_v3_single_shot_timer_pulse(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin", "vout"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing single shot timer pulse signals"
    times = [row["time"] for row in rows]
    vhigh = _max_signal_value(rows, ["vin", "vout"], default=0.9)
    if vhigh < 0.5:
        vhigh = 0.9
    vtrans = 0.5 * vhigh
    edges = _threshold_crossings([row["vin"] for row in rows], times, threshold=vtrans, direction="rising")
    if len(edges) < 2:
        return False, f"too_few_trigger_edges={len(edges)}"

    high_checks = 0
    low_checks = 0
    high_failures = 0
    low_failures = 0
    max_err = 0.0
    failures: list[str] = []
    transition_times: list[float] = []
    for edge_t in edges:
        transition_times.extend([edge_t, edge_t + 0.12e-9, edge_t + 2.12e-9])

    stride = max(1, len(rows) // 120)
    for row in rows[::stride]:
        t = row["time"]
        if t < 0.05e-9 or not _v3_away_from_edges(t, transition_times, margin_s=90e-12):
            continue
        expected_high = any(edge_t + 0.18e-9 <= t <= edge_t + 2.10e-9 for edge_t in edges)
        expected = vhigh if expected_high else 0.0
        err = abs(row["vout"] - expected)
        max_err = max(max_err, err)
        if expected_high:
            high_checks += 1
        else:
            low_checks += 1
        if err > 0.10:
            failures.append(f"t={t * 1e9:.3f}ns vout={row['vout']:.3f} expected={expected:.3f}")
            if expected_high:
                high_failures += 1
            else:
                low_failures += 1

    output_edges = _threshold_crossings(
        [row["vout"] for row in rows], times, threshold=vtrans, direction="rising"
    )
    output_falls = _threshold_crossings(
        [row["vout"] for row in rows], times, threshold=vtrans, direction="falling"
    )
    pulse_count_errors = abs(len(output_edges) - len(edges))
    width_errors = 0
    for rise in output_edges:
        fall = next((time for time in output_falls if time > rise), None)
        if fall is None or abs((fall - rise) - 2.0e-9) > 0.25e-9:
            width_errors += 1
    coverage_errors = int(high_checks < 8) + int(low_checks < 8)
    detect_mismatches = high_failures + pulse_count_errors + int(len(edges) < 2)
    edge_drive_mismatches = high_failures
    timer_mismatches = width_errors + high_failures
    one_pulse_mismatches = pulse_count_errors + int(bool(output_edges) and not output_falls)
    low_hold_mismatches = low_failures
    ok = coverage_errors == 0 and not failures
    detail = " ".join(failures[:6]) or "pulse_samples_match"
    return ok, (
        f"{detail} trigger_edges={len(edges)} output_rises={len(output_edges)} output_falls={len(output_falls)} "
        f"high_checks={high_checks} low_checks={low_checks} max_err={max_err:.3f} coverage_errors={coverage_errors}; "
        f"P_DETECT_RISING_VIN_CROSSINGS_AT_VTRANS mismatch_count={detect_mismatches}; "
        f"P_ON_EACH_QUALIFYING_RISING_EDGE_DRIVE mismatch_count={edge_drive_mismatches}; "
        f"P_USE_A_TIMER_TO_SCHEDULE_THE mismatch_count={timer_mismatches}; "
        f"P_GENERATE_ONE_OUTPUT_PULSE_PER_INPUT mismatch_count={one_pulse_mismatches}; "
        f"P_HOLD_THE_LOW_OUTPUT_LEVEL_BETWEEN mismatch_count={low_hold_mismatches}"
    )

CHECKER_ID = "v4_217_single_shot_timer_pulse"
CHECKER: Checker = check_v3_single_shot_timer_pulse
