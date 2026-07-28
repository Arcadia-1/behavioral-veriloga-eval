from __future__ import annotations

import hashlib
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
    / "calibration_pilot"
    / "score_spectre_campaign.py"
)


def load_audit():
    spec = importlib.util.spec_from_file_location("score_spectre_campaign_test", SCRIPT)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def canonical_sha256(value: object) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def test_build_audit_plan_verifies_frozen_score_and_submission_without_mutating_campaign(
    tmp_path: Path,
) -> None:
    audit = load_audit()
    experiment = tmp_path / "experiment"
    campaign_run = experiment / "output" / "master" / "run"
    runtime = campaign_run / "v4-501-G0-r00-oneshot"
    submission = runtime / "evidence" / "final_submission"
    submission.mkdir(parents=True)
    artifact = submission / "testbench.scs"
    artifact.write_text("simulator lang=spectre\n", encoding="utf-8")
    artifact_sha = hashlib.sha256(artifact.read_bytes()).hexdigest()
    submission_tree = canonical_sha256(
        [{"path": "testbench.scs", "sha256": artifact_sha}]
    )
    campaign_result = runtime / "evidence" / "campaign_result.json"
    write_json(
        campaign_result,
        {
            "cell": {
                "cell_id": runtime.name,
                "family_id": "001",
                "form": "testbench",
                "mode": "G0",
                "experimental_arm": "OneShot",
            },
            "experiment_result": {
                "final_submission": {
                    "status": "available",
                    "tree_sha256": submission_tree,
                    "artifacts": [
                        {
                            "path": "testbench.scs",
                            "sha256": artifact_sha,
                            "bytes": artifact.stat().st_size,
                        }
                    ],
                }
            },
        },
    )
    original_campaign_bytes = campaign_result.read_bytes()

    score = {
        "schema_version": "v4-calibration-score-report-v2",
        "cell_count": 2,
        "rows": [
            {
                "cell_id": runtime.name,
                "family_id": "001",
                "form": "testbench",
                "mode": "G0",
                "experimental_arm": "OneShot",
                "outcome": "runtime_failure",
                "trusted_replay": {"submission_tree_sha256": submission_tree},
            },
            {
                "cell_id": "v4-501-G2-r00-agentic",
                "family_id": "001",
                "form": "testbench",
                "mode": "G2",
                "experimental_arm": "Agentic",
                "outcome": "passed",
            },
        ],
    }
    score_path = experiment / "SCORE_FINAL_TRUSTED_REPLAY.json"
    write_json(score_path, score)
    freeze_path = experiment / "SPECTRE_AUDIT_FREEZE.json"
    write_json(
        freeze_path,
        {
            "schema_version": "vabench-spectre-audit-freeze-v1",
            "experiment_root": str(experiment),
            "master_output": "output/master",
            "score_report": {
                "path": score_path.name,
                "sha256": hashlib.sha256(score_path.read_bytes()).hexdigest(),
                "rows": 2,
            },
            "audit_policy": {"do_not_overwrite_frozen_score": True},
        },
    )

    plan = audit.build_audit_plan(
        score_path=score_path,
        campaign_run=campaign_run,
        freeze_manifest=freeze_path,
        source_outcomes={"runtime_failure"},
        cell_ids=set(),
    )

    assert [item["cell_id"] for item in plan] == [runtime.name]
    assert plan[0]["submission_tree_sha256"] == submission_tree
    assert plan[0]["runtime"] == runtime
    assert campaign_result.read_bytes() == original_campaign_bytes


def test_testbench_audit_runs_reference_and_all_five_frozen_mutations(
    tmp_path: Path,
) -> None:
    audit = load_audit()
    release_task = (
        ROOT
        / "benchmark-vabench-release-v4"
        / "release"
        / "benchmarkv4-r52"
        / "tasks"
        / "501-bang-bang-phase-detector-testbench"
    )
    runtime = tmp_path / "v4-501-G0-r00-oneshot"
    shutil.copytree(release_task / "evaluator", runtime / "evaluator")
    shutil.copy2(release_task / "task_record.json", runtime / "evaluator" / "task_record.json")
    submission = runtime / "evidence" / "final_submission"
    submission.mkdir(parents=True)
    candidate_text = (
        (release_task / "evaluator" / "reference_tb.scs").read_text(encoding="utf-8")
        + "\n// frozen candidate marker\n"
    )
    (submission / "testbench.scs").write_text(candidate_text, encoding="utf-8")

    policy = json.loads(
        (runtime / "evaluator" / "score_policy.json").read_text(encoding="utf-8")
    )
    mutation_ids = policy["negative_suite_mutation_ids"]
    frozen_mutation = (
        runtime
        / "evaluator"
        / "mutation_bundles"
        / mutation_ids[0]
        / "bbpd_ref.va"
    )
    frozen_mutation.write_text(
        frozen_mutation.read_text(encoding="utf-8") + "\n// frozen mutation marker\n",
        encoding="utf-8",
    )

    calls: list[dict[str, object]] = []

    def fake_simulate_case(**kwargs):
        calls.append(kwargs)
        tb_path = kwargs["tb_path"]
        assert "frozen candidate marker" in tb_path.read_text(encoding="utf-8")
        include_text = "\n".join(
            path.read_text(encoding="utf-8") for path in kwargs["include_paths"]
        )
        if kwargs["case_id"] == mutation_ids[0]:
            assert "frozen mutation marker" in include_text
        output_dir = kwargs["output_dir"]
        output_dir.mkdir(parents=True)
        required = sorted(kwargs["required_signals"])
        header = ["time", *required]
        values = ["0", *(["0"] * len(required))]
        (output_dir / "tran_spectre.csv").write_text(
            ",".join(header) + "\n" + ",".join(values) + "\n",
            encoding="utf-8",
        )
        return {
            "ok": True,
            "status": "success",
            "errors": [],
            "warnings": [],
            "signals": header,
            "rows": 1,
            "spectre_backend": "sui-direct",
            "spectre_mode": "ax",
        }

    def fake_evaluate(_checker_id, csv_path, **_kwargs):
        if csv_path.parent.name == "reference":
            return 1.0, ["reference accepted"]
        return 0.0, ["mutation detected"]

    result = audit.audit_cell(
        runtime=runtime,
        score_row={
            "cell_id": runtime.name,
            "family_id": "001",
            "form": "testbench",
            "mode": "G0",
            "experimental_arm": "OneShot",
            "outcome": "runtime_failure",
        },
        submission_tree_sha256="frozen-tree",
        cell_output=tmp_path / "audit-cell",
        config=audit.SpectreConfig(timeout_s=10),
        simulate_case=fake_simulate_case,
        behavior_evaluator=fake_evaluate,
    )

    assert len(calls) == 6
    assert [call["case_id"] for call in calls] == ["reference", *mutation_ids]
    assert result["outcome"] == "passed"
    assert result["reference_gate"] is True
    assert result["killed_count"] == 5
    assert result["survived_count"] == 0
    assert result["invalid_count"] == 0

    resumed = audit.audit_cell(
        runtime=runtime,
        score_row={
            "cell_id": runtime.name,
            "family_id": "001",
            "form": "testbench",
            "mode": "G0",
            "experimental_arm": "OneShot",
            "outcome": "runtime_failure",
        },
        submission_tree_sha256="frozen-tree",
        cell_output=tmp_path / "audit-cell",
        config=audit.SpectreConfig(timeout_s=10),
        simulate_case=fake_simulate_case,
        behavior_evaluator=fake_evaluate,
    )
    assert len(calls) == 6
    assert resumed["outcome"] == "passed"
    assert all(case["resumed_case"] for case in resumed["cases"])


