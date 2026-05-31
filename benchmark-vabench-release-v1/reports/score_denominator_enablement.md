# vaBench Release Score Denominator Enablement

Date: 2026-05-27

This report records the P1 write step that freezes `counts.benchmark_score`
for the release package before the score denominator manifest is rebuilt.

## Summary

| Metric | Value |
| --- | ---: |
| status | `enabled` |
| release entries | 79 |
| release forms | 271 |
| score-enabled entries | 66 |
| score-enabled forms | 236 |
| disabled entries | 13 |
| disabled forms | 35 |
| content-excluded entries | 13 |
| content-excluded forms | 35 |
| dual certification ready | `True` |

## Policy

- `source_of_truth_after_refresh`: benchmark-vabench-release-v1/reports/score_denominator_manifest.json
- `enabled_rule`: benchmark_score=true only for content-denominator entries with full static/EVAS/Spectre certification after dual_certification.status=pass.
- `excluded_rule`: Content-excluded duplicates remain package assets and certified parity evidence, but do not enter scored benchmark denominators.
- `l0_rule`: L0 conformance remains outside the L1/L2 benchmark denominator.

## Disabled Reasons

- `support_suite_not_core_circuit_score`: 13
