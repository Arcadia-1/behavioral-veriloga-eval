# EVAS/Spectre Mismatch Triage

Generated: 2026-05-31T11:42:31.895294+00:00

This report separates model failures, runner inconclusive rows, and
EVAS/Spectre semantic mismatches. L0 conformance rows are diagnostics
and are not part of the scored vaBench denominator.

## Summary

| Metric | Value |
| --- | ---: |
| total rows | 236 |
| strict dual pass rows | 85 |
| Spectre checker pass rows | 87 |
| EVAS PASS / Spectre FAIL rows | 0 |
| Spectre PASS / EVAS FAIL rows | 0 |
| parity gate rows | 2 |
| incomplete generation rows | 2 |
| runner inconclusive rows | 0 |

## Score Slices

| Slice | Rows | Strict dual pass | Pass rate | Meaning |
| --- | ---: | ---: | ---: | --- |
| `full_strict` | 236 | 85 | 36.02% | All scored rows. Incomplete generation and runner/output inconclusive rows are counted as failures. |
| `valid_candidate` | 234 | 85 | 36.32% | Rows with complete model artifacts and a reliable evaluator judgment. Syntax and behavior failure... |
| `behavior_ready` | 153 | 85 | 55.56% | Rows that reached the functional checker: strict dual pass plus model_behavior failure rows. |

## Difficulty Breakdown

| Difficulty | Rows | Strict dual pass | Strict rate | Valid candidates | Behavior-ready rows | Behavior-ready pass rate | Non-model/inconclusive |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `D1` | 36 | 22 | 61.11% | 36 | 27 | 81.48% | 0 |
| `D2` | 160 | 48 | 30.00% | 158 | 101 | 47.52% | 2 |
| `D3` | 40 | 15 | 37.50% | 40 | 25 | 60.00% | 0 |

## Form Breakdown