def test_dut_audit_runs_frozen_candidate_once_and_uses_canonical_checker(
    tmp_path: Path,
) -> None:
    audit = load_audit()
    release_task = (
        ROOT
        / "benchmark-vabench-release-v4"
        / "release"
        / "benchmarkv4-r52"
        / "tasks"
        / "001-bang-bang-phase-detector"
    )
    runtime = tmp_path / "v4-001-G0-r00-oneshot"
    shutil.copytree(release_task / "evaluator", runtime / "evaluator")
    shutil.copy2(release_task / "task_record.json", runtime / "evaluator" / "task_record.json")
    public_support = release_task / "public" / "task" / "public_support"
    if public_support.is_dir():
        shutil.copytree(public_support, runtime / "public" / "task" / "public_support")

    contract = json.loads(
        (release_task / "public_contract.json").read_text(encoding="utf-8")
    )
    submission = runtime / "evidence" / "final_submission"
    submission.mkdir(parents=True)
    for relative in contract["target_artifacts"]:
        source = release_task / "evaluator" / "solution" / relative
        if not source.is_file():
            source = release_task / "evaluator" / "trusted_solution" / relative
        target = submission / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            source.read_text(encoding="utf-8") + "\n// frozen DUT candidate marker\n",
            encoding="utf-8",
        )

    calls: list[dict[str, object]] = []

    def fake_simulate_case(**kwargs):
        calls.append(kwargs)
        include_text = "\n".join(
            path.read_text(encoding="utf-8") for path in kwargs["include_paths"]
        )
        assert "frozen DUT candidate marker" in include_text
        output_dir = kwargs["output_dir"]
        output_dir.mkdir(parents=True)
        required = sorted(kwargs["required_signals"])
        (output_dir / "tran_spectre.csv").write_text(
            ",".join(["time", *required])
            + "\n"
            + ",".join(["0", *(["0"] * len(required))])
            + "\n",
            encoding="utf-8",
        )
        return {
            "ok": True,
            "status": "success",
            "errors": [],
            "warnings": [],
            "signals": ["time", *required],
            "rows": 1,
            "spectre_backend": "sui-direct",
            "spectre_mode": "ax",
        }

    result = audit.audit_cell(
        runtime=runtime,
        score_row={
            "cell_id": runtime.name,
            "family_id": "001",
            "form": "dut",
            "mode": "G0",
            "experimental_arm": "OneShot",
            "outcome": "runtime_failure",
        },
        submission_tree_sha256="frozen-tree",
        cell_output=tmp_path / "audit-dut",
        config=audit.SpectreConfig(timeout_s=10),
        simulate_case=fake_simulate_case,
        behavior_evaluator=lambda *_args, **_kwargs: (1.0, ["DUT accepted"]),
    )

    assert len(calls) == 1
    assert calls[0]["case_id"] == "score"
    assert result["outcome"] == "passed"
    assert result["checker_task_id"] in {
        "v3_001_bang_bang_phase_detector",
        "v4_001_bang_bang_phase_detector",
    }


def test_dut_audit_uses_declared_trace_contract_not_checker_diagnostic_labels(
    tmp_path: Path,
) -> None:
    audit = load_audit()
    release_task = (
        ROOT
        / "benchmark-vabench-release-v4"
        / "release"
        / "benchmarkv4-r52"
        / "tasks"
        / "189-trim-ctrl-4bit"
    )
    runtime = tmp_path / "v4-189-G0-r00-oneshot"
    shutil.copytree(release_task / "evaluator", runtime / "evaluator")
    shutil.copy2(
        release_task / "task_record.json",
        runtime / "evaluator" / "task_record.json",
    )
    submission = runtime / "evidence" / "final_submission"
    submission.mkdir(parents=True)
    shutil.copy2(
        release_task / "evaluator" / "solution" / "trim_ctrl_4bit.va",
        submission / "trim_ctrl_4bit.va",
    )

    observed_required_signals: list[set[str]] = []

    def fake_simulate_case(**kwargs):
        observed_required_signals.append(set(kwargs["required_signals"]))
        output_dir = kwargs["output_dir"]
        output_dir.mkdir(parents=True)
        (output_dir / "tran_spectre.csv").write_text(
            "time,ain,dout0,dout1,dout2,dout3\n"
            "0,0,0,0,0,0\n",
            encoding="utf-8",
        )
        return {
            "ok": True,
            "status": "success",
            "errors": [],
            "warnings": [],
            "signals": ["time", "ain", "dout0", "dout1", "dout2", "dout3"],
            "rows": 1,
            "spectre_backend": "sui-direct",
            "spectre_mode": "ax",
        }

    result = audit.audit_cell(
        runtime=runtime,
        score_row={
            "cell_id": runtime.name,
            "family_id": "189",
            "form": "dut",
            "mode": "G0",
            "experimental_arm": "OneShot",
            "outcome": "runtime_failure",
        },
        submission_tree_sha256="frozen-tree",
        cell_output=tmp_path / "audit-dut-189",
        config=audit.SpectreConfig(timeout_s=600),
        simulate_case=fake_simulate_case,
        behavior_evaluator=lambda *_args, **_kwargs: (1.0, ["accepted"]),
    )

    assert observed_required_signals == [
        {"ain", "dout0", "dout1", "dout2", "dout3"}
    ]
    assert result["outcome"] == "passed"


