from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace

import pytest


ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "benchmark-vabench-release-v4" / "release" / "benchmarkv4"
BUILD_CAMPAIGN = (
    ROOT
    / "benchmark-vabench-release-v4"
    / "operations"
    / "calibration_pilot"
    / "build_campaign.py"
)
RUN_CAMPAIGN_WRAPPER = (
    ROOT
    / "benchmark-vabench-release-v4"
    / "runners"
    / "run_benchmarkv4_campaign.py"
)
RUN_CAMPAIGN = (
    ROOT
    / "benchmark-vabench-release-v4"
    / "operations"
    / "calibration_pilot"
    / "run_campaign.py"
)
TESTBENCH_SECURITY = ROOT / "benchmark-vabench-release-v4" / "runners" / "testbench_security.py"
DERIVED_TESTBENCH_ORACLE = (
    ROOT / "benchmark-vabench-release-v4" / "runners" / "derived_testbench_oracle.py"
)
RENDER_HARNESS = ROOT / "benchmark-vabench-release-v4" / "scripts" / "render_v4_harness.py"
FEEDBACK_ADAPTER = (
    ROOT
    / "benchmark-vabench-release-v4"
    / "operations"
    / "calibration_pilot"
    / "feedback_adapter.py"
)
PREPARE_BUDGET_REUSE = (
    ROOT
    / "benchmark-vabench-release-v4"
    / "operations"
    / "calibration_pilot"
    / "prepare_budget_reuse.py"
)
MATERIALIZE_RELEASE = (
    ROOT
    / "benchmark-vabench-release-v4"
    / "operations"
    / "tri_form_derivation_prep"
    / "materialize_tri_form_release.py"
)


@pytest.fixture(scope="session")
def r45_release(tmp_path_factory: pytest.TempPathFactory) -> Path:
    release = tmp_path_factory.mktemp("benchmarkv4-r45") / "release"
    subprocess.run(
        [
            sys.executable,
            str(MATERIALIZE_RELEASE),
            "--release-revision",
            "r45",
            "--output",
            str(release),
            "--force",
        ],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        check=True,
    )
    return release


def load_build_campaign():
    spec = importlib.util.spec_from_file_location("build_campaign", BUILD_CAMPAIGN)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_run_campaign():
    spec = importlib.util.spec_from_file_location("run_campaign", RUN_CAMPAIGN)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_testbench_security():
    spec = importlib.util.spec_from_file_location("testbench_security", TESTBENCH_SECURITY)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_derived_testbench_oracle():
    spec = importlib.util.spec_from_file_location(
        "derived_testbench_oracle", DERIVED_TESTBENCH_ORACLE
    )
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_feedback_adapter():
    spec = importlib.util.spec_from_file_location("feedback_adapter", FEEDBACK_ADAPTER)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_render_harness():
    spec = importlib.util.spec_from_file_location("render_v4_harness", RENDER_HARNESS)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_prepare_budget_reuse():
    spec = importlib.util.spec_from_file_location("prepare_budget_reuse", PREPARE_BUDGET_REUSE)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def write_runtime_policy(runtime: Path, artifacts: list[str]) -> None:
    evaluator = runtime / "evaluator"
    evaluator.mkdir(parents=True)
    (evaluator / "score_policy.json").write_text(
        json.dumps({"candidate_artifacts": artifacts}),
        encoding="utf-8",
    )


def campaign_cell(mode: str, release: Path = RELEASE) -> dict:
    campaign = load_build_campaign().build_campaign(
        release,
        family_ids=["001"],
        model_provider="test",
        model="test-model",
        max_working_tokens=4096,
        repetitions=1,
    )
    return next(
        cell
        for cell in campaign["cells"]
        if cell["task_id"] == "v4-001" and cell["mode"] == mode
    )


def run_args(output: Path, release: Path = RELEASE) -> SimpleNamespace:
    return SimpleNamespace(
        output=output,
        release=release,
        resume=False,
        dry_run=False,
        final_judge_command=None,
        tool_timeout_s=30,
        judge_timeout_s=30,
        evas_command="evas",
    )


class FakeClient:
    def __init__(self, message: dict) -> None:
        self.message = message

    def complete(self, _messages, _max_tokens, _tools):
        return {
            "id": "fake-response",
            "model": "test-model",
            "choices": [
                {"message": self.message, "finish_reason": "stop"}
            ],
            "usage": {"completion_tokens": 32},
        }


class UnexpectedClientCall:
    def complete(self, *_args, **_kwargs):
        raise AssertionError("resume should finish checkpointed tool calls before another model call")


