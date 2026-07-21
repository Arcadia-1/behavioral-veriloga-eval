from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runners"))

from checkers.v4.task_166 import CHECKER


TASK = (
    ROOT
    / "benchmark-vabench-release-v4"
    / "provenance"
    / "dut-base-v3-exact-five-hash-bound-v2"
    / "166-l2-cdac-4b-residue"
)


def _rows(*, rising_sample: bool, scale: float = 1.0, shift_s: float = 0.0):
    rows: list[dict[str, float]] = []
    state = 0.1
    previous = {name: 0.0 for name in ("clks", "dctrl1", "dctrl2", "dctrl3")}
    for index in range(901):
        source_ns = index * 0.02
        vin = 0.1 if source_ns < 12.0 else -0.2 if source_ns < 13.3 else 0.3
        signals = {
            "clks": 1.0 if 1.05 <= source_ns < 1.55 or 13.05 <= source_ns < 13.55 else 0.0,
            "dctrl3": 1.0 if 3.05 <= source_ns < 3.40 else 0.0,
            "dctrl2": 1.0 if 5.05 <= source_ns < 5.40 or 15.05 <= source_ns < 15.40 else 0.0,
            "dctrl1": 1.0 if 7.05 <= source_ns < 7.40 else 0.0,
        }
        clock_event = (
            previous["clks"] < 0.5 <= signals["clks"]
            if rising_sample
            else previous["clks"] >= 0.5 > signals["clks"]
        )
        if clock_event:
            state = vin
        for signal, step in (("dctrl3", 0.5), ("dctrl2", 0.25), ("dctrl1", 0.125)):
            if previous[signal] < 0.5 <= signals[signal]:
                state += step
        rows.append(
            {
                "time": shift_s + scale * source_ns * 1e-9,
                "vin": vin,
                **signals,
                "vres": state,
            }
        )
        previous = signals
    return rows


def test_task166_falling_edge_is_observable_and_timing_invariant() -> None:
    assert CHECKER(_rows(rising_sample=False))[0]
    assert CHECKER(_rows(rising_sample=False, scale=1.37, shift_s=2e-9))[0]
    passed, detail = CHECKER(_rows(rising_sample=True))
    assert not passed
    assert "property_id=P_FALLING_CLOCK_SAMPLE" in detail


def test_task166_canonical_decks_and_harness_share_edge_discriminating_stimulus() -> None:
    score = (TASK / "evaluator/score_tb.scs").read_text()
    feedback = (TASK / "public/task/feedback_tb.scs").read_text()
    score_semantics = [line for line in score.splitlines() if line]
    feedback_semantics = [
        line for line in feedback.splitlines()
        if line and not line.startswith("simulatorOptions ")
    ]
    assert score_semantics == feedback_semantics
    assert "13.25n -0.2 13.30n 0.3" in score
    assert "tran tran stop=18n maxstep=20p" in score
    harness = json.loads((TASK / "evaluator/harness_spec.json").read_text())
    for line in [*harness["deck"]["body_lines"], *harness["deck"]["analyses"]]:
        assert line in score


def test_task166_pure_edge_adversarial_fixture_preserves_all_control_steps() -> None:
    gold = (TASK / "evaluator/solution/l2_cdac_4b_residue.va").read_text()
    formal_mutation = (
        TASK
        / "evaluator/mutation_bundles/neg_004_sample_on_rising_clock/l2_cdac_4b_residue.va"
    ).read_text()
    falling = "cross(V(clks) - vdd / 2.0, -1)"
    rising = "cross(V(clks) - vdd / 2.0, +1)"
    assert falling in gold
    pure_edge_candidate = gold.replace(falling, rising, 1)
    assert rising in pure_edge_candidate
    assert "vres_level = vres_level + 0.125 * (vrefp - vrefn);" in pure_edge_candidate
    assert pure_edge_candidate.replace(rising, falling, 1) == gold

    # The certified bundle remains byte-compatible with its existing evidence;
    # the isolated edge-only adversary above is deliberately test-local.
    assert falling in formal_mutation
    assert "vres_level = vres_level + 0;" in formal_mutation
