# EVAS/Spectre Mismatch Triage

Generated: 2026-05-29T06:19:38.742645+00:00

This report separates model failures, runner inconclusive rows, and
EVAS/Spectre semantic mismatches. L0 conformance rows are diagnostics
and are not part of the scored vaBench denominator.

## Summary

| Metric | Value |
| --- | ---: |
| total rows | 236 |
| strict dual pass rows | 59 |
| Spectre checker pass rows | 59 |
| EVAS PASS / Spectre FAIL rows | 0 |
| Spectre PASS / EVAS FAIL rows | 0 |
| parity gate rows | 0 |
| incomplete generation rows | 4 |
| runner inconclusive rows | 0 |

## Score Slices

| Slice | Rows | Strict dual pass | Pass rate | Meaning |
| --- | ---: | ---: | ---: | --- |
| `full_strict` | 236 | 59 | 25.00% | All scored rows. Incomplete generation and runner/output inconclusive rows are counted as failures. |
| `valid_candidate` | 232 | 59 | 25.43% | Rows with complete model artifacts and a reliable evaluator judgment. Syntax and behavior failure... |
| `behavior_ready` | 195 | 59 | 30.26% | Rows that reached the functional checker: strict dual pass plus model_behavior failure rows. |

## Difficulty Breakdown

| Difficulty | Rows | Strict dual pass | Strict rate | Valid candidates | Behavior-ready rows | Behavior-ready pass rate | Non-model/inconclusive |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `D1` | 24 | 14 | 58.33% | 24 | 22 | 63.64% | 0 |
| `D2` | 180 | 37 | 20.56% | 178 | 150 | 24.67% | 2 |
| `D3` | 32 | 8 | 25.00% | 30 | 23 | 34.78% | 2 |

## Form Breakdown

