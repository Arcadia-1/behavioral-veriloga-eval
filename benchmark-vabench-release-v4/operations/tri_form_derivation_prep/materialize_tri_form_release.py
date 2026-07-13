#!/usr/bin/env python3
"""Materialize 400 DUT, 400 Testbench, and 400 Bugfix task views.

The frozen exact-five DUT release is the only family source.  The generated
views contain public inputs and small private reference records; canonical DUT
evaluator assets stay in the source release and are addressed by hash.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable


PACKAGE_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = PACKAGE_ROOT.parent
PREP_ROOT = Path(__file__).resolve().parent
RUNNERS_ROOT = PACKAGE_ROOT / "runners"
REPO_RUNNERS_ROOT = REPO_ROOT / "runners"
SCRIPTS_ROOT = PACKAGE_ROOT / "scripts"
for import_root in (RUNNERS_ROOT, REPO_RUNNERS_ROOT, SCRIPTS_ROOT):
    if str(import_root) not in sys.path:
        sys.path.insert(0, str(import_root))
from evidence_fingerprints import canonical_sha256, checker_fingerprints  # noqa: E402
from simulate_evas import CHECKS  # noqa: E402
from testbench_security import validate_testbench  # noqa: E402

DEFAULT_SOURCE = PACKAGE_ROOT / "release" / "dut-base-v3-exact-five-hash-bound-v2"
DEFAULT_OUTPUT = PACKAGE_ROOT / "release" / "tri-form-v4-1200-final"
GATE2_MUTATION_PLANS = PACKAGE_ROOT / "operations" / "gate2_mutation_plans"
PROMPT_ASSETS = PREP_ROOT / "prompt_assets"
MODES = {
    "G0": {"process": "direct_one_shot", "form_skill": False, "feedback_skill": False, "feedback_cli": False},
    "G1": {"process": "direct_one_shot", "form_skill": True, "feedback_skill": False, "feedback_cli": False},
    "G2": {"process": "agentic", "form_skill": False, "feedback_skill": False, "feedback_cli": True},
    "G3": {"process": "agentic", "form_skill": True, "feedback_skill": False, "feedback_cli": True},
    "G4": {"process": "agentic", "form_skill": False, "feedback_skill": True, "feedback_cli": True},
    "G5": {"process": "agentic", "form_skill": True, "feedback_skill": True, "feedback_cli": True},
}
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
NEUTRAL_WRAPPER = "neutral_wrapper.md"
REFERENCE_TOKENIZER = {
    "id": "vabench_utf8_lexeme",
    "version": "1.0.0",
    "algorithm": "Unicode word runs and individual non-whitespace punctuation marks",
}
COMPONENT_METADATA = {
    "neutral_wrapper.md": {"stable_id": "wrapper.neutral", "kind": "wrapper", "applicable_forms": ["dut", "testbench", "bugfix"]},
    "dut_modeling.md": {"stable_id": "skill.form.dut", "kind": "form_skill", "applicable_forms": ["dut"]},
    "testbench_verification.md": {"stable_id": "skill.form.testbench", "kind": "form_skill", "applicable_forms": ["testbench"]},
    "bugfix_diagnosis.md": {"stable_id": "skill.form.bugfix", "kind": "form_skill", "applicable_forms": ["bugfix"]},
    "feedback_core.md": {"stable_id": "skill.feedback.core", "kind": "feedback_skill", "applicable_forms": ["dut", "testbench", "bugfix"]},
    "feedback_dut.md": {"stable_id": "skill.feedback.dut", "kind": "feedback_skill", "applicable_forms": ["dut"]},
    "feedback_testbench.md": {"stable_id": "skill.feedback.testbench", "kind": "feedback_skill", "applicable_forms": ["testbench"]},
    "feedback_bugfix.md": {"stable_id": "skill.feedback.bugfix", "kind": "feedback_skill", "applicable_forms": ["bugfix"]},
}
CADENCE_SKILL_PROVENANCE = {
    "dut_modeling.md": {
        "type": "derived_from_installed_vendor_help",
        "tool": "Cadence Spectre",
        "tool_version": "21.1.0.509.isr12",
        "commands": ["spectre -h veriloga", "spectre -h ahdllint"],
        "retrieved_on": "2026-07-13",
        "derivation": "Concise paraphrase of general Verilog-A language, transition, event, and lint guidance; no benchmark outputs were used.",
    },
    "testbench_verification.md": {
        "type": "derived_from_installed_vendor_help",
        "tool": "Cadence Spectre",
        "tool_version": "21.1.0.509.isr12",
        "commands": ["spectre -h veriloga", "spectre -h vsource", "spectre -h tran", "spectre -h save"],
        "retrieved_on": "2026-07-13",
        "derivation": "Concise paraphrase of general Spectre instance, ahdl_include, DC/pulse/sine/PWL source, transient-analysis, and save syntax; no benchmark outputs were used.",
    },
    "bugfix_diagnosis.md": {
        "type": "derived_from_installed_vendor_help",
        "tool": "Cadence Spectre",
        "tool_version": "21.1.0.509.isr12",
        "commands": ["spectre -h veriloga", "spectre -h ahdllint"],
        "retrieved_on": "2026-07-13",
        "derivation": "Concise repair checklist grounded in general Verilog-A structure and AHDL lint categories; no benchmark mutations or outputs were used.",
    },
}
PROJECT_COMPONENT_PROVENANCE = {
    "neutral_wrapper.md": {
        "type": "project_authored_experiment_protocol",
        "source": "V4_TRI_FORM_BENCHMARK_REQUIREMENTS.md",
        "derivation": "Shared transport and submission-root contract; contains no circuit or debugging guidance.",
    },
    "feedback_core.md": {
        "type": "project_authored_facility_guidance",
        "source": "operations/calibration_pilot/feedback_adapter.py",
        "derivation": "Describes the observable vaBench feedback surface without prescribing a repair strategy.",
    },
    "feedback_dut.md": {
        "type": "project_authored_facility_guidance",
        "source": "operations/calibration_pilot/feedback_adapter.py",
        "derivation": "DUT-specific interpretation of public vaBench feedback channels.",
    },
    "feedback_testbench.md": {
        "type": "project_authored_facility_guidance",
        "source": "operations/calibration_pilot/feedback_adapter.py",
        "derivation": "Testbench-specific interpretation of reference and anonymous negative-case outcomes.",
    },
    "feedback_bugfix.md": {
        "type": "project_authored_facility_guidance",
        "source": "operations/calibration_pilot/feedback_adapter.py",
        "derivation": "Bugfix-specific interpretation of public vaBench feedback channels.",
    },
}
TRIVIAL_FAULT_CLASSES = {
    "zero_stub_output",
    "holds_clock_output_low",
    "constant_stub_output",
}
TRIVIAL_ID_MARKERS = {"force_zero", "stuck_zero", "constant_zero"}
SEMANTIC_MARKERS = {
    "async": 5, "asynchronous": 5, "edge": 5, "reset": 5, "hold": 5,
    "timing": 5, "delay": 4, "state": 5, "sequence": 5, "calibration": 4,
    "hysteresis": 4, "slew": 4, "settling": 4, "polarity": 4, "direction": 4,
    "gain": 3, "clipping": 3, "saturation": 3, "rail": 3, "weight": 3,
}
SPECTRE_INCLUDE_RE = re.compile(r"\b(?:ahdl_include|include)\s+[\"']([^\"']+)[\"']", re.IGNORECASE)
SPECTRE_INSTANCE_RE = re.compile(
    r"^\s*([A-Za-z_][A-Za-z0-9_$]*)\s*\(([^)]*)\)\s*([A-Za-z_][A-Za-z0-9_$]*)\b",
    re.IGNORECASE,
)
TESTBENCH_SECURITY_LIMITS = {
    "max_candidate_bytes": 1_000_000,
    "max_stop_time_s": 1.0,
    "max_analyses": 1,
    "max_saved_signals_floor": 64,
    "max_output_bytes": 100_000_000,
    "max_cpu_time_s": 120,
    "max_memory_mb": 2048,
    "max_wall_time_s": 180,
}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_compact_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n",
        encoding="utf-8",
    )


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def file_sha(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def canonical_sha(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return sha_bytes(payload.encode("utf-8"))


def reference_token_count(text: str) -> int:
    return len(re.findall(r"\w+|[^\w\s]", text, flags=re.UNICODE))


def component_fingerprint(component_id: str, path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    tokenizer_id = f"{REFERENCE_TOKENIZER['id']}@{REFERENCE_TOKENIZER['version']}"
    return {
        "id": component_id,
        "sha256": file_sha(path),
        "bytes": path.stat().st_size,
        "token_counts": {tokenizer_id: reference_token_count(text)},
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


def aggregate_file_sha(paths: Iterable[Path], *, base: Path) -> str:
    """Match the content identity used by canonical certification runners."""
    digest = hashlib.sha256()
    for path in sorted(paths):
        digest.update(path.relative_to(base).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(file_sha(path).encode("ascii"))
        digest.update(b"\0")
    return digest.hexdigest()


def aggregate_artifact_sha(artifacts: dict[str, Path]) -> str:
    digest = hashlib.sha256()
    for relative, path in sorted(artifacts.items()):
        if not path.is_file():
            raise SystemExit(f"missing artifact for evidence binding: {path}")
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(file_sha(path).encode("ascii"))
        digest.update(b"\0")
    return digest.hexdigest()


@lru_cache(maxsize=None)
def current_source_evidence_identity(source_task: Path) -> dict[str, Any]:
    evaluator = source_task / "evaluator"
    family_spec_path = evaluator / "family_spec.json"
    checker_profile_path = evaluator / "checker_profile.json"
    harness_path = evaluator / "harness_spec.json"
    feedback_profile_path = evaluator / "profiles" / "feedback.json"
    score_profile_path = evaluator / "profiles" / "score.json"
    feedback_deck_path = source_task / "public" / "task" / "feedback_tb.scs"
    score_deck_path = evaluator / "score_tb.scs"
    solution = evaluator / "solution"
    family_spec = read_json(family_spec_path)
    checker_profile = read_json(checker_profile_path)
    checker_task_id = str(checker_profile.get("checker_task_id") or "")
    artifact_paths = [
        str(item["path"])
        for item in (family_spec.get("artifact_contract") or {}).get("files") or []
    ]
    gold_files = [solution / relative for relative in artifact_paths]
    missing = [str(path) for path in gold_files if not path.is_file()]
    if missing:
        raise SystemExit(f"{source_task.name}: missing gold artifacts for evidence binding: {missing}")
    return {
        "task_inputs": {
            "family_spec_sha256": file_sha(family_spec_path),
            "checker_profile_sha256": file_sha(checker_profile_path),
            "harness_spec_sha256": file_sha(harness_path),
            "feedback_profile_sha256": file_sha(feedback_profile_path),
            "score_profile_sha256": file_sha(score_profile_path),
            "feedback_deck_sha256": file_sha(feedback_deck_path),
            "score_deck_sha256": file_sha(score_deck_path),
            "gold_bundle_sha256": aggregate_file_sha(gold_files, base=solution),
            "property_contract_sha256": canonical_sha256(family_spec.get("properties") or []),
            "trace_contract_sha256": canonical_sha256(family_spec.get("trace_contract") or {}),
        },
        "oracle": checker_fingerprints(
            checker_task_id,
            checker_profile,
            CHECKS.get(checker_task_id),
        ),
        "artifact_paths": artifact_paths,
    }


def fingerprint_mismatches(
    recorded: dict[str, Any],
    current: dict[str, Any],
    keys: Iterable[str],
    *,
    prefix: str,
) -> list[str]:
    return [
        f"{prefix}.{key}"
        for key in keys
        if not recorded.get(key) or recorded.get(key) != current.get(key)
    ]


def source_record_mismatches(
    record: dict[str, Any],
    current: dict[str, Any],
    *,
    task_input_keys: Iterable[str],
) -> list[str]:
    components = record.get("component_fingerprints") or {}
    mismatches = fingerprint_mismatches(
        components.get("task_inputs") or {},
        current["task_inputs"],
        task_input_keys,
        prefix="task_inputs",
    )
    mismatches.extend(
        fingerprint_mismatches(
            components.get("oracle") or {},
            current["oracle"],
            (
                "checker_profile_sha256",
                "checker_binding_sha256",
                "checker_implementation_sha256",
                "diagnostic_policy_sha256",
            ),
            prefix="oracle",
        )
    )
    return mismatches


def replay_record_sha(record: dict[str, Any]) -> str:
    payload = {key: value for key, value in record.items() if key != "record_sha256"}
    return canonical_sha(payload)


def compact_reference_replay_record(
    row: dict[str, Any],
    *,
    source_evidence_sha256: str,
) -> dict[str, Any]:
    """Keep only hash-bound simulator evidence needed by the release audit."""
    spectre_identity = row.get("spectre_identity") or {}
    spectre = row.get("spectre") or {}
    record = {
        "schema_version": "v4-reference-replay-row-v1",
        "canonical_id": str(row.get("canonical_id") or row.get("family_id") or "").zfill(3),
        "mutation_id": str(row.get("mutation_id") or ""),
        "profile": str(row.get("profile") or ""),
        "status": str(row.get("status") or ""),
        "source_evidence_sha256": source_evidence_sha256,
        "source_row_sha256": canonical_sha(row),
        "component_fingerprints": row.get("component_fingerprints") or {},
        "evaluators": {
            backend: (row.get("evaluators") or {}).get(backend) or {}
            for backend in ("ahdl_like", "evas", "spectre")
        },
        "checkers": {
            checker: (row.get("checkers") or {}).get(checker) or {}
            for checker in ("evas_behavior", "spectre_behavior")
        },
        "property_activation_status": row.get("property_activation_status"),
        "property_activation": {
            key: value
            for key, value in (row.get("property_activation") or {}).items()
            if key in {"status", "diagnostic_patterns", "matched_patterns", "matched_patterns_by_backend", "notes"}
        },
        "side_effect": {
            "required": (row.get("side_effect") or {}).get("required", False),
            "evas": (row.get("side_effect") or {}).get("evas") or {},
            "spectre": (row.get("side_effect") or {}).get("spectre") or {},
        },
        "evas": {
            key: (row.get("evas") or {}).get(key)
            for key in ("ran", "ok", "returncode", "warnings")
        },
        "spectre": {
            key: spectre.get(key)
            for key in ("ran", "ok", "rows", "untriaged_warnings")
        },
        "spectre_identity": {
            key: spectre_identity.get(key)
            for key in ("backend", "host", "mode", "transport_identity", "verification", "version")
            if spectre_identity.get(key) is not None
        },
    }
    if not record["canonical_id"].isdigit() or not record["mutation_id"]:
        raise SystemExit("reference replay evidence row lacks canonical_id or mutation_id")
    if record["profile"] not in {"feedback", "score"}:
        raise SystemExit(
            f"{record['canonical_id']}/{record['mutation_id']}: invalid replay profile {record['profile']!r}"
        )
    record["record_sha256"] = replay_record_sha(record)
    return record


def load_reference_replay_evidence(
    paths: Iterable[Path],
) -> tuple[dict[tuple[str, str, str], list[dict[str, Any]]], dict[str, dict[str, Any]]]:
    lookup: dict[tuple[str, str, str], list[dict[str, Any]]] = {}
    sources: dict[str, dict[str, Any]] = {}
    seen_records: set[str] = set()
    for path in paths:
        resolved = path.expanduser().resolve()
        payload = read_json(resolved)
        rows = payload.get("rows") or []
        if not isinstance(rows, list):
            raise SystemExit(f"reference replay evidence rows must be an array: {resolved}")
        evidence_sha = file_sha(resolved)
        sources[evidence_sha] = {
            "sha256": evidence_sha,
            "schema_version": str(payload.get("schema_version") or ""),
            "row_count": len(rows),
        }
        for row in rows:
            if not isinstance(row, dict):
                raise SystemExit(f"reference replay evidence contains a non-object row: {resolved}")
            record = compact_reference_replay_record(
                row,
                source_evidence_sha256=evidence_sha,
            )
            record_sha = str(record["record_sha256"])
            if record_sha in seen_records:
                continue
            seen_records.add(record_sha)
            key = (
                str(record["canonical_id"]),
                str(record["mutation_id"]),
                str(record["profile"]),
            )
            lookup.setdefault(key, []).append(record)
    for records in lookup.values():
        records.sort(key=lambda item: str(item["record_sha256"]))
    return lookup, sources


def reference_replay_mismatches(
    record: dict[str, Any],
    current: dict[str, Any],
    source_task: Path,
) -> list[str]:
    mismatches = source_record_mismatches(
        record,
        current,
        task_input_keys=(
            "deck_sha256",
            "profile_sha256",
            "harness_spec_sha256",
            "gold_bundle_sha256",
            "candidate_bundle_sha256",
            "property_contract_sha256",
            "trace_contract_sha256",
        ),
    )
    components = record.get("component_fingerprints") or {}
    assembly = components.get("assembly") or {}
    expected_lock_sha = file_sha(source_task / "evaluator" / "toolchain_lock.json")
    if assembly.get("release_snapshot_sha256") != expected_lock_sha:
        mismatches.append("assembly.release_snapshot_sha256")
    if record.get("status") not in {
        "PASS",
        "FAIL_PROPERTY_ACTIVATION",
        "property_activation_unverified",
    }:
        mismatches.append("supplemental.status")
    evaluators = record.get("evaluators") or {}
    if (evaluators.get("ahdl_like") or {}).get("compile_status") != "pass":
        mismatches.append("supplemental.evaluators.ahdl_like.compile_status")
    for backend in ("evas", "spectre"):
        backend_eval = evaluators.get(backend) or {}
        for key, expected in (
            ("compile_status", "pass"),
            ("simulation_status", "pass"),
            ("behavior_status", "behavior_fail"),
        ):
            if backend_eval.get(key) != expected:
                mismatches.append(f"supplemental.evaluators.{backend}.{key}")
        checker = (record.get("checkers") or {}).get(f"{backend}_behavior") or {}
        if checker.get("status") != "behavior_fail":
            mismatches.append(f"supplemental.checkers.{backend}_behavior.status")
    evas = record.get("evas") or {}
    if evas.get("ran") is not True or evas.get("ok") is not True or evas.get("returncode") != 0:
        mismatches.append("supplemental.evas.execution")
    spectre = record.get("spectre") or {}
    if spectre.get("ran") is not True or spectre.get("ok") is not True or int(spectre.get("rows") or 0) <= 0:
        mismatches.append("supplemental.spectre.execution")
    if spectre.get("untriaged_warnings"):
        mismatches.append("supplemental.spectre.untriaged_warnings")
    side_effect = record.get("side_effect") or {}
    if side_effect.get("required"):
        for backend in ("evas", "spectre"):
            if (side_effect.get(backend) or {}).get("pass") is not True:
                mismatches.append(f"supplemental.side_effect.{backend}")
    if record.get("record_sha256") != replay_record_sha(record):
        mismatches.append("supplemental.record_sha256")
    return sorted(set(mismatches))


def mutation_reference_identity(
    source_task: Path,
    mutation_id: str,
    reference_tb: Path,
    profile: str,
) -> dict[str, Any]:
    current = current_source_evidence_identity(source_task)
    mutation_dir = source_task / "evaluator" / "mutation_bundles" / mutation_id
    candidate_artifacts = {
        relative: (
            mutation_dir / relative
            if (mutation_dir / relative).is_file()
            else source_task / "evaluator" / "solution" / relative
        )
        for relative in current["artifact_paths"]
    }
    return {
        **current,
        "task_inputs": {
            **current["task_inputs"],
            "deck_sha256": file_sha(reference_tb),
            "profile_sha256": current["task_inputs"].get(f"{profile}_profile_sha256"),
            "candidate_bundle_sha256": aggregate_artifact_sha(candidate_artifacts),
        },
    }


def canonical_mutation_certificate_mismatches(
    record: dict[str, Any],
    current: dict[str, Any],
    source_task: Path,
) -> list[str]:
    mismatches = source_record_mismatches(
        record,
        current,
        task_input_keys=(
            "deck_sha256",
            "profile_sha256",
            "harness_spec_sha256",
            "gold_bundle_sha256",
            "candidate_bundle_sha256",
            "property_contract_sha256",
            "trace_contract_sha256",
        ),
    )
    if record.get("outcome") != "killed_behaviorally":
        mismatches.append("source.outcome")
    if (record.get("evaluators") or {}).get("spectre") != "compile_pass_behavior_fail":
        mismatches.append("source.evaluators.spectre")
    expected_lock_sha = file_sha(source_task / "evaluator" / "toolchain_lock.json")
    assembly = (record.get("component_fingerprints") or {}).get("assembly") or {}
    if assembly.get("release_snapshot_sha256") != expected_lock_sha:
        mismatches.append("source.assembly.release_snapshot_sha256")
    return sorted(set(mismatches))


def canonical_source_certificate_mismatches(
    record: dict[str, Any],
    source_task: Path,
    mutation_id: str,
) -> list[str]:
    current = current_source_evidence_identity(source_task)
    recorded_inputs = (record.get("component_fingerprints") or {}).get("task_inputs") or {}
    matching_profiles = [
        profile
        for profile in ("feedback", "score")
        if current["task_inputs"].get(f"{profile}_profile_sha256")
        == recorded_inputs.get("profile_sha256")
        and current["task_inputs"].get(f"{profile}_deck_sha256")
        == recorded_inputs.get("deck_sha256")
    ]
    if len(matching_profiles) != 1:
        return ["source.canonical_profile_binding"]
    profile = matching_profiles[0]
    deck = (
        source_task / "public" / "task" / "feedback_tb.scs"
        if profile == "feedback"
        else source_task / "evaluator" / "score_tb.scs"
    )
    identity = mutation_reference_identity(source_task, mutation_id, deck, profile)
    return canonical_mutation_certificate_mismatches(record, identity, source_task)


def gold_reference_certificate_state(
    source_task: Path,
    reference_tb: Path,
) -> dict[str, Any]:
    current = current_source_evidence_identity(source_task)
    current_inputs = current["task_inputs"]
    deck_sha = file_sha(reference_tb)
    matching_profiles = [
        profile
        for profile in ("feedback", "score")
        if current_inputs.get(f"{profile}_deck_sha256") == deck_sha
    ]
    certificate_path = source_task / "evaluator" / "certification.json"
    record = read_json(certificate_path)
    profile_pass = any(
        (record.get("checks") or {}).get("gold_bundle", {}).get(f"{profile}_profile") == "pass"
        for profile in matching_profiles
    )
    mismatches = source_record_mismatches(
        record,
        current,
        task_input_keys=(
            "family_spec_sha256",
            "checker_profile_sha256",
            "harness_spec_sha256",
            "gold_bundle_sha256",
            *(f"{profile}_profile_sha256" for profile in matching_profiles),
            *(f"{profile}_deck_sha256" for profile in matching_profiles),
        ),
    )
    if not matching_profiles:
        mismatches.append("task_inputs.reference_deck_sha256")
    reusable = (
        record.get("status") in {"pass", "gate2_pass"}
        and profile_pass
        and not mismatches
    )
    return {
        "path": certificate_path,
        "record": record,
        "matching_profiles": matching_profiles,
        "mismatches": sorted(set(mismatches)),
        "reusable": reusable,
    }


def select_reference_replay_candidate(
    replay_candidates: list[dict[str, Any]],
    current: dict[str, Any],
    source_task: Path,
) -> tuple[dict[str, Any] | None, list[str]]:
    mismatches: list[str] = []
    valid: list[dict[str, Any]] = []
    for replay_record in replay_candidates:
        candidate_mismatches = reference_replay_mismatches(
            replay_record,
            current,
            source_task,
        )
        if candidate_mismatches:
            mismatches.extend(candidate_mismatches)
        else:
            valid.append(replay_record)
    if len(valid) == 1:
        return valid[0], []
    if len(valid) > 1:
        return None, ["supplemental.ambiguous_valid_records"]
    if replay_candidates:
        return None, sorted(set(mismatches))
    return None, ["supplemental.reference_deck_evidence_missing"]


def materialized_artifact_hashes(output: Path) -> dict[str, str]:
    return {relative: file_sha(output / relative) for relative in MATERIALIZED_ARTIFACTS}


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def source_rel(path: Path, source_root: Path, source_reference: str) -> str:
    return (Path(source_reference) / path.relative_to(source_root)).as_posix()


def resolve_source_reference(source: Path, requested: str | None) -> str:
    if requested is None:
        try:
            return rel(source, PACKAGE_ROOT)
        except ValueError as exc:
            raise SystemExit(
                "source is outside the package; pass --source-reference with its future "
                "package-relative release path"
            ) from exc
    reference = Path(requested)
    if reference.is_absolute() or ".." in reference.parts or str(reference) in {"", "."}:
        raise SystemExit("--source-reference must be a non-empty safe relative path")
    return reference.as_posix()


def task_title(spec: dict[str, Any]) -> str:
    return str((spec.get("identity") or {}).get("title") or f"Family {spec['family_id']}")


def expand_bus_name(name: str) -> list[str]:
    match = re.fullmatch(r"(.+)\[(\d+):(\d+)\]", name)
    if match is None:
        return [name]
    base, first, last = match.groups()
    start = int(first)
    stop = int(last)
    step = -1 if start > stop else 1
    return [f"{base}{index}" for index in range(start, stop + step, step)]


def spectre_logical_lines(text: str) -> list[str]:
    logical: list[str] = []
    pending = ""
    paren_depth = 0
    for raw in text.splitlines():
        line = raw.split("//", 1)[0].strip()
        if not line:
            continue
        pending = f"{pending} {line}".strip()
        paren_depth += line.count("(") - line.count(")")
        continued = pending.endswith("\\")
        if continued:
            pending = pending[:-1].rstrip()
        if paren_depth <= 0 and not continued:
            logical.append(pending)
            pending = ""
            paren_depth = 0
    if pending:
        logical.append(pending)
    return logical


def reference_deck_structure(reference_tb: Path) -> tuple[list[str], list[tuple[str, str, list[str]]]]:
    text = reference_tb.read_text(encoding="utf-8")
    includes = SPECTRE_INCLUDE_RE.findall(text)
    instances: list[tuple[str, str, list[str]]] = []
    for line in spectre_logical_lines(text):
        match = SPECTRE_INSTANCE_RE.match(line)
        if match is None:
            continue
        name, nodes, module = match.groups()
        instances.append((name, module, [item for item in re.split(r"[\s,]+", nodes.strip()) if item]))
    return includes, instances


def reference_deck_saved_signals(reference_tb: Path) -> list[str]:
    saved: list[str] = []
    for line in spectre_logical_lines(reference_tb.read_text(encoding="utf-8")):
        match = re.match(r"^\s*save\s+(.+)$", line, re.IGNORECASE)
        if match is None:
            continue
        for token in re.split(r"[\s,]+", match.group(1).strip()):
            if token and token.lower() != "time" and token not in saved:
                saved.append(token)
    return ["time", *saved]


def render_interface(spec: dict[str, Any]) -> str:
    blocks: list[str] = []
    for file_record in (spec.get("artifact_contract") or {}).get("files") or []:
        blocks.append(f"- Artifact `{file_record['path']}`:")
        for module in file_record.get("modules") or []:
            role = str(module.get("role") or "module")
            blocks.append(f"  - Module `{module['name']}` ({role})")
            ports = sorted(module.get("ports") or [], key=lambda item: int(item.get("position", 0)))
            for port in ports:
                blocks.append(
                    f"    - position {port['position']}: `{port['name']}` "
                    f"({port['direction']}, {port['discipline']})"
                )
    return "\n".join(blocks) or "- Use the interface declared in `public_contract.json`."


def render_parameters(spec: dict[str, Any]) -> str:
    lines: list[str] = []
    for file_record in (spec.get("artifact_contract") or {}).get("files") or []:
        for module in file_record.get("modules") or []:
            for parameter in module.get("parameters") or []:
                units = f" {parameter['units']}" if parameter.get("units") else ""
                lines.append(
                    f"- `{module['name']}.{parameter['name']}` defaults to "
                    f"`{parameter.get('default')}`{units}; valid range: "
                    f"{parameter.get('valid_range', 'as declared')}; "
                    f"{parameter.get('override_behavior', 'honor public overrides')}."
                )
    return "\n".join(lines) or "- No public parameter is declared."


def render_properties(spec: dict[str, Any], verb: str) -> str:
    lines = []
    for prop in spec.get("properties") or []:
        signals = ", ".join(f"`{value}`" for value in prop.get("required_signals") or [])
        lines.append(f"- `{prop['id']}`: {verb} {prop['observable_contract']} Required traces: {signals}.")
    return "\n".join(lines)


def render_property_summary(spec: dict[str, Any]) -> str:
    return "\n".join(
        f"- `{prop['id']}`: {prop['observable_contract']}"
        for prop in spec.get("properties") or []
    )


def render_artifact_summary(spec: dict[str, Any]) -> str:
    lines: list[str] = []
    for file_record in (spec.get("artifact_contract") or {}).get("files") or []:
        modules = ", ".join(f"`{module['name']}`" for module in file_record.get("modules") or [])
        lines.append(f"- `{file_record['path']}`: {modules or 'declared Verilog-A artifact'}")
    return "\n".join(lines)


def supplied_testbench_inputs(
    spec: dict[str, Any],
    reference_tb: Path | None = None,
    public_support: Path | None = None,
) -> dict[str, Any]:
    binding = spec.get("testbench_binding") or {}
    template = str(binding.get("source_path_template") or "./dut/{artifact_path}")
    includes, deck_instances = reference_deck_structure(reference_tb) if reference_tb else ([], [])
    includes_by_name: dict[str, list[str]] = {}
    for include in includes:
        includes_by_name.setdefault(Path(include).name, []).append(include)

    artifacts = []
    for file_record in (spec.get("artifact_contract") or {}).get("files") or []:
        artifact_path = str(file_record["path"])
        candidates = includes_by_name.get(Path(artifact_path).name) or []
        if len(candidates) > 1:
            raise SystemExit(f"ambiguous reference include for {artifact_path}: {candidates}")
        artifacts.append({
            "public_input_path": f"supplied_dut/{artifact_path}",
            "testbench_include_path": candidates[0] if candidates else template.format(artifact_path=artifact_path),
        })

    support_artifacts = []
    if public_support and public_support.is_dir():
        for support in sorted(path for path in public_support.rglob("*") if path.is_file()):
            candidates = includes_by_name.get(support.name) or []
            if not candidates:
                continue
            if len(candidates) > 1:
                raise SystemExit(f"ambiguous reference support include for {support.name}: {candidates}")
            relative = support.relative_to(public_support).as_posix()
            support_artifacts.append({
                "public_input_path": f"public_support/{relative}",
                "testbench_include_path": candidates[0],
            })

    modules: dict[str, dict[str, Any]] = {}
    for file_record in (spec.get("artifact_contract") or {}).get("files") or []:
        for module in file_record.get("modules") or []:
            modules[str(module["name"])] = module
    instances = []
    for declared in binding.get("instances") or []:
        module_ref = str(declared["module_ref"])
        if not deck_instances:
            ordered_nets = [
                net
                for connection in sorted(declared.get("connections") or [], key=lambda item: int(item.get("position", 0)))
                for net in expand_bus_name(str(connection.get("net") or ""))
            ]
            instances.append({**declared, "ordered_nets": ordered_nets, "public_output_nets": []})
            continue
        matches = [item for item in deck_instances if item[1].lower() == module_ref.lower()]
        named = [item for item in matches if item[0].lower() == str(declared.get("name") or "").lower()]
        selected_instances = named if len(named) == 1 else matches
        if not selected_instances:
            raise SystemExit(f"cannot resolve one reference instance for module {module_ref}")
        module = modules.get(module_ref) or {}
        port_directions: list[str] = []
        for port in sorted(module.get("ports") or [], key=lambda item: int(item.get("position", 0))):
            port_directions.extend([str(port.get("direction") or "")] * len(expand_bus_name(str(port["name"]))))
        for actual_name, _, ordered_nets in selected_instances:
            actual_directions = port_directions if len(port_directions) == len(ordered_nets) else [""] * len(ordered_nets)
            instances.append({
                "name": actual_name,
                "module_ref": module_ref,
                "connections": declared.get("connections") or [],
                "ordered_nets": ordered_nets,
                "public_output_nets": [
                    net for net, direction in zip(ordered_nets, actual_directions) if direction == "output"
                ],
            })
    return {
        "read_only_dut_artifacts": artifacts,
        "read_only_support_artifacts": support_artifacts,
        "dut_instances": instances,
    }


def render_binding(spec: dict[str, Any]) -> str:
    supplied = supplied_testbench_inputs(spec)
    lines = [
        f"- Read-only DUT source `{item['public_input_path']}` is available to the submitted deck as "
        f"`{item['testbench_include_path']}`."
        for item in supplied["read_only_dut_artifacts"]
    ]
    for instance in supplied["dut_instances"]:
        connections = sorted(instance.get("connections") or [], key=lambda item: int(item.get("position", 0)))
        ports = ", ".join(f"{item['port_ref']}={item['net']}" for item in connections)
        lines.append(
            f"- Instantiate `{instance['module_ref']}` as `{instance['name']}` with ordered public binding: {ports}."
        )
    return "\n".join(lines)


def render_constraints(spec: dict[str, Any]) -> str:
    lines = [f"- {value}" for value in spec.get("modeling_constraints") or []]
    return "\n".join(lines) or "- Keep behavior deterministic and within the declared voltage-domain scope."


def render_dut_instruction(spec: dict[str, Any]) -> str:
    title = task_title(spec)
    paths = [str(item["path"]) for item in (spec.get("artifact_contract") or {}).get("files") or []]
    return f"""# {title}

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

