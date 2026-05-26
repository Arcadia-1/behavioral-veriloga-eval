# vaBench Release Score Denominator Manifest

Date: 2026-05-26

This manifest is the source of truth for what is allowed to enter the
benchmark score denominator. Counted rows must be in the frozen content
denominator, score-enabled, and certified by static, EVAS, and Spectre checks.

## Summary

| Metric | Value |
| --- | ---: |
| status | `score_enabled` |
| planned entries | 64 |
| release forms | 219 |
| core entries | 51 |
| support entries | 13 |
| core forms | 184 |
| support forms | 35 |
| content denominator entries | 51 |
| content-excluded entries | 13 |
| content denominator forms | 184 |
| content-excluded forms | 35 |
| certified entries | 63 |
| certified forms | 217 |
| score-enabled entries | 51 |
| score-enabled forms | 184 |
| scored entries | 51 |
| scored forms | 184 |
| core scored entries | 51 |
| core scored forms | 184 |
| support scored entries | 0 |
| support scored forms | 0 |
| L0 conformance counted | 0 |

## Entry Exclusion Reasons

- `benchmark_score_disabled`: 13
- `content_denominator_excluded:support_suite_not_core_circuit_score`: 13
- `entry_blocker:fresh_evas_spectre_dual_refresh_pending`: 1
- `entry_blocker:spectre_certification`: 1
- `entry_not_fully_certified`: 1

## Form Exclusion Reasons

- `benchmark_score_disabled`: 35
- `content_denominator_excluded:support_suite_not_core_circuit_score`: 35
- `task_spectre:pending`: 2
