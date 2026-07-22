from __future__ import annotations

import copy

import pytest

from runners.checkers.v4.registry import load_checker


VDD = 0.9
DT = 0.1e-9


def _clock(time: float, rise: float, period: float) -> float:
    phase = (time - rise) % period
    return VDD if time >= rise and phase < period / 2.0 else 0.0


def _rows_375() -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    edge_times = [2e-9 + 4e-9 * index for index in range(18)]
    for index in range(701):
        time = index * DT
        rst = VDD if time < 3e-9 else 0.0
        enable = VDD if 5e-9 <= time < 45e-9 or 53e-9 <= time else 0.0
        active_edges = [edge for edge in edge_times if edge <= time and enable > 0.45]
        segment_start = 5e-9 if time < 45e-9 else 53e-9
        segment_edges = [edge for edge in active_edges if edge >= segment_start]
        last_edge = segment_edges[-1] if segment_edges else None
        handoff_done = last_edge is not None and time >= last_edge + 1e-9
        phase_one = int(round((last_edge - 2e-9) / 4e-9)) % 2 == 0 if last_edge is not None else False
        rows.append(
            {
                "time": time,
                "clk_in": _clock(time, 2e-9, 8e-9),
                "rst": rst,
                "enable": enable,
                "phi1": VDD if enable > 0.45 and handoff_done and phase_one else 0.0,
                "phi2": VDD if enable > 0.45 and handoff_done and not phase_one else 0.0,
                "deadtime_metric": VDD if enable > 0.45 and last_edge is not None and not handoff_done else 0.0,
                "valid": VDD if enable > 0.45 and any(time >= edge + 1e-9 for edge in segment_edges) else 0.0,
            }
        )
    return rows


def _rows_376() -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    ramp = 0.0
    pwm = 0.0
    cycle = 0.0
    duty = 0.0
    previous_clk = 0.0
    for index in range(1201):
        time = index * DT
        clk = _clock(time, 1e-9, 5e-9)
        rst = VDD if time < 2e-9 else 0.0
        enable = VDD if 3e-9 <= time < 50e-9 or time >= 60e-9 else 0.0
        vctrl = 0.28 if int(time / 20e-9) % 2 == 0 else 0.76
        if previous_clk <= 0.45 < clk:
            if rst > 0.45 or enable <= 0.45:
                ramp = pwm = cycle = duty = 0.0
            else:
                cycle = 0.0
                if ramp >= 0.9 - 0.15 / 2.0:
                    ramp = 0.0
                    cycle = VDD
                else:
                    ramp += 0.15
                pwm = VDD if vctrl > ramp else 0.0
                duty = max(0.0, min(VDD, vctrl))
        inactive = rst > 0.45 or enable <= 0.45
        rows.append(
            {
                "time": time,
                "clk": clk,
                "rst": rst,
                "enable": enable,
                "vctrl": vctrl,
                "ramp_out": 0.0 if inactive else ramp,
                "pwm_out": 0.0 if inactive else pwm,
                "cycle_start": 0.0 if inactive else cycle,
                "duty_metric": 0.0 if inactive else duty,
            }
        )
        previous_clk = clk
    return rows


def _rows_382() -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    count = 0
    out_state = 0
    valid = False
    metric = 0.0
    previous_clk = 0.0
    for index in range(1201):
        time = index * DT
        clk = _clock(time, 1e-9, 3.5e-9)
        rst = VDD if time < 2e-9 else 0.0
        enable = VDD if 3e-9 <= time < 50e-9 or time >= 60e-9 else 0.0
        code = (1, 2, 4, 3)[int(time / 24e-9) % 4]
        if previous_clk <= 0.45 < clk:
            if rst > 0.45 or enable <= 0.45:
                count = 0
                out_state = 0
                valid = False
                metric = 0.0
            else:
                divisor = code + 1
                metric = VDD * divisor / 16.0
                if count >= divisor - 1:
                    count = 0
                    out_state = 1 - out_state
                    valid = True
                else:
                    count += 1
        inactive = rst > 0.45 or enable <= 0.45
        rows.append(
            {
                "time": time,
                "clk_in": clk,
                "rst": rst,
                "enable": enable,
                "n_0": VDD if code & 1 else 0.0,
                "n_1": VDD if code & 2 else 0.0,
                "n_2": VDD if code & 4 else 0.0,
                "n_3": VDD if code & 8 else 0.0,
                "clk_div": 0.0 if inactive else VDD * out_state,
                "ratio_metric": 0.0 if inactive else metric,
                "valid": 0.0 if inactive else VDD * valid,
            }
        )
        previous_clk = clk
    return rows


@pytest.mark.parametrize(
    ("checker_id", "rows_factory"),
    (
        ("v4_375_nonoverlap_clock_generator", _rows_375),
        ("v4_376_pwm_ramp_modulator_front_end", _rows_376),
        ("v4_382_programmable_frequency_divider", _rows_382),
    ),
)
def test_issue440_375_382_accepts_legal_clear_traces(checker_id: str, rows_factory) -> None:
    checker = load_checker(checker_id)
    assert checker is not None
    passed, detail = checker(rows_factory())
    assert passed, detail


@pytest.mark.parametrize(
    ("start", "stop", "updates"),
    (
        (1.0e-9, 2.0e-9, {"phi1": VDD, "deadtime_metric": VDD, "valid": VDD}),
        (47.0e-9, 48.0e-9, {"deadtime_metric": VDD}),
        (20.0e-9, 22.0e-9, {"valid": 0.0}),
    ),
)
def test_issue440_375_rejects_clear_or_valid_retention_violation(
    start: float,
    stop: float,
    updates: dict[str, float],
) -> None:
    checker = load_checker("v4_375_nonoverlap_clock_generator")
    assert checker is not None
    rows = copy.deepcopy(_rows_375())
    for row in rows:
        if start <= row["time"] <= stop:
            row.update(updates)
    passed, detail = checker(rows)
    assert not passed, detail


@pytest.mark.parametrize(
    ("checker_id", "rows_factory", "start", "stop", "outputs"),
    (
        (
            "v4_376_pwm_ramp_modulator_front_end",
            _rows_376,
            53.0e-9,
            54.0e-9,
            ("ramp_out", "pwm_out", "cycle_start", "duty_metric"),
        ),
        (
            "v4_382_programmable_frequency_divider",
            _rows_382,
            52.0e-9,
            52.8e-9,
            ("clk_div", "ratio_metric", "valid"),
        ),
    ),
)
def test_issue440_376_382_reject_between_edge_clear_violation(
    checker_id: str,
    rows_factory,
    start: float,
    stop: float,
    outputs: tuple[str, ...],
) -> None:
    checker = load_checker(checker_id)
    assert checker is not None
    rows = copy.deepcopy(rows_factory())
    for row in rows:
        if start <= row["time"] <= stop:
            row.update({output: VDD for output in outputs})
    passed, detail = checker(rows)
    assert not passed, detail
