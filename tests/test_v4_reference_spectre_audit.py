from __future__ import annotations

import importlib.util
import json
import shutil
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    ROOT
    / "benchmark-vabench-release-v4"
    / "operations"
    / "tri_form_derivation_prep"
    / "audit_tri_form_reference_spectre.py"
)


@pytest.fixture(scope="module")
def audit():
    runners = str(ROOT / "runners")
    if runners not in sys.path:
        sys.path.insert(0, runners)
    spec = importlib.util.spec_from_file_location("audit_tri_form_reference_spectre", SCRIPT)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_default_release_and_testbench_index_match_current_package(audit) -> None:
    assert audit.DEFAULT_RELEASE.name == "benchmarkv4-r51"
    rows = audit.resolve_task_rows(audit.DEFAULT_RELEASE, [])

    assert len(rows) == 400
    assert {key: rows[0][key] for key in ("family_id", "form", "task_dir", "task_id")} == {
        "family_id": "001",
        "form": "testbench",
        "task_dir": "tasks/501-bang-bang-phase-detector-testbench",
        "task_id": "v4-501",
    }
    assert rows[0]["public_contract"] == "tasks/501-bang-bang-phase-detector-testbench/public_contract.json"

def test_resolve_task_rows_rejects_unknown_or_non_testbench_task(audit) -> None:
    with pytest.raises(SystemExit, match="unknown testbench task id"):
        audit.resolve_task_rows(audit.DEFAULT_RELEASE, ["v4-001"])


def test_checker_and_include_resolution_use_current_canonical_assets(audit) -> None:
    row = audit.resolve_task_rows(audit.DEFAULT_RELEASE, ["v4-501"])[0]
    task_dir = audit.DEFAULT_RELEASE / row["task_dir"]
    task_record = audit.read_json(task_dir / "task_record.json")
    tb_path = task_dir / "evaluator" / "reference_tb.scs"

    checker_id = audit.checker_task_id(task_dir, task_record)
    assert checker_id in {
        "v3_001_bang_bang_phase_detector",
        "v4_001_bang_bang_phase_detector",
    }
    include_paths, missing = audit.include_paths_for_reference_tb(task_dir, tb_path)
    assert missing == []
    assert [path.name for path in include_paths] == ["bbpd_ref.va"]


def test_mutation_include_resolution_overlays_changed_files_on_supplied_bundle(
    audit,
    tmp_path: Path,
) -> None:
    task_dir = tmp_path / "task"
    supplied = task_dir / "public" / "supplied_dut"
    mutation = task_dir / "evaluator" / "mutation_bundles" / "neg_001"
    evaluator = task_dir / "evaluator"
    supplied.mkdir(parents=True)
    mutation.mkdir(parents=True)
    (supplied / "top.va").write_text("correct top\n", encoding="utf-8")
    (supplied / "companion.va").write_text("correct companion\n", encoding="utf-8")
    (mutation / "top.va").write_text("mutated top\n", encoding="utf-8")
    tb_path = evaluator / "reference_tb.scs"
    tb_path.write_text(
        'ahdl_include "./dut/top.va"\n'
        'ahdl_include "./dut/companion.va"\n',
        encoding="utf-8",
    )

    include_paths, missing = audit.include_paths_for_reference_tb(
        task_dir,
        tb_path,
        dut_root=mutation,
    )

    assert missing == []
    assert include_paths == [mutation / "top.va", supplied / "companion.va"]


def test_correct_include_resolution_accepts_staged_support_under_dut(
    audit,
    tmp_path: Path,
) -> None:
    task_dir = tmp_path / "task"
    supplied = task_dir / "public" / "supplied_dut"
    support = supplied / "support"
    evaluator = task_dir / "evaluator"
    support.mkdir(parents=True)
    evaluator.mkdir(parents=True)
    (supplied / "top.va").write_text("correct top\n", encoding="utf-8")
    (support / "helper.va").write_text("support helper\n", encoding="utf-8")
    tb_path = evaluator / "reference_tb.scs"
    tb_path.write_text(
        'ahdl_include "./dut/top.va"\n'
        'ahdl_include "./dut/support/helper.va"\n',
        encoding="utf-8",
    )

    include_paths, missing = audit.include_paths_for_reference_tb(task_dir, tb_path)

    assert missing == []
    assert include_paths == [supplied / "top.va", support / "helper.va"]


