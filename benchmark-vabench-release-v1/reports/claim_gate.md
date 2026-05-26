# vaBench Release Claim Gate

Date: 2026-05-26

This report is the paper-facing claim ledger. It separates what may be
claimed from the current release artifacts from what is still blocked.
It is not simulator certification evidence.

## Summary

| Metric | Value |
| --- | ---: |
| status | `in_progress` |
| claims | 9 |
| allowed claims | 5 |
| blocked claims | 4 |
| blocked completion-required claims | 4 |

## Claims

| ID | Status | Safe wording |
| --- | --- | --- |
| `C1_coverage_target_defined` | `allowed` | The current release package defines 64 planned L1/L2 entries; this is a coverage target, not a final scored benchmark result. |
| `C2_source_assets_static_clean` | `allowed` | The release has 64 materialized entries for the 64-entry plan and 219 static-certified forms with zero asset issues. |
| `C3_imported_dual_subset_clean` | `allowed` | On the imported certified subset (217 forms), EVAS PASS / Spectre FAIL count is 0. |
| `C4_full_release_dual_certified` | `blocked` | This claim is blocked until every release form has current EVAS/Spectre evidence with zero dual failures and zero EVAS PASS / Spectre FAIL mismatches. |
| `C5_score_denominator_enabled` | `allowed` | The release benchmark score denominator is enabled for 51 certified content-denominator entries and 184 forms. |
| `C6_speed_debug_claim` | `blocked` | Speed/debug has subset timing evidence, but release-wide speedup remains blocked until the dedicated artifact marks the speed claim allowed. |
| `C7_model_baseline_claim` | `blocked` | Model baseline reporting is pending until baseline runs report against the enabled score denominator. |
| `C8_l0_conformance_separate` | `allowed` | L0 conformance has 4 cases and contributes 0 entries to benchmark coverage. |
| `C9_release_package_complete` | `blocked` | The package structure and source assets are ready, but full completion remains blocked by fresh dual rerun, scoring, speed, and baseline gates. |

## Blocked Claim Details

### C4_full_release_dual_certified
- resolve 2 dual-pending forms
- complete fresh rerun for 2 queued forms (includes 0 historical source-equivalence blockers)
- bridge diagnostics must report a ready profile
- fresh dual rerun summary must import successfully
### C6_speed_debug_claim
- Run same-slice EVAS/Spectre timing for every scored release form, or state a narrower subset-only claim.
- Stratify or fix EVAS slow outliers before claiming aggregate speedup on the release package.
- Keep per-row EVAS and Spectre wall-clock timings from run_gold_dual_suite timing fields.
- Keep Spectre-reported runtime from spectre.out alongside wrapper wall-clock timings.
- Report machine/bridge/Cadence configuration with the timing artifact.
- Do not compute speedup from historical main120 summaries because they lack same-slice runtime metadata.
### C7_model_baseline_claim
- baseline runs must report against counted release entries/forms only
### C9_release_package_complete
- selected EVAS/Spectre rerun pending
- external blocker report active: 0 blocked, 1 pending
- speed/debug timing artifact not claimable
- release model baseline artifact pending

## Policy

- Allowed claims may be used only with their safe_wording scope.
- Blocked claims must not appear as paper conclusions, abstract claims, figure captions, or benchmark result text.
- Partial imported evidence must not be phrased as full-release certification.
- Score, speed, and baseline claims require an enabled denominator and fresh release evidence.
