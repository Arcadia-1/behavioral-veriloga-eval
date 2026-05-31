# EVAS/Spectre Mismatch Triage

Generated: 2026-05-31T20:08:12.703110+00:00

This report separates model failures, runner inconclusive rows, and
EVAS/Spectre semantic mismatches. L0 conformance rows are diagnostics
and are not part of the scored vaBench denominator.

## Summary

| Metric | Value |
| --- | ---: |
| total rows | 236 |
| strict dual pass rows | 92 |
| Spectre checker pass rows | 92 |
| EVAS PASS / Spectre FAIL rows | 0 |
| Spectre PASS / EVAS FAIL rows | 0 |
| parity gate rows | 0 |
| incomplete generation rows | 2 |
| runner inconclusive rows | 0 |

## Score Slices

| Slice | Rows | Strict dual pass | Pass rate | Meaning |
| --- | ---: | ---: | ---: | --- |
| `full_strict` | 236 | 92 | 38.98% | All scored rows. Incomplete generation and runner/output inconclusive rows are counted as failures. |
| `valid_candidate` | 234 | 92 | 39.32% | Rows with complete model artifacts and a reliable evaluator judgment. Syntax and behavior failure... |
| `behavior_ready` | 150 | 92 | 61.33% | Rows that reached the functional checker: strict dual pass plus model_behavior failure rows. |

## Difficulty Breakdown

| Difficulty | Rows | Strict dual pass | Strict rate | Valid candidates | Behavior-ready rows | Behavior-ready pass rate | Non-model/inconclusive |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `D1` | 36 | 25 | 69.44% | 36 | 28 | 89.29% | 0 |
| `D2` | 160 | 53 | 33.12% | 159 | 99 | 53.54% | 1 |
| `D3` | 40 | 14 | 35.00% | 39 | 23 | 60.87% | 1 |

## Form Breakdown