def test_mutation_include_resolution_never_falls_back_to_the_correct_dut(
    audit,
    tmp_path: Path,
) -> None:
    task_dir = tmp_path / "task"
    supplied_dut = task_dir / "public" / "supplied_dut"
    mutation_dir = task_dir / "evaluator" / "mutation_bundles" / "neg_001"
    evaluator = task_dir / "evaluator"
    supplied_dut.mkdir(parents=True)
    mutation_dir.mkdir(parents=True)
    (supplied_dut / "model.va").write_text("// correct\n", encoding="utf-8")
    (mutation_dir / "model.va").write_text("// mutant\n", encoding="utf-8")
    tb_path = evaluator / "reference_tb.scs"
    tb_path.write_text('ahdl_include "public/supplied_dut/model.va"\n', encoding="utf-8")

    include_paths, missing = audit.include_paths_for_reference_tb(
        task_dir,
        tb_path,
        dut_root=mutation_dir,
    )

    assert include_paths == [mutation_dir / "model.va"]
    assert missing == []

    (mutation_dir / "model.va").unlink()
    include_paths, missing = audit.include_paths_for_reference_tb(
        task_dir,
        tb_path,
        dut_root=mutation_dir,
    )
    assert include_paths == []
    assert missing == ["public/supplied_dut/model.va"]


def test_checker_resolution_accepts_an_audited_modular_v4_checker(audit) -> None:
    if not audit.has_behavior_check("v4_364_iq_upconversion_mixer_chain"):
        pytest.skip("requires the modular v4 checker registry")
    row = audit.resolve_task_rows(audit.DEFAULT_RELEASE, ["v4-864"])[0]
    task_dir = audit.DEFAULT_RELEASE / row["task_dir"]
    task_record = audit.read_json(task_dir / "task_record.json")

    assert audit.checker_task_id(task_dir, task_record) == "v4_364_iq_upconversion_mixer_chain"


def test_warning_extraction_classifies_known_infrastructure_noise(audit, tmp_path: Path) -> None:
    (tmp_path / "spectre.out").write_text(
        "WARNING (VACOMP-2435): benign compiler detail\n"
        "WARNING (CUSTOM-1): investigate this\n",
        encoding="utf-8",
    )

    warnings = audit.extract_warning_lines(
        tmp_path,
        {"warnings": ["remote_ahdlcmi_cache_prepare_failed rc=75"]},
    )

    assert len(warnings) == 3
    assert audit.is_benign_warning(warnings[0])
    assert audit.is_benign_warning(warnings[1])
    assert not audit.is_benign_warning(warnings[2])


def test_run_one_scores_reference_with_registered_checker(audit, tmp_path: Path, monkeypatch) -> None:
    row = audit.resolve_task_rows(audit.DEFAULT_RELEASE, ["v4-501"])[0]

    def fake_spectre_case(**kwargs):
        output_dir = kwargs["output_dir"]
        output_dir.mkdir(parents=True)
        (output_dir / "tran_spectre.csv").write_text("time,data\n0,0\n", encoding="utf-8")
        return {"ok": True, "status": "PASS", "warnings": [], "signals": ["data"], "rows": 1}

    monkeypatch.setattr(audit, "run_spectre_case", fake_spectre_case)
    monkeypatch.setattr(audit, "evaluate_behavior_with_timeout", lambda *args, **kwargs: (1.0, []))
    monkeypatch.setattr(audit, "validate_behavior_side_outputs", lambda *args, **kwargs: None)
    monkeypatch.setattr(audit, "behavior_side_output_names", lambda _checker_id: ())

    result = audit.run_one(
        release=audit.DEFAULT_RELEASE,
        row=row,
        output_root=tmp_path,
        spectre_backend="sui-direct",
        spectre_mode="ax",
        timeout_s=10,
        spectre_runtime_id="spectre-21.1.0-64bit-2022-09-24-csvcm36c-4",
        sui_host=None,
        sui_work_root=None,
        cadence_cshrc=None,
        keep_case_dirs=False,
    )

    assert result["status"] == "PASS"
    assert result["checker_task_id"] in {
        "v3_001_bang_bang_phase_detector",
        "v4_001_bang_bang_phase_detector",
    }
    assert result["behavior_score"] == 1.0
    assert not (tmp_path / "v4-501").exists()


