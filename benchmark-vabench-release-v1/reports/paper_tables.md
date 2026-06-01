# vaBench Release Paper Tables

Date: 2026-06-01

These tables are generated from the release reports and claim gate. They
are designed for paper drafting without turning pending evidence into
claims.

## Table Inventory

| ID | Rows | CSV | Caption |
| --- | ---: | --- | --- |
| `coverage` | 9 | `benchmark-vabench-release-v1/reports/paper_tables/coverage.csv` | Coverage/materialization status for the 79-entry L1/L2 release target, split into core circuit coverage and measurement/stimulus support; score denominator claims are governed by the score denominator manifest. |
| `parity` | 9 | `benchmark-vabench-release-v1/reports/paper_tables/parity.csv` | EVAS/Spectre parity status for certified release forms; score, speed/debug, and model baselines are separate gates. |
| `claim_gate` | 9 | `benchmark-vabench-release-v1/reports/paper_tables/claim_gate.csv` | Use only safe_wording for allowed claims; blocked claims must not be used as conclusions. |
| `external_blockers` | 1 | `benchmark-vabench-release-v1/reports/paper_tables/external_blockers.csv` | External blockers explain unavailable fresh Spectre evidence; they are not certification evidence. |
| `speed_baseline` | 3 | `benchmark-vabench-release-v1/reports/paper_tables/speed_baseline.csv` | Speed/debug remains blocked until same-slice timing covers the scored denominator; model baselines are claimable only when same-protocol final-judge reports match the fixed score denominator and expose hygiene slices. |

## Coverage

| metric | value | scope | claim_status |
| --- | --- | --- | --- |
| planned_l1_l2_entries | 79 | coverage target | allowed |
| core_circuit_entries | 66 | core coverage target | allowed |
| support_measurement_stimulus_entries | 13 | support coverage target | allowed |
| l1_entries | 62 | coverage target | allowed |
| l2_entries | 17 | coverage target | allowed |
| source_linked_entries | 79 | source package | allowed |
| asset_materialized_entries | 79 | source package | allowed |
| static_certified_forms | 271 | static checks | allowed |
| scored_entries | 66 | score denominator | allowed |

## Parity

| metric | value | scope | claim_status |
| --- | --- | --- | --- |
| dual_certified_release_forms | 271 | full certified release | allowed |
| fully_certified_entries | 79 | full certified release | allowed |
| evas_pass_spectre_fail_count | 0 | full certified release | allowed |
| dual_pending_release_forms | 0 | fresh full-release rerun | allowed |
| fresh_rerun_queue_rows | 54 | fresh full-release rerun | allowed |
| ready_rerun_bundles | 65 | fresh full-release rerun | allowed |
| bridge_status | ready | external bridge diagnostics | allowed |
| main120_gold_evas_pass | 0/0 | historical supporting evidence | supporting_only |
| main120_gold_spectre_pass | 0/0 | historical supporting evidence | supporting_only |

## Claims

| claim_id | status | completion_required | safe_wording |
| --- | --- | --- | --- |
| C1_coverage_target_defined | allowed | True | The current release package defines 79 planned L1/L2 entries; this is a coverage target, not a final scored benchmark result. |
| C2_source_assets_static_clean | allowed | True | The release has 79 materialized entries for the 79-entry plan and 271 static-certified forms with zero asset issues. |
| C3_imported_dual_subset_clean | allowed | False | On the full imported release evidence (271 forms), EVAS PASS / Spectre FAIL count is 0. |
| C4_full_release_dual_certified | allowed | True | The full release package has EVAS/Spectre certification for 271 forms with zero dual failures and zero EVAS PASS / Spectre FAIL mismatches. |
| C5_score_denominator_enabled | allowed | True | The release benchmark score denominator is enabled for 66 certified content-denominator entries and 236 forms. |
| C6_speed_debug_claim | blocked | True | Speed/debug has subset timing evidence, but release-wide speedup remains blocked until the dedicated artifact marks the speed claim allowed. |
| C7_model_baseline_claim | allowed | True | Same-protocol fixed-budget model baselines are claimable on the 236 scored core forms with Spectre as final judge: mimo-v2.5 92/236 (38.98%); mimo-v2.5-pro 112/236 (47.46%). Report form/category/difficulty and failure-axis slices alongside the headline full_strict score. |
| C8_l0_conformance_separate | allowed | True | L0 conformance has 4 cases and contributes 0 entries to benchmark coverage. |
| C9_release_package_complete | allowed | True | The clean vaBench release package structure, source assets, EVAS/Spectre certification, and score denominator are complete; speed/debug and model baselines remain separate gated claims. |

## External Blockers

| blocker_id | status | scope | stop_condition |
| --- | --- | --- | --- |
| B4_downstream_paper_claims_disabled | pending | speed/debug artifacts | paper_artifacts claim gates allow scored benchmark, speedup, and baseline claims only after their dedicated artifacts support them. |

## Speed / Baseline

| artifact | status | claim_allowed | claim_status |
| --- | --- | --- | --- |
| speed_debug | pending_measurement | False | blocked |
| baseline | claim_ready | True | allowed |
| score_denominator | score_enabled | True | allowed |

## Claim Boundary

- These tables are presentation artifacts; they do not create new certification evidence.
- Parity rows must be captioned according to whether they cover the full release or only an imported subset.
- Rows with blocked claim_status must not be used as paper conclusions.
- Allowed model-baseline rows still require full_strict headline scores plus form/category/difficulty and failure-axis slices.
