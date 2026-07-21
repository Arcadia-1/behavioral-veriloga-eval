from __future__ import annotations

import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
RUNNERS = ROOT / "runners"
if str(RUNNERS) not in sys.path:
    sys.path.insert(0, str(RUNNERS))

from checkers.common.issue109_factory import (  # noqa: E402
    VHI,
    VTH,
    _clip01,
    _normalized_inputs,
)
from checkers.v4.registry import load_checker  # noqa: E402


CHECKER_CASES = [
    ("v4_260_comparator_decision_capture", "edge", 1),
    ("v4_261_falling_edge_calibration_sampler", "sample_fall", -1),
    ("v4_262_resettable_phase_toggle_monitor", "toggle", 1),
    ("v4_263_settling_progress_counter", "counter", 1),
    ("v4_264_enable_qualified_bias_hold", "latch", 1),
    ("v4_267_clocked_power_ready_sampler", "counter", 1),
]


def _inputs(state: dict[str, float]) -> dict[str, float]:
    vss = state.get("vss", 0.02)
    span = state.get("span", 1.02)
    vdd = vss + span
    return {
        "rst": state["rst"],
        "in0": vss + span * state["x0"],
        "in1": vss + span * state["x1"],
        "in2": vss + span * state.get("x2", 0.35),
        "in3": vss + span * state.get("x3", 0.70),
        "ctrl0": VHI * state.get("c0", 0.0),
        "ctrl1": VHI * state.get("c1", 0.0),
        "vdd": vdd,
        "vss": vss,
        "en": state["en"],
    }


def _expected(
    mode: str,
    values: dict[str, float],
    state: dict[str, float],
) -> dict[str, float]:
    normalized = _normalized_inputs(values)
    if values["rst"] > VTH or normalized["valid"] <= 0.5:
        state["core"] = 0.0
        state["out"] = 0.0
        return {"out": 0.0, "flag": 0.0, "metric": 0.0}

    x0, x1, x2, c0 = (
        normalized["x0"],
        normalized["x1"],
        normalized["x2"],
        normalized["c0"],
    )
    if mode in {"edge", "sample_fall"}:
        decision = x0 > x1
        return {
            "out": VHI if decision else 0.0,
            "flag": VHI if decision else 0.0,
            "metric": VHI * _clip01(abs(x0 - x1)),
        }
    if mode == "toggle":
        if x0 > 0.50:
            state["out"] = 0.0 if state["out"] > 0.45 else VHI
        return {
            "out": state["out"],
            "flag": state["out"],
            "metric": VHI * _clip01(abs(x0 - x1)),
        }
    if mode == "counter":
        if x0 > 0.25 and x1 > 0.20:
            state["core"] = min(4.0, state["core"] + 1.0)
        else:
            state["core"] = 0.0
        return {
            "out": VHI * _clip01(state["core"] / 4.0),
            "flag": VHI if state["core"] >= 3.0 else 0.0,
            "metric": VHI * _clip01(abs(x0 - x1)),
        }
    if mode == "latch":
        if c0 > 0.45:
            state["out"] = VHI * _clip01(0.70 * x0 + 0.30 * x1)
        return {
            "out": state["out"],
            "flag": VHI if c0 > 0.45 else 0.0,
            "metric": VHI * _clip01(abs((state["out"] / VHI) - x2)),
        }
    raise AssertionError(f"unsupported mode {mode}")


def _clocked_row(
    time_s: float,
    clk: float,
    values: dict[str, float],
    outputs: dict[str, float],
) -> dict[str, float]:
    return {"time": time_s, "clk": clk, **values, **outputs}