def test_run_one_reports_unregistered_checker_without_starting_spectre(
    audit,
    tmp_path: Path,
    monkeypatch,
) -> None:
    row = audit.resolve_task_rows(audit.DEFAULT_RELEASE, ["v4-562"])[0]
    monkeypatch.setattr(
        audit,
        "run_spectre_case",
        lambda **_kwargs: pytest.fail("Spectre must not run without a registered checker"),
    )
    monkeypatch.setattr(audit, "has_behavior_check", lambda _checker_id: False)

    result = audit.run_one(
        release=audit.DEFAULT_RELEASE,
        row=row,
        output_root=tmp_path,
        spectre_backend="sui-direct",
        spectre_mode="ax",
        timeout_s=10,
        spectre_runtime_id="spectre-21.1.0-64bit-2022-09-24-csvcm36c-4",
        sui_host=None,
        sui_work_root=None,
        cadence_cshrc=None,
        keep_case_dirs=False,
    )

    assert result["status"] == "FAIL_CHECKER"
    assert "checker not registered" in result["notes"][0]


def test_correct_plus_five_uses_score_policy_sources_and_kills_all_negatives(
    audit,
    tmp_path: Path,
    monkeypatch,
) -> None:
    row = audit.resolve_task_rows(audit.DEFAULT_RELEASE, ["v4-501"])[0]
    task_dir = audit.DEFAULT_RELEASE / row["task_dir"]
    policy = audit.read_json(task_dir / "evaluator" / "score_policy.json")
    negative_ids = policy["negative_suite_mutation_ids"]
    calls = []

    def fake_spectre_case(**kwargs):
        calls.append(kwargs)
        output_dir = kwargs["output_dir"]
        output_dir.mkdir(parents=True)
        (output_dir / "tran_spectre.csv").write_text("time,data\n0,0\n", encoding="utf-8")
        return {"ok": True, "status": "PASS", "warnings": [], "signals": ["data"], "rows": 1}

    def fake_behavior(_checker_id, csv_path, **_kwargs):
        return (1.0, []) if csv_path.parent.name == "correct" else (0.0, ["mismatch_count=1"])

    monkeypatch.setattr(audit, "run_spectre_case", fake_spectre_case)
    monkeypatch.setattr(audit, "evaluate_behavior_with_timeout", fake_behavior)
    monkeypatch.setattr(audit, "validate_behavior_side_outputs", lambda *args, **kwargs: None)
    monkeypatch.setattr(audit, "behavior_side_output_names", lambda _checker_id: ())

    result = audit.run_correct_plus_mutations(
        release=audit.DEFAULT_RELEASE,
        row=row,
        output_root=tmp_path,
        spectre_backend="sui-direct",
        spectre_mode="ax",
        timeout_s=10,
        spectre_runtime_id="spectre-21.1.0-64bit-2022-09-24-csvcm36c-4",
        sui_host=None,
        sui_work_root=None,
        cadence_cshrc=None,
        keep_case_dirs=True,
    )

    assert len(calls) == 6
    assert {call["tb_path"] for call in calls} == {task_dir / "evaluator" / "reference_tb.scs"}
    assert {path.parent.name for path in calls[0]["include_paths"]} == {"supplied_dut"}
    assert [call["output_dir"].name for call in calls[1:]] == negative_ids
    assert [call["include_paths"][0].parent.name for call in calls[1:]] == negative_ids
    assert result["status"] == "PASS"
    assert result["reference_gate"] is True
    assert result["killed_count"] == 5
    assert result["kill_denominator"] == 5
    assert result["cases"][0]["expected"] == "behavior_pass"
    assert result["cases"][0]["observed"] == "behavior_pass"
    assert result["cases"][0]["outcome"] == "reference_pass"
    assert [case["mutation_id"] for case in result["cases"][1:]] == negative_ids
    assert {case["expected"] for case in result["cases"][1:]} == {"behavior_fail"}
    assert {case["observed"] for case in result["cases"][1:]} == {"behavior_fail"}
    assert {case["outcome"] for case in result["cases"][1:]} == {"killed_behaviorally"}
    assert {case["case_signature"]["schema_version"] for case in result["cases"]} == {
        "v4-reference-spectre-case-signature-v1"
    }
    assert all(case["case_signature_sha256"] for case in result["cases"])


