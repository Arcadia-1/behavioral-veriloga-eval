from __future__ import annotations

import importlib.util
import json
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
    spec = importlib.util.spec_from_file_location("run_campaign_read_test", RUN_CAMPAIGN)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def prepare_runtime(tmp_path: Path) -> Path:
    runtime = tmp_path / "runtime"
    task = runtime / "public" / "task"
    task.mkdir(parents=True)
    (runtime / "public" / "submission").mkdir(parents=True)
    (task / "instruction.md").write_text("# Task\n", encoding="utf-8")
    (task / "solver_contract.json").write_text('{"contract": true}\n', encoding="utf-8")
    (task / "public_contract.json").write_text('{"contract": true}\n', encoding="utf-8")
    supplied = task / "supplied_dut"
    supplied.mkdir()
    (supplied / "dut.va").write_text("module dut(); endmodule\n", encoding="utf-8")
    return runtime


def test_read_file_short_circuits_prompt_embedded_task_files(tmp_path: Path) -> None:
    module = load_run_campaign()
    runtime = prepare_runtime(tmp_path)

    text, done = module.execute_tool(
        "read_file",
        {"path": "task/solver_contract.json"},
        runtime,
        None,
        120,
        "compact",
    )

    payload = json.loads(text)
    assert done is False
    assert payload["status"] == "already_in_initial_prompt"
    assert payload["path"] == "task/solver_contract.json"
    assert '"contract": true' not in text


def test_read_file_returns_immutable_task_source_once_per_episode(tmp_path: Path) -> None:
    module = load_run_campaign()
    runtime = prepare_runtime(tmp_path)

    first, _ = module.execute_tool(
        "read_file",
        {"path": "task/supplied_dut/dut.va"},
        runtime,
        None,
        120,
        "compact",
    )
    second, _ = module.execute_tool(
        "read_file",
        {"path": "task/supplied_dut/dut.va"},
        runtime,
        None,
        120,
        "compact",
    )

    assert first == "module dut(); endmodule\n"
    payload = json.loads(second)
    assert payload["status"] == "already_provided_in_this_episode"
    assert payload["path"] == "task/supplied_dut/dut.va"
