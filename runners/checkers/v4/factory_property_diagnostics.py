"""Observable property diagnostics for factory checkers."""
from __future__ import annotations

from ..common.issue109_factory import (
    CLOCK_REQUIRED,
    CONT_REQUIRED,
    VHI,
    VTH,
    _clip01,
    _cont_expected,
    _normalized_inputs,
    _sample_times,
    _threshold_crossings,
    _values_at,
)


def append_continuous_property_diagnostics(
    rows: list[dict[str, float]],
    note: str,
    *,
    mode: str,
    normalization_property_id: str,
    function_property_id: str,
    tolerance: float = 0.085,
) -> str:
    """Append black-box mismatch counts without changing checker pass/fail.

    The normalization property is observed end to end, so it counts any
    sampled output-contract mismatch. The downstream function property counts
    mismatches only while the normalized input row is valid.
    """

    normalization_mismatches = 0
    function_mismatches = 0
    if rows and CONT_REQUIRED.issubset(rows[0]):
        names = (
            "in0",
            "in1",
            "in2",
            "in3",
            "ctrl0",
            "ctrl1",
            "vdd",
            "vss",
            "en",
            "out",
            "flag",
            "metric",
        )
        for time_s in _sample_times(rows):
            values = _values_at(rows, names, time_s)
            if values is None:
                continue
            before = _values_at(
                rows,
                names[:9],
                max(float(rows[0]["time"]), time_s - 0.12e-9),
            )
            after = _values_at(
                rows,
                names[:9],
                min(float(rows[-1]["time"]), time_s + 0.12e-9),
            )
            if before is not None and after is not None:
                before_flag = _cont_expected(mode, before)["flag"]
                after_flag = _cont_expected(mode, after)["flag"]
                if abs(before_flag - after_flag) > 0.45:
                    continue

            expected = _cont_expected(mode, values)
            mismatched = any(
                abs(float(values[name]) - expected[name]) > tolerance
                for name in ("out", "flag", "metric")
            )
            if not mismatched:
                continue
            normalization_mismatches += 1
            if _normalized_inputs(values)["valid"] > 0.5:
                function_mismatches += 1

    return (
        f"{note}; {normalization_property_id} "
        f"mismatch_count={normalization_mismatches}; "
        f"{function_property_id} mismatch_count={function_mismatches}"
    )


def append_clocked_property_diagnostics(
    rows: list[dict[str, float]],
    note: str,
    *,
    mode: str,
    edge: int,
    normalization_property_id: str,
    clear_property_id: str,
    tolerance: float = 0.10,
) -> str:
    """Append event-relative property counts for clocked factory checkers."""

    normalization_mismatches = 0
    clear_mismatches = 0
    if rows and CLOCK_REQUIRED.issubset(rows[0]):
        times = [float(row["time"]) for row in rows]
        direction = "rising" if edge > 0 else "falling"
        edges = _threshold_crossings([row["clk"] for row in rows], times, VTH, direction)
        min_period = min((b - a for a, b in zip(edges, edges[1:])), default=1.0e-9)
        delay = min(0.12e-9, 0.12 * min_period)
        core_state = 0.0
        out_state = 0.0
        for edge_t in edges:
            output_t = edge_t + delay
            if output_t >= times[-1] - 0.05e-9:
                continue
            inputs = _values_at(
                rows,
                (
                    "rst",
                    "in0",
                    "in1",
                    "in2",
                    "in3",
                    "ctrl0",
                    "ctrl1",
                    "vdd",
                    "vss",
                    "en",
                ),
                edge_t + 1.0e-12,
            )
            outputs = _values_at(rows, ("out", "flag", "metric"), output_t)
            if inputs is None or outputs is None:
                continue
            values = {
                name: inputs[name]
                for name in ("in0", "in1", "in2", "in3", "ctrl0", "ctrl1", "vdd", "vss", "en")
            }
            state = _normalized_inputs(values)
            x0, x1, x2, c0 = state["x0"], state["x1"], state["x2"], state["c0"]
            clear_sample = inputs["rst"] > VTH or state["valid"] <= 0.5
            if clear_sample:
                core_state = 0.0
                out_state = 0.0
                expected = {"out": 0.0, "flag": 0.0, "metric": 0.0}
            elif mode in {"edge", "sample_fall"}:
                decision = x0 > x1
                expected = {
                    "out": VHI if decision else 0.0,
                    "flag": VHI if decision else 0.0,
                    "metric": VHI * _clip01(abs(x0 - x1)),
                }
            elif mode == "toggle":
                if x0 > 0.50:
                    out_state = 0.0 if out_state > 0.45 else VHI
                expected = {
                    "out": out_state,
                    "flag": out_state,
                    "metric": VHI * _clip01(abs(x0 - x1)),
                }
            elif mode == "counter":
                if x0 > 0.25 and x1 > 0.20:
                    core_state = min(4.0, core_state + 1.0)
                else:
                    core_state = 0.0
                expected = {
                    "out": VHI * _clip01(core_state / 4.0),
                    "flag": VHI if core_state >= 3.0 else 0.0,
                    "metric": VHI * _clip01(abs(x0 - x1)),
                }
            elif mode == "latch":
                if c0 > 0.45:
                    out_state = VHI * _clip01(0.70 * x0 + 0.30 * x1)
                expected = {
                    "out": out_state,
                    "flag": VHI if c0 > 0.45 else 0.0,
                    "metric": VHI * _clip01(abs((out_state / VHI) - x2)),
                }
            else:
                raise ValueError(f"unsupported_clock_mode={mode}")

            mismatched = any(
                abs(float(outputs[name]) - expected[name]) > tolerance
                for name in ("out", "flag", "metric")
            )
            if not mismatched:
                continue
            normalization_mismatches += 1
            if clear_sample:
                clear_mismatches += 1

    return (
        f"{note}; {normalization_property_id} "
        f"mismatch_count={normalization_mismatches}; "
        f"{clear_property_id} mismatch_count={clear_mismatches}"
    )