| Form | Rows | Strict dual pass | Strict rate | Valid candidates | Behavior-ready rows | Behavior-ready pass rate | Non-model/inconclusive |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bugfix` | 52 | 13 | 25.00% | 50 | 41 | 31.71% | 2 |
| `dut` | 52 | 19 | 36.54% | 52 | 42 | 45.24% | 0 |
| `e2e` | 66 | 10 | 15.15% | 64 | 46 | 21.74% | 2 |
| `tb` | 66 | 17 | 25.76% | 66 | 66 | 25.76% | 0 |

## Category Breakdown

| Category | Rows | Strict dual pass | Strict rate | Valid candidates | Behavior-ready rows | Behavior-ready pass rate | Non-model/inconclusive |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseband Signal Conditioning | 30 | 6 | 20.00% | 30 | 25 | 24.00% | 0 |
| Bias Reference and Power Management | 28 | 4 | 14.29% | 28 | 23 | 17.39% | 0 |
| Calibration, DEM, and Control | 26 | 1 | 3.85% | 26 | 21 | 4.76% | 0 |
| Comparator and Decision Circuits | 30 | 15 | 50.00% | 30 | 26 | 57.69% | 0 |
| Data Converter Models | 44 | 17 | 38.64% | 44 | 36 | 47.22% | 0 |
| PLL Clock and Timing Systems | 36 | 9 | 25.00% | 33 | 27 | 33.33% | 3 |
| RF and AFE Behavioral Macromodels | 24 | 3 | 12.50% | 24 | 20 | 15.00% | 0 |
| Sampling and Analog Memory | 18 | 4 | 22.22% | 17 | 17 | 23.53% | 1 |

## Axis Counts

| Axis | Count | Meaning |
| --- | ---: | --- |
| `generation` | 4 | The model did not produce a complete usable artifact. |
| `model_behavior` | 136 | The candidate compiled and ran but failed the functional checker. |
| `model_dut_compile` | 29 | EVAS/static front-end rejected the generated Verilog-A DUT. |
| `model_spectre_ahdl_compile` | 4 | Spectre final judge rejected generated Verilog-A syntax/scope/operator usage. |
| `model_spectre_tb_source` | 2 | Spectre final judge rejected generated testbench source/waveform syntax. |
| `model_tb_compile` | 2 | EVAS/static front-end rejected the generated Spectre testbench. |
| `pass` | 59 | Strict EVAS+Spectre pass. |

## Failure Families

| Family | Axis | Count | Example | Evidence |
| --- | --- | ---: | --- | --- |
| `strict_dual_pass` | `pass` | 59 | `cdac_cal` | {"common_window_s": [0.0, 6.8e-08], "max_abs_v": 1.4987246884534677e-05, "max_nrmse": 2.250204650... |
| `veriloga_embedded_declaration` | `model_dut_compile` | 21 | `dwa_ptr_gen_smoke` | ERROR (VACOMP-1917): "dwa_ptr_gen.va", line 66: Encountered an embedded |
| `calibration_control_behavior` | `model_behavior` | 20 | `vbm1_cdac_calibration_bugfix` | FAIL_SIM_CORRECTNESS |
| `converter_code_or_transfer_behavior` | `model_behavior` | 19 | `flash_adc_3b_smoke` | FAIL_SIM_CORRECTNESS |
| `baseband_dynamic_behavior` | `model_behavior` | 19 | `vbm1_first_order_lowpass_e2e` | FAIL_SIM_CORRECTNESS |
| `reference_power_behavior` | `model_behavior` | 19 | `vbr1_l1_bandgap_reference_macro_model_e2e` | FAIL_SIM_CORRECTNESS |
| `timing_or_pll_behavior` | `model_behavior` | 18 | `bbpd_data_edge_alignment_smoke` | FAIL_SIM_CORRECTNESS |
| `rf_afe_macro_behavior` | `model_behavior` | 17 | `vbr1_l1_limiting_amplifier_frontend_dut` | FAIL_SIM_CORRECTNESS |
| `sample_hold_memory_behavior` | `model_behavior` | 13 | `vbr1_l1_acquisition_limited_sample_and_hold_bugfix` | FAIL_SIM_CORRECTNESS |
| `decision_threshold_behavior` | `model_behavior` | 11 | `comparator_hysteresis_smoke` | FAIL_SIM_CORRECTNESS |
| `incomplete_generation` | `generation` | 4 | `cppll_freq_step_reacquire_smoke` | no_code_extracted |
| `spectre_ahdl_syntax_scope_or_operator_reject` | `model_spectre_ahdl_compile` | 4 | `flash_adc_mini_array_e2e` | ERROR (VACOMP-2212): "cmp0_t = V(vss)<<--? ; cmp1_t = V(vss); cmp2_t = |
| `unsupported_math_or_cast_function` | `model_dut_compile` | 3 | `adpll_ratio_hop_smoke` | ERROR (VACOMP-2259): "ratio_int = round(V(ratio_ctrl))<<--? ;" |
| `unsupported_event_variable_or_wait` | `model_dut_compile` | 2 | `bbpd` | tran.csv missing |
| `unsupported_event_loop_form` | `model_dut_compile` | 2 | `vbm1_debounce_latch_e2e` | ERROR (VACOMP-2259): "timer<<--? t_arm;" |
| `spectre_tb_source_or_waveform_reject` | `model_spectre_tb_source` | 2 | `vbm1_simple_binary_voltage_dac_4b_e2e` | ERROR (CMI-2194): Vcode_0: Waveform type must be specified if any waveform |
| `guarded_transition_contribution` | `model_tb_compile` | 2 | `vbr1_l1_dwa_dem_encoder_bugfix` | ERROR (VACOMP-1192): "V(cell_en_o[i])<<--? <+ transition(target_cell[i] * |
| `other_compile_failure` | `model_dut_compile` | 1 | `vbr1_l1_bias_voltage_generator_with_enable_trim_e2e` | tran.csv missing |

## Mismatch / Conformance Seeds

No EVAS/Spectre mismatch rows were found in the selected inputs.

## Inputs

- `results/vabench-release-v1-baseline-dual-deepseek-v4-pro-20260529-eventfix9-samecandidates-full236-dual`
- `results/vabench-release-v1-baseline-dual-deepseek-v4-pro-20260529-eventfix9-wrapper-v4-changed55-dual`
- `results/vabench-release-v1-baseline-dual-deepseek-v4-pro-20260529-eventfix9-wrapper-v5-include2-dual`
