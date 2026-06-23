# vaBench Release Artifact Index

Date: 2026-06-23

This index maps the release package artifacts to their role in the
paper-facing claim surface. It is a navigation layer, not new
certification evidence.

## Summary

| Metric | Value |
| --- | ---: |
| status | `in_progress` |
| artifacts | 29 |
| missing artifacts | 0 |

## Artifacts

| ID | Status | Claim role | Certification evidence | Path |
| --- | --- | --- | --- | --- |
| `release_tracker` | `ready` | `coverage_plan` | `False` | `docs/VABENCH_RELEASE_TRACKER.csv` |
| `release_package_root` | `ready` | `release_structure` | `False` | `benchmark-vabench-release-v1` |
| `release_package_readme` | `ready` | `reproducibility` | `False` | `benchmark-vabench-release-v1/README.md` |
| `release_package_manifest` | `in_progress` | `reproducibility` | `False` | `benchmark-vabench-release-v1/MANIFEST.json` |
| `release_evaluator_contract` | `ready` | `reproducibility` | `False` | `benchmark-vabench-release-v1/EVALUATOR.json` |
| `release_schemas` | `ready` | `reproducibility` | `False` | `schemas/vabench-release-entry.schema.json` |
| `release_task_manifest_sync` | `pass` | `reproducibility` | `False` | `benchmark-vabench-release-v1/reports/release_task_manifest_sync.json` |
| `schema_validation` | `pass` | `reproducibility` | `False` | `benchmark-vabench-release-v1/reports/schema_validation.json` |
| `asset_integrity` | `pass` | `source_materialization` | `False` | `benchmark-vabench-release-v1/reports/asset_integrity.json` |
| `static_certification` | `pass` | `static_quality` | `True` | `benchmark-vabench-release-v1/reports/static_certification.json` |
| `dual_certification` | `pass` | `parity` | `True` | `benchmark-vabench-release-v1/reports/dual_certification.json` |
| `certification_matrix` | `complete` | `parity_audit` | `False` | `benchmark-vabench-release-v1/reports/certification_matrix.json` |
| `l0_conformance_manifest` | `ready` | `evaluator_health` | `False` | `benchmark-vabench-release-v1/reports/conformance_manifest.json` |
| `dual_rerun_queue` | `complete` | `rerun_plan` | `False` | `benchmark-vabench-release-v1/reports/dual_rerun_queue.json` |
| `dual_rerun_staging` | `complete` | `rerun_plan` | `False` | `benchmark-vabench-release-v1/reports/dual_rerun_staging_manifest.json` |
| `dual_rerun_import` | `imported` | `certification_import_gate` | `False` | `benchmark-vabench-release-v1/reports/dual_rerun_import.json` |
| `bridge_profile_diagnostics` | `ready` | `external_blocker` | `False` | `benchmark-vabench-release-v1/reports/bridge_profile_diagnostics.json` |
| `external_blockers` | `pending` | `external_blocker` | `False` | `benchmark-vabench-release-v1/reports/external_blockers.json` |
| `finish_readiness` | `ready_to_finish` | `recovery_path` | `False` | `benchmark-vabench-release-v1/reports/finish_readiness.json` |
| `finish_after_bridge_attempt` | `dry_run` | `recovery_path` | `False` | `benchmark-vabench-release-v1/reports/finish_after_bridge_attempt.json` |
| `speed_debug_artifact` | `measured_subset` | `speed_debug` | `False` | `benchmark-vabench-release-v1/reports/speed_debug_artifact.json` |
| `baseline_artifact` | `ready_for_baseline_runs` | `baseline` | `False` | `benchmark-vabench-release-v1/reports/baseline_artifact.json` |
| `score_denominator_enablement` | `enabled` | `scoring_denominator` | `False` | `benchmark-vabench-release-v1/reports/score_denominator_enablement.json` |
| `score_denominator_manifest` | `score_enabled` | `scoring_denominator` | `False` | `benchmark-vabench-release-v1/reports/score_denominator_manifest.json` |
| `paper_artifacts` | `in_progress` | `paper_claims` | `False` | `benchmark-vabench-release-v1/reports/paper_artifacts.json` |
| `claim_gate` | `in_progress` | `paper_claims` | `False` | `benchmark-vabench-release-v1/reports/claim_gate.json` |
| `paper_tables` | `in_progress` | `paper_claims` | `False` | `benchmark-vabench-release-v1/reports/paper_tables.json` |
| `completion_audit` | `in_progress` | `completion_gate` | `False` | `benchmark-vabench-release-v1/reports/completion_audit.json` |
| `checksum_manifest` | `pass` | `reproducibility` | `False` | `benchmark-vabench-release-v1/reports/checksum_manifest.json` |

## Commands

| ID | Command |
| --- | --- |
| `refresh_release_package` | `python3 runners/run_vabench_release_longrun.py` |
| `finish_after_bridge` | `python3 runners/finish_vabench_release_after_bridge.py` |
| `external_blockers` | `python3 runners/report_vabench_release_external_blockers.py` |
| `finish_readiness` | `python3 runners/report_vabench_release_finish_readiness.py` |
| `certification_matrix` | `python3 runners/report_vabench_release_certification_matrix.py` |
| `claim_gate` | `python3 runners/report_vabench_release_claim_gate.py` |
| `package_manifest` | `python3 runners/report_vabench_release_package_manifest.py` |
| `evaluator_contract` | `python3 runners/report_vabench_release_evaluator_contract.py` |
| `score_denominator_enablement` | `python3 runners/enable_vabench_release_score_denominator.py` |
| `paper_tables` | `python3 runners/report_vabench_release_paper_tables.py` |
| `primary_dual_rerun` | `./scripts/run_with_bridge.sh python3 runners/run_vabench_release_dual_rerun.py --output-root results/vabench-release-v1-dual-rerun --timeout-s 180` |
