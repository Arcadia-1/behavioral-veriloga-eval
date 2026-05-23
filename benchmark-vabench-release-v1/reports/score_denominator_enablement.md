# vaBench Release Score Denominator Enablement

Date: 2026-05-23

This report records the P1 write step that freezes `counts.benchmark_score`
for the release package before the score denominator manifest is rebuilt.

## Summary

| Metric | Value |
| --- | ---: |
| status | `enabled` |
| release entries | 73 |
| release forms | 249 |
| score-enabled entries | 73 |
| score-enabled forms | 249 |
| disabled entries | 0 |
| disabled forms | 0 |
| content-excluded entries | 0 |
| content-excluded forms | 0 |
| dual certification ready | `True` |

## Policy

- `source_of_truth_after_refresh`: benchmark-vabench-release-v1/reports/score_denominator_manifest.json
- `enabled_rule`: benchmark_score=true only for content-denominator entries with full static/EVAS/Spectre certification after dual_certification.status=pass.
- `excluded_rule`: Content-excluded duplicates remain package assets and certified parity evidence, but do not enter scored benchmark denominators.
- `l0_rule`: L0 conformance remains outside the L1/L2 benchmark denominator.

## Disabled Reasons

- none
