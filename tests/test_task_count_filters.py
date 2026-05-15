from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runners"))

import generate  # noqa: E402
import run_gold_suite  # noqa: E402
import score  # noqa: E402


def _write_task(root: Path, task_id: str, meta: dict, *, prompt: bool = True, gold: bool = True) -> Path:
    task_dir = root / "tasks" / "spec-to-va" / "voltage" / task_id
    task_dir.mkdir(parents=True)
    (task_dir / "meta.json").write_text(json.dumps({"id": task_id, **meta}), encoding="utf-8")
    if prompt:
        (task_dir / "prompt.md").write_text(f"# {task_id}\n", encoding="utf-8")
    if gold:
        gold_dir = task_dir / "gold"
        gold_dir.mkdir()
        (gold_dir / f"{task_id}.va").write_text(f"module {task_id}; endmodule\n", encoding="utf-8")
        (gold_dir / f"tb_{task_id}_ref.scs").write_text(
            f'ahdl_include "{task_id}.va"\ntran tran stop=1n\n',
            encoding="utf-8",
        )
    return task_dir


def _base_meta(**updates: object) -> dict:
    meta = {
        "family": "spec-to-va",
        "category": "demo",
        "domain": "voltage",
        "difficulty": "easy",
        "expected_backend": "evas",
        "scoring": ["dut_compile", "tb_compile", "sim_correct"],
    }
    meta.update(updates)
    return meta


def _evidence_only_meta() -> dict:
    return _base_meta(
        release_form="evidence-only",
        counts={"model_capability": False, "benchmark_coverage": False, "bugfix_claim": False},
    )


def test_generate_and_score_skip_evidence_only_by_default(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _write_task(tmp_path, "normal_task", _base_meta())
    _write_task(tmp_path, "evidence_only_task", _evidence_only_meta())
    monkeypatch.setattr(generate, "ROOT", tmp_path)
    monkeypatch.setattr(score, "ROOT", tmp_path)

    assert generate.list_task_dirs() == [("normal_task", tmp_path / "tasks/spec-to-va/voltage/normal_task")]
    assert score.list_all_task_dirs() == [("normal_task", tmp_path / "tasks/spec-to-va/voltage/normal_task")]

    with pytest.raises(ValueError, match="excluded from model-capability generation"):
        generate.list_task_dirs(selected={"evidence_only_task"})
    with pytest.raises(ValueError, match="excluded from model-capability scoring"):
        score.list_all_task_dirs(selected={"evidence_only_task"})


def test_gold_suite_skips_evidence_only_by_default(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    _write_task(tmp_path, "normal_task", _base_meta())
    _write_task(tmp_path, "evidence_only_task", _evidence_only_meta())
    monkeypatch.setattr(run_gold_suite, "benchmark_root", lambda: tmp_path)

    assert run_gold_suite.list_gold_task_dirs(families=("spec-to-va",)) == [
        tmp_path / "tasks/spec-to-va/voltage/normal_task"
    ]

    with pytest.raises(ValueError, match="excluded from benchmark-coverage gold-suite counts"):
        run_gold_suite.list_gold_task_dirs(selected={"evidence_only_task"}, families=("spec-to-va",))