def test_case_signature_is_stable_and_binds_audit_reuse_inputs(
    audit,
    tmp_path: Path,
    monkeypatch,
) -> None:
    row = audit.resolve_task_rows(audit.DEFAULT_RELEASE, ["v4-501"])[0]
    source_task_dir = audit.DEFAULT_RELEASE / row["task_dir"]
    release = tmp_path / "release"
    task_dir = release / row["task_dir"]
    shutil.copytree(source_task_dir, task_dir)

    task_record = audit.read_json(task_dir / "task_record.json")
    tb_path = task_dir / "evaluator" / "reference_tb.scs"
    score_policy = audit.read_json(task_dir / "evaluator" / "score_policy.json")
    checker_id = audit.checker_task_id(task_dir, task_record)
    include_paths, missing = audit.include_paths_for_reference_tb(task_dir, tb_path)

    kwargs = {
        "release": release,
        "row": row,
        "task_dir": task_dir,
        "task_record": task_record,
        "case_id": "correct",
        "case_kind": "correct",
        "mutation_id": "",
        "checker_id": checker_id,
        "tb_path": tb_path,
        "include_paths": include_paths,
        "missing_includes": missing,
        "score_policy": score_policy,
        "dut_root": task_dir / "public" / "supplied_dut",
        "spectre_backend": "sui-direct",
        "spectre_mode": "ax",
        "timeout_s": 10,
        "spectre_runtime_id": "spectre-21.1.0-64bit-2022-09-24-csvcm36c-4",
        "sui_host": "thu-sui",
        "sui_work_root": "/tmp/vaevas",
        "cadence_cshrc": "/opt/cadence.cshrc",
    }

    baseline_signature, baseline_sha = audit.build_case_signature(**kwargs)
    repeat_signature, repeat_sha = audit.build_case_signature(**kwargs)
    assert repeat_signature == baseline_signature
    assert repeat_sha == baseline_sha
    assert baseline_sha == audit.sha256_bytes(audit.canonical_json_bytes(baseline_signature))
    assert "sui_host" not in baseline_signature["spectre_run_config"]
    assert "sui_work_root" not in baseline_signature["spectre_run_config"]
    assert "cadence_cshrc" not in baseline_signature["spectre_run_config"]
    assert "bridge_repo" not in baseline_signature["spectre_run_config"]
    assert baseline_signature["spectre_run_config"]["spectre_runtime_id"] == (
        "spectre-21.1.0-64bit-2022-09-24-csvcm36c-4"
    )
    machine_only_kwargs = {
        **kwargs,
        "sui_host": "different-host",
        "sui_work_root": "/different/work/root",
        "cadence_cshrc": "/different/cadence.cshrc",
    }
    assert audit.build_case_signature(**machine_only_kwargs)[1] == baseline_sha

    changed = []

    (task_dir / "public" / "supplied_dut" / "bbpd_ref.va").write_text(
        "// changed dut\n",
        encoding="utf-8",
    )
    changed.append(audit.build_case_signature(**kwargs)[1])
    shutil.copy2(source_task_dir / "public" / "supplied_dut" / "bbpd_ref.va", task_dir / "public" / "supplied_dut" / "bbpd_ref.va")

    tb_path.write_text(tb_path.read_text(encoding="utf-8") + "\n// changed tb\n", encoding="utf-8")
    include_paths, missing = audit.include_paths_for_reference_tb(task_dir, tb_path)
    kwargs["include_paths"] = include_paths
    kwargs["missing_includes"] = missing
    changed.append(audit.build_case_signature(**kwargs)[1])
    shutil.copy2(source_task_dir / "evaluator" / "reference_tb.scs", tb_path)
    include_paths, missing = audit.include_paths_for_reference_tb(task_dir, tb_path)
    kwargs["include_paths"] = include_paths
    kwargs["missing_includes"] = missing

    profile_path = task_dir / "evaluator" / "checker_profile.json"
    profile = audit.read_json(profile_path)
    profile["signature_test_marker"] = "profile changed"
    profile_path.write_text(json.dumps(profile, sort_keys=True), encoding="utf-8")
    changed.append(audit.build_case_signature(**kwargs)[1])
    shutil.copy2(source_task_dir / "evaluator" / "checker_profile.json", profile_path)

    policy_path = task_dir / "evaluator" / "score_policy.json"
    policy = audit.read_json(policy_path)
    policy["signature_test_marker"] = "policy changed"
    policy_path.write_text(json.dumps(policy, sort_keys=True), encoding="utf-8")
    kwargs["score_policy"] = policy
    changed.append(audit.build_case_signature(**kwargs)[1])
    shutil.copy2(source_task_dir / "evaluator" / "score_policy.json", policy_path)
    kwargs["score_policy"] = audit.read_json(policy_path)

    mutation_id = score_policy["negative_suite_mutation_ids"][0]
    mutation_kwargs = {
        **kwargs,
        "case_id": mutation_id,
        "case_kind": "negative",
        "mutation_id": mutation_id,
        "dut_root": task_dir / "evaluator" / "mutation_bundles" / mutation_id,
    }
    mutation_include_paths, mutation_missing = audit.include_paths_for_reference_tb(
        task_dir,
        tb_path,
        dut_root=mutation_kwargs["dut_root"],
    )
    mutation_kwargs["include_paths"] = mutation_include_paths
    mutation_kwargs["missing_includes"] = mutation_missing
    mutation_baseline = audit.build_case_signature(**mutation_kwargs)[1]
    mutation_file = mutation_kwargs["dut_root"] / "bbpd_ref.va"
    mutation_file.write_text("// changed mutation\n", encoding="utf-8")
    changed.append(audit.build_case_signature(**mutation_kwargs)[1])
    assert changed[-1] != mutation_baseline

    config_kwargs = {**kwargs, "timeout_s": 11}
    changed.append(audit.build_case_signature(**config_kwargs)[1])

    runtime_kwargs = {**kwargs, "spectre_runtime_id": "spectre-runtime-changed"}
    changed.append(audit.build_case_signature(**runtime_kwargs)[1])

    support_path = task_dir / "evaluator" / "stimulus.csv"
    support_path.write_text("time,value\n0,0\n", encoding="utf-8")
    tb_path.write_text(
        tb_path.read_text(encoding="utf-8") + '\nparameters support_file="stimulus.csv"\n',
        encoding="utf-8",
    )
    support_sha = audit.build_case_signature(**kwargs)[1]
    changed.append(support_sha)
    support_path.write_text("time,value\n0,1\n", encoding="utf-8")
    changed.append(audit.build_case_signature(**kwargs)[1])
    assert changed[-1] != support_sha
    shutil.copy2(source_task_dir / "evaluator" / "reference_tb.scs", tb_path)
    support_path.unlink()

    monkeypatch.setattr(
        audit,
        "checker_implementation_bundle",
        lambda checker_id: {
            "checker_id": checker_id,
            "policy": {"implementation": "changed"},
            "source_sha256": "changed",
            "source_error": "",
            "files": [],
        },
    )
    changed.append(audit.build_case_signature(**kwargs)[1])

    monkeypatch.setattr(
        audit,
        "bridge_implementation_bundle",
        lambda: {
            "implementation_id": "changed-runner-rewrite",
            "functions": [{"function": "rewrite_ahdl_includes_for_staging", "source_sha256": "changed"}],
            "files": [],
        },
    )
    changed.append(audit.build_case_signature(**kwargs)[1])

    assert all(item != baseline_sha for item in changed)
    assert len(set(changed)) == len(changed)