def test_dut_audit_classifies_checker_timeout_as_retryable_infrastructure(
    tmp_path: Path,
) -> None:
    audit = load_audit()
    release_task = (
        ROOT
        / "benchmark-vabench-release-v4"
        / "release"
        / "benchmarkv4-r52"
        / "tasks"
        / "189-trim-ctrl-4bit"
    )
    runtime = tmp_path / "v4-189-G2-r00-agentic"
    shutil.copytree(release_task / "evaluator", runtime / "evaluator")
    shutil.copy2(
        release_task / "task_record.json",
        runtime / "evaluator" / "task_record.json",
    )
    submission = runtime / "evidence" / "final_submission"
    submission.mkdir(parents=True)
    shutil.copy2(
        release_task / "evaluator" / "solution" / "trim_ctrl_4bit.va",
        submission / "trim_ctrl_4bit.va",
    )

    def fake_simulate_case(**kwargs):
        output_dir = kwargs["output_dir"]
        output_dir.mkdir(parents=True)
        (output_dir / "tran_spectre.csv").write_text(
            "time,ain,dout0,dout1,dout2,dout3\n"
            "0,0,0,0,0,0\n",
            encoding="utf-8",
        )
        return {
            "ok": True,
            "status": "success",
            "errors": [],
            "warnings": [],
            "signals": ["time", "ain", "dout0", "dout1", "dout2", "dout3"],
            "rows": 1,
            "spectre_backend": "sui-direct",
            "spectre_mode": "ax",
        }

    result = audit.audit_cell(
        runtime=runtime,
        score_row={
            "cell_id": runtime.name,
            "family_id": "189",
            "form": "dut",
            "mode": "G2",
            "experimental_arm": "Agentic",
            "outcome": "runtime_failure",
        },
        submission_tree_sha256="frozen-tree",
        cell_output=tmp_path / "audit-timeout",
        config=audit.SpectreConfig(timeout_s=600),
        simulate_case=fake_simulate_case,
        behavior_evaluator=lambda *_args, **_kwargs: (
            0.0,
            ["behavior_eval_timeout>300s"],
        ),
    )

    assert result["outcome"] == "infrastructure_failure"
    assert result["failure_taxonomy"]["primary_class"] == "infrastructure"
    assert result["failure_taxonomy"]["stage"] == "checker_timeout"
    assert result["failure_taxonomy"]["retryable"] is True
    assert result["cases"][0]["failure_kind"] == "checker_timeout"
    assert result["cases"][0]["responsibility"] == "system"


def test_dut_audit_classifies_missing_declared_trace_signal_as_infrastructure(
    tmp_path: Path,
) -> None:
    audit = load_audit()
    release_task = (
        ROOT
        / "benchmark-vabench-release-v4"
        / "release"
        / "benchmarkv4-r52"
        / "tasks"
        / "189-trim-ctrl-4bit"
    )
    runtime = tmp_path / "v4-189-G2-r00-noevas"
    shutil.copytree(release_task / "evaluator", runtime / "evaluator")
    shutil.copy2(
        release_task / "task_record.json",
        runtime / "evaluator" / "task_record.json",
    )
    submission = runtime / "evidence" / "final_submission"
    submission.mkdir(parents=True)
    shutil.copy2(
        release_task / "evaluator" / "solution" / "trim_ctrl_4bit.va",
        submission / "trim_ctrl_4bit.va",
    )

    def fake_simulate_case(**kwargs):
        output_dir = kwargs["output_dir"]
        output_dir.mkdir(parents=True)
        (output_dir / "tran_spectre.csv").write_text(
            "time,ain,dout0,dout1,dout2\n"
            "0,0,0,0,0\n",
            encoding="utf-8",
        )
        return {
            "ok": True,
            "status": "success",
            "errors": [],
            "warnings": [],
            "signals": ["time", "ain", "dout0", "dout1", "dout2"],
            "rows": 1,
            "spectre_backend": "sui-direct",
            "spectre_mode": "ax",
        }

    result = audit.audit_cell(
        runtime=runtime,
        score_row={
            "cell_id": runtime.name,
            "family_id": "189",
            "form": "dut",
            "mode": "G2",
            "experimental_arm": "Agent-No-EVAS",
            "outcome": "runtime_failure",
        },
        submission_tree_sha256="frozen-tree",
        cell_output=tmp_path / "audit-missing-signal",
        config=audit.SpectreConfig(timeout_s=600),
        simulate_case=fake_simulate_case,
    )

    assert result["outcome"] == "infrastructure_failure"
    assert result["failure_taxonomy"]["primary_class"] == "infrastructure"
    assert result["failure_taxonomy"]["stage"] == "trace_contract"
    assert result["failure_taxonomy"]["retryable"] is True
    assert result["cases"][0]["failure_kind"] == "required_signal"
    assert result["cases"][0]["responsibility"] == "system"


