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
DEFAULT_PRIVATE_SUBDIR = "private_evaluator"
FORMS = ("dut", "testbench", "bugfix")
MODES = ("G0", "G1", "G2", "G3", "G4", "G5")
DIRECT_MODES = {"G0", "G1"}
AGENTIC_MODES = {"G2", "G3", "G4", "G5"}
WRAPPERS_BY_MODE = {
    "G0": "direct_wrapper.md",
    "G1": "direct_wrapper.md",
    "G2": "agentic_wrapper.md",
    "G3": "agentic_wrapper.md",
    "G4": "agentic_wrapper.md",
    "G5": "agentic_wrapper.md",
}
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
PUBLIC_MATERIALIZED_ARTIFACTS = (
    "TASK_INDEX.json",
    "prompt_modes/modes.json",
    "prompt_modes/manifest.json",
)
RELEASE_SEAL_ARTIFACTS = (
    "MANIFEST.json",
    *PUBLIC_MATERIALIZED_ARTIFACTS,
)
STANDALONE_EVALUATOR_COMMON = (
    "task_record.json",
    "family_spec.json",
    "checker_profile.json",
    "harness_spec.json",
    "score_tb.scs",
)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def iter_prompt_public_inputs(task_dir: Path, form: str, mode: str) -> list[Path]:
    public_inputs = [task_dir / "instruction.md"]
    if form == "testbench":
        public_inputs.extend(sorted((task_dir / "supplied_dut").rglob("*.va")))
    elif form == "bugfix":
        public_inputs.extend(sorted((task_dir / "buggy_bundle").rglob("*.va")))
    return public_inputs


def tree_sha(path: Path) -> str:
    digest = hashlib.sha256()
    for item in sorted(path.rglob("*")):
        if item.is_file():
            digest.update(item.relative_to(path).as_posix().encode("utf-8"))
            digest.update(b"\0")
            digest.update(item.read_bytes())
            digest.update(b"\0")
    return digest.hexdigest()


def tree_sha_skipping(path: Path, *, excluded_names: set[str]) -> str:
    digest = hashlib.sha256()
    for item in sorted(path.rglob("*")):
        if item.is_file() and item.name not in excluded_names:
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


def prompt_component_path(release: Path, component_id: str) -> Path:
    if component_id.endswith("_wrapper.md"):
        subdir = "wrappers"
    elif component_id in set(FORM_SKILLS.values()):
        subdir = "form_skills"
    elif component_id in set(FEEDBACK_GUIDES.values()):
        subdir = "feedback_guides"
    else:
        raise SystemExit(f"unknown prompt component: {component_id}")
    return release / "prompt_modes" / subdir / component_id


