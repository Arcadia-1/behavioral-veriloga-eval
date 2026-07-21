from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNERS = ROOT / "runners"
if str(RUNNERS) not in sys.path:
    sys.path.insert(0, str(RUNNERS))


def _times(stop_ns: float = 40.0, step_ns: float = 0.25) -> list[float]:
    return [index * step_ns for index in range(round(stop_ns / step_ns) + 1)]


def _pulse(time_ns: float, edges_ns: tuple[float, ...], high: float) -> float:
    return high if any(edge <= time_ns < edge + 0.5 for edge in edges_ns) else 0.0


def _state_at(time_ns: float, changes: tuple[tuple[float, tuple[int, ...]], ...]) -> tuple[int, ...]:
    state = changes[0][1]
    for change_ns, next_state in changes:
        if time_ns >= change_ns:
            state = next_state
    return state


def _latched_state(
    time_ns: float,
    edges_ns: tuple[float, ...],
    changes: tuple[tuple[float, tuple[int, ...]], ...],
    *,
    delay_ns: float,
) -> tuple[int, ...]:
    sampled = changes[0][1]
    for edge_ns in edges_ns:
        if time_ns >= edge_ns + delay_ns:
            sampled = _state_at(edge_ns, changes)
    return sampled


def _trace_153(
    *,
    tamper_input: bool = False,
    ignore_din3: bool = False,
    continuous_tracking: bool = False,
) -> list[dict[str, float]]:
    edges = (2.0, 12.0, 22.0, 32.0)
    changes = (
        (0.0, (0, 0, 0, 0, 0, 0)),
        (10.0, (1, 0, 1, 0, 1, 0)),
        (20.0, (0, 1, 1, 0, 0, 1)),
        (30.0, (0, 0, 0, 1, 0, 0)),
    )
    rows: list[dict[str, float]] = []
    for time_ns in _times():
        inputs = list(_state_at(time_ns, changes))
        sampled = list(
            inputs
            if continuous_tracking
            else _latched_state(time_ns, edges, changes, delay_ns=1.1)
        )
        if ignore_din3:
            sampled[3] = 0
        if tamper_input and time_ns >= 20.0:
            inputs[0] = 1 - inputs[0]
        yp = 0.75 / 64.0
        yn = 0.75 / 64.0
        for bit, value in enumerate(sampled):
            weight = 2.0 ** -(bit + 1)
            yp += weight * (0.925 if value else 0.575)
            yn += weight * (0.575 if value else 0.925)
        row = {"time": time_ns * 1e-9, "clks": _pulse(time_ns, edges, 1.5), "voutp": yp, "voutn": yn}
        row.update({f"din{bit}": 1.5 * value for bit, value in enumerate(inputs)})
        rows.append(row)
    return rows


def _trace_156(
    *,
    tamper_input: bool = False,
    ignore_din3: bool = False,
    continuous_tracking: bool = False,
) -> list[dict[str, float]]:
    edges = (1.0, 11.0, 21.0, 31.0)
    changes = (
        (0.0, (0, 0, 0, 0, 0, 0, 0)),
        (8.0, (1, 0, 1, 0, 1, 0, 1)),
        (18.0, (0, 1, 1, 0, 0, 1, 0)),
        (28.0, (0, 0, 0, 1, 0, 0, 0)),
    )
    rows: list[dict[str, float]] = []
    for time_ns in _times():
        inputs = list(_state_at(time_ns, changes))
        sampled = list(
            inputs
            if continuous_tracking
            else _latched_state(time_ns, edges, changes, delay_ns=1.1)
        )
        if ignore_din3:
            sampled[3] = 0
        if tamper_input and time_ns >= 18.0:
            inputs[0] = 1 - inputs[0]
        vout = 1.0 / 128.0
        for bit, value in enumerate(sampled):
            vout += (2.0 ** -(bit + 1)) * (5.0 if value else 1.0)
        row = {"time": time_ns * 1e-9, "clks": _pulse(time_ns, edges, 0.9), "vout": vout}
        row.update({f"din{bit}": 0.9 * value for bit, value in enumerate(inputs)})
        rows.append(row)
    return rows


