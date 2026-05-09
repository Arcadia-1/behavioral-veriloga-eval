# vaBench-main-v1 Main120 Confidence Audit

**Date**: 2026-05-08

Question: do we have factual confidence in the current `vaBench-main-v1` Main120
strategy after filling 30 packs / 120 tasks?

Short answer: not mathematical 100%, but the benchmark strategy has now reached
a practical release-gate confidence level for the current repository state.  The
remaining risks are explicitly bounded and have rerun triggers.

## Confidence Loop

| Loop item | Possible loophole | Test or mitigation | Result |
| --- | --- | --- | --- |
| L1 | Benchmark may not actually contain 30 packs / 120 tasks | Manifest and four-form coverage audit | PASS: 30 packs, 120 tasks, no missing forms |
| L2 | Prompt/checker/gold may be semantically misaligned | Full semantic prompt/checker/gold audit | PASS: 120/120, 0 WARN, 0 FAIL |
| L3 | Benchmark may contain hidden task-id/source routing | Integrity audit plus static leakage scan | PASS: no issues |
| L4 | Incremental evidence may miss old-task drift | EVAS/Spectre reuse hash audits for Draft7 and Draft11 staged gold | PASS |
| L5 | Incremental result pieces may not cover every manifest task | Result-union coverage audit | PASS: EVAS 120/120, Spectre 120/120, no missing/extra |
| L6 | EVAS-only success may not reflect Spectre behavior | Full Main120 Spectre audit through `jin -> thu-wei` | PASS: 120/120 |
| L7 | Prior composed evidence may hide integration issues | Full Main120 strict-EVAS and full Main120 Spectre runs | PASS: 120/120 each |

## Artifacts

| Evidence | Artifact |
| --- | --- |
| Full semantic audit | `analysis/vabench-main-v1_semantic_contract_audit_20260508.json` |
| Full integrity audit | `analysis/vabench-main-v1_integrity_audit_20260508.json` |
| Static leakage audit | `analysis/vabench-main-v1_main120_leakage_static_audit_20260508.json` |
| Result coverage audit | `analysis/vabench-main-v1_main120_result_coverage_audit_20260508.json` |
| Full Main120 strict-EVAS | `results/vabench-main-v1-main120-gold-evas-2026-05-08/summary.json` |
| Full Main120 Spectre | `results/vabench-main-v1-main120-gold-spectre-jin-2026-05-08/summary.json` |
| Draft7 EVAS reuse hash | `analysis/vabench-main-v1_draft7_reuse_hash_audit_20260508.json` |
| Draft7 Spectre reuse hash | `analysis/vabench-main-v1_draft7_spectre_reuse_hash_audit_20260508.json` |
| Draft11 EVAS reuse hash | `analysis/vabench-main-v1_draft11_new4_reuse_hash_audit_20260508.json` |
| Draft11 Spectre reuse hash | `analysis/vabench-main-v1_draft11_new4_spectre_reuse_hash_audit_20260508.json` |

## Remaining Risks And Rerun Triggers

| Residual risk | Why not fully eliminated | Required action |
| --- | --- | --- |
| Future code changes can invalidate evidence | Any benchmark, checker, validator, EVAS, bridge, or Spectre environment change can alter results | Rerun semantic/integrity audits and full Main120 EVAS/Spectre before using updated artifacts |
| Checker strength is finite | Passing checker means passing the public behavioral contract, not a theorem about all analog behavior | Use residual analysis and heldout packs before broader claims |
| Main120 may still be tuned against during method development | Main is now clean, but method iteration can overfit it | Build and lock `vaBench-heldout-v1` before final model/system claims |
| Extra packs are compact behavioral abstractions | They are useful for controlled model evaluation but not a full analog design corpus | Treat Main120 as v1; expand v2/stress sets for harder analog/nonideal tasks |

## Decision

For the current repository state, the Main120 benchmark gate is complete:

- Full semantic/integrity: PASS.
- Full strict-EVAS: 120/120 PASS.
- Full Spectre: 120/120 PASS.
- Leakage/result-coverage/reuse audits: PASS.

This is the strongest factual confidence level available short of freezing the
entire toolchain and proving checker completeness, which is outside the project
scope.  The next safe step is to run the model strategy matrix on Main120, while
building heldout before making final generalization claims.
