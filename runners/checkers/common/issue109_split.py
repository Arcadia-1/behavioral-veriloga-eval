"""Local checker-candidate utilities for canonical task-side 261_280.

These helpers intentionally mirror the observable formulas in the assigned
task family specs and keep diagnostics explicit: expected, observed, time, and
signal name are reported for the worst mismatch.
"""

from __future__ import annotations

from bisect import bisect_right
from math import isfinite


VTH = 0.45
VHI = 0.9
SPAN_MIN = 0.62
SPAN_MAX = 1.28


def clip01(value: float) -> float:
    return min(1.0, max(0.0, value))


def _missing(rows: list[dict[str, float]], required: set[str]) -> str | None:
    if not rows:
        return "missing_columns=" + ",".join(sorted(required))
    missing = sorted(required - set(rows[0]))
    return "missing_columns=" + ",".join(missing) if missing else None


def _values_at(rows: list[dict[str, float]], names: tuple[str, ...], time_s: float) -> dict[str, float] | None:
    times = [row["time"] for row in rows]
    idx = bisect_right(times, time_s)
    if idx <= 0:
        src = rows[0]
    elif idx >= len(rows):
        src = rows[-1]
    else:
        a = rows[idx - 1]
        b = rows[idx]
        dt = b["time"] - a["time"]
        frac = 0.0 if dt <= 0 else (time_s - a["time"]) / dt
        out = {"time": time_s}
        for name in names:
            if name == "time":
                continue
            if name not in a or name not in b:
                return None
            out[name] = a[name] + frac * (b[name] - a[name])
        return out
    if any(name not in src for name in names if name != "time"):
        return None
    return {name: (time_s if name == "time" else src[name]) for name in names}


def _crossings(rows: list[dict[str, float]], signal: str, threshold: float = VTH) -> list[float]:
    edges: list[float] = []
    for prev, cur in zip(rows, rows[1:]):
        a = prev[signal] - threshold
        b = cur[signal] - threshold
        if a < 0.0 <= b:
            dt = cur["time"] - prev["time"]
            frac = 0.0 if abs(b - a) < 1e-30 else -a / (b - a)
            edges.append(prev["time"] + frac * dt)
    return edges


def _stimulus_change_times(
    rows: list[dict[str, float]], signals: tuple[str, ...], tolerance: float = 1e-9
) -> list[float]:
    """Return trace times where a public stimulus is still changing.

    Continuous-output contracts may legitimately use the declared transition
    time. Sampling at the exact input breakpoint would then compare an output
    midpoint with its new steady-state target. Track public stimulus changes so
    individual checkers can request a short settling guard without weakening
    steady-state coverage.
    """

    changes: list[float] = []
    for previous, current in zip(rows, rows[1:]):
        if any(
            signal in previous
            and signal in current
            and abs(current[signal] - previous[signal]) > tolerance
            for signal in signals
        ):
            changes.append(current["time"])
    return changes


def _is_settled(change_times: list[float], time_s: float, settle_time_s: float) -> bool:
    if settle_time_s <= 0.0 or not change_times:
        return True
    idx = bisect_right(change_times, time_s) - 1
    return idx < 0 or time_s - change_times[idx] >= settle_time_s


def normalized(values: dict[str, float]) -> dict[str, float]:
    raw_span = values["vdd"] - values["vss"]
    span = max(raw_span, 0.05)
    valid = values["en"] > VTH and SPAN_MIN <= raw_span <= SPAN_MAX
    out = {"span": span, "raw_span": raw_span, "valid": 1.0 if valid else 0.0}
    for idx in range(4):
        out[f"x{idx}"] = clip01((values[f"in{idx}"] - values["vss"]) / span)
    out["c0"] = clip01(values["ctrl0"] / VHI)
    out["c1"] = clip01(values["ctrl1"] / VHI)
    return out


