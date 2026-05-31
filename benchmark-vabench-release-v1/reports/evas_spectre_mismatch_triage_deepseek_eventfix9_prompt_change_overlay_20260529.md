# EVAS/Spectre Mismatch Triage

Generated: 2026-05-29T07:35:34.918964+00:00

This report separates model failures, runner inconclusive rows, and
EVAS/Spectre semantic mismatches. L0 conformance rows are diagnostics
and are not part of the scored vaBench denominator.

## Summary

| Metric | Value |
| --- | ---: |
| total rows | 236 |
| strict dual pass rows | 66 |
| Spectre checker pass rows | 68 |
| EVAS PASS / Spectre FAIL rows | 0 |
| Spectre PASS / EVAS FAIL rows | 2 |
| parity gate rows | 0 |
| incomplete generation rows | 14 |
| runner inconclusive rows | 0 |

## Score Slices

| Slice | Rows | Strict dual pass | Pass rate | Meaning |
| --- | ---: | ---: | ---: | --- |
| `full_strict` | 236 | 66 | 27.97% | All scored rows. Incomplete generation and runner/output inconclusive rows are counted as failures. |
| `valid_candidate` | 222 | 66 | 29.73% | Rows with complete model artifacts and a reliable evaluator judgment. Syntax and behavior failure... |
| `behavior_ready` | 187 | 66 | 35.29% | Rows that reached the functional checker: strict dual pass plus model_behavior failure rows. |

## Difficulty Breakdown

| Difficulty | Rows | Strict dual pass | Strict rate | Valid candidates | Behavior-ready rows | Behavior-ready pass rate | Non-model/inconclusive |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `D1` | 36 | 19 | 52.78% | 35 | 32 | 59.38% | 1 |
| `D2` | 160 | 39 | 24.38% | 152 | 127 | 30.71% | 8 |
| `D3` | 40 | 8 | 20.00% | 35 | 28 | 28.57% | 5 |

## Form Breakdown

