"""Task-specific checker for canonical v4 DUT 343."""
from __future__ import annotations

from checkers.api import Checker
from _bisect import bisect_left

SETTLE = 6.5e-10
VDD = 0.9
VTH = 0.45

def _high(row: dict[str, float], signal: str, threshold: float = VTH) -> bool:
    return float(row.get(signal, 0.0)) > threshold

def _missing(rows: list[dict[str, float]], required: set[str]) -> list[str]:
    if not rows:
        return sorted(required)
    return sorted(required - set(rows[0]))

def _rising_indices(rows: list[dict[str, float]], signal: str, threshold: float = VTH) -> list[int]:
    result: list[int] = []
    previous = float(rows[0][signal])
    for index, row in enumerate(rows[1:], 1):
        value = float(row[signal])
        if previous <= threshold < value:
            result.append(index)
        previous = value
    return result

def _row_after(rows: list[dict[str, float]], time_s: float, delay_s: float = SETTLE) -> dict[str, float]:
    times = [float(row["time"]) for row in rows]
    index = bisect_left(times, time_s + delay_s)
    return rows[min(index, len(rows) - 1)]

def _code(row: dict[str, float], lsb_first: list[str]) -> int:
    return sum((1 << bit) for bit, signal in enumerate(lsb_first) if _high(row, signal))

def _gap(expected: float, observed: float) -> float:
    return abs(float(expected) - float(observed))

def _mismatch(
    errors: list[str], property_id: str, time_s: float, expected: object, observed: object, gap: float | None = None
) -> None:
    detail = (
        f"{property_id} mismatch_count=1 sample_time={time_s:.12g} "
        f"expected={expected} observed={observed}"
    )
    if gap is not None:
        detail += f" metric_gap={gap:.6g}"
    errors.append(detail)

def _finish(task_id: str, checks: int, errors: list[str], coverage: str, minimum: int) -> tuple[bool, str]:
    ok = checks >= minimum and not errors
    detail = "; ".join(errors[:6])
    return ok, (
        f"{task_id} checked={checks} mismatch_count={len(errors)} {coverage}"
        + (f" mismatch_detail={detail}" if detail else "")
    )

def check_v4_343_pipeline_adc_two_stage(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {
        "time", "vin", "clk", "rst", "valid_i", "code_3", "code_2", "code_1",
        "code_0", "valid_o", "residue_dbg",
    }
    missing = _missing(rows, required)
    if missing:
        return False, f"v4_343 missing_signals={','.join(missing)}"
    errors: list[str] = []
    reset_clear = any(
        _high(row, "rst")
        and _code(row, ["code_0", "code_1", "code_2", "code_3"]) == 0
        and not _high(row, "valid_o")
        and abs(float(row["residue_dbg"])) < 0.04
        for row in rows
    )
    if not reset_clear:
        _mismatch(errors, "P_PIPE_RESET_CLEAR", 0.0, "code/valid/residue clear", "not observed")

    clock_edges = _rising_indices(rows, "clk")
    samples: list[tuple[int, float, int]] = []
    residue_checks = 0
    for edge_number, index in enumerate(clock_edges):
        row = rows[index]
        if _high(row, "rst") or not _high(row, "valid_i"):
            continue
        vin = max(0.0, min(VDD, float(row["vin"])))
        expected_code = min(15, int(16.0 * vin / VDD))
        samples.append((edge_number, vin, expected_code))
        coarse = min(3, int(4.0 * vin / VDD))
        expected_residue = max(0.0, min(VDD, 4.0 * (vin - VDD * coarse / 4.0)))
        observed = _row_after(rows, float(row["time"]))
        if _gap(expected_residue, float(observed["residue_dbg"])) > 0.06:
            _mismatch(errors, "P_PIPE_RESIDUE", float(row["time"]), expected_residue, float(observed["residue_dbg"]), _gap(expected_residue, float(observed["residue_dbg"])))
        residue_checks += 1

    matched: set[int] = set()
    output_checks = 0
    valid_outputs_by_edge: set[int] = set()
    for edge_number, index in enumerate(clock_edges):
        observed = _row_after(rows, float(rows[index]["time"]))
        if _high(observed, "rst") or not _high(observed, "valid_o"):
            continue
        valid_outputs_by_edge.add(edge_number)
        observed_code = _code(observed, ["code_0", "code_1", "code_2", "code_3"])
        candidates = [
            (sample_index, sample)
            for sample_index, sample in enumerate(samples)
            if sample_index not in matched and 1 <= edge_number - sample[0] <= 3
        ]
        selected = next((item for item in candidates if item[1][2] == observed_code), None)
        if selected is None:
            expected = [item[1][2] for item in candidates]
            _mismatch(errors, "P_PIPE_ALIGNED_CODE", float(observed["time"]), expected, observed_code)
        else:
            matched.add(selected[0])
        output_checks += 1
    missing_valid = [
        sample[0]
        for sample_index, sample in enumerate(samples)
        if sample_index not in matched
        and not any(1 <= edge_number - sample[0] <= 3 for edge_number in valid_outputs_by_edge)
    ]
    if missing_valid:
        _mismatch(
            errors,
            "P_PIPE_VALID_LATENCY",
            float(rows[clock_edges[missing_valid[0]]]["time"]) if missing_valid[0] < len(clock_edges) else 0.0,
            "valid_o within 1..3 clocks of valid_i sample",
            f"missing_for_input_edges={missing_valid[:6]}",
            float(len(missing_valid)),
        )
    checks = min(residue_checks, output_checks)
    return _finish("v4_343", checks, errors, f"reset_clear={reset_clear} input_samples={len(samples)} output_valid={output_checks} matched={len(matched)}", 3)

CHECKER_ID = "v4_343_pipeline_adc_two_stage"
CHECKER: Checker = check_v4_343_pipeline_adc_two_stage
