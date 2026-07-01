from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
V3 = ROOT / "benchmark-vabench-release-v3"
TASKS = V3 / "TASKS.json"
TASK_ROOT = V3 / "tasks"


REQUIRED_EXTENSION_FIELDS = {
    "category",
    "certification_scope",
    "difficulty",
    "form",
    "id",
    "level",
    "syntax_focus",
    "target",
    "tier",
    "title",
}


def extension_tasks() -> dict[str, dict]:
    tasks = json.loads(TASKS.read_text(encoding="utf-8"))["tasks"]
    return {key: value for key, value in tasks.items() if int(key[:3]) > 300}


def test_all_v3_extension_tasks_have_manifest_metadata() -> None:
    tasks = extension_tasks()

    assert len(tasks) == 194
    for task_key, task in tasks.items():
        missing = REQUIRED_EXTENSION_FIELDS - set(task)
        assert missing == set(), f"{task_key} missing {sorted(missing)}"
        assert task["target"], f"{task_key} has no target artifact"
        assert str(task["certification_scope"]).endswith("_not_part_of_original_full_300_claim")
        assert str(task["tier"]).endswith("candidate")
        assert str(task["syntax_focus"]).strip()


def test_all_v3_extension_targets_exist_in_starter_and_solution() -> None:
    for task_key, task in extension_tasks().items():
        for target in task["target"]:
            assert (TASK_ROOT / task_key / "starter" / target).exists(), (
                f"{task_key} starter target missing: {target}"
            )
            assert (TASK_ROOT / task_key / "solution" / target).exists(), (
                f"{task_key} solution target missing: {target}"
            )


def test_all_v3_extension_prompts_state_required_behavior() -> None:
    for task_key in extension_tasks():
        instruction = (TASK_ROOT / task_key / "instruction.md").read_text(
            encoding="utf-8",
            errors="ignore",
        )
        assert "Required Behavior" in instruction, f"{task_key} lacks Required Behavior section"


def negative_variants(task_key: str) -> list[dict]:
    manifest = json.loads(
        (TASK_ROOT / task_key / "negative_variants" / "manifest.json").read_text(
            encoding="utf-8"
        )
    )
    for key in ("negative_variants", "cases", "variants"):
        value = manifest.get(key)
        if isinstance(value, list):
            return value
    return []


def test_all_v3_extension_negative_variants_are_materialized_and_distinct() -> None:
    for task_key in extension_tasks():
        variants = negative_variants(task_key)
        assert len(variants) == 5, f"{task_key} must have exactly five negative variants"
        seen_ids: set[str] = set()
        for variant in variants:
            variant_id = str(variant.get("id") or "")
            assert variant_id.startswith("neg_"), f"{task_key} malformed variant id {variant_id!r}"
            assert variant_id not in seen_ids, f"{task_key} duplicate variant id {variant_id}"
            seen_ids.add(variant_id)

            files = variant.get("files")
            assert isinstance(files, list) and files, f"{task_key} {variant_id} has no files"
            for file_name in files:
                negative_path = TASK_ROOT / task_key / "negative_variants" / file_name
                solution_path = TASK_ROOT / task_key / "solution" / Path(file_name).name
                assert negative_path.exists(), f"{task_key} {variant_id} missing {file_name}"
                assert solution_path.exists(), f"{task_key} solution missing {solution_path.name}"
                assert negative_path.read_text(encoding="utf-8", errors="ignore") != solution_path.read_text(
                    encoding="utf-8",
                    errors="ignore",
                ), f"{task_key} {variant_id} is identical to solution"
