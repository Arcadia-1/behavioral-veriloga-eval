# DeepSeek Wrapper-v4 Changed-Rerun Comparison

Generated: `2026-05-28T07:53:26.335711+00:00`

Scope: only the 55 rows whose wrapper-v1 candidates were attributed to
`prompt_contract_gap_old_wrapper`. This is not a full 236-row baseline.

## Headline

- old wrapper-v1 selected rows: 55
- old selected rows Spectre pass: 0/55
- wrapper-v4 generation: 55/55 generated
- wrapper-v4 EVAS initial pass: 7/55
- wrapper-v4 Spectre final pass: 7/55
- wrapper-v4 EVAS PASS / Spectre FAIL: 0
- wrapper-v4 Spectre PASS / EVAS FAIL: 0

## Old Wrapper-v1 Failure Roots

| Root cause | Count |
| --- | ---: |
| `missing_disciplines_vams_in_old_wrapper_candidate` | 28 |
| `invalid_or_incomplete_pwl_source_syntax` | 27 |

## New Wrapper-v4 Failure/Pass Status

| EVAS status | Count |
| --- | ---: |
| `FAIL_SIM_CORRECTNESS` | 37 |
| `PASS` | 7 |
| `FAIL_DUT_COMPILE` | 10 |
| `FAIL_TB_COMPILE` | 1 |

## New Passes By Form

| Form | Pass | Total |
| --- | ---: | ---: |
| `bugfix` | 1 | 11 |
| `dut` | 0 | 4 |
| `e2e` | 2 | 27 |
| `tb` | 4 | 13 |

## Rows Newly Passing Spectre

| Release task id | Form | Category |
| --- | --- | --- |
| `vbr1_l1_binary_weighted_voltage_dac:tb` | `tb` | Data Converter Models |
| `vbr1_l1_charge_pump_abstraction:bugfix` | `bugfix` | PLL Clock and Timing Systems |
| `vbr1_l1_pipeline_adc_stage:tb` | `tb` | Data Converter Models |
| `vbr1_l1_propagation_delay_comparator:e2e` | `e2e` | Comparator and Decision Circuits |
| `vbr1_l2_amplifier_filter_chain:e2e` | `e2e` | Baseband Signal Conditioning |
| `vbr1_l2_converter_static_linearity_measurement_flow:tb` | `tb` | Data Converter Models |
| `vbr1_l2_pipeline_adc_chain:tb` | `tb` | Data Converter Models |

## Interpretation

The wrapper-v4 contract repair converted 7 previously inconclusive old-wrapper
rows into EVAS/Spectre dual passes, with zero EVAS/Spectre pass/fail
mismatches on this rerun slice. The remaining failures should now be
attributed with the v4 candidates rather than carried over from the old
wrapper-v1 failure labels.