def fake_evas_command(tmp_path: Path) -> str:
    script = tmp_path / "fake_evas.py"
    script.write_text(
        """from pathlib import Path
import json
import sys
args = sys.argv[1:]
output = Path(args[args.index('-o') + 1])
output.mkdir(parents=True, exist_ok=True)
(output / 'invocation.json').write_text(json.dumps({'argv': args, 'cwd': str(Path.cwd())}))
""",
        encoding="utf-8",
    )
    return f"{sys.executable} {script}"


def test_active_agent_tools_expose_restricted_evas_not_feedback() -> None:
    runner = load_run_campaign()
    names = [tool["function"]["name"] for tool in runner.TOOLS]
    assert names == ["list_files", "read_file", "write_file", "run_evas", "finalize"]


def test_run_evas_dut_uses_fixed_public_contract(tmp_path: Path) -> None:
    runner = load_run_campaign()
    runtime = tmp_path / "runtime"
    task = runtime / "public" / "task"
    submission = runtime / "public" / "submission"
    task.mkdir(parents=True)
    submission.mkdir(parents=True)
    (task / "visible_test.scs").write_text("tran tran stop=1n\n", encoding="utf-8")
    (task / "evas_runtime.json").write_text(json.dumps({
        "schema_version": "r45-direct-evas-runtime-v1",
        "command": "evas simulate public/task/visible_test.scs -o public/submission/evas-output --spectre-strict",
        "working_directory": "runtime_package_root",
    }) + "\n", encoding="utf-8")

    result = runner.run_public_evas(runtime, {}, 30, fake_evas_command(tmp_path))

    assert result["status"] == "pass"
    invocation = json.loads(
        (submission / "evas-output" / "invocation.json").read_text(encoding="utf-8")
    )
    assert invocation["cwd"] == str(runtime)
    assert invocation["argv"][0] == "simulate"
    assert Path(invocation["argv"][1]) == task / "visible_test.scs"
    assert Path(invocation["argv"][invocation["argv"].index("-o") + 1]).is_relative_to(submission)


def test_run_evas_testbench_uses_candidate_and_public_case_only(tmp_path: Path) -> None:
    runner = load_run_campaign()
    runtime = tmp_path / "runtime"
    task = runtime / "public" / "task"
    submission = runtime / "public" / "submission"
    fixture_roots = {}
    for case in ["reference", *(f"mutation_{index:02d}" for index in range(1, 6))]:
        fixture_roots[case] = task / "visible_fixtures" / case / "dut"
        fixture_roots[case].mkdir(parents=True)
        (fixture_roots[case] / "dut.va").write_text(
            f"module dut; // {case}\nendmodule\n", encoding="utf-8"
        )
    fixture = fixture_roots["reference"]
    submission.mkdir(parents=True)
    (submission / "testbench.scs").write_text('ahdl_include "./dut/dut.va"\n', encoding="utf-8")
    (task / "evas_runtime.json").write_text(json.dumps({
        "schema_version": "r45-direct-evas-testbench-suite-v1",
        "candidate": "public/submission/testbench.scs",
        "fixture_policy": "read_only_and_identical_for_visible_and_final_replay",
        "working_directory": "runtime_package_root",
        "cases": [
            {"case": case, "dut_root": f"visible_fixtures/{case}/dut"}
            for case in fixture_roots
        ],
    }) + "\n", encoding="utf-8")

    result = runner.run_public_evas(
        runtime, {"case": "reference"}, 30, fake_evas_command(tmp_path)
    )

    assert result["status"] == "pass"
    run_dir = submission / "runs" / "reference"
    assert (run_dir / "testbench.scs").read_bytes() == (submission / "testbench.scs").read_bytes()
    assert (run_dir / "dut" / "dut.va").read_bytes() == (fixture / "dut.va").read_bytes()
    try:
        runner.run_public_evas(
            runtime, {"case": "../../evaluator"}, 30, fake_evas_command(tmp_path)
        )
    except ValueError as exc:
        assert "unknown public EVAS case" in str(exc)
    else:
        raise AssertionError("run_evas accepted a case outside the public suite")

    (submission / "testbench.scs").write_text(
        'ahdl_include "/etc/passwd"\n', encoding="utf-8"
    )
    try:
        runner.run_public_evas(
            runtime, {"case": "reference"}, 30, fake_evas_command(tmp_path)
        )
    except ValueError as exc:
        assert "escapes the public DUT fixture" in str(exc)
    else:
        raise AssertionError("run_evas accepted an absolute candidate include")


