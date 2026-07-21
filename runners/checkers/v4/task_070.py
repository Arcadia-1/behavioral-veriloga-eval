"""Task-specific checker for canonical v4 DUT 070."""
from __future__ import annotations

from bisect import bisect_right

from ..api import Checker
from .stimulus_relative import diagnostic, pass_note, require_signals


PROPERTIES = (
    "P_NOMINAL_CLOCK",
    "P_SEED_DECODE",
    "P_EDGE_MODULATION",
    "P_REPEATABILITY",
    "P_TIMING_BOUNDS",
    "P_OUTPUT_LEVELS",
)

BASE_SIGNALS = ("jitter_en", "clk_out", *tuple(f"seed{i}" for i in range(8)))


def _signal(base: str, label: str) -> str:
    return base if not label else f"{base}_{label}"


def _ref(rows: list[dict[str, float]], base: str, label: str) -> float | None:
    name = _signal(base, label)
    if name not in rows[0]:
        return None
    values = [float(row[name]) for row in rows if name in row]
    return sum(values) / len(values) if values else None


def _groups(rows: list[dict[str, float]]) -> list[str]:
    if not rows:
        return []
    columns = set(rows[0])
    groups: list[str] = []
    if {"time", *BASE_SIGNALS}.issubset(columns):
        groups.append("")
    for column in sorted(columns):
        if not column.startswith("clk_out_"):
            continue
        label = column[len("clk_out_") :]
        if all(_signal(base, label) in columns for base in BASE_SIGNALS):
            groups.append(label)
    return groups