| Form | Rows | Strict dual pass | Strict rate | Valid candidates | Behavior-ready rows | Behavior-ready pass rate | Non-model/inconclusive |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bugfix` | 52 | 18 | 34.62% | 49 | 41 | 43.90% | 3 |
| `dut` | 52 | 23 | 44.23% | 50 | 40 | 57.50% | 2 |
| `e2e` | 66 | 10 | 15.15% | 58 | 42 | 23.81% | 8 |
| `tb` | 66 | 15 | 22.73% | 65 | 64 | 23.44% | 1 |

## Category Breakdown

| Category | Rows | Strict dual pass | Strict rate | Valid candidates | Behavior-ready rows | Behavior-ready pass rate | Non-model/inconclusive |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseband Signal Conditioning | 30 | 6 | 20.00% | 30 | 25 | 24.00% | 0 |
| Bias Reference and Power Management | 28 | 9 | 32.14% | 23 | 21 | 42.86% | 5 |
| Calibration, DEM, and Control | 26 | 1 | 3.85% | 26 | 21 | 4.76% | 0 |
| Comparator and Decision Circuits | 30 | 15 | 50.00% | 30 | 26 | 57.69% | 0 |
| Data Converter Models | 44 | 17 | 38.64% | 44 | 36 | 47.22% | 0 |
| PLL Clock and Timing Systems | 36 | 9 | 25.00% | 32 | 26 | 34.62% | 4 |
| RF and AFE Behavioral Macromodels | 24 | 5 | 20.83% | 20 | 15 | 33.33% | 4 |
| Sampling and Analog Memory | 18 | 4 | 22.22% | 17 | 17 | 23.53% | 1 |

## Axis Counts

| Axis | Count | Meaning |
| --- | ---: | --- |
| `evas_spectre_mismatch` | 2 | EVAS and Spectre disagree on the same candidate; reduce to L0 conformance. |
| `generation` | 14 | The model did not produce a complete usable artifact. |
| `model_behavior` | 121 | The candidate compiled and ran but failed the functional checker. |
| `model_dut_compile` | 27 | EVAS/static front-end rejected the generated Verilog-A DUT. |
| `model_spectre_ahdl_compile` | 2 | Spectre final judge rejected generated Verilog-A syntax/scope/operator usage. |
| `model_spectre_tb_source` | 2 | Spectre final judge rejected generated testbench source/waveform syntax. |
| `model_tb_compile` | 2 | EVAS/static front-end rejected the generated Spectre testbench. |
| `pass` | 66 | Strict EVAS+Spectre pass. |

## Failure Families

| Family | Axis | Count | Example | Evidence |
| --- | --- | ---: | --- | --- |
| `strict_dual_pass` | `pass` | 66 | `cdac_cal` | {"common_window_s": [0.0, 6.8e-08], "max_abs_v": 1.4987246884534677e-05, "max_nrmse": 2.250204650... |
| `veriloga_embedded_declaration` | `model_dut_compile` | 22 | `dwa_ptr_gen_smoke` | ERROR (VACOMP-1917): "dwa_ptr_gen.va", line 66: Encountered an embedded |
| `calibration_control_behavior` | `model_behavior` | 20 | `vbm1_cdac_calibration_bugfix` | FAIL_SIM_CORRECTNESS |
| `converter_code_or_transfer_behavior` | `model_behavior` | 19 | `flash_adc_3b_smoke` | FAIL_SIM_CORRECTNESS |
| `baseband_dynamic_behavior` | `model_behavior` | 19 | `vbm1_first_order_lowpass_e2e` | FAIL_SIM_CORRECTNESS |
| `timing_or_pll_behavior` | `model_behavior` | 17 | `bbpd_data_edge_alignment_smoke` | FAIL_SIM_CORRECTNESS |
| `incomplete_generation` | `generation` | 14 | `cppll_freq_step_reacquire_smoke` | no_code_extracted |
| `sample_hold_memory_behavior` | `model_behavior` | 13 | `vbr1_l1_acquisition_limited_sample_and_hold_bugfix` | FAIL_SIM_CORRECTNESS |
| `reference_power_behavior` | `model_behavior` | 12 | `vbr1_l1_bandgap_reference_macro_model_tb` | FAIL_SIM_CORRECTNESS |
| `decision_threshold_behavior` | `model_behavior` | 11 | `comparator_hysteresis_smoke` | FAIL_SIM_CORRECTNESS |
| `rf_afe_macro_behavior` | `model_behavior` | 10 | `vbr1_l1_limiting_amplifier_frontend_tb` | FAIL_SIM_CORRECTNESS |
| `spectre_ahdl_syntax_scope_or_operator_reject` | `model_spectre_ahdl_compile` | 2 | `flash_adc_mini_array_e2e` | ERROR (VACOMP-2212): "cmp0_t = V(vss)<<--? ; cmp1_t = V(vss); cmp2_t = |
| `unsupported_event_loop_form` | `model_dut_compile` | 2 | `vbm1_debounce_latch_e2e` | ERROR (VACOMP-2259): "timer<<--? t_arm;" |
| `spectre_tb_source_or_waveform_reject` | `model_spectre_tb_source` | 2 | `vbm1_simple_binary_voltage_dac_4b_e2e` | ERROR (CMI-2194): Vcode_0: Waveform type must be specified if any waveform |
| `spectre_pass_evas_fail_behavior` | `evas_spectre_mismatch` | 2 | `vbr1_l1_bias_voltage_generator_with_enable_trim_dut` | FAIL_SIM_CORRECTNESS |
| `guarded_transition_contribution` | `model_tb_compile` | 2 | `vbr1_l1_dwa_dem_encoder_bugfix` | ERROR (VACOMP-1192): "V(cell_en_o[i])<<--? <+ transition(target_cell[i] * |
| `unsupported_math_or_cast_function` | `model_dut_compile` | 1 | `adpll_ratio_hop_smoke` | ERROR (VACOMP-2259): "ratio_int = round(V(ratio_ctrl))<<--? ;" |
| `unsupported_event_variable_or_wait` | `model_dut_compile` | 1 | `bbpd` | tran.csv missing |
| `other_compile_failure` | `model_dut_compile` | 1 | `vbr1_l1_log_rssi_power_detector_bugfix` | ERROR (VACOMP-2259): "[<<--? BEGIN file: dut_fixed.va]" |

## Mismatch / Conformance Seeds

| Task | Direction/axis | Family | Suggested L0 action | Evidence |
| --- | --- | --- | --- | --- |
| `vbr1_l1_bias_voltage_generator_with_enable_trim_dut` | Spectre PASS / EVAS FAIL | `spectre_pass_evas_fail_behavior` | minimize vbr1_l1_bias_voltage_generator_with_enable_trim into L0 event-sampling conformance | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_rf_mixer_downconverter_macro_tb` | Spectre PASS / EVAS FAIL | `spectre_pass_evas_fail_behavior` | minimize vbr1_l1_rf_mixer_downconverter_macro into L0 event-sampling conformance | FAIL_SIM_CORRECTNESS |

## Inputs

- `results/vabench-release-v1-baseline-dual-deepseek-v4-pro-20260529-eventfix9-samecandidates-full236-dual`
- `results/vabench-release-v1-baseline-dual-deepseek-v4-pro-20260529-eventfix9-wrapper-v4-changed55-dual`
- `results/vabench-release-v1-baseline-dual-deepseek-v4-pro-20260529-eventfix9-wrapper-v5-include2-dual`
- `results/vabench-release-v1-baseline-dual-deepseek-v4-pro-20260529-prompt-change-rerun53-dual`