def test_build_campaign_samples_complete_benchmarkv4_families_without_prompt_records() -> None:
    builder = load_build_campaign()

    campaign = builder.build_campaign(
        RELEASE,
        sample_families=2,
        seed=20260715,
        model_provider="openai-compatible",
        model="deepseek-v4-flash",
        max_working_tokens=65536,
        repetitions=1,
    )

    assert campaign["schema_version"] == "v4-calibration-campaign-v2"
    assert campaign["release"].endswith("release/benchmarkv4")
    assert campaign["family_count"] == 2
    assert campaign["task_count"] == 6
    assert campaign["cell_count"] == 36
    assert campaign["selection"]["method"] == "complete_family_sample_without_replacement"

    by_mode = {cell["mode"]: cell for cell in campaign["cells"][:6]}
    assert by_mode["G0"]["process"] == "direct_one_shot"
    assert by_mode["G0"]["evas_cli_available"] is False
    assert by_mode["G1"]["process"] == "direct_one_shot"
    assert by_mode["G2"]["process"] == "agentic"
    assert by_mode["G2"]["evas_cli_available"] is True
    assert by_mode["G5"]["response_protocol"] == "v4-strict-workspace-finalizer-v1"


def test_direct_parser_recovers_single_file_filename_marker_without_strict_compliance(
    tmp_path: Path,
) -> None:
    runner = load_run_campaign()
    runtime = tmp_path / "runtime"
    write_runtime_policy(runtime, ["element_shuffler.va"])

    text = (
        "<<<element_shuffler.va>>>\n"
        "module element_shuffler; endmodule\n"
        "<<<END_VABENCH_ARTIFACT>>>"
    )

    strict_mapping, strict_protocol = runner.parse_direct_artifacts(text, runtime)
    mapping, protocol = runner.parse_recoverable_direct_artifacts(text, runtime)

    assert strict_mapping is None
    assert strict_protocol == "invalid_exact_artifact_envelope"
    assert protocol == "normalized_filename_artifact_envelope"
    assert mapping == {"element_shuffler.va": "module element_shuffler; endmodule"}
    assert runner.direct_protocol_compliant(protocol) is False


def test_direct_parser_recovers_single_file_input_marker_without_strict_compliance(
    tmp_path: Path,
) -> None:
    runner = load_run_campaign()
    runtime = tmp_path / "runtime"
    write_runtime_policy(runtime, ["flash_folded_dac4.va"])

    text = (
        '<<<VABENCH_INPUT_ARTIFACT path="flash_folded_dac4.va">>\n'
        "module flash_folded_dac4; endmodule\n"
        "<<<END_VABENCH_ARTIFACT>>>"
    )

    strict_mapping, strict_protocol = runner.parse_direct_artifacts(text, runtime)
    mapping, protocol = runner.parse_recoverable_direct_artifacts(text, runtime)

    assert strict_mapping is None
    assert strict_protocol == "invalid_exact_artifact_envelope"
    assert protocol == "normalized_input_artifact_envelope"
    assert mapping == {"flash_folded_dac4.va": "module flash_folded_dac4; endmodule"}
    assert runner.direct_protocol_compliant(protocol) is False


def test_direct_parser_preserves_exact_body_and_records_evidence(tmp_path: Path) -> None:
    runner = load_run_campaign()
    runtime = tmp_path / "runtime"
    write_runtime_policy(runtime, ["nested/model.va"])
    (runtime / "public" / "submission").mkdir(parents=True)
    body = "\nmodule model;\nendmodule\n"
    text = (
        '<<<VABENCH_ARTIFACT path="nested/model.va">>>\n'
        f"{body}\n"
        "<<<END_VABENCH_ARTIFACT>>>\n"
    )

    result = runner.extract_direct_submission(text, runtime)

    artifact = runtime / "public" / "submission" / "nested" / "model.va"
    assert result["submission_protocol_compliant"] is True
    assert result["parse_diagnostics"] == []
    assert artifact.read_text(encoding="utf-8") == body
    assert result["response_sha256"] == hashlib.sha256(text.encode()).hexdigest()
    assert result["artifact_sha256"]["nested/model.va"] == hashlib.sha256(
        body.encode()
    ).hexdigest()


def test_usage_fallback_counts_reasoning_and_tool_arguments() -> None:
    runner = load_run_campaign()

    usage = runner.provider_output_usage(
        None,
        "visible",
        reasoning_text="hidden reasoning",
        tool_text='{"content":"module x; endmodule"}',
    )

    assert usage["source"] == "reference_estimate"
    assert usage["reasoning_tokens"] > 0
    assert usage["visible_tokens"] > runner.reference_tokens("visible")
    assert usage["output_tokens"] == usage["reasoning_tokens"] + usage["visible_tokens"]