def _transition_span_ps(
    rows: list[dict[str, float]],
    clk: str,
    low: float,
    high: float,
) -> float | None:
    span = high - low
    if span <= 0.0:
        return None
    lo_th = low + 0.2 * span
    hi_th = low + 0.8 * span
    spans: list[float] = []
    start: float | None = None
    for left, right in zip(rows, rows[1:]):
        lv = float(left[clk])
        rv = float(right[clk])
        if lv <= lo_th < rv:
            frac = (lo_th - lv) / (rv - lv)
            start = float(left["time"]) + frac * (float(right["time"]) - float(left["time"]))
        elif lv >= hi_th > rv:
            frac = (lv - hi_th) / (lv - rv)
            start = float(left["time"]) + frac * (float(right["time"]) - float(left["time"]))

        if start is None:
            continue
        if lv <= hi_th < rv:
            frac = (hi_th - lv) / (rv - lv)
            stop = float(left["time"]) + frac * (float(right["time"]) - float(left["time"]))
            spans.append(abs(stop - start) * 1.0e12)
            start = None
        elif lv >= lo_th > rv:
            frac = (lv - lo_th) / (lv - rv)
            stop = float(left["time"]) + frac * (float(right["time"]) - float(left["time"]))
            spans.append(abs(stop - start) * 1.0e12)
            start = None
    if not spans:
        return None
    spans.sort()
    return spans[len(spans) // 2]


def _sample_at(
    rows: list[dict[str, float]],
    times: list[float],
    signal: str,
    time_s: float,
) -> float | None:
    index = bisect_right(times, time_s)
    if index <= 0:
        return None
    return rows[index - 1].get(signal)


def _check_group(rows: list[dict[str, float]], label: str) -> tuple[bool, str]:
    required = {"time", *{_signal(base, label) for base in BASE_SIGNALS}}
    invalid = require_signals(rows, required, "P_NOMINAL_CLOCK")
    if invalid:
        return False, invalid
    clk = _signal("clk_out", label)
    jitter_en = _signal("jitter_en", label)
    seeds = [_signal(f"seed{bit}", label) for bit in range(8)]
    out_min = min(row[clk] for row in rows)
    out_max = max(row[clk] for row in rows)
    swing = out_max - out_min
    if swing < 0.10:
        return False, diagnostic(
            "P_OUTPUT_LEVELS",
            "semantic_mismatch",
            expected="clk_out_swing>=0.10",
            observed=f"clk_out_range={out_min:.3f}..{out_max:.3f}",
            event=label or "full_trace",
        )

    vdd_ref = _ref(rows, "vdd_ref", label)
    vth_ref = _ref(rows, "vth_ref", label)
    tr_ps_ref = _ref(rows, "tr_ps_ref", label)
    edge_threshold = out_min + 0.5 * swing
    transitions: list[float] = []
    last_high = rows[0][clk] > edge_threshold
    for row in rows[1:]:
        high = row[clk] > edge_threshold
        if high != last_high:
            transitions.append(row["time"])
        last_high = high
    if len(transitions) < 16:
        return False, diagnostic(
            "P_NOMINAL_CLOCK",
            "insufficient_coverage",
            expected="transitions>=16",
            observed=f"transitions={len(transitions)}",
            event=label or "full_trace",
        )
    if len(transitions) < 20:
        return False, diagnostic(
            "P_EDGE_MODULATION",
            "insufficient_coverage",
            expected="transitions>=20",
            observed=f"transitions={len(transitions)}",
            event=label or "full_trace",
        )
    expected_high = vdd_ref if vdd_ref is not None else 0.9
    high_tol = max(0.06, 0.08 * expected_high)
    if abs(out_min) > 0.08 or abs(out_max - expected_high) > high_tol:
        return False, diagnostic(
            "P_OUTPUT_LEVELS",
            "semantic_mismatch",
            expected=f"low=0.0,high={expected_high:.3f}",
            observed=f"low={out_min:.3f},high={out_max:.3f}",
            event=label or "full_trace",
        )
    if tr_ps_ref is not None and tr_ps_ref >= 45.0:
        observed_tr = _transition_span_ps(rows, clk, out_min, out_max)
        if observed_tr is None or observed_tr < max(25.0, 0.45 * tr_ps_ref):
            return False, diagnostic(
                "P_OUTPUT_LEVELS",
                "semantic_mismatch",
                expected=f"transition_span_ps>={max(25.0, 0.45 * tr_ps_ref):.3f}",
                observed=f"transition_span_ps={observed_tr if observed_tr is not None else 'missing'}",
                event=label or "transition_smoothing",
            )

    half_periods = [(b - a) / 1e-9 for a, b in zip(transitions, transitions[1:])]
    enabled_periods: list[tuple[int, float]] = []
    disabled_periods: list[tuple[int, float]] = []
    formula_failures: list[str] = []
    logic_threshold = vth_ref if vth_ref is not None else 0.45
    times = [float(row["time"]) for row in rows]
    for index, (edge_t, half_period_ns) in enumerate(zip(transitions, half_periods), start=1):
        enabled = _sample_at(rows, times, jitter_en, edge_t)
        if enabled is None:
            continue
        if enabled <= logic_threshold:
            disabled_periods.append((index, half_period_ns))
            continue
        enabled_periods.append((index, half_period_ns))
        seed = 0
        for bit, seed_signal in enumerate(seeds):
            value = _sample_at(rows, times, seed_signal, edge_t)
            if value is not None and value > logic_threshold:
                seed |= 1 << bit
        expected_ns = 10.0 + (((seed + 3 * index) % 5) - 2) * 0.8
        if abs(half_period_ns - expected_ns) > 0.18:
            formula_failures.append(
                diagnostic(
                    "P_EDGE_MODULATION",
                    "semantic_mismatch",
                    expected=f"half_period_ns={expected_ns:.3f}",
                    observed=f"half_period_ns={half_period_ns:.3f},seed={seed}",
                    event=f"{label or 'legacy'}:edge{index}",
                )
            )

    bounds_failures = [
        (index, period) for index, period in enabled_periods if period < 8.22 or period > 11.78
    ]
    if bounds_failures:
        index, period = bounds_failures[0]
        return False, diagnostic(
            "P_TIMING_BOUNDS",
            "semantic_mismatch",
            expected="half_period_ns=8.4..11.6",
            observed=f"half_period_ns={period:.3f},mismatch_count={len(bounds_failures)}",
            event=f"{label or 'legacy'}:edge{index}",
        )
    if len(enabled_periods) < 5:
        return False, diagnostic(
            "P_EDGE_MODULATION",
            "insufficient_coverage",
            expected="jitter_en_high_half_periods>=5",
            observed=f"enabled_half_periods={len(enabled_periods)}",
            event=f"{label or 'legacy'}:jitter_en_high",
        )
    if len(disabled_periods) < 3:
        return False, diagnostic(
            "P_NOMINAL_CLOCK",
            "insufficient_coverage",
            expected="jitter_en_low_half_periods>=3",
            observed=f"disabled_half_periods={len(disabled_periods)}",
            event=f"{label or 'legacy'}:jitter_en_low",
        )
    nominal_failures = [
        (index, period) for index, period in disabled_periods if abs(period - 10.0) > 0.18
    ]
    if nominal_failures:
        index, period = nominal_failures[0]
        return False, diagnostic(
            "P_NOMINAL_CLOCK",
            "semantic_mismatch",
            expected="half_period_ns=10.000",
            observed=f"half_period_ns={period:.3f},mismatch_count={len(nominal_failures)}",
            event=f"{label or 'legacy'}:edge{index}",
        )
    unique_enabled = {round(period, 1) for _, period in enabled_periods}
    if len(enabled_periods) >= 5 and len(unique_enabled) < 3:
        return False, diagnostic(
            "P_EDGE_MODULATION",
            "semantic_mismatch",
            expected="unique_enabled_half_periods>=3",
            observed=f"unique_enabled_half_periods={sorted(unique_enabled)}",
            event=f"{label or 'legacy'}:jitter_en_high",
        )

    repeat_failures: list[tuple[int, float, float]] = []
    enabled_by_index = {index: period for index, period in enabled_periods}
    for index, period in enabled_periods:
        repeated = enabled_by_index.get(index + 5)
        if repeated is not None and abs(repeated - period) > 0.18:
            repeat_failures.append((index, period, repeated))
    if repeat_failures:
        index, first, repeated = repeat_failures[0]
        return False, diagnostic(
            "P_REPEATABILITY",
            "semantic_mismatch",
            expected="edge_i_equals_edge_i_plus_5",
            observed=f"edge{index}={first:.3f}ns,edge{index + 5}={repeated:.3f}ns,mismatch_count={len(repeat_failures)}",
            event=f"{label or 'legacy'}:constant_seed",
        )
    if formula_failures:
        return False, " ".join(formula_failures[:5])
    return True, pass_note(PROPERTIES, (
        f"jitter_clock_contract_pass instance={label or 'legacy'} transitions={len(transitions)} "
        f"enabled_intervals={len(enabled_periods)} disabled_intervals={len(disabled_periods)} "
        f"output_range={out_min:.3f}..{out_max:.3f}"
    ))


def check_deterministic_jittered_clock(rows: list[dict[str, float]]) -> tuple[bool, str]:
    groups = _groups(rows)
    if not groups:
        return False, "missing time/jitter_en/seed*/clk_out grouped trace"
    notes: list[str] = []
    for label in groups:
        passed, detail = _check_group(rows, label)
        if not passed:
            return False, detail
        notes.append(detail)
    if len(groups) < 2 and any(name.startswith("vdd_ref_") for name in rows[0]):
        return False, diagnostic(
            "P_OUTPUT_LEVELS",
            "insufficient_coverage",
            expected="default_and_override_instances",
            observed=f"instances={groups}",
            event="parameter_override_coverage",
        )
    return True, " ".join(notes)

CHECKER_ID = "v4_070_jittered_clock_source_deterministic"
CHECKER: Checker = check_deterministic_jittered_clock
