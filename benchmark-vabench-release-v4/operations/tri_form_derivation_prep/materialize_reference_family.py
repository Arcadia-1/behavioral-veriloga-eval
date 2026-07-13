#!/usr/bin/env python3
"""Materialize one hash-bound DUT family as an auditable tri-form preview."""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any


PACKAGE = Path(__file__).resolve().parents[2]
PREP = Path(__file__).resolve().parent
if str(PREP) not in sys.path:
    sys.path.insert(0, str(PREP))

import materialize_tri_form_release as materializer  # noqa: E402


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SystemExit(f"expected a JSON object: {path}")
    return payload


def denominator_row(source: Path, family_id: str) -> dict[str, Any]:
    manifest = read_json(source / "score_denominator_manifest.json")
    matches = [
        row for row in manifest.get("tasks") or []
        if str(row.get("canonical_dut_id")) == family_id
    ]
    if len(matches) != 1:
        raise SystemExit(f"expected exactly one denominator row for {family_id}")
    return matches[0]


def materializer_row(source_task: Path, denominator: dict[str, Any]) -> dict[str, Any]:
    evaluator = source_task / "evaluator"
    catalog = read_json(evaluator / "mutation_catalog.json")
    mutations = catalog.get("mutations") or []
    if len(mutations) != 5:
        raise SystemExit(f"{source_task.name}: reference preview requires exactly five active mutations")

    active_mutations = []
    for mutation in mutations:
        mutation_id = str(mutation.get("id") or "")
        certification = evaluator / "mutation_bundles" / mutation_id / "certification.json"
        bundle = evaluator / "mutation_bundles" / mutation_id
        if not mutation_id or not certification.is_file() or not bundle.is_dir():
            raise SystemExit(f"{source_task.name}: incomplete mutation bundle for {mutation_id!r}")
        active_mutations.append({
            "mutation_id": mutation_id,
            "fault_class": str(mutation.get("fault_class") or ""),
            "trigger_condition": str(mutation.get("trigger_condition") or ""),
            "violated_property_ids": list(mutation.get("violated_property_ids") or []),
            "certification_path": (
                f"evaluator/mutation_bundles/{mutation_id}/certification.json"
            ),
            "certification_sha256": materializer.file_sha(certification),
            "mutation_bundle_sha256": materializer.tree_sha(bundle),
        })

    active_mutations.sort(key=lambda item: item["mutation_id"])
    family_id = str(denominator["canonical_dut_id"])
    hashes = {
        "mutation_catalog_sha256": materializer.file_sha(evaluator / "mutation_catalog.json"),
        "score_deck_sha256": materializer.file_sha(evaluator / "score_tb.scs"),
        "task_certification_sha256": materializer.file_sha(evaluator / "certification.json"),
    }
    return {
        "canonical_dut_id": family_id,
        "canonical_dut_slug": source_task.name,
        "release_dir": source_task.name,
        "title": str((read_json(evaluator / "family_spec.json").get("identity") or {}).get("title") or ""),
        "active_mutation_count": len(active_mutations),
        "active_mutations": active_mutations,
        # A semantic, nontrivial repair seed is preferred, while the shared policy
        # remains the final selector and records its rationale in the preview.
        "bugfix_seed": "neg_003_comparator_polarity",
        "hashes": hashes,
    }


