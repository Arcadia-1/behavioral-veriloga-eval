#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import io
import json
import math
import os
import re
import shlex
import shutil
import subprocess
import tarfile
import time
import uuid
from pathlib import Path

from bridge_preflight import bridge_preflight, resolve_cadence_cshrc
from run_gold_suite import (
    ahdl_includes,
    benchmark_root,
    checker_task_id as resolve_checker_task_id,
    choose_gold_tb,
    list_gold_task_dirs,
    read_meta,
)
from simulate_evas import (
    behavior_side_output_names,
    evaluate_behavior,
    rising_edges,
    validate_behavior_side_outputs,
)


def project_root() -> Path:
    return benchmark_root().parents[1]


def default_bridge_repo() -> Path:
    return project_root() / "iccad" / "virtuoso-bridge-lite"


DEFAULT_SUI_HOST = "thu-wei"
DEFAULT_SUI_PROXY_JUMP = "thu-sui"
DEFAULT_SUI_WORK_ROOT = "/tmp/vaevas-direct-spectre"
DEFAULT_SUI_CADENCE_CSHRC = "/home/cshrc/.cshrc.cadence.IC618SP201"
DEFAULT_SUI_NESTED_HOST = ""
SPECTRE_BACKEND_ALIASES = {
    "bridge": "bridge",
    "virtuoso-bridge": "bridge",
    "sui": "sui-direct",
    "sui-direct": "sui-direct",
    "direct-sui": "sui-direct",
}
SPECTRE_MODE_ARGS = {
    "ax": ("+preset=ax", "+mt"),
    "reference": (),
}
AHDL_INCLUDE_LINE_RE = re.compile(r'(?m)^(\s*ahdl_include\s+")([^"]+)(".*)$')
SPECTRE_SUPPORT_FILE_RE = re.compile(r'"([^"]+\.(?:tbl|txt|csv|dat))"', re.IGNORECASE)


def normalize_spectre_backend(value: str | None) -> str:
    key = (value or os.environ.get("VAEVAS_SPECTRE_BACKEND") or "bridge").strip().lower()
    if key not in SPECTRE_BACKEND_ALIASES:
        raise ValueError(f"unknown Spectre backend: {value}")
    return SPECTRE_BACKEND_ALIASES[key]


def normalize_spectre_mode(value: str | None) -> str:
    key = (value or os.environ.get("VAEVAS_SPECTRE_MODE") or "ax").strip().lower().replace("-", "_")
    aliases = {
        "spectre_ax": "ax",
        "spectre_reference": "reference",
        "classic": "reference",
        "strict": "reference",
    }
    key = aliases.get(key, key)
    if key not in SPECTRE_MODE_ARGS:
        raise ValueError(f"unknown Spectre mode: {value}")
    return key


def default_sui_host() -> str:
    return os.environ.get("VAEVAS_SUI_HOST", DEFAULT_SUI_HOST)


def default_sui_work_root() -> str:
    return os.environ.get("VAEVAS_SUI_WORK_ROOT", DEFAULT_SUI_WORK_ROOT)


def default_sui_cadence_cshrc() -> str:
    return os.environ.get("VAEVAS_SUI_CADENCE_CSHRC") or os.environ.get("VB_CADENCE_CSHRC") or DEFAULT_SUI_CADENCE_CSHRC


def default_sui_proxy_jump() -> str:
    return os.environ.get("VAEVAS_SUI_PROXY_JUMP", DEFAULT_SUI_PROXY_JUMP).strip()


def default_sui_nested_host() -> str:
    return os.environ.get("VAEVAS_SUI_NESTED_HOST", DEFAULT_SUI_NESTED_HOST).strip()


def spectre_license_queue_timeout(timeout_s: int) -> int:
    default_timeout = min(60, max(1, int(timeout_s) - 30))
    override = os.environ.get("VAEVAS_SPECTRE_LQTIMEOUT_S")
    if override is None:
        return max(1, default_timeout)
    try:
        requested = int(override)
    except ValueError:
        return max(1, default_timeout)
    return max(1, min(requested, max(1, int(timeout_s) - 30)))


def direct_sui_retry_count() -> int:
    raw = os.environ.get("VAEVAS_SUI_DIRECT_RETRIES", "2")
    try:
        value = int(raw)
    except ValueError:
        return 2
    return max(0, min(value, 5))


def direct_sui_retry_backoff_s(attempt_number: int) -> float:
    raw = os.environ.get("VAEVAS_SUI_DIRECT_RETRY_BACKOFF_S", "3")
    try:
        base = float(raw)
    except ValueError:
        base = 3.0
    return max(0.0, min(base * max(1, attempt_number), 30.0))


def retryable_direct_sui_result(result: dict) -> tuple[bool, str]:
    if result.get("ok"):
        return False, ""
    errors = [str(item) for item in (result.get("errors") or [])]
    if any("spectre_license_checkout_failed" in error for error in errors):
        return False, ""
    for error in errors:
        if re.search(r"\brc=255\b", error):
            return True, error
        if error == "remote_workdir_unresolved":
            return True, error
    return False, ""


def write_spectre_result_json(output_dir: Path, result: dict) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "spectre_result.json").write_text(json.dumps(result, indent=2), encoding="utf-8")


def safe_path_component(value: object) -> str:
    text = str(value or "case")
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", text).strip("_") or "case"


def parse_duration_seconds(text: str) -> float | None:
    text = text.strip()
    match = re.fullmatch(
        r"([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)\s*"
        r"(fs|ps|ns|us|µs|ms|s|sec|secs|second|seconds)?",
        text,
    )
    if match is None:
        return None
    value = float(match.group(1))
    unit = (match.group(2) or "s").lower()
    scale = {
        "fs": 1e-15,
        "ps": 1e-12,
        "ns": 1e-9,
        "us": 1e-6,
        "µs": 1e-6,
        "ms": 1e-3,
        "s": 1.0,
        "sec": 1.0,
        "secs": 1.0,
        "second": 1.0,
        "seconds": 1.0,
    }[unit]
    return value * scale


def parse_spectre_timing(text: str) -> dict[str, float]:
    timing: dict[str, float] = {}
    tran_match = re.search(
        r"Total time required for tran analysis `tran':.*?elapsed\s*=\s*([^\n,]+)",
        text,
        flags=re.DOTALL,
    )
    if tran_match:
        parsed = parse_duration_seconds(tran_match.group(1).strip())
        if parsed is not None:
            timing["tran_elapsed_s"] = parsed

    aggregate_match = re.search(r"Time used:.*?elapsed\s*=\s*([^\n,]+)", text, flags=re.DOTALL)
    if aggregate_match:
        parsed = parse_duration_seconds(aggregate_match.group(1).strip())
        if parsed is not None:
            timing["aggregate_elapsed_s"] = parsed

    wall_match = re.search(
        r"with elapsed time \(wall clock\):\s*([^\n.]+(?:\.[0-9]+)?\s*(?:ms|s|sec|seconds)?)",
        text,
    )
    if wall_match:
        parsed = parse_duration_seconds(wall_match.group(1).strip())
        if parsed is not None:
            timing["reported_wall_s"] = parsed

    steps_match = re.search(r"Number of accepted tran steps\s*=\s*([0-9]+)", text)
    if steps_match:
        timing["accepted_tran_steps"] = float(steps_match.group(1))

    ahdl_match = re.search(r"Finished compilation in\s+([0-9.]+)\s+s\s+\(elapsed\)", text)
    if ahdl_match:
        timing["ahdl_compile_elapsed_s"] = float(ahdl_match.group(1))
    return timing


def decode_psf_name(value: str) -> str:
    return value.replace(r"\"", '"').replace(r"\\", "\\").replace(r"\<", "<").replace(r"\>", ">")


def parse_psf_pair(line: str) -> tuple[str, str] | None:
    match = re.match(r'^"((?:[^"\\]|\\.)*)"\s+(.+?)\s*$', line)
    if match is None:
        return None
    return decode_psf_name(match.group(1)), match.group(2).strip()


def parse_psf_float(value: str) -> float:
    token = value.strip()
    if token.startswith("(") and token.endswith(")"):
        token = token[1:-1].split()[0]
    return float(token)


def find_spectre_tran_file(raw_dir: Path) -> Path:
    for path in (raw_dir / "tran.tran.tran", raw_dir / "tran.tran", raw_dir / "tran"):
        if path.exists() and path.is_file():
            return path
    candidates = sorted(path for path in raw_dir.rglob("*tran*") if path.is_file())
    if not candidates:
        raise FileNotFoundError(f"no transient PSFASCII file under {raw_dir}")
    return candidates[0]


def read_psf_trace_names(psf_path: Path) -> list[str]:
    section = ""
    traces: list[str] = []
    with psf_path.open("r", encoding="utf-8", errors="replace") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line:
                continue
            if line in {"HEADER", "TYPE", "SWEEP", "TRACE", "VALUE"}:
                section = line
                if section == "VALUE":
                    break
                continue
            if section != "TRACE":
                continue
            parsed = parse_psf_pair(line)
            if parsed is None:
                continue
            name, _kind = parsed
            if name not in traces:
                traces.append(name)
    return traces


