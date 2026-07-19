from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest


MODULE_DIR = (
    Path(__file__).resolve().parents[2]
    / "operations"
    / "tri_form_derivation_prep"
)
sys.path.insert(0, str(MODULE_DIR))
SPEC = importlib.util.spec_from_file_location(
    "refresh_rust_evas2_certifications",
    MODULE_DIR / "refresh_rust_evas2_certifications.py",
)
assert SPEC and SPEC.loader
refresh = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(refresh)


def family_row(family: str) -> dict:
    return {
        "canonical_dut_id": family,
        "release_dir": f"{family}-synthetic",
        "active_mutations": [
            {"mutation_id": f"mutation_{index:02d}"}
            for index in range(1, 6)
        ],
    }


def family_cases(family: str) -> dict[str, dict]:
    cases = {
        "gold": {
            "family_id": family,
            "case_id": "gold",
            "mutation_id": None,
            "checker_id": f"v4-{family}",
            "status": "pass",
            "checker_pass": True,
            "timing_invariant": True,
            "diagnostics_complete": True,
            "insufficient_excitation_rejected": True,
            "trace_row_count": 10,
        }
    }
    for index in range(1, 6):
        mutation_id = f"mutation_{index:02d}"
        cases[mutation_id] = {
            "family_id": family,
            "case_id": mutation_id,
            "mutation_id": mutation_id,
            "checker_id": f"v4-{family}",
            "status": "pass",
            "checker_pass": False,
            "timing_invariant": True,
            "diagnostics_complete": True,
            "insufficient_excitation_rejected": None,
            "trace_row_count": 10,
        }
    return cases


@pytest.mark.parametrize("release_revision", ["r45", "r47"])
def test_evidence_only_refresh_does_not_rewrite_source(
    tmp_path: Path,
    monkeypatch,
    release_revision: str,
) -> None:
    families = [f"{value:03d}" for value in range(1, 401)]
    report = tmp_path / "full400.json"
    report.write_text("{}\n", encoding="utf-8")
    output = tmp_path / "RUST_EVAS2_CERTIFICATION.json"
    monkeypatch.setattr(
        refresh,
        "load_family_rows",
        lambda source: [family_row(family) for family in families],
    )
    monkeypatch.setattr(
        refresh,
        "score_denominator_registry_sha256",
        lambda source: "a" * 64,
    )
    monkeypatch.setattr(
        refresh,
        "report_cases",
        lambda paths: (
            {family: family_cases(family) for family in families},
            {
                "evas_engine": "evas2",
                "evas_version": "0.8.3",
                "evas_backend": "evas-rust",
            },
        ),
    )

    def unexpected_source_write(*args, **kwargs):
        raise AssertionError("evidence-only refresh attempted to rewrite source")

    monkeypatch.setattr(refresh, "refresh_task_record", unexpected_source_write)
    monkeypatch.setattr(refresh, "update_registry_row", unexpected_source_write)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "refresh_rust_evas2_certifications.py",
            "--source",
            str(tmp_path / "source"),
            "--report",
            str(report),
            "--output",
            str(output),
            "--release-revision",
            release_revision,
        ],
    )

    assert refresh.main() == 0
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["schema_version"] == (
        f"v4-{release_revision}-rust-evas2-certification-report-v1"
    )
    assert payload["release_candidate"] == release_revision
    assert payload["source_score_denominator_registry_sha256"] == "a" * 64
    assert payload["source_certifications_updated"] is False
    assert payload["runtime"]["evas_version"] == "0.8.3"
    assert payload["summary"] == {
        "family_count": 400,
        "gold_pass_count": 400,
        "negative_case_count": 2000,
        "mutation_kill_count": 2000,
        "trace_axis_invariant_count": 2400,
        "insufficient_excitation_rejection_count": 400,
        "insufficient_excitation_not_applicable_count": 0,
        "diagnostic_present_count": 2400,
    }
    assert len(payload["cases"]) == 2400
