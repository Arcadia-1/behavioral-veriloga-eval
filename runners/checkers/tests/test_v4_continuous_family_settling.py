from __future__ import annotations

from collections.abc import Callable

import pytest

from runners.checkers.common.issue109_split import check_continuous, cont_expected
from runners.checkers.v4.task_278 import check_v4_278_lane_mask_replication_driver
from runners.checkers.v4.task_280 import check_v4_280_ready_reduction_fault_monitor
from runners.checkers.v4.task_286 import check_v4_286_explicit_replicated_stage_chain


VHI = 0.9


def _reduction_inputs(count: int) -> tuple[float, float, float, float]:
    return tuple(0.72 if idx < count else 0.18 for idx in range(4))


def _sum_inputs(kind: str) -> tuple[float, float, float, float]:
    if kind == "low":
        return (0.20, 0.10, 0.10, 0.10)
    if kind == "mid":
        return (0.55, 0.30, 0.35, 0.20)
    return (0.90, 0.10, 0.80, 0.70)


def _base_row(
    time_s: float,
    inputs: tuple[float, float, float, float],
    *,
    ctrl0: float = 0.2,
    en: float = VHI,
) -> dict[str, float]:
    return {
        "time": time_s,
        "in0": inputs[0],
        "in1": inputs[1],
        "in2": inputs[2],
        "in3": inputs[3],
        "ctrl0": ctrl0,
        "ctrl1": 0.2,
        "vdd": 1.0,
        "vss": 0.0,
        "en": en,
        "out": 0.0,
        "flag": 0.0,
        "metric": 0.0,
    }


def _fill_expected(row: dict[str, float], mode: str) -> None:
    expected = cont_expected(mode, row)
    row["out"] = expected["out"]
    row["flag"] = expected["flag"]
    row["metric"] = expected["metric"]


def _continuous_rows(mode: str, *, transition_tail: bool = False, wrong_after_settle: bool = False) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for idx in range(81):
        time_s = 12.0e-9 * idx / 80.0
        ctrl0 = 0.2 if idx < 27 else 0.8
        if idx < 10:
            row = _base_row(
                time_s,
                _reduction_inputs(0) if mode == "reduction" else _sum_inputs("low"),
                ctrl0=ctrl0,
                en=0.0,
            )
        elif mode == "reduction":
            count = 1 if idx < 20 else 3 if idx < 45 else 4
            row = _base_row(time_s, _reduction_inputs(count), ctrl0=ctrl0)
        else:
            kind = "low" if idx < 20 else "high" if idx < 45 else "low"
            row = _base_row(time_s, _sum_inputs(kind), ctrl0=ctrl0)
        _fill_expected(row, mode)
        if transition_tail and idx == 27:
            row["out"] = min(VHI, row["out"] + 0.13)
            row["metric"] = max(0.0, row["metric"] - 0.13)
            pre_sample = dict(row)
            pre_sample["time"] = time_s - 1e-12
            rows.append(pre_sample)
        if wrong_after_settle and idx >= 28:
            row["out"] = 0.0
            row["flag"] = 0.0
            row["metric"] = 0.0
        rows.append(row)
    return rows


@pytest.mark.parametrize(
    ("mode", "checker"),
    [
        ("reduction", check_v4_278_lane_mask_replication_driver),
        ("reduction", check_v4_280_ready_reduction_fault_monitor),
        ("sum", check_v4_286_explicit_replicated_stage_chain),
    ],
)
def test_continuous_family_allows_public_tr_transition_tail(
    mode: str,
    checker: Callable[[list[dict[str, float]]], tuple[bool, str]],
) -> None:
    rows = _continuous_rows(mode, transition_tail=True)

    unguarded_ok, unguarded_note = check_continuous(rows, mode, "unguarded")
    guarded_ok, guarded_note = checker(rows)

    assert not unguarded_ok, unguarded_note
    assert guarded_ok, guarded_note


@pytest.mark.parametrize(
    ("mode", "checker"),
    [
        ("reduction", check_v4_278_lane_mask_replication_driver),
        ("reduction", check_v4_280_ready_reduction_fault_monitor),
        ("sum", check_v4_286_explicit_replicated_stage_chain),
    ],
)
def test_continuous_family_still_rejects_wrong_settled_output(
    mode: str,
    checker: Callable[[list[dict[str, float]]], tuple[bool, str]],
) -> None:
    ok, note = checker(_continuous_rows(mode, transition_tail=True, wrong_after_settle=True))

    assert not ok, note
