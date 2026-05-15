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
}


def evaluate_main120_stable_check(task_id: str, csv_path: Path) -> tuple[bool, str] | None:
    if task_id == "vbm1_strongarm_comparator_behavior_bugfix":
        return None
    checker = MAIN120_STABLE_CHECKS.get(base_task_id(task_id))
    if checker is None:
        return None
    return checker(load_csv(csv_path))
