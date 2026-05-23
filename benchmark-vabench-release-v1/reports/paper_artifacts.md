# vaBench Paper-Facing Artifact Summary

Date: 2026-05-23

This is a claim-gated summary for paper writing. It records what can be
cited from the current release package and what must remain pending.

## Coverage

| Metric | Value |
| --- | ---: |
| planned L1/L2 entries | 73 |
| source-linked entries | 73 |
| entries with copied assets | 73 |
| static-certified release forms | 249 |
| dual-certified release forms | 249 |
| fully certified entries | 73 |
| certification matrix | `complete` |
| scored release entries | 73 |
| scored release forms | 245 |
| score denominator status | `score_enabled` |

## Parity

| Metric | Value |
| --- | ---: |
| release dual status | `pass` |
| dual-certified release forms | 249 |
| dual-pending release forms | 0 |
| dual-failed release forms | 0 |
| EVAS PASS / Spectre FAIL count | 0 |
| source-equivalence blocked forms | 0 |
| dual rerun staging status | `complete` |
| rerun rows with ready primary bundle | 0 |
| ready rerun bundles | 0 |
| latest dual rerun attempt | `complete` |
| bridge diagnostics | `ready` |
| bridge ready profiles | `default, ci, jin` |
| main120 EVAS gold pass | 0/0 |
| main120 Spectre gold pass | 0/0 |
| L0 conformance cases | 4 |
| L0 counted in benchmark denominator | 0 |

## Certification Gap

| Gate | Value |
| --- | --- |
| assets materialized | `True` |
| static certification complete | `True` |
| fresh dual rerun queue ready | `True` |
| fresh dual rerun queue rows | 0 |
| ready rerun bundles | 0 |
| dual-pending release forms | 0 |
| bridge ready | `True` |
| external blockers | `pending` |
| external blocked count | 0 |
| external pending count | 1 |
| stale rerun summary rejected | `True` |
| import status | `partial_imported` |

## Speed / Debug

- Status: `measured_subset`
- Claim allowed: `False`
- Reason: Timing exists for a subset only: 17 timed rows cover 17/257 scored forms. Wrapper aggregate Spectre/EVAS speedup is 1.835; do not claim release-wide EVAS speedup yet.

## Baselines

- Status: `ready_for_baseline_runs`
- Claim allowed: `False`
- Reason: Baseline artifact exists but has no claimable baseline summary yet.

## Claim Gates

| Claim | Allowed |
| --- | --- |
| `can_claim_release_assets_materialized` | `True` |
| `can_claim_top_level_coverage_plan` | `False` |
| `can_claim_release_package_complete` | `True` |
| `can_claim_scored_benchmark` | `True` |
| `can_claim_zero_evas_pass_spectre_fail_on_imported_release_evidence` | `True` |
| `can_claim_speedup` | `False` |
| `can_claim_model_baseline` | `False` |

## Remaining Counts

| Queue | Count |
| --- | ---: |
| `source_design_pending_entry_count` | 0 |
| `selected_rerun_pending_form_count` | 0 |
| `source_equivalence_blocked_form_count` | 0 |
| `missing_required_form_entry_count` | 0 |
| `current_seed_missing_form_entry_count` | 0 |

## Blocking Conditions

- external blocker report active: 0 blocked, 1 pending
- speed/debug timing artifact not claimable
- release model baseline artifact pending
