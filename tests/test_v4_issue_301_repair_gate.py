from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
    ROOT
    / "benchmark-vabench-release-v4"
    / "provenance"
    / "dut-base-v3-exact-five-hash-bound-v2"
)
FAMILY_IDS = tuple(f"{value:03d}" for value in range(231, 241))


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def family_dir(family_id: str) -> Path:
    matches = sorted(SOURCE.glob(f"{family_id}-*"))
    assert len(matches) == 1
    return matches[0]


def normalize_profile(profile: dict) -> dict:
    normalized = dict(profile)
    normalized.pop("profile_name", None)
    normalized.pop("public_visible", None)
    normalized.pop("simulatorOptions", None)
    return normalized


def normalize_deck(text: str) -> list[str]:
    return [
        line.rstrip()
        for line in text.splitlines()
        if line.strip() and not line.strip().startswith("simulatorOptions options")
    ]


def test_issue_301_feedback_and_score_profiles_have_semantic_parity() -> None:
    for family_id in FAMILY_IDS:
        family = family_dir(family_id)
        evaluator = family / "evaluator"
        feedback = read_json(evaluator / "profiles" / "feedback.json")
        score = read_json(evaluator / "profiles" / "score.json")
        assert normalize_profile(feedback) == normalize_profile(score)
        assert normalize_deck((family / "public" / "task" / "feedback_tb.scs").read_text()) == normalize_deck(
            (evaluator / "score_tb.scs").read_text()
        )


def test_issue_301_hash_bindings_are_current_for_target_rows() -> None:
    for family_id in FAMILY_IDS:
        family = family_dir(family_id)
        evaluator = family / "evaluator"
        record = read_json(evaluator / "task_record.json")
        row = read_json(SOURCE / "score_denominator_registry" / f"{family_id}.json")[
            "task"
        ]
        assert record["readiness_evidence"]["sha256"] == file_sha(evaluator / "certification.json")
        assert row["canonical_dut_id"] == family_id
        assert row["hashes"] == {
            "mutation_catalog_sha256": file_sha(evaluator / "mutation_catalog.json"),
            "score_deck_sha256": file_sha(evaluator / "score_tb.scs"),
            "task_certification_sha256": file_sha(evaluator / "certification.json"),
            "task_record_sha256": file_sha(evaluator / "task_record.json"),
        }


def test_issue_301_uses_family_registry_without_generated_release_edits() -> None:
    assert not (SOURCE / "score_denominator_manifest.json").exists()
    assert all(
        (SOURCE / "score_denominator_registry" / f"{family_id}.json").is_file()
        for family_id in FAMILY_IDS
    )
