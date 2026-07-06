from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
V3 = ROOT / "benchmark-vabench-release-v3"
TASKS = V3 / "TASKS.json"
CHECKS = V3 / "CHECKS.yaml"
TASK_ROOT = V3 / "tasks"
SOP_AUDIT = V3 / "reports" / "extension_sop_audit.json"
STAGED_BLOCKER_MATRIX = V3 / "reports" / "staged_blocker_matrix.json"


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
    return {
        key: value
        for key, value in tasks.items()
        if (number := task_number(key)) is not None and number > 300
    }


def replacement_candidate_tasks() -> dict[str, dict]:
    tasks = json.loads(TASKS.read_text(encoding="utf-8"))["tasks"]
    return {
        key: value
        for key, value in tasks.items()
        if task_number(key) is None and str(value.get("tier", "")).endswith("replacement-candidate")
    }


def task_number(task_key: str) -> int | None:
    match = re.match(r"^(\d{3})-", task_key)
    return int(match.group(1)) if match else None


def expected_extension_count() -> int:
    return len(extension_tasks())


def test_non_numbered_replacement_candidates_are_opt_in_only() -> None:
    candidates = replacement_candidate_tasks()
    assert set(candidates) == {
        "candidate-bias-supply-bias-validity-gate",
        "candidate-bias-power-mode-supply-current-metric",
        "candidate-bias-dynamic-supply-level-driver",
        "candidate-bias-power-enable-turnon-delay-gate",
        "candidate-bias-reference-settling-window-monitor",
    }

    checks_text = CHECKS.read_text(encoding="utf-8")
    for task_key, task in candidates.items():
        assert task.get("candidate_only") is True
        assert task.get("default_sweep") is False
        assert task.get("counted_in_score") is False
        assert task.get("certification_scope") == "materialized_replacement_candidate_not_final_numbered_benchmark"
        assert "outside the scored denominator" in str(task.get("replacement_policy", ""))

        block = checks_block(task_key)
        assert "candidate_scope: opt_in_replacement_only" in block
        assert "default_sweep: false" in block
        assert "counted_in_score: false" in block
        assert task_key in checks_text


def test_all_v3_extension_tasks_have_manifest_metadata() -> None:
    tasks = extension_tasks()

    assert len(tasks) == expected_extension_count()
    for task_key, task in tasks.items():
        missing = REQUIRED_EXTENSION_FIELDS - set(task)
        assert missing == set(), f"{task_key} missing {sorted(missing)}"
        assert task["target"], f"{task_key} has no target artifact"
        certification_scope = str(task["certification_scope"])
        assert (
            certification_scope.endswith("_not_part_of_original_full_300_claim")
            or certification_scope == "materialized_replacement_candidate_not_final_301_plus_benchmark_number"
        )
        tier = str(task["tier"])
        assert tier.endswith("candidate") or tier.endswith("behavior-certified")
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


def test_all_v3_extension_support_artifacts_are_declared_and_materialized() -> None:
    support_tasks: list[str] = []
    for task_key, task in extension_tasks().items():
        support = task.get("support", [])
        assert isinstance(support, list), f"{task_key} support must be a list"
        manifest = json.loads(
            (TASK_ROOT / task_key / "test_harness" / "visible_hidden_manifest.json").read_text(
                encoding="utf-8"
            )
        )
        manifest_support = manifest.get("support", [])
        assert isinstance(manifest_support, list), f"{task_key} manifest support must be a list"
        assert manifest_support == support, f"{task_key} support mismatch between TASKS and harness manifest"

        if support:
            support_tasks.append(task_key)
        for artifact in support:
            assert "/" not in artifact and "\\" not in artifact, (
                f"{task_key} support artifact must be a flat filename: {artifact}"
            )
            assert (TASK_ROOT / task_key / "starter" / artifact).exists(), (
                f"{task_key} starter support missing: {artifact}"
            )
            assert (TASK_ROOT / task_key / "solution" / artifact).exists(), (
                f"{task_key} solution support missing: {artifact}"
            )

    assert "488-table-model-string-param-source" in support_tasks


