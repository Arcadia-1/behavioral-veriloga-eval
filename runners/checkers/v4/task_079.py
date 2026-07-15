"""Task-specific checker for canonical v4 DUT 079."""
from __future__ import annotations

from ..api import Checker
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

def check_bound_step_period_guard(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "guard_out", "phase_out"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/guard_out/phase_out"
    g = [r["guard_out"] for r in rows]
    p = [r["phase_out"] for r in rows]
    t = [r["time"] for r in rows]
    gth = 0.5 * (max(g) + min(g))
    guard_hi_frac = weighted_logic_high_fraction(rows, "guard_out", gth)
    if not (0.08 <= guard_hi_frac <= 0.30):
        return False, f"guard_hi_frac_out_of_range={guard_hi_frac:.3f}"
    wraps = sum(1 for i in range(1, len(p)) if p[i] < p[i - 1] - 0.2)
    phase_span = max(p) - min(p)
    guard_rises = len(rising_edges(g, t, threshold=gth))
    rail_checks = 0
    max_phase_err = 0.0
    max_guard_err = 0.0
    rail_failure = ""
    if {"VDD", "VSS"}.issubset(rows[0]):
        guard_edges = rising_edges(g, t, threshold=gth)
        wrap_times = [
            t[idx]
            for idx in range(1, len(p))
            if p[idx] < p[idx - 1] - 0.2
        ]
        if len(wrap_times) >= 2:
            wrap_periods = sorted(b - a for a, b in zip(wrap_times, wrap_times[1:]))
            period = wrap_periods[len(wrap_periods) // 2]
            t0 = wrap_times[0]
        elif len(guard_edges) >= 2:
            guard_periods = sorted(b - a for a, b in zip(guard_edges, guard_edges[1:]))
            period = guard_periods[len(guard_periods) // 2]
            t0 = guard_edges[0]
        else:
            period = 8.0e-9
            t0 = rows[0]["time"]
        # Check recorded solver points directly. Interpolating a sawtooth across
        # the two samples that bracket a wrap invents a falling ramp which the
        # behavioral source never produced; the same applies to smoothed guard
        # edges. The recorded points already provide ample phase/rail coverage.
        for row in rows:
            sample_t = row["time"]
            if sample_t < t0 + 0.10e-9:
                continue
            vdd = float(row["VDD"])
            vss = float(row["VSS"])
            span = vdd - vss
            if span <= 0.2:
                continue
            phase = ((sample_t - t0) % period) / period
            expected_phase = vss + span * phase
            guard_observed = float(row["guard_out"])
            guard_norm = (guard_observed - vss) / span
            if 0.15 < guard_norm < 0.85:
                continue
            expected_guard = vdd if guard_norm >= 0.5 else vss
            phase_err = abs(float(row["phase_out"]) - expected_phase)
            guard_err = abs(guard_observed - expected_guard)
            max_guard_err = max(max_guard_err, guard_err)
            rail_checks += 1
            phase_time = (sample_t - t0) % period
            edge_margin = min(phase_time, period - phase_time)
            if edge_margin > 0.15e-9:
                max_phase_err = max(max_phase_err, phase_err)
            if edge_margin > 0.15e-9 and (phase_err > 0.055 or guard_err > 0.055):
                rail_failure = (
                    f"rail_tracking observed=phase:{float(row['phase_out']):.3f},guard:{guard_observed:.3f} "
                    f"expected=phase:{expected_phase:.3f},guard:{expected_guard:.3f} "
                    f"window={sample_t * 1e9:.3f}ns"
                )
                break
        if rail_checks < 20:
            rail_failure = f"insufficient_rail_tracking_samples observed={rail_checks} expected>=20 window=full_trace"
    if rail_failure:
        return False, rail_failure
    ok = wraps >= 3 and phase_span > 0.5 and guard_rises >= 3
    return ok, (
        f"guard_rises={guard_rises} wraps={wraps} phase_span={phase_span:.3f} "
        f"guard_hi_frac={guard_hi_frac:.3f} rail_checks={rail_checks} "
        f"max_phase_err={max_phase_err:.3f} max_guard_err={max_guard_err:.3f}"
    )

CHECKER_ID = "v4_079_ramp_step_source"
CHECKER: Checker = check_bound_step_period_guard