def test_correct_plus_five_never_counts_compile_or_missing_trace_as_kills(
    audit,
    tmp_path: Path,
    monkeypatch,
) -> None:
    row = audit.resolve_task_rows(audit.DEFAULT_RELEASE, ["v4-501"])[0]
    task_dir = audit.DEFAULT_RELEASE / row["task_dir"]
    negative_ids = audit.read_json(
        task_dir / "evaluator" / "score_policy.json"
    )["negative_suite_mutation_ids"]
    compile_failure = negative_ids[0]
    missing_trace = negative_ids[1]

    def fake_spectre_case(**kwargs):
        case_name = kwargs["output_dir"].name
        kwargs["output_dir"].mkdir(parents=True)
        if case_name == compile_failure:
            return {
                "ok": False,
                "status": "FAIL_COMPILE",
                "errors": ["compile failed"],
                "warnings": [],
            }
        if case_name != missing_trace:
            (kwargs["output_dir"] / "tran_spectre.csv").write_text(
                "time,data\n0,0\n",
                encoding="utf-8",
            )
        return {"ok": True, "status": "PASS", "warnings": [], "signals": ["data"], "rows": 1}

    def fake_behavior(_checker_id, csv_path, **_kwargs):
        return (1.0, []) if csv_path.parent.name == "correct" else (0.0, ["mutant detected"])

    monkeypatch.setattr(audit, "run_spectre_case", fake_spectre_case)
    monkeypatch.setattr(audit, "evaluate_behavior_with_timeout", fake_behavior)
    monkeypatch.setattr(audit, "validate_behavior_side_outputs", lambda *args, **kwargs: None)
    monkeypatch.setattr(audit, "behavior_side_output_names", lambda _checker_id: ())

    result = audit.run_correct_plus_mutations(
        release=audit.DEFAULT_RELEASE,
        row=row,
        output_root=tmp_path,
        spectre_backend="sui-direct",
        spectre_mode="ax",
        timeout_s=10,
        spectre_runtime_id="spectre-21.1.0-64bit-2022-09-24-csvcm36c-4",
        sui_host=None,
        sui_work_root=None,
        cadence_cshrc=None,
        keep_case_dirs=True,
    )

    cases = {case["case_id"]: case for case in result["cases"]}
    assert result["reference_gate"] is True
    assert result["killed_count"] == 3
    assert result["invalid_count"] == 2
    assert result["status"] == "FAIL_MUTATIONS"
    assert cases[compile_failure]["observed"] == "spectre_failed"
    assert cases[compile_failure]["outcome"] == "invalid_run"
    assert cases[missing_trace]["observed"] == "trace_missing"
    assert cases[missing_trace]["outcome"] == "invalid_run"


