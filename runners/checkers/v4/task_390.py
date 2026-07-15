"""Task-specific checker for canonical v4 DUT 390."""
from __future__ import annotations

from ..api import Checker
VCM = 0.45
VTH = 0.45

def _high(row: dict[str, float], signal: str, threshold: float = VTH) -> bool:
    return float(row[signal]) > threshold

def _rising(previous: dict[str, float], current: dict[str, float], signal: str, threshold: float = VTH) -> bool:
    return float(previous[signal]) <= threshold < float(current[signal])

def _sample_after(rows: list[dict[str, float]], event_index: int, delay: float = 4e-10) -> dict[str, float]:
    target = float(rows[event_index]["time"]) + delay
    for row in rows[event_index:]:
        if float(row["time"]) >= target:
            return row
    return rows[-1]

def _required(rows: list[dict[str, float]], signals: set[str], task: str) -> tuple[bool, str | None]:
    if not rows:
        return False, f"{task} trace_error=empty_trace"
    missing = sorted(signals - set(rows[0]))
    if missing:
        return False, f"{task} trace_error=missing_signals observed={','.join(missing)}"
    return True, None

def _new_mismatches(properties: list[str]) -> MismatchMap:
    return {property_id: [] for property_id in properties}

def _add(
    mismatches: MismatchMap,
    property_id: str,
    row: dict[str, float],
    expected: str,
    observed: str,
    gap: float,
) -> None:
    if len(mismatches[property_id]) < 24:
        mismatches[property_id].append((float(row["time"]), expected, observed, abs(float(gap))))

def _finish(task: str, properties: list[str], mismatches: MismatchMap, coverage: dict[str, int]) -> tuple[bool, str]:
    parts = [f"task={task}"]
    ok = True
    for property_id in properties:
        items = mismatches[property_id]
        count = len(items)
        if count:
            ok = False
            time, expected, observed, gap = items[0]
            parts.append(
                f"{property_id}:mismatch_count={count} expected={expected} "
                f"observed={observed} time={time:.6e} gap={gap:.6g}"
            )
        else:
            parts.append(
                f"{property_id}:mismatch_count=0 expected=contract_satisfied "
                "observed=contract_satisfied time=NA gap=0"
            )
    parts.append("coverage=" + ",".join(f"{key}:{value}" for key, value in sorted(coverage.items())))
    return ok, " | ".join(parts)

def _code(row: dict[str, float], names: list[str]) -> int:
    return sum((1 << bit) for bit, name in enumerate(names) if _high(row, name))

def _active(row: dict[str, float], reset: str = "rst", enable: str = "enable") -> bool:
    return not _high(row, reset) and _high(row, enable)

def _inactive_settled(rows: list[dict[str, float]], index: int, delay: float = 5e-10) -> bool:
    """Require controls to have remained inactive beyond output transition time."""
    target = float(rows[index]["time"]) - delay
    if target < float(rows[0]["time"]):
        return False
    for previous in reversed(rows[: index + 1]):
        if float(previous["time"]) <= target:
            return not _active(previous)
    return False

