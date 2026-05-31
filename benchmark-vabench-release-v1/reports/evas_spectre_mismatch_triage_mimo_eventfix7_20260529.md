# EVAS/Spectre Mismatch Triage

Generated: 2026-05-29T06:19:38.637347+00:00

This report separates model failures, runner inconclusive rows, and
EVAS/Spectre semantic mismatches. L0 conformance rows are diagnostics
and are not part of the scored vaBench denominator.

## Summary

| Metric | Value |
| --- | ---: |
| total rows | 236 |
| strict dual pass rows | 51 |
| Spectre checker pass rows | 51 |
| EVAS PASS / Spectre FAIL rows | 0 |
| Spectre PASS / EVAS FAIL rows | 0 |
| parity gate rows | 0 |
| incomplete generation rows | 21 |
| runner inconclusive rows | 3 |

## Score Slices

| Slice | Rows | Strict dual pass | Pass rate | Meaning |
| --- | ---: | ---: | ---: | --- |
| `full_strict` | 236 | 51 | 21.61% | All scored rows. Incomplete generation and runner/output inconclusive rows are counted as failures. |
| `valid_candidate` | 211 | 51 | 24.17% | Rows with complete model artifacts and a reliable evaluator judgment. Syntax and behavior failure... |
| `behavior_ready` | 164 | 51 | 31.10% | Rows that reached the functional checker: strict dual pass plus model_behavior failure rows. |

## Difficulty Breakdown

| Difficulty | Rows | Strict dual pass | Strict rate | Valid candidates | Behavior-ready rows | Behavior-ready pass rate | Non-model/inconclusive |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `D1` | 24 | 11 | 45.83% | 24 | 22 | 50.00% | 0 |
| `D2` | 180 | 32 | 17.78% | 164 | 123 | 26.02% | 16 |
| `D3` | 32 | 8 | 25.00% | 23 | 19 | 42.11% | 9 |

## Form Breakdown

