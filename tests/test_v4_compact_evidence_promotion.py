from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pytest


PREP = (
    Path(__file__).resolve().parents[1]
    / "benchmark-vabench-release-v4"
    / "operations"
    / "tri_form_derivation_prep"
)
if str(PREP) not in sys.path:
    sys.path.insert(0, str(PREP))

from promote_correct_plus_five_evidence import PromotionError, promote_report  # noqa: E402
from score_denominator_registry import write_family_row  # noqa: E402


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, value: object) -> None:
    write(path, json.dumps(value, indent=2, sort_keys=True) + "\n")


def source_fixture(tmp_path: Path) -> tuple[Path, Path, dict[str, str]]:
    source = tmp_path / "source"
    task = source / "001-sample"
    evaluator = task / "evaluator"
    run_dir = tmp_path / "machine" / "runtime" / "v4-501"

    write(evaluator / "reference_tb.scs", "reference deck\n")
    write(evaluator / "score_tb.scs", "score deck\n")
    write(task / "public" / "task" / "feedback_tb.scs", "feedback deck\n")
    write_json(evaluator / "checker_profile.json", {"checker_task_id": "v4_001_sample"})
    write(evaluator / "solution" / "dut.va", "module dut; // gold\nendmodule\n")
    mutation_ids = [f"neg_{index:03d}" for index in range(1, 6)]
    for mutation_id in mutation_ids:
        write(
            evaluator / "mutation_bundles" / mutation_id / "dut.va",
            f"module dut; // {mutation_id}\nendmodule\n",
        )

    row = {
        "canonical_dut_id": "001",
        "release_dir": "001-sample",
        "active_mutation_count": 5,
        "active_mutations": [{"mutation_id": item} for item in mutation_ids],
    }
    write_json(
        source / "score_denominator_registry" / "_meta.json",
        {"canonical_range": ["001", "001"], "counted_task_count": 1},
    )
    write_family_row(source, "001", row)

    write(run_dir / "public" / "submission" / "testbench.scs", "reference deck\n")
    write(run_dir / "evaluator" / "trusted_solution" / "dut.va", "module dut; // gold\nendmodule\n")
    for mutation_id in mutation_ids:
        write(
            run_dir / "evaluator" / "mutation_bundles" / mutation_id / "dut.va",
            f"module dut; // {mutation_id}\nendmodule\n",
        )

    paths = {
        "task": str(task),
        "run_dir": str(run_dir),
        "reference": str(evaluator / "reference_tb.scs"),
    }
    return source, run_dir, paths


def rust_report(tmp_path: Path, source: Path, run_dir: Path) -> Path:
    task = source / "001-sample"
    cases = [
        {
            "case_id": "reference",
            "role": "reference",
            "outcome": "reference_pass",
            "behavior": {"ok": True, "score": 1.0, "notes": ["gold behavior"]},
            "simulation": {"ok": True, "log_tail": "/secret/raw log", "stderr_tail": ""},
        }
    ]
    cases.extend(
        {
            "case_id": f"neg_{index:03d}",
            "role": "negative",
            "outcome": "killed_behaviorally",
            "behavior": {"ok": False, "score": 0.0, "notes": [f"kill {index}"]},
            "simulation": {"ok": True, "log_tail": "/secret/raw log"},
        }
        for index in range(1, 6)
    )
    report = {
        "schema_version": "v4-benchmarkv4-rust-evas-initial-judge-v1",
        "checker_module": "/machine/checkout/runners/simulate_evas.py",
        "checker_module_sha256": "a" * 64,
        "checker_aliases": "/machine/checkout/checker_aliases.json",
        "checker_aliases_sha256": "b" * 64,
        "claim_boundary": "EVAS formal judge; Spectre optional parity audit",
        "engine": {
            "name": "evas-rust",
            "git_commit": "deadbeef",
            "rust_library": "/machine/lib/libevas.dylib",
            "rust_library_sha256": "c" * 64,
            "spectre_strict": True,
        },
        "input_root": str(run_dir.parent),
        "task_count": 1,
        "status_counts": {"pass": 1},
        "results": [
            {
                "task_id": "v4-501",
                "family_id": "001",
                "form": "testbench",
                "run_dir": str(run_dir),
                "candidate_sha256": {
                    "testbench.scs": sha(task / "evaluator" / "reference_tb.scs")
                },
                "checker_task_id": "v4_001_sample",
                "reference_gate": "reference_pass",
                "kill_denominator": 5,
                "killed_count": 5,
                "status": "pass",
                "cases": cases,
            }
        ],
    }
    path = tmp_path / "raw-rust.json"
    write_json(path, report)
    return path


