from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "operations"
    / "tri_form_derivation_prep"
    / "run_v4_profile_parity_smoke.py"
)
SPEC = importlib.util.spec_from_file_location("run_v4_profile_parity_smoke", MODULE_PATH)
assert SPEC and SPEC.loader
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


def test_profile_evidence_uses_evas_083_rust_runtime() -> None:
    assert runner.REQUIRED_EVAS_VERSION == "0.8.3"
    assert runner.REQUIRED_EVAS_ENGINE == "evas2"
    assert runner.RUST_EVAS_LOG_ENGINE == "evas-rust"


def test_profile_evidence_labels_are_revision_scoped() -> None:
    assert runner.release_label("r44") == "release/benchmarkv4"
    assert runner.release_label("r45") == "release/benchmarkv4-r45"


def test_profile_cli_writes_selected_release_revision(tmp_path: Path, monkeypatch) -> None:
    output = tmp_path / "PROFILE_PARITY.json"
    monkeypatch.setattr(runner, "require_evas2_environment", lambda: None)
    monkeypatch.setattr(
        runner,
        "probe_evas2_runtime",
        lambda: {
            "evas_engine": "evas2",
            "evas_engine_used": "evas2",
            "evas_version": "0.8.3",
            "evas_backend": "evas-rust",
        },
    )
    monkeypatch.setattr(runner, "release_rows", lambda release, task_ids, family_range: [])
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "run_v4_profile_parity_smoke.py",
            "--release",
            str(tmp_path / "staged-release"),
            "--release-revision",
            "r45",
            "--output",
            str(output),
        ],
    )

    assert runner.main() == 0
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["release"] == "release/benchmarkv4-r45"
    assert payload["release_revision"] == "r45"
    assert payload["evas_version"] == "0.8.3"
