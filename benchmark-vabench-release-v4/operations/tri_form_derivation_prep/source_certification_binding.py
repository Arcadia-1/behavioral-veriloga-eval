#!/usr/bin/env python3
"""Validate source certification inputs before tri-form evidence reuse."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


RECERTIFICATION_EVIDENCE_SCHEMA = "v4-benchmarkv4-recertification-evidence-v1"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_sha_by_file_hash(path: Path, *, excluded_names: set[str] | None = None) -> str:
    """Match the canonical DUT evidence tree hash used by v4 certificates."""
    excluded_names = excluded_names or set()
    digest = hashlib.sha256()
    for item in sorted(path.rglob("*")):
        if not item.is_file() or item.name in excluded_names:
            continue
        digest.update(item.relative_to(path).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(file_sha(item).encode("ascii"))
        digest.update(b"\0")
    return digest.hexdigest()


def _check_hash(
    *,
    family: str,
    label: str,
    path: Path,
    expected: Any,
    problems: list[str],
) -> bool:
    if not path.is_file():
        problems.append(f"{family}: source {label} is missing")
        return False
    actual = file_sha(path)
    if expected != actual:
        problems.append(f"{family}: source {label} mismatch")
        return False
    return True


def _check_mapping(
    *,
    family: str,
    label: str,
    actual: dict[str, Any],
    expected: dict[str, str],
    problems: list[str],
) -> bool:
    valid = True
    for name, sha in expected.items():
        if actual.get(name) != sha:
            problems.append(f"{family}: source {label} mismatch: {name}")
            valid = False
    return valid


def _task_input_hashes(source_task: Path) -> tuple[dict[str, str], dict[str, str]]:
    evaluator = source_task / "evaluator"
    public = source_task / "public" / "task"
    certificate_inputs = {
        "checker_profile": file_sha(evaluator / "checker_profile.json"),
        "family_spec": file_sha(evaluator / "family_spec.json"),
        "feedback_profile": file_sha(evaluator / "profiles" / "feedback.json"),
        "gold_bundle": tree_sha_by_file_hash(evaluator / "solution"),
        "harness_spec": file_sha(evaluator / "harness_spec.json"),
        "score_profile": file_sha(evaluator / "profiles" / "score.json"),
    }
    component_inputs = {
        "checker_profile_sha256": certificate_inputs["checker_profile"],
        "family_spec_sha256": certificate_inputs["family_spec"],
        "feedback_deck_sha256": file_sha(public / "feedback_tb.scs"),
        "feedback_profile_sha256": certificate_inputs["feedback_profile"],
        "gold_bundle_sha256": certificate_inputs["gold_bundle"],
        "harness_spec_sha256": certificate_inputs["harness_spec"],
        "score_deck_sha256": file_sha(evaluator / "score_tb.scs"),
        "score_profile_sha256": certificate_inputs["score_profile"],
    }
    return certificate_inputs, component_inputs


def _safe_release_path(release: Path, relative: Any, problems: list[str], prefix: str) -> Path | None:
    value = str(relative or "")
    candidate = Path(value)
    if not value or candidate.is_absolute() or ".." in candidate.parts:
        problems.append(f"{prefix}: evidence path is not release-relative: {value!r}")
        return None
    return release / candidate


def _check_evidence_file_record(
    *,
    release: Path,
    record: dict[str, Any],
    problems: list[str],
    prefix: str,
) -> bool:
    path = _safe_release_path(release, record.get("path"), problems, prefix)
    if path is None:
        return False
    if not path.is_file():
        problems.append(f"{prefix}: evidence-bound file is missing: {record.get('path')!r}")
        return False
    actual = file_sha(path)
    if actual != record.get("sha256"):
        problems.append(f"{prefix}: evidence-bound file hash mismatch: {record.get('path')!r}")
        return False
    return True


def _package_relative_path(release: Path, path: Path) -> str:
    package_root = release.parents[1]
    try:
        return path.resolve().relative_to(package_root).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def _load_recertification_evidence(
    *,
    release: Path | None,
    evidence_path: Path | None,
) -> tuple[dict[str, dict[str, Any]], dict[str, Any] | None, list[str]]:
    if evidence_path is None:
        return {}, None, []
    evidence_path = evidence_path.expanduser().resolve()
    if not evidence_path.is_file():
        return {}, None, [f"recertification evidence is missing: {evidence_path}"]
    evidence = read_json(evidence_path)
    problems: list[str] = []
    if evidence.get("schema_version") != RECERTIFICATION_EVIDENCE_SCHEMA:
        problems.append("recertification evidence schema mismatch")

    summary = evidence.get("summary") or {}
    tasks = evidence.get("tasks") or []
    expected_task_count = len(tasks)
    expected_negative_count = 5 * expected_task_count
    expected_family_count = len({str(task.get("family_id") or "") for task in tasks})
    expected_summary = {
        "task_count": expected_task_count,
        "family_count": expected_family_count,
        "reference_pass_count": expected_task_count,
        "negative_case_count": expected_negative_count,
        "evas_behavioral_kill_count": expected_negative_count,
        "spectre_behavioral_kill_count": expected_negative_count,
        "untriaged_warning_count": 0,
        "status": "pass",
    }
    for key, expected in expected_summary.items():
        if summary.get(key) != expected:
            problems.append(f"recertification evidence summary mismatch: {key}")

    task_index: dict[str, dict[str, Any]] = {}
    if release is not None:
        release = release.expanduser().resolve()
        task_index_path = release / "TASK_INDEX.json"
        if not task_index_path.is_file():
            problems.append("release TASK_INDEX.json is missing for recertification evidence binding")
        elif (evidence.get("release") or {}).get("task_index_sha256") != file_sha(task_index_path):
            problems.append("recertification evidence TASK_INDEX hash mismatch")
        else:
            task_index = {
                str(row.get("task_id") or ""): row
                for row in read_json(task_index_path).get("tasks") or []
            }

    coverage: dict[str, dict[str, Any]] = {}
    for task in tasks:
        task_id = str(task.get("task_id") or "")
        family = str(task.get("family_id") or "")
        prefix = f"{family or task_id}: recertification evidence"
        if not task_id or not family:
            problems.append("recertification evidence task is missing task_id or family_id")
            continue
        if task.get("form") != "testbench":
            problems.append(f"{prefix}: task form is not testbench")
        if task.get("status") != "pass" or task.get("reference_gate") != "pass":
            problems.append(f"{prefix}: task status/reference gate is not pass")
        if task.get("kill_denominator") != 5 or task.get("killed_count") != 5:
            problems.append(f"{prefix}: exact-five kill result mismatch")
        if task.get("untriaged_warning_count") != 0:
            problems.append(f"{prefix}: untriaged warnings are present")

        indexed = task_index.get(task_id)
        task_dir = None
        if release is not None:
            if indexed is None:
                problems.append(f"{prefix}: task_id is absent from release TASK_INDEX")
            else:
                if indexed.get("form") != "testbench":
                    problems.append(f"{prefix}: TASK_INDEX row is not testbench")
                if str(indexed.get("family_id") or "") != family:
                    problems.append(f"{prefix}: TASK_INDEX family mismatch")
                if str(indexed.get("task_dir") or "") != str(task.get("task_dir") or ""):
                    problems.append(f"{prefix}: TASK_INDEX task_dir mismatch")
                task_dir = _safe_release_path(release, indexed.get("task_dir"), problems, prefix)

        case_ids: set[str] = set()
        negative_case_ids: set[str] = set()
        for case in task.get("cases") or []:
            case_id = str(case.get("case_id") or "")
            if not case_id:
                problems.append(f"{prefix}: case is missing case_id")
                continue
            if case_id in case_ids:
                problems.append(f"{prefix}: duplicate case_id {case_id}")
            case_ids.add(case_id)
            if case.get("role") == "negative":
                negative_case_ids.add(case_id)
            if case_id == "correct":
                if case.get("outcome") != "reference_pass":
                    problems.append(f"{prefix}: correct case is not reference_pass")
            else:
                if case.get("outcome") != "killed_behaviorally":
                    problems.append(f"{prefix}: negative case {case_id} is not killed")
            if (case.get("evas") or {}).get("status") not in {"reference_pass", "mutation_killed"}:
                problems.append(f"{prefix}: case {case_id} EVAS status mismatch")
            if (case.get("spectre") or {}).get("outcome") != case.get("outcome"):
                problems.append(f"{prefix}: case {case_id} Spectre outcome mismatch")
            for index, record in enumerate(case.get("candidate_files") or []):
                if release is not None and isinstance(record, dict):
                    _check_evidence_file_record(
                        release=release,
                        record=record,
                        problems=problems,
                        prefix=f"{prefix}: case {case_id} candidate {index}",
                    )
        if case_ids != {"correct", *negative_case_ids} or len(negative_case_ids) != 5:
            problems.append(f"{prefix}: cases are not correct plus exact-five negatives")

        if release is not None:
            for label, record in (
                ("reference_tb", task.get("reference_tb") or {}),
                ("checker profile", (task.get("checker") or {}).get("profile") or {}),
            ):
                if isinstance(record, dict):
                    _check_evidence_file_record(
                        release=release,
                        record=record,
                        problems=problems,
                        prefix=f"{prefix}: {label}",
                    )
                else:
                    problems.append(f"{prefix}: {label} file record is malformed")
            if task_dir is not None and task_dir.is_dir():
                score_path = task_dir / "evaluator" / "score_policy.json"
                if not score_path.is_file():
                    problems.append(f"{prefix}: score_policy.json is missing")
                else:
                    score = read_json(score_path)
                    expected_negatives = set(score.get("negative_suite_mutation_ids") or [])
                    if (
                        len(expected_negatives) != 5
                        or score.get("kill_ratio_denominator") != 5
                        or expected_negatives != negative_case_ids
                    ):
                        problems.append(f"{prefix}: score policy does not match evidence cases")

        coverage[family] = {
            "task_id": task_id,
            "negative_case_ids": negative_case_ids,
            "case_ids": case_ids,
        }

    if problems:
        return {}, None, problems

    evidence_summary = {
        "schema_version": evidence.get("schema_version"),
        "path": (
            _package_relative_path(release, evidence_path)
            if release is not None
            else evidence_path.as_posix()
        ),
        "sha256": file_sha(evidence_path),
        "family_ids": sorted(coverage),
        "task_ids": sorted(task["task_id"] for task in coverage.values()),
        "evaluators": ["evas", "spectre"],
        "reference_pass_count": summary.get("reference_pass_count"),
        "negative_case_count": summary.get("negative_case_count"),
        "evas_behavioral_kill_count": summary.get("evas_behavioral_kill_count"),
        "spectre_behavioral_kill_count": summary.get("spectre_behavioral_kill_count"),
        "untriaged_warning_count": summary.get("untriaged_warning_count"),
    }
    return coverage, evidence_summary, []


def inspect_source_certification_reuse(
    source: Path,
    source_rows: dict[str, dict[str, Any]],
    *,
    release: Path | None = None,
    recertification_evidence_path: Path | None = None,
) -> tuple[dict[str, Any], list[str]]:
    """Return exact reusable counts and every broken source hash binding.

    Outer denominator hashes are insufficient: a task record and certificate
    can remain byte-identical after one of their declared inputs changes.  This
    routine therefore validates the transitive task-record and certificate
    inputs before any tri-form release claims evidence reuse.
    """
    problems: list[str] = []
    reusable_gold = 0
    reusable_negatives = 0
    invalid_gold: list[str] = []
    invalid_negatives: list[str] = []
    stale_families: set[str] = set()
    negative_total = 0

    for family, row in sorted(source_rows.items()):
        source_task = source / str(row.get("release_dir") or "")
        evaluator = source_task / "evaluator"
        public = source_task / "public" / "task"
        row_hashes = row.get("hashes") or {}
        gold_valid = True
        if not source_task.is_dir():
            problems.append(f"{family}: source task directory is missing")
            invalid_gold.append(family)
            stale_families.add(family)
            negative_total += len(row.get("active_mutations") or [])
            invalid_negatives.extend(
                f"{family}/{item.get('mutation_id')}" for item in row.get("active_mutations") or []
            )
            continue

        record_path = evaluator / "task_record.json"
        certification_path = evaluator / "certification.json"
        for label, path, expected in (
            ("task record hash", record_path, row_hashes.get("task_record_sha256")),
            ("gold certification hash", certification_path, row_hashes.get("task_certification_sha256")),
            ("mutation catalog hash", evaluator / "mutation_catalog.json", row_hashes.get("mutation_catalog_sha256")),
            ("score deck hash", evaluator / "score_tb.scs", row_hashes.get("score_deck_sha256")),
        ):
            if not _check_hash(
                family=family, label=label, path=path, expected=expected, problems=problems
            ):
                gold_valid = False

        if record_path.is_file():
            record = read_json(record_path)
            evaluator_hashes = record.get("evaluator_hashes") or {}
            for relative, expected in sorted(evaluator_hashes.items()):
                # ``solution_tree`` is a historical opaque aggregate.  The
                # certificate's gold_bundle hash below binds the actual tree.
                if relative == "solution_tree":
                    continue
                path = evaluator / relative
                if not _check_hash(
                    family=family,
                    label=f"task record evaluator hash mismatch: {relative}",
                    path=path,
                    expected=expected,
                    problems=problems,
                ):
                    gold_valid = False
            public_hashes = record.get("public_hashes") or {}
            for relative, expected in sorted(public_hashes.items()):
                if not _check_hash(
                    family=family,
                    label=f"task record public hash mismatch: {relative}",
                    path=public / relative,
                    expected=expected,
                    problems=problems,
                ):
                    gold_valid = False
            readiness = record.get("readiness_evidence") or {}
            readiness_path = source_task / str(readiness.get("path") or "")
            if not _check_hash(
                family=family,
                label="task record readiness evidence hash",
                path=readiness_path,
                expected=readiness.get("sha256"),
                problems=problems,
            ):
                gold_valid = False

        if certification_path.is_file():
            certification = read_json(certification_path)
            evaluators = certification.get("evaluators") or {}
            if certification.get("status") != "gate2_pass":
                problems.append(f"{family}: source gold certification is not gate2_pass")
                gold_valid = False
            for evaluator_name in ("evas", "spectre"):
                if (evaluators.get(evaluator_name) or {}).get("status") != "pass":
                    problems.append(f"{family}: source gold lacks {evaluator_name} PASS")
                    gold_valid = False
            try:
                certificate_inputs, component_inputs = _task_input_hashes(source_task)
            except FileNotFoundError as exc:
                problems.append(f"{family}: source gold certification input is missing: {exc.filename}")
                gold_valid = False
            else:
                for profile_name in ("feedback", "score"):
                    profile_path = evaluator / "profiles" / f"{profile_name}.json"
                    profile = read_json(profile_path)
                    if profile.get("harness_spec_sha256") != certificate_inputs["harness_spec"]:
                        problems.append(
                            f"{family}: source gold {profile_name} profile "
                            "harness_spec_sha256 mismatch"
                        )
                        gold_valid = False
                if not _check_mapping(
                    family=family,
                    label="gold certification input hash",
                    actual=certification.get("input_hashes") or {},
                    expected=certificate_inputs,
                    problems=problems,
                ):
                    gold_valid = False
                task_inputs = ((certification.get("component_fingerprints") or {}).get("task_inputs") or {})
                if not _check_mapping(
                    family=family,
                    label="gold certification component hash",
                    actual=task_inputs,
                    expected=component_inputs,
                    problems=problems,
                ):
                    gold_valid = False

        if gold_valid:
            reusable_gold += 1
        else:
            invalid_gold.append(family)
            stale_families.add(family)

        for mutation in row.get("active_mutations") or []:
            negative_total += 1
            mutation_id = str(mutation.get("mutation_id") or "")
            pair = f"{family}/{mutation_id}"
            cert_path = source_task / str(mutation.get("certification_path") or "")
            bundle = cert_path.parent
            negative_valid = _check_hash(
                family=family,
                label=f"negative {mutation_id} certification hash",
                path=cert_path,
                expected=mutation.get("certification_sha256"),
                problems=problems,
            )
            if bundle.is_dir():
                actual_bundle_sha = tree_sha_by_file_hash(bundle)
                if mutation.get("mutation_bundle_sha256") != actual_bundle_sha:
                    problems.append(f"{family}: source negative {mutation_id} bundle hash mismatch")
                    negative_valid = False
            else:
                problems.append(f"{family}: source negative {mutation_id} bundle is missing")
                negative_valid = False
            if cert_path.is_file():
                negative_certification = read_json(cert_path)
                negative_evaluators = negative_certification.get("evaluators") or {}
                if negative_certification.get("outcome") != "killed_behaviorally":
                    problems.append(f"{family}: source negative {mutation_id} was not killed behaviorally")
                    negative_valid = False
                for evaluator_name in ("evas", "spectre"):
                    if negative_evaluators.get(evaluator_name) != "compile_pass_behavior_fail":
                        problems.append(
                            f"{family}: source negative {mutation_id} lacks {evaluator_name} behavioral kill"
                        )
                        negative_valid = False
                try:
                    negative_inputs = {
                        "checker_profile_sha256": file_sha(evaluator / "checker_profile.json"),
                        "harness_spec_sha256": file_sha(evaluator / "harness_spec.json"),
                    }
                    accepted_profile_hashes = {
                        file_sha(evaluator / "profiles" / "feedback.json"),
                        file_sha(evaluator / "profiles" / "score.json"),
                    }
                except FileNotFoundError as exc:
                    problems.append(
                        f"{family}: source negative {mutation_id} input is missing: {exc.filename}"
                    )
                    negative_valid = False
                else:
                    if not _check_mapping(
                        family=family,
                        label=f"negative {mutation_id} input hash",
                        actual=negative_certification.get("inputs") or {},
                        expected=negative_inputs,
                        problems=problems,
                    ):
                        negative_valid = False
                    declared_profile = (negative_certification.get("inputs") or {}).get(
                        "profile_sha256"
                    )
                    if declared_profile not in accepted_profile_hashes:
                        problems.append(
                            f"{family}: source negative {mutation_id} input hash mismatch: "
                            "profile_sha256"
                        )
                        negative_valid = False
            if negative_valid:
                reusable_negatives += 1
            else:
                invalid_negatives.append(pair)
                stale_families.add(family)

    recertification_coverage, recertification_summary, evidence_problems = _load_recertification_evidence(
        release=release,
        evidence_path=recertification_evidence_path,
    )
    original_invalid_gold = list(invalid_gold)
    original_invalid_negatives = list(invalid_negatives)
    covered_families = set(recertification_coverage)
    covered_invalid_gold = [family for family in original_invalid_gold if family in covered_families]
    covered_invalid_negatives = [
        pair
        for pair in original_invalid_negatives
        if pair.split("/", 1)[0] in covered_families
        and pair.split("/", 1)[1] in recertification_coverage[pair.split("/", 1)[0]]["negative_case_ids"]
    ]
    if covered_invalid_gold or covered_invalid_negatives:
        used_families = set(covered_invalid_gold) | {
            pair.split("/", 1)[0] for pair in covered_invalid_negatives
        }
        invalid_gold = [family for family in invalid_gold if family not in used_families]
        invalid_negatives = [
            pair
            for pair in invalid_negatives
            if not (
                pair.split("/", 1)[0] in used_families
                and pair.split("/", 1)[1]
                in recertification_coverage[pair.split("/", 1)[0]]["negative_case_ids"]
            )
        ]
        problems = [
            problem
            for problem in problems
            if problem.split(":", 1)[0] not in used_families
        ]
        if recertification_summary is not None:
            recertification_summary = {
                **recertification_summary,
                "used_family_ids": sorted(used_families),
                "used_stale_gold_family_ids": sorted(covered_invalid_gold),
                "used_stale_negative_case_ids": sorted(covered_invalid_negatives),
            }
    problems.extend(evidence_problems)
    stale_families = set(invalid_gold) | {pair.split("/", 1)[0] for pair in invalid_negatives}
    rerun_required = bool(invalid_gold or invalid_negatives)
    fresh_used = bool(covered_invalid_gold or covered_invalid_negatives)
    summary = {
        "policy": (
            "source_transitive_input_hash_bound_plus_release_recertification_evidence"
            if fresh_used
            else "source_transitive_input_hash_bound"
        ),
        "source_dut_gold_certification_total": len(source_rows),
        "source_dut_gold_certification_count": reusable_gold,
        "source_negative_certification_total": negative_total,
        "source_negative_certification_count": reusable_negatives,
        "fresh_dut_gold_certification_count": len(covered_invalid_gold),
        "fresh_negative_certification_count": len(covered_invalid_negatives),
        "effective_dut_gold_certification_count": reusable_gold + len(covered_invalid_gold),
        "effective_negative_certification_count": reusable_negatives + len(covered_invalid_negatives),
        "evaluators": ["evas", "spectre"],
        "simulation_rerun_required_for_materialization": rerun_required,
        "stale_certification_family_ids": sorted(stale_families),
        "stale_gold_family_ids": invalid_gold,
        "stale_negative_case_ids": invalid_negatives,
    }
    if fresh_used and recertification_summary is not None:
        summary["fresh_recertification_evidence"] = recertification_summary
    return summary, problems
