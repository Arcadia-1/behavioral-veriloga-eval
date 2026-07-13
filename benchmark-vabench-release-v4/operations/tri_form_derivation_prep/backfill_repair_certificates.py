#!/usr/bin/env python3
"""Backfill missing tri-form bugfix repair certificates.

This is intentionally a conservative evidence backfill, not a simulator rerun.
It rebuilds the private ``repair_certificate.json`` files from the canonical
DUT source certifications already referenced by each tri-form bugfix task.
When a legacy mutation certification does not carry enough component
fingerprints to prove score-deck hash reuse, the generated certificate remains
``canonical_deck_replay_pending`` instead of silently promoting the evidence.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Iterable


PACKAGE = Path(__file__).resolve().parents[2]
PREP = Path(__file__).resolve().parent
if str(PREP) not in sys.path:
    sys.path.insert(0, str(PREP))

import materialize_tri_form_release as materializer  # noqa: E402


DEFAULT_RELEASE = PACKAGE / "release" / "tri-form-v4-1200-final"
DEFAULT_SELECTION = PACKAGE / "operations" / "api_pilot_selection_10_20260714.json"


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SystemExit(f"expected JSON object: {path}")
    return payload


def selected_bugfix_tasks(selection: Path, family_ids: set[str] | None) -> list[Path]:
    payload = read_json(selection)
    tasks: list[Path] = []
    for family in payload.get("families") or []:
        family_id = str(family.get("family_id") or "")
        if family_ids is not None and family_id not in family_ids:
            continue
        bugfix = ((family.get("forms") or {}).get("bugfix") or {})
        relative = str(bugfix.get("path") or "")
        if not relative:
            raise SystemExit(f"selection family {family_id}: missing bugfix path")
        task_dir = PACKAGE / relative
        if not task_dir.is_dir():
            raise SystemExit(f"selection family {family_id}: missing task dir: {task_dir}")
        tasks.append(task_dir)
    return tasks


def active_mutations(source_task: Path) -> list[dict[str, Any]]:
    evaluator = source_task / "evaluator"
    catalog = read_json(evaluator / "mutation_catalog.json")
    rows: list[dict[str, Any]] = []
    for mutation in catalog.get("mutations") or []:
        mutation_id = str(mutation.get("id") or "")
        if not mutation_id:
            raise SystemExit(f"{source_task.name}: mutation without id")
        certification = evaluator / "mutation_bundles" / mutation_id / "certification.json"
        bundle = evaluator / "mutation_bundles" / mutation_id
        if not certification.is_file():
            evidence_path = str(((mutation.get("certification") or {}).get("evidence_path")) or "")
            candidates = [
                source_task / evidence_path,
                evaluator / evidence_path,
            ]
            certification = next((candidate for candidate in candidates if candidate.is_file()), certification)
        if not certification.is_file():
            raise SystemExit(f"{source_task.name}/{mutation_id}: missing certification")
        if not bundle.is_dir():
            raise SystemExit(f"{source_task.name}/{mutation_id}: missing mutation bundle")
        rows.append(
            {
                "mutation_id": mutation_id,
                "fault_class": str(mutation.get("fault_class") or ""),
                "trigger_condition": str(mutation.get("trigger_condition") or ""),
                "violated_property_ids": list(mutation.get("violated_property_ids") or []),
                "certification_path": certification.relative_to(source_task).as_posix(),
                "certification_sha256": materializer.file_sha(certification),
                "mutation_bundle_sha256": materializer.tree_sha(bundle),
            }
        )
    rows.sort(key=lambda item: str(item["mutation_id"]))
    return rows


def compare_sha(
    mismatches: list[str],
    *,
    label: str,
    recorded: str | None,
    current: str | None,
) -> None:
    if not recorded or not current or recorded != current:
        mismatches.append(label)


def mutation_fingerprint_mismatches(
    mutation_record: dict[str, Any],
    *,
    source_task: Path,
    buggy_bundle: Path,
    artifact_paths: Iterable[str],
) -> list[str]:
    """Return conservative hash-binding mismatches for a repair seed.

    New v2 negative certifications carry the full ``component_fingerprints``
    block and can be checked with the normal materializer logic.  Legacy v1
    records only carry a small ``inputs`` block, so we mark the missing
    canonical deck/candidate/gold bindings as pending rather than treating the
    old evidence as a strict score-deck proof.
    """
    current = materializer.current_source_evidence_identity(source_task)
    current_inputs = current["task_inputs"]
    candidate_files = [buggy_bundle / relative for relative in artifact_paths]
    missing = [str(path) for path in candidate_files if not path.is_file()]
    if missing:
        raise SystemExit(f"{source_task.name}: incomplete bugfix bundle: {missing}")
    mutation_current = {
        **current_inputs,
        "deck_sha256": materializer.file_sha(source_task / "evaluator" / "score_tb.scs"),
        "profile_sha256": current_inputs["score_profile_sha256"],
        "candidate_bundle_sha256": materializer.aggregate_file_sha(candidate_files, base=buggy_bundle),
    }
    if mutation_record.get("component_fingerprints"):
        return materializer.source_record_mismatches(
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

    legacy_inputs = mutation_record.get("inputs") or {}
    mismatches: list[str] = [
        "component_fingerprints.missing",
        "task_inputs.deck_sha256",
        "task_inputs.gold_bundle_sha256",
        "task_inputs.candidate_bundle_sha256",
        "task_inputs.property_contract_sha256",
        "task_inputs.trace_contract_sha256",
    ]
    compare_sha(
        mismatches,
        label="task_inputs.checker_profile_sha256",
        recorded=legacy_inputs.get("checker_profile_sha256"),
        current=current_inputs.get("checker_profile_sha256"),
    )
    compare_sha(
        mismatches,
        label="task_inputs.harness_spec_sha256",
        recorded=legacy_inputs.get("harness_spec_sha256"),
        current=current_inputs.get("harness_spec_sha256"),
    )
    compare_sha(
        mismatches,
        label="task_inputs.profile_sha256",
        recorded=legacy_inputs.get("profile_sha256"),
        current=current_inputs.get("score_profile_sha256"),
    )
    return sorted(set(mismatches))


def build_certificate(task_dir: Path) -> dict[str, Any]:
    task_record = read_json(task_dir / "TASK_RECORD.json")
    derivation = read_json(task_dir / "evaluator" / "derivation_manifest.json")
    family_id = str(task_record.get("family_id") or "")
    source_task = PACKAGE / str(task_record.get("canonical_dut_source") or "")
    if not source_task.is_dir():
        raise SystemExit(f"{task_dir.name}: missing canonical source: {source_task}")
    mutation_id = str(
        ((derivation.get("negative_assignment") or {}).get("bugfix_seed"))
        or ((derivation.get("selection_evidence") or {}).get("mutation_id"))
        or ""
    )
    if not mutation_id:
        raise SystemExit(f"{task_dir.name}: missing bugfix seed mutation id")
    buggy_bundle = task_dir / "buggy_bundle"
    if not buggy_bundle.is_dir():
        raise SystemExit(f"{task_dir.name}: missing buggy bundle")

    current = materializer.current_source_evidence_identity(source_task)
    gold_certificate = source_task / "evaluator" / "certification.json"
    gold_record = read_json(gold_certificate)
    gold_mismatches = materializer.source_record_mismatches(
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

    row = {
        "canonical_dut_id": family_id,
        "active_mutations": active_mutations(source_task),
    }
    mutation = next((item for item in row["active_mutations"] if item["mutation_id"] == mutation_id), None)
    if mutation is None:
        raise SystemExit(f"{task_dir.name}: source catalog does not contain seed {mutation_id}")
    mutation_certificate = source_task / str(mutation["certification_path"])
    mutation_record = read_json(mutation_certificate)
    mutation_mismatches = mutation_fingerprint_mismatches(
        mutation_record,
        source_task=source_task,
        buggy_bundle=buggy_bundle,
        artifact_paths=current["artifact_paths"],
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
        "score_deck_sha256": materializer.file_sha(source_task / "evaluator" / "score_tb.scs"),
        "buggy_bundle_sha256": materializer.tree_sha(buggy_bundle),
        "gold_solution_sha256": materializer.tree_sha(source_task / "evaluator" / "solution"),
        "gold_repair_status": "pass" if gold_reusable else "canonical_deck_replay_pending",
        "buggy_seed_status": "killed_behaviorally" if seed_reusable else "canonical_deck_replay_pending",
        "gold_fingerprint_mismatches": gold_mismatches,
        "buggy_seed_fingerprint_mismatches": mutation_mismatches,
        "gold_source_certification_sha256": materializer.file_sha(gold_certificate),
        "mutation_source_certification_sha256": materializer.file_sha(mutation_certificate),
        "evidence_rebinding_required": not gold_reusable or not seed_reusable,
        "simulation_rerun_required_for_materialization": False,
        "simulation_rerun_requirement_status": "not_determined_by_materialization",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selection", type=Path, default=DEFAULT_SELECTION)
    parser.add_argument("--families", nargs="*", default=None, help="Optional family ids, e.g. 010 342")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true", help="Overwrite existing repair certificates")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    family_ids = {str(item).zfill(3) for item in args.families} if args.families else None
    tasks = selected_bugfix_tasks(args.selection, family_ids)
    records: list[dict[str, Any]] = []
    for task_dir in tasks:
        target = task_dir / "evaluator" / "repair_certificate.json"
        if target.exists() and not args.force:
            certificate = read_json(target)
            action = "kept"
        else:
            certificate = build_certificate(task_dir)
            action = "would_write" if args.dry_run else "wrote"
            if not args.dry_run:
                materializer.write_json(target, certificate)
        task_record = read_json(task_dir / "TASK_RECORD.json")
        records.append(
            {
                "task_id": task_record.get("task_id"),
                "family_id": task_record.get("family_id"),
                "path": target.relative_to(PACKAGE).as_posix(),
                "action": action,
                "status": certificate.get("status"),
                "gold_repair_status": certificate.get("gold_repair_status"),
                "buggy_seed_status": certificate.get("buggy_seed_status"),
                "buggy_seed_mismatch_count": len(certificate.get("buggy_seed_fingerprint_mismatches") or []),
                "gold_mismatch_count": len(certificate.get("gold_fingerprint_mismatches") or []),
            }
        )
    summary = {
        "schema_version": "v4-repair-certificate-backfill-summary-v1",
        "selection": args.selection.relative_to(PACKAGE).as_posix(),
        "task_count": len(records),
        "status_counts": {
            status: sum(1 for record in records if record["status"] == status)
            for status in sorted({str(record["status"]) for record in records})
        },
        "records": records,
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
