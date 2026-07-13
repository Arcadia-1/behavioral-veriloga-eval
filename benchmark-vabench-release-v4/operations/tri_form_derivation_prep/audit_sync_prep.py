#!/usr/bin/env python3
"""Audit the generated tri-form derivation preparation snapshot."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def audit(manifest: dict[str, Any], require_bound: bool) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    families = manifest.get("families") or []
    if manifest.get("scoreable") is not False:
        errors.append("prep_manifest_must_be_non_scoreable")
    if len(families) != 400:
        errors.append(f"expected_400_families_observed_{len(families)}")
    family_ids = [str(item.get("family_id")) for item in families]
    if len(set(family_ids)) != len(family_ids):
        errors.append("duplicate_family_ids")
    if family_ids != [f"{index:03d}" for index in range(1, 401)]:
        errors.append("family_ids_not_exactly_001_through_400")

    testbench_ids: list[str] = []
    bugfix_ids: list[str] = []
    for family in families:
        family_id = int(family["family_id"])
        derived = family.get("derived_tasks") or {}
        testbench_id = str((derived.get("testbench") or {}).get("task_id"))
        bugfix_id = str((derived.get("bugfix") or {}).get("task_id"))
        testbench_ids.append(testbench_id)
        bugfix_ids.append(bugfix_id)
        if testbench_id != f"v4-{family_id + 500:03d}":
            errors.append(f"{family_id:03d}:invalid_testbench_id:{testbench_id}")
        if bugfix_id != f"v4-{family_id + 1000:04d}":
            errors.append(f"{family_id:03d}:invalid_bugfix_id:{bugfix_id}")

        draft = family.get("draft_derivation_manifest")
        if draft is None:
            if not family.get("blockers"):
                errors.append(f"{family_id:03d}:missing_draft_without_blocker")
            continue
        assignment = draft.get("negative_assignment") or {}
        seed = assignment.get("bugfix_seed")
        suite = assignment.get("testbench_suite") or []
        if len(suite) != 5 or len(set(suite)) != 5:
            errors.append(f"{family_id:03d}:testbench_suite_not_exactly_five_unique")
        if seed not in suite:
            errors.append(f"{family_id:03d}:bugfix_seed_not_in_testbench_suite")
        catalog_count = int((family.get("catalog") or {}).get("mutation_count", 0))
        excluded = (family.get("catalog") or {}).get("excluded_from_proposed_suite") or []
        if len(set(suite) | set(excluded)) != catalog_count:
            errors.append(f"{family_id:03d}:suite_and_exclusions_do_not_cover_catalog")

    if len(set(testbench_ids)) != len(testbench_ids):
        errors.append("duplicate_testbench_ids")
    if len(set(bugfix_ids)) != len(bugfix_ids):
        errors.append("duplicate_bugfix_ids")

    binding = manifest.get("base_release_binding") or {}
    if require_bound and binding.get("status") != "bound_to_frozen_dut_release":
        errors.append("frozen_base_release_binding_required")
    if binding.get("status") == "bound_to_frozen_dut_release" and binding.get(
        "task_hash_match_count"
    ) != 400:
        errors.append("base_release_task_hash_match_count_is_not_400")
    if binding.get("status") != "bound_to_frozen_dut_release":
        warnings.append("base_release_not_frozen_or_bound")

    summary = manifest.get("summary") or {}
    if summary.get("catalog_mutation_count") != 2051:
        errors.append("catalog_mutation_count_is_not_2051")
    if summary.get("formal_active_mutation_count") != 2000:
        errors.append("formal_active_mutation_count_is_not_2000")
    if summary.get("provenance_only_extra_count") != 51:
        errors.append("provenance_only_extra_count_is_not_51")
    if summary.get("blocked_family_count"):
        warnings.append(f"blocked_families={summary['blocked_family_count']}")
    if summary.get("manual_review_family_count"):
        warnings.append(f"manual_review_families={summary['manual_review_family_count']}")
    if summary.get("cross_profile_validation_candidate_count"):
        warnings.append(
            "cross_profile_validation_candidates="
            f"{summary['cross_profile_validation_candidate_count']}"
        )

    return {
        "schema_version": "v4-tri-form-derivation-prep-audit-v1",
        "status": "pass" if not errors else "fail",
        "require_bound": require_bound,
        "errors": errors,
        "warnings": warnings,
        "counts": {
            "families": len(families),
            "testbench_tasks": len(testbench_ids),
            "bugfix_tasks": len(bugfix_ids),
            "draft_assignments": sum(
                family.get("draft_derivation_manifest") is not None for family in families
            ),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    default_dir = Path(__file__).resolve().parent
    parser.add_argument("--manifest", type=Path, default=default_dir / "PREP_MANIFEST.json")
    parser.add_argument("--output", type=Path, default=default_dir / "AUDIT_REPORT.json")
    parser.add_argument("--require-bound", action="store_true")
    args = parser.parse_args()
    report = audit(_read_json(args.manifest), args.require_bound)
    _write_json(args.output, report)
    print(
        f"TRI_FORM_PREP_AUDIT status={report['status']} "
        f"errors={len(report['errors'])} warnings={len(report['warnings'])}"
    )
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