def _state_sequence(*, include_invalid_spans: bool) -> list[dict[str, float]]:
    low_span = 0.42 if include_invalid_spans else 1.02
    high_span = 1.48 if include_invalid_spans else 1.02
    return [
        {"rst": 0.90, "en": 0.90, "x0": 0.20, "x1": 0.80},
        {"rst": 0.00, "en": 0.00, "x0": 0.90, "x1": 0.10},
        {"rst": 0.00, "en": 0.90, "x0": 0.88, "x1": 0.18, "c0": 0.90, "x2": 0.20},
        {"rst": 0.00, "en": 0.90, "x0": 0.22, "x1": 0.78, "c0": 0.10, "x2": 0.80},
        {"rst": 0.00, "en": 0.90, "x0": 0.62, "x1": 0.20, "c0": 0.90, "span": low_span},
        {"rst": 0.00, "en": 0.90, "x0": 0.80, "x1": 0.30, "c0": 0.90, "x2": 0.30},
        {"rst": 0.00, "en": 0.90, "x0": 0.76, "x1": 0.22, "c0": 0.90, "span": high_span},
        {"rst": 0.00, "en": 0.90, "x0": 0.70, "x1": 0.40, "c0": 0.90, "x2": 0.40},
        {"rst": 0.00, "en": 0.90, "x0": 0.82, "x1": 0.32, "c0": 0.90, "x2": 0.55},
        {"rst": 0.00, "en": 0.90, "x0": 0.30, "x1": 0.74, "c0": 0.10, "x2": 0.15},
        {"rst": 0.00, "en": 0.90, "x0": 0.92, "x1": 0.28, "c0": 0.90, "x2": 0.72},
        {"rst": 0.00, "en": 0.90, "x0": 0.84, "x1": 0.26, "c0": 0.90, "x2": 0.22},
    ]


def _async_recovery_sequence(mode: str) -> list[dict[str, float]]:
    common_prefix = [
        {"rst": 0.90, "en": 0.90, "x0": 0.20, "x1": 0.80},
        {"rst": 0.00, "en": 0.00, "x0": 0.90, "x1": 0.10},
        {"rst": 0.00, "en": 0.90, "x0": 0.62, "x1": 0.20, "c0": 0.90, "span": 0.42},
        {"rst": 0.00, "en": 0.90, "x0": 0.76, "x1": 0.22, "c0": 0.90, "span": 1.48},
    ]
    if mode in {"edge", "sample_fall"}:
        tail = [
            {"rst": 0.00, "en": 0.90, "x0": 0.86, "x1": 0.16, "c0": 0.90, "x2": 0.20},
            {"rst": 0.00, "en": 0.90, "x0": 0.18, "x1": 0.78, "c0": 0.10, "x2": 0.80},
            {"rst": 0.00, "en": 0.90, "x0": 0.82, "x1": 0.30, "c0": 0.90, "x2": 0.35},
            {"rst": 0.00, "en": 0.90, "x0": 0.24, "x1": 0.72, "c0": 0.10, "x2": 0.65},
            {"rst": 0.00, "en": 0.90, "x0": 0.90, "x1": 0.28, "c0": 0.90, "x2": 0.15},
            {"rst": 0.00, "en": 0.90, "x0": 0.34, "x1": 0.80, "c0": 0.10, "x2": 0.85},
        ]
    elif mode == "toggle":
        tail = [
            {"rst": 0.00, "en": 0.90, "x0": 0.86, "x1": 0.16, "c0": 0.90, "x2": 0.20},
            {"rst": 0.00, "en": 0.90, "x0": 0.22, "x1": 0.78, "c0": 0.10, "x2": 0.80},
            {"rst": 0.00, "en": 0.90, "x0": 0.84, "x1": 0.26, "c0": 0.90, "x2": 0.35},
            {"rst": 0.00, "en": 0.90, "x0": 0.88, "x1": 0.34, "c0": 0.90, "x2": 0.65},
            {"rst": 0.00, "en": 0.90, "x0": 0.20, "x1": 0.74, "c0": 0.10, "x2": 0.15},
            {"rst": 0.00, "en": 0.90, "x0": 0.92, "x1": 0.28, "c0": 0.90, "x2": 0.85},
        ]
    elif mode == "counter":
        tail = [
            {"rst": 0.00, "en": 0.90, "x0": 0.86, "x1": 0.46, "c0": 0.90, "x2": 0.20},
            {"rst": 0.00, "en": 0.90, "x0": 0.78, "x1": 0.36, "c0": 0.10, "x2": 0.80},
            {"rst": 0.00, "en": 0.90, "x0": 0.82, "x1": 0.42, "c0": 0.90, "x2": 0.35},
            {"rst": 0.00, "en": 0.90, "x0": 0.80, "x1": 0.40, "c0": 0.90, "x2": 0.65},
            {"rst": 0.00, "en": 0.90, "x0": 0.76, "x1": 0.34, "c0": 0.10, "x2": 0.15},
            {"rst": 0.00, "en": 0.90, "x0": 0.92, "x1": 0.28, "c0": 0.90, "x2": 0.85},
        ]
    elif mode == "latch":
        tail = [
            {"rst": 0.00, "en": 0.90, "x0": 0.86, "x1": 0.16, "c0": 0.90, "x2": 0.20},
            {"rst": 0.00, "en": 0.90, "x0": 0.22, "x1": 0.78, "c0": 0.10, "x2": 0.80},
            {"rst": 0.00, "en": 0.90, "x0": 0.84, "x1": 0.26, "c0": 0.90, "x2": 0.35},
            {"rst": 0.00, "en": 0.90, "x0": 0.20, "x1": 0.74, "c0": 0.10, "x2": 0.65},
            {"rst": 0.00, "en": 0.90, "x0": 0.90, "x1": 0.28, "c0": 0.90, "x2": 0.15},
            {"rst": 0.00, "en": 0.90, "x0": 0.34, "x1": 0.80, "c0": 0.10, "x2": 0.85},
        ]
    else:
        raise AssertionError(f"unsupported mode {mode}")
    return common_prefix + tail


