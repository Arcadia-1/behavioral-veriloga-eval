# bpack48 Semantic Prompt-Checker-Gold Audit

**Date**: 2026-05-08

This audit checks whether public prompts expose the semantic contract that
checkers and gold harnesses later validate.  It is conservative and
heuristic: `WARN` means manual review or prompt cleanup is recommended, not
that the benchmark is invalid.

## Summary

- Tasks: `48`
- PASS: `5`
- WARN: `43`
- FAIL: `0`

## Issue Counts

| Issue | Count |
| --- | ---: |
| `duplicate_public_evaluation_contract` | 23 |
| `gold_tran_not_public` | 16 |
| `checker_source_task_not_named` | 9 |
| `checker_behavior_not_fully_named` | 4 |
| `tb_prompt_may_not_exclude_dut_generation` | 4 |
| `dut_only_prompt_contains_testbench_contract` | 3 |
| `dut_only_prompt_contains_two_block_deliverable` | 2 |

## Task Findings

| Status | Task | Pack | Form | Issues |
| --- | --- | --- | --- | --- |
| WARN | `bpack_analog_limiter_bugfix` | `analog_limiter` | `bugfix` | WARN:gold_tran_not_public=tran tran stop=120n maxstep=500p |
| WARN | `bpack_analog_limiter_e2e` | `analog_limiter` | `end-to-end` | WARN:gold_tran_not_public=tran tran stop=120n maxstep=500p |
| WARN | `bpack_analog_limiter_dut` | `analog_limiter` | `spec-to-va` | WARN:gold_tran_not_public=tran tran stop=120n maxstep=500p |
| WARN | `bpack_analog_limiter_tb` | `analog_limiter` | `tb-generation` | WARN:tb_prompt_may_not_exclude_dut_generation=missing explicit no-DUT constraint<br>WARN:gold_tran_not_public=tran tran stop=120n maxstep=500p |
| WARN | `bpack_binary_dac_4b_bugfix` | `binary_dac_4b` | `bugfix` | WARN:checker_source_task_not_named=dac_binary_clk_4b_smoke<br>WARN:duplicate_public_evaluation_contract=2 |
| WARN | `bpack_binary_dac_4b_e2e` | `binary_dac_4b` | `end-to-end` | WARN:checker_source_task_not_named=dac_binary_clk_4b_smoke |
| WARN | `bpack_binary_dac_4b_dut` | `binary_dac_4b` | `spec-to-va` | WARN:checker_source_task_not_named=dac_binary_clk_4b_smoke<br>WARN:duplicate_public_evaluation_contract=2 |
| WARN | `bpack_clock_divider_bugfix` | `clock_divider` | `bugfix` | WARN:checker_source_task_not_named=clk_div_smoke<br>WARN:duplicate_public_evaluation_contract=2 |
| WARN | `bpack_clock_divider_e2e` | `clock_divider` | `end-to-end` | WARN:checker_source_task_not_named=clk_div_smoke |
| WARN | `bpack_clock_divider_dut` | `clock_divider` | `spec-to-va` | WARN:checker_source_task_not_named=clk_div_smoke<br>WARN:duplicate_public_evaluation_contract=2 |
| WARN | `bpack_clock_divider_tb` | `clock_divider` | `tb-generation` | WARN:checker_source_task_not_named=clk_div_smoke<br>WARN:duplicate_public_evaluation_contract=2 |
| WARN | `bpack_dwa_pointer_bugfix` | `dwa_pointer` | `bugfix` | WARN:duplicate_public_evaluation_contract=3<br>WARN:checker_behavior_not_fully_named=dwa_rotation_correct: expected keywords ('dwa', 'rotation', 'pointer') |
| WARN | `bpack_dwa_pointer_e2e` | `dwa_pointer` | `end-to-end` | WARN:duplicate_public_evaluation_contract=2<br>WARN:checker_behavior_not_fully_named=dwa_rotation_correct: expected keywords ('dwa', 'rotation', 'pointer') |
| WARN | `bpack_dwa_pointer_dut` | `dwa_pointer` | `spec-to-va` | WARN:duplicate_public_evaluation_contract=3<br>WARN:dut_only_prompt_contains_testbench_contract=source spec retained TB contract<br>WARN:checker_behavior_not_fully_named=dwa_rotation_correct: expected keywords ('dwa', 'rotation', 'pointer') |
| WARN | `bpack_dwa_pointer_tb` | `dwa_pointer` | `tb-generation` | WARN:duplicate_public_evaluation_contract=3<br>WARN:checker_behavior_not_fully_named=dwa_rotation_correct: expected keywords ('dwa', 'rotation', 'pointer') |
| WARN | `bpack_flash_adc_3b_bugfix` | `flash_adc_3b` | `bugfix` | WARN:duplicate_public_evaluation_contract=3 |
| WARN | `bpack_flash_adc_3b_e2e` | `flash_adc_3b` | `end-to-end` | WARN:duplicate_public_evaluation_contract=2 |
| WARN | `bpack_flash_adc_3b_dut` | `flash_adc_3b` | `spec-to-va` | WARN:duplicate_public_evaluation_contract=3<br>WARN:dut_only_prompt_contains_testbench_contract=source spec retained TB contract<br>WARN:dut_only_prompt_contains_two_block_deliverable=conflicts with DUT-only wrapper |
| WARN | `bpack_flash_adc_3b_tb` | `flash_adc_3b` | `tb-generation` | WARN:duplicate_public_evaluation_contract=3 |
| WARN | `bpack_hysteresis_comparator_bugfix` | `hysteresis_comparator` | `bugfix` | WARN:duplicate_public_evaluation_contract=3 |
| WARN | `bpack_hysteresis_comparator_e2e` | `hysteresis_comparator` | `end-to-end` | WARN:duplicate_public_evaluation_contract=2 |
| WARN | `bpack_hysteresis_comparator_dut` | `hysteresis_comparator` | `spec-to-va` | WARN:duplicate_public_evaluation_contract=3<br>WARN:dut_only_prompt_contains_testbench_contract=source spec retained TB contract<br>WARN:dut_only_prompt_contains_two_block_deliverable=conflicts with DUT-only wrapper |
| WARN | `bpack_hysteresis_comparator_tb` | `hysteresis_comparator` | `tb-generation` | WARN:duplicate_public_evaluation_contract=3 |
| WARN | `bpack_pfd_updn_bugfix` | `pfd_updn` | `bugfix` | WARN:checker_source_task_not_named=swapped_pfd_outputs_bug |
| WARN | `bpack_pfd_updn_dut` | `pfd_updn` | `spec-to-va` | WARN:duplicate_public_evaluation_contract=2 |
| WARN | `bpack_pfd_updn_tb` | `pfd_updn` | `tb-generation` | WARN:duplicate_public_evaluation_contract=2 |
| WARN | `bpack_prbs7_lfsr_bugfix` | `prbs7_lfsr` | `bugfix` | WARN:duplicate_public_evaluation_contract=2 |
| WARN | `bpack_prbs7_lfsr_e2e` | `prbs7_lfsr` | `end-to-end` | WARN:duplicate_public_evaluation_contract=2 |
| WARN | `bpack_prbs7_lfsr_tb` | `prbs7_lfsr` | `tb-generation` | WARN:duplicate_public_evaluation_contract=2 |
| WARN | `bpack_pulse_stretcher_bugfix` | `pulse_stretcher` | `bugfix` | WARN:gold_tran_not_public=tran tran stop=140n maxstep=200p |
| WARN | `bpack_pulse_stretcher_e2e` | `pulse_stretcher` | `end-to-end` | WARN:gold_tran_not_public=tran tran stop=140n maxstep=200p |
| WARN | `bpack_pulse_stretcher_dut` | `pulse_stretcher` | `spec-to-va` | WARN:gold_tran_not_public=tran tran stop=140n maxstep=200p |
| WARN | `bpack_pulse_stretcher_tb` | `pulse_stretcher` | `tb-generation` | WARN:tb_prompt_may_not_exclude_dut_generation=missing explicit no-DUT constraint<br>WARN:gold_tran_not_public=tran tran stop=140n maxstep=200p |
| WARN | `bpack_sample_hold_bugfix` | `sample_hold` | `bugfix` | WARN:checker_source_task_not_named=wrong_edge_sample_hold_bug |
| WARN | `bpack_sample_hold_dut` | `sample_hold` | `spec-to-va` | WARN:duplicate_public_evaluation_contract=2 |
| WARN | `bpack_threshold_detector_bugfix` | `threshold_detector` | `bugfix` | WARN:gold_tran_not_public=tran tran stop=120n maxstep=500p |
| WARN | `bpack_threshold_detector_e2e` | `threshold_detector` | `end-to-end` | WARN:gold_tran_not_public=tran tran stop=120n maxstep=500p |
| WARN | `bpack_threshold_detector_dut` | `threshold_detector` | `spec-to-va` | WARN:gold_tran_not_public=tran tran stop=120n maxstep=500p |
| WARN | `bpack_threshold_detector_tb` | `threshold_detector` | `tb-generation` | WARN:tb_prompt_may_not_exclude_dut_generation=missing explicit no-DUT constraint<br>WARN:gold_tran_not_public=tran tran stop=120n maxstep=500p |
| WARN | `bpack_window_detector_bugfix` | `window_detector` | `bugfix` | WARN:gold_tran_not_public=tran tran stop=120n maxstep=500p |
| WARN | `bpack_window_detector_e2e` | `window_detector` | `end-to-end` | WARN:gold_tran_not_public=tran tran stop=120n maxstep=500p |
| WARN | `bpack_window_detector_dut` | `window_detector` | `spec-to-va` | WARN:gold_tran_not_public=tran tran stop=120n maxstep=500p |
| WARN | `bpack_window_detector_tb` | `window_detector` | `tb-generation` | WARN:tb_prompt_may_not_exclude_dut_generation=missing explicit no-DUT constraint<br>WARN:gold_tran_not_public=tran tran stop=120n maxstep=500p |
| PASS | `bpack_binary_dac_4b_tb` | `binary_dac_4b` | `tb-generation` | none |
| PASS | `bpack_pfd_updn_e2e` | `pfd_updn` | `end-to-end` | none |
| PASS | `bpack_prbs7_lfsr_dut` | `prbs7_lfsr` | `spec-to-va` | none |
| PASS | `bpack_sample_hold_e2e` | `sample_hold` | `end-to-end` | none |
| PASS | `bpack_sample_hold_tb` | `sample_hold` | `tb-generation` | none |

## Interpretation

- `PASS` means this heuristic found no prompt/checker/gold contract drift.
- `WARN` should be reviewed before promoting `bpack48` findings into a paper-facing claim.
- `FAIL` should be fixed or explicitly waived before using the affected task in a benchmark gate.
