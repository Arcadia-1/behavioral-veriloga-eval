# vaBench Release Dual Certification

Date: 2026-05-26

This report is generated from historical imported evidence plus fresh
release EVAS/Spectre rerun results when available.

## Summary

| Metric | Value |
| --- | ---: |
| status | `partial` |
| source | `historical main120 import plus fresh release dual rerun` |
| simulator rerun | `True` |
| release entries | 64 |
| dual-certified release forms | 217 |
| dual-failed release forms | 0 |
| dual-pending release forms | 2 |
| dual-pass materialized entries | 63 |
| dual-pending materialized entries | 1 |
| dual-failed materialized entries | 0 |
| fully certified entries | 63 |
| source-equivalence failures | 0 |
| source-equivalence blocked forms | 0 |
| EVAS PASS / Spectre FAIL count | 0 |

## Pending Or Failed Forms

| Entry | Form | Status | EVAS | Spectre | Blockers | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| `vbr1_l1_gain_estimator` | `tb` | `pending` | `pass` | `pending` | Spectre license checkout failed on thu-sui direct-SUI rerun (SPECTRE-209); current gold EVAS/checker passed. | `benchmark-vabench-release-v1/evidence/dual/vbr1_l1_gain_estimator/tb/evidence.json` |
| `vbr1_l1_gain_estimator` | `e2e` | `pending` | `pass` | `pending` | Spectre license checkout failed on thu-sui direct-SUI rerun (SPECTRE-209); current gold EVAS/checker passed. | `benchmark-vabench-release-v1/evidence/dual/vbr1_l1_gain_estimator/e2e/evidence.json` |

## Incomplete Entries

| Entry | Dual | Missing forms | Release blockers |
| --- | --- | --- | --- |
| `vbr1_l1_gain_estimator` | `pending` |  | fresh_evas_spectre_dual_refresh_pending, spectre_certification |

## Notes

- Historical imported evidence is retained for already certified forms.
- Fresh release dual rerun results replace pending forms when the primary gold/fixed bundle passes.
- Bugfix buggy companion bundles are not counted in the scored release denominator.
