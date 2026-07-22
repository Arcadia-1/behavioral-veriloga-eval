from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNERS = ROOT / "runners"
if str(RUNNERS) not in sys.path:
    sys.path.insert(0, str(RUNNERS))

from checkers.v4.task_113 import CHECKER, PROPERTY_IDS


TASK = (
    ROOT
    / "benchmark-vabench-release-v4"
    / "provenance"
    / "dut-base-v3-exact-five-hash-bound-v2"
    / "113-sar-weighted-sum"
)
BIT_SIGNALS = ("d10", "d9", "d8", "d7", "d6", "d5", "d4", "d3", "d2", "d1", "d0")
WEIGHTS = (448, 256, 128, 80, 48, 32, 16, 8, 4, 2, 1)
LOW_LEVEL = 0.55
HIGH_LEVEL = 0.75
OVERRIDE_VTH = 0.65


def _sar_stair_rows(
    *,
    ignored_bit: str | None = None,
    hardcoded_default_vth: bool = False,
    state_noise: float = 0.0,
) -> list[dict[str, float]]:
    toggle_ns = {signal: 6.0 + 6.0 * index for index, signal in enumerate(BIT_SIGNALS)}
    rows = []
    for index in range(151):
        time_ns = index * 0.5
        code_weight = 0
        high_count = 0
        row = {"time": time_ns * 1e-9}
        for signal, weight in zip(BIT_SIGNALS, WEIGHTS):
            high = time_ns >= toggle_ns[signal]
            row[signal] = HIGH_LEVEL if high else LOW_LEVEL
            high_count += int(high)
            decoded_high = row[signal] > (0.45 if hardcoded_default_vth else OVERRIDE_VTH)
            if decoded_high and signal != ignored_bit:
                code_weight += weight
        noise = state_noise if high_count % 2 else -state_noise
        row["vout"] = code_weight / 512.0 - 1.0 + noise
        rows.append(row)
    return rows


def test_task113_accepts_the_legal_eleven_bit_weighted_sum() -> None:
    passed, note = CHECKER(_sar_stair_rows())
    assert passed, note

    noisy_passed, noisy_note = CHECKER(_sar_stair_rows(state_noise=0.00015))
    assert noisy_passed, noisy_note


def test_task113_rejects_each_ignored_low_bit() -> None:
    for ignored_bit in ("d0", "d1", "d2", "d3"):
        passed, note = CHECKER(_sar_stair_rows(ignored_bit=ignored_bit))
        assert not passed, f"{ignored_bit} unexpectedly passed: {note}"
        assert "P_WEIGHT_ORDER" in note
        assert f"bit={ignored_bit}" in note


def test_task113_rejects_hardcoded_default_threshold() -> None:
    passed, note = CHECKER(_sar_stair_rows(hardcoded_default_vth=True))
    assert not passed
    assert "P_WEIGHT_ORDER" in note


def test_task113_score_feedback_and_property_inventory_are_bound() -> None:
    harness_path = TASK / "evaluator" / "harness_spec.json"
    harness = json.loads(harness_path.read_text())
    harness_sha = hashlib.sha256(harness_path.read_bytes()).hexdigest()
    score = json.loads((TASK / "evaluator" / "profiles" / "score.json").read_text())
    feedback = json.loads((TASK / "evaluator" / "profiles" / "feedback.json").read_text())

    assert tuple(harness["property_ids"]) == PROPERTY_IDS
    assert score["property_ids"] == feedback["property_ids"] == harness["property_ids"]
    assert score["harness_spec_sha256"] == feedback["harness_spec_sha256"] == harness_sha

    score_deck = (TASK / "evaluator" / "score_tb.scs").read_text()
    feedback_deck = (TASK / "public" / "task" / "feedback_tb.scs").read_text()
    normalized_feedback = feedback_deck.replace("simulatorOptions options evas_profile=balanced\n\n", "")
    assert score_deck == normalized_feedback
    for index, signal in enumerate(BIT_SIGNALS):
        assert f"V{signal} ({signal} 0)" in score_deck
        assert "vth=0.65" in score_deck
        assert f"{6 + 6 * index}.1n 0.75" in score_deck
        assert "0 0.55" in score_deck