| Form | Rows | Strict dual pass | Strict rate | Valid candidates | Behavior-ready rows | Behavior-ready pass rate | Non-model/inconclusive |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bugfix` | 52 | 12 | 23.08% | 50 | 33 | 36.36% | 2 |
| `dut` | 52 | 15 | 28.85% | 49 | 33 | 45.45% | 3 |
| `e2e` | 66 | 6 | 9.09% | 48 | 38 | 15.79% | 18 |
| `tb` | 66 | 18 | 27.27% | 64 | 60 | 30.00% | 2 |

## Category Breakdown

| Category | Rows | Strict dual pass | Strict rate | Valid candidates | Behavior-ready rows | Behavior-ready pass rate | Non-model/inconclusive |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseband Signal Conditioning | 30 | 3 | 10.00% | 30 | 25 | 12.00% | 0 |
| Bias Reference and Power Management | 28 | 0 | 0.00% | 27 | 19 | 0.00% | 1 |
| Calibration, DEM, and Control | 26 | 4 | 15.38% | 23 | 19 | 21.05% | 3 |
| Comparator and Decision Circuits | 30 | 9 | 30.00% | 27 | 19 | 47.37% | 3 |
| Data Converter Models | 44 | 18 | 40.91% | 37 | 27 | 66.67% | 7 |
| PLL Clock and Timing Systems | 36 | 9 | 25.00% | 28 | 23 | 39.13% | 8 |
| RF and AFE Behavioral Macromodels | 24 | 3 | 12.50% | 22 | 19 | 15.79% | 2 |
| Sampling and Analog Memory | 18 | 5 | 27.78% | 17 | 13 | 38.46% | 1 |

## Axis Counts

| Axis | Count | Meaning |
| --- | ---: | --- |
| `generation` | 21 | The model did not produce a complete usable artifact. |
| `model_behavior` | 113 | The candidate compiled and ran but failed the functional checker. |
| `model_dut_compile` | 32 | EVAS/static front-end rejected the generated Verilog-A DUT. |
| `model_spectre_ahdl_compile` | 7 | Spectre final judge rejected generated Verilog-A syntax/scope/operator usage. |
| `model_spectre_elab_or_topology` | 3 | Spectre final judge rejected parameter binding, range, or topology. |
| `model_spectre_tb_source` | 2 | Spectre final judge rejected generated testbench source/waveform syntax. |
| `model_tb_compile` | 3 | EVAS/static front-end rejected the generated Spectre testbench. |
| `pass` | 51 | Strict EVAS+Spectre pass. |
| `runner` | 3 | Evaluation infrastructure, staging, or external backend did not produce a reliable judgment. |
| `simulation_output_missing` | 1 | The run did not materialize required waveform artifacts such as tran.csv. |

## Failure Families

| Family | Axis | Count | Example | Evidence |
| --- | --- | ---: | --- | --- |
| `strict_dual_pass` | `pass` | 51 | `comparator_smoke` | {"common_window_s": [0.0, 3e-08], "max_abs_v": 1.795207543498628e-06, "max_nrmse": 7.884499852646... |
| `baseband_dynamic_behavior` | `model_behavior` | 22 | `vbm1_first_order_lowpass_bugfix` | FAIL_SIM_CORRECTNESS |
| `incomplete_generation` | `generation` | 21 | `adpll_ratio_hop_smoke` | no_code_extracted |
| `reference_power_behavior` | `model_behavior` | 19 | `vbr1_l1_bandgap_reference_macro_model_bugfix` | FAIL_SIM_CORRECTNESS |
| `rf_afe_macro_behavior` | `model_behavior` | 16 | `vbr1_l1_limiting_amplifier_frontend_bugfix` | FAIL_SIM_CORRECTNESS |
| `guarded_transition_contribution` | `model_dut_compile` | 15 | `flash_adc_3b_smoke` | ERROR (VACOMP-2143): "flash_adc_3b.va", line 32: Encountered the |
| `calibration_control_behavior` | `model_behavior` | 15 | `vbm1_cdac_calibration_bugfix` | FAIL_SIM_CORRECTNESS |
| `timing_or_pll_behavior` | `model_behavior` | 14 | `bbpd` | FAIL_SIM_CORRECTNESS |
| `decision_threshold_behavior` | `model_behavior` | 10 | `comparator_hysteresis_smoke` | FAIL_SIM_CORRECTNESS |
| `converter_code_or_transfer_behavior` | `model_behavior` | 9 | `flash_adc_mini_array_e2e` | spectre:observed_codes=0,1,2,3,4,5,6,7 expected_codes=0,1,2,3,4,5,6,7 comparator_mismatches=0 the... |
| `veriloga_embedded_declaration` | `model_dut_compile` | 8 | `vbm1_slew_rate_limiter_dut` | ERROR (VACOMP-1917): "slew_rate_limiter.va", line 17: Encountered an |
| `sample_hold_memory_behavior` | `model_behavior` | 8 | `vbr1_l1_acquisition_limited_sample_and_hold_bugfix` | FAIL_SIM_CORRECTNESS |
| `spectre_ahdl_syntax_scope_or_operator_reject` | `model_spectre_ahdl_compile` | 7 | `vbm1_debounce_latch_bugfix` | ERROR (VACOMP-2175): "integer above<<--? ; // 0: sig <= vth, 1: sig |
| `unsupported_event_variable_or_wait` | `model_dut_compile` | 5 | `vbm1_debounce_latch_e2e` | ERROR (VACOMP-2259): "event timer_event;<<--? " |
| `runner_or_staging_inconclusive` | `runner` | 3 | `bbpd_data_edge_alignment_smoke` | missing_required_stage_files: testbench.scs |
| `spectre_elaboration_parameter_or_topology_reject` | `model_spectre_elab_or_topology` | 3 | `vbr1_l1_bandgap_reference_macro_model_e2e` | (0) falls below lower bound in from range limit (0). |
| `unsupported_math_or_cast_function` | `model_dut_compile` | 2 | `cdac_cal` | ERROR (VACOMP-2259): "vout_p = vcm + 0.5 * full_scale * ($itor<<--? |
| `spectre_testbench_syntax` | `model_tb_compile` | 2 | `vbm1_strongarm_comparator_behavior_e2e` | ERROR (CMI-2204): |
| `spectre_tb_source_or_waveform_reject` | `model_spectre_tb_source` | 2 | `vbm1_strongarm_comparator_behavior_tb` | ERROR (CMI-2204): |
| `other_compile_failure` | `model_dut_compile` | 2 | `vbr1_l1_hysteresis_comparator_dut` | tran.csv missing |
| `digital_verilog_in_veriloga` | `model_dut_compile` | 1 | `vbm1_thermometer_decoder_guarded_e2e` | ERROR (VACOMP-2259): "reg [<<--? 2:0] thermo;" |
| `simulation_output_missing_after_run` | `simulation_output_missing` | 1 | `vbr1_l1_hysteresis_comparator_tb` | tran.csv missing |

## Mismatch / Conformance Seeds

No EVAS/Spectre mismatch rows were found in the selected inputs.

## Inputs

- `results/vabench-release-v1-baseline-dual-mimo-v2.5-pro-20260529-eventfix7-full236-dual`