def test_campaign_validation_rejects_output_path_escape() -> None:
    runner = load_run_campaign()
    cell = campaign_cell("G0")
    cell["cell_id"] = "../../outside"

    try:
        runner.validate_campaign_cells([cell], RELEASE)
    except ValueError as exc:
        assert "invalid campaign cell_id" in str(exc)
    else:
        raise AssertionError("campaign validation accepted a path-escaping cell id")


def test_direct_parser_rejects_prose_and_wrong_order(tmp_path: Path) -> None:
    runner = load_run_campaign()
    runtime = tmp_path / "runtime"
    write_runtime_policy(runtime, ["first.va", "second.va"])
    (runtime / "public" / "submission").mkdir(parents=True)

    wrong_order = (
        '<<<VABENCH_ARTIFACT path="second.va">>>\nsecond\n<<<END_VABENCH_ARTIFACT>>>\n'
        '<<<VABENCH_ARTIFACT path="first.va">>>\nfirst\n<<<END_VABENCH_ARTIFACT>>>'
    )
    mapping, _protocol, diagnostics = runner.parse_direct_artifacts_detailed(
        wrong_order, runtime
    )
    assert mapping is None
    assert "artifact_blocks_not_in_canonical_order" in diagnostics

    prose = (
        "Here are the files:\n"
        '<<<VABENCH_ARTIFACT path="first.va">>>\nfirst\n<<<END_VABENCH_ARTIFACT>>>\n'
        '<<<VABENCH_ARTIFACT path="second.va">>>\nsecond\n<<<END_VABENCH_ARTIFACT>>>'
    )
    mapping, _protocol, diagnostics = runner.parse_direct_artifacts_detailed(prose, runtime)
    assert mapping is None
    assert "non_whitespace_outside_artifact_blocks" in diagnostics


def test_submission_gate_rejects_undeclared_files_and_symlinks(tmp_path: Path) -> None:
    runner = load_run_campaign()
    runtime = tmp_path / "runtime"
    write_runtime_policy(runtime, ["model.va"])
    submission = runtime / "public" / "submission"
    submission.mkdir(parents=True)
    (submission / "model.va").write_text("module model; endmodule", encoding="utf-8")
    (submission / "extra.va").write_text("extra", encoding="utf-8")
    (submission / "link.va").symlink_to(submission / "model.va")

    gate = runner.submission_artifact_gate(runtime)

    assert gate["passed"] is False
    assert "undeclared_artifact_path:extra.va" in gate["diagnostics"]
    assert "symlink_not_allowed:link.va" in gate["diagnostics"]


def test_feedback_compaction_keeps_actionable_property_diagnostics() -> None:
    runner = load_run_campaign()
    stdout = "\n".join(
        [
            "FEEDBACK_EVAS_ENGINE evas_version=0.8.2 evas_engine=evas2",
            "FEEDBACK_BEHAVIOR_FAIL",
            "solver counters: accepted=812 rejected=4",
            (
                "task=v4_312_interleaved_adc_skew_monitor | "
                "P_SKEW_METRIC:mismatch_count=2 expected=0.04 "
                "observed=0.11 time=8.2e-08 gap=0.07"
            ),
        ]
    )

    compact = runner.compact_feedback_result(
        {"returncode": 1, "stdout": stdout, "stderr": "", "elapsed_s": 0.4}
    )

    assert compact["diagnostics"][0].startswith("task=v4_312")
    assert "P_SKEW_METRIC" in compact["diagnostics"][0]
    assert compact["markers"] == [
        "FEEDBACK_EVAS_ENGINE evas_version=0.8.2 evas_engine=evas2",
        "FEEDBACK_BEHAVIOR_FAIL",
    ]
    assert all("solver counters" not in line for line in compact["diagnostics"])


def test_feedback_compaction_keeps_reference_failure_detail() -> None:
    runner = load_run_campaign()
    stdout = "\n".join(
        [
            "reference: missing_vin_step_samples initial_samples=[0.0, 0.0] initial_ok=True",
            "FEEDBACK_TB_REFERENCE_FAIL",
        ]
    )

    lines = runner.compact_text_lines(stdout)

    assert lines == [
        "reference: missing_vin_step_samples initial_samples=[0.0, 0.0] initial_ok=True",
        "FEEDBACK_TB_REFERENCE_FAIL",
    ]


def test_feedback_compaction_keeps_invalid_run_root_cause() -> None:
    runner = load_run_campaign()
    stdout = "\n".join(
        [
            "reference: evas_engine=evas2",
            "reference: simulation failed",
            "FEEDBACK_TB_INVALID_RUN",
        ]
    )
    stderr = "Error: tb_candidate.scs:17: unknown instance parameter 'period'"

    compact = runner.compact_feedback_result(
        {"returncode": 1, "stdout": stdout, "stderr": stderr, "elapsed_s": 0.2}
    )

    assert stderr in compact["diagnostics"]
    assert compact["diagnostics"].index(stderr) < compact["diagnostics"].index(
        "FEEDBACK_TB_INVALID_RUN"
    )


