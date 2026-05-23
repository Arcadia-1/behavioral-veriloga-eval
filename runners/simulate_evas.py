#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import math
import multiprocessing as mp
import os
import re
import shutil
import subprocess
import tempfile
import warnings
from pathlib import Path

from main120_stable_checks import (
    check_background_calibration_accumulator as check_vbm1_background_calibration_accumulator,
    check_barrel_pointer_window as check_vbm1_barrel_pointer_window,
    check_cdac_calibration as check_vbm1_cdac_calibration,
    check_debounce_latch as check_vbm1_debounce_latch,
    check_edge_detector as check_vbm1_edge_detector,
    check_element_shuffler as check_vbm1_element_shuffler,
    check_file_metric_writer as check_vbm1_file_metric_writer,
    check_first_order_lowpass as check_vbm1_first_order_lowpass,
    check_gain_trim_controller as check_vbm1_gain_trim_controller,
    check_leaky_hold as check_vbm1_leaky_hold,
    check_lock_detector as check_vbm1_lock_detector,
    check_one_shot_timer as check_vbm1_one_shot_timer,
    check_offset_calibration_fsm as check_vbm1_offset_calibration_fsm,
    check_offset_comparator as check_vbm1_offset_comparator,
    check_peak_detector as check_vbm1_peak_detector,
    check_precision_rectifier as check_vbm1_precision_rectifier,
    check_resettable_counter_divider as check_vbm1_resettable_counter_divider,
    check_resettable_integrator as check_vbm1_resettable_integrator,
    check_rotating_element_selector as check_vbm1_rotating_element_selector,
    check_sar_logic_4b as check_vbm1_sar_logic_4b,
    check_segmented_dac as check_vbm1_segmented_dac,
    check_settling_time_measurement_tb as check_vbm1_settling_time_measurement_tb,
    check_slew_rate_limiter as check_vbm1_slew_rate_limiter,
    check_strongarm_comparator_behavior as check_vbm1_strongarm_comparator_behavior,
    check_thermometer_dac as check_vbm1_thermometer_dac,
    check_thermometer_decoder_guarded as check_vbm1_thermometer_decoder_guarded,
    check_track_hold_aperture as check_vbm1_track_hold_aperture,
    check_vco_phase_integrator as check_vbm1_vco_phase_integrator,
    check_voltage_clamp as check_vbm1_voltage_clamp,
)


def read_meta(task_dir: Path) -> dict:
    return json.loads((task_dir / "meta.json").read_text(encoding="utf-8"))


def copy_inputs(run_dir: Path, dut_path: Path, tb_path: Path) -> tuple[Path, Path]:
    example_dir = tb_path.parent
    for src in example_dir.iterdir():
        dst = run_dir / src.name
        if src.is_dir():
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)

    # If the candidate DUT lives outside the example directory, stage it too.
    if dut_path.parent != example_dir:
        shutil.copy2(dut_path, run_dir / dut_path.name)

    dut_dst = run_dir / dut_path.name
    tb_dst = run_dir / tb_path.name
    return dut_dst, tb_dst


def run_evas(run_dir: Path, tb_file: Path, output_dir: Path, timeout_s: int) -> subprocess.CompletedProcess[str]:
    cmd = ["evas", "simulate", tb_file.name, "-o", str(output_dir)]
    return subprocess.run(
        cmd,
        cwd=run_dir,
        capture_output=True,
        text=True,
        timeout=timeout_s,
    )


FILE_METRIC_WRITER_TASKS = {
    "vbm1_file_metric_writer_dut",
    "vbm1_file_metric_writer_tb",
    "vbm1_file_metric_writer_e2e",
}

FINAL_STEP_FILE_METRIC_TASKS = {
    "final_step_file_metric_smoke",
    "vbr1_l2_measurement_flow_tb",
    "vbr1_l2_measurement_flow_e2e",
}


def _remove_stale_metric_file(task_id: str, run_dir: Path) -> None:
    for name in behavior_side_output_names(task_id):
        metric_path = run_dir / name
        if metric_path.exists():
            metric_path.unlink()


def _rising_crossing_time(rows: list[dict[str, float]], signal: str, threshold: float = 0.45) -> float | None:
    for idx in range(1, len(rows)):
        prev = rows[idx - 1]
        cur = rows[idx]
        t0 = prev.get("time")
        t1 = cur.get("time")
        v0 = prev.get(signal)
        v1 = cur.get(signal)
        if t0 is None or t1 is None or v0 is None or v1 is None:
            continue
        if not (v0 <= threshold < v1):
            continue
        if v1 == v0:
            return t1
        alpha = (threshold - v0) / (v1 - v0)
        return t0 + alpha * (t1 - t0)
    return None


def _parse_metric_time_token(token: str) -> float:
    try:
        return float(token)
    except ValueError:
        pass

    match = re.fullmatch(r"([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)([a-zA-Zµ]*)", token.strip())
    if match is None:
        raise ValueError(token)
    number_text, suffix = match.groups()
    value = float(number_text)
    if "e" in number_text.lower():
        return value
    normalized = suffix.lower().removesuffix("s")
    scale = {
        "f": 1e-15,
        "p": 1e-12,
        "n": 1e-9,
        "u": 1e-6,
        "µ": 1e-6,
        "m": 1e-3,
        "": 1.0,
    }.get(normalized)
    if scale is None:
        raise ValueError(token)
    return value * scale


