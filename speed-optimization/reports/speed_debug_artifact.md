# vaBench Release Speed / Debug Artifact

Date: 2026-05-24

This artifact gates any EVAS speed/debug claim. It requires same-slice
EVAS and Spectre timing collected by the release dual rerun runner.

## Summary

| Metric | Value |
| --- | ---: |
| status | `measured_subset` |
| claim allowed | `False` |
| planned primary rerun rows | 4 |
| planned staged bundles | 0 |
| timed rows | 4 |
| timed scored forms | 4 / 245 |
| full score denominator timed | `False` |
| measurement plan | `measured_or_ready_to_import` |
| EVAS wall time | 5.988978543 |
| Spectre wall time | 16.235006709 |
| Spectre/EVAS speedup | 2.710813971436865 |
| median per-row wrapper speedup | 5.545027771398746 |
| geomean per-row wrapper speedup | 3.115750138088029 |
| EVAS reported total time | 2.8 |
| Spectre reported total time | 2.89 |
| reported-total Spectre/EVAS speedup | 1.0321428571428573 |
| median per-row reported-total speedup | 8.05 |

Reason: Timing exists for a subset only: 4 timed rows cover 4/245 scored forms. Wrapper aggregate Spectre/EVAS speedup is 2.711; do not claim release-wide EVAS speedup yet.

## Measurement Scope

- Selected summary: `results/vabench-release-v1-dual-rerun-ct06-split-20260524-r5-l2/summary.json`
- Summary selection: `{"imported_summary": "results/vabench-release-v1-dual-rerun-ct06-split-20260524-r5-l2/summary.json", "imported_summary_rejected_reason": "", "selected_summaries": ["results/vabench-release-v1-dual-rerun-ct06-split-20260524-r5-l2/summary.json"], "source": "dual_rerun_import"}`
- Missing scored-form examples: `[{"entry_id": "vbr1_l1_adc_code_capture_register", "form": "bugfix"}, {"entry_id": "vbr1_l1_adc_code_capture_register", "form": "dut"}, {"entry_id": "vbr1_l1_adc_code_capture_register", "form": "e2e"}, {"entry_id": "vbr1_l1_adc_code_capture_register", "form": "tb"}, {"entry_id": "vbr1_l1_aperture_delay_track_and_hold", "form": "bugfix"}, {"entry_id": "vbr1_l1_aperture_delay_track_and_hold", "form": "dut"}, {"entry_id": "vbr1_l1_aperture_delay_track_and_hold", "form": "e2e"}, {"entry_id": "vbr1_l1_aperture_delay_track_and_hold", "form": "tb"}, {"entry_id": "vbr1_l1_bang_bang_phase_detector", "form": "bugfix"}, {"entry_id": "vbr1_l1_bang_bang_phase_detector", "form": "dut"}]`
- Timed unscored-form examples: `[]`

## Slowest EVAS Wrapper Rows

| entry | form | variant | EVAS s | Spectre s | speedup | steps |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| vbr1_l2_serializer_frame_alignment_flow | tb | gold | 2.253523625 | 3.939709542 | 1.7482441711699384 | 1569.0 |
| vbr1_l2_serializer_frame_alignment_flow | e2e | gold | 2.2200757920000003 | 3.890366041 | 1.7523573091598306 | 1569.0 |
| vbr1_l2_event_controller | e2e | gold | 0.757860459 | 4.202357292 | 5.545027771398746 | 905.0 |
| vbr1_l2_event_controller | tb | gold | 0.757518667 | 4.202573834 | 5.547815541818192 | 905.0 |

## Measurement Plan

- Bridge ready: `True`
- Bundle variants: `{}`
- Bundle expected results: `{}`
- Claim blockers: `[]`

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