def test_feedback_compaction_keeps_rust_lowering_rejection() -> None:
    runner = load_run_campaign()
    stdout = "\n".join(
        [
            "required_trace_missing_node_count = 0",
            "Traceback (most recent call last):",
            (
                "RuntimeError: evas-rust full-model path was required but no supported "
                "whole-segment Rust runtime matched this design. RustSimProgram rejection: "
                "model:0:debounce_latch_Model:event_due_not_lowered"
            ),
            "FEEDBACK_EVAS_FAIL",
        ]
    )

    lines = runner.compact_text_lines(stdout)

    assert any(line.startswith("RuntimeError:") for line in lines)
    assert any("event_due_not_lowered" in line for line in lines)
    assert all("missing_node_count = 0" not in line for line in lines)
    assert lines.index(next(line for line in lines if line.startswith("RuntimeError:"))) < lines.index(
        "FEEDBACK_EVAS_FAIL"
    )


def test_direct_run_cell_submits_only_an_exact_artifact_response(
    tmp_path: Path, r45_release: Path
) -> None:
    runner = load_run_campaign()
    cell = campaign_cell("G0", r45_release)
    task = r45_release / "tasks" / "001-bang-bang-phase-detector"
    body = (task / "evaluator" / "solution" / "bbpd_ref.va").read_text(encoding="utf-8")
    response = (
        '<<<VABENCH_ARTIFACT path="bbpd_ref.va">>>\n'
        f"{body}\n"
        "<<<END_VABENCH_ARTIFACT>>>"
    )

    result = runner.run_cell(
        cell,
        run_args(tmp_path / "run", r45_release),
        FakeClient({"role": "assistant", "content": response}),
    )

    assert result["status"] == "submitted"
    assert result["submission_protocol_compliant"] is True
    assert result["artifact_gate"]["passed"] is True
    saved = tmp_path / "run" / cell["cell_id"] / "public" / "submission" / "bbpd_ref.va"
    assert saved.read_text(encoding="utf-8") == body


def test_agentic_run_cell_rejects_an_undeclared_file_at_finalize(
    tmp_path: Path, r45_release: Path
) -> None:
    runner = load_run_campaign()
    cell = campaign_cell("G2", r45_release)
    message = {
        "role": "assistant",
        "content": "",
        "tool_calls": [
            {
                "id": "write-required",
                "type": "function",
                "function": {
                    "name": "write_file",
                    "arguments": json.dumps(
                        {"path": "bbpd_ref.va", "content": "module bbpd_ref; endmodule"}
                    ),
                },
            },
            {
                "id": "write-extra",
                "type": "function",
                "function": {
                    "name": "write_file",
                    "arguments": json.dumps({"path": "extra.va", "content": "extra"}),
                },
            },
            {
                "id": "finalize",
                "type": "function",
                "function": {"name": "finalize", "arguments": "{}"},
            },
        ],
    }

    result = runner.run_cell(
        cell,
        run_args(tmp_path / "run", r45_release),
        FakeClient(message),
    )

    assert result["status"] == "invalid_submission"
    assert result["submission_protocol_compliant"] is False
    assert "undeclared_artifact_path:extra.va" in result["artifact_gate"]["diagnostics"]


def test_agentic_resume_finishes_pending_checkpointed_tool_calls(
    tmp_path: Path, r45_release: Path
) -> None:
    runner = load_run_campaign()
    cell = campaign_cell("G2", r45_release)
    args = run_args(tmp_path / "run", r45_release)
    args.resume = True
    runtime = args.output / cell["cell_id"]
    runner.export_runtime(cell, r45_release, runtime)
    prompt = (runtime / "agent_prompt.txt").read_text(encoding="utf-8")
    assistant = {
        "role": "assistant",
        "content": "",
        "tool_calls": [
            {
                "id": "write-required",
                "type": "function",
                "function": {
                    "name": "write_file",
                    "arguments": json.dumps(
                        {"path": "bbpd_ref.va", "content": "module bbpd_ref; endmodule"}
                    ),
                },
            },
            {
                "id": "finalize",
                "type": "function",
                "function": {"name": "finalize", "arguments": "{}"},
            },
        ],
    }
    (runtime / "evidence" / "conversation_checkpoint.json").write_text(
        json.dumps(
            {
                "schema_version": "v4-calibration-conversation-checkpoint-v1",
                "cell_id": cell["cell_id"],
                "messages": [{"role": "user", "content": prompt}, assistant],
                "output_tokens": 32,
                "events": [
                    {
                        "type": "model",
                        "requested_max_tokens": 4096,
                        "provider_output_tokens": 32,
                        "finish_reason": "tool_calls",
                    }
                ],
                "finalized": False,
            }
        ),
        encoding="utf-8",
    )

    result = runner.run_cell(cell, args, UnexpectedClientCall())

    assert result["status"] == "submitted"
    assert result["artifact_gate"]["passed"] is True
    assert (runtime / "public" / "submission" / "bbpd_ref.va").is_file()


