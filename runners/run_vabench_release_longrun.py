#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path

import audit_vabench_content_contract
import audit_vabench_release_assets
import audit_vabench_release_package
import certify_vabench_release_static
import import_vabench_release_dual_evidence
import import_vabench_release_dual_rerun_results
import init_vabench_release_goal
import materialize_vabench_release_designed_sources
import materialize_vabench_release_bugfix_companions
import materialize_vabench_release_selected
import materialize_vabench_release_tb_companions
import prepare_vabench_release_dual_rerun
import report_vabench_release_baseline_artifact
import report_vabench_release_artifact_index
import report_vabench_release_bridge_diagnostics
import report_vabench_release_claim_gate
import report_vabench_release_certification_matrix
import report_vabench_release_checksum_manifest
import report_vabench_release_completion_audit
import report_vabench_release_dual_rerun_queue
import report_vabench_release_evaluator_contract
import report_vabench_release_external_blockers
import report_vabench_release_finish_readiness
import report_vabench_manual_review_queue
import report_vabench_release_paper_artifacts
import report_vabench_release_paper_tables
import report_vabench_release_package_manifest
import report_vabench_release_remaining_work
import report_vabench_release_score_denominator
import report_vabench_release_speed_debug
import seed_vabench_release_package
import sync_vabench_release_conformance
import sync_vabench_release_task_manifests
import report_vabench_release_schema_validation


ROOT = Path(__file__).resolve().parents[1]
TESTS = [
    "tests/test_vabench_release_tracker.py",
    "tests/test_vabench_release_seed_manifest.py",
    "tests/test_vabench_release_asset_integrity.py",
    "tests/test_vabench_release_static_certification.py",
    "tests/test_vabench_release_dual_evidence.py",
    "tests/test_vabench_release_conformance_manifest.py",
    "tests/test_vabench_release_status_report.py",
    "tests/test_vabench_release_remaining_work.py",
    "tests/test_vabench_release_dual_rerun_queue.py",
    "tests/test_vabench_release_dual_rerun_staging.py",
    "tests/test_vabench_release_dual_rerun_import.py",
    "tests/test_vabench_release_score_denominator.py",
    "tests/test_vabench_release_speed_baseline_artifacts.py",
    "tests/test_bridge_wrapper_diagnostics.py",
    "tests/test_vabench_release_bridge_diagnostics.py",
    "tests/test_vabench_release_certification_matrix.py",
    "tests/test_vabench_release_external_blockers.py",
    "tests/test_vabench_release_finish_readiness.py",
    "tests/test_vabench_release_claim_gate.py",
    "tests/test_vabench_release_paper_tables.py",
    "tests/test_vabench_release_package_manifest.py",
    "tests/test_vabench_release_evaluator_contract.py",
    "tests/test_vabench_release_finish_after_bridge.py",
    "tests/test_vabench_release_paper_artifacts.py",
    "tests/test_vabench_release_completion_audit.py",
    "tests/test_vabench_release_artifact_index.py",
    "tests/test_vabench_release_schema_validation.py",
    "tests/test_vabench_release_checksum_manifest.py",
    "tests/test_vabench_release_package_readme.py",
]


@contextmanager
def isolated_argv() -> None:
    old_argv = sys.argv[:]
    sys.argv = [old_argv[0]]
    try:
        yield
    finally:
        sys.argv = old_argv


def run_step(func) -> None:
    with isolated_argv():
        func()


def run_tests() -> None:
    cmd = [sys.executable, "-m", "pytest", *TESTS, "-q"]
    subprocess.run(cmd, cwd=ROOT, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the conservative vaBench release long-run bootstrap.")
    parser.add_argument("--skip-tests", action="store_true", help="Generate artifacts without running pytest.")
    args = parser.parse_args()

    run_step(init_vabench_release_goal.main)
    run_step(seed_vabench_release_package.main)
    run_step(materialize_vabench_release_selected.main)
    run_step(materialize_vabench_release_designed_sources.main)
    run_step(materialize_vabench_release_tb_companions.main)
    run_step(materialize_vabench_release_bugfix_companions.main)
    run_step(sync_vabench_release_conformance.main)
    run_step(audit_vabench_release_assets.main)
    run_step(certify_vabench_release_static.main)
    run_step(import_vabench_release_dual_evidence.main)
    run_step(sync_vabench_release_task_manifests.main)
    run_step(audit_vabench_release_package.main)
    run_step(report_vabench_release_dual_rerun_queue.main)
    run_step(prepare_vabench_release_dual_rerun.main)
    import_vabench_release_dual_rerun_results.main([])
    run_step(sync_vabench_release_task_manifests.main)
    run_step(audit_vabench_release_package.main)
    run_step(report_vabench_release_remaining_work.main)
    run_step(report_vabench_release_certification_matrix.main)
    report_vabench_release_bridge_diagnostics.main([])
    run_step(report_vabench_release_external_blockers.main)
    run_step(report_vabench_release_finish_readiness.main)
    run_step(report_vabench_release_speed_debug.main)
    run_step(report_vabench_release_score_denominator.main)
    run_step(audit_vabench_content_contract.main)
    run_step(report_vabench_manual_review_queue.main)
    run_step(report_vabench_release_baseline_artifact.main)
    run_step(report_vabench_release_paper_artifacts.main)
    run_step(report_vabench_release_external_blockers.main)
    run_step(report_vabench_release_claim_gate.main)
    run_step(report_vabench_release_paper_tables.main)
    run_step(report_vabench_release_package_manifest.main)
    run_step(audit_vabench_content_contract.main)
    run_step(report_vabench_manual_review_queue.main)
    run_step(report_vabench_release_evaluator_contract.main)
    run_step(report_vabench_release_completion_audit.main)
    run_step(report_vabench_release_schema_validation.main)
    run_step(report_vabench_release_completion_audit.main)
    run_step(report_vabench_release_external_blockers.main)
    run_step(report_vabench_release_finish_readiness.main)
    run_step(report_vabench_release_claim_gate.main)
    run_step(report_vabench_release_paper_tables.main)
    run_step(report_vabench_release_package_manifest.main)
    run_step(report_vabench_release_evaluator_contract.main)
    run_step(report_vabench_release_checksum_manifest.main)
    run_step(report_vabench_release_artifact_index.main)
    run_step(report_vabench_release_schema_validation.main)
    run_step(report_vabench_release_completion_audit.main)
    run_step(report_vabench_release_artifact_index.main)
    run_step(report_vabench_release_checksum_manifest.main)
    if not args.skip_tests:
        run_tests()


if __name__ == "__main__":
    main()
