#!/usr/bin/env python3
"""Audit the materialized 1,200-task tri-form release."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


PACKAGE_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RELEASE = PACKAGE_ROOT / "release" / "benchmarkv4"
FORMS = ("dut", "testbench", "bugfix")
MODES = ("G0", "G1", "G2", "G3", "G4", "G5")
FORM_SKILLS = {
    "dut": "dut_modeling.md",
    "testbench": "testbench_verification.md",
    "bugfix": "bugfix_diagnosis.md",
}
FEEDBACK_GUIDES = {
    "dut": "feedback_dut.md",
    "testbench": "feedback_testbench.md",
    "bugfix": "feedback_bugfix.md",
}
WRAPPERS_BY_PROCESS = {
    "direct_one_shot": "direct_wrapper.md",
    "agentic": "agentic_wrapper.md",
}
COMPONENT_SUBDIR_BY_NAME = {
    **{name: "form_skills" for name in FORM_SKILLS.values()},
    **{name: "feedback_guides" for name in FEEDBACK_GUIDES.values()},
    **{name: "wrappers" for name in WRAPPERS_BY_PROCESS.values()},
}
MATERIALIZED_ARTIFACTS = (
    "TASK_INDEX.json",
    "BUGFIX_SEED_REVIEW.json",
    "prompt_modes/PROMPT_RECORDS.jsonl",
    "prompt_modes/modes.json",
    "prompt_modes/manifest.json",
)
RELEASE_SEAL_ARTIFACTS = (
    "MANIFEST.json",
    *MATERIALIZED_ARTIFACTS,
    "AUDIT_REPORT.json",
    "RUNTIME_INGESTION_EVIDENCE.json",
)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prompt_component_path(release: Path, component_id: str) -> Path | None:
    subdir = COMPONENT_SUBDIR_BY_NAME.get(component_id)
    if subdir is None:
        return None
    return release / "prompt_modes" / subdir / component_id


def tree_sha(path: Path) -> str:
    digest = hashlib.sha256()
    for item in sorted(path.rglob("*")):
        if item.is_file():
            digest.update(item.relative_to(path).as_posix().encode("utf-8"))
            digest.update(b"\0")
            digest.update(item.read_bytes())
            digest.update(b"\0")
    return digest.hexdigest()


def public_bundle_hash(task_dir: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(task_dir.rglob("*")):
        if not path.is_file() or "evaluator" in path.parts or path.name == "TASK_RECORD.json":
            continue
        digest.update(path.relative_to(task_dir).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def build_release_seal(
    release: Path,
    source_manifest_sha256: str,
    certification_reuse: dict[str, Any],
) -> dict[str, Any]:
    artifact_hashes = {}
    for relative in RELEASE_SEAL_ARTIFACTS:
        path = release / relative
        if not path.is_file():
            raise SystemExit(f"cannot seal release; missing artifact: {relative}")
        artifact_hashes[relative] = file_sha(path)
    return {
        "schema_version": "v4-tri-form-release-seal-v1",
        "release_status": "gate3_hash_bound_certification_reused",
        "source_score_denominator_manifest_sha256": source_manifest_sha256,
        "artifact_sha256": artifact_hashes,
        "certification_reuse": certification_reuse,
        "simulation_claim": "canonical DUT gold and exact-five negative EVAS/Spectre certifications reused by hash",
    }


def expected_task_id(form: str, family: str) -> str:
    offsets = {"dut": 0, "testbench": 500, "bugfix": 1000}
    value = offsets[form] + int(family)
    width = 3 if value < 1000 else 4
    return f"v4-{value:0{width}d}"


def mutation_certification_hashes(active_mutations: list[dict[str, Any]]) -> dict[str, str]:
    return {
        str(item.get("mutation_id") or ""): str(item.get("certification_sha256") or "")
        for item in active_mutations
    }


def expected_buggy_artifact_hashes(
    artifact_paths: list[str],
    changed_hashes: dict[str, str],
    solution: Path,
) -> dict[str, str]:
    return {
        artifact: changed_hashes.get(artifact, file_sha(solution / artifact))
        for artifact in artifact_paths
    }


def audit_source_certifications(
    source: Path,
    source_rows: dict[str, dict[str, Any]],
    problems: list[str],
) -> dict[str, Any]:
    gold_count = 0
    negative_count = 0
    for family, row in sorted(source_rows.items()):
        task_dir = source / str(row.get("release_dir") or "")
        task_cert_path = task_dir / "evaluator" / "certification.json"
        expected_task_sha = str((row.get("hashes") or {}).get("task_certification_sha256") or "")
        if not task_cert_path.is_file() or file_sha(task_cert_path) != expected_task_sha:
            problems.append(f"{family}: source gold certification hash mismatch")
        else:
            certification = read_json(task_cert_path)
            evaluators = certification.get("evaluators") or {}
            if certification.get("status") != "gate2_pass":
                problems.append(f"{family}: source gold certification is not gate2_pass")
            for evaluator_name in ("evas", "spectre"):
                if (evaluators.get(evaluator_name) or {}).get("status") != "pass":
                    problems.append(f"{family}: source gold lacks {evaluator_name} PASS")
            gold_count += 1
        for mutation in row.get("active_mutations") or []:
            mutation_id = str(mutation.get("mutation_id") or "")
            cert_path = task_dir / str(mutation.get("certification_path") or "")
            expected_sha = str(mutation.get("certification_sha256") or "")
            if not cert_path.is_file() or file_sha(cert_path) != expected_sha:
                problems.append(f"{family}/{mutation_id}: source negative certification hash mismatch")
                continue
            certification = read_json(cert_path)
            evaluators = certification.get("evaluators") or {}
            if certification.get("outcome") != "killed_behaviorally":
                problems.append(f"{family}/{mutation_id}: source negative was not killed behaviorally")
            for evaluator_name in ("evas", "spectre"):
                if evaluators.get(evaluator_name) != "compile_pass_behavior_fail":
                    problems.append(f"{family}/{mutation_id}: source negative lacks {evaluator_name} behavioral kill")
            negative_count += 1
    return {
        "policy": "source_denominator_hash_bound",
        "source_dut_gold_certification_count": gold_count,
        "source_negative_certification_count": negative_count,
        "evaluators": ["evas", "spectre"],
        "simulation_rerun_required_for_materialization": False,
    }


def audit_task(
    release: Path,
    source: Path,
    source_manifest_sha: str,
    source_rows: dict[str, dict[str, Any]],
    row: dict[str, Any],
    problems: list[str],
) -> None:
    task_dir = release / str(row.get("task_dir") or "")
    task_id = str(row.get("task_id") or "")
    form = str(row.get("form") or "")
    family = str(row.get("family_id") or "")
    prefix = f"{task_id or task_dir.name}:"
    if not task_dir.is_dir():
        problems.append(f"{prefix} task directory missing")
        return
    for required in ("TASK_RECORD.json", "instruction.md", "public_contract.json"):
        if not (task_dir / required).is_file():
            problems.append(f"{prefix} missing {required}")
    if problems and not (task_dir / "TASK_RECORD.json").is_file():
        return
    record = read_json(task_dir / "TASK_RECORD.json")
    contract = read_json(task_dir / "public_contract.json")
    if task_id != expected_task_id(form, family):
        problems.append(f"{prefix} ID does not match form/family numbering")
    if record.get("task_id") != task_id or record.get("form") != form or record.get("family_id") != family:
        problems.append(f"{prefix} task record identity mismatch")
    if contract.get("task_id") != task_id or contract.get("form") != form or str(contract.get("family_id")) != family:
        problems.append(f"{prefix} public contract identity mismatch")
    if record.get("public_bundle_sha256") != public_bundle_hash(task_dir):
        problems.append(f"{prefix} public bundle hash mismatch")
    source_task = PACKAGE_ROOT / str(record.get("canonical_dut_source") or "")
    if not source_task.is_dir() or source not in source_task.parents:
        problems.append(f"{prefix} canonical DUT source is invalid")
        return
    spec_path = source_task / "evaluator" / "family_spec.json"
    if not spec_path.is_file() or record.get("family_spec_sha256") != file_sha(spec_path):
        problems.append(f"{prefix} family spec hash mismatch")
        return
    spec = read_json(spec_path)
    artifact_paths = [str(item["path"]) for item in spec["artifact_contract"]["files"]]
    source_row = source_rows.get(family)
    if source_row is None:
        problems.append(f"{prefix} canonical denominator row missing")
        return
    if form == "dut":
        if record.get("candidate_artifacts") != artifact_paths:
            problems.append(f"{prefix} DUT candidate artifacts differ from family spec")
        return
    evaluator = task_dir / "evaluator"
    if not evaluator.is_dir():
        problems.append(f"{prefix} evaluator directory missing")
        return
    derivation = read_json(evaluator / "derivation_manifest.json")
    assignment = derivation.get("negative_assignment") or {}
    suite = assignment.get("testbench_suite") or []
    if len(suite) != 5 or len(set(suite)) != 5:
        problems.append(f"{prefix} testbench suite is not exactly five unique mutations")
    active_mutations = source_row.get("active_mutations") or []
    expected_suite = [str(item.get("mutation_id") or "") for item in active_mutations]
    if suite != expected_suite:
        problems.append(f"{prefix} testbench suite differs from the exact-five denominator")
    if assignment.get("bugfix_seed") not in suite:
        problems.append(f"{prefix} bugfix seed is not a member of the testbench suite")
    base_dut = derivation.get("base_dut") or {}
    expected_base = {
        "canonical_task_id": f"v4-{family}",
        "canonical_task_slug": source_task.name,
        "family_spec_sha256": file_sha(spec_path),
        "mutation_catalog_sha256": file_sha(source_task / "evaluator" / "mutation_catalog.json"),
        "source_release_manifest_sha256": source_manifest_sha,
    }
    for field, expected in expected_base.items():
        if base_dut.get(field) != expected:
            problems.append(f"{prefix} derivation base hash mismatch for {field}")
    if base_dut.get("family_spec_sha256") != file_sha(spec_path):
        problems.append(f"{prefix} derivation family hash mismatch")
    if form == "testbench":
        if record.get("candidate_artifacts") != ["testbench.scs"] or contract.get("target_artifacts") != ["testbench.scs"]:
            problems.append(f"{prefix} testbench output is not exactly testbench.scs")
        score = read_json(evaluator / "score_policy.json")
        if score.get("candidate_artifacts") != ["testbench.scs"] or score.get("kill_ratio_denominator") != 5:
            problems.append(f"{prefix} testbench score policy mismatch")
        supplied = task_dir / "supplied_dut"
        if tree_sha(supplied) != tree_sha(source_task / "evaluator" / "solution"):
            problems.append(f"{prefix} supplied DUT differs from canonical gold")
        reference = read_json(evaluator / "reference_certificate.json")
        score_tb = source_task / "evaluator" / "score_tb.scs"
        score_tb_sha = file_sha(score_tb)
        if file_sha(evaluator / "reference_tb.scs") != score_tb_sha:
            problems.append(f"{prefix} reference testbench differs from the canonical score deck")
        expected_cert_hashes = mutation_certification_hashes(active_mutations)
        if reference.get("reference_tb_sha256") != score_tb_sha:
            problems.append(f"{prefix} reference testbench certificate hash mismatch")
        if reference.get("mutation_certification_sha256") != expected_cert_hashes:
            problems.append(f"{prefix} mutation certification hash map differs from the denominator")
        for item in active_mutations:
            mutation_id = str(item.get("mutation_id") or "")
            cert_path = source_task / str(item.get("certification_path") or "")
            expected_sha = str(item.get("certification_sha256") or "")
            if not cert_path.is_file() or file_sha(cert_path) != expected_sha:
                problems.append(f"{prefix} source certification hash mismatch for {mutation_id}")
                continue
            certification = read_json(cert_path)
            if certification.get("outcome") != "killed_behaviorally":
                problems.append(f"{prefix} source certification is not behaviorally killed for {mutation_id}")
            evaluators = certification.get("evaluators") or {}
            for evaluator_name in ("evas", "spectre"):
                if evaluators.get(evaluator_name) != "compile_pass_behavior_fail":
                    problems.append(
                        f"{prefix} source certification lacks {evaluator_name} behavioral kill "
                        f"for {mutation_id}"
                    )
        if reference.get("negative_suite_status") != "five_of_five_killed_behaviorally":
            problems.append(f"{prefix} reference testbench is not five-of-five certified")
        public_text = (task_dir / "instruction.md").read_text(encoding="utf-8") + json.dumps(contract)
        if "neg_" in public_text or "mutation_id" in public_text:
            problems.append(f"{prefix} public testbench view leaks negative identity")
    elif form == "bugfix":
        if record.get("candidate_artifacts") != artifact_paths or contract.get("target_artifacts") != artifact_paths:
            problems.append(f"{prefix} bugfix artifact contract mismatch")
        buggy = task_dir / "buggy_bundle"
        buggy_paths = sorted(path.relative_to(buggy).as_posix() for path in buggy.rglob("*.va"))
        if buggy_paths != sorted(artifact_paths):
            problems.append(f"{prefix} buggy bundle file set mismatch")
        seed_id = str(assignment.get("bugfix_seed") or "")
        mutation_catalog = read_json(source_task / "evaluator" / "mutation_catalog.json")
        mutation_rows = {
            str(item.get("id") or ""): item for item in mutation_catalog.get("mutations") or []
        }
        seed_catalog = mutation_rows.get(seed_id)
        if seed_catalog is None:
            problems.append(f"{prefix} Bugfix seed is missing from the canonical mutation catalog")
        else:
            changed_hashes = seed_catalog.get("artifact_hashes") or {}
            expected_hashes = expected_buggy_artifact_hashes(
                artifact_paths,
                changed_hashes,
                source_task / "evaluator" / "solution",
            )
            actual_hashes = {
                path.relative_to(buggy).as_posix(): file_sha(path)
                for path in buggy.rglob("*.va")
            }
            if actual_hashes != expected_hashes:
                problems.append(f"{prefix} buggy bundle differs from the selected canonical mutation")
        if tree_sha(buggy) == tree_sha(source_task / "evaluator" / "solution"):
            problems.append(f"{prefix} buggy bundle is byte-identical to gold")
        private_materialization = derivation.get("private_materialization") or {}
        if private_materialization.get("buggy_bundle_sha256") != tree_sha(buggy):
            problems.append(f"{prefix} buggy bundle hash mismatch")
        gold_reference = read_json(evaluator / "gold_repair_reference.json")
        if gold_reference.get("solution_tree_sha256") != tree_sha(source_task / "evaluator" / "solution"):
            problems.append(f"{prefix} gold repair solution hash mismatch")
        if gold_reference.get("gold_dut_certification_sha256") != (
            source_row.get("hashes") or {}
        ).get("task_certification_sha256"):
            problems.append(f"{prefix} gold DUT certification hash mismatch")
        public_text = (task_dir / "instruction.md").read_text(encoding="utf-8") + json.dumps(contract)
        forbidden = ("neg_", "faulty file", "root cause", "changed line", "public summary")
        for marker in forbidden:
            if marker.lower() in public_text.lower():
                problems.append(f"{prefix} public bugfix view leaks forbidden marker {marker!r}")
        if re.search(r"\bmutation\b", public_text, re.IGNORECASE):
            problems.append(f"{prefix} public bugfix view leaks forbidden marker 'mutation'")
        selection = derivation.get("selection_evidence") or {}
        if selection.get("selection_status") != "policy_reviewed" or selection.get("triviality_markers"):
            problems.append(f"{prefix} Bugfix seed lacks nontrivial semantic review")


def audit_prompt_records(release: Path, tasks: list[dict[str, Any]], problems: list[str]) -> int:
    path = release / "prompt_modes" / "PROMPT_RECORDS.jsonl"
    if not path.is_file():
        problems.append("prompt record file missing")
        return 0
    seen: dict[str, set[str]] = defaultdict(set)
    task_forms = {str(row["task_id"]): str(row["form"]) for row in tasks}
    task_dirs = {str(row["task_id"]): release / str(row["task_dir"]) for row in tasks}
    component_manifest = read_json(release / "prompt_modes" / "manifest.json")
    component_records = component_manifest.get("components") or {}
    tokenizer = component_manifest.get("reference_tokenizer") or {}
    tokenizer_key = f"{tokenizer.get('id')}@{tokenizer.get('version')}"
    required_assets = {
        *WRAPPERS_BY_PROCESS.values(), *FORM_SKILLS.values(), *FEEDBACK_GUIDES.values()
    }
    if set(component_records) != required_assets:
        problems.append("prompt component manifest set mismatch")
    for name, component in component_records.items():
        for field in ("stable_id", "semantic_version", "applicable_forms", "sha256", "bytes", "license", "provenance", "token_counts"):
            if field not in component:
                problems.append(f"prompt component manifest {name}: missing {field}")
        if tokenizer_key not in (component.get("token_counts") or {}):
            problems.append(f"prompt component manifest {name}: missing reference-tokenizer count")
    count = 0
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            problems.append(f"prompt record line {line_no} is invalid JSON: {exc}")
            continue
        count += 1
        task_id = str(row.get("task_id") or "")
        mode = str(row.get("mode") or "")
        seen[task_id].add(mode)
        expected_cli = mode in {"G2", "G3", "G4", "G5"}
        if row.get("feedback_cli_available") is not expected_cli:
            problems.append(f"{task_id}/{mode}: feedback availability mismatch")
        expected_process = "direct_one_shot" if mode in {"G0", "G1"} else "agentic"
        if row.get("process") != expected_process:
            problems.append(f"{task_id}/{mode}: process mismatch")
        form = task_forms.get(task_id, "")
        task_dir = task_dirs.get(task_id)
        if task_dir is None:
            problems.append(f"{task_id}/{mode}: prompt record has no task directory")
            continue
        public_inputs = [task_dir / "instruction.md"]
        if form == "testbench":
            public_inputs.extend(sorted((task_dir / "supplied_dut").rglob("*.va")))
        elif form == "bugfix":
            public_inputs.extend(sorted((task_dir / "buggy_bundle").rglob("*.va")))
        expected_input_hashes = {
            item.relative_to(task_dir).as_posix(): file_sha(item) for item in public_inputs
        }
        if row.get("canonical_instruction_sha256") != file_sha(task_dir / "instruction.md"):
            problems.append(f"{task_id}/{mode}: canonical instruction hash mismatch")
        if row.get("public_input_hashes") != expected_input_hashes:
            problems.append(f"{task_id}/{mode}: public input hash replay mismatch")
        expected_skills: list[str] = []
        if mode in {"G1", "G3", "G5"}:
            expected_skills.append(FORM_SKILLS.get(form, ""))
        if mode in {"G4", "G5"}:
            expected_skills.append(FEEDBACK_GUIDES.get(form, ""))
        expected_wrapper = WRAPPERS_BY_PROCESS[expected_process]
        expected_components = [*expected_skills, expected_wrapper]
        skills = row.get("skill_hashes") or {}
        if set(skills) != set(expected_skills):
            problems.append(f"{task_id}/{mode}: exact skill composition mismatch")
        for name in expected_skills:
            if skills.get(name) != (component_records.get(name) or {}).get("sha256"):
                problems.append(f"{task_id}/{mode}: skill hash mismatch for {name}")
        prompt_component_hashes = row.get("prompt_component_hashes") or {}
        if set(prompt_component_hashes) != set(expected_components):
            problems.append(f"{task_id}/{mode}: exact prompt component composition mismatch")
        for name in expected_components:
            if prompt_component_hashes.get(name) != (component_records.get(name) or {}).get("sha256"):
                problems.append(f"{task_id}/{mode}: prompt component hash mismatch for {name}")
        component_order = row.get("component_order") or []
        expected_suffix = [*expected_skills, expected_wrapper]
        if component_order[-len(expected_suffix):] != expected_suffix:
            problems.append(f"{task_id}/{mode}: component order mismatch")
        static_components = row.get("static_components") or []
        if [item.get("id") for item in static_components] != component_order:
            problems.append(f"{task_id}/{mode}: static component fingerprint order mismatch")
        public_component_paths = {
            "instruction" if item.name == "instruction.md" else f"public_input:{item.relative_to(task_dir).as_posix()}": item
            for item in public_inputs
        }
        for item in static_components:
            component_id = str(item.get("id") or "")
            actual_path = public_component_paths.get(component_id)
            if actual_path is None and component_id in component_records:
                actual_path = prompt_component_path(release, component_id)
            if actual_path is None or not actual_path.is_file():
                problems.append(f"{task_id}/{mode}: unresolved static component {component_id}")
            elif item.get("sha256") != file_sha(actual_path) or item.get("bytes") != actual_path.stat().st_size:
                problems.append(f"{task_id}/{mode}: static component fingerprint mismatch for {component_id}")
            if not isinstance(item.get("bytes"), int) or item.get("bytes") < 0:
                problems.append(f"{task_id}/{mode}: invalid component byte count")
            if len(str(item.get("sha256") or "")) != 64:
                problems.append(f"{task_id}/{mode}: invalid component hash")
            if tokenizer_key not in (item.get("token_counts") or {}):
                problems.append(f"{task_id}/{mode}: missing component token count")
    expected_ids = {str(row["task_id"]) for row in tasks}
    if set(seen) != expected_ids:
        problems.append("prompt record task coverage mismatch")
    for task_id in expected_ids:
        if seen[task_id] != set(MODES):
            problems.append(f"{task_id}: prompt mode coverage mismatch")
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release", type=Path, default=DEFAULT_RELEASE)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--seal-output", type=Path)
    args = parser.parse_args()
    release = args.release.expanduser().resolve()
    manifest = read_json(release / "MANIFEST.json")
    tasks = read_json(release / "TASK_INDEX.json").get("tasks") or []
    source = PACKAGE_ROOT / str(manifest.get("source_release") or "")
    problems: list[str] = []
    source_manifest_path = source / "score_denominator_manifest.json"
    if not source_manifest_path.is_file():
        raise SystemExit(f"source denominator missing: {source_manifest_path}")
    source_manifest = read_json(source_manifest_path)
    source_manifest_sha = file_sha(source_manifest_path)
    source_rows = {
        str(item.get("canonical_dut_id") or ""): item
        for item in source_manifest.get("tasks") or []
    }
    expected_materialized_hashes = {
        relative: file_sha(release / relative)
        for relative in MATERIALIZED_ARTIFACTS
        if (release / relative).is_file()
    }
    if set(expected_materialized_hashes) != set(MATERIALIZED_ARTIFACTS):
        problems.append("one or more materialized release artifacts are missing")
    if manifest.get("materialized_artifact_sha256") != expected_materialized_hashes:
        problems.append("materialized artifact hash binding mismatch")
    certification_reuse = audit_source_certifications(source, source_rows, problems)
    counts = Counter(str(row.get("form") or "") for row in tasks)
    if len(tasks) != 1200 or counts != Counter({form: 400 for form in FORMS}):
        problems.append(f"task counts mismatch: total={len(tasks)} forms={dict(counts)}")
    family_forms: dict[str, set[str]] = defaultdict(set)
    for row in tasks:
        family_forms[str(row.get("family_id") or "")].add(str(row.get("form") or ""))
        audit_task(release, source, source_manifest_sha, source_rows, row, problems)
    expected_families = {f"{value:03d}" for value in range(1, 401)}
    if set(family_forms) != expected_families:
        problems.append("family coverage is not exactly 001-400")
    for family in expected_families:
        if family_forms[family] != set(FORMS):
            problems.append(f"{family}: missing one or more task forms")
    task_by_family_form = {
        (str(row.get("family_id") or ""), str(row.get("form") or "")): release / str(row.get("task_dir") or "")
        for row in tasks
    }
    for family in sorted(expected_families):
        testbench_dir = task_by_family_form.get((family, "testbench"))
        bugfix_dir = task_by_family_form.get((family, "bugfix"))
        if testbench_dir is None or bugfix_dir is None:
            continue
        testbench_seed = (
            read_json(testbench_dir / "evaluator" / "derivation_manifest.json").get("negative_assignment") or {}
        ).get("bugfix_seed")
        bugfix_seed = (
            read_json(bugfix_dir / "evaluator" / "derivation_manifest.json").get("negative_assignment") or {}
        ).get("bugfix_seed")
        if testbench_seed != bugfix_seed:
            problems.append(
                f"{family}: cross-form Bugfix seed mismatch: testbench={testbench_seed} bugfix={bugfix_seed}"
            )
    prompt_count = audit_prompt_records(release, tasks, problems)
    if prompt_count != 7200:
        problems.append(f"prompt record count is {prompt_count}, expected 7200")
    report = {
        "schema_version": "v4-tri-form-release-audit-v1",
        "status": "pass" if not problems else "fail",
        "family_count": len(family_forms),
        "task_count": len(tasks),
        "task_counts": dict(sorted(counts.items())),
        "prompt_record_count": prompt_count,
        "certification_reuse": certification_reuse,
        "input_hashes": {
            "source_score_denominator_manifest_sha256": source_manifest_sha,
            "manifest_sha256": file_sha(release / "MANIFEST.json"),
            **expected_materialized_hashes,
        },
        "problems": problems,
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.seal_output:
        if problems:
            raise SystemExit("cannot seal release while audit problems remain")
        if not args.output:
            raise SystemExit("--seal-output requires --output so the audit report can be hash-bound")
        seal = build_release_seal(release, source_manifest_sha, certification_reuse)
        args.seal_output.parent.mkdir(parents=True, exist_ok=True)
        args.seal_output.write_text(json.dumps(seal, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not problems else 1


if __name__ == "__main__":
    raise SystemExit(main())
