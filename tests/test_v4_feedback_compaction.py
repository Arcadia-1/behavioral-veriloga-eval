from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUN_CAMPAIGN = (
    ROOT
    / "benchmark-vabench-release-v4"
    / "operations"
    / "calibration_pilot"
    / "run_campaign.py"
)


def load_run_campaign():
    spec = importlib.util.spec_from_file_location("run_campaign_under_test", RUN_CAMPAIGN)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_compact_feedback_result_keeps_oracle_lines_and_drops_counters() -> None:
    module = load_run_campaign()
    noisy_counters = "\n".join(f"    timer_counter_{idx} = {idx}" for idx in range(200))
    compact = module.compact_feedback_result(
        {
            "returncode": 1,
            "elapsed_s": 12.5,
            "stdout": "\n".join(
                [
                    "reference: simulation failed",
                    "EVAS -- Event-driven Verilog-A Simulator",
                    noisy_counters,
                    "ERROR: Invalid source vin: PWL wave must contain an even number of values",
                    "FEEDBACK_TB_INVALID_RUN",
                ]
            ),
            "stderr": "",
        }
    )

    text = "\n".join(compact["diagnostics"])
    assert compact["schema_version"] == "v4-feedback-tool-result-compact-v1"
    assert compact["status"] == "fail"
    assert "reference: simulation failed" in text
    assert "ERROR: Invalid source vin" in text
    assert "FEEDBACK_TB_INVALID_RUN" in text
    assert "timer_counter_199" not in text
    assert compact["stdout_chars"] > len(text)


def test_compact_feedback_result_keeps_negative_coverage_summary() -> None:
    module = load_run_campaign()
    compact = module.compact_feedback_result(
        {
            "returncode": 1,
            "elapsed_s": 3.0,
            "stdout": "\n".join(
                [
                    "reference: edges=10 hold_ok",
                    "negative_1: edges=10 hold_ok",
                    "negative_2: output_not_held jitter=0.5000V",
                    "FEEDBACK_TB_NEGATIVE_COVERAGE_FAIL killed=4/5 survived=1 invalid=0",
                ]
            ),
            "stderr": "",
        }
    )

    assert compact["markers"] == [
        "FEEDBACK_TB_NEGATIVE_COVERAGE_FAIL killed=4/5 survived=1 invalid=0"
    ]
    assert compact["diagnostics"] == [
        "reference: edges=10 hold_ok",
        "negative_1: edges=10 hold_ok",
        "negative_2: output_not_held jitter=0.5000V",
        "FEEDBACK_TB_NEGATIVE_COVERAGE_FAIL killed=4/5 survived=1 invalid=0",
    ]