def check_v4_390_common_mode_feedback_loop(rows: list[dict[str, float]]) -> tuple[bool, str]:
    properties = [
        "P_RESET_DISABLE_CLEAR", "P_COMMON_MODE_ERROR", "P_TRIM_DIRECTION",
        "P_DIFFERENTIAL_PRESERVATION", "P_LOCK_QUALIFICATION",
    ]
    required = {"time", "vop_in", "von_in", "clk", "rst", "enable", "vop_out", "von_out", "trim_2", "trim_1", "trim_0", "cm_error", "locked"}
    valid, note = _required(rows, required, "v4_390")
    if not valid:
        return False, note or "v4_390 trace_error=unknown"
    mismatches = _new_mismatches(properties)
    coverage = {"inactive_rows": 0, "clock_edges": 0, "nonzero_trim": 0, "lock_samples": 0}
    previous_code = 0
    in_tolerance_streak = 0
    previous = rows[0]
    for index, row in enumerate(rows):
        if not _active(row):
            coverage["inactive_rows"] += 1
            if _inactive_settled(rows, index) and (abs(float(row["cm_error"])) > 0.035 or _code(row, ["trim_0", "trim_1", "trim_2"]) != 0 or _high(row, "locked")):
                _add(mismatches, "P_RESET_DISABLE_CLEAR", row, "trim=0,cm_error=0,locked=0", f"trim={_code(row,['trim_0','trim_1','trim_2'])},cm_error={row['cm_error']:.4g},locked={int(_high(row,'locked'))}", max(abs(float(row["cm_error"])), float(_code(row,["trim_0","trim_1","trim_2"]))))
            if _inactive_settled(rows, index) and (abs(float(row["vop_out"]) - float(row["vop_in"])) > 0.04 or abs(float(row["von_out"]) - float(row["von_in"])) > 0.04):
                _add(mismatches, "P_RESET_DISABLE_CLEAR", row, "output_bypass", f"vop_out={row['vop_out']:.4g},von_out={row['von_out']:.4g}", max(abs(float(row["vop_out"])-float(row["vop_in"])), abs(float(row["von_out"])-float(row["von_in"]))))
            previous_code = 0
            in_tolerance_streak = 0
        elif index and _rising(previous, row, "clk"):
            sample = _sample_after(rows, index, 7e-10)
            coverage["clock_edges"] += 1
            code = _code(sample, ["trim_0", "trim_1", "trim_2"])
            if code:
                coverage["nonzero_trim"] += 1
            raw_error = 0.5 * (float(row["vop_in"]) + float(row["von_in"])) - VCM
            residual_before = raw_error - 0.01 * previous_code
            expected_code = previous_code
            if residual_before > 0.01 and previous_code < 7:
                expected_code += 1
            elif residual_before < -0.01 and previous_code > 0:
                expected_code -= 1
            if code != expected_code:
                _add(mismatches, "P_TRIM_DIRECTION", sample, f"trim_code={expected_code}", f"trim_code={code}", code - expected_code)
            residual_after = raw_error - 0.01 * code
            in_tolerance_streak = in_tolerance_streak + 1 if abs(residual_after) <= 0.0105 else 0
            expected_lock = in_tolerance_streak >= 2
            observed_lock = _high(sample, "locked")
            coverage["lock_samples"] += 1
            if observed_lock and in_tolerance_streak < 2:
                _add(mismatches, "P_LOCK_QUALIFICATION", sample, f"locked=0 before_two_updates streak={in_tolerance_streak}", "locked=1", 1.0)
            if not observed_lock and in_tolerance_streak >= 3:
                _add(mismatches, "P_LOCK_QUALIFICATION", sample, f"locked=1 after_streak={in_tolerance_streak}", "locked=0", 1.0)
            previous_code = code
        if _active(row):
            expected_error = 0.5 * (float(row["vop_out"]) + float(row["von_out"])) - VCM
            if abs(float(row["cm_error"]) - expected_error) > 0.035:
                _add(mismatches, "P_COMMON_MODE_ERROR", row, f"cm_error={expected_error:.5g}", f"cm_error={row['cm_error']:.5g}", float(row["cm_error"]) - expected_error)
            in_diff = float(row["vop_in"]) - float(row["von_in"])
            out_diff = float(row["vop_out"]) - float(row["von_out"])
            if in_diff * out_diff < -0.002 or abs(out_diff - in_diff) > 0.05:
                _add(mismatches, "P_DIFFERENTIAL_PRESERVATION", row, f"output_diff={in_diff:.5g}", f"output_diff={out_diff:.5g}", out_diff - in_diff)
        previous = row
    if coverage["clock_edges"] < 5:
        _add(mismatches, "P_TRIM_DIRECTION", rows[-1], "at_least_5_enabled_clock_edges", f"clock_edges={coverage['clock_edges']}", 5 - coverage["clock_edges"])
    return _finish("v4_390_common_mode_feedback_loop", properties, mismatches, coverage)

CHECKER_ID = "v4_390_common_mode_feedback_loop"
CHECKER: Checker = check_v4_390_common_mode_feedback_loop
