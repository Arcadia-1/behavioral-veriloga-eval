"""Task-specific checker for canonical v4 DUT 079."""
from __future__ import annotations

from statistics import median

from ..api import Checker
from .stimulus_relative import diagnostic, pass_note, require_signals


PROPERTY_IDS = (
    "P_PHASE_RAMP",
    "P_PHASE_WRAP",
    "P_GUARD_WINDOW",
    "P_GUARD_LOW",
    "P_RAIL_TRACKING",
    "P_PERIODICITY",
)


def rising_edges(values: list[float], times: list[float], threshold: float = 0.45) -> list[float]:
    edges: list[float] = []
    for i in range(1, len(values)):
        if values[i - 1] < threshold <= values[i]:
            edges.append(times[i])
    return edges


def weighted_logic_high_fraction(rows: list[dict[str, float]], signal: str, threshold: float) -> float:
    if len(rows) < 2:
        return 0.0
    total_dt = rows[-1]["time"] - rows[0]["time"]
    if total_dt <= 0.0:
        return 0.0

    high_dt = 0.0
    for idx in range(1, len(rows)):
        dt = rows[idx]["time"] - rows[idx - 1]["time"]
        if dt <= 0.0:
            continue
        v_mid = 0.5 * (rows[idx - 1][signal] + rows[idx][signal])
        if v_mid > threshold:
            high_dt += dt
    return high_dt / total_dt


def _normalized_phase(row: dict[str, float]) -> float | None:
    vdd = float(row["VDD"])
    vss = float(row["VSS"])
    span = vdd - vss
    if span <= 0.2:
        return None
    return (float(row["phase_out"]) - vss) / span


def _infer_phase_timing(
    rows: list[dict[str, float]],
    wrap_indices: list[int],
) -> tuple[float, float, float] | None:
    normalized = [_normalized_phase(row) for row in rows]
    positive_slopes: list[float] = []
    for index in range(1, len(rows)):
        before = normalized[index - 1]
        after = normalized[index]
        dt = float(rows[index]["time"]) - float(rows[index - 1]["time"])
        if before is None or after is None or dt <= 0.0:
            continue
        phase_delta = after - before
        if 0.0 < phase_delta < 0.25:
            positive_slopes.append(phase_delta / dt)
    if len(positive_slopes) < 4:
        return None

    phase_slope = median(positive_slopes)
    if phase_slope <= 0.0:
        return None
    period = 1.0 / phase_slope

    wrap_origins: list[float] = []
    for index in wrap_indices:
        phase = normalized[index]
        if phase is None or not (-0.1 <= phase <= 0.35):
            continue
        sample_t = float(rows[index]["time"])
        wrap_origins.append(sample_t - phase * period)
    if len(wrap_origins) < 2:
        return None

    period_errors = [
        abs((after - before) - period) / period
        for before, after in zip(wrap_origins, wrap_origins[1:])
    ]
    max_period_error = max(period_errors, default=0.0)
    if max_period_error > 0.15:
        return None

    aligned_origins = [
        origin - ordinal * period
        for ordinal, origin in enumerate(wrap_origins)
    ]
    t0 = median(aligned_origins)
    max_origin_error = max(abs(origin - t0) / period for origin in aligned_origins)
    if max_origin_error > 0.15:
        return None
    return period, t0, max(max_period_error, max_origin_error)