def test_correct_plus_five_treats_missing_checker_columns_as_invalid_runs(
    audit,
    tmp_path: Path,
    monkeypatch,
) -> None:
    row = audit.resolve_task_rows(audit.DEFAULT_RELEASE, ["v4-501"])[0]
    spectre_calls = 0

    def fake_spectre_case(**kwargs):
        nonlocal spectre_calls
        spectre_calls += 1
        kwargs["output_dir"].mkdir(parents=True)
        (kwargs["output_dir"] / "tran_spectre.csv").write_text(
            "time,data\n0,0\n",
            encoding="utf-8",
        )
        return {"ok": True, "status": "PASS", "warnings": [], "signals": ["data"], "rows": 1}

    monkeypatch.setattr(audit, "run_spectre_case", fake_spectre_case)
    monkeypatch.setattr(
        audit,
        "evaluate_behavior_with_timeout",
        lambda *args, **kwargs: (0.0, ["missing_columns=clk,out"]),
    )
    monkeypatch.setattr(audit, "validate_behavior_side_outputs", lambda *args, **kwargs: None)
    monkeypatch.setattr(audit, "behavior_side_output_names", lambda _checker_id: ())

    result = audit.run_correct_plus_mutations(
        release=audit.DEFAULT_RELEASE,
        row=row,
        output_root=tmp_path,
        spectre_backend="sui-direct",
        spectre_mode="ax",
        timeout_s=10,
        spectre_runtime_id="spectre-21.1.0-64bit-2022-09-24-csvcm36c-4",
        sui_host=None,
        sui_work_root=None,
        cadence_cshrc=None,
        keep_case_dirs=True,
    )

    assert result["status"] == "FAIL_REFERENCE"
    assert result["reference_gate"] is False
    assert result["killed_count"] == 0
    assert result["invalid_count"] == 0
    assert result["skipped_count"] == 5
    assert spectre_calls == 1
    assert len(result["cases"]) == 1
    assert {case["observed"] for case in result["cases"]} == {"checker_invalid"}
    assert {case["outcome"] for case in result["cases"]} == {"invalid_run"}


