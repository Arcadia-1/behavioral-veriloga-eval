"""Shared helpers for Issue109 factory-closure checker candidates.

This module preserves the observable formulas and colon-form diagnostics used
by the 250-268 aggregate factory candidates while allowing one explicit task
function per module.
"""

from __future__ import annotations

from bisect import bisect_right

Row = dict[str, float]
CheckResult = tuple[bool, str]

VTH = 0.45
VHI = 0.9
SPAN_MIN = 0.62
SPAN_MAX = 1.28

CONT_REQUIRED = {"time", "in0", "in1", "in2", "in3", "ctrl0", "ctrl1", "vdd", "vss", "en", "out", "flag", "metric"}
CLOCK_REQUIRED = CONT_REQUIRED | {"clk", "rst"}


def _clip01(value: float) -> float:
    return min(1.0, max(0.0, float(value)))


def _missing_columns(rows: list[Row], required: set[str]) -> str | None:
    if not rows:
        return "missing_columns=" + ",".join(sorted(required))
    missing = sorted(required - set(rows[0]))
    if missing:
        return "missing_columns=" + ",".join(missing)
    return None


def _times(rows: list[Row]) -> list[float]:
    return [float(row["time"]) for row in rows]


def _value_at(rows: list[Row], name: str, time_s: float) -> float | None:
    times = _times(rows)
    if not times or time_s < times[0] or time_s > times[-1]:
        return None
    idx = bisect_right(times, time_s)
    if idx <= 0:
        return float(rows[0][name])
    if idx >= len(rows):
        return float(rows[-1][name])
    t0, t1 = times[idx - 1], times[idx]
    y0, y1 = float(rows[idx - 1][name]), float(rows[idx][name])
    if t1 == t0:
        return y1
    frac = (time_s - t0) / (t1 - t0)
    return y0 + frac * (y1 - y0)


def _values_at(rows: list[Row], names: tuple[str, ...], time_s: float) -> dict[str, float] | None:
    values: dict[str, float] = {}
    for name in names:
        value = _value_at(rows, name, time_s)
        if value is None:
            return None
        values[name] = value
    return values


def _sample_times(rows: list[Row], count: int = 48) -> list[float]:
    times = _times(rows)
    if len(times) < 2:
        return []
    start = times[0] + 0.06 * (times[-1] - times[0])
    stop = times[-1] - 0.04 * (times[-1] - times[0])
    if stop <= start:
        return []
    return [start + (stop - start) * i / max(1, count - 1) for i in range(count)]


def _threshold_crossings(values: list[float], times: list[float], threshold: float, direction: str) -> list[float]:
    edges: list[float] = []
    for idx in range(1, len(values)):
        y0, y1 = float(values[idx - 1]), float(values[idx])
        rising = y0 < threshold <= y1
        falling = y0 > threshold >= y1
        if (direction == "rising" and not rising) or (direction == "falling" and not falling):
            continue
        if y1 == y0:
            edges.append(float(times[idx]))
        else:
            frac = (threshold - y0) / (y1 - y0)
            edges.append(float(times[idx - 1]) + frac * (float(times[idx]) - float(times[idx - 1])))
    return edges


def _normalized_inputs(values: dict[str, float]) -> dict[str, float]:
    span = values["vdd"] - values["vss"]
    norm_span = span if span >= 0.05 else 0.05
    return {
        "span": norm_span,
        "raw_span": span,
        "valid": 1.0 if values["en"] > VTH and SPAN_MIN <= span <= SPAN_MAX else 0.0,
        "x0": _clip01((values["in0"] - values["vss"]) / norm_span),
        "x1": _clip01((values["in1"] - values["vss"]) / norm_span),
        "x2": _clip01((values["in2"] - values["vss"]) / norm_span),
        "x3": _clip01((values["in3"] - values["vss"]) / norm_span),
        "c0": _clip01(values["ctrl0"] / VHI),
        "c1": _clip01(values["ctrl1"] / VHI),
    }


