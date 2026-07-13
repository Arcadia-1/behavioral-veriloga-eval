#!/usr/bin/env python3
"""Audit the materialized 1,200-task tri-form release."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


PACKAGE_ROOT = Path(__file__).resolve().parents[2]
RUNNERS_ROOT = PACKAGE_ROOT / "runners"
if str(RUNNERS_ROOT) not in sys.path:
    sys.path.insert(0, str(RUNNERS_ROOT))
from testbench_security import validate_testbench  # noqa: E402
from materialize_tri_form_release import (  # noqa: E402
    canonical_mutation_certificate_mismatches,
    gold_reference_certificate_state,
    mutation_reference_identity,
    reference_replay_mismatches,
)
DEFAULT_RELEASE = PACKAGE_ROOT / "release" / "tri-form-v4-1200-final"
FORMS = ("dut", "testbench", "bugfix")
MODES = ("G0", "G1", "G2", "G3", "G4", "G5")
FORM_SKILLS = {
    "dut": "dut_modeling.md",
    "testbench": "testbench_verification.md",
    "bugfix": "bugfix_diagnosis.md",
}
FEEDBACK_ADAPTERS = {
    "dut": "feedback_dut.md",
    "testbench": "feedback_testbench.md",
    "bugfix": "feedback_bugfix.md",
}
MATERIALIZED_ARTIFACTS = (
    "TASK_INDEX.json",
    "BUGFIX_SEED_REVIEW.json",
    "REFERENCE_REPLAY_PLAN.json",
    "REFERENCE_REPLAY_EVIDENCE.json",
    "prompt_modes/PROMPT_RECORDS.jsonl",
    "prompt_modes/modes.json",
    "prompt_modes/skills/manifest.json",
)
RELEASE_SEAL_ARTIFACTS = (
    "MANIFEST.json",
    *MATERIALIZED_ARTIFACTS,
    "AUDIT_REPORT.json",
    "RUNTIME_INGESTION_EVIDENCE.json",
)
PRIVATE_PUBLIC_CONTRACT_KEYS = {
    "testbench_binding",
    "dut_source_root",
    "source_path_template",
    "source_checker_profile",
    "checker_id",
    "checker_source",
    "mutation_catalog",
    "private_deck",
    "private_window",
}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def reference_saved_signals(path: Path) -> list[str]:
    saved: list[str] = []
    pending = ""
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("//", 1)[0].strip()
        if not line:
            continue
        if pending:
            pending = f"{pending} {line}".strip()
        elif re.match(r"^save\b", line, re.IGNORECASE):
            pending = line
        if pending and not pending.endswith("\\"):
            body = re.sub(r"^save\s+", "", pending, flags=re.IGNORECASE)
            for token in re.split(r"[\s,]+", body.strip()):
                if token and token.lower() != "time" and token not in saved:
                    saved.append(token)
            pending = ""
        elif pending:
            pending = pending[:-1].rstrip()
    return ["time", *saved]


def property_semantics(properties: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {key: value for key, value in prop.items() if key != "required_signals"}
        for prop in properties
    ]


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def replay_record_sha(record: dict[str, Any]) -> str:
    return canonical_sha({key: value for key, value in record.items() if key != "record_sha256"})


def expected_reference_replay_plan(
    reference_certificates: list[tuple[str, dict[str, Any]]],
) -> set[tuple[str, str, str, str]]:
    return {
        (
            family,
            str(mutation_id),
            str(case.get("replay_profile") or ""),
            str(case.get("reference_deck_sha256") or ""),
        )
        for family, certificate in reference_certificates
        for mutation_id, case in (certificate.get("negative_cases") or {}).items()
        if case.get("source_hash_reusable") is not True
    }


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


def nested_keys(value: Any) -> set[str]:
    if isinstance(value, dict):
        keys = set(value)
        for item in value.values():
            keys.update(nested_keys(item))
        return keys
    if isinstance(value, list):
        keys: set[str] = set()
        for item in value:
            keys.update(nested_keys(item))
        return keys
    return set()


def buggy_source_leak_markers(path: Path) -> list[str]:
    """Return only explicit evaluator metadata markers found in public Bugfix sources."""
    patterns = {
        "mutation_id": re.compile(r"\bmutation_id\b", re.IGNORECASE),
        "negative_variants": re.compile(r"\bnegative_variants\b", re.IGNORECASE),
        "negative_id": re.compile(r"\bneg_\d{3}(?:\b|_)", re.IGNORECASE),
        "checker_id": re.compile(r"\bchecker_id\b", re.IGNORECASE),
        "violated_property_ids": re.compile(r"\bviolated_property_ids\b", re.IGNORECASE),
        "bugfix_seed": re.compile(r"\bbugfix_seed\b", re.IGNORECASE),
        "gold_implementation": re.compile(r"\bgold implementation\b", re.IGNORECASE),
        "root_cause_label": re.compile(r"\broot cause\s*:", re.IGNORECASE),
    }
    text = "\n".join(
        source.read_text(encoding="utf-8", errors="replace")
        for source in sorted(path.rglob("*.va"))
    )
    return sorted(name for name, pattern in patterns.items() if pattern.search(text))


def expected_solver_contract(public_contract: dict[str, Any]) -> dict[str, Any]:
    form = str(public_contract["form"])
    properties = json.loads(json.dumps(public_contract["properties"]))
    trace_contract = public_contract["trace_contract"]
    if form != "testbench":
        for prop in properties:
            prop.pop("required_signals", None)
        entry_ports: list[str] = []
        for file_record in (public_contract.get("artifact_contract") or {}).get("files") or []:
            for module in file_record.get("modules") or []:
                if module.get("role") != "entry":
                    continue
                for port in sorted(module.get("ports") or [], key=lambda item: int(item.get("position", 0))):
                    name = str(port["name"])
                    if name not in entry_ports:
                        entry_ports.append(name)
        trace_contract = {"required_signals": ["time", *entry_ports]}
    projection = {
        "schema_version": "v4-solver-contract-v1",
        "task_id": public_contract["task_id"],
        "family_id": public_contract["family_id"],
        "form": form,
        "title": (public_contract.get("identity") or {}).get("title"),
        "target_artifacts": public_contract["target_artifacts"],
        "submission_contract": public_contract["submission_contract"],
        "artifact_contract": public_contract["artifact_contract"],
        "properties": properties,
        "trace_contract": trace_contract,
        "modeling_constraints": public_contract.get("modeling_constraints") or [],
    }
    for key in (
        "supplied_inputs",
        "evaluation_summary",
        "security_policy",
        "buggy_input_artifacts",
        "editable_scope",
        "problem_statement",
    ):
        if key in public_contract:
            projection[key] = public_contract[key]
    return projection


def expected_supplied_inputs(spec: dict[str, Any]) -> dict[str, Any]:
    binding = spec.get("testbench_binding") or {}
    template = str(binding.get("source_path_template") or "./dut/{artifact_path}")
    artifacts = []
    for file_record in (spec.get("artifact_contract") or {}).get("files") or []:
        artifact_path = str(file_record["path"])
        artifacts.append({
            "public_input_path": f"supplied_dut/{artifact_path}",
            "testbench_include_path": template.format(artifact_path=artifact_path),
        })
    return {
        "read_only_dut_artifacts": artifacts,
        "dut_instances": binding.get("instances") or [],
    }


def build_release_seal(release: Path, source_manifest_sha256: str) -> dict[str, Any]:
    artifact_hashes = {}
    for relative in RELEASE_SEAL_ARTIFACTS:
        path = release / relative
        if not path.is_file():
            raise SystemExit(f"cannot seal release; missing artifact: {relative}")
        artifact_hashes[relative] = file_sha(path)
    return {
        "schema_version": "v4-tri-form-release-seal-v1",
        "release_status": "package_structure_sealed",
        "source_score_denominator_manifest_sha256": source_manifest_sha256,
        "artifact_sha256": artifact_hashes,
        "simulation_claim": "not established by this static seal",
    }


def expected_task_id(form: str, family: str) -> str:
    offsets = {"dut": 0, "testbench": 500, "bugfix": 1000}
    value = offsets[form] + int(family)
    width = 3 if value < 1000 else 4
    return f"v4-{value:0{width}d}"


def audit_task(
    release: Path,
    source: Path,
    row: dict[str, Any],
    problems: list[str],
    replay_records: dict[str, dict[str, Any]] | None = None,
    source_reference: str | None = None,
) -> None:
    task_dir = release / str(row.get("task_dir") or "")
    task_id = str(row.get("task_id") or "")
    form = str(row.get("form") or "")
    family = str(row.get("family_id") or "")
    prefix = f"{task_id or task_dir.name}:"
    if not task_dir.is_dir():
        problems.append(f"{prefix} task directory missing")
        return
    required_paths = {
        required: task_dir / required
        for required in ("TASK_RECORD.json", "instruction.md", "public_contract.json", "solver_contract.json")
    }
    for required, path in required_paths.items():
        if not path.is_file():
            problems.append(f"{prefix} missing {required}")
    if any(
        not required_paths[required].is_file()
        for required in ("TASK_RECORD.json", "public_contract.json", "solver_contract.json")
    ):
        return
    record = read_json(task_dir / "TASK_RECORD.json")
    contract = read_json(task_dir / "public_contract.json")
    solver_contract = read_json(task_dir / "solver_contract.json")
    if task_id != expected_task_id(form, family):
        problems.append(f"{prefix} ID does not match form/family numbering")
    if record.get("task_id") != task_id or record.get("form") != form or record.get("family_id") != family:
        problems.append(f"{prefix} task record identity mismatch")
    if contract.get("task_id") != task_id or contract.get("form") != form or str(contract.get("family_id")) != family:
        problems.append(f"{prefix} public contract identity mismatch")
    if solver_contract != expected_solver_contract(contract):
        problems.append(f"{prefix} solver contract is not the deterministic public-contract projection")
    leaked_solver = sorted(nested_keys(solver_contract) & PRIVATE_PUBLIC_CONTRACT_KEYS)
    if leaked_solver:
        problems.append(f"{prefix} solver contract leaks private evaluator keys: {', '.join(leaked_solver)}")
    if form != "testbench":
        if any("required_signals" in prop for prop in solver_contract.get("properties") or []):
            problems.append(f"{prefix} solver properties expose evaluator trace bindings")
        entry_ports = {
            str(port["name"])
            for file_record in (solver_contract.get("artifact_contract") or {}).get("files") or []
            for module in file_record.get("modules") or []
            if module.get("role") == "entry"
            for port in module.get("ports") or []
        }
        solver_traces = set((solver_contract.get("trace_contract") or {}).get("required_signals") or [])
        if not solver_traces <= entry_ports | {"time"}:
            problems.append(f"{prefix} solver trace contract exposes evaluator-only aliases")
    if record.get("public_bundle_sha256") != public_bundle_hash(task_dir):
        problems.append(f"{prefix} public bundle hash mismatch")
    recorded_source = Path(str(record.get("canonical_dut_source") or ""))
    if (
        recorded_source.is_absolute()
        or not recorded_source.parts
        or ".." in recorded_source.parts
        or str(recorded_source) in {"", "."}
    ):
        problems.append(f"{prefix} canonical DUT source path is unsafe")
        return
    if source_reference is not None:
        expected_source = Path(source_reference) / recorded_source.name
        if recorded_source != expected_source:
            problems.append(f"{prefix} canonical DUT source path differs from release manifest")
            return
    source_task = source / recorded_source.name
    if not recorded_source.name or not source_task.is_dir() or source not in source_task.parents:
        problems.append(f"{prefix} canonical DUT source is invalid")
        return
    spec_path = source_task / "evaluator" / "family_spec.json"
    if not spec_path.is_file() or record.get("family_spec_sha256") != file_sha(spec_path):
        problems.append(f"{prefix} family spec hash mismatch")
        return
    spec = read_json(spec_path)
    artifact_paths = [str(item["path"]) for item in spec["artifact_contract"]["files"]]
    if contract.get("schema_version") != "v4-tri-form-public-contract-v2":
        problems.append(f"{prefix} public contract schema is not v2")
    leaked = sorted(nested_keys(contract) & PRIVATE_PUBLIC_CONTRACT_KEYS)
    if leaked:
        problems.append(f"{prefix} public contract leaks private evaluator keys: {', '.join(leaked)}")
    for field in ("identity", "artifact_contract", "modeling_constraints"):
        if contract.get(field) != spec.get(field, [] if field == "modeling_constraints" else None):
            problems.append(f"{prefix} public observable contract differs at {field}")
    if property_semantics(contract.get("properties") or []) != property_semantics(spec.get("properties") or []):
        problems.append(f"{prefix} public observable contract differs at properties")
    if form != "testbench":
        if contract.get("properties") != spec.get("properties"):
            problems.append(f"{prefix} public property trace contract differs")
        if contract.get("trace_contract") != spec.get("trace_contract"):
            problems.append(f"{prefix} public observable contract differs at trace_contract")
    if contract.get("submission_contract") != {
        "target_artifacts_relative_to": "submission_root",
        "agentic_submission_root": "public/submission",
        "exact_declared_file_set_required": True,
    }:
        problems.append(f"{prefix} submission-root contract mismatch")
    if form == "dut":
        if record.get("candidate_artifacts") != artifact_paths or contract.get("target_artifacts") != artifact_paths:
            problems.append(f"{prefix} DUT candidate artifacts differ from family spec")
        if "supplied_inputs" in contract:
            problems.append(f"{prefix} DUT public contract contains Testbench-only supplied inputs")
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
    if assignment.get("bugfix_seed") not in suite:
        problems.append(f"{prefix} bugfix seed is not a member of the testbench suite")
    if derivation.get("base_dut", {}).get("family_spec_sha256") != file_sha(spec_path):
        problems.append(f"{prefix} derivation family hash mismatch")
    if form == "testbench":
        if record.get("candidate_artifacts") != ["testbench.scs"] or contract.get("target_artifacts") != ["testbench.scs"]:
            problems.append(f"{prefix} testbench output is not exactly testbench.scs")
        supplied_inputs = contract.get("supplied_inputs") or {}
        expected_dut_paths = {f"supplied_dut/{path}" for path in artifact_paths}
        actual_dut_paths = {
            str(item.get("public_input_path") or "")
            for item in supplied_inputs.get("read_only_dut_artifacts") or []
        }
        if actual_dut_paths != expected_dut_paths:
            problems.append(f"{prefix} public supplied-DUT artifact projection mismatch")
        expected_modules = {
            str(item.get("module_ref") or "")
            for item in (spec.get("testbench_binding") or {}).get("instances") or []
        }
        actual_modules = {
            str(item.get("module_ref") or "")
            for item in supplied_inputs.get("dut_instances") or []
        }
        if actual_modules != expected_modules:
            problems.append(f"{prefix} public supplied-DUT module projection mismatch")
        score = read_json(evaluator / "score_policy.json")
        if score.get("candidate_artifacts") != ["testbench.scs"] or score.get("kill_ratio_denominator") != 5:
            problems.append(f"{prefix} testbench score policy mismatch")
        supplied = task_dir / "supplied_dut"
        if tree_sha(supplied) != tree_sha(source_task / "evaluator" / "solution"):
            problems.append(f"{prefix} supplied DUT differs from canonical gold")
        reference = read_json(evaluator / "reference_certificate.json")
        if reference.get("schema_version") != "v4-reference-testbench-certificate-v2":
            problems.append(f"{prefix} reference certificate schema mismatch")
        if reference.get("reference_tb_sha256") != file_sha(evaluator / "reference_tb.scs"):
            problems.append(f"{prefix} reference certificate deck hash mismatch")
        gold_state = gold_reference_certificate_state(
            source_task,
            evaluator / "reference_tb.scs",
        )
        if reference.get("gold_source_certification_sha256") != file_sha(gold_state["path"]):
            problems.append(f"{prefix} gold source certification hash mismatch")
        if reference.get("reference_profile_candidates") != gold_state["matching_profiles"]:
            problems.append(f"{prefix} reference profile candidates differ from current source")
        if reference.get("gold_fingerprint_mismatches") != gold_state["mismatches"]:
            problems.append(f"{prefix} gold fingerprint mismatch list differs from current source")
        expected_gold_status = "pass" if gold_state["reusable"] else "canonical_deck_replay_pending"
        if reference.get("correct_dut_status") != expected_gold_status:
            problems.append(f"{prefix} correct-DUT reference status differs from current source")
        negative_cases = reference.get("negative_cases") or {}
        if set(negative_cases) != set(suite):
            problems.append(f"{prefix} reference certificate negative suite mismatch")
        pending = sorted(
            mutation_id
            for mutation_id, case in negative_cases.items()
            if case.get("status") != "killed_behaviorally"
        )
        if reference.get("pending_mutation_ids") != pending:
            problems.append(f"{prefix} reference certificate pending list mismatch")
        source_reused = sum(
            case.get("evidence_source") == "canonical_mutation_certification"
            for case in negative_cases.values()
        )
        supplemental_reused = sum(
            case.get("evidence_source") == "supplemental_reference_deck_replay"
            for case in negative_cases.values()
        )
        if reference.get("source_reused_negative_count") != source_reused:
            problems.append(f"{prefix} source-reused negative count mismatch")
        if reference.get("supplemental_reused_negative_count") != supplemental_reused:
            problems.append(f"{prefix} supplemental-reused negative count mismatch")
        for mutation_id, case in negative_cases.items():
            evidence_source = case.get("evidence_source")
            source_certification = (
                source_task
                / "evaluator"
                / "mutation_bundles"
                / mutation_id
                / "certification.json"
            )
            if not source_certification.is_file():
                problems.append(f"{prefix} {mutation_id} source certification is missing")
                continue
            if case.get("source_certification_sha256") != file_sha(source_certification):
                problems.append(f"{prefix} {mutation_id} source certification hash mismatch")
            current_identity = mutation_reference_identity(
                source_task,
                mutation_id,
                evaluator / "reference_tb.scs",
                str(case.get("replay_profile") or ""),
            )
            source_mismatches = canonical_mutation_certificate_mismatches(
                read_json(source_certification),
                current_identity,
            )
            if case.get("source_fingerprint_mismatches") != source_mismatches:
                problems.append(
                    f"{prefix} {mutation_id} source fingerprint mismatch list differs from current source"
                )
            if evidence_source == "canonical_mutation_certification":
                if (
                    case.get("source_hash_reusable") is not True
                    or source_mismatches
                    or case.get("replay_record_sha256") is not None
                ):
                    problems.append(f"{prefix} {mutation_id} canonical evidence binding mismatch")
            elif evidence_source == "supplemental_reference_deck_replay":
                if case.get("source_hash_reusable") is not False or not source_mismatches:
                    problems.append(f"{prefix} {mutation_id} supplemental evidence precedence mismatch")
                record_sha = str(case.get("replay_record_sha256") or "")
                record = (replay_records or {}).get(record_sha)
                if record is None:
                    problems.append(f"{prefix} {mutation_id} supplemental replay record missing")
                    continue
                if record.get("record_sha256") != replay_record_sha(record):
                    problems.append(f"{prefix} {mutation_id} supplemental replay record hash mismatch")
                if (
                    str(record.get("canonical_id") or "") != family
                    or str(record.get("mutation_id") or "") != mutation_id
                    or str(record.get("profile") or "") != str(case.get("replay_profile") or "")
                ):
                    problems.append(f"{prefix} {mutation_id} supplemental replay identity mismatch")
                replay_mismatches = reference_replay_mismatches(
                    record,
                    current_identity,
                    source_task,
                )
                if replay_mismatches:
                    problems.append(
                        f"{prefix} {mutation_id} supplemental replay binding mismatch: "
                        + ", ".join(replay_mismatches)
                    )
            elif evidence_source != "pending":
                problems.append(f"{prefix} {mutation_id} unknown reference evidence source")
        if reference.get("negative_suite_status") == "five_of_five_killed_behaviorally" and pending:
            problems.append(f"{prefix} reference certificate overclaims five-of-five evidence")
        evidence_rebinding_required = reference.get("correct_dut_status") != "pass" or bool(pending)
        if reference.get("evidence_rebinding_required") is not evidence_rebinding_required:
            problems.append(f"{prefix} reference certificate evidence-rebinding flag mismatch")
        if reference.get("simulation_rerun_required_for_materialization") is not False:
            problems.append(f"{prefix} materialization incorrectly requires a simulation rerun")
        if reference.get("simulation_rerun_requirement_status") != "not_determined_by_materialization":
            problems.append(f"{prefix} reference certificate overstates simulation rerun policy")
        security_policy = read_json(evaluator / "testbench_security_policy.json")
        if contract.get("security_policy") != security_policy:
            problems.append(f"{prefix} public and evaluator security policies differ")
        expected_traces = reference_saved_signals(evaluator / "reference_tb.scs")
        if contract.get("trace_contract") != {"required_signals": expected_traces}:
            problems.append(f"{prefix} testbench trace contract does not match reference saves")
        for prop in contract.get("properties") or []:
            if prop.get("required_signals") != expected_traces:
                problems.append(f"{prefix} property {prop.get('id')} trace contract does not match reference saves")
        security = validate_testbench(evaluator / "reference_tb.scs", contract, security_policy)
        if not security.valid:
            problems.append(f"{prefix} reference testbench fails structural security: {'; '.join(security.diagnostics)}")
        public_text = (task_dir / "instruction.md").read_text(encoding="utf-8") + json.dumps(contract)
        if "neg_" in public_text or "mutation_id" in public_text:
            problems.append(f"{prefix} public testbench view leaks negative identity")
    elif form == "bugfix":
        if record.get("candidate_artifacts") != artifact_paths or contract.get("target_artifacts") != artifact_paths:
            problems.append(f"{prefix} bugfix artifact contract mismatch")
        if "supplied_inputs" in contract:
            problems.append(f"{prefix} Bugfix public contract contains Testbench-only supplied inputs")
        buggy = task_dir / "buggy_bundle"
        buggy_paths = sorted(path.relative_to(buggy).as_posix() for path in buggy.rglob("*.va"))
        if buggy_paths != sorted(artifact_paths):
            problems.append(f"{prefix} buggy bundle file set mismatch")
        if tree_sha(buggy) == tree_sha(source_task / "evaluator" / "solution"):
            problems.append(f"{prefix} buggy bundle is byte-identical to gold")
        public_text = (task_dir / "instruction.md").read_text(encoding="utf-8") + json.dumps(contract)
        forbidden = ("neg_", "faulty file", "root cause", "changed line", "public summary")
        for marker in forbidden:
            if marker.lower() in public_text.lower():
                problems.append(f"{prefix} public bugfix view leaks forbidden marker {marker!r}")
        if re.search(r"\bmutation\b", public_text, re.IGNORECASE):
            problems.append(f"{prefix} public bugfix view leaks forbidden marker 'mutation'")
        source_markers = buggy_source_leak_markers(buggy)
        if source_markers:
            problems.append(
                f"{prefix} buggy source bundle leaks evaluator metadata: {', '.join(source_markers)}"
            )
        selection = derivation.get("selection_evidence") or {}
        if selection.get("selection_status") != "policy_reviewed" or selection.get("triviality_markers"):
            problems.append(f"{prefix} Bugfix seed lacks nontrivial semantic review")
        repair = read_json(evaluator / "repair_certificate.json")
        if repair.get("schema_version") != "v4-bugfix-repair-certificate-v1":
            problems.append(f"{prefix} Bugfix repair certificate schema mismatch")
        if repair.get("buggy_bundle_sha256") != tree_sha(buggy):
            problems.append(f"{prefix} Bugfix repair certificate bundle hash mismatch")
        if repair.get("gold_solution_sha256") != tree_sha(source_task / "evaluator" / "solution"):
            problems.append(f"{prefix} Bugfix repair certificate gold hash mismatch")
        if repair.get("status") == "pass" and (
            repair.get("gold_repair_status") != "pass"
            or repair.get("buggy_seed_status") != "killed_behaviorally"
        ):
            problems.append(f"{prefix} Bugfix repair certificate overclaims pass")
        evidence_rebinding_required = (
            repair.get("gold_repair_status") != "pass"
            or repair.get("buggy_seed_status") != "killed_behaviorally"
        )
        if repair.get("evidence_rebinding_required") is not evidence_rebinding_required:
            problems.append(f"{prefix} Bugfix repair evidence-rebinding flag mismatch")
        if repair.get("simulation_rerun_required_for_materialization") is not False:
            problems.append(f"{prefix} Bugfix materialization incorrectly requires a simulation rerun")
        if repair.get("simulation_rerun_requirement_status") != "not_determined_by_materialization":
            problems.append(f"{prefix} Bugfix repair certificate overstates simulation rerun policy")


def prompt_public_inputs(task_dir: Path, form: str) -> list[Path]:
    paths = [task_dir / "instruction.md", task_dir / "solver_contract.json"]
    if form == "testbench":
        paths.extend(sorted((task_dir / "supplied_dut").rglob("*.va")))
    elif form == "bugfix":
        paths.extend(sorted((task_dir / "buggy_bundle").rglob("*.va")))
    support = task_dir / "public_support"
    if support.is_dir():
        paths.extend(sorted(path for path in support.rglob("*") if path.is_file()))
    return paths


def audit_prompt_records(release: Path, tasks: list[dict[str, Any]], problems: list[str]) -> int:
    path = release / "prompt_modes" / "PROMPT_RECORDS.jsonl"
    if not path.is_file():
        problems.append("prompt record file missing")
        return 0
    seen: dict[str, set[str]] = defaultdict(set)
    base_hashes_by_task: dict[str, set[str]] = defaultdict(set)
    tasks_with_missing_public_inputs: set[str] = set()
    task_forms = {str(row["task_id"]): str(row["form"]) for row in tasks}
    task_dirs = {str(row["task_id"]): release / str(row["task_dir"]) for row in tasks}
    mode_registry = read_json(release / "prompt_modes" / "modes.json")
    if mode_registry.get("composition_order") != [
        "canonical_instruction_and_public_inputs",
        "form_skill",
        "feedback_core_and_form_adapter",
        "neutral_wrapper",
    ]:
        problems.append("prompt mode registry does not place neutral wrapper last")
    if mode_registry.get("transport_normalization") != {
        "semantics_blind": True,
        "direct": "last_complete_labeled_bundle_v1",
        "agentic": "unique_common_submission_prefix_v1",
        "protocol_compliance_reported_separately": True,
    }:
        problems.append("prompt mode transport-normalization registry mismatch")
    skill_manifest = read_json(release / "prompt_modes" / "skills" / "manifest.json")
    skill_records = skill_manifest.get("skills") or {}
    tokenizer = skill_manifest.get("reference_tokenizer") or {}
    tokenizer_key = f"{tokenizer.get('id')}@{tokenizer.get('version')}"
    required_assets = {
        "neutral_wrapper.md", *FORM_SKILLS.values(), "feedback_core.md", *FEEDBACK_ADAPTERS.values()
    }
    if set(skill_records) != required_assets:
        problems.append("skill manifest component set mismatch")
    for name, component in skill_records.items():
        for field in ("stable_id", "semantic_version", "applicable_forms", "sha256", "bytes", "license", "provenance", "token_counts"):
            if field not in component:
                problems.append(f"skill manifest {name}: missing {field}")
        if tokenizer_key not in (component.get("token_counts") or {}):
            problems.append(f"skill manifest {name}: missing reference-tokenizer count")
        provenance_type = str((component.get("provenance") or {}).get("type") or "")
        if name in FORM_SKILLS.values() and provenance_type != "derived_from_installed_vendor_help":
            problems.append(f"skill manifest {name}: form skill is not vendor-help derived")
        if name == "neutral_wrapper.md" and provenance_type != "project_authored_experiment_protocol":
            problems.append("skill manifest neutral_wrapper.md: wrapper provenance mismatch")
        if name.startswith("feedback_") and provenance_type != "project_authored_facility_guidance":
            problems.append(f"skill manifest {name}: feedback provenance mismatch")
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
        expected_response_protocol = (
            "v4-workspace-finalizer-with-prefix-normalization-v2"
            if expected_cli
            else "v4-exact-artifact-blocks-with-semantic-blind-normalization-v2"
        )
        if row.get("response_protocol") != expected_response_protocol:
            problems.append(f"{task_id}/{mode}: response protocol mismatch")
        form = task_forms.get(task_id, "")
        task_dir = task_dirs.get(task_id)
        if task_dir is None:
            problems.append(f"{task_id}/{mode}: prompt record has no task directory")
            continue
        if not (task_dir / "instruction.md").is_file() or not (task_dir / "solver_contract.json").is_file():
            # audit_task already reports these once per task. Avoid both a crash
            # and six duplicate mode-level diagnostics for the same missing asset.
            tasks_with_missing_public_inputs.add(task_id)
            continue
        public_inputs = prompt_public_inputs(task_dir, form)
        expected_input_hashes = {
            item.relative_to(task_dir).as_posix(): file_sha(item) for item in public_inputs
        }
        if row.get("canonical_instruction_sha256") != file_sha(task_dir / "instruction.md"):
            problems.append(f"{task_id}/{mode}: canonical instruction hash mismatch")
        if row.get("solver_contract_sha256") != file_sha(task_dir / "solver_contract.json"):
            problems.append(f"{task_id}/{mode}: solver contract hash mismatch")
        if row.get("base_public_input_hashes") != expected_input_hashes:
            problems.append(f"{task_id}/{mode}: base public input hash mismatch")
        if row.get("public_input_hashes") != expected_input_hashes:
            problems.append(f"{task_id}/{mode}: public input hash replay mismatch")
        base_hashes_by_task[task_id].add(
            hashlib.sha256(json.dumps(expected_input_hashes, sort_keys=True).encode("utf-8")).hexdigest()
        )
        expected_skills: list[str] = []
        if mode in {"G1", "G3", "G5"}:
            expected_skills.append(FORM_SKILLS.get(form, ""))
        if mode in {"G4", "G5"}:
            expected_skills.extend(["feedback_core.md", FEEDBACK_ADAPTERS.get(form, "")])
        skills = row.get("skill_hashes") or {}
        if set(skills) != set(expected_skills):
            problems.append(f"{task_id}/{mode}: exact skill composition mismatch")
        for name in expected_skills:
            if skills.get(name) != (skill_records.get(name) or {}).get("sha256"):
                problems.append(f"{task_id}/{mode}: skill hash mismatch for {name}")
        component_order = row.get("component_order") or []
        expected_suffix = [*expected_skills, "neutral_wrapper.md"]
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
            if actual_path is None and component_id in skill_records:
                actual_path = release / "prompt_modes" / "skills" / component_id
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
        if task_id not in tasks_with_missing_public_inputs and len(base_hashes_by_task[task_id]) != 1:
            problems.append(f"{task_id}: G0-G5 base public inputs differ")
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release", type=Path, default=DEFAULT_RELEASE)
    parser.add_argument(
        "--source",
        type=Path,
        help="Exact-five source release to audit; defaults to MANIFEST.json source_release.",
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument("--seal-output", type=Path)
    args = parser.parse_args()
    release = args.release.expanduser().resolve()
    manifest = read_json(release / "MANIFEST.json")
    tasks = read_json(release / "TASK_INDEX.json").get("tasks") or []
    source = (
        args.source.expanduser().resolve()
        if args.source is not None
        else PACKAGE_ROOT / str(manifest.get("source_release") or "")
    )
    problems: list[str] = []
    if not source.is_dir():
        problems.append(f"exact-five source release is missing: {source}")
    replay_payload = read_json(release / "REFERENCE_REPLAY_EVIDENCE.json")
    replay_rows = replay_payload.get("rows") or []
    replay_summary = replay_payload.get("summary") or {}
    raw_status_counts = Counter(str(row.get("status") or "") for row in replay_rows)
    expected_replay_summary = {
        "row_count": len(replay_rows),
        "behaviorally_certified_row_count": len(replay_rows),
        "diagnostic_only_nonpass_count": sum(
            row.get("status") != "PASS" for row in replay_rows
        ),
        "raw_status_counts": dict(sorted(raw_status_counts.items())),
        "family_count": len({str(row.get("canonical_id") or "") for row in replay_rows}),
        "profile_counts": {
            profile: sum(row.get("profile") == profile for row in replay_rows)
            for profile in ("feedback", "score")
        },
    }
    if replay_summary != expected_replay_summary:
        problems.append("reference replay evidence summary mismatch")
    replay_records: dict[str, dict[str, Any]] = {}
    for record in replay_rows:
        if not isinstance(record, dict):
            problems.append("reference replay evidence contains a non-object row")
            continue
        record_sha = str(record.get("record_sha256") or "")
        if not record_sha or record_sha != replay_record_sha(record):
            problems.append("reference replay evidence contains a row hash mismatch")
            continue
        if record_sha in replay_records:
            problems.append(f"duplicate reference replay record hash: {record_sha}")
            continue
        replay_records[record_sha] = record
    replay_plan = read_json(release / "REFERENCE_REPLAY_PLAN.json")
    replay_plan_rows = replay_plan.get("mutations") or []
    expected_materialized_hashes = {
        relative: file_sha(release / relative)
        for relative in MATERIALIZED_ARTIFACTS
        if (release / relative).is_file()
    }
    if set(expected_materialized_hashes) != set(MATERIALIZED_ARTIFACTS):
        problems.append("one or more materialized release artifacts are missing")
    if manifest.get("materialized_artifact_sha256") != expected_materialized_hashes:
        problems.append("materialized artifact hash binding mismatch")
    if manifest.get("simulation_rerun_count_for_materialization") != 0:
        problems.append("materialization must not classify evidence rebinding as simulator reruns")
    if manifest.get("simulation_rerun_requirement_status") != "not_determined_by_materialization":
        problems.append("manifest overstates simulation rerun requirements")
    if manifest.get("evidence_rebinding_required_case_count") != manifest.get(
        "reference_testbench_pending_case_count"
    ):
        problems.append("manifest evidence-rebinding count differs from pending reference cases")
    counts = Counter(str(row.get("form") or "") for row in tasks)
    if len(tasks) != 1200 or counts != Counter({form: 400 for form in FORMS}):
        problems.append(f"task counts mismatch: total={len(tasks)} forms={dict(counts)}")
    family_forms: dict[str, set[str]] = defaultdict(set)
    for row in tasks:
        family_forms[str(row.get("family_id") or "")].add(str(row.get("form") or ""))
        audit_task(
            release,
            source,
            row,
            problems,
            replay_records,
            source_reference=str(manifest.get("source_release") or ""),
        )
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
        testbench_derivation = read_json(testbench_dir / "evaluator" / "derivation_manifest.json")
        bugfix_derivation = read_json(bugfix_dir / "evaluator" / "derivation_manifest.json")
        testbench_seed = (testbench_derivation.get("negative_assignment") or {}).get("bugfix_seed")
        bugfix_seed = (bugfix_derivation.get("negative_assignment") or {}).get("bugfix_seed")
        if testbench_seed != bugfix_seed:
            problems.append(
                f"{family}: cross-form Bugfix seed mismatch: testbench={testbench_seed} bugfix={bugfix_seed}"
            )
    prompt_count = audit_prompt_records(release, tasks, problems)
    if prompt_count != 7200:
        problems.append(f"prompt record count is {prompt_count}, expected 7200")
    reference_certificates = [
        (
            str(row.get("family_id") or ""),
            read_json(release / str(row["task_dir"]) / "evaluator" / "reference_certificate.json"),
        )
        for row in tasks
        if row.get("form") == "testbench"
    ]
    pending_reference_cases = sum(
        int(certificate.get("pending_negative_count") or 0)
        + int(certificate.get("correct_dut_status") != "pass")
        for _family, certificate in reference_certificates
    )
    certified_reference_families = sum(
        certificate.get("negative_suite_status") == "five_of_five_killed_behaviorally"
        and certificate.get("correct_dut_status") == "pass"
        for _family, certificate in reference_certificates
    )
    expected_status = (
        "package_materialized_behavior_evidence_ready"
        if pending_reference_cases == 0 and certified_reference_families == 400
        else "package_materialized_behavior_evidence_pending"
    )
    if manifest.get("release_status") != expected_status:
        problems.append("manifest release status differs from reference evidence readiness")
    if manifest.get("reference_testbench_pending_case_count") != pending_reference_cases:
        problems.append("manifest pending reference-case count mismatch")
    if manifest.get("reference_testbench_certified_family_count") != certified_reference_families:
        problems.append("manifest certified reference-family count mismatch")
    if manifest.get("reference_replay_plan_case_count") != len(replay_plan_rows):
        problems.append("manifest reference replay plan count mismatch")
    if manifest.get("reference_replay_evidence_case_count") != len(replay_rows):
        problems.append("manifest reference replay evidence count mismatch")
    expected_replay_plan = expected_reference_replay_plan(reference_certificates)
    actual_replay_plan = {
        (
            str(item.get("canonical_id") or ""),
            str(item.get("mutation_id") or ""),
            str(item.get("profile") or ""),
            str(item.get("reference_deck_sha256") or ""),
        )
        for item in replay_plan_rows
        if isinstance(item, dict)
    }
    if actual_replay_plan != expected_replay_plan or len(actual_replay_plan) != len(replay_plan_rows):
        problems.append("reference replay plan does not exactly match source-unbound Testbench cases")
    bound_replay_hashes = {
        str(case.get("replay_record_sha256") or "")
        for _family, certificate in reference_certificates
        for case in (certificate.get("negative_cases") or {}).values()
        if case.get("evidence_source") == "supplemental_reference_deck_replay"
    }
    if bound_replay_hashes != set(replay_records):
        problems.append("reference replay evidence rows do not exactly match bound Testbench cases")
    report = {
        "schema_version": "v4-tri-form-release-audit-v1",
        "status": "pass" if not problems else "fail",
        "family_count": len(family_forms),
        "task_count": len(tasks),
        "task_counts": dict(sorted(counts.items())),
        "prompt_record_count": prompt_count,
        "input_hashes": {
            "source_score_denominator_manifest_sha256": file_sha(source / "score_denominator_manifest.json"),
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
        seal = build_release_seal(
            release,
            file_sha(source / "score_denominator_manifest.json"),
        )
        args.seal_output.parent.mkdir(parents=True, exist_ok=True)
        args.seal_output.write_text(json.dumps(seal, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not problems else 1


if __name__ == "__main__":
    raise SystemExit(main())
