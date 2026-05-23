# vaBench Release Completion Audit

Date: 2026-05-23

This report maps the active goal to concrete release evidence. It is
intentionally conservative: partial or blocked evidence does not count as
completion.

## Summary

| Metric | Value |
| --- | ---: |
| status | `in_progress` |
| proved requirements | 5 |
| blocked requirements | 0 |
| incomplete requirements | 3 |

## Requirement Audit

| ID | Status | Finding |
| --- | --- | --- |
| `R1_schema_package` | `proved` | Release package root, package manifest, evaluator contract, and all current release schemas are present and validate current release JSON surfaces. |
| `R2_tracker_75_entries` | `incomplete` | Tracker has 73 rows with level counts {'L1': 57, 'L2': 16}. |
| `R3_source_materialization` | `incomplete` | source-linked=73, asset-materialized=73, asset-status=pass |
| `R4_static_certification` | `proved` | static-status=pass, static-certified-forms=249 |
| `R5_dual_certification` | `proved` | dual-status=pass, dual-certified=249, dual-pending=0, EVAS-pass/Spectre-fail=0, staging=complete, import=partial_imported, bridge=ready, finish-readiness=blocked |
| `R6_l0_conformance_separate` | `proved` | conformance-cases=4, benchmark-coverage-count=0 |
| `R7_paper_artifacts` | `incomplete` | paper-status=in_progress, speed=measured_subset, speed-claim=False, baseline=ready_for_baseline_runs, baseline-claim=False, paper-tables=in_progress |
| `R8_no_overclaiming` | `proved` | scored=73, scored_forms=245, paper-claim-gates={'can_claim_release_assets_materialized': True, 'can_claim_top_level_coverage_plan': False, 'can_claim_release_package_complete': True, 'can_claim_scored_benchmark': True, 'can_claim_zero_evas_pass_spectre_fail_on_imported_release_evidence': True, 'can_claim_speedup': False, 'can_claim_model_baseline': False, 'blocking_conditions': ['external blocker report active: 0 blocked, 1 pending', 'speed/debug timing artifact not claimable', 'release model baseline artifact pending']}, blocked-claim-ids=['C6_speed_debug_claim', 'C7_model_baseline_claim'] |

## Blocking Conditions

- external blocker report active: 0 blocked, 1 pending
- speed/debug timing artifact not claimable
- release model baseline artifact pending

## Next Actions

- Use score_denominator_manifest.json as the recovery checklist for enabling scored release rows.
- Complete full-denominator same-slice EVAS/Spectre speed/debug timing from the fresh rerun.
- Run simple model baselines only after benchmark_score is enabled for certified release rows.