{render_artifact_summary(spec)}

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

{render_property_summary(spec)}

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: {', '.join(f'`{path}`' for path in paths)}.
Do not add or omit artifacts.
"""


def render_testbench_instruction(spec: dict[str, Any]) -> str:
    title = task_title(spec)
    return f"""# {title} Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `{title}` DUT. The evaluator runs the same submitted bytes
against the correct DUT and five anonymous semantic negative DUTs. Your
testbench must accept the correct DUT and expose all five behavioral faults.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

The exact read-only source paths, modules, ports, instance names, and ordered
terminal bindings are declared in `solver_contract.json`.

## Public Parameter Contract

Honor the public parameter declarations in `solver_contract.json` when choosing
stimulus and coverage.

## Required Behavior

Create stimulus and save traces sufficient for the fixed evaluator oracle to check:

{render_property_summary(spec)}

The required trace names are: {', '.join(f'`{x}`' for x in (spec.get('trace_contract') or {}).get('required_signals') or [])}.

## Modeling Constraints

- Submit one self-contained top-level transient `.scs` file.
- Use only the exact declared testbench include paths and public DUT interfaces.
- Do not redefine the DUT, drive declared DUT outputs, inspect private internals,
  access undeclared files, or emit a self-reported result.
- Respect every public resource limit in `solver_contract.json`.
- Missing traces, setup errors, and invalid runs do not count as behavioral kills.