| Form | Rows | Strict dual pass | Strict rate | Valid candidates | Behavior-ready rows | Behavior-ready pass rate | Non-model/inconclusive |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bugfix` | 52 | 43 | 82.69% | 52 | 50 | 86.00% | 0 |
| `dut` | 52 | 10 | 19.23% | 51 | 19 | 52.63% | 1 |
| `e2e` | 66 | 8 | 12.12% | 65 | 21 | 38.10% | 1 |
| `tb` | 66 | 31 | 46.97% | 66 | 60 | 51.67% | 0 |

## Category Breakdown

| Category | Rows | Strict dual pass | Strict rate | Valid candidates | Behavior-ready rows | Behavior-ready pass rate | Non-model/inconclusive |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseband Signal Conditioning | 30 | 14 | 46.67% | 30 | 22 | 63.64% | 0 |
| Bias Reference and Power Management | 28 | 15 | 53.57% | 28 | 20 | 75.00% | 0 |
| Calibration, DEM, and Control | 26 | 8 | 30.77% | 25 | 16 | 50.00% | 1 |
| Comparator and Decision Circuits | 30 | 14 | 46.67% | 30 | 19 | 73.68% | 0 |
| Data Converter Models | 44 | 17 | 38.64% | 44 | 28 | 60.71% | 0 |
| PLL Clock and Timing Systems | 36 | 11 | 30.56% | 35 | 22 | 50.00% | 1 |
| RF and AFE Behavioral Macromodels | 24 | 9 | 37.50% | 24 | 14 | 64.29% | 0 |
| Sampling and Analog Memory | 18 | 4 | 22.22% | 18 | 9 | 44.44% | 0 |

## Axis Counts

| Axis | Count | Meaning |
| --- | ---: | --- |
| `generation` | 2 | The model did not produce a complete usable artifact. |
| `model_behavior` | 58 | The candidate compiled and ran but failed the functional checker. |
| `model_dut_compile` | 63 | EVAS/static front-end rejected the generated Verilog-A DUT. |
| `model_spectre_ahdl_compile` | 14 | Spectre final judge rejected generated Verilog-A syntax/scope/operator usage. |
| `model_spectre_elab_or_topology` | 2 | Spectre final judge rejected parameter binding, range, or topology. |
| `model_spectre_tb_source` | 1 | Spectre final judge rejected generated testbench source/waveform syntax. |
| `model_tb_compile` | 4 | EVAS/static front-end rejected the generated Spectre testbench. |
| `pass` | 92 | Strict EVAS+Spectre pass. |

## Failure Families

| Family | Axis | Count | Example | Evidence |
| --- | --- | ---: | --- | --- |
| `strict_dual_pass` | `pass` | 92 | `comparator_smoke` | {"common_window_s": [0.0, 3e-08], "max_abs_v": 1.0, "max_nrmse": 0.009166666666666667, "max_relat... |
| `other_compile_failure` | `model_dut_compile` | 17 | `cdac_cal` | ERROR (VACOMP-2212): "d_vec[<<--? 1] = (V(D1) > (vdd_val + vss_val)/2.0) ? |
| `unsupported_event_variable_or_wait` | `model_dut_compile` | 17 | `pipeline_stage` | ERROR (VACOMP-2212): "@(posedge PHI1<<--? ) begin" |
| `guarded_transition_contribution` | `model_dut_compile` | 15 | `cmp_delay_smoke` | ERROR (VACOMP-1917): "cmp_delay.va", line 28: Encountered an embedded |
| `spectre_ahdl_syntax_scope_or_operator_reject` | `model_spectre_ahdl_compile` | 14 | `bbpd_data_edge_alignment_smoke` | ERROR (VACOMP-1563): "retimed_target = vss;<<--? " |
| `timing_or_pll_behavior` | `model_behavior` | 11 | `bbpd` | FAIL_SIM_CORRECTNESS |
| `converter_code_or_transfer_behavior` | `model_behavior` | 11 | `vbm1_sar_logic_4b_dut` | FAIL_SIM_CORRECTNESS |
| `veriloga_embedded_declaration` | `model_tb_compile` | 10 | `sar_adc_dac_weighted_8b_smoke` | ERROR (VACOMP-1917): "dac_weighted_8b.va", line 11: Encountered an embedded |
| `calibration_control_behavior` | `model_behavior` | 8 | `vbm1_cdac_calibration_tb` | FAIL_SIM_CORRECTNESS |
| `baseband_dynamic_behavior` | `model_behavior` | 8 | `vbm1_resettable_integrator_e2e` | FAIL_SIM_CORRECTNESS |
| `decision_threshold_behavior` | `model_behavior` | 5 | `vbm1_debounce_latch_tb` | FAIL_SIM_CORRECTNESS |
| `sample_hold_memory_behavior` | `model_behavior` | 5 | `vbr1_l1_acquisition_limited_sample_and_hold_tb` | FAIL_SIM_CORRECTNESS |
| `reference_power_behavior` | `model_behavior` | 5 | `vbr1_l1_bandgap_reference_macro_model_tb` | FAIL_SIM_CORRECTNESS |
| `rf_afe_macro_behavior` | `model_behavior` | 5 | `vbr1_l1_lna_gain_compression_macro_dut` | FAIL_SIM_CORRECTNESS |
| `unsupported_event_loop_form` | `model_dut_compile` | 4 | `adpll_ratio_hop_smoke` | ERROR (VACOMP-2259): "initial<<--? begin" |
| `spectre_testbench_syntax` | `model_dut_compile` | 3 | `vbm1_gain_trim_controller_tb` | tran.csv missing |
| `incomplete_generation` | `generation` | 2 | `vbm1_pfd_reset_race_dut` | no_code_extracted |
| `spectre_elaboration_parameter_or_topology_reject` | `model_spectre_elab_or_topology` | 2 | `vbm1_resettable_integrator_dut` | below lower bound in from range limit (0). |
| `spectre_tb_source_or_waveform_reject` | `model_spectre_tb_source` | 1 | `vbr1_l1_rf_mixer_downconverter_macro_tb` | ERROR (CMI-2194): Vvin: Waveform type must be specified if any waveform |
| `digital_verilog_in_veriloga` | `model_dut_compile` | 1 | `vbr1_l2_iq_downconversion_chain_e2e` | ERROR (VACOMP-1552): "@(cross(rst - 0.45,<<--? 1)) begin" |

## Mismatch / Conformance Seeds

No EVAS/Spectre mismatch rows were found in the selected inputs.

## Inputs

- `results/vabench-release-v1-baseline-dual-mimo-v2.5-20260601-full236-highout32k-currentevas-v4-dual`
