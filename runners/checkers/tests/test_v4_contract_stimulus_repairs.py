from __future__ import annotations

from runners.checkers.v4.task_026 import CHECKER as CHECK_PHASE_ACCUMULATOR
from runners.checkers.v4.task_169 import CHECKER as CHECK_LINEAR_PFD_GAIN
from runners.checkers.v4.task_305 import CHECKER as CHECK_CAP_FEEDBACK


def _cap_feedback_rows(
    *,
    corrupt_active_hold: bool = False,
    analog_clear_transition: bool = False,
) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    edge_times_ns = [1.0 + 2.0 * index for index in range(12)]
    target = 0.45
    sample_value = 0.0
    settled_streak = 0
    settled = 0.0
    for sample_index in range(260):
        time_ns = 0.1 * sample_index
        clk = 0.9 if any(edge <= time_ns < edge + 0.4 for edge in edge_times_ns) else 0.0
        rst = 0.9 if time_ns < 1.5 or 4.2 <= time_ns < 4.7 else 0.0
        enable = 0.0 if 9.2 <= time_ns < 9.7 else 0.9
        edge_count = sum(edge <= time_ns for edge in edge_times_ns)
        event_edge_count = sum(edge < time_ns for edge in edge_times_ns)
        code = (edge_count // 3) % 4
        event_code = (event_edge_count // 3) % 4
        vin = 0.36
        edge_hit = any(abs(time_ns - edge) < 1e-12 for edge in edge_times_ns)
        if edge_hit:
            if enable > 0.45 and rst <= 0.45:
                sample_value = vin
                gain = 1.0 + 0.75 * event_code
                next_target = min(1.0, max(0.0, 0.45 + gain * (sample_value - 0.45)))
                settled_streak = settled_streak + 1 if abs(next_target - target) < 10e-3 else 0
                target = next_target
                settled = 0.9 if settled_streak >= 2 else 0.0
            else:
                sample_value = 0.0
                target = 0.45
                settled_streak = 0
                settled = 0.0
        if rst > 0.45 or enable <= 0.45:
            sample_value = 0.0
            target = 0.45
            settled_streak = 0
            settled = 0.0
        if rst > 0.45 or enable <= 0.45:
            observed_sample = 0.0
            observed_target = 0.45
            observed_settled = 0.0
        else:
            observed_sample = sample_value
            observed_target = target
            observed_settled = settled
        if analog_clear_transition:
            since_clear = min(
                (
                    time_ns - start
                    for start in (4.2, 9.2)
                    if start <= time_ns < start + 0.3
                ),
                default=None,
            )
            if since_clear is not None:
                fraction = since_clear / 0.3
                observed_sample = 0.36 * (1.0 - fraction)
                observed_target = target + 0.20 * (1.0 - fraction)
        if corrupt_active_hold and 13.4 <= time_ns <= 14.4 and rst <= 0.45 and enable > 0.45:
            observed_target = min(1.0, observed_target + 0.25)
        rows.append(
            {
                "time": time_ns * 1e-9,
                "clk": clk,
                "rst": rst,
                "enable": enable,
                "gain_0": 0.9 if code & 1 else 0.0,
                "gain_1": 0.9 if code & 2 else 0.0,
                "vin": vin,
                "vout": observed_target,
                "sampled_metric": observed_sample,
                "settled": observed_settled,
            }
        )
    return rows


def test_task305_allows_reset_or_disable_to_clear_mid_hold_window() -> None:
    passed, note = CHECK_CAP_FEEDBACK(_cap_feedback_rows())
    assert passed, note


def test_task305_allows_analog_clear_transition_before_settle_guard() -> None:
    passed, note = CHECK_CAP_FEEDBACK(_cap_feedback_rows(analog_clear_transition=True))
    assert passed, note


def test_task305_still_rejects_active_window_hold_errors() -> None:
    passed, note = CHECK_CAP_FEEDBACK(_cap_feedback_rows(corrupt_active_hold=True))
    assert not passed, note
    assert "hold_errors=" in note


def _phase_accumulator_rows(
    *,
    supply_transient: bool = True,
    wrong_step: bool = False,
    no_wrap: bool = False,
    wrong_period: bool = False,
) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    step = 0.16 if wrong_step else 0.22
    cadence_ns = 8.0 if wrong_period else 5.0
    phase = 0.0
    event_index = 0
    for sample_index in range(760):
        time_ns = 0.1 * sample_index
        while time_ns >= (event_index + 1) * cadence_ns - 1e-12:
            phase = min(0.99, phase + step) if no_wrap else (phase + step) % 1.0
            event_index += 1
        vdd = 1.0
        if supply_transient and 12.0 <= time_ns <= 13.0:
            vdd = 1.0 + 0.2 * (1.0 - abs(time_ns - 12.5) / 0.5)
        clk = vdd if phase < 0.5 else 0.0
        phase_out = phase if supply_transient and 12.0 <= time_ns <= 13.0 else phase * vdd
        rows.append(
            {
                "time": time_ns * 1e-9,
                "VDD": vdd,
                "VSS": 0.0,
                "phase_out": phase_out,
                "clk_out": clk,
            }
        )
    return rows


def test_task026_ignores_supply_scaling_transients_between_timer_ticks() -> None:
    passed, note = CHECK_PHASE_ACCUMULATOR(_phase_accumulator_rows())
    assert passed, note


def test_task026_still_rejects_wrong_step_and_period() -> None:
    passed, note = CHECK_PHASE_ACCUMULATOR(_phase_accumulator_rows(wrong_step=True))
    assert not passed, note
    assert "P_PARAMETERIZED_PERIOD" in note

    passed, note = CHECK_PHASE_ACCUMULATOR(_phase_accumulator_rows(no_wrap=True))
    assert not passed, note
    assert "P_MODULO_WRAP" in note

    passed, note = CHECK_PHASE_ACCUMULATOR(_phase_accumulator_rows(wrong_period=True))
    assert not passed, note
    assert "P_PARAMETERIZED_PERIOD" in note


def _linear_pfd_rows(*, negative_window: bool = True) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for sample_index in range(80):
        time_ns = 0.1 * sample_index
        if time_ns < 2.0:
            in1, in2 = 0.70, 0.10
        elif time_ns < 4.0:
            in1, in2 = 0.10, 0.10
        elif negative_window:
            in1, in2 = 0.10, 0.70
        else:
            in1, in2 = 0.70, 0.10
        rows.append(
            {
                "time": time_ns * 1e-9,
                "in1": in1,
                "in2": in2,
                "out": 2.03 * (in1 - in2),
            }
        )
    return rows


def test_task169_requires_explicit_positive_and_negative_physical_windows() -> None:
    passed, note = CHECK_LINEAR_PFD_GAIN(_linear_pfd_rows(negative_window=False))
    assert not passed, note
    assert "positive_and_negative" in note

    passed, note = CHECK_LINEAR_PFD_GAIN(_linear_pfd_rows())
    assert passed, note
