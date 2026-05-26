# vaBench Paper-Facing Artifact Summary

Date: 2026-05-26

This is a claim-gated summary for paper writing. It records what can be
cited from the current release package and what must remain pending.

## Coverage

| Metric | Value |
| --- | ---: |
| planned L1/L2 entries | 64 |
| core circuit entries | 51 |
| support entries | 13 |
| D1/D2/D3 difficulty counts | `{'D1': 7, 'D2': 43, 'D3': 14}` |
| source-linked entries | 64 |
| entries with copied assets | 64 |
| static-certified release forms | 219 |
| dual-certified release forms | 217 |
| fully certified entries | 63 |
| certification matrix | `partial` |
| scored release entries | 51 |
| scored release forms | 184 |
| core scored release entries | 51 |
| core scored release forms | 184 |
| support scored release entries | 0 |
| support scored release forms | 0 |
| score denominator status | `score_enabled` |

## Parity

| Metric | Value |
| --- | ---: |
| release dual status | `partial` |
| dual-certified release forms | 217 |
| dual-pending release forms | 2 |
| dual-failed release forms | 0 |
| EVAS PASS / Spectre FAIL count | 0 |
| source-equivalence blocked forms | 0 |
| dual rerun staging status | `ready` |
| rerun rows with ready primary bundle | 2 |
| ready rerun bundles | 2 |
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
| fresh dual rerun queue rows | 2 |
| ready rerun bundles | 2 |
| dual-pending release forms | 2 |
| bridge ready | `True` |
| external blockers | `pending` |
| external blocked count | 0 |
| external pending count | 1 |
| stale rerun summary rejected | `False` |
| import status | `imported` |

## Speed / Debug

- Status: `measured_with_failures`
- Claim allowed: `False`
- Reason: Timing exists, but at least one rerun row did not PASS.

## Baselines

- Status: `pending_release_baselines`
- Claim allowed: `False`
- Reason: Score denominator is enabled, but no claimable model baseline summary has been produced yet.

## Claim Gates

| Claim | Allowed |
| --- | --- |
| `can_claim_release_assets_materialized` | `True` |
| `can_claim_top_level_coverage_plan` | `True` |
| `can_claim_release_package_complete` | `False` |
| `can_claim_scored_benchmark` | `True` |
| `can_claim_zero_evas_pass_spectre_fail_on_imported_release_evidence` | `True` |
| `can_claim_speedup` | `False` |
| `can_claim_model_baseline` | `False` |

## Remaining Counts

| Queue | Count |
| --- | ---: |
| `source_design_pending_entry_count` | 0 |
| `selected_rerun_pending_form_count` | 2 |
| `source_equivalence_blocked_form_count` | 0 |
| `missing_required_form_entry_count` | 0 |
| `current_seed_missing_form_entry_count` | 0 |

## Blocking Conditions

- selected EVAS/Spectre rerun pending
- external blocker report active: 0 blocked, 1 pending
- speed/debug timing artifact not claimable
- release model baseline artifact pending
