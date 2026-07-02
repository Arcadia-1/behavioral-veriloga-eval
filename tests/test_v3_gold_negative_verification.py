from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNERS = ROOT / "runners"
SCRIPT = ROOT / "scripts" / "run_v3_gold_negative_verification.py"


def load_verifier_module():
    sys.path.insert(0, str(RUNNERS))
    spec = importlib.util.spec_from_file_location("run_v3_gold_negative_verification", SCRIPT)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_task_filter_accepts_slugs_and_three_digit_numbers() -> None:
    verifier = load_verifier_module()
    task_filter = verifier.parse_task_filter(
        "431, 432-hierarchy-nested-parameter-chain,,494-continuous-zi-nd-filter"
    )

    assert verifier.task_matches_filter(Path("431-hierarchy-support-artifact-staging"), task_filter)
    assert verifier.task_matches_filter(Path("432-hierarchy-nested-parameter-chain"), task_filter)
    assert verifier.task_matches_filter(Path("494-continuous-zi-nd-filter"), task_filter)
    assert not verifier.task_matches_filter(Path("433-preprocessor-ifndef-elsif-undef"), task_filter)


def test_empty_task_filter_matches_all_tasks() -> None:
    verifier = load_verifier_module()

    assert verifier.parse_task_filter("") == set()
    assert verifier.task_matches_filter(Path("301-function-clamp-window"), set())
    assert verifier.task_matches_filter(Path("not-numbered"), set())


def test_read_sim_correct_task_slugs_only_returns_behavior_contracts(tmp_path: Path) -> None:
    verifier = load_verifier_module()
    checks = tmp_path / "CHECKS.yaml"
    checks.write_text(
        """
301-function-clamp-window: |
  backend: evas
  sim_correct:
    positive:
      - solution/function_clamp_window.va
410-macro-ifdef-gain-select: |
  backend: evas_pending
  syntax:
    must_include:
      - "`ifdef"
411-escaped-identifier-state: |
  backend: evas
  sim_correct:
    positive:
      - solution/escaped_identifier_state.va
""".lstrip(),
        encoding="utf-8",
    )

    assert verifier.read_sim_correct_task_slugs(checks) == {
        "301-function-clamp-window",
        "411-escaped-identifier-state",
    }


def test_negative_variant_ids_supports_all_manifest_shapes(tmp_path: Path) -> None:
    verifier = load_verifier_module()
    for key in ("cases", "variants", "negative_variants"):
        task_dir = tmp_path / key
        manifest_dir = task_dir / "negative_variants"
        manifest_dir.mkdir(parents=True)
        (manifest_dir / "manifest.json").write_text(
            json.dumps({key: [{"id": "neg_001"}, {"id": "neg_002"}, {"id": ""}]}),
            encoding="utf-8",
        )

        assert verifier.negative_variant_ids(task_dir) == ["neg_001", "neg_002"]


def test_simulator_failure_summary_extracts_concise_error() -> None:
    verifier = load_verifier_module()

    assert verifier.simulator_failure_summary(
        "Reading file\nERROR: Failed to compile Verilog-A file foo.va: unsupported $mfactor()\n"
    ) == "simulator_error=Failed to compile Verilog-A file foo.va: unsupported $mfactor()"
    assert verifier.simulator_failure_summary(
        "Traceback...\nevas.simulator.backend.CompilationError: Unknown child module: resistor in dut.rload\n"
    ) == "simulator_error=Unknown child module: resistor in dut.rload"
    assert verifier.simulator_failure_summary(
        "evas completes with 1 errors, 0 warnings."
    ) == "simulator_error=evas completed with 1 error but did not expose a detailed diagnostic in captured output"