def audit_standalone_evaluator(
    evaluator_task_dir: Path,
    source_task: Path,
    form: str,
    prefix: str,
    problems: list[str],
) -> Path | None:
    evaluator = evaluator_task_dir / "evaluator"
    source_eval = source_task / "evaluator"
    if not evaluator.is_dir():
        problems.append(f"{prefix} evaluator directory missing")
        return None
    for name in STANDALONE_EVALUATOR_COMMON:
        local = evaluator / name
        source = source_eval / name
        if not local.is_file():
            problems.append(f"{prefix} standalone evaluator missing {name}")
        elif not source.is_file() or file_sha(local) != file_sha(source):
            problems.append(f"{prefix} standalone evaluator {name} differs from canonical source")
    for directory in ("profiles", "solution"):
        local = evaluator / directory
        source = source_eval / directory
        if not local.is_dir():
            problems.append(f"{prefix} standalone evaluator missing {directory}/")
        elif tree_sha(local) != tree_sha(source):
            problems.append(f"{prefix} standalone evaluator {directory}/ differs from canonical source")
    if form == "testbench":
        for name in ("mutation_catalog.json",):
            local = evaluator / name
            source = source_eval / name
            if not local.is_file():
                problems.append(f"{prefix} standalone testbench evaluator missing {name}")
            elif not source.is_file() or file_sha(local) != file_sha(source):
                problems.append(f"{prefix} standalone testbench evaluator {name} differs from canonical source")
        local_mutations = evaluator / "mutation_bundles"
        source_mutations = source_eval / "mutation_bundles"
        if not local_mutations.is_dir():
            problems.append(f"{prefix} standalone testbench evaluator missing mutation_bundles/")
        elif tree_sha(local_mutations) != tree_sha_skipping(source_mutations, excluded_names={"certification.json"}):
            problems.append(f"{prefix} standalone testbench evaluator mutation_bundles/ scoring files differ from canonical source")
        if list(local_mutations.rglob("certification.json")):
            problems.append(f"{prefix} standalone testbench evaluator should not copy negative certification files")
    return evaluator


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
        "schema_version": "v4-benchmarkv4-release-seal-v1",
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
    private_evaluator: Path,
    source: Path,
    source_manifest_sha: str,
    source_rows: dict[str, dict[str, Any]],
    row: dict[str, Any],
    problems: list[str],
) -> None:
    task_dir = release / str(row.get("task_dir") or "")
    evaluator_task_dir = private_evaluator / str(row.get("task_dir") or "")
    task_id = str(row.get("task_id") or "")
    form = str(row.get("form") or "")
    family = str(row.get("family_id") or "")
    prefix = f"{task_id or task_dir.name}:"
    if not task_dir.is_dir():
        problems.append(f"{prefix} task directory missing")
        return
    if (task_dir / "evaluator").exists():
        problems.append(f"{prefix} public task directory contains private evaluator/")
    for required in ("TASK_RECORD.json", "instruction.md", "public_contract.json"):
        if not (task_dir / required).is_file():
            problems.append(f"{prefix} missing {required}")
    if (task_dir / "direct_public_contract.json").exists():
        problems.append(f"{prefix} direct_public_contract.json should not be present")
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
    instruction_text = (task_dir / "instruction.md").read_text(encoding="utf-8")
    for marker in ("test_visible", "Public visible tests", "hidden evaluator", "Vela"):
        if marker in instruction_text:
            problems.append(f"{prefix} instruction leaks run/evaluator marker {marker!r}")
    if form != "testbench" and "visible testbench" in instruction_text.lower():
        problems.append(f"{prefix} non-testbench instruction leaks visible testbench wording")
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
    evaluator = audit_standalone_evaluator(evaluator_task_dir, source_task, form, prefix, problems)
    if evaluator is None:
        return
    if form == "dut":
        if record.get("candidate_artifacts") != artifact_paths:
            problems.append(f"{prefix} DUT candidate artifacts differ from family spec")
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
        if gold_reference.get("materialized_solution") != "evaluator/solution":
            problems.append(f"{prefix} gold repair reference does not point to the materialized solution")
        if gold_reference.get("solution_tree_sha256") != tree_sha(evaluator / "solution"):
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