def _cont_expected(mode: str, values: dict[str, float]) -> dict[str, float]:
    state = _normalized_inputs(values)
    x0, x1, x2, x3 = state["x0"], state["x1"], state["x2"], state["x3"]
    c0, c1 = state["c0"], state["c1"]
    if mode == "gain":
        core = 0.82 * x0 + 0.18 * c0 + 0.08
        flag = core > 0.78
        metric = abs(core - x0) / 0.55
    elif mode == "sum":
        core = 0.36 * x0 + 0.28 * x1 + 0.18 * x2 + 0.10 * x3 + 0.04
        flag = core > 0.48
        metric = abs(x0 - x1) / 0.55
    elif mode == "window":
        core = x0
        flag = 0.24 <= x0 <= 0.72 and c0 > 0.35
        metric = abs(x0 - 0.48) / 0.48
    elif mode == "mux":
        idx = (2 if c1 > 0.5 else 0) + (1 if c0 > 0.5 else 0)
        selected = (x0, x1, x2, x3)[idx]
        core = 0.88 * selected + 0.04
        flag = idx > 0
        metric = idx / 3.0
    elif mode == "reduction":
        count = sum(1 for item in (x0, x1, x2, x3) if item > 0.50)
        core = count / 4.0
        flag = count >= 3
        metric = core
    elif mode == "phase":
        core = _clip01(0.5 + (x0 - x1) + 0.25 * (c0 - c1))
        flag = (x0 > 0.50) != (x1 > 0.50)
        metric = abs(x0 - x1)
    elif mode == "priority":
        core = 0.25 if x0 > 0.58 else 0.50 if x1 > 0.58 else 0.75 if x2 > 0.58 else 1.0 if c0 > 0.58 else 0.0
        flag = core >= 0.50
        metric = core
    elif mode == "translate":
        core = 0.76 * x0 + 0.18 * c1 + 0.12
        flag = state["raw_span"] >= 0.78
        metric = abs((values["in0"] - values["vss"]) - 0.5 * state["span"]) / state["span"]
    else:
        raise ValueError(f"unsupported_cont_mode={mode}")
    if state["valid"] <= 0.5:
        return {"out": 0.0, "flag": 0.0, "metric": 0.0}
    return {"out": VHI * _clip01(core), "flag": VHI if flag else 0.0, "metric": VHI * _clip01(metric)}


def _worst_error(observed: dict[str, float], expected: dict[str, float], time_s: float, previous: tuple[float, str]) -> tuple[float, str]:
    worst_err, worst_note = previous
    for name in ("out", "flag", "metric"):
        err = abs(observed[name] - expected[name])
        if err > worst_err:
            worst_err = err
            worst_note = (
                f"time={time_s:.4e} signal={name} expected={expected[name]:.5f} "
                f"observed={observed[name]:.5f} mismatch={err:.5f}"
            )
    return worst_err, worst_note


def check_continuous_factory(rows: list[Row], *, mode: str, task_name: str) -> CheckResult:
    missing = _missing_columns(rows, CONT_REQUIRED)
    if missing:
        return False, f"{task_name}: {missing}"
    checked = 0
    worst = (0.0, "")
    out_expected: list[float] = []
    flag_expected: list[float] = []
    metric_expected: list[float] = []
    saw_enable_low = False
    for time_s in _sample_times(rows):
        values = _values_at(rows, ("in0", "in1", "in2", "in3", "ctrl0", "ctrl1", "vdd", "vss", "en", "out", "flag", "metric"), time_s)
        if values is None:
            continue
        expected = _cont_expected(mode, values)
        before = _values_at(rows, ("in0", "in1", "in2", "in3", "ctrl0", "ctrl1", "vdd", "vss", "en"), max(float(rows[0]["time"]), time_s - 0.12e-9))
        after = _values_at(rows, ("in0", "in1", "in2", "in3", "ctrl0", "ctrl1", "vdd", "vss", "en"), min(float(rows[-1]["time"]), time_s + 0.12e-9))
        if before is not None and after is not None:
            before_expected = _cont_expected(mode, before)
            after_expected = _cont_expected(mode, after)
            if any(
                abs(before_expected[name] - after_expected[name]) > 0.08
                for name in ("out", "flag", "metric")
            ):
                continue
        observed = {"out": values["out"], "flag": values["flag"], "metric": values["metric"]}
        worst = _worst_error(observed, expected, time_s, worst)
        out_expected.append(expected["out"])
        flag_expected.append(expected["flag"])
        metric_expected.append(expected["metric"])
        saw_enable_low = saw_enable_low or values["en"] <= VTH
        checked += 1
    if checked < 10:
        return False, f"{task_name}: insufficient_samples={checked}"
    if not saw_enable_low:
        return False, f"{task_name}: missing_enable_low_coverage"
    if max(out_expected) - min(out_expected) < 0.16:
        return False, f"{task_name}: insufficient_out_dynamic_range"
    if max(flag_expected) - min(flag_expected) < 0.45:
        return False, f"{task_name}: insufficient_flag_dynamic_range"
    if max(metric_expected) - min(metric_expected) < 0.12:
        return False, f"{task_name}: insufficient_metric_dynamic_range"
    if worst[0] > 0.085:
        return False, f"{task_name}: max_error={worst[0]:.5f} {worst[1]}"
    return True, f"{task_name}: samples={checked} max_error={worst[0]:.5f}"