def check_bound_step_period_guard(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "guard_out", "phase_out"}
    missing = require_signals(rows, required, "P_PHASE_RAMP")
    if missing is not None:
        return False, missing
    g = [r["guard_out"] for r in rows]
    p = [r["phase_out"] for r in rows]
    t = [r["time"] for r in rows]
    gth = 0.5 * (max(g) + min(g))
    guard_hi_frac = weighted_logic_high_fraction(rows, "guard_out", gth)
    if not (0.08 <= guard_hi_frac <= 0.30):
        return False, diagnostic(
            "P_GUARD_WINDOW",
            "value_mismatch",
            expected="guard_hi_fraction:0.08..0.30",
            observed=f"guard_hi_fraction:{guard_hi_frac:.3f}",
            event="full_trace",
        )
    wraps = sum(1 for i in range(1, len(p)) if p[i] < p[i - 1] - 0.2)
    phase_span = max(p) - min(p)
    guard_rises = len(rising_edges(g, t, threshold=gth))
    rail_checks = 0
    max_phase_err = 0.0
    max_guard_err = 0.0
    rail_failure = ""
    if {"VDD", "VSS"}.issubset(rows[0]):
        guard_edges = rising_edges(g, t, threshold=gth)
        wrap_indices = [
            idx
            for idx in range(1, len(p))
            if p[idx] < p[idx - 1] - 0.2
        ]
        phase_timing = _infer_phase_timing(rows, wrap_indices)
        if phase_timing is None:
            return False, diagnostic(
                "P_PERIODICITY",
                "missing_event",
                expected="stable_positive_phase_slope_and_corrected_wrap_origins>=2",
                observed=f"phase_wraps:{len(wrap_indices)},guard_rises:{len(guard_edges)}",
                event="full_trace",
            )
        period, t0, _period_error = phase_timing
        edge_guard = 0.02 * period
        guard_transition_times = [
            t[idx]
            for idx in range(1, len(g))
            if (g[idx - 1] < gth <= g[idx]) or (g[idx - 1] >= gth > g[idx])
        ]
        # Check recorded solver points directly. Interpolating a sawtooth across
        # the two samples that bracket a wrap invents a falling ramp which the
        # behavioral source never produced; the same applies to smoothed guard
        # edges. The recorded points already provide ample phase/rail coverage.
        for row in rows:
            sample_t = row["time"]
            if sample_t < t0 + edge_guard:
                continue
            vdd = float(row["VDD"])
            vss = float(row["VSS"])
            span = vdd - vss
            if span <= 0.2:
                continue
            phase = ((sample_t - t0) % period) / period
            expected_phase = vss + span * phase
            guard_observed = float(row["guard_out"])
            if abs(guard_observed - vdd) <= abs(guard_observed - vss):
                expected_guard = vdd
            else:
                expected_guard = vss
            phase_err = abs(float(row["phase_out"]) - expected_phase)
            guard_err = abs(guard_observed - expected_guard)
            if any(abs(sample_t - edge_time) <= edge_guard for edge_time in guard_transition_times):
                continue
            max_guard_err = max(max_guard_err, guard_err)
            rail_checks += 1
            phase_time = (sample_t - t0) % period
            edge_margin = min(phase_time, period - phase_time)
            if edge_margin > edge_guard:
                max_phase_err = max(max_phase_err, phase_err)
            if edge_margin > edge_guard and (phase_err > 0.055 or guard_err > 0.055):
                rail_failure = diagnostic(
                    "P_RAIL_TRACKING",
                    "value_mismatch",
                    expected=f"phase:{expected_phase:.3f},guard:{expected_guard:.3f}",
                    observed=f"phase:{float(row['phase_out']):.3f},guard:{guard_observed:.3f}",
                    event="periodic_sample",
                )
                break
        if rail_checks < 20 and not rail_failure:
            rail_failure = diagnostic(
                "P_RAIL_TRACKING",
                "missing_event",
                expected="rail_tracking_samples>=20",
                observed=f"rail_tracking_samples:{rail_checks}",
                event="full_trace",
            )
    if rail_failure:
        return False, rail_failure
    ok = wraps >= 3 and phase_span > 0.5 and guard_rises >= 3
    note = (
        f"guard_rises={guard_rises} wraps={wraps} phase_span={phase_span:.3f} "
        f"guard_hi_frac={guard_hi_frac:.3f} rail_checks={rail_checks} "
        f"max_phase_err={max_phase_err:.3f} max_guard_err={max_guard_err:.3f}"
    )
    if not ok:
        return False, diagnostic(
            "P_PHASE_WRAP",
            "missing_event",
            expected="wraps>=3,guard_rises>=3,phase_span>0.5",
            observed=f"wraps:{wraps},guard_rises:{guard_rises},phase_span:{phase_span:.3f}",
            event="full_trace",
        )
    return True, pass_note(PROPERTY_IDS, note)

CHECKER_ID = "v4_079_ramp_step_source"
CHECKER: Checker = check_bound_step_period_guard