def _clocked_rows(
    mode: str,
    edge: int,
    *,
    include_invalid_spans: bool = True,
    corrupt_async_clear: bool = False,
) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    state = {"core": 0.0, "out": 0.0}
    previous = {"out": 0.0, "flag": 0.0, "metric": 0.0}
    start_s = 21.0e-9
    period_s = 4.0e-9
    high_before_edge = edge < 0

    for index, item in enumerate(_state_sequence(include_invalid_spans=include_invalid_spans)):
        edge_s = start_s + index * period_s
        values = _inputs(item)
        expected = _expected(mode, values, state)
        pre_clk = VHI if high_before_edge else 0.0
        post_clk = 0.0 if high_before_edge else VHI
        idle_clk = 0.0
        rows.extend(
            [
                _clocked_row(edge_s - 10.0e-12, pre_clk, values, previous),
                _clocked_row(edge_s, post_clk, values, previous),
                _clocked_row(edge_s + 1.0e-12, post_clk, values, previous),
                _clocked_row(edge_s + 0.12e-9, post_clk, values, expected),
                _clocked_row(edge_s + 0.45 * period_s, post_clk, values, expected),
                _clocked_row(edge_s + 0.55 * period_s, idle_clk, values, expected),
            ]
        )
        previous = expected

        if corrupt_async_clear and index == 5:
            reset_values = {**values, "rst": VHI}
            reset_t = edge_s + 0.68 * period_s
            rows.extend(
                [
                    _clocked_row(reset_t - 10.0e-12, idle_clk, {**values, "rst": 0.0}, previous),
                    _clocked_row(reset_t, idle_clk, reset_values, previous),
                    _clocked_row(reset_t + 1.0e-12, idle_clk, reset_values, previous),
                    _clocked_row(reset_t + 0.12e-9, idle_clk, reset_values, previous),
                    _clocked_row(reset_t + 0.36e-9, idle_clk, {**values, "rst": 0.0}, previous),
                ]
            )

    return sorted(rows, key=lambda row: row["time"])


