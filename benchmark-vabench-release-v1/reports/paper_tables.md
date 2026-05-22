# vaBench Release Paper Tables

Date: 2026-05-19

These tables are generated from the release reports and claim gate. They
are designed for paper drafting without turning pending evidence into
claims.

## Table Inventory

| ID | Rows | CSV | Caption |
| --- | ---: | --- | --- |
| `coverage` | 7 | `benchmark-vabench-release-v1/reports/paper_tables/coverage.csv` | Coverage/materialization status for the 75-entry L1/L2 release target; score denominator claims remain disabled while certification is pending. |
| `parity` | 9 | `benchmark-vabench-release-v1/reports/paper_tables/parity.csv` | EVAS/Spectre parity status for certified release forms; score, speed/debug, and model baselines are separate gates. |
| `claim_gate` | 9 | `benchmark-vabench-release-v1/reports/paper_tables/claim_gate.csv` | Use only safe_wording for allowed claims; blocked claims must not be used as conclusions. |
| `external_blockers` | 1 | `benchmark-vabench-release-v1/reports/paper_tables/external_blockers.csv` | External blockers explain unavailable fresh Spectre evidence; they are not certification evidence. |
| `speed_baseline` | 3 | `benchmark-vabench-release-v1/reports/paper_tables/speed_baseline.csv` | Speed/debug and baseline results are pending until the score denominator is enabled and same-slice evidence exists. |

## Coverage

| metric | value | scope | claim_status |
| --- | --- | --- | --- |
| planned_l1_l2_entries | 75 | coverage target | allowed |
| l1_entries | 60 | coverage target | allowed |
| l2_entries | 15 | coverage target | allowed |
| source_linked_entries | 75 | source package | allowed |
| asset_materialized_entries | 75 | source package | allowed |
| static_certified_forms | 259 | static checks | allowed |
| scored_entries | 74 | score denominator | allowed |

## Parity

| metric | value | scope | claim_status |
| --- | --- | --- | --- |
| dual_certified_release_forms | 259 | full certified release | allowed |
| fully_certified_entries | 75 | full certified release | allowed |
| evas_pass_spectre_fail_count | 0 | full certified release | allowed |
| dual_pending_release_forms | 0 | fresh full-release rerun | allowed |
| fresh_rerun_queue_rows | 0 | fresh full-release rerun | allowed |
| ready_rerun_bundles | 0 | fresh full-release rerun | allowed |
| bridge_status | ready | external bridge diagnostics | allowed |
| main120_gold_evas_pass | 120/120 | historical supporting evidence | supporting_only |
| main120_gold_spectre_pass | 120/120 | historical supporting evidence | supporting_only |

## Claims

| claim_id | status | completion_required | safe_wording |
| --- | --- | --- | --- |
| C1_coverage_target_defined | allowed | True | The current release package defines 75 planned L1/L2 entries; this is a coverage target, not a final scored benchmark result. |
| C2_source_assets_static_clean | allowed | True | The release has 75/75 materialized entries and 259 static-certified forms with zero asset issues. |
| C3_imported_dual_subset_clean | allowed | False | On the full imported release evidence (259 forms), EVAS PASS / Spectre FAIL count is 0. |
| C4_full_release_dual_certified | allowed | True | The full release package has EVAS/Spectre certification for 259 forms with zero dual failures and zero EVAS PASS / Spectre FAIL mismatches. |
| C5_score_denominator_enabled | allowed | True | The release benchmark score denominator is enabled for 74 certified content-denominator entries and 255 forms. |
| C6_speed_debug_claim | blocked | True | Speed/debug has subset timing evidence, but release-wide speedup remains blocked until the dedicated artifact marks the speed claim allowed. |
| C7_model_baseline_claim | blocked | True | Model baseline reporting is pending until baseline runs report against the enabled score denominator. |
| C8_l0_conformance_separate | allowed | True | L0 conformance has 4 cases and contributes 0 entries to benchmark coverage. |
| C9_release_package_complete | allowed | True | The clean vaBench release package structure, source assets, EVAS/Spectre certification, and score denominator are complete; speed/debug and model baselines remain separate gated claims. |

## External Blockers

| blocker_id | status | scope | stop_condition |
| --- | --- | --- | --- |
| B4_downstream_paper_claims_disabled | pending | speed/debug, model baseline artifacts | paper_artifacts claim gates allow scored benchmark, speedup, and baseline claims only after their dedicated artifacts support them. |

## Speed / Baseline

| artifact | status | claim_allowed | claim_status |
| --- | --- | --- | --- |
| speed_debug | measured_subset | False | blocked |
| baseline | ready_for_baseline_runs | False | blocked |
| score_denominator | score_enabled | True | allowed |

## Claim Boundary

- These tables are presentation artifacts; they do not create new certification evidence.
- Parity rows must be captioned according to whether they cover the full release or only an imported subset.
- Rows with blocked claim_status must not be used as paper conclusions.