def test_testbench_audit_preserves_checker_timeout_stage_in_aggregate(
    tmp_path: Path,
) -> None:
    audit = load_audit()
    release_task = (
        ROOT
        / "benchmark-vabench-release-v4"
        / "release"
        / "benchmarkv4-r52"
        / "tasks"
        / "501-bang-bang-phase-detector-testbench"
    )
    runtime = tmp_path / "v4-501-G2-r00-agentic"
    shutil.copytree(release_task / "evaluator", runtime / "evaluator")
    shutil.copy2(
        release_task / "task_record.json",
        runtime / "evaluator" / "task_record.json",
    )
    submission = runtime / "evidence" / "final_submission"
    submission.mkdir(parents=True)
    shutil.copy2(
        release_task / "evaluator" / "reference_tb.scs",
        submission / "testbench.scs",
    )

    def fake_simulate_case(**kwargs):
        output_dir = kwargs["output_dir"]
        output_dir.mkdir(parents=True)
        required = sorted(kwargs["required_signals"])
        (output_dir / "tran_spectre.csv").write_text(
            ",".join(["time", *required])
            + "\n"
            + ",".join(["0", *(["0"] * len(required))])
            + "\n",
            encoding="utf-8",
        )
        return {
            "ok": True,
            "status": "success",
            "errors": [],
            "warnings": [],
            "signals": ["time", *required],
            "rows": 1,
            "spectre_backend": "sui-direct",
            "spectre_mode": "ax",
        }

    result = audit.audit_cell(
        runtime=runtime,
        score_row={
            "cell_id": runtime.name,
            "family_id": "001",
            "form": "testbench",
            "mode": "G2",
            "experimental_arm": "Agentic",
            "outcome": "runtime_failure",
        },
        submission_tree_sha256="frozen-tree",
        cell_output=tmp_path / "audit-testbench-timeout",
        config=audit.SpectreConfig(timeout_s=600),
        simulate_case=fake_simulate_case,
        behavior_evaluator=lambda *_args, **_kwargs: (
            0.0,
            ["behavior_eval_timeout>300s"],
        ),
    )

    assert result["outcome"] == "infrastructure_failure"
    assert result["failure_taxonomy"]["stage"] == "checker_timeout"
    assert {
        case["failure_kind"] for case in result["cases"]
    } == {"checker_timeout"}


def test_testbench_audit_rejects_spectre_no_ground_run_before_checker(
    tmp_path: Path,
) -> None:
    audit = load_audit()
    release_task = (
        ROOT
        / "benchmark-vabench-release-v4"
        / "release"
        / "benchmarkv4-r52"
        / "tasks"
        / "501-bang-bang-phase-detector-testbench"
    )
    runtime = tmp_path / "v4-501-G2-r00-agentic"
    shutil.copytree(release_task / "evaluator", runtime / "evaluator")
    shutil.copy2(
        release_task / "task_record.json",
        runtime / "evaluator" / "task_record.json",
    )
    submission = runtime / "evidence" / "final_submission"
    submission.mkdir(parents=True)
    candidate_text = (
        release_task / "evaluator" / "reference_tb.scs"
    ).read_text(encoding="utf-8")
    (submission / "testbench.scs").write_text(
        candidate_text.replace(" 0)", " vss)"),
        encoding="utf-8",
    )

    checker_calls = 0

    def fake_simulate_case(**kwargs):
        output_dir = kwargs["output_dir"]
        output_dir.mkdir(parents=True)
        required = sorted(kwargs["required_signals"])
        (output_dir / "tran_spectre.csv").write_text(
            ",".join(["time", *required])
            + "\n"
            + ",".join(["0", *(["0"] * len(required))])
            + "\n",
            encoding="utf-8",
        )
        warning = (
            "WARNING (SPECTRE-470): No ground node was found in the netlist. "
            "To continue with this simulation, Spectre will add a gmin."
        )
        (output_dir / "spectre.out").write_text(warning + "\n", encoding="utf-8")
        return {
            "ok": True,
            "status": "success",
            "errors": [],
            "warnings": [],
            "signals": ["time", *required],
            "rows": 1,
            "spectre_backend": "sui-direct",
            "spectre_mode": "ax",
            "stdout_tail": warning,
        }

    def fake_evaluate(*_args, **_kwargs):
        nonlocal checker_calls
        checker_calls += 1
        return 1.0, ["must not be evaluated"]

    result = audit.audit_cell(
        runtime=runtime,
        score_row={
            "cell_id": runtime.name,
            "family_id": "001",
            "form": "testbench",
            "mode": "G2",
            "experimental_arm": "Agentic",
            "outcome": "behavior_failure",
        },
        submission_tree_sha256="frozen-tree",
        cell_output=tmp_path / "audit-testbench-no-ground",
        config=audit.SpectreConfig(timeout_s=600),
        simulate_case=fake_simulate_case,
        behavior_evaluator=fake_evaluate,
    )

    assert checker_calls == 0
    assert result["outcome"] == "runtime_failure"
    assert result["failure_taxonomy"]["primary_class"] == "runtime"
    assert result["failure_taxonomy"]["responsibility"] == "candidate"
    assert result["cases"][0]["outcome"] == "invalid_run"
    assert result["cases"][0]["failure_kind"] == "floating_source_reference"


def test_testbench_case_reclassifies_cached_spectre_no_ground_run(
    tmp_path: Path,
) -> None:
    audit = load_audit()
    output_dir = tmp_path / "reference"
    warning = (
        "WARNING (SPECTRE-470): No ground node was found in the netlist. "
        "Spectre will add a gmin."
    )
    write_json(
        output_dir / "case_audit_result.json",
        {
            "case_cache_schema_version": "vabench-spectre-case-cache-v1",
            "case_id": "reference",
            "role": "reference",
            "outcome": "reference_fail",
            "responsibility": "candidate",
            "failure_kind": None,
            "behavior_score": 0.0,
            "behavior_notes": ["reference: checked=0"],
            "spectre": {
                "ok": True,
                "status": "success",
                "stdout_tail": warning,
            },
        },
    )
    tb_source = tmp_path / "candidate.scs"
    tb_source.write_text(
        "simulator lang=spectre\n"
        "global 0\n"
        "Vclk (clk vss) vsource dc=0.9\n"
        "Ven (enable vss) vsource dc=0.4\n",
        encoding="utf-8",
    )

    case, oracle = audit._testbench_case(
        runtime=tmp_path / "unused-runtime",
        cell_id="v4-832-G2-r00-agentic",
        tb_source=tb_source,
        source_eval=tmp_path / "unused-evaluator",
        public_contract={},
        target_artifacts=[],
        negative_bundle=None,
        checker_task_id="v4_332_polyphase_iq_balance_monitor",
        required_signals=set(),
        case_id="reference",
        output_dir=output_dir,
        trace_cache_root=tmp_path / "trace-cache",
        config=audit.SpectreConfig(timeout_s=600),
        simulate_case=lambda **_kwargs: pytest.fail("cached case was rerun"),
        behavior_evaluator=lambda *_args, **_kwargs: pytest.fail(
            "cached no-ground trace reached checker"
        ),
    )

    assert case["resumed_case"] is True
    assert case["outcome"] == "invalid_run"
    assert case["responsibility"] == "candidate"
    assert case["failure_kind"] == "floating_source_reference"
    assert oracle.outcome == audit.CaseOutcome.INVALID_RUN


