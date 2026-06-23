# vaBench Release Baseline Artifact

Date: 2026-06-23

This artifact gates model-baseline claims for the clean vaBench release.
It intentionally keeps baseline workflows simple and secondary to the
benchmark/evaluator contribution.

## Summary

| Metric | Value |
| --- | ---: |
| status | `ready_for_baseline_runs` |
| claim allowed | `False` |
| scored release entries | 73 |
| scored release forms | 265 |
| score denominator status | `score_enabled` |
| fully certified entries | 79 |
| dual pending forms | 0 |
| dual failed forms | 0 |
| baseline summaries | 113 |
| execution plan | `ready_for_baseline_runs` |

## Minimal Baseline Lanes

- `prompt_only_generation`
- `evas_feedback_debug_generation`
- `spectre_final_judge_confirmation`

## Execution Plan

- Use score_denominator_manifest.json as the frozen scored-row source.
- Run prompt-only model generation on the scored denominator.
- Run EVAS-feedback debugging as an engineering baseline, with Spectre as final judge.
- Aggregate pass@1, axis rates, and failure taxonomy into a release baseline summary.

## Blocked By

- none

## Required To Claim

- Use the enabled score_denominator_manifest.json as the denominator source of truth.
- Run baseline model outputs through the release evaluator on scored rows.
- Publish pass@1 / axis rates / failure taxonomy with Spectre as the final judge.
- Keep baseline methods simple and describe them as stress tests, not as the paper's core method.
