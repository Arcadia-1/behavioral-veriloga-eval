#!/usr/bin/env python3
"""Build a non-scoreable Testbench/Bugfix derivation preparation snapshot."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "v4-tri-form-derivation-prep-v1"
SELECTION_POLICY = (
    "Preserve a valid legacy semantic Bugfix seed when available; then choose "
    "five certified mutations by maximizing distinct fault classes, violated "
    "properties, and trigger conditions. Stable mutation ID ordering resolves "
    "ties only. Every catalog with more than five eligible mutations remains "
    "subject to manual semantic review."
)
TRIVIAL_SEED_MARKERS = (
    "constant_output",
    "identity_passthrough",
    "no_effect",
    "stuck_zero",
    "stuck_at_zero",
    "zero_output",
)


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _find_feedback_deck(task_dir: Path) -> Path | None:
    candidates = (
        task_dir / "test_feedback" / "feedback_tb.scs",
        task_dir / "test_feedback" / "public_tb.scs",
        task_dir / "test_feedback" / "tb_visible_smoke.scs",
        task_dir / "test_feedback" / "visible.scs",
    )
    return next((path for path in candidates if path.is_file()), None)


def _catalog_mutations(catalog: dict[str, Any]) -> list[dict[str, Any]]:
    raw = catalog.get("mutations") or catalog.get("cases") or catalog.get("negatives") or []
    return [item for item in raw if isinstance(item, dict)]


def _is_certified(mutation: dict[str, Any]) -> bool:
    certification = mutation.get("certification") or {}
    return (
        certification.get("status") == "pass"
        and certification.get("compile_status") == "pass"
        and certification.get("simulation_status") == "pass"
        and certification.get("behavior_status") == "killed_behaviorally"
    )


def _legacy_assignment(path: Path) -> tuple[str | None, list[str]]:
    if not path.is_file():
        return None, []
    data = _read_json(path)
    assignment = data.get("negative_assignment") or {}
    if assignment:
        seed = assignment.get("bugfix_seed")
        suite = assignment.get("testbench_suite") or []
        return str(seed) if seed else None, [str(item) for item in suite]
    partition = data.get("mutation_partition") or {}
    seed_value = partition.get("bugfix_seed") or []
    if isinstance(seed_value, str):
        seed = seed_value
    else:
        seed = str(seed_value[0]) if seed_value else None
    suite = []
    for key in ("testbench_public_feedback", "testbench_private_score"):
        suite.extend(str(item) for item in partition.get(key) or [])
    if seed and seed not in suite:
        suite.append(seed)
    return seed, suite


def _mutation_profile(mutation: dict[str, Any]) -> str | None:
    profile = (mutation.get("certification") or {}).get("profile")
    return str(profile) if profile else None


def _property_ids(mutation: dict[str, Any]) -> set[str]:
    return {str(item) for item in mutation.get("violated_property_ids") or []}


def _fault_class(mutation: dict[str, Any]) -> str:
    return str(mutation.get("fault_class") or "unspecified")


def _trigger(mutation: dict[str, Any]) -> str:
    return str(mutation.get("trigger_condition") or "unspecified")


def _seed_score(mutation: dict[str, Any]) -> tuple[int, int, int, int]:
    text = f"{mutation.get('id', '')} {_fault_class(mutation)}".lower()
    nontrivial = int(not any(marker in text for marker in TRIVIAL_SEED_MARKERS))
    return (
        nontrivial,
        int(bool(_property_ids(mutation))),
        int(_trigger(mutation) != "unspecified"),
        int(_mutation_profile(mutation) == "score"),
    )


def _choose_seed(
    eligible: list[dict[str, Any]], legacy_seed: str | None
) -> tuple[dict[str, Any] | None, str]:
    by_id = {str(item.get("id")): item for item in eligible}
    if legacy_seed and legacy_seed in by_id:
        return by_id[legacy_seed], "legacy_semantic_assignment"
    best: dict[str, Any] | None = None
    best_score: tuple[int, int, int, int] | None = None
    for mutation in sorted(eligible, key=lambda item: str(item.get("id"))):
        score = _seed_score(mutation)
        if best_score is None or score > best_score:
            best = mutation
            best_score = score
    return best, "semantic_heuristic_fallback"


def _choose_suite(
    eligible: list[dict[str, Any]], seed: dict[str, Any] | None
) -> list[dict[str, Any]]:
    if seed is None:
        return []
    chosen = [seed]
    chosen_ids = {str(seed.get("id"))}
    used_classes = {_fault_class(seed)}
    used_properties = _property_ids(seed)
    used_triggers = {_trigger(seed)}
    while len(chosen) < 5:
        best: dict[str, Any] | None = None
        best_score: tuple[int, int, int, int] | None = None
        for mutation in sorted(eligible, key=lambda item: str(item.get("id"))):
            mutation_id = str(mutation.get("id"))
            if mutation_id in chosen_ids:
                continue
            properties = _property_ids(mutation)
            score = (
                int(_fault_class(mutation) not in used_classes),
                len(properties - used_properties),
                int(_trigger(mutation) not in used_triggers),
                int(_mutation_profile(mutation) == "score"),
            )
            if best_score is None or score > best_score:
                best = mutation
                best_score = score
        if best is None:
            break
        chosen.append(best)
        chosen_ids.add(str(best.get("id")))
        used_classes.add(_fault_class(best))
        used_properties.update(_property_ids(best))
        used_triggers.add(_trigger(best))
    return chosen


def _ahdl_include_paths(deck: Path) -> list[str]:
    if not deck.is_file():
        return []
    text = deck.read_text(encoding="utf-8", errors="ignore")
    return re.findall(r'\bahdl_include\s+"([^"]+)"', text)


def _binding_status(include_paths: list[str], target_artifacts: list[str]) -> str:
    expected = {f"./dut/{artifact}" for artifact in target_artifacts}
    bare = set(target_artifacts)
    includes = set(include_paths)
    present_targets = {
        artifact
        for artifact in target_artifacts
        if f"./dut/{artifact}" in includes or artifact in includes
    }
    if set(target_artifacts) - present_targets:
        return "missing_or_unrecognized_dut_include"
    non_dut = includes - expected - bare
    if non_dut:
        if all(path.startswith("./support/") for path in non_dut):
            return "support_binding_review_required"
        return "undeclared_external_include_review_required"
    if includes & bare:
        return "mechanical_dut_path_normalization_required"
    return "ready"


def _seed_rationale(seed: dict[str, Any] | None) -> str:
    if seed is None:
        return "No eligible compile-pass behavioral mutation is available."
    properties = sorted(_property_ids(seed))
    return (
        f"Select {_fault_class(seed)} under trigger '{_trigger(seed)}'; it "
        f"violates {', '.join(properties) if properties else 'an undeclared property'} "
        "while preserving the public DUT interface."
    )


def _family_record(package_root: Path, row: dict[str, Any]) -> dict[str, Any]:
    family_id = str(row["canonical_dut_id"])
    task_dir = package_root / "tasks" / str(row["old_dut_slug"])
    catalog_path = task_dir / "negative_variants" / "manifest.json"
    derivation_path = task_dir / "evaluator" / "derivation_manifest.json"
    family_spec_path = task_dir / "family_spec.json"
    score_deck = task_dir / "evaluator" / "score_tb.scs"
    feedback_deck = _find_feedback_deck(task_dir)
    blockers: list[str] = []
    if not task_dir.is_dir():
        blockers.append("missing_source_task_dir")
    if not catalog_path.is_file():
        blockers.append("missing_mutation_catalog")
    if not score_deck.is_file():
        blockers.append("missing_canonical_score_deck")
    if not family_spec_path.is_file():
        blockers.append("missing_family_spec")

    catalog = _read_json(catalog_path) if catalog_path.is_file() else {}
    mutations = _catalog_mutations(catalog)
    mutation_ids = [str(item.get("id")) for item in mutations]
    duplicate_ids = sorted(item for item, count in Counter(mutation_ids).items() if count > 1)
    if duplicate_ids:
        blockers.append("duplicate_mutation_ids")
    eligible = [item for item in mutations if _is_certified(item)]
    if len(eligible) < 5:
        blockers.append("fewer_than_five_catalog_certified_mutations")

    legacy_seed, legacy_suite = _legacy_assignment(derivation_path)
    seed, seed_source = _choose_seed(eligible, legacy_seed)
    suite = _choose_suite(eligible, seed)
    suite_ids = [str(item.get("id")) for item in suite]
    excluded_ids = sorted(set(mutation_ids) - set(suite_ids))
    suite_classes = [_fault_class(item) for item in suite]
    suite_meanings = {
        (_fault_class(item), _trigger(item), tuple(sorted(_property_ids(item)))) for item in suite
    }
    seed_id = str(seed.get("id")) if seed else None
    if seed_id and seed_id not in suite_ids:
        blockers.append("bugfix_seed_not_in_testbench_suite")

    include_paths = _ahdl_include_paths(score_deck)
    target_artifacts = [str(item) for item in row.get("target_artifacts") or []]
    reference_fixture_status = _binding_status(include_paths, target_artifacts)
    family_spec = _read_json(family_spec_path) if family_spec_path.is_file() else {}
    testbench_binding = family_spec.get("testbench_binding") or {}
    candidate_binding_ready = (
        testbench_binding.get("dut_source_root") == "dut"
        and testbench_binding.get("source_path_template") == "./dut/{artifact_path}"
        and bool(testbench_binding.get("instances"))
    )
    if family_spec_path.is_file() and not candidate_binding_ready:
        blockers.append("candidate_testbench_binding_incomplete")
    if reference_fixture_status == "mechanical_dut_path_normalization_required":
        review_warnings_for_binding = ["reference_deck_legacy_path_adapter_required"]
    elif reference_fixture_status == "support_binding_review_required":
        review_warnings_for_binding = [
            "reference_deck_support_resources_require_private_declaration"
        ]
    elif reference_fixture_status == "ready":
        review_warnings_for_binding = []
    else:
        review_warnings_for_binding = ["reference_deck_include_graph_requires_manual_review"]

    feedback_hash = _sha256(feedback_deck) if feedback_deck else None
    score_hash = _sha256(score_deck) if score_deck.is_file() else None
    score_profile_ids = [
        str(item.get("id")) for item in suite if _mutation_profile(item) == "score"
    ]
    replay_ids = [
        str(item.get("id")) for item in suite if _mutation_profile(item) != "score"
    ]
    review_reasons: list[str] = []
    review_warnings: list[str] = list(review_warnings_for_binding)
    if len(eligible) > 5:
        review_reasons.append("more_than_five_eligible_mutations_requires_semantic_exclusion_review")
    if len(suite_classes) == 5 and len(set(suite_classes)) < 5:
        review_warnings.append("selected_suite_reuses_fault_class_labels")
    if len(suite) == 5 and len(suite_meanings) < 5:
        review_reasons.append("selected_suite_has_duplicate_semantic_meaning_proxy")
    if seed_source != "legacy_semantic_assignment":
        review_reasons.append("bugfix_seed_lacks_legacy_semantic_assignment")
    if seed and _seed_score(seed)[0] == 0:
        review_reasons.append("bugfix_seed_has_triviality_marker")

    if blockers:
        review_status = "blocked"
    elif review_reasons:
        review_status = "manual_review_required"
    else:
        review_status = "provisional_complete"

    base_dut = {
        "canonical_task_id": f"v4-{family_id}",
        "canonical_task_slug": str(row["canonical_dut_slug"]),
        "mutation_catalog_sha256": _sha256(catalog_path) if catalog_path.is_file() else None,
        "canonical_score_tb_sha256": score_hash,
    }
    draft_manifest = None
    if seed_id and len(suite_ids) == 5 and score_hash:
        draft_manifest = {
            "schema_version": "v4-derivation-manifest-v2-draft",
            "family_id": family_id,
            "base_dut": base_dut,
            "negative_assignment": {
                "bugfix_seed": seed_id,
                "testbench_suite": suite_ids,
            },
            "selection_evidence": {
                "bugfix_seed_source": seed_source,
                "bugfix_seed_rationale": _seed_rationale(seed),
                "suite_selection_policy": SELECTION_POLICY,
                "semantic_review_status": review_status,
                "review_reasons": review_reasons,
                "review_warnings": review_warnings,
            },
        }

    return {
        "family_id": family_id,
        "title": row.get("title"),
        "category": row.get("category"),
        "level": row.get("level"),
        "source": {
            "current_task_dir": _relative(task_dir, package_root),
            "canonical_dut_dir": f"formal_tasks/{row['canonical_dut_slug']}",
            "mutation_catalog": _relative(catalog_path, package_root),
            "family_spec": _relative(family_spec_path, package_root),
            "legacy_derivation_manifest": (
                _relative(derivation_path, package_root) if derivation_path.is_file() else None
            ),
            "score_deck": _relative(score_deck, package_root) if score_deck.is_file() else None,
            "feedback_deck": _relative(feedback_deck, package_root) if feedback_deck else None,
        },
        "derived_tasks": {
            "testbench": {
                "task_id": f"v4-{row['canonical_testbench_id']}",
                "formal_dir": str(row["canonical_testbench_slug"]),
                "candidate_artifacts": ["testbench.scs"],
                "supplied_dut_artifacts": list(row.get("target_artifacts") or []),
            },
            "bugfix": {
                "task_id": f"v4-{row['canonical_bugfix_id']}",
                "formal_dir": str(row["canonical_bugfix_slug"]),
                "candidate_artifacts": list(row.get("target_artifacts") or []),
            },
        },
        "catalog": {
            "mutation_count": len(mutations),
            "catalog_certified_count": len(eligible),
            "fault_class_count": len({_fault_class(item) for item in eligible}),
            "legacy_bugfix_seed": legacy_seed,
            "legacy_testbench_union": sorted(set(legacy_suite)),
            "excluded_from_proposed_suite": excluded_ids,
            "proposed_suite_semantics": [
                {
                    "id": str(item.get("id")),
                    "fault_class": _fault_class(item),
                    "trigger_condition": _trigger(item),
                    "violated_property_ids": sorted(_property_ids(item)),
                    "legacy_certification_profile": _mutation_profile(item),
                }
                for item in suite
            ],
            "excluded_semantics": [
                {
                    "id": str(item.get("id")),
                    "fault_class": _fault_class(item),
                    "trigger_condition": _trigger(item),
                    "violated_property_ids": sorted(_property_ids(item)),
                    "legacy_certification_profile": _mutation_profile(item),
                }
                for item in mutations
                if str(item.get("id")) in excluded_ids
            ],
        },
        "canonical_suite": {
            "seed_profile": "score",
            "score_deck_sha256": score_hash,
            "legacy_feedback_deck_sha256": feedback_hash,
            "legacy_feedback_differs": bool(
                feedback_hash and score_hash and feedback_hash != score_hash
            ),
            "logical_dut_include_paths": include_paths,
            "reference_fixture_status": reference_fixture_status,
            "candidate_binding_ready": candidate_binding_ready,
            "selected_score_profile_mutations": score_profile_ids,
            "reused_score_profile_negative_evidence": score_profile_ids,
            "cross_profile_validation_candidates": replay_ids,
            "gold_score_evidence_reusable": bool(score_hash),
            "reference_fixture_migration_requires_analog_rerun": False,
        },
        "draft_derivation_manifest": draft_manifest,
        "review_status": review_status,
        "review_reasons": review_reasons,
        "review_warnings": review_warnings,
        "blockers": blockers,
    }


def _write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _validate_base_release_manifest(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    claim = data.get("claim_boundary") or {}
    required_claim = {
        "release_kind": "canonical_dut_base",
        "completed_gate": "dut_base_gate2",
        "tri_form_gate2_complete": False,
        "tri_form_gate3_complete": False,
        "next_gate": "canonical_suite_unification_pending",
    }
    for key, expected in required_claim.items():
        if claim.get(key) != expected:
            raise SystemExit(
                f"base release claim boundary mismatch for {key}: "
                f"expected {expected!r}, observed {claim.get(key)!r}"
            )
    tasks = data.get("tasks") or []
    if data.get("counted_task_count") != 400 or len(tasks) != 400:
        raise SystemExit("base release manifest must contain exactly 400 counted DUT tasks")
    task_map = {str(item.get("canonical_dut_id")): item for item in tasks}
    if sorted(task_map) != [f"{index:03d}" for index in range(1, 401)]:
        raise SystemExit("base release manifest task IDs are not exactly 001 through 400")
    return task_map


def _render_handoff(manifest: dict[str, Any]) -> str:
    summary = manifest["summary"]
    binding = manifest["base_release_binding"]
    return "\n".join(
        [
            "# Tri-Form Derivation Prep Handoff",
            "",
            "This snapshot prepares Testbench and Bugfix derivation without modifying the DUT closeout lane.",
            "",
            "## Current Snapshot",
            "",
            f"- Families: {summary['family_count']}",
            f"- Source-catalog mutations: {summary['catalog_mutation_count']}",
            f"- Formal active mutations: {summary['formal_active_mutation_count']}",
            f"- Provenance-only excluded mutations: {summary['provenance_only_extra_count']}",
            f"- Exactly five eligible: {summary['exactly_five_eligible_count']}",
            f"- More than five eligible: {summary['overfive_eligible_count']}",
            f"- Blocked families: {summary['blocked_family_count']}",
            f"- Manual semantic review: {summary['manual_review_family_count']}",
            f"- Reused score-profile negative evidence: {summary['reused_score_profile_negative_count']}",
            f"- Cross-profile rows requiring carry-forward audit or targeted run: {summary['cross_profile_validation_candidate_count']}",
            f"- Mandatory new gold runs: {summary['mandatory_new_gold_run_count']}",
            f"- Candidate testbench binding ready: {summary['candidate_binding_ready_count']}/{summary['family_count']}",
            f"- Private reference-fixture migration actions: {summary['reference_fixture_action_count']}",
            "",
            "## Release Binding",
            "",
            f"- Status: `{binding['status']}`",
            f"- Manifest: `{binding.get('manifest_path')}`",
            f"- SHA-256: `{binding.get('manifest_sha256')}`",
            "",
            "The snapshot is not scoreable until the base release is frozen, every manual suite review is resolved,",
            "the active five-mutation suites have canonical evidence, and Gate 3 certificates are generated.",
            "",
            "## Safe Next Step",
            "",
            "Re-run this builder with `--base-release-manifest` after the DUT closeout thread publishes its immutable",
            "manifest. Compare the new input hashes, resolve `OVERFIVE_REVIEW.json`, then audit the 814",
            "cross-profile cells before scheduling only the rows that cannot be carried forward.",
            "",
        ]
    )


def _render_overfive_review(records: list[dict[str, Any]]) -> str:
    rows = [
        "# Over-Five Mutation Semantic Review",
        "",
        "These proposals are not final assignments. Review whether the selected five retain the strongest distinct",
        "fault meanings and whether the Bugfix seed is a representative single semantic fault.",
        "",
        "| Family | Count | Bugfix seed | Proposed T | Excluded |",
        "|---|---:|---|---|---|",
    ]
    for record in records:
        catalog = record["catalog"]
        draft = record["draft_derivation_manifest"] or {}
        assignment = draft.get("negative_assignment") or {}
        rows.append(
            "| "
            + " | ".join(
                [
                    record["family_id"],
                    str(catalog["catalog_certified_count"]),
                    str(assignment.get("bugfix_seed") or "BLOCKED"),
                    ", ".join(assignment.get("testbench_suite") or []),
                    ", ".join(catalog["excluded_from_proposed_suite"]) or "none",
                ]
            )
            + " |"
        )
    rows.extend(
        [
            "",
            "Detailed fault classes, trigger conditions, properties, and legacy profiles are retained in",
            "`OVERFIVE_REVIEW.json`.",
            "",
        ]
    )
    return "\n".join(rows)


def build(package_root: Path, output_dir: Path, base_release_manifest: Path | None) -> dict[str, Any]:
    numbering_path = package_root / "reports" / "v4_task_family_numbering" / "numbering_plan.json"
    requirements_path = package_root / "V4_TRI_FORM_BENCHMARK_REQUIREMENTS.md"
    numbering = _read_json(numbering_path)
    rows = numbering.get("rows") or []
    records = [_family_record(package_root, row) for row in rows]

    mutation_distribution = Counter(record["catalog"]["mutation_count"] for record in records)
    eligible_distribution = Counter(record["catalog"]["catalog_certified_count"] for record in records)
    base_binding = {
        "status": "pending_frozen_dut_release",
        "manifest_path": None,
        "manifest_sha256": None,
        "task_hash_match_count": 0,
    }
    if base_release_manifest is not None:
        resolved = base_release_manifest.expanduser().resolve()
        if not resolved.is_file():
            raise SystemExit(f"base release manifest does not exist: {resolved}")
        release_manifest = _read_json(resolved)
        release_tasks = _validate_base_release_manifest(release_manifest)
        task_hash_match_count = 0
        for record in records:
            release_task = release_tasks[record["family_id"]]
            release_hashes = release_task.get("evaluator_hashes") or {}
            draft = record.get("draft_derivation_manifest") or {}
            base_dut = draft.get("base_dut") or {
                "mutation_catalog_sha256": _sha256(
                    package_root / record["source"]["mutation_catalog"]
                ),
                "canonical_score_tb_sha256": _sha256(
                    package_root / record["source"]["score_deck"]
                ),
            }
            catalog_match = (
                base_dut.get("mutation_catalog_sha256")
                == release_hashes.get("mutation_catalog.json")
            )
            score_deck_match = (
                base_dut.get("canonical_score_tb_sha256")
                == release_hashes.get("score_tb.scs")
            )
            target_match = list(record["derived_tasks"]["bugfix"]["candidate_artifacts"]) == list(
                release_task.get("target_artifacts") or []
            )
            hashes_match = catalog_match and score_deck_match and target_match
            if hashes_match:
                task_hash_match_count += 1
            else:
                record["blockers"].append("base_release_task_hash_mismatch")
                record["review_status"] = "blocked"
                if record.get("draft_derivation_manifest"):
                    record["draft_derivation_manifest"]["selection_evidence"][
                        "semantic_review_status"
                    ] = "blocked"
            record["base_release_task_binding"] = {
                "release_dir": release_task.get("release_dir"),
                "certification_sha256": release_hashes.get("certification.json"),
                "mutation_catalog_hash_match": catalog_match,
                "score_deck_hash_match": score_deck_match,
                "target_artifacts_match": target_match,
                "status": "match" if hashes_match else "mismatch",
            }
        if task_hash_match_count != 400:
            raise SystemExit(
                f"base release binding mismatch: {task_hash_match_count}/400 task hashes match"
            )
        base_binding = {
            "status": "bound_to_frozen_dut_release",
            "manifest_path": str(resolved),
            "manifest_sha256": _sha256(resolved),
            "claim_boundary": release_manifest["claim_boundary"],
            "task_hash_match_count": task_hash_match_count,
        }

    summary = {
        "family_count": len(records),
        "catalog_mutation_count": sum(record["catalog"]["mutation_count"] for record in records),
        "formal_active_mutation_count": sum(
            len(record["draft_derivation_manifest"]["negative_assignment"]["testbench_suite"])
            for record in records
            if record["draft_derivation_manifest"]
        ),
        "provenance_only_extra_count": sum(
            len(record["catalog"]["excluded_from_proposed_suite"]) for record in records
        ),
        "catalog_certified_mutation_count": sum(
            record["catalog"]["catalog_certified_count"] for record in records
        ),
        "mutation_count_distribution": {str(key): value for key, value in sorted(mutation_distribution.items())},
        "eligible_count_distribution": {str(key): value for key, value in sorted(eligible_distribution.items())},
        "exactly_five_eligible_count": sum(
            record["catalog"]["catalog_certified_count"] == 5 for record in records
        ),
        "overfive_eligible_count": sum(
            record["catalog"]["catalog_certified_count"] > 5 for record in records
        ),
        "blocked_family_count": sum(record["review_status"] == "blocked" for record in records),
        "manual_review_family_count": sum(
            record["review_status"] == "manual_review_required" for record in records
        ),
        "provisional_complete_family_count": sum(
            record["review_status"] == "provisional_complete" for record in records
        ),
        "candidate_binding_ready_count": sum(
            record["canonical_suite"]["candidate_binding_ready"] for record in records
        ),
        "reference_fixture_status_distribution": dict(
            sorted(
                Counter(
                    record["canonical_suite"]["reference_fixture_status"] for record in records
                ).items()
            )
        ),
        "reference_fixture_action_count": sum(
            record["canonical_suite"]["reference_fixture_status"] != "ready"
            for record in records
        ),
        "legacy_feedback_differs_count": sum(
            record["canonical_suite"]["legacy_feedback_differs"] for record in records
        ),
        "reused_score_profile_negative_count": sum(
            len(record["canonical_suite"]["reused_score_profile_negative_evidence"])
            for record in records
        ),
        "cross_profile_validation_candidate_count": sum(
            len(record["canonical_suite"]["cross_profile_validation_candidates"])
            for record in records
        ),
        "cross_profile_validation_family_count": sum(
            bool(record["canonical_suite"]["cross_profile_validation_candidates"])
            for record in records
        ),
        "mandatory_new_gold_run_count": 0,
    }
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "scoreable": False,
        "status": "derivation_prep_unbound" if base_release_manifest is None else "derivation_prep_bound",
        "policy_id": "v4-tri-form-requirements-2026-07-12",
        "inputs": {
            "requirements_path": _relative(requirements_path, package_root),
            "requirements_sha256": _sha256(requirements_path),
            "numbering_plan_path": _relative(numbering_path, package_root),
            "numbering_plan_sha256": _sha256(numbering_path),
        },
        "base_release_binding": base_binding,
        "summary": summary,
        "families": records,
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    _write_json(output_dir / "PREP_MANIFEST.json", manifest)
    _write_json(
        output_dir / "OVERFIVE_REVIEW.json",
        {
            "schema_version": "v4-overfive-semantic-review-v1",
            "families": [
                record
                for record in records
                if record["catalog"]["catalog_certified_count"] > 5
                or "selected_suite_has_duplicate_semantic_meaning_proxy" in record["review_reasons"]
            ],
        },
    )
    overfive_records = [
        record
        for record in records
        if record["catalog"]["catalog_certified_count"] > 5
        or "selected_suite_has_duplicate_semantic_meaning_proxy" in record["review_reasons"]
    ]
    (output_dir / "OVERFIVE_REVIEW.md").write_text(
        _render_overfive_review(overfive_records), encoding="utf-8"
    )
    _write_json(
        output_dir / "RUNNER_GAP_MATRIX.json",
        {
            "schema_version": "v4-tri-form-runner-gap-matrix-v1",
            "canonical_suite_policy": (
                "candidate testbenches use ./dut stable binding; private reference score_tb.scs "
                "keeps its certified bytes and uses a content-identical path adapter"
            ),
            "legacy_runner_status": "incompatible_visible_private_partition",
            "required_runner_changes": [
                "replace public/private mutation subsets with one five-case suite",
                "consume mutation_catalog.mutations rather than legacy cases/negatives only",
                "evaluate one unchanged candidate testbench against reference plus five opaque negatives",
                "report invalid_run separately from behaviorally_killed and survived",
                "use standalone Rust EVAS for feedback and one sealed Spectre invocation for final score",
            ],
            "families": [
                {
                    "family_id": record["family_id"],
                    "candidate_binding_ready": record["canonical_suite"]["candidate_binding_ready"],
                    "reference_fixture_status": record["canonical_suite"][
                        "reference_fixture_status"
                    ],
                    "cross_profile_validation_candidates": record["canonical_suite"][
                        "cross_profile_validation_candidates"
                    ],
                    "blockers": record["blockers"],
                }
                for record in records
                if record["canonical_suite"]["cross_profile_validation_candidates"]
                or record["canonical_suite"]["reference_fixture_status"] != "ready"
                or record["blockers"]
            ],
        },
    )
    _write_json(
        output_dir / "SCORE_REPLAY_QUEUE.json",
        {
            "schema_version": "v4-tri-form-score-replay-queue-v1",
            "status": "carry_forward_audit_required_before_execution",
            "mandatory_new_gold_runs": [],
            "cross_profile_validation_candidates": [
                {
                    "family_id": record["family_id"],
                    "mutation_id": mutation_id,
                    "reason": "mutation_only_certified_under_legacy_feedback_deck",
                    "score_deck": record["source"]["score_deck"],
                    "disposition": "reuse_if_semantic_witness_portable_else_targeted_run",
                }
                for record in records
                for mutation_id in record["canonical_suite"][
                    "cross_profile_validation_candidates"
                ]
            ],
            "reference_fixture_migration_actions": [
                {
                    "family_id": record["family_id"],
                    "status": record["canonical_suite"]["reference_fixture_status"],
                    "score_deck": record["source"]["score_deck"],
                    "analog_rerun_required": False,
                }
                for record in records
                if record["canonical_suite"]["reference_fixture_status"] != "ready"
            ],
        },
    )
    _write_json(
        output_dir / "DERIVATIVE_TASK_INDEX.json",
        {
            "schema_version": "v4-tri-form-derivative-task-index-v1",
            "status": "planned_unmaterialized",
            "base_release_binding": base_binding,
            "task_count": 800,
            "tasks": [
                {
                    "task_id": derived["task_id"],
                    "form": form,
                    "formal_dir": derived["formal_dir"],
                    "source_family_id": record["family_id"],
                    "candidate_artifacts": derived["candidate_artifacts"],
                    "materialization_status": "pending_gate3",
                }
                for record in records
                for form, derived in record["derived_tasks"].items()
            ],
        },
    )
    _write_json(
        output_dir / "ACTIVE_MUTATION_SUITE_INDEX.json",
        {
            "schema_version": "v4-tri-form-active-mutation-suite-v1",
            "status": "selected_pending_semantic_review_and_gate3",
            "policy": (
                "Exactly five active negatives per family; Bugfix seed is a member of the "
                "same five-case Testbench suite."
            ),
            "family_count": 400,
            "active_mutation_count": summary["formal_active_mutation_count"],
            "families": [
                {
                    "family_id": record["family_id"],
                    "bugfix_seed": record["draft_derivation_manifest"]["negative_assignment"][
                        "bugfix_seed"
                    ],
                    "testbench_suite": record["draft_derivation_manifest"][
                        "negative_assignment"
                    ]["testbench_suite"],
                    "review_status": record["review_status"],
                }
                for record in records
            ],
        },
    )
    _write_json(
        output_dir / "EXCLUDED_MUTATION_ARCHIVE_INDEX.json",
        {
            "schema_version": "v4-tri-form-excluded-mutation-archive-v1",
            "status": "provenance_only_not_in_formal_release",
            "policy": (
                "Retain source lineage and evidence outside the scored release; do not "
                "export these mutations as active DUT, Testbench, or Bugfix cases."
            ),
            "excluded_mutation_count": summary["provenance_only_extra_count"],
            "families": [
                {
                    "family_id": record["family_id"],
                    "source_catalog": record["source"]["mutation_catalog"],
                    "excluded_mutations": record["catalog"]["excluded_semantics"],
                }
                for record in records
                if record["catalog"]["excluded_semantics"]
            ],
        },
    )
    _write_json(
        output_dir / "BLOCKERS.json",
        {
            "schema_version": "v4-tri-form-derivation-blockers-v1",
            "families": [
                {
                    "family_id": record["family_id"],
                    "blockers": record["blockers"],
                    "review_reasons": record["review_reasons"],
                }
                for record in records
                if record["blockers"]
            ],
        },
    )
    (output_dir / "HANDOFF.md").write_text(_render_handoff(manifest), encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    default_package_root = Path(__file__).resolve().parents[2]
    parser.add_argument("--package-root", type=Path, default=default_package_root)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--base-release-manifest", type=Path)
    args = parser.parse_args()
    package_root = args.package_root.expanduser().resolve()
    output_dir = (
        args.output_dir.expanduser().resolve()
        if args.output_dir
        else Path(__file__).resolve().parent
    )
    manifest = build(package_root, output_dir, args.base_release_manifest)
    summary = manifest["summary"]
    print(
        "TRI_FORM_PREP "
        f"families={summary['family_count']} "
        f"mutations={summary['catalog_mutation_count']} "
        f"active={summary['formal_active_mutation_count']} "
        f"blocked={summary['blocked_family_count']} "
        f"manual_review={summary['manual_review_family_count']} "
        f"cross_profile={summary['cross_profile_validation_candidate_count']}"
    )
    return 0 if summary["family_count"] == 400 else 1


if __name__ == "__main__":
    raise SystemExit(main())
