from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _times(stop_ns: float = 42.0, step_ns: float = 0.05) -> list[float]:
    return [index * step_ns for index in range(round(stop_ns / step_ns) + 1)]


def _pulse(time_ns: float, edges_ns: tuple[float, ...]) -> float:
    return 0.9 if any(edge <= time_ns < edge + 0.5 for edge in edges_ns) else 0.0


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
    delay_ns: float = 1.8,
) -> tuple[int, ...]:
    sampled = changes[0][1]
    for edge_ns in edges_ns:
        if time_ns >= edge_ns + delay_ns:
            sampled = _state_at(edge_ns, changes)
    return sampled


def _independent_changes() -> tuple[tuple[float, tuple[int, ...]], ...]:
    changes: list[tuple[float, tuple[int, ...]]] = [(0.0, (0, 0, 0, 0, 0, 0, 0, 0))]
    for bit, edge_ns in enumerate((1.0, 6.0, 11.0, 16.0, 21.0, 26.0, 31.0, 36.0)):
        one_hot = tuple(1 if index == bit else 0 for index in range(8))
        changes.append((edge_ns - 0.15, one_hot))
        changes.append((edge_ns + 0.55, (0, 0, 0, 0, 0, 0, 0, 0)))
    return tuple(changes)


def _grouped_changes() -> tuple[tuple[float, tuple[int, ...]], ...]:
    return (
        (0.0, (0, 0, 0, 0, 0, 0, 0, 0)),
        (8.0, (1, 1, 1, 0, 0, 0, 0, 0)),
        (18.0, (1, 1, 1, 1, 1, 0, 0, 0)),
        (28.0, (1, 1, 1, 1, 1, 1, 1, 1)),
    )


def _trace_158(
    *,
    changes: tuple[tuple[float, tuple[int, ...]], ...],
    edges_ns: tuple[float, ...],
    weights: tuple[float, ...] = (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0),
    stop_ns: float = 42.0,
) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for time_ns in _times(stop_ns):
        inputs = _state_at(time_ns, changes)
        sampled = _latched_state(time_ns, edges_ns, changes)
        weighted_count = sum(bit * weight for bit, weight in zip(sampled, weights))
        row = {
            "time": time_ns * 1e-9,
            "vin": 0.1,
            "clks": _pulse(time_ns, edges_ns),
            "dout": weighted_count / 8.0,
            "vres": 0.1 - (weighted_count - 4.0) / 8.0,
        }
        row.update({f"dt{bit}": 0.9 * value for bit, value in enumerate(inputs)})
        rows.append(row)
    return rows


def _legacy_sum_only_accepts(rows: list[dict[str, float]]) -> bool:
    from runners.checkers.v4.task_158 import (
        _v3_edge_sample_times,
        _v3_logic_at,
        sample_signal_at,
    )

    tap_names = [f"dt{idx}" for idx in range(8)]
    for edge_t, sample_t in _v3_edge_sample_times(rows, "clks", threshold=0.45):
        tap_bits = [_v3_logic_at(rows, name, edge_t, threshold=0.45) for name in tap_names]
        vin = sample_signal_at(rows, "vin", edge_t)
        dout = sample_signal_at(rows, "dout", sample_t)
        vres = sample_signal_at(rows, "vres", sample_t)
        if vin is None or dout is None or vres is None or any(bit is None for bit in tap_bits):
            return False
        count = float(sum(tap_bits))
        if abs(dout - count / 8.0) > 0.035:
            return False
        if abs(vres - (vin - (count - 4.0) / 8.0)) > 0.035:
            return False
    return True


def test_task158_accepts_independent_one_hot_tap_coverage() -> None:
    from runners.checkers.v4.task_158 import CHECKER

    passed, note = CHECKER(
        _trace_158(changes=_independent_changes(), edges_ns=(1.0, 6.0, 11.0, 16.0, 21.0, 26.0, 31.0, 36.0))
    )
    assert passed, note
    assert "independent_one_hot_taps=8" in note


def test_task158_rejects_old_pass_wrong_weight_regression() -> None:
    from runners.checkers.v4.task_158 import CHECKER

    group_preserving_wrong_weights = (2.0, 0.0, 1.0, 2.0, 0.0, 2.0, 0.0, 1.0)
    grouped_rows = _trace_158(
        changes=_grouped_changes(),
        edges_ns=(1.0, 11.0, 21.0, 31.0),
        weights=group_preserving_wrong_weights,
        stop_ns=40.0,
    )
    assert _legacy_sum_only_accepts(grouped_rows)
    passed, note = CHECKER(grouped_rows)
    assert not passed
    assert "missing_independent_tap_coverage" in note

    independent_rows = _trace_158(
        changes=_independent_changes(),
        edges_ns=(1.0, 6.0, 11.0, 16.0, 21.0, 26.0, 31.0, 36.0),
        weights=group_preserving_wrong_weights,
    )
    passed, note = CHECKER(independent_rows)
    assert not passed
    assert "max_dout_error=" in note
