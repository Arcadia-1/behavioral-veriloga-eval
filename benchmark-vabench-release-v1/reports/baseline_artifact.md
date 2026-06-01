# vaBench Release Baseline Artifact

Date: 2026-06-01

This artifact gates model-baseline claims for the clean vaBench release.
It intentionally keeps baseline workflows simple and secondary to the
benchmark/evaluator contribution.

## Summary

| Metric | Value |
| --- | ---: |
| status | `claim_ready` |
| claim allowed | `True` |
| scored release entries | 66 |
| scored release forms | 236 |
| score denominator status | `score_enabled` |
| fully certified entries | 79 |
| dual pending forms | 0 |
| dual failed forms | 0 |
| baseline summaries | 112 |
| final-judge baseline reports | 2 |
| execution plan | `claim_ready` |

## Current Final-Judge Baselines

| Model | Rows | Strict pass | Strict rate | Category macro rate | Mismatches |
| --- | ---: | ---: | ---: | ---: | ---: |
| mimo-v2.5 | 236 | 92 | 38.98% | 38.33% | 0 |
| mimo-v2.5-pro | 236 | 112 | 47.46% | 47.03% | 0 |

## Evaluation Hygiene

- Primary metric: full_strict pass@1 on the 236 scored core forms
- Diagnostic slices: valid_candidate pass@1, behavior_ready pass rate, category macro-average pass rate, form-level pass rates, failure-axis counts
- Required stratification: model, form, category, difficulty, failure_axis

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
- Publish full_strict pass@1, category macro averages, form slices, axis rates, and failure taxonomy with Spectre as the final judge.
- Keep baseline methods simple and describe them as benchmark stress tests, not as the paper's core method.