def _trace_159(*, continuous_tracking: bool = False) -> list[dict[str, float]]:
    edges = (1.0, 11.0, 21.0, 31.0)
    changes = (
        (0.0, tuple(0 for _ in range(15))),
        (8.0, tuple(int(bit < 5) for bit in range(15))),
        (18.0, tuple(int(bit < 10) for bit in range(15))),
        (28.0, tuple(1 for _ in range(15))),
    )
    rows: list[dict[str, float]] = []
    for time_ns in _times():
        inputs = _state_at(time_ns, changes)
        sampled = inputs if continuous_tracking else _latched_state(time_ns, edges, changes, delay_ns=0.1)
        row = {
            "time": time_ns * 1e-9,
            "clks": _pulse(time_ns, edges, 0.9),
            "dout": sum(sampled) / 15.0,
        }
        row.update({f"dt{bit}": 0.9 * value for bit, value in enumerate(inputs)})
        rows.append(row)
    return rows


def test_repaired_checkers_accept_stimulus_relative_valid_traces() -> None:
    from checkers.v4.task_153 import CHECKER as checker_153
    from checkers.v4.task_156 import CHECKER as checker_156
    from checkers.v4.task_159 import CHECKER as checker_159

    for checker, rows in (
        (checker_153, _trace_153()),
        (checker_156, _trace_156()),
        (checker_159, _trace_159()),
    ):
        passed, note = checker(rows)
        assert passed, note
        assert "checked_property_ids=" in note


def test_153_rejects_fixed_output_replay_after_input_tampering() -> None:
    from checkers.v4.task_153 import CHECKER

    passed, note = CHECKER(_trace_153(tamper_input=True))
    assert not passed
    assert "P_CLOCKED_SIX_BIT_WEIGHTED_CODE" in note


def test_156_rejects_fixed_output_replay_after_input_tampering() -> None:
    from checkers.v4.task_156 import CHECKER

    passed, note = CHECKER(_trace_156(tamper_input=True))
    assert not passed
    assert "P_CLOCKED_SEVEN_BIT_WEIGHTED_SUM" in note


def test_153_rejects_ignored_din3_and_continuous_tracking() -> None:
    from checkers.v4.task_153 import CHECKER

    ignored, ignored_note = CHECKER(_trace_153(ignore_din3=True))
    tracking, tracking_note = CHECKER(_trace_153(continuous_tracking=True))
    assert not ignored
    assert "value_mismatch" in ignored_note
    assert not tracking
    assert "hold_mismatch" in tracking_note


def test_156_rejects_ignored_din3_and_continuous_tracking() -> None:
    from checkers.v4.task_156 import CHECKER

    ignored, ignored_note = CHECKER(_trace_156(ignore_din3=True))
    tracking, tracking_note = CHECKER(_trace_156(continuous_tracking=True))
    assert not ignored
    assert "value_mismatch" in ignored_note
    assert not tracking
    assert "hold_mismatch" in tracking_note


def test_159_rejects_continuous_tracking_between_clock_edges() -> None:
    from checkers.v4.task_159 import CHECKER

    passed, note = CHECKER(_trace_159(continuous_tracking=True))
    assert not passed
    assert "hold_mismatch" in note


def _trace_162(*, ignore_upper: bool = False, clock_glitch: bool = False) -> list[dict[str, float]]:
    edges = (1.0, 7.0, 13.0, 19.0, 25.0, 31.0, 37.0, 43.0, 49.0)
    changes = (
        (0.0, (1, 1, 1, 0, 0, 0, 0, 0)),
        (6.0, (1, 1, 1, 1, 1, 0, 0, 0)),
        (12.0, (1, 1, 1, 1, 1, 1, 0, 0)),
        (18.0, (1, 0, 0, 0, 0, 0, 1, 0)),
        (24.0, (1, 1, 1, 1, 1, 0, 0, 1)),
    )
    sampled_counts: list[int] = []
    rows: list[dict[str, float]] = []
    for time_ns in _times(52.0, 0.1):
        inputs = _state_at(time_ns, changes)
        prior_edges = [edge for edge in edges if edge <= time_ns]
        sampled_counts = [sum(_state_at(edge, changes)) for edge in prior_edges]
        code = sampled_counts[-5] if len(sampled_counts) >= 5 else 0
        if ignore_upper and len(sampled_counts) >= 5:
            sampled_inputs = _state_at(prior_edges[-5], changes)
            code = sum(sampled_inputs[:5])
        clock_high = _pulse(time_ns, edges, 0.9) > 0.45
        row = {"time": time_ns * 1e-9, "clk": 0.9 if clock_high else 0.0}
        row.update({f"din{bit}": 0.9 * value for bit, value in enumerate(inputs)})
        for bit in range(4):
            value = (code >> bit) & 1
            if clock_glitch and clock_high:
                value = 1 - value
            row[f"dout{bit}"] = float(value)
        rows.append(row)
    return rows