def test_spectre_no_ground_warning_does_not_reclassify_grounded_source_graph(
    tmp_path: Path,
) -> None:
    audit = load_audit()
    tb_source = tmp_path / "grounded.scs"
    tb_source.write_text(
        "simulator lang=spectre\n"
        "global 0\n"
        "V0 (gnd 0) vsource dc=0\n"
        "Vclk (clk gnd) vsource dc=0.9\n",
        encoding="utf-8",
    )
    warning = {
        "stdout_tail": (
            "WARNING (SPECTRE-470): No ground node was found in the netlist"
        )
    }

    assert not audit._spectre_added_ground_gmin(warning, tb_source)

    global_ground = tmp_path / "global-ground.scs"
    global_ground.write_text(
        "simulator lang=spectre\n"
        "global (gnd)\n"
        "Vclk (clk gnd) vsource dc=0.9\n",
        encoding="utf-8",
    )
    assert not audit._spectre_added_ground_gmin(warning, global_ground)

    output_only = tmp_path / "output-only.scs"
    output_only.write_text(
        "simulator lang=spectre\n"
        "XDUT (out) output_driver\n",
        encoding="utf-8",
    )
    assert not audit._spectre_added_ground_gmin(warning, output_only)


def test_run_audit_resumes_a_matching_sidecar_result_without_rerunning_cell(
    tmp_path: Path,
) -> None:
    audit = load_audit()
    release_task = (
        ROOT
        / "benchmark-vabench-release-v4"
        / "release"
        / "benchmarkv4-r52"
        / "tasks"
        / "501-bang-bang-phase-detector-testbench"
    )
    runtime = tmp_path / "campaign" / "v4-501-G0-r00-oneshot"
    shutil.copytree(release_task / "evaluator", runtime / "evaluator")
    shutil.copy2(release_task / "task_record.json", runtime / "evaluator" / "task_record.json")
    plan = [
        {
            "cell_id": runtime.name,
            "runtime": runtime,
            "submission_tree_sha256": "frozen-tree",
            "score_row": {
                "cell_id": runtime.name,
                "family_id": "001",
                "form": "testbench",
                "mode": "G0",
                "experimental_arm": "OneShot",
                "outcome": "runtime_failure",
            },
        }
    ]
    calls = 0

    def fake_audit_cell(**kwargs):
        nonlocal calls
        calls += 1
        return {
            "schema_version": audit.SCHEMA_VERSION,
            "cell_id": kwargs["score_row"]["cell_id"],
            "family_id": "001",
            "form": "testbench",
            "mode": "G0",
            "experimental_arm": "OneShot",
            "source_outcome": "runtime_failure",
            "outcome": "passed",
            "diagnostics": [],
            "failure_taxonomy": None,
            "reference_gate": True,
            "killed_count": 5,
            "survived_count": 0,
            "invalid_count": 0,
            "cases": [],
        }

    work_root = tmp_path / "spectre-sidecar"
    output = tmp_path / "SCORE_SPECTRE_AUDIT.json"
    first = audit.run_audit(
        plan=plan,
        work_root=work_root,
        output=output,
        config=audit.SpectreConfig(timeout_s=10),
        workers=1,
        cell_auditor=fake_audit_cell,
    )
    second = audit.run_audit(
        plan=plan,
        work_root=work_root,
        output=output,
        config=audit.SpectreConfig(timeout_s=10),
        workers=1,
        cell_auditor=fake_audit_cell,
    )

    assert calls == 1
    assert first["resumed_cell_count"] == 0
    assert second["resumed_cell_count"] == 1
    assert second["cell_count"] == 1
    assert second["rows"][0]["outcome"] == "passed"
    assert second["rows"][0]["input_signature_sha256"]
    assert json.loads(output.read_text(encoding="utf-8")) == second