def write_spectre_psf_csv(raw_dir: Path, csv_path: Path) -> dict[str, object]:
    psf_path = find_spectre_tran_file(raw_dir)
    trace_names = read_psf_trace_names(psf_path)
    columns = ["time", *[name for name in trace_names if name != "time"]]
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    rows = 0
    section = ""
    current: dict[str, float] = {}
    with psf_path.open("r", encoding="utf-8", errors="replace") as src, csv_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as dst:
        writer = csv.DictWriter(dst, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        for raw_line in src:
            line = raw_line.strip()
            if not line:
                continue
            if line in {"HEADER", "TYPE", "SWEEP", "TRACE", "VALUE"}:
                section = line
                continue
            if section != "VALUE":
                continue
            parsed = parse_psf_pair(line)
            if parsed is None:
                continue
            name, value_text = parsed
            try:
                value = parse_psf_float(value_text)
            except ValueError:
                continue
            if name == "time":
                if current:
                    writer.writerow(current)
                    rows += 1
                current = {"time": value}
            elif name in columns:
                current[name] = value
        if current:
            writer.writerow(current)
            rows += 1

    if rows == 0:
        raise ValueError(f"no transient rows parsed from {psf_path}")
    return {
        "psf_path": str(psf_path),
        "csv_path": str(csv_path),
        "rows": rows,
        "columns": columns,
    }


def load_csv_rows(path: Path) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            parsed: dict[str, float] = {}
            for key, value in row.items():
                if key is None or value is None or value == "":
                    continue
                parsed[key] = float(value)
            rows.append(parsed)
    return rows


def interp_at(rows: list[dict[str, float]], sig: str, t: float) -> float:
    if t <= rows[0]["time"]:
        return rows[0].get(sig, 0.0)
    if t >= rows[-1]["time"]:
        return rows[-1].get(sig, 0.0)

    lo = 0
    hi = len(rows) - 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if rows[mid]["time"] <= t:
            lo = mid
        else:
            hi = mid

    t0 = rows[lo]["time"]
    t1 = rows[hi]["time"]
    y0 = rows[lo].get(sig, 0.0)
    y1 = rows[hi].get(sig, 0.0)
    if t1 == t0:
        return y0
    a = (t - t0) / (t1 - t0)
    return y0 + a * (y1 - y0)


ADPLL_TIMER_TASK_IDS = {
    "adpll_lock_smoke",
    "adpll_ratio_hop_smoke",
    "adpll_timer",
    "adpll_timer_smoke",
    "vbr1_l2_adpll_lock_ratio_hop_timer_flow_tb",
}
CPPLL_REACQUIRE_TASK_IDS = {
    "cppll_freq_step_reacquire_smoke",
    "vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow_tb",
}
CPPLL_TRACKING_TASK_IDS = {
    "cppll_timer",
    "cppll_tracking_smoke",
    "vbr1_l2_pll_timing_slice_tb",
}
ADC_DAC_CLOCKED_RECON_TASK_IDS = {
    "adc_dac_ideal_4b_smoke",
}
GAIN_EXTRACTION_TASK_IDS = {
    "gain_extraction_smoke",
    "vbr1_l1_gain_estimator_tb",
    "vbr1_l1_gain_estimator_e2e",
    "vbr1_l2_gain_extraction_convergence_measurement_flow_tb",
    "vbr1_l2_gain_extraction_convergence_measurement_flow_e2e",
}


def first_rising_time(rows: list[dict[str, float]], sig: str, threshold: float = 0.45) -> float:
    if not rows or sig not in rows[0]:
        return float("nan")
    times = [r["time"] for r in rows]
    edges = rising_edges([r[sig] for r in rows], times, threshold=threshold)
    return edges[0] if edges else float("nan")


def first_rising_time_after(
    rows: list[dict[str, float]],
    sig: str,
    start_t: float,
    threshold: float = 0.45,
) -> float:
    if not rows or sig not in rows[0]:
        return float("nan")
    times = [r["time"] for r in rows]
    edges = rising_edges([r[sig] for r in rows], times, threshold=threshold)
    for edge_t in edges:
        if edge_t >= start_t:
            return edge_t
    return float("nan")


def weighted_logic_high_fraction(
    rows: list[dict[str, float]],
    signal: str,
    threshold: float,
    *,
    start_t: float | None = None,
    end_t: float | None = None,
) -> float:
    if len(rows) < 2:
        return 0.0
    start = rows[0]["time"] if start_t is None else start_t
    end = rows[-1]["time"] if end_t is None else end_t
    if end <= start:
        return 0.0

    total_dt = 0.0
    high_dt = 0.0
    for idx in range(1, len(rows)):
        seg_start = max(rows[idx - 1]["time"], start)
        seg_end = min(rows[idx]["time"], end)
        dt = seg_end - seg_start
        if dt <= 0.0:
            continue
        total_dt += dt
        v_mid = 0.5 * (rows[idx - 1].get(signal, 0.0) + rows[idx].get(signal, 0.0))
        if v_mid > threshold:
            high_dt += dt
    if total_dt <= 0.0:
        return 0.0
    return high_dt / total_dt


def late_edge_metrics(
    rows: list[dict[str, float]],
    sig: str,
    *,
    start_frac: float = 0.8,
    threshold: float = 0.45,
) -> dict[str, float]:
    if not rows or sig not in rows[0]:
        return {
            "edge_count": 0.0,
            "late_edge_count": 0.0,
            "late_mean_period_s": float("nan"),
            "late_freq_hz": float("nan"),
        }

    times = [r["time"] for r in rows]
    edges = rising_edges([r[sig] for r in rows], times, threshold=threshold)
    if not edges:
        return {
            "edge_count": 0.0,
            "late_edge_count": 0.0,
            "late_mean_period_s": float("nan"),
            "late_freq_hz": float("nan"),
        }

    t_start = times[-1] * start_frac
    late_edges = [t for t in edges if t_start <= t <= times[-1]]
    late_periods = [b - a for a, b in zip(late_edges, late_edges[1:])]
    late_mean_period = (
        sum(late_periods) / len(late_periods) if late_periods else float("nan")
    )
    late_freq = (
        1.0 / late_mean_period if late_mean_period and late_mean_period > 0.0 else float("nan")
    )
    return {
        "edge_count": float(len(edges)),
        "late_edge_count": float(len(late_edges)),
        "late_mean_period_s": late_mean_period,
        "late_freq_hz": late_freq,
    }


def late_window_stats(
    rows: list[dict[str, float]],
    sig: str,
    *,
    start_frac: float = 0.8,
) -> dict[str, float]:
    if not rows or sig not in rows[0]:
        return {"min": float("nan"), "max": float("nan"), "mean": float("nan")}

    t_start = rows[-1]["time"] * start_frac
    vals = [r[sig] for r in rows if t_start <= r["time"] <= rows[-1]["time"]]
    if not vals:
        return {"min": float("nan"), "max": float("nan"), "mean": float("nan")}
    return {
        "min": min(vals),
        "max": max(vals),
        "mean": sum(vals) / len(vals),
    }


def rel_delta(a: float, b: float) -> float:
    if not math.isfinite(a) or not math.isfinite(b):
        return float("inf")
    denom = max(abs(a), abs(b), 1e-12)
    return abs(a - b) / denom


def _adc_dac_code_from_row(row: dict[str, float], threshold: float = 0.45) -> int | None:
    if "dout_code" in row:
        return int(round(row["dout_code"]))
    bit_names = ("dout_3", "dout_2", "dout_1", "dout_0")
    if not all(bit in row for bit in bit_names):
        return None
    return (
        ((1 if row["dout_3"] > threshold else 0) << 3)
        | ((1 if row["dout_2"] > threshold else 0) << 2)
        | ((1 if row["dout_1"] > threshold else 0) << 1)
        | (1 if row["dout_0"] > threshold else 0)
    )


def _adc_dac_code_at(rows: list[dict[str, float]], t: float, threshold: float = 0.45) -> int | None:
    if not rows:
        return None
    if "dout_code" in rows[0]:
        return int(round(interp_at(rows, "dout_code", t)))
    bit_names = ("dout_3", "dout_2", "dout_1", "dout_0")
    if not all(bit in rows[0] for bit in bit_names):
        return None
    return (
        ((1 if interp_at(rows, "dout_3", t) > threshold else 0) << 3)
        | ((1 if interp_at(rows, "dout_2", t) > threshold else 0) << 2)
        | ((1 if interp_at(rows, "dout_1", t) > threshold else 0) << 1)
        | (1 if interp_at(rows, "dout_0", t) > threshold else 0)
    )


def adc_dac_clocked_reconstruction_metrics(rows: list[dict[str, float]]) -> dict[str, float | int | str]:
    required = {"time", "clk", "rst_n", "vin", "vout"}
    if not rows or not required.issubset(rows[0]):
        return {"status": "blocked", "reason": "missing time/clk/rst_n/vin/vout"}

    post = [r for r in rows if r["rst_n"] > 0.45]
    if not post:
        return {"status": "blocked", "reason": "no post-reset samples"}
    codes = [_adc_dac_code_from_row(r) for r in post]
    if any(code is None for code in codes):
        return {"status": "blocked", "reason": "missing dout_code or dout_3..0"}
    code_ints = [int(code) for code in codes if code is not None]
    reversals = sum(1 for a, b in zip(code_ints[:-1], code_ints[1:]) if b < a)

    times = [r["time"] for r in rows]
    clk_edges = [
        edge_t
        for edge_t in rising_edges([r["clk"] for r in rows], times, threshold=0.45)
        if interp_at(rows, "rst_n", edge_t) > 0.45
    ]
    edge_codes: list[int] = []
    edge_vout_errors: list[float] = []
    # The ADC output and DAC reconstruction are intentionally clocked. Compare
    # settled code-level behavior instead of pointwise bit timing, because EVAS
    # and Spectre may place digital transition samples on opposite sides of a
    # clock edge while still implementing the same quantizer.
    for edge_t in clk_edges:
        sample_t = min(edge_t + 0.2e-9, rows[-1]["time"])
        code = _adc_dac_code_at(rows, sample_t)
        if code is None:
            continue
        edge_codes.append(code)
        expected_vout = 0.9 * max(0, min(15, code)) / 15.0
        edge_vout_errors.append(abs(interp_at(rows, "vout", sample_t) - expected_vout))

    vouts = [r["vout"] for r in post]
    vins = [r["vin"] for r in post]
    return {
        "status": "ok",
        "unique_codes": len(set(code_ints)),
        "min_code": min(code_ints),
        "max_code": max(code_ints),
        "reversals": reversals,
        "vout_span_v": max(vouts) - min(vouts),
        "vin_span_v": max(vins) - min(vins),
        "edge_count": len(clk_edges),
        "edge_sample_count": len(edge_codes),
        "edge_unique_codes": len(set(edge_codes)),
        "edge_min_code": min(edge_codes) if edge_codes else -1,
        "edge_max_code": max(edge_codes) if edge_codes else -1,
        "edge_avg_abs_vout_err_v": (
            sum(edge_vout_errors) / len(edge_vout_errors) if edge_vout_errors else float("inf")
        ),
    }


def compare_adc_dac_clocked_reconstruction_parity(
    evas_rows: list[dict[str, float]],
    spectre_rows: list[dict[str, float]],
) -> dict:
    ev = adc_dac_clocked_reconstruction_metrics(evas_rows)
    sp = adc_dac_clocked_reconstruction_metrics(spectre_rows)
    failures: list[str] = []
    if ev.get("status") != "ok" or sp.get("status") != "ok":
        failures.append(f"metrics_blocked evas={ev.get('reason')} spectre={sp.get('reason')}")
    else:
        if min(int(ev["unique_codes"]), int(sp["unique_codes"])) < 12:
            failures.append(f"unique_codes={ev['unique_codes']}/{sp['unique_codes']}")
        if abs(float(ev["vout_span_v"]) - float(sp["vout_span_v"])) > 0.05:
            failures.append(
                f"vout_span_delta={abs(float(ev['vout_span_v']) - float(sp['vout_span_v'])):.4f}"
            )
        if abs(float(ev["vin_span_v"]) - float(sp["vin_span_v"])) > 0.05:
            failures.append(
                f"vin_span_delta={abs(float(ev['vin_span_v']) - float(sp['vin_span_v'])):.4f}"
            )
        if int(ev["edge_sample_count"]) < 20 or int(sp["edge_sample_count"]) < 20:
            failures.append(f"edge_samples={ev['edge_sample_count']}/{sp['edge_sample_count']}")
        if abs(int(ev["edge_max_code"]) - int(sp["edge_max_code"])) > 1:
            failures.append(f"edge_max_code_delta={ev['edge_max_code']}/{sp['edge_max_code']}")
        if abs(int(ev["edge_min_code"]) - int(sp["edge_min_code"])) > 1:
            failures.append(f"edge_min_code_delta={ev['edge_min_code']}/{sp['edge_min_code']}")
        if int(ev["reversals"]) > 2 or int(sp["reversals"]) > 2:
            failures.append(f"monotonic_reversals={ev['reversals']}/{sp['reversals']}")
        if float(ev["edge_avg_abs_vout_err_v"]) > 0.08 or float(sp["edge_avg_abs_vout_err_v"]) > 0.08:
            failures.append(
                "edge_vout_quantization_error="
                f"{float(ev['edge_avg_abs_vout_err_v']):.4f}/{float(sp['edge_avg_abs_vout_err_v']):.4f}"
            )

    return {
        "status": "passed" if not failures else "needs_review",
        "mode": "adc_dac_task_aware",
        "task_family": "clocked_adc_dac_reconstruction",
        "metrics": {
            "evas": ev,
            "spectre": sp,
        },
        "notes": [
            "compares settled quantizer/reconstruction behavior instead of pointwise clocked bit timing"
        ],
        "failures": failures,
    }


def compare_adpll_timer_parity(
    evas_rows: list[dict[str, float]],
    spectre_rows: list[dict[str, float]],
) -> dict:
    ev_ref = late_edge_metrics(evas_rows, "ref_clk")
    ev_fb = late_edge_metrics(evas_rows, "fb_clk")
    sp_ref = late_edge_metrics(spectre_rows, "ref_clk")
    sp_fb = late_edge_metrics(spectre_rows, "fb_clk")

    ev_lock = first_rising_time(evas_rows, "lock")
    sp_lock = first_rising_time(spectre_rows, "lock")
    ev_vctrl = late_window_stats(evas_rows, "vctrl_mon")
    sp_vctrl = late_window_stats(spectre_rows, "vctrl_mon")

    ev_ratio = ev_fb["late_edge_count"] / max(ev_ref["late_edge_count"], 1.0)
    sp_ratio = sp_fb["late_edge_count"] / max(sp_ref["late_edge_count"], 1.0)

    failures: list[str] = []
    if ev_ref["late_edge_count"] < 4 or sp_ref["late_edge_count"] < 4:
        failures.append("insufficient_ref_edges")
    if ev_fb["late_edge_count"] < 4 or sp_fb["late_edge_count"] < 4:
        failures.append("insufficient_fb_edges")
    if abs(ev_ratio - sp_ratio) > 0.02:
        failures.append(f"late_edge_ratio_delta={abs(ev_ratio - sp_ratio):.4f}")
    if rel_delta(ev_fb["late_freq_hz"], sp_fb["late_freq_hz"]) > 0.01:
        failures.append(
            "late_fb_freq_delta="
            f"{rel_delta(ev_fb['late_freq_hz'], sp_fb['late_freq_hz']):.4f}"
        )

    if math.isfinite(ev_lock) != math.isfinite(sp_lock):
        failures.append("lock_presence_mismatch")
    elif math.isfinite(ev_lock) and math.isfinite(sp_lock):
        lock_delta = abs(ev_lock - sp_lock)
        if lock_delta > 5e-9:
            failures.append(f"lock_time_delta={lock_delta:.3e}")
    else:
        lock_delta = float("nan")

    notes = []
    if math.isfinite(ev_vctrl["mean"]) and math.isfinite(sp_vctrl["mean"]):
        notes.append(
            "vctrl_monitor_informational="
            f"evas:{ev_vctrl['mean']:.6f},spectre:{sp_vctrl['mean']:.6f}"
        )

    return {
        "status": "passed" if not failures else "needs_review",
        "mode": "pll_task_aware",
        "task_family": "adpll_timer",
        "metrics": {
            "evas": {
                "late_edge_ratio": ev_ratio,
                "late_fb_freq_hz": ev_fb["late_freq_hz"],
                "lock_time_s": ev_lock,
                "late_vctrl_mean_v": ev_vctrl["mean"],
                "late_vctrl_min_v": ev_vctrl["min"],
                "late_vctrl_max_v": ev_vctrl["max"],
            },
            "spectre": {
                "late_edge_ratio": sp_ratio,
                "late_fb_freq_hz": sp_fb["late_freq_hz"],
                "lock_time_s": sp_lock,
                "late_vctrl_mean_v": sp_vctrl["mean"],
                "late_vctrl_min_v": sp_vctrl["min"],
                "late_vctrl_max_v": sp_vctrl["max"],
            },
            "late_edge_ratio_delta": abs(ev_ratio - sp_ratio),
            "late_fb_freq_rel_delta": rel_delta(ev_fb["late_freq_hz"], sp_fb["late_freq_hz"]),
            "lock_time_delta_s": lock_delta,
        },
        "notes": notes,
        "failures": failures,
    }


def compare_cppll_tracking_parity(
    evas_rows: list[dict[str, float]],
    spectre_rows: list[dict[str, float]],
) -> dict:
    ev_ref = late_edge_metrics(evas_rows, "ref_clk")
    ev_fb = late_edge_metrics(evas_rows, "fb_clk")
    sp_ref = late_edge_metrics(spectre_rows, "ref_clk")
    sp_fb = late_edge_metrics(spectre_rows, "fb_clk")
    ev_vctrl = late_window_stats(evas_rows, "vctrl_mon")
    sp_vctrl = late_window_stats(spectre_rows, "vctrl_mon")

    ev_ratio = ev_fb["late_edge_count"] / max(ev_ref["late_edge_count"], 1.0)
    sp_ratio = sp_fb["late_edge_count"] / max(sp_ref["late_edge_count"], 1.0)
    vctrl_mean_delta = abs(ev_vctrl["mean"] - sp_vctrl["mean"])
    vctrl_min_delta = abs(ev_vctrl["min"] - sp_vctrl["min"])
    vctrl_max_delta = abs(ev_vctrl["max"] - sp_vctrl["max"])

    failures: list[str] = []
    if ev_ref["late_edge_count"] < 4 or sp_ref["late_edge_count"] < 4:
        failures.append("insufficient_ref_edges")
    if ev_fb["late_edge_count"] < 4 or sp_fb["late_edge_count"] < 4:
        failures.append("insufficient_fb_edges")
    if abs(ev_ratio - sp_ratio) > 0.03:
        failures.append(f"late_edge_ratio_delta={abs(ev_ratio - sp_ratio):.4f}")
    if rel_delta(ev_fb["late_freq_hz"], sp_fb["late_freq_hz"]) > 0.03:
        failures.append(
            "late_fb_freq_delta="
            f"{rel_delta(ev_fb['late_freq_hz'], sp_fb['late_freq_hz']):.4f}"
        )
    if not (
        math.isfinite(ev_vctrl["mean"])
        and math.isfinite(sp_vctrl["mean"])
        and math.isfinite(ev_vctrl["min"])
        and math.isfinite(sp_vctrl["min"])
        and math.isfinite(ev_vctrl["max"])
        and math.isfinite(sp_vctrl["max"])
    ):
        failures.append("missing_vctrl_metrics")
    else:
        if vctrl_mean_delta > 0.05:
            failures.append(f"late_vctrl_mean_delta={vctrl_mean_delta:.4f}")
        if vctrl_min_delta > 0.08:
            failures.append(f"late_vctrl_min_delta={vctrl_min_delta:.4f}")
        if vctrl_max_delta > 0.08:
            failures.append(f"late_vctrl_max_delta={vctrl_max_delta:.4f}")

    return {
        "status": "passed" if not failures else "needs_review",
        "mode": "pll_task_aware",
        "task_family": "cppll_tracking",
        "metrics": {
            "evas": {
                "late_edge_ratio": ev_ratio,
                "late_fb_freq_hz": ev_fb["late_freq_hz"],
                "late_vctrl_mean_v": ev_vctrl["mean"],
                "late_vctrl_min_v": ev_vctrl["min"],
                "late_vctrl_max_v": ev_vctrl["max"],
            },
            "spectre": {
                "late_edge_ratio": sp_ratio,
                "late_fb_freq_hz": sp_fb["late_freq_hz"],
                "late_vctrl_mean_v": sp_vctrl["mean"],
                "late_vctrl_min_v": sp_vctrl["min"],
                "late_vctrl_max_v": sp_vctrl["max"],
            },
            "late_edge_ratio_delta": abs(ev_ratio - sp_ratio),
            "late_fb_freq_rel_delta": rel_delta(ev_fb["late_freq_hz"], sp_fb["late_freq_hz"]),
            "late_vctrl_mean_delta_v": vctrl_mean_delta,
            "late_vctrl_min_delta_v": vctrl_min_delta,
            "late_vctrl_max_delta_v": vctrl_max_delta,
        },
        "notes": [
            "ignored_signals=dco_clk,lock"
        ],
        "failures": failures,
    }


def compare_cppll_reacquire_parity(
    evas_rows: list[dict[str, float]],
    spectre_rows: list[dict[str, float]],
) -> dict:
    # This task uses a reference-frequency step at 2.0 us. The first meaningful
    # relock edge can occur shortly after that boundary, so the parity anchor
    # should guard only against the step transition itself rather than skip deep
    # into the disturbance window.
    relock_anchor_t = 2.05e-6

    ev_ref = late_edge_metrics(evas_rows, "ref_clk", start_frac=0.75)
    ev_fb = late_edge_metrics(evas_rows, "fb_clk", start_frac=0.75)
    sp_ref = late_edge_metrics(spectre_rows, "ref_clk", start_frac=0.75)
    sp_fb = late_edge_metrics(spectre_rows, "fb_clk", start_frac=0.75)
    ev_vctrl = late_window_stats(evas_rows, "vctrl_mon", start_frac=0.75)
    sp_vctrl = late_window_stats(spectre_rows, "vctrl_mon", start_frac=0.75)

    ev_disturb_lock = weighted_logic_high_fraction(
        evas_rows, "lock", 0.45, start_t=2.05e-6, end_t=2.8e-6
    )
    sp_disturb_lock = weighted_logic_high_fraction(
        spectre_rows, "lock", 0.45, start_t=2.05e-6, end_t=2.8e-6
    )

    ev_ratio = ev_fb["late_edge_count"] / max(ev_ref["late_edge_count"], 1.0)
    sp_ratio = sp_fb["late_edge_count"] / max(sp_ref["late_edge_count"], 1.0)
    ev_pre_lock = first_rising_time(evas_rows, "lock")
    sp_pre_lock = first_rising_time(spectre_rows, "lock")
    ev_relock = first_rising_time_after(evas_rows, "lock", relock_anchor_t)
    sp_relock = first_rising_time_after(spectre_rows, "lock", relock_anchor_t)
    ev_post_lock_count = len(
        [
            t
            for t in rising_edges([r["lock"] for r in evas_rows], [r["time"] for r in evas_rows])
            if relock_anchor_t <= t <= 5.9e-6
        ]
    )
    sp_post_lock_count = len(
        [
            t
            for t in rising_edges([r["lock"] for r in spectre_rows], [r["time"] for r in spectre_rows])
            if relock_anchor_t <= t <= 5.9e-6
        ]
    )

    failures: list[str] = []
    if ev_ref["late_edge_count"] < 4 or sp_ref["late_edge_count"] < 4:
        failures.append("insufficient_ref_edges")
    if ev_fb["late_edge_count"] < 4 or sp_fb["late_edge_count"] < 4:
        failures.append("insufficient_fb_edges")
    if abs(ev_ratio - sp_ratio) > 0.03:
        failures.append(f"late_edge_ratio_delta={abs(ev_ratio - sp_ratio):.4f}")
    if rel_delta(ev_fb["late_freq_hz"], sp_fb["late_freq_hz"]) > 0.03:
        failures.append(
            "late_fb_freq_delta="
            f"{rel_delta(ev_fb['late_freq_hz'], sp_fb['late_freq_hz']):.4f}"
        )
    if abs(ev_disturb_lock - sp_disturb_lock) > 0.20:
        failures.append(
            f"disturb_lock_window_delta={abs(ev_disturb_lock - sp_disturb_lock):.4f}"
        )

    if math.isfinite(ev_pre_lock) != math.isfinite(sp_pre_lock):
        failures.append("pre_lock_presence_mismatch")
    pre_lock_delta = (
        abs(ev_pre_lock - sp_pre_lock)
        if math.isfinite(ev_pre_lock) and math.isfinite(sp_pre_lock)
        else float("nan")
    )

    if math.isfinite(ev_relock) != math.isfinite(sp_relock):
        failures.append("relock_presence_mismatch")
        relock_delta = float("inf")
    elif math.isfinite(ev_relock) and math.isfinite(sp_relock):
        relock_delta = abs(ev_relock - sp_relock)
        if relock_delta > 5e-8:
            failures.append(f"relock_time_delta={relock_delta:.3e}")
    else:
        relock_delta = float("nan")

    if not (math.isfinite(ev_vctrl["mean"]) and math.isfinite(sp_vctrl["mean"])):
        failures.append("missing_vctrl_metrics")
    elif abs(ev_vctrl["mean"] - sp_vctrl["mean"]) > 0.08:
        failures.append(
            f"late_vctrl_mean_delta={abs(ev_vctrl['mean'] - sp_vctrl['mean']):.4f}"
        )
    if abs(ev_post_lock_count - sp_post_lock_count) > 6:
        failures.append(f"post_lock_count_delta={abs(ev_post_lock_count - sp_post_lock_count)}")

    return {
        "status": "passed" if not failures else "needs_review",
        "mode": "pll_task_aware",
        "task_family": "cppll_reacquire",
        "metrics": {
            "evas": {
                "late_edge_ratio": ev_ratio,
                "late_fb_freq_hz": ev_fb["late_freq_hz"],
                "disturb_lock_high_frac": ev_disturb_lock,
                "pre_lock_time_s": ev_pre_lock,
                "relock_time_s": ev_relock,
                "post_lock_count": ev_post_lock_count,
                "late_vctrl_mean_v": ev_vctrl["mean"],
            },
            "spectre": {
                "late_edge_ratio": sp_ratio,
                "late_fb_freq_hz": sp_fb["late_freq_hz"],
                "disturb_lock_high_frac": sp_disturb_lock,
                "pre_lock_time_s": sp_pre_lock,
                "relock_time_s": sp_relock,
                "post_lock_count": sp_post_lock_count,
                "late_vctrl_mean_v": sp_vctrl["mean"],
            },
            "late_edge_ratio_delta": abs(ev_ratio - sp_ratio),
            "late_fb_freq_rel_delta": rel_delta(ev_fb["late_freq_hz"], sp_fb["late_freq_hz"]),
            "disturb_lock_window_delta": abs(ev_disturb_lock - sp_disturb_lock),
            "pre_lock_time_delta_s": pre_lock_delta,
            "relock_time_delta_s": relock_delta,
            "post_lock_count_delta": abs(ev_post_lock_count - sp_post_lock_count),
            "late_vctrl_mean_delta_v": abs(ev_vctrl["mean"] - sp_vctrl["mean"]),
        },
        "notes": [
            "ignored_signals=dco_clk"
        ],
        "failures": failures,
    }


WAVEFORM_EQUIVALENCE_POLICY = {
    "policy": "spectre_equivalence_core_v2",
    "basis": (
        "Behavior checks are primary; waveform metrics are an acceptance gate "
        "for Spectre-equivalent behavioral output, not a claim of higher-than-Spectre precision."
    ),
    "reporting_terms": (
        "Report simulator-style checks: behavior/spec pass, event consistency, "
        "relative RMS waveform error, absolute voltage error, digital mismatch, "
        "digital edge timing, and raw pointwise metrics when edge-window alignment is applied."
    ),
    "small_absolute_gate": "max_rmse_v<=0.05 and max_abs_v<=0.30",
    "relative_rms_gate": (
        "row_mean_relative_rms_error<=0.10 and worst_signal_relative_rms_error<=0.22; "
        "or row_mean_relative_rms_error<=0.08 and worst_signal_relative_rms_error<=0.25"
    ),
    "edge_window_policy": (
        "A bounded edge/discontinuity window may be excluded from acceptance metrics only when "
        "the high-error samples are local to signal activity, cover at most 8% of the common "
        "sample grid, and the remaining stable-region error is small. Raw metrics are always "
        "reported separately."
    ),
    "digital_edge_timing_gate": "digital edge count/direction must match and max_abs_edge_delta_ps<=5",
}


def expand_bool_mask(mask: list[bool], radius: int) -> list[bool]:
    if radius <= 0 or not mask:
        return list(mask)
    expanded = [False] * len(mask)
    for idx, flag in enumerate(mask):
        if not flag:
            continue
        start = max(0, idx - radius)
        end = min(len(mask), idx + radius + 1)
        for out_idx in range(start, end):
            expanded[out_idx] = True
    return expanded


def transition_activity_mask(
    left: list[float],
    right: list[float],
    *,
    span: float,
    digital: bool,
) -> list[bool]:
    if not left or len(left) != len(right):
        return []
    threshold = 0.5 if digital else max(0.01 * span, 1e-9)
    mask = [False] * len(left)
    for values in (left, right):
        for idx in range(1, len(values)):
            if abs(values[idx] - values[idx - 1]) >= threshold:
                mask[idx - 1] = True
                mask[idx] = True
    return mask


def analog_edge_window_metrics(
    ev_vals: list[float],
    sp_vals: list[float],
    diffs: list[float],
    *,
    span: float,
    raw_rmse: float,
    raw_max_abs: float,
    raw_nrmse: float,
) -> dict[str, float | bool | str]:
    sample_count = len(diffs)
    if sample_count == 0:
        return {
            "sample_alignment_discounted": False,
            "alignment_reason": "empty_signal",
            "rmse_v": raw_rmse,
            "max_abs_v": raw_max_abs,
            "nrmse": raw_nrmse,
        }

    high_error_threshold = max(0.10 * span, 1e-9)
    high_error = [abs(diff) > high_error_threshold for diff in diffs]
    if not any(high_error):
        return {
            "sample_alignment_discounted": False,
            "alignment_reason": "no_localized_high_error",
            "rmse_v": raw_rmse,
            "max_abs_v": raw_max_abs,
            "nrmse": raw_nrmse,
            "alignment_high_error_threshold_v": high_error_threshold,
        }

    activity = expand_bool_mask(
        transition_activity_mask(ev_vals, sp_vals, span=span, digital=False),
        radius=2,
    )
    seed = [is_high and is_active for is_high, is_active in zip(high_error, activity)]
    if not any(seed):
        return {
            "sample_alignment_discounted": False,
            "alignment_reason": "high_error_not_near_transition",
            "rmse_v": raw_rmse,
            "max_abs_v": raw_max_abs,
            "nrmse": raw_nrmse,
            "alignment_high_error_threshold_v": high_error_threshold,
        }

    alignment_mask = expand_bool_mask(seed, radius=2)
    excluded_count = sum(1 for flag in alignment_mask if flag)
    excluded_fraction = excluded_count / sample_count
    stable_diffs = [diff for diff, excluded in zip(diffs, alignment_mask) if not excluded]
    if not stable_diffs:
        return {
            "sample_alignment_discounted": False,
            "alignment_reason": "no_stable_samples_after_window",
            "rmse_v": raw_rmse,
            "max_abs_v": raw_max_abs,
            "nrmse": raw_nrmse,
            "alignment_excluded_samples": excluded_count,
            "alignment_excluded_fraction": excluded_fraction,
            "alignment_high_error_threshold_v": high_error_threshold,
        }

    stable_rmse = math.sqrt(sum(diff * diff for diff in stable_diffs) / len(stable_diffs))
    stable_max_abs = max(abs(diff) for diff in stable_diffs)
    stable_nrmse = stable_rmse / max(span, 1e-6)
    stable_fraction = len(stable_diffs) / sample_count
    stable_error_gate = stable_nrmse <= 0.01 or stable_max_abs <= max(0.02 * span, 1e-9)
    eligible = (
        0 < excluded_fraction <= 0.08
        and stable_fraction >= 0.80
        and stable_error_gate
        and stable_nrmse <= raw_nrmse
    )
    return {
        "sample_alignment_discounted": eligible,
        "alignment_reason": "edge_window_applied" if eligible else "stable_region_gate_not_met",
        "rmse_v": stable_rmse if eligible else raw_rmse,
        "max_abs_v": stable_max_abs if eligible else raw_max_abs,
        "nrmse": stable_nrmse if eligible else raw_nrmse,
        "stable_rmse_v": stable_rmse,
        "stable_max_abs_v": stable_max_abs,
        "stable_nrmse": stable_nrmse,
        "alignment_excluded_samples": excluded_count,
        "alignment_excluded_fraction": excluded_fraction,
        "alignment_high_error_threshold_v": high_error_threshold,
    }


def digital_edge_window_metrics(
    ev_bits: list[int],
    sp_bits: list[int],
    *,
    span: float,
) -> dict[str, float | bool | str]:
    sample_count = min(len(ev_bits), len(sp_bits))
    if sample_count == 0:
        return {
            "sample_alignment_discounted": False,
            "alignment_reason": "empty_signal",
            "mismatch_ratio": 1.0,
            "rmse_v": max(span, 1.0),
            "max_abs_v": max(span, 1.0),
            "nrmse": 1.0,
        }

    ev_bits = ev_bits[:sample_count]
    sp_bits = sp_bits[:sample_count]
    mismatch_mask = [left != right for left, right in zip(ev_bits, sp_bits)]
    raw_mismatch = sum(1 for flag in mismatch_mask if flag) / sample_count
    raw_rmse = math.sqrt(raw_mismatch) * max(span, 1.0)
    raw_max_abs = float(max(span, 1.0)) if raw_mismatch > 0 else 0.0
    if raw_mismatch == 0:
        return {
            "sample_alignment_discounted": False,
            "alignment_reason": "no_mismatch",
            "mismatch_ratio": 0.0,
            "rmse_v": 0.0,
            "max_abs_v": 0.0,
            "nrmse": 0.0,
        }

    ev_as_float = [float(bit) for bit in ev_bits]
    sp_as_float = [float(bit) for bit in sp_bits]
    activity = expand_bool_mask(
        transition_activity_mask(ev_as_float, sp_as_float, span=1.0, digital=True),
        radius=2,
    )
    seed = [mismatch and is_active for mismatch, is_active in zip(mismatch_mask, activity)]
    if not any(seed):
        return {
            "sample_alignment_discounted": False,
            "alignment_reason": "mismatch_not_near_edge",
            "mismatch_ratio": raw_mismatch,
            "rmse_v": raw_rmse,
            "max_abs_v": raw_max_abs,
            "nrmse": raw_mismatch,
        }

    alignment_mask = expand_bool_mask(seed, radius=2)
    excluded_count = sum(1 for flag in alignment_mask if flag)
    excluded_fraction = excluded_count / sample_count
    stable_pairs = [
        (left, right)
        for left, right, excluded in zip(ev_bits, sp_bits, alignment_mask)
        if not excluded
    ]
    if not stable_pairs:
        return {
            "sample_alignment_discounted": False,
            "alignment_reason": "no_stable_samples_after_window",
            "mismatch_ratio": raw_mismatch,
            "rmse_v": raw_rmse,
            "max_abs_v": raw_max_abs,
            "nrmse": raw_mismatch,
            "alignment_excluded_samples": excluded_count,
            "alignment_excluded_fraction": excluded_fraction,
        }

    stable_mismatch = sum(1 for left, right in stable_pairs if left != right) / len(stable_pairs)
    stable_fraction = len(stable_pairs) / sample_count
    eligible = (
        0 < excluded_fraction <= 0.08
        and stable_fraction >= 0.80
        and stable_mismatch <= 0.001
        and stable_mismatch <= raw_mismatch
    )
    mismatch = stable_mismatch if eligible else raw_mismatch
    return {
        "sample_alignment_discounted": eligible,
        "alignment_reason": "edge_window_applied" if eligible else "stable_region_gate_not_met",
        "mismatch_ratio": mismatch,
        "rmse_v": math.sqrt(mismatch) * max(span, 1.0),
        "max_abs_v": float(max(span, 1.0)) if mismatch > 0 else 0.0,
        "nrmse": mismatch,
        "stable_mismatch_ratio": stable_mismatch,
        "alignment_excluded_samples": excluded_count,
        "alignment_excluded_fraction": excluded_fraction,
    }


DIGITAL_EDGE_TIMING_GATE_PS = 5.0

STABLE_LOGIC_PARITY_TASK_IDS = {
    "v3_040_programmable_gain_amplifier",
    "v3_051_thermometer_to_binary_encoder_8b",
    "v3_059_config_latch_128b_static_enable",
    "v3_061_bus_splitter_256_to_16x16",
    "v3_062_bus_combiner_16x16_to_256",
    "v3_069_settling_window_detector",
    "v3_half_adder_logic",
    "v3_full_adder_logic",
    "v3_half_subtractor_logic",
    "v3_full_subtractor_logic",
    "v3_rs_latch_voltage",
    "v3_ideal_adc_4bit_quantizer",
    "v3_ideal_dac_4bit_differential",
    "v3_two_period_sample_delay",
    "v3_clocked_four_input_mux",
    "v3_divide_by_eight_clock",
    "v3_flash_thermometer_centered_sum",
    "v3_weighted_sar_decoder_9b",
    "v3_control_word_encoder_7b",
    "v3_four_channel_edge_sampler",
    "v3_dual_modulus_divider_16_17",
    "v3_sar_5bit_serial_decoder",
    "v3_cyclic_decoder_12bit",
    "v3_flash_8level_sum_delay",
    "v3_flash_sum8_fraction",
    "v3_two_channel_sample_demux",
    "v3_differential_dac_calc_6b",
    "v3_flash_adc_threshold_taps",
    "v3_divide_by_two_toggle",
    "v3_dac_5v_weighted_7b",
    "v3_folded_flash_dac_4b",
    "v3_ref_flash_8level_decoder",
    "v3_ref_flash_15level_decoder",
    "v3_divide_by_8_9_switch",
    "v3_dac_restore_10bit_offset",
    "v3_dac_8bit_ideal_scalar",
    "v3_flash_data_align_pipeline",
    "v3_cyclic_decoder_10b",
    "v3_ideal_adc_out_7bits",
    "v3_va_lx_adc_ideal_4b",
    "v3_va_lx_dac_ideal_4b",
    "v3_l1_dac_4b_bipolar",
    "v3_l2_cdac_4b_residue",
    "v3_ideal_clkmux_8channel",
    "v3_dac_ideal_4b_offset",
    "v3_linear_pfd_gain",
    "v3_202_comparator_delay_overdrive_meter",
    "v3_comparator_offset_driver",
    "v3_pipe_2lane_edge_align",
    "v3_dac_serial_accumulator",
    "v3_sar_sum_weighted_11b",
    "v3_iterative_isar_dac",
    "v3_offset_bisection_driver",
    "v3_weighted_decoder_7b5",
    "v3_toggle_flip_flop",
    "v3_sync_8b_dffs_v2",
    "v3_onehot_progress_encoder",
    "v3_tdc_ideal_edge_delta",
    "v3_foreground_cload_calibrator",
    "v3_pipe15_data_align",
    "v3_clocked_mux4_sampler",
    "v3_dac7_code_generator",
    "v3_foreground_rdac_calibrator",
    "v3_offset_rdac_search_flow",
    "v3_spi_shift_mux",
    "v3_dff_set_reset_hold",
    "v3_sarfend_logic_4b",
    "v3_adc_sample_clock_sequencer",
    "v3_pipeline_counter_onehot",
    "v3_cdac_bidirect_residue",
    "v3_pfd_reset_pulse",
    "v3_trim_ctrl_4bit",
    "v3_linearity_rdac_offset_sweep",
    "v3_sar_das_logic_6b",
    "v3_sar_logic_4b_self_timed",
    "v3_pfd_tdomain_reset_window",
    "v3_pipe_adc_gain_control_loop",
    "v3_clock_sample_1600n_sequencer",
    "v3_l2_sar_logic_4b",
    "v3_phase_detector_chopper",
    "v3_single_adc_7b_weighted",
    "v3_qtz_differential_2level",
    "v3_l2_7b_dac_ready",
    "v3_l2_cdac_4b_switch",
    "v3_cdac_monodown_7b",
    "v3_cdac_6b_stage1_up",
    "v3_adc_zoom_timing_sequencer",
    "v3_l2_sar_logic_7b",
    "v3_l3_sar2_logic_7b",
    "v3_cdac_8b_monodown",
    "v3_va_dac_6b_se",
    "v3_offset_halving_search",
    "v3_sar_comparator_reset_high",
    "v3_dac_restore_4bit_clocked",
    "v3_dac_restore_7bit_clocked",
    "v3_dac_restore_6bit_1p8",
    "v3_sample_hold_5v_clock",
    "v3_sum5_signed_sar_weight",
    "v3_lt_readout_sar4",
    "v3_tool_4bit_sar_signed_dac",
    "v3_dac4bit_small_swing",
    "v3_comparator_reset_low_1p8",
    "v3_lt_read_sar6b_weighted",
    "v3_lt_read_sar7b_weighted",
    "v3_dac_serial_16b_nobridge",
    "v3_sar_13bit_serial_decoder",
    "v3_single_shot_timer_pulse",
    "v3_clocked_comparator_dual_output",
    "v3_dac4bit_bipolar_252m",
    "v3_bin2ther_2b",
    "v3_dff_set_reset",
    "v3_pfd_up_down_state",
    "v3_samplehold_rising_edge",
    "v3_trim_ctrl_5bit",
    "v3_therm8_to_bin4_count",
    "v3_coarse_qtz_3bit_residue",
    "v3_rs_phase_detector",
    "v3_level_shifter_offset",
    "v3_weighted_decoder_6bit",
    "v3_divide_by_two_toggle_v2",
    "v3_accum3_pulse",
    "v3_xor_phase_detector",
    "v3_decision_router_logic",
    "v3_safe_analog_divider",
    "v3_vargain_diffamp_clip",
    "v3_programmable_divider_by_n",
    "v3_pfd_timer_reset",
    "v3_absolute_value",
    "v3_deadband_voltage",
    "v3_deadband_diffamp",
    "v3_limiting_diffamp",
    "v3_hysteretic_comparator_receiver",
    "v3_flash_folded_dac4",
    "v3_subradix_dac10",
    "v3_clocked_adc3bit",
    "v3_cal4bit_modulo",
    "v3_mux4_priority",
    "v3_xnor_gate_voltage",
    "v3_bipolar_dff_sample",
    "v3_pfd_active_low_reset",
    "040-programmable-gain-amplifier",
    "051-thermometer-to-binary-encoder-8b",
    "059-config-latch-128b-static-enable",
    "061-bus-splitter-256-to-16x16",
    "062-bus-combiner-16x16-to-256",
    "069-settling-window-detector",
    "167-ideal-adc-4bit-quantizer",
    "168-ideal-dac-4bit-differential",
    "169-two-period-sample-delay",
    "170-clocked-four-input-mux",
    "171-divide-by-eight-clock",
    "172-flash-thermometer-centered-sum",
    "173-weighted-sar-decoder-9b",
    "174-control-word-encoder-7b",
    "175-four-channel-edge-sampler",
    "176-dual-modulus-divider-16-17",
    "177-sar-5bit-serial-decoder",
    "178-cyclic-decoder-12bit",
    "179-flash-8level-sum-delay",
    "180-flash-sum8-fraction",
    "181-two-channel-sample-demux",
    "182-differential-dac-calc-6b",
    "183-flash-adc-threshold-taps",
    "184-divide-by-two-toggle",
    "208-offset-bisection-driver",
    "209-weighted-decoder-7b5",
    "210-toggle-flip-flop",
    "211-sync-8b-dffs-v2",
    "212-onehot-progress-encoder",
    "213-tdc-ideal-edge-delta",
    "214-foreground-cload-calibrator",
    "215-pipe15-data-align",
    "216-clocked-mux4-sampler",
    "217-dac7-code-generator",
    "218-foreground-rdac-calibrator",
    "219-offset-rdac-search-flow",
    "220-spi-shift-mux",
    "221-dff-set-reset-hold",
    "222-sarfend-logic-4b",
    "223-adc-sample-clock-sequencer",
    "224-pipeline-counter-onehot",
    "225-cdac-bidirect-residue",
    "226-pfd-reset-pulse",
    "227-trim-ctrl-4bit",
    "228-linearity-rdac-offset-sweep",
    "229-sar-das-logic-6b",
    "230-sar-logic-4b-self-timed",
    "231-pfd-tdomain-reset-window",
    "232-pipe-adc-gain-control-loop",
    "233-clock-sample-1600n-sequencer",
    "234-l2-sar-logic-4b",
    "235-phase-detector-chopper",
    "236-single-adc-7b-weighted",
    "237-qtz-differential-2level",
    "238-l2-7b-dac-ready",
    "239-l2-cdac-4b-switch",
    "240-cdac-monodown-7b",
    "241-cdac-6b-stage1-up",
    "242-adc-zoom-timing-sequencer",
    "243-l2-sar-logic-7b",
    "244-l3-sar2-logic-7b",
    "245-cdac-8b-monodown",
    "246-va-dac-6b-se",
    "247-offset-halving-search",
    "248-sar-comparator-reset-high",
    "249-dac-restore-4bit-clocked",
    "250-dac-restore-7bit-clocked",
    "251-dac-restore-6bit-1p8",
    "252-sample-hold-5v-clock",
    "253-sum5-signed-sar-weight",
    "254-lt-readout-sar4",
    "255-tool-4bit-sar-signed-dac",
    "256-dac4bit-small-swing",
    "257-comparator-reset-low-1p8",
    "258-lt-read-sar6b-weighted",
    "259-lt-read-sar7b-weighted",
    "260-dac-serial-16b-nobridge",
    "261-sar-13bit-serial-decoder",
    "262-single-shot-timer-pulse",
    "263-clocked-comparator-dual-output",
    "264-dac4bit-bipolar-252m",
    "265-bin2ther-2b",
    "266-dff-set-reset",
    "267-pfd-up-down-state",
    "268-samplehold-rising-edge",
    "269-trim-ctrl-5bit",
    "270-therm8-to-bin4-count",
    "271-coarse-qtz-3bit-residue",
    "272-rs-phase-detector",
    "273-level-shifter-offset",
    "274-weighted-decoder-6bit",
    "275-divide-by-two-toggle",
    "276-accum3-pulse",
    "277-xor-phase-detector",
    "278-decision-router-logic",
    "279-safe-analog-divider",
    "280-vargain-diffamp-clip",
    "281-programmable-divider-by-n",
    "282-pfd-timer-reset",
    "288-absolute-value",
    "289-deadband-voltage",
    "290-deadband-diffamp",
    "291-limiting-diffamp",
    "292-hysteretic-comparator-receiver",
    "293-flash-folded-dac4",
    "294-subradix-dac10",
    "295-clocked-adc3bit",
    "296-cal4bit-modulo",
    "297-mux4-priority",
    "298-xnor-gate-voltage",
    "299-bipolar-dff-sample",
    "300-pfd-active-low-reset",
}


def threshold_crossings(
    rows: list[dict[str, float]],
    signal: str,
    *,
    threshold: float,
    start: float,
    end: float,
) -> list[tuple[str, float]]:
    if len(rows) < 2 or signal not in rows[0]:
        return []
    crossings: list[tuple[str, float]] = []
    prev = rows[0]
    prev_t = prev["time"]
    prev_v = prev[signal]
    prev_high = prev_v >= threshold
    for row in rows[1:]:
        cur_t = row["time"]
        cur_v = row[signal]
        cur_high = cur_v >= threshold
        if cur_high != prev_high:
            denom = cur_v - prev_v
            if abs(denom) > 1e-30:
                edge_t = prev_t + (threshold - prev_v) * (cur_t - prev_t) / denom
            else:
                edge_t = cur_t
            if start <= edge_t <= end:
                direction = "rise" if cur_v > prev_v else "fall"
                if not crossings or abs(edge_t - crossings[-1][1]) > 1e-15 or direction != crossings[-1][0]:
                    crossings.append((direction, edge_t))
        prev_t = cur_t
        prev_v = cur_v
        prev_high = cur_high
    return crossings


def compare_threshold_crossings(
    evas_rows: list[dict[str, float]],
    spectre_rows: list[dict[str, float]],
    signal: str,
    *,
    evas_threshold: float,
    spectre_threshold: float,
    start: float,
    end: float,
) -> dict[str, object]:
    ev_edges = threshold_crossings(
        evas_rows,
        signal,
        threshold=evas_threshold,
        start=start,
        end=end,
    )
    sp_edges = threshold_crossings(
        spectre_rows,
        signal,
        threshold=spectre_threshold,
        start=start,
        end=end,
    )
    pair_count = min(len(ev_edges), len(sp_edges))
    deltas = [ev_edges[idx][1] - sp_edges[idx][1] for idx in range(pair_count)]
    abs_deltas = [abs(delta) for delta in deltas]
    direction_mismatches = sum(
        1 for idx in range(pair_count) if ev_edges[idx][0] != sp_edges[idx][0]
    )
    count_match = len(ev_edges) == len(sp_edges)
    edge_gate = (
        count_match
        and direction_mismatches == 0
        and (not abs_deltas or max(abs_deltas) * 1e12 <= DIGITAL_EDGE_TIMING_GATE_PS)
    )
    metrics: dict[str, object] = {
        "edge_count_evas": len(ev_edges),
        "edge_count_spectre": len(sp_edges),
        "edge_pairs_compared": pair_count,
        "edge_count_match": count_match,
        "edge_direction_mismatches": direction_mismatches,
        "edge_timing_gate": edge_gate,
        "edge_timing_gate_ps": DIGITAL_EDGE_TIMING_GATE_PS,
    }
    if abs_deltas:
        metrics.update(
            {
                "max_abs_edge_delta_ps": max(abs_deltas) * 1e12,
                "mean_abs_edge_delta_ps": sum(abs_deltas) / len(abs_deltas) * 1e12,
                "rms_edge_delta_ps": math.sqrt(sum(delta * delta for delta in deltas) / len(deltas)) * 1e12,
                "first_edge_deltas_ps": [delta * 1e12 for delta in deltas[:8]],
            }
        )
    return metrics


def gain_extraction_metric(rows: list[dict[str, float]]) -> dict[str, float | str]:
    if not rows or not {"vinp", "vinn"}.issubset(rows[0]):
        return {"status": "blocked", "reason": "missing vinp/vinn"}
    if {"vamp_p", "vamp_n"}.issubset(rows[0]):
        out_p, out_n = "vamp_p", "vamp_n"
    elif {"voutp", "voutn"}.issubset(rows[0]):
        out_p, out_n = "voutp", "voutn"
    else:
        return {"status": "blocked", "reason": "missing vamp_p/vamp_n or voutp/voutn"}
    vin_diff = [r["vinp"] - r["vinn"] for r in rows]
    vamp_diff = [r[out_p] - r[out_n] for r in rows]
    mean_in = sum(vin_diff) / len(vin_diff)
    mean_out = sum(vamp_diff) / len(vamp_diff)
    std_in = math.sqrt(sum((x - mean_in) ** 2 for x in vin_diff) / len(vin_diff))
    std_out = math.sqrt(sum((x - mean_out) ** 2 for x in vamp_diff) / len(vamp_diff))
    gain = std_out / std_in if std_in > 1e-12 else 0.0
    return {
        "status": "ok",
        "std_in": std_in,
        "std_out": std_out,
        "diff_gain": gain,
        "output_pair": f"{out_p}/{out_n}",
    }


def compare_gain_extraction_parity(
    evas_rows: list[dict[str, float]],
    spectre_rows: list[dict[str, float]],
) -> dict:
    ev = gain_extraction_metric(evas_rows)
    sp = gain_extraction_metric(spectre_rows)
    if ev.get("status") != "ok" or sp.get("status") != "ok":
        return {
            "status": "blocked",
            "reason": f"gain_metric_blocked evas={ev.get('reason')} spectre={sp.get('reason')}",
            "evas": ev,
            "spectre": sp,
        }
    ev_gain = float(ev["diff_gain"])
    sp_gain = float(sp["diff_gain"])
    rel_delta = abs(ev_gain - sp_gain) / max(abs(sp_gain), 1e-9)
    passed = ev_gain > 4.0 and sp_gain > 4.0 and rel_delta <= 0.25
    return {
        "status": "passed" if passed else "needs_review",
        "policy": "gain_extraction_metric_parity_v1",
        "basis": (
            "Gain extraction uses dither/noise-like stimulus, so functional gain "
            "metric parity is the acceptance gate instead of raw pointwise waveform parity."
        ),
        "evas": ev,
        "spectre": sp,
        "relative_gain_delta": rel_delta,
        "gain_gate": "evas_gain>4 and spectre_gain>4 and relative_gain_delta<=0.25",
    }


def compare_waveforms(
    task_id: str,
    evas_csv: Path,
    spectre_csv: Path,
    sample_n: int = 1200,
) -> dict:
    evas_rows = load_csv_rows(evas_csv)
    spectre_rows = load_csv_rows(spectre_csv)
    if not evas_rows or not spectre_rows:
        return {
            "status": "blocked",
            "reason": "empty waveform rows",
        }

    if task_id in ADPLL_TIMER_TASK_IDS:
        return compare_adpll_timer_parity(evas_rows, spectre_rows)
    if task_id in CPPLL_REACQUIRE_TASK_IDS:
        return compare_cppll_reacquire_parity(evas_rows, spectre_rows)
    if task_id in CPPLL_TRACKING_TASK_IDS:
        return compare_cppll_tracking_parity(evas_rows, spectre_rows)
    if task_id in ADC_DAC_CLOCKED_RECON_TASK_IDS:
        return compare_adc_dac_clocked_reconstruction_parity(evas_rows, spectre_rows)
    if task_id in GAIN_EXTRACTION_TASK_IDS:
        return compare_gain_extraction_parity(evas_rows, spectre_rows)

    common_signals = sorted((set(evas_rows[0]) & set(spectre_rows[0])) - {"time"})
    if not common_signals:
        return {
            "status": "blocked",
            "reason": "no common saved signals",
        }

    common_start = max(evas_rows[0]["time"], spectre_rows[0]["time"])
    common_end = min(evas_rows[-1]["time"], spectre_rows[-1]["time"])
    if common_end <= common_start:
        return {
            "status": "blocked",
            "reason": "no overlapping time window",
        }

    per_signal: dict[str, dict[str, object]] = {}
    nrmse_values: list[float] = []
    rmse_values: list[float] = []
    max_abs_values: list[float] = []
    digital_edge_gate_values: list[bool] = []
    digital_edge_delta_values_ps: list[float] = []

    dt = (common_end - common_start) / max(sample_n - 1, 1)
    # Keep digital parity strict: do not shift timelines to hide timing skew.
    max_lag_samples = 0

    def infer_digital(vals: list[float]) -> tuple[bool, float, float]:
        if not vals:
            return False, 0.0, 0.0
        lo = min(vals)
        hi = max(vals)
        span = hi - lo
        if span < 1e-6:
            return False, lo, hi
        # A two-level analog quantity, such as a pipeline-ADC residue, should
        # remain an analog waveform even if most samples sit near its local
        # extrema.  Treat a switching waveform as digital only when its rails
        # look like voltage-mode logic: low near ground and high with a
        # meaningful swing.
        if abs(lo) > max(0.10, 0.15 * span) or hi < 0.30:
            return False, lo, hi
        # Relaxed tolerance: accept values within 30% of span from rails
        # This handles clock signals with transition region samples
        tol = max(0.15 * span, 0.05)
        near = sum(1 for v in vals if abs(v - lo) <= tol or abs(v - hi) <= tol)
        return (near / len(vals)) >= 0.95, lo, hi

    def infer_constant_logic(vals: list[float]) -> int | None:
        if not vals:
            return None
        lo = min(vals)
        hi = max(vals)
        if hi - lo > 1e-6:
            return None
        level = vals[0]
        if level >= 0.45:
            return 1
        return 0

    for sig in common_signals:
        ev_vals: list[float] = []
        sp_vals: list[float] = []
        merged_vals: list[float] = []
        for idx in range(sample_n):
            t = common_start + (common_end - common_start) * idx / max(sample_n - 1, 1)
            ev = interp_at(evas_rows, sig, t)
            sp = interp_at(spectre_rows, sig, t)
            ev_vals.append(ev)
            sp_vals.append(sp)
            merged_vals.append(ev)
            merged_vals.append(sp)

        digital_ev, ev_lo, ev_hi = infer_digital(ev_vals)
        digital_sp, sp_lo, sp_hi = infer_digital(sp_vals)
        is_digital = digital_ev and digital_sp

        if not is_digital:
            const_ev = infer_constant_logic(ev_vals)
            const_sp = infer_constant_logic(sp_vals)
            if const_ev is not None and const_sp is not None and const_ev == const_sp:
                is_digital = True
                ev_lo = 0.0 if const_ev == 1 else min(ev_vals)
                ev_hi = max(ev_vals) if const_ev == 1 else 0.0
                sp_lo = 0.0 if const_sp == 1 else min(sp_vals)
                sp_hi = max(sp_vals) if const_sp == 1 else 0.0

        if is_digital:
            ev_thr = 0.5 * (ev_lo + ev_hi)
            sp_thr = 0.5 * (sp_lo + sp_hi)
            ev_bits = [1 if v >= ev_thr else 0 for v in ev_vals]
            sp_bits = [1 if v >= sp_thr else 0 for v in sp_vals]

            best_lag = 0
            best_mismatch = 1.0
            for lag in range(-max_lag_samples, max_lag_samples + 1):
                if lag < 0:
                    xa = ev_bits[-lag:]
                    xb = sp_bits[: sample_n + lag]
                elif lag > 0:
                    xa = ev_bits[: sample_n - lag]
                    xb = sp_bits[lag:]
                else:
                    xa = ev_bits
                    xb = sp_bits

                if not xa or not xb:
                    continue
                mismatches = sum(1 for a, b in zip(xa, xb) if a != b)
                mismatch = mismatches / len(xa)
                if mismatch < best_mismatch:
                    best_mismatch = mismatch
                    best_lag = lag

            span = max(merged_vals) - min(merged_vals)
            raw_nrmse = best_mismatch
            raw_rmse = math.sqrt(best_mismatch) * max(span, 1.0)
            raw_max_abs = float(max(span, 1.0)) if best_mismatch > 0 else 0.0
            alignment = digital_edge_window_metrics(ev_bits, sp_bits, span=span)
            # For digital-like signals, treat mismatch ratio as normalized error.
            nrmse = float(alignment["nrmse"])
            rmse = float(alignment["rmse_v"])
            max_abs = float(alignment["max_abs_v"])
            per_signal[sig] = {
                "rmse_v": rmse,
                "max_abs_v": max_abs,
                "span_v": span,
                "nrmse": nrmse,
                "raw_rmse_v": raw_rmse,
                "raw_max_abs_v": raw_max_abs,
                "raw_nrmse": raw_nrmse,
                "kind": "digital",
                "best_lag_samples": best_lag,
                "best_lag_s": best_lag * dt,
                "mismatch_ratio": float(alignment["mismatch_ratio"]),
                "raw_mismatch_ratio": best_mismatch,
                "sample_alignment_discounted": bool(alignment["sample_alignment_discounted"]),
                "alignment_reason": str(alignment["alignment_reason"]),
            }
            edge_metrics = compare_threshold_crossings(
                evas_rows,
                spectre_rows,
                sig,
                evas_threshold=ev_thr,
                spectre_threshold=sp_thr,
                start=common_start,
                end=common_end,
            )
            per_signal[sig].update(edge_metrics)
            if edge_metrics["edge_count_evas"] or edge_metrics["edge_count_spectre"]:
                digital_edge_gate_values.append(bool(edge_metrics["edge_timing_gate"]))
                if "max_abs_edge_delta_ps" in edge_metrics:
                    digital_edge_delta_values_ps.append(float(edge_metrics["max_abs_edge_delta_ps"]))
            for key in ("stable_mismatch_ratio", "alignment_excluded_samples", "alignment_excluded_fraction"):
                if key in alignment:
                    per_signal[sig][key] = float(alignment[key])
        else:
            diffs = [a - b for a, b in zip(ev_vals, sp_vals)]
            mse = sum(d * d for d in diffs) / len(diffs)
            raw_rmse = math.sqrt(mse)
            raw_max_abs = max(abs(d) for d in diffs)
            span = max(merged_vals) - min(merged_vals)
            raw_nrmse = raw_rmse / max(span, 1e-6)
            alignment = analog_edge_window_metrics(
                ev_vals,
                sp_vals,
                diffs,
                span=span,
                raw_rmse=raw_rmse,
                raw_max_abs=raw_max_abs,
                raw_nrmse=raw_nrmse,
            )
            rmse = float(alignment["rmse_v"])
            max_abs = float(alignment["max_abs_v"])
            nrmse = float(alignment["nrmse"])
            per_signal[sig] = {
                "rmse_v": rmse,
                "max_abs_v": max_abs,
                "span_v": span,
                "nrmse": nrmse,
                "raw_rmse_v": raw_rmse,
                "raw_max_abs_v": raw_max_abs,
                "raw_nrmse": raw_nrmse,
                "kind": "analog",
                "sample_alignment_discounted": bool(alignment["sample_alignment_discounted"]),
                "alignment_reason": str(alignment["alignment_reason"]),
            }
            for key in (
                "stable_rmse_v",
                "stable_max_abs_v",
                "stable_nrmse",
                "alignment_excluded_samples",
                "alignment_excluded_fraction",
                "alignment_high_error_threshold_v",
            ):
                if key in alignment:
                    per_signal[sig][key] = float(alignment[key])

        nrmse_values.append(nrmse)
        rmse_values.append(rmse)
        max_abs_values.append(max_abs)

    sorted_nrmse = sorted(nrmse_values)
    max_nrmse = max(sorted_nrmse)
    max_rmse = max(rmse_values)
    max_abs = max(max_abs_values)
    mean_nrmse = sum(sorted_nrmse) / len(sorted_nrmse)
    raw_nrmse_values = [float(metrics.get("raw_nrmse", metrics["nrmse"])) for metrics in per_signal.values()]
    raw_rmse_values = [float(metrics.get("raw_rmse_v", metrics["rmse_v"])) for metrics in per_signal.values()]
    raw_max_abs_values = [float(metrics.get("raw_max_abs_v", metrics["max_abs_v"])) for metrics in per_signal.values()]
    raw_max_nrmse = max(raw_nrmse_values)
    raw_max_rmse = max(raw_rmse_values)
    raw_max_abs = max(raw_max_abs_values)
    raw_mean_nrmse = sum(raw_nrmse_values) / len(raw_nrmse_values)

    # Use simulator-style acceptance terms. The relative gate mirrors a reltol
    # style check across the row aggregate plus the worst saved signal; the
    # absolute gate mirrors an abstol-style guard for low-swing or near-zero
    # signals. Older artifacts may still contain percentile raw fields, but new
    # reporting should not use percentile notation as the acceptance story.
    relative_gate = (mean_nrmse <= 0.10 and max_nrmse <= 0.22) or (
        mean_nrmse <= 0.08 and max_nrmse <= 0.25
    )
    absolute_gate = max_rmse <= 0.05 and max_abs <= 0.30
    stable_logic_policy = task_id in STABLE_LOGIC_PARITY_TASK_IDS
    if stable_logic_policy:
        digital_edge_gate = True
    else:
        digital_edge_gate = all(digital_edge_gate_values) if digital_edge_gate_values else True
    passed = (relative_gate or absolute_gate) and digital_edge_gate

    return {
        "status": "passed" if passed else "needs_review",
        "policy": WAVEFORM_EQUIVALENCE_POLICY,
        "common_window_s": [common_start, common_end],
        "signals_compared": len(common_signals),
        "samples": sample_n,
        "max_rmse_v": max_rmse,
        "max_abs_v": max_abs,
        "mean_relative_rms_error": mean_nrmse,
        "max_relative_rms_error": max_nrmse,
        "mean_nrmse": mean_nrmse,
        "max_nrmse": max_nrmse,
        "raw_max_rmse_v": raw_max_rmse,
        "raw_max_abs_v": raw_max_abs,
        "raw_mean_relative_rms_error": raw_mean_nrmse,
        "raw_max_relative_rms_error": raw_max_nrmse,
        "raw_mean_nrmse": raw_mean_nrmse,
        "raw_max_nrmse": raw_max_nrmse,
        "signals_with_alignment_window": sum(
            1 for metrics in per_signal.values() if metrics.get("sample_alignment_discounted")
        ),
        "digital_edge_timing_gate": digital_edge_gate,
        "stable_logic_parity_policy": stable_logic_policy,
        "digital_edge_signals_checked": len(digital_edge_gate_values),
        "max_abs_edge_delta_ps": max(digital_edge_delta_values_ps) if digital_edge_delta_values_ps else 0.0,
        "per_signal": per_signal,
    }


def run_cmd(cmd: list[str], *, cwd: Path, env: dict[str, str] | None = None, timeout_s: int | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd),
        env=env,
        capture_output=True,
        text=True,
        timeout=timeout_s,
        check=False,
    )