def test_all_v3_extension_prompts_state_required_behavior() -> None:
    for task_key in extension_tasks():
        instruction = (TASK_ROOT / task_key / "instruction.md").read_text(
            encoding="utf-8",
            errors="ignore",
        )
        assert "Required Behavior" in instruction, f"{task_key} lacks Required Behavior section"


def test_all_v3_extension_tasks_have_manifest_behavior_contracts() -> None:
    for task_key, task in extension_tasks().items():
        assert str(task.get("description") or "").strip(), f"{task_key} missing manifest description"
        required_behavior = task.get("required_behavior")
        visible_tests = task.get("visible_tests")
        hidden_tests = task.get("hidden_tests")
        manifest_negative_ids = task.get("negative_variants")

        assert isinstance(required_behavior, list) and len(required_behavior) >= 2, (
            f"{task_key} must list manifest required behavior"
        )
        assert all(str(item).strip() for item in required_behavior)
        assert not any(str(item).lower().strip().endswith(("interface.", "parameters.")) for item in required_behavior)
        assert not any(str(item).lower().strip() == "required behavior." for item in required_behavior)
        assert not any(str(item).lstrip().startswith(("-", "*")) for item in required_behavior)
        assert not any("return exactly one source artifact" in str(item).lower() for item in required_behavior)
        assert not any(str(item).strip().endswith((";.", ":.")) for item in required_behavior)
        assert isinstance(visible_tests, list) and visible_tests, f"{task_key} missing visible test summary"
        assert isinstance(hidden_tests, list) and hidden_tests, f"{task_key} missing hidden test summary"

        expected_negative_ids = [str(variant["id"]) for variant in negative_variants(task_key)]
        assert manifest_negative_ids == expected_negative_ids, (
            f"{task_key} manifest negative_variants must mirror negative_variants/manifest.json"
        )


def test_all_v3_extension_negative_variant_descriptions_are_task_specific() -> None:
    banned_templates = (
        "Compiles and runs, but incorrectly forces the primary output to zero.",
        "Compiles and runs, but incorrectly reports the metric output as zero.",
        "Compiles and runs, but handles reset with the wrong polarity.",
        "Compiles and runs, but uses a shifted logic or comparison threshold.",
        "Compiles and runs, but scales the final output incorrectly.",
        "Force output low after otherwise plausible computation.",
        "Use a shifted threshold or condition that fails boundary checks.",
        "Use a shifted decision threshold that passes simple midscale smoke tests but fails boundary checks.",
        "Bias reset/state initialization so startup-sensitive tests fail.",
        "Offset the metric output while leaving the main path plausible.",
        "Offset the metric output while leaving the main output mostly plausible.",
        "Scale the final output so calibrated checks fail.",
        "Scale the final output so coarse tests may pass but calibrated checks fail.",
    )

    for task_key in extension_tasks():
        title = extension_tasks()[task_key]["title"]
        variants = negative_variants(task_key)
        cases = negative_cases_index(task_key)
        case_by_id = {str(case["id"]): case for case in cases}

        for variant in variants:
            variant_id = str(variant["id"])
            description = str(variant.get("description") or "")
            why_wrong = str(
                case_by_id[variant_id].get("why_wrong")
                or case_by_id[variant_id].get("description")
                or ""
            )

            assert description.startswith(f"{title}: "), (
                f"{task_key} {variant_id} description must name the task behavior"
            )
            assert description == why_wrong, (
                f"{task_key} {variant_id} manifest and negative_cases descriptions diverge"
            )
            assert not any(template in description for template in banned_templates), (
                f"{task_key} {variant_id} still uses a generic negative-template description"
            )


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

    assert len(distinct_tasks) == expected_extension_count()
    assert len(identical_tasks) == 0
    assert "361-white-noise-voltage-source" in distinct_tasks
    assert "397-hierarchy-gain-child" in distinct_tasks
    assert "409-macro-functionlike-clamp" in distinct_tasks
    assert "410-macro-ifdef-gain-select" in distinct_tasks
    assert "434-repeat-loop-accumulator" in distinct_tasks
    assert "445-limexp-soft-exponential" in distinct_tasks
    assert "457-nested-function-pipeline" in distinct_tasks
    assert "336-directive-configurable-threshold" in distinct_tasks
    assert "340-bound-step-clock-guard" in distinct_tasks
    assert "456-event-or-cross-timer" in distinct_tasks
    assert "331-above-threshold-latch" in distinct_tasks
    assert "335-above-resettable-peak-marker" in distinct_tasks
    assert "327-idtmod-wrapped-ramp-source" in distinct_tasks
    assert "330-idtmod-clock-phase-meter" in distinct_tasks
    assert "431-hierarchy-support-artifact-staging" in distinct_tasks
    assert "435-ddt-voltage-derivative-source" in distinct_tasks
    assert "444-zi-zp-discrete-filter" in distinct_tasks
    assert "489-event-nested-or-expression" in distinct_tasks
    assert "492-kcl-inductor-idt-voltage" in distinct_tasks


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


