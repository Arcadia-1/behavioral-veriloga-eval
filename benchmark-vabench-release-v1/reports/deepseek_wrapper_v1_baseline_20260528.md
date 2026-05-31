# DeepSeek Wrapper-v1 Baseline Rerun

Date: 2026-05-28

## Scope

- Benchmark: `vabench-release-v1`
- Score denominator: 236 core scored forms
- Model: `deepseek-v4-pro`
- Public prompt version: `public-contract-v3`
- Runner wrapper version: `release-runner-wrapper-v1`
- Generation output:
  `results/vabench-release-v1-baseline-minimax-deepseek-v4-pro-20260528-wrapper-v1-full`
- Dual judge output:
  `results/vabench-release-v1-baseline-dual-deepseek-v4-pro-20260528-wrapper-v1-full-dual-thu-wei`
- Spectre backend: `sui-direct`, host `thu-wei`

## EVAS-Filter Result

| Metric | Value |
| --- | ---: |
| selected scored forms | 236 |
| generated | 232 |
| no code extracted | 4 |
| EVAS pass | 54 / 236 |
| EVAS pass rate | 22.88% |

### EVAS Status Counts

| Status | Count |
| --- | ---: |
| PASS | 54 |
| FAIL_SIM_CORRECTNESS | 128 |
| FAIL_DUT_COMPILE | 35 |
| FAIL_TB_COMPILE | 14 |
| FAIL_INFRA | 5 |

### EVAS Pass By Form

| Form | Pass / Total | Pass Rate |
| --- | ---: | ---: |
| dut | 20 / 52 | 38.46% |
| bugfix | 14 / 52 | 26.92% |
| tb | 13 / 66 | 19.70% |
| e2e | 7 / 66 | 10.61% |

### No-Code Rows

All four no-code rows ended with `finish_reason=length` and empty raw response.

| Task | Form |
| --- | --- |
| `vbr1_l1_bang_bang_phase_detector` | bugfix |
| `vbr1_l1_clock_divider` | bugfix |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | e2e |
| `vbr1_l2_converter_front_end` | e2e |

## Spectre-Final Dual Judge

| Metric | Value |
| --- | ---: |
| selected scored forms | 236 |
| completed dual rows | 231 |
| skipped rows | 4 |
| runner error rows | 1 |
| Spectre final pass | 51 / 231 completed |
| clean EVAS/Spectre dual pass | 48 / 231 completed |
| EVAS PASS / Spectre FAIL | 4 |
| Spectre PASS / EVAS FAIL | 1 |

### Spectre Pass By Form

| Form | Spectre Pass / Total |
| --- | ---: |
| dut | 19 / 52 |
| bugfix | 12 / 52 |
| tb | 12 / 66 |
| e2e | 8 / 66 |

### Dual Status Counts

| Dual Status | Count |
| --- | ---: |
| PASS | 48 |
| FAIL_EVAS | 177 |
| FAIL_SPECTRE | 3 |
| FAIL_SPECTRE_BEHAVIOR | 1 |
| FAIL_PARITY | 2 |
| missing | 5 |

## Non-Completed Rows

- Skipped because generation produced no candidate files:
  - `vbr1_l1_bang_bang_phase_detector:bugfix`
  - `vbr1_l1_clock_divider:bugfix`
  - `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow:e2e`
  - `vbr1_l2_converter_front_end:e2e`
- Runner error:
  - `vbr1_l1_propagation_delay_comparator:dut`
  - EVAS timed out at 300 s in the full run.
  - A targeted retry with `timeout-s=900` also timed out, so this should be
    treated as an EVAS/runtime infrastructure timeout for this candidate, not a
    normal Spectre behavioral result.

## EVAS/Spectre Exceptions

| Task | Dual Status | EVAS | Spectre checker |
| --- | --- | --- | --- |
| `vbr1_l1_pfd_up_dn_logic:bugfix` | FAIL_SPECTRE | PASS | fail |
| `vbr1_l1_sar_logic:dut` | FAIL_SPECTRE | PASS | fail |
| `vbr1_l1_charge_pump_abstraction:bugfix` | FAIL_SPECTRE | PASS | fail |
| `vbr1_l1_threshold_comparator:tb` | FAIL_SPECTRE_BEHAVIOR | PASS | fail |
| `vbr1_l1_clocked_adc_quantizer:dut` | FAIL_PARITY | PASS | pass |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap:dut` | FAIL_PARITY | PASS | pass |
| `vbr1_l2_comparator_measurement_flow:e2e` | FAIL_EVAS | FAIL_SIM_CORRECTNESS | pass |

## Comparison Boundary

This run is the first full DeepSeek run using `release-runner-wrapper-v1`.
It should not be directly compared against older results unless the report
states the prompt/wrapper version difference.

Relative to the previous clean Spectre-final baseline reported as 46 / 236, the
new EVAS-filter count is 54 / 236 and the completed Spectre-final count is
51 / 231 completed rows. The remaining 5 rows are 4 no-code skips plus 1
repeatable EVAS timeout.