## Output Contract

Return exactly one submission-root-relative artifact named `testbench.scs`. Do not return a DUT,
checker, script, data file, waveform, or auxiliary deck.
"""


def render_bugfix_instruction(spec: dict[str, Any]) -> str:
    title = task_title(spec)
    paths = [str(item["path"]) for item in (spec.get("artifact_contract") or {}).get("files") or []]
    return f"""# {title} Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

{render_artifact_summary(spec)}

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

{render_property_summary(spec)}

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: {', '.join(f'`{path}`' for path in paths)}.
Every supplied `.va` file is editable; do not add or omit files.
"""


def public_semantics(spec: dict[str, Any]) -> dict[str, Any]:
    return {
        "family_id": spec["family_id"],
        "identity": spec["identity"],
        "artifact_contract": spec["artifact_contract"],
        "properties": spec["properties"],
        "trace_contract": spec["trace_contract"],
        "modeling_constraints": spec.get("modeling_constraints") or [],
    }


def submission_contract() -> dict[str, Any]:
    return {
        "target_artifacts_relative_to": "submission_root",
        "agentic_submission_root": "public/submission",
        "exact_declared_file_set_required": True,
    }


def testbench_security_policy(
    spec: dict[str, Any],
    supplied_inputs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    required_signals = list((spec.get("trace_contract") or {}).get("required_signals") or [])
    supplied = supplied_inputs or supplied_testbench_inputs(spec)
    allowed_includes = [
        str(item["testbench_include_path"])
        for key in ("read_only_dut_artifacts", "read_only_support_artifacts")
        for item in supplied.get(key) or []
    ]
    limits = dict(TESTBENCH_SECURITY_LIMITS)
    limits["max_saved_signals"] = max(
        int(limits.pop("max_saved_signals_floor")),
        len({expanded.lower() for item in required_signals if str(item).lower() != "time" for expanded in expand_bus_name(str(item))}) + 16,
    )
    return {
        "schema_version": "v4-testbench-security-policy-v2",
        "candidate_artifacts": ["testbench.scs"],
        "allowed_include_paths": allowed_includes,
        "forbidden_rules": [
            "undeclared_include",
            "absolute_path",
            "path_traversal",
            "process_execution",
            "network_access",
            "simulator_scripting_escape",
            "dut_redefinition",
            "direct_dut_output_drive",
            "private_hierarchical_probe",
            "unbounded_resource_use",
        ],
        "required_rules": [
            "declared_dut_binding",
            "transient_analysis",
            "all_required_public_traces",
        ],
        "limits": limits,
        "rejection_outcome": "invalid_run",
    }


def build_dut_public_contract(spec: dict[str, Any], task_id: str) -> dict[str, Any]:
    contract = public_semantics(spec)
    contract.update({
        "schema_version": "v4-tri-form-public-contract-v2",
        "task_id": task_id,
        "form": "dut",
        "target_artifacts": [str(item["path"]) for item in spec["artifact_contract"]["files"]],
        "submission_contract": submission_contract(),
        "feedback": {"available_in_modes": ["G2", "G3", "G4", "G5"], "command": "vabench feedback run"},
    })
    return contract


def build_testbench_public_contract(
    spec: dict[str, Any],
    task_id: str,
    reference_tb: Path | None = None,
    public_support: Path | None = None,
) -> dict[str, Any]:
    supplied = supplied_testbench_inputs(spec, reference_tb, public_support)
    contract = json.loads(json.dumps(public_semantics(spec)))
    if reference_tb is not None:
        required_signals = reference_deck_saved_signals(reference_tb)
        contract["trace_contract"] = {"required_signals": required_signals}
        for prop in contract.get("properties") or []:
            prop["required_signals"] = required_signals
    contract.update({
        "schema_version": "v4-tri-form-public-contract-v2",
        "task_id": task_id,
        "form": "testbench",
        "target_artifacts": ["testbench.scs"],
        "submission_contract": submission_contract(),
        "supplied_inputs": supplied,
        "evaluation_summary": {
            "reference_cases": 1,
            "anonymous_negative_cases": 5,
            "full_credit": "valid candidate and reference pass and all five negatives killed behaviorally",
        },
        "feedback": {"available_in_modes": ["G2", "G3", "G4", "G5"], "command": "vabench feedback run"},
        "security_policy": testbench_security_policy(contract, supplied),
    })
    return contract


def select_reference_testbench(
    source_task: Path,
    spec: dict[str, Any],
    task_id: str,
    public_support: Path | None,
) -> tuple[Path, dict[str, Any], str]:
    candidates = (
        ("score", source_task / "evaluator" / "score_tb.scs"),
        ("feedback", source_task / "public" / "task" / "feedback_tb.scs"),
    )
    diagnostics: dict[str, tuple[str, ...]] = {}
    for profile, reference in candidates:
        if not reference.is_file():
            continue
        contract = build_testbench_public_contract(spec, task_id, reference, public_support)
        result = validate_testbench(reference, contract, contract["security_policy"])
        if result.valid:
            return reference, contract, profile
        diagnostics[profile] = result.diagnostics
    raise SystemExit(f"no structurally valid reference testbench for {task_id}: {diagnostics}")


def build_bugfix_public_contract(spec: dict[str, Any], task_id: str) -> dict[str, Any]:
    artifacts = [str(item["path"]) for item in spec["artifact_contract"]["files"]]
    contract = public_semantics(spec)
    contract.update({
        "schema_version": "v4-tri-form-public-contract-v2",
        "task_id": task_id,
        "form": "bugfix",
        "target_artifacts": artifacts,
        "submission_contract": submission_contract(),
        "buggy_input_artifacts": [f"buggy_bundle/{path}" for path in artifacts],
        "editable_scope": "complete_declared_verilog_a_bundle",
        "problem_statement": "the supplied system violates the public contract",
        "feedback": {"available_in_modes": ["G2", "G3", "G4", "G5"], "command": "vabench feedback run"},
    })
    return contract


def build_solver_contract(public_contract: dict[str, Any]) -> dict[str, Any]:
    """Project the complete public record into the exact solver-visible contract."""
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


def mutation_score(item: dict[str, Any], preferred: bool) -> tuple[int, str]:
    mutation_id = str(item["mutation_id"])
    fault_class = str(item.get("fault_class") or "")
    trigger = str(item.get("trigger_condition") or "")
    text = f"{mutation_id} {fault_class} {trigger}".lower()
    score = 3 * len(item.get("violated_property_ids") or []) + min(len(trigger.split()), 8)
    for marker, weight in SEMANTIC_MARKERS.items():
        if marker in text:
            score += weight
    trivial = []
    if fault_class.lower() in TRIVIAL_FAULT_CLASSES:
        trivial.append(fault_class.lower())
    trivial.extend(marker for marker in TRIVIAL_ID_MARKERS if marker in mutation_id.lower())
    trivial = sorted(set(trivial))
    score -= 24 * len(trivial)
    if preferred:
        score += 2
    return score, ",".join(trivial)


def select_bugfix_seed(row: dict[str, Any]) -> dict[str, Any]:
    preferred = str(row.get("bugfix_seed") or "")
    ranked = []
    for item in row["active_mutations"]:
        score, markers = mutation_score(item, str(item["mutation_id"]) == preferred)
        ranked.append((score, str(item["mutation_id"]), markers, item))
    ranked.sort(key=lambda value: (-value[0], value[1]))
    score, mutation_id, markers, item = ranked[0]
    return {
        "mutation_id": mutation_id,
        "selection_policy": "semantic_fault_complexity_v1",
        "selection_status": "policy_reviewed",
        "source_preferred_seed": preferred,
        "source_preferred_seed_preserved": mutation_id == preferred,
        "semantic_score": score,
        "triviality_markers": markers.split(",") if markers else [],
        "rationale": (
            f"Select fault class {item.get('fault_class')} under trigger "
            f"'{item.get('trigger_condition')}' because it exercises "
            f"{', '.join(item.get('violated_property_ids') or [])} as one compile-pass semantic defect."
        ),
    }


def copy_solution(source_task: Path, destination: Path, spec: dict[str, Any]) -> list[str]:
    paths = [str(item["path"]) for item in spec["artifact_contract"]["files"]]
    for artifact in paths:
        source = source_task / "evaluator" / "solution" / artifact
        if not source.is_file():
            raise SystemExit(f"{source_task.name}: missing solution artifact {artifact}")
        target = destination / artifact
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    return paths


def sanitize_public_buggy_source(text: str) -> tuple[str, bool]:
    """Remove a leading evaluator annotation block without changing Verilog-A code."""
    lines = text.splitlines(keepends=True)
    first_code = next(
        (index for index, line in enumerate(lines) if line.strip() and not line.lstrip().startswith("//")),
        len(lines),
    )
    marker = re.compile(
        r"\b(?:mutation_id|negative_variants|checker_id|violated_property_ids|bugfix_seed)\b|"
        r"\bneg_\d{3}(?:\b|_)",
        re.IGNORECASE,
    )
    marker_index = next(
        (index for index, line in enumerate(lines[:first_code]) if marker.search(line)),
        None,
    )
    if marker_index is None:
        return text, False
    block_end = marker_index + 1
    while block_end < first_code and (
        not lines[block_end].strip() or lines[block_end].lstrip().startswith("//")
    ):
        block_end += 1
    return "".join([*lines[:marker_index], *lines[block_end:]]), True


def overlay_mutation(source_task: Path, mutation_id: str, destination: Path, artifact_paths: list[str]) -> list[str]:
    mutation_dir = source_task / "evaluator" / "mutation_bundles" / mutation_id
    candidates = sorted(mutation_dir.rglob("*.va"))
    if not candidates:
        raise SystemExit(f"{source_task.name}/{mutation_id}: mutation bundle has no Verilog-A source")
    changed: list[str] = []
    by_name = {Path(path).name: path for path in artifact_paths}
    for source in candidates:
        relative = source.relative_to(mutation_dir).as_posix()
        if relative in artifact_paths:
            target_rel = relative
        elif source.name in by_name:
            target_rel = by_name[source.name]
        elif len(artifact_paths) == 1:
            target_rel = artifact_paths[0]
        else:
            raise SystemExit(f"{source_task.name}/{mutation_id}: cannot map {relative} into DUT bundle")
        target = destination / target_rel
        target.parent.mkdir(parents=True, exist_ok=True)
        differs_from_gold = not target.is_file() or source.read_bytes() != target.read_bytes()
        public_text, _ = sanitize_public_buggy_source(source.read_text(encoding="utf-8"))
        target.write_text(public_text, encoding="utf-8")
        if differs_from_gold:
            changed.append(target_rel)
    changed = sorted(set(changed))
    if not changed:
        raise SystemExit(f"{source_task.name}/{mutation_id}: mutation bundle is byte-identical to gold")
    return changed


def common_task_record(
    *, task_id: str, form: str, family_id: str, directory: str, spec_sha: str,
    source_task: str, candidate_artifacts: list[str], public_bundle_sha: str,
) -> dict[str, Any]:
    return {
        "schema_version": "v4-tri-form-task-record-v1",
        "task_id": task_id,
        "form": form,
        "family_id": family_id,
        "task_dir": directory,
        "candidate_artifacts": candidate_artifacts,
        "family_spec_sha256": spec_sha,
        "canonical_dut_source": source_task,
        "public_bundle_sha256": public_bundle_sha,
        "scored": True,
        "modes": list(MODES),
    }


def public_bundle_hash(task_dir: Path) -> str:
    included = [
        path for path in sorted(task_dir.rglob("*"))
        if path.is_file() and "evaluator" not in path.parts and path.name != "TASK_RECORD.json"
    ]
    digest = hashlib.sha256()
    for path in included:
        digest.update(path.relative_to(task_dir).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def write_task_record(task_dir: Path, record: dict[str, Any]) -> None:
    write_json(task_dir / "TASK_RECORD.json", record)


def write_public_contract_views(task_dir: Path, contract: dict[str, Any]) -> None:
    write_json(task_dir / "public_contract.json", contract)
    write_compact_json(task_dir / "solver_contract.json", build_solver_contract(contract))


def copy_public_support(source_task: Path, task_dir: Path) -> None:
    source = source_task / "public" / "task" / "public_support"
    if source.is_dir():
        shutil.copytree(source, task_dir / "public_support", dirs_exist_ok=True)


def build_reference_testbench_certificate(
    source_task: Path,
    row: dict[str, Any],
    reference_tb: Path,
    replay_evidence: dict[tuple[str, str, str], list[dict[str, Any]]] | None = None,
) -> dict[str, Any]:
    deck_sha = file_sha(reference_tb)
    current = current_source_evidence_identity(source_task)
    current_inputs = current["task_inputs"]
    gold_state = gold_reference_certificate_state(source_task, reference_tb)
    matching_profiles = list(gold_state["matching_profiles"])
    gold_certificate = gold_state["path"]
    gold_mismatches = list(gold_state["mismatches"])
    gold_reusable = bool(gold_state["reusable"])
    negative_cases: dict[str, Any] = {}
    source_reused_count = 0
    supplemental_reused_count = 0
    for item in row["active_mutations"]:
        mutation_id = str(item["mutation_id"])
        certification = source_task / str(item["certification_path"])
        record = read_json(certification)
        recorded_inputs = (record.get("component_fingerprints") or {}).get("task_inputs") or {}
        selected_profile = next(
            (
                profile
                for profile in matching_profiles
                if current_inputs.get(f"{profile}_profile_sha256") == recorded_inputs.get("profile_sha256")
            ),
            matching_profiles[0] if matching_profiles else "",
        )
        mutation_identity = mutation_reference_identity(
            source_task,
            mutation_id,
            reference_tb,
            selected_profile,
        )
        semantic_mismatches = canonical_source_certificate_mismatches(
            record,
            source_task,
            mutation_id,
        )
        mismatches = canonical_mutation_certificate_mismatches(
            record,
            mutation_identity,
            source_task,
        )
        semantic_certified = not semantic_mismatches
        source_reusable = semantic_certified and not mismatches
        selected_replay: dict[str, Any] | None = None
        replay_mismatches = ["supplemental.reference_deck_evidence_missing"]
        if semantic_certified and not source_reusable:
            replay_candidates = (replay_evidence or {}).get(
                (str(row["canonical_dut_id"]), mutation_id, selected_profile),
                [],
            )
            selected_replay, replay_mismatches = select_reference_replay_candidate(
                replay_candidates,
                mutation_identity,
                source_task,
            )
        reusable = semantic_certified and (source_reusable or selected_replay is not None)
        if source_reusable:
            source_reused_count += 1
        elif selected_replay is not None:
            supplemental_reused_count += 1
        negative_cases[mutation_id] = {
            "status": "killed_behaviorally" if reusable else "canonical_deck_replay_pending",
            "evidence_source": (
                "canonical_mutation_certification"
                if source_reusable
                else "supplemental_reference_deck_replay"
                if selected_replay is not None
                else "pending"
            ),
            "source_certification_sha256": file_sha(certification),
            "source_deck_sha256": recorded_inputs.get("deck_sha256"),
            "reference_deck_sha256": deck_sha,
            "hash_reusable": reusable,
            "source_hash_reusable": source_reusable,
            "source_fingerprint_mismatches": mismatches,
            "canonical_semantic_certification_status": (
                "certified_under_canonical_profile"
                if semantic_certified
                else "canonical_semantic_certification_invalid"
            ),
            "canonical_semantic_fingerprint_mismatches": semantic_mismatches,
            "replay_profile": selected_profile,
            "replay_record_sha256": (
                selected_replay.get("record_sha256") if selected_replay is not None else None
            ),
            "replay_fingerprint_mismatches": [] if selected_replay is not None else replay_mismatches,
            "reference_behavioral_kill_status": (
                "verified_by_canonical_dual_backend_evidence"
                if source_reusable
                else "verified_by_supplemental_dual_backend_replay"
                if selected_replay is not None
                else "pending"
            ),
            "reference_replay_raw_status": (
                selected_replay.get("status") if selected_replay is not None else None
            ),
            "reference_property_activation_status": (
                selected_replay.get("property_activation_status")
                if selected_replay is not None
                else None
            ),
            "property_activation_claim_under_reference_deck": False,
            "fingerprint_mismatches": (
                []
                if reusable
                else sorted(set([*semantic_mismatches, *mismatches, *replay_mismatches]))
            ),
        }
    pending = sorted(
        mutation_id
        for mutation_id, record in negative_cases.items()
        if not record["hash_reusable"]
    )
    return {
        "schema_version": "v4-reference-testbench-certificate-v2",
        "evidence_source": "hash_bound_composite_reference_evidence_v2",
        "negative_evidence_policy": (
            "canonical_semantic_certification_plus_reference_deck_dual_backend_behavioral_kill_v1"
        ),
        "property_activation_claim_under_reference_deck": False,
        "reference_tb_sha256": deck_sha,
        "correct_dut_status": "pass" if gold_reusable else "canonical_deck_replay_pending",
        "gold_source_certification_sha256": file_sha(gold_certificate),
        "reference_profile_candidates": matching_profiles,
        "gold_fingerprint_mismatches": gold_mismatches,
        "negative_cases": negative_cases,
        "negative_suite_status": (
            "five_of_five_killed_behaviorally"
            if gold_reusable and not pending
            else "canonical_deck_replay_pending"
        ),
        "reused_negative_count": len(negative_cases) - len(pending),
        "source_reused_negative_count": source_reused_count,
        "supplemental_reused_negative_count": supplemental_reused_count,
        "pending_negative_count": len(pending),
        "pending_mutation_ids": pending,
        "evidence_rebinding_required": not gold_reusable or bool(pending),
        "simulation_rerun_required_for_materialization": False,
        "simulation_rerun_requirement_status": "not_determined_by_materialization",
    }


def build_bugfix_repair_certificate(
    source_task: Path,
    row: dict[str, Any],
    mutation_id: str,
    buggy_bundle: Path,
) -> dict[str, Any]:
    deck_sha = file_sha(source_task / "evaluator" / "score_tb.scs")
    current = current_source_evidence_identity(source_task)
    current_inputs = current["task_inputs"]
    gold_certificate = source_task / "evaluator" / "certification.json"
    gold_record = read_json(gold_certificate)
    gold_mismatches = source_record_mismatches(
        gold_record,
        current,
        task_input_keys=(
            "family_spec_sha256",
            "checker_profile_sha256",
            "harness_spec_sha256",
            "score_profile_sha256",
            "score_deck_sha256",
            "gold_bundle_sha256",
        ),
    )
    gold_reusable = (
        gold_record.get("status") in {"pass", "gate2_pass"}
        and (gold_record.get("checks") or {}).get("gold_bundle", {}).get("score_profile") == "pass"
        and not gold_mismatches
    )
    mutation = next(item for item in row["active_mutations"] if item["mutation_id"] == mutation_id)
    mutation_certificate = source_task / str(mutation["certification_path"])
    mutation_record = read_json(mutation_certificate)
    candidate_files = [buggy_bundle / relative for relative in current["artifact_paths"]]
    missing = [str(path) for path in candidate_files if not path.is_file()]
    if missing:
        raise SystemExit(f"{source_task.name}/{mutation_id}: incomplete bugfix bundle: {missing}")
    mutation_current = {
        **current_inputs,
        "deck_sha256": deck_sha,
        "profile_sha256": current_inputs["score_profile_sha256"],
        "candidate_bundle_sha256": aggregate_file_sha(candidate_files, base=buggy_bundle),
    }
    mutation_mismatches = source_record_mismatches(
        mutation_record,
        {**current, "task_inputs": mutation_current},
        task_input_keys=(
            "deck_sha256",
            "profile_sha256",
            "harness_spec_sha256",
            "gold_bundle_sha256",
            "candidate_bundle_sha256",
            "property_contract_sha256",
            "trace_contract_sha256",
        ),
    )
    seed_reusable = (
        mutation_record.get("outcome") == "killed_behaviorally"
        and (mutation_record.get("evaluators") or {}).get("spectre") == "compile_pass_behavior_fail"
        and not mutation_mismatches
    )
    return {
        "schema_version": "v4-bugfix-repair-certificate-v1",
        "evidence_source": "hash_bound_canonical_case_reuse_v1",
        "status": "pass" if gold_reusable and seed_reusable else "canonical_deck_replay_pending",
        "score_deck_sha256": deck_sha,
        "buggy_bundle_sha256": tree_sha(buggy_bundle),
        "gold_solution_sha256": tree_sha(source_task / "evaluator" / "solution"),
        "gold_repair_status": "pass" if gold_reusable else "canonical_deck_replay_pending",
        "buggy_seed_status": "killed_behaviorally" if seed_reusable else "canonical_deck_replay_pending",
        "gold_fingerprint_mismatches": gold_mismatches,
        "buggy_seed_fingerprint_mismatches": mutation_mismatches,
        "gold_source_certification_sha256": file_sha(gold_certificate),
        "mutation_source_certification_sha256": file_sha(mutation_certificate),
        "evidence_rebinding_required": not gold_reusable or not seed_reusable,
        "simulation_rerun_required_for_materialization": False,
        "simulation_rerun_requirement_status": "not_determined_by_materialization",
    }


def build_dut_view(
    output: Path,
    source: Path,
    source_reference: str,
    source_task: Path,
    row: dict[str, Any],
    spec: dict[str, Any],
    spec_sha: str,
) -> dict[str, Any]:
    family = str(row["canonical_dut_id"])
    task_dir = output / "tasks" / "dut" / source_task.name
    task_dir.mkdir(parents=True)
    write_text(task_dir / "instruction.md", render_dut_instruction(spec))
    copy_public_support(source_task, task_dir)
    contract = build_dut_public_contract(spec, f"v4-{family}")
    write_public_contract_views(task_dir, contract)
    evaluator = task_dir / "evaluator"
    evaluator.mkdir()
    write_json(evaluator / "score_policy.json", {
        "schema_version": "v4-dut-score-policy-v1",
        "task_id": f"v4-{family}",
        "candidate_artifacts": contract["target_artifacts"],
        "full_contract_pass_required": True,
        "spectre_final_judge": True,
        "source_checker_profile": source_rel(
            source_task / "evaluator" / "checker_profile.json", source, source_reference
        ),
    })
    bundle_sha = public_bundle_hash(task_dir)
    write_task_record(task_dir, common_task_record(
        task_id=f"v4-{family}", form="dut", family_id=family,
        directory=rel(task_dir, output), spec_sha=spec_sha,
        source_task=source_rel(source_task, source, source_reference),
        candidate_artifacts=contract["target_artifacts"], public_bundle_sha=bundle_sha,
    ))
    return {"task_id": f"v4-{family}", "form": "dut", "family_id": family, "task_dir": rel(task_dir, output)}


def build_testbench_view(
    output: Path,
    source: Path,
    source_reference: str,
    source_task: Path,
    row: dict[str, Any],
    spec: dict[str, Any],
    spec_sha: str,
    source_manifest_sha: str,
    seed_review: dict[str, Any],
    replay_evidence: dict[tuple[str, str, str], list[dict[str, Any]]] | None = None,
) -> dict[str, Any]:
    family = str(row["canonical_dut_id"])
    task_num = 500 + int(family)
    slug = source_task.name.split("-", 1)[1]
    task_dir = output / "tasks" / "testbench" / f"{task_num:03d}-{slug}-testbench"
    task_dir.mkdir(parents=True)
    copy_public_support(source_task, task_dir)
    supplied = task_dir / "supplied_dut"
    artifacts = copy_solution(source_task, supplied, spec)
    reference_source, contract, reference_profile = select_reference_testbench(
        source_task,
        spec,
        f"v4-{task_num:03d}",
        task_dir / "public_support",
    )
    write_text(task_dir / "instruction.md", render_testbench_instruction(contract))
    write_public_contract_views(task_dir, contract)
    evaluator = task_dir / "evaluator"
    evaluator.mkdir()
    suite = [str(item["mutation_id"]) for item in row["active_mutations"]]
    derivation = {
        "schema_version": "v4-derivation-manifest-v2",
        "family_id": family,
        "base_dut": {
            "canonical_task_id": f"v4-{family}",
            "canonical_task_slug": source_task.name,
            "family_spec_sha256": spec_sha,
            "source_release_manifest_sha256": source_manifest_sha,
            "mutation_catalog_sha256": row["hashes"]["mutation_catalog_sha256"],
            "canonical_score_tb_sha256": row["hashes"]["score_deck_sha256"],
            "reference_testbench_profile": reference_profile,
            "reference_testbench_sha256": file_sha(reference_source),
        },
        "negative_assignment": {"bugfix_seed": seed_review["mutation_id"], "testbench_suite": suite},
    }
    write_json(evaluator / "derivation_manifest.json", derivation)
    write_json(evaluator / "score_policy.json", {
        "schema_version": "v4-testbench-score-policy-v1",
        "task_id": f"v4-{task_num:03d}",
        "candidate_artifacts": ["testbench.scs"],
        "reference_gate": "all applicable public properties pass on supplied correct DUT",
        "negative_outcomes": ["killed_behaviorally", "survived", "invalid_run"],
        "full_credit": "reference_gate and five_of_five_killed_behaviorally",
        "kill_ratio_denominator": 5,
        "spectre_final_judge": True,
        "source_checker_profile": source_rel(
            source_task / "evaluator" / "checker_profile.json", source, source_reference
        ),
    })
    write_json(evaluator / "testbench_security_policy.json", contract["security_policy"])
    shutil.copy2(reference_source, evaluator / "reference_tb.scs")
    write_json(
        evaluator / "reference_certificate.json",
        build_reference_testbench_certificate(
            source_task,
            row,
            evaluator / "reference_tb.scs",
            replay_evidence,
        ),
    )
    bundle_sha = public_bundle_hash(task_dir)
    write_task_record(task_dir, common_task_record(
        task_id=f"v4-{task_num:03d}", form="testbench", family_id=family,
        directory=rel(task_dir, output), spec_sha=spec_sha,
        source_task=source_rel(source_task, source, source_reference),
        candidate_artifacts=["testbench.scs"],
        public_bundle_sha=bundle_sha,
    ))
    return {"task_id": f"v4-{task_num:03d}", "form": "testbench", "family_id": family, "task_dir": rel(task_dir, output)}


def build_bugfix_view(
    output: Path,
    source: Path,
    source_reference: str,
    source_task: Path,
    row: dict[str, Any],
    spec: dict[str, Any],
    spec_sha: str,
    source_manifest_sha: str, seed_review: dict[str, Any],
) -> dict[str, Any]:
    family = str(row["canonical_dut_id"])
    task_num = 1000 + int(family)
    slug = source_task.name.split("-", 1)[1]
    task_dir = output / "tasks" / "bugfix" / f"{task_num:04d}-{slug}-bugfix"
    task_dir.mkdir(parents=True)
    write_text(task_dir / "instruction.md", render_bugfix_instruction(spec))
    copy_public_support(source_task, task_dir)
    buggy = task_dir / "buggy_bundle"
    artifacts = copy_solution(source_task, buggy, spec)
    changed = overlay_mutation(source_task, seed_review["mutation_id"], buggy, artifacts)
    contract = build_bugfix_public_contract(spec, f"v4-{task_num}")
    write_public_contract_views(task_dir, contract)
    evaluator = task_dir / "evaluator"
    evaluator.mkdir()
    write_json(evaluator / "score_policy.json", {
        "schema_version": "v4-bugfix-score-policy-v1",
        "task_id": f"v4-{task_num}",
        "candidate_artifacts": artifacts,
        "artifact_mode": spec["artifact_contract"]["mode"],
        "full_contract_pass_required": True,
        "spectre_final_judge": True,
        "source_checker_profile": source_rel(
            source_task / "evaluator" / "checker_profile.json", source, source_reference
        ),
        "gold_solution_tree_sha256": tree_sha(source_task / "evaluator" / "solution"),
    })
    write_json(evaluator / "derivation_manifest.json", {
        "schema_version": "v4-derivation-manifest-v2",
        "family_id": family,
        "base_dut": {
            "canonical_task_id": f"v4-{family}",
            "canonical_task_slug": source_task.name,
            "family_spec_sha256": spec_sha,
            "source_release_manifest_sha256": source_manifest_sha,
            "mutation_catalog_sha256": row["hashes"]["mutation_catalog_sha256"],
        },
        "negative_assignment": {
            "bugfix_seed": seed_review["mutation_id"],
            "testbench_suite": [str(item["mutation_id"]) for item in row["active_mutations"]],
        },
        "selection_evidence": seed_review,
        "private_materialization": {
            "changed_artifacts": changed,
            "buggy_bundle_sha256": tree_sha(buggy),
        },
    })
    write_json(evaluator / "gold_repair_reference.json", {
        "schema_version": "v4-gold-repair-reference-v1",
        "source_solution": source_rel(
            source_task / "evaluator" / "solution", source, source_reference
        ),
        "solution_tree_sha256": tree_sha(source_task / "evaluator" / "solution"),
        "gold_dut_certification_sha256": row["hashes"]["task_certification_sha256"],
        "simulation_rerun_required_for_materialization": False,
    })
    write_json(
        evaluator / "repair_certificate.json",
        build_bugfix_repair_certificate(source_task, row, seed_review["mutation_id"], buggy),
    )
    bundle_sha = public_bundle_hash(task_dir)
    write_task_record(task_dir, common_task_record(
        task_id=f"v4-{task_num}", form="bugfix", family_id=family,
        directory=rel(task_dir, output), spec_sha=spec_sha,
        source_task=source_rel(source_task, source, source_reference),
        candidate_artifacts=artifacts,
        public_bundle_sha=bundle_sha,
    ))
    return {"task_id": f"v4-{task_num}", "form": "bugfix", "family_id": family, "task_dir": rel(task_dir, output)}


def build_reference_replay_plan(
    output: Path,
    task_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    mutations: list[dict[str, Any]] = []
    for task in task_rows:
        if task["form"] != "testbench":
            continue
        family = str(task["family_id"])
        task_dir = output / str(task["task_dir"])
        certificate = read_json(task_dir / "evaluator" / "reference_certificate.json")
        derivation = read_json(task_dir / "evaluator" / "derivation_manifest.json")
        profile = str((derivation.get("base_dut") or {}).get("reference_testbench_profile") or "")
        plan_path = GATE2_MUTATION_PLANS / f"{family}.json"
        if not plan_path.is_file():
            raise SystemExit(f"missing canonical mutation plan for reference replay: {plan_path}")
        family_plan = (read_json(plan_path).get("families") or {}).get(family) or {}
        source_slug = str(family_plan.get("source_slug") or "")
        mutation_specs = family_plan.get("mutations") or {}
        diagnostic_patterns = family_plan.get("diagnostic_patterns") or {}
        for mutation_id, case in sorted((certificate.get("negative_cases") or {}).items()):
            if case.get("source_hash_reusable") is True:
                continue
            mutation = mutation_specs.get(mutation_id)
            if not isinstance(mutation, dict):
                raise SystemExit(f"{family}/{mutation_id}: missing mutation plan entry")
            mutations.append({
                "canonical_id": family,
                "source_slug": source_slug,
                "mutation_id": mutation_id,
                "profile": profile,
                "partition": str(mutation.get("partition") or "H"),
                "fault_class": str(mutation.get("fault_class") or ""),
                "trigger_condition": str(mutation.get("trigger_condition") or ""),
                "violated_property_ids": list(mutation.get("violated_property_ids") or []),
                "diagnostic_patterns": list(diagnostic_patterns.get(mutation_id) or []),
                "reference_deck_sha256": case.get("reference_deck_sha256"),
                "source_certification_sha256": case.get("source_certification_sha256"),
                "source_fingerprint_mismatches": case.get("source_fingerprint_mismatches") or [],
            })
    mutations.sort(key=lambda item: (int(item["canonical_id"]), item["mutation_id"], item["profile"]))
    return {
        "schema_version": "v4-reference-testbench-replay-plan-v1",
        "task_ids": sorted({item["canonical_id"] for item in mutations}, key=int),
        "mutations": mutations,
        "summary": {
            "family_count": len({item["canonical_id"] for item in mutations}),
            "mutation_count": len(mutations),
            "profile_counts": {
                profile: sum(item["profile"] == profile for item in mutations)
                for profile in ("feedback", "score")
            },
            "reason": "canonical selected-profile evidence does not bind to the single reference testbench deck",
        },
    }


def write_selected_reference_replay_evidence(
    output: Path,
    task_rows: list[dict[str, Any]],
    replay_lookup: dict[tuple[str, str, str], list[dict[str, Any]]],
    replay_sources: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    selected_hashes: set[str] = set()
    for task in task_rows:
        if task["form"] != "testbench":
            continue
        certificate = read_json(
            output / str(task["task_dir"]) / "evaluator" / "reference_certificate.json"
        )
        for case in (certificate.get("negative_cases") or {}).values():
            if case.get("evidence_source") == "supplemental_reference_deck_replay":
                selected_hashes.add(str(case.get("replay_record_sha256") or ""))
    all_records = [record for records in replay_lookup.values() for record in records]
    selected = [record for record in all_records if record.get("record_sha256") in selected_hashes]
    selected.sort(key=lambda item: (int(item["canonical_id"]), item["mutation_id"], item["profile"]))
    if len(selected) != len(selected_hashes):
        found = {str(item.get("record_sha256") or "") for item in selected}
        raise SystemExit(f"selected reference replay rows are missing: {sorted(selected_hashes - found)}")
    used_source_hashes = {str(item["source_evidence_sha256"]) for item in selected}
    raw_status_counts = {
        status: sum(item.get("status") == status for item in selected)
        for status in sorted({str(item.get("status") or "") for item in selected})
    }
    payload = {
        "schema_version": "v4-reference-testbench-replay-evidence-v1",
        "spectre_final_judge": True,
        "source_evidence": [replay_sources[value] for value in sorted(used_source_hashes)],
        "rows": selected,
        "summary": {
            "row_count": len(selected),
            "behaviorally_certified_row_count": len(selected),
            "diagnostic_only_nonpass_count": sum(
                item.get("status") != "PASS" for item in selected
            ),
            "raw_status_counts": raw_status_counts,
            "family_count": len({item["canonical_id"] for item in selected}),
            "profile_counts": {
                profile: sum(item["profile"] == profile for item in selected)
                for profile in ("feedback", "score")
            },
        },
    }
    write_json(output / "REFERENCE_REPLAY_EVIDENCE.json", payload)
    return payload


def refresh_public_task_views(output: Path, task_rows: list[dict[str, Any]]) -> dict[str, int]:
    """Regenerate public projections without touching private evaluator assets."""
    counts: dict[str, int] = {"dut": 0, "testbench": 0, "bugfix": 0}
    for task in task_rows:
        task_dir = output / str(task["task_dir"])
        record_path = task_dir / "TASK_RECORD.json"
        record = read_json(record_path)
        source_task = PACKAGE_ROOT / str(record["canonical_dut_source"])
        spec = read_json(source_task / "evaluator" / "family_spec.json")
        task_id = str(task["task_id"])
        form = str(task["form"])
        if form == "dut":
            contract = build_dut_public_contract(spec, task_id)
            write_text(task_dir / "instruction.md", render_dut_instruction(spec))
        elif form == "testbench":
            reference_source, contract, _ = select_reference_testbench(
                source_task,
                spec,
                task_id,
                source_task / "public" / "task" / "public_support",
            )
            write_text(task_dir / "instruction.md", render_testbench_instruction(contract))
        elif form == "bugfix":
            contract = build_bugfix_public_contract(spec, task_id)
            write_text(task_dir / "instruction.md", render_bugfix_instruction(spec))
        else:
            raise SystemExit(f"unsupported task form while refreshing public views: {form}")
        copy_public_support(source_task, task_dir)
        write_public_contract_views(task_dir, contract)
        record["public_bundle_sha256"] = public_bundle_hash(task_dir)
        write_json(record_path, record)
        counts[form] += 1
    return counts


def install_prompt_assets(output: Path) -> dict[str, dict[str, Any]]:
    target = output / "prompt_modes" / "skills"
    target.mkdir(parents=True, exist_ok=True)
    records: dict[str, dict[str, Any]] = {}
    for source in sorted(PROMPT_ASSETS.glob("*.md")):
        if source.name not in COMPONENT_METADATA:
            raise SystemExit(f"prompt component lacks metadata: {source.name}")
        destination = target / source.name
        shutil.copy2(source, destination)
        metadata = COMPONENT_METADATA[source.name]
        fingerprint = component_fingerprint(source.name, destination)
        provenance = CADENCE_SKILL_PROVENANCE.get(source.name)
        if provenance is None:
            provenance = PROJECT_COMPONENT_PROVENANCE[source.name]
        records[source.name] = {
            "path": rel(destination, output),
            **fingerprint,
            "stable_id": metadata["stable_id"],
            "kind": metadata["kind"],
            "semantic_version": "1.0.0",
            "applicable_forms": metadata["applicable_forms"],
            "license": {"status": "repository_license_pending", "spdx": None},
            "provenance": provenance,
        }
    write_json(output / "prompt_modes" / "skills" / "manifest.json", {
        "schema_version": "v4-skill-manifest-v1",
        "reference_tokenizer": REFERENCE_TOKENIZER,
        "skills": records,
    })
    write_json(output / "prompt_modes" / "modes.json", {
        "schema_version": "v4-prompt-mode-registry-v2",
        "modes": MODES,
        "composition_order": ["canonical_instruction_and_public_inputs", "form_skill", "feedback_core_and_form_adapter", "neutral_wrapper"],
        "transport_normalization": {
            "semantics_blind": True,
            "direct": "last_complete_labeled_bundle_v1",
            "agentic": "unique_common_submission_prefix_v1",
            "protocol_compliance_reported_separately": True,
        },
        "working_token_budget": "runner_supplied_same_ceiling_within_comparison_stratum",
        "wall_time_policy": "safety_limit_not_ability_budget",
    })
    return records


def iter_public_inputs(task_dir: Path, form: str) -> Iterable[Path]:
    yield task_dir / "instruction.md"
    yield task_dir / "solver_contract.json"
    if form == "testbench":
        yield from sorted((task_dir / "supplied_dut").rglob("*.va"))
    elif form == "bugfix":
        yield from sorted((task_dir / "buggy_bundle").rglob("*.va"))
    support = task_dir / "public_support"
    if support.is_dir():
        yield from sorted(path for path in support.rglob("*") if path.is_file())


def write_prompt_records(output: Path, task_rows: list[dict[str, Any]], skills: dict[str, dict[str, Any]]) -> None:
    path = output / "prompt_modes" / "PROMPT_RECORDS.jsonl"
    with path.open("w", encoding="utf-8") as handle:
        for task in task_rows:
            task_dir = output / task["task_dir"]
            instruction_sha = file_sha(task_dir / "instruction.md")
            input_hashes = {rel(item, task_dir): file_sha(item) for item in iter_public_inputs(task_dir, task["form"])}
            solver_contract_sha = file_sha(task_dir / "solver_contract.json")
            for mode, policy in MODES.items():
                public_components = [
                    component_fingerprint(
                        "instruction" if item.name == "instruction.md" else f"public_input:{rel(item, task_dir)}",
                        item,
                    )
                    for item in iter_public_inputs(task_dir, task["form"])
                ]
                components = [item["id"] for item in public_components]
                skill_ids: list[str] = []
                if policy["form_skill"]:
                    skill_ids.append(FORM_SKILLS[task["form"]])
                if policy["feedback_skill"]:
                    skill_ids.extend(["feedback_core.md", FEEDBACK_ADAPTERS[task["form"]]])
                components.extend([*skill_ids, NEUTRAL_WRAPPER])
                static_components = public_components + [
                    {
                        "id": name,
                        "sha256": skills[name]["sha256"],
                        "bytes": skills[name]["bytes"],
                        "token_counts": skills[name]["token_counts"],
                    }
                    for name in [*skill_ids, NEUTRAL_WRAPPER]
                ]
                record = {
                    "schema_version": "v4-prompt-record-v2",
                    "task_id": task["task_id"],
                    "family_id": task["family_id"],
                    "form": task["form"],
                    "mode": mode,
                    "process": policy["process"],
                    "feedback_cli_available": policy["feedback_cli"],
                    "canonical_instruction_sha256": instruction_sha,
                    "solver_contract_sha256": solver_contract_sha,
                    "base_public_input_hashes": input_hashes,
                    "public_input_hashes": input_hashes,
                    "component_order": components,
                    "static_components": static_components,
                    "reference_tokenizer": REFERENCE_TOKENIZER,
                    "skill_hashes": {name: skills[name]["sha256"] for name in skill_ids},
                    "response_protocol": (
                        "v4-exact-artifact-blocks-with-semantic-blind-normalization-v2"
                        if policy["process"] == "direct_one_shot"
                        else "v4-workspace-finalizer-with-prefix-normalization-v2"
                    ),
                }
                handle.write(json.dumps(record, sort_keys=True) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument(
        "--source-reference",
        help="Package-relative path recorded for an external temporary source release.",
    )
    parser.add_argument(
        "--reference-replay-evidence",
        type=Path,
        action="append",
        default=[],
        help="Raw v4 mutation evidence collected under each Testbench reference deck/profile.",
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    source = args.source.expanduser().resolve()
    source_reference = resolve_source_reference(source, args.source_reference)
    replay_lookup, replay_sources = load_reference_replay_evidence(
        args.reference_replay_evidence
    )
    output = args.output.expanduser().resolve()
    if output.exists():
        if not args.force:
            raise SystemExit(f"output exists; pass --force to replace it: {output}")
        shutil.rmtree(output)
    output.mkdir(parents=True)

    denominator_path = source / "score_denominator_manifest.json"
    denominator = read_json(denominator_path)
    rows = denominator.get("tasks") or []
    if len(rows) != 400:
        raise SystemExit("source release must contain exactly 400 canonical DUT rows")
    source_manifest_sha = file_sha(denominator_path)
    task_rows: list[dict[str, Any]] = []
    seed_rows: list[dict[str, Any]] = []
    for row in rows:
        family = str(row["canonical_dut_id"])
        source_task = source / str(row["release_dir"])
        spec_path = source_task / "evaluator" / "family_spec.json"
        spec = read_json(spec_path)
        if str(spec.get("family_id")) != family:
            raise SystemExit(f"{source_task.name}: family spec ID mismatch")
        spec_sha = file_sha(spec_path)
        seed_review = select_bugfix_seed(row)
        seed_rows.append({"family_id": family, **seed_review})
        task_rows.extend([
            build_dut_view(
                output, source, source_reference, source_task, row, spec, spec_sha
            ),
            build_testbench_view(
                output,
                source,
                source_reference,
                source_task,
                row,
                spec,
                spec_sha,
                source_manifest_sha,
                seed_review,
                replay_lookup,
            ),
            build_bugfix_view(
                output,
                source,
                source_reference,
                source_task,
                row,
                spec,
                spec_sha,
                source_manifest_sha,
                seed_review,
            ),
        ])

    task_rows.sort(key=lambda item: (item["form"], int(item["family_id"])))
    skills = install_prompt_assets(output)
    write_prompt_records(output, task_rows, skills)
    write_json(output / "BUGFIX_SEED_REVIEW.json", {
        "schema_version": "v4-bugfix-seed-review-v1",
        "selection_policy": "semantic_fault_complexity_v1",
        "families": seed_rows,
    })
    write_json(output / "TASK_INDEX.json", {"schema_version": "v4-tri-form-task-index-v1", "tasks": task_rows})
    replay_plan = build_reference_replay_plan(output, task_rows)
    write_json(output / "REFERENCE_REPLAY_PLAN.json", replay_plan)
    replay_evidence = write_selected_reference_replay_evidence(
        output,
        task_rows,
        replay_lookup,
        replay_sources,
    )
    counts = {form: sum(item["form"] == form for item in task_rows) for form in ("dut", "testbench", "bugfix")}
    reference_certificates = [
        read_json(output / item["task_dir"] / "evaluator" / "reference_certificate.json")
        for item in task_rows
        if item["form"] == "testbench"
    ]
    pending_reference_cases = sum(
        int(certificate.get("pending_negative_count") or 0)
        + int(certificate.get("correct_dut_status") != "pass")
        for certificate in reference_certificates
    )
    certified_reference_families = sum(
        certificate.get("negative_suite_status") == "five_of_five_killed_behaviorally"
        and certificate.get("correct_dut_status") == "pass"
        for certificate in reference_certificates
    )
    manifest = {
        "schema_version": "v4-tri-form-release-manifest-v1",
        "release_status": (
            "package_materialized_behavior_evidence_ready"
            if pending_reference_cases == 0 and certified_reference_families == 400
            else "package_materialized_behavior_evidence_pending"
        ),
        "family_count": 400,
        "task_count": len(task_rows),
        "task_counts": counts,
        "source_release": source_reference,
        "source_score_denominator_manifest_sha256": source_manifest_sha,
        "source_active_mutation_count": denominator.get("active_mutation_count"),
        "active_mutations_per_family": denominator.get("active_mutations_per_family"),
        "spectre_final_judge": True,
        "reference_testbench_certified_family_count": certified_reference_families,
        "reference_testbench_pending_case_count": pending_reference_cases,
        "evidence_rebinding_required_case_count": pending_reference_cases,
        "reference_replay_plan_case_count": len(replay_plan["mutations"]),
        "reference_replay_evidence_case_count": len(replay_evidence["rows"]),
        "simulation_rerun_count_for_materialization": 0,
        "simulation_rerun_requirement_status": "not_determined_by_materialization",
        "prompt_record_count": len(task_rows) * len(MODES),
        "tasks_index": "TASK_INDEX.json",
        "materialized_artifact_sha256": materialized_artifact_hashes(output),
    }
    write_json(output / "MANIFEST.json", manifest)
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