def cont_expected(mode: str, values: dict[str, float]) -> dict[str, float]:
    s = normalized(values)
    x0, x1, x2, x3, c0, c1 = s["x0"], s["x1"], s["x2"], s["x3"], s["c0"], s["c1"]
    if s["valid"] <= 0.5:
        return {"out": 0.0, "flag": 0.0, "metric": 0.0}
    if mode == "mux":
        idx = (2 if c1 > 0.5 else 0) + (1 if c0 > 0.5 else 0)
        selected = (x0, x1, x2, x3)[idx]
        return {
            "out": VHI * clip01(0.88 * selected + 0.04),
            "flag": VHI if idx > 0 else 0.0,
            "metric": VHI * clip01(idx / 3.0),
        }
    if mode == "reduction":
        count = sum(1 for item in (x0, x1, x2, x3) if item > 0.50)
        level = VHI * clip01(count / 4.0)
        return {"out": level, "flag": VHI if count >= 3 else 0.0, "metric": level}
    if mode == "sum":
        core = 0.36 * x0 + 0.28 * x1 + 0.18 * x2 + 0.10 * x3 + 0.04
        return {
            "out": VHI * clip01(core),
            "flag": VHI if core > 0.48 else 0.0,
            "metric": VHI * clip01(abs(x0 - x1) / 0.55),
        }
    if mode == "window":
        return {
            "out": VHI * clip01(x0),
            "flag": VHI if 0.24 <= x0 <= 0.72 and c0 > 0.35 else 0.0,
            "metric": VHI * clip01(abs(x0 - 0.48) / 0.48),
        }
    raise ValueError(f"unsupported continuous mode {mode}")


def clock_expected(mode: str, state: dict[str, float], values: dict[str, float]) -> dict[str, float]:
    s = normalized(values)
    x0, x1, x2, c0 = s["x0"], s["x1"], s["x2"], s["c0"]
    if values["rst"] > VTH or s["valid"] <= 0.5:
        state["core"] = 0.0
        state["out"] = 0.0
        return {"out": 0.0, "flag": 0.0, "metric": 0.0}
    if mode == "accum":
        aux = clip01(abs(x0 - x1) + 0.35 * c0)
        state["core"] = clip01(0.62 * state["core"] + 0.32 * aux)
        return {"out": VHI * state["core"], "flag": VHI if state["core"] > 0.58 else 0.0, "metric": VHI * aux}
    if mode == "counter":
        state["core"] = min(4.0, state["core"] + 1.0) if x0 > 0.25 and x1 > 0.20 else 0.0
        return {
            "out": VHI * clip01(state["core"] / 4.0),
            "flag": VHI if state["core"] >= 3.0 else 0.0,
            "metric": VHI * clip01(abs(x0 - x1)),
        }
    if mode == "latch":
        if c0 > VTH:
            state["out"] = VHI * clip01(0.70 * x0 + 0.30 * x1)
        return {
            "out": state["out"],
            "flag": VHI if c0 > VTH else 0.0,
            "metric": VHI * clip01(abs((state["out"] / VHI) - x2)),
        }
    if mode == "edge":
        decision = x0 > x1
        return {"out": VHI if decision else 0.0, "flag": VHI if decision else 0.0, "metric": VHI * clip01(abs(x0 - x1))}
    raise ValueError(f"unsupported clock mode {mode}")


def _update_worst(
    worst: dict[str, float | str],
    time_s: float,
    signal: str,
    expected: float,
    observed: float,
) -> None:
    err = abs(observed - expected)
    if err > float(worst["err"]):
        worst.update({"err": err, "time": time_s, "signal": signal, "expected": expected, "observed": observed})


def _format_mismatch(label: str, worst: dict[str, float | str]) -> str:
    return (
        f"{label}_mismatch signal={worst['signal']} time={float(worst['time']):.6e} "
        f"expected={float(worst['expected']):.6g} observed={float(worst['observed']):.6g} "
        f"mismatch={float(worst['err']):.6g}"
    )