def _async_recovery_rows(mode: str, edge: int) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    state = {"core": 0.0, "out": 0.0}
    previous = {"out": 0.0, "flag": 0.0, "metric": 0.0}
    start_s = 101.0e-9
    period_s = 4.0e-9
    high_before_edge = edge < 0

    for index, item in enumerate(_async_recovery_sequence(mode)):
        edge_s = start_s + index * period_s
        values = _inputs(item)
        expected = _expected(mode, values, state)
        pre_clk = VHI if high_before_edge else 0.0
        post_clk = 0.0 if high_before_edge else VHI
        idle_clk = 0.0
        rows.extend(
            [
                _clocked_row(edge_s - 10.0e-12, pre_clk, values, previous),
                _clocked_row(edge_s, post_clk, values, previous),
                _clocked_row(edge_s + 1.0e-12, post_clk, values, previous),
                _clocked_row(edge_s + 0.12e-9, post_clk, values, expected),
                _clocked_row(edge_s + 0.45 * period_s, post_clk, values, expected),
                _clocked_row(edge_s + 0.55 * period_s, idle_clk, values, expected),
            ]
        )
        previous = expected

        if index == 5:
            reset_t = edge_s + 0.68 * period_s
            reset_values = {**values, "rst": VHI}
            cleared = {"out": 0.0, "flag": 0.0, "metric": 0.0}
            rows.extend(
                [
                    _clocked_row(reset_t - 10.0e-12, idle_clk, {**values, "rst": 0.0}, previous),
                    _clocked_row(reset_t, idle_clk, reset_values, previous),
                    _clocked_row(reset_t + 1.0e-12, idle_clk, reset_values, previous),
                    _clocked_row(reset_t + 0.12e-9, idle_clk, reset_values, cleared),
                    _clocked_row(reset_t + 0.36e-9, idle_clk, {**values, "rst": 0.0}, cleared),
                ]
            )
            state["core"] = 0.0
            state["out"] = 0.0
            previous = cleared

    return sorted(rows, key=lambda row: row["time"])


@pytest.mark.parametrize(("checker_id", "mode", "edge"), CHECKER_CASES)
def test_issue440_260_267_accepts_span_and_async_reset_covered_trace(
    checker_id: str,
    mode: str,
    edge: int,
) -> None:
    checker = load_checker(checker_id)
    assert checker is not None

    passed, note = checker(_clocked_rows(mode, edge))

    assert passed, note


@pytest.mark.parametrize(("checker_id", "mode", "edge"), CHECKER_CASES)
def test_issue440_260_267_accepts_async_reset_recovery_from_cleared_state(
    checker_id: str,
    mode: str,
    edge: int,
) -> None:
    checker = load_checker(checker_id)
    assert checker is not None

    passed, note = checker(_async_recovery_rows(mode, edge))

    assert passed, note


@pytest.mark.parametrize(("checker_id", "mode", "edge"), CHECKER_CASES)
def test_issue440_260_267_rejects_missing_invalid_span_coverage(
    checker_id: str,
    mode: str,
    edge: int,
) -> None:
    checker = load_checker(checker_id)
    assert checker is not None

    passed, note = checker(_clocked_rows(mode, edge, include_invalid_spans=False))

    assert not passed
    if checker_id == "v4_260_comparator_decision_capture":
        assert "missing_invalid_span_coverage" in note


@pytest.mark.parametrize(("checker_id", "mode", "edge"), CHECKER_CASES)
def test_issue440_260_267_rejects_async_reset_without_immediate_clear(
    checker_id: str,
    mode: str,
    edge: int,
) -> None:
    checker = load_checker(checker_id)
    assert checker is not None

    passed, note = checker(_clocked_rows(mode, edge, corrupt_async_clear=True))

    assert not passed
    if checker_id == "v4_260_comparator_decision_capture":
        assert "max_error" in note
