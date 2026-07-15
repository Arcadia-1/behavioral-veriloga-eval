"""Task-specific checker for canonical v4 DUT 347."""
from __future__ import annotations

from ..api import Checker
from _bisect import bisect_left

SETTLE = 6.5e-10
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

def check_v4_347_power_reset_sequencer_system(rows: list[dict[str, float]]) -> tuple[bool, str]:
    outputs = ["por_n", "rst_n_core", "en_ana", "en_dig", "ready"]
    required = {"time", "vdd_sense", "clk", "rst_n_ext", "enable_req", *outputs}
    missing = _missing(rows, required)
    if missing:
        return False, f"v4_347 missing_signals={','.join(missing)}"
    errors: list[str] = []
    good_count = 0
    por = core = False
    stage = 0
    ready = False
    checks = 0
    startup_seen = brownout_seen = False
    for index in _rising_indices(rows, "clk"):
        edge = rows[index]
        time_s = float(edge["time"])
        power_good = float(edge["vdd_sense"]) >= 0.72 and _high(edge, "rst_n_ext")
        old_por, old_core = por, core
        old_ana = stage >= 1 and old_core
        old_dig = stage >= 2 and old_core
        if not power_good:
            good_count = 0
            por = core = ready = False
            stage = 0
            brownout_seen = True
        else:
            good_count = min(2, good_count + 1)
            por = good_count >= 2
            if not old_por:
                core = False
            elif _high(edge, "enable_req"):
                core = True
            if not old_core:
                stage = 0
            else:
                stage = min(2, stage + 1)
            ready = old_ana and old_dig
        observed = _row_after(rows, time_s)
        expected = [por, core and por, stage >= 1 and core and por, stage >= 2 and core and por, ready and por]
        for signal, value in zip(outputs, expected):
            if _high(observed, signal) != value:
                _mismatch(errors, "P_PWR_SEQUENCE_ORDER", time_s, f"{signal}={int(value)}", f"{signal}={int(_high(observed, signal))}", 1.0)
        startup_seen = startup_seen or all(_high(observed, signal) for signal in outputs)
        checks += 1
    async_clear = any(
        (float(row["vdd_sense"]) < 0.68 or not _high(row, "rst_n_ext"))
        and all(not _high(row, signal) for signal in outputs)
        for row in rows
    )
    if not async_clear:
        _mismatch(errors, "P_PWR_ASYNC_CLEAR", 0.0, "all outputs low during reset/brownout", "not observed")
    return _finish("v4_347", checks, errors, f"startup_seen={startup_seen} brownout_seen={brownout_seen} async_clear={async_clear}", 10)

CHECKER_ID = "v4_347_power_reset_sequencer_system"
CHECKER: Checker = check_v4_347_power_reset_sequencer_system
