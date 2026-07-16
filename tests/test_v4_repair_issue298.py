from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
    ROOT
    / "benchmark-vabench-release-v4"
    / "provenance"
    / "dut-base-v3-exact-five-hash-bound-v2"
)


def _family_dir(family_id: str) -> Path:
    matches = sorted(SOURCE.glob(f"{family_id}-*"))
    assert len(matches) == 1
    return matches[0]


def _read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _normalized_deck(path: Path) -> list[str]:
    lines = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("simulatorOptions options"):
            continue
        lines.append(re.sub(r"\s+", " ", line))
    return lines


def test_issue298_feedback_and_score_profiles_share_canonical_semantics() -> None:
    for number in range(201, 211):
        family = _family_dir(f"{number:03d}")
        evaluator = family / "evaluator"
        public = family / "public" / "task"
        harness = _read_json(evaluator / "harness_spec.json")
        feedback = _read_json(evaluator / "profiles" / "feedback.json")
        score = _read_json(evaluator / "profiles" / "score.json")

        assert feedback["property_ids"] == score["property_ids"] == harness["property_ids"]
        assert feedback["harness_spec_sha256"] == score["harness_spec_sha256"]
        assert feedback["parameters"] == score["parameters"]
        assert feedback["corners"] == score["corners"]
        assert feedback["simulatorOptions"] == {"evas_profile": "balanced"}
        assert score["simulatorOptions"] == {}
        assert feedback["deck_overrides"] == {}
        assert score["deck_overrides"] == {}
        assert harness["profile_defaults"]["feedback"].get("deck_overrides", {}) == {}
        assert harness["profile_defaults"]["score"].get("deck_overrides", {}) == {}

        assert _normalized_deck(public / "feedback_tb.scs") == _normalized_deck(
            evaluator / "score_tb.scs"
        )
