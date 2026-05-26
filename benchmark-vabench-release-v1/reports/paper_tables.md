# vaBench Release Paper Tables

Date: 2026-05-26

These tables are generated from the release reports and claim gate. They
are designed for paper drafting without turning pending evidence into
claims.

## Table Inventory

| ID | Rows | CSV | Caption |
| --- | ---: | --- | --- |
| `coverage` | 9 | `benchmark-vabench-release-v1/reports/paper_tables/coverage.csv` | Coverage/materialization status for the 64-entry L1/L2 release target, split into core circuit coverage and measurement/stimulus support; score denominator claims are governed by the score denominator manifest. |
| `parity` | 9 | `benchmark-vabench-release-v1/reports/paper_tables/parity.csv` | EVAS/Spectre parity status for certified release forms; score, speed/debug, and model baselines are separate gates. |
| `claim_gate` | 9 | `benchmark-vabench-release-v1/reports/paper_tables/claim_gate.csv` | Use only safe_wording for allowed claims; blocked claims must not be used as conclusions. |
| `external_blockers` | 2 | `benchmark-vabench-release-v1/reports/paper_tables/external_blockers.csv` | External blockers explain unavailable fresh Spectre evidence; they are not certification evidence. |
| `speed_baseline` | 3 | `benchmark-vabench-release-v1/reports/paper_tables/speed_baseline.csv` | Speed/debug and baseline results are pending until the score denominator is enabled and same-slice evidence exists. |

## Coverage

| metric | value | scope | claim_status |
| --- | --- | --- | --- |
| planned_l1_l2_entries | 64 | coverage target | allowed |
| core_circuit_entries | 51 | core coverage target | allowed |
| support_measurement_stimulus_entries | 13 | support coverage target | allowed |
| l1_entries | 51 | coverage target | allowed |
| l2_entries | 13 | coverage target | allowed |
| source_linked_entries | 64 | source package | allowed |
| asset_materialized_entries | 64 | source package | allowed |
| static_certified_forms | 219 | static checks | allowed |
| scored_entries | 51 | score denominator | allowed |

## Parity

| metric | value | scope | claim_status |
| --- | --- | --- | --- |
| dual_certified_release_forms | 217 | imported certified subset | allowed |
| fully_certified_entries | 63 | imported certified subset | allowed |
| evas_pass_spectre_fail_count | 0 | imported certified subset | allowed |
| dual_pending_release_forms | 2 | fresh full-release rerun | blocked |
| fresh_rerun_queue_rows | 2 | fresh full-release rerun | blocked |
| ready_rerun_bundles | 2 | fresh full-release rerun | blocked |
| bridge_status | ready | external bridge diagnostics | blocked |
| main120_gold_evas_pass | 0/0 | historical supporting evidence | supporting_only |
| main120_gold_spectre_pass | 0/0 | historical supporting evidence | supporting_only |

## Claims

| claim_id | status | completion_required | safe_wording |
| --- | --- | --- | --- |
| C1_coverage_target_defined | allowed | True | The current release package defines 64 planned L1/L2 entries; this is a coverage target, not a final scored benchmark result. |
| C2_source_assets_static_clean | allowed | True | The release has 64 materialized entries for the 64-entry plan and 219 static-certified forms with zero asset issues. |
| C3_imported_dual_subset_clean | allowed | False | On the imported certified subset (217 forms), EVAS PASS / Spectre FAIL count is 0. |
| C4_full_release_dual_certified | blocked | True | This claim is blocked until every release form has current EVAS/Spectre evidence with zero dual failures and zero EVAS PASS / Spectre FAIL mismatches. |
| C5_score_denominator_enabled | allowed | True | The release benchmark score denominator is enabled for 51 certified content-denominator entries and 184 forms. |
| C6_speed_debug_claim | blocked | True | Speed/debug has subset timing evidence, but release-wide speedup remains blocked until the dedicated artifact marks the speed claim allowed. |
| C7_model_baseline_claim | blocked | True | Model baseline reporting is pending until baseline runs report against the enabled score denominator. |
| C8_l0_conformance_separate | allowed | True | L0 conformance has 4 cases and contributes 0 entries to benchmark coverage. |
| C9_release_package_complete | blocked | True | The package structure and source assets are ready, but full completion remains blocked by fresh dual rerun, scoring, speed, and baseline gates. |

## External Blockers

| blocker_id | status | scope | stop_condition |
| --- | --- | --- | --- |
| B2_fresh_dual_rerun_not_complete | ready_to_continue | 2 primary EVAS/Spectre release rows | The active rerun summary has status=complete, zero expected misses, and is imported into dual_certification.json. |
| B4_downstream_paper_claims_disabled | pending | speed/debug, model baseline artifacts | paper_artifacts claim gates allow scored benchmark, speedup, and baseline claims only after their dedicated artifacts support them. |

## Speed / Baseline

| artifact | status | claim_allowed | claim_status |
| --- | --- | --- | --- |
| speed_debug | measured_with_failures | False | blocked |
| baseline | pending_release_baselines | False | blocked |
| score_denominator | score_enabled | True | allowed |

## Claim Boundary

- These tables are presentation artifacts; they do not create new certification evidence.
- Parity rows must be captioned according to whether they cover the full release or only an imported subset.
- Rows with blocked claim_status must not be used as paper conclusions.
