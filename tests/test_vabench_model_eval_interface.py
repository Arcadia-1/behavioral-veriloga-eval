from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runners"))

from run_vabench_model_eval import main, parse_args, selected_rows  # noqa: E402


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_unified_model_eval_selects_default_model_roster() -> None:
    args = parse_args(["--list", "--limit", "3"])
    rows = selected_rows(args)

    assert len(rows) == 3
    assert all(row["counted_in_score"] is True for row in rows)
    assert {row["provenance"] for row in rows} <= {"inherited_v1"}


def test_unified_model_eval_command_preview_writes_redacted_summary(tmp_path: Path) -> None:
    output_root = tmp_path / "preview"
    rc = main(
        [
            "--model",
            "preview-model",
            "--base-url",
            "http://127.0.0.1/v1",
            "--limit",
            "1",
            "--output-root",
            str(output_root),
            "--final-judge",
            "spectre",
            "--print-commands",
            "--api-key-file",
            "/private/tmp/example-api-key",
            "--extra-body-json",
            '{"metadata":"example"}',
            "--proxy-url",
            "http://user:pass@127.0.0.1:7890",
        ]
    )

    assert rc == 0
    summary = read_json(output_root / "summary.json")
    assert summary["status"] == "command_preview"
    assert summary["selected_scored_rows"] == 1
    assert summary["score_roster"].endswith("benchmark-vabench-release-v1/reports/model_eval_roster.json")
    assert [item["stage"] for item in summary["commands"]] == ["generation_evas", "spectre_final"]
    assert all("/private/tmp/example-api-key" not in item["command"] for item in summary["commands"])
    assert all("user:pass" not in item["command"] for item in summary["commands"])
    assert any("<redacted>" in item["command"] for item in summary["commands"])


def test_unified_model_eval_dry_run_generates_summary(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("PYTHONPYCACHEPREFIX", "/private/tmp/vabench_pycache")
    output_root = tmp_path / "dry-run"
    rc = main(
        [
            "--model",
            "dry-run-model",
            "--base-url",
            "http://127.0.0.1/v1",
            "--limit",
            "1",
            "--output-root",
            str(output_root),
            "--dry-run",
            "--final-judge",
            "spectre",
        ]
    )

    assert rc == 0
    summary = read_json(output_root / "summary.json")
    generation_summary = read_json(output_root / "generation_evas" / "summary.json")

    assert summary["status"] == "complete_dry_run"
    assert summary["selected_scored_rows"] == 1
    assert summary["generation_evas"]["status"] == "completed"
    assert summary["spectre_final"]["status"] == "skipped"
    assert summary["spectre_final"]["skipped_reason"] == "dry_run"
    assert summary["claim_allowed"] is False
    assert generation_summary["dry_run"] is True
    assert generation_summary["score_roster"].endswith("benchmark-vabench-release-v1/reports/model_eval_roster.json")