@pytest.mark.parametrize(
    "invalid_note",
    [
        "empty_trace",
        "insufficient_select_coverage low=0 high=1",
    ],
)
def test_correct_plus_five_rejects_other_checker_contract_failures(
    audit,
    tmp_path: Path,
    monkeypatch,
    invalid_note: str,
) -> None:
    row = audit.resolve_task_rows(audit.DEFAULT_RELEASE, ["v4-501"])[0]
    spectre_calls = 0

    def fake_spectre_case(**kwargs):
        nonlocal spectre_calls
        spectre_calls += 1
        kwargs["output_dir"].mkdir(parents=True)
        (kwargs["output_dir"] / "tran_spectre.csv").write_text(
            "time,data\n0,0\n",
            encoding="utf-8",
        )
        return {"ok": True, "status": "PASS", "warnings": [], "signals": ["data"], "rows": 1}

    monkeypatch.setattr(audit, "run_spectre_case", fake_spectre_case)
    monkeypatch.setattr(
        audit,
        "evaluate_behavior_with_timeout",
        lambda *args, **kwargs: (0.0, [invalid_note]),
    )
    monkeypatch.setattr(audit, "validate_behavior_side_outputs", lambda *args, **kwargs: None)
    monkeypatch.setattr(audit, "behavior_side_output_names", lambda _checker_id: ())

    result = audit.run_correct_plus_mutations(
        release=audit.DEFAULT_RELEASE,
        row=row,
        output_root=tmp_path,
        spectre_backend="sui-direct",
        spectre_mode="ax",
        timeout_s=10,
        spectre_runtime_id="spectre-21.1.0-64bit-2022-09-24-csvcm36c-4",
        sui_host=None,
        sui_work_root=None,
        cadence_cshrc=None,
        keep_case_dirs=True,
    )

    assert result["killed_count"] == 0
    assert result["invalid_count"] == 0
    assert result["skipped_count"] == 5
    assert spectre_calls == 1
    assert len(result["cases"]) == 1
    assert {case["observed"] for case in result["cases"]} == {"checker_invalid"}
    assert {case["outcome"] for case in result["cases"]} == {"invalid_run"}