def _validate_file_metric_output(task_id: str, run_dir: Path, csv_path: Path) -> tuple[bool, str] | None:
    if task_id in FINAL_STEP_FILE_METRIC_TASKS:
        candidate_paths = []
        for path in (run_dir / "candidate.out", csv_path.parent / "candidate.out"):
            if path not in candidate_paths:
                candidate_paths.append(path)
        metric_path = next((path for path in candidate_paths if path.exists()), None)
        if metric_path is None:
            return False, "candidate_file_missing"
        text = metric_path.read_text(encoding="utf-8").strip()
        match = re.fullmatch(
            r"count=([0-9]+)\s+metric=([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)",
            text,
        )
        if match is None:
            return False, f"candidate_file_bad_format={text!r}"
        count = int(match.group(1))
        metric = float(match.group(2))
        ok = count == 4 and abs(metric - 1.0) <= 0.02
        return ok, f"candidate_file_count={count} metric={metric:.3f}"

    if task_id not in FILE_METRIC_WRITER_TASKS:
        return None
    metric_path = run_dir / "metric.out"
    if not metric_path.exists():
        return False, "metric_file_missing"
    lines = [line.strip() for line in metric_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(lines) != 1:
        return False, f"metric_file_line_count={len(lines)} expected=1"
    parts = lines[0].split()
    if len(parts) != 2 or parts[0] != "cross":
        return False, f"metric_file_bad_format={lines[0]!r}"
    try:
        metric_time = _parse_metric_time_token(parts[1])
    except ValueError:
        return False, f"metric_file_bad_time={parts[1]!r}"
    crossing_time = _rising_crossing_time(load_csv(csv_path), "vin")
    if crossing_time is None:
        return False, "metric_file_no_waveform_crossing"
    delta = abs(metric_time - crossing_time)
    ok = delta <= 1e-9
    return ok, f"metric_file_time={metric_time:.3e} waveform_cross={crossing_time:.3e} delta={delta:.3e}"


def validate_behavior_side_outputs(task_id: str, run_dir: Path, csv_path: Path) -> tuple[bool, str] | None:
    return _validate_file_metric_output(task_id, run_dir, csv_path)


def behavior_side_output_names(task_id: str) -> tuple[str, ...]:
    if task_id in FINAL_STEP_FILE_METRIC_TASKS:
        return ("candidate.out",)
    if task_id in FILE_METRIC_WRITER_TASKS:
        return ("metric.out",)
    return ()


def load_csv(csv_path: Path) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({k: float(v) for k, v in row.items()})
    return rows


def evaluate_noise_gen_csv(csv_path: Path) -> tuple[float, list[str]]:
    """Fast streaming checker for noise_gen tasks on very large CSV files."""
    count = 0
    mean = 0.0
    m2 = 0.0
    max_abs = 0.0
    missing_cols = False

    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fields = set(reader.fieldnames or [])
        if not {"vin_i", "vout_o"}.issubset(fields):
            missing_cols = True
        else:
            for row in reader:
                try:
                    x = float(row["vout_o"]) - float(row["vin_i"])
                except (TypeError, ValueError):
                    continue
                count += 1
                delta = x - mean
                mean += delta / count
                m2 += delta * (x - mean)
                ax = abs(x)
                if ax > max_abs:
                    max_abs = ax

    if missing_cols:
        return 0.0, ["missing vin_i/vout_o"]
    if count == 0:
        return 0.0, ["noise_gen_empty_csv"]

    var = m2 / count
    std = math.sqrt(max(var, 0.0))
    ok = std > 0.01 and max_abs > 0.05
    return (1.0 if ok else 0.0), [f"noise_std={std:.4f} max_abs={max_abs:.4f} samples={count}"]


def _csv_fields(csv_path: Path) -> set[str]:
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return set(reader.fieldnames or [])


def _float_cell(row: dict[str, str], key: str, default: float = 0.0) -> float:
    try:
        return float(row.get(key, default))
    except (TypeError, ValueError):
        return default


def _stream_max(csv_path: Path, key: str) -> float:
    max_val = 0.0
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            max_val = max(max_val, _float_cell(row, key))
    return max_val


def _stream_pfd_deadzone_csv(csv_path: Path) -> tuple[float, list[str]]:
    fields = _csv_fields(csv_path)
    required = {"time", "ref", "div", "up", "dn"}
    if not required.issubset(fields):
        return 0.0, ["missing ref/div/up/dn"]

    vth = 0.5 * _stream_max(csv_path, "ref")
    prev_time: float | None = None
    prev_up = 0.0
    prev_dn = 0.0
    prev_up_bit = 0
    initialized = False
    high_up_dt = 0.0
    high_dn_dt = 0.0
    total_dt = 0.0
    run_len = 0
    max_run = 0
    up_pulses = 0

    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            time = _float_cell(row, "time")
            up = _float_cell(row, "up")
            dn = _float_cell(row, "dn")
            up_bit = 1 if up > vth else 0
            dn_bit = 1 if dn > vth else 0
            if initialized:
                dt = time - (prev_time if prev_time is not None else time)
                if dt > 0.0:
                    total_dt += dt
                    if 0.5 * (prev_up + up) > vth:
                        high_up_dt += dt
                    if 0.5 * (prev_dn + dn) > vth:
                        high_dn_dt += dt
                if prev_up_bit == 0 and up_bit == 1:
                    up_pulses += 1
            if up_bit and dn_bit:
                run_len += 1
                max_run = max(max_run, run_len)
            else:
                run_len = 0
            initialized = True
            prev_time = time
            prev_up = up
            prev_dn = dn
            prev_up_bit = up_bit

    up_frac = high_up_dt / max(total_dt, 1e-18)
    dn_frac = high_dn_dt / max(total_dt, 1e-18)
    if not (0.001 <= up_frac <= 0.03):
        return 0.0, [f"up_frac_out_of_range={up_frac:.4f}"]
    if dn_frac > 0.002:
        return 0.0, [f"dn_frac_too_high={dn_frac:.4f}"]
    if max_run > 6:
        return 0.0, [f"overlap_too_long={max_run}"]
    if up_pulses < 10:
        return 0.0, [f"too_few_up_pulses={up_pulses}"]
    return 1.0, [f"up_frac={up_frac:.4f} dn_frac={dn_frac:.4f} up_pulses={up_pulses}"]


def _stream_pfd_reset_race_csv(csv_path: Path) -> tuple[float, list[str]]:
    fields = _csv_fields(csv_path)
    required = {"time", "ref", "div", "up", "dn"}
    if not required.issubset(fields):
        return 0.0, ["missing ref/div/up/dn"]

    vth = 0.5 * _stream_max(csv_path, "ref")
    windows = {
        "first": {"start": 20e-9, "end": 120e-9, "up_dt": 0.0, "dn_dt": 0.0, "dt": 0.0, "up_pulses": 0, "dn_pulses": 0, "rows": 0},
        "second": {"start": 160e-9, "end": 260e-9, "up_dt": 0.0, "dn_dt": 0.0, "dt": 0.0, "up_pulses": 0, "dn_pulses": 0, "rows": 0},
    }
    total_dt = 0.0
    overlap_dt = 0.0
    prev: dict[str, float] | None = None
    prev_up_bit = 0
    prev_dn_bit = 0

    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur = {
                "time": _float_cell(row, "time"),
                "up": _float_cell(row, "up"),
                "dn": _float_cell(row, "dn"),
            }
            up_bit = 1 if cur["up"] > vth else 0
            dn_bit = 1 if cur["dn"] > vth else 0
            for state in windows.values():
                if state["start"] <= cur["time"] <= state["end"]:
                    state["rows"] += 1
                    if prev_up_bit == 0 and up_bit == 1:
                        state["up_pulses"] += 1
                    if prev_dn_bit == 0 and dn_bit == 1:
                        state["dn_pulses"] += 1
            if prev is not None:
                dt = cur["time"] - prev["time"]
                if dt > 0.0:
                    total_dt += dt
                    up_mid = 0.5 * (prev["up"] + cur["up"])
                    dn_mid = 0.5 * (prev["dn"] + cur["dn"])
                    if up_mid > vth and dn_mid > vth:
                        overlap_dt += dt
                    mid_t = 0.5 * (prev["time"] + cur["time"])
                    for state in windows.values():
                        if state["start"] <= mid_t <= state["end"]:
                            state["dt"] += dt
                            if up_mid > vth:
                                state["up_dt"] += dt
                            if dn_mid > vth:
                                state["dn_dt"] += dt
            prev = cur
            prev_up_bit = up_bit
            prev_dn_bit = dn_bit

    first = windows["first"]
    second = windows["second"]
    if first["rows"] < 4 or second["rows"] < 4:
        return 0.0, ["insufficient_window_samples"]
    up_first = first["up_dt"] / max(first["dt"], 1e-18)
    dn_first = first["dn_dt"] / max(first["dt"], 1e-18)
    up_second = second["up_dt"] / max(second["dt"], 1e-18)
    dn_second = second["dn_dt"] / max(second["dt"], 1e-18)
    overlap_frac = overlap_dt / max(total_dt, 1e-18)
    ok = (
        0.001 <= up_first <= 0.08
        and dn_first <= 0.01
        and 0.001 <= dn_second <= 0.08
        and up_second <= 0.01
        and first["up_pulses"] >= 4
        and second["dn_pulses"] >= 4
        and overlap_frac <= 0.01
    )
    return (1.0 if ok else 0.0), [
        f"up_first={up_first:.4f} dn_first={dn_first:.4f} "
        f"up_second={up_second:.4f} dn_second={dn_second:.4f} "
        f"up_pulses_first={int(first['up_pulses'])} "
        f"dn_pulses_second={int(second['dn_pulses'])} "
        f"overlap_frac={overlap_frac:.4f}"
    ]


def _stream_dac_binary_clk_4b_csv(csv_path: Path) -> tuple[float, list[str]]:
    fields = _csv_fields(csv_path)
    required = {"din3", "din2", "din1", "din0", "aout"}
    if not required.issubset(fields):
        return 0.0, ["missing din*/aout"]
    sums = {idx: 0.0 for idx in range(16)}
    counts = {idx: 0 for idx in range(16)}
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            code = (
                (1 if _float_cell(row, "din3") > 0.45 else 0) * 8
                + (1 if _float_cell(row, "din2") > 0.45 else 0) * 4
                + (1 if _float_cell(row, "din1") > 0.45 else 0) * 2
                + (1 if _float_cell(row, "din0") > 0.45 else 0)
            )
            sums[code] += _float_cell(row, "aout")
            counts[code] += 1
    medians = {code: sums[code] / counts[code] for code in counts if counts[code] > 0}
    sorted_codes = sorted(medians)
    monotonic = all(medians[sorted_codes[i]] <= medians[sorted_codes[i + 1]] + 1e-9 for i in range(len(sorted_codes) - 1))
    span = medians[sorted_codes[-1]] - medians[sorted_codes[0]] if sorted_codes else 0.0
    ok = len(sorted_codes) >= 14 and monotonic and span > 0.7
    return (1.0 if ok else 0.0), [f"levels={len(sorted_codes)} aout_span={span:.3f}"]


def _stream_sar_adc_dac_weighted_8b_csv(csv_path: Path) -> tuple[float, list[str]]:
    fields = _csv_fields(csv_path)
    required = {"vin", "vin_sh", "vout", "rst_n"} | {f"dout_{idx}" for idx in range(8)}
    if not required.issubset(fields):
        return 0.0, ["missing vin/vin_sh/vout/rst_n or dout_0..7"]
    count = 0
    err_sum = 0.0
    min_vout = float("inf")
    max_vout = float("-inf")
    codes: set[int] = set()
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if _float_cell(row, "rst_n") <= 0.45:
                continue
            code = sum((1 if _float_cell(row, f"dout_{idx}") > 0.45 else 0) << idx for idx in range(8))
            vin_sh = _float_cell(row, "vin_sh")
            vout = _float_cell(row, "vout")
            codes.add(code)
            err_sum += abs(vin_sh - vout)
            min_vout = min(min_vout, vout)
            max_vout = max(max_vout, vout)
            count += 1
    if count == 0:
        return 0.0, ["no post-reset samples"]
    unique_codes = len(codes)
    avg_abs_err = err_sum / count
    vout_span = max_vout - min_vout
    ok = unique_codes >= 48 and vout_span > 0.7 and avg_abs_err < 0.08
    return (1.0 if ok else 0.0), [f"unique_codes={unique_codes} avg_abs_err={avg_abs_err:.4f} vout_span={vout_span:.3f}"]


def _stream_dwa_ptr_gen_no_overlap_csv(csv_path: Path) -> tuple[float, list[str]]:
    fields = _csv_fields(csv_path)
    required = {"time", "clk_i", "rst_ni", "ptr_0", "cell_en_0"}
    if not required.issubset(fields):
        return 0.0, ["missing time/clk_i/rst_ni/ptr_0/cell_en_0"]
    ptr_cols = sorted([name for name in fields if re.fullmatch(r"ptr_\d+", name)], key=lambda n: int(n.rsplit("_", 1)[1]))
    cell_cols = sorted([name for name in fields if re.fullmatch(r"cell_en_\d+", name)], key=lambda n: int(n.rsplit("_", 1)[1]))
    if not ptr_cols or not cell_cols:
        return 0.0, ["missing ptr_* or cell_en_* columns"]

    pending_samples: list[float] = []
    sampled_cycles = 0
    bad_ptr_rows = 0
    max_active_cells = 0
    overlap_count = 0
    prev_active: set[int] | None = None
    prev_clk = 0.0
    initialized = False

    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            time = _float_cell(row, "time")
            clk = _float_cell(row, "clk_i")
            if initialized and prev_clk < 0.45 <= clk:
                pending_samples.append(time + 1.0e-9)
            while pending_samples and time >= pending_samples[0]:
                pending_samples.pop(0)
                if _float_cell(row, "rst_ni") <= 0.45:
                    continue
                sampled_cycles += 1
                ptr_active = {idx for idx, col in enumerate(ptr_cols) if _float_cell(row, col) > 0.45}
                if len(ptr_active) not in (0, 1):
                    bad_ptr_rows += 1
                active_cells = {idx for idx, col in enumerate(cell_cols) if _float_cell(row, col) > 0.45}
                max_active_cells = max(max_active_cells, len(active_cells))
                if prev_active is not None and prev_active & active_cells:
                    overlap_count += 1
                prev_active = active_cells
            prev_clk = clk
            initialized = True
    if sampled_cycles < 2:
        return 0.0, [f"insufficient_post_reset_samples count={sampled_cycles}"]
    ok = bad_ptr_rows == 0 and max_active_cells > 0 and overlap_count == 0
    return (1.0 if ok else 0.0), [
        f"sampled_cycles={sampled_cycles} bad_ptr_rows={bad_ptr_rows} "
        f"max_active_cells={max_active_cells} overlap_count={overlap_count}"
    ]


def _stream_not_gate_csv(csv_path: Path) -> tuple[float, list[str]]:
    fields = _csv_fields(csv_path)
    if {"a", "y"}.issubset(fields):
        a_col, y_col = "a", "y"
    elif {"not_a", "not_y"}.issubset(fields):
        a_col, y_col = "not_a", "not_y"
    else:
        return 0.0, ["missing a/y"]
    sampled_count = 0
    good = 0
    last_t = -1.0
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            time = _float_cell(row, "time")
            if time - last_t < 5e-10:
                continue
            last_t = time
            sampled_count += 1
            if (_float_cell(row, a_col) > 0.4) != (_float_cell(row, y_col) > 0.4):
                good += 1
    if sampled_count < 10:
        return 0.0, [f"too_few_samples={sampled_count}"]
    frac = good / sampled_count
    return (1.0 if frac > 0.9 else 0.0), [f"invert_match_frac={frac:.3f}"]


def _stream_gray_counter_one_bit_change_csv(csv_path: Path) -> tuple[float, list[str]]:
    fields = _csv_fields(csv_path)

    def pick(names: list[str]) -> str | None:
        lower = {field.lower(): field for field in fields}
        for name in names:
            if name.lower() in lower:
                return lower[name.lower()]
        return None

    clk_col = pick(["clk", "CLK"])
    rst_col = pick(["rst", "RST", "rstb", "RSTB"])
    g_cols = [pick([f"g{idx}", f"G{idx}"]) for idx in range(4)]
    if clk_col is None or rst_col is None or any(col is None for col in g_cols):
        return 0.0, ["missing clk/rst/g0..g3"]

    total_rows = 0
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for _ in reader:
            total_rows += 1
    if total_rows == 0:
        return 0.0, ["empty"]
    reset_prefix_rows = max(4, total_rows // 10)

    rst_prefix_high = False
    edge_count = 0
    post_reset_codes: list[int] = []
    pending_offsets: list[int] = []
    prev_clk: float | None = None

    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row_idx, row in enumerate(reader):
            clk = _float_cell(row, clk_col)
            rst = _float_cell(row, rst_col)
            if row_idx < reset_prefix_rows and rst > 0.45:
                rst_prefix_high = True
            if prev_clk is not None and prev_clk <= 0.45 < clk:
                # Match the row-based checker's settle=min(edge_idx + 8, last_row).
                # The current edge row is processed below, so start at 9.
                pending_offsets.append(9)
                edge_count += 1
            prev_clk = clk

            for pending_idx in range(len(pending_offsets) - 1, -1, -1):
                pending_offsets[pending_idx] -= 1
                if pending_offsets[pending_idx] > 0:
                    continue
                del pending_offsets[pending_idx]
                if (rst_prefix_high and rst > 0.45) or ((not rst_prefix_high) and rst < 0.45):
                    continue
                code = 0
                for bit_idx, col in enumerate(g_cols):
                    assert col is not None
                    if _float_cell(row, col) > 0.45:
                        code |= 1 << bit_idx
                post_reset_codes.append(code)

    if edge_count < 20:
        return 0.0, [f"not_enough_clk_edges={edge_count}"]
    if len(post_reset_codes) < 16:
        return 0.0, [f"not_enough_post_reset_codes={len(post_reset_codes)}"]

    bad_transitions = sum(
        1
        for a, b in zip(post_reset_codes[:-1], post_reset_codes[1:])
        if bin(a ^ b).count("1") != 1
    )
    unique_codes = set(post_reset_codes)
    expected_grays = {i ^ (i >> 1) for i in range(16)}
    if bad_transitions:
        return 0.0, [f"gray_property_violated bad_transitions={bad_transitions}"]
    missing = 16 - len(expected_grays & unique_codes)
    if missing:
        return 0.0, [f"missing_gray_codes count={missing}"]
    return 1.0, [f"unique_codes={len(unique_codes)} bad_transitions={bad_transitions}"]


def _stream_dwa_wraparound_csv(csv_path: Path) -> tuple[float, list[str]]:
    fields = _csv_fields(csv_path)
    required = {"time", "clk_i", "rst_ni", "ptr_0", "cell_en_0", "code_0"}
    if not required.issubset(fields):
        return 0.0, ["missing time/clk_i/rst_ni/ptr_0/cell_en_0/code_0"]

    ptr_cols = sorted(
        [field for field in fields if re.fullmatch(r"ptr_\d+", field)],
        key=lambda item: int(item.rsplit("_", 1)[1]),
    )
    cell_cols = sorted(
        [field for field in fields if re.fullmatch(r"cell_en_\d+", field)],
        key=lambda item: int(item.rsplit("_", 1)[1]),
    )
    code_cols = sorted(
        [field for field in fields if re.fullmatch(r"code_\d+", field)],
        key=lambda item: int(item.rsplit("_", 1)[1]),
    )
    if len(ptr_cols) != 16 or len(cell_cols) != 16 or len(code_cols) != 4:
        return 0.0, ["expected ptr_0..15, cell_en_0..15, and code_0..3 columns"]

    pending_samples: list[float] = []
    sampled: list[tuple[int, list[int], set[int]]] = []
    initialized = False
    prev_clk = 0.0
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            time = _float_cell(row, "time")
            clk = _float_cell(row, "clk_i")
            if initialized and prev_clk < 0.45 <= clk:
                pending_samples.append(time + 1.0e-9)
            while pending_samples and time >= pending_samples[0]:
                pending_samples.pop(0)
                if _float_cell(row, "rst_ni") <= 0.45:
                    continue
                code = sum(
                    (1 if _float_cell(row, col) > 0.45 else 0) << int(col[5:])
                    for col in code_cols
                )
                ptr_active = [idx for idx, col in enumerate(ptr_cols) if _float_cell(row, col) > 0.45]
                active_cells = {idx for idx, col in enumerate(cell_cols) if _float_cell(row, col) > 0.45}
                sampled.append((code, ptr_active, active_cells))
            prev_clk = clk
            initialized = True

    if len(sampled) < 5:
        return 0.0, [f"insufficient_post_reset_samples count={len(sampled)}"]

    expected_ptr = 13
    bad_ptr_rows = 0
    bad_count_rows = 0
    wrap_events = 0
    split_wrap_rows = 0
    prev_ptr = expected_ptr
    for code, ptr_active, active_cells in sampled:
        expected_ptr = (expected_ptr + code) % 16
        if expected_ptr < prev_ptr:
            wrap_events += 1
        if ptr_active != [expected_ptr]:
            bad_ptr_rows += 1
        if len(active_cells) != code:
            bad_count_rows += 1
        if active_cells and (max(active_cells) - min(active_cells) + 1) > len(active_cells):
            split_wrap_rows += 1
        prev_ptr = expected_ptr

    ok = bad_ptr_rows == 0 and bad_count_rows == 0 and wrap_events >= 2 and split_wrap_rows >= 2
    return (1.0 if ok else 0.0), [
        f"sampled_cycles={len(sampled)} bad_ptr_rows={bad_ptr_rows} "
        f"bad_count_rows={bad_count_rows} wrap_events={wrap_events} "
        f"split_wrap_rows={split_wrap_rows}"
    ]


def _stream_gain_extraction_csv(csv_path: Path) -> tuple[float, list[str]]:
    fields = _csv_fields(csv_path)
    required = {"vinp", "vinn", "vamp_p", "vamp_n"}
    if not required.issubset(fields):
        return 0.0, ["missing vinp/vinn/vamp_p/vamp_n"]

    count = 0
    mean_in = 0.0
    mean_out = 0.0
    m2_in = 0.0
    m2_out = 0.0
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            vin = _float_cell(row, "vinp") - _float_cell(row, "vinn")
            vout = _float_cell(row, "vamp_p") - _float_cell(row, "vamp_n")
            count += 1
            delta_in = vin - mean_in
            mean_in += delta_in / count
            m2_in += delta_in * (vin - mean_in)
            delta_out = vout - mean_out
            mean_out += delta_out / count
            m2_out += delta_out * (vout - mean_out)
    if count == 0:
        return 0.0, ["empty"]
    std_in = math.sqrt(max(m2_in / count, 0.0))
    std_out = math.sqrt(max(m2_out / count, 0.0))
    gain = std_out / std_in if std_in > 1e-12 else 0.0
    ok = gain > 4.0 and std_out > std_in
    return (1.0 if ok else 0.0), [f"diff_gain={gain:.2f}"]


def _stream_multimod_divider_ratio_switch_csv(csv_path: Path) -> tuple[float, list[str]]:
    fields = _csv_fields(csv_path)
    required = {"time", "clk_in", "div_out"}
    if not required.issubset(fields):
        return 0.0, ["missing time/clk_in/div_out"]

    in_edges: list[float] = []
    out_edges: list[float] = []
    initialized = False
    prev_in = 0.0
    prev_out = 0.0
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            time = _float_cell(row, "time")
            clk_in = _float_cell(row, "clk_in")
            div_out = _float_cell(row, "div_out")
            if initialized and prev_in < 0.45 <= clk_in:
                in_edges.append(time)
            if initialized and prev_out < 0.45 <= div_out:
                out_edges.append(time)
            prev_in = clk_in
            prev_out = div_out
            initialized = True

    if len(in_edges) < 40 or len(out_edges) < 10:
        return 0.0, [f"not_enough_edges in={len(in_edges)} out={len(out_edges)}"]

    windows = [
        (10e-9, 90e-9, 4, "pre_div4"),
        (120e-9, 190e-9, 5, "mid_div5"),
        (220e-9, 300e-9, 4, "post_div4"),
    ]
    details: list[str] = []
    for t0, t1, expected_ratio, label in windows:
        win_in = [time for time in in_edges if t0 <= time <= t1]
        win_out = [time for time in out_edges if t0 <= time <= t1]
        if len(win_in) < expected_ratio * 2 or len(win_out) < 2:
            return 0.0, [f"{label}_insufficient_edges in={len(win_in)} out={len(win_out)}"]
        measured_ratio = len(win_in) / max(len(win_out), 1)
        details.append(f"{label}={measured_ratio:.2f}")
        if abs(measured_ratio - expected_ratio) > 0.35:
            return 0.0, [";".join(details)]
    return 1.0, [";".join(details)]


STREAMING_BEHAVIOR_CHECKS = {
    "pfd_deadzone_smoke": _stream_pfd_deadzone_csv,
    "pfd_reset_race_smoke": _stream_pfd_reset_race_csv,
    "dac_binary_clk_4b_smoke": _stream_dac_binary_clk_4b_csv,
    "sar_adc_dac_weighted_8b_smoke": _stream_sar_adc_dac_weighted_8b_csv,
    "dwa_ptr_gen_no_overlap_smoke": _stream_dwa_ptr_gen_no_overlap_csv,
    "digital_basics_smoke": _stream_not_gate_csv,
    "gray_counter_one_bit_change_smoke": _stream_gray_counter_one_bit_change_csv,
    "dwa_wraparound_smoke": _stream_dwa_wraparound_csv,
    "gain_extraction_smoke": _stream_gain_extraction_csv,
    "multimod_divider_ratio_switch_smoke": _stream_multimod_divider_ratio_switch_csv,
}

VALIDATED_FAST_CHECKER_TASKS = frozenset(STREAMING_BEHAVIOR_CHECKS)


def _env_enabled(name: str) -> bool:
    return os.environ.get(name, "").strip().lower() in {"1", "true", "yes", "on"}


def _streaming_notes_require_row_fallback(notes: list[str]) -> bool:
    """Avoid turning observable/interface mismatches into behavior failures."""
    fallback_prefixes = (
        "missing ",
        "expected ",
    )
    return any(note.startswith(fallback_prefixes) for note in notes)


def evaluate_streaming_behavior(task_id: str, csv_path: Path) -> tuple[float, list[str]] | None:
    force_streaming = _env_enabled("VAEVAS_ENABLE_EXPERIMENTAL_STREAMING_CHECKERS")
    if not force_streaming:
        if _env_enabled("VAEVAS_DISABLE_VALIDATED_FAST_CHECKERS"):
            return None
        if task_id not in VALIDATED_FAST_CHECKER_TASKS:
            return None

    checker = STREAMING_BEHAVIOR_CHECKS.get(task_id)
    if checker is None:
        return None
    score, notes = checker(csv_path)
    if not force_streaming and _streaming_notes_require_row_fallback(notes):
        return None
    return score, [f"streaming_checker:{note}" for note in notes]


def rising_edges(values: list[float], times: list[float], threshold: float = 0.45) -> list[float]:
    edges: list[float] = []
    for i in range(1, len(values)):
        if values[i - 1] < threshold <= values[i]:
            edges.append(times[i])
    return edges


def sample_rows_at_or_after_times(
    rows: list[dict[str, float]],
    target_times: list[float],
    *,
    rst_key: str | None = None,
    rst_threshold: float = 0.45,
) -> list[dict[str, float]]:
    """Return rows whose time is the first sample at/after each target time.

    This function is linear in len(rows) + len(target_times). It replaces
    repeated per-target full scans that become O(n^2) on large tran.csv files.
    """
    if not rows or not target_times:
        return []

    sampled: list[dict[str, float]] = []
    row_idx = 0
    n_rows = len(rows)
    for t in target_times:
        while row_idx < n_rows and rows[row_idx]["time"] < t:
            row_idx += 1
        if row_idx >= n_rows:
            break
        row = rows[row_idx]
        if rst_key is None or row.get(rst_key, 0.0) > rst_threshold:
            sampled.append(row)
    return sampled


def decode_bus(rows: list[dict[str, float]], bit_names: list[str], threshold: float = 0.45) -> list[int]:
    decoded: list[int] = []
    for row in rows:
        code = 0
        for bit_name in bit_names:
            bit = 1 if row[bit_name] >= threshold else 0
            m = re.search(r"(\d+)$", bit_name)
            if m is None:
                warnings.warn(
                    f"decode_bus: bit_name {bit_name!r} has no trailing digit; "
                    "defaulting to bit index 0, result may be incorrect",
                    stacklevel=2,
                )
            idx = int(m.group(1)) if m else 0
            code |= bit << idx
        decoded.append(code)
    return decoded


def indexed_columns(keys: set[str], prefix: str) -> list[str]:
    cols = [k for k in keys if re.fullmatch(rf"{re.escape(prefix)}\d+", k)]
    return sorted(cols, key=lambda name: int(re.search(r"(\d+)$", name).group(1)))


def _canonical_signal_name(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", name.lower())


def _set_alias_if_missing(row: dict[str, float], alias: str, value: float) -> None:
    if alias and alias not in row:
        row[alias] = value


def _expanded_row_aliases(row: dict[str, float]) -> dict[str, float]:
    expanded = dict(row)
    original = list(row.items())
    for raw_key, value in original:
        key = raw_key.strip()
        if not key:
            continue

        candidates = {key, key.lower()}
        for sep in (":", "."):
            if sep in key:
                tail = key.split(sep)[-1]
                candidates.add(tail)
                candidates.add(tail.lower())

        vm = re.match(r"(?i)^v\(\s*([^)]+)\s*\)$", key)
        if vm:
            inner = vm.group(1).strip()
            candidates.add(inner)
            candidates.add(inner.lower())

        for cand in list(candidates):
            cm = re.match(r"^([A-Za-z_][A-Za-z0-9_$]*)\[(\d+)\]$", cand)
            if cm:
                root = cm.group(1)
                idx = cm.group(2)
                candidates.update(
                    {
                        f"{root}_{idx}",
                        f"{root}{idx}",
                        f"{root.lower()}_{idx}",
                        f"{root.lower()}{idx}",
                    }
                )
                # Common generated DWA/vector port names use direction suffixes
                # (`ptr_o[0]`, `cell_en_o[0]`, `code_i[0]`). The checkers use
                # scalar observable names (`ptr_0`, `cell_en_0`, `code_0`).
                stripped_root = root.lower()
                for suffix in ("_msb_i", "_lsb_i", "_o", "_i"):
                    if stripped_root.endswith(suffix):
                        stripped_root = stripped_root[: -len(suffix)]
                        break
                if stripped_root in {"ptr", "cell_en", "code"}:
                    candidates.update(
                        {
                            f"{stripped_root}_{idx}",
                            f"{stripped_root}{idx}",
                        }
                    )

            dm = re.search(r"(dout|din|div_code|cell_en|ptr|state|code|bin_o|g|d)_?(\d+)$", cand.lower())
            if dm:
                root = dm.group(1)
                idx = dm.group(2)
                candidates.update(
                    {
                        f"{root}_{idx}",
                        f"{root}{idx}",
                    }
                )
                if root == "d":
                    candidates.update({f"dout_{idx}", f"dout{idx}"})

        for alias in candidates:
            _set_alias_if_missing(expanded, alias, value)

    canonical_map: dict[str, str] = {}
    for key in expanded:
        canonical_map.setdefault(_canonical_signal_name(key), key)

    for idx in range(16):
        for target in (
            f"dout_{idx}",
            f"dout{idx}",
            f"din_{idx}",
            f"din{idx}",
            f"ptr_{idx}",
            f"cell_en_{idx}",
            f"g{idx}",
            f"state_{idx}",
            f"div_code_{idx}",
        ):
            ckey = _canonical_signal_name(target)
            if target not in expanded and ckey in canonical_map:
                expanded[target] = expanded[canonical_map[ckey]]

    for target in (
        "vin",
        "vout",
        "vin_sh",
        "rst_n",
        "clk",
        "clk_in",
        "clk_out",
        "lock",
        "ref_clk",
        "fb_clk",
        "vctrl_mon",
        "vinp",
        "vinn",
        "out_p",
        "out_n",
        "outp",
        "outn",
        "a",
        "b",
        "y",
        "d",
        "q",
        "qb",
        "rst",
        "ref",
        "div",
        "up",
        "dn",
        "serial_out",
        "dpn",
        "rstb",
        "en",
        "phase_out",
        "guard_out",
        "delay_out",
        "seen_out",
        "first_err_out",
        "max_err_out",
        "count_out",
        "metric_out",
        "mode",
        "out",
        "vin_i",
        "vout_o",
    ):
        ckey = _canonical_signal_name(target)
        if target not in expanded and ckey in canonical_map:
            expanded[target] = expanded[canonical_map[ckey]]

    return expanded


_TASK_ALIAS_CANDIDATES: dict[str, dict[str, tuple[str, ...]]] = {
    "digital_basics_smoke": {
        "a": ("not_a",),
        "y": ("not_y",),
    },
    "and_gate_smoke": {
        "a": ("and_a",),
        "b": ("and_b",),
        "y": ("and_y",),
    },
    "or_gate_smoke": {
        "a": ("or_a",),
        "b": ("or_b",),
        "y": ("or_y",),
    },
    "dff_rst_smoke": {
        "d": ("dff_d",),
        "clk": ("dff_clk",),
        "rst": ("dff_rst",),
        "q": ("dff_q",),
        "qb": ("dff_qb",),
    },
    "dwa_ptr_gen_no_overlap_smoke": {
        "clk_i": ("clk",),
        "rst_ni": ("rst_n",),
    },
    "dwa_wraparound_smoke": {
        "clk_i": ("clk",),
        "rst_ni": ("rst_n",),
        "code_0": ("code0",),
        "code_1": ("code1",),
        "code_2": ("code2",),
        "code_3": ("code3",),
    },
    "noise_gen_smoke": {
        "vin_i": ("vin",),
        "vout_o": ("vout",),
    },
    "sar_adc_dac_weighted_8b_smoke": {
        "vin_sh": ("vin",),
    },
}


def normalize_rows_for_task(task_id: str, rows: list[dict[str, float]]) -> list[dict[str, float]]:
    if not rows:
        return rows
    normalized = [_expanded_row_aliases(row) for row in rows]
    alias_rules = _TASK_ALIAS_CANDIDATES.get(task_id, {})
    if not alias_rules:
        return normalized
    for row in normalized:
        for target, candidates in alias_rules.items():
            if target in row:
                continue
            for cand in candidates:
                if cand in row:
                    row[target] = row[cand]
                    break
    return normalized


def check_clk_div(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows or "clk_in" not in rows[0] or "clk_out" not in rows[0]:
        return False, "missing clk_in/clk_out"
    times = [r["time"] for r in rows]
    in_edges = rising_edges([r["clk_in"] for r in rows], times)
    out_edges = rising_edges([r["clk_out"] for r in rows], times)
    if len(in_edges) < 8 or len(out_edges) < 2:
        return False, "not enough clock edges"
    ratio = len(in_edges) / max(len(out_edges), 1)
    return (3.0 <= ratio <= 5.0), f"edge_ratio={ratio:.2f}"


def check_clk_divider(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows or not {"clk_in", "clk_out", "lock"}.issubset(rows[0]):
        return False, "missing clk_in/clk_out/lock"

    sample = rows[0]
    div_cols: list[str] = []
    for idx in range(8):
        col = None
        for candidate in (f"div_code_{idx}", f"div_code[{idx}]"):
            if candidate in sample:
                col = candidate
                break
        if col is None:
            return False, "missing div_code_*"
        div_cols.append(col)

    ratio = 0
    for idx, col in enumerate(div_cols):
        if sample[col] > 0.45:
            ratio |= (1 << idx)
    if ratio < 1:
        ratio = 1

    times = [r["time"] for r in rows]
    clk_vals = [r["clk_in"] for r in rows]
    out_vals = [r["clk_out"] for r in rows]
    lock_vals = [r["lock"] for r in rows]

    in_edges = rising_edges(clk_vals, times)
    out_edges = rising_edges(out_vals, times)
    lock_edges = rising_edges(lock_vals, times)
    final_lock_high = lock_vals[-1] > 0.45

    if len(in_edges) < 8 or len(out_edges) < 2:
        return False, "not enough clock edges"

    if ratio == 1:
        level_match = sum(1 for ci, co in zip(clk_vals, out_vals) if ((ci > 0.45) == (co > 0.45))) / max(len(rows), 1)
        edge_ratio = len(in_edges) / max(len(out_edges), 1)
        ok = level_match > 0.98 and 0.95 <= edge_ratio <= 1.05 and final_lock_high
        return ok, f"ratio_code=1 in_edges={len(in_edges)} out_edges={len(out_edges)} lock_edges={len(lock_edges)} final_lock_high={final_lock_high} level_match={level_match:.3f} edge_ratio={edge_ratio:.3f}"

    if len(in_edges) < max(12, ratio * 2) or len(out_edges) < 3:
        return False, "not enough clock edges"

    intervals: list[int] = []
    for idx in range(1, len(out_edges)):
        start_t = out_edges[idx - 1]
        end_t = out_edges[idx]
        in_count = sum(1 for t in in_edges if start_t < t <= end_t)
        intervals.append(in_count)

    if len(intervals) < 2:
        return False, "insufficient output periods"

    measured = intervals[1:] if len(intervals) > 2 else intervals
    mismatch = [n for n in measured if n != ratio]
    period_match = 1.0 - (len(mismatch) / len(measured))

    hist: dict[int, int] = {}
    for n in measured:
        hist[n] = hist.get(n, 0) + 1

    high_seen = any(v > 0.45 for v in out_vals)
    low_seen = any(v <= 0.45 for v in out_vals)

    ok = (len(mismatch) == 0) and final_lock_high and high_seen and low_seen
    return ok, f"ratio_code={ratio} in_edges={len(in_edges)} out_edges={len(out_edges)} lock_edges={len(lock_edges)} final_lock_high={final_lock_high} period_match={period_match:.3f} interval_hist={hist}"


def check_comparator(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows or not {"vinp", "vinn", "out_p"}.issubset(rows[0]):
        return False, "missing vinp/vinn/out_p"
    out_vals = [r["out_p"] for r in rows]
    out_lo = min(out_vals)
    out_hi = max(out_vals)
    span = out_hi - out_lo
    if span < 0.3:
        return False, f"output_span_too_small={span:.3f}"
    vth = out_lo + 0.5 * span
    margin = 20e-3
    high_rows = [r for r in rows if r["vinp"] > r["vinn"] + margin]
    low_rows = [r for r in rows if r["vinn"] > r["vinp"] + margin]
    if not high_rows or not low_rows:
        return False, "insufficient_positive_negative_input_windows"
    high_frac = sum(1 for r in high_rows if r["out_p"] > vth) / len(high_rows)
    low_frac = sum(1 for r in low_rows if r["out_p"] < vth) / len(low_rows)
    ok = high_frac > 0.80 and low_frac > 0.80
    return ok, f"high_frac={high_frac:.3f} low_frac={low_frac:.3f} span={span:.3f}"


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


def _logic_state(value: float, threshold: float = 0.45) -> str:
    return "H" if value > threshold else "L"


def _differential_output_state(out_p: float, out_n: float, threshold: float = 0.45) -> str:
    if out_p > threshold and out_n < threshold:
        return "P"
    if out_p < threshold and out_n > threshold:
        return "N"
    if out_p < threshold and out_n < threshold:
        return "Z"
    return "X"


def check_release_threshold_comparator(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vinp", "vinn", "out_p"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/vinp/vinn/out_p"

    times = [r["time"] for r in rows]
    diff = [r["vinp"] - r["vinn"] for r in rows]
    out_vals = [r["out_p"] for r in rows]
    out_lo = min(out_vals)
    out_hi = max(out_vals)
    span = out_hi - out_lo
    if span < 0.60:
        return False, f"output_span_too_small={span:.3f}"

    vth = out_lo + 0.5 * span
    margin = 20e-3
    high_rows = [r for r in rows if r["vinp"] - r["vinn"] >= margin]
    low_rows = [r for r in rows if r["vinn"] - r["vinp"] >= margin]
    if len(high_rows) < 5 or len(low_rows) < 5:
        return False, "insufficient_positive_negative_input_windows"

    high_frac = sum(1 for r in high_rows if r["out_p"] > vth) / len(high_rows)
    low_frac = sum(1 for r in low_rows if r["out_p"] < vth) / len(low_rows)

    diff_rises = _threshold_crossings(diff, times, threshold=0.0, direction="rising")
    diff_falls = _threshold_crossings(diff, times, threshold=0.0, direction="falling")
    out_rises = _threshold_crossings(out_vals, times, threshold=vth, direction="rising")
    out_falls = _threshold_crossings(out_vals, times, threshold=vth, direction="falling")
    if not diff_rises or not diff_falls:
        return False, "missing_rising_or_falling_input_crossing"
    if not out_rises or not out_falls:
        return False, "missing_rising_or_falling_output_transition"

    settle_s = 2.0e-9
    rising_aligned = any(abs(ot - dt) <= settle_s for dt in diff_rises for ot in out_rises)
    falling_aligned = any(abs(ot - dt) <= settle_s for dt in diff_falls for ot in out_falls)
    ok = high_frac > 0.90 and low_frac > 0.90 and rising_aligned and falling_aligned
    return ok, (
        f"high_frac={high_frac:.3f} low_frac={low_frac:.3f} span={span:.3f} "
        f"diff_rises={len(diff_rises)} diff_falls={len(diff_falls)} "
        f"out_rises={len(out_rises)} out_falls={len(out_falls)} "
        f"rising_aligned={rising_aligned} falling_aligned={falling_aligned}"
    )


def check_release_offset_comparator(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "vinp", "vinn", "out_p"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/clk/vinp/vinn/out_p"

    times = [r["time"] for r in rows]
    clk_vals = [r["clk"] for r in rows]
    out_vals = [r["out_p"] for r in rows]
    out_span = max(out_vals) - min(out_vals)
    if out_span < 0.60:
        return False, f"output_span_too_small={out_span:.3f}"

    edge_times = rising_edges(clk_vals, times, threshold=0.45)
    if len(edge_times) < 7:
        return False, f"too_few_clock_edges={len(edge_times)}"

    vos = 5e-3
    sample_delay = 0.50e-9
    expected: list[str] = []
    observed: list[str] = []
    diffs_mv: list[float] = []
    mismatches = 0
    for edge_t in edge_times[:7]:
        sample_t = edge_t + sample_delay
        vinp = sample_signal_at(rows, "vinp", edge_t)
        vinn = sample_signal_at(rows, "vinn", edge_t)
        out_p = sample_signal_at(rows, "out_p", sample_t)
        if vinp is None or vinn is None or out_p is None:
            return False, f"missing_sample_near_edge={edge_t * 1e9:.2f}ns"
        diff_v = vinp - vinn
        diffs_mv.append(diff_v * 1e3)
        want = "H" if diff_v > vos else "L"
        got = _logic_state(out_p)
        expected.append(want)
        observed.append(got)
        if got != want:
            mismatches += 1

    sequence = "".join(observed)
    expected_sequence = "".join(expected)
    has_below_offset_positive = any(0.0 <= mv < vos * 1e3 for mv, want in zip(diffs_mv, expected) if want == "L")
    has_above_offset_positive = any(mv > vos * 1e3 for mv, want in zip(diffs_mv, expected) if want == "H")
    has_negative_low = any(mv < -1.0 for mv, want in zip(diffs_mv, expected) if want == "L")
    ok = (
        mismatches == 0
        and sequence == "LLLHHLL"
        and has_below_offset_positive
        and has_above_offset_positive
        and has_negative_low
    )
    diff_text = ",".join(f"{mv:.1f}" for mv in diffs_mv)
    return ok, (
        f"offset_decisions={sequence} expected={expected_sequence} "
        f"diffs_mv=[{diff_text}] mismatches={mismatches} "
        f"below_offset_positive={has_below_offset_positive} "
        f"above_offset_positive={has_above_offset_positive}"
    )


def check_release_strongarm_latch_comparator(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "vinp", "vinn", "out_p", "out_n"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/clk/vinp/vinn/out_p/out_n"

    out_p_vals = [r["out_p"] for r in rows]
    out_n_vals = [r["out_n"] for r in rows]
    out_p_span = max(out_p_vals) - min(out_p_vals)
    out_n_span = max(out_n_vals) - min(out_n_vals)
    if out_p_span < 0.60 or out_n_span < 0.60:
        return False, f"insufficient_toggle out_p_span={out_p_span:.3f} out_n_span={out_n_span:.3f}"

    sample_plan = [
        ("p_decision", 0.66e-9, "P", "positive"),
        ("p_hold_after_input_swap", 0.88e-9, "P", "negative"),
        ("reset_after_p", 1.12e-9, "Z", "negative"),
        ("n_decision", 1.66e-9, "N", "negative"),
        ("n_hold_after_input_swap", 1.88e-9, "N", "positive"),
        ("reset_after_n", 2.12e-9, "Z", "positive"),
        ("second_p_decision", 2.70e-9, "P", "positive"),
        ("second_n_decision", 3.70e-9, "N", "negative"),
    ]

    states: list[str] = []
    diff_signs: list[str] = []
    mismatches: list[str] = []
    for label, sample_t, expected_state, expected_diff_sign in sample_plan:
        out_p = sample_signal_at(rows, "out_p", sample_t)
        out_n = sample_signal_at(rows, "out_n", sample_t)
        vinp = sample_signal_at(rows, "vinp", sample_t)
        vinn = sample_signal_at(rows, "vinn", sample_t)
        if out_p is None or out_n is None or vinp is None or vinn is None:
            return False, f"missing_sample:{label}"
        state = _differential_output_state(out_p, out_n)
        diff = vinp - vinn
        diff_sign = "positive" if diff > 0.2e-3 else ("negative" if diff < -0.2e-3 else "near_zero")
        states.append(state)
        diff_signs.append(diff_sign)
        if state != expected_state or diff_sign != expected_diff_sign:
            mismatches.append(f"{label}:{state}/{diff_sign}")

    ok = not mismatches
    return ok, (
        f"latch_states={''.join(states)} expected=PPZNNZPN "
        f"diff_signs={','.join(diff_signs)} mismatches={';'.join(mismatches) or 'none'}"
    )


def check_cmp_delay(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "vinp", "vinn", "out_p"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/clk/vinp/vinn/out_p"

    phases = [
        (0.0e-9, 4.0e-9, 10e-3),
        (4.0e-9, 8.0e-9, 1e-3),
        (8.0e-9, 12.0e-9, 0.1e-3),
        (12.0e-9, 16.0e-9, 0.01e-3),
    ]
    threshold = 0.45
    clk_rise_offset = 0.1e-9
    times = [r["time"] for r in rows]
    out_p = [r["out_p"] for r in rows]

    delays_ns: list[float] = []
    missing_high: list[str] = []
    for start_t, end_t, diff_v in phases:
        phase_samples = [r["out_p"] for r in rows if start_t <= r["time"] < end_t]
        if not phase_samples or max(phase_samples) < threshold:
            missing_high.append(f"{diff_v * 1e3:.2g}mV")
            continue

        search_start = start_t + clk_rise_offset
        crossing_t = None
        for idx, t in enumerate(times):
            if t < search_start or t >= min(end_t, search_start + 3.0e-9):
                continue
            if out_p[idx] > threshold:
                crossing_t = t
                break
        if crossing_t is None:
            return False, f"missing_threshold_crossing diff={diff_v * 1e3:.2g}mV"
        delays_ns.append((crossing_t - search_start) * 1e9)

    if missing_high:
        return False, f"out_p_never_high phases={','.join(missing_high)}"
    if len(delays_ns) != len(phases):
        return False, f"insufficient_delay_measurements count={len(delays_ns)}"

    monotonic = all(delays_ns[i] <= delays_ns[i + 1] + 0.12 for i in range(len(delays_ns) - 1))
    ok = monotonic
    return ok, f"delays_ns={[round(v, 3) for v in delays_ns]} monotonic={monotonic}"


def check_cmp_strongarm(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "out_p", "out_n"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/out_p/out_n"

    threshold = 0.45
    out_p = [r["out_p"] for r in rows]
    out_n = [r["out_n"] for r in rows]

    out_p_span = max(out_p) - min(out_p)
    out_n_span = max(out_n) - min(out_n)
    if out_p_span < threshold or out_n_span < threshold:
        return False, f"insufficient_toggle out_p_span={out_p_span:.3f} out_n_span={out_n_span:.3f}"

    samples = []
    for sample_t in [0.75e-9, 1.75e-9, 2.75e-9, 3.75e-9]:
        out_p_sample = sample_signal_at(rows, "out_p", sample_t)
        out_n_sample = sample_signal_at(rows, "out_n", sample_t)
        if out_p_sample is None or out_n_sample is None:
            return False, f"missing_decision_sample_at={sample_t * 1e9:.2f}ns"
        if out_p_sample > threshold and out_n_sample < threshold:
            samples.append("P")
        elif out_p_sample < threshold and out_n_sample > threshold:
            samples.append("N")
        else:
            samples.append("X")

    ok = samples == ["P", "P", "N", "N"]
    return ok, f"decision_samples={''.join(samples)} expected=PPNN"


def check_strongarm_reset_priority_bug(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "rst", "inp", "inn", "outp", "outn"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/rst/inp/inn/outp/outn"

    threshold = 0.45
    reset_window = [r for r in rows if r["rst"] > threshold]
    active_window = [r for r in rows if r["time"] >= 24e-9 and r["rst"] < threshold]
    if not reset_window or not active_window:
        return False, "insufficient_reset_or_active_window"

    reset_outp_max = max(r["outp"] for r in reset_window)
    reset_outn_max = max(r["outn"] for r in reset_window)

    high_rows = [r for r in active_window if r["inp"] > r["inn"] + 5e-3]
    low_rows = [r for r in active_window if r["inp"] + 5e-3 < r["inn"]]
    if not high_rows or not low_rows:
        return False, "missing_post_reset_polarity_windows"

    high_outp = sum(1 for r in high_rows if r["outp"] > threshold) / len(high_rows)
    high_outn = sum(1 for r in high_rows if r["outn"] < threshold) / len(high_rows)
    low_outp = sum(1 for r in low_rows if r["outp"] < threshold) / len(low_rows)
    low_outn = sum(1 for r in low_rows if r["outn"] > threshold) / len(low_rows)

    ok = (
        reset_outp_max < 0.1
        and reset_outn_max < 0.1
        and high_outp > 0.75
        and high_outn > 0.75
        and low_outp > 0.75
        and low_outn > 0.75
    )
    return ok, (
        f"reset_outp_max={reset_outp_max:.3f} "
        f"reset_outn_max={reset_outn_max:.3f} "
        f"high_outp={high_outp:.3f} high_outn={high_outn:.3f} "
        f"low_outp={low_outp:.3f} low_outn={low_outn:.3f}"
    )


def check_cmp_hysteresis(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "out_p", "out_n"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/out_p/out_n"

    threshold = 0.45
    times_ns = [r["time"] * 1e9 for r in rows]
    out_p = [r["out_p"] for r in rows]
    out_n = [r["out_n"] for r in rows]

    if max(out_p) - min(out_p) < threshold or max(out_n) - min(out_n) < threshold:
        return False, "outputs_do_not_toggle"

    pre = [out_p[idx] for idx, t in enumerate(times_ns) if t < 20.0]
    mid = [out_p[idx] for idx, t in enumerate(times_ns) if 35.0 < t < 60.0]
    post = [out_p[idx] for idx, t in enumerate(times_ns) if t > 75.0]
    if not pre or not mid or not post:
        return False, "insufficient_hysteresis_windows"

    pre_low_frac = sum(1 for v in pre if v < threshold) / len(pre)
    mid_high_frac = sum(1 for v in mid if v > threshold) / len(mid)
    post_low_frac = sum(1 for v in post if v < threshold) / len(post)
    if pre_low_frac < 0.95 or mid_high_frac < 0.95 or post_low_frac < 0.95:
        return False, f"window_fracs pre={pre_low_frac:.3f} mid={mid_high_frac:.3f} post={post_low_frac:.3f}"

    rise_t = None
    fall_t = None
    for idx in range(1, len(out_p)):
        if rise_t is None and out_p[idx - 1] < threshold <= out_p[idx]:
            rise_t = times_ns[idx]
        if fall_t is None and out_p[idx - 1] > threshold >= out_p[idx]:
            fall_t = times_ns[idx]

    if rise_t is None or fall_t is None:
        return False, "missing_trip_crossings"
    if not (29.0 <= rise_t <= 31.5):
        return False, f"rise_t_out_of_range={rise_t:.3f}ns"
    if not (68.5 <= fall_t <= 71.5):
        return False, f"fall_t_out_of_range={fall_t:.3f}ns"
    return True, f"rise_t={rise_t:.3f}ns fall_t={fall_t:.3f}ns"


def check_ramp_gen(rows: list[dict[str, float]]) -> tuple[bool, str]:
    bit_names = [f"code_{i}" for i in range(12) if f"code_{i}" in rows[0]]
    if not bit_names:
        return False, "missing code_* bits"
    codes = decode_bus(rows, bit_names)
    nondecreasing = all(codes[i] <= codes[i + 1] for i in range(len(codes) - 1))
    return nondecreasing, f"code_start={codes[0]} code_end={codes[-1]}"


def check_d2b(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "empty tran.csv"
    if all(k in rows[0] for k in ["bin_o_3", "bin_o_2", "bin_o_1", "bin_o_0"]):
        codes = decode_bus(rows, ["bin_o_0", "bin_o_1", "bin_o_2", "bin_o_3"])
        stable = len(set(codes)) == 1
        return stable and codes[0] == 9, f"stable_code={codes[0]}"
    dout_bits = [k for k in rows[0] if re.fullmatch(r"dout[_\[]?\d+\]?", k, flags=re.IGNORECASE)]
    vin_col = next((k for k in rows[0] if k.lower().startswith("vin")), None)
    if vin_col and dout_bits:
        codes = decode_bus(rows, dout_bits)
        vins = [r[vin_col] for r in rows]
        pairs = sorted(zip(vins, codes), key=lambda x: x[0])
        monotonic = all(pairs[i][1] <= pairs[i + 1][1] for i in range(len(pairs) - 1))
        return monotonic, "dynamic monotonic code check"
    return False, "missing d2b outputs"


def check_adc_dac_ideal_4b(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows or not {"vin", "vout", "rst_n"}.issubset(rows[0]):
        return False, "missing vin/vout/rst_n"
    post = [r for r in rows if r["rst_n"] > 0.45]
    if not post:
        return False, "no post-reset samples"
    if "dout_code" in rows[0]:
        codes = [int(round(r["dout_code"])) for r in post]
    elif {"dout_3", "dout_2", "dout_1", "dout_0"}.issubset(rows[0]):
        codes = [
            ((1 if r["dout_3"] > 0.45 else 0) << 3)
            | ((1 if r["dout_2"] > 0.45 else 0) << 2)
            | ((1 if r["dout_1"] > 0.45 else 0) << 1)
            | (1 if r["dout_0"] > 0.45 else 0)
            for r in post
        ]
    else:
        return False, "missing dout_code or dout_3..0"
    vouts = [r["vout"] for r in post]
    vins = [r["vin"] for r in post]
    unique_codes = len(set(codes))
    monotonic = all(codes[i] <= codes[i + 1] for i in range(len(codes) - 1))
    span = max(vouts) - min(vouts)
    vin_span = max(vins) - min(vins)
    ok = unique_codes >= 12 and monotonic and span > 0.6 and vin_span > 0.6
    return ok, f"unique_codes={unique_codes} vout_span={span:.3f} vin_span={vin_span:.3f}"


def check_dac_binary_clk_4b(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows or not {"din3", "din2", "din1", "din0", "aout"}.issubset(rows[0]):
        return False, "missing din*/aout"
    levels: dict[int, list[float]] = {}
    for r in rows:
        code = (
            (1 if r["din3"] > 0.45 else 0) * 8
            + (1 if r["din2"] > 0.45 else 0) * 4
            + (1 if r["din1"] > 0.45 else 0) * 2
            + (1 if r["din0"] > 0.45 else 0)
        )
        levels.setdefault(code, []).append(r["aout"])
    medians = {c: sum(vs) / len(vs) for c, vs in levels.items()}
    sorted_codes = sorted(medians)
    monotonic = all(medians[sorted_codes[i]] <= medians[sorted_codes[i + 1]] + 1e-9 for i in range(len(sorted_codes) - 1))
    span = medians[sorted_codes[-1]] - medians[sorted_codes[0]] if sorted_codes else 0.0
    ok = len(sorted_codes) >= 14 and monotonic and span > 0.7
    return ok, f"levels={len(sorted_codes)} aout_span={span:.3f}"


def check_dac_therm_16b(rows: list[dict[str, float]]) -> tuple[bool, str]:
    bit_names = [f"d{i}" for i in range(16) if f"d{i}" in rows[0]]
    if not rows or not bit_names or "vout" not in rows[0]:
        return False, "missing d*/vout"
    ones_counts = [sum(1 for b in bit_names if r[b] > 0.45) for r in rows]
    vouts = [r["vout"] for r in rows]
    max_ones = max(ones_counts)
    max_vout = max(vouts)
    last_pairs: dict[int, float] = {}
    for ones, vout in zip(ones_counts, vouts):
        last_pairs[ones] = vout
    sorted_ones = sorted(last_pairs)
    monotonic = all(last_pairs[sorted_ones[i]] <= last_pairs[sorted_ones[i + 1]] + 1e-9 for i in range(len(sorted_ones) - 1))
    ok = max_ones == 16 and max_vout > 15.0 and monotonic
    return ok, f"max_ones={max_ones} max_vout={max_vout:.3f}"


def check_vbm1_thermometer_dac_15seg(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "empty"
    seg_names = [f"seg{i}" for i in range(15)]
    required = {"time", "aout", *seg_names}
    if not required.issubset(rows[0]):
        return False, f"missing time/aout/seg0..seg14; keys={list(rows[0].keys())[:10]}"

    checkpoints = [
        (15e-9, 0),
        (45e-9, 1),
        (75e-9, 2),
        (105e-9, 7),
        (135e-9, 14),
        (165e-9, 15),
    ]
    levels: list[tuple[int, float]] = []
    errors: list[float] = []
    notes: list[str] = []
    for target_t, expected_count in checkpoints:
        row = min(rows, key=lambda r: abs(r["time"] - target_t))
        observed_count = sum(1 for name in seg_names if row[name] > 0.45)
        expected_v = 0.9 * expected_count / 15.0
        error = abs(row["aout"] - expected_v)
        levels.append((expected_count, row["aout"]))
        errors.append(error)
        notes.append(f"{expected_count}:{row['aout']:.3f}/{observed_count}")

    monotonic = all(levels[i][1] <= levels[i + 1][1] + 1e-6 for i in range(len(levels) - 1))
    counts_match = all(
        sum(1 for name in seg_names if min(rows, key=lambda r, t=t: abs(r["time"] - t))[name] > 0.45) == count
        for t, count in checkpoints
    )
    max_err = max(errors)
    full_scale_ok = abs(levels[-1][1] - 0.9) <= 0.02
    ok = counts_match and monotonic and max_err <= 0.02 and full_scale_ok
    return ok, (
        f"levels={' '.join(notes)} max_err={max_err:.3f} "
        f"monotonic={monotonic} counts_match={counts_match} "
        f"full_scale_ok={full_scale_ok}"
    )


def check_sar_adc_dac_weighted_8b(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows or not {"vin", "vin_sh", "vout", "rst_n"}.issubset(rows[0]):
        return False, "missing vin/vin_sh/vout/rst_n"
    post = [r for r in rows if r["rst_n"] > 0.45]
    if not post:
        return False, "no post-reset samples"
    # Always decode from dout bits for consistent comparison across simulators
    # (EVAS has dout_code column, but Spectre does not - using bits ensures fairness)
    bit_names = [f"dout_{idx}" for idx in range(8) if f"dout_{idx}" in rows[0]]
    if len(bit_names) != 8:
        return False, "missing dout_0..7"
    codes = [
        sum((1 if r[name] > 0.45 else 0) << idx for idx, name in enumerate(bit_names))
        for r in post
    ]
    vinsh = [r["vin_sh"] for r in post]
    vouts = [r["vout"] for r in post]
    unique_codes = len(set(codes))
    avg_abs_err = sum(abs(a - b) for a, b in zip(vinsh, vouts)) / len(post)
    vout_span = max(vouts) - min(vouts)
    ok = (
        unique_codes >= 48
        and vout_span > 0.7
        and avg_abs_err < 0.08
    )
    return ok, f"unique_codes={unique_codes} avg_abs_err={avg_abs_err:.4f} vout_span={vout_span:.3f}"


def check_not_gate(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows or not {"a", "y"}.issubset(rows[0]):
        return False, "missing a/y"
    # Down-sample to ≥500 ps spacing to avoid over-weighting EVAS transition sub-steps
    sampled: list[dict[str, float]] = []
    last_t = -1.0
    for r in rows:
        if r["time"] - last_t >= 5e-10:
            sampled.append(r)
            last_t = r["time"]
    check_rows = sampled if len(sampled) >= 10 else rows
    good = sum(1 for r in check_rows if (r["a"] > 0.4) != (r["y"] > 0.4))
    frac = good / len(check_rows)
    return frac > 0.9, f"invert_match_frac={frac:.3f}"


def check_and_gate(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"a", "b", "y"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing a/b/y"
    check_rows = [r for r in rows if r["time"] >= rows[0]["time"] + 5e-10]
    if len(check_rows) < 10:
        check_rows = rows
    good = 0
    for r in check_rows:
        a_hi = r["a"] > 0.45
        b_hi = r["b"] > 0.45
        y_hi = r["y"] > 0.45
        if y_hi == (a_hi and b_hi):
            good += 1
    frac = good / len(check_rows)
    return frac > 0.92, f"and_truth_match_frac={frac:.3f}"


def check_or_gate(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"a", "b", "y"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing a/b/y"
    check_rows = [r for r in rows if r["time"] >= rows[0]["time"] + 5e-10]
    if len(check_rows) < 10:
        check_rows = rows
    good = 0
    for r in check_rows:
        a_hi = r["a"] > 0.45
        b_hi = r["b"] > 0.45
        y_hi = r["y"] > 0.45
        if y_hi == (a_hi or b_hi):
            good += 1
    frac = good / len(check_rows)
    return frac > 0.92, f"or_truth_match_frac={frac:.3f}"


def check_dff_rst(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "d", "clk", "rst", "q", "qb"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/d/clk/rst/q/qb"
    clk_max = max(r["clk"] for r in rows)
    vth = 0.45 if clk_max < 0.9 else 0.5 * clk_max
    edges = [
        idx
        for idx in range(1, len(rows))
        if rows[idx - 1]["clk"] <= vth < rows[idx]["clk"]
    ]
    if len(edges) < 6:
        return False, f"too_few_clk_edges={len(edges)}"

    mismatches = 0
    qb_mismatches = 0
    checks = 0
    for idx in edges:
        edge_row = rows[idx]
        edge_time = edge_row["time"]
        settle = idx
        while settle + 1 < len(rows) and rows[settle]["time"] < edge_time + 100e-12:
            settle += 1
        r = rows[settle]
        expected_q_hi = False if edge_row["rst"] > vth else (edge_row["d"] > vth)
        q_hi = r["q"] > vth
        qb_hi = r["qb"] > vth
        checks += 1
        if q_hi != expected_q_hi:
            mismatches += 1
        if qb_hi == q_hi:
            qb_mismatches += 1
    ok = checks >= 6 and mismatches <= 1 and qb_mismatches <= 1
    return ok, f"checks={checks} q_mismatch={mismatches} qb_mismatch={qb_mismatches}"


def check_lfsr(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows or not {"dpn", "rstb"}.issubset(rows[0]):
        return False, "missing dpn/rstb"
    post = [r["dpn"] for r in rows if r["rstb"] > 0.45]
    if len(post) < 2:
        return False, "not enough post-reset samples"
    binary = [1 if v > 0.45 else 0 for v in post]
    hi_frac = sum(binary) / len(binary)
    transitions = sum(1 for i in range(len(binary) - 1) if binary[i] != binary[i + 1])
    ok = 0.05 < hi_frac < 0.95 and transitions >= 10
    return ok, f"transitions={transitions} hi_frac={hi_frac:.3f}"


def check_prbs7(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"clk", "rst_n", "en", "serial_out"} | {f"state_{i}" for i in range(7)}
    if not rows or not required.issubset(rows[0]):
        return False, "missing clk/rst_n/en/serial_out/state_*"

    post = [r for r in rows if r["rst_n"] > 0.45 and r["en"] > 0.45]
    if len(post) < 2:
        return False, "no post-reset enabled samples"

    def bit(row: dict[str, float], name: str) -> int:
        return 1 if row[name] > 0.45 else 0

    def state_code(row: dict[str, float]) -> int:
        code = 0
        for idx in range(7):
            code |= bit(row, f"state_{idx}") << idx
        return code

    serial = [bit(r, "serial_out") for r in post]
    states = [state_code(r) for r in post]

    if all(code == 0 for code in states):
        return False, "state stuck at zero"

    serial_transitions = sum(1 for i in range(len(serial) - 1) if serial[i] != serial[i + 1])
    unique_states = len(set(states))
    state_transitions = sum(1 for i in range(len(states) - 1) if states[i] != states[i + 1])

    ok = serial_transitions >= 10 and unique_states >= 8 and state_transitions >= 8
    return ok, f"serial_transitions={serial_transitions} unique_states={unique_states} state_transitions={state_transitions}"


def check_therm2bin(rows: list[dict[str, float]]) -> tuple[bool, str]:
    therm_bits = [f"therm_{i}" for i in range(15)]
    bin_bits = [f"bin_{i}" for i in range(4)]
    required = set(therm_bits + bin_bits)
    if not rows or not required.issubset(rows[0]):
        return False, "missing therm_* or bin_* signals"

    def bit(row: dict[str, float], name: str) -> int:
        return 1 if row[name] > 0.45 else 0

    def thermometer_count(row: dict[str, float]) -> int:
        return sum(bit(row, name) for name in therm_bits)

    def binary_code(row: dict[str, float]) -> int:
        return sum(bit(row, f"bin_{idx}") << idx for idx in range(4))

    counts = [thermometer_count(row) for row in rows]
    codes = [binary_code(row) for row in rows]

    if not counts:
        return False, "empty therm2bin dataset"

    def far_from_threshold(v: float, lo: float = 0.35, hi: float = 0.55) -> bool:
        return v <= lo or v >= hi

    stable_indices = []
    for idx in range(1, len(rows)):
        if counts[idx] != counts[idx - 1]:
            continue
        therm_stable = all(
            far_from_threshold(rows[idx][name]) and far_from_threshold(rows[idx - 1][name])
            for name in therm_bits
        )
        bin_stable = all(
            far_from_threshold(rows[idx][name])
            for name in bin_bits
        )
        if therm_stable and bin_stable:
            stable_indices.append(idx)

    min_stable_points = max(10, len(rows) // 20)
    if len(stable_indices) < min_stable_points:
        return False, f"insufficient_strict_stable_points={len(stable_indices)}"

    mismatches = [idx for idx in stable_indices if codes[idx] != min(counts[idx], 15)]
    stable_ok = len(mismatches) == 0
    distinct_counts = len(set(counts))
    bubble_present = any(
        counts[i] > counts[i + 1]
        for i in range(len(counts) - 1)
    )
    ok = stable_ok and distinct_counts >= 6 and bubble_present
    return ok, f"distinct_counts={distinct_counts} bubble_present={bubble_present} strict_stable_points={len(stable_indices)} strict_mismatches={len(mismatches)}"


def check_multimod_divider(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"clk_in", "mod", "prescaler_out", "mod_0", "mod_1", "mod_2", "mod_3"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing clk_in/mod/prescaler_out/mod_*"

    times = [r["time"] for r in rows]
    clk_edges = [i for i in range(1, len(rows)) if rows[i - 1]["clk_in"] < 0.45 <= rows[i]["clk_in"]]
    out_edges = [i for i in range(1, len(rows)) if rows[i - 1]["prescaler_out"] < 0.45 <= rows[i]["prescaler_out"]]
    clk_edge_times = [times[idx] for idx in clk_edges]

    if len(clk_edges) < 8 or len(out_edges) < 4:
        return False, "not enough clock or output edges"

    base = sum((1 if rows[0][f"mod_{idx}"] > 0.45 else 0) << idx for idx in range(4))
    if base < 1:
        base = 1

    switch_time = None
    for idx in range(1, len(rows)):
        if rows[idx - 1]["mod"] < 0.45 <= rows[idx]["mod"]:
            switch_time = times[idx]
            break

    if switch_time is None:
        return False, "no MOD transition found"

    intervals = []
    for idx in range(1, len(out_edges)):
        start_idx = out_edges[idx - 1]
        end_idx = out_edges[idx]
        start_t = times[start_idx]
        end_t = times[end_idx]
        interval_len = sum(1 for clk_t in clk_edge_times if start_t < clk_t <= end_t)
        intervals.append((start_t, end_t, interval_len))

    pre = [interval for start_t, end_t, interval in intervals if end_t < switch_time]
    post = [interval for start_t, end_t, interval in intervals if start_t >= switch_time]

    pre_ok = len(pre) >= 2 and all(interval == base for interval in pre)
    post_ok = len(post) >= 2 and all(interval == base + 1 for interval in post)
    ok = pre_ok and post_ok
    return ok, f"base={base} pre_count={len(pre)} post_count={len(post)} switch_time_ns={switch_time * 1e9:.3f}"


def check_multimod_divider_ratio_switch(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk_in", "div_out"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/clk_in/div_out"

    times = [r["time"] for r in rows]
    in_edges = rising_edges([r["clk_in"] for r in rows], times)
    out_edges = rising_edges([r["div_out"] for r in rows], times)
    if len(in_edges) < 40 or len(out_edges) < 10:
        return False, f"not_enough_edges in={len(in_edges)} out={len(out_edges)}"

    windows = [
        (10e-9, 90e-9, 4, "pre_div4"),
        (120e-9, 190e-9, 5, "mid_div5"),
        (220e-9, 300e-9, 4, "post_div4"),
    ]
    details: list[str] = []
    for t0, t1, expected_ratio, label in windows:
        win_in = [t for t in in_edges if t0 <= t <= t1]
        win_out = [t for t in out_edges if t0 <= t <= t1]
        if len(win_in) < expected_ratio * 2 or len(win_out) < 2:
            return False, f"{label}_insufficient_edges in={len(win_in)} out={len(win_out)}"
        measured_ratio = len(win_in) / max(len(win_out), 1)
        details.append(f"{label}={measured_ratio:.2f}")
        if abs(measured_ratio - expected_ratio) > 0.35:
            return False, ";".join(details)
    return True, ";".join(details)


def check_bbpd(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "data", "clk", "retimed_data", "up", "down"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/data/clk/retimed_data/up/down"

    vth = 0.45
    data_edges = [
        i
        for i in range(1, len(rows))
        if rows[i - 1]["data"] < vth <= rows[i]["data"] or rows[i - 1]["data"] > vth >= rows[i]["data"]
    ]
    up_edges = [i for i in range(1, len(rows)) if rows[i - 1]["up"] < vth <= rows[i]["up"]]
    down_edges = [i for i in range(1, len(rows)) if rows[i - 1]["down"] < vth <= rows[i]["down"]]

    if len(data_edges) < 6:
        return False, "not enough data edges"

    overlap = sum(1 for r in rows if r["up"] > vth and r["down"] > vth)
    overlap_frac = overlap / max(len(rows), 1)

    edge_trigger_ok = len(up_edges) + len(down_edges) >= max(4, len(data_edges) // 4)
    pulse_presence_ok = len(up_edges) >= 2 and len(down_edges) >= 2
    non_overlap_ok = overlap_frac < 0.02

    directional_counts = {
        "up_expected": 0,
        "down_expected": 0,
        "up_correct": 0,
        "down_correct": 0,
        "wrong": 0,
        "missing": 0,
    }
    response_window_s = 0.2e-9
    for edge_idx in data_edges:
        clk_high = rows[edge_idx]["clk"] > vth
        retimed_high = rows[edge_idx]["retimed_data"] > vth
        if clk_high and not retimed_high:
            expected = "up"
        elif not clk_high and retimed_high:
            expected = "down"
        else:
            continue

        directional_counts[f"{expected}_expected"] += 1
        wrong = "down" if expected == "up" else "up"
        edge_time = rows[edge_idx]["time"]
        window_rows = []
        for row in rows[edge_idx:]:
            if row["time"] > edge_time + response_window_s:
                break
            window_rows.append(row)
        expected_hit = any(row[expected] > vth for row in window_rows)
        wrong_hit = any(row[wrong] > vth for row in window_rows)
        if expected_hit and not wrong_hit:
            directional_counts[f"{expected}_correct"] += 1
        elif wrong_hit:
            directional_counts["wrong"] += 1
        else:
            directional_counts["missing"] += 1

    directional_ok = (
        directional_counts["up_expected"] >= 2
        and directional_counts["down_expected"] >= 2
        and directional_counts["up_correct"] >= max(2, int(0.75 * directional_counts["up_expected"]))
        and directional_counts["down_correct"] >= max(2, int(0.75 * directional_counts["down_expected"]))
        and directional_counts["wrong"] == 0
    )
    ok = edge_trigger_ok and pulse_presence_ok and non_overlap_ok and directional_ok
    return ok, (
        f"data_edges={len(data_edges)} up_edges={len(up_edges)} down_edges={len(down_edges)} "
        f"overlap_frac={overlap_frac:.4f} "
        f"direction_up={directional_counts['up_correct']}/{directional_counts['up_expected']} "
        f"direction_down={directional_counts['down_correct']}/{directional_counts['down_expected']} "
        f"wrong_direction={directional_counts['wrong']} missing_direction={directional_counts['missing']}"
    )


def check_bbpd_data_edge_alignment(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"clk", "data", "up", "dn"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing clk/data/up/dn"

    vth = 0.45
    times = [r["time"] for r in rows]
    up = [r["up"] for r in rows]
    dn = [r["dn"] for r in rows]
    data = [r["data"] for r in rows]

    up_edges = [times[i] for i in range(1, len(rows)) if up[i - 1] <= vth < up[i]]
    dn_edges = [times[i] for i in range(1, len(rows)) if dn[i - 1] <= vth < dn[i]]
    data_edges = [
        times[i]
        for i in range(1, len(rows))
        if ((data[i - 1] <= vth < data[i]) or (data[i - 1] >= vth > data[i]))
    ]

    if len(data_edges) < 6:
        return False, f"too_few_data_edges={len(data_edges)}"
    if len(up_edges) + len(dn_edges) < 6:
        return False, f"too_few_updn_pulses={len(up_edges) + len(dn_edges)}"

    overlap = sum(1 for r in rows if r["up"] > vth and r["dn"] > vth)
    overlap_frac = overlap / max(len(rows), 1)
    if overlap_frac > 0.02:
        return False, f"overlap_frac={overlap_frac:.4f}"

    lead_window_end = 80e-9
    lag_window_start = 90e-9
    up_lead = sum(1 for t in up_edges if t <= lead_window_end)
    dn_lead = sum(1 for t in dn_edges if t <= lead_window_end)
    up_lag = sum(1 for t in up_edges if t >= lag_window_start)
    dn_lag = sum(1 for t in dn_edges if t >= lag_window_start)

    if up_lead < 3 or up_lead <= dn_lead:
        return False, f"lead_window_updn={up_lead}/{dn_lead}"
    if dn_lag < 3 or dn_lag <= up_lag:
        return False, f"lag_window_updn={up_lag}/{dn_lag}"

    return True, (
        f"data_edges={len(data_edges)} "
        f"lead_updn={up_lead}/{dn_lead} "
        f"lag_updn={up_lag}/{dn_lag} "
        f"overlap_frac={overlap_frac:.4f}"
    )


def _find_bus_columns(sample: dict[str, float], base: str) -> dict[int, str]:
    cols: dict[int, str] = {}
    pattern = re.compile(rf"^{re.escape(base)}(?:_|\[)?(\d+)\]?$", re.IGNORECASE)
    for name in sample:
        m = pattern.match(name)
        if m:
            cols[int(m.group(1))] = name
    return cols


def _pick_column(sample: dict[str, float], candidates: list[str]) -> str | None:
    lower_map = {k.lower(): k for k in sample.keys()}
    for name in candidates:
        if name in sample:
            return name
        if name.lower() in lower_map:
            return lower_map[name.lower()]
    return None


def check_bad_bus_output_loop(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "empty tran.csv"

    sample = rows[0]
    code_cols = _find_bus_columns(sample, "CODE")
    dout_cols = _find_bus_columns(sample, "DOUT")
    bit_indices = [idx for idx in range(4) if idx in code_cols and idx in dout_cols]

    if len(bit_indices) != 4:
        return False, "missing CODE_*/DOUT_* bit columns"

    mismatch = 0
    total = 0
    code_patterns = set()
    dout_patterns = set()
    uniform_rows = 0
    stable_rows = 0
    prev_code_tuple = None
    settle_until = float("-inf")
    settle_s = 0.1e-9

    for row in rows:
        code_vec = []
        dout_vec = []
        for idx in bit_indices:
            code_bit = 1 if row[code_cols[idx]] > 0.45 else 0
            dout_bit = 1 if row[dout_cols[idx]] > 0.45 else 0
            code_vec.append(code_bit)
            dout_vec.append(dout_bit)
        code_tuple = tuple(code_vec)
        dout_tuple = tuple(dout_vec)
        t = row.get("time", 0.0)
        if prev_code_tuple is not None and code_tuple != prev_code_tuple:
            settle_until = max(settle_until, t + settle_s)
        prev_code_tuple = code_tuple

        code_patterns.add(code_tuple)
        dout_patterns.add(dout_tuple)
        if len(set(dout_tuple)) == 1:
            uniform_rows += 1
        if t <= settle_until:
            continue
        stable_rows += 1
        for code_bit, dout_bit in zip(code_tuple, dout_tuple):
            total += 1
            if code_bit != dout_bit:
                mismatch += 1

    mismatch_frac = mismatch / max(total, 1)
    uniform_frac = uniform_rows / max(len(rows), 1)
    ok = (
        mismatch_frac < 0.05
        and len(code_patterns) >= 6
        and len(dout_patterns) >= 6
        and uniform_frac < 0.8
        and stable_rows >= 20
    )
    return ok, (
        f"mismatch_frac={mismatch_frac:.4f} code_patterns={len(code_patterns)} "
        f"dout_patterns={len(dout_patterns)} uniform_frac={uniform_frac:.3f} "
        f"stable_rows={stable_rows}"
    )


def check_missing_transition_outputs(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "empty tran.csv"

    sample = rows[0]
    vin_col = _pick_column(sample, ["VIN", "vin", "vin_i"])
    flag_col = _pick_column(sample, ["FLAG", "flag", "flag_o", "out_p", "out"])
    if vin_col is None or flag_col is None:
        return False, "missing VIN/FLAG columns"

    vins = [r[vin_col] for r in rows]
    flags = [r[flag_col] for r in rows]
    vmin = min(vins)
    vmax = max(vins)
    if vmax - vmin < 0.2:
        return False, "VIN does not cross threshold range"

    threshold = 0.5 * (vmax + vmin)
    margin = max(0.05 * (vmax - vmin), 0.03)
    crossing_times = [
        rows[i]["time"]
        for i in range(1, len(rows))
        if (vins[i - 1] - threshold) * (vins[i] - threshold) <= 0 and vins[i - 1] != vins[i]
    ]
    settle_s = 0.5e-9
    stable_indices = [
        i
        for i, vin in enumerate(vins)
        if abs(vin - threshold) > margin
        and all(abs(rows[i]["time"] - t_cross) > settle_s for t_cross in crossing_times)
    ]
    if len(stable_indices) < max(10, len(rows) // 4):
        return False, "insufficient stable samples away from threshold"

    mismatch = 0
    for idx in stable_indices:
        expected = vins[idx] > threshold
        observed = flags[idx] > 0.45
        if expected != observed:
            mismatch += 1

    mismatch_frac = mismatch / len(stable_indices)
    flag_span = max(flags) - min(flags)
    high_seen = any(flags[idx] > 0.45 for idx in stable_indices)
    low_seen = any(flags[idx] <= 0.45 for idx in stable_indices)
    ok = mismatch_frac < 0.08 and flag_span > 0.4 and high_seen and low_seen
    return ok, f"mismatch_frac={mismatch_frac:.4f} flag_span={flag_span:.3f} stable_samples={len(stable_indices)}"


def check_dwa_ptr_gen(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "no rows"
    keys = set(rows[0].keys())
    # Accept either bus-integer format (ptr_code/cell_en_code) or individual bits (ptr_0..ptr_15)
    use_codes = {"clk_i", "rst_ni", "cell_en_code", "ptr_code"}.issubset(keys)
    use_bits  = {"clk_i", "rst_ni", "ptr_0", "cell_en_0"}.issubset(keys)
    if not use_codes and not use_bits:
        return False, "missing required columns (need ptr_code/cell_en_code or ptr_0..15/cell_en_0..15)"
    post = [r for r in rows if r["rst_ni"] > 0.45]
    if not post:
        return False, "no post-reset samples"
    if use_codes:
        ptr_codes  = [int(round(r["ptr_code"])) for r in post]
        cell_codes = [int(round(r["cell_en_code"])) for r in post]
    else:
        # Reconstruct integer codes from individual bit columns
        ptr_bits  = [k for k in keys if k.startswith("ptr_") and k[4:].isdigit()]
        cell_bits = [k for k in keys if k.startswith("cell_en_") and k[8:].isdigit()]
        ptr_codes  = [sum(int(r[b] > 0.45) << int(b[4:])  for b in ptr_bits)  for r in post]
        cell_codes = [sum(int(r[b] > 0.45) << int(b[8:]) for b in cell_bits) for r in post]
    ptr_nonzero = all(v > 0 for v in ptr_codes)
    ptr_unique = len(set(ptr_codes))
    cell_active = max(cell_codes) > 0
    ok = ptr_nonzero and cell_active and ptr_unique >= 4
    return ok, f"ptr_unique={ptr_unique} max_cell_code={max(cell_codes)}"


def check_dwa_ptr_gen_no_overlap(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "no rows"

    keys = set(rows[0].keys())
    required = {"time", "clk_i", "rst_ni", "ptr_0", "cell_en_0"}
    if not required.issubset(keys):
        return False, "missing time/clk_i/rst_ni/ptr_0/cell_en_0"

    ptr_cols = indexed_columns(keys, "ptr_")
    cell_cols = indexed_columns(keys, "cell_en_")
    if not ptr_cols or not cell_cols:
        return False, "missing ptr_* or cell_en_* columns"

    times = [r["time"] for r in rows]
    clk_vals = [r["clk_i"] for r in rows]
    rst_vals = [r["rst_ni"] for r in rows]
    edge_times = rising_edges(clk_vals, times)
    if not edge_times:
        return False, "no_clock_edges"

    sample_times = [edge_t + 1.0e-9 for edge_t in edge_times]
    sampled_rows = sample_rows_at_or_after_times(rows, sample_times, rst_key="rst_ni")

    if len(sampled_rows) < 2:
        return False, f"insufficient_post_reset_samples count={len(sampled_rows)}"

    bad_ptr_rows = 0
    cell_counts: list[int] = []
    overlap_count = 0
    prev_active: set[int] | None = None

    for row in sampled_rows:
        ptr_active = {idx for idx, col in enumerate(ptr_cols) if row[col] > 0.45}
        if len(ptr_active) not in (0, 1):
            bad_ptr_rows += 1

        active_cells = {idx for idx, col in enumerate(cell_cols) if row[col] > 0.45}
        cell_counts.append(len(active_cells))

        if prev_active is not None and prev_active & active_cells:
            overlap_count += 1
        prev_active = active_cells

    cell_active = max(cell_counts) > 0
    ok = bad_ptr_rows == 0 and cell_active and overlap_count == 0
    return ok, (
        f"sampled_cycles={len(sampled_rows)} bad_ptr_rows={bad_ptr_rows} "
        f"max_active_cells={max(cell_counts)} overlap_count={overlap_count}"
    )


def check_dwa_wraparound(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "no rows"

    keys = set(rows[0].keys())
    required = {"time", "clk_i", "rst_ni", "ptr_0", "cell_en_0", "code_0"}
    if not required.issubset(keys):
        return False, "missing time/clk_i/rst_ni/ptr_0/cell_en_0/code_0"

    ptr_cols = indexed_columns(keys, "ptr_")
    cell_cols = indexed_columns(keys, "cell_en_")
    code_cols = indexed_columns(keys, "code_")
    if len(ptr_cols) != 16 or len(cell_cols) != 16 or len(code_cols) != 4:
        return False, "expected ptr_0..15, cell_en_0..15, and code_0..3 columns"

    times = [r["time"] for r in rows]
    edge_times = rising_edges([r["clk_i"] for r in rows], times)
    sample_times = [edge_t + 1.0e-9 for edge_t in edge_times]
    sampled_rows = sample_rows_at_or_after_times(rows, sample_times, rst_key="rst_ni")

    if len(sampled_rows) < 5:
        return False, f"insufficient_post_reset_samples count={len(sampled_rows)}"

    expected_ptr = 13
    bad_ptr_rows = 0
    bad_count_rows = 0
    wrap_events = 0
    split_wrap_rows = 0
    prev_ptr = expected_ptr

    for row in sampled_rows:
        code = sum(int(row[col] > 0.45) << int(col[5:]) for col in code_cols)
        expected_ptr = (expected_ptr + code) % 16
        if expected_ptr < prev_ptr:
            wrap_events += 1

        ptr_active = [idx for idx, col in enumerate(ptr_cols) if row[col] > 0.45]
        active_cells = {idx for idx, col in enumerate(cell_cols) if row[col] > 0.45}

        if ptr_active != [expected_ptr]:
            bad_ptr_rows += 1
        if len(active_cells) != code:
            bad_count_rows += 1
        if active_cells and (max(active_cells) - min(active_cells) + 1) > len(active_cells):
            split_wrap_rows += 1

        prev_ptr = expected_ptr

    ok = bad_ptr_rows == 0 and bad_count_rows == 0 and wrap_events >= 2 and split_wrap_rows >= 2
    return ok, (
        f"sampled_cycles={len(sampled_rows)} bad_ptr_rows={bad_ptr_rows} "
        f"bad_count_rows={bad_count_rows} wrap_events={wrap_events} "
        f"split_wrap_rows={split_wrap_rows}"
    )


def check_dwa_dem_encoder_release(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "no rows"

    keys = set(rows[0].keys())
    required = {"time", "clk_i", "rst_ni", "ptr_0", "cell_en_0", "code_0"}
    if not required.issubset(keys):
        return False, "missing time/clk_i/rst_ni/ptr_0/cell_en_0/code_0"

    ptr_cols = indexed_columns(keys, "ptr_")
    cell_cols = indexed_columns(keys, "cell_en_")
    code_cols = indexed_columns(keys, "code_")
    if len(ptr_cols) != 16 or len(cell_cols) != 16 or len(code_cols) != 4:
        return False, "expected ptr_0..15, cell_en_0..15, and code_0..3 columns"

    times = [r["time"] for r in rows]
    edge_times = rising_edges([r["clk_i"] for r in rows], times)
    sampled_rows = sample_rows_at_or_after_times(rows, [t + 1.0e-9 for t in edge_times], rst_key="rst_ni")
    if len(sampled_rows) < 5:
        return False, f"insufficient_post_reset_samples count={len(sampled_rows)}"

    ptr = 0
    previous_code: int | None = None
    bad_ptr_rows = 0
    bad_span_rows = 0
    wrap_events = 0
    split_wrap_rows = 0
    active_counts: list[int] = []
    ptr_sequence: list[int] = []

    for row_idx, row in enumerate(sampled_rows):
        row_code = sum(int(row[col] > 0.45) << int(col[5:]) for col in code_cols)
        effective_code = row_code if previous_code is None else previous_code
        prev_ptr = ptr
        ptr = (ptr + effective_code) % 16
        if row_idx > 0 and ptr < prev_ptr:
            wrap_events += 1

        ptr_active = [idx for idx, col in enumerate(ptr_cols) if row[col] > 0.45]
        if ptr_active != [ptr]:
            bad_ptr_rows += 1

        # The release gold emits an MSB span plus the LSB boundary unit, so a
        # code of N drives a contiguous circular run of N+1 active cells ending
        # at the pointer.
        expected_cells = {(ptr - offset) % 16 for offset in range(effective_code + 1)}
        active_cells = {idx for idx, col in enumerate(cell_cols) if row[col] > 0.45}
        active_counts.append(len(active_cells))
        if active_cells != expected_cells:
            bad_span_rows += 1
        if active_cells and (max(active_cells) - min(active_cells) + 1) > len(active_cells):
            split_wrap_rows += 1

        ptr_sequence.append(ptr)
        previous_code = row_code

    ok = (
        bad_ptr_rows == 0
        and bad_span_rows == 0
        and wrap_events >= 2
        and split_wrap_rows >= 2
        and len(set(ptr_sequence)) >= 5
        and max(active_counts) >= 8
    )
    return ok, (
        f"sampled_cycles={len(sampled_rows)} bad_ptr_rows={bad_ptr_rows} "
        f"bad_span_rows={bad_span_rows} ptr_unique={len(set(ptr_sequence))} "
        f"wrap_events={wrap_events} split_wrap_rows={split_wrap_rows} "
        f"max_active_cells={max(active_counts)}"
    )


def check_clk_burst_gen(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows or not {"CLK", "RST_N", "CLK_OUT"}.issubset(rows[0]):
        return False, "missing CLK/RST_N/CLK_OUT"
    vth = 0.45
    post = [r for r in rows if r["RST_N"] > 0.45]
    if len(post) < 4:
        return False, "no post-reset samples"

    times = [r["time"] for r in post]
    clk = [r["CLK"] for r in post]
    edge_idx = [i for i in range(1, len(post)) if clk[i - 1] < vth <= clk[i]]
    if len(edge_idx) < 16:
        return False, f"too_few_post_reset_clk_edges={len(edge_idx)}"

    periods = [times[edge_idx[i + 1]] - times[edge_idx[i]] for i in range(len(edge_idx) - 1)]
    positive_periods = sorted(period for period in periods if period > 0)
    if not positive_periods:
        return False, "cannot_estimate_clk_period"
    period = positive_periods[len(positive_periods) // 2]

    def sample_at_or_after(target_t: float, limit_t: float | None = None) -> dict[str, float] | None:
        for row in post:
            t = row["time"]
            if t >= target_t and (limit_t is None or t < limit_t):
                return row
        return None

    high_phase_failures = 0
    low_phase_failures = 0
    checked_cycles = 0
    enabled_cycles = 0
    disabled_cycles = 0

    # Contract for the release task/testbench: div=8, pass cycles 0 and 1,
    # suppress cycles 2..7, then repeat. Sample away from transitions so the
    # checker is not sensitive to simulator breakpoint placement.
    for cycle_idx, edge in enumerate(edge_idx[:-1]):
        edge_t = times[edge]
        next_edge_t = times[edge_idx[cycle_idx + 1]]
        frame_pos = cycle_idx % 8
        should_pass = frame_pos < 2

        high_sample = sample_at_or_after(edge_t + 0.25 * period, next_edge_t)
        low_sample = sample_at_or_after(edge_t + 0.75 * period, next_edge_t)
        if high_sample is None or low_sample is None:
            continue

        checked_cycles += 1
        if should_pass:
            enabled_cycles += 1
            if high_sample["CLK_OUT"] <= vth:
                high_phase_failures += 1
        else:
            disabled_cycles += 1
            if high_sample["CLK_OUT"] > vth:
                high_phase_failures += 1
        if low_sample["CLK_OUT"] > vth:
            low_phase_failures += 1

    ok = (
        checked_cycles >= 16
        and enabled_cycles >= 4
        and disabled_cycles >= 8
        and high_phase_failures == 0
        and low_phase_failures == 0
    )
    return ok, (
        f"burst_cycles_checked={checked_cycles} enabled_cycles={enabled_cycles} "
        f"disabled_cycles={disabled_cycles} high_phase_failures={high_phase_failures} "
        f"low_phase_failures={low_phase_failures}"
    )


def check_noise_gen(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows or not {"vin_i", "vout_o"}.issubset(rows[0]):
        return False, "missing vin_i/vout_o"
    noises = [r["vout_o"] - r["vin_i"] for r in rows]
    mean = sum(noises) / len(noises)
    var = sum((x - mean) ** 2 for x in noises) / len(noises)
    std = var ** 0.5
    ok = std > 0.01 and max(abs(x) for x in noises) > 0.05
    return ok, f"noise_std={std:.4f}"


def check_gain_extraction(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows or not {"vinp", "vinn", "vamp_p", "vamp_n"}.issubset(rows[0]):
        return False, "missing vinp/vinn/vamp_p/vamp_n"
    vin_diff = [r["vinp"] - r["vinn"] for r in rows]
    vamp_diff = [r["vamp_p"] - r["vamp_n"] for r in rows]
    mean_in = sum(vin_diff) / len(vin_diff)
    mean_out = sum(vamp_diff) / len(vamp_diff)
    std_in = (sum((x - mean_in) ** 2 for x in vin_diff) / len(vin_diff)) ** 0.5
    std_out = (sum((x - mean_out) ** 2 for x in vamp_diff) / len(vamp_diff)) ** 0.5
    gain = std_out / std_in if std_in > 1e-12 else 0.0
    ok = gain > 4.0 and std_out > std_in
    return ok, f"diff_gain={gain:.2f}"


def check_adpll_lock(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"ref_clk", "fb_clk", "lock", "vctrl_mon"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing ref_clk/fb_clk/lock/vctrl_mon"

    times = [r["time"] for r in rows]
    ref_edges = rising_edges([r["ref_clk"] for r in rows], times)
    fb_edges = rising_edges([r["fb_clk"] for r in rows], times)
    lock_edges = rising_edges([r["lock"] for r in rows], times)

    if len(ref_edges) < 8 or len(fb_edges) < 8:
        return False, f"not_enough_edges ref={len(ref_edges)} fb={len(fb_edges)}"

    t_end = times[-1]
    t_start = t_end * 0.8
    ref_late = [t for t in ref_edges if t_start <= t <= t_end]
    fb_late = [t for t in fb_edges if t_start <= t <= t_end]
    if not ref_late or not fb_late:
        return False, "missing late-window edges"

    ratio = len(fb_late) / max(len(ref_late), 1)
    lock_ok = bool(lock_edges) and lock_edges[0] <= 1.0e-6
    vctrl_vals = [r["vctrl_mon"] for r in rows]
    vctrl_in_range = all(-1e-6 <= v <= 1.2 for v in vctrl_vals)
    freq_ok = 0.95 <= ratio <= 1.05
    ok = freq_ok and lock_ok and vctrl_in_range
    return ok, (
        f"late_edge_ratio={ratio:.3f} "
        f"lock_time={(lock_edges[0] if lock_edges else float('nan')):.3e} "
        f"vctrl_range_ok={vctrl_in_range}"
    )


def edge_frequency_ratio(
    rows: list[dict[str, float]],
    num_signal: str,
    den_signal: str,
    t_start: float,
    t_end: float,
) -> tuple[float, str]:
    window = time_window(rows, t_start, t_end)
    if len(window) < 4 or num_signal not in window[0] or den_signal not in window[0]:
        return float("nan"), "missing_window_or_signals"

    times = [r["time"] for r in window]
    num_edges = rising_edges([r[num_signal] for r in window], times)
    den_edges = rising_edges([r[den_signal] for r in window], times)
    if len(num_edges) < 3 or len(den_edges) < 3:
        return float("nan"), f"not_enough_edges num={len(num_edges)} den={len(den_edges)}"

    num_freq = (len(num_edges) - 1) / max(num_edges[-1] - num_edges[0], 1e-18)
    den_freq = (len(den_edges) - 1) / max(den_edges[-1] - den_edges[0], 1e-18)
    return num_freq / max(den_freq, 1e-18), "ok"


def first_threshold_crossing(rows: list[dict[str, float]], signal: str, threshold: float) -> float:
    if not rows or signal not in rows[0]:
        return float("nan")
    prev = rows[0][signal]
    for row in rows[1:]:
        cur = row[signal]
        if prev < threshold <= cur:
            return row["time"]
        prev = cur
    return float("nan")


def check_adpll_ratio_hop(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"ref_clk", "vout", "lock", "vctrl_mon", "ratio_ctrl"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing ref_clk/vout/lock/vctrl_mon/ratio_ctrl"

    hop_t = first_threshold_crossing(rows, "ratio_ctrl", 5.0)
    if not math.isfinite(hop_t):
        return False, "ratio_hop_not_detected"

    pre_ratio, pre_note = edge_frequency_ratio(rows, "vout", "ref_clk", hop_t - 1.0e-6, hop_t - 2.0e-7)
    post_ratio, post_note = edge_frequency_ratio(rows, "vout", "ref_clk", hop_t + 1.2e-6, hop_t + 2.5e-6)
    if pre_note != "ok":
        return False, f"pre_window_{pre_note}"
    if post_note != "ok":
        return False, f"post_window_{post_note}"

    vth = max(r["lock"] for r in rows) * 0.5 if rows else 0.45
    pre_lock = weighted_logic_high_fraction_window(rows, "lock", vth, hop_t - 4.0e-7, hop_t - 5.0e-8)
    post_lock = weighted_logic_high_fraction_window(rows, "lock", vth, hop_t + 1.8e-6, hop_t + 2.8e-6)
    vctrl_vals = [r["vctrl_mon"] for r in rows]
    vctrl_in_range = all(-1e-6 <= v <= 1.2 for v in vctrl_vals)

    ok = (
        abs(pre_ratio - 4.0) <= 0.25
        and abs(post_ratio - 6.0) <= 0.35
        and pre_lock >= 0.8
        and post_lock >= 0.8
        and vctrl_in_range
    )
    return ok, (
        f"hop_t={hop_t:.3e} "
        f"pre_ratio={pre_ratio:.3f} "
        f"post_ratio={post_ratio:.3f} "
        f"pre_lock={pre_lock:.3f} "
        f"post_lock={post_lock:.3f} "
        f"vctrl_range_ok={vctrl_in_range}"
    )


def check_cppll_tracking(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"ref_clk", "fb_clk", "lock", "vctrl_mon"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing ref_clk/fb_clk/lock/vctrl_mon"

    times = [r["time"] for r in rows]
    ref_edges = rising_edges([r["ref_clk"] for r in rows], times)
    fb_edges = rising_edges([r["fb_clk"] for r in rows], times)
    lock_edges = rising_edges([r["lock"] for r in rows], times)

    if len(ref_edges) < 8 or len(fb_edges) < 8:
        return False, f"not_enough_edges ref={len(ref_edges)} fb={len(fb_edges)}"

    t_end = times[-1]
    t_start = t_end * 0.8
    ref_late = [t for t in ref_edges if t_start <= t <= t_end]
    fb_late = [t for t in fb_edges if t_start <= t <= t_end]
    if len(ref_late) < 4 or len(fb_late) < 4:
        return False, "not_enough_late_edges"

    ref_periods = [b - a for a, b in zip(ref_late, ref_late[1:])]
    fb_periods = [b - a for a, b in zip(fb_late, fb_late[1:])]
    ref_period = sum(ref_periods) / len(ref_periods)
    fb_period = sum(fb_periods) / len(fb_periods)
    if ref_period <= 0.0 or fb_period <= 0.0:
        return False, "non_positive_period"

    freq_ratio = ref_period / fb_period
    fb_jitter = max(fb_periods) - min(fb_periods)
    fb_jitter_frac = fb_jitter / fb_period if fb_period > 0.0 else float("inf")
    vctrl_vals = [r["vctrl_mon"] for r in rows]
    vctrl_min = min(vctrl_vals)
    vctrl_max = max(vctrl_vals)
    vctrl_in_range = all(-1e-6 <= v <= 0.95 for v in vctrl_vals)
    lock_vmax = max(r["lock"] for r in rows)
    lock_vth = max(0.45, lock_vmax * 0.5)
    late_lock_frac = weighted_logic_high_fraction_window(rows, "lock", lock_vth, t_start, t_end)
    freq_ok = 0.97 <= freq_ratio <= 1.03
    stability_ok = fb_jitter_frac <= 0.10
    late_lock_ok = late_lock_frac >= 0.75
    ok = freq_ok and stability_ok and late_lock_ok and vctrl_in_range
    return ok, (
        f"freq_ratio={freq_ratio:.4f} "
        f"fb_jitter_frac={fb_jitter_frac:.4f} "
        f"late_lock_frac={late_lock_frac:.3f} "
        f"lock_time={(lock_edges[0] if lock_edges else float('nan')):.3e} "
        f"vctrl_min={vctrl_min:.3f} "
        f"vctrl_max={vctrl_max:.3f}"
    )


def check_sample_hold(rows: list[dict[str, float]]) -> tuple[bool, str]:
    """S&H: output steps at clock edges, held between them."""
    if not rows or not {"in", "clk", "out"}.issubset(rows[0]):
        return False, "missing in/clk/out columns"
    vth = 0.45
    times = [r["time"] for r in rows]
    clk  = [r["clk"]  for r in rows]
    vin  = [r["in"]   for r in rows]
    vout = [r["out"]  for r in rows]
    edge_idx = [i for i in range(1, len(clk)) if clk[i - 1] <= vth < clk[i]]
    if len(edge_idx) < 10:
        return False, f"too_few_clock_edges={len(edge_idx)}"
    # Check hold stability: for 3 consecutive hold windows, skip 2ns after edge, stop 2ns before next
    for i in range(min(3, len(edge_idx) - 1)):
        t_start = times[edge_idx[i]] + 2e-9
        t_end   = times[edge_idx[i + 1]] - 2e-9
        window = [vout[j] for j in range(edge_idx[i], edge_idx[i + 1])
                  if t_start <= times[j] <= t_end]
        if len(window) < 2:
            continue
        jitter = max(window) - min(window)
        if jitter > 0.02:
            return False, f"output_not_held jitter={jitter:.4f}V"
    # Output should track input at edges (settled 2ns after edge)
    mismatches = 0
    for idx in edge_idx[:20]:
        t_settle = times[idx] + 2e-9
        settle_idx = next((j for j in range(idx, len(times)) if times[j] >= t_settle), idx)
        if abs(vout[settle_idx] - vin[idx]) > 0.015:
            mismatches += 1
    if mismatches > 4:
        return False, f"sample_mismatch={mismatches}/20"
    return True, f"edges={len(edge_idx)} hold_ok"


def check_sample_hold_droop(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"vin", "clk", "vout"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing vin/clk/vout"

    vth = 0.45
    times = [r["time"] for r in rows]
    clk = [r["clk"] for r in rows]
    vin = [r["vin"] for r in rows]
    vout = [r["vout"] for r in rows]
    edge_idx = [i for i in range(1, len(clk)) if clk[i - 1] <= vth < clk[i]]

    if len(edge_idx) < 6:
        return False, f"too_few_clock_edges={len(edge_idx)}"

    sample_mismatch = 0
    checked_samples = 0
    for i in range(min(6, len(edge_idx) - 1)):
        idx = edge_idx[i]
        t_target = times[idx] + 1.2e-9
        settle_idx = next((j for j in range(idx, len(rows)) if times[j] >= t_target), len(rows) - 1)
        err = abs(vout[settle_idx] - vin[idx])
        checked_samples += 1
        if err > 0.04:
            sample_mismatch += 1
    if checked_samples == 0 or sample_mismatch > 1:
        return False, f"sample_mismatch={sample_mismatch}/{max(checked_samples, 1)}"

    droop_windows = 0
    droop_failures = 0
    for i in range(min(6, len(edge_idx) - 1)):
        start_i = edge_idx[i]
        end_i = edge_idx[i + 1]
        t_start = times[start_i] + 1.5e-9
        t_end = times[end_i] - 1.5e-9
        idxs = [j for j in range(start_i, end_i) if t_start <= times[j] <= t_end]
        if len(idxs) < 6:
            continue
        first = vout[idxs[0]]
        if first < 0.55:
            continue
        last = vout[idxs[-1]]
        droop = first - last
        upward_steps = sum(1 for a, b in zip(idxs[:-1], idxs[1:]) if (vout[b] - vout[a]) > 0.004)
        droop_windows += 1
        if droop < 0.006 or droop > 0.30:
            droop_failures += 1
        if upward_steps > max(1, len(idxs) // 8):
            droop_failures += 1

    if droop_windows < 2:
        return False, f"insufficient_high_hold_windows={droop_windows}"
    if droop_failures > 0:
        return False, f"droop_failures={droop_failures} windows={droop_windows}"

    return True, (
        f"edges={len(edge_idx)} "
        f"sample_mismatch={sample_mismatch}/{checked_samples} "
        f"droop_windows={droop_windows}"
    )


def check_release_vin_sampled_droop_hold(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "sample", "rst", "vin", "vout"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/sample/rst/vin/vout"

    times = [r["time"] for r in rows]
    sample_edges = _threshold_crossings([r["sample"] for r in rows], times, threshold=0.45, direction="rising")
    if len(sample_edges) < 3:
        return False, f"too_few_sample_edges={len(sample_edges)}"

    expected: list[float] = []
    observed: list[float] = []
    errors: list[float] = []
    for edge_t in sample_edges[:3]:
        want = sample_signal_at(rows, "vin", edge_t + 0.05e-9)
        got = sample_signal_at(rows, "vout", edge_t + 1.20e-9)
        if want is None or got is None:
            return False, f"missing_sample_window_at={edge_t:.3e}"
        expected.append(want)
        observed.append(got)
        errors.append(abs(got - want))

    max_err = max(errors)
    expected_span = max(expected) - min(expected)
    observed_span = max(observed) - min(observed)
    sample_match = max_err <= 0.045 and expected_span >= 0.35 and observed_span >= 0.30

    # Use the high second sample as the droop window; reset begins well after it.
    second_edge = sample_edges[1]
    droop_start_t = second_edge + 2.0e-9
    reset_edges = _threshold_crossings([r["rst"] for r in rows], times, threshold=0.45, direction="rising")
    droop_end_t = (reset_edges[0] - 2.0e-9) if reset_edges else (second_edge + 35.0e-9)
    droop_values = [r["vout"] for r in rows if droop_start_t <= r["time"] <= droop_end_t]
    if len(droop_values) < 8:
        return False, f"insufficient_droop_window_samples={len(droop_values)}"
    droop = droop_values[0] - droop_values[-1]
    upward_steps = sum(1 for a, b in zip(droop_values[:-1], droop_values[1:]) if b - a > 0.004)
    droop_ok = 0.04 <= droop <= 0.45 and upward_steps <= max(1, len(droop_values) // 10)

    reset_t = reset_edges[0] if reset_edges else 125.0e-9
    reset_sample = sample_signal_at(rows, "vout", reset_t + 8.0e-9)
    reset_clear = reset_sample is not None and reset_sample < 0.05

    ok = sample_match and droop_ok and reset_clear
    exp_text = ",".join(f"{value:.3f}" for value in expected)
    obs_text = ",".join(f"{value:.3f}" for value in observed)
    return ok, (
        f"vin_samples={exp_text} held_samples={obs_text} "
        f"max_sample_err={max_err:.3f} expected_span={expected_span:.3f} "
        f"observed_span={observed_span:.3f} droop={droop:.3f} "
        f"upward_steps={upward_steps} reset_clear={reset_clear}"
    )


def check_release_converter_front_end_chain(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin", "clk", "vout", "valid", "coarse"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/vin/clk/vout/valid/coarse"

    times = [r["time"] for r in rows]
    clk_edges = _threshold_crossings([r["clk"] for r in rows], times, threshold=0.45, direction="rising")
    if len(clk_edges) < 6:
        return False, f"too_few_clk_edges={len(clk_edges)}"

    sample_errors: list[float] = []
    coarse_mismatches = 0
    valid_hits = 0
    valid_low_hits = 0
    aperture_sensitive = 0
    for edge_t in clk_edges[:8]:
        vin_edge = sample_signal_at(rows, "vin", edge_t)
        vin_aperture = sample_signal_at(rows, "vin", edge_t + 0.20e-9)
        vout_settled = sample_signal_at(rows, "vout", edge_t + 1.00e-9)
        valid_high = sample_signal_at(rows, "valid", edge_t + 0.80e-9)
        valid_low = sample_signal_at(rows, "valid", edge_t + 3.50e-9)
        coarse = sample_signal_at(rows, "coarse", edge_t + 1.00e-9)
        if None in (vin_edge, vin_aperture, vout_settled, valid_high, valid_low, coarse):
            return False, f"missing_front_end_sample_at={edge_t:.3e}"
        assert vin_edge is not None and vin_aperture is not None and vout_settled is not None
        assert valid_high is not None and valid_low is not None and coarse is not None
        sample_errors.append(abs(vout_settled - vin_aperture))
        expected_coarse_high = vin_aperture > 0.45
        if (coarse > 0.45) != expected_coarse_high:
            coarse_mismatches += 1
        if valid_high > 0.45:
            valid_hits += 1
        if valid_low < 0.45:
            valid_low_hits += 1
        if abs(vin_aperture - vin_edge) > 0.18 and abs(vout_settled - vin_aperture) + 0.08 < abs(vout_settled - vin_edge):
            aperture_sensitive += 1

    max_sample_err = max(sample_errors)
    sample_ok = max_sample_err <= 0.055
    coarse_ok = coarse_mismatches == 0
    valid_ok = valid_hits >= 6 and valid_low_hits >= 6
    aperture_ok = aperture_sensitive >= 2

    droop_windows = 0
    droop_failures = 0
    for start_t, end_t in zip(clk_edges[:7], clk_edges[1:8]):
        t_start = start_t + 2.0e-9
        t_end = end_t - 2.0e-9
        idxs = [idx for idx, row in enumerate(rows) if t_start <= row["time"] <= t_end]
        if len(idxs) < 8:
            continue
        first = rows[idxs[0]]["vout"]
        if first < 0.55:
            continue
        last = rows[idxs[-1]]["vout"]
        droop = first - last
        upward_steps = sum(1 for a, b in zip(idxs[:-1], idxs[1:]) if rows[b]["vout"] - rows[a]["vout"] > 0.004)
        droop_windows += 1
        if not (0.004 <= droop <= 0.16) or upward_steps > max(1, len(idxs) // 8):
            droop_failures += 1

    droop_ok = droop_windows >= 2 and droop_failures == 0
    ok = sample_ok and coarse_ok and valid_ok and aperture_ok and droop_ok
    return ok, (
        f"edges={len(clk_edges)} max_sample_err={max_sample_err:.3f} "
        f"coarse_mismatches={coarse_mismatches} valid_high_hits={valid_hits} "
        f"valid_low_hits={valid_low_hits} aperture_sensitive={aperture_sensitive} "
        f"droop_windows={droop_windows} droop_failures={droop_failures}"
    )


def check_flash_adc_3b(rows: list[dict[str, float]]) -> tuple[bool, str]:
    """3-bit flash ADC: all 8 codes present, monotonic with ramp input."""
    if not rows or not {"vin", "clk", "dout2", "dout1", "dout0"}.issubset(rows[0]):
        return False, "missing vin/clk/dout2/dout1/dout0"
    vth = 0.45
    clk = [r["clk"] for r in rows]
    edge_idx = [i for i in range(1, len(clk)) if clk[i - 1] <= vth < clk[i]]
    if len(edge_idx) < 20:
        return False, f"too_few_edges={len(edge_idx)}"
    codes = []
    for idx in edge_idx:
        settle = min(idx + 5, len(rows) - 1)
        c = (int(rows[settle]["dout2"] > vth) << 2 |
             int(rows[settle]["dout1"] > vth) << 1 |
             int(rows[settle]["dout0"] > vth))
        codes.append(c)
    unique = set(codes)
    if len(unique) < 8:
        return False, f"only_{len(unique)}_codes (need 8)"
    # monotonicity: fewer than 5% reversals
    reversals = sum(1 for i in range(1, len(codes)) if codes[i] < codes[i - 1] - 1)
    if reversals > len(codes) * 0.05:
        return False, f"not_monotonic reversals={reversals}"
    return True, f"codes={len(unique)}/8 reversals={reversals}"


_RELEASE_FLASH_ADC_CMP_COLS = tuple(f"cmp{idx}" for idx in range(7))
_RELEASE_FLASH_ADC_BIT_COLS = ("dout0", "dout1", "dout2")


def check_release_flash_adc_mini_array(rows: list[dict[str, float]]) -> tuple[bool, str]:
    """Release flash ADC mini-array: seven comparator decisions plus encoder."""
    required = {"time", "vin", "clk", "dout0", "dout1", "dout2", *_RELEASE_FLASH_ADC_CMP_COLS}
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0].keys())) if rows else sorted(required)
        return False, f"missing_columns={','.join(missing)}"

    vth = 0.45
    times = [r["time"] for r in rows]
    edge_times = rising_edges([r["clk"] for r in rows], times, threshold=vth)
    sample_rows = sample_rows_at_or_after_times(rows, [edge_t + 0.5e-9 for edge_t in edge_times])
    if len(sample_rows) < 8:
        return False, f"too_few_settled_samples={len(sample_rows)}"

    thresholds = [(idx + 1) * 0.9 / 8.0 for idx in range(7)]
    observed_codes: list[int] = []
    expected_codes: list[int] = []
    comparator_mismatches = 0
    thermometer_errors = 0
    encoder_mismatches = 0
    out_of_range = 0

    for row in sample_rows:
        vin = row["vin"]
        expected_cmp = [1 if vin >= threshold - 1e-6 else 0 for threshold in thresholds]
        observed_cmp = [1 if row[col] >= vth else 0 for col in _RELEASE_FLASH_ADC_CMP_COLS]
        expected_code = sum(expected_cmp)
        observed_code = (
            (1 if row["dout0"] >= vth else 0)
            | ((1 if row["dout1"] >= vth else 0) << 1)
            | ((1 if row["dout2"] >= vth else 0) << 2)
        )

        if observed_cmp != expected_cmp:
            comparator_mismatches += 1
        if any(lo < hi for lo, hi in zip(observed_cmp, observed_cmp[1:])):
            thermometer_errors += 1
        if observed_code != sum(observed_cmp):
            encoder_mismatches += 1
        if not 0 <= observed_code <= 7:
            out_of_range += 1
        observed_codes.append(observed_code)
        expected_codes.append(expected_code)

    observed_unique = sorted(set(observed_codes))
    expected_unique = sorted(set(expected_codes))
    reversals = sum(1 for prev, curr in zip(observed_codes, observed_codes[1:]) if curr < prev)
    ok = (
        observed_unique == list(range(8))
        and expected_unique == list(range(8))
        and comparator_mismatches == 0
        and thermometer_errors == 0
        and encoder_mismatches == 0
        and out_of_range == 0
        and reversals == 0
    )
    return ok, (
        f"observed_codes={','.join(str(c) for c in observed_unique)} "
        f"expected_codes={','.join(str(c) for c in expected_unique)} "
        f"comparator_mismatches={comparator_mismatches} "
        f"thermometer_errors={thermometer_errors} "
        f"encoder_mismatches={encoder_mismatches} "
        f"reversals={reversals}"
    )


def check_serializer_8b(rows: list[dict[str, float]]) -> tuple[bool, str]:
    """8-bit P2S: verify 0xA5 bit sequence MSB-first after LOAD."""
    if not rows or not {"load", "clk", "sout"}.issubset(rows[0]):
        return False, "missing load/clk/sout"
    vth = 0.45
    load = [r["load"] for r in rows]
    clk  = [r["clk"]  for r in rows]
    sout = [r["sout"] for r in rows]
    times = [r["time"] for r in rows]

    # find LOAD falling edge
    load_fall = next((i for i in range(1, len(load)) if load[i - 1] > vth > load[i]), None)
    if load_fall is None:
        return False, "LOAD never deasserted"
    expected = [1, 0, 1, 0, 0, 1, 0, 1]  # 0xA5 MSB-first
    load_fall_t = times[load_fall]

    # collect CLK rising edges strictly after LOAD falls
    edges = [
        i for i in range(max(1, load_fall), len(clk))
        if clk[i - 1] <= vth < clk[i] and times[i] > load_fall_t + 1e-15
    ]
    if len(edges) < 7:
        return False, f"only_{len(edges)}_edges_after_load"

    # Sample sout at the middle of the next CLK period (wait for transition to settle)
    # transition() with tedge=100p takes ~100ps to complete, so we need to wait longer
    # CLK period is 5ns, so middle of period is ~2.5ns after edge
    # Find sample index at ~1ns after each edge (enough time for transition)
    edge_bits = []
    for e in edges[:8]:
        edge_t = times[e]
        # Find sample index at edge_t + 1ns (waiting for transition to settle)
        target_t = edge_t + 1e-9
        sample_idx = e
        while sample_idx < len(rows) and times[sample_idx] < target_t:
            sample_idx += 1
        sample_idx = min(sample_idx, len(rows) - 1)
        bit = int(sout[sample_idx] > vth)
        edge_bits.append(bit)

    if len(edge_bits) < 8:
        return False, f"only_{len(edge_bits)}_sampled_bits"
    mismatches = sum(1 for a, b in zip(edge_bits, expected) if a != b)
    if mismatches > 1:
        return False, f"bit_mismatch expected={expected} got={edge_bits}"
    return True, f"0xA5_serialized_ok mode=edge_only mismatches={mismatches}"


def check_serializer_frame_alignment(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"clk", "frame", "sout"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing clk/frame/sout"

    vth = 0.45
    times = [r["time"] for r in rows]
    clk = [r["clk"] for r in rows]
    frame = [r["frame"] for r in rows]
    sout = [r["sout"] for r in rows]

    clk_edges = [i for i in range(1, len(rows)) if clk[i - 1] <= vth < clk[i]]
    frame_rise = [i for i in range(1, len(rows)) if frame[i - 1] <= vth < frame[i]]
    frame_fall = [i for i in range(1, len(rows)) if frame[i - 1] >= vth > frame[i]]
    if len(frame_rise) < 2:
        return False, f"frame_rises={len(frame_rise)}"
    if len(clk_edges) < 16:
        return False, f"clk_edges={len(clk_edges)}"

    # Estimate bit period from clock edge spacing.
    periods = [times[clk_edges[i]] - times[clk_edges[i - 1]] for i in range(1, min(len(clk_edges), 10))]
    periods = [p for p in periods if p > 0.0]
    if not periods:
        return False, "invalid_clk_period"
    period = sorted(periods)[len(periods) // 2]

    expected_words = [0xA5, 0x3C]
    mismatch_total = 0
    detail_parts: list[str] = []

    for frame_idx, expected_word in enumerate(expected_words):
        t_frame = times[frame_rise[frame_idx]]
        clk_edge_times = [times[idx] for idx in clk_edges]
        near = [i for i, t_edge in enumerate(clk_edge_times) if abs(t_edge - t_frame) <= 0.6 * period]
        if near:
            start_pos = min(near, key=lambda i: abs(clk_edge_times[i] - t_frame))
        else:
            start_pos = next((i for i, t_edge in enumerate(clk_edge_times) if t_edge >= t_frame), None)
            if start_pos is None:
                return False, f"frame{frame_idx}_no_clk_after_frame"
        bit_edges = clk_edge_times[start_pos:start_pos + 8]
        if len(bit_edges) < 8:
            return False, f"frame{frame_idx}_insufficient_bits={len(bit_edges)}"

        expected_bits = [((expected_word >> bit) & 1) for bit in range(7, -1, -1)]
        observed_bits: list[int] = []
        for t_edge in bit_edges:
            t_sample = t_edge + 0.8e-9
            sample_idx = next((i for i, t in enumerate(times) if t >= t_sample), len(rows) - 1)
            observed_bits.append(1 if sout[sample_idx] > vth else 0)
        mismatches = sum(1 for a, b in zip(observed_bits, expected_bits) if a != b)
        mismatch_total += mismatches
        detail_parts.append(f"w{frame_idx}_mm={mismatches}")
        if mismatches > 1:
            return False, f"frame{frame_idx}_bit_mismatch exp={expected_bits} got={observed_bits}"

    # Frame pulse width should be around one bit window.
    pulse_widths: list[float] = []
    for r_idx in frame_rise[:2]:
        fall_idx = next((f for f in frame_fall if f > r_idx), None)
        if fall_idx is None:
            return False, "frame_without_fall_edge"
        pulse_widths.append(times[fall_idx] - times[r_idx])
    if any((w < 0.2 * period or w > 1.6 * period) for w in pulse_widths):
        return False, f"frame_pulse_widths={pulse_widths}"

    return True, (
        f"frame_rises={len(frame_rise)} "
        f"period={period:.3e} "
        f"pulse_w={[round(w / period, 2) for w in pulse_widths]} "
        f"{' '.join(detail_parts)} "
        f"mismatch_total={mismatch_total}"
    )


def check_xor_pd(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows or not {"ref", "div", "pd_out"}.issubset(rows[0]):
        return False, "missing ref/div/pd_out"
    vhi = max(max(r["ref"], r["div"], r["pd_out"]) for r in rows)
    vlo = min(min(r["ref"], r["div"], r["pd_out"]) for r in rows)
    vth = vlo + 0.5 * (vhi - vlo)
    pd = [r["pd_out"] for r in rows]
    hi_frac = sum(1 for v in pd if v > vth) / len(pd)
    binary = [1 if v > vth else 0 for v in pd]
    transitions = sum(1 for i in range(1, len(binary)) if binary[i] != binary[i - 1])
    if hi_frac < 0.10:
        return False, f"pd_out_stuck_low hi_frac={hi_frac:.3f}"
    if hi_frac > 0.90:
        return False, f"pd_out_stuck_high hi_frac={hi_frac:.3f}"
    if transitions < 15:
        return False, f"too_few_transitions={transitions}"
    if not (0.30 <= hi_frac <= 0.70):
        return False, f"duty_out_of_range={hi_frac:.3f}"
    stable_margin = max(0.08, 0.20 * (vhi - vlo))
    stable_rows = [
        r
        for r in rows
        if abs(r["ref"] - vth) >= stable_margin
        and abs(r["div"] - vth) >= stable_margin
        and abs(r["pd_out"] - vth) >= stable_margin
    ]
    if len(stable_rows) < max(12, len(rows) // 4):
        return False, f"insufficient_stable_logic_samples={len(stable_rows)}"
    mismatches = sum(
        1
        for r in stable_rows
        if ((r["ref"] > vth) ^ (r["div"] > vth)) != (r["pd_out"] > vth)
    )
    mismatch_frac = mismatches / len(stable_rows)
    if mismatch_frac > 0.05:
        return False, f"xor_mismatch_frac={mismatch_frac:.3f} mismatches={mismatches} stable={len(stable_rows)}"
    return True, f"duty={hi_frac:.3f} transitions={transitions} xor_mismatch_frac={mismatch_frac:.3f}"


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


def time_window(rows: list[dict[str, float]], t_start: float, t_end: float) -> list[dict[str, float]]:
    return [r for r in rows if t_start <= r["time"] <= t_end]


def weighted_logic_high_fraction_window(
    rows: list[dict[str, float]],
    signal: str,
    threshold: float,
    t_start: float,
    t_end: float,
) -> float:
    return weighted_logic_high_fraction(time_window(rows, t_start, t_end), signal, threshold)


def check_pfd_updn(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows or not {"ref", "div", "up", "dn"}.issubset(rows[0]):
        return False, "missing ref/div/up/dn"
    vth = max(r["ref"] for r in rows) * 0.5
    up = [1 if r["up"] > vth else 0 for r in rows]
    dn = [1 if r["dn"] > vth else 0 for r in rows]
    up_frac = weighted_logic_high_fraction(rows, "up", vth)
    dn_frac = weighted_logic_high_fraction(rows, "dn", vth)
    both_hi = [a & b for a, b in zip(up, dn)]
    run_len = 0
    max_run = 0
    for b in both_hi:
        if b:
            run_len += 1
            max_run = max(max_run, run_len)
        else:
            run_len = 0
    up_pulses = sum(1 for i in range(1, len(up)) if up[i - 1] == 0 and up[i] == 1)
    if max_run > 5:
        return False, f"overlap_too_long={max_run}"
    if up_frac < 0.01:
        return False, f"up_never_high up_frac={up_frac:.3f}"
    if up_frac < dn_frac:
        return False, f"up_frac_lt_dn_frac up={up_frac:.3f} dn={dn_frac:.3f}"
    if up_pulses < 10:
        return False, f"too_few_up_pulses={up_pulses}"
    return True, f"up_frac={up_frac:.3f} dn_frac={dn_frac:.3f} up_pulses={up_pulses}"


def check_pfd_deadzone(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows or not {"ref", "div", "up", "dn"}.issubset(rows[0]):
        return False, "missing ref/div/up/dn"
    vth = max(r["ref"] for r in rows) * 0.5
    up = [1 if r["up"] > vth else 0 for r in rows]
    dn = [1 if r["dn"] > vth else 0 for r in rows]
    up_frac = weighted_logic_high_fraction(rows, "up", vth)
    dn_frac = weighted_logic_high_fraction(rows, "dn", vth)
    both_hi = [a & b for a, b in zip(up, dn)]

    run_len = 0
    max_run = 0
    for bit in both_hi:
        if bit:
            run_len += 1
            max_run = max(max_run, run_len)
        else:
            run_len = 0

    up_pulses = sum(1 for i in range(1, len(up)) if up[i - 1] == 0 and up[i] == 1)
    if not (0.001 <= up_frac <= 0.03):
        return False, f"up_frac_out_of_range={up_frac:.4f}"
    if dn_frac > 0.002:
        return False, f"dn_frac_too_high={dn_frac:.4f}"
    if max_run > 6:
        return False, f"overlap_too_long={max_run}"
    if up_pulses < 10:
        return False, f"too_few_up_pulses={up_pulses}"
    return True, f"up_frac={up_frac:.4f} dn_frac={dn_frac:.4f} up_pulses={up_pulses}"


def check_pfd_small_phase_error_response(rows: list[dict[str, float]]) -> tuple[bool, str]:
    return check_pfd_deadzone(rows)


_RELEASE_SIMPLE_BINARY_DAC_CODES = tuple(range(16))
_RELEASE_SIMPLE_BINARY_DAC_SAMPLE_TIMES_NS = tuple(5.0 + 10.0 * idx for idx in range(16))


def check_simple_binary_dac_4b(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "aout", "code_0", "code_1", "code_2", "code_3"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/aout/code_0/code_1/code_2/code_3"
    expected = [0.9 * code / 15.0 for code in _RELEASE_SIMPLE_BINARY_DAC_CODES]
    observed: list[float] = []
    observed_codes: list[int] = []
    code_mismatches = 0
    for t_ns, expected_code in zip(_RELEASE_SIMPLE_BINARY_DAC_SAMPLE_TIMES_NS, _RELEASE_SIMPLE_BINARY_DAC_CODES):
        value = sample_signal_at(rows, "aout", t_ns * 1e-9)
        if value is None:
            return False, f"missing_sample_at={t_ns:g}ns"
        observed_code = 0
        for bit_idx in range(4):
            bit_value = sample_signal_at(rows, f"code_{bit_idx}", t_ns * 1e-9)
            if bit_value is None:
                return False, f"missing_code_{bit_idx}_sample_at={t_ns:g}ns"
            if bit_value > 0.45:
                observed_code |= 1 << bit_idx
        if observed_code != expected_code:
            code_mismatches += 1
        observed_codes.append(observed_code)
        observed.append(value)
    max_err = max(abs(got - want) for got, want in zip(observed, expected))
    monotonic = all(b >= a - 1e-3 for a, b in zip(observed, observed[1:]))
    zero_scale_ok = abs(observed[0]) <= 0.02
    full_scale_ok = abs(observed[-1] - 0.90) <= 0.02
    ok = max_err <= 0.02 and monotonic and zero_scale_ok and full_scale_ok and code_mismatches == 0
    obs_text = ",".join(f"{value:.3f}" for value in observed)
    exp_text = ",".join(f"{value:.3f}" for value in expected)
    code_text = ",".join(str(code) for code in observed_codes)
    return ok, (
        f"simple_binary_dac_levels={obs_text} expected={exp_text} "
        f"observed_codes={code_text} code_mismatches={code_mismatches} "
        f"max_err={max_err:.3f} monotonic={monotonic} "
        f"zero_scale_ok={zero_scale_ok} full_scale_ok={full_scale_ok}"
    )


def check_pfd_reset_race(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows or not {"ref", "div", "up", "dn"}.issubset(rows[0]):
        return False, "missing ref/div/up/dn"

    vth = max(r["ref"] for r in rows) * 0.5
    first = time_window(rows, 20e-9, 120e-9)
    second = time_window(rows, 160e-9, 260e-9)
    if len(first) < 4 or len(second) < 4:
        return False, "insufficient_window_samples"

    up_first = weighted_logic_high_fraction(first, "up", vth)
    dn_first = weighted_logic_high_fraction(first, "dn", vth)
    up_second = weighted_logic_high_fraction(second, "up", vth)
    dn_second = weighted_logic_high_fraction(second, "dn", vth)

    first_times = [r["time"] for r in first]
    second_times = [r["time"] for r in second]
    up_pulses_first = len(rising_edges([r["up"] for r in first], first_times, threshold=vth))
    dn_pulses_second = len(rising_edges([r["dn"] for r in second], second_times, threshold=vth))

    overlap_dt = 0.0
    total_dt = 0.0
    for idx in range(1, len(rows)):
        dt = rows[idx]["time"] - rows[idx - 1]["time"]
        if dt <= 0.0:
            continue
        total_dt += dt
        up_mid = 0.5 * (rows[idx - 1]["up"] + rows[idx]["up"])
        dn_mid = 0.5 * (rows[idx - 1]["dn"] + rows[idx]["dn"])
        if up_mid > vth and dn_mid > vth:
            overlap_dt += dt
    overlap_frac = overlap_dt / max(total_dt, 1e-18)

    ok = (
        0.001 <= up_first <= 0.08
        and dn_first <= 0.01
        and 0.001 <= dn_second <= 0.08
        and up_second <= 0.01
        and up_pulses_first >= 4
        and dn_pulses_second >= 4
        and overlap_frac <= 0.01
    )
    return ok, (
        f"up_first={up_first:.4f} dn_first={dn_first:.4f} "
        f"up_second={up_second:.4f} dn_second={dn_second:.4f} "
        f"up_pulses_first={up_pulses_first} dn_pulses_second={dn_pulses_second} "
        f"overlap_frac={overlap_frac:.4f}"
    )


def check_cppll_freq_step_reacquire(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"ref_clk", "fb_clk", "lock", "vctrl_mon"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing ref_clk/fb_clk/lock/vctrl_mon"

    vth = 0.45
    times = [r["time"] for r in rows]
    ref_edges = rising_edges([r["ref_clk"] for r in rows], times, threshold=vth)
    fb_edges = rising_edges([r["fb_clk"] for r in rows], times, threshold=vth)
    if len(ref_edges) < 12 or len(fb_edges) < 12:
        return False, f"not_enough_edges ref={len(ref_edges)} fb={len(fb_edges)}"

    ref_late = [t for t in ref_edges if 4.5e-6 <= t <= 5.9e-6]
    fb_late = [t for t in fb_edges if 4.5e-6 <= t <= 5.9e-6]
    if len(ref_late) < 4 or len(fb_late) < 4:
        return False, (
            f"not_enough_late_edges ref_late={len(ref_late)} fb_late={len(fb_late)}"
        )

    ref_periods = [b - a for a, b in zip(ref_late, ref_late[1:])]
    fb_periods = [b - a for a, b in zip(fb_late, fb_late[1:])]
    ref_period = sum(ref_periods) / len(ref_periods)
    fb_period = sum(fb_periods) / len(fb_periods)
    if ref_period <= 0.0 or fb_period <= 0.0:
        return False, "non_positive_period"
    freq_ratio = ref_period / fb_period

    lock_edges = rising_edges([r["lock"] for r in rows], times, threshold=vth)
    pre_lock_edges = [t for t in lock_edges if t < 2.0e-6]
    post_lock_edges = [t for t in lock_edges if 2.2e-6 <= t <= 5.9e-6]
    relock_time = post_lock_edges[0] if post_lock_edges else float("nan")

    disturb_low_frac = 1.0 - weighted_logic_high_fraction_window(
        rows, "lock", vth, 2.05e-6, 2.8e-6
    )

    vctrl_vals = [r["vctrl_mon"] for r in rows]
    vctrl_min = min(vctrl_vals)
    vctrl_max = max(vctrl_vals)
    vctrl_in_range = all(-1e-6 <= v <= 0.95 for v in vctrl_vals)

    ok = (
        bool(pre_lock_edges)
        and disturb_low_frac >= 0.25
        and bool(post_lock_edges)
        and 0.97 <= freq_ratio <= 1.03
        and vctrl_in_range
    )
    return ok, (
        f"pre_lock_edges={len(pre_lock_edges)} "
        f"disturb_lock_low_frac={disturb_low_frac:.3f} "
        f"post_lock_edges={len(post_lock_edges)} "
        f"late_freq_ratio={freq_ratio:.4f} "
        f"relock_time={(relock_time if post_lock_edges else float('nan')):.3e} "
        f"vctrl_min={vctrl_min:.3f} "
        f"vctrl_max={vctrl_max:.3f}"
    )


def check_gray_counter_4b(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"clk", "rstb", "g3", "g2", "g1", "g0"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing clk/rstb/g3/g2/g1/g0"
    vth = max(r["clk"] for r in rows) * 0.5
    clk = [r["clk"] for r in rows]
    times_ns = [r["time"] * 1e9 for r in rows]
    edge_idx = [i for i in range(1, len(clk)) if clk[i - 1] <= vth < clk[i]]
    codes: list[int] = []
    for idx in edge_idx:
        settle = min(idx + 8, len(rows) - 1)
        code = (
            (1 if rows[settle]["g3"] > vth else 0) << 3
            | (1 if rows[settle]["g2"] > vth else 0) << 2
            | (1 if rows[settle]["g1"] > vth else 0) << 1
            | (1 if rows[settle]["g0"] > vth else 0)
        )
        codes.append(code)
    post_reset = [codes[i] for i, idx in enumerate(edge_idx) if times_ns[idx] > 55.0]
    if len(post_reset) < 20:
        return False, f"not_enough_post_reset_edges={len(post_reset)}"
    bad_transitions = 0
    for a, b in zip(post_reset[:-1], post_reset[1:]):
        if bin(a ^ b).count("1") != 1:
            bad_transitions += 1
    unique_codes = set(post_reset)
    expected_grays = {i ^ (i >> 1) for i in range(16)}
    if bad_transitions > 0:
        return False, f"gray_property_violated bad_transitions={bad_transitions}"
    if not expected_grays.issubset(unique_codes):
        return False, f"missing_gray_codes count={16 - len(expected_grays & unique_codes)}"
    return True, f"unique_codes={len(unique_codes)} bad_transitions={bad_transitions}"


def check_gray_counter_one_bit_change(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "empty"
    sample = rows[0]
    clk_col = _pick_column(sample, ["clk", "CLK"])
    rst_col = _pick_column(sample, ["rst", "RST", "rstb", "RSTB"])
    if clk_col is None or rst_col is None:
        return False, "missing clk/rst"

    g_cols = [_pick_column(sample, [f"g{idx}", f"G{idx}"]) for idx in range(4)]
    if any(col is None for col in g_cols):
        return False, "missing g0..g3"

    threshold = 0.45
    clk = [r[clk_col] for r in rows]
    edge_idx = [i for i in range(1, len(clk)) if clk[i - 1] <= threshold < clk[i]]
    if len(edge_idx) < 20:
        return False, f"not_enough_clk_edges={len(edge_idx)}"

    rst_high_active = any(r[rst_col] > threshold for r in rows[: max(4, len(rows) // 10)])
    post_reset_codes: list[int] = []
    for idx in edge_idx:
        settle = min(idx + 8, len(rows) - 1)
        rst_val = rows[settle][rst_col]
        if (rst_high_active and rst_val > threshold) or ((not rst_high_active) and rst_val < threshold):
            continue
        code = 0
        for bit_idx, col in enumerate(g_cols):
            if rows[settle][col] > threshold:
                code |= 1 << bit_idx
        post_reset_codes.append(code)

    if len(post_reset_codes) < 16:
        return False, f"not_enough_post_reset_codes={len(post_reset_codes)}"

    bad_transitions = sum(1 for a, b in zip(post_reset_codes[:-1], post_reset_codes[1:]) if bin(a ^ b).count("1") != 1)
    unique_codes = set(post_reset_codes)
    expected_grays = {i ^ (i >> 1) for i in range(16)}
    if bad_transitions:
        return False, f"gray_property_violated bad_transitions={bad_transitions}"
    if not expected_grays.issubset(unique_codes):
        return False, f"missing_gray_codes count={16 - len(expected_grays & unique_codes)}"
    return True, f"unique_codes={len(unique_codes)} bad_transitions={bad_transitions}"


def check_prbs7(rows: list[dict[str, float]]) -> tuple[bool, str]:
    """PRBS-7: check serial output has many transitions and ~50% high fraction."""
    if not rows:
        return False, "empty"
    serial_col = next((k for k in rows[0] if k.lower() in {"prbs_out", "serial", "serial_out", "dout", "q_out", "q"}), None)
    if serial_col is None:
        return False, f"missing serial column; keys={list(rows[0].keys())[:8]}"
    post = [r[serial_col] for r in rows if r["time"] > 2e-8]
    if len(post) < 20:
        return False, "too_few_post_init_samples"
    binary = [1 if v > 0.45 else 0 for v in post]
    transitions = sum(1 for i in range(len(binary) - 1) if binary[i] != binary[i + 1])
    hi_frac = sum(binary) / len(binary)
    ok = transitions >= 20 and 0.2 < hi_frac < 0.8
    return ok, f"transitions={transitions} hi_frac={hi_frac:.3f}"


def check_therm2bin(rows: list[dict[str, float]]) -> tuple[bool, str]:
    """Thermometer-to-binary: check all 4 output bits are high in final window (all 15 inputs on)."""
    if not rows:
        return False, "empty"
    b_cols = [k for k in rows[0] if k.lower() in {"b3", "b2", "b1", "b0", "bin_3", "bin_2", "bin_1", "bin_0"}]
    if len(b_cols) < 4:
        return False, f"missing b3..b0; got {list(rows[0].keys())[:12]}"
    b_cols = sorted(
        b_cols,
        key=lambda name: int(re.findall(r"(\d+)$", name)[0]),
    )[:4]
    t_end = rows[-1]["time"]
    late = [r for r in rows if r["time"] > t_end * 0.75]
    if not late:
        return False, "no late-window rows"
    all_high = all(r[c] > 0.45 for r in late for c in b_cols)
    return all_high, f"all_bits_high_final_window={all_high}"


def check_sar_logic(rows: list[dict[str, float]]) -> tuple[bool, str]:
    """10-bit SAR logic: check RDY asserts and DP_DAC bits show activity."""
    if not rows:
        return False, "empty"
    rdy_col = next((k for k in rows[0] if k.lower() in {"rdy", "ready", "eoc", "done"}), None)
    if rdy_col is None:
        return False, f"missing rdy/eoc column; keys={list(rows[0].keys())[:10]}"
    rdy_vals = [r[rdy_col] for r in rows]
    rdy_high = any(v > 0.45 for v in rdy_vals)
    dac_cols = [k for k in rows[0] if re.search(r"dp_dac|dp_n|dp_p|dac_bit|cap", k.lower())]
    dac_activity = False
    for col in dac_cols[:4]:
        vals = [r[col] for r in rows]
        if max(vals) - min(vals) > 0.4:
            dac_activity = True
            break
    ok = rdy_high and dac_activity
    return ok, f"rdy_asserted={rdy_high} dac_activity={dac_activity}"


def check_pipeline_stage(rows: list[dict[str, float]]) -> tuple[bool, str]:
    """1.5-bit MDAC: verify sub-ADC decisions and gain-of-2 residue."""
    required = {"time", "phi1", "phi2", "vin", "vres", "d1", "d0"}
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0].keys())) if rows else sorted(required)
        return False, f"missing_columns={','.join(missing)}"

    vth = 0.45
    times = [r["time"] for r in rows]
    phi2_edges = rising_edges([r["phi2"] for r in rows], times, threshold=vth)
    sample_rows = sample_rows_at_or_after_times(rows, [edge_t + 0.8e-9 for edge_t in phi2_edges])
    if len(sample_rows) < 3:
        return False, f"phi2_samples={len(sample_rows)}"

    region_counts = {"upper": 0, "middle": 0, "lower": 0}
    bit_mismatches = 0
    residue_mismatches = 0
    bounded_failures = 0
    max_residue_err = 0.0

    for row in sample_rows:
        vin = row["vin"]
        vin_rel = vin - 0.45
        if vin_rel > 0.9 / 4.0:
            region = "upper"
            exp_d1, exp_d0 = 1, 0
            exp_vres = 0.45 + 2.0 * vin_rel - 0.9 / 2.0
        elif vin_rel < -0.9 / 4.0:
            region = "lower"
            exp_d1, exp_d0 = 0, 0
            exp_vres = 0.45 + 2.0 * vin_rel + 0.9 / 2.0
        else:
            region = "middle"
            exp_d1, exp_d0 = 0, 1
            exp_vres = 0.45 + 2.0 * vin_rel
        exp_vres = min(0.9, max(0.0, exp_vres))
        region_counts[region] += 1

        got_d1 = 1 if row["d1"] >= vth else 0
        got_d0 = 1 if row["d0"] >= vth else 0
        if (got_d1, got_d0) != (exp_d1, exp_d0):
            bit_mismatches += 1

        err = abs(row["vres"] - exp_vres)
        max_residue_err = max(max_residue_err, err)
        if err > 0.04:
            residue_mismatches += 1
        if row["vres"] < -0.02 or row["vres"] > 0.92:
            bounded_failures += 1

    missing_regions = [name for name, count in region_counts.items() if count == 0]
    ok = (
        not missing_regions
        and bit_mismatches == 0
        and residue_mismatches == 0
        and bounded_failures == 0
    )
    return ok, (
        f"regions=upper:{region_counts['upper']},middle:{region_counts['middle']},lower:{region_counts['lower']} "
        f"bit_mismatches={bit_mismatches} "
        f"residue_mismatches={residue_mismatches} "
        f"max_residue_err={max_residue_err:.4f} "
        f"bounded_failures={bounded_failures}"
    )


def _pipeline_adc_chain_stage_code(value: float, *, vrefp: float = 0.9, vrefn: float = 0.0) -> int:
    span = vrefp - vrefn
    if value < vrefn + span * 0.25:
        return 0
    if value < vrefn + span * 0.50:
        return 1
    if value < vrefn + span * 0.75:
        return 2
    return 3


def _pipeline_adc_chain_expected(vin: float, *, vrefp: float = 0.9, vrefn: float = 0.0) -> tuple[int, int, int, float, float]:
    span = vrefp - vrefn
    vin = min(vrefp, max(vrefn, vin))
    s1_code = _pipeline_adc_chain_stage_code(vin, vrefp=vrefp, vrefn=vrefn)
    center1 = vrefn + (s1_code + 0.5) * span / 4.0
    res1 = (vrefp + vrefn) / 2.0 + 4.0 * (vin - center1)
    res1 = min(vrefp, max(vrefn, res1))

    s2_code = _pipeline_adc_chain_stage_code(res1, vrefp=vrefp, vrefn=vrefn)
    center2 = vrefn + (s2_code + 0.5) * span / 4.0
    res2 = (vrefp + vrefn) / 2.0 + 4.0 * (res1 - center2)
    res2 = min(vrefp, max(vrefn, res2))

    final_code = 4 * s1_code + s2_code
    return s1_code, s2_code, final_code, res1, res2


def check_release_pipeline_adc_chain(rows: list[dict[str, float]]) -> tuple[bool, str]:
    """Release L2 pipeline ADC: verify two-stage decisions, residues, and final code."""
    required = {
        "time",
        "vin",
        "clk",
        "res1",
        "res2",
        "s1b1",
        "s1b0",
        "s2b1",
        "s2b0",
        "dout3",
        "dout2",
        "dout1",
        "dout0",
    }
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0].keys())) if rows else sorted(required)
        return False, f"missing_columns={','.join(missing)}"

    vth = 0.45
    times = [row["time"] for row in rows]
    edge_times = rising_edges([row["clk"] for row in rows], times, threshold=vth)
    sample_rows = sample_rows_at_or_after_times(rows, [edge_t + 0.8e-9 for edge_t in edge_times])
    if len(sample_rows) < 16:
        return False, f"too_few_settled_samples={len(sample_rows)}"

    observed_codes: list[int] = []
    expected_codes: list[int] = []
    stage_bit_mismatches = 0
    final_concat_mismatches = 0
    final_code_mismatches = 0
    residue_mismatches = 0
    bounded_failures = 0
    max_res1_err = 0.0
    max_res2_err = 0.0
    res2_values: list[float] = []

    for row in sample_rows:
        exp_s1, exp_s2, exp_final, exp_res1, exp_res2 = _pipeline_adc_chain_expected(row["vin"])
        got_s1 = ((1 if row["s1b1"] >= vth else 0) << 1) | (1 if row["s1b0"] >= vth else 0)
        got_s2 = ((1 if row["s2b1"] >= vth else 0) << 1) | (1 if row["s2b0"] >= vth else 0)
        got_final = (
            ((1 if row["dout3"] >= vth else 0) << 3)
            | ((1 if row["dout2"] >= vth else 0) << 2)
            | ((1 if row["dout1"] >= vth else 0) << 1)
            | (1 if row["dout0"] >= vth else 0)
        )
        got_concat = 4 * got_s1 + got_s2

        if got_s1 != exp_s1 or got_s2 != exp_s2:
            stage_bit_mismatches += 1
        if got_final != got_concat:
            final_concat_mismatches += 1
        if got_final != exp_final:
            final_code_mismatches += 1

        res1_err = abs(row["res1"] - exp_res1)
        res2_err = abs(row["res2"] - exp_res2)
        max_res1_err = max(max_res1_err, res1_err)
        max_res2_err = max(max_res2_err, res2_err)
        if res1_err > 0.04 or res2_err > 0.04:
            residue_mismatches += 1
        if row["res1"] < -0.02 or row["res1"] > 0.92 or row["res2"] < -0.02 or row["res2"] > 0.92:
            bounded_failures += 1

        observed_codes.append(got_final)
        expected_codes.append(exp_final)
        res2_values.append(row["res2"])

    observed_unique = sorted(set(observed_codes))
    expected_unique = sorted(set(expected_codes))
    reversals = sum(1 for prev, curr in zip(observed_codes, observed_codes[1:]) if curr < prev)
    res2_span = max(res2_values) - min(res2_values) if res2_values else 0.0
    ok = (
        observed_unique == list(range(16))
        and expected_unique == list(range(16))
        and stage_bit_mismatches == 0
        and final_concat_mismatches == 0
        and final_code_mismatches == 0
        and residue_mismatches == 0
        and bounded_failures == 0
        and reversals == 0
        and res2_span > 0.20
    )
    return ok, (
        f"observed_codes={','.join(str(code) for code in observed_unique)} "
        f"expected_codes={','.join(str(code) for code in expected_unique)} "
        f"stage_bit_mismatches={stage_bit_mismatches} "
        f"final_concat_mismatches={final_concat_mismatches} "
        f"final_code_mismatches={final_code_mismatches} "
        f"residue_mismatches={residue_mismatches} "
        f"max_res1_err={max_res1_err:.4f} "
        f"max_res2_err={max_res2_err:.4f} "
        f"res2_span={res2_span:.4f} "
        f"reversals={reversals} "
        f"bounded_failures={bounded_failures}"
    )


def check_sar_12bit(rows: list[dict[str, float]]) -> tuple[bool, str]:
    """12-bit SAR: check EOC/RDY asserts and DAC bits show activity."""
    return check_sar_logic(rows)


def check_segmented_dac(rows: list[dict[str, float]]) -> tuple[bool, str]:
    """Segmented 14-bit DAC: check differential output spans meaningful range."""
    if not rows:
        return False, "empty"
    vop_col = next((k for k in rows[0] if k.lower() in {"vout_p", "iout_p", "voutp"}), None)
    von_col = next((k for k in rows[0] if k.lower() in {"vout_n", "iout_n", "voutn"}), None)
    if vop_col is None or von_col is None:
        vout_col = next((k for k in rows[0] if "vout" in k.lower() or "iout" in k.lower()), None)
        if vout_col is None:
            return False, f"missing vout_p/vout_n; keys={list(rows[0].keys())[:10]}"
        vvals = [r[vout_col] for r in rows]
        ok = max(vvals) - min(vvals) > 0.1
        return ok, f"vout_range={max(vvals)-min(vvals):.3f}"
    diff = [r[vop_col] - r[von_col] for r in rows]
    diff_range = max(diff) - min(diff)
    ok = diff_range > 0.1
    return ok, f"diff_range={diff_range:.3f}"


def check_comparator_offset_search(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "inp", "inn", "outp"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/inp/inn/outp"

    threshold = 0.45
    outp = [r["outp"] for r in rows]
    times = [r["time"] for r in rows]
    rise_t = next((times[idx] for idx in range(1, len(rows)) if outp[idx - 1] < threshold <= outp[idx]), None)
    if rise_t is None:
        return False, "no_output_crossing"

    crossing_row = next((r for r in rows if r["time"] >= rise_t), rows[-1])
    crossing_voltage = crossing_row["inp"]
    low_window = [r["outp"] for r in rows if r["inp"] <= 0.501]
    high_window = [r["outp"] for r in rows if r["inp"] >= 0.509]
    if not low_window or not high_window:
        return False, "insufficient_offset_windows"

    low_frac = sum(1 for v in low_window if v < threshold) / len(low_window)
    high_frac = sum(1 for v in high_window if v > threshold) / len(high_window)
    ok = abs(crossing_voltage - 0.505) <= 0.003 and low_frac > 0.9 and high_frac > 0.9
    return ok, (
        f"crossing_voltage={crossing_voltage:.4f} "
        f"low_frac={low_frac:.3f} "
        f"high_frac={high_frac:.3f}"
    )


def check_comparator_measurement_flow(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "inp", "inn", "outp", "trip_v", "offset_est", "valid"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/inp/inn/outp/trip_v/offset_est/valid"

    threshold = 0.45
    outp = [r["outp"] for r in rows]
    valid = [r["valid"] for r in rows]
    if max(outp) - min(outp) < 0.3:
        return False, f"outp_range={max(outp) - min(outp):.3f}"
    if max(valid) - min(valid) < 0.3:
        return False, f"valid_range={max(valid) - min(valid):.3f}"

    low_window = [r for r in rows if r["inp"] <= r["inn"] + 0.001]
    high_window = [r for r in rows if r["inp"] >= r["inn"] + 0.009]
    if not low_window or not high_window:
        return False, "insufficient_pre_post_trip_windows"

    low_frac = sum(1 for r in low_window if r["outp"] < threshold) / len(low_window)
    high_frac = sum(1 for r in high_window if r["outp"] > threshold) / len(high_window)
    pre_valid_low_frac = sum(1 for r in low_window if r["valid"] < threshold) / len(low_window)
    if low_frac < 0.9 or high_frac < 0.9 or pre_valid_low_frac < 0.9:
        return False, (
            f"output_or_valid_window_fail low_frac={low_frac:.3f} "
            f"high_frac={high_frac:.3f} pre_valid_low_frac={pre_valid_low_frac:.3f}"
        )

    valid_rows = [r for r in rows if r["valid"] > threshold]
    if not valid_rows:
        return False, "valid_never_asserts"

    first_valid = valid_rows[0]
    final_valid_rows = [r for r in valid_rows if r["time"] >= first_valid["time"] + 2e-9]
    if len(final_valid_rows) < 3:
        final_valid_rows = valid_rows[-min(5, len(valid_rows)) :]

    trip_vals = [r["trip_v"] for r in final_valid_rows]
    offset_vals = [r["offset_est"] for r in final_valid_rows]
    trip_avg = sum(trip_vals) / len(trip_vals)
    offset_avg = sum(offset_vals) / len(offset_vals)
    inn_avg = sum(r["inn"] for r in final_valid_rows) / len(final_valid_rows)
    expected_trip = inn_avg + 0.005
    expected_offset = 0.005
    trip_span = max(trip_vals) - min(trip_vals)
    offset_span = max(offset_vals) - min(offset_vals)

    ok = (
        abs(trip_avg - expected_trip) <= 0.0015
        and abs(offset_avg - expected_offset) <= 0.0015
        and trip_span <= 0.002
        and offset_span <= 0.002
    )
    return ok, (
        f"trip_avg={trip_avg:.4f} expected_trip={expected_trip:.4f} "
        f"offset_avg={offset_avg:.4f} low_frac={low_frac:.3f} "
        f"high_frac={high_frac:.3f} trip_span={trip_span:.4f} "
        f"offset_span={offset_span:.4f}"
    )


def check_cdac_cal(rows: list[dict[str, float]]) -> tuple[bool, str]:
    """CDAC with cal: check differential output varies with control bits."""
    if not rows:
        return False, "empty"
    vdac_cols = [k for k in rows[0] if "vdac" in k.lower() or "vcap" in k.lower() or "vout" in k.lower()]
    if not vdac_cols:
        return False, f"missing vdac columns; keys={list(rows[0].keys())[:10]}"
    for col in vdac_cols[:2]:
        vals = [r[col] for r in rows]
        if max(vals) - min(vals) > 0.05:
            return True, f"vdac_activity col={col} range={max(vals)-min(vals):.3f}"
    return False, f"no vdac activity in {vdac_cols[:4]}"


_RELEASE_CDAC_CODE_SEQUENCE = (
    0,
    1,
    2,
    3,
    7,
    15,
    16,
    32,
    64,
    128,
    256,
    512,
    255,
    511,
    767,
    1023,
)
_RELEASE_CDAC_CAL_SEQUENCE = (0, 1, 2, 3) * 4
_RELEASE_CDAC_SAMPLE_START_S = 5e-9
_RELEASE_CDAC_SAMPLE_PERIOD_S = 4e-9


def _release_cdac_state_index(edge_t: float) -> int | None:
    idx = int(round((edge_t - _RELEASE_CDAC_SAMPLE_START_S) / _RELEASE_CDAC_SAMPLE_PERIOD_S))
    if idx < 0 or idx >= len(_RELEASE_CDAC_CODE_SEQUENCE):
        return None
    expected_edge_t = _RELEASE_CDAC_SAMPLE_START_S + idx * _RELEASE_CDAC_SAMPLE_PERIOD_S
    if abs(edge_t - expected_edge_t) > 0.35e-9:
        return None
    return idx


def check_release_cdac_feedback_dac(rows: list[dict[str, float]]) -> tuple[bool, str]:
    """Release CDAC: verify settled differential output follows code + 32*cal."""
    required = {"time", "clk", "cal0", "cal1", "vdac_p", "vdac_n"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/clk/cal0/cal1/vdac_p/vdac_n"

    times = [r["time"] for r in rows]
    clk_edges = rising_edges([r["clk"] for r in rows], times)
    if len(clk_edges) < 14:
        return False, f"clk_edges={len(clk_edges)}"

    checked = 0
    covered_states: set[int] = set()
    mismatches = 0
    cal_mismatches = 0
    diff_values: list[float] = []
    max_diff_error = 0.0
    max_cm_error = 0.0

    for edge_t in clk_edges:
        state_idx = _release_cdac_state_index(edge_t)
        if state_idx is None:
            continue
        sample_t = edge_t + 0.25e-9
        vdac_p = sample_signal_at(rows, "vdac_p", sample_t)
        vdac_n = sample_signal_at(rows, "vdac_n", sample_t)
        cal0 = sample_signal_at(rows, "cal0", edge_t)
        cal1 = sample_signal_at(rows, "cal1", edge_t)
        if vdac_p is None or vdac_n is None or cal0 is None or cal1 is None:
            continue

        code = _RELEASE_CDAC_CODE_SEQUENCE[state_idx]
        expected_cal = _RELEASE_CDAC_CAL_SEQUENCE[state_idx]
        observed_cal = (1 if cal0 > 0.45 else 0) | (2 if cal1 > 0.45 else 0)
        expected_diff = 0.6 * (((code + 32 * expected_cal) / 1023.0) - 0.5)
        actual_diff = vdac_p - vdac_n
        diff_error = abs(actual_diff - expected_diff)
        cm_error = abs(0.5 * (vdac_p + vdac_n) - 0.45)

        checked += 1
        covered_states.add(state_idx)
        diff_values.append(actual_diff)
        max_diff_error = max(max_diff_error, diff_error)
        max_cm_error = max(max_cm_error, cm_error)
        if observed_cal != expected_cal:
            cal_mismatches += 1
        if diff_error > 0.035 or cm_error > 0.025:
            mismatches += 1

    if checked < 14 or len(covered_states) < 14:
        return False, f"settled_samples={checked} covered_states={len(covered_states)}"
    diff_span = max(diff_values) - min(diff_values)
    allowed_mismatches = max(1, checked // 10)
    ok = (
        mismatches <= allowed_mismatches
        and cal_mismatches <= allowed_mismatches
        and diff_span > 0.035
        and max_cm_error <= 0.025
    )
    return ok, (
        f"samples={checked} mismatches={mismatches}/{allowed_mismatches} "
        f"cal_mismatches={cal_mismatches} covered_states={len(covered_states)} "
        f"diff_span={diff_span:.4f} "
        f"max_diff_error={max_diff_error:.4f} max_cm_error={max_cm_error:.4f}"
    )


def check_sc_integrator(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "empty"
    keys = rows[0].keys()
    phi2_col = next((k for k in keys if k.lower() == "phi2"), None)
    vout_col = next((k for k in keys if k.lower() in {"vout", "out"}), None)
    if phi2_col is None or vout_col is None:
        return False, f"missing phi2/vout; keys={list(keys)[:10]}"

    edges = [
        rows[i]["time"]
        for i in range(1, len(rows))
        if rows[i - 1][phi2_col] < 0.45 <= rows[i][phi2_col]
    ]
    if len(edges) < 3:
        return False, f"phi2_edges={len(edges)}"

    samples: list[float] = []
    for t_edge in edges[:5]:
        window = [
            r[vout_col]
            for r in rows
            if t_edge + 0.5e-9 <= r["time"] <= t_edge + 2.0e-9
        ]
        if window:
            samples.append(sum(window) / len(window))
    if len(samples) < 3:
        return False, f"insufficient_vout_samples={len(samples)}"

    monotonic = all(samples[i + 1] >= samples[i] - 2e-3 for i in range(len(samples) - 1))
    total_step = samples[-1] - samples[0]
    ok = monotonic and total_step > 0.05
    return ok, f"monotonic={monotonic} total_step={total_step:.3f}"


def check_bg_cal(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "empty"
    trim_cols = sorted(
        [k for k in rows[0] if re.fullmatch(r"trim_?[0-5]", k.lower())],
        key=lambda name: int(re.findall(r"(\d+)$", name)[0]),
    )
    settled_col = next((k for k in rows[0] if k.lower() in {"settled", "done", "rdy"}), None)
    if len(trim_cols) < 6 or settled_col is None:
        return False, f"missing trim/settled columns; keys={list(rows[0].keys())[:12]}"

    codes = []
    for row in rows:
        code = 0
        for idx, col in enumerate(trim_cols):
            if row[col] > 0.45:
                code |= 1 << idx
        codes.append(code)

    code_span = max(codes) - min(codes)
    settled_high = any(r[settled_col] > 0.45 for r in rows[int(len(rows) * 0.75):])
    ok = code_span >= 4 and settled_high
    return ok, f"code_span={code_span} settled_high={settled_high}"


def check_multitone(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "empty"
    out_col = next((k for k in rows[0] if k.lower() in {"out", "vout"}), None)
    if out_col is None:
        return False, f"missing out/vout column; keys={list(rows[0].keys())[:10]}"

    times = [r["time"] for r in rows]
    vals = [r[out_col] for r in rows]

    def interp(t: float) -> float | None:
        if not times:
            return None
        if t <= times[0]:
            return vals[0]
        if t >= times[-1]:
            return vals[-1]
        lo = 0
        hi = len(times) - 1
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if times[mid] <= t:
                lo = mid
            else:
                hi = mid
        t0 = times[lo]
        t1 = times[hi]
        if t1 == t0:
            return vals[lo]
        a = (t - t0) / (t1 - t0)
        return vals[lo] + a * (vals[hi] - vals[lo])

    samples = [
        (0.125e-6, 0.2 * math.sin(2 * math.pi * 1e6 * 0.125e-6) + 0.1 * math.sin(2 * math.pi * 2e6 * 0.125e-6) + 0.05 * math.sin(2 * math.pi * 3e6 * 0.125e-6)),
        (0.275e-6, 0.2 * math.sin(2 * math.pi * 1e6 * 0.275e-6) + 0.1 * math.sin(2 * math.pi * 2e6 * 0.275e-6) + 0.05 * math.sin(2 * math.pi * 3e6 * 0.275e-6)),
        (0.410e-6, 0.2 * math.sin(2 * math.pi * 1e6 * 0.410e-6) + 0.1 * math.sin(2 * math.pi * 2e6 * 0.410e-6) + 0.05 * math.sin(2 * math.pi * 3e6 * 0.410e-6)),
    ]
    errs = []
    for t_check, expected in samples:
        measured = interp(t_check)
        if measured is None:
            errs.append(1.0)
            continue
        errs.append(abs(measured - expected))
    max_err = max(errs)
    ok = max_err < 0.03
    return ok, f"max_err={max_err:.4f}"


def check_nrz_prbs(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "empty"
    outp_col = next((k for k in rows[0] if k.lower() in {"outp", "voutp", "out_p"}), None)
    outn_col = next((k for k in rows[0] if k.lower() in {"outn", "voutn", "out_n"}), None)
    if outp_col is None or outn_col is None:
        return False, f"missing differential outputs; keys={list(rows[0].keys())[:12]}"

    outp = [r[outp_col] for r in rows]
    outn = [r[outn_col] for r in rows]
    transitions = sum(1 for i in range(1, len(outp)) if (outp[i - 1] - 0.45) * (outp[i] - 0.45) < 0)
    complement_err = sum(abs((a + b) - 0.9) for a, b in zip(outp, outn)) / len(outp)
    swing = max(outp) - min(outp)
    ok = transitions >= 8 and complement_err < 0.08 and swing > 0.2
    return ok, f"transitions={transitions} complement_err={complement_err:.4f} swing={swing:.3f}"


def check_mixed_domain_cdac_bug(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "empty"
    vout_col = next((k for k in rows[0] if k.lower() in {"vout", "out"}), None)
    if vout_col is None:
        return False, f"missing vout column; keys={list(rows[0].keys())[:10]}"

    targets = [
        (17e-9, 0.2),
        (37e-9, 0.5),
        (57e-9, 0.8),
    ]
    errs = []
    for t_check, expected in targets:
        window = [r[vout_col] for r in rows if abs(r["time"] - t_check) <= 1.5e-9]
        if not window:
            errs.append(1.0)
            continue
        measured = sum(window) / len(window)
        errs.append(abs(measured - expected))
    max_err = max(errs)
    ok = max_err < 0.05
    return ok, f"max_err={max_err:.4f}"


def check_spectre_port_discipline(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "empty"
    required = {"a", "b", "y"}
    keymap = {k.lower(): k for k in rows[0]}
    if not required.issubset(keymap):
        return False, f"missing a/b/y; keys={list(rows[0].keys())[:10]}"

    windows = [
        (10e-9, 0.0, "00"),
        (30e-9, 0.0, "10"),
        (50e-9, 0.0, "01"),
        (70e-9, 0.9, "11"),
    ]
    errs: list[str] = []
    for t_check, expected, label in windows:
        vals = [r[keymap["y"]] for r in rows if abs(r["time"] - t_check) <= 1.5e-9]
        if not vals:
            errs.append(f"{label}_no_samples")
            continue
        measured = sum(vals) / len(vals)
        if abs(measured - expected) > 0.05:
            errs.append(f"{label}_err={abs(measured - expected):.3f}")
    return (not errs), ("ok" if not errs else ";".join(errs))


def check_inverted_comparator_logic_bug(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "empty"
    required = {"vinp", "vinn", "out_p"}
    if not required.issubset(rows[0]):
        return False, "missing vinp/vinn/out_p"

    windows = [
        (10e-9, 0.0, "low0"),
        (30e-9, 0.9, "high1"),
        (50e-9, 0.0, "low2"),
        (70e-9, 0.9, "high3"),
    ]
    errs: list[str] = []
    for t_check, expected, label in windows:
        vals = [r["out_p"] for r in rows if abs(r["time"] - t_check) <= 1.5e-9]
        if not vals:
            errs.append(f"{label}_no_samples")
            continue
        measured = sum(vals) / len(vals)
        if abs(measured - expected) > 0.08:
            errs.append(f"{label}_err={abs(measured - expected):.3f}")
    return (not errs), ("ok" if not errs else ";".join(errs))


def check_mux_4to1(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"d0", "d1", "d2", "d3", "sel1", "sel0", "y", "time"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing d0/d1/d2/d3/sel1/sel0/y/time"
    windows = [
        (50e-9, 0.1, "sel0"),
        (150e-9, 0.3, "sel1"),
        (250e-9, 0.6, "sel2"),
        (350e-9, 0.8, "sel3"),
    ]
    tol = 20e-3
    failures: list[str] = []
    for t_check, expected, label in windows:
        window = [
            r["y"]
            for r in rows
            if t_check - 10e-9 <= r["time"] <= t_check + 10e-9
        ]
        if not window:
            failures.append(f"{label}_no_samples")
            continue
        measured = sum(window) / len(window)
        if abs(measured - expected) > tol:
            failures.append(f"{label}_err={abs(measured - expected):.4f}")
    if failures:
        return False, ";".join(failures)
    return True, "all_4_select_windows_correct"


def check_above_threshold_startup(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin", "out"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/vin/out"
    if max(r["vin"] for r in rows) < 0.45:
        return False, "vin_never_above_threshold"
    out_vals = [r["out"] for r in rows]
    out_min = min(out_vals)
    out_max = max(out_vals)
    span = out_max - out_min
    if span < 0.2:
        return False, f"out_not_latched_high span={span:.3f}"
    vth = out_min + 0.5 * span
    first_hi_t = next((r["time"] for r in rows if r["out"] > vth), None)
    if first_hi_t is None:
        return False, "out_never_high"
    late = [r["out"] for r in rows if r["time"] >= rows[-1]["time"] * 0.6]
    late_hi_frac = sum(1 for v in late if v > vth) / max(len(late), 1)
    ok = first_hi_t <= 2e-9 and late_hi_frac > 0.95
    return ok, f"first_hi_t_ns={first_hi_t*1e9:.3f} late_hi_frac={late_hi_frac:.3f}"


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
    ok = wraps >= 3 and phase_span > 0.5 and guard_rises >= 3
    return ok, f"guard_rises={guard_rises} wraps={wraps} phase_span={phase_span:.3f} guard_hi_frac={guard_hi_frac:.3f}"


def check_cross_hysteresis_window(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin", "out"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/vin/out"
    out_vals = [r["out"] for r in rows]
    lo = min(out_vals)
    hi = max(out_vals)
    span = hi - lo
    if span < 0.3:
        return False, f"out_span_too_small={span:.3f}"
    low1 = [r["out"] for r in rows if r["time"] <= 20e-9]
    high_mid = [r["out"] for r in rows if 35e-9 <= r["time"] <= 55e-9]
    low2 = [r["out"] for r in rows if r["time"] >= 75e-9]
    if not low1 or not high_mid or not low2:
        return False, "insufficient_window_samples"
    m_low1 = sum(low1) / len(low1)
    m_high = sum(high_mid) / len(high_mid)
    m_low2 = sum(low2) / len(low2)
    ok = (m_high - m_low1) > 0.45 * span and (m_high - m_low2) > 0.45 * span
    return ok, f"low1={m_low1:.3f} high={m_high:.3f} low2={m_low2:.3f} span={span:.3f}"


def check_true_window_comparator(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin", "out"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/vin/out"
    out_vals = [r["out"] for r in rows]
    lo = min(out_vals)
    hi = max(out_vals)
    span = hi - lo
    if span < 0.3:
        return False, f"out_span_too_small={span:.3f}"

    vth = lo + 0.5 * span
    t_mid = 0.5 * (rows[0]["time"] + rows[-1]["time"])

    def frac_high(selected: list[dict[str, float]]) -> float:
        if not selected:
            return 0.0
        return sum(1 for row in selected if row["out"] > vth) / len(selected)

    below = [r for r in rows if r["vin"] <= 0.18]
    above = [r for r in rows if r["vin"] >= 0.72]
    inside_rise = [r for r in rows if r["time"] <= t_mid and 0.34 <= r["vin"] <= 0.56]
    inside_fall = [r for r in rows if r["time"] > t_mid and 0.34 <= r["vin"] <= 0.56]

    if min(len(below), len(above), len(inside_rise), len(inside_fall)) < 3:
        return (
            False,
            "insufficient_window_samples "
            f"below={len(below)} above={len(above)} rise={len(inside_rise)} fall={len(inside_fall)}",
        )

    below_hi = frac_high(below)
    above_hi = frac_high(above)
    rise_hi = frac_high(inside_rise)
    fall_hi = frac_high(inside_fall)
    ok = below_hi < 0.10 and above_hi < 0.10 and rise_hi > 0.80 and fall_hi > 0.80
    return (
        ok,
        f"below_hi={below_hi:.3f} above_hi={above_hi:.3f} "
        f"inside_rise_hi={rise_hi:.3f} inside_fall_hi={fall_hi:.3f} span={span:.3f}",
    )


def check_cross_interval_163p333(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "delay_out", "seen_out"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/delay_out/seen_out"
    seen_hi = max(r["seen_out"] for r in rows)
    if seen_hi < 0.3:
        return False, f"seen_out_never_high={seen_hi:.3f}"

    seen_th = 0.5 * seen_hi
    seen_rows = [r for r in rows if r["seen_out"] > seen_th]
    if not seen_rows:
        return False, "seen_out_no_logic_high_samples"
    # The event happens late in a short run. Averaging the final 30% of the
    # whole waveform incorrectly includes pre-event zeros, so measure the
    # settled delay level only after seen_out has asserted.
    settle_start = seen_rows[0]["time"] + 0.2e-9
    settled_rows = [r for r in seen_rows if r["time"] >= settle_start]
    if len(settled_rows) < 3:
        settled_rows = seen_rows
    tail_count = min(len(settled_rows), max(5, len(settled_rows) // 3))
    tail = sorted(r["delay_out"] for r in settled_rows[-tail_count:])
    if not tail:
        return False, "no_post_seen_delay_samples"
    delay_level = tail[len(tail) // 2]
    vdd_est = max(max(r["seen_out"] for r in rows), 1e-6)
    delay_ps = delay_level / vdd_est * 200.0
    ok = 130.0 <= delay_ps <= 190.0
    return ok, f"delay_ps={delay_ps:.3f} seen_hi={seen_hi:.3f} post_seen_samples={len(settled_rows)}"


def check_cross_sine_precision(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"first_err_out", "max_err_out", "count_out"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing first_err_out/max_err_out/count_out"
    vdd_est = max(r["count_out"] for r in rows)
    if vdd_est < 0.2:
        return False, f"count_out_too_low={vdd_est:.3f}"
    count_est = max(r["count_out"] for r in rows) / max(vdd_est, 1e-6) * 3.0
    max_err_ps = max(r["max_err_out"] for r in rows) / max(vdd_est, 1e-6) * 10.0
    ok = count_est >= 2.5 and max_err_ps < 1.0
    return ok, f"count_est={count_est:.2f} max_err_ps={max_err_ps:.4f}"


def check_differential_voltage_output(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "din", "en", "outp", "outn"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/din/en/outp/outn"

    vout_hi = max(max(r["outp"] for r in rows), max(r["outn"] for r in rows))
    logic_th = 0.45 if vout_hi <= 1.2 else 0.5 * vout_hi

    def settled(items: list[dict[str, float]]) -> list[dict[str, float]]:
        if len(items) < 6:
            return items
        return items[len(items) // 4 :]

    disabled = settled([r for r in rows if r["en"] <= logic_th])
    enabled_low = settled([r for r in rows if r["en"] > logic_th and r["din"] <= logic_th])
    enabled_high = settled([r for r in rows if r["en"] > logic_th and r["din"] > logic_th])
    if len(disabled) < 5 or len(enabled_low) < 5 or len(enabled_high) < 5:
        return False, "insufficient_window_samples"

    def mean_diff(items: list[dict[str, float]]) -> float:
        return sum(r["outp"] - r["outn"] for r in items) / len(items)

    def mean_abs_diff(items: list[dict[str, float]]) -> float:
        return sum(abs(r["outp"] - r["outn"]) for r in items) / len(items)

    def mean_cm(items: list[dict[str, float]]) -> float:
        return sum(0.5 * (r["outp"] + r["outn"]) for r in items) / len(items)

    dis_diff = mean_diff(disabled)
    dis_abs_diff = mean_abs_diff(disabled)
    low_diff = mean_diff(enabled_low)
    high_diff = mean_diff(enabled_high)
    cms = [mean_cm(disabled), mean_cm(enabled_low), mean_cm(enabled_high)]
    cm_span = max(cms) - min(cms)
    ok = dis_abs_diff < 0.08 and low_diff < -0.20 and high_diff > 0.20 and cm_span < 0.12
    return ok, (
        f"disabled_diff={dis_diff:.3f} disabled_abs_diff={dis_abs_diff:.3f} low_diff={low_diff:.3f} "
        f"high_diff={high_diff:.3f} cm_span={cm_span:.3f}"
    )


def check_final_step_file_metric(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "ref", "metric_out"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/ref/metric_out"
    ref_high = max(r["ref"] for r in rows)
    vth = 0.45 if ref_high < 1.0 else 0.5 * ref_high
    ref_edges = rising_edges([r["ref"] for r in rows], [r["time"] for r in rows], threshold=vth)
    expected_edges = [10e-9, 30e-9, 50e-9, 70e-9]
    if len(ref_edges) != len(expected_edges):
        return False, f"ref_edges={len(ref_edges)} expected={len(expected_edges)}"
    edge_errs = [abs(edge - expected) for edge, expected in zip(ref_edges, expected_edges)]
    max_edge_err = max(edge_errs) if edge_errs else float("inf")
    if max_edge_err > 0.5e-9:
        return False, f"ref_edge_grid_error_ns={max_edge_err * 1e9:.3f}"

    metric_vals = [r["metric_out"] for r in rows]
    vmax = max(metric_vals)
    if vmax < 0.2:
        return False, f"metric_out_too_low={vmax:.3f}"
    expected_levels = [ref_high * count / 4.0 for count in range(1, 5)]
    windows = [
        (12e-9, 18e-9),
        (32e-9, 38e-9),
        (52e-9, 58e-9),
        (72e-9, 78e-9),
    ]
    levels: list[float] = []
    for t0, t1 in windows:
        vals = [r["metric_out"] for r in rows if t0 <= r["time"] <= t1]
        if not vals:
            return False, "insufficient_metric_plateau_samples"
        levels.append(sum(vals) / len(vals))
    level_errs = [abs(level - expected) for level, expected in zip(levels, expected_levels)]
    max_level_err = max(level_errs) if level_errs else float("inf")
    tail = [r["metric_out"] for r in rows if r["time"] >= rows[-1]["time"] * 0.85]
    final_level = sum(tail) / len(tail) if tail else 0.0
    final_norm = final_level / max(ref_high, 1e-6)
    dips = sum(1 for i in range(1, len(metric_vals)) if metric_vals[i] + 0.03 < metric_vals[i - 1])
    ok = max_level_err <= 0.08 and final_norm > 0.90 and dips <= 3
    return ok, (
        f"ref_edges={len(ref_edges)} max_edge_err_ns={max_edge_err * 1e9:.3f} "
        f"metric_levels={[round(v,3) for v in levels]} max_level_err={max_level_err:.3f} "
        f"final_norm={final_norm:.3f} metric_dips={dips}"
    )


def check_parameter_type_override(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows or "out" not in rows[0]:
        return False, "missing out"
    out_vals = [r["out"] for r in rows]
    vhi = max(out_vals)
    vth = 0.5 * vhi
    times = [r["time"] for r in rows]
    pulses = len(rising_edges(out_vals, times, threshold=vth))
    ok = 3 <= pulses <= 5 and 0.60 <= vhi <= 0.85
    return ok, f"pulses={pulses} peak={vhi:.3f}"


def check_phase_accumulator_timer_wrap(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk_out", "phase_out"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/clk_out/phase_out"
    phase_vals = [r["phase_out"] for r in rows]
    clk_vals = [r["clk_out"] for r in rows]
    times = [r["time"] for r in rows]
    phase_span = max(phase_vals) - min(phase_vals)
    if phase_span < 0.4:
        return False, f"phase_span_too_small={phase_span:.3f}"
    phase_lo = min(phase_vals)
    high_th = phase_lo + 0.70 * phase_span
    low_th = phase_lo + 0.30 * phase_span
    wraps = 0
    armed = False
    for phase in phase_vals:
        if phase >= high_th:
            armed = True
        elif armed and phase <= low_th:
            wraps += 1
            armed = False
    cth = 0.5 * (max(clk_vals) + min(clk_vals))
    clk_rises = len(rising_edges(clk_vals, times, threshold=cth))
    ok = wraps >= 3 and clk_rises >= 3
    return ok, f"wraps={wraps} clk_rises={clk_rises} phase_span={phase_span:.3f}"


def check_simultaneous_event_order(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "ref", "out"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/ref/out"
    ref_high = max(r["ref"] for r in rows)
    vth = 0.45 if ref_high < 1.0 else 0.5 * ref_high
    ref_edges = rising_edges([r["ref"] for r in rows], [r["time"] for r in rows], threshold=vth)
    expected_edges = [10e-9, 30e-9, 50e-9, 70e-9]
    if len(ref_edges) != len(expected_edges):
        return False, f"ref_edges={len(ref_edges)} expected={len(expected_edges)}"
    edge_errs = [abs(edge - expected) for edge, expected in zip(ref_edges, expected_edges)]
    max_edge_err = max(edge_errs) if edge_errs else float("inf")
    if max_edge_err > 0.5e-9:
        return False, f"ref_edge_grid_error_ns={max_edge_err * 1e9:.3f}"

    windows = [
        (12e-9, 18e-9),
        (32e-9, 38e-9),
        (52e-9, 58e-9),
        (72e-9, 78e-9),
    ]
    levels: list[float] = []
    for t0, t1 in windows:
        vals = [r["out"] for r in rows if t0 <= r["time"] <= t1]
        if not vals:
            return False, "insufficient_window_samples"
        levels.append(sum(vals) / len(vals))
    monotonic = all(levels[i] <= levels[i + 1] + 0.05 for i in range(len(levels) - 1))
    span = levels[-1] - levels[0]
    expected_levels = [0.2 * cycle * ref_high for cycle in range(1, 5)]
    level_errs = [abs(level - expected) for level, expected in zip(levels, expected_levels)]
    max_level_err = max(level_errs) if level_errs else float("inf")
    ok = monotonic and span > 0.40 and max_level_err <= 0.08
    return ok, (
        f"ref_edges={len(ref_edges)} max_edge_err_ns={max_edge_err * 1e9:.3f} "
        f"plateau_levels={[round(v,3) for v in levels]} max_level_err={max_level_err:.3f} "
        f"span={span:.3f}"
    )


def check_timer_absolute_grid(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk_out"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/clk_out"
    clk_vals = [r["clk_out"] for r in rows]
    times = [r["time"] for r in rows]
    cth = 0.5 * (max(clk_vals) + min(clk_vals))
    rises = rising_edges(clk_vals, times, threshold=cth)
    if len(rises) < 4:
        return False, f"too_few_rising_edges={len(rises)}"
    targets = [10.1e-9, 30.1e-9, 50.1e-9, 70.1e-9]
    errs = [abs(r - t) for r, t in zip(rises[:4], targets)]
    max_err = max(errs) if errs else float("inf")
    ok = max_err <= 2.0e-9
    return ok, f"rises_ns={[round(v*1e9,3) for v in rises[:4]]} max_err_ns={max_err*1e9:.3f}"


def check_transition_branch_target(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "mode", "clk", "out"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/mode/clk/out"
    w_low0 = [r["out"] for r in rows if 15e-9 <= r["time"] <= 22e-9]
    w_high1 = [r["out"] for r in rows if 35e-9 <= r["time"] <= 42e-9]
    w_high2 = [r["out"] for r in rows if 55e-9 <= r["time"] <= 62e-9]
    w_low3 = [r["out"] for r in rows if 75e-9 <= r["time"] <= 85e-9]
    if not (w_low0 and w_high1 and w_high2 and w_low3):
        return False, "insufficient_window_samples"
    m0 = sum(w_low0) / len(w_low0)
    m1 = sum(w_high1) / len(w_high1)
    m2 = sum(w_high2) / len(w_high2)
    m3 = sum(w_low3) / len(w_low3)
    span = max(m1, m2) - min(m0, m3)
    ok = (m1 - m0) > 0.35 * max(span, 1e-6) and (m2 - m3) > 0.35 * max(span, 1e-6)
    return ok, f"means=({m0:.3f},{m1:.3f},{m2:.3f},{m3:.3f})"


def check_release_calibration_loop(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "out"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/clk/rst/out"
    input_key = "vin" if "vin" in rows[0] else "err" if "err" in rows[0] else None
    if input_key is None:
        return False, "missing vin/err input"

    reset_rows = [r for r in rows if r["rst"] > 0.45 and r["time"] < 3e-9]
    post_rows = [r for r in rows if r["rst"] <= 0.45 and r["time"] > 3e-9]
    if len(post_rows) < 10:
        return False, f"too_few_post_reset_rows={len(post_rows)}"

    reset_mean = sum(r["out"] for r in reset_rows) / len(reset_rows) if reset_rows else rows[0]["out"]
    out_vals = [r["out"] for r in post_rows]
    out_min = min(out_vals)
    out_max = max(out_vals)
    out_span = out_max - out_min
    if not (0.0 <= out_min <= out_max <= 0.95):
        return False, f"out_range=({out_min:.3f},{out_max:.3f})"
    if abs(reset_mean - 0.45) > 0.12:
        return False, f"reset_trim_mean={reset_mean:.3f}"
    if out_span < 0.12:
        return False, f"trim_span_too_small={out_span:.3f}"

    edge_idx = [
        idx for idx in range(1, len(rows))
        if rows[idx - 1]["clk"] <= 0.45 < rows[idx]["clk"] and rows[idx]["rst"] <= 0.45
    ]
    directional_checks = 0
    directional_matches = 0
    prev_out: float | None = None
    for idx in edge_idx:
        settle = min(idx + 3, len(rows) - 1)
        current_out = rows[settle]["out"]
        if prev_out is None:
            prev_out = current_out
            continue
        errv = rows[idx][input_key] - 0.45
        delta = current_out - prev_out
        prev_out = current_out
        if abs(errv) <= 0.08:
            continue
        if current_out < 0.08 or current_out > 0.82 or prev_out < 0.08 or prev_out > 0.82:
            continue
        directional_checks += 1
        if (errv > 0.0 and delta > 0.004) or (errv < 0.0 and delta < -0.004):
            directional_matches += 1
    if directional_checks < 3:
        return False, f"too_few_directional_trim_checks={directional_checks}"
    if directional_matches < directional_checks - 1:
        return False, f"trim_direction_mismatches={directional_checks - directional_matches}/{directional_checks}"

    return True, (
        f"release_calibration_loop reset={reset_mean:.3f} span={out_span:.3f} "
        f"direction={directional_matches}/{directional_checks}"
    )


def mean_in_window(rows: list[dict[str, float]], key: str, start: float, stop: float) -> float | None:
    values = [r[key] for r in rows if start <= r["time"] <= stop and key in r]
    if not values:
        return None
    return sum(values) / len(values)


def edge_settled_values(rows: list[dict[str, float]], key: str, *, clk_key: str = "clk", rst_key: str = "rst") -> list[tuple[dict[str, float], float]]:
    values: list[tuple[dict[str, float], float]] = []
    for idx in range(1, len(rows)):
        if rows[idx - 1][clk_key] <= 0.45 < rows[idx][clk_key] and rows[idx].get(rst_key, 0.0) <= 0.45:
            settle = min(idx + 3, len(rows) - 1)
            values.append((rows[idx], rows[settle][key]))
    return values


def check_release_charge_pump(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "up", "dn", "vctrl", "metric"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/clk/rst/up/dn/vctrl/metric"

    ctrl_vals = [r["vctrl"] for r in rows]
    ctrl_min = min(ctrl_vals)
    ctrl_max = max(ctrl_vals)
    if not (0.0 <= ctrl_min <= ctrl_max <= 0.95):
        return False, f"charge_pump_vctrl_range=({ctrl_min:.3f},{ctrl_max:.3f})"

    reset_vals = [r["vctrl"] for r in rows if r["rst"] > 0.45 and r["time"] <= 3.0e-9]
    if not reset_vals:
        return False, "charge_pump_missing_reset_window"
    reset_mean = sum(reset_vals) / len(reset_vals)
    if abs(reset_mean - 0.45) > 0.12:
        return False, f"charge_pump_reset_mean={reset_mean:.3f}"
    ctrl_span = ctrl_max - ctrl_min
    if ctrl_span < 0.12:
        return False, f"charge_pump_vctrl_span_too_small={ctrl_span:.3f}"

    samples = edge_settled_values(rows, "vctrl")
    up_checks = down_checks = up_ok = down_ok = 0
    previous: float | None = None
    for edge_row, ctrl in samples:
        if previous is None:
            previous = ctrl
            continue
        previous_out = previous
        delta = ctrl - previous_out
        previous = ctrl
        if edge_row["time"] > 60e-9:
            continue
        if ctrl < 0.08 or ctrl > 0.82 or previous_out < 0.08 or previous_out > 0.82:
            continue
        up_high = edge_row["up"] > 0.45
        dn_high = edge_row["dn"] > 0.45
        if up_high and not dn_high:
            up_checks += 1
            if delta > 0.004:
                up_ok += 1
        elif dn_high and not up_high:
            down_checks += 1
            if delta < -0.004:
                down_ok += 1
    if up_checks < 2 or down_checks < 2:
        return False, f"charge_pump_missing_polarity_windows up={up_checks} down={down_checks}"
    if up_ok < up_checks - 1 or down_ok < down_checks - 1:
        return False, f"charge_pump_polarity up={up_ok}/{up_checks} down={down_ok}/{down_checks}"
    return True, (
        f"release_charge_pump reset={reset_mean:.3f} span={ctrl_span:.3f} "
        f"polarity up={up_ok}/{up_checks} down={down_ok}/{down_checks}"
    )


def check_release_loop_filter(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "vin", "out", "metric"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/clk/rst/vin/out/metric"

    out_vals = [r["out"] for r in rows if "out" in r]
    if not out_vals:
        return False, "loop_filter_missing_out_values"
    out_min = min(out_vals)
    out_max = max(out_vals)
    if not (0.0 <= out_min <= out_max <= 0.95):
        return False, f"loop_filter_out_range=({out_min:.3f},{out_max:.3f})"

    edge_samples: list[tuple[dict[str, float], float, float]] = []
    for idx in range(1, len(rows)):
        if rows[idx - 1]["clk"] <= 0.45 < rows[idx]["clk"] and rows[idx]["rst"] <= 0.45:
            settle = min(idx + 3, len(rows) - 1)
            edge_samples.append((rows[idx], rows[settle]["out"], rows[settle]["metric"]))
    if len(edge_samples) < 12:
        return False, f"loop_filter_too_few_edge_samples={len(edge_samples)}"

    deltas: list[tuple[dict[str, float], float, float, float]] = []
    previous_out: float | None = None
    for edge_row, out, metric in edge_samples:
        if previous_out is not None:
            deltas.append((edge_row, out - previous_out, out, metric))
        previous_out = out

    positive_deltas = [
        delta
        for edge_row, delta, out, _metric in deltas
        if edge_row["time"] < 40e-9 and edge_row["vin"] > 0.55 and 0.08 < out < 0.93
    ]
    if len(positive_deltas) < 4:
        return False, f"loop_filter_missing_positive_pi_steps={len(positive_deltas)}"
    first_pos = positive_deltas[0]
    later_pos = positive_deltas[-1]
    proportional_decay = first_pos > 0.08 and 0.0 < later_pos < first_pos * 0.65
    if not proportional_decay:
        return False, f"loop_filter_no_proportional_decay first={first_pos:.3f} later={later_pos:.3f}"

    negative_deltas = [
        delta
        for edge_row, delta, out, _metric in deltas
        if 32e-9 <= edge_row["time"] <= 50e-9 and edge_row["vin"] < 0.40 and 0.08 < out < 0.93
    ]
    negative_ok = len(negative_deltas) >= 3 and sum(1 for delta in negative_deltas if delta < -0.003) >= 3
    if not negative_ok:
        return False, f"loop_filter_missing_negative_response={len(negative_deltas)}"

    near_deadband_hold = mean_in_window(rows, "out", 48e-9, 54e-9)
    if near_deadband_hold is None or near_deadband_hold < 0.80:
        value = "missing" if near_deadband_hold is None else f"{near_deadband_hold:.3f}"
        return False, f"loop_filter_missing_integral_residual={value}"

    early_metric = mean_in_window(rows, "metric", 8e-9, 18e-9)
    late_metric = mean_in_window(rows, "metric", 24e-9, 50e-9)
    reset_metric = mean_in_window(rows, "metric", 64.5e-9, 70e-9)
    if early_metric is None or late_metric is None or reset_metric is None:
        return False, "loop_filter_missing_metric_windows"
    metric_timing = early_metric < 0.15 and late_metric > 0.65 and reset_metric < 0.15
    if not metric_timing:
        return False, (
            f"loop_filter_metric_timing early={early_metric:.3f} "
            f"late={late_metric:.3f} reset={reset_metric:.3f}"
        )

    late_reset = mean_in_window(rows, "out", 64.5e-9, 66e-9)
    after_reset = mean_in_window(rows, "out", 67e-9, 70e-9)
    if late_reset is None or after_reset is None:
        return False, "loop_filter_missing_late_reset_window"
    if abs(late_reset - 0.45) > 0.02 or abs(after_reset - 0.45) > 0.02:
        return False, f"loop_filter_reset_not_cleared late={late_reset:.3f} after={after_reset:.3f}"
    return True, (
        f"loop_filter_pi first_pos_delta={first_pos:.3f} later_pos_delta={later_pos:.3f} "
        f"negative_steps={sum(1 for delta in negative_deltas if delta < -0.003)}/{len(negative_deltas)} "
        f"integral_residual={near_deadband_hold:.3f} metric={early_metric:.3f}/{late_metric:.3f}/{reset_metric:.3f} "
        f"reset={late_reset:.3f}/{after_reset:.3f}"
    )


def check_release_deadband_calibration(rows: list[dict[str, float]]) -> tuple[bool, str]:
    ok, note = check_release_calibration_loop(rows)
    if not ok:
        return ok, note
    samples = edge_settled_values(rows, "out")
    hold_checks = hold_ok = 0
    previous: float | None = None
    for edge_row, out in samples:
        if previous is None:
            previous = out
            continue
        errv = edge_row.get("vin", edge_row.get("err", 0.45)) - 0.45
        delta = abs(out - previous)
        previous = out
        if abs(errv) <= 0.055 and edge_row["time"] < 60e-9:
            hold_checks += 1
            if delta <= 0.025:
                hold_ok += 1
    if hold_checks < 2:
        return False, f"deadband_missing_hold_samples={hold_checks}"
    if hold_ok < hold_checks:
        return False, f"deadband_hold_mismatches={hold_checks - hold_ok}/{hold_checks}"
    return True, f"{note}; deadband_hold={hold_ok}/{hold_checks}"


def check_release_sar_calibration_fsm(rows: list[dict[str, float]]) -> tuple[bool, str]:
    ok, note = check_release_calibration_loop(rows)
    if not ok:
        return ok, note
    samples = [(edge, out) for edge, out in edge_settled_values(rows, "out") if edge["time"] < 45e-9]
    deltas = [abs(samples[idx][1] - samples[idx - 1][1]) for idx in range(1, len(samples))]
    active_deltas = [d for d in deltas if d > 0.015]
    if len(active_deltas) < 4:
        return False, f"sar_cal_too_few_active_steps={len(active_deltas)}"
    if active_deltas[-1] > 0.60 * active_deltas[0]:
        return False, f"sar_cal_step_not_halving first={active_deltas[0]:.3f} last={active_deltas[-1]:.3f}"
    metric_values = [r.get("metric", 0.0) for r in rows if r["time"] > 20e-9]
    if metric_values and max(metric_values) <= 0.45:
        return False, "sar_cal_done_never_asserted"
    return True, f"{note}; sar_step_first_last={active_deltas[0]:.3f}/{active_deltas[-1]:.3f}"


def check_release_filter_chain(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "vin", "out", "metric"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/clk/rst/vin/out/metric"
    post_rows = [r for r in rows if r["rst"] <= 0.45 and r["time"] > 3e-9]
    if len(post_rows) < 10:
        return False, f"too_few_post_reset_rows={len(post_rows)}"

    out_vals = [r["out"] for r in post_rows]
    metric_vals = [r["metric"] for r in post_rows]
    out_min = min(out_vals)
    out_max = max(out_vals)
    metric_min = min(metric_vals)
    metric_max = max(metric_vals)
    if not (-0.02 <= out_min <= out_max <= 0.92):
        return False, f"out_range=({out_min:.3f},{out_max:.3f})"
    if not (-0.10 <= metric_min <= metric_max <= 1.00):
        return False, f"metric_range=({metric_min:.3f},{metric_max:.3f})"
    if out_max - out_min < 0.18:
        return False, f"out_span_too_small={out_max - out_min:.3f}"

    low_rows = [r for r in post_rows if r["vin"] < 0.35]
    high_rows = [r for r in post_rows if r["vin"] > 0.60]
    if not low_rows or not high_rows:
        return False, "missing_low_or_high_vin_window"
    low_min = min(r["out"] for r in low_rows)
    high_max = max(r["out"] for r in high_rows)
    if high_max <= low_min + 0.10:
        return False, f"gain_response_too_small low_min={low_min:.3f} high_max={high_max:.3f}"

    return True, (
        f"release_filter_chain out_span={out_max - out_min:.3f} "
        f"low_min={low_min:.3f} high_max={high_max:.3f}"
    )


def check_release_voltage_gain_amplifier(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "vin", "out", "metric"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/clk/rst/vin/out/metric"

    reset_out = mean_in_window(rows, "out", 0.5e-9, 2.0e-9)
    high_out = mean_in_window(rows, "out", 16.0e-9, 24.0e-9)
    mid_out = mean_in_window(rows, "out", 33.0e-9, 36.0e-9)
    low_out = mean_in_window(rows, "out", 46.0e-9, 55.0e-9)
    late_high_out = mean_in_window(rows, "out", 74.0e-9, 79.0e-9)
    high_metric = mean_in_window(rows, "metric", 16.0e-9, 24.0e-9)
    mid_metric = mean_in_window(rows, "metric", 33.0e-9, 36.0e-9)
    low_metric = mean_in_window(rows, "metric", 46.0e-9, 55.0e-9)
    if None in (reset_out, high_out, mid_out, low_out, late_high_out, high_metric, mid_metric, low_metric):
        return False, "gain_amp_missing_sample_windows"
    assert reset_out is not None
    assert high_out is not None
    assert mid_out is not None
    assert low_out is not None
    assert late_high_out is not None
    assert high_metric is not None
    assert mid_metric is not None
    assert low_metric is not None

    out_vals = [r["out"] for r in rows if r["rst"] <= 0.45 and r["time"] > 3e-9]
    if not out_vals:
        return False, "gain_amp_no_post_reset_rows"
    out_min = min(out_vals)
    out_max = max(out_vals)
    if not (-0.02 <= out_min <= out_max <= 0.92):
        return False, f"gain_amp_unclamped_range=({out_min:.3f},{out_max:.3f})"
    if abs(reset_out - 0.45) > 0.12 or abs(mid_out - 0.45) > 0.08:
        return False, f"gain_amp_common_mode reset={reset_out:.3f} mid={mid_out:.3f}"
    if high_out < 0.84 or late_high_out < 0.80:
        return False, f"gain_amp_high_not_railed high={high_out:.3f} late={late_high_out:.3f}"
    if low_out > 0.08:
        return False, f"gain_amp_low_not_railed low={low_out:.3f}"
    if high_metric < 0.65 or low_metric < 0.65 or mid_metric > 0.18:
        return False, (
            "gain_amp_saturation_metric_wrong "
            f"high={high_metric:.3f} mid={mid_metric:.3f} low={low_metric:.3f}"
        )
    return True, (
        "release_voltage_gain_amplifier "
        f"out_high_mid_low={high_out:.3f}/{mid_out:.3f}/{low_out:.3f} "
        f"sat_metric={high_metric:.3f}/{mid_metric:.3f}/{low_metric:.3f}"
    )


def check_release_two_pole_filter(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "vin", "out", "metric"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/clk/rst/vin/out/metric"

    reset_out = mean_in_window(rows, "out", 0.5e-9, 2.0e-9)
    early_high = mean_in_window(rows, "out", 14.0e-9, 16.0e-9)
    late_high = mean_in_window(rows, "out", 24.0e-9, 28.0e-9)
    early_low = mean_in_window(rows, "out", 44.0e-9, 47.0e-9)
    late_low = mean_in_window(rows, "out", 54.0e-9, 58.0e-9)
    metric_high = mean_in_window(rows, "metric", 14.0e-9, 20.0e-9)
    metric_low = mean_in_window(rows, "metric", 44.0e-9, 52.0e-9)
    if None in (reset_out, early_high, late_high, early_low, late_low, metric_high, metric_low):
        return False, "two_pole_missing_sample_windows"
    assert reset_out is not None
    assert early_high is not None
    assert late_high is not None
    assert early_low is not None
    assert late_low is not None
    assert metric_high is not None
    assert metric_low is not None

    post_rows = [r for r in rows if r["rst"] <= 0.45 and 3e-9 < r["time"] < 70e-9]
    if len(post_rows) < 10:
        return False, f"two_pole_too_few_post_reset_rows={len(post_rows)}"
    out_vals = [r["out"] for r in post_rows]
    metric_vals = [r["metric"] for r in post_rows]
    metric_span = max(metric_vals) - min(metric_vals)
    if not (-0.02 <= min(out_vals) <= max(out_vals) <= 0.92):
        return False, f"two_pole_out_range=({min(out_vals):.3f},{max(out_vals):.3f})"
    if abs(reset_out - 0.45) > 0.12:
        return False, f"two_pole_reset_out={reset_out:.3f}"
    if late_high <= early_high + 0.10 or early_high > 0.68:
        return False, f"two_pole_missing_lagged_rise early={early_high:.3f} late={late_high:.3f}"
    if late_low >= early_low - 0.06 or early_low < 0.20:
        return False, f"two_pole_missing_lagged_fall early={early_low:.3f} late={late_low:.3f}"
    if metric_span < 0.09 or metric_high <= 0.50 or metric_low >= 0.40:
        return False, (
            "two_pole_metric_not_state_difference "
            f"span={metric_span:.3f} high={metric_high:.3f} low={metric_low:.3f}"
        )
    return True, (
        "release_two_pole_filter "
        f"rise={early_high:.3f}->{late_high:.3f} "
        f"fall={early_low:.3f}->{late_low:.3f} metric_span={metric_span:.3f}"
    )


def check_release_amplifier_filter_chain(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "vin", "out", "metric"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/clk/rst/vin/out/metric"

    early_high_out = mean_in_window(rows, "out", 12.5e-9, 15.0e-9)
    late_high_out = mean_in_window(rows, "out", 24.0e-9, 28.0e-9)
    early_high_metric = mean_in_window(rows, "metric", 12.5e-9, 15.0e-9)
    late_high_metric = mean_in_window(rows, "metric", 24.0e-9, 28.0e-9)
    mid_metric = mean_in_window(rows, "metric", 33.0e-9, 36.0e-9)
    low_metric = mean_in_window(rows, "metric", 46.0e-9, 55.0e-9)
    low_out = mean_in_window(rows, "out", 54.0e-9, 58.0e-9)
    if None in (early_high_out, late_high_out, early_high_metric, late_high_metric, mid_metric, low_metric, low_out):
        return False, "amp_filter_missing_sample_windows"
    assert early_high_out is not None
    assert late_high_out is not None
    assert early_high_metric is not None
    assert late_high_metric is not None
    assert mid_metric is not None
    assert low_metric is not None
    assert low_out is not None

    post_rows = [r for r in rows if r["rst"] <= 0.45 and 3e-9 < r["time"] < 70e-9]
    if len(post_rows) < 10:
        return False, f"amp_filter_too_few_post_reset_rows={len(post_rows)}"
    out_vals = [r["out"] for r in post_rows]
    metric_vals = [r["metric"] for r in post_rows]
    if not (-0.02 <= min(out_vals) <= max(out_vals) <= 0.92):
        return False, f"amp_filter_out_range=({min(out_vals):.3f},{max(out_vals):.3f})"
    if not (-0.02 <= min(metric_vals) <= max(metric_vals) <= 0.92):
        return False, f"amp_filter_metric_range=({min(metric_vals):.3f},{max(metric_vals):.3f})"
    if early_high_metric < 0.84 or late_high_metric < 0.84 or low_metric > 0.08:
        return False, (
            "amp_filter_metric_not_preamp_target "
            f"early={early_high_metric:.3f} late={late_high_metric:.3f} low={low_metric:.3f}"
        )
    if abs(mid_metric - 0.45) > 0.08:
        return False, f"amp_filter_mid_metric_not_common_mode={mid_metric:.3f}"
    if late_high_out <= early_high_out + 0.09:
        return False, f"amp_filter_missing_lagged_settling early={early_high_out:.3f} late={late_high_out:.3f}"
    if early_high_metric - early_high_out < 0.12:
        return False, f"amp_filter_output_not_lagging_metric gap={early_high_metric - early_high_out:.3f}"
    if low_out > 0.35:
        return False, f"amp_filter_output_not_falling low={low_out:.3f}"
    return True, (
        "release_amplifier_filter_chain "
        f"metric_high_low={early_high_metric:.3f}/{low_metric:.3f} "
        f"out_lag={early_high_out:.3f}->{late_high_out:.3f}"
    )


def check_release_signal_conditioning_chain(rows: list[dict[str, float]]) -> tuple[bool, str]:
    ok, note = check_release_filter_chain(rows)
    if not ok:
        return ok, note
    two_pole_ok, two_pole_note = check_release_two_pole_filter(rows)
    if not two_pole_ok:
        return False, two_pole_note
    high_rows = [r for r in rows if r["rst"] <= 0.45 and r["vin"] > 0.80]
    low_rows = [r for r in rows if r["rst"] <= 0.45 and r["vin"] < 0.20]
    if not high_rows or not low_rows:
        return False, "conditioning_chain_missing_limit_windows"
    high_max = max(r["out"] for r in high_rows)
    low_min = min(r["out"] for r in low_rows)
    if high_max > 0.92 or low_min < -0.02:
        return False, f"conditioning_chain_unbounded=({low_min:.3f},{high_max:.3f})"
    if high_max <= low_min + 0.18:
        return False, f"conditioning_chain_response_too_small=({low_min:.3f},{high_max:.3f})"
    return True, f"{note}; {two_pole_note}; conditioning_limits={low_min:.3f}/{high_max:.3f}"


def check_release_soft_hysteretic_limiter(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "vin", "out", "metric"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/clk/rst/vin/out/metric"

    high_limited = mean_in_window(rows, "out", 16.0e-9, 24.0e-9)
    low_limited = mean_in_window(rows, "out", 46.0e-9, 55.0e-9)
    high_memory = mean_in_window(rows, "out", 31.0e-9, 36.0e-9)
    low_memory = mean_in_window(rows, "out", 61.0e-9, 66.0e-9)
    high_metric = mean_in_window(rows, "metric", 16.0e-9, 24.0e-9)
    low_metric = mean_in_window(rows, "metric", 46.0e-9, 55.0e-9)
    high_memory_metric = mean_in_window(rows, "metric", 31.0e-9, 36.0e-9)
    low_memory_metric = mean_in_window(rows, "metric", 61.0e-9, 66.0e-9)
    if None in (
        high_limited,
        low_limited,
        high_memory,
        low_memory,
        high_metric,
        low_metric,
        high_memory_metric,
        low_memory_metric,
    ):
        return False, "soft_limiter_missing_sample_windows"
    assert high_limited is not None
    assert low_limited is not None
    assert high_memory is not None
    assert low_memory is not None
    assert high_metric is not None
    assert low_metric is not None
    assert high_memory_metric is not None
    assert low_memory_metric is not None

    post_rows = [r for r in rows if r["rst"] <= 0.45 and 3e-9 < r["time"] < 70e-9]
    if len(post_rows) < 10:
        return False, f"soft_limiter_too_few_post_reset_rows={len(post_rows)}"
    out_min = min(r["out"] for r in post_rows)
    out_max = max(r["out"] for r in post_rows)
    metric_span = max(r["metric"] for r in post_rows) - min(r["metric"] for r in post_rows)
    if not (-0.02 <= out_min <= out_max <= 0.92):
        return False, f"soft_limiter_out_range=({out_min:.3f},{out_max:.3f})"
    if high_limited > 0.84 or high_limited < 0.70:
        return False, f"soft_limiter_high_compression={high_limited:.3f}"
    if low_limited < 0.08 or low_limited > 0.22:
        return False, f"soft_limiter_low_compression={low_limited:.3f}"
    if high_memory <= low_memory + 0.08:
        return False, f"soft_limiter_hysteresis_not_visible high={high_memory:.3f} low={low_memory:.3f}"
    if high_metric < 0.58 or high_memory_metric < 0.58 or low_metric > 0.32 or low_memory_metric > 0.32:
        return False, (
            "soft_limiter_metric_not_stateful "
            f"high={high_metric:.3f}/{high_memory_metric:.3f} low={low_metric:.3f}/{low_memory_metric:.3f}"
        )
    if metric_span < 0.30:
        return False, f"soft_limiter_metric_span_too_small={metric_span:.3f}"
    return True, (
        "release_soft_hysteretic_limiter "
        f"limited={low_limited:.3f}/{high_limited:.3f} "
        f"memory={low_memory:.3f}/{high_memory:.3f} metric_span={metric_span:.3f}"
    )


def check_release_quantized_reconstruction(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "vin", "out", "metric"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/clk/rst/vin/out/metric"
    vth = 0.45
    edge_idx = [
        idx for idx in range(1, len(rows))
        if rows[idx - 1]["clk"] <= vth < rows[idx]["clk"] and rows[idx]["rst"] <= vth
    ]
    if len(edge_idx) < 8:
        return False, f"too_few_post_reset_clk_edges={len(edge_idx)}"

    mismatches = 0
    checked = 0
    for idx in edge_idx:
        settle = min(idx + 3, len(rows) - 1)
        sample = max(0.0, min(0.9, rows[idx]["vin"]))
        code = round(sample / 0.9 * 15.0)
        expected = 0.9 * code / 15.0
        actual = rows[settle]["out"]
        checked += 1
        if abs(actual - expected) > 0.08:
            mismatches += 1
    if checked == 0:
        return False, "no_quantizer_samples"
    if mismatches > max(1, checked // 5):
        return False, f"quantized_recon_mismatches={mismatches}/{checked}"

    metric_vals = [r["metric"] for r in rows if r["rst"] <= vth]
    metric_hi = sum(1 for v in metric_vals if v > 0.45)
    metric_lo = sum(1 for v in metric_vals if v <= 0.45)
    if metric_hi == 0 or metric_lo == 0:
        return False, f"metric_not_windowed hi={metric_hi} lo={metric_lo}"
    return True, f"quantized_recon_mismatches={mismatches}/{checked} metric_hi={metric_hi}"


def check_release_event_pulse_stretcher(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "trig", "rst", "pulse"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/trig/rst/pulse"
    vth = 0.45
    trig_edges = rising_edges([r["trig"] for r in rows], [r["time"] for r in rows], threshold=vth)
    if len(trig_edges) < 5:
        return False, f"trig_edges={len(trig_edges)}"
    expected_samples = [
        (1.8e-9, True, "first_trigger_high"),
        (4.4e-9, True, "burst_middle_high"),
        (6.4e-9, True, "retrigger_extended_high"),
        (8.4e-9, False, "burst_final_low"),
        (17.2e-9, True, "single_trigger_high"),
        (19.4e-9, True, "second_burst_middle_high"),
        (21.4e-9, True, "second_retrigger_extended_high"),
        (23.4e-9, False, "second_burst_final_low"),
        (24.6e-9, True, "pre_reset_high"),
        (26.0e-9, False, "reset_forces_low"),
    ]
    failures: list[str] = []
    notes: list[str] = []
    for sample_t, should_be_high, label in expected_samples:
        value = sample_signal_at(rows, "pulse", sample_t)
        if value is None:
            failures.append(f"{label}=missing")
            continue
        is_high = value > vth
        notes.append(f"{label}:{value:.3f}")
        if is_high != should_be_high:
            failures.append(f"{label}={value:.3f}")
    if failures:
        return False, " ".join(failures) + " " + " ".join(notes)
    return True, f"trig_edges={len(trig_edges)} " + " ".join(notes)


def check_release_dac_mismatch_unit_weighting(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "b0", "b1", "b2", "b3", "out"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/b0/b1/b2/b3/out"
    weights = [1.00, 2.02, 3.96, 8.08]
    denom = sum(weights)
    sample_times = [7e-9, 15e-9, 25e-9, 35e-9]
    mismatches = 0
    details: list[str] = []
    for t in sample_times:
        row = min(rows, key=lambda r: abs(r["time"] - t))
        code_sum = sum(weights[idx] for idx, bit in enumerate(("b0", "b1", "b2", "b3")) if row[bit] > 0.45)
        expected = 0.9 * code_sum / denom
        actual = row["out"]
        delta = abs(actual - expected)
        details.append(f"{t * 1e9:.0f}ns:{actual:.4f}/{expected:.4f}")
        if delta > 0.0015:
            mismatches += 1
    if mismatches:
        return False, f"dac_weight_mismatches={mismatches} {' '.join(details)}"
    return True, f"dac_weight_samples {' '.join(details)}"


CHECKS = {
    # legacy short IDs (example-level names)
    "adc_dac_ideal_4b": check_adc_dac_ideal_4b,
    "clk_burst_gen": check_clk_burst_gen,
    "clk_div_smoke": check_clk_div,
    "clk_divider": check_clk_divider,
    "comparator_smoke": check_comparator,
    "dac_binary_clk_4b": check_dac_binary_clk_4b,
    "dac_therm_16b": check_dac_therm_16b,
    "digital_basics": check_not_gate,
    "dwa_ptr_gen": check_dwa_ptr_gen,
    "gain_extraction": check_gain_extraction,
    "lfsr": check_lfsr,
    "prbs7": check_prbs7,
    "therm2bin": check_therm2bin,
    "multimod_divider": check_multimod_divider,
    "bbpd": check_bbpd,
    "bad_bus_output_loop": check_bad_bus_output_loop,
    "missing_transition_outputs": check_missing_transition_outputs,
    "noise_gen": check_noise_gen,
    "sar_adc_dac_weighted_8b": check_sar_adc_dac_weighted_8b,
    # formal task IDs (tasks/end-to-end/voltage/)
    "adpll_lock_smoke": check_adpll_lock,
    "adpll_ratio_hop_smoke": check_adpll_ratio_hop,
    "adpll_timer_smoke": check_adpll_lock,
    "above_threshold_startup_smoke": check_above_threshold_startup,
    "and_gate_smoke": check_and_gate,
    "or_gate_smoke": check_or_gate,
    "not_gate_smoke": check_not_gate,
    "dff_rst_smoke": check_dff_rst,
    "bound_step_period_guard_smoke": check_bound_step_period_guard,
    "cross_hysteresis_window_smoke": check_cross_hysteresis_window,
    "window_comparator_smoke": check_true_window_comparator,
    "cross_interval_163p333_smoke": check_cross_interval_163p333,
    "cross_sine_precision_smoke": check_cross_sine_precision,
    "differential_voltage_output_smoke": check_differential_voltage_output,
    "final_step_file_metric_smoke": check_final_step_file_metric,
    "parameter_type_override_smoke": check_parameter_type_override,
    "phase_accumulator_timer_wrap_smoke": check_phase_accumulator_timer_wrap,
    "simultaneous_event_order_smoke": check_simultaneous_event_order,
    "timer_absolute_grid_smoke": check_timer_absolute_grid,
    "transition_branch_target_smoke": check_transition_branch_target,
    "clk_div_smoke": check_clk_div,
    "cmp_delay_smoke": check_cmp_delay,
    "comparator_hysteresis_smoke": check_cmp_hysteresis,
    "comparator_measurement_flow_smoke": check_comparator_measurement_flow,
    "comparator_offset_search_smoke": check_comparator_offset_search,
    "cmp_strongarm_smoke": check_cmp_strongarm,
    "comparator_smoke": check_comparator,
    "cppll_freq_step_reacquire_smoke": check_cppll_freq_step_reacquire,
    "cppll_tracking_smoke": check_cppll_tracking,
    "d2b_4bit_smoke": check_d2b,
    "ramp_gen_smoke": check_ramp_gen,
    "adc_dac_ideal_4b_smoke": check_adc_dac_ideal_4b,
    "clk_burst_gen_smoke": check_clk_burst_gen,
    "dac_binary_clk_4b_smoke": check_dac_binary_clk_4b,
    "dac_therm_16b_smoke": check_dac_therm_16b,
    "digital_basics_smoke": check_not_gate,
    "dwa_ptr_gen_smoke": check_dwa_ptr_gen,
    "dwa_ptr_gen_no_overlap_smoke": check_dwa_ptr_gen_no_overlap,
    "dwa_wraparound_smoke": check_dwa_wraparound,
    "bbpd_data_edge_alignment_smoke": check_bbpd_data_edge_alignment,
    "gain_extraction_smoke": check_gain_extraction,
    "lfsr_smoke": check_lfsr,
    "noise_gen_smoke": check_noise_gen,
    "sar_adc_dac_weighted_8b_smoke": check_sar_adc_dac_weighted_8b,
    "sample_hold_smoke": check_sample_hold,
    "sample_hold_droop_smoke": check_sample_hold_droop,
    "flash_adc_3b_smoke": check_flash_adc_3b,
    "flash_adc_mini_array_e2e": check_release_flash_adc_mini_array,
    "pipeline_adc_chain_e2e": check_release_pipeline_adc_chain,
    "serializer_8b_smoke": check_serializer_8b,
    "serializer_frame_alignment_smoke": check_serializer_frame_alignment,
    "xor_pd_smoke": check_xor_pd,
    "pfd_updn_smoke": check_pfd_updn,
    "pfd_deadzone_smoke": check_pfd_deadzone,
    "pfd_small_phase_response_smoke": check_pfd_small_phase_error_response,
    "pfd_reset_race_smoke": check_pfd_reset_race,
    "gray_counter_one_bit_change_smoke": check_gray_counter_one_bit_change,
    "gray_counter_4b_smoke": check_gray_counter_4b,
    "multimod_divider_ratio_switch_smoke": check_multimod_divider_ratio_switch,
    "mux_4to1_smoke": check_mux_4to1,
    # spec-to-va task IDs
    "clk_divider":    check_clk_divider,
    "prbs7":          check_prbs7,
    "therm2bin":      check_therm2bin,
    "d2b_4bit":       check_d2b,
    "sar_logic":      check_sar_logic,
    "sar_logic_10b":  check_sar_logic,
    "pipeline_stage": check_pipeline_stage,
    "sar_12bit":      check_sar_12bit,
    "segmented_dac":  check_segmented_dac,
    "cdac_cal":       check_cdac_cal,
    "sc_integrator":  check_sc_integrator,
    "bg_cal":         check_bg_cal,
    "adpll_timer":    check_adpll_lock,
    "cppll_timer":    check_cppll_tracking,
    "multitone":      check_multitone,
    "nrz_prbs":       check_nrz_prbs,
    "mixed_domain_cdac_bug": check_mixed_domain_cdac_bug,
    "spectre_port_discipline": check_spectre_port_discipline,
    "strongarm_reset_priority_bug": check_strongarm_reset_priority_bug,
    "vbm1_background_calibration_accumulator_dut": check_vbm1_background_calibration_accumulator,
    "vbm1_background_calibration_accumulator_tb": check_vbm1_background_calibration_accumulator,
    "vbm1_background_calibration_accumulator_bugfix": check_vbm1_background_calibration_accumulator,
    "vbm1_background_calibration_accumulator_e2e": check_vbm1_background_calibration_accumulator,
    "vbm1_barrel_pointer_window_dut": check_vbm1_barrel_pointer_window,
    "vbm1_barrel_pointer_window_tb": check_vbm1_barrel_pointer_window,
    "vbm1_barrel_pointer_window_bugfix": check_vbm1_barrel_pointer_window,
    "vbm1_barrel_pointer_window_e2e": check_vbm1_barrel_pointer_window,
    "vbm1_cdac_calibration_dut": check_vbm1_cdac_calibration,
    "vbm1_cdac_calibration_tb": check_vbm1_cdac_calibration,
    "vbm1_cdac_calibration_bugfix": check_vbm1_cdac_calibration,
    "vbm1_cdac_calibration_e2e": check_vbm1_cdac_calibration,
    "vbm1_debounce_latch_dut": check_vbm1_debounce_latch,
    "vbm1_debounce_latch_tb": check_vbm1_debounce_latch,
    "vbm1_debounce_latch_bugfix": check_vbm1_debounce_latch,
    "vbm1_debounce_latch_e2e": check_vbm1_debounce_latch,
    "vbm1_edge_detector_dut": check_vbm1_edge_detector,
    "vbm1_edge_detector_tb": check_vbm1_edge_detector,
    "vbm1_edge_detector_bugfix": check_vbm1_edge_detector,
    "vbm1_edge_detector_e2e": check_vbm1_edge_detector,
    "vbm1_element_shuffler_dut": check_vbm1_element_shuffler,
    "vbm1_element_shuffler_tb": check_vbm1_element_shuffler,
    "vbm1_element_shuffler_bugfix": check_vbm1_element_shuffler,
    "vbm1_element_shuffler_e2e": check_vbm1_element_shuffler,
    "vbm1_file_metric_writer_dut": check_vbm1_file_metric_writer,
    "vbm1_file_metric_writer_tb": check_vbm1_file_metric_writer,
    "vbm1_file_metric_writer_e2e": check_vbm1_file_metric_writer,
    "vbm1_first_order_lowpass_dut": check_vbm1_first_order_lowpass,
    "vbm1_first_order_lowpass_tb": check_vbm1_first_order_lowpass,
    "vbm1_first_order_lowpass_bugfix": check_vbm1_first_order_lowpass,
    "vbm1_first_order_lowpass_e2e": check_vbm1_first_order_lowpass,
    "vbm1_gain_trim_controller_dut": check_vbm1_gain_trim_controller,
    "vbm1_gain_trim_controller_tb": check_vbm1_gain_trim_controller,
    "vbm1_gain_trim_controller_bugfix": check_vbm1_gain_trim_controller,
    "vbm1_gain_trim_controller_e2e": check_vbm1_gain_trim_controller,
    "vbm1_leaky_hold_dut": check_vbm1_leaky_hold,
    "vbm1_leaky_hold_tb": check_vbm1_leaky_hold,
    "vbm1_leaky_hold_bugfix": check_vbm1_leaky_hold,
    "vbm1_leaky_hold_e2e": check_vbm1_leaky_hold,
    "vbm1_lock_detector_dut": check_vbm1_lock_detector,
    "vbm1_lock_detector_tb": check_vbm1_lock_detector,
    "vbm1_lock_detector_bugfix": check_vbm1_lock_detector,
    "vbm1_lock_detector_e2e": check_vbm1_lock_detector,
    "vbm1_offset_calibration_fsm_dut": check_vbm1_offset_calibration_fsm,
    "vbm1_offset_calibration_fsm_tb": check_vbm1_offset_calibration_fsm,
    "vbm1_offset_calibration_fsm_bugfix": check_vbm1_offset_calibration_fsm,
    "vbm1_offset_calibration_fsm_e2e": check_vbm1_offset_calibration_fsm,
    "vbm1_offset_comparator_dut": check_vbm1_offset_comparator,
    "vbm1_offset_comparator_tb": check_vbm1_offset_comparator,
    "vbm1_offset_comparator_bugfix": check_vbm1_offset_comparator,
    "vbm1_offset_comparator_e2e": check_vbm1_offset_comparator,
    "vbm1_one_shot_timer_dut": check_vbm1_one_shot_timer,
    "vbm1_one_shot_timer_tb": check_vbm1_one_shot_timer,
    "vbm1_one_shot_timer_bugfix": check_vbm1_one_shot_timer,
    "vbm1_one_shot_timer_e2e": check_vbm1_one_shot_timer,
    "vbm1_peak_detector_dut": check_vbm1_peak_detector,
    "vbm1_peak_detector_tb": check_vbm1_peak_detector,
    "vbm1_peak_detector_bugfix": check_vbm1_peak_detector,
    "vbm1_peak_detector_e2e": check_vbm1_peak_detector,
    "vbm1_precision_rectifier_dut": check_vbm1_precision_rectifier,
    "vbm1_precision_rectifier_tb": check_vbm1_precision_rectifier,
    "vbm1_precision_rectifier_bugfix": check_vbm1_precision_rectifier,
    "vbm1_precision_rectifier_e2e": check_vbm1_precision_rectifier,
    "vbm1_resettable_counter_divider_dut": check_vbm1_resettable_counter_divider,
    "vbm1_resettable_counter_divider_tb": check_vbm1_resettable_counter_divider,
    "vbm1_resettable_counter_divider_e2e": check_vbm1_resettable_counter_divider,
    "vbm1_resettable_integrator_dut": check_vbm1_resettable_integrator,
    "vbm1_resettable_integrator_tb": check_vbm1_resettable_integrator,
    "vbm1_resettable_integrator_bugfix": check_vbm1_resettable_integrator,
    "vbm1_resettable_integrator_e2e": check_vbm1_resettable_integrator,
    "vbm1_rotating_element_selector_dut": check_vbm1_rotating_element_selector,
    "vbm1_rotating_element_selector_tb": check_vbm1_rotating_element_selector,
    "vbm1_rotating_element_selector_bugfix": check_vbm1_rotating_element_selector,
    "vbm1_rotating_element_selector_e2e": check_vbm1_rotating_element_selector,
    "vbm1_sar_logic_4b_dut": check_vbm1_sar_logic_4b,
    "vbm1_sar_logic_4b_tb": check_vbm1_sar_logic_4b,
    "vbm1_sar_logic_4b_bugfix": check_vbm1_sar_logic_4b,
    "vbm1_sar_logic_4b_e2e": check_vbm1_sar_logic_4b,
    "vbm1_pfd_reset_race_dut": check_pfd_reset_race,
    "vbm1_pfd_reset_race_tb": check_pfd_reset_race,
    "vbm1_pfd_reset_race_bugfix": check_pfd_reset_race,
    "vbm1_pfd_reset_race_e2e": check_pfd_reset_race,
    "vbm1_pfd_small_phase_error_response_dut": check_pfd_small_phase_error_response,
    "vbm1_segmented_dac_dut": check_vbm1_segmented_dac,
    "vbm1_segmented_dac_tb": check_vbm1_segmented_dac,
    "vbm1_segmented_dac_bugfix": check_vbm1_segmented_dac,
    "vbm1_segmented_dac_e2e": check_vbm1_segmented_dac,
    "vbm1_settling_time_measurement_tb_dut": check_vbm1_settling_time_measurement_tb,
    "vbm1_settling_time_measurement_tb_tb": check_vbm1_settling_time_measurement_tb,
    "vbm1_settling_time_measurement_tb_e2e": check_vbm1_settling_time_measurement_tb,
    "vbm1_strongarm_comparator_behavior_dut": check_vbm1_strongarm_comparator_behavior,
    "vbm1_strongarm_comparator_behavior_tb": check_vbm1_strongarm_comparator_behavior,
    "vbm1_strongarm_comparator_behavior_e2e": check_vbm1_strongarm_comparator_behavior,
    "vbm1_strongarm_comparator_behavior_bugfix": check_strongarm_reset_priority_bug,
    "vbm1_thermometer_dac_dut": check_vbm1_thermometer_dac,
    "vbm1_thermometer_dac_tb": check_vbm1_thermometer_dac,
    "vbm1_thermometer_dac_bugfix": check_vbm1_thermometer_dac,
    "vbm1_thermometer_dac_e2e": check_vbm1_thermometer_dac,
    "vbm1_simple_binary_voltage_dac_4b_dut": check_simple_binary_dac_4b,
    "vbm1_simple_binary_voltage_dac_4b_tb": check_simple_binary_dac_4b,
    "vbm1_simple_binary_voltage_dac_4b_bugfix": check_simple_binary_dac_4b,
    "vbm1_simple_binary_voltage_dac_4b_e2e": check_simple_binary_dac_4b,
    "vbm1_thermometer_dac_15seg_dut": check_vbm1_thermometer_dac_15seg,
    "vbm1_thermometer_dac_15seg_tb": check_vbm1_thermometer_dac_15seg,
    "vbm1_thermometer_dac_15seg_bugfix": check_vbm1_thermometer_dac_15seg,
    "vbm1_thermometer_dac_15seg_e2e": check_vbm1_thermometer_dac_15seg,
    "vbm1_thermometer_decoder_guarded_dut": check_vbm1_thermometer_decoder_guarded,
    "vbm1_thermometer_decoder_guarded_tb": check_vbm1_thermometer_decoder_guarded,
    "vbm1_thermometer_decoder_guarded_bugfix": check_vbm1_thermometer_decoder_guarded,
    "vbm1_thermometer_decoder_guarded_e2e": check_vbm1_thermometer_decoder_guarded,
    "vbm1_track_hold_aperture_dut": check_vbm1_track_hold_aperture,
    "vbm1_track_hold_aperture_tb": check_vbm1_track_hold_aperture,
    "vbm1_track_hold_aperture_bugfix": check_vbm1_track_hold_aperture,
    "vbm1_track_hold_aperture_e2e": check_vbm1_track_hold_aperture,
    "vbm1_vco_phase_integrator_dut": check_vbm1_vco_phase_integrator,
    "vbm1_vco_phase_integrator_tb": check_vbm1_vco_phase_integrator,
    "vbm1_vco_phase_integrator_e2e": check_vbm1_vco_phase_integrator,
    "vbm1_slew_rate_limiter_dut": check_vbm1_slew_rate_limiter,
    "vbm1_slew_rate_limiter_tb": check_vbm1_slew_rate_limiter,
    "vbm1_slew_rate_limiter_bugfix": check_vbm1_slew_rate_limiter,
    "vbm1_slew_rate_limiter_e2e": check_vbm1_slew_rate_limiter,
    "vbm1_voltage_clamp_dut": check_vbm1_voltage_clamp,
    "vbm1_voltage_clamp_tb": check_vbm1_voltage_clamp,
    "vbm1_voltage_clamp_bugfix": check_vbm1_voltage_clamp,
    "vbm1_voltage_clamp_e2e": check_vbm1_voltage_clamp,
    "wrong_edge_sample_hold_bug": check_sample_hold,
    "inverted_comparator_logic_bug": check_inverted_comparator_logic_bug,
    "swapped_pfd_outputs_bug": check_pfd_updn,
}


RELEASE_CHECK_ALIASES = {
    # Release-v1 designed tasks whose public task IDs differ from legacy/main120 checker IDs.
    # The first group reuses stronger existing waveform checkers.
    "vbr1_l1_burst_clock_source": check_clk_burst_gen,
    "vbr1_l1_clocked_adc_quantizer": check_flash_adc_3b,
    "vbr1_l1_digital_phase_accumulator_with_modulo_wrap": check_phase_accumulator_timer_wrap,
    "vbr1_l1_dither_or_noise_like_deterministic_source": check_noise_gen,
    "vbr1_l1_dwa_dem_encoder": check_dwa_dem_encoder_release,
    "vbr1_l1_hysteresis_comparator": check_cmp_hysteresis,
    "vbr1_l1_offset_comparator": check_release_offset_comparator,
    "vbr1_l1_binary_weighted_voltage_dac": check_simple_binary_dac_4b,
    "vbr1_l1_pipeline_adc_stage": check_pipeline_stage,
    "vbr1_l2_pipeline_adc_chain": check_release_pipeline_adc_chain,
    "vbr1_l1_pfd_small_phase_error_response": check_pfd_small_phase_error_response,
    "vbr1_l1_propagation_delay_comparator": check_cmp_delay,
    "vbr1_l1_ramp_or_step_source": check_bound_step_period_guard,
    "vbr1_l1_clocked_sample_and_hold": check_sample_hold,
    "vbr1_l1_sample_and_hold_with_droop_leakage": check_release_vin_sampled_droop_hold,
    "vbr1_l1_serializer_frame_aligner": check_serializer_frame_alignment,
    "vbr1_l1_strongarm_style_latch_comparator": check_release_strongarm_latch_comparator,
    "vbr1_l1_threshold_comparator": check_release_threshold_comparator,
    "vbr1_l1_unit_element_thermometer_dac": check_vbm1_thermometer_dac_15seg,
    "vbr1_l1_vco_phase_integrator": check_vbm1_vco_phase_integrator,
    "vbr1_l1_window_comparator_detector": check_true_window_comparator,
    "vbr1_l1_xor_phase_detector": check_xor_pd,
    # Release-generic checks are intentionally conservative behavior guards for
    # newly designed source tasks. They prove reset/range/response properties,
    # but should be replaced by stronger per-function checkers before paper claims.
    "vbr1_l1_calibration_deadband_controller": check_release_deadband_calibration,
    "vbr1_l1_charge_pump_abstraction": check_release_charge_pump,
    "vbr1_l1_loop_filter_abstraction": check_release_loop_filter,
    "vbr1_l1_successive_approximation_calibration_search_fsm": check_release_sar_calibration_fsm,
    "vbr1_l2_complete_calibration_loop": check_release_calibration_loop,
    "vbr1_l1_higher_order_filter": check_release_two_pole_filter,
    "vbr1_l1_soft_hysteretic_limiter": check_release_soft_hysteretic_limiter,
    "vbr1_l1_voltage_gain_amplifier": check_release_voltage_gain_amplifier,
    "vbr1_l2_amplifier_filter_chain": check_release_amplifier_filter_chain,
    "vbr1_l1_dac_mismatch_unit_weighting_model": check_release_dac_mismatch_unit_weighting,
    "vbr1_l1_event_pulse_stretcher": check_release_event_pulse_stretcher,
    "vbr1_l2_adc_dac_source_sweep_flow": check_release_quantized_reconstruction,
    "vbr1_l2_converter_front_end": check_release_converter_front_end_chain,
}


for _entry_id, _checker in RELEASE_CHECK_ALIASES.items():
    for _form in ("dut", "tb", "bugfix", "e2e"):
        CHECKS.setdefault(f"{_entry_id}_{_form}", _checker)


RELEASE_FORM_CHECK_ALIASES = {
    "vbr1_l1_strongarm_style_latch_comparator_bugfix": check_strongarm_reset_priority_bug,
    "vbr1_l2_gain_extraction_convergence_measurement_flow_tb": check_gain_extraction,
    "vbr1_l1_gain_estimator_tb": check_gain_extraction,
    "vbr1_l2_weighted_sar_adc_dac_loop_tb": check_sar_adc_dac_weighted_8b,
    "vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow_tb": check_cppll_freq_step_reacquire,
    "vbr1_l2_pll_timing_slice_tb": check_cppll_tracking,
    "vbr1_l2_adc_dac_reconstruction_chain_tb": check_adc_dac_ideal_4b,
    "vbr1_l1_bang_bang_phase_detector_bugfix": check_bbpd,
    "vbr1_l1_edge_interval_timer_tb": check_cross_interval_163p333,
    "vbr1_l1_lfsr_prbs_generator_bugfix": check_prbs7,
    "vbr1_l1_clock_divider_bugfix": check_clk_divider,
    "vbr1_l2_adpll_lock_ratio_hop_timer_flow_tb": check_adpll_ratio_hop,
    "vbr1_l1_capacitive_weighted_sar_feedback_dac_bugfix": check_release_cdac_feedback_dac,
    "vbr1_l1_capacitive_weighted_sar_feedback_dac_e2e": check_release_cdac_feedback_dac,
    "vbr1_l1_capacitive_weighted_sar_feedback_dac_tb": check_release_cdac_feedback_dac,
    "vbr1_l1_lfsr_prbs_generator_tb": check_lfsr,
    "vbr1_l2_event_controller_tb": check_simultaneous_event_order,
    "vbr1_l2_measurement_flow_tb": check_final_step_file_metric,
    "vbr1_l2_serializer_frame_alignment_flow_tb": check_serializer_frame_alignment,
    "vbr1_l1_bang_bang_phase_detector_tb": check_bbpd_data_edge_alignment,
    "vbr1_l2_flash_adc_mini_array_e2e": check_release_flash_adc_mini_array,
    "vbr1_l2_flash_adc_mini_array_tb": check_release_flash_adc_mini_array,
    "vbr1_l2_pipeline_adc_chain_e2e": check_release_pipeline_adc_chain,
    "vbr1_l2_pipeline_adc_chain_tb": check_release_pipeline_adc_chain,
    "vbr1_l2_comparator_measurement_flow_e2e": check_comparator_measurement_flow,
    "vbr1_l2_comparator_measurement_flow_tb": check_comparator_measurement_flow,
    "vbr1_l1_sine_periodic_voltage_source_e2e": check_multitone,
    "vbr1_l1_sine_periodic_voltage_source_tb": check_multitone,
}

CHECKS.update(RELEASE_FORM_CHECK_ALIASES)


def has_behavior_check(task_id: str) -> bool:
    return task_id in CHECKS


def evaluate_behavior(task_id: str, csv_path: Path) -> tuple[float, list[str]]:
    if task_id not in CHECKS:
        return 0.0, [f"no behavior check implemented for {task_id}"]
    if task_id in {"noise_gen", "noise_gen_smoke"}:
        return evaluate_noise_gen_csv(csv_path)
    streaming_result = evaluate_streaming_behavior(task_id, csv_path)
    if streaming_result is not None:
        return streaming_result
    rows = normalize_rows_for_task(task_id, load_csv(csv_path))
    ok, note = CHECKS[task_id](rows)
    return (1.0 if ok else 0.0), [note]


def _behavior_eval_worker(task_id: str, csv_path: str, queue: mp.Queue) -> None:
    """Run checker evaluation in a child process so large CSVs cannot hang scoring."""
    try:
        queue.put(("ok", evaluate_behavior(task_id, Path(csv_path))))
    except Exception as exc:  # pragma: no cover - defensive worker boundary
        queue.put(("error", f"{type(exc).__name__}: {str(exc)[:300]}"))


def evaluate_behavior_with_timeout(
    task_id: str,
    csv_path: Path,
    *,
    timeout_s: int,
) -> tuple[float, list[str]]:
    """Evaluate behavior with a watchdog separate from EVAS simulation timeout.

    `evas simulate` can finish successfully while producing a very large CSV.
    Without a second timeout, Python-side checker parsing can block an entire
    full92 matrix run. Keep this timeout shorter than simulation timeout so one
    pathological waveform becomes a normal task failure instead of a matrix hang.
    """
    direct_max_bytes = int(os.environ.get("VAEVAS_BEHAVIOR_DIRECT_MAX_BYTES", "5000000"))
    try:
        if csv_path.stat().st_size <= direct_max_bytes:
            return evaluate_behavior(task_id, csv_path)
    except OSError:
        pass

    eval_timeout_s = max(10, min(60, max(1, timeout_s // 3)))
    ctx = mp.get_context("spawn")
    queue: mp.Queue = ctx.Queue(maxsize=1)
    proc = ctx.Process(
        target=_behavior_eval_worker,
        args=(task_id, str(csv_path), queue),
    )
    proc.start()
    proc.join(eval_timeout_s)
    if proc.is_alive():
        proc.terminate()
        proc.join(5)
        if proc.is_alive():
            proc.kill()
            proc.join(5)
        return 0.0, [f"behavior_eval_timeout>{eval_timeout_s}s"]
    if queue.empty():
        return 0.0, ["behavior_eval_no_result"]
    status, payload = queue.get()
    if status == "ok":
        return payload
    return 0.0, [f"behavior_eval_error={payload}"]


def _duration_to_seconds(value: str, unit: str) -> float:
    number = float(value)
    normalized = unit.lower()
    if normalized == "ms":
        return number / 1000.0
    if normalized in {"us", "µs"}:
        return number / 1_000_000.0
    if normalized == "ns":
        return number / 1_000_000_000.0
    return number


def parse_evas_timing(text: str) -> dict[str, float]:
    timing: dict[str, float] = {}
    tran_match = re.search(
        r"Tran analysis time:\s*CPU\s*=\s*[\d.]+\s*\w+,\s*elapsed\s*=\s*([\d.]+)\s*(ns|us|µs|ms|s)",
        text,
        re.IGNORECASE,
    )
    total_match = re.search(
        r"Total time:\s*CPU\s*=\s*[\d.]+\s*\w+,\s*elapsed\s*=\s*([\d.]+)\s*(ns|us|µs|ms|s)",
        text,
        re.IGNORECASE,
    )
    steps_match = re.search(r"Number of accepted tran steps\s*=\s*([0-9]+)", text)
    if tran_match:
        timing["tran_elapsed_s"] = _duration_to_seconds(tran_match.group(1), tran_match.group(2))
    if total_match:
        timing["total_elapsed_s"] = _duration_to_seconds(total_match.group(1), total_match.group(2))
    if steps_match:
        timing["accepted_tran_steps"] = float(steps_match.group(1))
    return timing


def run_case(
    task_dir: Path,
    dut_path: Path,
    tb_path: Path,
    *,
    output_root: Path | None = None,
    keep_run_dir: bool = False,
    timeout_s: int = 120,
    task_id_override: str | None = None,
    checker_task_id_override: str | None = None,
) -> dict:
    meta = read_meta(task_dir)
    task_id = task_id_override or meta.get("id") or meta.get("task_id") or task_dir.name
    checker_task_id = (
        checker_task_id_override
        or meta.get("checker_task_id")
        or meta.get("source_checker_task_id")
        or task_id
    )
    scoring = set(meta.get("scoring", ["dut_compile", "tb_compile", "sim_correct"]))

    temp_ctx = tempfile.TemporaryDirectory(prefix=f"{task_id}_")
    try:
        run_dir = Path(temp_ctx.name)
        out_dir = output_root.resolve() if output_root else run_dir / "output"
        out_dir.mkdir(parents=True, exist_ok=True)
        dut_dst, tb_dst = copy_inputs(run_dir, dut_path, tb_path)
        _remove_stale_metric_file(checker_task_id, run_dir)
        proc = run_evas(run_dir, tb_dst, out_dir, timeout_s)
        combined = (proc.stdout or "") + "\n" + (proc.stderr or "")

        dut_compile = 1.0 if "Compiled Verilog-A module:" in combined else 0.0
        tb_compile = 1.0 if ("Transient Analysis" in combined or (out_dir / "tran.csv").exists()) else 0.0

        notes = [f"returncode={proc.returncode}"]
        if dut_compile == 0.0:
            notes.append("dut_not_compiled")
        if tb_compile == 0.0:
            notes.append("tb_not_executed")

        csv_path = out_dir / "tran.csv"
        if "sim_correct" in scoring and proc.returncode == 0 and csv_path.exists():
            sim_correct, behavior_notes = evaluate_behavior_with_timeout(
                checker_task_id,
                csv_path,
                timeout_s=timeout_s,
            )
            notes.extend(behavior_notes)
            metric_result = validate_behavior_side_outputs(checker_task_id, run_dir, csv_path)
            if metric_result is not None:
                metric_ok, metric_note = metric_result
                notes.append(metric_note)
                if not metric_ok:
                    sim_correct = 0.0
        elif "sim_correct" in scoring:
            sim_correct = 0.0
            notes.append("tran.csv missing")
        else:
            sim_correct = 1.0
            notes.append("sim_correct not required by scoring")

        required_axes: list[tuple[str, float]] = []
        if "dut_compile" in scoring or "syntax" in scoring:
            required_axes.append(("dut_compile", dut_compile))
        if "tb_compile" in scoring or "routing" in scoring or "simulation" in scoring:
            required_axes.append(("tb_compile", tb_compile))
        if "sim_correct" in scoring:
            required_axes.append(("sim_correct", sim_correct))

        if required_axes:
            weighted_total = round(sum(score for _, score in required_axes) / len(required_axes), 4)
        else:
            weighted_total = round((dut_compile + tb_compile + sim_correct) / 3.0, 4)

        if ("dut_compile" in scoring or "syntax" in scoring) and dut_compile < 1.0:
            status = "FAIL_DUT_COMPILE"
        elif ("tb_compile" in scoring or "routing" in scoring or "simulation" in scoring) and tb_compile < 1.0:
            status = "FAIL_TB_COMPILE"
        elif "sim_correct" in scoring and sim_correct < 1.0:
            status = "FAIL_SIM_CORRECTNESS"
        else:
            status = "PASS"

        return {
            "task_id": task_id,
            "checker_task_id": checker_task_id,
            "status": status,
            "backend_used": "evas",
            "scores": {
                "dut_compile": dut_compile,
                "tb_compile": tb_compile,
                "sim_correct": sim_correct,
                "weighted_total": weighted_total,
            },
            "artifacts": [
                str(dut_dst),
                str(tb_dst),
                str(out_dir / "tran.csv"),
                str(out_dir / "strobe.txt"),
            ],
            "notes": notes,
            "timing": parse_evas_timing(combined),
            "stdout_tail": combined[-4000:],
        }
    finally:
        if not keep_run_dir:
            temp_ctx.cleanup()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("task_dir")
    ap.add_argument("dut")
    ap.add_argument("tb")
    ap.add_argument("--output-root", default=None)
    ap.add_argument("--keep-run-dir", action="store_true")
    ap.add_argument("--timeout-s", type=int, default=120)
    ap.add_argument("--task-id", default=None)
    ap.add_argument("--checker-task-id", default=None)
    args = ap.parse_args()

    task_dir = Path(args.task_dir).resolve()
    dut_path = Path(args.dut).resolve()
    tb_path = Path(args.tb).resolve()
    output_root = Path(args.output_root).resolve() if args.output_root else None
    result = run_case(
        task_dir,
        dut_path,
        tb_path,
        output_root=output_root,
        keep_run_dir=args.keep_run_dir,
        timeout_s=args.timeout_s,
        task_id_override=args.task_id,
        checker_task_id_override=args.checker_task_id,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
