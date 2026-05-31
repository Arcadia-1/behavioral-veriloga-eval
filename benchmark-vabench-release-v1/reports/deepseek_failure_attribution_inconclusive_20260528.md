# DeepSeek Inconclusive Rows - 2026-05-28

Scope: rows that should not currently be counted as either Spectre-final model passes or direct model failures.

Interpretation: these rows need a wrapper-v4 regeneration/rerun or runner/evaluator triage before they are used as model-capability evidence. Fixed-budget `finish_reason=length` generations are classified separately as `model_incomplete_generation`.

## Breakdown

| Primary attribution | Rows |
| --- | --- |
| `prompt_contract_gap_old_wrapper` | 55 |
| `evaluator_runner_review` | 1 |

## Root Details

| Root detail | Rows |
| --- | --- |
| `missing_disciplines_vams_in_old_wrapper_candidate` | 28 |
| `invalid_or_incomplete_pwl_source_syntax` | 27 |
| `simulator_or_checker_crash_before_waveform` | 1 |

## Rows

| Release task | Form | Category | Attribution | Root detail | Evidence |
| --- | --- | --- | --- | --- | --- |
| `vbr1_l1_higher_order_filter:e2e` | `e2e` | Baseband Signal Conditioning | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | higher_order_filter.va:missing_disciplines_vams |
| `vbr1_l1_precision_rectifier_envelope_detector:bugfix` | `bugfix` | Baseband Signal Conditioning | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | precision_rectifier_envelope_detector.va:missing_disciplines_vams |
| `vbr1_l1_programmable_gain_amplifier:bugfix` | `bugfix` | Baseband Signal Conditioning | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | programmable_gain_amplifier.va:missing_disciplines_vams |
| `vbr1_l1_programmable_gain_amplifier:dut` | `dut` | Baseband Signal Conditioning | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | programmable_gain_amplifier.va:missing_disciplines_vams |
| `vbr1_l1_programmable_gain_amplifier:e2e` | `e2e` | Baseband Signal Conditioning | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Failed to parse tb_programmable_gain_amplifier.scs: Invalid PWL wave token 'vdd' in source Vrst |
| `vbr1_l1_soft_hysteretic_limiter:bugfix` | `bugfix` | Baseband Signal Conditioning | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | soft_hysteretic_limiter.va:missing_disciplines_vams |
| `vbr1_l1_soft_hysteretic_limiter:e2e` | `e2e` | Baseband Signal Conditioning | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Failed to parse tb_soft_hysteretic_limiter.scs: Spectre-incompatible PWL wave syntax at line 16: multiline wave=[...] requires bac... |
| `vbr1_l2_amplifier_filter_chain:e2e` | `e2e` | Baseband Signal Conditioning | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | amplifier_filter_chain.va:missing_disciplines_vams |
| `vbr1_l1_bandgap_reference_macro_model:e2e` | `e2e` | Bias Reference and Power Management | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | bandgap_reference_macro_model.va:missing_disciplines_vams |
| `vbr1_l1_bias_voltage_generator_with_enable_trim:e2e` | `e2e` | Bias Reference and Power Management | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Failed to parse tb_bias_voltage_generator_with_enable_trim.scs: Spectre-incompatible PWL wave syntax at line 9: multiline wave=[..... |
| `vbr1_l1_ldo_regulator_macro_model:e2e` | `e2e` | Bias Reference and Power Management | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | ldo_regulator_macro_model.va:missing_disciplines_vams |
| `vbr1_l1_uvlo_brownout_detector:bugfix` | `bugfix` | Bias Reference and Power Management | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | uvlo_brownout_detector.va:missing_disciplines_vams |
| `vbr1_l1_uvlo_brownout_detector:tb` | `tb` | Bias Reference and Power Management | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Invalid source Vvin: Vvin: PWL wave must contain at least one time/value pair |
| `vbr1_l2_ldo_load_step_recovery_flow:e2e` | `e2e` | Bias Reference and Power Management | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | ldo_load_step_recovery_flow.va:missing_disciplines_vams |
| `vbr1_l1_calibration_deadband_controller:bugfix` | `bugfix` | Calibration, DEM, and Control | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | calibration_deadband_controller.va:missing_disciplines_vams |
| `vbr1_l1_calibration_deadband_controller:e2e` | `e2e` | Calibration, DEM, and Control | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Failed to parse tb_calibration_deadband_controller.scs: Spectre-incompatible PWL wave syntax at line 9: multiline wave=[...] requi... |
| `vbr1_l1_calibration_deadband_controller:tb` | `tb` | Calibration, DEM, and Control | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Failed to parse tb_calibration_deadband_controller.scs: Spectre-incompatible PWL wave syntax at line 9: multiline wave=[...] requi... |
| `vbr1_l1_dwa_dem_encoder:e2e` | `e2e` | Calibration, DEM, and Control | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | dwa_ptr_gen.va:missing_disciplines_vams |
| `vbr1_l1_gain_trim_controller:bugfix` | `bugfix` | Calibration, DEM, and Control | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | dut_fixed.va:missing_disciplines_vams |
| `vbr1_l1_gain_trim_controller:e2e` | `e2e` | Calibration, DEM, and Control | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | gain_trim_controller.va:missing_disciplines_vams |
| `vbr1_l1_successive_approximation_calibration_search_fsm:dut` | `dut` | Calibration, DEM, and Control | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | successive_approximation_calibration_search_fsm.va:missing_disciplines_vams |
| `vbr1_l2_complete_calibration_loop:e2e` | `e2e` | Calibration, DEM, and Control | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Invalid source Vrst: Vrst: PWL wave must contain at least one time/value pair |
| `vbr1_l1_offset_comparator:e2e` | `e2e` | Comparator and Decision Circuits | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | cmp_offset_ref.va:missing_disciplines_vams |
| `vbr1_l1_propagation_delay_comparator:e2e` | `e2e` | Comparator and Decision Circuits | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Failed to parse tb_cmp_delay_ref.scs: Spectre-incompatible PWL wave syntax at line 11: multiline wave=[...] requires backslash lin... |
| `vbr1_l1_strongarm_style_latch_comparator:e2e` | `e2e` | Comparator and Decision Circuits | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Failed to parse tb_cmp_strongarm_ref.scs: Spectre-incompatible PWL wave syntax at line 7: multiline wave=[...] requires backslash... |
| `vbr1_l1_binary_weighted_voltage_dac:e2e` | `e2e` | Data Converter Models | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Invalid source Vcode0: Vcode0: PWL wave must contain at least one time/value pair |
| `vbr1_l1_binary_weighted_voltage_dac:tb` | `tb` | Data Converter Models | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Invalid source Vcode0: Vcode0: PWL wave must contain at least one time/value pair |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac:e2e` | `e2e` | Data Converter Models | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | cdac_cal.va:missing_disciplines_vams |
| `vbr1_l1_pipeline_adc_stage:tb` | `tb` | Data Converter Models | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Failed to parse tb_pipeline_stage_ref.scs: Spectre-incompatible PWL wave syntax at line 12: multiline wave=[...] requires backslas... |
| `vbr1_l1_sar_logic:dut` | `dut` | Data Converter Models | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | sar_logic_4b.va:missing_disciplines_vams |
| `vbr1_l1_sar_logic:e2e` | `e2e` | Data Converter Models | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Failed to parse tb_sar_logic_4b_ref.scs: Spectre-incompatible PWL wave syntax at line 10: multiline wave=[...] requires backslash... |
| `vbr1_l1_segmented_dac:tb` | `tb` | Data Converter Models | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Invalid source Vb0: Vb0: PWL wave must contain at least one time/value pair |
| `vbr1_l1_thermometer_code_decoder:tb` | `tb` | Data Converter Models | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Invalid source Vb0: Vb0: PWL wave must contain at least one time/value pair |
| `vbr1_l2_converter_static_linearity_measurement_flow:tb` | `tb` | Data Converter Models | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Invalid source Vrst: Vrst: PWL wave must contain at least one time/value pair |
| `vbr1_l2_flash_adc_mini_array:e2e` | `e2e` | Data Converter Models | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Failed to parse tb_flash_adc_3b_ref.scs: Spectre-incompatible PWL wave syntax at line 13: multiline wave=[...] requires backslash... |
| `vbr1_l2_flash_adc_mini_array:tb` | `tb` | Data Converter Models | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Failed to parse tb_flash_adc_3b_ref.scs: Spectre-incompatible PWL wave syntax at line 10: multiline wave=[...] requires backslash... |
| `vbr1_l2_pipeline_adc_chain:e2e` | `e2e` | Data Converter Models | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | pipeline_adc_chain_4b.va:missing_disciplines_vams |
| `vbr1_l2_pipeline_adc_chain:tb` | `tb` | Data Converter Models | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Invalid source Vin: Vin: PWL wave must contain at least one time/value pair |
| `vbr1_l2_weighted_sar_adc_dac_loop:e2e` | `e2e` | Data Converter Models | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Invalid source Vrst_n: Vrst_n: PWL wave must contain at least one time/value pair |
| `vbr1_l1_bang_bang_phase_detector:e2e` | `e2e` | PLL Clock and Timing Systems | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | bbpd_data_edge_alignment_ref.va:missing_disciplines_vams |
| `vbr1_l1_bang_bang_phase_detector:tb` | `tb` | PLL Clock and Timing Systems | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Failed to parse tb_bbpd_data_edge_alignment_ref.scs: Spectre-incompatible PWL wave syntax at line 10: multiline wave=[...] require... |
| `vbr1_l1_charge_pump_abstraction:bugfix` | `bugfix` | PLL Clock and Timing Systems | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | charge_pump_abstraction.va:missing_disciplines_vams |
| `vbr1_l1_clock_divider:dut` | `dut` | PLL Clock and Timing Systems | `evaluator_runner_review` | `simulator_or_checker_crash_before_waveform` | tran.csv missing |
| `vbr1_l1_pfd_up_dn_logic:bugfix` | `bugfix` | PLL Clock and Timing Systems | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | dut_fixed.va:missing_disciplines_vams |
| `vbr1_l1_pfd_up_dn_logic:tb` | `tb` | PLL Clock and Timing Systems | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Invalid source Vref: Vref: PWL wave must contain at least one time/value pair |
| `vbr1_l1_limiting_amplifier_frontend:tb` | `tb` | RF and AFE Behavioral Macromodels | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Failed to parse tb_limiting_amplifier_frontend.scs: Spectre-incompatible PWL wave syntax at line 7: multiline wave=[...] requires... |
| `vbr1_l1_lna_gain_compression_macro:e2e` | `e2e` | RF and AFE Behavioral Macromodels | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Invalid source Vvin: Vvin: PWL wave must contain at least one time/value pair |
| `vbr1_l1_log_rssi_power_detector:bugfix` | `bugfix` | RF and AFE Behavioral Macromodels | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | log_rssi_power_detector.va:missing_disciplines_vams |
| `vbr1_l1_rf_mixer_downconverter_macro:bugfix` | `bugfix` | RF and AFE Behavioral Macromodels | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | rf_mixer_downconverter_macro.va:missing_disciplines_vams |
| `vbr1_l2_iq_downconversion_chain:e2e` | `e2e` | RF and AFE Behavioral Macromodels | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | iq_downconversion_chain.va:missing_disciplines_vams |
| `vbr1_l1_acquisition_limited_sample_and_hold:bugfix` | `bugfix` | Sampling and Analog Memory | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | acquisition_limited_sample_hold.va:missing_disciplines_vams |
| `vbr1_l1_acquisition_limited_sample_and_hold:dut` | `dut` | Sampling and Analog Memory | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | acquisition_limited_sample_hold.va:missing_disciplines_vams |
| `vbr1_l1_acquisition_limited_sample_and_hold:e2e` | `e2e` | Sampling and Analog Memory | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Failed to parse tb_acquisition_limited_sample_hold.scs: Spectre-incompatible PWL wave syntax at line 7: multiline wave=[...] requi... |
| `vbr1_l1_aperture_delay_track_and_hold:e2e` | `e2e` | Sampling and Analog Memory | `prompt_contract_gap_old_wrapper` | `missing_disciplines_vams_in_old_wrapper_candidate` | sample_hold_aperture_ref.va:missing_disciplines_vams |
| `vbr1_l1_sample_and_hold_with_droop_leakage:e2e` | `e2e` | Sampling and Analog Memory | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Failed to parse tb_leaky_hold_ref.scs: Spectre-incompatible PWL wave syntax at line 11: multiline wave=[...] requires backslash li... |
| `vbr1_l1_sample_and_hold_with_droop_leakage:tb` | `tb` | Sampling and Analog Memory | `prompt_contract_gap_old_wrapper` | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Failed to parse tb_leaky_hold_ref.scs: Spectre-incompatible PWL wave syntax at line 9: multiline wave=[...] requires backslash lin... |
