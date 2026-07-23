from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runners"))

from checkers.v4.task_091 import CHECKER as CHECKER_091
from checkers.v4.task_220 import CHECKER as CHECKER_220


VDD_091 = 0.9
VTH_091 = 0.45


def _pwl(time_ns: float, points: list[tuple[float, float]]) -> float:
    for (left_time, left_value), (right_time, right_value) in zip(points, points[1:]):
        if left_time <= time_ns <= right_time:
            if right_time == left_time:
                return right_value
            fraction = (time_ns - left_time) / (right_time - left_time)
            return left_value + fraction * (right_value - left_value)
    return points[-1][1]


def _chop_value(time_ns: float) -> float:
    if time_ns < 2.0:
        return 0.0
    phase_ns = (time_ns - 2.0) % 2.0
    if phase_ns <= 0.05:
        return 0.9 * phase_ns / 0.05
    if phase_ns <= 0.95:
        return 0.9
    if phase_ns <= 1.0:
        return 0.9 * (1.0 - (phase_ns - 0.95) / 0.05)
    return 0.0


def _rows_091(
    *,
    core_gain: float = 3.0,
    offset: float = 0.020,
    alpha: float = 0.25,
    ignore_hold: bool = False,
    update_on_chop: bool = True,
) -> list[dict[str, float]]:
    vinp_points = [
        (0.0, 0.47), (24.0, 0.47), (24.1, 0.435),
        (42.0, 0.435), (42.1, 0.46), (70.0, 0.46),
    ]
    vinn_points = [
        (0.0, 0.43), (24.0, 0.43), (24.1, 0.465),
        (42.0, 0.465), (42.1, 0.44), (70.0, 0.44),
    ]
    rst_points = [(0.0, 0.9), (1.5, 0.9), (1.6, 0.0), (70.0, 0.0)]
    enable_points = [
        (0.0, 0.0), (3.0, 0.0), (3.1, 0.9),
        (55.0, 0.9), (55.1, 0.0), (58.0, 0.0),
        (58.1, 0.9), (70.0, 0.9),
    ]
    hold_points = [
        (0.0, 0.0), (18.0, 0.0), (18.1, 0.9),
        (22.0, 0.9), (22.1, 0.0), (48.0, 0.0),
        (48.1, 0.9), (52.0, 0.9), (52.1, 0.0), (70.0, 0.0),
    ]

    events: list[tuple[float, str, int]] = [(55.05, "clear", 0)]
    for base_ns in range(2, 70, 2):
        events.append((base_ns + 0.025, "chop", +1))
        events.append((base_ns + 0.975, "chop", -1))
    events.sort()

    baseband = residual = 0.0
    settled = 0.0
    converged = 0
    event_index = 0
    rows: list[dict[str, float]] = []
    for step in range(1401):
        time_ns = 0.05 * step
        while event_index < len(events) and events[event_index][0] <= time_ns + 1.0e-12:
            event_time_ns, kind, polarity = events[event_index]
            rst = _pwl(event_time_ns, rst_points)
            enable = _pwl(event_time_ns, enable_points)
            hold = _pwl(event_time_ns, hold_points)
            if kind == "clear" or rst > VTH_091 or enable <= VTH_091:
                baseband = residual = 0.0
                settled = 0.0
                converged = 0
            elif (hold <= VTH_091 or ignore_hold) and update_on_chop:
                input_diff = _pwl(event_time_ns, vinp_points) - _pwl(event_time_ns, vinn_points)
                demodulated = core_gain * (input_diff + polarity * offset)
                baseband += alpha * (demodulated - baseband)
                residual = baseband - 3.0 * input_diff
                converged = converged + 1 if abs(residual) <= 0.020 else 0
                settled = VDD_091 if converged >= 3 else 0.0
            event_index += 1

        rows.append({
            "time": time_ns * 1.0e-9,
            "vinp": _pwl(time_ns, vinp_points),
            "vinn": _pwl(time_ns, vinn_points),
            "chop_clk": _chop_value(time_ns),
            "rst": _pwl(time_ns, rst_points),
            "enable": _pwl(time_ns, enable_points),
            "hold": _pwl(time_ns, hold_points),
            "voutp": min(0.9, max(0.0, 0.45 + 0.5 * baseband)),
            "voutn": min(0.9, max(0.0, 0.45 - 0.5 * baseband)),
            "settled": settled,
            "offset_residual": residual,
        })
    return rows


def test_task091_samples_state_inputs_at_reconstructed_chop_event() -> None:
    passed, detail = CHECKER_091(_rows_091())
    assert passed, detail


def test_task091_event_time_replay_preserves_negative_discrimination() -> None:
    negative_rows = {
        "no_synchronous_demod": _rows_091(update_on_chop=False),
        "offset_omitted": _rows_091(offset=0.0),
        "lowpass_bypassed": _rows_091(alpha=1.0),
        "gain_wrong": _rows_091(core_gain=1.5),
        "hold_ignored": _rows_091(ignore_hold=True),
    }
    for name, rows in negative_rows.items():
        passed, detail = CHECKER_091(rows)
        assert not passed, f"{name} unexpectedly passed: {detail}"


def _rows_220() -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    state = 0
    previous_ref = previous_fb = 0.0
    for step in range(57):
        time_ns = 0.05 * step
        ref = 1.2 if 1.15 <= time_ns < 1.35 or 2.05 <= time_ns < 2.25 else 0.0
        fb = 1.2 if 0.45 <= time_ns < 0.65 or 2.40 <= time_ns < 2.60 else 0.0
        if previous_ref <= 0.6 < ref:
            state = min(1, state + 1)
        if previous_fb <= 0.6 < fb:
            state = max(-1, state - 1)
        previous_ref = ref
        previous_fb = fb
        rows.append({
            "time": time_ns * 1.0e-9,
            "ref": ref,
            "fb": fb,
            "up": 1.2 if state == 1 else 0.0,
            "down": 1.2 if state == -1 else 0.0,
        })
    return rows


def test_task220_falling_edges_do_not_erase_rising_edge_state_coverage() -> None:
    passed, detail = CHECKER_220(_rows_220())
    assert passed, detail


def test_task220_rising_only_guard_preserves_negative_discrimination() -> None:
    gold = _rows_220()
    negative_rows: dict[str, list[dict[str, float]]] = {}

    negative_rows["zero"] = [{**row, "up": 0.0, "down": 0.0} for row in gold]
    negative_rows["swapped_ref_fb"] = [
        {**row, "up": row["down"], "down": row["up"]} for row in gold
    ]
    negative_rows["no_fb_decrement"] = [{**row, "down": 0.0} for row in gold]
    negative_rows["up_stuck_for_zero_state"] = [
        {**row, "up": 1.2 if row["up"] == 0.0 and row["down"] == 0.0 else row["up"]}
        for row in gold
    ]
    negative_rows["metric_scale_low"] = [
        {**row, "up": 0.42 * row["up"], "down": 0.42 * row["down"]}
        for row in gold
    ]

    for name, rows in negative_rows.items():
        passed, detail = CHECKER_220(rows)
        assert not passed, f"{name} unexpectedly passed: {detail}"
