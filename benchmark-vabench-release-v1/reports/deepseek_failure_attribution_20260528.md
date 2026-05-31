# DeepSeek Failure Attribution - 2026-05-28

Scope: wrapper-v1 DeepSeek v4-pro candidates rejudged by the current EVAS/Spectre dual runner, with the propagation-delay comparator DUT row replaced by the wrapper-v4 preflight rerun.

Interpretation rule: Spectre checker pass is the model score signal; EVAS/Spectre waveform parity debt is an EVAS-core issue; old wrapper include/PWL/scaffold gaps are not counted as direct model ability failures until a fresh wrapper-v4 generation is run.

## Count Sanity

| Metric | Count | Rate |
| --- | --- | --- |
| Total scored forms | 236 | 100.00% |
| Clean dual pass | 50 | 21.19% |
| Clean dual non-pass | 186 | 78.81% |
| Spectre-final model pass | 52 | 22.03% |
| EVAS parity debt among Spectre passes | 2 | 0.85% |

## Attribution Summary

| Primary attribution | Rows | Share of clean-dual failures |
| --- | --- | --- |
| `model_behavior_failure` | 106 | 56.99% |
| `model_veriloga_subset_failure` | 18 | 9.68% |
| `prompt_contract_gap_old_wrapper` | 55 | 29.57% |
| `evas_core_parity_debt` | 2 | 1.08% |
| `model_incomplete_generation` | 4 | 2.15% |
| `evaluator_runner_review` | 1 | 0.54% |

## Root Cause Families

| Root cause family | Rows | Share of clean-dual failures |
| --- | --- | --- |
| `behavior_checker_mismatch` | 106 | 56.99% |
| `veriloga_spectre_subset_violation` | 18 | 9.68% |
| `public_contract_missing_include` | 28 | 15.05% |
| `spectre_scs_source_contract` | 27 | 14.52% |
| `evas_spectre_semantics` | 2 | 1.08% |
| `model_output_budget_exhausted` | 4 | 2.15% |
| `simulation_output_missing` | 1 | 0.54% |

## Model-Ability View

| Bucket | Rows | Meaning |
| --- | --- | --- |
| Direct model failures | 128 | Behavior-check mismatches, clear Verilog-A/Spectre subset violations, and incomplete fixed-budget generations. |
| Spectre-final model passes | 52 | Includes two rows that still fail EVAS waveform parity. |
| Inconclusive/non-model rows | 56 | Old prompt-contract gaps or evaluator-review rows; fixed-budget length failures are counted as incomplete model failures. |

## Raw Evaluator Status

| EVAS status | Rows |
| --- | --- |
| `PASS` | 52 |
| `FAIL_SIM_CORRECTNESS` | 107 |
| `FAIL_DUT_COMPILE` | 57 |
| `FAIL_TB_COMPILE` | 16 |
| `INCOMPLETE` | 4 |

## Failure Rows

The CSV/JSON files contain the full audit columns. This Markdown table keeps the evidence field compact for review.

