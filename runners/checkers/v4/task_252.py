from __future__ import annotations

from bisect import bisect_left
from math import isfinite

from ..api import Checker
from ..common.issue109_factory import CheckResult, Row
from ..common.issue109_split import SPAN_MAX, SPAN_MIN, VTH, cont_expected, normalized
from .factory_property_diagnostics import append_continuous_property_diagnostics


TASK_LABEL = 'v4_252_supply_qualified_window_flag'
SOURCE_TASK_ID = 'v3_343_supply_qualified_window_flag'
LEGACY_SYMBOL = '343-supply-qualified-window-flag'

_REQUIRED = {
    "time", "in0", "in1", "in2", "in3", "ctrl0", "ctrl1",
    "vdd", "vss", "en", "out", "flag", "metric",
}


def _regime(row: Row) -> tuple[bool, bool]:
    state = normalized(row)
    valid = bool(state["valid"] > 0.5)
    flag = bool(valid and 0.24 <= state["x0"] <= 0.72 and state["c0"] > 0.35)
    return valid, flag


def _sample(rows: list[Row], times: list[float], time_s: float) -> Row | None:
    index = bisect_left(times, time_s)
    if index < len(times) and abs(times[index] - time_s) <= 1e-18:
        return dict(rows[index])
    if index <= 0 or index >= len(rows):
        return None
    before, after = rows[index - 1], rows[index]
    # Do not linearly blend across a validity or discrete flag boundary.  An
    # adaptive trace can legitimately bracket an instantaneous regime change
    # with a wide interval; interpolating the outputs there invents behavior.
    if _regime(before) != _regime(after):
        return None
    before_state = normalized(before)
    after_state = normalized(after)
    if max(
        abs(float(before_state[name]) - float(after_state[name]))
        for name in ("x0", "x1", "x2", "x3", "c0", "c1", "valid")
    ) > 0.12:
        return None
    dt = times[index] - times[index - 1]
    if dt <= 0.0:
        return None
    fraction = (time_s - times[index - 1]) / dt
    sample = {
        name: time_s if name == "time" else before[name] + fraction * (after[name] - before[name])
        for name in _REQUIRED
    }
    if _regime(sample) != _regime(before):
        return None
    return sample


def check_window_continuous_physical(rows: list[Row], task_name: str) -> CheckResult:
    if not rows:
        return False, f"{task_name}_missing_columns=" + ",".join(sorted(_REQUIRED))
    missing = sorted(_REQUIRED - set(rows[0]))
    if missing:
        return False, f"{task_name}_missing_columns=" + ",".join(missing)
    rows = sorted(rows, key=lambda row: float(row["time"]))
    times = [float(row["time"]) for row in rows]
    start, stop = times[0], times[-1]
    if stop <= start:
        return False, f"{task_name}_insufficient_time_span"
    checked = 0
    saw_disabled = False
    expected_ranges = {name: [] for name in ("out", "flag", "metric")}
    worst = (0.0, 0.0, "", 0.0, 0.0)
    for index in range(1, 96):
        time_s = start + (stop - start) * index / 96.0
        values = _sample(rows, times, time_s)
        if values is None or any(not isfinite(float(values[name])) for name in _REQUIRED):
            continue
        state = normalized(values)
        # Avoid grading within the analogue uncertainty band of a discrete
        # validity/flag decision; stable behavior on either side remains fully
        # covered by the fixed physical sample grid.
        raw_span = state["raw_span"]
        if min(abs(raw_span - SPAN_MIN), abs(raw_span - SPAN_MAX)) <= 0.03:
            continue
        if abs(state["x0"] - 0.24) <= 0.03 or abs(state["x0"] - 0.72) <= 0.03:
            continue
        expected = cont_expected("window", values)
        for signal in ("out", "flag", "metric"):
            observed = float(values[signal])
            target = float(expected[signal])
            error = abs(observed - target)
            expected_ranges[signal].append(target)
            if error > worst[0]:
                worst = (error, time_s, signal, target, observed)
        saw_disabled = saw_disabled or values["en"] <= VTH or not (SPAN_MIN <= raw_span <= SPAN_MAX)
        checked += 1
    if checked < 12:
        return False, f"{task_name}_insufficient_samples checked={checked}"
    if not saw_disabled:
        return False, f"{task_name}_missing_disabled_or_bad_span_coverage checked={checked}"
    for signal, values in expected_ranges.items():
        minimum_span = 0.40 if signal == "flag" else 0.10
        if max(values) - min(values) < minimum_span:
            return False, f"{task_name}_insufficient_expected_dynamic_range signal={signal}"
    if worst[0] > 0.085:
        return False, (
            f"{task_name}_mismatch signal={worst[2]} time={worst[1]:.6e} "
            f"expected={worst[3]:.6g} observed={worst[4]:.6g} max_error={worst[0]:.6g}"
        )
    return True, f"{task_name}_samples={checked} max_mismatch={worst[0]:.6g}"


def check_v4_252_supply_qualified_window_flag(rows: list[Row]) -> CheckResult:
    """Check v4_252_supply_qualified_window_flag: Supply Qualified Window Flag continuous window behavior."""
    ok, note = check_window_continuous_physical(rows, TASK_LABEL)
    return ok, append_continuous_property_diagnostics(
        rows,
        note,
        mode='window',
        normalization_property_id='P_MEASURE_ANALOG_INPUTS_RELATIVE_TO_THE',
        function_property_id='P_WHEN_VALID_DRIVE_OUT_VHI_CLIP01',
    )


CHECKS = {
    TASK_LABEL: check_v4_252_supply_qualified_window_flag,
    SOURCE_TASK_ID: check_v4_252_supply_qualified_window_flag,
    LEGACY_SYMBOL: check_v4_252_supply_qualified_window_flag,
}

CHECKER_ID = TASK_LABEL
CHECKER: Checker = check_v4_252_supply_qualified_window_flag
