from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "benchmark-vabench-release-v1" / "README.md"


def test_package_readme_documents_claim_boundaries_and_entry_reports() -> None:
    text = README.read_text(encoding="utf-8")

    assert "79-entry L1/L2" in text
    assert "vaBench release target" in text
    assert "not part of the scored benchmark" in text
    assert "reports/claim_gate.json" in text
    assert "reports/paper_tables.json" in text
    assert "reports/score_denominator_manifest.json" in text
    assert "reports/external_blockers.json" in text
    assert "reports/finish_readiness.json" in text
    assert "MANIFEST.json" in text
    assert "EVALUATOR.json" in text
    assert "Do not claim EVAS speedup" in text


def test_package_readme_documents_reproducible_commands_and_bridge_gate() -> None:
    text = README.read_text(encoding="utf-8")

    assert "python3 runners/run_vabench_release_longrun.py" in text
    assert "python3 runners/finish_vabench_release_after_bridge.py" in text
    assert "./scripts/run_with_bridge.sh python3 runners/run_vabench_release_dual_rerun.py" in text
    assert "Blocked or dry-run summaries must not be imported as certification evidence" in text
    assert "reports/bridge_profile_diagnostics.json" in text
    assert "before importing any fresh rerun summary" in text
