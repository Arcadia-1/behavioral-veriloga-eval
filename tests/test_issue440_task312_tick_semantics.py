from __future__ import annotations

import csv
from pathlib import Path
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runners"))

from checkers.v4.task_312 import check_v4_312_interleaved_adc_skew_monitor


R51_SPECTRE_CASES = (
    ROOT.parents[1]
    / "_experiment_runs"
    / "r51-spectre-recert-20260722"
    / "work"
    / "v4-812"
    / "v4-812"
)

NS = 1e-9
VIN_A = [(0.0, 0.70), (10.0, 0.70), (10.1, 0.46), (26.0, 0.46), (26.1, 0.72), (45.0, 0.72)]
VIN_B = [(0.0, 0.40), (12.0, 0.40), (12.1, 0.44), (26.0, 0.44), (26.1, 0.40), (45.0, 0.40)]
CLOCK_EVENTS = sorted(
    [(6.03 + 6.0 * index, "a") for index in range(7)]
    + [(7.33 + 6.0 * index, "b") for index in range(7)]
)


def _load_spectre_rows(case: str) -> list[dict[str, float]]:
    csv_path = R51_SPECTRE_CASES / case / "tran_spectre.csv"
    if not csv_path.is_file():
        pytest.skip("r51 Spectre replay artifacts are not available")
    with csv_path.open(newline="", encoding="utf-8") as handle:
        return [
            {name: float(value) for name, value in row.items()}
            for row in csv.DictReader(handle)
        ]


def _pwl(time_ns: float, points: list[tuple[float, float]]) -> float:
    if time_ns <= points[0][0]:
        return points[0][1]
    for (left_t, left_v), (right_t, right_v) in zip(points, points[1:]):
        if time_ns <= right_t:
            fraction = (time_ns - left_t) / (right_t - left_t)
            return left_v + fraction * (right_v - left_v)
    return points[-1][1]


def _rst(time_ns: float) -> float:
    return 0.9 if time_ns < 2.2 or 24.0 <= time_ns < 26.0 else 0.0


def _enable(time_ns: float) -> float:
    return 0.0 if time_ns < 5.1 or 18.0 <= time_ns < 20.0 else 0.9


def _clock(time_ns: float, delay_ns: float) -> float:
    if time_ns < delay_ns:
        return 0.0
    phase = (time_ns - delay_ns) % 6.0
    if phase < 0.06:
        return 0.9 * phase / 0.06
    if phase < 1.56:
        return 0.9
    if phase < 1.62:
        return 0.9 * (1.0 - (phase - 1.56) / 0.06)
    return 0.0


def _synthetic_rows(step_ns: float, *, alarm_after_one: bool) -> list[dict[str, float]]:
    event_index = 0
    sa = sb = 0.45
    ready_a = ready_b = False
    consecutive = 0
    updates: list[tuple[float, float, float]] = []
    for tick_index in range(91):
        tick_ns = 0.5 * tick_index
        while event_index < len(CLOCK_EVENTS) and CLOCK_EVENTS[event_index][0] <= tick_ns:
            event_ns, channel = CLOCK_EVENTS[event_index]
            if _rst(event_ns) > 0.45 or _enable(event_ns) <= 0.45:
                sa = sb = 0.45
                ready_a = ready_b = False
            elif channel == "a":
                sa = _pwl(event_ns, VIN_A)
                ready_a = True
            else:
                sb = _pwl(event_ns, VIN_B)
                ready_b = True
            event_index += 1
        if _rst(tick_ns) > 0.45 or _enable(tick_ns) <= 0.45 or not (ready_a and ready_b):
            consecutive = 0
            updates.append((0.0, 0.0, 0.0))
            continue
        skew = abs(sa - sb)
        magnitude = 0.5 * (abs(sa - 0.45) + abs(sb - 0.45))
        consecutive = consecutive + 1 if skew > 0.04 else 0
        alarm_threshold = 1 if alarm_after_one else 2
        updates.append((skew, magnitude, 0.9 if consecutive >= alarm_threshold else 0.0))

    def output(time_ns: float, output_index: int) -> float:
        tick_index = min(int((time_ns + 1e-12) / 0.5), len(updates) - 1)
        tick_ns = 0.5 * tick_index
        new_value = updates[tick_index][output_index]
        old_value = updates[tick_index - 1][output_index] if tick_index else 0.0
        fraction = max(0.0, min(1.0, (time_ns - tick_ns) / 0.2))
        return old_value + fraction * (new_value - old_value)

    times_ns = {round(index * step_ns, 12) for index in range(int(45.0 / step_ns) + 1)}
    times_ns.add(45.0)
    for index in range(7):
        for delay_ns in (6.0 + 6.0 * index, 7.3 + 6.0 * index):
            times_ns.update(
                (
                    delay_ns,
                    delay_ns + 0.03,
                    delay_ns + 0.06,
                    delay_ns + 1.56,
                    delay_ns + 1.62,
                )
            )
    times_ns.update((2.2, 5.1, 10.0, 10.1, 12.0, 12.1, 18.0, 20.0, 24.0, 26.0, 26.1))

    return [
        {
            "time": time_ns * NS,
            "vin_a": _pwl(time_ns, VIN_A),
            "vin_b": _pwl(time_ns, VIN_B),
            "clk_a": _clock(time_ns, 6.0),
            "clk_b": _clock(time_ns, 7.3),
            "rst": _rst(time_ns),
            "enable": _enable(time_ns),
            "skew_metric": output(time_ns, 0),
            "magnitude_metric": output(time_ns, 1),
            "alarm": output(time_ns, 2),
        }
        for time_ns in sorted(time_ns for time_ns in times_ns if 0.0 <= time_ns <= 45.0)
    ]


def test_task312_r51_spectre_reference_passes_and_early_alarm_is_killed() -> None:
    reference_ok, reference_note = check_v4_312_interleaved_adc_skew_monitor(
        _load_spectre_rows("correct")
    )
    mutation_ok, mutation_note = check_v4_312_interleaved_adc_skew_monitor(
        _load_spectre_rows("neg_003_alarm_after_one_violation")
    )

    assert reference_ok, reference_note
    assert not mutation_ok, mutation_note
    assert "P_ASSERT_ALARM_WHEN_SKEW_METRIC_EXCEEDS" in mutation_note


@pytest.mark.parametrize("step_ns", [0.02, 0.37])
def test_task312_reference_result_is_independent_of_solver_row_density(step_ns: float) -> None:
    ok, note = check_v4_312_interleaved_adc_skew_monitor(
        _synthetic_rows(step_ns, alarm_after_one=False)
    )

    assert ok, note
    assert "checked=48" in note
    assert "alarm_errors=0" in note


@pytest.mark.parametrize("step_ns", [0.02, 0.37])
def test_task312_rejects_alarm_after_one_tick_on_different_grids(step_ns: float) -> None:
    ok, note = check_v4_312_interleaved_adc_skew_monitor(
        _synthetic_rows(step_ns, alarm_after_one=True)
    )

    assert not ok
    assert "alarm_errors=2" in note
    assert "P_ASSERT_ALARM_WHEN_SKEW_METRIC_EXCEEDS" in note