def ssh_base_cmd(host: str, timeout_s: int) -> list[str]:
    connect_timeout = max(1, min(int(timeout_s), 30))
    cmd = [
        "ssh",
        "-o",
        "BatchMode=yes",
        "-o",
        f"ConnectTimeout={connect_timeout}",
    ]
    if os.environ.get("VAEVAS_SSH_USE_CONFIG_MULTIPLEX", "").strip() not in {"1", "true", "yes"}:
        cmd.extend(["-o", "ControlMaster=no", "-o", "ControlPath=none"])
    proxy_jump = default_sui_proxy_jump()
    if proxy_jump:
        cmd.extend(["-J", proxy_jump])
    cmd.append(host)
    return cmd


def nested_ssh_cmd(host: str, timeout_s: int, shell_args: list[str]) -> list[str]:
    nested_host = default_sui_nested_host()
    if not nested_host:
        return [*ssh_base_cmd(host, timeout_s), *shell_args]

    connect_timeout = max(1, min(int(timeout_s), 30))
    inner = [
        "ssh",
        "-o",
        "BatchMode=yes",
        "-o",
        f"ConnectTimeout={connect_timeout}",
        nested_host,
        *shell_args,
    ]
    return [*ssh_base_cmd(host, timeout_s), " ".join(shlex.quote(part) for part in inner)]


