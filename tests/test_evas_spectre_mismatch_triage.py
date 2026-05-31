from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runners"))

import report_evas_spectre_mismatch_triage as triage  # noqa: E402


def write_result(root: Path, task_id: str, row: dict[str, object]) -> Path:
    result_dir = root / "results" / task_id
    result_dir.mkdir(parents=True)
    path = result_dir / "result.json"
    payload = {
        "task_id": task_id,
        "release_task_id": f"{task_id}:dut",
        "release_entry_id": task_id,
        "form": "dut",
        "category": "Comparator and Decision Circuits",
        "difficulty": "D2",
    }
    payload.update(row)
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_triage_identifies_pass_incomplete_and_two_mismatch_directions(tmp_path: Path) -> None:
    root = tmp_path / "dual"
    write_result(
        root,
        "row_pass",
        {
            "status": "DONE",
            "dual_result": {
                "status": "PASS",
                "evas": {"status": "PASS", "notes": ["returncode=0"]},
                "spectre": {"status": "success", "ok": True, "behavior_score": 1.0},
                "parity": {"status": "passed"},
            },
            "classification": {
                "evas_status": "PASS",
                "spectre_checker_pass": True,
                "dual_status": "PASS",
                "dual_pass": True,
            },
        },
    )
    write_result(
        root,
        "row_evas_pass_spectre_fail",
        {
            "status": "DONE",
            "dual_result": {
                "status": "FAIL_SPECTRE",
                "evas": {"status": "PASS", "notes": ["returncode=0"]},
                "spectre": {
                    "status": "error",
                    "ok": False,
                    "errors": ["spectre_failed rc=2"],
                    "stdout_tail": "ERROR (VACOMP-1917): embedded declaration statement",
                },
                "parity": {"status": "blocked"},
            },
            "classification": {
                "evas_status": "PASS",
                "spectre_checker_pass": False,
                "dual_status": "FAIL_SPECTRE",
                "evas_pass_spectre_fail": True,
            },
        },
    )
    write_result(
        root,
        "row_spectre_pass_evas_fail",
        {
            "status": "DONE",
            "dual_result": {
                "status": "FAIL_EVAS",
                "evas": {
                    "status": "FAIL_DUT_COMPILE",
                    "stdout_tail": "ERROR: unsupported timer event form",
                },
                "spectre": {"status": "success", "ok": True, "behavior_score": 1.0},
                "parity": {"status": "blocked"},
            },
            "classification": {
                "evas_status": "FAIL_DUT_COMPILE",
                "spectre_checker_pass": True,
                "dual_status": "FAIL_EVAS",
                "spectre_pass_evas_fail": True,
            },
        },
    )
    write_result(
        root,
        "row_incomplete",
        {
            "status": "INCOMPLETE",
            "generation_status": "no_code_extracted",
            "generation_finish_reason": "length",
            "incomplete_reason": "model_output_budget_exhausted",
        },
    )

    report = triage.build_report([root])

    assert report["total_rows"] == 4
    assert report["strict_dual_pass_rows"] == 1
    assert report["evas_pass_spectre_fail_rows"] == 1
    assert report["spectre_pass_evas_fail_rows"] == 1
    assert report["incomplete_generation_rows"] == 1
    slices = {item["slice"]: item for item in report["score_slices"]}
    assert slices["full_strict"]["total_rows"] == 4
    assert slices["full_strict"]["strict_dual_pass_rate_pct"] == 25.0
    assert slices["valid_candidate"]["total_rows"] == 3
    assert slices["behavior_ready"]["total_rows"] == 1
    difficulty = {item["difficulty"]: item for item in report["breakdowns"]["difficulty"]}
    assert difficulty["D2"]["non_model_or_inconclusive_rows"] == 1
    families = {row["root_cause_family"] for row in report["rows"]}
    assert "strict_dual_pass" in families
    assert "spectre_rejects_evas_accepted_candidate" in families
    assert "evas_rejects_spectre_accepted_dut" in families
    assert "incomplete_generation" in families


def test_triage_marks_parity_failure_as_conformance_seed(tmp_path: Path) -> None:
    root = tmp_path / "dual"
    write_result(
        root,
        "row_waveform",
        {
            "status": "DONE",
            "dual_result": {
                "status": "FAIL_PARITY",
                "evas": {"status": "PASS", "notes": ["returncode=0"]},
                "spectre": {"status": "success", "ok": True, "behavior_score": 1.0},
                "parity": {"status": "failed", "max_rmse_v": 0.2, "max_abs_v": 0.5},
            },
            "classification": {
                "evas_status": "PASS",
                "spectre_checker_pass": True,
                "dual_status": "FAIL_PARITY",
                "dual_pass": False,
            },
        },
    )

    report = triage.build_report([root])
    row = report["rows"][0]

    assert row["triage_axis"] == "parity"
    assert row["root_cause_family"] == "waveform_parity_gate"
    assert report["parity_gate_rows"] == 1
    assert report["conformance_seed_rows"][0]["task_id"] == "row_waveform"