def test_run_audit_retries_matching_retryable_infrastructure_result(
    tmp_path: Path,
) -> None:
    audit = load_audit()
    release_task = (
        ROOT
        / "benchmark-vabench-release-v4"
        / "release"
        / "benchmarkv4-r52"
        / "tasks"
        / "501-bang-bang-phase-detector-testbench"
    )
    runtime = tmp_path / "campaign" / "v4-501-G0-r00-oneshot"
    shutil.copytree(release_task / "evaluator", runtime / "evaluator")
    shutil.copy2(release_task / "task_record.json", runtime / "evaluator" / "task_record.json")
    plan = [
        {
            "cell_id": runtime.name,
            "runtime": runtime,
            "submission_tree_sha256": "frozen-tree",
            "score_row": {
                "cell_id": runtime.name,
                "family_id": "001",
                "form": "testbench",
                "mode": "G0",
                "experimental_arm": "OneShot",
                "outcome": "runtime_failure",
            },
        }
    ]
    calls = 0

    def fake_audit_cell(**kwargs):
        nonlocal calls
        calls += 1
        if calls == 1:
            return {
                "schema_version": audit.SCHEMA_VERSION,
                "cell_id": kwargs["score_row"]["cell_id"],
                "source_outcome": "runtime_failure",
                "outcome": "infrastructure_failure",
                "failure_taxonomy": audit.taxonomy(
                    "infrastructure",
                    "checker_timeout",
                    retryable=True,
                    responsibility="system",
                ),
            }
        return {
            "schema_version": audit.SCHEMA_VERSION,
            "cell_id": kwargs["score_row"]["cell_id"],
            "source_outcome": "runtime_failure",
            "outcome": "behavior_failure",
            "failure_taxonomy": audit.taxonomy("property", "property_check"),
        }

    work_root = tmp_path / "spectre-sidecar"
    output = tmp_path / "SCORE_SPECTRE_AUDIT.json"
    first = audit.run_audit(
        plan=plan,
        work_root=work_root,
        output=output,
        config=audit.SpectreConfig(timeout_s=10, checker_timeout_s=3),
        workers=1,
        cell_auditor=fake_audit_cell,
    )
    second = audit.run_audit(
        plan=plan,
        work_root=work_root,
        output=output,
        config=audit.SpectreConfig(timeout_s=10, checker_timeout_s=3),
        workers=1,
        cell_auditor=fake_audit_cell,
    )

    assert calls == 2
    assert first["resumed_cell_count"] == 0
    assert second["resumed_cell_count"] == 0
    assert second["rows"][0]["outcome"] == "behavior_failure"
    assert second["rows"][0]["pass_impact_reason"] == (
        "attribution_only_nonpass_reclassification"
    )
    assert second["pass_impact"]["net_confirmed_pass_delta"] == 0


def test_dut_checker_retry_reuses_successful_spectre_trace_and_own_timeout(
    tmp_path: Path,
) -> None:
    audit = load_audit()
    release_task = (
        ROOT
        / "benchmark-vabench-release-v4"
        / "release"
        / "benchmarkv4-r52"
        / "tasks"
        / "189-trim-ctrl-4bit"
    )
    runtime = tmp_path / "v4-189-G2-r00-agentic"
    shutil.copytree(release_task / "evaluator", runtime / "evaluator")
    shutil.copy2(release_task / "task_record.json", runtime / "evaluator" / "task_record.json")
    submission = runtime / "evidence" / "final_submission"
    submission.mkdir(parents=True)
    shutil.copy2(
        release_task / "evaluator" / "solution" / "trim_ctrl_4bit.va",
        submission / "trim_ctrl_4bit.va",
    )
    simulate_calls = 0
    checker_timeouts: list[int] = []

    def fake_simulate_case(**kwargs):
        nonlocal simulate_calls
        simulate_calls += 1
        output_dir = kwargs["output_dir"]
        output_dir.mkdir(parents=True, exist_ok=True)
        required = sorted(kwargs["required_signals"])
        (output_dir / "tran_spectre.csv").write_text(
            ",".join(["time", *required])
            + "\n"
            + ",".join(["0", *(["0"] * len(required))])
            + "\n",
            encoding="utf-8",
        )
        return {
            "ok": True,
            "status": "success",
            "errors": [],
            "warnings": [],
            "signals": ["time", *required],
            "rows": 1,
            "spectre_backend": "sui-direct",
            "spectre_mode": "ax",
        }

    checker_calls = 0

    def fake_checker(_checker_id, _csv_path, *, timeout_s):
        nonlocal checker_calls
        checker_calls += 1
        checker_timeouts.append(timeout_s)
        if checker_calls == 1:
            return 0.0, [f"behavior_eval_timeout>{timeout_s}s"]
        return 0.0, ["P_EXPECTED mismatch_count=1"]

    kwargs = {
        "runtime": runtime,
        "score_row": {
            "cell_id": runtime.name,
            "family_id": "189",
            "form": "dut",
            "mode": "G2",
            "experimental_arm": "Agentic",
            "outcome": "runtime_failure",
        },
        "submission_tree_sha256": "frozen-tree",
        "cell_output": tmp_path / "audit-dut",
        "trace_cache_root": tmp_path / "trace-cache",
        "config": audit.SpectreConfig(timeout_s=600, checker_timeout_s=17),
        "simulate_case": fake_simulate_case,
        "behavior_evaluator": fake_checker,
    }
    first = audit.audit_cell(**kwargs)
    second = audit.audit_cell(**kwargs)

    assert first["outcome"] == "infrastructure_failure"
    assert first["failure_taxonomy"]["stage"] == "checker_timeout"
    assert second["outcome"] == "behavior_failure"
    assert simulate_calls == 1
    assert checker_timeouts == [17, 17]


def test_trace_cache_binds_trace_implementation_but_not_checker_implementation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    audit = load_audit()
    tb = tmp_path / "tb.scs"
    tb.write_text("simulator lang=spectre\ntran tran stop=1n\n", encoding="utf-8")
    dut = tmp_path / "dut.va"
    dut.write_text("module dut; endmodule\n", encoding="utf-8")
    calls = 0

    def fake_simulate_case(**kwargs):
        nonlocal calls
        calls += 1
        output_dir = kwargs["output_dir"]
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "tran_spectre.csv").write_text(
            "time,out\n0,0\n", encoding="utf-8"
        )
        return {"ok": True, "status": "success"}

    kwargs = {
        "cell_id": "trace-cache-cell",
        "case_id": "score",
        "tb_path": tb,
        "include_paths": [dut],
        "requested_output_dir": tmp_path / "uncached",
        "trace_cache_root": tmp_path / "cache",
        "required_signals": {"out"},
        "side_output_files": (),
        "config": audit.SpectreConfig(timeout_s=10, checker_timeout_s=3),
        "simulate_case": fake_simulate_case,
    }
    implementation = audit._spectre_trace_implementation_sha256()
    assert set(implementation) == {
        "default_simulate_case",
        "run_gold_dual_suite.py",
    }
    assert "simulate_evas.py" not in implementation

    _first, _path, first_reused = audit._run_or_reuse_spectre_trace(**kwargs)
    _second, _path, second_reused = audit._run_or_reuse_spectre_trace(**kwargs)
    monkeypatch.setattr(
        audit,
        "_spectre_trace_implementation_sha256",
        lambda: {**implementation, "default_simulate_case": "changed"},
    )
    _third, _path, third_reused = audit._run_or_reuse_spectre_trace(**kwargs)

    assert first_reused is False
    assert second_reused is True
    assert third_reused is False
    assert calls == 2


