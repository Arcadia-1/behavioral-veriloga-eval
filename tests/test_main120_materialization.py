from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runners"))

import materialize_main120_inventory as inv  # noqa: E402


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def write_result(root: Path, task_id: str, backend: str) -> None:
    write_json(
        root / task_id / f"{backend}_result.json",
        {
            "task_id": task_id,
            "backend": backend,
            "status": "PASS",
            "scores": {"weighted_total": 1.0},
        },
    )


def test_parse_task_id_maps_forms_to_task_families() -> None:
    parsed = inv.parse_task_id("vbm1_cdac_calibration_dut")

    assert parsed.base == "cdac_calibration"
    assert parsed.form == "dut"
    assert parsed.family == "spec-to-va"
    assert parsed.category_hint == "dac"


def test_build_rows_treats_main120_as_result_asset_not_current_task(tmp_path: Path) -> None:
    task_id = "vbm1_file_metric_writer_dut"
    evas_dir = tmp_path / "results" / "evas"
    spectre_dir = tmp_path / "results" / "spectre"
    tasks_root = tmp_path / "tasks"

    write_json(
        evas_dir / "summary.json",
        {"backend": "evas", "evas": {"pass_tasks": [task_id], "axis_rates": {"sim_correct": 1.0}}},
    )
    write_json(
        spectre_dir / "summary.json",
        {
            "backend": "spectre",
            "spectre": {"pass_tasks": [task_id], "axis_rates": {"sim_correct": 1.0}},
        },
    )
    write_result(evas_dir, task_id, "evas")
    write_result(spectre_dir, task_id, "spectre")

    for root in (evas_dir, spectre_dir):
        staged = root / task_id / "staged"
        staged.mkdir(parents=True, exist_ok=True)
        (staged / "file_metric_writer.va").write_text("module file_metric_writer; endmodule\n", encoding="utf-8")
        (staged / "tb_file_metric_writer_ref.scs").write_text("tran tran stop=1n\n", encoding="utf-8")
    (evas_dir / task_id / "staged" / "metric.out").write_text("generated output\n", encoding="utf-8")

    tracked_meta = tasks_root / "spec-to-va" / "voltage" / "file_metric_writer" / "meta.json"
    write_json(
        tracked_meta,
        {
            "id": "file_metric_writer",
            "family": "spec-to-va",
            "category": "measurement",
            "domain": "voltage",
            "difficulty": "medium",
            "expected_backend": "evas",
            "scoring": ["dut_compile", "tb_compile", "sim_correct"],
        },
    )

    rows, stats = inv.build_rows(tmp_path, evas_dir, spectre_dir, tasks_root)

    assert stats["task_rows"] == 1
    assert stats["paired_tasks"] == 1
    assert stats["dual_pass"] == 1
    assert stats["exact_current_overlap"] == 0
    assert stats["needs_source_task"] == 1
    assert stats["staged_source_hash_match"] == 1
    assert rows[0]["exact_current_task"] == "no"
    assert rows[0]["materialization_state"] == "needs_source_task"
    assert rows[0]["staged_source_hash_match"] == "yes"
    assert rows[0]["asset_type"] == "vabench_task"
    assert rows[0]["release_form"] == "normal"
    assert rows[0]["counts_model_capability"] == "true"
    assert rows[0]["counts_bugfix_claim"] == "false"


def test_build_rows_marks_fixed_only_bugfix_as_evidence_only(tmp_path: Path) -> None:
    task_id = "vbm1_cdac_calibration_bugfix"
    evas_dir = tmp_path / "results" / "evas"
    spectre_dir = tmp_path / "results" / "spectre"
    tasks_root = tmp_path / "tasks"

    write_json(
        evas_dir / "summary.json",
        {"backend": "evas", "evas": {"pass_tasks": [task_id], "axis_rates": {"sim_correct": 1.0}}},
    )
    write_json(
        spectre_dir / "summary.json",
        {
            "backend": "spectre",
            "spectre": {"pass_tasks": [task_id], "axis_rates": {"sim_correct": 1.0}},
        },
    )
    write_result(evas_dir, task_id, "evas")
    write_result(spectre_dir, task_id, "spectre")

    for root in (evas_dir, spectre_dir):
        staged = root / task_id / "staged"
        staged.mkdir(parents=True, exist_ok=True)
        (staged / "cdac_calibration.va").write_text("module cdac_calibration; endmodule\n", encoding="utf-8")
        (staged / "tb_cdac_calibration_ref.scs").write_text("tran tran stop=1n\n", encoding="utf-8")

    rows, stats = inv.build_rows(tmp_path, evas_dir, spectre_dir, tasks_root)

    assert rows[0]["release_form"] == "evidence-only"
    assert rows[0]["provenance_status"] == "historical_bugfix_fixed_only"
    assert rows[0]["counts_model_capability"] == "false"
    assert rows[0]["counts_benchmark_coverage"] == "false"
    assert rows[0]["counts_bugfix_claim"] == "false"
    assert "missing_buggy_fixed_pair" in rows[0]["promotion_blockers"]
    assert stats["countable_model_capability"] == 0


def test_build_rows_uses_current_task_promotion_contract_for_reconstructed_bugfix(tmp_path: Path) -> None:
    task_id = "vbm1_cdac_calibration_bugfix"
    evas_dir = tmp_path / "results" / "evas"
    spectre_dir = tmp_path / "results" / "spectre"
    tasks_root = tmp_path / "tasks"

    write_json(
        evas_dir / "summary.json",
        {"backend": "evas", "evas": {"pass_tasks": [task_id], "axis_rates": {"sim_correct": 1.0}}},
    )
    write_json(
        spectre_dir / "summary.json",
        {
            "backend": "spectre",
            "spectre": {"pass_tasks": [task_id], "axis_rates": {"sim_correct": 1.0}},
        },
    )
    write_result(evas_dir, task_id, "evas")
    write_result(spectre_dir, task_id, "spectre")

    for root in (evas_dir, spectre_dir):
        staged = root / task_id / "staged"
        staged.mkdir(parents=True, exist_ok=True)
        (staged / "cdac_calibration.va").write_text("module cdac_calibration; endmodule\n", encoding="utf-8")
        (staged / "tb_cdac_calibration_ref.scs").write_text("tran tran stop=1n\n", encoding="utf-8")

    write_json(
        tasks_root / "bugfix" / "voltage" / "dac" / task_id / "meta.json",
        {
            "id": task_id,
            "family": "bugfix",
            "category": "dac",
            "domain": "voltage",
            "difficulty": "easy",
            "expected_backend": "evas",
            "scoring": ["dut_compile", "tb_compile", "sim_correct"],
            "asset_type": "vabench_task",
            "benchmark_split": "vabench-main-v1",
            "release_form": "true-bugfix",
            "provenance_status": "reconstructed_badcase",
            "badcase_origin": "reconstructed",
            "source_main120_id": task_id,
            "counts": {"model_capability": True, "benchmark_coverage": True, "bugfix_claim": True},
        },
    )

    rows, stats = inv.build_rows(tmp_path, evas_dir, spectre_dir, tasks_root)

    assert rows[0]["exact_current_task"] == "yes"
    assert rows[0]["release_form"] == "true-bugfix"
    assert rows[0]["provenance_status"] == "reconstructed_badcase"
    assert rows[0]["badcase_origin"] == "reconstructed"
    assert rows[0]["counts_model_capability"] == "true"
    assert rows[0]["counts_bugfix_claim"] == "true"
    assert stats["countable_model_capability"] == 1
    assert stats["countable_bugfix_claim"] == 1