def check_clocked_factory(
    rows: list[Row],
    *,
    mode: str,
    edge: int,
    task_name: str,
    min_edges: int = 8,
    asynchronous_reset: bool = False,
) -> CheckResult:
    missing = _missing_columns(rows, CLOCK_REQUIRED)
    if missing:
        return False, f"{task_name}: {missing}"
    times = _times(rows)
    direction = "rising" if edge > 0 else "falling"
    edges = _threshold_crossings([row["clk"] for row in rows], times, VTH, direction)
    if len(edges) < min_edges:
        return False, (
            f"{task_name}: too_few_clock_edges={len(edges)} "
            f"required={min_edges} direction={direction}"
        )
    min_period = min((b - a for a, b in zip(edges, edges[1:])), default=1.0e-9)
    delay = min(0.12e-9, 0.12 * min_period)
    core_state = 0.0
    out_state = 0.0
    checked = 0
    worst = (0.0, "")
    out_expected: list[float] = []
    flag_expected: list[float] = []
    metric_expected: list[float] = []
    saw_reset = False
    saw_enable_low = False
    saw_invalid_low_span = False
    saw_invalid_high_span = False
    if asynchronous_reset:
        reset_assertions = _threshold_crossings(
            [row["rst"] for row in rows], times, VTH, "rising"
        )
        for reset_t in reset_assertions:
            output_t = reset_t + delay
            if output_t >= times[-1] - 0.05e-9:
                continue
            outputs = _values_at(rows, ("out", "flag", "metric"), output_t)
            if outputs is None:
                continue
            worst = _worst_error(
                outputs,
                {"out": 0.0, "flag": 0.0, "metric": 0.0},
                output_t,
                worst,
            )
            saw_reset = True
    for edge_t in edges:
        output_t = edge_t + delay
        if output_t >= times[-1] - 0.05e-9:
            continue
        inputs = _values_at(rows, ("rst", "in0", "in1", "in2", "in3", "ctrl0", "ctrl1", "vdd", "vss", "en"), edge_t + 1.0e-12)
        outputs = _values_at(rows, ("out", "flag", "metric"), output_t)
        if inputs is None or outputs is None:
            continue
        values = {name: inputs[name] for name in ("in0", "in1", "in2", "in3", "ctrl0", "ctrl1", "vdd", "vss", "en")}
        state = _normalized_inputs(values)
        saw_invalid_low_span = saw_invalid_low_span or state["raw_span"] < SPAN_MIN
        saw_invalid_high_span = saw_invalid_high_span or state["raw_span"] > SPAN_MAX
        x0, x1, x2, c0 = state["x0"], state["x1"], state["x2"], state["c0"]
        if inputs["rst"] > VTH or state["valid"] <= 0.5:
            core_state = 0.0
            out_state = 0.0
            expected = {"out": 0.0, "flag": 0.0, "metric": 0.0}
            saw_reset = saw_reset or inputs["rst"] > VTH
            saw_enable_low = saw_enable_low or inputs["en"] <= VTH
        elif mode in {"edge", "sample_fall"}:
            decision = x0 > x1
            expected = {"out": VHI if decision else 0.0, "flag": VHI if decision else 0.0, "metric": VHI * _clip01(abs(x0 - x1))}
        elif mode == "toggle":
            if x0 > 0.50:
                out_state = 0.0 if out_state > 0.45 else VHI
            expected = {"out": out_state, "flag": out_state, "metric": VHI * _clip01(abs(x0 - x1))}
        elif mode == "counter":
            if x0 > 0.25 and x1 > 0.20:
                core_state = min(4.0, core_state + 1.0)
            else:
                core_state = 0.0
            expected = {"out": VHI * _clip01(core_state / 4.0), "flag": VHI if core_state >= 3.0 else 0.0, "metric": VHI * _clip01(abs(x0 - x1))}
        elif mode == "latch":
            if c0 > 0.45:
                out_state = VHI * _clip01(0.70 * x0 + 0.30 * x1)
            expected = {"out": out_state, "flag": VHI if c0 > 0.45 else 0.0, "metric": VHI * _clip01(abs((out_state / VHI) - x2))}
        else:
            raise ValueError(f"unsupported_clock_mode={mode}")
        worst = _worst_error(outputs, expected, output_t, worst)
        out_expected.append(expected["out"])
        flag_expected.append(expected["flag"])
        metric_expected.append(expected["metric"])
        checked += 1
    if checked < min_edges:
        return False, (
            f"{task_name}: insufficient_clock_samples={checked} required={min_edges}"
        )
    if not (saw_reset and saw_enable_low):
        return False, f"{task_name}: missing_reset_or_enable_low_coverage reset={saw_reset} enable_low={saw_enable_low}"
    if not (saw_invalid_low_span and saw_invalid_high_span):
        return False, (
            f"{task_name}: missing_invalid_span_coverage "
            f"low={saw_invalid_low_span} high={saw_invalid_high_span}"
        )
    if max(out_expected) - min(out_expected) < 0.16:
        return False, f"{task_name}: insufficient_clock_out_dynamic_range"
    if max(flag_expected) - min(flag_expected) < 0.45:
        return False, f"{task_name}: insufficient_clock_flag_dynamic_range"
    if max(metric_expected) - min(metric_expected) < 0.12:
        return False, f"{task_name}: insufficient_clock_metric_dynamic_range"
    if worst[0] > 0.10:
        return False, f"{task_name}: max_error={worst[0]:.5f} {worst[1]}"
    return True, f"{task_name}: samples={checked} max_error={worst[0]:.5f} edge={direction}"


