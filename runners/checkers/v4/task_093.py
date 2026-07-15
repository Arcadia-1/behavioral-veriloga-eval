"""Task-specific checker for canonical v4 DUT 093."""
from __future__ import annotations

from ..api import Checker
import csv
import math

def _csv_header_indices(csv_path: Path) -> tuple[list[str], dict[str, int]]:
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, [])
    return header, {name: idx for idx, name in enumerate(header)}

def _csv_required_indices(csv_path: Path, required: set[str]) -> tuple[dict[str, int] | None, list[str]]:
    header, index = _csv_header_indices(csv_path)
    missing = sorted(required - set(header))
    if missing:
        return None, missing
    return {name: index[name] for name in required}, []

def _float_at(row: list[str], index: int, default: float = 0.0) -> float:
    try:
        return float(row[index])
    except (IndexError, TypeError, ValueError):
        return default

def _stream_gain_estimator_csv(csv_path: Path) -> tuple[float, list[str]]:
    required = {"time", "vinp", "vinn", "voutp", "voutn", "gain_out", "valid"}
    indices, missing = _csv_required_indices(csv_path, required)
    if indices is None:
        # The row-based checker has no aliases for these required outputs, so
        # missing columns would fail after loading the full CSV.
        return 0.0, [f"required_columns_missing={'/'.join(missing)}"]
    assert indices is not None

    last_time = 0.0
    final_valid = 0.0
    max_valid = 0.0
    valid_count = 0
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            last_time = _float_at(row, indices["time"])
            valid = final_valid = _float_at(row, indices["valid"])
            if valid > 0.45:
                valid_count += 1
            if valid > max_valid:
                max_valid = valid

    if valid_count < 20:
        return 0.0, [f"insufficient_valid_samples={valid_count}"]

    late_start = last_time * 0.65
    late_valid_count = 0
    vin_min = math.inf
    vin_max = -math.inf
    vout_min = math.inf
    vout_max = -math.inf
    gain_sum = 0.0
    vdd_est = max(max_valid, 1e-6)

    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            time_value = _float_at(row, indices["time"])
            if time_value < late_start:
                continue
            valid = _float_at(row, indices["valid"])
            if valid <= 0.45:
                continue
            vin_diff = _float_at(row, indices["vinp"]) - _float_at(row, indices["vinn"])
            vout_diff = _float_at(row, indices["voutp"]) - _float_at(row, indices["voutn"])
            vin_min = min(vin_min, vin_diff)
            vin_max = max(vin_max, vin_diff)
            vout_min = min(vout_min, vout_diff)
            vout_max = max(vout_max, vout_diff)
            gain_sum += _float_at(row, indices["gain_out"]) / vdd_est * 10.0
            late_valid_count += 1

    if late_valid_count < 10:
        return 0.0, [f"late_valid_samples={late_valid_count}"]

    in_span = vin_max - vin_min
    out_span = vout_max - vout_min
    waveform_gain = out_span / in_span if in_span > 1e-12 else 0.0
    gain_est = gain_sum / late_valid_count
    gain_err = abs(gain_est - waveform_gain)
    valid_final = final_valid > 0.45
    ok = (
        valid_final
        and 0.045 <= in_span <= 0.075
        and 0.27 <= out_span <= 0.45
        and 5.0 <= waveform_gain <= 7.2
        and gain_err <= 0.35
    )
    return (1.0 if ok else 0.0), [
        f"in_span={in_span:.4f} out_span={out_span:.4f} "
        f"waveform_gain={waveform_gain:.2f} gain_est={gain_est:.2f} "
        f"gain_err={gain_err:.2f} valid_final={valid_final}"
    ]

def check_gain_estimator(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vinp", "vinn", "voutp", "voutn", "gain_out", "valid"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/vinp/vinn/voutp/voutn/gain_out/valid"

    valid_rows = [row for row in rows if row["valid"] > 0.45]
    if len(valid_rows) < 20:
        return False, f"insufficient_valid_samples={len(valid_rows)}"

    late_start = rows[-1]["time"] * 0.65
    late = [row for row in rows if row["time"] >= late_start]
    late_valid = [row for row in late if row["valid"] > 0.45]
    if len(late_valid) < 10:
        return False, f"late_valid_samples={len(late_valid)}"

    vin_diff = [row["vinp"] - row["vinn"] for row in late_valid]
    vout_diff = [row["voutp"] - row["voutn"] for row in late_valid]
    in_span = max(vin_diff) - min(vin_diff)
    out_span = max(vout_diff) - min(vout_diff)
    waveform_gain = out_span / in_span if in_span > 1e-12 else 0.0

    vdd_est = max(max(row["valid"] for row in rows), 1e-6)
    gain_estimates = [row["gain_out"] / vdd_est * 10.0 for row in late_valid]
    gain_est = sum(gain_estimates) / len(gain_estimates)
    gain_err = abs(gain_est - waveform_gain)

    valid_final = rows[-1]["valid"] > 0.45
    ok = (
        valid_final
        and 0.045 <= in_span <= 0.075
        and 0.27 <= out_span <= 0.45
        and 5.0 <= waveform_gain <= 7.2
        and gain_err <= 0.35
    )
    return ok, (
        f"in_span={in_span:.4f} out_span={out_span:.4f} "
        f"waveform_gain={waveform_gain:.2f} gain_est={gain_est:.2f} "
        f"gain_err={gain_err:.2f} valid_final={valid_final}"
    )

CHECKER_ID = "v4_093_gain_estimator"
CHECKER: Checker = check_gain_estimator
STREAMING_CHECKER = _stream_gain_estimator_csv
