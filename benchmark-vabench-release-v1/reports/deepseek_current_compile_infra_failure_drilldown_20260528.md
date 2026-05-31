# DeepSeek Compile/Infra Failure Drilldown - 2026-05-28

Scope: `effective_latest_merged` from `deepseek_current_failed_tasks_20260528.csv`. This mixes the valid full v3 baseline with the valid v7 targeted slice for the 40 changed L1/L2 forms, so it is an operational debugging view rather than a paper score.

## Counts

| bucket | count |
| --- | --- |
| FAIL_DUT_COMPILE | 46 |
| FAIL_INFRA / missing artifact | 24 |
| FAIL_TB_COMPILE | 14 |
| simulation output missing | 2 |

## Root-Cause Patterns

### FAIL_DUT_COMPILE

- 24 generic compile/staging crashes: summary notes only contain `returncode=1`, `dut_not_compiled`, `tb_not_executed`, and `tran.csv missing`. A rerun of `vbr1_l1_higher_order_filter:dut` shows the concrete mechanism: local declaration inside an analog event block, rejected as Spectre-incompatible.
- 12 `conditional_transition`: model places `transition(...)` under a conditional/event-controlled branch. This violates the strict Verilog-A subset we use for EVAS/Spectre alignment.
- 8 `conditional_cross`: model places `cross(...)` inside a conditional procedural block instead of an unconditional analog event expression.
- 1 `dynamic_analog_vector_index`: DWA pointer generation uses variable indices on analog vectors such as `code_msb_i[i]`/`ptr_o[i]`.
- 1 `digital_verilog_syntax`: model emits digital Verilog `always @(` syntax in a `.va` file.

Representative rerun evidence:

```text
vbr1_l1_higher_order_filter:dut
ERROR: Failed to compile Verilog-A file higher_order_filter.va:
Parse error: Spectre-incompatible local declaration inside analog/procedural statement; move declarations to module scope
```

### FAIL_INFRA / Missing Artifact

- 19 cases are `no_code_extracted` with `finish_reason=length`; `raw_response.txt` is empty and no candidate `.va`/`.scs` file exists. These are mostly e2e forms where the model ran into the output limit or failed to emit parseable fenced files.
- 5 cases are partial generations: a `.va` file exists, but `testbench.scs` is missing. These are also mostly e2e tasks where the model starts with DUT code and never reaches the required TB file.

Partial-generation examples: `vbr1_l2_ldo_load_step_recovery_flow:e2e`, `vbr1_l1_capacitive_weighted_sar_feedback_dac:e2e`, `vbr1_l2_converter_static_linearity_measurement_flow:e2e`, `vbr1_l1_lna_gain_compression_macro:e2e`, `vbr1_l2_pipeline_adc_chain:e2e`.

### FAIL_TB_COMPILE

- 11 generic TB execution failures: generated `.scs` exists, gold DUT compiles, but TB parsing/execution stops before `tran.csv`.
- 1 undefined module: generated TB instantiates `vpulse`/`vpwl` as modules instead of using `vsource type=pulse/pwl`.
- 2 TB forms are classified as TB compile but notes include `dut_not_compiled`; these are harness/include coupling failures rather than pure DUT design errors.

Representative rerun evidence:

```text
vbr1_l1_programmable_gain_amplifier:tb
ERROR: Invalid source Vrst: PWL waveform times must be strictly increasing
ERROR: Invalid source Vgs: PWL waveform times must be strictly increasing
ERROR: Invalid source Vvin: PWL waveform times must be strictly increasing

vbr1_l2_weighted_sar_adc_dac_loop:tb
ERROR: Cannot find VA file: 'sar_adc_weighted_8b.va'
ERROR: Cannot find VA file: 'sh_ideal.va'

vbr1_l2_pipeline_adc_chain:tb
ERROR: Invalid source Vvin: PWL wave must contain at least one time/value pair
```

### Simulation Output Missing