def check_clocked_output_hold(
    rows: list[Row],
    *,
    edge: int,
    task_name: str,
    min_intervals: int = 4,
) -> CheckResult:
    """Require clocked observables to remain stable between update events."""
    missing = _missing_columns(rows, CLOCK_REQUIRED)
    if missing:
        return False, f"{task_name}: {missing}"

    times = _times(rows)
    direction = "rising" if edge > 0 else "falling"
    clock_edges = _threshold_crossings(
        [row["clk"] for row in rows], times, VTH, direction
    )
    reset_assertions = _threshold_crossings(
        [row["rst"] for row in rows], times, VTH, "rising"
    )
    update_times = sorted(set(clock_edges + reset_assertions))

    checked = 0
    worst = (0.0, "")
    for start_t, end_t in zip(update_times, update_times[1:]):
        interval = end_t - start_t
        if interval <= 0.20e-9:
            continue
        guard = min(0.18e-9, 0.20 * interval)
        probe_start = start_t + guard
        probe_end = end_t - guard
        if probe_end <= probe_start:
            continue
        baseline: dict[str, float] | None = None
        interval_rows = 0
        for row in rows:
            row_time = float(row["time"])
            if row_time < probe_start or row_time > probe_end:
                continue
            if baseline is None:
                baseline = {
                    signal: float(row[signal])
                    for signal in ("out", "flag", "metric")
                }
                interval_rows = 1
                continue
            interval_rows += 1
            for signal in ("out", "flag", "metric"):
                if baseline is None:
                    continue
                error = abs(float(row[signal]) - baseline[signal])
                if error > worst[0]:
                    worst = (
                        error,
                        f"signal={signal} time={row_time:.6g} "
                        f"baseline={baseline[signal]:.5f} observed={float(row[signal]):.5f}",
                    )
        if interval_rows >= 2:
            checked += 1

    if checked < min_intervals:
        return False, (
            f"{task_name}: insufficient_hold_intervals={checked} "
            f"required={min_intervals} edge={direction}"
        )
    if worst[0] > 0.10:
        return False, (
            f"{task_name}: inter_edge_hold_error={worst[0]:.5f} {worst[1]}"
        )
    return True, (
        f"{task_name}: hold_intervals={checked} "
        f"max_hold_error={worst[0]:.5f} edge={direction}"
    )
