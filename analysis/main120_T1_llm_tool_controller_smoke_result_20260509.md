# Main120 T1 LLM-Assisted Tool Controller Smoke - 2026-05-09

T1 is evaluated as a bounded fallback after S2: start from the 10 S2 Spectre compile-fail residuals, ask the LLM for a short compile-repair plan, execute one repair step, and accept/reject through EVAS before targeted Spectre audit.

Model setting: `mimo-v2.5-pro`, reasoning disabled, `max_tokens=4096`, temperature 0, top-p 1. Spectre audit used bridge profile `jin` with `max_workers=2`.

## Slice Result

| row | PASS | compile OK | compile fail | behavior fail | DUT compile fail | TB compile fail |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| S2 Spectre residual slice | 0/10 | 0/10 | 10/10 | 0/10 | 6 | 4 |
| T1 maintained EVAS slice | 0/10 | 8/10 | 2/10 | 8/10 | 2 | 0 |
| T1 Spectre slice | 1/10 | 7/10 | 3/10 | 6/10 | 2 | 1 |

## Main120 Splice Estimate

| row | PASS | compile OK | compile fail | behavior fail | DUT compile fail | TB compile fail |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| S2 full Spectre recomputed | 29/120 | 110/120 | 10/120 | 81/120 | 6 | 4 |
| S2 + T1 targeted splice | 30/120 | 117/120 | 3/120 | 87/120 | 2 | 1 |

This splice is not a substitute for a checkpoint full run, but it is the right targeted regression evidence after changing only these residual candidates.

## Cost

| tasks | api calls | input tokens | output tokens | reasoning tokens | total tokens | avg tokens/task | api elapsed s | avg api s/task |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 10 | 28 | 102426 | 9979 | 0 | 112405 | 11240.5 | 214.088 | 21.409 |

## Per Task

| task | S2 Spectre | T1 EVAS | T1 Spectre | rounds | api calls | tokens | api s |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: |
| `vbm1_debounce_latch_e2e` | FAIL_DUT_COMPILE | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS | 1 | 2 | 9194 | 20.338 |
| `vbm1_debounce_latch_tb` | FAIL_TB_COMPILE | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS | 1 | 2 | 7206 | 21.156 |
| `vbm1_edge_detector_e2e` | FAIL_DUT_COMPILE | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS | 2 | 4 | 16479 | 32.199 |
| `vbm1_edge_detector_tb` | FAIL_TB_COMPILE | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS | 2 | 4 | 14557 | 25.509 |
| `vbm1_lock_detector_tb` | FAIL_TB_COMPILE | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS | 2 | 4 | 14293 | 29.205 |
| `vbm1_offset_comparator_e2e` | FAIL_TB_COMPILE | FAIL_SIM_CORRECTNESS | FAIL_TB_COMPILE | 1 | 2 | 8141 | 15.319 |
| `vbm1_one_shot_timer_e2e` | FAIL_DUT_COMPILE | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS | 2 | 4 | 18473 | 36.660 |
| `vbm1_resettable_integrator_bugfix` | FAIL_DUT_COMPILE | FAIL_DUT_COMPILE | FAIL_DUT_COMPILE | 1 | 2 | 6984 | 10.247 |
| `vbm1_vco_phase_integrator_bugfix` | FAIL_DUT_COMPILE | FAIL_DUT_COMPILE | FAIL_DUT_COMPILE | 1 | 2 | 8018 | 12.970 |
| `vbm1_voltage_clamp_dut` | FAIL_DUT_COMPILE | FAIL_SIM_CORRECTNESS | PASS | 1 | 2 | 9060 | 10.485 |

## Interpretation

- T1 is not a replacement for S2; it is a fallback tool for S2 residual compile failures.
- On this residual slice, T1 converted Spectre compile failures from 10/10 to 3/10 and produced one Spectre PASS.
- The main benefit is open-ended compile repair exploration under validator accept/reject, at nonzero token/time cost.
- Remaining failures are now mostly behavior residuals plus three compile residuals, so the next work should split behavior tools from residual compile tools.

## Remaining Compile Residuals

- `vbm1_offset_comparator_e2e`: FAIL_TB_COMPILE - contract_save_pruned=removed:1,inserted:1,signals:4; generated_include=cmp_offset_ref.va; spectre_strict:preflight_pass; spectre_data_empty; spectre_tran_csv_missing
- `vbm1_resettable_integrator_bugfix`: FAIL_DUT_COMPILE - contract_save_pruned=removed:1,inserted:1,signals:3; spectre_strict:preflight_pass; spectre_data_missing_time; spectre_returncode=2
- `vbm1_vco_phase_integrator_bugfix`: FAIL_DUT_COMPILE - contract_save_pruned=removed:1,inserted:1,signals:3; spectre_strict:conditional_transition=vco_phase_integrator.va; spectre_data_missing_time; spectre_returncode=2

