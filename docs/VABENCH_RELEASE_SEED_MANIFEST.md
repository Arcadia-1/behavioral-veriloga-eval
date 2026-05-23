# vaBench Release Seed Manifest

Date: 2026-05-16

This manifest records current L1 seed entries copied from reviewed
source tasks plus generated true-bugfix companions where a single-cause
badcase could be reconstructed from existing release gold.

## Summary

| Metric | Count |
| --- | ---: |
| seed entries | 24 |
| seed entries with all required forms present | 24 |
| generated true-bugfix companions in seed rows | 2 |

## Rows

| Entry | Base ID | Forms | Missing forms | Package task dir | Notes |
| --- | --- | --- | --- | --- | --- |
| `vbr1_l1_binary_weighted_voltage_dac` | `simple_binary_voltage_dac_4b` | `dut|tb|bugfix|e2e` | `` | `benchmark-vabench-release-v1/tasks/CT01_data_converters/vbr1_l1_binary_weighted_voltage_dac` | release assets copied from source tasks; not scored until certified |
| `vbr1_l1_segmented_dac` | `segmented_dac` | `dut|tb|bugfix|e2e` | `` | `benchmark-vabench-release-v1/tasks/CT01_data_converters/vbr1_l1_segmented_dac` | release assets copied from source tasks; not scored until certified |
| `vbr1_l1_thermometer_code_decoder` | `thermometer_decoder_guarded` | `dut|tb|bugfix|e2e` | `` | `benchmark-vabench-release-v1/tasks/CT01_data_converters/vbr1_l1_thermometer_code_decoder` | release assets copied from source tasks; not scored until certified |
| `vbr1_l1_sar_logic` | `sar_logic_4b` | `dut|tb|bugfix|e2e` | `` | `benchmark-vabench-release-v1/tasks/CT01_data_converters/vbr1_l1_sar_logic` | release assets copied from source tasks; not scored until certified |
| `vbr1_l1_offset_comparator` | `offset_comparator` | `dut|tb|bugfix|e2e` | `` | `benchmark-vabench-release-v1/tasks/CT02_comparators_and_decision_circuits/vbr1_l1_offset_comparator` | release assets copied from source tasks; not scored until certified |
| `vbr1_l1_strongarm_style_latch_comparator` | `strongarm_comparator_behavior` | `dut|tb|bugfix|e2e` | `` | `benchmark-vabench-release-v1/tasks/CT02_comparators_and_decision_circuits/vbr1_l1_strongarm_style_latch_comparator` | release assets copied from source tasks; not scored until certified |
| `vbr1_l1_vco_phase_integrator` | `vco_phase_integrator` | `dut|tb|bugfix|e2e` | `` | `benchmark-vabench-release-v1/tasks/CT05_pll_clock_event_timing/vbr1_l1_vco_phase_integrator` | release assets copied from source tasks; not scored until certified; true-bugfix companion generated from existing release gold |
| `vbr1_l1_pfd_up_dn_logic` | `pfd_reset_race` | `dut|tb|bugfix|e2e` | `` | `benchmark-vabench-release-v1/tasks/CT05_pll_clock_event_timing/vbr1_l1_pfd_up_dn_logic` | release assets copied from source tasks; not scored until certified |
| `vbr1_l1_clock_divider` | `resettable_counter_divider` | `dut|tb|bugfix|e2e` | `` | `benchmark-vabench-release-v1/tasks/CT05_pll_clock_event_timing/vbr1_l1_clock_divider` | release assets copied from source tasks; not scored until certified; true-bugfix companion generated from existing release gold |
| `vbr1_l1_lock_detector` | `lock_detector` | `dut|tb|bugfix|e2e` | `` | `benchmark-vabench-release-v1/tasks/CT05_pll_clock_event_timing/vbr1_l1_lock_detector` | release assets copied from source tasks; not scored until certified |
| `vbr1_l1_trim_calibration_controller` | `cdac_calibration` | `dut|tb|bugfix|e2e` | `` | `benchmark-vabench-release-v1/tasks/CT07_calibration_dem_and_control/vbr1_l1_trim_calibration_controller` | release assets copied from source tasks; not scored until certified |
| `vbr1_l1_gain_trim_controller` | `gain_trim_controller` | `dut|tb|bugfix|e2e` | `` | `benchmark-vabench-release-v1/tasks/CT07_calibration_dem_and_control/vbr1_l1_gain_trim_controller` | release assets copied from source tasks; not scored until certified |
| `vbr1_l1_rotating_dem_selector` | `rotating_element_selector` | `dut|tb|bugfix|e2e` | `` | `benchmark-vabench-release-v1/tasks/CT07_calibration_dem_and_control/vbr1_l1_rotating_dem_selector` | release assets copied from source tasks; not scored until certified |
| `vbr1_l1_windowed_dem_pointer` | `barrel_pointer_window` | `dut|tb|bugfix|e2e` | `` | `benchmark-vabench-release-v1/tasks/CT07_calibration_dem_and_control/vbr1_l1_windowed_dem_pointer` | release assets copied from source tasks; not scored until certified |
| `vbr1_l1_element_shuffler` | `element_shuffler` | `dut|tb|bugfix|e2e` | `` | `benchmark-vabench-release-v1/tasks/CT07_calibration_dem_and_control/vbr1_l1_element_shuffler` | release assets copied from source tasks; not scored until certified |
| `vbr1_l1_debounce_latch` | `debounce_latch` | `dut|tb|bugfix|e2e` | `` | `benchmark-vabench-release-v1/tasks/CT02_comparators_and_decision_circuits/vbr1_l1_debounce_latch` | release assets copied from source tasks; not scored until certified |
| `vbr1_l1_crossing_metric_writer` | `file_metric_writer` | `tb|dut|e2e` | `` | `benchmark-vabench-release-v1/tasks/CT08_measurement_and_testbench_instrumentation/vbr1_l1_crossing_metric_writer` | release assets copied from source tasks; not scored until certified |
| `vbr1_l1_settling_time_detector` | `settling_time_measurement_tb` | `tb|e2e` | `` | `benchmark-vabench-release-v1/tasks/CT08_measurement_and_testbench_instrumentation/vbr1_l1_settling_time_detector` | release assets copied from source tasks; not scored until certified |
| `vbr1_l1_peak_detector` | `peak_detector` | `dut|tb|bugfix|e2e` | `` | `benchmark-vabench-release-v1/tasks/CT08_measurement_and_testbench_instrumentation/vbr1_l1_peak_detector` | release assets copied from source tasks; not scored until certified |
| `vbr1_l1_first_order_lowpass` | `first_order_lowpass` | `dut|tb|bugfix|e2e` | `` | `benchmark-vabench-release-v1/tasks/CT04_analog_behavioral_signal_conditioning/vbr1_l1_first_order_lowpass` | release assets copied from source tasks; not scored until certified |
| `vbr1_l1_resettable_integrator` | `resettable_integrator` | `dut|tb|bugfix|e2e` | `` | `benchmark-vabench-release-v1/tasks/CT04_analog_behavioral_signal_conditioning/vbr1_l1_resettable_integrator` | release assets copied from source tasks; not scored until certified |
| `vbr1_l1_slew_rate_limiter` | `slew_rate_limiter` | `dut|tb|bugfix|e2e` | `` | `benchmark-vabench-release-v1/tasks/CT04_analog_behavioral_signal_conditioning/vbr1_l1_slew_rate_limiter` | release assets copied from source tasks; not scored until certified |
| `vbr1_l1_aperture_delay_track_and_hold` | `track_hold_aperture` | `dut|tb|bugfix|e2e` | `` | `benchmark-vabench-release-v1/tasks/CT03_sample_hold_and_analog_memory/vbr1_l1_aperture_delay_track_and_hold` | release assets copied from source tasks; not scored until certified |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `leaky_hold` | `dut|tb|bugfix|e2e` | `` | `benchmark-vabench-release-v1/tasks/CT03_sample_hold_and_analog_memory/vbr1_l1_sample_and_hold_with_droop_leakage` | release assets copied from source tasks; not scored until certified |
