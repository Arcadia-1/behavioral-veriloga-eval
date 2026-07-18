from __future__ import annotations

import ast
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "benchmark-vabench-release-v4"
ACTIVE_ENTRYPOINTS = (
    PACKAGE
    / "operations"
    / "tri_form_derivation_prep"
    / "export_tri_form_runtime.py",
    PACKAGE / "runners" / "run_benchmarkv4_campaign.py",
    PACKAGE / "operations" / "calibration_pilot" / "build_campaign.py",
    PACKAGE / "operations" / "calibration_pilot" / "run_campaign.py",
    PACKAGE
    / "operations"
    / "tri_form_derivation_prep"
    / "run_v4_reference_evas_smoke.py",
    PACKAGE
    / "operations"
    / "tri_form_derivation_prep"
    / "audit_tri_form_reference_spectre.py",
    PACKAGE
    / "operations"
    / "tri_form_derivation_prep"
    / "run_v4_profile_parity_smoke.py",
)


def default_release_literals(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(
            isinstance(target, ast.Name) and target.id == "DEFAULT_RELEASE"
            for target in node.targets
        ):
            continue
        literals = [
            child.value
            for child in ast.walk(node.value)
            if isinstance(child, ast.Constant) and isinstance(child.value, str)
        ]
        if literals:
            return set(literals)
    raise AssertionError(f"DEFAULT_RELEASE not found in {path}")


@pytest.mark.parametrize("entrypoint", ACTIVE_ENTRYPOINTS, ids=lambda path: path.name)
def test_active_benchmark_entrypoint_defaults_to_r46(entrypoint: Path) -> None:
    literals = default_release_literals(entrypoint)
    assert "benchmarkv4-r46" in literals
    assert "benchmarkv4-r45" not in literals


def test_operator_docs_name_r46_as_the_active_default() -> None:
    documents = (
        ROOT / "docs" / "REPO_LAYOUT_POLICY.md",
        PACKAGE / "runners" / "README.md",
        PACKAGE / "operations" / "calibration_pilot" / "README.md",
        PACKAGE / "operations" / "tri_form_derivation_prep" / "README.md",
    )
    for document in documents:
        text = document.read_text(encoding="utf-8")
        assert "benchmarkv4-r46" in text, document


def test_active_metamorphic_evidence_defaults_to_r46() -> None:
    path = PACKAGE / "scripts" / "run_v4_stimulus_metamorphic.py"
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    defaults = {
        target.id: node.value.value
        for node in tree.body
        if isinstance(node, ast.Assign)
        and isinstance(node.value, ast.Constant)
        and isinstance(node.value.value, str)
        for target in node.targets
        if isinstance(target, ast.Name)
    }
    assert defaults["DEFAULT_RELEASE_REVISION"] == "r46"
