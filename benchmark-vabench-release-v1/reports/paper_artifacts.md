# vaBench Paper-Facing Artifact Summary

Date: 2026-05-21

This is a claim-gated summary for paper writing. It records what can be
cited from the current release package and what must remain pending.

## Coverage

| Metric | Value |
| --- | ---: |
| planned L1/L2 entries | 75 |
| source-linked entries | 75 |
| entries with copied assets | 75 |
| static-certified release forms | 259 |
| dual-certified release forms | 259 |
| fully certified entries | 75 |
| certification matrix | `complete` |
| scored release entries | 74 |
| scored release forms | 255 |
| score denominator status | `score_enabled` |

## Parity

| Metric | Value |
| --- | ---: |
| release dual status | `pass` |
| dual-certified release forms | 259 |
| dual-pending release forms | 0 |
| dual-failed release forms | 0 |
| EVAS PASS / Spectre FAIL count | 0 |
| source-equivalence blocked forms | 0 |
| dual rerun staging status | `complete` |
| rerun rows with ready primary bundle | 0 |
| ready rerun bundles | 0 |
| latest dual rerun attempt | `dry_run` |
| bridge diagnostics | `ready` |
| bridge ready profiles | `ci` |
| main120 EVAS gold pass | 120/120 |
| main120 Spectre gold pass | 120/120 |
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
| stale rerun summary rejected | `False` |
| import status | `imported` |

## Speed / Debug

- Status: `measured`
- Claim allowed: `False`
- Reason: Timing exists, but this slice does not show an EVAS speedup over Spectre.

## Baselines

- Status: `ready_for_baseline_runs`
- Claim allowed: `False`
- Reason: Baseline artifact exists but has no claimable baseline summary yet.

## Claim Gates

| Claim | Allowed |
| --- | --- |
| `can_claim_release_assets_materialized` | `True` |
| `can_claim_top_level_coverage_plan` | `True` |
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
