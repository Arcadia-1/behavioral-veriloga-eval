# L1/L2 Prompt-Sufficiency Rerun Manifest

Rows: 40

Claim boundary: This is a targeted rerun manifest for prompt changes only; it is not the full 236-form baseline.

| Task | Level | Form | Difficulty | Category | Markers |
| --- | --- | --- | --- | --- | --- |
| `vbr1_l1_first_order_lowpass:bugfix` | `L1` | `bugfix` | `D1` | Baseband Signal Conditioning | `l1_bugfix_mismatch_framing` |
| `vbr1_l1_precision_rectifier_envelope_detector:bugfix` | `L1` | `bugfix` | `D2` | Baseband Signal Conditioning | `l1_bugfix_mismatch_framing` |
| `vbr1_l1_programmable_gain_amplifier:bugfix` | `L1` | `bugfix` | `D2` | Baseband Signal Conditioning | `l1_bugfix_mismatch_framing` |
| `vbr1_l1_resettable_integrator:bugfix` | `L1` | `bugfix` | `D2` | Baseband Signal Conditioning | `l1_bugfix_mismatch_framing` |
| `vbr1_l2_amplifier_filter_chain:e2e` | `L2` | `e2e` | `D3` | Baseband Signal Conditioning | `l2_behavior_contract` |
| `vbr1_l2_amplifier_filter_chain:tb` | `L2` | `tb` | `D3` | Baseband Signal Conditioning | `l2_behavior_contract` |
| `vbr1_l2_ldo_load_step_recovery_flow:e2e` | `L2` | `e2e` | `D3` | Bias Reference and Power Management | `l2_behavior_contract` |
| `vbr1_l2_ldo_load_step_recovery_flow:tb` | `L2` | `tb` | `D3` | Bias Reference and Power Management | `l2_behavior_contract` |
| `vbr1_l2_reference_startup_enable_flow:e2e` | `L2` | `e2e` | `D3` | Bias Reference and Power Management | `l2_behavior_contract` |
| `vbr1_l2_reference_startup_enable_flow:tb` | `L2` | `tb` | `D3` | Bias Reference and Power Management | `l2_behavior_contract` |
| `vbr1_l1_dwa_dem_encoder:tb` | `L1` | `tb` | `D2` | Calibration, DEM, and Control | `l1_tb_stimulus_contract` |
| `vbr1_l2_complete_calibration_loop:e2e` | `L2` | `e2e` | `D3` | Calibration, DEM, and Control | `l2_behavior_contract` |
| `vbr1_l2_complete_calibration_loop:tb` | `L2` | `tb` | `D3` | Calibration, DEM, and Control | `l2_behavior_contract` |
| `vbr1_l2_comparator_measurement_flow:e2e` | `L2` | `e2e` | `D3` | Comparator and Decision Circuits | `l2_behavior_contract` |
| `vbr1_l2_comparator_measurement_flow:tb` | `L2` | `tb` | `D3` | Comparator and Decision Circuits | `l2_behavior_contract` |
| `vbr1_l1_binary_weighted_voltage_dac:e2e` | `L1` | `e2e` | `D1` | Data Converter Models | `l1_behavior_contract` |
| `vbr1_l1_binary_weighted_voltage_dac:tb` | `L1` | `tb` | `D1` | Data Converter Models | `l1_tb_stimulus_contract` |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac:tb` | `L1` | `tb` | `D2` | Data Converter Models | `legacy_public_stimulus_schedule` |
| `vbr1_l1_clocked_adc_quantizer:tb` | `L1` | `tb` | `D2` | Data Converter Models | `l1_tb_stimulus_contract` |
| `vbr1_l1_pipeline_adc_stage:e2e` | `L1` | `e2e` | `D3` | Data Converter Models | `l1_behavior_contract` |
| `vbr1_l1_unit_element_thermometer_dac:e2e` | `L1` | `e2e` | `D1` | Data Converter Models | `l1_behavior_contract` |
| `vbr1_l2_converter_static_linearity_measurement_flow:e2e` | `L2` | `e2e` | `D3` | Data Converter Models | `l2_behavior_contract` |
| `vbr1_l2_converter_static_linearity_measurement_flow:tb` | `L2` | `tb` | `D3` | Data Converter Models | `l2_behavior_contract` |
| `vbr1_l2_flash_adc_mini_array:e2e` | `L2` | `e2e` | `D3` | Data Converter Models | `l2_behavior_contract` |
| `vbr1_l2_flash_adc_mini_array:tb` | `L2` | `tb` | `D3` | Data Converter Models | `l2_behavior_contract` |
| `vbr1_l2_pipeline_adc_chain:e2e` | `L2` | `e2e` | `D3` | Data Converter Models | `l2_behavior_contract` |
| `vbr1_l2_pipeline_adc_chain:tb` | `L2` | `tb` | `D3` | Data Converter Models | `l2_behavior_contract` |
| `vbr1_l2_weighted_sar_adc_dac_loop:e2e` | `L2` | `e2e` | `D3` | Data Converter Models | `l2_behavior_contract` |
| `vbr1_l2_weighted_sar_adc_dac_loop:tb` | `L2` | `tb` | `D3` | Data Converter Models | `l2_behavior_contract` |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow:e2e` | `L2` | `e2e` | `D3` | PLL Clock and Timing Systems | `l2_behavior_contract` |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow:tb` | `L2` | `tb` | `D3` | PLL Clock and Timing Systems | `l2_behavior_contract` |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow:e2e` | `L2` | `e2e` | `D3` | PLL Clock and Timing Systems | `l2_behavior_contract` |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow:tb` | `L2` | `tb` | `D3` | PLL Clock and Timing Systems | `l2_behavior_contract` |
| `vbr1_l2_agc_receiver_leveling_loop:e2e` | `L2` | `e2e` | `D3` | RF and AFE Behavioral Macromodels | `l2_behavior_contract` |
| `vbr1_l2_agc_receiver_leveling_loop:tb` | `L2` | `tb` | `D3` | RF and AFE Behavioral Macromodels | `l2_behavior_contract` |
| `vbr1_l2_iq_downconversion_chain:e2e` | `L2` | `e2e` | `D3` | RF and AFE Behavioral Macromodels | `l2_behavior_contract` |
| `vbr1_l2_iq_downconversion_chain:tb` | `L2` | `tb` | `D3` | RF and AFE Behavioral Macromodels | `l2_behavior_contract` |
| `vbr1_l1_acquisition_limited_sample_and_hold:bugfix` | `L1` | `bugfix` | `D2` | Sampling and Analog Memory | `l1_bugfix_mismatch_framing` |
| `vbr1_l2_converter_front_end:e2e` | `L2` | `e2e` | `D3` | Sampling and Analog Memory | `l2_behavior_contract` |
| `vbr1_l2_converter_front_end:tb` | `L2` | `tb` | `D3` | Sampling and Analog Memory | `l2_behavior_contract` |