def spectre_report(tmp_path: Path, source: Path) -> Path:
    task = source / "001-sample"
    preview = tmp_path / "preview"
    reference = preview / "tasks" / "501-sample-testbench" / "evaluator" / "reference_tb.scs"
    write(reference, (task / "evaluator" / "reference_tb.scs").read_text())

    def candidate(case_id: str) -> Path:
        if case_id == "correct":
            destination = preview / "tasks" / "501-sample-testbench" / "public" / "supplied_dut" / "dut.va"
            source_path = task / "evaluator" / "solution" / "dut.va"
        else:
            destination = (
                preview
                / "tasks"
                / "501-sample-testbench"
                / "evaluator"
                / "mutation_bundles"
                / case_id
                / "dut.va"
            )
            source_path = task / "evaluator" / "mutation_bundles" / case_id / "dut.va"
        write(destination, source_path.read_text())
        return destination

    cases = []
    for case_id in ["correct", *(f"neg_{index:03d}" for index in range(1, 6))]:
        correct = case_id == "correct"
        cases.append(
            {
                "case_id": case_id,
                "case_kind": "correct" if correct else "negative",
                "expected": "behavior_pass" if correct else "behavior_fail",
                "observed": "behavior_pass" if correct else "behavior_fail",
                "outcome": "reference_pass" if correct else "killed_behaviorally",
                "behavior_score": 1.0 if correct else 0.0,
                "behavior_notes": ["spectre behavior"],
                "include_paths": [str(candidate(case_id))],
                "case_dir": f"/machine/work/{case_id}",
                "spectre": {
                    "ok": True,
                    "status": "success",
                    "csv_path": f"/machine/work/{case_id}/tran.csv",
                    "remote_run_dir": f"/remote/{case_id}",
                },
                "benign_warning_lines": ["WARNING (KNOWN-1): accepted environment warning"],
                "untriaged_warning_lines": [],
            }
        )
    report = {
        "schema_version": "v4-tri-form-reference-spectre-audit-v2",
        "release": str(preview),
        "spectre_backend": "sui-direct",
        "spectre_mode": "ax",
        "sui_host": "private-host",
        "sui_work_root": "/remote/work",
        "task_count": 1,
        "pass_count": 1,
        "reference_gate_pass_count": 1,
        "kill_denominator": 5,
        "killed_count": 5,
        "untriaged_warning_count": 0,
        "results": [
            {
                "task_id": "v4-501",
                "family_id": "001",
                "task_dir": "tasks/501-sample-testbench",
                "checker_task_id": "v4_001_sample",
                "reference_tb": str(reference),
                "reference_gate": True,
                "kill_denominator": 5,
                "killed_count": 5,
                "invalid_count": 0,
                "status": "PASS",
                "cases": cases,
                "warning_lines": ["WARNING (KNOWN-1): accepted environment warning"],
                "untriaged_warning_lines": [],
            }
        ],
    }
    path = tmp_path / "raw-spectre.json"
    write_json(path, report)
    return path


@pytest.mark.parametrize("kind", ["rust", "spectre"])
def test_promotion_is_compact_hash_bound_and_path_clean(tmp_path: Path, kind: str) -> None:
    source, run_dir, _ = source_fixture(tmp_path)
    raw = rust_report(tmp_path, source, run_dir) if kind == "rust" else spectre_report(tmp_path, source)
    runner = tmp_path / "runner.py"
    write(runner, "# exact runner\n")

    promoted = promote_report(
        source_root=source,
        report_path=raw,
        deck_kind="reference",
        runner_file=runner,
    )

    assert promoted["schema_version"] == "v4-compact-correct-plus-five-evidence-v1"
    assert promoted["source_report_sha256"] == sha(raw)
    assert promoted["tool_fingerprints"]["runner_sha256"] == sha(runner)
    task = promoted["tasks"][0]
    assert task["candidate_testbench"] == {
        "path": "001-sample/evaluator/reference_tb.scs",
        "sha256": sha(source / "001-sample" / "evaluator" / "reference_tb.scs"),
    }
    assert task["checker"]["profile_sha256"] == sha(
        source / "001-sample" / "evaluator" / "checker_profile.json"
    )
    assert [case["case_id"] for case in task["cases"]] == [
        "correct",
        "neg_001",
        "neg_002",
        "neg_003",
        "neg_004",
        "neg_005",
    ]
    assert all(case["candidate_files"] for case in task["cases"])
    assert task["status"] == "pass"
    if kind == "spectre":
        assert task["warnings"]["benign"] == [
            "WARNING (KNOWN-1): accepted environment warning"
        ]
        assert all(case["warnings"]["benign_count"] == 1 for case in task["cases"])
    serialized = json.dumps(promoted, sort_keys=True)
    for forbidden in (str(tmp_path), "log_tail", "remote_run_dir", "csv_path", "sui_host"):
        assert forbidden not in serialized


def test_promotion_rejects_report_that_is_not_bound_to_selected_deck(tmp_path: Path) -> None:
    source, run_dir, _ = source_fixture(tmp_path)
    raw = rust_report(tmp_path, source, run_dir)

    with pytest.raises(PromotionError, match="candidate testbench hash"):
        promote_report(source_root=source, report_path=raw, deck_kind="score")


def test_promotion_rejects_non_exact_five_or_failed_cases(tmp_path: Path) -> None:
    source, run_dir, _ = source_fixture(tmp_path)
    raw = rust_report(tmp_path, source, run_dir)
    report = json.loads(raw.read_text())
    report["results"][0]["cases"].pop()
    report["results"][0]["killed_count"] = 4
    write_json(raw, report)

    with pytest.raises(PromotionError, match="exact active negative set"):
        promote_report(source_root=source, report_path=raw, deck_kind="reference")


def test_task_filter_excludes_failed_rows_in_a_mixed_report(tmp_path: Path) -> None:
    source, run_dir, _ = source_fixture(tmp_path)
    raw = rust_report(tmp_path, source, run_dir)
    report = json.loads(raw.read_text())
    failed = json.loads(json.dumps(report["results"][0]))
    failed["task_id"] = "v4-999"
    failed["status"] = "fail"
    report["results"].append(failed)
    write_json(raw, report)

    promoted = promote_report(
        source_root=source,
        report_path=raw,
        deck_kind="reference",
        task_ids={"v4-501"},
    )

    assert [task["task_id"] for task in promoted["tasks"]] == ["v4-501"]
