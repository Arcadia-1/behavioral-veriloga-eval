from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runners"))

from checkers.v4 import task_191, task_192, task_193, task_194


FAMILY_BASE = (
    ROOT
    / "benchmark-vabench-release-v4"
    / "provenance"
    / "dut-base-v3-exact-five-hash-bound-v2"
)


def _timing_rows(signal: str, *, immediate: bool) -> list[dict[str, float]]:
    return [
        {"time": 0.0, signal: 0.0},
        {"time": 25e-12, signal: 0.55 if immediate else 0.0},
        {"time": 100e-12, signal: 1.1},
    ]


def _initial_194_rows(*, wrong_phase: bool) -> list[dict[str, float]]:
    row = {
        "dout10": 0.0,
        "dout11": 0.0,
        "dout12": 0.0,
        "dout13": 0.0 if wrong_phase else 0.9,
        **{f"gainctrl{bit}": 0.9 if (90 >> bit) & 1 else 0.0 for bit in range(7)},
        "ddiff": 0.0,
        "dop": 0.96,
        "dom": 0.32,
        "gctrlcode": 0.90,
    }
    return [{"time": 0.0, **row}, {"time": 0.2e-9, **row}]


def test_task_191_rejects_bypassed_public_output_delay() -> None:
    assert task_191._assert_logic_levels(
        _timing_rows("d1", immediate=False), {"d1": 0}, 25e-12, vhi=1.1
    )[0]
    assert not task_191._assert_logic_levels(
        _timing_rows("d1", immediate=True), {"d1": 0}, 25e-12, vhi=1.1
    )[0]


def test_task_192_rejects_bypassed_public_logic_delay() -> None:
    assert task_192._assert_logic_levels(
        _timing_rows("cmpck", immediate=False), {"cmpck": 0}, 25e-12, vhi=1.1
    )[0]
    assert not task_192._assert_logic_levels(
        _timing_rows("cmpck", immediate=True), {"cmpck": 0}, 25e-12, vhi=1.1
    )[0]


def test_task_194_checks_initial_minus_dac_phase() -> None:
    assert task_194._check_initial_outputs(_initial_194_rows(wrong_phase=False), 0.1e-9)[0]
    ok, detail = task_194._check_initial_outputs(_initial_194_rows(wrong_phase=True), 0.1e-9)
    assert not ok
    assert "initial_dout13" in detail


def _pfd_rows(
    *,
    scale: float = 1.0,
    shift_s: float = 0.0,
    reset_fraction: float = 1.0,
    transition_s: float = 0.0,
) -> list[dict[str, float]]:
    source_events = ((0.92e-9, "in1"), (1.47e-9, "in2"), (2.57e-9, "in2"), (3.02e-9, "in1"))
    events = [(shift_s + scale * time_s, signal) for time_s, signal in source_events]
    reset_window = 120e-12 * reset_fraction
    transition_window = scale * transition_s

    def outputs_at(time_s: float) -> tuple[float, float]:
        state = 0
        clear_time: float | None = None
        for event_time, signal in events:
            if time_s < event_time:
                break
            if clear_time is not None and event_time >= clear_time:
                state = 0
                clear_time = None
            if signal == "in1":
                if state == -1:
                    state = 2
                    clear_time = event_time + reset_window
                else:
                    state = 1
            elif state == 1:
                state = 2
                clear_time = event_time + reset_window
            else:
                state = -1
        if clear_time is not None and time_s >= clear_time:
            if transition_window > 0.0 and time_s < clear_time + transition_window:
                level = 1.0 - (time_s - clear_time) / transition_window
                return level, level
            state = 0
        return {
            0: (0.0, 0.0),
            1: (1.0, 0.0),
            -1: (0.0, 1.0),
            2: (1.0, 1.0),
        }[state]

    rows: list[dict[str, float]] = []
    for index in range(901):
        source_time = index * 4.5e-9 / 900
        time_s = shift_s + scale * source_time
        up, dn = outputs_at(time_s)
        rows.append(
            {
                "time": time_s,
                "in1": 1.0 if 0.92e-9 <= source_time < 1.22e-9 or 3.02e-9 <= source_time < 3.32e-9 else 0.0,
                "in2": 1.0 if 1.47e-9 <= source_time < 1.77e-9 or 2.57e-9 <= source_time < 2.87e-9 else 0.0,
                "up": up,
                "dn": dn,
                "vdd": 1.0,
                "gnd": 0.0,
            }
        )
    return rows


def test_task_193_reset_window_uses_public_ton_contract() -> None:
    assert task_193.CHECKER(_pfd_rows())[0]
    assert task_193.CHECKER(_pfd_rows(scale=1.37, shift_s=2e-9))[0]
    assert task_193.CHECKER(
        _pfd_rows(scale=1.37, shift_s=2e-9, transition_s=30e-12)
    )[0]
    ok, detail = task_193.CHECKER(
        _pfd_rows(
            scale=1.37,
            shift_s=2e-9,
            reset_fraction=100.0 / 120.0,
            transition_s=40e-12,
        )
    )
    assert not ok
    assert "P_CLEAR_AFTER_RESET_WINDOW mismatch_count=" in detail
    for reset_fraction in (2.0 / 3.0, 0.35):
        ok, detail = task_193.CHECKER(
            _pfd_rows(scale=1.37, shift_s=2e-9, reset_fraction=reset_fraction)
        )
        assert not ok
        assert "P_CLEAR_AFTER_RESET_WINDOW mismatch_count=" in detail


def _assert_canonical_decks_match_harness(task_id: int) -> tuple[str, dict[str, object]]:
    family = next(FAMILY_BASE.glob(f"{task_id}-*"))
    score = (family / "evaluator/score_tb.scs").read_text()
    feedback = (family / "public/task/feedback_tb.scs").read_text()
    score_semantics = [line for line in score.splitlines() if line]
    feedback_semantics = [
        line
        for line in feedback.splitlines()
        if line and not line.startswith("simulatorOptions ")
    ]
    assert score_semantics == feedback_semantics
    harness = json.loads((family / "evaluator/harness_spec.json").read_text())
    for line in [*harness["deck"]["body_lines"], *harness["deck"]["analyses"]]:
        assert line in score
        assert line in feedback
    return score, harness


def test_task_196_stimulus_covers_positive_lo_negative_rf() -> None:
    score, harness = _assert_canonical_decks_match_harness(196)
    assert "tran tran stop=3.8n maxstep=10p" in score
    assert "3.0n 0.5" in score
    assert "3.0n -0.24" in score
    assert harness["deck"]["analyses"] == ["tran tran stop=3.8n maxstep=10p"]


def test_task_197_stimulus_separates_din0_and_din2() -> None:
    score, harness = _assert_canonical_decks_match_harness(197)
    assert "Vb0 (din0 0) vsource type=pwl wave=[0 0 1n 0 1.05n 0.9 2n 0.9 2.05n 0" in score
    assert "Vb2 (din2 0) vsource type=pwl wave=[0 0 1n 0 1.05n 0 2n 0 2.05n 0.9" in score
    assert "tran tran stop=3.8n maxstep=10p" in score
    assert harness["deck"]["analyses"] == ["tran tran stop=3.8n maxstep=10p"]
