from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "runners" / "testbench_security.py"
SPEC = importlib.util.spec_from_file_location("v4_testbench_security", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def _task() -> tuple[dict, dict, str]:
    task = (
        ROOT
        / "release"
        / "tri-form-v4-1200-final"
        / "tasks"
        / "testbench"
        / "842-sar-adc-system-4b-testbench"
    )
    contract = json.loads((task / "public_contract.json").read_text(encoding="utf-8"))
    policy = json.loads((task / "evaluator" / "testbench_security_policy.json").read_text(encoding="utf-8"))
    deck = (task / "evaluator" / "reference_tb.scs").read_text(encoding="utf-8")
    return contract, policy, deck


def _validate(tmp_path: Path, deck: str):
    contract, policy, _ = _task()
    candidate = tmp_path / "testbench.scs"
    candidate.write_text(deck, encoding="utf-8")
    return MODULE.validate_testbench(candidate, contract, policy)


def test_reference_deck_passes_structural_security(tmp_path: Path) -> None:
    _, _, deck = _task()
    result = _validate(tmp_path, deck)
    assert result.valid, result.diagnostics


def test_undeclared_include_and_path_traversal_are_rejected(tmp_path: Path) -> None:
    _, _, deck = _task()
    result = _validate(tmp_path, deck + '\nahdl_include "../private/gold.va"\n')
    assert not result.valid
    assert {item.rule for item in result.findings} >= {"path_traversal", "undeclared_include"}


def test_dut_redefinition_is_rejected(tmp_path: Path) -> None:
    _, _, deck = _task()
    result = _validate(tmp_path, deck + "\nsimulator lang=veriloga\nmodule sar_adc_top; endmodule\n")
    assert not result.valid
    assert "dut_redefinition" in {item.rule for item in result.findings}


def test_direct_output_drive_is_rejected(tmp_path: Path) -> None:
    _, _, deck = _task()
    result = _validate(tmp_path, deck + "\nVcheat (done 0) vsource dc=0.9\n")
    assert not result.valid
    assert "direct_dut_output_drive" in {item.rule for item in result.findings}


def test_literal_zero_current_anchor_on_output_is_allowed(tmp_path: Path) -> None:
    _, _, deck = _task()
    result = _validate(tmp_path, deck + "\nIanchor (done 0) isource dc=0\n")
    assert result.valid, result.diagnostics


def test_private_probe_is_rejected(tmp_path: Path) -> None:
    _, _, deck = _task()
    result = _validate(tmp_path, deck.replace("save vin", "save XDUT.secret vin"))
    assert not result.valid
    assert "private_hierarchical_probe" in {item.rule for item in result.findings}


def test_missing_required_trace_is_rejected(tmp_path: Path) -> None:
    _, _, deck = _task()
    result = _validate(tmp_path, deck.replace(" done sample_dbg dac_dbg", " done sample_dbg"))
    assert not result.valid
    assert "all_required_public_traces" in {item.rule for item in result.findings}


def test_unbounded_transient_is_rejected(tmp_path: Path) -> None:
    _, _, deck = _task()
    result = _validate(tmp_path, deck.replace("tran tran stop=215n maxstep=100p", "tran tran"))
    assert not result.valid
    assert "unbounded_resource_use" in {item.rule for item in result.findings}
