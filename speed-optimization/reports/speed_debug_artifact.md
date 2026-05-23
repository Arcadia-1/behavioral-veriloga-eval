# vaBench Release Speed / Debug Artifact

Date: 2026-05-23

This artifact gates any EVAS speed/debug claim. It requires same-slice
EVAS and Spectre timing collected by the release dual rerun runner.

## Summary

| Metric | Value |
| --- | ---: |
| status | `measured_subset` |
| claim allowed | `False` |
| planned primary rerun rows | 17 |
| planned staged bundles | 0 |
| timed rows | 17 |
| timed scored forms | 17 / 257 |
| full score denominator timed | `False` |
| measurement plan | `measured_or_ready_to_import` |
| EVAS wall time | 55.599428001999996 |
| Spectre wall time | 102.014595167 |
| Spectre/EVAS speedup | 1.8348137531798057 |
| median per-row wrapper speedup | 2.3898691403306853 |
| geomean per-row wrapper speedup | 2.699687551600851 |
| EVAS reported total time | 31.399999999999995 |
| Spectre reported total time | 31.8 |
| reported-total Spectre/EVAS speedup | 1.012738853503185 |
| median per-row reported-total speedup | 6.5249999999999995 |

Reason: Timing exists for a subset only: 17 timed rows cover 17/257 scored forms. Wrapper aggregate Spectre/EVAS speedup is 1.835; do not claim release-wide EVAS speedup yet.

## Measurement Scope

- Selected summary: `results/vabench-release-v1-dual-rerun-ct02-complete-20260523-r2/summary.json`
- Summary selection: `{"imported_summary": "results/vabench-release-v1-dual-rerun-ct02-complete-20260523-r2/summary.json", "imported_summary_rejected_reason": "", "selected_summaries": ["results/vabench-release-v1-dual-rerun-ct02-complete-20260523-r2/summary.json"], "source": "dual_rerun_import"}`
- Missing scored-form examples: `[{"entry_id": "vbr1_l1_aperture_delay_track_and_hold", "form": "bugfix"}, {"entry_id": "vbr1_l1_aperture_delay_track_and_hold", "form": "dut"}, {"entry_id": "vbr1_l1_aperture_delay_track_and_hold", "form": "e2e"}, {"entry_id": "vbr1_l1_aperture_delay_track_and_hold", "form": "tb"}, {"entry_id": "vbr1_l1_bang_bang_phase_detector", "form": "bugfix"}, {"entry_id": "vbr1_l1_bang_bang_phase_detector", "form": "dut"}, {"entry_id": "vbr1_l1_bang_bang_phase_detector", "form": "e2e"}, {"entry_id": "vbr1_l1_bang_bang_phase_detector", "form": "tb"}, {"entry_id": "vbr1_l1_binary_weighted_voltage_dac", "form": "bugfix"}, {"entry_id": "vbr1_l1_binary_weighted_voltage_dac", "form": "dut"}]`
- Timed unscored-form examples: `[]`

## Slowest EVAS Wrapper Rows

| entry | form | variant | EVAS s | Spectre s | speedup | steps |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| vbr1_l1_window_comparator_detector | e2e | gold | 7.328478041999999 | 4.313404417000001 | 0.5885812023014316 | 4511.0 |
| vbr1_l1_window_comparator_detector | tb | gold | 7.273588708999998 | 4.3141732919999995 | 0.5931285730607566 | 4511.0 |
| vbr1_l1_window_comparator_detector | dut | gold | 6.868539417000001 | 4.745104875000003 | 0.6908462755932674 | 4511.0 |
| vbr1_l1_window_comparator_detector | bugfix | fixed | 6.089859750000002 | 6.059713624999997 | 0.9950497833714471 | 4511.0 |
| vbr1_l1_strongarm_style_latch_comparator | e2e | gold | 4.29303275 | 7.5276608330000006 | 1.7534599131581283 | 811.0 |
| vbr1_l1_strongarm_style_latch_comparator | dut | gold | 4.292659958 | 7.528189208 | 1.7537352787448532 | 811.0 |
| vbr1_l1_strongarm_style_latch_comparator | tb | gold | 4.291940792 | 7.479084208 | 1.7425879271076392 | 811.0 |
| vbr1_l1_offset_comparator | bugfix | fixed | 2.68494925 | 7.402392333 | 2.7569952515862264 | 1421.0 |

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
