# EVAS/Spectre Mismatch Triage

Generated: 2026-05-29T06:19:38.963131+00:00

This report separates model failures, runner inconclusive rows, and
EVAS/Spectre semantic mismatches. L0 conformance rows are diagnostics
and are not part of the scored vaBench denominator.

## Summary

| Metric | Value |
| --- | ---: |
| total rows | 472 |
| strict dual pass rows | 103 |
| Spectre checker pass rows | 103 |
| EVAS PASS / Spectre FAIL rows | 0 |
| Spectre PASS / EVAS FAIL rows | 0 |
| parity gate rows | 0 |
| incomplete generation rows | 25 |
| runner inconclusive rows | 3 |

## Score Slices

| Slice | Rows | Strict dual pass | Pass rate | Meaning |
| --- | ---: | ---: | ---: | --- |
| `full_strict` | 472 | 103 | 21.82% | All scored rows. Incomplete generation and runner/output inconclusive rows are counted as failures. |
| `valid_candidate` | 443 | 103 | 23.25% | Rows with complete model artifacts and a reliable evaluator judgment. Syntax and behavior failure... |
| `behavior_ready` | 317 | 103 | 32.49% | Rows that reached the functional checker: strict dual pass plus model_behavior failure rows. |

## Difficulty Breakdown

| Difficulty | Rows | Strict dual pass | Strict rate | Valid candidates | Behavior-ready rows | Behavior-ready pass rate | Non-model/inconclusive |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `D1` | 48 | 24 | 50.00% | 48 | 41 | 58.54% | 0 |
| `D2` | 360 | 67 | 18.61% | 342 | 242 | 27.69% | 18 |
| `D3` | 64 | 12 | 18.75% | 53 | 34 | 35.29% | 11 |

## Form Breakdown