| Release task | Form | Dual | EVAS | Attribution | Root detail | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| `vbr1_l1_first_order_lowpass:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | lowpass_samples=0.627,0.865,0.982,0.999 input_step=True monotonic=True response_fast_enough=True not_instant=False bo... |
| `vbr1_l1_first_order_lowpass:tb` | `tb` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | lowpass_samples=0.627,0.865,0.982,0.999 input_step=True monotonic=True response_fast_enough=True not_instant=False bo... |
| `vbr1_l1_higher_order_filter:bugfix` | `bugfix` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `model_veriloga_subset_failure` | `local_declaration_inside_analog_or_procedural_block+spectre_veriloga_parse_error` | ERROR: Failed to compile Verilog-A file higher_order_filter.va: Parse error at L64:13: Spectre-incompatible local dec... |
| `vbr1_l1_higher_order_filter:dut` | `dut` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | two_pole_reset_out=0.000 |
| `vbr1_l1_higher_order_filter:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | higher_order_filter.va:missing_disciplines_vams |
| `vbr1_l1_higher_order_filter:tb` | `tb` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | two_pole_missing_lagged_rise early=0.450 late=0.422 |
| `vbr1_l1_precision_rectifier_envelope_detector:bugfix` | `bugfix` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | precision_rectifier_envelope_detector.va:missing_disciplines_vams |
| `vbr1_l1_precision_rectifier_envelope_detector:dut` | `dut` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `model_veriloga_subset_failure` | `local_declaration_inside_analog_or_procedural_block+conditional_cross_operator+spectre_veriloga_parse_error` | ERROR: Failed to compile Verilog-A file precision_rectifier_envelope_detector.va: Parse error at L88:11: Spectre-inco... |
| `vbr1_l1_precision_rectifier_envelope_detector:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `model_veriloga_subset_failure` | `local_declaration_inside_analog_or_procedural_block+spectre_veriloga_parse_error` | ERROR: Failed to compile Verilog-A file precision_rectifier_envelope_detector.va: Parse error at L62:5: Spectre-incom... |
| `vbr1_l1_precision_rectifier_envelope_detector:tb` | `tb` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | rectifier_positive_half_not_rectified=0.450 |
| `vbr1_l1_programmable_gain_amplifier:bugfix` | `bugfix` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | programmable_gain_amplifier.va:missing_disciplines_vams |
| `vbr1_l1_programmable_gain_amplifier:dut` | `dut` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | programmable_gain_amplifier.va:missing_disciplines_vams |
| `vbr1_l1_programmable_gain_amplifier:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Failed to parse tb_programmable_gain_amplifier.scs: Invalid PWL wave token 'vdd' in source Vrst |
| `vbr1_l1_programmable_gain_amplifier:tb` | `tb` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | pga_reset_out=0.585 |
| `vbr1_l1_resettable_integrator:bugfix` | `bugfix` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | integrator_samples=0.000,0.000,0.000,0.000,0.000 input_drive=True reset_sequence=True pre_reset_integrated=False rese... |
| `vbr1_l1_resettable_integrator:dut` | `dut` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | integrator_samples=0.000,0.000,0.000,0.000,0.000 input_drive=True reset_sequence=True pre_reset_integrated=False rese... |
| `vbr1_l1_resettable_integrator:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | integrator_samples=0.500,0.500,0.500,0.500,0.500 input_drive=True reset_sequence=False pre_reset_integrated=False res... |
| `vbr1_l1_resettable_integrator:tb` | `tb` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | integrator_samples=0.850,0.850,0.850,0.850,0.850 input_drive=True reset_sequence=False pre_reset_integrated=False res... |
| `vbr1_l1_slew_rate_limiter:bugfix` | `bugfix` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | slew_samples=0.800,0.800,0.100,0.100,0.100 input_sequence=True rising_limited=False high_reached=True falling_limited... |
| `vbr1_l1_slew_rate_limiter:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | slew_samples=0.435,0.900,0.900,0.615,0.165 input_sequence=False rising_limited=False high_reached=True falling_limite... |
| `vbr1_l1_slew_rate_limiter:tb` | `tb` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | slew_samples=0.435,0.900,0.615,0.315,0.000 input_sequence=False rising_limited=False high_reached=True falling_limite... |
| `vbr1_l1_soft_hysteretic_limiter:bugfix` | `bugfix` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | soft_hysteretic_limiter.va:missing_disciplines_vams |
| `vbr1_l1_soft_hysteretic_limiter:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Failed to parse tb_soft_hysteretic_limiter.scs: Spectre-incompatible PWL wave syntax at line 16: multiline wav... |
| `vbr1_l2_amplifier_filter_chain:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | amplifier_filter_chain.va:missing_disciplines_vams |
| `vbr1_l2_amplifier_filter_chain:tb` | `tb` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | amp_filter_metric_not_preamp_target early=0.450 late=0.855 low=0.022 |
| `vbr1_l1_bandgap_reference_macro_model:bugfix` | `bugfix` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `model_veriloga_subset_failure` | `local_declaration_inside_analog_or_procedural_block+spectre_veriloga_parse_error` | ERROR: Failed to compile Verilog-A file bandgap_reference_macro_model.va: Parse error at L97:5: Spectre-incompatible... |
| `vbr1_l1_bandgap_reference_macro_model:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | bandgap_reference_macro_model.va:missing_disciplines_vams |
| `vbr1_l1_bandgap_reference_macro_model:tb` | `tb` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | bandgap_reference_not_held_low_pre_start=0.146 |
| `vbr1_l1_bias_voltage_generator_with_enable_trim:bugfix` | `bugfix` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | bias_low_trim_wrong=0.000 |
| `vbr1_l1_bias_voltage_generator_with_enable_trim:dut` | `dut` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | bias_not_disabled early=1.000 late=1.000 |
| `vbr1_l1_bias_voltage_generator_with_enable_trim:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Failed to parse tb_bias_voltage_generator_with_enable_trim.scs: Spectre-incompatible PWL wave syntax at line 9... |
| `vbr1_l1_bias_voltage_generator_with_enable_trim:tb` | `tb` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | bias_not_disabled early=0.000 late=0.594 |
| `vbr1_l1_ldo_regulator_macro_model:bugfix` | `bugfix` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | ldo_light_load_regulation_wrong=0.694 |
| `vbr1_l1_ldo_regulator_macro_model:dut` | `dut` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | ldo_light_load_regulation_wrong=0.960 |
| `vbr1_l1_ldo_regulator_macro_model:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | ldo_regulator_macro_model.va:missing_disciplines_vams |
| `vbr1_l1_power_on_reset_detector:bugfix` | `bugfix` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | por_not_released=1.000 |
| `vbr1_l1_power_on_reset_detector:dut` | `dut` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | por_not_released=1.800 |
| `vbr1_l1_power_on_reset_detector:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | por_not_released=0.502 |
| `vbr1_l1_power_on_reset_detector:tb` | `tb` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | por_not_released=0.900 |
| `vbr1_l1_ptat_ctat_reference_generator:bugfix` | `bugfix` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | ptat_ctat_reference_range=1.161/1.250/1.250 |
| `vbr1_l1_ptat_ctat_reference_generator:dut` | `dut` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | ptat_ctat_reference_range=0.000/0.000/0.000 |
| `vbr1_l1_ptat_ctat_reference_generator:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | ptat_ctat_reference_range=1.100/1.100/1.100 |
| `vbr1_l1_uvlo_brownout_detector:bugfix` | `bugfix` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | uvlo_brownout_detector.va:missing_disciplines_vams |
| `vbr1_l1_uvlo_brownout_detector:dut` | `dut` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | uvlo_hysteresis_hold_failed good=0.000 hold=0.000 |
| `vbr1_l1_uvlo_brownout_detector:tb` | `tb` | `FAIL_EVAS` | `FAIL_TB_COMPILE` | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Invalid source Vvin: Vvin: PWL wave must contain at least one time/value pair |
| `vbr1_l2_ldo_load_step_recovery_flow:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | ldo_load_step_recovery_flow.va:missing_disciplines_vams |
| `vbr1_l2_ldo_load_step_recovery_flow:tb` | `tb` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | ldo_flow_no_transient_droop pre=0.601 early=0.568 |
| `vbr1_l2_reference_startup_enable_flow:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | ref_startup_supply_off_not_low=0.331 |
| `vbr1_l2_reference_startup_enable_flow:tb` | `tb` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | ref_startup_ignores_enable=0.396 |
| `vbr1_l1_calibration_deadband_controller:bugfix` | `bugfix` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | calibration_deadband_controller.va:missing_disciplines_vams |
| `vbr1_l1_calibration_deadband_controller:dut` | `dut` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | deadband_hold_mismatches=2/10 |
| `vbr1_l1_calibration_deadband_controller:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Failed to parse tb_calibration_deadband_controller.scs: Spectre-incompatible PWL wave syntax at line 9: multil... |
| `vbr1_l1_calibration_deadband_controller:tb` | `tb` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Failed to parse tb_calibration_deadband_controller.scs: Spectre-incompatible PWL wave syntax at line 9: multil... |
| `vbr1_l1_dwa_dem_encoder:bugfix` | `bugfix` | `FAIL_EVAS` | `FAIL_TB_COMPILE` | `model_veriloga_subset_failure` | `conditional_transition_operator` | ERROR: Failed to compile Verilog-A file dwa_ptr_gen.va: Spectre-incompatible Verilog-A: transition() contribution is... |
| `vbr1_l1_dwa_dem_encoder:dut` | `dut` | `FAIL_EVAS` | `FAIL_TB_COMPILE` | `model_veriloga_subset_failure` | `spectre_veriloga_parse_error` | ERROR: Failed to compile Verilog-A file v2b_4b.va: Parse error at L64:20: Expected ASSIGN, got IDENT ('i') |
| `vbr1_l1_dwa_dem_encoder:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | dwa_ptr_gen.va:missing_disciplines_vams |
| `vbr1_l1_dwa_dem_encoder:tb` | `tb` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | sampled_cycles=10 bad_ptr_rows=0 bad_span_rows=0 ptr_unique=2 wrap_events=0 split_wrap_rows=0 max_active_cells=2 |
| `vbr1_l1_element_shuffler:bugfix` | `bugfix` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | active_sequence=2,0,3,1,2,0 expected=1,2,3,0,1,2 |
| `vbr1_l1_element_shuffler:dut` | `dut` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | active_sequence=0,3,1,2,0,3 expected=1,2,3,0,1,2 |
| `vbr1_l1_element_shuffler:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | active_sequence=-,-,-,-,-,- expected=1,2,3,0,1,2 |
| `vbr1_l1_element_shuffler:tb` | `tb` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | active_sequence=2,0,3,1,2,0 expected=1,2,3,0,1,2 |
| `vbr1_l1_gain_trim_controller:bugfix` | `bugfix` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | dut_fixed.va:missing_disciplines_vams |
| `vbr1_l1_gain_trim_controller:dut` | `dut` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `model_veriloga_subset_failure` | `local_declaration_inside_analog_or_procedural_block+spectre_veriloga_parse_error` | ERROR: Failed to compile Verilog-A file gain_trim_controller.va: Parse error at L58:9: Spectre-incompatible local dec... |
| `vbr1_l1_gain_trim_controller:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | gain_trim_controller.va:missing_disciplines_vams |
| `vbr1_l1_gain_trim_controller:tb` | `tb` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | gain_trim_samples=0.300,0.350,0.550,0.800,0.750,0.350,0.050,0.050 reset_nominal=True low_meas_increases=True reaches_... |
| `vbr1_l1_successive_approximation_calibration_search_fsm:bugfix` | `bugfix` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | sar_cal_too_few_active_steps=3 |
| `vbr1_l1_successive_approximation_calibration_search_fsm:dut` | `dut` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | successive_approximation_calibration_search_fsm.va:missing_disciplines_vams |
| `vbr1_l1_successive_approximation_calibration_search_fsm:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | sar_cal_reset_mean=0.763 |
| `vbr1_l1_successive_approximation_calibration_search_fsm:tb` | `tb` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | sar_cal_too_few_active_steps=2 |
| `vbr1_l1_trim_calibration_controller:bugfix` | `bugfix` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | trim_samples=0.700,0.900,1.000,0.800,0.800,0.900 in_range=False reset_nominal=False early_increases=True mid_decrease... |
| `vbr1_l1_trim_calibration_controller:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | trim_samples=0.510,0.630,0.690,0.810,0.850,0.730 in_range=True reset_nominal=True early_increases=True mid_decreases=... |
| `vbr1_l1_trim_calibration_controller:tb` | `tb` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | trim_samples=0.390,0.270,0.210,0.090,0.110,0.230 in_range=True reset_nominal=True early_increases=False mid_decreases... |
| `vbr1_l2_complete_calibration_loop:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_TB_COMPILE` | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Invalid source Vrst: Vrst: PWL wave must contain at least one time/value pair |
| `vbr1_l2_complete_calibration_loop:tb` | `tb` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | complete_cal_loop_input_span_too_small=0.200 |
| `vbr1_l1_debounce_latch:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `model_veriloga_subset_failure` | `conditional_cross_operator` | ERROR: Failed to compile Verilog-A file debounce_latch.va: Module debounce_latch uses Spectre-restricted operator(s)... |
| `vbr1_l1_debounce_latch:tb` | `tb` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | debounce_early_low=LLHH late_high=HH |
| `vbr1_l1_hysteresis_comparator:bugfix` | `bugfix` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | outputs_do_not_toggle |
| `vbr1_l1_hysteresis_comparator:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | window_fracs pre=0.377 mid=0.000 post=1.000 |
| `vbr1_l1_hysteresis_comparator:tb` | `tb` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | window_fracs pre=1.000 mid=0.602 post=1.000 |
| `vbr1_l1_offset_comparator:bugfix` | `bugfix` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | offset_decisions=LLLHHLL expected=LHHHLLL |
| `vbr1_l1_offset_comparator:dut` | `dut` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | offset_decisions=LLLHHLL expected=LHHHLLL |
| `vbr1_l1_offset_comparator:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | cmp_offset_ref.va:missing_disciplines_vams |
| `vbr1_l1_offset_comparator:tb` | `tb` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | offset_decisions=LLHHLLL expected=LHHHLLL |
| `vbr1_l1_propagation_delay_comparator:bugfix` | `bugfix` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | out_p_never_high phases=10mV,1mV,0.1mV,0.01mV |
| `vbr1_l1_propagation_delay_comparator:dut` | `dut` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `model_veriloga_subset_failure` | `conditional_cross_operator+unbounded_event_loop` | cmp_delay.va:unsupported_unbounded_event_loop |
| `vbr1_l1_propagation_delay_comparator:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Failed to parse tb_cmp_delay_ref.scs: Spectre-incompatible PWL wave syntax at line 11: multiline wave=[...] re... |
| `vbr1_l1_propagation_delay_comparator:tb` | `tb` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | out_p_not_low_before_clock diff=10mV |
| `vbr1_l1_strongarm_style_latch_comparator:dut` | `dut` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `model_veriloga_subset_failure` | `local_declaration_inside_analog_or_procedural_block+spectre_veriloga_parse_error` | ERROR: Failed to compile Verilog-A file cmp_strongarm.va: Parse error at L58:7: Spectre-incompatible local declaratio... |
| `vbr1_l1_strongarm_style_latch_comparator:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Failed to parse tb_cmp_strongarm_ref.scs: Spectre-incompatible PWL wave syntax at line 7: multiline wave=[...]... |
| `vbr1_l1_strongarm_style_latch_comparator:tb` | `tb` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | decision_samples=XXXX expected=PPNN |
| `vbr1_l1_binary_weighted_voltage_dac:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_TB_COMPILE` | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Invalid source Vcode0: Vcode0: PWL wave must contain at least one time/value pair |
| `vbr1_l1_binary_weighted_voltage_dac:tb` | `tb` | `FAIL_EVAS` | `FAIL_TB_COMPILE` | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Invalid source Vcode0: Vcode0: PWL wave must contain at least one time/value pair |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac:bugfix` | `bugfix` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | samples=16 mismatches=16/1 cal_mismatches=0 covered_states=16 diff_span=1.3491 max_diff_error=0.6537 max_cm_error=0.0000 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | cdac_cal.va:missing_disciplines_vams |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac:tb` | `tb` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | samples=16 mismatches=13/1 cal_mismatches=15 covered_states=16 diff_span=0.6152 max_diff_error=0.6012 max_cm_error=0.... |
| `vbr1_l1_clocked_adc_quantizer:dut` | `dut` | `FAIL_PARITY` | `PASS` | `evas_core_parity_debt` | `evas_spectre_real_to_integer_cast_semantics` | max_rmse_v=0.6532 ; max_abs_v=1 ; mean_relative_rms_error=0.134 ; max_relative_rms_error=0.4267 |
| `vbr1_l1_clocked_adc_quantizer:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | too_few_edges=9 |
| `vbr1_l1_dac_mismatch_unit_weighting_model:bugfix` | `bugfix` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `model_veriloga_subset_failure` | `local_declaration_inside_analog_or_procedural_block+spectre_veriloga_parse_error` | ERROR: Failed to compile Verilog-A file dac_mismatch_unit_weighting_model.va: Parse error at L73:3: Spectre-incompati... |
| `vbr1_l1_dac_mismatch_unit_weighting_model:dut` | `dut` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | dac_weight_mismatches=3 7ns:0.0625/0.0598 15ns:0.1166/0.1207 25ns:0.4242/0.4171 35ns:0.9000/0.9000 |
| `vbr1_l1_dac_mismatch_unit_weighting_model:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | dac_weight_mismatches=3 7ns:0.0620/0.0598 15ns:0.1200/0.1207 25ns:0.2400/0.2367 35ns:0.3600/0.3574 |
| `vbr1_l1_dac_mismatch_unit_weighting_model:tb` | `tb` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | dac_weight_mismatches=3 7ns:0.0598/0.0598 15ns:0.1207/0.1805 25ns:0.2367/0.2964 35ns:0.3574/0.4171 |
| `vbr1_l1_pipeline_adc_stage:bugfix` | `bugfix` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `model_veriloga_subset_failure` | `local_declaration_inside_analog_or_procedural_block+spectre_veriloga_parse_error` | ERROR: Failed to compile Verilog-A file pipeline_stage.va: Parse error at L71:5: Spectre-incompatible local declarati... |
| `vbr1_l1_pipeline_adc_stage:dut` | `dut` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | regions=upper:5,middle:5,lower:5 bit_mismatches=10 residue_mismatches=15 max_residue_err=0.5400 bounded_failures=0 |
| `vbr1_l1_pipeline_adc_stage:tb` | `tb` | `FAIL_EVAS` | `FAIL_TB_COMPILE` | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Failed to parse tb_pipeline_stage_ref.scs: Spectre-incompatible PWL wave syntax at line 12: multiline wave=[..... |
| `vbr1_l1_sar_logic:bugfix` | `bugfix` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | sar_rdy_sequence=LLH expected=LHL code176=0101 expected_code=1010 |
| `vbr1_l1_sar_logic:dut` | `dut` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | sar_logic_4b.va:missing_disciplines_vams |
| `vbr1_l1_sar_logic:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Failed to parse tb_sar_logic_4b_ref.scs: Spectre-incompatible PWL wave syntax at line 10: multiline wave=[...]... |
| `vbr1_l1_sar_logic:tb` | `tb` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | sar_rdy_sequence=LLL expected=LHL code176=1000 expected_code=1010 |
| `vbr1_l1_segmented_dac:dut` | `dut` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | dac_levels=0.000,0.075,0.150,0.525,0.900 expected=0.000,0.060,0.120,0.420,0.720 monotonic=True |
| `vbr1_l1_segmented_dac:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | dac_levels=0.060,0.240,0.360,0.540,0.780 expected=0.000,0.060,0.120,0.420,0.720 monotonic=True |
| `vbr1_l1_segmented_dac:tb` | `tb` | `FAIL_EVAS` | `FAIL_TB_COMPILE` | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Invalid source Vb0: Vb0: PWL wave must contain at least one time/value pair |
| `vbr1_l1_thermometer_code_decoder:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | thermometer_sequence=-,-,-,-,-,- expected=-,-,0,01,012,012 |
| `vbr1_l1_thermometer_code_decoder:tb` | `tb` | `FAIL_EVAS` | `FAIL_TB_COMPILE` | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Invalid source Vb0: Vb0: PWL wave must contain at least one time/value pair |
| `vbr1_l1_unit_element_thermometer_dac:tb` | `tb` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | levels=0:0.000/0 1:0.120/2 2:0.420/7 7:0.900/15 14:0.900/15 15:0.900/15 max_err=0.480 monotonic=True counts_match=Fal... |
| `vbr1_l2_converter_static_linearity_measurement_flow:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `model_veriloga_subset_failure` | `local_declaration_inside_analog_or_procedural_block+spectre_veriloga_parse_error` | ERROR: Failed to compile Verilog-A file converter_static_linearity_measurement_flow.va: Parse error at L113:9: Spectr... |
| `vbr1_l2_converter_static_linearity_measurement_flow:tb` | `tb` | `FAIL_EVAS` | `FAIL_TB_COMPILE` | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Invalid source Vrst: Vrst: PWL wave must contain at least one time/value pair |
| `vbr1_l2_flash_adc_mini_array:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Failed to parse tb_flash_adc_3b_ref.scs: Spectre-incompatible PWL wave syntax at line 13: multiline wave=[...]... |
| `vbr1_l2_flash_adc_mini_array:tb` | `tb` | `FAIL_EVAS` | `FAIL_TB_COMPILE` | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Failed to parse tb_flash_adc_3b_ref.scs: Spectre-incompatible PWL wave syntax at line 10: multiline wave=[...]... |
| `vbr1_l2_pipeline_adc_chain:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | pipeline_adc_chain_4b.va:missing_disciplines_vams |
| `vbr1_l2_pipeline_adc_chain:tb` | `tb` | `FAIL_EVAS` | `FAIL_TB_COMPILE` | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Invalid source Vin: Vin: PWL wave must contain at least one time/value pair |
| `vbr1_l2_weighted_sar_adc_dac_loop:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_TB_COMPILE` | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Invalid source Vrst_n: Vrst_n: PWL wave must contain at least one time/value pair |
| `vbr1_l2_weighted_sar_adc_dac_loop:tb` | `tb` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | samples=95 unique_codes=91 code_range=0-255 sample_span=0.994 vout_span=1.000 avg_quant_err=0.0588 max_quant_err=0.10... |
| `vbr1_l1_bang_bang_phase_detector:bugfix` | `bugfix` | `INCOMPLETE` | `INCOMPLETE` | `model_incomplete_generation` | `incomplete_no_code_extracted_finish_reason_length` | generation_status=no_code_extracted finish_reason=length |
| `vbr1_l1_bang_bang_phase_detector:dut` | `dut` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | data_edges=150 up_edges=60 down_edges=60 overlap_frac=0.0209 direction_up=0/60 direction_down=0/90 wrong_direction=15... |
| `vbr1_l1_bang_bang_phase_detector:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | bbpd_data_edge_alignment_ref.va:missing_disciplines_vams |
| `vbr1_l1_bang_bang_phase_detector:tb` | `tb` | `FAIL_EVAS` | `FAIL_TB_COMPILE` | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Failed to parse tb_bbpd_data_edge_alignment_ref.scs: Spectre-incompatible PWL wave syntax at line 10: multilin... |
| `vbr1_l1_charge_pump_abstraction:bugfix` | `bugfix` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | charge_pump_abstraction.va:missing_disciplines_vams |
| `vbr1_l1_charge_pump_abstraction:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | charge_pump_missing_polarity_windows up=1 down=0 |
| `vbr1_l1_charge_pump_abstraction:tb` | `tb` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | charge_pump_vctrl_span_too_small=0.000 |
| `vbr1_l1_clock_divider:bugfix` | `bugfix` | `INCOMPLETE` | `INCOMPLETE` | `model_incomplete_generation` | `incomplete_no_code_extracted_finish_reason_length` | generation_status=no_code_extracted finish_reason=length |
| `vbr1_l1_clock_divider:dut` | `dut` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `evaluator_runner_review` | `simulator_or_checker_crash_before_waveform` | tran.csv missing |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap:bugfix` | `bugfix` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | phase_span_too_small=0.000 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap:dut` | `dut` | `FAIL_PARITY` | `PASS` | `evas_core_parity_debt` | `evas_spectre_timer_zero_start_ordering` | max_rmse_v=0.432 ; max_abs_v=1 ; mean_relative_rms_error=0.2461 ; max_relative_rms_error=0.3055 |
| `vbr1_l1_lock_detector:bugfix` | `bugfix` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | lock_sequence=LLLL expected=LLHH |
| `vbr1_l1_lock_detector:dut` | `dut` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `model_veriloga_subset_failure` | `local_declaration_inside_analog_or_procedural_block+spectre_veriloga_parse_error` | ERROR: Failed to compile Verilog-A file lock_detector.va: Parse error at L70:9: Spectre-incompatible local declaratio... |
| `vbr1_l1_lock_detector:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `model_veriloga_subset_failure` | `local_declaration_inside_analog_or_procedural_block+spectre_veriloga_parse_error` | ERROR: Failed to compile Verilog-A file lock_detector.va: Parse error at L71:17: Spectre-incompatible local declarati... |
| `vbr1_l1_lock_detector:tb` | `tb` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | lock_sequence=LLLL expected=LLHH |
| `vbr1_l1_loop_filter_abstraction:bugfix` | `bugfix` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | loop_filter_no_proportional_decay first=0.067 later=0.036 |
| `vbr1_l1_loop_filter_abstraction:dut` | `dut` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | loop_filter_no_proportional_decay first=0.092 later=-0.003 |
| `vbr1_l1_loop_filter_abstraction:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `model_veriloga_subset_failure` | `local_declaration_inside_analog_or_procedural_block+spectre_veriloga_parse_error` | ERROR: Failed to compile Verilog-A file loop_filter_abstraction.va: Parse error at L87:13: Spectre-incompatible local... |
| `vbr1_l1_loop_filter_abstraction:tb` | `tb` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | loop_filter_too_few_edge_samples=7 |
| `vbr1_l1_pfd_up_dn_logic:bugfix` | `bugfix` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | dut_fixed.va:missing_disciplines_vams |
| `vbr1_l1_pfd_up_dn_logic:dut` | `dut` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | up_first=0.0000 dn_first=0.0000 up_second=0.0000 dn_second=0.0000 up_pulses_first=0 dn_pulses_second=0 overlap_frac=0... |
| `vbr1_l1_pfd_up_dn_logic:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | up_first=0.0000 dn_first=0.0048 up_second=0.0000 dn_second=0.0000 up_pulses_first=0 dn_pulses_second=0 overlap_frac=0... |
| `vbr1_l1_pfd_up_dn_logic:tb` | `tb` | `FAIL_EVAS` | `FAIL_TB_COMPILE` | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Invalid source Vref: Vref: PWL wave must contain at least one time/value pair |
| `vbr1_l1_vco_phase_integrator:bugfix` | `bugfix` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | phase_1ns=0.100 phase_10ns=0.000 phase_span=0.950 clk_edges=44 early_edges=4 late_edges=36 |
| `vbr1_l1_vco_phase_integrator:dut` | `dut` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `model_veriloga_subset_failure` | `local_declaration_inside_analog_or_procedural_block+spectre_veriloga_parse_error` | ERROR: Failed to compile Verilog-A file vco_phase_integrator.va: Parse error at L58:7: Spectre-incompatible local dec... |
| `vbr1_l1_vco_phase_integrator:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | phase_1ns=0.000 phase_10ns=0.030 phase_span=0.030 clk_edges=0 early_edges=0 late_edges=0 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | hop_t=1.500e-06 pre_ratio=3.528 post_ratio=3.520 pre_lock=0.000 post_lock=0.000 vctrl_range_ok=True |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow:tb` | `tb` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | hop_t=2.500e-06 pre_ratio=10.001 post_ratio=15.001 pre_lock=1.000 post_lock=1.000 vctrl_range_ok=True |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow:e2e` | `e2e` | `INCOMPLETE` | `INCOMPLETE` | `model_incomplete_generation` | `incomplete_no_code_extracted_finish_reason_length` | generation_status=no_code_extracted finish_reason=length |
| `vbr1_l1_limiting_amplifier_frontend:dut` | `dut` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | limiter_small_gain_missing vin=0.500 out=0.100 |
| `vbr1_l1_limiting_amplifier_frontend:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `model_veriloga_subset_failure` | `local_declaration_inside_analog_or_procedural_block` | an embedded declaration statement outside a labeled block. Specify the |
| `vbr1_l1_limiting_amplifier_frontend:tb` | `tb` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Failed to parse tb_limiting_amplifier_frontend.scs: Spectre-incompatible PWL wave syntax at line 7: multiline... |
| `vbr1_l1_lna_gain_compression_macro:bugfix` | `bugfix` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | lna_small_signal_gain_missing vin=0.520 out=0.000 |
| `vbr1_l1_lna_gain_compression_macro:dut` | `dut` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | lna_high_compression_wrong=0.600 |
| `vbr1_l1_lna_gain_compression_macro:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_TB_COMPILE` | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Invalid source Vvin: Vvin: PWL wave must contain at least one time/value pair |
| `vbr1_l1_lna_gain_compression_macro:tb` | `tb` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | lna_small_signal_gain_missing vin=0.488 out=0.450 |
| `vbr1_l1_log_rssi_power_detector:bugfix` | `bugfix` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | log_rssi_power_detector.va:missing_disciplines_vams |
| `vbr1_l1_log_rssi_power_detector:dut` | `dut` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | rssi_floor_wrong=0.600 |
| `vbr1_l1_log_rssi_power_detector:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | rssi_floor_wrong=0.200 |
| `vbr1_l1_log_rssi_power_detector:tb` | `tb` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | rssi_not_monotonic_loglike small/mid/high=0.120/0.120/0.504 |
| `vbr1_l1_pa_compression_macro:bugfix` | `bugfix` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | pa_high_compression_wrong=1.650 |
| `vbr1_l1_pa_compression_macro:dut` | `dut` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | pa_high_compression_wrong=3.000 |
| `vbr1_l1_pa_compression_macro:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | pa_gain_missing vin=0.429 out=0.000 |
| `vbr1_l1_pa_compression_macro:tb` | `tb` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | pa_gain_missing vin=0.030 out=0.039 |
| `vbr1_l1_rf_mixer_downconverter_macro:bugfix` | `bugfix` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | rf_mixer_downconverter_macro.va:missing_disciplines_vams |
| `vbr1_l1_rf_mixer_downconverter_macro:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | mixer_missing_sample_windows |
| `vbr1_l2_agc_receiver_leveling_loop:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | agc_gain_not_reduced overload=0.022 settled=0.001 |
| `vbr1_l2_agc_receiver_leveling_loop:tb` | `tb` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | agc_gain_not_reduced overload=0.000 settled=0.430 |
| `vbr1_l2_iq_downconversion_chain:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | iq_downconversion_chain.va:missing_disciplines_vams |
| `vbr1_l2_iq_downconversion_chain:tb` | `tb` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | iq_positive_quadrature_missing i=0.450 q=0.450 |
| `vbr1_l1_acquisition_limited_sample_and_hold:bugfix` | `bugfix` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | acquisition_limited_sample_hold.va:missing_disciplines_vams |
| `vbr1_l1_acquisition_limited_sample_and_hold:dut` | `dut` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | acquisition_limited_sample_hold.va:missing_disciplines_vams |
| `vbr1_l1_acquisition_limited_sample_and_hold:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Failed to parse tb_acquisition_limited_sample_hold.scs: Spectre-incompatible PWL wave syntax at line 7: multil... |
| `vbr1_l1_acquisition_limited_sample_and_hold:tb` | `tb` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | acq_hold_drifted_after_fall delta=0.316 |
| `vbr1_l1_aperture_delay_track_and_hold:bugfix` | `bugfix` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | aperture_samples=0.100,0.350,0.600,0.250,0.700,0.400,0.800 expected=0.350,0.600,0.250,0.700,0.400,0.800,0.800 mismatc... |
| `vbr1_l1_aperture_delay_track_and_hold:dut` | `dut` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | aperture_samples=0.000,0.000,0.000,0.000,0.000,0.000,0.000 expected=0.100,0.350,0.600,0.250,0.700,0.400,0.800 mismatc... |
| `vbr1_l1_aperture_delay_track_and_hold:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | sample_hold_aperture_ref.va:missing_disciplines_vams |
| `vbr1_l1_clocked_sample_and_hold:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | too_few_clock_edges=5 |
| `vbr1_l1_clocked_sample_and_hold:tb` | `tb` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | too_few_clock_edges=0 |
| `vbr1_l1_sample_and_hold_with_droop_leakage:bugfix` | `bugfix` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | vin_samples=0.200,0.720,0.340 held_samples=0.200,0.719,0.340 max_sample_err=0.001 expected_span=0.520 observed_span=0... |
| `vbr1_l1_sample_and_hold_with_droop_leakage:e2e` | `e2e` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Failed to parse tb_leaky_hold_ref.scs: Spectre-incompatible PWL wave syntax at line 11: multiline wave=[...] r... |
| `vbr1_l1_sample_and_hold_with_droop_leakage:tb` | `tb` | `FAIL_EVAS` | `FAIL_DUT_COMPILE` | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Failed to parse tb_leaky_hold_ref.scs: Spectre-incompatible PWL wave syntax at line 9: multiline wave=[...] re... |
| `vbr1_l2_converter_front_end:e2e` | `e2e` | `INCOMPLETE` | `INCOMPLETE` | `model_incomplete_generation` | `incomplete_no_code_extracted_finish_reason_length` | generation_status=no_code_extracted finish_reason=length |
| `vbr1_l2_converter_front_end:tb` | `tb` | `FAIL_EVAS` | `FAIL_SIM_CORRECTNESS` | `model_behavior_failure` | `compiled_and_ran_but_failed_hidden_behavior_checker` | edges=9 max_sample_err=0.000 coarse_mismatches=0 valid_high_hits=8 valid_low_hits=8 aperture_sensitive=0 droop_window... |
