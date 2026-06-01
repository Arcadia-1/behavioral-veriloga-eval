# MiMo 2.5-pro L2 Observability Affected Slice

Date: `2026-06-01`
Model: `mimo-v2.5-pro`

| Metric | Value |
| --- | ---: |
| selected scored forms | 8 |
| generated / incomplete | {'generated': 7, 'no_code_extracted': 1} |
| EVAS pass | 3 / 8 |
| Spectre final pass | 3 / 8 |
| completed dual | 7 |
| skipped | 1 |
| EVAS PASS / Spectre FAIL | 0 |
| Spectre PASS / EVAS FAIL | 0 |

## By Form

| Form | Total | EVAS Pass | Spectre Pass | Incomplete |
| --- | ---: | ---: | ---: | ---: |
| `e2e` | 4 | 0 | 0 | 1 |
| `tb` | 4 | 3 | 3 | 0 |

## Failure Rows

| Task | Form | Axis | Detail |
| --- | --- | --- | --- |
| `vbr1_l2_amplifier_filter_chain:e2e` | `e2e` | `behavior_or_compile_fail_evas` | FAIL_SIM_CORRECTNESS \| amp_filter_metric_not_preamp_target early=0.289 late=0.774 low=0.000 |
| `vbr1_l2_iq_downconversion_chain:e2e` | `e2e` | `behavior_or_compile_fail_evas` | FAIL_SIM_CORRECTNESS \| iq_positive_quadrature_missing i=0.180 q=0.180 |
| `vbr1_l2_reference_startup_enable_flow:e2e` | `e2e` | `behavior_or_compile_fail_evas` | FAIL_SIM_CORRECTNESS \| ref_startup_valid_metric_low=0.589 |
| `vbr1_l2_weighted_sar_adc_dac_loop:e2e` | `e2e` | `incomplete_generation` | missing_candidate_files |
| `vbr1_l2_weighted_sar_adc_dac_loop:tb` | `tb` | `behavior_or_compile_fail_evas` | FAIL_SIM_CORRECTNESS \| tran.csv missing |

## Claim Boundary

- This is an affected-slice regression check, not a replacement for the full 236-form model baseline.
- Spectre final judge is used for pass/fail; EVAS/Spectre mismatch count is reported separately.
- The skipped SAR e2e row remains in the selected denominator as incomplete generation.
