#!/usr/bin/env python3
from __future__ import annotations

import csv
import re
from pathlib import Path


FORM_RE = re.compile(r"_(dut|tb|bugfix|e2e)$")


def load_csv(path: Path) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for raw in reader:
            row: dict[str, float] = {}
            for key, value in raw.items():
                if value in (None, ""):
                    continue
                try:
                    row[str(key)] = float(value)
                except ValueError:
                    pass
            if row:
                rows.append(row)
    rows.sort(key=lambda row: row.get("time", 0.0))
    return rows


def base_task_id(task_id: str) -> str:
    return FORM_RE.sub("", task_id)


def sample_signal(rows: list[dict[str, float]], signal: str, time_s: float) -> float | None:
    if not rows or signal not in rows[0] or "time" not in rows[0]:
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
    return rows[-1].get(signal)


def _crossing_times(
    rows: list[dict[str, float]],
    signal: str,
    *,
    threshold: float = 0.45,
    direction: str = "rising",
) -> list[float]:
    if not rows or "time" not in rows[0] or signal not in rows[0]:
        return []
    crossings: list[float] = []
    for idx in range(1, len(rows)):
        prev = rows[idx - 1]
        cur = rows[idx]
        t0 = prev.get("time")
        t1 = cur.get("time")
        v0 = prev.get(signal)
        v1 = cur.get(signal)
        if t0 is None or t1 is None or v0 is None or v1 is None:
            continue
        if direction == "rising":
            hit = v0 <= threshold < v1
        elif direction == "falling":
            hit = v0 >= threshold > v1
        else:
            raise ValueError(f"unsupported direction={direction!r}")
        if not hit:
            continue
        if v1 == v0:
            crossings.append(t1)
        else:
            alpha = (threshold - v0) / (v1 - v0)
            crossings.append(t0 + alpha * (t1 - t0))
    return crossings


def _active_indices(
    rows: list[dict[str, float]],
    signals: list[str],
    time_s: float,
    threshold: float,
) -> tuple[int, ...] | None:
    active: list[int] = []
    for idx, signal in enumerate(signals):
        value = sample_signal(rows, signal, time_s)
        if value is None:
            return None
        if value > threshold:
            active.append(idx)
    return tuple(active)


def _sequence_check(
    rows: list[dict[str, float]],
    signals: list[str],
    sample_times_ns: list[float],
    expected: list[tuple[int, ...]],
    *,
    label: str,
    threshold: float = 0.45,
) -> tuple[bool, str]:
    if not rows or "time" not in rows[0] or not set(signals).issubset(rows[0]):
        return False, f"missing time/{','.join(signals)}"
    observed: list[tuple[int, ...]] = []
    for t_ns in sample_times_ns:
        active = _active_indices(rows, signals, t_ns * 1e-9, threshold)
        if active is None:
            return False, f"missing_sample_at={t_ns:g}ns"
        observed.append(active)
    obs_text = ",".join("".join(str(idx) for idx in item) or "-" for item in observed)
    exp_text = ",".join("".join(str(idx) for idx in item) or "-" for item in expected)
    return observed == expected, f"{label}={obs_text} expected={exp_text}"


def check_barrel_pointer_window(rows: list[dict[str, float]]) -> tuple[bool, str]:
    return _sequence_check(
        rows,
        ["win0", "win1", "win2", "win3"],
        [20.0, 40.0, 60.0, 80.0, 100.0, 120.0],
        [(1, 2), (2, 3), (0, 3), (0, 1), (1, 2), (2, 3)],
        label="window_sequence",
    )


