"""Task-specific checker for canonical v4 DUT 342."""
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

def _expected_trials(sample: float) -> list[int]:
    final_code = 0
    trial_code = 8
    sequence = [trial_code]
    for bit in (3, 2, 1, 0):
        weight = 1 << bit
        if sample >= VDD * trial_code / 16.0:
            final_code = trial_code
        else:
            final_code = trial_code - weight
        trial_code = final_code if bit == 0 else final_code + (1 << (bit - 1))
        sequence.append(trial_code)
    return sequence

def _rail_gap(value: float) -> float:
    return min(abs(value), abs(value - VDD))

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

def check_v4_342_sar_adc_system_4b(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {
        "time", "vin", "clk", "rst", "start", "code_3", "code_2", "code_1",
        "code_0", "done", "sample_dbg", "dac_dbg",
    }
    missing = _missing(rows, required)
    if missing:
        return False, f"v4_342 missing_signals={','.join(missing)}"
    errors: list[str] = []
    reset_rows = [row for row in rows if _high(row, "rst")]
    reset_check_rows = []
    if reset_rows:
        reset_start = float(reset_rows[0]["time"])
        reset_check_rows = [
            row for row in reset_rows if float(row["time"]) >= reset_start + SETTLE
        ] or [reset_rows[-1]]
    reset_failures = [
        row
        for row in reset_check_rows
        if _code(row, ["code_0", "code_1", "code_2", "code_3"]) != 0
        or _high(row, "done")
        or abs(float(row["sample_dbg"])) >= 0.04
        or abs(float(row["dac_dbg"])) >= 0.04
    ]
    reset_clear = bool(reset_check_rows) and not reset_failures
    if not reset_clear:
        observed = reset_failures[0] if reset_failures else None
        _mismatch(
            errors,
            "P_SAR_RESET_CLEAR",
            float(observed["time"]) if observed else 0.0,
            "code=0 done=0 sample_dbg=0 dac_dbg=0",
            (
                f"code={_code(observed, ['code_0', 'code_1', 'code_2', 'code_3'])} "
                f"done={float(observed['done']):.6g} sample_dbg={float(observed['sample_dbg']):.6g} "
                f"dac_dbg={float(observed['dac_dbg']):.6g}"
                if observed
                else "no settled reset sample"
            ),
        )

    clock_edges = _rising_indices(rows, "clk")
    start_edges = _rising_indices(rows, "start")
    checks = 0
    trial_checks = 0
    completion_hold_checks = 0
    codes: set[int] = set()
    for start_number, start_index in enumerate(start_edges):
        start_time = float(rows[start_index]["time"])
        following = [index for index in clock_edges if float(rows[index]["time"]) > start_time]
        if len(following) < 5:
            continue
        sample_edge = following[0]
        final_edge = following[4]
        sample_time = float(rows[sample_edge]["time"])
        final_time = float(rows[final_edge]["time"])
        sample_input = float(rows[sample_edge]["vin"])
        conversion_edges = following[:5]
        observed_rows = [_row_after(rows, float(rows[index]["time"])) for index in conversion_edges]
        hold_rows = [
            row
            for row in rows
            if sample_time + SETTLE <= float(row["time"]) <= final_time + SETTLE
        ] or observed_rows
        hold_gaps = [_gap(sample_input, float(row["sample_dbg"])) for row in hold_rows]
        if max(hold_gaps) > 0.035:
            worst = max(range(len(hold_gaps)), key=hold_gaps.__getitem__)
            _mismatch(
                errors, "P_SAR_SAMPLE_HOLD", float(hold_rows[worst]["time"]), sample_input,
                float(hold_rows[worst]["sample_dbg"]), hold_gaps[worst],
            )
        expected_trials = _expected_trials(sample_input)
        for position, (edge_index, observed, expected_trial) in enumerate(
            zip(conversion_edges, observed_rows, expected_trials)
        ):
            edge_time = float(rows[edge_index]["time"])
            expected_dac = VDD * expected_trial / 16.0
            observed_dac = float(observed["dac_dbg"])
            if _gap(expected_dac, observed_dac) > 0.045:
                _mismatch(errors, "P_SAR_DAC_TRIAL", edge_time, expected_dac, observed_dac, _gap(expected_dac, observed_dac))
            expected_done = position == 4
            if _high(observed, "done") != expected_done:
                _mismatch(errors, "P_SAR_COMPLETION", edge_time, int(expected_done), int(_high(observed, "done")), 1.0)
            for signal in ("code_3", "code_2", "code_1", "code_0"):
                value = float(observed[signal])
                if _rail_gap(value) > 0.12:
                    _mismatch(errors, "P_SAR_FINAL_CODE", edge_time, "vss-or-vdd rail", value, _rail_gap(value))
                    break
            done_value = float(observed["done"])
            if _rail_gap(done_value) > 0.12:
                _mismatch(errors, "P_SAR_COMPLETION", edge_time, "vss-or-vdd rail", done_value, _rail_gap(done_value))
            trial_checks += 1
        expected_code = max(0, min(15, int(16.0 * sample_input / VDD)))
        final = observed_rows[-1]
        observed_code = _code(final, ["code_0", "code_1", "code_2", "code_3"])
        codes.add(observed_code)
        if observed_code != expected_code:
            _mismatch(errors, "P_SAR_FINAL_CODE", final_time, expected_code, observed_code, abs(expected_code - observed_code))

        next_start_time = (
            float(rows[start_edges[start_number + 1]]["time"])
            if start_number + 1 < len(start_edges)
            else float(rows[-1]["time"]) + SETTLE
        )
        reset_after_final = [
            float(row["time"])
            for row in rows
            if float(row["time"]) > final_time and _high(row, "rst")
        ]
        hold_end = min([next_start_time, *reset_after_final])
        completion_rows = [
            row
            for row in rows
            if final_time + SETTLE <= float(row["time"]) < hold_end
        ]
        completion_failures = [
            row
            for row in completion_rows
            if not _high(row, "done")
            or _rail_gap(float(row["done"])) > 0.12
            or _code(row, ["code_0", "code_1", "code_2", "code_3"]) != expected_code
        ]
        if completion_failures:
            observed = completion_failures[0]
            _mismatch(
                errors,
                "P_SAR_COMPLETION",
                float(observed["time"]),
                f"done={VDD} stable_code={expected_code}",
                (
                    f"done={float(observed['done']):.6g} "
                    f"code={_code(observed, ['code_0', 'code_1', 'code_2', 'code_3'])}"
                ),
            )
        completion_hold_checks += len(completion_rows)
        checks += 1
    if checks and completion_hold_checks == 0:
        _mismatch(
            errors,
            "P_SAR_COMPLETION",
            float(rows[-1]["time"]),
            "at least one settled post-completion hold sample",
            "none observed",
        )
    return _finish(
        "v4_342", checks, errors,
        (
            f"reset_clear={reset_clear} reset_checks={len(reset_check_rows)} "
            f"trial_checks={trial_checks} completion_hold_checks={completion_hold_checks} "
            f"codes={sorted(codes)}"
        ),
        2,
    )

CHECKER_ID = "v4_342_sar_adc_system_4b"
CHECKER: Checker = check_v4_342_sar_adc_system_4b
