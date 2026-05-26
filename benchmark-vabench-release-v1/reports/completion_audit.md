# vaBench Release Completion Audit

Date: 2026-05-26

This report maps the active goal to concrete release evidence. It is
intentionally conservative: partial or blocked evidence does not count as
completion.

## Summary

| Metric | Value |
| --- | ---: |
| status | `in_progress` |
| proved requirements | 6 |
| blocked requirements | 1 |
| incomplete requirements | 1 |

## Requirement Audit

| ID | Status | Finding |
| --- | --- | --- |
| `R1_schema_package` | `proved` | Release package root, package manifest, evaluator contract, and all current release schemas are present and validate current release JSON surfaces. |
| `R2_tracker_64_entries` | `proved` | Tracker has 64 rows with level counts {'L1': 51, 'L2': 13}. |
| `R3_source_materialization` | `proved` | source-linked=64, asset-materialized=64, asset-status=pass |
| `R4_static_certification` | `proved` | static-status=pass, static-certified-forms=219 |
| `R5_dual_certification` | `blocked` | dual-status=partial, dual-certified=217, dual-pending=2, EVAS-pass/Spectre-fail=0, staging=ready, import=imported, bridge=ready, finish-readiness=ready_to_run |
| `R6_l0_conformance_separate` | `proved` | conformance-cases=4, benchmark-coverage-count=0 |
| `R7_paper_artifacts` | `incomplete` | paper-status=in_progress, speed=measured_with_failures, speed-claim=False, baseline=pending_release_baselines, baseline-claim=False, paper-tables=in_progress |
| `R8_no_overclaiming` | `proved` | scored=51, scored_forms=184, paper-claim-gates={'can_claim_release_assets_materialized': True, 'can_claim_top_level_coverage_plan': True, 'can_claim_release_package_complete': False, 'can_claim_scored_benchmark': True, 'can_claim_zero_evas_pass_spectre_fail_on_imported_release_evidence': True, 'can_claim_speedup': False, 'can_claim_model_baseline': False, 'blocking_conditions': ['selected EVAS/Spectre rerun pending', 'external blocker report active: 0 blocked, 1 pending', 'speed/debug timing artifact not claimable', 'release model baseline artifact pending']}, blocked-claim-ids=['C4_full_release_dual_certified', 'C6_speed_debug_claim', 'C7_model_baseline_claim', 'C9_release_package_complete'] |

## Blocking Conditions

- selected EVAS/Spectre rerun pending
- external blocker report active: 0 blocked, 1 pending
- speed/debug timing artifact not claimable
- release model baseline artifact pending

## Next Actions

- Use score_denominator_manifest.json as the recovery checklist for enabling scored release rows.
- Complete full-denominator same-slice EVAS/Spectre speed/debug timing from the fresh rerun.
- Run simple model baselines only after benchmark_score is enabled for certified release rows.
