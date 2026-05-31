# EVAS/Spectre Mismatch Triage

Generated: 2026-05-29T07:35:34.802641+00:00

This report separates model failures, runner inconclusive rows, and
EVAS/Spectre semantic mismatches. L0 conformance rows are diagnostics
and are not part of the scored vaBench denominator.

## Summary

| Metric | Value |
| --- | ---: |
| total rows | 236 |
| strict dual pass rows | 55 |
| Spectre checker pass rows | 58 |
| EVAS PASS / Spectre FAIL rows | 0 |
| Spectre PASS / EVAS FAIL rows | 3 |
| parity gate rows | 0 |
| incomplete generation rows | 23 |
| runner inconclusive rows | 6 |

## Score Slices

| Slice | Rows | Strict dual pass | Pass rate | Meaning |
| --- | ---: | ---: | ---: | --- |
| `full_strict` | 236 | 55 | 23.31% | All scored rows. Incomplete generation and runner/output inconclusive rows are counted as failures. |
| `valid_candidate` | 206 | 55 | 26.70% | Rows with complete model artifacts and a reliable evaluator judgment. Syntax and behavior failure... |
| `behavior_ready` | 155 | 55 | 35.48% | Rows that reached the functional checker: strict dual pass plus model_behavior failure rows. |

## Difficulty Breakdown

| Difficulty | Rows | Strict dual pass | Strict rate | Valid candidates | Behavior-ready rows | Behavior-ready pass rate | Non-model/inconclusive |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `D1` | 36 | 13 | 36.11% | 34 | 29 | 44.83% | 2 |
| `D2` | 160 | 34 | 21.25% | 142 | 105 | 32.38% | 18 |
| `D3` | 40 | 8 | 20.00% | 30 | 21 | 38.10% | 10 |

## Form Breakdown