def check_background_calibration_accumulator(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows or "time" not in rows[0] or "accum" not in rows[0]:
        return False, "missing time/accum"
    sample_times_ns = [20.0, 40.0, 80.0, 100.0, 140.0, 180.0, 210.0]
    expected = [0.45, 0.49, 0.57, 0.61, 0.53, 0.53, 0.57]
    observed: list[float] = []
    for t_ns in sample_times_ns:
        value = sample_signal(rows, "accum", t_ns * 1e-9)
        if value is None:
            return False, f"missing_sample_at={t_ns:g}ns"
        observed.append(value)

    min_accum = min(row.get("accum", 0.0) for row in rows)
    max_accum = max(row.get("accum", 0.0) for row in rows)
    in_range = min_accum >= 0.04 and max_accum <= 0.86
    level_ok = all(abs(got - want) <= 0.025 for got, want in zip(observed, expected))
    direction_ok = (
        abs(observed[0] - 0.45) <= 0.03
        and observed[1] < observed[2] < observed[3]
        and observed[3] > observed[4]
        and abs(observed[4] - observed[5]) <= 0.03
        and observed[6] > observed[5] + 0.02
    )
    ok = level_ok and direction_ok and in_range
    obs_text = ",".join(f"{value:.3f}" for value in observed)
    exp_text = ",".join(f"{value:.3f}" for value in expected)
    return ok, f"accum_samples={obs_text} expected={exp_text} direction_ok={direction_ok} in_range={in_range}"


def check_cdac_calibration(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows or "time" not in rows[0] or "trim" not in rows[0]:
        return False, "missing time/trim"
    sample_times_ns = [40.0, 80.0, 100.0, 140.0, 180.0, 210.0]
    samples: list[float] = []
    for t_ns in sample_times_ns:
        value = sample_signal(rows, "trim", t_ns * 1e-9)
        if value is None:
            return False, f"missing_sample_at={t_ns:g}ns"
        samples.append(value)

    min_trim = min(row.get("trim", 0.0) for row in rows)
    max_trim = max(row.get("trim", 0.0) for row in rows)
    in_range = min_trim >= 0.04 and max_trim <= 0.86
    early_increases = samples[0] < samples[1] < samples[2]
    mid_decreases = samples[2] > samples[3] >= samples[4] - 0.02
    late_recovers = samples[5] > samples[4] + 0.02
    reset_sample = sample_signal(rows, "trim", 20e-9)
    reset_nominal = reset_sample is not None and abs(reset_sample - 0.45) <= 0.03
    ok = in_range and reset_nominal and early_increases and mid_decreases and late_recovers
    values = ",".join(f"{value:.3f}" for value in samples)
    return ok, (
        f"trim_samples={values} in_range={in_range} reset_nominal={reset_nominal} "
        f"early_increases={early_increases} mid_decreases={mid_decreases} "
        f"late_recovers={late_recovers}"
    )


def check_element_shuffler(rows: list[dict[str, float]]) -> tuple[bool, str]:
    return _sequence_check(
        rows,
        ["out0", "out1", "out2", "out3"],
        [20.0, 40.0, 60.0, 80.0, 100.0, 120.0],
        [(1,), (2,), (3,), (0,), (1,), (2,)],
        label="active_sequence",
    )


def check_edge_detector(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "rst_n", "pulse"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/rst_n/pulse"

    high_times_ns = [33.0, 78.0, 123.0, 168.0]
    low_times_ns = [20.0, 40.0, 85.0, 130.0, 175.0]
    high_ok = []
    low_ok = []
    for t_ns in high_times_ns:
        value = sample_signal(rows, "pulse", t_ns * 1e-9)
        if value is None:
            return False, f"missing_sample_at={t_ns:g}ns"
        high_ok.append(value > 0.45)
    for t_ns in low_times_ns:
        value = sample_signal(rows, "pulse", t_ns * 1e-9)
        if value is None:
            return False, f"missing_sample_at={t_ns:g}ns"
        low_ok.append(value < 0.45)

    ok = all(high_ok) and all(low_ok)
    return ok, (
        "rising_edge_pulse_samples="
        f"{''.join('H' if item else 'L' for item in high_ok)} "
        "low_window_samples="
        f"{''.join('L' if item else 'H' for item in low_ok)}"
    )


def check_debounce_latch(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows or "time" not in rows[0] or "out" not in rows[0]:
        return False, "missing time/out"
    early_times_ns = [34.0, 40.0, 72.0, 82.0]
    late_times_ns = [100.0, 130.0]
    early_low: list[bool] = []
    late_high: list[bool] = []
    for t_ns in early_times_ns:
        value = sample_signal(rows, "out", t_ns * 1e-9)
        if value is None:
            return False, f"missing_sample_at={t_ns:g}ns"
        early_low.append(value < 0.45)
    for t_ns in late_times_ns:
        value = sample_signal(rows, "out", t_ns * 1e-9)
        if value is None:
            return False, f"missing_sample_at={t_ns:g}ns"
        late_high.append(value > 0.45)
    ok = all(early_low) and all(late_high)
    early_text = "".join("L" if item else "H" for item in early_low)
    late_text = "".join("H" if item else "L" for item in late_high)
    return ok, f"debounce_early_low={early_text} late_high={late_text}"


def check_leaky_hold(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vout"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/vout"

    sample_times_ns = [25.0, 40.0, 80.0, 110.0, 120.0, 140.0]
    samples: list[float] = []
    for t_ns in sample_times_ns:
        value = sample_signal(rows, "vout", t_ns * 1e-9)
        if value is None:
            return False, f"missing_sample_at={t_ns:g}ns"
        samples.append(value)

    high, early_decay, mid_decay, late_decay, reset_early, reset_late = samples
    sample_captured = high > 0.60
    decay_direction = early_decay > mid_decay > late_decay
    decay_amount = early_decay - late_decay > 0.20
    reset_clear = reset_early < 0.05 and reset_late < 0.05
    ok = sample_captured and decay_direction and decay_amount and reset_clear
    values = ",".join(f"{value:.3f}" for value in samples)
    return ok, (
        f"leaky_hold_samples={values} sample_captured={sample_captured} "
        f"decay_direction={decay_direction} decay_amount={decay_amount} "
        f"reset_clear={reset_clear}"
    )


def check_one_shot_timer(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "rst_n", "pulse"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/rst_n/pulse"

    high_times_ns = [42.0, 87.0, 132.0, 177.0, 222.0]
    low_times_ns = [50.0, 94.5, 139.5, 184.5, 229.5]
    high_ok: list[bool] = []
    low_ok: list[bool] = []
    for t_ns in high_times_ns:
        value = sample_signal(rows, "pulse", t_ns * 1e-9)
        if value is None:
            return False, f"missing_sample_at={t_ns:g}ns"
        high_ok.append(value > 0.45)
    for t_ns in low_times_ns:
        value = sample_signal(rows, "pulse", t_ns * 1e-9)
        if value is None:
            return False, f"missing_sample_at={t_ns:g}ns"
        low_ok.append(value < 0.45)

    reset_clear = True
    reset_sample = sample_signal(rows, "rst_n", 46.5e-9)
    if reset_sample is not None and reset_sample < 0.45:
        pulse_during_reset = sample_signal(rows, "pulse", 46.5e-9)
        if pulse_during_reset is None:
            return False, "missing_sample_at=46.5ns"
        reset_clear = pulse_during_reset < 0.45

    ok = all(high_ok) and all(low_ok) and reset_clear
    return ok, (
        "pulse_high_windows="
        f"{''.join('H' if item else 'L' for item in high_ok)} "
        "pulse_low_windows="
        f"{''.join('L' if item else 'H' for item in low_ok)} "
        f"reset_clear={reset_clear}"
    )


def check_rotating_element_selector(rows: list[dict[str, float]]) -> tuple[bool, str]:
    return _sequence_check(
        rows,
        ["sel0", "sel1", "sel2", "sel3"],
        [20.0, 40.0, 60.0, 80.0, 100.0, 120.0],
        [(1,), (2,), (3,), (0,), (1,), (2,)],
        label="active_sequence",
    )


def check_segmented_dac(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows or "time" not in rows[0] or "aout" not in rows[0]:
        return False, "missing time/aout"
    sample_times_ns = [15.0, 45.0, 75.0, 105.0, 135.0]
    expected = [0.0, 0.06, 0.12, 0.42, 0.72]
    observed: list[float] = []
    for t_ns in sample_times_ns:
        value = sample_signal(rows, "aout", t_ns * 1e-9)
        if value is None:
            return False, f"missing_sample_at={t_ns:g}ns"
        observed.append(value)
    level_ok = all(abs(got - want) <= 0.02 for got, want in zip(observed, expected))
    monotonic = all(b >= a - 1e-3 for a, b in zip(observed, observed[1:]))
    ok = level_ok and monotonic
    obs_text = ",".join(f"{value:.3f}" for value in observed)
    exp_text = ",".join(f"{value:.3f}" for value in expected)
    return ok, f"dac_levels={obs_text} expected={exp_text} monotonic={monotonic}"


def check_thermometer_dac(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows or "time" not in rows[0] or "aout" not in rows[0]:
        return False, "missing time/aout"
    sample_times_ns = [10.0, 30.0, 50.0, 70.0, 90.0, 110.0, 130.0, 150.0]
    expected = [0.0, 0.12, 0.24, 0.36, 0.48, 0.60, 0.72, 0.90]
    observed: list[float] = []
    for t_ns in sample_times_ns:
        value = sample_signal(rows, "aout", t_ns * 1e-9)
        if value is None:
            return False, f"missing_sample_at={t_ns:g}ns"
        observed.append(value)
    max_err = max(abs(got - want) for got, want in zip(observed, expected))
    monotonic = all(b >= a - 1e-3 for a, b in zip(observed, observed[1:]))
    full_scale_ok = abs(observed[-1] - 0.90) <= 0.02
    ok = max_err <= 0.02 and monotonic and full_scale_ok
    obs_text = ",".join(f"{value:.3f}" for value in observed)
    exp_text = ",".join(f"{value:.3f}" for value in expected)
    return ok, (
        f"dac_levels={obs_text} expected={exp_text} max_err={max_err:.3f} "
        f"monotonic={monotonic} full_scale_ok={full_scale_ok}"
    )


def check_thermometer_decoder_guarded(rows: list[dict[str, float]]) -> tuple[bool, str]:
    return _sequence_check(
        rows,
        ["th0", "th1", "th2", "th3"],
        [10.0, 30.0, 50.0, 70.0, 90.0, 110.0],
        [(), (), (0,), (0, 1), (0, 1, 2), (0, 1, 2)],
        label="thermometer_sequence",
    )


def check_strongarm_comparator_behavior(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "out_p", "out_n"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/out_p/out_n"
    samples = []
    for t_ns in [0.75, 1.75, 2.75, 3.75]:
        out_p = sample_signal(rows, "out_p", t_ns * 1e-9)
        out_n = sample_signal(rows, "out_n", t_ns * 1e-9)
        if out_p is None or out_n is None:
            return False, f"missing_sample_at={t_ns:g}ns"
        if out_p > 0.45 and out_n < 0.45:
            samples.append("P")
        elif out_p < 0.45 and out_n > 0.45:
            samples.append("N")
        else:
            samples.append("X")
    note = f"decision_samples={''.join(samples)} expected=PPNN"
    return samples == ["P", "P", "N", "N"], note


def check_track_hold_aperture(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "vin", "vout"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/clk/vin/vout"

    edge_times = _crossing_times(rows, "clk", direction="rising")
    if len(edge_times) < 5:
        return False, f"too_few_clk_edges={len(edge_times)}"

    observations: list[float] = []
    expected: list[float] = []
    mismatches = 0
    for edge_time in edge_times[:7]:
        want = sample_signal(rows, "vin", edge_time + 0.20e-9)
        got = sample_signal(rows, "vout", edge_time + 1.00e-9)
        if want is None or got is None:
            continue
        expected.append(want)
        observations.append(got)
        if abs(got - want) > 0.035:
            mismatches += 1

    if len(observations) < 5:
        return False, f"insufficient_aperture_samples={len(observations)}"
    span = max(observations) - min(observations)
    ok = mismatches == 0 and span > 0.40
    obs_text = ",".join(f"{value:.3f}" for value in observations)
    exp_text = ",".join(f"{value:.3f}" for value in expected)
    return ok, f"aperture_samples={obs_text} expected={exp_text} mismatches={mismatches} span={span:.3f}"


def check_voltage_clamp(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "raw_level", "clamped_level"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/raw_level/clamped_level"

    sample_times_ns = [10.0, 35.0, 60.0, 85.0, 110.0]
    observed: list[float] = []
    expected: list[float] = []
    raw_values: list[float] = []
    for t_ns in sample_times_ns:
        raw = sample_signal(rows, "raw_level", t_ns * 1e-9)
        got = sample_signal(rows, "clamped_level", t_ns * 1e-9)
        if raw is None or got is None:
            return False, f"missing_sample_at={t_ns:g}ns"
        raw_values.append(raw)
        observed.append(got)
        expected.append(min(max(raw, 0.18), 0.72))

    max_err = max(abs(got - want) for got, want in zip(observed, expected))
    lower_clamped = observed[0] > raw_values[0] + 0.08 and abs(observed[0] - 0.18) <= 0.035
    upper_clamped = observed[3] < raw_values[3] - 0.08 and abs(observed[3] - 0.72) <= 0.035
    mid_follows = abs(observed[1] - raw_values[1]) <= 0.035 and abs(observed[2] - raw_values[2]) <= 0.035
    ok = max_err <= 0.04 and lower_clamped and upper_clamped and mid_follows
    obs_text = ",".join(f"{value:.3f}" for value in observed)
    exp_text = ",".join(f"{value:.3f}" for value in expected)
    return ok, (
        f"clamp_samples={obs_text} expected={exp_text} max_err={max_err:.3f} "
        f"lower_clamped={lower_clamped} upper_clamped={upper_clamped} mid_follows={mid_follows}"
    )


def check_precision_rectifier(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin", "vout"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/vin/vout"

    sample_times_ns = [20.0, 55.0, 95.0, 115.0]
    observed: list[float] = []
    expected: list[float] = []
    for t_ns in sample_times_ns:
        vin = sample_signal(rows, "vin", t_ns * 1e-9)
        vout = sample_signal(rows, "vout", t_ns * 1e-9)
        if vin is None or vout is None:
            return False, f"missing_sample_at={t_ns:g}ns"
        observed.append(vout)
        expected.append(vin if vin > 0.0 else 0.0)

    max_err = max(abs(got - want) for got, want in zip(observed, expected))
    negative_zero = observed[0] < 0.04 and observed[2] < 0.04 and observed[3] < 0.04
    positive_follows = abs(observed[1] - expected[1]) <= 0.04 and observed[1] > 0.25
    ok = max_err <= 0.04 and negative_zero and positive_follows
    obs_text = ",".join(f"{value:.3f}" for value in observed)
    exp_text = ",".join(f"{value:.3f}" for value in expected)
    return ok, (
        f"rectifier_samples={obs_text} expected={exp_text} max_err={max_err:.3f} "
        f"negative_zero={negative_zero} positive_follows={positive_follows}"
    )


def check_peak_detector(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vout"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/vout"

    sample_times_ns = [80.0, 128.0, 165.0]
    samples: list[float] = []
    for t_ns in sample_times_ns:
        value = sample_signal(rows, "vout", t_ns * 1e-9)
        if value is None:
            return False, f"missing_sample_at={t_ns:g}ns"
        samples.append(value)

    first_peak = abs(samples[0] - 0.55) <= 0.04
    reset_clear = samples[1] < 0.05
    second_peak = abs(samples[2] - 0.70) <= 0.04
    ok = first_peak and reset_clear and second_peak
    values = ",".join(f"{value:.3f}" for value in samples)
    return ok, f"peak_samples={values} first_peak={first_peak} reset_clear={reset_clear} second_peak={second_peak}"


def check_slew_rate_limiter(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vout"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/vout"

    sample_times_ns = [40.0, 80.0, 100.0, 120.0, 150.0]
    samples: list[float] = []
    for t_ns in sample_times_ns:
        value = sample_signal(rows, "vout", t_ns * 1e-9)
        if value is None:
            return False, f"missing_sample_at={t_ns:g}ns"
        samples.append(value)

    rising_limited = 0.20 <= samples[0] <= 0.40
    high_reached = samples[1] > 0.74
    falling_limited = samples[2] > samples[3] > samples[4] and samples[2] > 0.65 and 0.34 <= samples[3] <= 0.58
    low_reached = abs(samples[4] - 0.10) <= 0.05
    ok = rising_limited and high_reached and falling_limited and low_reached
    values = ",".join(f"{value:.3f}" for value in samples)
    return ok, (
        f"slew_samples={values} rising_limited={rising_limited} "
        f"high_reached={high_reached} falling_limited={falling_limited} low_reached={low_reached}"
    )


def check_first_order_lowpass(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vout"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/vout"

    sample_times_ns = [30.0, 50.0, 90.0, 150.0]
    samples: list[float] = []
    for t_ns in sample_times_ns:
        value = sample_signal(rows, "vout", t_ns * 1e-9)
        if value is None:
            return False, f"missing_sample_at={t_ns:g}ns"
        samples.append(value)

    monotonic = samples[0] < samples[1] < samples[2] <= samples[3] + 0.03
    response_fast_enough = samples[1] > 0.55 and samples[2] > 0.70 and samples[3] > 0.76
    not_instant = samples[0] < 0.45
    ok = monotonic and response_fast_enough and not_instant
    values = ",".join(f"{value:.3f}" for value in samples)
    return ok, (
        f"lowpass_samples={values} monotonic={monotonic} "
        f"response_fast_enough={response_fast_enough} not_instant={not_instant}"
    )


def check_resettable_integrator(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vout"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/vout"

    sample_times_ns = [200.0, 230.0, 245.0, 300.0]
    samples: list[float] = []
    for t_ns in sample_times_ns:
        value = sample_signal(rows, "vout", t_ns * 1e-9)
        if value is None:
            return False, f"missing_sample_at={t_ns:g}ns"
        samples.append(value)

    pre_reset_integrated = samples[0] > 0.30
    reset_clear = samples[1] < 0.05 and samples[2] < 0.05
    post_reset_restarts = 0.06 <= samples[3] <= 0.18
    ok = pre_reset_integrated and reset_clear and post_reset_restarts
    values = ",".join(f"{value:.3f}" for value in samples)
    return ok, (
        f"integrator_samples={values} pre_reset_integrated={pre_reset_integrated} "
        f"reset_clear={reset_clear} post_reset_restarts={post_reset_restarts}"
    )


def check_gain_trim_controller(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "gain_ctrl"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/gain_ctrl"

    sample_times_ns = [20.0, 70.0, 100.0, 150.0, 178.0]
    samples: list[float] = []
    for t_ns in sample_times_ns:
        value = sample_signal(rows, "gain_ctrl", t_ns * 1e-9)
        if value is None:
            return False, f"missing_sample_at={t_ns:g}ns"
        samples.append(value)

    reset_nominal = abs(samples[0] - 0.30) <= 0.04
    low_meas_increases = samples[0] < samples[1] < samples[2]
    high_meas_decreases = samples[2] > samples[3] > samples[4] - 0.02
    in_range = all(0.04 <= value <= 0.86 for value in samples)
    ok = reset_nominal and low_meas_increases and high_meas_decreases and in_range
    values = ",".join(f"{value:.3f}" for value in samples)
    return ok, (
        f"gain_trim_samples={values} reset_nominal={reset_nominal} "
        f"low_meas_increases={low_meas_increases} high_meas_decreases={high_meas_decreases} "
        f"in_range={in_range}"
    )


def check_offset_comparator(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "out_p"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/out_p"

    sample_times_ns = [2.0, 6.0, 10.0, 14.0, 18.0, 22.0, 26.0]
    observed: list[str] = []
    for t_ns in sample_times_ns:
        value = sample_signal(rows, "out_p", t_ns * 1e-9)
        if value is None:
            return False, f"missing_sample_at={t_ns:g}ns"
        observed.append("H" if value > 0.45 else "L")

    sequence = "".join(observed)
    ok = sequence == "LHHHLLL"
    return ok, f"offset_decisions={sequence} expected=LHHHLLL"


def check_lock_detector(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "lock"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/lock"

    sample_times_ns = [45.0, 85.0, 125.0, 165.0]
    observed: list[str] = []
    for t_ns in sample_times_ns:
        value = sample_signal(rows, "lock", t_ns * 1e-9)
        if value is None:
            return False, f"missing_sample_at={t_ns:g}ns"
        observed.append("H" if value > 0.45 else "L")

    sequence = "".join(observed)
    ok = sequence == "LLHH"
    return ok, f"lock_sequence={sequence} expected=LLHH"


def check_offset_calibration_fsm(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows or "time" not in rows[0] or "trim" not in rows[0]:
        return False, "missing time/trim"

    sample_times_ns = [35.0, 75.0, 145.0, 215.0]
    samples: list[float] = []
    for t_ns in sample_times_ns:
        value = sample_signal(rows, "trim", t_ns * 1e-9)
        if value is None:
            return False, f"missing_sample_at={t_ns:g}ns"
        samples.append(value)

    early_increases = samples[0] < samples[1]
    middle_decreases = samples[2] < samples[1]
    late_recovers = samples[3] > samples[2]
    in_range = all(0.04 <= value <= 0.86 for value in samples)
    ok = early_increases and middle_decreases and late_recovers and in_range
    values = ",".join(f"{value:.3f}" for value in samples)
    return ok, (
        f"offset_trim_samples={values} early_increases={early_increases} "
        f"middle_decreases={middle_decreases} late_recovers={late_recovers} in_range={in_range}"
    )


def check_sar_logic_4b(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "rdy", "dp_dac_3", "dp_dac_2", "dp_dac_1", "dp_dac_0"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/rdy/dp_dac_[3:0]"

    rdy_samples: list[str] = []
    for t_ns in [126.0, 176.0, 226.0]:
        value = sample_signal(rows, "rdy", t_ns * 1e-9)
        if value is None:
            return False, f"missing_sample_at={t_ns:g}ns"
        rdy_samples.append("H" if value > 0.45 else "L")

    code_bits: list[str] = []
    for signal in ["dp_dac_3", "dp_dac_2", "dp_dac_1", "dp_dac_0"]:
        value = sample_signal(rows, signal, 176e-9)
        if value is None:
            return False, "missing_code_sample_at=176ns"
        code_bits.append("1" if value > 0.45 else "0")

    rdy_sequence = "".join(rdy_samples)
    code = "".join(code_bits)
    ok = rdy_sequence == "LHL" and code == "1010"
    return ok, f"sar_rdy_sequence={rdy_sequence} expected=LHL code176={code} expected_code=1010"


MAIN120_STABLE_CHECKS = {
    "vbm1_background_calibration_accumulator": check_background_calibration_accumulator,
    "vbm1_barrel_pointer_window": check_barrel_pointer_window,
    "vbm1_cdac_calibration": check_cdac_calibration,
    "vbm1_debounce_latch": check_debounce_latch,
    "vbm1_edge_detector": check_edge_detector,
    "vbm1_element_shuffler": check_element_shuffler,
    "vbm1_leaky_hold": check_leaky_hold,
    "vbm1_one_shot_timer": check_one_shot_timer,
    "vbm1_rotating_element_selector": check_rotating_element_selector,
    "vbm1_segmented_dac": check_segmented_dac,
    "vbm1_strongarm_comparator_behavior": check_strongarm_comparator_behavior,
    "vbm1_thermometer_dac": check_thermometer_dac,
    "vbm1_thermometer_decoder_guarded": check_thermometer_decoder_guarded,
    "vbm1_track_hold_aperture": check_track_hold_aperture,
    "vbm1_first_order_lowpass": check_first_order_lowpass,
    "vbm1_gain_trim_controller": check_gain_trim_controller,
    "vbm1_lock_detector": check_lock_detector,
    "vbm1_offset_calibration_fsm": check_offset_calibration_fsm,
    "vbm1_offset_comparator": check_offset_comparator,
    "vbm1_peak_detector": check_peak_detector,
    "vbm1_precision_rectifier": check_precision_rectifier,
    "vbm1_resettable_integrator": check_resettable_integrator,
    "vbm1_sar_logic_4b": check_sar_logic_4b,
    "vbm1_slew_rate_limiter": check_slew_rate_limiter,
    "vbm1_voltage_clamp": check_voltage_clamp,
}


def evaluate_main120_stable_check(task_id: str, csv_path: Path) -> tuple[bool, str] | None:
    if task_id == "vbm1_strongarm_comparator_behavior_bugfix":
        return None
    checker = MAIN120_STABLE_CHECKS.get(base_task_id(task_id))
    if checker is None:
        return None
    return checker(load_csv(csv_path))