def _trace_163(*, publish_on_ready: bool = False) -> list[dict[str, float]]:
    ready_edges = (1.0, 2.0, 3.0, 4.0, 5.0, 13.0, 14.0, 15.0, 16.0)
    clock_edges = (10.0, 24.0)
    decisions = ((1, 0), (0, 1), (0, 0), (1, 0), (0, 1), (0, 1), (1, 0), (0, 0), (1, 0))
    rows: list[dict[str, float]] = []
    for time_ns in _times(30.0, 0.05):
        period_start = 0 if time_ns < 10.0 else (5 if time_ns < 24.0 else 9)
        prior_ready = [index for index, edge in enumerate(ready_edges) if edge <= time_ns]
        group = [index for index in prior_ready if period_start <= index < (5 if period_start == 0 else 9)]
        total = 0.0
        for offset, index in enumerate(group):
            dp, dn = decisions[index]
            weight = 2.0 ** (9 - offset)
            total += weight if dp else (0.5 * weight if dn else 0.0)
        first = 2.0**9 + 0.5 * 2.0**8 + 2.0**6 + 0.5 * 2.0**5
        second = 0.5 * 2.0**9 + 2.0**8 + 2.0**6
        published = 0.0 if time_ns < 10.0 else ((first / 1023.0 - 0.5) if time_ns < 24.0 else (second / 1023.0 - 0.5))
        dout = total / 1023.0 - 0.5 if publish_on_ready and group else published
        active = next((i for i, edge in enumerate(ready_edges) if edge - 0.2 <= time_ns < edge + 0.5), None)
        dp, dn = decisions[active] if active is not None else (0, 0)
        rows.append({
            "time": time_ns * 1e-9,
            "ready": _pulse(time_ns, ready_edges, 1.1),
            "clks": _pulse(time_ns, clock_edges, 1.1),
            "dp": 1.1 * dp,
            "dn": 1.1 * dn,
            "dout": dout,
        })
    return rows


def _trace_165(*, transparent: bool = False, wrong_fourth: bool = False) -> list[dict[str, float]]:
    edges = (1.0, 11.0, 21.0, 31.0)
    changes = (
        (0.0, (0, 0, 0, 0)),
        (8.0, (1, 0, 1, 0)),
        (18.0, (0, 1, 1, 1)),
        (28.0, (1, 1, 1, 1)),
    )
    weights = (0.0625, 0.125, 0.25, 0.5)
    rows: list[dict[str, float]] = []
    for time_ns in _times(36.0, 0.1):
        inputs = _state_at(time_ns, changes)
        sampled = inputs if transparent else _latched_state(time_ns, edges, changes, delay_ns=0.1)
        value = 1.8 * sum(weight * bit for weight, bit in zip(weights, sampled))
        if wrong_fourth and time_ns >= 31.1:
            value = 0.0
        row = {"time": time_ns * 1e-9, "rdy": _pulse(time_ns, edges, 1.8), "aout": value}
        row.update({f"din{bit + 1}": 1.8 * bit_value for bit, bit_value in enumerate(inputs)})
        rows.append(row)
    return rows


def test_162_observes_each_upper_input_independently() -> None:
    from checkers.v4.task_162 import CHECKER

    assert CHECKER(_trace_162())[0]
    passed, note = CHECKER(_trace_162(ignore_upper=True))
    assert not passed
    assert "P_BINARY_OUTPUT_ORDER" in note


def test_162_rejects_pure_clock_high_output_glitches() -> None:
    from checkers.v4.task_162 import CHECKER

    passed, note = CHECKER(_trace_162(clock_glitch=True))
    assert not passed
    assert "P_EVENT_HELD_OUTPUTS" in note


def test_163_rejects_publication_between_ready_glitches() -> None:
    from checkers.v4.task_163 import CHECKER

    assert CHECKER(_trace_163())[0]
    passed, note = CHECKER(_trace_163(publish_on_ready=True))
    assert not passed
    assert "P_CLOCKED_PUBLICATION_HOLD" in note


def test_165_checks_hold_and_fourth_ready_sample() -> None:
    from checkers.v4.task_165 import CHECKER

    assert CHECKER(_trace_165())[0]
    assert not CHECKER(_trace_165(transparent=True))[0]
    assert not CHECKER(_trace_165(wrong_fourth=True))[0]