def test_campaign_wrapper_dry_run_exports_agentic_cells(
    tmp_path: Path, r45_release: Path
) -> None:
    output = tmp_path / "campaign"
    completed = subprocess.run(
        [
            sys.executable,
            str(RUN_CAMPAIGN_WRAPPER),
            "--release",
            str(r45_release),
            "--sample-families",
            "1",
            "--seed",
            "20260715",
            "--mode",
            "G2",
            "--output-root",
            str(output),
            "--model",
            "deepseek-v4-flash",
            "--dry-run",
            "--workers",
            "1",
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr + completed.stdout
    campaign = json.loads((output / "campaign.json").read_text(encoding="utf-8"))
    assert campaign["cell_count"] == 3
    assert {cell["mode"] for cell in campaign["cells"]} == {"G2"}
    assert {cell["process"] for cell in campaign["cells"]} == {"agentic"}
    summary = json.loads((output / "run" / "SUMMARY.json").read_text(encoding="utf-8"))
    assert summary["statuses"] == {"prepared": 3}


def test_campaign_wrapper_task_id_filter_does_not_require_selection(
    tmp_path: Path, r45_release: Path
) -> None:
    output = tmp_path / "campaign-task"
    completed = subprocess.run(
        [
            sys.executable,
            str(RUN_CAMPAIGN_WRAPPER),
            "--release",
            str(r45_release),
            "--task-id",
            "v4-006",
            "--mode",
            "G0",
            "--output-root",
            str(output),
            "--model",
            "deepseek-v4-flash",
            "--dry-run",
            "--workers",
            "1",
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr + completed.stdout
    campaign = json.loads((output / "campaign.json").read_text(encoding="utf-8"))
    assert campaign["cell_count"] == 1
    assert campaign["cells"][0]["task_id"] == "v4-006"
    assert campaign["cells"][0]["mode"] == "G0"


def test_campaign_wrapper_redacts_credential_and_operator_command_paths(
    tmp_path: Path, r45_release: Path,
) -> None:
    output = tmp_path / "campaign-redacted"
    secret_path = tmp_path / "private" / "provider.key"
    judge_command = f"python3 {tmp_path / 'private' / 'judge.py'}"
    completed = subprocess.run(
        [
            sys.executable,
            str(RUN_CAMPAIGN_WRAPPER),
            "--release",
            str(r45_release),
            "--task-id",
            "v4-001",
            "--mode",
            "G0",
            "--output-root",
            str(output),
            "--model",
            "test-model",
            "--api-key-file",
            str(secret_path),
            "--final-judge-command",
            judge_command,
            "--dry-run",
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr + completed.stdout
    summary_text = (output / "wrapper_summary.json").read_text(encoding="utf-8")
    campaign_text = (output / "campaign.json").read_text(encoding="utf-8")
    persisted_text = summary_text + campaign_text
    assert str(secret_path) not in persisted_text
    assert judge_command not in persisted_text
    assert "<redacted-credential-file>" in summary_text
    assert "<redacted-operator-command>" in summary_text


def test_budget_reuse_requires_identical_execution_configuration() -> None:
    reuse = load_prepare_budget_reuse()
    base = {
        "model_provider": "test-provider",
        "model": "test-model",
        "release_manifest_sha256": "a" * 64,
        "selection_manifest_sha256": "b" * 64,
        "max_output_tokens": 4096,
        "execution_config": {
            "temperature": 0.0,
            "stream": False,
            "base_url_sha256": "c" * 64,
            "evas_command_sha256": "d" * 64,
        },
    }
    target = json.loads(json.dumps(base))
    target["max_output_tokens"] = 65536
    reuse.check_campaign_compatibility(base, target)

    target["execution_config"]["temperature"] = 0.2
    try:
        reuse.check_campaign_compatibility(base, target)
    except ValueError as exc:
        assert "execution_config mismatch" in str(exc)
    else:
        raise AssertionError("reuse accepted a different decoding configuration")


def test_feedback_adapter_uses_exported_lowercase_task_record(tmp_path: Path) -> None:
    adapter = load_feedback_adapter()
    runtime = tmp_path / "runtime"
    (runtime / "evidence").mkdir(parents=True)
    (runtime / "evaluator").mkdir()
    (runtime / "evidence" / "attempt_record.json").write_text(
        json.dumps({"task_id": "v4-001"}), encoding="utf-8"
    )
    task_dir = RELEASE / "tasks" / "001-bang-bang-phase-detector"
    record = json.loads((task_dir / "task_record.json").read_text(encoding="utf-8"))
    (runtime / "evaluator" / "task_record.json").write_text(
        json.dumps(record), encoding="utf-8"
    )

    observed, task_dir = adapter.runtime_task(runtime)

    assert observed["task_id"] == "v4-001"
    assert task_dir.name == "001-bang-bang-phase-detector"


def test_feedback_adapter_uses_the_frozen_five_case_testbench_suite() -> None:
    adapter = load_feedback_adapter()
    evaluator = (
        RELEASE
        / "tasks"
        / "501-bang-bang-phase-detector-testbench"
        / "evaluator"
    )

    suite = adapter.testbench_negative_suite(evaluator)

    assert suite == [
        "neg_001_swap_outputs",
        "neg_003_never_clears_on_clock",
        "neg_004_both_outputs_on_direction",
        "neg_006_weak_high_level",
        "neg_005_retimed_ignored",
    ]


def test_harness_renderer_reproduces_tracked_profiles() -> None:
    renderer = load_render_harness()
    task_dir = RELEASE / "tasks" / "001-bang-bang-phase-detector"
    spec, spec_hash = renderer.load_spec(task_dir / "evaluator" / "harness_spec.json")

    for profile_name in ("feedback", "score"):
        observed = renderer.build_profile(spec, profile_name, spec_hash)
        expected = json.loads(
            (task_dir / "evaluator" / "profiles" / f"{profile_name}.json").read_text(
                encoding="utf-8"
            )
        )
        assert observed == expected


def test_benchmarkv4_testbench_security_uses_public_binding_schema(tmp_path: Path) -> None:
    security = load_testbench_security()
    task = RELEASE / "tasks" / "506-element-shuffler-testbench"
    contract = json.loads((task / "public_contract.json").read_text(encoding="utf-8"))
    policy = json.loads((task / "evaluator" / "score_policy.json").read_text(encoding="utf-8"))
    candidate = tmp_path / "testbench.scs"
    candidate.write_text(
        "\n".join(
            [
                "simulator lang=spectre",
                'ahdl_include "./dut/element_shuffler.va"',
                "XDUT (clk rst_n out0 out1 out2 out3) element_shuffler",
                "tran tran stop=20n",
                "save clk rst_n out0 out1 out2 out3",
            ]
        ),
        encoding="utf-8",
    )

    result = security.validate_testbench(candidate, contract, policy)

    assert result.valid, result.diagnostics


def test_benchmarkv4_testbench_security_rejects_suffixed_or_hierarchical_saves(
    tmp_path: Path,
) -> None:
    security = load_testbench_security()
    task = RELEASE / "tasks" / "506-element-shuffler-testbench"
    contract = json.loads((task / "public_contract.json").read_text(encoding="utf-8"))
    policy = json.loads((task / "evaluator" / "score_policy.json").read_text(encoding="utf-8"))
    candidate = tmp_path / "testbench.scs"
    candidate.write_text(
        "\n".join(
            [
                "simulator lang=spectre",
                'ahdl_include "./dut/element_shuffler.va"',
                "XDUT (clk rst_n out0 out1 out2 out3) element_shuffler",
                "tran tran stop=20n",
                "save clk:V rst_n:V out0:V out1:V out2:V out3:V",
            ]
        ),
        encoding="utf-8",
    )

    result = security.validate_testbench(candidate, contract, policy)

    assert not result.valid
    assert any("private_hierarchical_probe" in item for item in result.diagnostics)


def test_benchmarkv4_testbench_security_enforces_instance_parameters_and_uniqueness(
    tmp_path: Path,
) -> None:
    security = load_testbench_security()
    task = RELEASE / "tasks" / "506-element-shuffler-testbench"
    contract = json.loads((task / "public_contract.json").read_text(encoding="utf-8"))
    contract["testbench_binding"]["instances"][0]["parameter_overrides"] = {"width": 4}
    policy = json.loads(
        (task / "evaluator" / "testbench_security_policy.json").read_text(encoding="utf-8")
    )
    candidate = tmp_path / "testbench.scs"
    required_lines = [
        "simulator lang=spectre",
        'ahdl_include "./dut/element_shuffler.va"',
        "tran tran stop=20n",
        "save clk rst_n out0 out1 out2 out3",
    ]

    candidate.write_text(
        "\n".join(
            required_lines[:2]
            + ["XDUT (clk rst_n out0 out1 out2 out3) element_shuffler"]
            + required_lines[2:]
        ),
        encoding="utf-8",
    )
    missing_parameter = security.validate_testbench(candidate, contract, policy)
    assert not missing_parameter.valid
    assert any("declared_dut_binding" in item for item in missing_parameter.diagnostics)

    instance = "XDUT (clk rst_n out0 out1 out2 out3) element_shuffler width=4"
    candidate.write_text(
        "\n".join(required_lines[:2] + [instance, instance] + required_lines[2:]),
        encoding="utf-8",
    )
    duplicate = security.validate_testbench(candidate, contract, policy)
    assert not duplicate.valid
    assert any("declared_dut_binding" in item for item in duplicate.diagnostics)

    candidate.write_text(
        "\n".join(required_lines[:2] + [instance] + required_lines[2:]),
        encoding="utf-8",
    )
    valid = security.validate_testbench(candidate, contract, policy)
    assert valid.valid, valid.diagnostics


def test_testbench_security_allows_declared_read_only_support() -> None:
    security = load_testbench_security()
    contract = {
        "artifact_contract": {"files": [{"path": "dut.va"}]},
        "supplied_support_artifacts": ["supplied_dut/support/helper.va"],
        "testbench_binding": {"source_path_template": "./dut/{artifact_path}"},
    }

    assert security._allowed_includes(contract) == {
        "./dut/dut.va",
        "./dut/support/helper.va",
    }


def test_negative_bundle_prefers_declared_artifact_over_legacy_alias(tmp_path: Path) -> None:
    oracle = load_derived_testbench_oracle()
    bundle = tmp_path / "negative"
    bundle.mkdir()
    declared = bundle / "cmp_offset_ref.va"
    alias = bundle / "neg_001.va"
    declared.write_text("module cmp_offset_ref; endmodule\n", encoding="utf-8")
    alias.write_text("module legacy_alias; endmodule\n", encoding="utf-8")

    mapped = oracle._negative_bundle_sources(bundle, ["cmp_offset_ref.va"])

    assert mapped == {"cmp_offset_ref.va": declared}


def test_testbench_oracle_stages_modern_dut_and_support_paths(tmp_path: Path) -> None:
    oracle = load_derived_testbench_oracle()
    evaluator = tmp_path / "evaluator"
    (evaluator / "solution" / "support").mkdir(parents=True)
    (evaluator / "solution" / "dut.va").write_text(
        "module dut; endmodule\n", encoding="utf-8"
    )
    (evaluator / "solution" / "support" / "helper.va").write_text(
        "module helper; endmodule\n", encoding="utf-8"
    )
    run_dir = tmp_path / "run"
    run_dir.mkdir()

    oracle._prepare_dut_sources(
        package_root=ROOT,
        source_formal=evaluator,
        run_dir=run_dir,
        target_artifacts=["dut.va"],
        dut_subdir="dut",
        public_contract={
            "supplied_support_artifacts": ["supplied_dut/support/helper.va"]
        },
    )

    assert (run_dir / "dut" / "dut.va").is_file()
    assert (run_dir / "dut" / "support" / "helper.va").is_file()


def test_testbench_oracle_failure_excerpt_keeps_error_before_counters() -> None:
    oracle = load_derived_testbench_oracle()
    combined = "\n".join(
        [
            "Reading netlist tb_candidate.scs",
            "Error: tb_candidate.scs:4: ahdl source loaded with include",
            *(f"solver_counter_{index} = 0" for index in range(500)),
            "evas completes with 1 errors, 0 warnings.",
        ]
    )

    excerpt = oracle._simulation_failure_excerpt(combined)

    assert "Error: tb_candidate.scs:4" in excerpt
    assert "solver_counter_250" not in excerpt


def test_testbench_oracle_requires_r45_evas_version(monkeypatch) -> None:
    oracle = load_derived_testbench_oracle()
    monkeypatch.setenv("EVAS_ENGINE", "evas2")
    monkeypatch.setenv("VAEVAS_DEFAULT_EVAS_ENGINE", "evas2")
    runtime_report = "\n".join(
        [
            "Version 0.8.3 -- Jul 2026",
            "evas_engine = evas-rust",
            "evas_rust_required = true",
            "evas_rust_full_model_required = true",
            "rust_full_model_required_failures = 0",
        ]
    )

    valid, note = oracle._validate_required_evas_engine(runtime_report, "evas2")
    stale, stale_note = oracle._validate_required_evas_engine(
        runtime_report.replace("Version 0.8.3", "Version 0.8.2"), "evas2"
    )

    assert valid is True
    assert "evas_version=0.8.3" in note
    assert stale is False
    assert "observed='0.8.2'" in stale_note