| Form | Rows | Strict dual pass | Strict rate | Valid candidates | Behavior-ready rows | Behavior-ready pass rate | Non-model/inconclusive |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bugfix` | 104 | 24 | 23.08% | 100 | 66 | 36.36% | 4 |
| `dut` | 104 | 34 | 32.69% | 101 | 73 | 46.58% | 3 |
| `e2e` | 132 | 14 | 10.61% | 112 | 65 | 21.54% | 20 |
| `tb` | 132 | 31 | 23.48% | 130 | 113 | 27.43% | 2 |

## Category Breakdown

| Category | Rows | Strict dual pass | Strict rate | Valid candidates | Behavior-ready rows | Behavior-ready pass rate | Non-model/inconclusive |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseband Signal Conditioning | 60 | 8 | 13.33% | 60 | 44 | 18.18% | 0 |
| Bias Reference and Power Management | 56 | 4 | 7.14% | 55 | 38 | 10.53% | 1 |
| Calibration, DEM, and Control | 52 | 5 | 9.62% | 49 | 35 | 14.29% | 3 |
| Comparator and Decision Circuits | 60 | 23 | 38.33% | 57 | 43 | 53.49% | 3 |
| Data Converter Models | 88 | 31 | 35.23% | 81 | 53 | 58.49% | 7 |
| PLL Clock and Timing Systems | 72 | 17 | 23.61% | 61 | 45 | 37.78% | 11 |
| RF and AFE Behavioral Macromodels | 48 | 6 | 12.50% | 46 | 35 | 17.14% | 2 |
| Sampling and Analog Memory | 36 | 9 | 25.00% | 34 | 24 | 37.50% | 2 |

## Axis Counts

| Axis | Count | Meaning |
| --- | ---: | --- |
| `generation` | 25 | The model did not produce a complete usable artifact. |
| `model_behavior` | 214 | The candidate compiled and ran but failed the functional checker. |
| `model_dut_compile` | 94 | EVAS/static front-end rejected the generated Verilog-A DUT. |
| `model_spectre_ahdl_compile` | 8 | Spectre final judge rejected generated Verilog-A syntax/scope/operator usage. |
| `model_spectre_elab_or_topology` | 3 | Spectre final judge rejected parameter binding, range, or topology. |
| `model_spectre_tb_source` | 3 | Spectre final judge rejected generated testbench source/waveform syntax. |
| `model_tb_compile` | 18 | EVAS/static front-end rejected the generated Spectre testbench. |
| `pass` | 103 | Strict EVAS+Spectre pass. |
| `runner` | 3 | Evaluation infrastructure, staging, or external backend did not produce a reliable judgment. |
| `simulation_output_missing` | 1 | The run did not materialize required waveform artifacts such as tran.csv. |

## Failure Families

| Family | Axis | Count | Example | Evidence |
| --- | --- | ---: | --- | --- |
| `strict_dual_pass` | `pass` | 103 | `cdac_cal` | {"common_window_s": [0.0, 6.8e-08], "max_abs_v": 1.4987246884534677e-05, "max_nrmse": 2.250204650... |
| `baseband_dynamic_behavior` | `model_behavior` | 36 | `vbm1_first_order_lowpass_e2e` | FAIL_SIM_CORRECTNESS |
| `reference_power_behavior` | `model_behavior` | 34 | `vbr1_l1_bandgap_reference_macro_model_tb` | FAIL_SIM_CORRECTNESS |
| `calibration_control_behavior` | `model_behavior` | 30 | `vbm1_cdac_calibration_bugfix` | FAIL_SIM_CORRECTNESS |
| `spectre_testbench_syntax` | `model_dut_compile` | 29 | `cmp_delay_smoke` | ERROR (SFE-874): "cmp_delay_smoke__tb_cmp_delay_ref.scs" 11: Cannot run the |
| `other_compile_failure` | `model_dut_compile` | 29 | `dwa_ptr_gen_smoke` | ERROR (VACOMP-2259): "electrical clk_i<<--? , rst_ni;" |
| `rf_afe_macro_behavior` | `model_behavior` | 29 | `vbr1_l1_limiting_amplifier_frontend_dut` | FAIL_SIM_CORRECTNESS |
| `timing_or_pll_behavior` | `model_behavior` | 28 | `vbm1_lock_detector_bugfix` | FAIL_SIM_CORRECTNESS |
| `incomplete_generation` | `generation` | 25 | `cppll_freq_step_reacquire_smoke` | no_code_extracted |
| `veriloga_embedded_declaration` | `model_dut_compile` | 23 | `bbpd_data_edge_alignment_smoke` | ERROR (VACOMP-1917): "bbpd_data_edge_alignment_ref.va", line 41: |
| `converter_code_or_transfer_behavior` | `model_behavior` | 22 | `flash_adc_3b_smoke` | FAIL_SIM_CORRECTNESS |
| `decision_threshold_behavior` | `model_behavior` | 20 | `comparator_hysteresis_smoke` | FAIL_SIM_CORRECTNESS |
| `guarded_transition_contribution` | `model_tb_compile` | 16 | `vbr1_l1_dwa_dem_encoder_bugfix` | ERROR (VACOMP-1192): "V(cell_en_o[i])<<--? <+ transition(target_cell[i] * |
| `sample_hold_memory_behavior` | `model_behavior` | 15 | `vbr1_l1_acquisition_limited_sample_and_hold_tb` | FAIL_SIM_CORRECTNESS |
| `spectre_ahdl_syntax_scope_or_operator_reject` | `model_spectre_ahdl_compile` | 8 | `vbr1_l2_reference_startup_enable_flow_e2e` | ERROR (VACOMP-2212): "out_target =<<--? 0.0;" |
| `unsupported_event_variable_or_wait` | `model_dut_compile` | 7 | `bbpd` | tran.csv missing |
| `unsupported_math_or_cast_function` | `model_dut_compile` | 5 | `adpll_ratio_hop_smoke` | ERROR (VACOMP-2259): "ratio_int = round(V(ratio_ctrl))<<--? ;" |
| `spectre_tb_source_or_waveform_reject` | `model_spectre_tb_source` | 3 | `vbm1_thermometer_decoder_guarded_e2e` | FATAL (CMI-2212): Ven: Data is not given for bit source pattern. |
| `runner_or_staging_inconclusive` | `runner` | 3 | `bbpd_data_edge_alignment_smoke` | missing_required_stage_files: testbench.scs |
| `spectre_elaboration_parameter_or_topology_reject` | `model_spectre_elab_or_topology` | 3 | `vbr1_l1_bandgap_reference_macro_model_e2e` | (0) falls below lower bound in from range limit (0). |
| `unsupported_event_loop_form` | `model_dut_compile` | 2 | `vbm1_debounce_latch_e2e` | ERROR (VACOMP-2259): "timer<<--? t_arm;" |
| `digital_verilog_in_veriloga` | `model_dut_compile` | 1 | `vbm1_thermometer_decoder_guarded_e2e` | ERROR (VACOMP-2259): "reg [<<--? 2:0] thermo;" |
| `simulation_output_missing_after_run` | `simulation_output_missing` | 1 | `vbr1_l1_hysteresis_comparator_tb` | tran.csv missing |

## Mismatch / Conformance Seeds

No EVAS/Spectre mismatch rows were found in the selected inputs.

## Inputs

- `results/vabench-release-v1-baseline-dual-deepseek-v4-pro-20260529-eventfix9-samecandidates-full236-dual`
- `results/vabench-release-v1-baseline-dual-mimo-v2.5-pro-20260529-eventfix7-full236-dual`
