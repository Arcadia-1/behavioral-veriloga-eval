# vaBench Release Speed / Debug Artifact

Date: 2026-05-21

This artifact gates any EVAS speed/debug claim. It requires same-slice
EVAS and Spectre timing collected by the release dual rerun runner.

## Summary

| Metric | Value |
| --- | ---: |
| status | `measured` |
| claim allowed | `False` |
| planned primary rerun rows | 277 |
| planned staged bundles | 0 |
| timed rows | 277 |
| timed scored forms | 255 / 255 |
| full score denominator timed | `True` |
| measurement plan | `measured_or_ready_to_import` |
| EVAS wall time | 1389.931596052999 |
| Spectre wall time | 1284.5083710420001 |
| Spectre/EVAS speedup | 0.924152220648577 |
| median per-row wrapper speedup | 5.177946901299534 |
| geomean per-row wrapper speedup | 3.992393119271372 |
| EVAS reported total time | 1107.7000000000012 |
| Spectre reported total time | 211.51799999999997 |
| reported-total Spectre/EVAS speedup | 0.19095242394150017 |
| median per-row reported-total speedup | 1.2425 |

Reason: Timing exists, but this slice does not show an EVAS speedup over Spectre.

## Measurement Scope

- Selected summary: `results/vabench-release-v1-dual-rerun-speed-remaining-fix9-20260521/summary.json`
- Summary selection: `{"imported_summary": "results/vabench-release-v1-dual-rerun/summary.json", "imported_summary_rejected_reason": "imported summary is a dry-run sample", "selected_summaries": ["results/vabench-release-v1-dual-rerun-20260516-full-after-fixes/summary.json", "results/vabench-release-v1-dual-rerun-speed-remaining-smoke-20260521-bridge-retry/summary.json", "results/vabench-release-v1-dual-rerun-speed-remaining-20260521/summary.json", "results/vabench-release-v1-dual-rerun-speed-remaining-fix9-20260521/summary.json"], "source": "merged_complete_timing_summaries"}`
- Missing scored-form examples: `[]`
- Timed unscored-form examples: `[{"entry_id": "vbr1_l1_clocked_comparator", "form": "bugfix"}, {"entry_id": "vbr1_l1_clocked_comparator", "form": "dut"}, {"entry_id": "vbr1_l1_clocked_comparator", "form": "e2e"}, {"entry_id": "vbr1_l1_clocked_comparator", "form": "tb"}, {"entry_id": "vbr1_l1_pfd_dead_zone_model", "form": "bugfix"}, {"entry_id": "vbr1_l1_pfd_dead_zone_model", "form": "dut"}, {"entry_id": "vbr1_l1_pfd_dead_zone_model", "form": "e2e"}, {"entry_id": "vbr1_l1_pfd_dead_zone_model", "form": "tb"}, {"entry_id": "vbr1_l1_resettable_sample_and_hold", "form": "bugfix"}, {"entry_id": "vbr1_l1_resettable_sample_and_hold", "form": "dut"}]`

## Slowest EVAS Wrapper Rows

| entry | form | variant | EVAS s | Spectre s | speedup | steps |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| vbr1_l1_gain_estimator | e2e | gold | 118.07542783399998 | 11.64240133300001 | 0.09860139020091328 | 114117.0 |
| vbr1_l2_gain_extraction_convergence_measurement_flow | tb | gold | 116.20911758300008 | 10.664386457999854 | 0.09176893069842841 | 114117.0 |
| vbr1_l1_gain_estimator | tb | gold | 115.77935929199998 | 10.738692416999925 | 0.09275135466863771 | 114117.0 |
| vbr1_l2_gain_extraction_convergence_measurement_flow | e2e | gold | 115.381564583 | 10.781796332999875 | 0.09344470559024154 | 114117.0 |
| vbr1_l1_pfd_up_dn_logic | bugfix | fixed | 84.49880625000003 | 4.521887457999924 | 0.05351421704847957 | 30058.0 |
| vbr1_l1_pfd_up_dn_logic | tb | gold | 82.98954312499995 | 4.601050999999984 | 0.055441334254242365 | 30058.0 |
| vbr1_l1_pfd_up_dn_logic | e2e | gold | 81.97216370800004 | 4.392928833000042 | 0.053590495044738166 | 30058.0 |
| vbr1_l1_pfd_up_dn_logic | dut | gold | 71.40262341699997 | 6.333877875000098 | 0.08870651485743716 | 30058.0 |

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
