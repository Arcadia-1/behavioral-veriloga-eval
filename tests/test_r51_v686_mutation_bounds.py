from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
    ROOT
    / "benchmark-vabench-release-v4/provenance"
    / "dut-base-v3-exact-five-hash-bound-v2"
)
SOURCE_TASK = SOURCE / "186-sarfend-logic-4b"
RELEASE = ROOT / "benchmark-vabench-release-v4/release/benchmarkv4-r51"
TESTBENCH_TASK = RELEASE / "tasks/686-sarfend-logic-4b-testbench"
BUGFIX_TASK = RELEASE / "tasks/1186-sarfend-logic-4b-bugfix"
ARTIFACT = "sarfend_logic_4b.va"
BOUNDED_MUTATIONS = {
    "neg_002_inverted_comparator",
    "neg_003_no_test_override",
    "neg_004_wrong_dout_mapping",
    "neg_005_metric_scale_low",
}
BOUND_GUARD = "if ((V(clks)<0.45) && (pointer<4)) begin"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def raw_tree_sha(path: Path) -> str:
    digest = hashlib.sha256()
    for item in sorted(path.rglob("*")):
        if item.is_file():
            digest.update(item.relative_to(path).as_posix().encode("utf-8"))
            digest.update(b"\0")
            digest.update(item.read_bytes())
            digest.update(b"\0")
    return digest.hexdigest()


def file_hash_tree_sha(path: Path) -> str:
    digest = hashlib.sha256()
    for item in sorted(path.rglob("*")):
        if item.is_file():
            digest.update(item.relative_to(path).as_posix().encode("utf-8"))
            digest.update(b"\0")
            digest.update(file_sha(item).encode("ascii"))
            digest.update(b"\0")
    return digest.hexdigest()


def public_bundle_sha(task: Path) -> str:
    public = task / "public"
    digest = hashlib.sha256()
    for item in sorted(public.rglob("*")):
        if item.is_file():
            digest.update(item.relative_to(public).as_posix().encode("utf-8"))
            digest.update(b"\0")
            digest.update(item.read_bytes())
            digest.update(b"\0")
    return digest.hexdigest()


def test_family_186_mutations_keep_bounds_across_materialized_copies() -> None:
    evaluator = TESTBENCH_TASK / "evaluator"
    source_evaluator = SOURCE_TASK / "evaluator"
    policy = read_json(evaluator / "score_policy.json")

    for index, mutation_id in enumerate(
        policy["negative_suite_mutation_ids"], start=1
    ):
        source = (
            source_evaluator / "mutation_bundles" / mutation_id / ARTIFACT
        )
        copies = [
            evaluator / "mutation_bundles" / mutation_id / ARTIFACT,
            TESTBENCH_TASK
            / "public/visible_fixtures"
            / f"mutation_{index:02d}/dut"
            / ARTIFACT,
            evaluator
            / "trusted_replay_fixtures"
            / f"mutation_{index:02d}/dut"
            / ARTIFACT,
        ]
        assert all(copy.read_bytes() == source.read_bytes() for copy in copies)
        if mutation_id in BOUNDED_MUTATIONS:
            assert BOUND_GUARD in source.read_text(encoding="utf-8")

    bugfix_seed = policy["bugfix_seed_mutation_id"]
    bugfix_source = (
        source_evaluator / "mutation_bundles" / bugfix_seed / ARTIFACT
    )
    assert (
        BUGFIX_TASK / "public/buggy_bundle" / ARTIFACT
    ).read_bytes() == bugfix_source.read_bytes()
    assert BOUND_GUARD in bugfix_source.read_text(encoding="utf-8")


def test_family_186_mutation_and_fixture_hash_bindings_are_current() -> None:
    source_evaluator = SOURCE_TASK / "evaluator"
    evaluator = TESTBENCH_TASK / "evaluator"

    for relative in ("mutation_catalog.json", "mutation_bundles/manifest.json"):
        assert (evaluator / relative).read_bytes() == (
            source_evaluator / relative
        ).read_bytes()
        payload = read_json(source_evaluator / relative)
        for row in payload["mutations"]:
            artifact = (
                source_evaluator
                / "mutation_bundles"
                / row["id"]
                / ARTIFACT
            )
            assert row["artifact_hashes"][ARTIFACT] == file_sha(artifact)

    catalog_sha = file_sha(source_evaluator / "mutation_catalog.json")
    assert read_json(source_evaluator / "derivation_manifest.json")[
        "mutation_catalog_sha256"
    ] == catalog_sha
    assert read_json(evaluator / "score_policy.json")[
        "mutation_catalog_sha256"
    ] == catalog_sha

    registry = read_json(SOURCE / "score_denominator_registry/186.json")["task"]
    assert registry["hashes"]["mutation_catalog_sha256"] == catalog_sha
    assert registry["hashes"]["task_record_sha256"] == file_sha(
        source_evaluator / "task_record.json"
    )
    for row in registry["active_mutations"]:
        bundle = source_evaluator / "mutation_bundles" / row["mutation_id"]
        assert row["mutation_bundle_sha256"] == file_hash_tree_sha(bundle)

    visible = TESTBENCH_TASK / "public/visible_fixtures"
    trusted = evaluator / "trusted_replay_fixtures"
    runtime = read_json(TESTBENCH_TASK / "public/evas_runtime.json")
    record = read_json(TESTBENCH_TASK / "task_record.json")
    assert raw_tree_sha(visible) == raw_tree_sha(trusted)
    assert runtime["fixture_tree_sha256"] == raw_tree_sha(visible)
    assert (evaluator / "trusted_replay_suite.json").read_bytes() == (
        TESTBENCH_TASK / "public/evas_runtime.json"
    ).read_bytes()
    assert record["evaluation_binding"]["public_fixture_tree_sha256"] == raw_tree_sha(
        visible
    )
    assert record["public_bundle_sha256"] == public_bundle_sha(TESTBENCH_TASK)
