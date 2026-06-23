# vaBench Release Speed / Debug Artifact

Date: 2026-06-23

This artifact gates any EVAS speed/debug claim. It requires same-slice
EVAS and Spectre timing collected by the release dual rerun runner.

## Summary

| Metric | Value |
| --- | ---: |
| status | `measured_subset` |
| claim allowed | `False` |
| planned primary rerun rows | 8 |
| planned staged bundles | 0 |
| timed rows | 8 |
| timed scored forms | 8 / 265 |
| full score denominator timed | `False` |
| measurement plan | `measured_or_ready_to_import` |
| EVAS wall time | 165.307315125 |
| Spectre wall time | 108.234825959 |
| Spectre/EVAS speedup | 0.6547491614461003 |
| median per-row wrapper speedup | 11.565893341282028 |
| geomean per-row wrapper speedup | 3.511763011638079 |
| EVAS reported total time | 147.89999999999998 |
| Spectre reported total time | 27.34 |
| reported-total Spectre/EVAS speedup | 0.18485463150777556 |
| median per-row reported-total speedup | 10.4 |

Reason: Timing exists for a subset only: 8 timed rows cover 8/265 scored forms. Wrapper aggregate Spectre/EVAS speedup is 0.655; do not claim release-wide EVAS speedup yet.

## Measurement Scope

- Selected summary: `benchmark-vabench-release-v1/reports/l2_observability_targeted_dual_20260601_r2_import_summary.json`
- Summary selection: `{"imported_summary": "benchmark-vabench-release-v1/reports/l2_observability_targeted_dual_20260601_r2_import_summary.json", "imported_summary_rejected_reason": "", "selected_summaries": ["benchmark-vabench-release-v1/reports/l2_observability_targeted_dual_20260601_r2_import_summary.json"], "source": "dual_rerun_import"}`
- Missing scored-form examples: `[{"entry_id": "vbr11_l1_bootstrapped_sample_switch", "form": "bugfix"}, {"entry_id": "vbr11_l1_bootstrapped_sample_switch", "form": "dut"}, {"entry_id": "vbr11_l1_bootstrapped_sample_switch", "form": "e2e"}, {"entry_id": "vbr11_l1_bootstrapped_sample_switch", "form": "tb"}, {"entry_id": "vbr11_l1_sigma_delta_modulator_loop", "form": "bugfix"}, {"entry_id": "vbr11_l1_sigma_delta_modulator_loop", "form": "dut"}, {"entry_id": "vbr11_l1_sigma_delta_modulator_loop", "form": "e2e"}, {"entry_id": "vbr11_l1_sigma_delta_modulator_loop", "form": "tb"}, {"entry_id": "vbr11_l2_bandgap_startup_trim_flow", "form": "bugfix"}, {"entry_id": "vbr11_l2_bandgap_startup_trim_flow", "form": "dut"}]`
- Timed unscored-form examples: `[]`

## Slowest EVAS Wrapper Rows

| entry | form | variant | EVAS s | Spectre s | speedup | steps |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| vbr1_l2_weighted_sar_adc_dac_loop | tb | gold | 77.74803166699999 | 17.651390667 | 0.22703328030993872 | 10648.0 |
| vbr1_l2_weighted_sar_adc_dac_loop | e2e | gold | 77.74739441700001 | 16.619955250000004 | 0.21376864619871988 | 10648.0 |
| vbr1_l2_amplifier_filter_chain | e2e | gold | 3.0339192919999998 | 13.149446000000001 | 4.3341449572087045 | 491.0 |
| vbr1_l2_amplifier_filter_chain | tb | gold | 2.9867673750000003 | 13.871675792000001 | 4.644377700154837 | 491.0 |
| vbr1_l2_reference_startup_enable_flow | e2e | gold | 1.0182922910000016 | 12.220407583 | 12.000883922040789 | 455.0 |
| vbr1_l2_reference_startup_enable_flow | tb | gold | 1.0159884170000026 | 11.750813667 | 11.565893341282028 | 455.0 |
| vbr1_l2_iq_downconversion_chain | tb | gold | 0.8788525410000005 | 12.012653417 | 13.66856538109502 | 519.0 |
| vbr1_l2_iq_downconversion_chain | e2e | gold | 0.8780691249999997 | 10.958483582999996 | 12.48020602364307 | 519.0 |

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
