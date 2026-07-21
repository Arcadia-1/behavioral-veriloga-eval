from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

TASK_ROOT = (
    ROOT
    / "benchmark-vabench-release-v4"
    / "provenance"
    / "dut-base-v3-exact-five-hash-bound-v2"
)


def _times(stop_ns: float, step_ns: float = 0.25) -> list[float]:
    return [index * step_ns for index in range(round(stop_ns / step_ns) + 1)]


def _pulse(time_ns: float, edges_ns: tuple[float, ...]) -> float:
    return 0.9 if any(edge <= time_ns < edge + 0.5 for edge in edges_ns) else 0.0


def _state_at(time_ns: float, changes: tuple[tuple[float, object], ...]) -> object:
    state = changes[0][1]
    for change_ns, next_state in changes:
        if time_ns >= change_ns:
            state = next_state
    return state


def _sampled_state(
    time_ns: float,
    edges_ns: tuple[float, ...],
    changes: tuple[tuple[float, object], ...],
    *,
    delay_ns: float = 0.0,
) -> object:
    sampled = changes[0][1]
    for edge_ns in edges_ns:
        if time_ns >= edge_ns + delay_ns:
            sampled = _state_at(edge_ns, changes)
    return sampled


def _trace_154(*, continuous_tracking: bool = False) -> list[dict[str, float]]:
    edges = (2.0, 12.0, 22.0, 32.0, 42.0)
    changes = (
        (0.0, -0.13),
        (5.0, 0.13),
        (7.0, -0.13),
        (8.0, -0.05),
        (18.0, 0.02),
        (28.0, 0.09),
        (38.0, 0.13),
    )
    thresholds = [-0.125 + tap * (0.25 / 31.0) for tap in (1, 5, 10, 15, 20, 25, 30)]
    rows: list[dict[str, float]] = []
    for time_ns in _times(46.0):
        vin = float(_state_at(time_ns, changes))
        sampled_vin = vin if continuous_tracking else float(_sampled_state(time_ns, edges, changes))
        row = {"time": time_ns * 1e-9, "vin": vin, "clk": _pulse(time_ns, edges)}
        row.update(
            {f"dout{index}": 0.9 if sampled_vin > threshold else 0.0 for index, threshold in enumerate(thresholds)}
        )
        rows.append(row)
    return rows


WEIGHTS_161 = (1, 2, 4, 8, 16, 32, 64, 64, 128, 256, 512)


def _trace_161(*, continuous_tracking: bool = False, d7_weight: int = 64) -> list[dict[str, float]]:
    edges = (1.0, 11.0, 21.0, 31.0, 42.0)
    changes = (
        (0.0, (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)),
        (4.0, (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)),
        (6.0, (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)),
        (8.0, (1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1)),
        (18.0, (0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1)),
        (28.0, (1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1)),
        (38.0, (0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0)),
    )
    weights = list(WEIGHTS_161)
    weights[7] = d7_weight
    rows: list[dict[str, float]] = []
    for time_ns in _times(46.0):
        bits = tuple(_state_at(time_ns, changes))
        sampled_bits = bits if continuous_tracking else tuple(_sampled_state(time_ns, edges, changes))
        code = sum(bit * weight for bit, weight in zip(sampled_bits, weights)) - 32
        row = {
            "time": time_ns * 1e-9,
            "clk": _pulse(time_ns, edges),
            "vout": (code + 0.5) * (1.8 / 1024.0) - 0.9,
        }
        row.update({f"D{index}": 0.9 * value for index, value in enumerate(bits)})
        rows.append(row)
    return rows


def test_154_rejects_continuous_tracking_but_accepts_clocked_hold() -> None:
    from runners.checkers.v4.task_154 import CHECKER

    passed, note = CHECKER(_trace_154())
    assert passed, note
    passed, note = CHECKER(_trace_154(continuous_tracking=True))
    assert not passed
    assert "hold_mismatch" in note


def test_161_checks_unsampled_hold_and_redundant_d7_weight() -> None:
    from runners.checkers.v4.task_161 import CHECKER

    passed, note = CHECKER(_trace_161())
    assert passed, note
    passed, note = CHECKER(_trace_161(continuous_tracking=True))
    assert not passed
    assert "P_OUTPUT_SMOOTH_HOLD" in note
    passed, note = CHECKER(_trace_161(d7_weight=32))
    assert not passed
    assert "P_OFFSET_MIDRISE_OUTPUT" in note


def _semantic_deck_lines(text: str) -> list[str]:
    return [
        line
        for line in text.splitlines()
        if line and not line.startswith("simulatorOptions options")
    ]


def test_strengthened_stimuli_preserve_feedback_score_timing_invariant() -> None:
    expected_markers = {
        "154-flash-adc-threshold-taps": ("5n 0.13", "7n -0.13"),
        "161-dac-restore-10bit-offset": ("42.05n 0.9", "38n 0.9", "stop=46n"),
    }
    for task_name, markers in expected_markers.items():
        task = TASK_ROOT / task_name
        feedback = (task / "public/task/feedback_tb.scs").read_text(encoding="utf-8")
        score = (task / "evaluator/score_tb.scs").read_text(encoding="utf-8")
        harness = json.loads((task / "evaluator/harness_spec.json").read_text(encoding="utf-8"))
        assert _semantic_deck_lines(feedback) == _semantic_deck_lines(score)
        for body_line in harness["deck"]["body_lines"]:
            assert body_line in feedback
            assert body_line in score
        for marker in markers:
            assert marker in feedback
            assert marker in score
            assert marker in json.dumps(harness)
