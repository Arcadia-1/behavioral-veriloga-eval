# EVAS/Spectre Mismatch Triage

Generated: 2026-05-31T11:39:48.481427+00:00

This report separates model failures, runner inconclusive rows, and
EVAS/Spectre semantic mismatches. L0 conformance rows are diagnostics
and are not part of the scored vaBench denominator.

## Summary

| Metric | Value |
| --- | ---: |
| total rows | 236 |
| strict dual pass rows | 110 |
| Spectre checker pass rows | 113 |
| EVAS PASS / Spectre FAIL rows | 5 |
| Spectre PASS / EVAS FAIL rows | 2 |
| parity gate rows | 1 |
| incomplete generation rows | 8 |
| runner inconclusive rows | 1 |

## Score Slices

| Slice | Rows | Strict dual pass | Pass rate | Meaning |
| --- | ---: | ---: | ---: | --- |
| `full_strict` | 236 | 110 | 46.61% | All scored rows. Incomplete generation and runner/output inconclusive rows are counted as failures. |
| `valid_candidate` | 227 | 110 | 48.46% | Rows with complete model artifacts and a reliable evaluator judgment. Syntax and behavior failure... |
| `behavior_ready` | 188 | 110 | 58.51% | Rows that reached the functional checker: strict dual pass plus model_behavior failure rows. |

## Difficulty Breakdown

| Difficulty | Rows | Strict dual pass | Strict rate | Valid candidates | Behavior-ready rows | Behavior-ready pass rate | Non-model/inconclusive |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `D1` | 36 | 33 | 91.67% | 36 | 33 | 100.00% | 0 |
| `D2` | 160 | 62 | 38.75% | 155 | 128 | 48.44% | 5 |
| `D3` | 40 | 15 | 37.50% | 36 | 27 | 55.56% | 4 |

## Form Breakdown

