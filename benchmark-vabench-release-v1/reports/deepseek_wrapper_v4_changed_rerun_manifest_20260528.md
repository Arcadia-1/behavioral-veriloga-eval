# DeepSeek Wrapper-v4 Changed Rerun Manifest

Generated: `2026-05-28T14:20:27.519619+00:00`

This is a minimal rerun queue. It includes only rows whose old wrapper-v1
candidate failure was attributed to missing shared prompt-wrapper contract
rules. It does not request a full 236-row baseline rerun.

## Summary

- selected for wrapper-v4 regeneration: 55
- skipped inconclusive rows: 1
- task-id file: `benchmark-vabench-release-v1/reports/deepseek_wrapper_v4_changed_rerun_task_ids_20260528.txt`

## Selected Root Causes

| Root cause | Count |
| --- | ---: |
| `missing_disciplines_vams_in_old_wrapper_candidate` | 28 |
| `invalid_or_incomplete_pwl_source_syntax` | 27 |

## Skipped Inconclusive Rows

| Attribution | Count | Reason |
| --- | ---: | --- |
| `evaluator_runner_review` | 1 | needs evaluator or checker triage before being counted as model evidence |

## Selected Rows

| Release task id | Form | Level | Category | Root cause | Evidence |
| --- | --- | --- | --- | --- | --- |
| `vbr1_l1_higher_order_filter:e2e` | `e2e` | `L1` | Baseband Signal Conditioning | `missing_disciplines_vams_in_old_wrapper_candidate` | higher_order_filter.va:missing_disciplines_vams |
| `vbr1_l1_precision_rectifier_envelope_detector:bugfix` | `bugfix` | `L1` | Baseband Signal Conditioning | `missing_disciplines_vams_in_old_wrapper_candidate` | precision_rectifier_envelope_detector.va:missing_disciplines_vams |
| `vbr1_l1_programmable_gain_amplifier:bugfix` | `bugfix` | `L1` | Baseband Signal Conditioning | `missing_disciplines_vams_in_old_wrapper_candidate` | programmable_gain_amplifier.va:missing_disciplines_vams |
| `vbr1_l1_programmable_gain_amplifier:dut` | `dut` | `L1` | Baseband Signal Conditioning | `missing_disciplines_vams_in_old_wrapper_candidate` | programmable_gain_amplifier.va:missing_disciplines_vams |
| `vbr1_l1_programmable_gain_amplifier:e2e` | `e2e` | `L1` | Baseband Signal Conditioning | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Failed to parse tb_programmable_gain_amplifier.scs: Invalid PWL wave token 'vdd' in source Vrst |
| `vbr1_l1_soft_hysteretic_limiter:bugfix` | `bugfix` | `L1` | Baseband Signal Conditioning | `missing_disciplines_vams_in_old_wrapper_candidate` | soft_hysteretic_limiter.va:missing_disciplines_vams |
| `vbr1_l1_soft_hysteretic_limiter:e2e` | `e2e` | `L1` | Baseband Signal Conditioning | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Failed to parse tb_soft_hysteretic_limiter.scs: Spectre-incompatible PWL wave syntax at line 16: multiline wave=[...] requires backslash line continuation |
| `vbr1_l2_amplifier_filter_chain:e2e` | `e2e` | `L2` | Baseband Signal Conditioning | `missing_disciplines_vams_in_old_wrapper_candidate` | amplifier_filter_chain.va:missing_disciplines_vams |
| `vbr1_l1_bandgap_reference_macro_model:e2e` | `e2e` | `L1` | Bias Reference and Power Management | `missing_disciplines_vams_in_old_wrapper_candidate` | bandgap_reference_macro_model.va:missing_disciplines_vams |
| `vbr1_l1_bias_voltage_generator_with_enable_trim:e2e` | `e2e` | `L1` | Bias Reference and Power Management | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Failed to parse tb_bias_voltage_generator_with_enable_trim.scs: Spectre-incompatible PWL wave syntax at line 9: multiline wave=[...] requires backslash line continuation |
| `vbr1_l1_ldo_regulator_macro_model:e2e` | `e2e` | `L1` | Bias Reference and Power Management | `missing_disciplines_vams_in_old_wrapper_candidate` | ldo_regulator_macro_model.va:missing_disciplines_vams |
| `vbr1_l1_uvlo_brownout_detector:bugfix` | `bugfix` | `L1` | Bias Reference and Power Management | `missing_disciplines_vams_in_old_wrapper_candidate` | uvlo_brownout_detector.va:missing_disciplines_vams |
| `vbr1_l1_uvlo_brownout_detector:tb` | `tb` | `L1` | Bias Reference and Power Management | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Invalid source Vvin: Vvin: PWL wave must contain at least one time/value pair |
| `vbr1_l2_ldo_load_step_recovery_flow:e2e` | `e2e` | `L2` | Bias Reference and Power Management | `missing_disciplines_vams_in_old_wrapper_candidate` | ldo_load_step_recovery_flow.va:missing_disciplines_vams |
| `vbr1_l1_calibration_deadband_controller:bugfix` | `bugfix` | `L1` | Calibration, DEM, and Control | `missing_disciplines_vams_in_old_wrapper_candidate` | calibration_deadband_controller.va:missing_disciplines_vams |
| `vbr1_l1_calibration_deadband_controller:e2e` | `e2e` | `L1` | Calibration, DEM, and Control | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Failed to parse tb_calibration_deadband_controller.scs: Spectre-incompatible PWL wave syntax at line 9: multiline wave=[...] requires backslash line continuation |
| `vbr1_l1_calibration_deadband_controller:tb` | `tb` | `L1` | Calibration, DEM, and Control | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Failed to parse tb_calibration_deadband_controller.scs: Spectre-incompatible PWL wave syntax at line 9: multiline wave=[...] requires backslash line continuation |
| `vbr1_l1_dwa_dem_encoder:e2e` | `e2e` | `L1` | Calibration, DEM, and Control | `missing_disciplines_vams_in_old_wrapper_candidate` | dwa_ptr_gen.va:missing_disciplines_vams |
| `vbr1_l1_gain_trim_controller:bugfix` | `bugfix` | `L1` | Calibration, DEM, and Control | `missing_disciplines_vams_in_old_wrapper_candidate` | dut_fixed.va:missing_disciplines_vams |
| `vbr1_l1_gain_trim_controller:e2e` | `e2e` | `L1` | Calibration, DEM, and Control | `missing_disciplines_vams_in_old_wrapper_candidate` | gain_trim_controller.va:missing_disciplines_vams |
| `vbr1_l1_successive_approximation_calibration_search_fsm:dut` | `dut` | `L1` | Calibration, DEM, and Control | `missing_disciplines_vams_in_old_wrapper_candidate` | successive_approximation_calibration_search_fsm.va:missing_disciplines_vams |
| `vbr1_l2_complete_calibration_loop:e2e` | `e2e` | `L2` | Calibration, DEM, and Control | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Invalid source Vrst: Vrst: PWL wave must contain at least one time/value pair |
| `vbr1_l1_offset_comparator:e2e` | `e2e` | `L1` | Comparator and Decision Circuits | `missing_disciplines_vams_in_old_wrapper_candidate` | cmp_offset_ref.va:missing_disciplines_vams |
| `vbr1_l1_propagation_delay_comparator:e2e` | `e2e` | `L1` | Comparator and Decision Circuits | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Failed to parse tb_cmp_delay_ref.scs: Spectre-incompatible PWL wave syntax at line 11: multiline wave=[...] requires backslash line continuation |
| `vbr1_l1_strongarm_style_latch_comparator:e2e` | `e2e` | `L1` | Comparator and Decision Circuits | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Failed to parse tb_cmp_strongarm_ref.scs: Spectre-incompatible PWL wave syntax at line 7: multiline wave=[...] requires backslash line continuation |
| `vbr1_l1_binary_weighted_voltage_dac:e2e` | `e2e` | `L1` | Data Converter Models | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Invalid source Vcode0: Vcode0: PWL wave must contain at least one time/value pair |
| `vbr1_l1_binary_weighted_voltage_dac:tb` | `tb` | `L1` | Data Converter Models | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Invalid source Vcode0: Vcode0: PWL wave must contain at least one time/value pair |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac:e2e` | `e2e` | `L1` | Data Converter Models | `missing_disciplines_vams_in_old_wrapper_candidate` | cdac_cal.va:missing_disciplines_vams |
| `vbr1_l1_pipeline_adc_stage:tb` | `tb` | `L1` | Data Converter Models | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Failed to parse tb_pipeline_stage_ref.scs: Spectre-incompatible PWL wave syntax at line 12: multiline wave=[...] requires backslash line continuation |
| `vbr1_l1_sar_logic:dut` | `dut` | `L1` | Data Converter Models | `missing_disciplines_vams_in_old_wrapper_candidate` | sar_logic_4b.va:missing_disciplines_vams |
| `vbr1_l1_sar_logic:e2e` | `e2e` | `L1` | Data Converter Models | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Failed to parse tb_sar_logic_4b_ref.scs: Spectre-incompatible PWL wave syntax at line 10: multiline wave=[...] requires backslash line continuation |
| `vbr1_l1_segmented_dac:tb` | `tb` | `L1` | Data Converter Models | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Invalid source Vb0: Vb0: PWL wave must contain at least one time/value pair |
| `vbr1_l1_thermometer_code_decoder:tb` | `tb` | `L1` | Data Converter Models | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Invalid source Vb0: Vb0: PWL wave must contain at least one time/value pair |
| `vbr1_l2_converter_static_linearity_measurement_flow:tb` | `tb` | `L2` | Data Converter Models | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Invalid source Vrst: Vrst: PWL wave must contain at least one time/value pair |
| `vbr1_l2_flash_adc_mini_array:e2e` | `e2e` | `L2` | Data Converter Models | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Failed to parse tb_flash_adc_3b_ref.scs: Spectre-incompatible PWL wave syntax at line 13: multiline wave=[...] requires backslash line continuation |
| `vbr1_l2_flash_adc_mini_array:tb` | `tb` | `L2` | Data Converter Models | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Failed to parse tb_flash_adc_3b_ref.scs: Spectre-incompatible PWL wave syntax at line 10: multiline wave=[...] requires backslash line continuation |
| `vbr1_l2_pipeline_adc_chain:e2e` | `e2e` | `L2` | Data Converter Models | `missing_disciplines_vams_in_old_wrapper_candidate` | pipeline_adc_chain_4b.va:missing_disciplines_vams |
| `vbr1_l2_pipeline_adc_chain:tb` | `tb` | `L2` | Data Converter Models | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Invalid source Vin: Vin: PWL wave must contain at least one time/value pair |
| `vbr1_l2_weighted_sar_adc_dac_loop:e2e` | `e2e` | `L2` | Data Converter Models | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Invalid source Vrst_n: Vrst_n: PWL wave must contain at least one time/value pair |
| `vbr1_l1_bang_bang_phase_detector:e2e` | `e2e` | `L1` | PLL Clock and Timing Systems | `missing_disciplines_vams_in_old_wrapper_candidate` | bbpd_data_edge_alignment_ref.va:missing_disciplines_vams |
| `vbr1_l1_bang_bang_phase_detector:tb` | `tb` | `L1` | PLL Clock and Timing Systems | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Failed to parse tb_bbpd_data_edge_alignment_ref.scs: Spectre-incompatible PWL wave syntax at line 10: multiline wave=[...] requires backslash line continuation |
| `vbr1_l1_charge_pump_abstraction:bugfix` | `bugfix` | `L1` | PLL Clock and Timing Systems | `missing_disciplines_vams_in_old_wrapper_candidate` | charge_pump_abstraction.va:missing_disciplines_vams |
| `vbr1_l1_pfd_up_dn_logic:bugfix` | `bugfix` | `L1` | PLL Clock and Timing Systems | `missing_disciplines_vams_in_old_wrapper_candidate` | dut_fixed.va:missing_disciplines_vams |
| `vbr1_l1_pfd_up_dn_logic:tb` | `tb` | `L1` | PLL Clock and Timing Systems | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Invalid source Vref: Vref: PWL wave must contain at least one time/value pair |
| `vbr1_l1_limiting_amplifier_frontend:tb` | `tb` | `L1` | RF and AFE Behavioral Macromodels | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Failed to parse tb_limiting_amplifier_frontend.scs: Spectre-incompatible PWL wave syntax at line 7: multiline wave=[...] requires backslash line continuation |
| `vbr1_l1_lna_gain_compression_macro:e2e` | `e2e` | `L1` | RF and AFE Behavioral Macromodels | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Invalid source Vvin: Vvin: PWL wave must contain at least one time/value pair |
| `vbr1_l1_log_rssi_power_detector:bugfix` | `bugfix` | `L1` | RF and AFE Behavioral Macromodels | `missing_disciplines_vams_in_old_wrapper_candidate` | log_rssi_power_detector.va:missing_disciplines_vams |
| `vbr1_l1_rf_mixer_downconverter_macro:bugfix` | `bugfix` | `L1` | RF and AFE Behavioral Macromodels | `missing_disciplines_vams_in_old_wrapper_candidate` | rf_mixer_downconverter_macro.va:missing_disciplines_vams |
| `vbr1_l2_iq_downconversion_chain:e2e` | `e2e` | `L2` | RF and AFE Behavioral Macromodels | `missing_disciplines_vams_in_old_wrapper_candidate` | iq_downconversion_chain.va:missing_disciplines_vams |
| `vbr1_l1_acquisition_limited_sample_and_hold:bugfix` | `bugfix` | `L1` | Sampling and Analog Memory | `missing_disciplines_vams_in_old_wrapper_candidate` | acquisition_limited_sample_hold.va:missing_disciplines_vams |
| `vbr1_l1_acquisition_limited_sample_and_hold:dut` | `dut` | `L1` | Sampling and Analog Memory | `missing_disciplines_vams_in_old_wrapper_candidate` | acquisition_limited_sample_hold.va:missing_disciplines_vams |
| `vbr1_l1_acquisition_limited_sample_and_hold:e2e` | `e2e` | `L1` | Sampling and Analog Memory | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Failed to parse tb_acquisition_limited_sample_hold.scs: Spectre-incompatible PWL wave syntax at line 7: multiline wave=[...] requires backslash line continuation |
| `vbr1_l1_aperture_delay_track_and_hold:e2e` | `e2e` | `L1` | Sampling and Analog Memory | `missing_disciplines_vams_in_old_wrapper_candidate` | sample_hold_aperture_ref.va:missing_disciplines_vams |
| `vbr1_l1_sample_and_hold_with_droop_leakage:e2e` | `e2e` | `L1` | Sampling and Analog Memory | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Failed to parse tb_leaky_hold_ref.scs: Spectre-incompatible PWL wave syntax at line 11: multiline wave=[...] requires backslash line continuation |
| `vbr1_l1_sample_and_hold_with_droop_leakage:tb` | `tb` | `L1` | Sampling and Analog Memory | `invalid_or_incomplete_pwl_source_syntax` | ERROR: Failed to parse tb_leaky_hold_ref.scs: Spectre-incompatible PWL wave syntax at line 9: multiline wave=[...] requires backslash line continuation |
