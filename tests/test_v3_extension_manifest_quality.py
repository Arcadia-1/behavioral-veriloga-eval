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