def test_trace_cache_binds_relative_include_paths(tmp_path: Path) -> None:
    audit = load_audit()
    tb = tmp_path / "tb.scs"
    tb.write_text("simulator lang=spectre\ntran tran stop=1n\n", encoding="utf-8")
    dut = tmp_path / "dut.va"
    dut.write_text("module dut; endmodule\n", encoding="utf-8")
    calls = 0

    def fake_simulate_case(**kwargs):
        nonlocal calls
        calls += 1
        output_dir = kwargs["output_dir"]
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "tran_spectre.csv").write_text(
            "time,out\n0,0\n", encoding="utf-8"
        )
        return {"ok": True, "status": "success"}

    kwargs = {
        "cell_id": "trace-cache-path-cell",
        "case_id": "score",
        "tb_path": tb,
        "include_paths": [dut],
        "requested_output_dir": tmp_path / "uncached",
        "trace_cache_root": tmp_path / "cache",
        "required_signals": {"out"},
        "side_output_files": (),
        "config": audit.SpectreConfig(timeout_s=10, checker_timeout_s=3),
        "simulate_case": fake_simulate_case,
    }

    _first, _path, first_reused = audit._run_or_reuse_spectre_trace(**kwargs)
    support = tmp_path / "support"
    support.mkdir()
    moved = support / "dut.va"
    moved.write_bytes(dut.read_bytes())
    kwargs["include_paths"] = [moved]
    _second, _path, second_reused = audit._run_or_reuse_spectre_trace(**kwargs)

    assert first_reused is False
    assert second_reused is False
    assert calls == 2


def test_summary_excludes_runtime_and_infrastructure_without_inventing_pass_gain() -> None:
    audit = load_audit()
    rows = [
        {
            "cell_id": "spectre-runtime-a",
            "form": "dut",
            "experimental_arm": "Agentic",
            "source_outcome": "runtime_failure",
            "outcome": "runtime_failure",
            "failure_taxonomy": audit.taxonomy("runtime", "simulation"),
        },
        {
            "cell_id": "spectre-runtime-b",
            "form": "dut",
            "experimental_arm": "Agentic",
            "source_outcome": "runtime_failure",
            "outcome": "runtime_failure",
            "failure_taxonomy": audit.taxonomy("runtime", "simulation"),
        },
        {
            "cell_id": "checker-timeout",
            "form": "testbench",
            "experimental_arm": "Agentic",
            "source_outcome": "runtime_failure",
            "outcome": "infrastructure_failure",
            "failure_taxonomy": audit.taxonomy(
                "infrastructure",
                "checker_timeout",
                retryable=True,
                responsibility="system",
            ),
        },
        {
            "cell_id": "stale-score-provenance",
            "form": "testbench",
            "experimental_arm": "Agentic",
            "source_outcome": "runtime_failure",
            "outcome": "passed",
            "failure_taxonomy": None,
        },
        {
            "cell_id": "both-nonpass",
            "form": "testbench",
            "experimental_arm": "Agentic",
            "source_outcome": "runtime_failure",
            "outcome": "behavior_failure",
            "failure_taxonomy": audit.taxonomy("property", "property_check"),
        },
    ]

    summary = audit._summarize_audit(
        rows,
        resumed_cell_count=0,
        config=audit.SpectreConfig(),
    )

    assert summary["semantic_denominator"] == {
        "eligible_cells": 2,
        "excluded_cells": 3,
        "excluded_by_reason": {
            "retryable_infrastructure": 1,
            "unresolved_simulation_runtime": 2,
        },
    }
    assert summary["pass_impact"]["net_confirmed_pass_delta"] == 0
    assert summary["pass_impact"]["by_reason"] == {
        "attribution_only_nonpass_reclassification": 2,
        "provenance_resolution_to_pass": 1,
        "unchanged": 2,
    }


def test_resume_signature_changes_with_spectre_execution_environment(
    tmp_path: Path,
) -> None:
    audit = load_audit()
    release_task = (
        ROOT
        / "benchmark-vabench-release-v4"
        / "release"
        / "benchmarkv4-r52"
        / "tasks"
        / "501-bang-bang-phase-detector-testbench"
    )
    runtime = tmp_path / "campaign" / "v4-501-G0-r00-oneshot"
    shutil.copytree(release_task / "evaluator", runtime / "evaluator")
    shutil.copy2(
        release_task / "task_record.json",
        runtime / "evaluator" / "task_record.json",
    )
    item = {
        "cell_id": runtime.name,
        "runtime": runtime,
        "submission_tree_sha256": "frozen-tree",
        "score_row": {
            "cell_id": runtime.name,
            "family_id": "001",
            "form": "testbench",
            "mode": "G0",
            "experimental_arm": "OneShot",
            "outcome": "runtime_failure",
        },
    }
    baseline = audit.SpectreConfig(
        backend="sui-direct",
        timeout_s=10,
        sui_host="spectre-a",
        sui_work_root="/tmp/spectre-a",
        cadence_cshrc="/opt/cadence/a.cshrc",
    )
    _, baseline_sha = audit._cell_input_signature(item, baseline)

    for override in (
        {"sui_host": "spectre-b"},
        {"sui_work_root": "/tmp/spectre-b"},
        {"cadence_cshrc": "/opt/cadence/b.cshrc"},
        {"checker_timeout_s": 20},
    ):
        changed = audit.SpectreConfig(
            backend="sui-direct",
            timeout_s=10,
            checker_timeout_s=override.get(
                "checker_timeout_s", baseline.checker_timeout_s
            ),
            sui_host=override.get("sui_host", baseline.sui_host),
            sui_work_root=override.get(
                "sui_work_root", baseline.sui_work_root
            ),
            cadence_cshrc=override.get(
                "cadence_cshrc", baseline.cadence_cshrc
            ),
        )
        _, changed_sha = audit._cell_input_signature(item, changed)
        assert changed_sha != baseline_sha