def negative_cases_index(task_key: str) -> list[dict]:
    cases_path = TASK_ROOT / task_key / "negative_variants" / "negative_cases.json"
    assert cases_path.exists(), f"{task_key} missing negative_cases.json"
    payload = json.loads(cases_path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        cases = payload.get("negative_cases")
        if isinstance(cases, list):
            return cases
    raise AssertionError(f"{task_key} negative_cases.json must be a list or contain negative_cases")


def checks_block(task_key: str) -> str:
    checks = CHECKS.read_text(encoding="utf-8")
    match = re.search(
        rf"^{re.escape(task_key)}: \|\n(?P<body>.*?)(?=^[^\s][^:\n]*: \|\n|\Z)",
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


def test_all_v3_extension_negative_cases_index_matches_manifest() -> None:
    for task_key in extension_tasks():
        variants = negative_variants(task_key)
        cases = negative_cases_index(task_key)
        assert len(cases) == 5, f"{task_key} negative_cases.json must list exactly five cases"

        variant_index = {
            str(variant.get("id") or ""): sorted(str(file_name) for file_name in variant.get("files", []))
            for variant in variants
        }
        case_index = {
            str(case.get("id") or ""): sorted(str(file_name) for file_name in case.get("files", []))
            for case in cases
        }
        assert case_index == variant_index, f"{task_key} negative_cases.json must mirror manifest.json"
        for case in cases:
            why_wrong = str(case.get("why_wrong") or case.get("description") or "").strip()
            assert len(why_wrong.split()) >= 4, f"{task_key} {case.get('id')} must explain why it is wrong"


def test_all_v3_extension_negative_variants_describe_expected_mutation() -> None:
    for task_key in extension_tasks():
        for variant in negative_variants(task_key):
            variant_id = str(variant.get("id") or "")
            expected = str(variant.get("expected") or "")
            description = str(variant.get("description") or "").strip()

            assert expected.startswith("compile_but_fail_full_behavior"), (
                f"{task_key} {variant_id} must declare a partial-credit behavioral failure expectation"
            )
            assert len(description.split()) >= 4, (
                f"{task_key} {variant_id} must describe the intended behavior mutation"
            )
            assert "outputput" not in description and "inputput" not in description, (
                f"{task_key} {variant_id} has a mechanically corrupted mutation description"
            )


def test_behavior_certified_extension_checks_reference_expected_artifacts() -> None:
    sop_audit = json.loads(SOP_AUDIT.read_text(encoding="utf-8"))
    current_tasks = extension_tasks()
    sop_rows = [row for row in sop_audit["tasks"] if row["task"] in current_tasks]
    sop_tasks = {row["task"] for row in sop_rows}
    assert sop_tasks

    behavior_tasks = [
        task_key
        for task_key in current_tasks
        if task_key in sop_tasks and has_sim_correct(task_key)
    ]
    expected_ready_count = sum(
        1
        for row in sop_rows
        if row.get("sop_ready") and has_sim_correct(row["task"])
    )
    assert len(behavior_tasks) == expected_ready_count

    for task_key in behavior_tasks:
        task = current_tasks[task_key]
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
