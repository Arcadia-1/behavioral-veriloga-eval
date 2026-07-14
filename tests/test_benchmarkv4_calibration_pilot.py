from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys


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


def write_runtime_policy(runtime: Path, artifacts: list[str]) -> None:
    evaluator = runtime / "evaluator"
    evaluator.mkdir(parents=True)
    (evaluator / "score_policy.json").write_text(
        json.dumps({"candidate_artifacts": artifacts}),
        encoding="utf-8",
    )


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
    assert by_mode["G0"]["feedback_cli_available"] is False
    assert by_mode["G1"]["process"] == "direct_one_shot"
    assert by_mode["G2"]["process"] == "agentic"
    assert by_mode["G2"]["feedback_cli_available"] is True
    assert by_mode["G5"]["response_protocol"] == "v4-workspace-finalizer-with-prefix-normalization-v2"


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

    mapping, protocol = runner.parse_direct_artifacts(text, runtime)

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

    mapping, protocol = runner.parse_direct_artifacts(text, runtime)

    assert protocol == "normalized_input_artifact_envelope"
    assert mapping == {"flash_folded_dac4.va": "module flash_folded_dac4; endmodule"}
    assert runner.direct_protocol_compliant(protocol) is False


def test_campaign_wrapper_dry_run_exports_agentic_cells(tmp_path: Path) -> None:
    output = tmp_path / "campaign"
    completed = subprocess.run(
        [
            sys.executable,
            str(RUN_CAMPAIGN_WRAPPER),
            "--release",
            str(RELEASE),
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


def test_campaign_wrapper_task_id_filter_does_not_require_selection(tmp_path: Path) -> None:
    output = tmp_path / "campaign-task"
    completed = subprocess.run(
        [
            sys.executable,
            str(RUN_CAMPAIGN_WRAPPER),
            "--release",
            str(RELEASE),
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