def audit_prompt_components(
    release: Path,
    tasks: list[dict[str, Any]],
    problems: list[str],
) -> int:
    if (release / "prompt_modes" / "PROMPT_RECORDS.jsonl").exists():
        problems.append("public release should not include prompt_modes/PROMPT_RECORDS.jsonl")
    component_manifest = read_json(release / "prompt_modes" / "manifest.json")
    mode_manifest = read_json(release / "prompt_modes" / "modes.json")
    wrapper_records = component_manifest.get("wrappers") or {}
    form_skill_records = component_manifest.get("form_skills") or {}
    feedback_guide_records = component_manifest.get("feedback_guides") or {}
    component_records = component_manifest.get("components") or {
        **wrapper_records,
        **form_skill_records,
        **feedback_guide_records,
    }
    tokenizer = component_manifest.get("reference_tokenizer") or {}
    tokenizer_key = f"{tokenizer.get('id')}@{tokenizer.get('version')}"
    required_wrappers = set(WRAPPERS_BY_MODE.values())
    required_form_skills = set(FORM_SKILLS.values())
    required_feedback_guides = set(FEEDBACK_GUIDES.values())
    if set(wrapper_records) != required_wrappers:
        problems.append("component manifest wrapper set mismatch")
    if set(form_skill_records) != required_form_skills:
        problems.append("component manifest form-skill set mismatch")
    if set(feedback_guide_records) != required_feedback_guides:
        problems.append("component manifest feedback-guide set mismatch")
    if set(component_records) != required_wrappers | required_form_skills | required_feedback_guides:
        problems.append("component manifest component set mismatch")
    if (release / "prompt_modes" / "skills" / "manifest.json").exists():
        problems.append("legacy prompt_modes/skills/manifest.json should not be present")
    if (release / "prompt_modes" / "skills").exists():
        problems.append("legacy prompt_modes/skills/ directory should not be present")
    for name, component in component_records.items():
        for field in ("stable_id", "semantic_version", "applicable_forms", "sha256", "bytes", "license", "provenance", "token_counts"):
            if field not in component:
                problems.append(f"component manifest {name}: missing {field}")
        if tokenizer_key not in (component.get("token_counts") or {}):
            problems.append(f"component manifest {name}: missing reference-tokenizer count")
        expected_path = prompt_component_path(release, name)
        if component.get("path") != expected_path.relative_to(release).as_posix():
            problems.append(f"component manifest {name}: path does not match component kind")
    mode_records = mode_manifest.get("modes") or {}
    if set(mode_records) != set(MODES):
        problems.append("prompt mode registry does not define exactly G0-G5")
    count = 0
    for task in tasks:
        task_id = str(task.get("task_id") or "")
        form = str(task.get("form") or "")
        task_dir = release / str(task.get("task_dir") or "")
        for mode in MODES:
            count += 1
            policy = mode_records.get(mode) or {}
            expected_cli = mode in AGENTIC_MODES
            if bool(policy.get("feedback_cli")) is not expected_cli:
                problems.append(f"{task_id}/{mode}: feedback availability mismatch")
            public_inputs = iter_prompt_public_inputs(task_dir, form, mode)
            for item in public_inputs:
                if not item.is_file():
                    problems.append(f"{task_id}/{mode}: prompt public input missing: {item.relative_to(task_dir)}")
            expected_components: list[str] = []
            if mode in {"G1", "G3", "G5"}:
                expected_components.append(FORM_SKILLS.get(form, ""))
            if mode in {"G4", "G5"}:
                expected_components.append(FEEDBACK_GUIDES.get(form, ""))
            expected_components.append(WRAPPERS_BY_MODE.get(mode, ""))
            for name in expected_components:
                component = component_records.get(name) or {}
                if component.get("sha256") != file_sha(prompt_component_path(release, name)):
                    problems.append(f"{task_id}/{mode}: prompt component hash mismatch for {name}")
            if mode in DIRECT_MODES:
                public_component_paths = {
                    "instruction" if item.name == "instruction.md" else f"public_input:{item.relative_to(task_dir).as_posix()}": item
                    for item in public_inputs
                }
                direct_text_parts: list[str] = []
                for component_id in ["instruction", *expected_components]:
                    actual_path = public_component_paths.get(component_id)
                    if actual_path is None and component_id in component_records:
                        actual_path = prompt_component_path(release, component_id)
                    if actual_path is not None and actual_path.is_file():
                        direct_text_parts.append(actual_path.read_text(encoding="utf-8", errors="replace"))
                direct_text = "\n".join(direct_text_parts)
                for marker in (
                    "Feedback tools",
                    "feedback CLI",
                    "vabench feedback",
                    "private Spectre",
                    "public/submission",
                    "agentic mode",
                    "mounted public task inputs",
                ):
                    if marker.lower() in direct_text.lower():
                        problems.append(f"{task_id}/{mode}: direct prompt leaks {marker!r}")
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release", type=Path, default=DEFAULT_RELEASE)
    parser.add_argument("--private-evaluator", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--seal-output", type=Path)
    args = parser.parse_args()
    release = args.release.expanduser().resolve()
    private_evaluator = (
        args.private_evaluator.expanduser().resolve()
        if args.private_evaluator is not None
        else release / DEFAULT_PRIVATE_SUBDIR
    )
    manifest = read_json(release / "MANIFEST.json")
    tasks = read_json(release / "TASK_INDEX.json").get("tasks") or []
    source = PACKAGE_ROOT / str(manifest.get("source_release") or "")
    problems: list[str] = []
    if not private_evaluator.is_dir():
        problems.append(f"private evaluator mirror missing: {private_evaluator}")
    else:
        private_manifest = private_evaluator / "MANIFEST.json"
        if not private_manifest.is_file():
            problems.append("private evaluator manifest missing")
        else:
            private_payload = read_json(private_manifest)
            if private_payload.get("public_release") != rel(release, PACKAGE_ROOT):
                problems.append("private evaluator manifest public_release mismatch")
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
        for relative in PUBLIC_MATERIALIZED_ARTIFACTS
        if (release / relative).is_file()
    }
    if set(expected_materialized_hashes) != set(PUBLIC_MATERIALIZED_ARTIFACTS):
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
        audit_task(release, private_evaluator, source, source_manifest_sha, source_rows, row, problems)
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
            read_json(private_evaluator / testbench_dir.relative_to(release) / "evaluator" / "derivation_manifest.json").get("negative_assignment") or {}
        ).get("bugfix_seed")
        bugfix_seed = (
            read_json(private_evaluator / bugfix_dir.relative_to(release) / "evaluator" / "derivation_manifest.json").get("negative_assignment") or {}
        ).get("bugfix_seed")
        if testbench_seed != bugfix_seed:
            problems.append(
                f"{family}: cross-form Bugfix seed mismatch: testbench={testbench_seed} bugfix={bugfix_seed}"
            )
    prompt_count = audit_prompt_components(release, tasks, problems)
    if prompt_count != 7200:
        problems.append(f"prompt record count is {prompt_count}, expected 7200")
    report = {
        "schema_version": "v4-benchmarkv4-release-audit-v1",
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
