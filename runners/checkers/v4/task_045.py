"""Task-specific checker for canonical v4 DUT 045."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import diagnostic, pass_note, require_signals


PROPERTY_IDS = (
    "P_INITIAL_DECISION",
    "P_RISING_DIFFERENTIAL",
    "P_FALLING_DIFFERENTIAL",
    "P_BIDIRECTIONAL_RESPONSE",
    "P_RAIL_SMOOTHING",
)


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

def _conditional_time_fraction(
    rows: list[dict[str, float]],
    region_predicate,
    pass_predicate,
) -> float:
    """Time-weighted pass fraction for sparse or adaptive transient samples."""
    total_dt = 0.0
    pass_dt = 0.0
    for prev, cur in zip(rows, rows[1:]):
        dt = cur["time"] - prev["time"]
        if dt <= 0.0:
            continue
        if not region_predicate(prev):
            continue
        total_dt += dt
        if pass_predicate(prev):
            pass_dt += dt
    if total_dt <= 0.0:
        return 0.0
    return pass_dt / total_dt

def check_release_threshold_comparator(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vinp", "vinn", "out_p"}
    missing = require_signals(rows, required, "P_BIDIRECTIONAL_RESPONSE")
    if missing:
        return False, missing

    times = [r["time"] for r in rows]
    diff = [r["vinp"] - r["vinn"] for r in rows]
    out_vals = [r["out_p"] for r in rows]
    out_lo = min(out_vals)
    out_hi = max(out_vals)
    span = out_hi - out_lo
    if span < 0.60:
        return False, diagnostic(
            "P_RAIL_SMOOTHING",
            "behavior_mismatch",
            expected="output_span>=0.60",
            observed=f"output_span={span:.3f}",
            event="full_trace",
        )

    vth = out_lo + 0.5 * span
    margin = 20e-3
    high_rows = [r for r in rows if r["vinp"] - r["vinn"] >= margin]
    low_rows = [r for r in rows if r["vinn"] - r["vinp"] >= margin]
    if len(high_rows) < 5 or len(low_rows) < 5:
        return False, diagnostic(
            "P_BIDIRECTIONAL_RESPONSE",
            "insufficient_excitation",
            expected="positive_rows>=5,negative_rows>=5",
            observed=f"positive_rows={len(high_rows)},negative_rows={len(low_rows)}",
            event="differential_input_regions",
        )

    high_frac = _conditional_time_fraction(
        rows,
        lambda r: r["vinp"] - r["vinn"] >= margin,
        lambda r: r["out_p"] > vth,
    )
    low_frac = _conditional_time_fraction(
        rows,
        lambda r: r["vinn"] - r["vinp"] >= margin,
        lambda r: r["out_p"] < vth,
    )

    diff_rises = _threshold_crossings(diff, times, threshold=0.0, direction="rising")
    diff_falls = _threshold_crossings(diff, times, threshold=0.0, direction="falling")
    out_rises = _threshold_crossings(out_vals, times, threshold=vth, direction="rising")
    out_falls = _threshold_crossings(out_vals, times, threshold=vth, direction="falling")
    if not diff_rises or not diff_falls:
        return False, diagnostic(
            "P_BIDIRECTIONAL_RESPONSE",
            "insufficient_excitation",
            expected="rising_and_falling_input_crossings",
            observed=f"diff_rises={len(diff_rises)},diff_falls={len(diff_falls)}",
            event="vinp_minus_vinn.zero_crossing",
        )
    if not out_rises or not out_falls:
        return False, diagnostic(
            "P_BIDIRECTIONAL_RESPONSE",
            "behavior_mismatch",
            expected="rising_and_falling_output_transitions",
            observed=f"out_rises={len(out_rises)},out_falls={len(out_falls)}",
            event="out_p.midrail_crossing",
        )

    settle_s = 2.0e-9
    rising_aligned = any(abs(ot - dt) <= settle_s for dt in diff_rises for ot in out_rises)
    falling_aligned = any(abs(ot - dt) <= settle_s for dt in diff_falls for ot in out_falls)
    ok = high_frac > 0.90 and low_frac > 0.90 and rising_aligned and falling_aligned
    note = (
        f"high_frac={high_frac:.3f} low_frac={low_frac:.3f} span={span:.3f} "
        f"diff_rises={len(diff_rises)} diff_falls={len(diff_falls)} "
        f"out_rises={len(out_rises)} out_falls={len(out_falls)} "
        f"rising_aligned={rising_aligned} falling_aligned={falling_aligned}"
    )
    if high_frac <= 0.90 or low_frac <= 0.90:
        return False, diagnostic(
            "P_INITIAL_DECISION",
            "behavior_mismatch",
            expected="high_frac>0.90,low_frac>0.90",
            observed=f"high_frac={high_frac:.3f},low_frac={low_frac:.3f}",
            event="stable_differential_regions",
        )
    if not rising_aligned:
        return False, diagnostic(
            "P_RISING_DIFFERENTIAL",
            "behavior_mismatch",
            expected="output_rise_within_2ns_of_input_rise",
            observed=f"input_rises={len(diff_rises)},output_rises={len(out_rises)}",
            event="rising_zero_crossing",
        )
    if not falling_aligned:
        return False, diagnostic(
            "P_FALLING_DIFFERENTIAL",
            "behavior_mismatch",
            expected="output_fall_within_2ns_of_input_fall",
            observed=f"input_falls={len(diff_falls)},output_falls={len(out_falls)}",
            event="falling_zero_crossing",
        )
    return ok, pass_note(PROPERTY_IDS, note)

CHECKER_ID = "v4_045_threshold_comparator"
CHECKER: Checker = check_release_threshold_comparator
