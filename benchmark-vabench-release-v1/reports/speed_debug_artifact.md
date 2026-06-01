# vaBench Release Speed / Debug Artifact

Date: 2026-06-01

This artifact gates any EVAS speed/debug claim. It requires same-slice
EVAS and Spectre timing collected by the release dual rerun runner.

## Summary

| Metric | Value |
| --- | ---: |
| status | `pending_measurement` |
| claim allowed | `False` |
| planned primary rerun rows | 54 |
| planned staged bundles | 65 |
| timed rows | 0 |
| timed scored forms | 0 / 236 |
| full score denominator timed | `False` |
| measurement plan | `ready_to_measure` |
| EVAS wall time | None |
| Spectre wall time | None |
| Spectre/EVAS speedup | None |
| median per-row wrapper speedup | None |
| geomean per-row wrapper speedup | None |
| EVAS reported total time | None |
| Spectre reported total time | None |
| reported-total Spectre/EVAS speedup | None |
| median per-row reported-total speedup | None |

Reason: Stale dual rerun timing summary rejected: summary tasks_total=8, current queue_count=54.

## Measurement Scope

- Selected summary: `benchmark-vabench-release-v1/reports/l2_observability_targeted_dual_20260601_r2_import_summary.json`
- Summary selection: `{"imported_summary": "benchmark-vabench-release-v1/reports/l2_observability_targeted_dual_20260601_r2_import_summary.json", "imported_summary_rejected_reason": "", "selected_summaries": ["benchmark-vabench-release-v1/reports/l2_observability_targeted_dual_20260601_r2_import_summary.json"], "source": "dual_rerun_import"}`
- Missing scored-form examples: `[{"entry_id": "vbr1_l1_acquisition_limited_sample_and_hold", "form": "bugfix"}, {"entry_id": "vbr1_l1_acquisition_limited_sample_and_hold", "form": "dut"}, {"entry_id": "vbr1_l1_acquisition_limited_sample_and_hold", "form": "e2e"}, {"entry_id": "vbr1_l1_acquisition_limited_sample_and_hold", "form": "tb"}, {"entry_id": "vbr1_l1_aperture_delay_track_and_hold", "form": "bugfix"}, {"entry_id": "vbr1_l1_aperture_delay_track_and_hold", "form": "dut"}, {"entry_id": "vbr1_l1_aperture_delay_track_and_hold", "form": "e2e"}, {"entry_id": "vbr1_l1_aperture_delay_track_and_hold", "form": "tb"}, {"entry_id": "vbr1_l1_bandgap_reference_macro_model", "form": "bugfix"}, {"entry_id": "vbr1_l1_bandgap_reference_macro_model", "form": "dut"}]`
- Timed unscored-form examples: `[]`

## Slowest EVAS Wrapper Rows

| entry | form | variant | EVAS s | Spectre s | speedup | steps |
| --- | --- | --- | ---: | ---: | ---: | ---: |

## Measurement Plan

- Bridge ready: `True`
- Bundle variants: `{"buggy": 11, "fixed": 11, "gold": 43}`
- Bundle expected results: `{"fail": 11, "pass": 54}`
- Claim blockers: `["fresh dual rerun summary is not complete"]`

## Debug Triage Order

- bridge_profile_diagnostics.json for SSH/tunnel readiness
- external_blockers.json for claim-boundary blocker chain
- dual_rerun_staging_manifest.json for per-bundle staging blockers
- imported dual rerun summary for per-row simulator/checker failures
- dual_rerun_import.json for stale or incomplete import blockers

## Required To Claim

- Run same-slice EVAS/Spectre timing for every scored release form, or state a narrower subset-only claim.
- Stratify or fix EVAS slow outliers before claiming aggregate speedup on the release package.
- Keep per-row EVAS and Spectre wall-clock timings from run_gold_dual_suite timing fields.
- Keep Spectre-reported runtime from spectre.out alongside wrapper wall-clock timings.
- Report machine/bridge/Cadence configuration with the timing artifact.
- Do not compute speedup from historical main120 summaries because they lack same-slice runtime metadata.
