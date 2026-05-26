# vaBench Release Speed / Debug Artifact

Date: 2026-05-26

This artifact gates any EVAS speed/debug claim. It requires same-slice
EVAS and Spectre timing collected by the release dual rerun runner.

## Summary

| Metric | Value |
| --- | ---: |
| status | `measured_with_failures` |
| claim allowed | `False` |
| planned primary rerun rows | 2 |
| planned staged bundles | 2 |
| timed rows | 2 |
| timed scored forms | 0 / 184 |
| full score denominator timed | `False` |
| measurement plan | `measured_or_ready_to_import` |
| EVAS wall time | 9.364832209 |
| Spectre wall time | 129.990263541 |
| Spectre/EVAS speedup | 13.88068260487079 |
| median per-row wrapper speedup | 12.54401424436662 |
| geomean per-row wrapper speedup | 13.966117092974612 |
| EVAS reported total time | 7.0 |
| Spectre reported total time | None |
| reported-total Spectre/EVAS speedup | None |
| median per-row reported-total speedup | None |

Reason: Timing exists, but at least one rerun row did not PASS.

## Measurement Scope

- Selected summary: `results/vabench-release-v1-ct07-gain-dual-20260526_sui_r2/summary.json`
- Summary selection: `{"imported_summary": "results/vabench-release-v1-ct07-gain-dual-20260526_sui_r2/summary.json", "imported_summary_rejected_reason": "", "selected_summaries": ["results/vabench-release-v1-ct07-gain-dual-20260526_sui_r2/summary.json"], "source": "dual_rerun_import"}`
- Missing scored-form examples: `[{"entry_id": "vbr1_l1_acquisition_limited_sample_and_hold", "form": "bugfix"}, {"entry_id": "vbr1_l1_acquisition_limited_sample_and_hold", "form": "dut"}, {"entry_id": "vbr1_l1_acquisition_limited_sample_and_hold", "form": "e2e"}, {"entry_id": "vbr1_l1_acquisition_limited_sample_and_hold", "form": "tb"}, {"entry_id": "vbr1_l1_aperture_delay_track_and_hold", "form": "bugfix"}, {"entry_id": "vbr1_l1_aperture_delay_track_and_hold", "form": "dut"}, {"entry_id": "vbr1_l1_aperture_delay_track_and_hold", "form": "e2e"}, {"entry_id": "vbr1_l1_aperture_delay_track_and_hold", "form": "tb"}, {"entry_id": "vbr1_l1_bang_bang_phase_detector", "form": "bugfix"}, {"entry_id": "vbr1_l1_bang_bang_phase_detector", "form": "dut"}]`
- Timed unscored-form examples: `[{"entry_id": "vbr1_l1_gain_estimator", "form": "e2e"}, {"entry_id": "vbr1_l1_gain_estimator", "form": "tb"}]`

## Slowest EVAS Wrapper Rows

| entry | form | variant | EVAS s | Spectre s | speedup | steps |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| vbr1_l1_gain_estimator | e2e | gold | 5.19981 | 65.226490708 | 12.54401424436662 | 1204.0 |
| vbr1_l1_gain_estimator | tb | gold | 4.165022209 | 64.76377283299999 | 15.549442375854566 | 1204.0 |

## Measurement Plan

- Bridge ready: `True`
- Bundle variants: `{"gold": 2}`
- Bundle expected results: `{"pass": 2}`
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