| Form | Rows | Strict dual pass | Strict rate | Valid candidates | Behavior-ready rows | Behavior-ready pass rate | Non-model/inconclusive |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bugfix` | 52 | 37 | 71.15% | 51 | 48 | 77.08% | 1 |
| `dut` | 52 | 12 | 23.08% | 51 | 18 | 66.67% | 1 |
| `e2e` | 66 | 3 | 4.55% | 66 | 29 | 10.34% | 0 |
| `tb` | 66 | 33 | 50.00% | 66 | 58 | 56.90% | 0 |

## Category Breakdown

| Category | Rows | Strict dual pass | Strict rate | Valid candidates | Behavior-ready rows | Behavior-ready pass rate | Non-model/inconclusive |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseband Signal Conditioning | 30 | 11 | 36.67% | 30 | 20 | 55.00% | 0 |
| Bias Reference and Power Management | 28 | 9 | 32.14% | 28 | 15 | 60.00% | 0 |
| Calibration, DEM, and Control | 26 | 5 | 19.23% | 26 | 15 | 33.33% | 0 |
| Comparator and Decision Circuits | 30 | 16 | 53.33% | 29 | 21 | 76.19% | 1 |
| Data Converter Models | 44 | 19 | 43.18% | 44 | 30 | 63.33% | 0 |
| PLL Clock and Timing Systems | 36 | 10 | 27.78% | 35 | 21 | 47.62% | 1 |
| RF and AFE Behavioral Macromodels | 24 | 10 | 41.67% | 24 | 18 | 55.56% | 0 |
| Sampling and Analog Memory | 18 | 5 | 27.78% | 18 | 13 | 38.46% | 0 |

## Axis Counts

| Axis | Count | Meaning |
| --- | ---: | --- |
| `generation` | 2 | The model did not produce a complete usable artifact. |
| `model_behavior` | 68 | The candidate compiled and ran but failed the functional checker. |
| `model_dut_compile` | 52 | EVAS/static front-end rejected the generated Verilog-A DUT. |
| `model_spectre_ahdl_compile` | 19 | Spectre final judge rejected generated Verilog-A syntax/scope/operator usage. |
| `model_spectre_elab_or_topology` | 2 | Spectre final judge rejected parameter binding, range, or topology. |
| `model_spectre_tb_source` | 2 | Spectre final judge rejected generated testbench source/waveform syntax. |
| `model_tb_compile` | 4 | EVAS/static front-end rejected the generated Spectre testbench. |
| `parity` | 2 | Both sides may pass behavior, but waveform parity needs a conformance/checker-window audit. |
| `pass` | 85 | Strict EVAS+Spectre pass. |

## Failure Families

| Family | Axis | Count | Example | Evidence |
| --- | --- | ---: | --- | --- |
| `strict_dual_pass` | `pass` | 85 | `comparator_measurement_flow_smoke` | {"common_window_s": [0.0, 1e-07], "max_abs_v": 1.0, "max_nrmse": 0.004166666666666667, "max_relat... |
| `spectre_ahdl_syntax_scope_or_operator_reject` | `model_spectre_ahdl_compile` | 19 | `cppll_freq_step_reacquire_smoke` | ERROR (VACOMP-2212): "fb_period = $abstime - last_event_time_fb;<<--? " |
| `other_compile_failure` | `model_dut_compile` | 14 | `vbm1_first_order_lowpass_e2e` | ERROR (VACOMP-2259): "vout <+<<--? transition(state, 0, 500p, 500p);" |
| `veriloga_embedded_declaration` | `model_dut_compile` | 13 | `flash_adc_mini_array_e2e` | ERROR (VACOMP-1742): "real thresholds[7]<<--? ;" |
| `unsupported_event_variable_or_wait` | `model_dut_compile` | 13 | `pipeline_stage` | ERROR (VACOMP-2212): "@(posedge PHI1<<--? ) begin" |
| `guarded_transition_contribution` | `model_dut_compile` | 12 | `adpll_ratio_hop_smoke` | ERROR (VACOMP-1549): "dco_val = ~dco_val;<<--? " |
| `timing_or_pll_behavior` | `model_behavior` | 11 | `bbpd` | FAIL_SIM_CORRECTNESS |
| `converter_code_or_transfer_behavior` | `model_behavior` | 11 | `pipeline_adc_chain_e2e` | spectre:observed_codes=0 expected_codes=0 stage_bit_mismatches=0 final_concat_mismatches=0 final_... |
| `calibration_control_behavior` | `model_behavior` | 10 | `vbm1_cdac_calibration_e2e` | FAIL_SIM_CORRECTNESS |
| `baseband_dynamic_behavior` | `model_behavior` | 9 | `vbm1_first_order_lowpass_bugfix` | spectre:lowpass_samples=0.756,0.800,0.800,0.800 input_step=True monotonic=True response_fast_enou... |
| `sample_hold_memory_behavior` | `model_behavior` | 8 | `vbr1_l1_acquisition_limited_sample_and_hold_bugfix` | FAIL_SIM_CORRECTNESS |
| `rf_afe_macro_behavior` | `model_behavior` | 8 | `vbr1_l1_lna_gain_compression_macro_dut` | FAIL_SIM_CORRECTNESS |
| `reference_power_behavior` | `model_behavior` | 6 | `vbr1_l1_bandgap_reference_macro_model_bugfix` | spectre:bandgap_brownout_not_reset=0.550 |
| `decision_threshold_behavior` | `model_behavior` | 5 | `comparator_hysteresis_smoke` | FAIL_SIM_CORRECTNESS |
| `spectre_testbench_syntax` | `model_tb_compile` | 2 | `sar_adc_dac_weighted_8b_smoke` | ERROR (SFE-709): |
| `waveform_parity_gate` | `parity` | 2 | `vbm1_vco_phase_integrator_tb` | {"common_window_s": [0.0, 1.8e-07], "max_abs_v": 1.0, "max_nrmse": 0.3312767732565065, "max_relat... |
| `spectre_tb_source_or_waveform_reject` | `model_spectre_tb_source` | 2 | `vbr1_l1_calibration_deadband_controller_tb` | ERROR (CMI-2194): Vvin: Waveform type must be specified if any waveform |
| `incomplete_generation` | `generation` | 2 | `vbr1_l1_clock_divider_bugfix` | no_code_extracted |
| `spectre_elaboration_parameter_or_topology_reject` | `model_spectre_elab_or_topology` | 2 | `vbr1_l1_higher_order_filter_e2e` | spectre_failed rc=1 |
| `digital_verilog_in_veriloga` | `model_dut_compile` | 1 | `vbm1_sar_logic_4b_e2e` | ERROR (VACOMP-2259): "@(posedge(CLKS)<<--? ) begin" |
| `unsupported_event_loop_form` | `model_dut_compile` | 1 | `vbr1_l1_digital_phase_accumulator_with_modulo_wrap_dut` | ERROR (VACOMP-2189): "forever<<--? begin" |

## Mismatch / Conformance Seeds

| Task | Direction/axis | Family | Suggested L0 action | Evidence |
| --- | --- | --- | --- | --- |
| `vbm1_vco_phase_integrator_tb` | parity | `waveform_parity_gate` | minimize vbr1_l1_vco_phase_integrator into L0 waveform/checker-window conformance | {"common_window_s": [0.0, 1.8e-07], "max_abs_v": 1.0, "max_nrmse": 0.3312767732565065, "max_relat... |
| `vbr1_l1_ptat_ctat_reference_generator_tb` | parity | `waveform_parity_gate` | minimize vbr1_l1_ptat_ctat_reference_generator into L0 waveform/checker-window conformance | {"common_window_s": [0.0, 8e-08], "max_abs_v": 1.0, "max_nrmse": 0.3308238846211788, "max_relativ... |

## Inputs

- `results/vabench-release-v1-baseline-dual-mimo-v2.5-20260530-mimo25-full236-v1-dual`
- `results/vabench-release-v1-baseline-dual-mimo-v2.5-20260531-mimo25-mismatch7-suiwei-nested-v3-dual`