def test_triage_marks_direct_sui_timeout_as_runner_inconclusive(tmp_path: Path) -> None:
    root = tmp_path / "dual"
    write_result(
        root,
        "row_timeout",
        {
            "status": "DONE",
            "dual_result": {
                "status": "FAIL_SPECTRE",
                "evas": {"status": "PASS"},
                "spectre": {
                    "status": "error",
                    "ok": False,
                    "errors": ["sui_direct_timeout_after_s=30"],
                },
            },
            "classification": {
                "evas_status": "PASS",
                "spectre_checker_pass": False,
                "dual_status": "FAIL_SPECTRE",
                "evas_pass_spectre_fail": False,
                "spectre_backend_inconclusive": True,
            },
        },
    )

    report = triage.build_report([root])
    row = report["rows"][0]

    assert row["triage_axis"] == "runner"
    assert row["root_cause_family"] == "spectre_license_or_backend_unavailable"
    assert report["runner_inconclusive_rows"] == 1
    assert report["evas_pass_spectre_fail_rows"] == 0


def test_dedupe_by_task_keeps_last_input(tmp_path: Path) -> None:
    old_root = tmp_path / "old"
    new_root = tmp_path / "new"
    write_result(
        old_root,
        "same_task",
        {
            "status": "DONE",
            "dual_result": {
                "status": "FAIL_EVAS",
                "evas": {"status": "FAIL_DUT_COMPILE"},
                "spectre": {"status": "error", "ok": False},
            },
            "classification": {"evas_status": "FAIL_DUT_COMPILE", "dual_status": "FAIL_EVAS"},
        },
    )
    write_result(
        new_root,
        "same_task",
        {
            "status": "DONE",
            "dual_result": {
                "status": "PASS",
                "evas": {"status": "PASS"},
                "spectre": {"status": "success", "ok": True, "behavior_score": 1.0},
                "parity": {"status": "passed"},
            },
            "classification": {
                "evas_status": "PASS",
                "spectre_checker_pass": True,
                "dual_status": "PASS",
                "dual_pass": True,
            },
        },
    )

    report = triage.build_report([old_root, new_root], dedupe_by_task=True)

    assert report["total_rows"] == 1
    assert report["strict_dual_pass_rows"] == 1
    assert report["rows"][0]["source"] == "new"


def test_spectre_error_rows_are_model_side_when_log_is_specific(tmp_path: Path) -> None:
    root = tmp_path / "dual"
    cases = {
        "row_ahdl": (
            "ERROR (VACOMP-2212): Encountered undeclared identifier: out_target.",
            "model_spectre_ahdl_compile",
            "spectre_ahdl_syntax_scope_or_operator_reject",
        ),
        "row_tb_source": (
            "ERROR (CMI-2194): Vvin: Waveform type must be specified if any waveform parameters are given.",
            "model_spectre_tb_source",
            "spectre_tb_source_or_waveform_reject",
        ),
        "row_topology": (
            "FATAL: The following branches form a loop of rigid branches (shorts).",
            "model_spectre_elab_or_topology",
            "spectre_elaboration_parameter_or_topology_reject",
        ),
    }
    for task_id, (stdout_tail, _axis, _family) in cases.items():
        write_result(
            root,
            task_id,
            {
                "status": "DONE",
                "dual_result": {
                    "status": "FAIL_EVAS",
                    "evas": {"status": "FAIL_SIM_CORRECTNESS"},
                    "spectre": {
                        "status": "error",
                        "ok": False,
                        "errors": ["spectre_failed rc=2"],
                        "stdout_tail": stdout_tail,
                    },
                },
                "classification": {
                    "evas_status": "FAIL_SIM_CORRECTNESS",
                    "spectre_checker_pass": False,
                    "dual_status": "FAIL_EVAS",
                },
            },
        )

    report = triage.build_report([root])
    rows = {row["task_id"]: row for row in report["rows"]}

    for task_id, (_stdout_tail, axis, family) in cases.items():
        assert rows[task_id]["triage_axis"] == axis
        assert rows[task_id]["root_cause_family"] == family
        assert "backend" not in rows[task_id]["triage_axis"]


def test_missing_tran_csv_is_separated_from_compile_failures(tmp_path: Path) -> None:
    root = tmp_path / "dual"
    write_result(
        root,
        "row_missing_waveform",
        {
            "status": "DONE",
            "dual_result": {
                "status": "FAIL_EVAS",
                "evas": {"status": "FAIL_DUT_COMPILE", "stdout_tail": "tran.csv missing"},
                "spectre": {"status": "success", "ok": False, "behavior_score": 0.0},
            },
            "classification": {
                "evas_status": "FAIL_DUT_COMPILE",
                "spectre_checker_pass": False,
                "dual_status": "FAIL_EVAS",
            },
        },
    )

    report = triage.build_report([root])
    row = report["rows"][0]

    assert row["triage_axis"] == "simulation_output_missing"
    assert row["root_cause_family"] == "simulation_output_missing_after_run"