def check_continuous(
    rows: list[dict[str, float]],
    mode: str,
    label: str,
    *,
    settle_time_s: float = 0.0,
) -> tuple[bool, str]:
    required = {"time", "in0", "in1", "in2", "in3", "ctrl0", "ctrl1", "vdd", "vss", "en", "out", "flag", "metric"}
    msg = _missing(rows, required)
    if msg:
        return False, msg
    rows = sorted(rows, key=lambda row: row["time"])
    names = tuple(sorted(required))
    stimulus_signals = (
        "in0", "in1", "in2", "in3", "ctrl0", "ctrl1", "vdd", "vss", "en"
    )
    change_times = _stimulus_change_times(rows, stimulus_signals)
    start, stop = rows[0]["time"], rows[-1]["time"]
    checked = 0
    saw_disabled = False
    expected_ranges = {"out": [], "flag": [], "metric": []}
    worst: dict[str, float | str] = {"err": 0.0, "time": 0.0, "signal": "", "expected": 0.0, "observed": 0.0}
    for idx in range(1, 80):
        time_s = start + (stop - start) * idx / 80.0
        if not _is_settled(change_times, time_s, settle_time_s):
            continue
        values = _values_at(rows, names, time_s)
        if values is None or any(not isfinite(values[name]) for name in names if name != "time"):
            continue
        expected = cont_expected(mode, values)
        for signal in ("out", "flag", "metric"):
            expected_ranges[signal].append(expected[signal])
            _update_worst(worst, time_s, signal, expected[signal], values[signal])
        saw_disabled = saw_disabled or values["en"] <= VTH or not (SPAN_MIN <= values["vdd"] - values["vss"] <= SPAN_MAX)
        checked += 1
    if checked < 12:
        return False, f"{label}_insufficient_samples checked={checked}"
    if not saw_disabled:
        return False, f"{label}_missing_disabled_or_bad_span_coverage checked={checked}"
    for signal, values in expected_ranges.items():
        if max(values) - min(values) < (0.40 if signal == "flag" else 0.10):
            return False, f"{label}_insufficient_expected_dynamic_range signal={signal}"
    if float(worst["err"]) > 0.085:
        return False, _format_mismatch(label, worst)
    return True, f"{label}_samples={checked} max_mismatch={float(worst['err']):.6g}"


def check_clocked(rows: list[dict[str, float]], mode: str, label: str) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "in0", "in1", "in2", "in3", "ctrl0", "ctrl1", "vdd", "vss", "en", "out", "flag", "metric"}
    msg = _missing(rows, required)
    if msg:
        return False, msg
    rows = sorted(rows, key=lambda row: row["time"])
    edges = _crossings(rows, "clk")
    if len(edges) < 6:
        return False, f"{label}_too_few_clock_edges edges={len(edges)}"
    min_period = min((b - a for a, b in zip(edges, edges[1:])), default=1e-9)
    delay = min(0.12e-9, 0.12 * min_period)
    names = tuple(sorted(required - {"out", "flag", "metric"}))
    state = {"core": 0.0, "out": 0.0}
    checked = 0
    saw_reset = False
    saw_disabled = False
    expected_ranges = {"out": [], "flag": [], "metric": []}
    worst: dict[str, float | str] = {"err": 0.0, "time": 0.0, "signal": "", "expected": 0.0, "observed": 0.0}
    for edge_t in edges:
        sample_t = edge_t + delay
        if sample_t >= rows[-1]["time"]:
            continue
        values = _values_at(rows, names, edge_t + 1e-12)
        outputs = _values_at(rows, ("out", "flag", "metric"), sample_t)
        if values is None or outputs is None:
            continue
        expected = clock_expected(mode, state, values)
        for signal in ("out", "flag", "metric"):
            expected_ranges[signal].append(expected[signal])
            _update_worst(worst, sample_t, signal, expected[signal], outputs[signal])
        saw_reset = saw_reset or values["rst"] > VTH
        saw_disabled = saw_disabled or values["en"] <= VTH or not (SPAN_MIN <= values["vdd"] - values["vss"] <= SPAN_MAX)
        checked += 1
    if checked < 6:
        return False, f"{label}_insufficient_edge_samples checked={checked}"
    if not (saw_reset and saw_disabled):
        return False, f"{label}_missing_reset_or_disabled_coverage reset={saw_reset} disabled={saw_disabled}"
    for signal, values in expected_ranges.items():
        if max(values) - min(values) < (0.40 if signal == "flag" else 0.10):
            return False, f"{label}_insufficient_expected_dynamic_range signal={signal}"
    if float(worst["err"]) > 0.10:
        return False, _format_mismatch(label, worst)
    return True, f"{label}_edges={checked} max_mismatch={float(worst['err']):.6g}"