def build_preview(
    *, source: Path, family_id: str, output: Path, replay_evidence: list[Path], force: bool
) -> dict[str, Any]:
    if output.exists():
        if not force:
            raise SystemExit(f"output exists; pass --force to replace it: {output}")
        shutil.rmtree(output)
    output.mkdir(parents=True)

    source_row = denominator_row(source, family_id)
    source_task = source / str(source_row.get("release_dir") or "")
    if not source_task.is_dir():
        raise SystemExit(f"missing source task directory: {source_task}")

    canonical_root = output / "canonical_dut"
    embedded_task = canonical_root / source_task.name
    canonical_root.mkdir()
    shutil.copytree(source_task, embedded_task)
    shutil.copy2(source / "score_denominator_manifest.json", canonical_root / "score_denominator_manifest.json")

    row = materializer_row(embedded_task, source_row)
    spec_path = embedded_task / "evaluator" / "family_spec.json"
    spec = read_json(spec_path)
    spec_sha = materializer.file_sha(spec_path)
    source_manifest_sha = materializer.file_sha(canonical_root / "score_denominator_manifest.json")
    seed_review = materializer.select_bugfix_seed(row)
    replay_lookup, replay_sources = materializer.load_reference_replay_evidence(replay_evidence)

    task_rows = [
        materializer.build_dut_view(
            output, canonical_root, "canonical_dut", embedded_task, row, spec, spec_sha
        ),
        materializer.build_testbench_view(
            output,
            canonical_root,
            "canonical_dut",
            embedded_task,
            row,
            spec,
            spec_sha,
            source_manifest_sha,
            seed_review,
            replay_lookup,
        ),
        materializer.build_bugfix_view(
            output,
            canonical_root,
            "canonical_dut",
            embedded_task,
            row,
            spec,
            spec_sha,
            source_manifest_sha,
            seed_review,
        ),
    ]
    task_rows.sort(key=lambda item: (str(item["form"]), int(item["family_id"])))
    # The runtime exporter resolves canonical_dut_source from PACKAGE, matching
    # the formal release layout. Keep this self-contained preview executable
    # under the same rule instead of relying on its current working directory.
    package_source = materializer.rel(embedded_task, PACKAGE)
    for task in task_rows:
        record_path = output / str(task["task_dir"]) / "TASK_RECORD.json"
        record = read_json(record_path)
        record["canonical_dut_source"] = package_source
        materializer.write_json(record_path, record)
    skills = materializer.install_prompt_assets(output)
    materializer.write_prompt_records(output, task_rows, skills)
    materializer.write_json(output / "TASK_INDEX.json", {
        "schema_version": "v4-tri-form-task-index-v1",
        "tasks": task_rows,
    })
    materializer.write_json(output / "BUGFIX_SEED_REVIEW.json", {
        "schema_version": "v4-bugfix-seed-review-v1",
        "selection_policy": "semantic_fault_complexity_v1",
        "families": [{"family_id": family_id, **seed_review}],
    })
    replay_plan = materializer.build_reference_replay_plan(output, task_rows)
    materializer.write_json(output / "REFERENCE_REPLAY_PLAN.json", replay_plan)
    replay_records = materializer.write_selected_reference_replay_evidence(
        output, task_rows, replay_lookup, replay_sources
    )

    testbench_dir = output / next(
        row["task_dir"] for row in task_rows if row["form"] == "testbench"
    )
    bugfix_dir = output / next(
        row["task_dir"] for row in task_rows if row["form"] == "bugfix"
    )
    testbench_certificate = read_json(testbench_dir / "evaluator" / "reference_certificate.json")
    bugfix_certificate = read_json(bugfix_dir / "evaluator" / "repair_certificate.json")
    ready = (
        testbench_certificate.get("correct_dut_status") == "pass"
        and testbench_certificate.get("negative_suite_status") == "five_of_five_killed_behaviorally"
        and bugfix_certificate.get("status") == "pass"
    )
    manifest = {
        "schema_version": "v4-reference-family-preview-v1",
        "family_id": family_id,
        "release_status": "ready_for_human_review" if ready else "evidence_incomplete",
        "formal_release_promotion_required": True,
        "family_count": 1,
        "task_count": len(task_rows),
        "prompt_record_count": len(task_rows) * len(materializer.MODES),
        "source": "canonical_dut",
        "source_score_denominator_manifest_sha256": source_manifest_sha,
        "testbench_reference_certificate": {
            "correct_dut_status": testbench_certificate.get("correct_dut_status"),
            "negative_suite_status": testbench_certificate.get("negative_suite_status"),
            "reused_negative_count": testbench_certificate.get("reused_negative_count"),
            "pending_negative_count": testbench_certificate.get("pending_negative_count"),
        },
        "bugfix_repair_certificate": {
            "status": bugfix_certificate.get("status"),
            "buggy_seed_status": bugfix_certificate.get("buggy_seed_status"),
            "gold_repair_status": bugfix_certificate.get("gold_repair_status"),
        },
        "reference_replay": {
            "planned_case_count": len(replay_plan.get("mutations") or []),
            "embedded_evidence_case_count": len(replay_records.get("rows") or []),
        },
    }
    materializer.write_json(output / "REFERENCE_FAMILY_MANIFEST.json", manifest)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--family-id", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--reference-replay-evidence", type=Path, action="append", default=[])
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    family_id = str(args.family_id).zfill(3)
    result = build_preview(
        source=args.source.expanduser().resolve(),
        family_id=family_id,
        output=args.output.expanduser().resolve(),
        replay_evidence=[path.expanduser().resolve() for path in args.reference_replay_evidence],
        force=args.force,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["release_status"] == "ready_for_human_review" else 1


if __name__ == "__main__":
    raise SystemExit(main())
