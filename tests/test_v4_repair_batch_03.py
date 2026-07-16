from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
    ROOT
    / "benchmark-vabench-release-v4"
    / "provenance"
    / "dut-base-v3-exact-five-hash-bound-v2"
)
RENDERER = ROOT / "benchmark-vabench-release-v4" / "scripts" / "render_v4_harness.py"
PARITY = ROOT / "benchmark-vabench-release-v4" / "scripts" / "validate_v4_profile_parity.py"
CERTIFIER = ROOT / "benchmark-vabench-release-v4" / "scripts" / "validate_v4_checker_batch.py"
PREP = (
    ROOT
    / "benchmark-vabench-release-v4"
    / "operations"
    / "tri_form_derivation_prep"
)
FAMILIES = tuple(f"{value:03d}" for value in range(21, 31))


def _family(family_id: str) -> Path:
    matches = sorted(SOURCE.glob(f"{family_id}-*"))
    assert len(matches) == 1
    return matches[0]


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _tree_sha(path: Path) -> str:
    digest = hashlib.sha256()
    for item in sorted(path.rglob("*")):
        if not item.is_file():
            continue
        digest.update(item.relative_to(path).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(_sha(item).encode("ascii"))
        digest.update(b"\0")
    return digest.hexdigest()


def _materialize_batch(output: Path) -> list[dict[str, object]]:
    sys.path.insert(0, str(PREP))
    from materialize_tri_form_release import (  # noqa: PLC0415
        build_bugfix_view,
        build_dut_view,
        build_testbench_view,
        file_sha,
        install_prompt_assets,
        read_json,
        select_bugfix_seed,
        write_json,
    )

    denominator = read_json(SOURCE / "score_denominator_manifest.json")
    rows = {
        str(row["canonical_dut_id"]): row
        for row in denominator["tasks"]
        if str(row["canonical_dut_id"]) in FAMILIES
    }
    assert sorted(rows) == list(FAMILIES)
    task_rows: list[dict[str, object]] = []
    for family_id in FAMILIES:
        row = rows[family_id]
        source_task = SOURCE / str(row["release_dir"])
        spec_path = source_task / "evaluator" / "family_spec.json"
        spec = read_json(spec_path)
        seed_review = select_bugfix_seed(row)
        task_rows.extend(
            [
                build_dut_view(output, source_task, row, spec, file_sha(spec_path)),
                build_testbench_view(
                    output, source_task, row, spec, file_sha(spec_path), seed_review
                ),
                build_bugfix_view(
                    output, source_task, row, spec, file_sha(spec_path), seed_review
                ),
            ]
        )
    task_rows.sort(key=lambda item: int(str(item["task_id"]).split("-", 1)[1]))
    install_prompt_assets(output)
    write_json(
        output / "TASK_INDEX.json",
        {"schema_version": "v4-benchmarkv4-task-index-v1", "tasks": task_rows},
    )
    return task_rows


def test_batch_03_profiles_have_zero_semantic_drift() -> None:
    result = subprocess.run(
        [sys.executable, str(PARITY), "--family-range", "021-030"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads(result.stdout)
    assert report["status"] == "PASS"
    assert report["checked_families"] == list(FAMILIES)


def test_batch_03_source_profiles_are_deterministically_regenerated(tmp_path: Path) -> None:
    for family_id in FAMILIES:
        task = _family(family_id)
        evaluator = task / "evaluator"
        for profile_name in ("feedback", "score"):
            profile_out = tmp_path / family_id / f"{profile_name}.json"
            deck_out = tmp_path / family_id / f"{profile_name}.scs"
            result = subprocess.run(
                [
                    sys.executable,
                    str(RENDERER),
                    "--spec",
                    str(evaluator / "harness_spec.json"),
                    "--profile",
                    profile_name,
                    "--profile-output",
                    str(profile_out),
                    "--deck-output",
                    str(deck_out),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            assert result.returncode == 0, result.stdout + result.stderr
            expected_profile = evaluator / "profiles" / f"{profile_name}.json"
            expected_deck = (
                task / "public" / "task" / "feedback_tb.scs"
                if profile_name == "feedback"
                else evaluator / "score_tb.scs"
            )
            assert _sha(profile_out) == _sha(expected_profile)
            assert _sha(deck_out) == _sha(expected_deck)


def test_batch_03_all_three_forms_materialize_deterministically(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    first_rows = _materialize_batch(first)
    second_rows = _materialize_batch(second)

    assert len(first_rows) == 30
    assert first_rows == second_rows
    assert _tree_sha(first) == _tree_sha(second)
    assert {form: sum(row["form"] == form for row in first_rows) for form in (
        "dut",
        "testbench",
        "bugfix",
    )} == {"dut": 10, "testbench": 10, "bugfix": 10}

    for row in first_rows:
        task = first / str(row["task_dir"])
        record = json.loads((task / "task_record.json").read_text(encoding="utf-8"))
        assert record["task_id"] == row["task_id"]
        assert record["family_id"] == row["family_id"]
        assert record["form"] == row["form"]
        assert (task / "public_contract.json").is_file()
        assert (task / "evaluator" / "checker_profile.json").is_file()


def test_batch_03_checkers_are_stimulus_relative_and_emit_public_properties() -> None:
    absolute_window = re.compile(r"\b(?:time|t|start|stop)\s*(?:<|>|<=|>=)\s*[0-9.]+e-9")
    for family_id in FAMILIES:
        task = _family(family_id)
        checker_path = ROOT / "runners" / "checkers" / "v4" / f"task_{family_id}.py"
        checker_text = checker_path.read_text(encoding="utf-8")
        properties = json.loads(
            (task / "evaluator" / "harness_spec.json").read_text(encoding="utf-8")
        )["property_ids"]
        assert absolute_window.search(checker_text) is None, checker_path
        assert all(property_id in checker_text for property_id in properties), family_id


def test_batch_03_trace_contracts_equal_the_public_observable_contract() -> None:
    for family_id in FAMILIES:
        task = _family(family_id)
        public = json.loads(
            (task / "public" / "task" / "public_contract.json").read_text(encoding="utf-8")
        )
        checker = json.loads(
            (task / "evaluator" / "checker_profile.json").read_text(encoding="utf-8")
        )
        assert checker["trace_contract"]["public_observables"] == public["public_observables"]
        assert checker["trace_contract"]["extra_trace_signals"] == []


def test_batch_03_records_bind_profiles_checker_and_five_mutations() -> None:
    denominator = json.loads((SOURCE / "score_denominator_manifest.json").read_text(encoding="utf-8"))
    rows = {str(row["canonical_dut_id"]): row for row in denominator["tasks"]}
    for family_id in FAMILIES:
        task = _family(family_id)
        evaluator = task / "evaluator"
        record = json.loads((evaluator / "task_record.json").read_text(encoding="utf-8"))
        harness = json.loads((evaluator / "harness_spec.json").read_text(encoding="utf-8"))
        manifest = json.loads(
            (evaluator / "mutation_bundles" / "manifest.json").read_text(encoding="utf-8")
        )
        assert len(manifest["mutations"]) == 5
        assert rows[family_id]["active_mutation_count"] == 5
        assert len(rows[family_id]["active_mutations"]) == 5
        for relative in (
            "checker_profile.json",
            "harness_spec.json",
            "profiles/feedback.json",
            "profiles/score.json",
            "score_tb.scs",
        ):
            assert record["evaluator_hashes"][relative] == _sha(evaluator / relative)
        assert record["public_hashes"]["feedback_tb.scs"] == _sha(
            task / "public" / "task" / "feedback_tb.scs"
        )
        assert harness["source_contract"]["checker_profile_sha256"] == _sha(
            evaluator / "checker_profile.json"
        )


def test_batch_03_checkers_reject_complete_but_unexcited_traces_with_diagnostics() -> None:
    from runners.checkers.v4.registry import load_checker

    for family_id in FAMILIES:
        task = _family(family_id)
        record = json.loads(
            (task / "evaluator" / "task_record.json").read_text(encoding="utf-8")
        )
        harness = json.loads(
            (task / "evaluator" / "harness_spec.json").read_text(encoding="utf-8")
        )
        public = json.loads(
            (task / "public" / "task" / "public_contract.json").read_text(encoding="utf-8")
        )
        checker = load_checker(record["checker_task_id"])
        assert checker is not None
        rows = [
            {"time": index * 1e-9, **{signal: 0.0 for signal in public["public_observables"]}}
            for index in range(8)
        ]
        passed, note = checker(rows)
        assert not passed, family_id
        assert "checked=" in note and "mismatch_count=" in note
        assert all(property_id in note for property_id in harness["property_ids"]), note


def test_batch_03_timing_metamorph_is_exact_and_certifier_is_importable() -> None:
    from runners.checkers.v4.stimulus_relative import transformed_rows

    rows = [{"time": 0.0, "x": 1.0}, {"time": 4e-9, "x": 2.0}]
    transformed = transformed_rows(rows, scale=1.37, shift_s=2e-9)
    assert transformed[0] == {"time": 2e-9, "x": 1.0}
    assert transformed[1]["time"] == 1.37 * 4e-9 + 2e-9
    result = subprocess.run(
        [sys.executable, str(CERTIFIER), "--help"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "timing-scale" in result.stdout


def test_batch_03_certifier_requires_explicit_evas2_backend(tmp_path: Path) -> None:
    env = os.environ.copy()
    env.pop("EVAS_ENGINE", None)
    env.pop("VAEVAS_DEFAULT_EVAS_ENGINE", None)
    result = subprocess.run(
        [
            sys.executable,
            str(CERTIFIER),
            "--family-range",
            "021-021",
            "--output",
            str(tmp_path / "report.json"),
            "--work-root",
            str(tmp_path / "work"),
        ],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode != 0
    assert "requires EVAS_ENGINE=evas2" in result.stderr
