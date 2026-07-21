"""Task-specific checker for canonical v4 DUT 343."""
from __future__ import annotations

from ..api import Checker
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
    reset_clear_rows = [
        row for row in rows
        if _high(row, "rst")
        and _code(row, ["code_0", "code_1", "code_2", "code_3"]) == 0
        and not _high(row, "valid_o")
        and abs(float(row["residue_dbg"])) < 0.04
    ]
    reset_clear = bool(reset_clear_rows)
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

    sample_times = [float(rows[clock_edges[sample[0]]]["time"]) for sample in samples]
    first_sample_time = min(sample_times, default=0.0)
    last_sample_time = max(sample_times, default=0.0)
    mid_reset_time = next(
        (
            float(row["time"])
            for row in reset_clear_rows
            if first_sample_time < float(row["time"]) < last_sample_time
        ),
        None,
    )
    mid_reset_clear = mid_reset_time is not None
    if not mid_reset_clear:
        _mismatch(errors, "P_PIPE_MIDRUN_RESET_CLEAR", 0.0, "mid-run reset clears code/valid/residue between valid samples", "not observed")

    expected_by_edge: dict[int, tuple[int, tuple[int, float, int]]] = {}
    reset_blocked_samples: set[int] = set()
    for sample_index, sample in enumerate(samples):
        expected_edge = sample[0] + 2
        if expected_edge >= len(clock_edges) or _high(rows[clock_edges[expected_edge]], "rst"):
            reset_blocked_samples.add(sample_index)
            continue
        expected_by_edge[expected_edge] = (sample_index, sample)
    matched: set[int] = set()
    output_checks = 0
    valid_outputs_by_edge: set[int] = set()
    for edge_number, index in enumerate(clock_edges):
        observed = _row_after(rows, float(rows[index]["time"]))
        if _high(observed, "rst") or not _high(observed, "valid_o"):
            continue
        valid_outputs_by_edge.add(edge_number)
        observed_code = _code(observed, ["code_0", "code_1", "code_2", "code_3"])
        selected = expected_by_edge.get(edge_number)
        if selected is None or selected[0] in matched:
            _mismatch(errors, "P_PIPE_EXACT_LATENCY", float(observed["time"]), "valid_o only on sample_edge+2", f"valid_at_edge={edge_number}")
        elif selected[1][2] != observed_code:
            _mismatch(errors, "P_PIPE_ALIGNED_CODE", float(observed["time"]), selected[1][2], observed_code)
        else:
            matched.add(selected[0])
        output_checks += 1
    missing_valid = [
        sample[0]
        for sample_index, sample in enumerate(samples)
        if sample_index not in matched
        and sample_index not in reset_blocked_samples
        and sample[0] + 2 not in valid_outputs_by_edge
    ]
    if missing_valid:
        _mismatch(
            errors,
            "P_PIPE_VALID_LATENCY",
            float(rows[clock_edges[missing_valid[0]]]["time"]) if missing_valid[0] < len(clock_edges) else 0.0,
            "valid_o exactly two rising clocks after valid_i sample",
            f"missing_for_input_edges={missing_valid[:6]}",
            float(len(missing_valid)),
        )
    post_reset_samples = [
        sample for sample in samples
        if mid_reset_time is not None and float(rows[clock_edges[sample[0]]]["time"]) > mid_reset_time
    ]
    if mid_reset_clear and not post_reset_samples:
        _mismatch(errors, "P_PIPE_RESET_RECOVERY", mid_reset_time or 0.0, "post-reset valid_i sample", "not observed")
    checks = min(residue_checks, output_checks)
    return _finish("v4_343", checks, errors, f"reset_clear={reset_clear} mid_reset_clear={mid_reset_clear} post_reset_samples={len(post_reset_samples)} input_samples={len(samples)} output_valid={output_checks} matched={len(matched)}", 3)

CHECKER_ID = "v4_343_pipeline_adc_two_stage"
CHECKER: Checker = check_v4_343_pipeline_adc_two_stage