These are not checker-value mismatches. DUT and TB reach the simulator, then EVAS crashes before writing `tran.csv`.

```text
vbr1_l1_log_rssi_power_detector:e2e
ZeroDivisionError: float division by zero

vbr1_l1_lock_detector:bugfix
KeyError: 'rst_n'
```

## Task List: FAIL_DUT_COMPILE

| source_scope | release_task_id | task_id | form | status | reason_detail |
| --- | --- | --- | --- | --- | --- |
| formal_full_v3 | vbr1_l1_higher_order_filter:dut | vbr1_l1_higher_order_filter_dut | dut | FAIL_DUT_COMPILE | returncode=1 ; dut_not_compiled ; tb_not_executed ; tran.csv missing |
| formal_full_v3 | vbr1_l1_precision_rectifier_envelope_detector:e2e | vbr1_l1_precision_rectifier_envelope_detector_e2e | e2e | FAIL_DUT_COMPILE | returncode=1 ; dut_not_compiled ; tb_not_executed ; tran.csv missing |
| formal_full_v3 | vbr1_l1_programmable_gain_amplifier:e2e | vbr1_l1_programmable_gain_amplifier_e2e | e2e | FAIL_DUT_COMPILE | returncode=1 ; dut_not_compiled ; tb_not_executed ; tran.csv missing |
| formal_full_v3 | vbr1_l1_soft_hysteretic_limiter:dut | vbr1_l1_soft_hysteretic_limiter_dut | dut | FAIL_DUT_COMPILE | returncode=1 ; dut_not_compiled ; tb_not_executed ; tran.csv missing |
| formal_full_v3 | vbr1_l1_bias_voltage_generator_with_enable_trim:e2e | vbr1_l1_bias_voltage_generator_with_enable_trim_e2e | e2e | FAIL_DUT_COMPILE | returncode=1 ; dut_not_compiled ; tb_not_executed ; tran.csv missing |
| formal_full_v3 | vbr1_l1_ldo_regulator_macro_model:e2e | vbr1_l1_ldo_regulator_macro_model_e2e | e2e | FAIL_DUT_COMPILE | returncode=1 ; dut_not_compiled ; tb_not_executed ; tran.csv missing |
| formal_full_v3 | vbr1_l1_power_on_reset_detector:bugfix | vbr1_l1_power_on_reset_detector_bugfix | bugfix | FAIL_DUT_COMPILE | spectre_strict:conditional_transition=power_on_reset_detector.va |
| formal_full_v3 | vbr1_l1_ptat_ctat_reference_generator:dut | vbr1_l1_ptat_ctat_reference_generator_dut | dut | FAIL_DUT_COMPILE | spectre_strict:conditional_transition=ptat_ctat_reference_generator.va |
| formal_full_v3 | vbr1_l1_uvlo_brownout_detector:dut | vbr1_l1_uvlo_brownout_detector_dut | dut | FAIL_DUT_COMPILE | spectre_strict:conditional_transition=uvlo_brownout_detector.va |
| formal_full_v3 | vbr1_l1_uvlo_brownout_detector:e2e | vbr1_l1_uvlo_brownout_detector_e2e | e2e | FAIL_DUT_COMPILE | returncode=1 ; dut_not_compiled ; tb_not_executed ; tran.csv missing |
| formal_full_v3 | vbr1_l1_calibration_deadband_controller:dut | vbr1_l1_calibration_deadband_controller_dut | dut | FAIL_DUT_COMPILE | spectre_strict:conditional_cross=calibration_deadband_controller.va:41:conditional_block |
| formal_full_v3 | vbr1_l1_dwa_dem_encoder:bugfix | vbr1_l1_dwa_dem_encoder_bugfix | bugfix | FAIL_DUT_COMPILE | aux_include=v2b_4b.va ; spectre_strict:dynamic_analog_vector_index=dwa_ptr_gen.va:55:i:code_msb_i[i],dwa_ptr_gen.va:73:i:ptr_o[i],dwa_ptr_gen.va:75:i:ptr_o[i],dwa_ptr_gen.va:86:i:code_msb_i[i],dwa_ptr_gen.va:99:i:cell_en_o[i],dwa_ptr_gen.va:101:i:cell_en_o[i],dwa_ptr_gen.va:106:i:cell_en_o[i],dwa_ptr_gen.va:108:i:cell_en_o[i] |
| formal_full_v3 | vbr1_l1_successive_approximation_calibration_search_fsm:e2e | vbr1_l1_successive_approximation_calibration_search_fsm_e2e | e2e | FAIL_DUT_COMPILE | spectre_strict:conditional_cross=successive_approximation_calibration_search_fsm.va:28:conditional_block |
| formal_full_v3 | vbr1_l1_debounce_latch:dut | vbm1_debounce_latch_dut | dut | FAIL_DUT_COMPILE | spectre_strict:conditional_cross=debounce_latch.va:26:conditional_block |
| formal_full_v3 | vbr1_l1_debounce_latch:e2e | vbm1_debounce_latch_e2e | e2e | FAIL_DUT_COMPILE | returncode=1 ; dut_not_compiled ; tb_not_executed ; tran.csv missing |
| formal_full_v3 | vbr1_l1_hysteresis_comparator:bugfix | vbr1_l1_hysteresis_comparator_bugfix | bugfix | FAIL_DUT_COMPILE | returncode=1 ; dut_not_compiled ; tb_not_executed ; tran.csv missing |
| formal_full_v3 | vbr1_l1_hysteresis_comparator:dut | vbr1_l1_hysteresis_comparator_dut | dut | FAIL_DUT_COMPILE | spectre_strict:conditional_transition=cmp_hysteresis.va |
| formal_full_v3 | vbr1_l1_propagation_delay_comparator:bugfix | vbr1_l1_propagation_delay_comparator_bugfix | bugfix | FAIL_DUT_COMPILE | aux_include=edge_interval_timer.va ; spectre_strict:conditional_transition=cmp_delay.va |
| formal_full_v3 | vbr1_l1_threshold_comparator:bugfix | vbr1_l1_threshold_comparator_bugfix | bugfix | FAIL_DUT_COMPILE | spectre_strict:conditional_transition=dut_fixed.va |
| formal_full_v3 | vbr1_l1_window_comparator_detector:dut | vbr1_l1_window_comparator_detector_dut | dut | FAIL_DUT_COMPILE | spectre_strict:conditional_transition=window_comparator_ref.va |
| formal_full_v3 | vbr1_l1_dac_mismatch_unit_weighting_model:e2e | vbr1_l1_dac_mismatch_unit_weighting_model_e2e | e2e | FAIL_DUT_COMPILE | returncode=1 ; dut_not_compiled ; tb_not_executed ; tran.csv missing |
| formal_full_v3 | vbr1_l1_charge_pump_abstraction:tb | vbr1_l1_charge_pump_abstraction_tb | tb | FAIL_DUT_COMPILE | returncode=1 ; dut_not_compiled ; tb_not_executed ; tran.csv missing |
| formal_full_v3 | vbr1_l1_clock_divider:bugfix | vbr1_l1_clock_divider_bugfix | bugfix | FAIL_DUT_COMPILE | spectre_strict:conditional_cross=clk_divider_ref.va:44:conditional_block |
| formal_full_v3 | vbr1_l1_limiting_amplifier_frontend:tb | vbr1_l1_limiting_amplifier_frontend_tb | tb | FAIL_DUT_COMPILE | returncode=1 ; dut_not_compiled ; tb_not_executed ; tran.csv missing |
| formal_full_v3 | vbr1_l1_lna_gain_compression_macro:dut | vbr1_l1_lna_gain_compression_macro_dut | dut | FAIL_DUT_COMPILE | spectre_strict:conditional_transition=lna_gain_compression_macro.va |
| formal_full_v3 | vbr1_l1_log_rssi_power_detector:dut | vbr1_l1_log_rssi_power_detector_dut | dut | FAIL_DUT_COMPILE | spectre_strict:conditional_cross=log_rssi_power_detector.va:39:conditional_block |
| formal_full_v3 | vbr1_l1_log_rssi_power_detector:tb | vbr1_l1_log_rssi_power_detector_tb | tb | FAIL_DUT_COMPILE | returncode=1 ; dut_not_compiled ; tb_not_executed ; tran.csv missing |
| formal_full_v3 | vbr1_l1_pa_compression_macro:e2e | vbr1_l1_pa_compression_macro_e2e | e2e | FAIL_DUT_COMPILE | spectre_strict:conditional_transition=pa_compression_macro.va |
| formal_full_v3 | vbr1_l1_acquisition_limited_sample_and_hold:e2e | vbr1_l1_acquisition_limited_sample_and_hold_e2e | e2e | FAIL_DUT_COMPILE | spectre_strict:digital_verilog_syntax=digital_always_block: always @( in acquisition_limited_sample_hold.va |
| formal_full_v3 | vbr1_l1_aperture_delay_track_and_hold:e2e | vbr1_l1_aperture_delay_track_and_hold_e2e | e2e | FAIL_DUT_COMPILE | returncode=1 ; dut_not_compiled ; tb_not_executed ; tran.csv missing |
| formal_full_v3 | vbr1_l1_aperture_delay_track_and_hold:tb | vbr1_l1_aperture_delay_track_and_hold_tb | tb | FAIL_DUT_COMPILE | returncode=1 ; dut_not_compiled ; tb_not_executed ; tran.csv missing |
| formal_full_v3 | vbr1_l1_sar_logic:tb | vbm1_sar_logic_4b_tb | tb | FAIL_DUT_COMPILE | returncode=1 ; dut_not_compiled ; tb_not_executed ; tran.csv missing |
| formal_full_v3 | vbr1_l1_element_shuffler:bugfix | vbm1_element_shuffler_bugfix | bugfix | FAIL_DUT_COMPILE | spectre_strict:conditional_cross=dut_fixed.va:26:conditional_block |
| formal_full_v3 | vbr1_l1_element_shuffler:dut | vbm1_element_shuffler_dut | dut | FAIL_DUT_COMPILE | spectre_strict:conditional_cross=element_shuffler.va:25:conditional_block |
| formal_full_v3 | vbr1_l1_hysteresis_comparator:e2e | comparator_hysteresis_smoke | e2e | FAIL_DUT_COMPILE | returncode=1 ; dut_not_compiled ; tb_not_executed ; tran.csv missing |
| formal_full_v3 | vbr1_l1_offset_comparator:e2e | vbm1_offset_comparator_e2e | e2e | FAIL_DUT_COMPILE | returncode=1 ; dut_not_compiled ; tb_not_executed ; tran.csv missing |
| formal_full_v3 | vbr1_l1_strongarm_style_latch_comparator:dut | vbm1_strongarm_comparator_behavior_dut | dut | FAIL_DUT_COMPILE | spectre_strict:conditional_transition=cmp_strongarm.va |
| formal_full_v3 | vbr1_l1_strongarm_style_latch_comparator:e2e | vbm1_strongarm_comparator_behavior_e2e | e2e | FAIL_DUT_COMPILE | returncode=1 ; dut_not_compiled ; tb_not_executed ; tran.csv missing |
| formal_full_v3 | vbr1_l1_thermometer_code_decoder:bugfix | vbm1_thermometer_decoder_guarded_bugfix | bugfix | FAIL_DUT_COMPILE | spectre_strict:conditional_transition=dut_fixed.va |
| formal_full_v3 | vbr1_l1_thermometer_code_decoder:e2e | vbm1_thermometer_decoder_guarded_e2e | e2e | FAIL_DUT_COMPILE | spectre_strict:conditional_transition=thermometer_decoder_guarded.va |
| formal_full_v3 | vbr1_l1_thermometer_code_decoder:tb | vbm1_thermometer_decoder_guarded_tb | tb | FAIL_DUT_COMPILE | returncode=1 ; dut_not_compiled ; tb_not_executed ; tran.csv missing |
| formal_full_v3 | vbr1_l1_clocked_adc_quantizer:e2e | flash_adc_3b_smoke | e2e | FAIL_DUT_COMPILE | returncode=1 ; dut_not_compiled ; tb_not_executed ; tran.csv missing |
| targeted_slice_v7 | vbr1_l2_flash_adc_mini_array:e2e | flash_adc_mini_array_e2e | e2e | FAIL_DUT_COMPILE | returncode=1 ; dut_not_compiled ; tb_not_executed ; tran.csv missing |
| formal_full_v3 | vbr1_l1_clock_divider:dut | vbm1_resettable_counter_divider_dut | dut | FAIL_DUT_COMPILE | spectre_strict:conditional_cross=clk_divider_ref.va:40:conditional_block |
| formal_full_v3 | vbr1_l1_slew_rate_limiter:bugfix | vbm1_slew_rate_limiter_bugfix | bugfix | FAIL_DUT_COMPILE | returncode=1 ; dut_not_compiled ; tb_not_executed ; tran.csv missing |
| formal_full_v3 | vbr1_l1_slew_rate_limiter:e2e | vbm1_slew_rate_limiter_e2e | e2e | FAIL_DUT_COMPILE | returncode=1 ; dut_not_compiled ; tb_not_executed ; tran.csv missing |

## Task List: FAIL_INFRA / missing artifact

| source_scope | release_task_id | task_id | form | status | reason_detail |
| --- | --- | --- | --- | --- | --- |
| formal_full_v3 | vbr1_l1_bandgap_reference_macro_model:e2e | vbr1_l1_bandgap_reference_macro_model_e2e | e2e | FAIL_INFRA | missing_generated_files: dut.va, testbench.scs |
| formal_full_v3 | vbr1_l1_power_on_reset_detector:e2e | vbr1_l1_power_on_reset_detector_e2e | e2e | FAIL_INFRA | missing_generated_files: dut.va, testbench.scs |
| targeted_slice_v7 | vbr1_l2_ldo_load_step_recovery_flow:e2e | vbr1_l2_ldo_load_step_recovery_flow_e2e | e2e | FAIL_INFRA | missing_generated_files: testbench.scs |
| targeted_slice_v7 | vbr1_l2_reference_startup_enable_flow:e2e | vbr1_l2_reference_startup_enable_flow_e2e | e2e | FAIL_INFRA | missing_generated_files: dut.va, testbench.scs |
| formal_full_v3 | vbr1_l1_calibration_deadband_controller:e2e | vbr1_l1_calibration_deadband_controller_e2e | e2e | FAIL_INFRA | missing_generated_files: dut.va, testbench.scs |
| formal_full_v3 | vbr1_l1_capacitive_weighted_sar_feedback_dac:e2e | vbr1_l1_capacitive_weighted_sar_feedback_dac_e2e | e2e | FAIL_INFRA | missing_generated_files: testbench.scs |
| targeted_slice_v7 | vbr1_l1_capacitive_weighted_sar_feedback_dac:tb | vbr1_l1_capacitive_weighted_sar_feedback_dac_tb | tb | FAIL_INFRA | missing_generated_files: testbench.scs |
| targeted_slice_v7 | vbr1_l2_converter_static_linearity_measurement_flow:e2e | vbr1_l2_converter_static_linearity_measurement_flow_e2e | e2e | FAIL_INFRA | missing_generated_files: testbench.scs |
| formal_full_v3 | vbr1_l1_bang_bang_phase_detector:tb | vbr1_l1_bang_bang_phase_detector_tb | tb | FAIL_INFRA | missing_generated_files: testbench.scs |
| formal_full_v3 | vbr1_l1_charge_pump_abstraction:e2e | vbr1_l1_charge_pump_abstraction_e2e | e2e | FAIL_INFRA | missing_generated_files: dut.va, testbench.scs |
| formal_full_v3 | vbr1_l1_lna_gain_compression_macro:e2e | vbr1_l1_lna_gain_compression_macro_e2e | e2e | FAIL_INFRA | missing_generated_files: testbench.scs |
| targeted_slice_v7 | vbr1_l2_agc_receiver_leveling_loop:e2e | vbr1_l2_agc_receiver_leveling_loop_e2e | e2e | FAIL_INFRA | missing_generated_files: dut.va, testbench.scs |
| formal_full_v3 | vbr1_l1_sample_and_hold_with_droop_leakage:e2e | vbr1_l1_sample_and_hold_with_droop_leakage_e2e | e2e | FAIL_INFRA | missing_generated_files: dut.va, testbench.scs |
| formal_full_v3 | vbr1_l1_sar_logic:e2e | vbm1_sar_logic_4b_e2e | e2e | FAIL_INFRA | missing_generated_files: dut.va, testbench.scs |
| formal_full_v3 | vbr1_l1_dwa_dem_encoder:e2e | dwa_ptr_gen_smoke | e2e | FAIL_INFRA | missing_generated_files: dut.va, testbench.scs |
| formal_full_v3 | vbr1_l1_propagation_delay_comparator:e2e | cmp_delay_smoke | e2e | FAIL_INFRA | missing_generated_files: dut.va, testbench.scs |
| targeted_slice_v7 | vbr1_l1_binary_weighted_voltage_dac:e2e | vbm1_simple_binary_voltage_dac_4b_e2e | e2e | FAIL_INFRA | missing_generated_files: dut.va, testbench.scs |
| targeted_slice_v7 | vbr1_l2_pipeline_adc_chain:e2e | pipeline_adc_chain_e2e | e2e | FAIL_INFRA | missing_generated_files: testbench.scs |
| formal_full_v3 | vbr1_l1_clock_divider:e2e | vbm1_resettable_counter_divider_e2e | e2e | FAIL_INFRA | missing_generated_files: dut.va, testbench.scs |
| formal_full_v3 | vbr1_l1_bang_bang_phase_detector:e2e | bbpd_data_edge_alignment_smoke | e2e | FAIL_INFRA | missing_generated_files: dut.va, testbench.scs |
| formal_full_v3 | vbr1_l1_pfd_up_dn_logic:e2e | vbm1_pfd_reset_race_e2e | e2e | FAIL_INFRA | missing_generated_files: dut.va, testbench.scs |
| formal_full_v3 | vbr1_l1_lock_detector:e2e | vbm1_lock_detector_e2e | e2e | FAIL_INFRA | missing_generated_files: dut.va, testbench.scs |
| targeted_slice_v7 | vbr1_l2_adpll_lock_ratio_hop_timer_flow:e2e | adpll_ratio_hop_smoke | e2e | FAIL_INFRA | missing_generated_files: dut.va, testbench.scs |
| targeted_slice_v7 | vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow:e2e | cppll_freq_step_reacquire_smoke | e2e | FAIL_INFRA | missing_generated_files: dut.va, testbench.scs |

## Task List: FAIL_TB_COMPILE

| source_scope | release_task_id | task_id | form | status | reason_detail |
| --- | --- | --- | --- | --- | --- |
| formal_full_v3 | vbr1_l1_programmable_gain_amplifier:tb | vbr1_l1_programmable_gain_amplifier_tb | tb | FAIL_TB_COMPILE | returncode=1 ; tb_not_executed ; tran.csv missing |
| formal_full_v3 | vbr1_l1_soft_hysteretic_limiter:tb | vbr1_l1_soft_hysteretic_limiter_tb | tb | FAIL_TB_COMPILE | spectre_strict:undefined_module=vpulse,vpwl;available_modules=soft_hysteretic_limiter |
| targeted_slice_v7 | vbr1_l2_amplifier_filter_chain:tb | vbr1_l2_amplifier_filter_chain_tb | tb | FAIL_TB_COMPILE | returncode=1 ; tb_not_executed ; tran.csv missing |
| formal_full_v3 | vbr1_l1_propagation_delay_comparator:tb | vbr1_l1_propagation_delay_comparator_tb | tb | FAIL_TB_COMPILE | returncode=1 ; dut_not_compiled ; tb_not_executed ; tran.csv missing |
| targeted_slice_v7 | vbr1_l2_weighted_sar_adc_dac_loop:tb | vbr1_l2_weighted_sar_adc_dac_loop_tb | tb | FAIL_TB_COMPILE | returncode=1 ; tb_not_executed ; tran.csv missing |
| formal_full_v3 | vbr1_l1_acquisition_limited_sample_and_hold:tb | vbr1_l1_acquisition_limited_sample_and_hold_tb | tb | FAIL_TB_COMPILE | returncode=1 ; tb_not_executed ; tran.csv missing |
| formal_full_v3 | vbr1_l1_clocked_sample_and_hold:tb | vbr1_l1_clocked_sample_and_hold_tb | tb | FAIL_TB_COMPILE | returncode=1 ; tb_not_executed ; tran.csv missing |
| targeted_slice_v7 | vbr1_l2_converter_front_end:e2e | vbr1_l2_converter_front_end_e2e | e2e | FAIL_TB_COMPILE | returncode=1 ; tb_not_executed ; tran.csv missing |
| formal_full_v3 | vbr1_l1_pipeline_adc_stage:tb | vbr1_l1_pipeline_adc_stage_tb | tb | FAIL_TB_COMPILE | returncode=1 ; dut_not_compiled ; tb_not_executed ; tran.csv missing |
| formal_full_v3 | vbr1_l1_gain_trim_controller:tb | vbm1_gain_trim_controller_tb | tb | FAIL_TB_COMPILE | returncode=1 ; tb_not_executed ; tran.csv missing |
| targeted_slice_v7 | vbr1_l1_binary_weighted_voltage_dac:tb | vbm1_simple_binary_voltage_dac_4b_tb | tb | FAIL_TB_COMPILE | returncode=1 ; tb_not_executed ; tran.csv missing |
| targeted_slice_v7 | vbr1_l1_unit_element_thermometer_dac:e2e | vbm1_thermometer_dac_15seg_e2e | e2e | FAIL_TB_COMPILE | returncode=1 ; tb_not_executed ; tran.csv missing |
| formal_full_v3 | vbr1_l1_unit_element_thermometer_dac:tb | vbm1_thermometer_dac_15seg_tb | tb | FAIL_TB_COMPILE | returncode=1 ; tb_not_executed ; tran.csv missing |
| targeted_slice_v7 | vbr1_l2_pipeline_adc_chain:tb | vbr1_l2_pipeline_adc_chain_tb | tb | FAIL_TB_COMPILE | returncode=1 ; tb_not_executed ; tran.csv missing |

## Task List: simulation output missing

| source_scope | release_task_id | task_id | form | status | reason_detail |
| --- | --- | --- | --- | --- | --- |
| formal_full_v3 | vbr1_l1_log_rssi_power_detector:e2e | vbr1_l1_log_rssi_power_detector_e2e | e2e | FAIL_SIM_CORRECTNESS | returncode=1 ; tran.csv missing |
| formal_full_v3 | vbr1_l1_lock_detector:bugfix | vbm1_lock_detector_bugfix | bugfix | FAIL_SIM_CORRECTNESS | returncode=1 ; tran.csv missing |
