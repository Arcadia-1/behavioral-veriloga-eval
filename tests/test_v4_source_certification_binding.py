from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


PREP = (
    Path(__file__).resolve().parents[1]
    / "benchmark-vabench-release-v4"
    / "operations"
    / "tri_form_derivation_prep"
)
if str(PREP) not in sys.path:
    sys.path.insert(0, str(PREP))

from source_certification_binding import inspect_source_certification_reuse  # noqa: E402


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_sha_by_file_hash(path: Path, *, exclude: set[str] | None = None) -> str:
    exclude = exclude or set()
    digest = hashlib.sha256()
    for item in sorted(path.rglob("*")):
        if not item.is_file() or item.name in exclude:
            continue
        digest.update(item.relative_to(path).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(file_sha(item).encode("ascii"))
        digest.update(b"\0")
    return digest.hexdigest()


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def source_fixture(tmp_path: Path) -> tuple[Path, dict[str, dict]]:
    source = tmp_path / "source"
    task = source / "001-sample"
    evaluator = task / "evaluator"
    public = task / "public" / "task"
    mutation = evaluator / "mutation_bundles" / "neg_001"
    (evaluator / "profiles").mkdir(parents=True)
    (evaluator / "solution").mkdir()
    mutation.mkdir(parents=True)
    public.mkdir(parents=True)

    files = {
        evaluator / "family_spec.json": '{"family_id":"001","revision":"current"}\n',
        evaluator / "checker_profile.json": '{"checker_task_id":"v4_001_sample"}\n',
        evaluator / "harness_spec.json": '{"harness":"current"}\n',
        evaluator / "profiles" / "feedback.json": '{"profile":"feedback-current"}\n',
        evaluator / "profiles" / "score.json": '{"profile":"score-current"}\n',
        evaluator / "score_tb.scs": "score deck current\n",
        evaluator / "mutation_catalog.json": '{"mutations":[{"id":"neg_001"}]}\n',
        evaluator / "solution" / "dut.va": "module dut; endmodule\n",
        mutation / "dut.va": "module dut; // negative\nendmodule\n",
        public / "feedback_tb.scs": "feedback deck current\n",
        public / "instruction.md": "instruction current\n",
        public / "public_contract.json": '{"family_id":"001"}\n',
    }
    for path, text in files.items():
        path.write_text(text, encoding="utf-8")
    harness_sha = file_sha(evaluator / "harness_spec.json")
    write_json(
        evaluator / "profiles" / "feedback.json",
        {"harness_spec_sha256": harness_sha, "profile": "feedback-current"},
    )
    write_json(
        evaluator / "profiles" / "score.json",
        {"harness_spec_sha256": harness_sha, "profile": "score-current"},
    )

    actual = {
        "checker_profile": file_sha(evaluator / "checker_profile.json"),
        "family_spec": file_sha(evaluator / "family_spec.json"),
        "feedback_profile": file_sha(evaluator / "profiles" / "feedback.json"),
        "gold_bundle": tree_sha_by_file_hash(evaluator / "solution"),
        "harness_spec": file_sha(evaluator / "harness_spec.json"),
        "score_profile": file_sha(evaluator / "profiles" / "score.json"),
    }
    task_inputs = {
        "checker_profile_sha256": actual["checker_profile"],
        "family_spec_sha256": actual["family_spec"],
        "feedback_deck_sha256": file_sha(public / "feedback_tb.scs"),
        "feedback_profile_sha256": actual["feedback_profile"],
        "gold_bundle_sha256": actual["gold_bundle"],
        "harness_spec_sha256": actual["harness_spec"],
        "score_deck_sha256": file_sha(evaluator / "score_tb.scs"),
        "score_profile_sha256": actual["score_profile"],
    }
    certification = {
        "schema_version": "v4-task-certification-v3",
        "status": "gate2_pass",
        "evaluators": {"evas": {"status": "pass"}, "spectre": {"status": "pass"}},
        "input_hashes": actual,
        "component_fingerprints": {"task_inputs": task_inputs},
    }
    write_json(evaluator / "certification.json", certification)
    negative_certification = {
        "schema_version": "v4-negative-certification-v1",
        "outcome": "killed_behaviorally",
        "evaluators": {
            "evas": "compile_pass_behavior_fail",
            "spectre": "compile_pass_behavior_fail",
        },
        "inputs": {
            "checker_profile_sha256": actual["checker_profile"],
            "harness_spec_sha256": actual["harness_spec"],
            "profile_sha256": actual["feedback_profile"],
            "mutation_bundle_sha256": tree_sha_by_file_hash(
                mutation, exclude={"certification.json"}
            ),
        },
    }
    write_json(mutation / "certification.json", negative_certification)

    task_record = {
        "evaluator_hashes": {
            "certification.json": file_sha(evaluator / "certification.json"),
            "checker_profile.json": actual["checker_profile"],
            "family_spec.json": actual["family_spec"],
            "harness_spec.json": actual["harness_spec"],
            "mutation_catalog.json": file_sha(evaluator / "mutation_catalog.json"),
            "profiles/feedback.json": actual["feedback_profile"],
            "profiles/score.json": actual["score_profile"],
            "score_tb.scs": file_sha(evaluator / "score_tb.scs"),
        },
        "public_hashes": {
            "feedback_tb.scs": file_sha(public / "feedback_tb.scs"),
            "instruction.md": file_sha(public / "instruction.md"),
            "public_contract.json": file_sha(public / "public_contract.json"),
        },
        "readiness_evidence": {
            "path": "evaluator/certification.json",
            "sha256": file_sha(evaluator / "certification.json"),
        },
    }
    write_json(evaluator / "task_record.json", task_record)
    row = {
        "canonical_dut_id": "001",
        "release_dir": task.name,
        "hashes": {
            "task_record_sha256": file_sha(evaluator / "task_record.json"),
            "task_certification_sha256": file_sha(evaluator / "certification.json"),
            "mutation_catalog_sha256": file_sha(evaluator / "mutation_catalog.json"),
            "score_deck_sha256": file_sha(evaluator / "score_tb.scs"),
        },
        "active_mutations": [
            {
                "mutation_id": "neg_001",
                "certification_path": "evaluator/mutation_bundles/neg_001/certification.json",
                "certification_sha256": file_sha(mutation / "certification.json"),
                "mutation_bundle_sha256": tree_sha_by_file_hash(mutation),
            }
        ],
    }
    return source, {"001": row}


def test_current_source_inputs_are_reusable_when_every_hash_binding_matches(tmp_path: Path) -> None:
    source, rows = source_fixture(tmp_path)
    summary, problems = inspect_source_certification_reuse(source, rows)
    assert problems == []
    assert summary["source_dut_gold_certification_count"] == 1
    assert summary["source_negative_certification_count"] == 1
    assert summary["simulation_rerun_required_for_materialization"] is False
    assert summary["stale_certification_family_ids"] == []


def test_stale_inner_hashes_cannot_be_reused_even_when_outer_file_hashes_match(tmp_path: Path) -> None:
    source, rows = source_fixture(tmp_path)
    evaluator = source / "001-sample" / "evaluator"

    # Simulate the current regression: mutate bound inputs, while keeping the
    # old task record/certification files and updating only their outer row SHA.
    (evaluator / "family_spec.json").write_text(
        '{"family_id":"001","revision":"changed-after-certification"}\n',
        encoding="utf-8",
    )
    (evaluator / "harness_spec.json").write_text(
        '{"harness":"changed-after-certification"}\n', encoding="utf-8"
    )

    summary, problems = inspect_source_certification_reuse(source, rows)
    assert any("task record evaluator hash mismatch: family_spec.json" in item for item in problems)
    assert any("gold certification input hash mismatch: family_spec" in item for item in problems)
    assert any("feedback profile harness_spec_sha256 mismatch" in item for item in problems)
    assert any("negative neg_001 input hash mismatch: harness_spec_sha256" in item for item in problems)
    assert summary["source_dut_gold_certification_count"] == 0
    assert summary["source_negative_certification_count"] == 0
    assert summary["simulation_rerun_required_for_materialization"] is True
    assert summary["stale_certification_family_ids"] == ["001"]


def test_unshipped_hash_only_refresh_cannot_revalidate_a_negative(tmp_path: Path) -> None:
    source, rows = source_fixture(tmp_path)
    task = source / "001-sample"
    evaluator = task / "evaluator"
    mutation = evaluator / "mutation_bundles" / "neg_001"
    certificate_path = mutation / "certification.json"

    (evaluator / "harness_spec.json").write_text(
        '{"harness":"changed-after-certification"}\n', encoding="utf-8"
    )
    certificate = json.loads(certificate_path.read_text())
    certificate["refresh_evidence"] = {
        "candidate_testbench_sha256": file_sha(task / "public" / "task" / "feedback_tb.scs"),
        "case_id": "neg_001",
        "claim_scope": "testbench_reference_negative_behavioral_kill",
        "evaluators": {
            "evas": {"artifact_sha256": "a" * 64, "status": "pass"},
            "spectre": {"artifact_sha256": "b" * 64, "status": "pass"},
        },
        "outcome": "killed_behaviorally",
        "schema_version": "v4-source-certification-refresh-evidence-v1",
        "task_id": "v4-501",
    }
    write_json(certificate_path, certificate)
    mutation_row = rows["001"]["active_mutations"][0]
    mutation_row["certification_sha256"] = file_sha(certificate_path)
    mutation_row["mutation_bundle_sha256"] = tree_sha_by_file_hash(mutation)

    summary, _ = inspect_source_certification_reuse(source, rows)

    assert summary["source_dut_gold_certification_count"] == 0
    assert summary["source_negative_certification_count"] == 0
    assert summary["stale_gold_family_ids"] == ["001"]
    assert summary["stale_negative_case_ids"] == ["001/neg_001"]