def test_cli_requires_explicit_spectre_backend(tmp_path: Path) -> None:
    audit = load_audit()

    with pytest.raises(SystemExit) as exc_info:
        audit.main(
            [
                "--score",
                str(tmp_path / "score.json"),
                "--campaign-run",
                str(tmp_path / "run"),
                "--freeze-manifest",
                str(tmp_path / "freeze.json"),
                "--work-root",
                str(tmp_path / "work"),
                "--output",
                str(tmp_path / "output.json"),
                "--plan-only",
            ]
        )

    assert exc_info.value.code == 2


def test_run_audit_allows_up_to_48_workers_for_remote_spectre_throughput(
    tmp_path: Path,
) -> None:
    audit = load_audit()

    result = audit.run_audit(
        plan=[],
        work_root=tmp_path / "work",
        output=tmp_path / "score.json",
        config=audit.SpectreConfig(timeout_s=10),
        workers=48,
    )

    assert result["cell_count"] == 0
    with pytest.raises(ValueError, match="between 1 and 48"):
        audit.run_audit(
            plan=[],
            work_root=tmp_path / "too-many",
            output=tmp_path / "too-many.json",
            config=audit.SpectreConfig(timeout_s=10),
            workers=49,
        )


def test_testbench_spectre_compile_error_is_not_reported_as_runtime(
    tmp_path: Path,
) -> None:
    audit = load_audit()
    release_task = (
        ROOT
        / "benchmark-vabench-release-v4"
        / "release"
        / "benchmarkv4-r52"
        / "tasks"
        / "501-bang-bang-phase-detector-testbench"
    )
    runtime = tmp_path / "v4-501-G0-r00-oneshot"
    shutil.copytree(release_task / "evaluator", runtime / "evaluator")
    shutil.copy2(release_task / "task_record.json", runtime / "evaluator" / "task_record.json")
    submission = runtime / "evidence" / "final_submission"
    submission.mkdir(parents=True)
    shutil.copy2(
        release_task / "evaluator" / "reference_tb.scs",
        submission / "testbench.scs",
    )

    def compile_failure(**_kwargs):
        return {
            "ok": False,
            "status": "error",
            "errors": [
                "spectre_failed rc=2",
                "Error found by spectre during circuit read-in.",
            ],
            "warnings": [],
            "stdout_tail": "Licensing Information:\nspectre terminated prematurely",
        }

    result = audit.audit_cell(
        runtime=runtime,
        score_row={
            "cell_id": runtime.name,
            "family_id": "001",
            "form": "testbench",
            "mode": "G0",
            "experimental_arm": "OneShot",
            "outcome": "runtime_failure",
        },
        submission_tree_sha256="frozen-tree",
        cell_output=tmp_path / "audit-cell",
        config=audit.SpectreConfig(timeout_s=10),
        simulate_case=compile_failure,
    )

    assert result["outcome"] == "compile_failure"
    assert result["failure_taxonomy"]["primary_class"] == "compile"
    assert {case["failure_kind"] for case in result["cases"]} == {"compile"}


def test_spectre_x_maxstep_override_is_invalid_oracle_config(
    tmp_path: Path,
) -> None:
    audit = load_audit()
    tb = tmp_path / "tb.scs"
    tb.write_text(
        "simulator lang=spectre\n"
        "tran tran stop=10n maxstep=5p\n",
        encoding="utf-8",
    )
    output_dir = tmp_path / "spectre"
    output_dir.mkdir()
    (output_dir / "spectre.out").write_text(
        "WARNING (SPECTRE-592): ax mode changed maxstep settings.\n"
        "    maxstep = 76 ps\n",
        encoding="utf-8",
    )

    notes = audit._spectre_oracle_config_issue(
        tb,
        {"ok": True, "status": "success", "stdout_tail": ""},
        output_dir,
    )

    assert notes
    assert "not a semantic oracle" in notes[0]
    assert "rerun required" in notes[1]


def test_spectre_transport_connection_closed_is_retryable_infrastructure() -> None:
    audit = load_audit()

    kind = audit._spectre_failure_kind(
        {
            "ok": False,
            "errors": ["spectre_failed rc=255"],
            "stdout_tail": "Connection closed by UNKNOWN port 65535",
        }
    )

    assert kind == "infrastructure"


def test_bridge_lite_missing_preflight_blocks_before_spectre_launch(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    audit = load_audit()
    launched = False

    def forbidden_launch(**_kwargs):
        nonlocal launched
        launched = True
        pytest.fail("remote Spectre launch must not run when bridge-lite is missing")

    monkeypatch.setattr(audit, "default_bridge_repo", lambda: tmp_path / "missing-bridge")
    monkeypatch.setattr(audit, "run_spectre_case", forbidden_launch)

    with pytest.raises(FileNotFoundError, match="bridge-lite preflight failed"):
        audit._default_simulate_case(
            cell_id="preflight-cell",
            case_id="score",
            tb_path=tmp_path / "tb.scs",
            include_paths=[],
            output_dir=tmp_path / "out",
            required_signals=set(),
            config=audit.SpectreConfig(backend="bridge", timeout_s=10),
        )

    assert launched is False


def test_summary_preserves_invalid_oracle_config_as_retryable_infrastructure() -> None:
    audit = load_audit()
    rows = [
        {
            "cell_id": "spectre-x-artifact",
            "form": "testbench",
            "experimental_arm": "Agentic",
            "source_outcome": "behavior_failure",
            "outcome": "infrastructure_failure",
            "failure_taxonomy": audit.taxonomy(
                "infrastructure",
                "invalid_oracle_config",
                retryable=True,
                responsibility="system",
            ),
        }
    ]

    summary = audit._summarize_audit(
        rows,
        resumed_cell_count=0,
        config=audit.SpectreConfig(),
    )

    assert summary["semantic_denominator"] == {
        "eligible_cells": 0,
        "excluded_cells": 1,
        "excluded_by_reason": {"retryable_infrastructure": 1},
    }
    assert summary["infrastructure_cells"] == ["spectre-x-artifact"]