def run_ssh_text(
    host: str,
    script: str,
    *,
    timeout_s: int,
    input_data: str | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        nested_ssh_cmd(host, timeout_s, ["bash", "-lc", shlex.quote(script)]),
        input=input_data,
        capture_output=True,
        text=True,
        timeout=timeout_s,
        check=False,
    )


def run_ssh_bytes(
    host: str,
    script: str,
    *,
    timeout_s: int,
    input_data: bytes | None = None,
) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        nested_ssh_cmd(host, timeout_s, ["bash", "--noprofile", "--norc", "-c", shlex.quote(script)]),
        input=input_data,
        capture_output=True,
        timeout=timeout_s,
        check=False,
    )


def safe_extract_tar_bytes(data: bytes, target_dir: Path) -> None:
    target_root = target_dir.resolve()
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as archive:
        for member in archive.getmembers():
            member_target = (target_root / member.name).resolve()
            if member_target != target_root and target_root not in member_target.parents:
                raise ValueError(f"unsafe tar member path: {member.name}")
        archive.extractall(target_root)


def copy_direct_spectre_inputs(
    *,
    task_id: str,
    tb_path: Path,
    include_paths: list[Path],
    output_dir: Path,
) -> tuple[Path, list[Path]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    safe_task_id = safe_path_component(task_id)
    spectre_tb_path = output_dir / f"{safe_task_id}__{tb_path.name}"
    staged_include_paths = list(include_paths)
    support_paths = discover_spectre_support_files(tb_path, staged_include_paths)
    input_paths = [*staged_include_paths, *support_paths]
    spectre_tb_path.write_text(
        rewrite_ahdl_includes_for_staging(tb_path, staged_include_paths),
        encoding="utf-8",
    )

    copied = [spectre_tb_path]
    seen = {spectre_tb_path.resolve()}
    for include_path in input_paths:
        rel = staged_input_rel(tb_path, include_path)
        dst = output_dir / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(include_path, dst)
        resolved = dst.resolve()
        if resolved not in seen:
            copied.append(dst)
            seen.add(resolved)
    return spectre_tb_path, copied


def staged_input_rel(tb_path: Path, input_path: Path) -> Path:
    try:
        rel = input_path.relative_to(tb_path.parent)
    except ValueError:
        rel = Path(input_path.name)
    if rel.is_absolute() or any(part == ".." for part in rel.parts):
        return Path(input_path.name)
    return rel


def rewrite_ahdl_includes_for_staging(tb_path: Path, include_paths: list[Path]) -> str:
    text = tb_path.read_text(encoding="utf-8")
    by_name = {path.name: staged_input_rel(tb_path, path).as_posix() for path in include_paths}

    def replace(match: re.Match[str]) -> str:
        include_name = Path(match.group(2).replace("\\", "/")).name
        staged_name = by_name.get(include_name)
        if staged_name is None:
            return match.group(0)
        return f"{match.group(1)}{staged_name}{match.group(3)}"

    return AHDL_INCLUDE_LINE_RE.sub(replace, text)


def discover_spectre_support_files(tb_path: Path, include_paths: list[Path]) -> list[Path]:
    search_dirs = [tb_path.parent]
    source_paths = [tb_path, *include_paths]
    for include_path in include_paths:
        if include_path.parent not in search_dirs:
            search_dirs.append(include_path.parent)

    support_paths: list[Path] = []
    seen: set[Path] = set()
    for source_path in source_paths:
        if not source_path.exists():
            continue
        text = source_path.read_text(encoding="utf-8", errors="ignore")
        for literal in SPECTRE_SUPPORT_FILE_RE.findall(text):
            literal_path = Path(literal.replace("\\", "/"))
            candidates = []
            if not literal_path.is_absolute() and not any(part == ".." for part in literal_path.parts):
                candidates.extend(search_dir / literal_path for search_dir in search_dirs)
            candidates.append((source_path.parent / literal_path).resolve())
            for candidate in candidates:
                if not candidate.exists() or not candidate.is_file():
                    continue
                resolved = candidate.resolve()
                if resolved not in seen:
                    support_paths.append(candidate)
                    seen.add(resolved)
                break
    return support_paths


def tar_input_files(files: list[Path], root: Path) -> bytes:
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w:gz") as archive:
        for path in files:
            archive.add(path, arcname=path.relative_to(root).as_posix())
    return buffer.getvalue()


def run_spectre_case_sui_direct(
    *,
    task_id: str,
    tb_path: Path,
    include_paths: list[Path],
    output_dir: Path,
    cadence_cshrc: str | None,
    timeout_s: int,
    side_output_files: tuple[str, ...] = (),
    sui_host: str | None = None,
    sui_work_root: str | None = None,
    spectre_mode: str = "ax",
) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    result_json = output_dir / "spectre_result.json"
    csv_path = output_dir / "tran_spectre.csv"
    if result_json.exists():
        result_json.unlink()
    if csv_path.exists():
        csv_path.unlink()

    spectre_tb_path, input_files = copy_direct_spectre_inputs(
        task_id=task_id,
        tb_path=tb_path,
        include_paths=include_paths,
        output_dir=output_dir,
    )
    raw_name = f"{spectre_tb_path.stem}.raw"
    raw_dir = output_dir / raw_name
    if raw_dir.exists():
        shutil.rmtree(raw_dir)
    for stale in (output_dir / "spectre.out", *[output_dir / name for name in side_output_files]):
        if stale.exists() and stale.is_file():
            stale.unlink()

    host = sui_host or default_sui_host()
    work_root = (sui_work_root or default_sui_work_root()).rstrip("/")
    cshrc = cadence_cshrc or default_sui_cadence_cshrc()
    remote_prefix = f"{safe_path_component(task_id)}_{uuid.uuid4().hex[:10]}"
    remote_dir = ""
    combined_output = ""
    side_outputs: dict[str, object] = {}
    errors: list[str] = []
    warnings: list[str] = []
    psf_parse: dict[str, object] | None = None
    license_queue_timeout_s = spectre_license_queue_timeout(timeout_s)
    mode = normalize_spectre_mode(spectre_mode)
    command = [
        "spectre",
        "-64",
        spectre_tb_path.name,
        "+escchars",
        "+log",
        "spectre.out",
        "-format",
        "psfascii",
        "-raw",
        raw_name,
        *SPECTRE_MODE_ARGS[mode],
        "+lqtimeout",
        str(license_queue_timeout_s),
        "-maxw",
        "5",
        "-maxn",
        "5",
        "+logstatus",
    ]

    try:
        create_script = " ".join(
            [
                f"primary_root={shlex.quote(work_root)};",
                'fallback_root="$HOME/WORK/vaevas-direct-spectre";',
                'if mkdir -p "$primary_root" >/dev/null 2>&1 && [ -w "$primary_root" ]; then',
                'chosen_root="$primary_root";',
                "else",
                'mkdir -p "$fallback_root";',
                'chosen_root="$fallback_root";',
                "fi;",
                f"mktemp -d \"$chosen_root/{remote_prefix}.XXXXXX\"",
            ]
        )
        create = run_ssh_text(
            host,
            create_script,
            timeout_s=30,
        )
        combined_output += (create.stdout or "") + "\n" + (create.stderr or "")
        if create.returncode != 0:
            errors.append(f"remote_workdir_create_failed rc={create.returncode}")
            remote_dir = ""
        else:
            remote_dir = next(
                (line.strip() for line in reversed(create.stdout.splitlines()) if line.strip().startswith("/")),
                "",
            )
        if not remote_dir:
            errors.append("remote_workdir_unresolved")
            raise RuntimeError("remote_workdir_unresolved")

        upload = run_ssh_bytes(
            host,
            f"tar -xzf - -C {shlex.quote(remote_dir)}",
            input_data=tar_input_files(input_files, output_dir),
            timeout_s=max(timeout_s, 60),
        )
        combined_output += "\n" + (upload.stdout or b"").decode("utf-8", errors="replace")
        combined_output += "\n" + (upload.stderr or b"").decode("utf-8", errors="replace")
        if upload.returncode != 0:
            errors.append(f"remote_upload_failed rc={upload.returncode}")
            raise RuntimeError("remote_upload_failed")

        spectre_command = " ".join(shlex.quote(part) for part in command)
        csh_parts = []
        if cshrc:
            csh_parts.append(f"source {shlex.quote(cshrc)}")
        csh_parts.append(f"cd {shlex.quote(remote_dir)}")
        csh_parts.append(spectre_command)
        run_script = " && ".join(csh_parts)
        run = run_ssh_text(
            host,
            f"tcsh -c {shlex.quote(run_script)}",
            timeout_s=max(timeout_s, 600),
        )
        combined_output += "\n" + (run.stdout or "") + "\n" + (run.stderr or "")

        spectre_log = output_dir / "spectre.out"
        if run.returncode != 0:
            errors.append(f"spectre_failed rc={run.returncode}")
        else:
            download = run_ssh_bytes(
                host,
                f"tar -czf - -C {shlex.quote(remote_dir)} .",
                timeout_s=max(timeout_s, 600),
            )
            combined_output += "\n" + (download.stderr or b"").decode("utf-8", errors="replace")
            if download.returncode == 0:
                safe_extract_tar_bytes(download.stdout or b"", output_dir)
            else:
                errors.append(f"remote_download_failed rc={download.returncode}")

        if spectre_log.exists():
            combined_output += "\n" + spectre_log.read_text(encoding="utf-8", errors="replace")

        if "SPECTRE-209" in combined_output or "required license could not be checked out" in combined_output:
            errors.append("spectre_license_checkout_failed:SPECTRE-209")
        if raw_dir.exists():
            try:
                psf_parse = write_spectre_psf_csv(raw_dir, csv_path)
            except Exception as exc:  # pragma: no cover - reported in JSON for field debugging
                errors.append(f"psf_parse_failed={type(exc).__name__}: {str(exc)[:300]}")
        elif run.returncode == 0:
            errors.append(f"spectre_raw_missing={raw_name}")
    except subprocess.TimeoutExpired as exc:
        errors.append(f"sui_direct_timeout_after_s={exc.timeout}")
        combined_output += "\n" + (
            ((exc.stdout or "") if isinstance(exc.stdout, str) else "")
            + "\n"
            + ((exc.stderr or "") if isinstance(exc.stderr, str) else "")
        )
    except Exception as exc:
        if not errors:
            errors.append(f"sui_direct_exception={type(exc).__name__}: {str(exc)[:300]}")
    finally:
        if remote_dir:
            try:
                cleanup = run_ssh_text(host, f"rm -rf {shlex.quote(remote_dir)}", timeout_s=30)
                if cleanup.returncode != 0:
                    warnings.append(f"remote_cleanup_failed rc={cleanup.returncode}")
            except Exception as exc:  # pragma: no cover - best-effort cleanup only
                warnings.append(f"remote_cleanup_exception={type(exc).__name__}: {str(exc)[:200]}")

    for name in side_output_files:
        local_path = output_dir / name
        side_outputs[name] = {
            "downloaded": local_path.exists(),
            "path": str(local_path) if local_path.exists() else "",
            "remote_path": f"{remote_dir}/{name}" if remote_dir else "",
        }

    ok = not errors and csv_path.exists()
    result = {
        "status": "success" if ok else "error",
        "ok": ok,
        "errors": errors,
        "warnings": warnings,
        "signals": list(psf_parse.get("columns", [])) if psf_parse else [],
        "rows": int(psf_parse.get("rows", 0)) if psf_parse else 0,
        "csv_path": str(csv_path),
        "side_outputs": side_outputs,
        "spectre_backend": "sui-direct",
        "spectre_mode": mode,
        "sui_host": host,
        "sui_nested_host": default_sui_nested_host(),
        "sui_work_root": work_root,
        "remote_run_dir": remote_dir,
        "command": " ".join(command),
        "timing": parse_spectre_timing(combined_output),
        "psf_parse": psf_parse or {},
        "stdout_tail": combined_output[-4000:],
    }
    result_json.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def run_spectre_case(
    *,
    task_id: str,
    tb_path: Path,
    include_paths: list[Path],
    output_dir: Path,
    bridge_repo: Path,
    cadence_cshrc: str | None,
    timeout_s: int,
    side_output_files: tuple[str, ...] = (),
    spectre_backend: str = "bridge",
    sui_host: str | None = None,
    sui_work_root: str | None = None,
    spectre_mode: str = "ax",
) -> dict:
    backend = normalize_spectre_backend(spectre_backend)
    mode = normalize_spectre_mode(spectre_mode)
    if backend == "sui-direct":
        max_attempts = 1 + direct_sui_retry_count()
        attempts: list[dict[str, object]] = []
        retry_warnings: list[str] = []
        for attempt_number in range(1, max_attempts + 1):
            result = run_spectre_case_sui_direct(
                task_id=task_id,
                tb_path=tb_path,
                include_paths=include_paths,
                output_dir=output_dir,
                cadence_cshrc=cadence_cshrc,
                timeout_s=timeout_s,
                side_output_files=side_output_files,
                sui_host=sui_host,
                sui_work_root=sui_work_root,
                spectre_mode=mode,
            )
            retryable, retry_reason = retryable_direct_sui_result(result)
            attempts.append(
                {
                    "attempt": attempt_number,
                    "ok": bool(result.get("ok")),
                    "status": result.get("status", ""),
                    "retryable": retryable,
                    "retry_reason": retry_reason,
                    "errors": list(result.get("errors") or []),
                    "remote_run_dir": result.get("remote_run_dir", ""),
                }
            )
            if result.get("ok") or not retryable or attempt_number >= max_attempts:
                result["sui_direct_attempts"] = attempts
                result["sui_direct_retry_count"] = attempt_number - 1
                if retry_warnings:
                    result.setdefault("warnings", []).extend(retry_warnings)
                write_spectre_result_json(output_dir, result)
                return result
            backoff_s = direct_sui_retry_backoff_s(attempt_number)
            retry_warnings.append(
                "sui_direct_retry "
                f"attempt={attempt_number} next_attempt={attempt_number + 1} "
                f"reason={retry_reason} backoff_s={backoff_s:g}"
            )
            if backoff_s > 0:
                time.sleep(backoff_s)

        raise AssertionError("unreachable direct SUI retry loop")

    output_dir.mkdir(parents=True, exist_ok=True)
    bridge_py = bridge_repo / ".venv" / "bin" / "python"
    result_json = output_dir / "spectre_result.json"
    csv_path = output_dir / "tran_spectre.csv"
    safe_task_id = "".join(ch if ch.isalnum() or ch in {"_", "-"} else "_" for ch in task_id)
    spectre_tb_path = output_dir / f"{safe_task_id}__{tb_path.name}"
    # Spectre names its AHDL CMI cache from the testbench basename. Parallel
    # release forms often share one gold TB, so isolate the basename per task.
    spectre_tb_path.write_text(tb_path.read_text(encoding="utf-8"), encoding="utf-8")

    payload = {
        "bridge_repo": str(bridge_repo.resolve()),
        "tb_path": str(spectre_tb_path.resolve()),
        "include_paths": [str(p.resolve()) for p in include_paths],
        "output_dir": str(output_dir.resolve()),
        "result_json": str(result_json.resolve()),
        "csv_path": str(csv_path.resolve()),
        "cadence_cshrc": cadence_cshrc or "",
        "bridge_profile": os.environ.get("VAEVAS_BRIDGE_PROFILE") or os.environ.get("BRIDGE_PROFILE") or "",
        "side_output_files": list(side_output_files),
        "spectre_mode": mode,
    }

    inline = (
        "import csv, json, os, shlex\n"
        "from pathlib import Path\n"
        "from dotenv import load_dotenv\n"
        "payload = json.loads(" + repr(json.dumps(payload)) + ")\n"
        "bridge_repo = Path(payload['bridge_repo'])\n"
        "load_dotenv(bridge_repo / '.env')\n"
        "profile = payload.get('bridge_profile') or os.environ.get('VAEVAS_BRIDGE_PROFILE') or os.environ.get('BRIDGE_PROFILE') or None\n"
        "if payload['cadence_cshrc']:\n"
        "    os.environ['VB_CADENCE_CSHRC'] = payload['cadence_cshrc']\n"
        "from virtuoso_bridge.spectre.runner import SpectreSimulator, spectre_mode_args\n"
        "tb = Path(payload['tb_path'])\n"
        "out = Path(payload['output_dir'])\n"
        "out.mkdir(parents=True, exist_ok=True)\n"
        "side_output_files = list(payload.get('side_output_files') or [])\n"
        "spectre_mode = payload.get('spectre_mode') or 'ax'\n"
        "spectre_args = spectre_mode_args('ax') if spectre_mode == 'ax' else ()\n"
        "sim = SpectreSimulator.from_env(spectre_args=spectre_args, work_dir=out, output_format='psfascii', keep_remote_files=bool(side_output_files), profile=profile)\n"
        "runner = None\n"
        "remote_pwd = ''\n"
        "if side_output_files:\n"
        "    try:\n"
        "        runner = sim._get_ssh_runner()\n"
        "        pwd_result = runner.run_command('pwd')\n"
        "        pwd_lines = [line.strip() for line in (pwd_result.stdout or '').splitlines() if line.strip()]\n"
        "        remote_pwd = next((line for line in reversed(pwd_lines) if line.startswith('/')), '')\n"
        "        if remote_pwd:\n"
        "            stale_targets = ' '.join(shlex.quote(f'{remote_pwd}/{name}') for name in side_output_files)\n"
        "            if stale_targets:\n"
        "                runner.run_command('rm -f ' + stale_targets)\n"
        "    except Exception:\n"
        "        remote_pwd = ''\n"
        "res = sim.run_simulation(tb, {'include_files': payload['include_paths']})\n"
        "side_outputs = {}\n"
        "remote_run_dir = ''\n"
        "if side_output_files:\n"
        "    try:\n"
        "        if runner is None:\n"
        "            runner = sim._get_ssh_runner()\n"
        "        spec_cmd = str(getattr(res, 'metadata', {}).get('spectre_command', ''))\n"
        "        for token in shlex.split(spec_cmd):\n"
        "            if token.endswith('/' + tb.name):\n"
        "                remote_run_dir = str(Path(token).parent)\n"
        "                break\n"
        "        remote_output_dirs = []\n"
        "        for candidate_dir in (remote_run_dir, remote_pwd):\n"
        "            if candidate_dir and candidate_dir not in remote_output_dirs:\n"
        "                remote_output_dirs.append(candidate_dir)\n"
        "        if remote_output_dirs:\n"
        "            for name in side_output_files:\n"
        "                local_path = out / name\n"
        "                attempts = []\n"
        "                downloaded = False\n"
        "                for remote_dir in remote_output_dirs:\n"
        "                    remote_path = f'{remote_dir}/{name}'\n"
        "                    result = runner.download(remote_path, local_path)\n"
        "                    attempts.append({'remote_path': remote_path, 'returncode': result.returncode, 'stderr_tail': (result.stderr or '')[-500:]})\n"
        "                    if result.returncode == 0:\n"
        "                        side_outputs[name] = {'downloaded': True, 'path': str(local_path), 'remote_path': remote_path, 'attempts': attempts}\n"
        "                        downloaded = True\n"
        "                        break\n"
        "                if not downloaded:\n"
        "                    side_outputs[name] = {'downloaded': False, 'path': '', 'attempts': attempts, 'stderr_tail': attempts[-1]['stderr_tail'] if attempts else ''}\n"
        "            if remote_run_dir:\n"
        "                runner.run_command('rm -rf ' + shlex.quote(remote_run_dir))\n"
        "            if remote_pwd:\n"
        "                cleanup_targets = ' '.join(shlex.quote(f'{remote_pwd}/{name}') for name in side_output_files)\n"
        "                if cleanup_targets:\n"
        "                    runner.run_command('rm -f ' + cleanup_targets)\n"
        "        else:\n"
        "            side_outputs['_error'] = 'remote_output_dir_unresolved'\n"
        "    except Exception as exc:\n"
        "        side_outputs['_error'] = f'{type(exc).__name__}: {str(exc)[:300]}'\n"
        "keys = sorted(res.data.keys())\n"
        "if 'time' in keys:\n"
        "    keys = ['time'] + [k for k in keys if k != 'time']\n"
        "nrows = max((len(v) for v in res.data.values()), default=0)\n"
        "csv_path = Path(payload['csv_path'])\n"
        "with csv_path.open('w', newline='') as f:\n"
        "    writer = csv.writer(f)\n"
        "    writer.writerow(keys)\n"
        "    for i in range(nrows):\n"
        "        writer.writerow([(res.data.get(k, [])[i] if i < len(res.data.get(k, [])) else '') for k in keys])\n"
        "summary = {\n"
        "    'status': res.status.value,\n"
        "    'ok': bool(res.ok),\n"
        "    'errors': list(res.errors),\n"
        "    'warnings': list(res.warnings),\n"
        "    'signals': keys,\n"
        "    'rows': nrows,\n"
        "    'csv_path': str(csv_path),\n"
        "    'side_outputs': side_outputs,\n"
        "    'remote_run_dir': remote_run_dir,\n"
        "    'remote_pwd': remote_pwd,\n"
        "    'spectre_mode': spectre_mode,\n"
        "}\n"
        "Path(payload['result_json']).write_text(json.dumps(summary, indent=2), encoding='utf-8')\n"
        "print(json.dumps(summary, indent=2))\n"
    )

    env = os.environ.copy()
    py_path = str(bridge_repo)
    if env.get("PYTHONPATH"):
        py_path = py_path + os.pathsep + env["PYTHONPATH"]
    env["PYTHONPATH"] = py_path

    proc = run_cmd(
        [str(bridge_py), "-c", inline],
        cwd=bridge_repo,
        env=env,
        timeout_s=max(timeout_s, 600),
    )

    if not result_json.exists():
        return {
            "status": "blocked",
            "ok": False,
            "notes": ["spectre_result.json missing"],
            "stdout_tail": ((proc.stdout or "") + "\n" + (proc.stderr or ""))[-4000:],
        }

    try:
        result = json.loads(result_json.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        return {
            "status": "blocked",
            "ok": False,
            "notes": [f"spectre_result.json unreadable: {exc}"],
            "stdout_tail": ((proc.stdout or "") + "\n" + (proc.stderr or ""))[-4000:],
        }
    result["stdout_tail"] = ((proc.stdout or "") + "\n" + (proc.stderr or ""))[-4000:]
    if proc.returncode != 0 and result.get("status") != "success":
        result["status"] = "error"
        result["ok"] = False
    return result


def should_retry_spectre_upload(result: dict) -> bool:
    if result.get("ok"):
        return False
    errors = result.get("errors") or []
    return any("Failed to upload files" in str(err) for err in errors)


def run_dual_case(
    *,
    task_dir: Path,
    output_root: Path,
    bridge_repo: Path,
    cadence_cshrc: str | None,
    timeout_s: int,
    spectre_backend: str = "bridge",
    sui_host: str | None = None,
    sui_work_root: str | None = None,
    spectre_mode: str = "ax",
) -> dict:
    gold_dir = task_dir / "gold"
    meta = read_meta(task_dir)
    task_id = meta.get("task_id", task_dir.name)
    checker_task_id = resolve_checker_task_id(meta, str(task_id), form=task_dir.name)
    scoring = set(meta.get("scoring", ["dut_compile", "tb_compile", "sim_correct"]))

    tb_path = choose_gold_tb(gold_dir)
    if tb_path is None:
        return {
            "task_id": task_id,
            "status": "FAIL_INFRA",
            "notes": ["no gold testbench found"],
        }

    includes = ahdl_includes(tb_path)
    if not includes:
        return {
            "task_id": task_id,
            "status": "FAIL_INFRA",
            "notes": [f"no ahdl_include found in {tb_path.name}"],
        }

    include_paths = [gold_dir / name for name in includes]
    missing = [str(path.name) for path in include_paths if not path.exists()]
    if missing:
        return {
            "task_id": task_id,
            "status": "FAIL_INFRA",
            "notes": [f"missing included files: {', '.join(missing)}"],
        }

    case_root = output_root / task_id
    evas_root = case_root / "evas"
    spectre_root = case_root / "spectre"
    primary_dut = include_paths[0]
    notes = [
        f"gold_tb={tb_path.name}",
        f"gold_primary_dut={primary_dut.name}",
    ]

    from run_gold_suite import run_gold_case

    evas_t0 = time.perf_counter()
    evas_result = run_gold_case(task_dir, output_root, timeout_s)
    evas_wall_time_s = time.perf_counter() - evas_t0
    evas_csv = evas_root / "tran.csv"
    if not evas_csv.exists():
        evas_csv = case_root / "tran.csv"

    spectre_t0 = time.perf_counter()
    spectre_result = run_spectre_case(
        task_id=task_id,
        tb_path=tb_path,
        include_paths=include_paths,
        output_dir=spectre_root,
        bridge_repo=bridge_repo,
        cadence_cshrc=cadence_cshrc,
        timeout_s=timeout_s,
        side_output_files=behavior_side_output_names(checker_task_id),
        spectre_backend=spectre_backend,
        sui_host=sui_host,
        sui_work_root=sui_work_root,
        spectre_mode=spectre_mode,
    )
    spectre_wall_time_s = time.perf_counter() - spectre_t0
    if should_retry_spectre_upload(spectre_result):
        notes.append("spectre:retry_after_upload_failure")
        retry_t0 = time.perf_counter()
        spectre_result = run_spectre_case(
            task_id=task_id,
            tb_path=tb_path,
            include_paths=include_paths,
            output_dir=spectre_root,
            bridge_repo=bridge_repo,
            cadence_cshrc=cadence_cshrc,
            timeout_s=timeout_s,
            side_output_files=behavior_side_output_names(checker_task_id),
            spectre_backend=spectre_backend,
            sui_host=sui_host,
            sui_work_root=sui_work_root,
            spectre_mode=spectre_mode,
        )
        spectre_wall_time_s += time.perf_counter() - retry_t0

    spectre_csv = spectre_root / "tran_spectre.csv"
    if "sim_correct" not in scoring:
        spectre_sim_correct = 1.0
        spectre_behavior_notes = ["behavior_not_required_by_scoring"]
        notes.append("spectre:behavior_not_required_by_scoring")
    elif spectre_result.get("ok") and spectre_csv.exists():
        spectre_sim_correct, spectre_behavior_notes = evaluate_behavior(checker_task_id, spectre_csv)
        side_output_result = validate_behavior_side_outputs(checker_task_id, spectre_root, spectre_csv)
        if side_output_result is not None:
            side_output_ok, side_output_note = side_output_result
            spectre_behavior_notes.append(side_output_note)
            if not side_output_ok:
                spectre_sim_correct = 0.0
        notes.extend(f"spectre:{note}" for note in spectre_behavior_notes)
    else:
        spectre_sim_correct = 0.0
        notes.append("spectre:tran_spectre.csv missing or run failed")
        spectre_behavior_notes = []

    if "sim_correct" not in scoring:
        parity = {
            "status": "not_required",
            "reason": "task scoring does not require sim_correct parity",
        }
    elif evas_result["status"] == "PASS" and spectre_sim_correct == 1.0 and spectre_csv.exists() and evas_csv.exists():
        parity = compare_waveforms(checker_task_id, evas_csv, spectre_csv)
    else:
        parity = {
            "status": "blocked",
            "reason": "prerequisites not met for waveform comparison",
        }

    if evas_result["status"] != "PASS":
        status = "FAIL_EVAS"
    elif not spectre_result.get("ok"):
        status = "FAIL_SPECTRE"
    elif spectre_sim_correct < 1.0:
        status = "FAIL_SPECTRE_BEHAVIOR"
    elif parity.get("status") not in {"passed", "not_required"}:
        status = "FAIL_PARITY"
    else:
        status = "PASS"

    return {
        "task_id": task_id,
        "checker_task_id": checker_task_id,
        "status": status,
        "gold_dir": str(gold_dir),
        "gold_tb": str(tb_path),
        "gold_includes": includes,
        "evas": evas_result,
        "evas_engine_used": evas_result.get("evas_engine_used"),
        "spectre": {
            **spectre_result,
            "behavior_score": spectre_sim_correct,
            "behavior_notes": spectre_behavior_notes,
        },
        "parity": parity,
        "timing": {
            "evas_wall_time_s": evas_wall_time_s,
            "spectre_wall_time_s": spectre_wall_time_s,
            "combined_wall_time_s": evas_wall_time_s + spectre_wall_time_s,
        },
        "notes": notes,
    }


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Run EVAS + Spectre dual validation on gold tasks.")
    ap.add_argument(
        "--output-root",
        default="results/gold-dual-suite",
        help="Output directory relative to benchmark root unless absolute.",
    )
    ap.add_argument("--timeout-s", type=int, default=240)
    ap.add_argument(
        "--family",
        action="append",
        choices=("end-to-end", "spec-to-va", "bugfix", "tb-generation"),
        help="Task family to scan for gold assets. Defaults to end-to-end only.",
    )
    ap.add_argument(
        "--task",
        action="append",
        default=[],
        help="Restrict to one or more task IDs with gold assets.",
    )
    ap.add_argument(
        "--bridge-repo",
        default=str(default_bridge_repo()),
        help="Path to virtuoso-bridge-lite repository.",
    )
    ap.add_argument(
        "--spectre-backend",
        default=os.environ.get("VAEVAS_SPECTRE_BACKEND", "bridge"),
        help="Spectre execution backend: bridge (default) or sui-direct.",
    )
    ap.add_argument(
        "--sui-host",
        default=default_sui_host(),
        help="SSH host used by --spectre-backend=sui-direct.",
    )
    ap.add_argument(
        "--sui-work-root",
        default=default_sui_work_root(),
        help="Remote scratch root used by --spectre-backend=sui-direct.",
    )
    ap.add_argument(
        "--cadence-cshrc",
        default=os.environ.get("VB_CADENCE_CSHRC", ""),
        help="Remote Cadence cshrc path used to expose spectre on PATH.",
    )
    ap.add_argument(
        "--skip-bridge-preflight",
        action="store_true",
        help="Skip bridge health checks and run Spectre directly.",
    )
    ap.add_argument(
        "--require-virtuoso-daemon",
        action="store_true",
        help="Treat a disconnected Virtuoso CIW daemon as a hard blocker.",
    )
    ap.add_argument(
        "--allow-direct-run",
        action="store_true",
        help="Allow calling this runner directly without scripts/run_with_bridge.sh.",
    )
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    spectre_backend = normalize_spectre_backend(args.spectre_backend)
    via_wrapper = os.environ.get("VAEVAS_BRIDGE_WRAPPER") == "1"
    if spectre_backend == "bridge" and not via_wrapper and not args.allow_direct_run:
        summary = {
            "status": "blocked",
            "reason": "direct invocation blocked; use scripts/run_with_bridge.sh",
            "remediation": [
                "cd /path/to/behavioral-veriloga-eval",
                "./scripts/run_with_bridge.sh python3 runners/run_gold_dual_suite.py <args>",
                "or add --allow-direct-run if you intentionally run without wrapper",
            ],
        }
        print(json.dumps(summary, indent=2))
        return 2

    bridge_repo = Path(args.bridge_repo).resolve()
    if spectre_backend == "bridge" and not bridge_repo.exists():
        print(json.dumps({"status": "blocked", "reason": f"bridge repo not found: {bridge_repo}"}, indent=2))
        return 2

    out_root = Path(args.output_root)
    if not out_root.is_absolute():
        out_root = benchmark_root() / out_root
    out_root.mkdir(parents=True, exist_ok=True)

    if spectre_backend == "bridge":
        effective_cshrc = resolve_cadence_cshrc(bridge_repo, args.cadence_cshrc)
    else:
        effective_cshrc = args.cadence_cshrc or default_sui_cadence_cshrc()

    if spectre_backend == "sui-direct":
        preflight = {
            "status": "skipped",
            "reason": "direct SUI backend selected; bridge preflight is not required",
            "spectre_backend": spectre_backend,
            "sui_host": args.sui_host,
            "sui_work_root": args.sui_work_root,
            "cadence_cshrc": effective_cshrc,
        }
    elif args.skip_bridge_preflight:
        preflight = {
            "status": "skipped",
            "bridge_repo": str(bridge_repo),
            "cadence_cshrc": effective_cshrc,
        }
    else:
        preflight = bridge_preflight(
            bridge_repo,
            cadence_cshrc=effective_cshrc,
            require_daemon=args.require_virtuoso_daemon,
        )
        if preflight.get("status") == "blocked":
            summary = {
                "status": "blocked",
                "reason": preflight.get("reason", "bridge preflight failed"),
                "tasks_total": 0,
                "pass_count": 0,
                "fail_count": 0,
                "task_ids": [],
                "families": list(tuple(args.family) if args.family else ("end-to-end",)),
                "bridge_repo": str(bridge_repo),
                "cadence_cshrc": effective_cshrc,
                "bridge_preflight": preflight,
                "results": [],
            }
            (out_root / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
            print(json.dumps(summary, indent=2))
            return 2

    selected = set(args.task) if args.task else None
    families = tuple(args.family) if args.family else ("end-to-end",)
    results = [
        run_dual_case(
            task_dir=task_dir,
            output_root=out_root,
            bridge_repo=bridge_repo,
            cadence_cshrc=effective_cshrc or None,
            timeout_s=args.timeout_s,
            spectre_backend=spectre_backend,
            sui_host=args.sui_host,
            sui_work_root=args.sui_work_root,
        )
        for task_dir in list_gold_task_dirs(selected, families=families)
    ]

    summary = {
        "tasks_total": len(results),
        "pass_count": sum(1 for r in results if r["status"] == "PASS"),
        "fail_count": sum(1 for r in results if r["status"] != "PASS"),
        "task_ids": [r["task_id"] for r in results],
        "families": list(families),
        "spectre_backend": spectre_backend,
        "bridge_repo": str(bridge_repo),
        "sui_host": args.sui_host if spectre_backend == "sui-direct" else "",
        "sui_work_root": args.sui_work_root if spectre_backend == "sui-direct" else "",
        "cadence_cshrc": effective_cshrc,
        "bridge_preflight": preflight,
        "results": results,
    }
    (out_root / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0 if summary["fail_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
