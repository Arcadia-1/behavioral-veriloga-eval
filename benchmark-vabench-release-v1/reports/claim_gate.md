# vaBench Release Claim Gate

Date: 2026-05-23

This report is the paper-facing claim ledger. It separates what may be
claimed from the current release artifacts from what is still blocked.
It is not simulator certification evidence.

## Summary

| Metric | Value |
| --- | ---: |
| status | `in_progress` |
| claims | 9 |
| allowed claims | 7 |
| blocked claims | 2 |
| blocked completion-required claims | 2 |

## Claims

| ID | Status | Safe wording |
| --- | --- | --- |
| `C1_coverage_target_defined` | `allowed` | The current release package defines 73 planned L1/L2 entries; this is a coverage target, not a final scored benchmark result. |
| `C2_source_assets_static_clean` | `allowed` | The release has 73 materialized entries for the 73-entry plan and 249 static-certified forms with zero asset issues. |
| `C3_imported_dual_subset_clean` | `allowed` | On the full imported release evidence (249 forms), EVAS PASS / Spectre FAIL count is 0. |
| `C4_full_release_dual_certified` | `allowed` | The full release package has EVAS/Spectre certification for 249 forms with zero dual failures and zero EVAS PASS / Spectre FAIL mismatches. |
| `C5_score_denominator_enabled` | `allowed` | The release benchmark score denominator is enabled for 73 certified content-denominator entries and 245 forms. |
| `C6_speed_debug_claim` | `blocked` | Speed/debug has subset timing evidence, but release-wide speedup remains blocked until the dedicated artifact marks the speed claim allowed. |
| `C7_model_baseline_claim` | `blocked` | Model baseline reporting is pending until baseline runs report against the enabled score denominator. |
| `C8_l0_conformance_separate` | `allowed` | L0 conformance has 4 cases and contributes 0 entries to benchmark coverage. |
| `C9_release_package_complete` | `allowed` | The clean vaBench release package structure, source assets, EVAS/Spectre certification, and score denominator are complete; speed/debug and model baselines remain separate gated claims. |

## Blocked Claim Details

### C6_speed_debug_claim
- Run same-slice EVAS/Spectre timing for every scored release form, or state a narrower subset-only claim.
- Stratify or fix EVAS slow outliers before claiming aggregate speedup on the release package.
- Keep per-row EVAS and Spectre wall-clock timings from run_gold_dual_suite timing fields.
- Keep Spectre-reported runtime from spectre.out alongside wrapper wall-clock timings.
- Report machine/bridge/Cadence configuration with the timing artifact.
- Do not compute speedup from historical main120 summaries because they lack same-slice runtime metadata.
### C7_model_baseline_claim
- baseline runs must report against counted release entries/forms only

## Policy

- Allowed claims may be used only with their safe_wording scope.
- Blocked claims must not appear as paper conclusions, abstract claims, figure captions, or benchmark result text.
- Partial imported evidence must not be phrased as full-release certification.
- Score, speed, and baseline claims require an enabled denominator and fresh release evidence.
