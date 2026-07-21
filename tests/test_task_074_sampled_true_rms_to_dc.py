from __future__ import annotations

import math
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
RUNNERS = ROOT / "runners"
if str(RUNNERS) not in sys.path:
    sys.path.insert(0, str(RUNNERS))

from checkers.v4.task_074 import CHECKER


TASK = (
    ROOT
    / "benchmark-vabench-release-v4"
    / "provenance"
    / "dut-base-v3-exact-five-hash-bound-v2"
    / "074-sampled-true-rms-to-dc-converter"
)


def _logic_reset(time_ns: float) -> bool:
    return time_ns < 2.5 or 42.0 <= time_ns < 46.0


def _logic_enable(time_ns: float) -> bool:
    return 3.0 <= time_ns < 23.0 or time_ns >= 31.0


def _differential(time_ns: float) -> float:
    return 0.28 * math.sin(2.0 * math.pi * time_ns / 19.0) + 0.08 * math.cos(
        2.0 * math.pi * time_ns / 11.0
    )


def _synthetic_rows(mode: str = "correct") -> list[dict[str, float]]:
    rising_edges = [1.0 + 4.0 * index for index in range(21)]
    falling_edges = [edge + 2.0 for edge in rising_edges]
    sample_events = falling_edges if mode == "falling" else rising_edges
    all_events = sorted((time, "sample") for time in sample_events)
    if mode != "reset_wrong":
        all_events.append((42.0, "reset"))
        all_events.sort()

    count = 0
    accumulation = 0.0
    rms_out = 0.0
    valid = 0.0
    event_index = 0
    rows: list[dict[str, float]] = []
    for index in range(1701):
        time_ns = index * 0.05
        while event_index < len(all_events) and all_events[event_index][0] <= time_ns + 1e-12:
            event_time, event_kind = all_events[event_index]
            if event_kind == "reset":
                count = 0
                accumulation = 0.0
                rms_out = 0.0
                valid = 0.0
            else:
                reset_active = _logic_reset(event_time)
                if mode == "reset_wrong":
                    reset_active = not reset_active
                if reset_active:
                    count = 0
                    accumulation = 0.0
                    rms_out = 0.0
                    valid = 0.0
                else:
                    valid = 0.0
                    if _logic_enable(event_time):
                        value = _differential(event_time)
                        accumulation += abs(value) if mode == "mean_abs" else value * value
                        count += 1
                        if count == 4:
                            if mode == "mean_abs":
                                rms_out = accumulation / 4.0
                            else:
                                divisor = 8.0 if mode == "scale_low" else 4.0
                                rms_out = math.sqrt(accumulation / divisor)
                            count = 0
                            accumulation = 0.0
                            valid = 0.9
            event_index += 1

        clock_phase = (time_ns - 1.0) % 4.0
        clk = 0.9 if time_ns >= 1.0 and clock_phase < 2.0 else 0.0
        differential = _differential(time_ns)
        rows.append(
            {
                "time": time_ns * 1e-9,
                "vinp": 0.45 + 0.5 * differential,
                "vinn": 0.45 - 0.5 * differential,
                "clk": clk,
                "reset": 0.9 if _logic_reset(time_ns) else 0.0,
                "enable": 0.9 if _logic_enable(time_ns) else 0.0,
                "rms_out": rms_out,
                "valid": valid,
            }
        )
    return rows


def test_task_074_checker_accepts_independently_recomputed_rms_trace() -> None:
    passed, detail = CHECKER(_synthetic_rows())
    assert passed, detail


def test_task_074_checker_rejects_five_behavioral_fault_classes() -> None:
    for mode in ("zero", "mean_abs", "falling", "reset_wrong", "scale_low"):
        rows = _synthetic_rows(mode)
        if mode == "zero":
            for row in rows:
                row["rms_out"] = 0.0
                row["valid"] = 0.0
        passed, detail = CHECKER(rows)
        assert not passed, f"{mode} unexpectedly passed: {detail}"


def test_task_074_public_contract_is_port_only_and_six_section() -> None:
    instruction = (TASK / "public/task/instruction.md").read_text(encoding="utf-8")
    headings = [
        "## Task Contract",
        "## Public Verilog-A Interface",
        "## Public Parameter Contract",
        "## Required Behavior",
        "## Modeling Constraints",
        "## Output Contract",
    ]
    assert all(heading in instruction for heading in headings)
    assert "sampled_true_rms_to_dc.va" in instruction
    assert "file I/O" in instruction
    assert "$fopen" not in instruction and "$fwrite" not in instruction


def test_task_074_gold_and_five_mutations_are_file_io_free() -> None:
    sources = [TASK / "evaluator/solution/sampled_true_rms_to_dc.va"]
    sources.extend(sorted((TASK / "evaluator/mutation_bundles").glob("neg_*/sampled_true_rms_to_dc.va")))
    assert len(sources) == 6
    for source in sources:
        text = source.read_text(encoding="utf-8")
        assert "module sampled_true_rms_to_dc" in text
        assert "$fopen" not in text
        assert "$fwrite" not in text
        assert "filename" not in text


def test_task_074_feedback_and_score_use_the_same_stimulus() -> None:
    feedback = (TASK / "public/task/feedback_tb.scs").read_text(encoding="utf-8")
    score = (TASK / "evaluator/score_tb.scs").read_text(encoding="utf-8")
    for deck in (feedback, score):
        assert "sampled_true_rms_to_dc.va" in deck
        assert "save vinp vinn clk reset enable rms_out valid" in deck
        assert "metric.out" not in deck
    assert feedback == score
    assert "period=5n" in feedback
