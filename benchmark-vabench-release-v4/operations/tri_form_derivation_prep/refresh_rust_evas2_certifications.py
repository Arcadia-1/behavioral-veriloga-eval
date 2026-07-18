#!/usr/bin/env python3
"""Replace legacy dual-simulator V4 certificates with fresh Rust EVAS2 evidence."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from score_denominator_registry import (
    load_family_rows,
    write_family_row,
)
from source_certification_binding import _task_input_hashes, file_sha, tree_sha_by_file_hash


SCHEMA_VERSION = "v4-r44-rust-evas2-certification-report-v1"
GOLD_SCHEMA_VERSION = "v4-task-certification-rust-evas2-v1"
NEGATIVE_SCHEMA_VERSION = "v4-negative-certification-rust-evas2-v1"
POLICY = "rust_evas2_only"


class RefreshError(ValueError):
    """Raised when executable evidence is incomplete or inconsistent."""


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RefreshError(f"expected JSON object: {path}")
    return value


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def report_cases(paths: list[Path]) -> tuple[dict[str, dict[str, Any]], dict[str, str]]:
    families: dict[str, dict[str, Any]] = {}
    runtime: dict[str, str] | None = None
    for path in paths:
        report = read_json(path)
        if report.get("schema_version") != "v4-checker-batch-certification-v1":
            raise RefreshError(f"unsupported certification report: {path}")
        if report.get("status") != "pass" or report.get("certification_policy") != POLICY:
            raise RefreshError(f"report is not a Rust EVAS2 PASS: {path}")
        current_runtime = report.get("runtime") or {}
        if runtime is None:
            runtime = {str(key): str(value) for key, value in current_runtime.items()}
        elif runtime != {str(key): str(value) for key, value in current_runtime.items()}:
            raise RefreshError("certification reports used different Rust EVAS2 runtimes")
        for case in report.get("cases") or []:
            family = str(case.get("family_id") or "")
            case_id = str(case.get("case_id") or "")
            if not family or not case_id:
                raise RefreshError(f"report has an unidentified case: {path}")
            family_cases = families.setdefault(family, {})
            if case_id in family_cases:
                raise RefreshError(f"duplicate case evidence: {family}/{case_id}")
            family_cases[case_id] = case
    return families, runtime or {}


def catalog_mutation(task: Path, mutation_id: str) -> dict[str, Any]:
    catalog = read_json(task / "evaluator" / "mutation_catalog.json")
    for mutation in catalog.get("mutations") or []:
        if str(mutation.get("id")) == mutation_id:
            return mutation
    raise RefreshError(f"{task.name}/{mutation_id}: mutation is absent from catalog")


def validate_family_cases(
    family: str,
    row: dict[str, Any],
    cases: dict[str, dict[str, Any]],
) -> list[str]:
    mutation_ids = [str(item.get("mutation_id") or "") for item in row.get("active_mutations") or []]
    expected = {"gold", *mutation_ids}
    if len(mutation_ids) != 5 or len(set(mutation_ids)) != 5:
        raise RefreshError(f"{family}: denominator is not exact-five")
    if set(cases) != expected:
        raise RefreshError(
            f"{family}: evidence case mismatch; missing={sorted(expected - set(cases))} "
            f"extra={sorted(set(cases) - expected)}"
        )
    for case_id, case in cases.items():
        expected_pass = case_id == "gold"
        if case.get("status") != "pass":
            raise RefreshError(f"{family}/{case_id}: certification status is not pass")
        if case.get("checker_pass") is not expected_pass:
            raise RefreshError(f"{family}/{case_id}: checker classification is wrong")
        if case.get("diagnostics_complete") is not True:
            raise RefreshError(f"{family}/{case_id}: checker diagnostic is empty")
    if cases["gold"].get("insufficient_excitation_rejected") is False:
        raise RefreshError(f"{family}: invalid insufficient-excitation result")
    return mutation_ids


def gold_certificate(
    family: str,
    task: Path,
    cases: dict[str, dict[str, Any]],
    runtime: dict[str, str],
    evidence_ref: dict[str, str],
) -> dict[str, Any]:
    certificate_inputs, component_inputs = _task_input_hashes(task)
    gold = cases["gold"]
    return {
        "schema_version": GOLD_SCHEMA_VERSION,
        "family_id": family,
        "status": "gate2_pass",
        "certification_policy": POLICY,
        "evaluators": {"evas2": {**runtime, "status": "pass"}},
        "input_hashes": certificate_inputs,
        "component_fingerprints": {"task_inputs": component_inputs},
        "checks": {
            "gold_behavior": "pass",
            "active_negative_count": 5,
            "active_negatives": "all_killed_behaviorally",
            "trace_axis_metamorphic": (
                "classification_invariant"
                if gold.get("timing_invariant") is True
                else "diagnostic_difference"
            ),
            "insufficient_excitation": (
                "rejected"
                if gold.get("insufficient_excitation_rejected") is True
                else "not_applicable"
            ),
            "diagnostic": "present",
        },
        "evidence": {
            **evidence_ref,
            "campaign": "r44-full400",
            "checker_id": gold.get("checker_id"),
            "trace_row_count": gold.get("trace_row_count"),
        },
    }


def negative_certificate(
    family: str,
    mutation_id: str,
    task: Path,
    case: dict[str, Any],
    runtime: dict[str, str],
    evidence_ref: dict[str, str],
) -> dict[str, Any]:
    evaluator = task / "evaluator"
    mutation = catalog_mutation(task, mutation_id)
    profile = str((mutation.get("certification") or {}).get("profile") or "score")
    if profile not in {"feedback", "score"}:
        raise RefreshError(f"{task.name}/{mutation_id}: invalid profile {profile!r}")
    violated = [str(value) for value in mutation.get("violated_property_ids") or []]
    if not violated:
        raise RefreshError(f"{task.name}/{mutation_id}: missing violated_property_ids")
    return {
        "schema_version": NEGATIVE_SCHEMA_VERSION,
        "family_id": family,
        "mutation_id": mutation_id,
        "status": "pass",
        "outcome": "killed_behaviorally",
        "certification_policy": POLICY,
        "evaluators": {"evas2": "compile_pass_behavior_fail"},
        "runtime": runtime,
        "inputs": {
            "checker_profile_sha256": file_sha(evaluator / "checker_profile.json"),
            "harness_spec_sha256": file_sha(evaluator / "harness_spec.json"),
            "profile_sha256": file_sha(evaluator / "profiles" / f"{profile}.json"),
        },
        "checks": {
            "compile": "pass",
            "behavior": "fail_as_expected",
            "trace_axis_metamorphic": (
                "classification_invariant"
                if case.get("timing_invariant") is True
                else "diagnostic_difference"
            ),
            "diagnostic": "present",
        },
        "diagnostics": {
            "violated_property_ids": violated,
            "expected": (
                f"properties {', '.join(violated)} satisfy the public contract; "
                f"fault class {mutation.get('fault_class') or 'unspecified'} is rejected"
            ),
            "observed": f"EVAS: {str(case.get('checker_note') or '').strip()}",
        },
        "evidence": {
            **evidence_ref,
            "campaign": "r44-full400",
            "checker_id": case.get("checker_id"),
            "trace_row_count": case.get("trace_row_count"),
        },
    }


def refresh_task_record(task: Path) -> None:
    evaluator = task / "evaluator"
    public = task / "public" / "task"
    record_path = evaluator / "task_record.json"
    record = read_json(record_path)
    for relative in list((record.get("evaluator_hashes") or {}).keys()):
        if relative == "solution_tree":
            continue
        record["evaluator_hashes"][relative] = file_sha(evaluator / relative)
    for relative in list((record.get("public_hashes") or {}).keys()):
        record["public_hashes"][relative] = file_sha(public / relative)
    record["readiness_evidence"] = {
        "kind": "task_certification",
        "path": "evaluator/certification.json",
        "sha256": file_sha(evaluator / "certification.json"),
    }
    write_json(record_path, record)


def update_registry_row(source: Path, family: str, row: dict[str, Any], task: Path) -> None:
    evaluator = task / "evaluator"
    row["hashes"] = {
        "mutation_catalog_sha256": file_sha(evaluator / "mutation_catalog.json"),
        "score_deck_sha256": file_sha(evaluator / "score_tb.scs"),
        "task_certification_sha256": file_sha(evaluator / "certification.json"),
        "task_record_sha256": file_sha(evaluator / "task_record.json"),
    }
    for mutation in row.get("active_mutations") or []:
        cert_path = task / str(mutation["certification_path"])
        mutation["certification_sha256"] = file_sha(cert_path)
        mutation["mutation_bundle_sha256"] = tree_sha_by_file_hash(cert_path.parent)
    write_family_row(source, family, row)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--report", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    source = args.source.expanduser().resolve()
    report_paths = [path.expanduser().resolve() for path in args.report]
    family_cases, runtime = report_cases(report_paths)
    rows = {str(row["canonical_dut_id"]): row for row in load_family_rows(source)}
    if set(rows) != {f"{value:03d}" for value in range(1, 401)}:
        raise SystemExit("source denominator does not contain exactly families 001-400")
    if set(family_cases) != set(rows):
        raise SystemExit(
            f"evidence coverage mismatch: missing={sorted(set(rows) - set(family_cases))} "
            f"extra={sorted(set(family_cases) - set(rows))}"
        )

    compact_cases: list[dict[str, Any]] = []
    for family in sorted(rows):
        row = rows[family]
        cases = family_cases[family]
        mutation_ids = validate_family_cases(family, row, cases)
        for case_id in ["gold", *mutation_ids]:
            case = cases[case_id]
            compact_cases.append(
                {
                    key: case.get(key)
                    for key in (
                        "family_id",
                        "case_id",
                        "mutation_id",
                        "checker_id",
                        "status",
                        "checker_pass",
                        "timing_invariant",
                        "diagnostics_complete",
                        "insufficient_excitation_rejected",
                        "trace_row_count",
                    )
                }
            )

    output = args.output.expanduser().resolve()
    payload = {
        "schema_version": SCHEMA_VERSION,
        "status": "pass",
        "release_candidate": "r44",
        "certification_policy": POLICY,
        "runtime": runtime,
        "summary": {
            "family_count": 400,
            "gold_pass_count": 400,
            "negative_case_count": 2000,
            "mutation_kill_count": 2000,
            "trace_axis_invariant_count": sum(
                case.get("timing_invariant") is True for case in compact_cases
            ),
            "insufficient_excitation_rejection_count": sum(
                case.get("mutation_id") is None
                and case.get("insufficient_excitation_rejected") is True
                for case in compact_cases
            ),
            "insufficient_excitation_not_applicable_count": sum(
                case.get("mutation_id") is None
                and case.get("insufficient_excitation_rejected") is None
                for case in compact_cases
            ),
            "diagnostic_present_count": 2400,
        },
        "input_report_sha256": [
            {"name": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
            for path in report_paths
        ],
        "cases": compact_cases,
    }
    write_json(output, payload)
    package_root = Path(__file__).resolve().parents[2]
    try:
        evidence_path = output.relative_to(package_root).as_posix()
    except ValueError as exc:
        raise SystemExit("certification output must be inside benchmark-vabench-release-v4") from exc
    evidence_ref = {
        "report_path": evidence_path,
        "report_sha256": file_sha(output),
    }

    for family in sorted(rows):
        row = rows[family]
        task = source / str(row["release_dir"])
        cases = family_cases[family]
        mutation_ids = validate_family_cases(family, row, cases)
        write_json(
            task / "evaluator" / "certification.json",
            gold_certificate(family, task, cases, runtime, evidence_ref),
        )
        for mutation_id in mutation_ids:
            mutation = next(
                item for item in row["active_mutations"] if item["mutation_id"] == mutation_id
            )
            cert_path = task / str(mutation["certification_path"])
            write_json(
                cert_path,
                negative_certificate(
                    family, mutation_id, task, cases[mutation_id], runtime, evidence_ref
                ),
            )
        refresh_task_record(task)
        update_registry_row(source, family, row, task)
    print(json.dumps({"status": "pass", **payload["summary"]}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