| Form | Rows | Strict dual pass | Strict rate | Valid candidates | Behavior-ready rows | Behavior-ready pass rate | Non-model/inconclusive |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bugfix` | 52 | 14 | 26.92% | 48 | 31 | 45.16% | 4 |
| `dut` | 52 | 16 | 30.77% | 50 | 30 | 53.33% | 2 |
| `e2e` | 66 | 7 | 10.61% | 46 | 36 | 19.44% | 20 |
| `tb` | 66 | 18 | 27.27% | 62 | 58 | 31.03% | 4 |

## Category Breakdown

| Category | Rows | Strict dual pass | Strict rate | Valid candidates | Behavior-ready rows | Behavior-ready pass rate | Non-model/inconclusive |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseband Signal Conditioning | 30 | 3 | 10.00% | 30 | 25 | 12.00% | 0 |
| Bias Reference and Power Management | 28 | 6 | 21.43% | 22 | 18 | 33.33% | 6 |
| Calibration, DEM, and Control | 26 | 4 | 15.38% | 23 | 19 | 21.05% | 3 |
| Comparator and Decision Circuits | 30 | 9 | 30.00% | 27 | 19 | 47.37% | 3 |
| Data Converter Models | 44 | 18 | 40.91% | 37 | 27 | 66.67% | 7 |
| PLL Clock and Timing Systems | 36 | 9 | 25.00% | 29 | 23 | 39.13% | 7 |
| RF and AFE Behavioral Macromodels | 24 | 1 | 4.17% | 21 | 11 | 9.09% | 3 |
| Sampling and Analog Memory | 18 | 5 | 27.78% | 17 | 13 | 38.46% | 1 |

## Axis Counts

| Axis | Count | Meaning |
| --- | ---: | --- |
| `evas_spectre_mismatch` | 3 | EVAS and Spectre disagree on the same candidate; reduce to L0 conformance. |
| `generation` | 23 | The model did not produce a complete usable artifact. |
| `model_behavior` | 100 | The candidate compiled and ran but failed the functional checker. |
| `model_dut_compile` | 36 | EVAS/static front-end rejected the generated Verilog-A DUT. |
| `model_spectre_ahdl_compile` | 6 | Spectre final judge rejected generated Verilog-A syntax/scope/operator usage. |
| `model_spectre_elab_or_topology` | 2 | Spectre final judge rejected parameter binding, range, or topology. |
| `model_spectre_tb_source` | 1 | Spectre final judge rejected generated testbench source/waveform syntax. |
| `model_tb_compile` | 3 | EVAS/static front-end rejected the generated Spectre testbench. |
| `pass` | 55 | Strict EVAS+Spectre pass. |
| `runner` | 6 | Evaluation infrastructure, staging, or external backend did not produce a reliable judgment. |
| `simulation_output_missing` | 1 | The run did not materialize required waveform artifacts such as tran.csv. |

## Failure Families

| Family | Axis | Count | Example | Evidence |
| --- | --- | ---: | --- | --- |
| `strict_dual_pass` | `pass` | 55 | `comparator_smoke` | {"common_window_s": [0.0, 3e-08], "max_abs_v": 1.795207543498628e-06, "max_nrmse": 7.884499852646... |
| `incomplete_generation` | `generation` | 23 | `adpll_ratio_hop_smoke` | no_code_extracted |
| `baseband_dynamic_behavior` | `model_behavior` | 22 | `vbm1_first_order_lowpass_bugfix` | FAIL_SIM_CORRECTNESS |
| `guarded_transition_contribution` | `model_dut_compile` | 17 | `flash_adc_3b_smoke` | ERROR (VACOMP-2143): "flash_adc_3b.va", line 32: Encountered the |
| `calibration_control_behavior` | `model_behavior` | 15 | `vbm1_cdac_calibration_bugfix` | FAIL_SIM_CORRECTNESS |
| `timing_or_pll_behavior` | `model_behavior` | 14 | `bbpd` | FAIL_SIM_CORRECTNESS |
| `reference_power_behavior` | `model_behavior` | 12 | `vbr1_l1_bandgap_reference_macro_model_e2e` | FAIL_SIM_CORRECTNESS |
| `decision_threshold_behavior` | `model_behavior` | 10 | `comparator_hysteresis_smoke` | FAIL_SIM_CORRECTNESS |
| `veriloga_embedded_declaration` | `model_dut_compile` | 10 | `vbm1_slew_rate_limiter_dut` | ERROR (VACOMP-1917): "slew_rate_limiter.va", line 17: Encountered an |
| `rf_afe_macro_behavior` | `model_behavior` | 10 | `vbr1_l1_limiting_amplifier_frontend_e2e` | FAIL_SIM_CORRECTNESS |
| `converter_code_or_transfer_behavior` | `model_behavior` | 9 | `flash_adc_mini_array_e2e` | spectre:observed_codes=0,1,2,3,4,5,6,7 expected_codes=0,1,2,3,4,5,6,7 comparator_mismatches=0 the... |
| `sample_hold_memory_behavior` | `model_behavior` | 8 | `vbr1_l1_acquisition_limited_sample_and_hold_bugfix` | FAIL_SIM_CORRECTNESS |
| `spectre_ahdl_syntax_scope_or_operator_reject` | `model_spectre_ahdl_compile` | 6 | `vbm1_debounce_latch_bugfix` | ERROR (VACOMP-2175): "integer above<<--? ; // 0: sig <= vth, 1: sig |
| `unsupported_event_variable_or_wait` | `model_dut_compile` | 4 | `vbm1_debounce_latch_e2e` | ERROR (VACOMP-2259): "event timer_event;<<--? " |
| `runner_or_staging_inconclusive` | `runner` | 3 | `bbpd_data_edge_alignment_smoke` | missing_required_stage_files: testbench.scs |
| `unsupported_math_or_cast_function` | `model_dut_compile` | 3 | `cdac_cal` | ERROR (VACOMP-2259): "vout_p = vcm + 0.5 * full_scale * ($itor<<--? |
| `spectre_pass_evas_fail_behavior` | `evas_spectre_mismatch` | 3 | `vbr1_l1_bandgap_reference_macro_model_dut` | FAIL_SIM_CORRECTNESS |
| `spectre_run_inconclusive` | `runner` | 3 | `vbr1_l1_bandgap_reference_macro_model_tb` | spectre:tran_spectre.csv missing or run failed |
| `other_compile_failure` | `model_dut_compile` | 3 | `vbr1_l1_hysteresis_comparator_dut` | tran.csv missing |
| `spectre_elaboration_parameter_or_topology_reject` | `model_spectre_elab_or_topology` | 2 | `vbr1_l1_bang_bang_phase_detector_bugfix` | FATAL: The following branches form a loop of rigid branches (shorts) when |
| `spectre_testbench_syntax` | `model_tb_compile` | 1 | `vbm1_strongarm_comparator_behavior_e2e` | ERROR (CMI-2204): |
| `spectre_tb_source_or_waveform_reject` | `model_spectre_tb_source` | 1 | `vbm1_strongarm_comparator_behavior_tb` | ERROR (CMI-2204): |
| `digital_verilog_in_veriloga` | `model_dut_compile` | 1 | `vbm1_thermometer_decoder_guarded_e2e` | ERROR (VACOMP-2259): "reg [<<--? 2:0] thermo;" |
| `simulation_output_missing_after_run` | `simulation_output_missing` | 1 | `vbr1_l1_hysteresis_comparator_tb` | tran.csv missing |

## Mismatch / Conformance Seeds

| Task | Direction/axis | Family | Suggested L0 action | Evidence |
| --- | --- | --- | --- | --- |
| `vbr1_l1_bandgap_reference_macro_model_dut` | Spectre PASS / EVAS FAIL | `spectre_pass_evas_fail_behavior` | minimize vbr1_l1_bandgap_reference_macro_model into L0 event-sampling conformance | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_log_rssi_power_detector_tb` | Spectre PASS / EVAS FAIL | `spectre_pass_evas_fail_behavior` | minimize vbr1_l1_log_rssi_power_detector into L0 event-sampling conformance | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_rf_mixer_downconverter_macro_tb` | Spectre PASS / EVAS FAIL | `spectre_pass_evas_fail_behavior` | minimize vbr1_l1_rf_mixer_downconverter_macro into L0 event-sampling conformance | FAIL_SIM_CORRECTNESS |

## Inputs

- `results/vabench-release-v1-baseline-dual-mimo-v2.5-pro-20260529-eventfix7-full236-dual`
- `results/vabench-release-v1-baseline-dual-mimo-v2.5-pro-20260529-prompt-change-rerun53-dual`