| Form | Rows | Strict dual pass | Strict rate | Valid candidates | Behavior-ready rows | Behavior-ready pass rate | Non-model/inconclusive |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bugfix` | 52 | 42 | 80.77% | 51 | 51 | 82.35% | 1 |
| `dut` | 52 | 20 | 38.46% | 52 | 36 | 55.56% | 0 |
| `e2e` | 66 | 16 | 24.24% | 60 | 46 | 34.78% | 6 |
| `tb` | 66 | 32 | 48.48% | 64 | 55 | 58.18% | 2 |

## Category Breakdown

| Category | Rows | Strict dual pass | Strict rate | Valid candidates | Behavior-ready rows | Behavior-ready pass rate | Non-model/inconclusive |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseband Signal Conditioning | 30 | 18 | 60.00% | 30 | 23 | 78.26% | 0 |
| Bias Reference and Power Management | 28 | 13 | 46.43% | 28 | 24 | 54.17% | 0 |
| Calibration, DEM, and Control | 26 | 6 | 23.08% | 24 | 21 | 28.57% | 2 |
| Comparator and Decision Circuits | 30 | 20 | 66.67% | 29 | 26 | 76.92% | 1 |
| Data Converter Models | 44 | 20 | 45.45% | 43 | 35 | 57.14% | 1 |
| PLL Clock and Timing Systems | 36 | 14 | 38.89% | 31 | 25 | 56.00% | 5 |
| RF and AFE Behavioral Macromodels | 24 | 12 | 50.00% | 24 | 20 | 60.00% | 0 |
| Sampling and Analog Memory | 18 | 7 | 38.89% | 18 | 14 | 50.00% | 0 |

## Axis Counts

| Axis | Count | Meaning |
| --- | ---: | --- |
| `evas_spectre_mismatch` | 7 | EVAS and Spectre disagree on the same candidate; reduce to L0 conformance. |
| `generation` | 8 | The model did not produce a complete usable artifact. |
| `model_behavior` | 78 | The candidate compiled and ran but failed the functional checker. |
| `model_dut_compile` | 24 | EVAS/static front-end rejected the generated Verilog-A DUT. |
| `model_spectre_ahdl_compile` | 2 | Spectre final judge rejected generated Verilog-A syntax/scope/operator usage. |
| `model_spectre_elab_or_topology` | 2 | Spectre final judge rejected parameter binding, range, or topology. |
| `model_spectre_tb_source` | 2 | Spectre final judge rejected generated testbench source/waveform syntax. |
| `model_tb_compile` | 1 | EVAS/static front-end rejected the generated Spectre testbench. |
| `parity` | 1 | Both sides may pass behavior, but waveform parity needs a conformance/checker-window audit. |
| `pass` | 110 | Strict EVAS+Spectre pass. |
| `runner` | 1 | Evaluation infrastructure, staging, or external backend did not produce a reliable judgment. |

## Failure Families

| Family | Axis | Count | Example | Evidence |
| --- | --- | ---: | --- | --- |
| `strict_dual_pass` | `pass` | 110 | `cdac_cal` | {"common_window_s": [0.0, 6.8e-08], "max_abs_v": 7.538062663736689e-06, "max_nrmse": 1.5137141323... |
| `calibration_control_behavior` | `model_behavior` | 15 | `vbm1_cdac_calibration_e2e` | FAIL_SIM_CORRECTNESS |
| `converter_code_or_transfer_behavior` | `model_behavior` | 15 | `vbm1_sar_logic_4b_dut` | FAIL_SIM_CORRECTNESS |
| `timing_or_pll_behavior` | `model_behavior` | 11 | `bbpd` | FAIL_SIM_CORRECTNESS |
| `reference_power_behavior` | `model_behavior` | 11 | `vbr1_l1_bandgap_reference_macro_model_bugfix` | spectre:bandgap_brownout_not_reset=0.550 |
| `incomplete_generation` | `generation` | 8 | `adpll_ratio_hop_smoke` | no_code_extracted |
| `guarded_transition_contribution` | `model_dut_compile` | 8 | `phase_accumulator_timer_wrap_smoke` | ERROR (VACOMP-2143): "phase_accumulator_timer_wrap_ref.va", line 34: |
| `rf_afe_macro_behavior` | `model_behavior` | 8 | `vbr1_l1_lna_gain_compression_macro_tb` | FAIL_SIM_CORRECTNESS |
| `veriloga_embedded_declaration` | `model_dut_compile` | 7 | `vbm1_slew_rate_limiter_dut` | ERROR (VACOMP-1917): "slew_rate_limiter.va", line 15: Encountered an |
| `sample_hold_memory_behavior` | `model_behavior` | 7 | `vbr1_l1_acquisition_limited_sample_and_hold_bugfix` | FAIL_SIM_CORRECTNESS |
| `decision_threshold_behavior` | `model_behavior` | 6 | `comparator_hysteresis_smoke` | FAIL_SIM_CORRECTNESS |
| `spectre_rejects_evas_accepted_candidate` | `evas_spectre_mismatch` | 5 | `vbm1_lock_detector_tb` | ERROR (SFE-1997): "vbm1_lock_detector_tb__tb_lock_detector_ref.scs" 9: |
| `baseband_dynamic_behavior` | `model_behavior` | 5 | `vbm1_resettable_integrator_dut` | FAIL_SIM_CORRECTNESS |
| `other_compile_failure` | `model_dut_compile` | 3 | `flash_adc_3b_smoke` | tran.csv missing |
| `unsupported_event_variable_or_wait` | `model_dut_compile` | 3 | `vbm1_thermometer_decoder_guarded_dut` | ERROR (VACOMP-2259): "task compute_targets;<<--? " |
| `spectre_tb_source_or_waveform_reject` | `model_spectre_tb_source` | 2 | `sar_adc_dac_weighted_8b_smoke` | ERROR (CMI-2194): Vvin: Waveform type must be specified if any waveform |
| `spectre_testbench_syntax` | `model_dut_compile` | 2 | `vbm1_debounce_latch_e2e` | ERROR (SFE-874): "vbm1_debounce_latch_e2e__tb_debounce_latch_ref.scs" 7: |
| `spectre_pass_evas_fail_behavior` | `evas_spectre_mismatch` | 2 | `vbr1_l1_calibration_deadband_controller_tb` | FAIL_SIM_CORRECTNESS |
| `spectre_ahdl_syntax_scope_or_operator_reject` | `model_spectre_ahdl_compile` | 2 | `vbr1_l1_ldo_regulator_macro_model_dut` | ERROR (VACOMP-2212): "ldo_regulator_macro_model.va", line 53: Encountered |
| `spectre_elaboration_parameter_or_topology_reject` | `model_spectre_elab_or_topology` | 2 | `vbr1_l2_adpll_lock_ratio_hop_timer_flow_tb` | ERROR (SFE-1997): |
| `unsupported_event_loop_form` | `model_dut_compile` | 1 | `vbm1_lock_detector_dut` | ERROR (VACOMP-2212): "disable lock_detector<<--? ; // reset handled |
| `waveform_parity_gate` | `parity` | 1 | `vbm1_resettable_counter_divider_tb` | {"common_window_s": [0.0, 8e-08], "max_abs_v": 1.0, "max_nrmse": 0.7866666666666666, "max_relativ... |
| `restricted_analog_operator_placement` | `model_dut_compile` | 1 | `vbr1_l1_programmable_gain_amplifier_dut` | ERROR (VACOMP-2146): "programmable_gain_amplifier.va", line 39: Encountered |
| `spectre_run_inconclusive` | `runner` | 1 | `vbr1_l2_complete_calibration_loop_tb` | ERROR (CMI-2116): XDUT: Too few terminals given (5 < 7). |

## Mismatch / Conformance Seeds

| Task | Direction/axis | Family | Suggested L0 action | Evidence |
| --- | --- | --- | --- | --- |
| `vbm1_lock_detector_tb` | EVAS PASS / Spectre FAIL | `spectre_rejects_evas_accepted_candidate` | minimize vbr1_l1_lock_detector into L0 syntax/dialect conformance | ERROR (SFE-1997): "vbm1_lock_detector_tb__tb_lock_detector_ref.scs" 9: |
| `vbm1_resettable_counter_divider_tb` | parity | `waveform_parity_gate` | minimize vbr1_l1_clock_divider into L0 waveform/checker-window conformance | {"common_window_s": [0.0, 8e-08], "max_abs_v": 1.0, "max_nrmse": 0.7866666666666666, "max_relativ... |
| `vbm1_thermometer_dac_15seg_e2e` | EVAS PASS / Spectre FAIL | `spectre_rejects_evas_accepted_candidate` | minimize vbr1_l1_unit_element_thermometer_dac into L0 syntax/dialect conformance | ERROR (SFE-1997): |
| `vbr1_l1_calibration_deadband_controller_tb` | Spectre PASS / EVAS FAIL | `spectre_pass_evas_fail_behavior` | minimize vbr1_l1_calibration_deadband_controller into L0 event-sampling conformance | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_pipeline_adc_stage_e2e` | EVAS PASS / Spectre FAIL | `spectre_rejects_evas_accepted_candidate` | minimize vbr1_l1_pipeline_adc_stage into L0 syntax/dialect conformance | ERROR (VACOMP-1697): "parameter real vdd = 0.9;<<--? " |
| `vbr1_l1_ptat_ctat_reference_generator_tb` | Spectre PASS / EVAS FAIL | `spectre_pass_evas_fail_behavior` | minimize vbr1_l1_ptat_ctat_reference_generator into L0 event-sampling conformance | ptat_metric_not_monotonic cold=0.000 hot=0.000 |
| `vbr1_l2_agc_receiver_leveling_loop_tb` | EVAS PASS / Spectre FAIL | `spectre_rejects_evas_accepted_candidate` | minimize vbr1_l2_agc_receiver_leveling_loop into L0 syntax/dialect conformance | ERROR (CMI-2116): XDUT: Too few terminals given (5 < 7). |
| `vbr1_l2_ldo_load_step_recovery_flow_tb` | EVAS PASS / Spectre FAIL | `spectre_rejects_evas_accepted_candidate` | minimize vbr1_l2_ldo_load_step_recovery_flow into L0 syntax/dialect conformance | ERROR (CMI-2116): XDUT: Too few terminals given (5 < 7). |

## Inputs

- `results/vabench-release-v1-baseline-dual-mimo-v2.5-pro-20260531-mimo25pro-full236-highout32k-currentevas-v1-dual`
