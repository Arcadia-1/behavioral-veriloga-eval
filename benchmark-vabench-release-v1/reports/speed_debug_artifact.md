# vaBench Release Speed / Debug Artifact

Date: 2026-05-27

This artifact gates any EVAS speed/debug claim. It requires same-slice
EVAS and Spectre timing collected by the release dual rerun runner.

## Summary

| Metric | Value |
| --- | ---: |
| status | `measured_subset` |
| claim allowed | `False` |
| planned primary rerun rows | 54 |
| planned staged bundles | 65 |
| timed rows | 54 |
| timed scored forms | 52 / 236 |
| full score denominator timed | `False` |
| measurement plan | `measured_or_ready_to_import` |
| EVAS wall time | 43.617206748 |
| Spectre wall time | 288.042362961 |
| Spectre/EVAS speedup | 6.603869996196116 |
| median per-row wrapper speedup | 10.10993214287678 |
| geomean per-row wrapper speedup | 8.327224384594006 |
| EVAS reported total time | 9.799999999999986 |
| Spectre reported total time | 37.962 |
| reported-total Spectre/EVAS speedup | 3.873673469387761 |
| median per-row reported-total speedup | 5.720000000000001 |

Reason: Timing exists for a subset only: 54 timed rows cover 52/236 scored forms. Wrapper aggregate Spectre/EVAS speedup is 6.604; do not claim release-wide EVAS speedup yet.

## Measurement Scope

- Selected summary: `results/vabench-release-v1-dual-rerun/summary.json`
- Summary selection: `{"imported_summary": "results/vabench-release-v1-dual-rerun/summary.json", "imported_summary_rejected_reason": "", "selected_summaries": ["results/vabench-release-v1-dual-rerun/summary.json"], "source": "dual_rerun_import"}`
- Missing scored-form examples: `[{"entry_id": "vbr1_l1_acquisition_limited_sample_and_hold", "form": "bugfix"}, {"entry_id": "vbr1_l1_acquisition_limited_sample_and_hold", "form": "dut"}, {"entry_id": "vbr1_l1_acquisition_limited_sample_and_hold", "form": "e2e"}, {"entry_id": "vbr1_l1_acquisition_limited_sample_and_hold", "form": "tb"}, {"entry_id": "vbr1_l1_aperture_delay_track_and_hold", "form": "bugfix"}, {"entry_id": "vbr1_l1_aperture_delay_track_and_hold", "form": "dut"}, {"entry_id": "vbr1_l1_aperture_delay_track_and_hold", "form": "e2e"}, {"entry_id": "vbr1_l1_aperture_delay_track_and_hold", "form": "tb"}, {"entry_id": "vbr1_l1_bang_bang_phase_detector", "form": "bugfix"}, {"entry_id": "vbr1_l1_bang_bang_phase_detector", "form": "dut"}]`
- Timed unscored-form examples: `[{"entry_id": "vbr1_l1_gain_estimator", "form": "e2e"}, {"entry_id": "vbr1_l1_gain_estimator", "form": "tb"}]`

## Slowest EVAS Wrapper Rows

| entry | form | variant | EVAS s | Spectre s | speedup | steps |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| vbr1_l1_gain_estimator | tb | gold | 3.4178656249999992 | 4.535630125000001 | 1.3270358237094244 | 1204.0 |
| vbr1_l1_gain_estimator | e2e | gold | 3.4050362079999985 | 4.513027374999998 | 1.3253977635823133 | 1204.0 |
| vbr1_l1_bandgap_reference_macro_model | dut | gold | 1.5505648330000001 | 7.672428041999999 | 4.9481504279673025 | 478.0 |
| vbr1_l1_bandgap_reference_macro_model | tb | gold | 1.5495730419999998 | 6.857146125 | 4.42518418889737 | 478.0 |
| vbr1_l1_bias_voltage_generator_with_enable_trim | e2e | gold | 1.5495391250000001 | 4.737767791 | 3.0575335043573033 | 464.0 |
| vbr1_l1_bandgap_reference_macro_model | e2e | gold | 1.549518875 | 7.712991667 | 4.977668740563099 | 478.0 |
| vbr1_l1_bias_voltage_generator_with_enable_trim | bugfix | fixed | 1.5493725839999999 | 6.614365875000001 | 4.269060872320173 | 464.0 |
| vbr1_l1_bias_voltage_generator_with_enable_trim | dut | gold | 1.5490505 | 4.669098833 | 3.014168248872454 | 464.0 |

## Measurement Plan

- Bridge ready: `True`
- Bundle variants: `{"buggy": 11, "fixed": 11, "gold": 43}`
- Bundle expected results: `{"fail": 11, "pass": 54}`
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