def test_correct_plus_five_rejects_non_five_score_policy_without_running_spectre(
    audit,
    tmp_path: Path,
    monkeypatch,
) -> None:
    row = audit.resolve_task_rows(audit.DEFAULT_RELEASE, ["v4-501"])[0]
    original_read_json = audit.read_json

    def fake_read_json(path: Path):
        value = original_read_json(path)
        if path.name == "score_policy.json":
            value["negative_suite_mutation_ids"] = value["negative_suite_mutation_ids"][:4]
        return value

    monkeypatch.setattr(audit, "read_json", fake_read_json)
    monkeypatch.setattr(
        audit,
        "run_spectre_case",
        lambda **_kwargs: pytest.fail("Spectre must not run for an invalid score policy"),
    )

    result = audit.run_correct_plus_mutations(
        release=audit.DEFAULT_RELEASE,
        row=row,
        output_root=tmp_path,
        spectre_backend="sui-direct",
        spectre_mode="ax",
        timeout_s=10,
        spectre_runtime_id="spectre-21.1.0-64bit-2022-09-24-csvcm36c-4",
        sui_host=None,
        sui_work_root=None,
        cadence_cshrc=None,
        keep_case_dirs=False,
    )

    assert result["status"] == "FAIL_MUTATION_SETUP"
    assert result["reference_gate"] is False
    assert result["killed_count"] == 0
    assert result["kill_denominator"] == 5
    assert "exactly five" in result["notes"][0]


def test_main_include_mutations_selects_correct_plus_five_schema(
    audit,
    tmp_path: Path,
    monkeypatch,
) -> None:
    output = tmp_path / "summary.json"
    work_root = tmp_path / "work"
    monkeypatch.setattr(
        audit,
        "resolve_task_rows",
        lambda _release, _task_ids: [{"task_id": "v4-501"}],
    )
    monkeypatch.setattr(audit, "normalize_spectre_backend", lambda value: value)
    monkeypatch.setattr(audit, "normalize_spectre_mode", lambda value: value)
    monkeypatch.setattr(
        audit,
        "run_one",
        lambda **_kwargs: pytest.fail("single-reference runner must not be selected"),
    )
    monkeypatch.setattr(
        audit,
        "run_correct_plus_mutations",
        lambda **_kwargs: {
            "task_id": "v4-501",
            "status": "PASS",
            "wall_time_s": 1.0,
            "reference_gate": True,
            "killed_count": 5,
            "untriaged_warning_lines": [],
        },
    )

    return_code = audit.main(
        [
            "--task-id",
            "v4-501",
            "--output",
            str(output),
            "--work-root",
            str(work_root),
            "--include-mutations",
            "--spectre-runtime-id",
            "spectre-21.1.0-64bit-2022-09-24-csvcm36c-4",
        ]
    )

    summary = audit.read_json(output)
    assert return_code == 0
    assert summary["schema_version"] == "v4-benchmarkv4-reference-spectre-correct-plus-five-audit-v1"
    assert summary["include_mutations"] is True
    assert summary["spectre_runtime_id"] == "spectre-21.1.0-64bit-2022-09-24-csvcm36c-4"
    assert summary["reference_gate_pass_count"] == 1
    assert summary["killed_count"] == 5
    assert summary["kill_denominator"] == 5


def test_main_default_preserves_v1_schema_and_single_reference_runner(
    audit,
    tmp_path: Path,
    monkeypatch,
) -> None:
    output = tmp_path / "summary.json"
    work_root = tmp_path / "work"
    monkeypatch.setattr(
        audit,
        "resolve_task_rows",
        lambda _release, _task_ids: [{"task_id": "v4-501"}],
    )
    monkeypatch.setattr(audit, "normalize_spectre_backend", lambda value: value)
    monkeypatch.setattr(audit, "normalize_spectre_mode", lambda value: value)
    monkeypatch.setattr(
        audit,
        "run_correct_plus_mutations",
        lambda **_kwargs: pytest.fail("correct-plus-five runner must be opt-in"),
    )
    monkeypatch.setattr(
        audit,
        "run_one",
        lambda **_kwargs: {
            "task_id": "v4-501",
            "status": "PASS",
            "wall_time_s": 1.0,
            "behavior_score": 1.0,
            "untriaged_warning_lines": [],
        },
    )

    return_code = audit.main(
        [
            "--task-id",
            "v4-501",
            "--output",
            str(output),
            "--work-root",
            str(work_root),
        ]
    )

    summary = audit.read_json(output)
    assert return_code == 0
    assert summary["schema_version"] == "v4-benchmarkv4-reference-spectre-audit-v1"
    assert "include_mutations" not in summary
