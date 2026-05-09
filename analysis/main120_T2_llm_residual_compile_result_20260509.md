# Main120 T2 Residual Compile Fallback - 2026-05-09

T2 reruns the T1 LLM plan-execute fallback only on the three T1 Spectre compile residuals.

Model setting: `mimo-v2.5-pro`, reasoning disabled, `max_tokens=4096`, temperature 0, top-p 1. Spectre audit used bridge profile `jin` with `max_workers=2`.

## Slice Result

| row | PASS | compile OK | compile fail | behavior fail | DUT compile fail | TB compile fail |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| T1 Spectre residual slice | 0/3 | 0/3 | 3/3 | 0/3 | 2 | 1 |
| T2 maintained EVAS slice | 0/3 | 1/3 | 2/3 | 1/3 | 2 | 0 |
| T2 Spectre validator slice | 0/3 | 0/3 | 3/3 | 0/3 | 2 | 1 |

## Cost

| tasks | api calls | input tokens | output tokens | total tokens | api elapsed s |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 3 | 6 | 21233 | 1931 | 23164 | 57.634 |

## Per Task

| task | T1 Spectre | T2 EVAS | T2 Spectre validator | Spectre log errors | tokens | api s |
| --- | --- | --- | --- | ---: | ---: | ---: |
| `vbm1_offset_comparator_e2e` | FAIL_TB_COMPILE | FAIL_SIM_CORRECTNESS | FAIL_TB_COMPILE | 0 | 8071 | 17.225 |
| `vbm1_resettable_integrator_bugfix` | FAIL_DUT_COMPILE | FAIL_DUT_COMPILE | FAIL_DUT_COMPILE | 1 | 7107 | 24.199 |
| `vbm1_vco_phase_integrator_bugfix` | FAIL_DUT_COMPILE | FAIL_DUT_COMPILE | FAIL_DUT_COMPILE | 3 | 7986 | 16.210 |

## Interpretation

- T2 did not improve the final Spectre validator status relative to the three T1 residuals.
- EVAS considered offset_comparator_e2e compile-closed, and the Spectre log shows 0 simulator errors, but the validator still labels it FAIL_TB_COMPILE because tran extraction/checker data is missing. This is an output-extraction/validation-label residual rather than an AHDL syntax compile residual.
- The two integrator bugfix tasks remain true Spectre AHDL compile failures due to generated use of non-Verilog-A $abstime_step, and vco additionally retains conditional transition.
- Blind T1-style LLM compile fallback appears insufficient for these final two integrator residuals; next action should be trace/memory plus targeted regeneration constraints or behavior/semantic repair, not more generic loop rounds.

## Remaining Actions

- `vbm1_offset_comparator_e2e`: inspect save/output extraction and validator labeling, because Spectre itself completes with 0 errors but the result is still `spectre_data_empty` / `tran_csv_missing`.
- `vbm1_resettable_integrator_bugfix`: forbid `$abstime_step` and require Spectre-compatible integration constructs, or route to targeted module regeneration.
- `vbm1_vco_phase_integrator_bugfix`: same `$abstime_step` issue plus remaining conditional `transition()`, so it needs a stricter Verilog-A operator skill or trace-guided regeneration.
