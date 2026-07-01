from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
V3 = ROOT / "benchmark-vabench-release-v3"
TASKS = V3 / "TASKS.json"
CHECKS = V3 / "CHECKS.yaml"
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


def scs_has_feature(text: str, feature: str) -> bool:
    lowered = text.lower()
    if feature == "include":
        return "ahdl_include" in lowered or re.search(r"(?m)^\s*include\b", text) is not None
    if feature == "instance":
        return re.search(r"(?im)^\s*x\w*\s*\(", text) is not None
    if feature == "source":
        return "vsource" in lowered or "isource" in lowered
    if feature == "tran":
        return re.search(r"(?im)^\s*tran\b", text) is not None
    if feature == "save":
        return re.search(r"(?im)^\s*save\b", text) is not None
    raise AssertionError(f"unknown SCS feature {feature!r}")


def test_all_v3_extension_tasks_have_visible_and_hidden_harness_files() -> None:
    for task_key in extension_tasks():
        base = TASK_ROOT / task_key
        for rel_path in (
            "test_visible/visible.scs",
            "test_hidden/hidden.scs",
            "test_harness/visible_hidden_manifest.json",
        ):
            assert (base / rel_path).exists(), f"{task_key} missing {rel_path}"


def test_all_v3_extension_harness_manifests_reference_visible_and_hidden_scs() -> None:
    for task_key in extension_tasks():
        manifest = json.loads(
            (TASK_ROOT / task_key / "test_harness" / "visible_hidden_manifest.json").read_text(
                encoding="utf-8"
            )
        )
        manifest_text = json.dumps(manifest).lower()
        assert "visible.scs" in manifest_text, f"{task_key} manifest does not expose visible.scs"
        assert "hidden.scs" in manifest_text, f"{task_key} manifest does not protect hidden.scs"


def test_all_v3_extension_visible_and_hidden_scs_are_executable_testbenches() -> None:
    required_features = ("include", "instance", "source", "tran", "save")
    for task_key in extension_tasks():
        for rel_path in ("test_visible/visible.scs", "test_hidden/hidden.scs"):
            text = (TASK_ROOT / task_key / rel_path).read_text(
                encoding="utf-8",
                errors="ignore",
            )
            missing = [
                feature
                for feature in required_features
                if not scs_has_feature(text, feature)
            ]
            assert missing == [], f"{task_key} {rel_path} missing SCS features {missing}"


def test_v3_extension_visible_hidden_diversity_is_audited() -> None:
    distinct_tasks: list[str] = []
    identical_tasks: list[str] = []
    for task_key in extension_tasks():
        visible = (TASK_ROOT / task_key / "test_visible" / "visible.scs").read_text(
            encoding="utf-8",
            errors="ignore",
        )
        hidden = (TASK_ROOT / task_key / "test_hidden" / "hidden.scs").read_text(
            encoding="utf-8",
            errors="ignore",
        )
        if visible == hidden:
            identical_tasks.append(task_key)
        else:
            distinct_tasks.append(task_key)

    assert len(distinct_tasks) == 172
    assert len(identical_tasks) == 22
    assert "327-idtmod-wrapped-ramp-source" in identical_tasks
    assert "341-wreal-gain-pass-through" in distinct_tasks
    assert "346-logic-assign-inverter" in distinct_tasks
    assert "351-always-posedged-dff" in distinct_tasks
    assert "356-mixed-logic-enable-voltage-driver" in distinct_tasks
    assert "361-white-noise-voltage-source" in distinct_tasks
    assert "397-hierarchy-gain-child" in distinct_tasks
    assert "409-macro-functionlike-clamp" in distinct_tasks
    assert "410-macro-ifdef-gain-select" in distinct_tasks
    assert "419-wreal-logic-threshold-bridge" in distinct_tasks
    assert "434-repeat-loop-accumulator" in distinct_tasks
    assert "445-limexp-soft-exponential" in distinct_tasks
    assert "457-nested-function-pipeline" in distinct_tasks
    assert "336-directive-configurable-threshold" in distinct_tasks
    assert "340-bound-step-clock-guard" in distinct_tasks
    assert "456-event-or-cross-timer" in distinct_tasks
    assert "331-above-threshold-latch" in distinct_tasks
    assert "335-above-resettable-peak-marker" in distinct_tasks


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


def checks_block(task_key: str) -> str:
    checks = CHECKS.read_text(encoding="utf-8")
    match = re.search(
        rf"^{re.escape(task_key)}: \|\n(?P<body>.*?)(?=^\d{{3}}-|\Z)",
        checks,
        flags=re.MULTILINE | re.DOTALL,
    )
    assert match, f"{task_key} missing CHECKS block"
    return match.group("body")


def sim_correct_refs(task_key: str, prefix: str) -> list[str]:
    body = checks_block(task_key)
    if "sim_correct:" not in body:
        return []
    return re.findall(rf"^\s+-\s+({re.escape(prefix)}\S+)", body, flags=re.MULTILINE)


def has_sim_correct(task_key: str) -> bool:
    return "sim_correct:" in checks_block(task_key)


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


def test_behavior_certified_extension_checks_reference_expected_artifacts() -> None:
    behavior_tasks = [
        task_key
        for task_key in extension_tasks()
        if has_sim_correct(task_key)
    ]
    assert len(behavior_tasks) == 153

    for task_key in behavior_tasks:
        task = extension_tasks()[task_key]
        positive_refs = sim_correct_refs(task_key, "solution/")
        negative_refs = sim_correct_refs(task_key, "negative_variants/")
        manifest_refs = {
            f"negative_variants/{file_name}"
            for variant in negative_variants(task_key)
            for file_name in variant["files"]
        }

        if positive_refs or negative_refs:
            assert positive_refs == [f"solution/{task['target'][0]}"], (
                f"{task_key} sim_correct positive must use canonical solution target"
            )
            assert set(negative_refs) == manifest_refs, (
                f"{task_key} sim_correct negatives must match negative manifest"
            )
            assert len(negative_refs) == 5, f"{task_key} sim_correct must include five negatives"
        else:
            assert (TASK_ROOT / task_key / "solution" / task["target"][0]).exists(), (
                f"{task_key} legacy sim_correct relies on TASKS target"
            )
            assert len(manifest_refs) == 5, (
                f"{task_key} legacy sim_correct relies on negative manifest"
            )
        for ref in [*positive_refs, *negative_refs]:
            assert (TASK_ROOT / task_key / ref).exists(), f"{task_key} missing CHECKS ref {ref}"
