# v3 Staged Promotion Gold Probe

Date: 2026-07-03

## Summary

- `gold_total`: 0
- `gold_pass`: 0
- `gold_fail`: 0
- `expectation_fail`: 0
- `skipped_staged_tasks`: 0
- `gold_wall_s_total`: 0
- `gold_wall_s_max`: 0.0
- `slow_gold_threshold_s`: 20.0
- `slow_gold_count`: 0
- `wall_s`: 399.17277

## Rows

| Task | Status | First behavior note |
| --- | --- | --- |
| `001-bang-bang-phase-detector` | `FAIL_SIM_CORRECTNESS` | data_edges=8 up_edges=3 down_edges=3 overlap_frac=0.0000 direction_up=0/3 direction_down=0/3 none=2/2 wrong_direction=6 missing_direction=0 false_pulse=0 |
| `001-bang-bang-phase-detector` | `FAIL_SIM_CORRECTNESS` | data_edges=8 up_edges=3 down_edges=0 overlap_frac=0.0000 direction_up=3/3 direction_down=0/3 none=2/2 wrong_direction=0 missing_direction=3 false_pulse=0 |
| `001-bang-bang-phase-detector` | `FAIL_SIM_CORRECTNESS` | data_edges=8 up_edges=3 down_edges=3 overlap_frac=0.0000 direction_up=2/3 direction_down=0/3 none=1/2 wrong_direction=4 missing_direction=0 false_pulse=1 |
| `001-bang-bang-phase-detector` | `FAIL_SIM_CORRECTNESS` | data_edges=8 up_edges=6 down_edges=6 overlap_frac=0.1992 direction_up=0/3 direction_down=0/3 none=2/2 wrong_direction=6 missing_direction=0 false_pulse=0 |
| `001-bang-bang-phase-detector` | `FAIL_SIM_CORRECTNESS` | data_edges=8 up_edges=4 down_edges=4 overlap_frac=0.0000 direction_up=3/3 direction_down=3/3 none=0/2 wrong_direction=0 missing_direction=0 false_pulse=2 |
| `002-capacitive-sar-feedback-dac` | `FAIL_SIM_CORRECTNESS` | samples=17 main_codes=16 cal_codes=[0, 1, 2, 3] mismatches=8 monotonic_errors=1 diff_span=0.6000 max_diff_error=0.0563 max_cm_error=0.0000 |
| `002-capacitive-sar-feedback-dac` | `FAIL_SIM_CORRECTNESS` | samples=17 main_codes=16 cal_codes=[0, 1, 2, 3] mismatches=17 monotonic_errors=9 diff_span=0.6563 max_diff_error=0.7126 max_cm_error=0.0000 |
| `002-capacitive-sar-feedback-dac` | `FAIL_SIM_CORRECTNESS` | samples=17 main_codes=16 cal_codes=[0, 1, 2, 3] mismatches=4 monotonic_errors=1 diff_span=0.6563 max_diff_error=0.1501 max_cm_error=0.0000 |
| `002-capacitive-sar-feedback-dac` | `FAIL_SIM_CORRECTNESS` | samples=17 main_codes=16 cal_codes=[0, 1, 2, 3] mismatches=4 monotonic_errors=1 diff_span=0.6282 max_diff_error=0.0282 max_cm_error=0.0000 |
| `002-capacitive-sar-feedback-dac` | `FAIL_SIM_CORRECTNESS` | samples=17 main_codes=16 cal_codes=[0, 1, 2, 3] mismatches=17 monotonic_errors=0 diff_span=0.6563 max_diff_error=0.0000 max_cm_error=0.0500 |
| `003-pipeline-adc-stage` | `FAIL_SIM_CORRECTNESS` | regions=upper:3,middle:4,lower:3 bit_mismatches=4 residue_mismatches=4 max_residue_err=0.4480 bounded_failures=0 |
| `003-pipeline-adc-stage` | `FAIL_SIM_CORRECTNESS` | regions=upper:3,middle:4,lower:3 bit_mismatches=3 residue_mismatches=0 max_residue_err=0.0000 bounded_failures=0 |
| `003-pipeline-adc-stage` | `FAIL_SIM_CORRECTNESS` | regions=upper:3,middle:4,lower:3 bit_mismatches=0 residue_mismatches=4 max_residue_err=0.4480 bounded_failures=0 |
| `003-pipeline-adc-stage` | `FAIL_SIM_CORRECTNESS` | regions=upper:3,middle:4,lower:3 bit_mismatches=4 residue_mismatches=0 max_residue_err=0.0000 bounded_failures=0 |
| `003-pipeline-adc-stage` | `FAIL_SIM_CORRECTNESS` | regions=upper:3,middle:4,lower:3 bit_mismatches=0 residue_mismatches=8 max_residue_err=0.2250 bounded_failures=0 |
| `004-trim-calibration-controller` | `FAIL_SIM_CORRECTNESS` | first_increment_80ns:0.450!=0.510 second_increment_100ns:0.450!=0.570 decrement_140ns:0.450!=0.390 lower_clamp_path_180ns:0.450!=0.150 late_recovery_210ns:0.450!=0.230 reset_20ns:0.450/0.450 hold_before_active_40ns:0.450/0.450 first_increment_80ns:0.450/0.510 second_increment_100ns:0.450/0.570 decrement_140ns:0.450/0.390 lower_clamp_path_180ns:0.450/0.150 late_recovery_210ns:0.450/0.230 |
| `004-trim-calibration-controller` | `FAIL_SIM_CORRECTNESS` | first_increment_80ns:0.390!=0.510 second_increment_100ns:0.330!=0.570 decrement_140ns:0.510!=0.390 lower_clamp_path_180ns:0.750!=0.150 late_recovery_210ns:0.670!=0.230 reset_20ns:0.450/0.450 hold_before_active_40ns:0.450/0.450 first_increment_80ns:0.390/0.510 second_increment_100ns:0.330/0.570 decrement_140ns:0.510/0.390 lower_clamp_path_180ns:0.750/0.150 late_recovery_210ns:0.670/0.230 |
| `004-trim-calibration-controller` | `FAIL_SIM_CORRECTNESS` | second_increment_100ns:0.550!=0.570 lower_clamp_path_180ns:0.200!=0.150 late_recovery_210ns:0.250!=0.230 reset_20ns:0.450/0.450 hold_before_active_40ns:0.450/0.450 first_increment_80ns:0.500/0.510 second_increment_100ns:0.550/0.570 decrement_140ns:0.400/0.390 lower_clamp_path_180ns:0.200/0.150 late_recovery_210ns:0.250/0.230 |
| `004-trim-calibration-controller` | `FAIL_SIM_CORRECTNESS` | reset_20ns:0.500!=0.450 hold_before_active_40ns:0.500!=0.450 first_increment_80ns:0.560!=0.510 second_increment_100ns:0.620!=0.570 decrement_140ns:0.440!=0.390 lower_clamp_path_180ns:0.200!=0.150 late_recovery_210ns:0.260!=0.230 reset_20ns:0.500/0.450 hold_before_active_40ns:0.500/0.450 first_increment_80ns:0.560/0.510 second_increment_100ns:0.620/0.570 decrement_140ns:0.440/0.390 lower_clamp_path_180ns:0.200/0.150 late_recovery_210ns:0.260/0.230 |
| `004-trim-calibration-controller` | `FAIL_SIM_CORRECTNESS` | late_recovery_210ns:0.210!=0.230 range=(0.030,0.570) reset_20ns:0.450/0.450 hold_before_active_40ns:0.450/0.450 first_increment_80ns:0.510/0.510 second_increment_100ns:0.570/0.570 decrement_140ns:0.390/0.390 lower_clamp_path_180ns:0.150/0.150 late_recovery_210ns:0.210/0.230 |
| `005-debounce-latch` | `FAIL_SIM_CORRECTNESS` | short_glitch_low_40ns:0.900 pre_qualify_low_82ns:0.900 reset_arm_rejected_20ns:0.000 short_glitch_low_34ns:0.000 short_glitch_low_40ns:0.900 reset_cancel_low_67ns:0.000 post_cancel_low_72ns:0.000 pre_qualify_low_82ns:0.900 qualified_high_100ns:0.900 qualified_high_130ns:0.900 |
| `005-debounce-latch` | `FAIL_SIM_CORRECTNESS` | short_glitch_low_34ns:0.900 post_cancel_low_72ns:0.900 pre_qualify_low_82ns:0.900 reset_arm_rejected_20ns:0.000 short_glitch_low_34ns:0.900 short_glitch_low_40ns:0.000 reset_cancel_low_67ns:0.000 post_cancel_low_72ns:0.900 pre_qualify_low_82ns:0.900 qualified_high_100ns:0.900 qualified_high_130ns:0.900 |
| `005-debounce-latch` | `FAIL_SIM_CORRECTNESS` | reset_arm_rejected_20ns:0.900 reset_arm_rejected_20ns:0.900 short_glitch_low_34ns:0.000 short_glitch_low_40ns:0.000 reset_cancel_low_67ns:0.000 post_cancel_low_72ns:0.000 pre_qualify_low_82ns:0.000 qualified_high_100ns:0.900 qualified_high_130ns:0.900 |
| `005-debounce-latch` | `FAIL_SIM_CORRECTNESS` | reset_cancel_low_67ns:0.900 reset_arm_rejected_20ns:0.000 short_glitch_low_34ns:0.000 short_glitch_low_40ns:0.000 reset_cancel_low_67ns:0.900 post_cancel_low_72ns:0.000 pre_qualify_low_82ns:0.000 qualified_high_100ns:0.900 qualified_high_130ns:0.900 |
| `005-debounce-latch` | `FAIL_SIM_CORRECTNESS` | qualified_high_100ns:0.000 qualified_high_130ns:0.000 reset_arm_rejected_20ns:0.000 short_glitch_low_34ns:0.000 short_glitch_low_40ns:0.000 reset_cancel_low_67ns:0.000 post_cancel_low_72ns:0.000 pre_qualify_low_82ns:0.000 qualified_high_100ns:0.000 qualified_high_130ns:0.000 |
| `006-element-shuffler` | `FAIL_SIM_CORRECTNESS` | active_sequence=1,1,1,1,1,1,1,1,1,1 expected=2,0,3,1,2,0,2,0,3,1 failures=20ns_active=[1]_expected=2 40ns_active=[1]_expected=0 60ns_active=[1]_expected=3 100ns_active=[1]_expected=2 120ns_active=[1]_expected=0 160ns_active=[1]_expected=2 180ns_active=[1]_expected=0 200ns_active=[1]_expected=3 |
| `006-element-shuffler` | `FAIL_SIM_CORRECTNESS` | active_sequence=0,1,0,1,0,1,0,1,0,1 expected=2,0,3,1,2,0,2,0,3,1 failures=20ns_active=[0]_expected=2 40ns_active=[1]_expected=0 60ns_active=[0]_expected=3 100ns_active=[0]_expected=2 120ns_active=[1]_expected=0 160ns_active=[0]_expected=2 180ns_active=[1]_expected=0 200ns_active=[0]_expected=3 |
| `006-element-shuffler` | `FAIL_SIM_CORRECTNESS` | active_sequence=1,2,3,0,1,2,1,2,3,0 expected=2,0,3,1,2,0,2,0,3,1 failures=20ns_active=[1]_expected=2 40ns_active=[2]_expected=0 80ns_active=[0]_expected=1 100ns_active=[1]_expected=2 120ns_active=[2]_expected=0 160ns_active=[1]_expected=2 180ns_active=[2]_expected=0 220ns_active=[0]_expected=1 |
| `006-element-shuffler` | `FAIL_SIM_CORRECTNESS` | active_sequence=3,3,3,3,3,3,3,3,3,3 expected=2,0,3,1,2,0,2,0,3,1 failures=20ns_active=[3]_expected=2 40ns_active=[3]_expected=0 80ns_active=[3]_expected=1 100ns_active=[3]_expected=2 120ns_active=[3]_expected=0 160ns_active=[3]_expected=2 180ns_active=[3]_expected=0 220ns_active=[3]_expected=1 |
| `006-element-shuffler` | `FAIL_SIM_CORRECTNESS` | active_sequence=0,0,0,0,0,0,0,0,0,0 expected=2,0,3,1,2,0,2,0,3,1 failures=20ns_active=[0]_expected=2 60ns_active=[0]_expected=3 80ns_active=[0]_expected=1 100ns_active=[0]_expected=2 160ns_active=[0]_expected=2 200ns_active=[0]_expected=3 220ns_active=[0]_expected=1 |
| `007-first-order-lowpass` | `FAIL_SIM_CORRECTNESS` | lowpass_samples=0.030,0.089,0.194,0.324 input_step=True monotonic=True response_fast_enough=False not_instant=True bounded=True |
| `007-first-order-lowpass` | `FAIL_SIM_CORRECTNESS` | lowpass_samples=0.800,0.800,0.800,0.800 input_step=True monotonic=False response_fast_enough=True not_instant=False bounded=True |
| `007-first-order-lowpass` | `FAIL_SIM_CORRECTNESS` | lowpass_samples=0.405,0.211,0.115,0.101 input_step=True monotonic=False response_fast_enough=False not_instant=True bounded=True |
| `007-first-order-lowpass` | `FAIL_SIM_CORRECTNESS` | lowpass_samples=0.305,0.350,0.350,0.350 input_step=True monotonic=False response_fast_enough=False not_instant=True bounded=True |
| `007-first-order-lowpass` | `FAIL_SIM_CORRECTNESS` | lowpass_samples=0.000,0.000,0.000,0.000 input_step=True monotonic=False response_fast_enough=False not_instant=True bounded=True |
| `008-gain-trim-controller` | `FAIL_SIM_CORRECTNESS` | gain_trim_samples=0.300,0.300,0.300,0.300,0.300,0.300,0.300,0.300,0.300 reset_nominal=True low_meas_increases=False reaches_upper_clamp=False deadband_holds=True high_meas_decreases=False reaches_lower_clamp=False in_range=True |
| `008-gain-trim-controller` | `FAIL_SIM_CORRECTNESS` | gain_trim_samples=0.300,0.200,0.050,0.050,0.050,0.100,0.450,0.750,0.850 reset_nominal=True low_meas_increases=False reaches_upper_clamp=False deadband_holds=True high_meas_decreases=False reaches_lower_clamp=False in_range=True |
| `008-gain-trim-controller` | `FAIL_SIM_CORRECTNESS` | gain_trim_samples=0.300,0.380,0.540,0.740,0.780,0.740,0.460,0.220,0.100 reset_nominal=True low_meas_increases=True reaches_upper_clamp=False deadband_holds=False high_meas_decreases=True reaches_lower_clamp=False in_range=True |
| `008-gain-trim-controller` | `FAIL_SIM_CORRECTNESS` | gain_trim_samples=0.350,0.450,0.650,0.850,0.850,0.800,0.450,0.150,0.050 reset_nominal=False low_meas_increases=True reaches_upper_clamp=True deadband_holds=True high_meas_decreases=True reaches_lower_clamp=True in_range=True |
| `008-gain-trim-controller` | `FAIL_SIM_CORRECTNESS` | gain_trim_samples=0.300,0.400,0.600,0.850,0.800,0.700,0.350,0.050,0.050 reset_nominal=True low_meas_increases=True reaches_upper_clamp=True deadband_holds=False high_meas_decreases=True reaches_lower_clamp=True in_range=True |
| `009-lock-detector` | `FAIL_SIM_CORRECTNESS` | events=9 aligned=8 mismatch=1 good_lock_after_three=1 early_locks=0 mismatch_clears=1 mismatch_failures=0 reset_low=True final_lock_low=True |
| `009-lock-detector` | `FAIL_SIM_CORRECTNESS` | events=9 aligned=8 mismatch=1 good_lock_after_three=3 early_locks=1 mismatch_clears=0 mismatch_failures=1 reset_low=True final_lock_low=False |
| `009-lock-detector` | `FAIL_SIM_CORRECTNESS` | events=9 aligned=8 mismatch=1 good_lock_after_three=3 early_locks=1 mismatch_clears=0 mismatch_failures=1 reset_low=True final_lock_low=False |
| `009-lock-detector` | `FAIL_SIM_CORRECTNESS` | events=9 aligned=8 mismatch=1 good_lock_after_three=5 early_locks=0 mismatch_clears=1 mismatch_failures=0 reset_low=False final_lock_low=True |
| `009-lock-detector` | `FAIL_SIM_CORRECTNESS` | events=9 aligned=8 mismatch=1 good_lock_after_three=3 early_locks=1 mismatch_clears=0 mismatch_failures=1 reset_low=True final_lock_low=False |
| `010-offset-comparator` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/neg_001_zero_offset/neg_001.va |
| `010-offset-comparator` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/neg_002_large_offset/neg_002.va |
| `010-offset-comparator` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/neg_003_falling_edge/neg_003.va |
| `010-offset-comparator` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/neg_004_async_response/neg_004.va |
| `010-offset-comparator` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/neg_005_weak_high/neg_005.va |
| `011-pfd-up-dn-logic` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/pfd_up_dn_logic__dut/neg_001.va |
| `011-pfd-up-dn-logic` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/pfd_up_dn_logic__dut/neg_002.va |
| `011-pfd-up-dn-logic` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/pfd_up_dn_logic__dut/neg_003.va |
| `011-pfd-up-dn-logic` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/pfd_up_dn_logic__dut/neg_004.va |
| `011-pfd-up-dn-logic` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/pfd_up_dn_logic__dut/neg_005.va |
| `012-clock-divider` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/clock_divider__dut/neg_001.va |
| `012-clock-divider` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/clock_divider__dut/neg_002.va |
| `012-clock-divider` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/clock_divider__dut/neg_003.va |
| `012-clock-divider` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/clock_divider__dut/neg_004.va |
| `012-clock-divider` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/clock_divider__dut/neg_005.va |
| `013-resettable-integrator` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/resettable_integrator__dut/neg_001.va |
| `013-resettable-integrator` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/resettable_integrator__dut/neg_002.va |
| `013-resettable-integrator` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/resettable_integrator__dut/neg_003.va |
| `013-resettable-integrator` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/resettable_integrator__dut/neg_004.va |
| `013-resettable-integrator` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/resettable_integrator__dut/neg_005.va |
| `014-sar-logic` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/sar_logic__dut/neg_001.va |
| `014-sar-logic` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/sar_logic__dut/neg_002.va |
| `014-sar-logic` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/sar_logic__dut/neg_003.va |
| `014-sar-logic` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/sar_logic__dut/neg_004.va |
| `014-sar-logic` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/sar_logic__dut/neg_005.va |
| `015-segmented-dac` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/segmented_dac__dut/neg_001.va |
| `015-segmented-dac` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/segmented_dac__dut/neg_002.va |
| `015-segmented-dac` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/segmented_dac__dut/neg_003.va |
| `015-segmented-dac` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/segmented_dac__dut/neg_004.va |
| `015-segmented-dac` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/segmented_dac__dut/neg_005.va |
| `016-binary-weighted-voltage-dac` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/binary_weighted_voltage_dac__dut/neg_001.va |
| `016-binary-weighted-voltage-dac` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/binary_weighted_voltage_dac__dut/neg_002.va |
| `016-binary-weighted-voltage-dac` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/binary_weighted_voltage_dac__dut/neg_003.va |
| `016-binary-weighted-voltage-dac` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/binary_weighted_voltage_dac__dut/neg_004.va |
| `016-binary-weighted-voltage-dac` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/binary_weighted_voltage_dac__dut/neg_005.va |
| `017-slew-rate-limiter` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/slew_rate_limiter__dut/neg_001.va |
| `017-slew-rate-limiter` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/slew_rate_limiter__dut/neg_002.va |
| `017-slew-rate-limiter` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/slew_rate_limiter__dut/neg_003.va |
| `017-slew-rate-limiter` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/slew_rate_limiter__dut/neg_004.va |
| `017-slew-rate-limiter` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/slew_rate_limiter__dut/neg_005.va |
| `018-strongarm-style-latch-comparator` | `FAIL_SIM_CORRECTNESS` | insufficient_toggle out_p_span=0.000 out_n_span=0.900 |
| `018-strongarm-style-latch-comparator` | `FAIL_SIM_CORRECTNESS` | insufficient_toggle out_p_span=0.000 out_n_span=0.900 |
| `018-strongarm-style-latch-comparator` | `FAIL_SIM_CORRECTNESS` | insufficient_toggle out_p_span=0.000 out_n_span=0.900 |
| `018-strongarm-style-latch-comparator` | `FAIL_SIM_CORRECTNESS` | insufficient_toggle out_p_span=0.000 out_n_span=0.900 |
| `018-strongarm-style-latch-comparator` | `FAIL_SIM_CORRECTNESS` | insufficient_toggle out_p_span=0.000 out_n_span=0.900 |
| `019-unit-element-thermometer-dac` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/unit_element_thermometer_dac__dut/neg_001.va |
| `019-unit-element-thermometer-dac` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/unit_element_thermometer_dac__dut/neg_002.va |
| `019-unit-element-thermometer-dac` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/unit_element_thermometer_dac__dut/neg_003.va |
| `019-unit-element-thermometer-dac` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/unit_element_thermometer_dac__dut/neg_004.va |
| `019-unit-element-thermometer-dac` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/unit_element_thermometer_dac__dut/neg_005.va |
| `020-thermometer-code-decoder` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/thermometer_code_decoder__dut/neg_001.va |
| `020-thermometer-code-decoder` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/thermometer_code_decoder__dut/neg_002.va |
| `020-thermometer-code-decoder` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/thermometer_code_decoder__dut/neg_003.va |
| `020-thermometer-code-decoder` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/thermometer_code_decoder__dut/neg_004.va |
| `020-thermometer-code-decoder` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/thermometer_code_decoder__dut/neg_005.va |
| `021-vco-phase-integrator` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/vco_phase_integrator__dut/neg_001.va |
| `021-vco-phase-integrator` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/vco_phase_integrator__dut/neg_002.va |
| `021-vco-phase-integrator` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/vco_phase_integrator__dut/neg_003.va |
| `021-vco-phase-integrator` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/vco_phase_integrator__dut/neg_004.va |
| `021-vco-phase-integrator` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/vco_phase_integrator__dut/neg_005.va |
| `022-bandgap-reference-macro-model` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/bandgap_reference_macro_model__dut/neg_001.va |
| `022-bandgap-reference-macro-model` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/bandgap_reference_macro_model__dut/neg_002.va |
| `022-bandgap-reference-macro-model` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/bandgap_reference_macro_model__dut/neg_003.va |
| `022-bandgap-reference-macro-model` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/bandgap_reference_macro_model__dut/neg_004.va |
| `022-bandgap-reference-macro-model` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/bandgap_reference_macro_model__dut/neg_005.va |
| `023-calibration-deadband-controller` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/calibration_deadband_controller__dut/neg_001.va |
| `023-calibration-deadband-controller` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/calibration_deadband_controller__dut/neg_002.va |
| `023-calibration-deadband-controller` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/calibration_deadband_controller__dut/neg_003.va |
| `023-calibration-deadband-controller` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/calibration_deadband_controller__dut/neg_004.va |
| `023-calibration-deadband-controller` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/calibration_deadband_controller__dut/neg_005.va |
| `024-charge-pump-abstraction` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/charge_pump_abstraction__dut/neg_001.va |
| `024-charge-pump-abstraction` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/charge_pump_abstraction__dut/neg_002.va |
| `024-charge-pump-abstraction` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/charge_pump_abstraction__dut/neg_003.va |
| `024-charge-pump-abstraction` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/charge_pump_abstraction__dut/neg_004.va |
| `024-charge-pump-abstraction` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/charge_pump_abstraction__dut/neg_005.va |
| `025-clocked-adc-quantizer` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/clocked_adc_quantizer__dut/neg_001.va |
| `025-clocked-adc-quantizer` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/clocked_adc_quantizer__dut/neg_002.va |
| `025-clocked-adc-quantizer` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/clocked_adc_quantizer__dut/neg_003.va |
| `025-clocked-adc-quantizer` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/clocked_adc_quantizer__dut/neg_004.va |
| `025-clocked-adc-quantizer` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/clocked_adc_quantizer__dut/neg_005.va |
| `026-clocked-sample-and-hold` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/clocked_sample_hold__dut/neg_001.va |
| `026-clocked-sample-and-hold` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/clocked_sample_hold__dut/neg_002.va |
| `026-clocked-sample-and-hold` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/clocked_sample_hold__dut/neg_003.va |
| `026-clocked-sample-and-hold` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/clocked_sample_hold__dut/neg_004.va |
| `026-clocked-sample-and-hold` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/clocked_sample_hold__dut/neg_005.va |
| `027-dac-mismatch-unit-weighting-model` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/dac_mismatch_unit_weighting_model__dut/neg_001.va |
| `027-dac-mismatch-unit-weighting-model` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/dac_mismatch_unit_weighting_model__dut/neg_002.va |
| `027-dac-mismatch-unit-weighting-model` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/dac_mismatch_unit_weighting_model__dut/neg_003.va |
| `027-dac-mismatch-unit-weighting-model` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/dac_mismatch_unit_weighting_model__dut/neg_004.va |
| `027-dac-mismatch-unit-weighting-model` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/dac_mismatch_unit_weighting_model__dut/neg_005.va |
| `028-digital-phase-accumulator-with-modulo-wrap` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/digital_phase_accumulator_with_modulo_wrap__dut/neg_001.va |
| `028-digital-phase-accumulator-with-modulo-wrap` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/digital_phase_accumulator_with_modulo_wrap__dut/neg_002.va |
| `028-digital-phase-accumulator-with-modulo-wrap` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/digital_phase_accumulator_with_modulo_wrap__dut/neg_003.va |
| `028-digital-phase-accumulator-with-modulo-wrap` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/digital_phase_accumulator_with_modulo_wrap__dut/neg_004.va |
| `028-digital-phase-accumulator-with-modulo-wrap` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/digital_phase_accumulator_with_modulo_wrap__dut/neg_005.va |
| `029-dwa-dem-encoder` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/dwa_dem_encoder__dut/neg_001.va |
| `029-dwa-dem-encoder` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/dwa_dem_encoder__dut/neg_002.va |
| `029-dwa-dem-encoder` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/dwa_dem_encoder__dut/neg_003.va |
| `029-dwa-dem-encoder` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/dwa_dem_encoder__dut/neg_004.va |
| `029-dwa-dem-encoder` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/dwa_dem_encoder__dut/neg_005.va |
| `030-higher-order-filter` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/higher_order_filter__dut/neg_001.va |
| `030-higher-order-filter` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/higher_order_filter__dut/neg_002.va |
| `030-higher-order-filter` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/higher_order_filter__dut/neg_003.va |
| `030-higher-order-filter` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/higher_order_filter__dut/neg_004.va |
| `030-higher-order-filter` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/higher_order_filter__dut/neg_005.va |
| `031-hysteresis-comparator` | `FAIL_SIM_CORRECTNESS` | window_fracs pre=0.000 mid=0.000 post=0.000 |
| `031-hysteresis-comparator` | `FAIL_SIM_CORRECTNESS` | window_fracs pre=0.000 mid=0.000 post=0.000 |
| `031-hysteresis-comparator` | `FAIL_SIM_CORRECTNESS` | window_fracs pre=0.000 mid=0.000 post=0.000 |
| `031-hysteresis-comparator` | `FAIL_SIM_CORRECTNESS` | window_fracs pre=0.000 mid=0.000 post=0.000 |
| `031-hysteresis-comparator` | `FAIL_SIM_CORRECTNESS` | window_fracs pre=0.000 mid=0.000 post=0.000 |
| `032-ldo-regulator-macro-model` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/ldo_regulator_macro_model__dut/neg_001.va |
| `032-ldo-regulator-macro-model` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/ldo_regulator_macro_model__dut/neg_002.va |
| `032-ldo-regulator-macro-model` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/ldo_regulator_macro_model__dut/neg_003.va |
| `032-ldo-regulator-macro-model` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/ldo_regulator_macro_model__dut/neg_004.va |
| `032-ldo-regulator-macro-model` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/ldo_regulator_macro_model__dut/neg_005.va |
| `033-limiting-amplifier-frontend` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/limiting_amplifier_frontend__dut/neg_001.va |
| `033-limiting-amplifier-frontend` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/limiting_amplifier_frontend__dut/neg_002.va |
| `033-limiting-amplifier-frontend` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/limiting_amplifier_frontend__dut/neg_003.va |
| `033-limiting-amplifier-frontend` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/limiting_amplifier_frontend__dut/neg_004.va |
| `033-limiting-amplifier-frontend` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/limiting_amplifier_frontend__dut/neg_005.va |
| `034-lna-gain-compression-macro` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/lna_gain_compression_macro__dut/neg_001.va |
| `034-lna-gain-compression-macro` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/lna_gain_compression_macro__dut/neg_002.va |
| `034-lna-gain-compression-macro` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/lna_gain_compression_macro__dut/neg_003.va |
| `034-lna-gain-compression-macro` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/lna_gain_compression_macro__dut/neg_004.va |
| `034-lna-gain-compression-macro` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/lna_gain_compression_macro__dut/neg_005.va |
| `035-log-rssi-power-detector` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/log_rssi_power_detector__dut/neg_001.va |
| `035-log-rssi-power-detector` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/log_rssi_power_detector__dut/neg_002.va |
| `035-log-rssi-power-detector` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/log_rssi_power_detector__dut/neg_003.va |
| `035-log-rssi-power-detector` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/log_rssi_power_detector__dut/neg_004.va |
| `035-log-rssi-power-detector` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/log_rssi_power_detector__dut/neg_005.va |
| `036-loop-filter-abstraction` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/loop_filter_abstraction__dut/neg_001.va |
| `036-loop-filter-abstraction` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/loop_filter_abstraction__dut/neg_002.va |
| `036-loop-filter-abstraction` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/loop_filter_abstraction__dut/neg_003.va |
| `036-loop-filter-abstraction` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/loop_filter_abstraction__dut/neg_004.va |
| `036-loop-filter-abstraction` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/loop_filter_abstraction__dut/neg_005.va |
| `037-pa-compression-macro` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/pa_compression_macro__dut/neg_001.va |
| `037-pa-compression-macro` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/pa_compression_macro__dut/neg_002.va |
| `037-pa-compression-macro` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/pa_compression_macro__dut/neg_003.va |
| `037-pa-compression-macro` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/pa_compression_macro__dut/neg_004.va |
| `037-pa-compression-macro` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/pa_compression_macro__dut/neg_005.va |
| `038-power-on-reset-detector` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/power_on_reset_detector__dut/neg_001.va |
| `038-power-on-reset-detector` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/power_on_reset_detector__dut/neg_002.va |
| `038-power-on-reset-detector` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/power_on_reset_detector__dut/neg_003.va |
| `038-power-on-reset-detector` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/power_on_reset_detector__dut/neg_004.va |
| `038-power-on-reset-detector` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/power_on_reset_detector__dut/neg_005.va |
| `039-precision-rectifier-envelope-detector` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/precision_rectifier_envelope_detector__dut/neg_001.va |
| `039-precision-rectifier-envelope-detector` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/precision_rectifier_envelope_detector__dut/neg_002.va |
| `039-precision-rectifier-envelope-detector` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/precision_rectifier_envelope_detector__dut/neg_003.va |
| `039-precision-rectifier-envelope-detector` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/precision_rectifier_envelope_detector__dut/neg_004.va |
| `039-precision-rectifier-envelope-detector` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/precision_rectifier_envelope_detector__dut/neg_005.va |
| `040-programmable-gain-amplifier` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/programmable_gain_amplifier__dut/neg_001.va |
| `040-programmable-gain-amplifier` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/programmable_gain_amplifier__dut/neg_002.va |
| `040-programmable-gain-amplifier` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/programmable_gain_amplifier__dut/neg_003.va |
| `040-programmable-gain-amplifier` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/programmable_gain_amplifier__dut/neg_004.va |
| `040-programmable-gain-amplifier` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/programmable_gain_amplifier__dut/neg_005.va |
| `041-propagation-delay-comparator` | `FAIL_SIM_CORRECTNESS` | delays_ns=[0.061, 0.061, 0.061, 0.061] monotonic=True total_growth_ns=0.000 |
| `041-propagation-delay-comparator` | `FAIL_SIM_CORRECTNESS` | delays_ns=[0.061, 0.061, 0.061, 0.061] monotonic=True total_growth_ns=0.000 |
| `041-propagation-delay-comparator` | `FAIL_SIM_CORRECTNESS` | delays_ns=[0.061, 0.061, 0.061, 0.061] monotonic=True total_growth_ns=0.000 |
| `041-propagation-delay-comparator` | `FAIL_SIM_CORRECTNESS` | delays_ns=[0.061, 0.061, 0.061, 0.061] monotonic=True total_growth_ns=0.000 |
| `041-propagation-delay-comparator` | `FAIL_SIM_CORRECTNESS` | delays_ns=[0.061, 0.061, 0.061, 0.061] monotonic=True total_growth_ns=0.000 |
| `042-ptat-ctat-reference-generator` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/ptat_ctat_reference_generator__dut/neg_001.va |
| `042-ptat-ctat-reference-generator` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/ptat_ctat_reference_generator__dut/neg_002.va |
| `042-ptat-ctat-reference-generator` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/ptat_ctat_reference_generator__dut/neg_003.va |
| `042-ptat-ctat-reference-generator` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/ptat_ctat_reference_generator__dut/neg_004.va |
| `042-ptat-ctat-reference-generator` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/ptat_ctat_reference_generator__dut/neg_005.va |
| `043-rf-mixer-downconverter-macro` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/rf_mixer_downconverter_macro__dut/neg_001.va |
| `043-rf-mixer-downconverter-macro` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/rf_mixer_downconverter_macro__dut/neg_002.va |
| `043-rf-mixer-downconverter-macro` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/rf_mixer_downconverter_macro__dut/neg_003.va |
| `043-rf-mixer-downconverter-macro` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/rf_mixer_downconverter_macro__dut/neg_004.va |
| `043-rf-mixer-downconverter-macro` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/rf_mixer_downconverter_macro__dut/neg_005.va |
| `044-sample-and-hold-with-droop-leakage` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/sample_hold_with_droop_leakage__dut/neg_001.va |
| `044-sample-and-hold-with-droop-leakage` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/sample_hold_with_droop_leakage__dut/neg_002.va |
| `044-sample-and-hold-with-droop-leakage` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/sample_hold_with_droop_leakage__dut/neg_003.va |
| `044-sample-and-hold-with-droop-leakage` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/sample_hold_with_droop_leakage__dut/neg_004.va |
| `044-sample-and-hold-with-droop-leakage` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/sample_hold_with_droop_leakage__dut/neg_005.va |
| `045-soft-hysteretic-limiter` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/soft_hysteretic_limiter__dut/neg_001.va |
| `045-soft-hysteretic-limiter` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/soft_hysteretic_limiter__dut/neg_002.va |
| `045-soft-hysteretic-limiter` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/soft_hysteretic_limiter__dut/neg_003.va |
| `045-soft-hysteretic-limiter` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/soft_hysteretic_limiter__dut/neg_004.va |
| `045-soft-hysteretic-limiter` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/soft_hysteretic_limiter__dut/neg_005.va |
| `046-successive-approximation-calibration-search-fsm` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/successive_approximation_calibration_search_fsm__dut/neg_001.va |
| `046-successive-approximation-calibration-search-fsm` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/successive_approximation_calibration_search_fsm__dut/neg_002.va |
| `046-successive-approximation-calibration-search-fsm` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/successive_approximation_calibration_search_fsm__dut/neg_003.va |
| `046-successive-approximation-calibration-search-fsm` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/successive_approximation_calibration_search_fsm__dut/neg_004.va |
| `046-successive-approximation-calibration-search-fsm` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/successive_approximation_calibration_search_fsm__dut/neg_005.va |
| `047-threshold-comparator` | `FAIL_SIM_CORRECTNESS` | high_frac=0.000 low_frac=0.000 span=0.900 diff_rises=1 diff_falls=1 out_rises=1 out_falls=1 rising_aligned=False falling_aligned=False |
| `047-threshold-comparator` | `FAIL_SIM_CORRECTNESS` | high_frac=0.000 low_frac=0.000 span=0.900 diff_rises=1 diff_falls=1 out_rises=1 out_falls=1 rising_aligned=False falling_aligned=False |
| `047-threshold-comparator` | `FAIL_SIM_CORRECTNESS` | high_frac=0.000 low_frac=0.000 span=0.900 diff_rises=1 diff_falls=1 out_rises=1 out_falls=1 rising_aligned=False falling_aligned=False |
| `047-threshold-comparator` | `FAIL_SIM_CORRECTNESS` | high_frac=0.000 low_frac=0.000 span=0.900 diff_rises=1 diff_falls=1 out_rises=1 out_falls=1 rising_aligned=False falling_aligned=False |
| `047-threshold-comparator` | `FAIL_SIM_CORRECTNESS` | high_frac=0.000 low_frac=0.000 span=0.900 diff_rises=1 diff_falls=1 out_rises=1 out_falls=1 rising_aligned=False falling_aligned=False |
| `048-uvlo-brownout-detector` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/uvlo_brownout_detector__dut/neg_001.va |
| `048-uvlo-brownout-detector` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/uvlo_brownout_detector__dut/neg_002.va |
| `048-uvlo-brownout-detector` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/uvlo_brownout_detector__dut/neg_003.va |
| `048-uvlo-brownout-detector` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/uvlo_brownout_detector__dut/neg_004.va |
| `048-uvlo-brownout-detector` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/uvlo_brownout_detector__dut/neg_005.va |
| `049-window-comparator-detector` | `FAIL_SIM_CORRECTNESS` | below_hi=1.000 above_hi=1.000 inside_rise_hi=0.000 inside_fall_hi=0.000 span=0.900 |
| `049-window-comparator-detector` | `FAIL_SIM_CORRECTNESS` | below_hi=0.000 above_hi=1.000 inside_rise_hi=1.000 inside_fall_hi=1.000 span=0.900 |
| `049-window-comparator-detector` | `FAIL_SIM_CORRECTNESS` | below_hi=0.000 above_hi=0.000 inside_rise_hi=0.267 inside_fall_hi=0.267 span=0.900 |
| `049-window-comparator-detector` | `FAIL_SIM_CORRECTNESS` | out_span_too_small=0.000 |
| `049-window-comparator-detector` | `FAIL_SIM_CORRECTNESS` | below_hi=1.000 above_hi=1.000 inside_rise_hi=0.000 inside_fall_hi=0.000 span=0.900 |
| `050-bin-to-thermometer-decoder-8b` | `FAIL_SIM_CORRECTNESS` | checked=[-1, 0, 1, 128, 255] boundary_seen=[0, 1, 255] enable_low_ok=True count_errors=4 cumulative_errors=0 |
| `050-bin-to-thermometer-decoder-8b` | `FAIL_SIM_CORRECTNESS` | checked=[-1, 0, 1, 128, 255] boundary_seen=[0, 1, 255] enable_low_ok=True count_errors=0 cumulative_errors=3 |
| `050-bin-to-thermometer-decoder-8b` | `FAIL_SIM_CORRECTNESS` | checked=[-1, 0, 1, 128, 255] boundary_seen=[0, 1, 255] enable_low_ok=False count_errors=1 cumulative_errors=0 |
| `050-bin-to-thermometer-decoder-8b` | `FAIL_SIM_CORRECTNESS` | checked=[-1, 0, 1, 128, 255] boundary_seen=[0, 1, 255] enable_low_ok=True count_errors=3 cumulative_errors=0 |
| `050-bin-to-thermometer-decoder-8b` | `FAIL_SIM_CORRECTNESS` | checked=[-1, 0, 1, 128, 255] boundary_seen=[0, 1, 255] enable_low_ok=True count_errors=2 cumulative_errors=0 |
| `051-thermometer-to-binary-encoder-8b` | `FAIL_SIM_CORRECTNESS` | checked=['0', '1', '128', '255', 'invalid'] valid_errors=0 count_errors=4 |
| `051-thermometer-to-binary-encoder-8b` | `FAIL_SIM_CORRECTNESS` | checked=['0', '1', '128', '255', 'invalid'] valid_errors=1 count_errors=0 |
| `051-thermometer-to-binary-encoder-8b` | `FAIL_SIM_CORRECTNESS` | checked=['0', '1', '128', '255', 'invalid'] valid_errors=3 count_errors=3 |
| `051-thermometer-to-binary-encoder-8b` | `FAIL_SIM_CORRECTNESS` | checked=['0', '1', '128', '255', 'invalid'] valid_errors=4 count_errors=0 |
| `051-thermometer-to-binary-encoder-8b` | `FAIL_SIM_CORRECTNESS` | checked=['0', '1', '128', '255', 'invalid'] valid_errors=0 count_errors=2 |
| `052-gray-to-binary-converter-8b` | `FAIL_SIM_CORRECTNESS` | checked=[0, 1, 2, 3, 7, 15, 16, 31, 63, 127, 128, 200, 255, 255] errors=12 |
| `052-gray-to-binary-converter-8b` | `FAIL_SIM_CORRECTNESS` | checked=[0, 1, 2, 3, 7, 15, 16, 31, 63, 127, 128, 200, 255, 255] errors=12 |
| `052-gray-to-binary-converter-8b` | `FAIL_SIM_CORRECTNESS` | checked=[0, 1, 2, 3, 7, 15, 16, 31, 63, 127, 128, 200, 255, 255] errors=14 |
| `052-gray-to-binary-converter-8b` | `FAIL_SIM_CORRECTNESS` | checked=[0, 1, 2, 3, 7, 15, 16, 31, 63, 127, 128, 200, 255, 255] errors=4 |
| `052-gray-to-binary-converter-8b` | `FAIL_SIM_CORRECTNESS` | checked=[0, 1, 2, 3, 7, 15, 16, 31, 63, 127, 128, 200, 255, 255] errors=11 |
| `053-binary-to-gray-converter-8b` | `FAIL_SIM_CORRECTNESS` | checked=[0, 1, 2, 3, 7, 15, 16, 31, 63, 127, 128, 200, 255, 255] errors=12 |
| `053-binary-to-gray-converter-8b` | `FAIL_SIM_CORRECTNESS` | checked=[0, 1, 2, 3, 7, 15, 16, 31, 63, 127, 128, 200, 255, 255] errors=11 |
| `053-binary-to-gray-converter-8b` | `FAIL_SIM_CORRECTNESS` | checked=[0, 1, 2, 3, 7, 15, 16, 31, 63, 127, 128, 200, 255, 255] errors=14 |
| `053-binary-to-gray-converter-8b` | `FAIL_SIM_CORRECTNESS` | checked=[0, 1, 2, 3, 7, 15, 16, 31, 63, 127, 128, 200, 255, 255] errors=4 |
| `053-binary-to-gray-converter-8b` | `FAIL_SIM_CORRECTNESS` | checked=[0, 1, 2, 3, 7, 15, 16, 31, 63, 127, 128, 200, 255, 255] errors=13 |
| `054-onehot-to-binary-encoder-16b` | `FAIL_SIM_CORRECTNESS` | checked=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', 'invalid', 'invalid', 'invalid'] valid_errors=16 code_errors=15 |
| `054-onehot-to-binary-encoder-16b` | `FAIL_SIM_CORRECTNESS` | checked=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', 'invalid', 'invalid', 'invalid'] valid_errors=0 code_errors=19 |
| `054-onehot-to-binary-encoder-16b` | `FAIL_SIM_CORRECTNESS` | checked=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', 'invalid', 'invalid', 'invalid'] valid_errors=0 code_errors=12 |
| `054-onehot-to-binary-encoder-16b` | `FAIL_SIM_CORRECTNESS` | checked=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', 'invalid', 'invalid', 'invalid'] valid_errors=3 code_errors=0 |
| `054-onehot-to-binary-encoder-16b` | `FAIL_SIM_CORRECTNESS` | checked=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', 'invalid', 'invalid', 'invalid'] valid_errors=0 code_errors=16 |
| `055-binary-to-onehot-decoder-16b` | `FAIL_SIM_CORRECTNESS` | checked=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, -1, -1] errors=16 enable_low_seen=True |
| `055-binary-to-onehot-decoder-16b` | `FAIL_SIM_CORRECTNESS` | checked=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, -1, -1] errors=18 enable_low_seen=True |
| `055-binary-to-onehot-decoder-16b` | `FAIL_SIM_CORRECTNESS` | checked=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, -1, -1] errors=16 enable_low_seen=True |
| `055-binary-to-onehot-decoder-16b` | `FAIL_SIM_CORRECTNESS` | checked=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, -1, -1] errors=2 enable_low_seen=True |
| `055-binary-to-onehot-decoder-16b` | `FAIL_SIM_CORRECTNESS` | checked=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, -1, -1] errors=12 enable_low_seen=True |
| `056-decimal-digit-to-bcd-encoder` | `FAIL_SIM_CORRECTNESS` | checked=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'invalid', 'invalid', 'invalid'] valid_errors=10 code_errors=9 |
| `056-decimal-digit-to-bcd-encoder` | `FAIL_SIM_CORRECTNESS` | checked=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'invalid', 'invalid', 'invalid'] valid_errors=0 code_errors=13 |
| `056-decimal-digit-to-bcd-encoder` | `FAIL_SIM_CORRECTNESS` | checked=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'invalid', 'invalid', 'invalid'] valid_errors=0 code_errors=7 |
| `056-decimal-digit-to-bcd-encoder` | `FAIL_SIM_CORRECTNESS` | checked=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'invalid', 'invalid', 'invalid'] valid_errors=3 code_errors=0 |
| `056-decimal-digit-to-bcd-encoder` | `FAIL_SIM_CORRECTNESS` | checked=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'invalid', 'invalid', 'invalid'] valid_errors=0 code_errors=10 |
| `057-signed-magnitude-to-twos-complement-8b` | `FAIL_SIM_CORRECTNESS` | checked=[0, 1, -1, 2, -2, 63, -63, 127, -127, 0, 0] errors=8 neg_zero_seen=True |
| `057-signed-magnitude-to-twos-complement-8b` | `FAIL_SIM_CORRECTNESS` | checked=[0, 1, -1, 2, -2, 63, -63, 127, -127, 0, 0] errors=11 neg_zero_seen=True |
| `057-signed-magnitude-to-twos-complement-8b` | `FAIL_SIM_CORRECTNESS` | checked=[0, 1, -1, 2, -2, 63, -63, 127, -127, 0, 0] errors=6 neg_zero_seen=True |
| `057-signed-magnitude-to-twos-complement-8b` | `FAIL_SIM_CORRECTNESS` | checked=[0, 1, -1, 2, -2, 63, -63, 127, -127, 0, 0] errors=4 neg_zero_seen=True |
| `057-signed-magnitude-to-twos-complement-8b` | `FAIL_SIM_CORRECTNESS` | checked=[0, 1, -1, 2, -2, 63, -63, 127, -127, 0, 0] errors=6 neg_zero_seen=True |
| `058-config-latch-32b-clocked` | `FAIL_SIM_CORRECTNESS` | checked=6 bit_errors=26 |
| `058-config-latch-32b-clocked` | `FAIL_SIM_CORRECTNESS` | checked=6 bit_errors=64 |
| `058-config-latch-32b-clocked` | `FAIL_SIM_CORRECTNESS` | checked=6 bit_errors=128 |
| `058-config-latch-32b-clocked` | `FAIL_SIM_CORRECTNESS` | checked=6 bit_errors=64 |
| `058-config-latch-32b-clocked` | `FAIL_SIM_CORRECTNESS` | checked=6 bit_errors=64 |
| `059-config-latch-128b-static-enable` | `FAIL_SIM_CORRECTNESS` | checked=3 bit_errors=46 |
| `059-config-latch-128b-static-enable` | `FAIL_SIM_CORRECTNESS` | checked=3 bit_errors=72 |
| `059-config-latch-128b-static-enable` | `FAIL_SIM_CORRECTNESS` | checked=3 bit_errors=256 |
| `059-config-latch-128b-static-enable` | `FAIL_SIM_CORRECTNESS` | checked=3 bit_errors=118 |
| `059-config-latch-128b-static-enable` | `FAIL_SIM_CORRECTNESS` | checked=3 bit_errors=148 |
| `060-config-shift-register-64b` | `FAIL_SIM_CORRECTNESS` | checked=12 reset_samples=1 bit_errors=79 |
| `060-config-shift-register-64b` | `FAIL_SIM_CORRECTNESS` | checked=12 reset_samples=1 bit_errors=22 |
| `060-config-shift-register-64b` | `FAIL_SIM_CORRECTNESS` | checked=12 reset_samples=1 bit_errors=4 |
| `060-config-shift-register-64b` | `FAIL_SIM_CORRECTNESS` | checked=12 reset_samples=1 bit_errors=22 |
| `060-config-shift-register-64b` | `FAIL_SIM_CORRECTNESS` | checked=12 reset_samples=1 bit_errors=36 |
| `061-bus-splitter-256-to-16x16` | `FAIL_SIM_CORRECTNESS` | bit_errors=230 |
| `061-bus-splitter-256-to-16x16` | `FAIL_SIM_CORRECTNESS` | bit_errors=230 |
| `061-bus-splitter-256-to-16x16` | `FAIL_SIM_CORRECTNESS` | bit_errors=240 |
| `061-bus-splitter-256-to-16x16` | `FAIL_SIM_CORRECTNESS` | bit_errors=768 |
| `061-bus-splitter-256-to-16x16` | `FAIL_SIM_CORRECTNESS` | bit_errors=10 |
| `062-bus-combiner-16x16-to-256` | `FAIL_SIM_CORRECTNESS` | bit_errors=230 |
| `062-bus-combiner-16x16-to-256` | `FAIL_SIM_CORRECTNESS` | bit_errors=230 |
| `062-bus-combiner-16x16-to-256` | `FAIL_SIM_CORRECTNESS` | bit_errors=240 |
| `062-bus-combiner-16x16-to-256` | `FAIL_SIM_CORRECTNESS` | bit_errors=768 |
| `062-bus-combiner-16x16-to-256` | `FAIL_SIM_CORRECTNESS` | bit_errors=10 |
| `063-masked-config-update-32b` | `FAIL_SIM_CORRECTNESS` | bit_errors=46 |
| `063-masked-config-update-32b` | `FAIL_SIM_CORRECTNESS` | bit_errors=92 |
| `063-masked-config-update-32b` | `FAIL_SIM_CORRECTNESS` | bit_errors=28 |
| `063-masked-config-update-32b` | `FAIL_SIM_CORRECTNESS` | bit_errors=52 |
| `063-masked-config-update-32b` | `FAIL_SIM_CORRECTNESS` | bit_errors=64 |
| `064-edge-interval-tdc-8b` | `FAIL_SIM_CORRECTNESS` | checked=[8, 23, 39] errors=3 |
| `064-edge-interval-tdc-8b` | `FAIL_SIM_CORRECTNESS` | checked=[8, 23, 39] errors=3 |
| `064-edge-interval-tdc-8b` | `FAIL_SIM_CORRECTNESS` | checked=[8, 23, 39] errors=3 |
| `064-edge-interval-tdc-8b` | `FAIL_SIM_CORRECTNESS` | checked=[8, 23, 39] errors=3 |
| `064-edge-interval-tdc-8b` | `FAIL_SIM_CORRECTNESS` | checked=[8, 23, 39] errors=3 |
| `065-period-meter-16b` | `FAIL_SIM_CORRECTNESS` | checked=[20, 25, 35, 40] errors=4 |
| `065-period-meter-16b` | `FAIL_SIM_CORRECTNESS` | checked=[20, 25, 35, 40] errors=4 |
| `065-period-meter-16b` | `FAIL_SIM_CORRECTNESS` | checked=[20, 25, 35, 40] errors=4 |
| `065-period-meter-16b` | `FAIL_SIM_CORRECTNESS` | checked=[20, 25, 35, 40] errors=4 |
| `065-period-meter-16b` | `FAIL_SIM_CORRECTNESS` | checked=[20, 25, 35, 40] errors=3 |
| `066-duty-cycle-meter-8b` | `FAIL_SIM_CORRECTNESS` | checked=[38, 46, 62, 42] errors=4 |
| `066-duty-cycle-meter-8b` | `FAIL_SIM_CORRECTNESS` | checked=[38, 45, 62, 42] errors=4 |
| `066-duty-cycle-meter-8b` | `FAIL_SIM_CORRECTNESS` | checked=[38, 45, 62, 42] errors=4 |
| `066-duty-cycle-meter-8b` | `FAIL_SIM_CORRECTNESS` | checked=[38, 45, 62, 42] errors=4 |
| `066-duty-cycle-meter-8b` | `FAIL_SIM_CORRECTNESS` | checked=[38, 45, 62, 42] errors=4 |
| `067-event-counter-windowed-16b` | `FAIL_SIM_CORRECTNESS` | checked=[3, 3] errors=2 |
| `067-event-counter-windowed-16b` | `FAIL_SIM_CORRECTNESS` | checked=[3, 3] errors=1 |
| `067-event-counter-windowed-16b` | `FAIL_SIM_CORRECTNESS` | checked=[3, 3] errors=1 |
| `067-event-counter-windowed-16b` | `FAIL_SIM_CORRECTNESS` | checked=[3, 3] errors=2 |
| `067-event-counter-windowed-16b` | `FAIL_SIM_CORRECTNESS` | checked=[3, 3] errors=2 |
| `068-latency-counter-ready-valid-12b` | `FAIL_SIM_CORRECTNESS` | checked=[2, 3] errors=2 |
| `068-latency-counter-ready-valid-12b` | `FAIL_SIM_CORRECTNESS` | checked=[2, 3] errors=2 |
| `068-latency-counter-ready-valid-12b` | `FAIL_SIM_CORRECTNESS` | checked=[2, 3] errors=2 |
| `068-latency-counter-ready-valid-12b` | `FAIL_SIM_CORRECTNESS` | checked=[2, 3] errors=2 |
| `068-latency-counter-ready-valid-12b` | `FAIL_SIM_CORRECTNESS` | checked=[2, 3] errors=2 |
| `069-settling-window-detector` | `FAIL_SIM_CORRECTNESS` | errors=16 intervals=[(55.1, 105.1), (115.1, 150.0)] settled_seen=False reset_seen=True early_seen=False |
| `069-settling-window-detector` | `FAIL_SIM_CORRECTNESS` | errors=28 intervals=[(55.1, 105.1), (115.1, 150.0)] settled_seen=True reset_seen=True early_seen=True |
| `069-settling-window-detector` | `FAIL_SIM_CORRECTNESS` | errors=31 intervals=[(55.1, 105.1), (115.1, 150.0)] settled_seen=True reset_seen=True early_seen=True |
| `069-settling-window-detector` | `FAIL_SIM_CORRECTNESS` | errors=23 intervals=[(55.1, 105.1), (115.1, 150.0)] settled_seen=True reset_seen=True early_seen=True |
| `069-settling-window-detector` | `FAIL_SIM_CORRECTNESS` | errors=16 intervals=[(55.1, 105.1), (115.1, 150.0)] settled_seen=True reset_seen=True early_seen=False |
| `070-active-low-reset-synchronizer` | `FAIL_SIM_CORRECTNESS` | checked=15 violations=8 |
| `070-active-low-reset-synchronizer` | `FAIL_SIM_CORRECTNESS` | checked=15 violations=79 |
| `070-active-low-reset-synchronizer` | `FAIL_SIM_CORRECTNESS` | checked=15 violations=2 |
| `070-active-low-reset-synchronizer` | `FAIL_SIM_CORRECTNESS` | checked=15 violations=87 |
| `070-active-low-reset-synchronizer` | `FAIL_SIM_CORRECTNESS` | checked=15 violations=10 |
| `071-active-high-reset-synchronizer` | `FAIL_SIM_CORRECTNESS` | checked=15 violations=79 |
| `071-active-high-reset-synchronizer` | `FAIL_SIM_CORRECTNESS` | checked=15 violations=8 |
| `071-active-high-reset-synchronizer` | `FAIL_SIM_CORRECTNESS` | checked=15 violations=2 |
| `071-active-high-reset-synchronizer` | `FAIL_SIM_CORRECTNESS` | checked=15 violations=87 |
| `071-active-high-reset-synchronizer` | `FAIL_SIM_CORRECTNESS` | checked=15 violations=10 |
| `072-enable-gated-clock-pulse` | `FAIL_SIM_CORRECTNESS` | errors=140 saw_high=False saw_blocked=True |
| `072-enable-gated-clock-pulse` | `FAIL_SIM_CORRECTNESS` | errors=53 saw_high=True saw_blocked=False |
| `072-enable-gated-clock-pulse` | `FAIL_SIM_CORRECTNESS` | errors=144 saw_high=True saw_blocked=True |
| `072-enable-gated-clock-pulse` | `FAIL_SIM_CORRECTNESS` | errors=160 saw_high=True saw_blocked=False |
| `072-enable-gated-clock-pulse` | `FAIL_SIM_CORRECTNESS` | errors=324 saw_high=True saw_blocked=False |
| `073-low-active-enable-decoder-4b` | `FAIL_SIM_CORRECTNESS` | checked=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, -1, -1] errors=16 |
| `073-low-active-enable-decoder-4b` | `FAIL_SIM_CORRECTNESS` | checked=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, -1, -1] errors=18 |
| `073-low-active-enable-decoder-4b` | `FAIL_SIM_CORRECTNESS` | checked=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, -1, -1] errors=2 |
| `073-low-active-enable-decoder-4b` | `FAIL_SIM_CORRECTNESS` | checked=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, -1, -1] errors=12 |
| `073-low-active-enable-decoder-4b` | `FAIL_SIM_CORRECTNESS` | checked=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, -1, -1] errors=12 |
| `074-configurable-polarity-edge-detector` | `FAIL_SIM_CORRECTNESS` | events=4 missed=4 false_pulses=0 |
| `074-configurable-polarity-edge-detector` | `FAIL_SIM_CORRECTNESS` | events=4 missed=0 false_pulses=86 |
| `074-configurable-polarity-edge-detector` | `FAIL_SIM_CORRECTNESS` | events=4 missed=2 false_pulses=43 |
| `074-configurable-polarity-edge-detector` | `FAIL_SIM_CORRECTNESS` | events=4 missed=0 false_pulses=2378 |
| `074-configurable-polarity-edge-detector` | `FAIL_SIM_CORRECTNESS` | events=4 missed=0 false_pulses=324 |
| `075-prbs-generator-32b-seeded` | `FAIL_SIM_CORRECTNESS` | checked=18 errors=18 |
| `075-prbs-generator-32b-seeded` | `FAIL_SIM_CORRECTNESS` | checked=18 errors=16 |
| `075-prbs-generator-32b-seeded` | `FAIL_SIM_CORRECTNESS` | checked=18 errors=15 |
| `075-prbs-generator-32b-seeded` | `FAIL_SIM_CORRECTNESS` | checked=18 errors=16 |
| `075-prbs-generator-32b-seeded` | `FAIL_SIM_CORRECTNESS` | checked=18 errors=18 |
| `076-multiphase-clock-generator-4ph` | `FAIL_SIM_CORRECTNESS` | too_few_edges={'clk0': 0, 'clk90': 0, 'clk180': 0, 'clk270': 0} |
| `076-multiphase-clock-generator-4ph` | `FAIL_SIM_CORRECTNESS` | edge_counts={'clk0': 4, 'clk90': 4, 'clk180': 4, 'clk270': 4} phase_errors=9 period_errors=0 |
| `076-multiphase-clock-generator-4ph` | `FAIL_SIM_CORRECTNESS` | edge_counts={'clk0': 4, 'clk90': 4, 'clk180': 4, 'clk270': 4} phase_errors=3 period_errors=0 |
| `076-multiphase-clock-generator-4ph` | `FAIL_SIM_CORRECTNESS` | edge_counts={'clk0': 3, 'clk90': 4, 'clk180': 4, 'clk270': 4} phase_errors=0 period_errors=2 |
| `076-multiphase-clock-generator-4ph` | `FAIL_SIM_CORRECTNESS` | edge_counts={'clk0': 4, 'clk90': 4, 'clk180': 4, 'clk270': 4} phase_errors=3 period_errors=0 |
| `077-configurable-pulse-train-generator` | `FAIL_SIM_CORRECTNESS` | errors=9 done_seen=True pulse_count=0 expected_total=3 |
| `077-configurable-pulse-train-generator` | `FAIL_SIM_CORRECTNESS` | errors=3 done_seen=True pulse_count=3 expected_total=3 |
| `077-configurable-pulse-train-generator` | `FAIL_SIM_CORRECTNESS` | errors=8 done_seen=True pulse_count=3 expected_total=3 |
| `077-configurable-pulse-train-generator` | `FAIL_SIM_CORRECTNESS` | errors=2 done_seen=True pulse_count=3 expected_total=3 |
| `077-configurable-pulse-train-generator` | `FAIL_SIM_CORRECTNESS` | errors=4 done_seen=True pulse_count=4 expected_total=3 |
| `078-staircase-dac-stimulus-8b` | `FAIL_SIM_CORRECTNESS` | checked=[0, 1, 2, 3, 4, 5, 6, 7, 0, 0, 1, 2, 3, 4, 5] errors=12 |
| `078-staircase-dac-stimulus-8b` | `FAIL_SIM_CORRECTNESS` | checked=[0, 1, 2, 3, 4, 5, 6, 7, 0, 0, 1, 2, 3, 4, 5] errors=12 |
| `078-staircase-dac-stimulus-8b` | `FAIL_SIM_CORRECTNESS` | checked=[0, 1, 2, 3, 4, 5, 6, 7, 0, 0, 1, 2, 3, 4, 5] errors=15 |
| `078-staircase-dac-stimulus-8b` | `FAIL_SIM_CORRECTNESS` | checked=[0, 1, 2, 3, 4, 5, 6, 7, 0, 0, 1, 2, 3, 4, 5] errors=10 |
| `078-staircase-dac-stimulus-8b` | `FAIL_SIM_CORRECTNESS` | checked=[0, 1, 2, 3, 4, 5, 6, 7, 0, 0, 1, 2, 3, 4, 5] errors=12 |
| `079-jittered-clock-source-deterministic` | `FAIL_SIM_CORRECTNESS` | too_few_edges=0 |
| `079-jittered-clock-source-deterministic` | `FAIL_SIM_CORRECTNESS` | periods_ns=[20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0] varying=False bounded=True prefix_ok=False |
| `079-jittered-clock-source-deterministic` | `FAIL_SIM_CORRECTNESS` | periods_ns=[29.6, 27.2, 28.8, 26.4, 28.0, 29.6, 27.2] varying=True bounded=False prefix_ok=False |
| `079-jittered-clock-source-deterministic` | `FAIL_SIM_CORRECTNESS` | periods_ns=[27.0, 16.5, 23.5, 13.0, 20.0, 27.0, 16.5, 23.5, 13.0, 20.0] varying=True bounded=False prefix_ok=False |
| `079-jittered-clock-source-deterministic` | `FAIL_SIM_CORRECTNESS` | periods_ns=[20.0, 21.6, 19.2, 20.8, 18.4, 20.0, 21.6, 19.2, 20.8, 18.4] varying=True bounded=True prefix_ok=False |
| `080-acquisition-limited-sample-and-hold` | `FAIL_SIM_CORRECTNESS` | acq_hold_reset_out=0.000 |
| `080-acquisition-limited-sample-and-hold` | `FAIL_SIM_CORRECTNESS` | acq_hold_reset_out=0.189 |
| `080-acquisition-limited-sample-and-hold` | `FAIL_SIM_CORRECTNESS` | acq_hold_reset_out=0.189 |
| `080-acquisition-limited-sample-and-hold` | `FAIL_SIM_CORRECTNESS` | acq_hold_reset_out=0.189 |
| `080-acquisition-limited-sample-and-hold` | `FAIL_SIM_CORRECTNESS` | acq_hold_reset_out=0.189 |
| `081-aperture-delay-track-and-hold` | `FAIL_SIM_CORRECTNESS` | aperture_samples=0.000,0.000,0.000,0.000,0.000,0.000,0.000 expected=0.350,0.600,0.250,0.700,0.400,0.800,0.800 mismatches=7 span=0.000 |
| `081-aperture-delay-track-and-hold` | `FAIL_SIM_CORRECTNESS` | aperture_samples=0.100,0.350,0.600,0.250,0.700,0.400,0.800 expected=0.350,0.600,0.250,0.700,0.400,0.800,0.800 mismatches=6 span=0.700 |
| `081-aperture-delay-track-and-hold` | `FAIL_SIM_CORRECTNESS` | aperture_samples=0.175,0.300,0.125,0.350,0.200,0.400,0.400 expected=0.350,0.600,0.250,0.700,0.400,0.800,0.800 mismatches=7 span=0.275 |
| `081-aperture-delay-track-and-hold` | `FAIL_SIM_CORRECTNESS` | aperture_samples=0.550,0.300,0.650,0.200,0.500,0.100,0.100 expected=0.350,0.600,0.250,0.700,0.400,0.800,0.800 mismatches=7 span=0.550 |
| `081-aperture-delay-track-and-hold` | `FAIL_SIM_CORRECTNESS` | aperture_samples=0.147,0.252,0.105,0.294,0.168,0.336,0.336 expected=0.350,0.600,0.250,0.700,0.400,0.800,0.800 mismatches=7 span=0.231 |
| `082-bias-voltage-generator-with-enable-trim` | `FAIL_SIM_CORRECTNESS` | bias_low_trim_wrong=0.000 |
| `082-bias-voltage-generator-with-enable-trim` | `FAIL_SIM_CORRECTNESS` | bias_low_trim_wrong=0.151 |
| `082-bias-voltage-generator-with-enable-trim` | `FAIL_SIM_CORRECTNESS` | bias_low_trim_wrong=0.151 |
| `082-bias-voltage-generator-with-enable-trim` | `FAIL_SIM_CORRECTNESS` | bias_low_trim_wrong=0.151 |
| `082-bias-voltage-generator-with-enable-trim` | `FAIL_SIM_CORRECTNESS` | bias_low_trim_wrong=0.151 |
| `083-crossing-metric-writer` | `FAIL_SIM_CORRECTNESS` | cross_t=3.050e-08 cross_window_ok=True done_before=0.000 done_after=0.000 done_final=0.000 |
| `083-crossing-metric-writer` | `FAIL_SIM_CORRECTNESS` | cross_t=3.050e-08 cross_window_ok=True done_before=0.000 done_after=0.378 done_final=0.378 |
| `083-crossing-metric-writer` | `FAIL_SIM_CORRECTNESS` | cross_t=3.050e-08 cross_window_ok=True done_before=0.000 done_after=0.000 done_final=0.000 |
| `083-crossing-metric-writer` | `FAIL_SIM_CORRECTNESS` | cross_t=3.050e-08 cross_window_ok=True done_before=0.000 done_after=0.378 done_final=0.378 |
| `083-crossing-metric-writer` | `FAIL_SIM_CORRECTNESS` | cross_t=3.050e-08 cross_window_ok=True done_before=0.000 done_after=0.378 done_final=0.378 |
| `084-peak-detector` | `FAIL_SIM_CORRECTNESS` | peak_samples=0.000,0.000,0.000 first_peak=False reset_clear=True second_peak=False |
| `084-peak-detector` | `FAIL_SIM_CORRECTNESS` | peak_samples=0.231,0.000,0.294 first_peak=False reset_clear=True second_peak=False |
| `084-peak-detector` | `FAIL_SIM_CORRECTNESS` | peak_samples=0.231,0.000,0.294 first_peak=False reset_clear=True second_peak=False |
| `084-peak-detector` | `FAIL_SIM_CORRECTNESS` | peak_samples=0.000,0.105,0.000 first_peak=False reset_clear=False second_peak=False |
| `084-peak-detector` | `FAIL_SIM_CORRECTNESS` | peak_samples=0.231,0.000,0.294 first_peak=False reset_clear=True second_peak=False |
| `085-burst-clock-source` | `FAIL_SIM_CORRECTNESS` | burst_cycles_checked=25 enabled_cycles=7 disabled_cycles=18 high_phase_failures=7 low_phase_failures=0 |
| `085-burst-clock-source` | `FAIL_SIM_CORRECTNESS` | burst_cycles_checked=25 enabled_cycles=7 disabled_cycles=18 high_phase_failures=18 low_phase_failures=0 |
| `085-burst-clock-source` | `FAIL_SIM_CORRECTNESS` | burst_cycles_checked=25 enabled_cycles=7 disabled_cycles=18 high_phase_failures=3 low_phase_failures=0 |
| `085-burst-clock-source` | `FAIL_SIM_CORRECTNESS` | burst_cycles_checked=25 enabled_cycles=7 disabled_cycles=18 high_phase_failures=6 low_phase_failures=0 |
| `085-burst-clock-source` | `FAIL_SIM_CORRECTNESS` | burst_cycles_checked=25 enabled_cycles=7 disabled_cycles=18 high_phase_failures=7 low_phase_failures=0 |
| `086-dither-noise-like-deterministic-source` | `FAIL_SIM_CORRECTNESS` | noise_mean=-0.7500 noise_std=0.0000 max_abs=0.7500 |
| `086-dither-noise-like-deterministic-source` | `FAIL_SIM_CORRECTNESS` | noise_mean=0.0000 noise_std=0.0000 max_abs=0.0000 |
| `086-dither-noise-like-deterministic-source` | `FAIL_SIM_CORRECTNESS` | noise_mean=0.0117 noise_std=0.3545 max_abs=0.7916 |
| `086-dither-noise-like-deterministic-source` | `FAIL_SIM_CORRECTNESS` | noise_mean=0.1219 noise_std=0.0567 max_abs=0.2467 |
| `086-dither-noise-like-deterministic-source` | `FAIL_SIM_CORRECTNESS` | used_negative_manifest_file=negative_variants/neg_005_metric_scale_low/noise_gen.va |
| `087-lfsr-prbs-generator` | `FAIL_SIM_CORRECTNESS` | unique_state_steps=1 |
| `087-lfsr-prbs-generator` | `FAIL_SIM_CORRECTNESS` | state_steps=139 checked_transitions=138 mismatches=65 serial_transitions=64 |
| `087-lfsr-prbs-generator` | `FAIL_SIM_CORRECTNESS` | state_steps=139 checked_transitions=138 mismatches=1 serial_transitions=65 |
| `087-lfsr-prbs-generator` | `FAIL_SIM_CORRECTNESS` | serial_state_mismatch code=126 |
| `087-lfsr-prbs-generator` | `FAIL_SIM_CORRECTNESS` | simulator_error=Model prbs7_ref not found (available: ['prbs7']) |
| `088-ramp-step-source` | `FAIL_SIM_CORRECTNESS` | guard_hi_frac_out_of_range=0.000 |
| `088-ramp-step-source` | `FAIL_SIM_CORRECTNESS` | guard_hi_frac_out_of_range=0.036 |
| `088-ramp-step-source` | `FAIL_SIM_CORRECTNESS` | guard_hi_frac_out_of_range=0.000 |
| `088-ramp-step-source` | `FAIL_SIM_CORRECTNESS` | guard_hi_frac_out_of_range=0.540 |
| `088-ramp-step-source` | `FAIL_SIM_CORRECTNESS` | guard_rises=5 wraps=0 phase_span=0.861 guard_hi_frac=0.213 |
| `089-sine-periodic-voltage-source` | `FAIL_SIM_CORRECTNESS` | max_err=0.2768 |
| `089-sine-periodic-voltage-source` | `FAIL_SIM_CORRECTNESS` | max_err=0.0496 |
| `089-sine-periodic-voltage-source` | `FAIL_SIM_CORRECTNESS` | max_err=0.0418 |
| `089-sine-periodic-voltage-source` | `FAIL_SIM_CORRECTNESS` | max_err=0.1384 |
| `089-sine-periodic-voltage-source` | `FAIL_SIM_CORRECTNESS` | max_err=0.1605 |
| `090-adpll-ratio-hop-timer` | `FAIL_SIM_CORRECTNESS` | streaming_checker:pre_window_not_enough_edges num=0 den=40 |
| `090-adpll-ratio-hop-timer` | `FAIL_SIM_CORRECTNESS` | streaming_checker:pre_divider_window_not_enough_edges num=160 den=0 |
| `090-adpll-ratio-hop-timer` | `FAIL_SIM_CORRECTNESS` | streaming_checker:pre_divider_window_not_enough_edges num=160 den=0 |
| `090-adpll-ratio-hop-timer` | `FAIL_SIM_CORRECTNESS` | streaming_checker:pre_divider_window_not_enough_edges num=160 den=0 |
| `090-adpll-ratio-hop-timer` | `FAIL_SIM_CORRECTNESS` | streaming_checker:pre_divider_window_not_enough_edges num=160 den=0 |
| `091-agc-receiver-leveling-loop` | `FAIL_SIM_CORRECTNESS` | agc_gain_not_reduced overload=0.450 settled=0.450 |
| `091-agc-receiver-leveling-loop` | `FAIL_SIM_CORRECTNESS` | agc_gain_not_reduced overload=0.080 settled=0.178 |
| `091-agc-receiver-leveling-loop` | `FAIL_SIM_CORRECTNESS` | agc_gain_not_reduced overload=0.080 settled=0.185 |
| `091-agc-receiver-leveling-loop` | `FAIL_SIM_CORRECTNESS` | agc_gain_not_reduced overload=0.261 settled=0.261 |
| `091-agc-receiver-leveling-loop` | `FAIL_SIM_CORRECTNESS` | agc_gain_not_reduced overload=0.080 settled=0.178 |
| `092-amplifier-filter-chain` | `FAIL_SIM_CORRECTNESS` | amp_filter_metric_not_preamp_target early=0.000 late=0.000 low=0.000 |
| `092-amplifier-filter-chain` | `FAIL_SIM_CORRECTNESS` | amp_filter_metric_not_preamp_target early=0.378 late=0.378 low=0.000 |
| `092-amplifier-filter-chain` | `FAIL_SIM_CORRECTNESS` | amp_filter_metric_not_preamp_target early=0.378 late=0.378 low=0.000 |
| `092-amplifier-filter-chain` | `FAIL_SIM_CORRECTNESS` | amp_filter_metric_not_preamp_target early=0.189 late=0.189 low=0.189 |
| `092-amplifier-filter-chain` | `FAIL_SIM_CORRECTNESS` | amp_filter_metric_not_preamp_target early=0.378 late=0.378 low=0.000 |
| `093-bbpd-data-edge-alignment` | `FAIL_SIM_CORRECTNESS` | too_few_updn_pulses=0 |
| `093-bbpd-data-edge-alignment` | `FAIL_SIM_CORRECTNESS` | too_few_updn_pulses=0 |
| `093-bbpd-data-edge-alignment` | `FAIL_SIM_CORRECTNESS` | too_few_updn_pulses=0 |
| `093-bbpd-data-edge-alignment` | `FAIL_SIM_CORRECTNESS` | too_few_updn_pulses=0 |
| `093-bbpd-data-edge-alignment` | `FAIL_SIM_CORRECTNESS` | too_few_updn_pulses=0 |
| `094-comparator-offset-search` | `FAIL_SIM_CORRECTNESS` | outp_range=0.000 |
| `094-comparator-offset-search` | `FAIL_SIM_CORRECTNESS` | output_or_valid_window_fail low_frac=1.000 high_frac=0.000 pre_valid_low_frac=1.000 |
| `094-comparator-offset-search` | `FAIL_SIM_CORRECTNESS` | outp_range=0.000 |
| `094-comparator-offset-search` | `FAIL_SIM_CORRECTNESS` | output_or_valid_window_fail low_frac=1.000 high_frac=0.000 pre_valid_low_frac=1.000 |
| `094-comparator-offset-search` | `FAIL_SIM_CORRECTNESS` | output_or_valid_window_fail low_frac=1.000 high_frac=0.000 pre_valid_low_frac=1.000 |
| `095-complete-calibration-loop` | `FAIL_SIM_CORRECTNESS` | complete_cal_loop_reset_mean=0.000 |
| `095-complete-calibration-loop` | `FAIL_SIM_CORRECTNESS` | complete_cal_loop_reset_mean=0.195 |
| `095-complete-calibration-loop` | `FAIL_SIM_CORRECTNESS` | complete_cal_loop_reset_mean=0.194 |
| `095-complete-calibration-loop` | `FAIL_SIM_CORRECTNESS` | complete_cal_loop_reset_mean=0.192 |
| `095-complete-calibration-loop` | `FAIL_SIM_CORRECTNESS` | complete_cal_loop_reset_mean=0.195 |
| `096-converter-static-linearity-measurement` | `FAIL_SIM_CORRECTNESS` | converter_code_coverage=[0] |
| `096-converter-static-linearity-measurement` | `FAIL_SIM_CORRECTNESS` | converter_code_coverage=[0, 1, 2, 3, 4, 5, 6] |
| `096-converter-static-linearity-measurement` | `FAIL_SIM_CORRECTNESS` | converter_code_coverage=[0, 1, 2, 3, 4, 5, 6] |
| `096-converter-static-linearity-measurement` | `FAIL_SIM_CORRECTNESS` | converter_code_coverage=[0] |
| `096-converter-static-linearity-measurement` | `FAIL_SIM_CORRECTNESS` | converter_code_coverage=[0, 1, 2, 3, 4, 5, 6] |
| `097-cppll-tracking-reacquire-timer` | `FAIL_SIM_CORRECTNESS` | streaming_checker:not_enough_edges ref=305 fb=0 |
| `097-cppll-tracking-reacquire-timer` | `FAIL_SIM_CORRECTNESS` | streaming_checker:freq_ratio=0.9796 relock_time=nan disturb_low_frac=0.000 vctrl_min=0.427 vctrl_max=0.483 vctrl_span=0.056 |
| `097-cppll-tracking-reacquire-timer` | `FAIL_SIM_CORRECTNESS` | streaming_checker:freq_ratio=0.8684 relock_time=nan disturb_low_frac=1.000 vctrl_min=0.427 vctrl_max=0.480 vctrl_span=0.053 |
| `097-cppll-tracking-reacquire-timer` | `FAIL_SIM_CORRECTNESS` | streaming_checker:freq_ratio=0.9750 relock_time=2.810e-06 disturb_low_frac=0.949 vctrl_min=0.450 vctrl_max=0.450 vctrl_span=0.000 |
| `097-cppll-tracking-reacquire-timer` | `FAIL_SIM_CORRECTNESS` | streaming_checker:freq_ratio=0.9796 relock_time=2.966e-06 disturb_low_frac=0.896 vctrl_min=1.100 vctrl_max=1.100 vctrl_span=0.000 |
| `098-edge-crossing-interval-timer` | `FAIL_SIM_CORRECTNESS` | streaming_checker:seen_out_never_high=0.000 |
| `098-edge-crossing-interval-timer` | `FAIL_SIM_CORRECTNESS` | streaming_checker:delay_ps=68.600 seen_hi=1.000 post_seen_samples=322 |
| `098-edge-crossing-interval-timer` | `FAIL_SIM_CORRECTNESS` | streaming_checker:seen_out_never_high=0.000 |
| `098-edge-crossing-interval-timer` | `FAIL_SIM_CORRECTNESS` | streaming_checker:delay_ps=68.600 seen_hi=1.000 post_seen_samples=326 |
| `098-edge-crossing-interval-timer` | `FAIL_SIM_CORRECTNESS` | streaming_checker:delay_ps=68.600 seen_hi=1.000 post_seen_samples=326 |
| `099-dither-adder` | `FAIL_SIM_CORRECTNESS` | dither_high=-0.3707 dither_low=-0.1930 high_err=0.0831 low_err=0.0545 cm_max=0.4500 |
| `099-dither-adder` | `FAIL_SIM_CORRECTNESS` | dither_high=-0.0320 dither_low=0.0320 high_err=0.0000 low_err=0.0000 cm_max=0.0000 |
| `099-dither-adder` | `FAIL_SIM_CORRECTNESS` | dither_high=-0.0000 dither_low=-0.0000 high_err=0.0000 low_err=0.0000 cm_max=0.0320 |
| `099-dither-adder` | `FAIL_SIM_CORRECTNESS` | dither_high=0.0320 dither_low=0.0320 high_err=0.0000 low_err=0.0000 cm_max=0.0000 |
| `099-dither-adder` | `FAIL_SIM_CORRECTNESS` | dither_high=-0.3458 dither_low=-0.3397 high_err=0.0241 low_err=0.0158 cm_max=0.2018 |
| `100-final-step-file-metric` | `FAIL_SIM_CORRECTNESS` | metric_out_too_low=0.000 |
| `100-final-step-file-metric` | `FAIL_SIM_CORRECTNESS` | ref_edges=4 max_edge_err_ns=0.032 metric_levels=[0.095, 0.189, 0.283, 0.378] max_level_err=0.522 final_norm=0.401 metric_dips=0 |
| `100-final-step-file-metric` | `FAIL_SIM_CORRECTNESS` | ref_edges=4 max_edge_err_ns=0.040 metric_levels=[0.091, 0.185, 0.28, 0.374] max_level_err=0.526 final_norm=0.383 metric_dips=0 |
| `100-final-step-file-metric` | `FAIL_SIM_CORRECTNESS` | ref_edges=4 max_edge_err_ns=0.025 metric_levels=[0.095, 0.189, 0.283, 0.378] max_level_err=0.522 final_norm=0.401 metric_dips=0 |
| `100-final-step-file-metric` | `FAIL_SIM_CORRECTNESS` | ref_edges=4 max_edge_err_ns=0.025 metric_levels=[0.095, 0.189, 0.283, 0.378] max_level_err=0.522 final_norm=0.401 metric_dips=0 |
| `101-fixed-gain-amplifier` | `FAIL_SIM_CORRECTNESS` | gain=0.000 gain_err=0.0000 cm_max=0.4500 |
| `101-fixed-gain-amplifier` | `FAIL_SIM_CORRECTNESS` | gain=1.000 gain_err=0.0000 cm_max=0.0000 |
| `101-fixed-gain-amplifier` | `FAIL_SIM_CORRECTNESS` | gain=-5.250 gain_err=0.0000 cm_max=0.0000 |
| `101-fixed-gain-amplifier` | `FAIL_SIM_CORRECTNESS` | gain=8.640 gain_err=0.0000 cm_max=0.0000 |
| `101-fixed-gain-amplifier` | `FAIL_SIM_CORRECTNESS` | gain=4.854 gain_err=3.6546 cm_max=0.2371 |
| `102-gain-estimator` | `FAIL_SIM_CORRECTNESS` | streaming_checker:insufficient_valid_samples=0 |
| `102-gain-estimator` | `FAIL_SIM_CORRECTNESS` | streaming_checker:insufficient_valid_samples=0 |
| `102-gain-estimator` | `FAIL_SIM_CORRECTNESS` | streaming_checker:insufficient_valid_samples=0 |
| `102-gain-estimator` | `FAIL_SIM_CORRECTNESS` | streaming_checker:insufficient_valid_samples=0 |
| `102-gain-estimator` | `FAIL_SIM_CORRECTNESS` | streaming_checker:insufficient_valid_samples=0 |
| `103-iq-downconversion-chain` | `FAIL_SIM_CORRECTNESS` | iq_positive_quadrature_missing i=0.000 q=0.000 |
| `103-iq-downconversion-chain` | `FAIL_SIM_CORRECTNESS` | iq_positive_quadrature_missing i=0.307 q=0.307 |
| `103-iq-downconversion-chain` | `FAIL_SIM_CORRECTNESS` | iq_positive_quadrature_missing i=0.270 q=0.269 |
| `103-iq-downconversion-chain` | `FAIL_SIM_CORRECTNESS` | iq_positive_quadrature_missing i=0.189 q=0.189 |
| `103-iq-downconversion-chain` | `FAIL_SIM_CORRECTNESS` | iq_positive_quadrature_missing i=0.307 q=0.307 |
| `104-ldo-load-step-recovery` | `FAIL_SIM_CORRECTNESS` | ldo_flow_pre_step_regulation_wrong=0.000 |
| `104-ldo-load-step-recovery` | `FAIL_SIM_CORRECTNESS` | ldo_flow_pre_step_regulation_wrong=0.254 |
| `104-ldo-load-step-recovery` | `FAIL_SIM_CORRECTNESS` | ldo_flow_pre_step_regulation_wrong=0.255 |
| `104-ldo-load-step-recovery` | `FAIL_SIM_CORRECTNESS` | ldo_flow_pre_step_regulation_wrong=0.252 |
| `104-ldo-load-step-recovery` | `FAIL_SIM_CORRECTNESS` | ldo_flow_pre_step_regulation_wrong=0.254 |
| `105-pipeline-adc-chain-4b` | `FAIL_SIM_CORRECTNESS` | observed_codes=0 expected_codes=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15 stage_bit_mismatches=16 final_concat_mismatches=0 final_code_mismatches=16 residue_mismatches=17 max_res1_err=0.8438 max_res2_err=0.6750 res2_span=0.0000 reversals=0 bounded_failures=0 |
| `105-pipeline-adc-chain-4b` | `FAIL_SIM_CORRECTNESS` | observed_codes=0 expected_codes=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15 stage_bit_mismatches=16 final_concat_mismatches=0 final_code_mismatches=16 residue_mismatches=17 max_res1_err=0.4894 max_res2_err=0.3915 res2_span=0.1890 reversals=0 bounded_failures=0 |
| `105-pipeline-adc-chain-4b` | `FAIL_SIM_CORRECTNESS` | observed_codes=0 expected_codes=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15 stage_bit_mismatches=16 final_concat_mismatches=0 final_code_mismatches=16 residue_mismatches=17 max_res1_err=0.6311 max_res2_err=0.5805 res2_span=0.1890 reversals=0 bounded_failures=0 |
| `105-pipeline-adc-chain-4b` | `FAIL_SIM_CORRECTNESS` | observed_codes=0 expected_codes=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15 stage_bit_mismatches=16 final_concat_mismatches=0 final_code_mismatches=16 residue_mismatches=17 max_res1_err=0.4894 max_res2_err=0.3915 res2_span=0.1890 reversals=0 bounded_failures=0 |
| `105-pipeline-adc-chain-4b` | `FAIL_SIM_CORRECTNESS` | observed_codes=0 expected_codes=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15 stage_bit_mismatches=16 final_concat_mismatches=0 final_code_mismatches=16 residue_mismatches=17 max_res1_err=0.4894 max_res2_err=0.3915 res2_span=0.1890 reversals=0 bounded_failures=0 |
| `106-programmable-stimulus-sequencer` | `FAIL_SIM_CORRECTNESS` | streaming_checker:sequencer_ramp_not_monotonic drops=0 delta=0.000 start=0.000 |
| `106-programmable-stimulus-sequencer` | `FAIL_SIM_CORRECTNESS` | streaming_checker:sequencer_ramp_not_monotonic drops=0 delta=0.000 start=0.300 |
| `106-programmable-stimulus-sequencer` | `FAIL_SIM_CORRECTNESS` | streaming_checker:sequencer_chirp_segment_wrong min=0.450 max=0.450 mean=0.450 crossings=126 |
| `106-programmable-stimulus-sequencer` | `FAIL_SIM_CORRECTNESS` | streaming_checker:sequencer_mode_switch_discontinuity=0.016/0.144 |
| `106-programmable-stimulus-sequencer` | `FAIL_SIM_CORRECTNESS` | streaming_checker:sequencer_ramp_not_monotonic drops=0 delta=0.089 start=0.090 |
| `107-reference-step-clock` | `FAIL_SIM_CORRECTNESS` | insufficient_clock_swing=0.000 |
| `107-reference-step-clock` | `FAIL_SIM_CORRECTNESS` | period_pre=1.800e-08 period_post=1.800e-08 duty_pre=0.496 duty_post=0.501 |
| `107-reference-step-clock` | `FAIL_SIM_CORRECTNESS` | period_pre=1.800e-08 period_post=2.000e-08 duty_pre=0.496 duty_post=0.500 |
| `107-reference-step-clock` | `FAIL_SIM_CORRECTNESS` | period_pre=1.800e-08 period_post=2.041e-08 duty_pre=0.496 duty_post=0.494 |
| `107-reference-step-clock` | `FAIL_SIM_CORRECTNESS` | period_pre=1.800e-08 period_post=2.200e-08 duty_pre=0.699 duty_post=0.698 |
| `108-reference-startup-enable-flow` | `FAIL_SIM_CORRECTNESS` | ref_startup_wrong_reference=0.000 |
| `108-reference-startup-enable-flow` | `FAIL_SIM_CORRECTNESS` | ref_startup_wrong_reference=0.227 |
| `108-reference-startup-enable-flow` | `FAIL_SIM_CORRECTNESS` | ref_startup_wrong_reference=0.226 |
| `108-reference-startup-enable-flow` | `FAIL_SIM_CORRECTNESS` | ref_startup_wrong_reference=0.227 |
| `108-reference-startup-enable-flow` | `FAIL_SIM_CORRECTNESS` | ref_startup_wrong_reference=0.227 |
| `109-sample-hold-droop-front-end` | `FAIL_SIM_CORRECTNESS` | edges=9 max_sample_err=0.780 coarse_mismatches=4 valid_high_hits=0 valid_low_hits=8 aperture_sensitive=2 droop_windows=0 droop_failures=0 |
| `109-sample-hold-droop-front-end` | `FAIL_SIM_CORRECTNESS` | edges=9 max_sample_err=0.452 coarse_mismatches=0 valid_high_hits=0 valid_low_hits=8 aperture_sensitive=2 droop_windows=0 droop_failures=0 |
| `109-sample-hold-droop-front-end` | `FAIL_SIM_CORRECTNESS` | edges=9 max_sample_err=0.662 coarse_mismatches=4 valid_high_hits=0 valid_low_hits=8 aperture_sensitive=2 droop_windows=0 droop_failures=0 |
| `109-sample-hold-droop-front-end` | `FAIL_SIM_CORRECTNESS` | edges=9 max_sample_err=0.452 coarse_mismatches=0 valid_high_hits=0 valid_low_hits=8 aperture_sensitive=2 droop_windows=0 droop_failures=0 |
| `109-sample-hold-droop-front-end` | `FAIL_SIM_CORRECTNESS` | edges=9 max_sample_err=0.452 coarse_mismatches=0 valid_high_hits=0 valid_low_hits=8 aperture_sensitive=2 droop_windows=0 droop_failures=0 |
| `110-settling-time-measurement` | `FAIL_SIM_CORRECTNESS` | vout_samples=0.000,0.000,0.000,0.000,0.000 done_samples=0.000,0.000,0.000,0.000,0.000 monotone=False boundary_ok=False late_settled=False |
| `110-settling-time-measurement` | `FAIL_SIM_CORRECTNESS` | vout_samples=0.181,0.306,0.330,0.330,0.334 done_samples=0.000,0.000,0.000,0.378,0.378 monotone=True boundary_ok=False late_settled=False |
| `110-settling-time-measurement` | `FAIL_SIM_CORRECTNESS` | vout_samples=0.181,0.306,0.330,0.330,0.334 done_samples=0.000,0.000,0.000,0.378,0.378 monotone=True boundary_ok=False late_settled=False |
| `110-settling-time-measurement` | `FAIL_SIM_CORRECTNESS` | vout_samples=0.181,0.306,0.330,0.330,0.334 done_samples=0.000,0.000,0.000,0.378,0.378 monotone=True boundary_ok=False late_settled=False |
| `110-settling-time-measurement` | `FAIL_SIM_CORRECTNESS` | vout_samples=0.181,0.306,0.330,0.330,0.334 done_samples=0.000,0.000,0.000,0.378,0.378 monotone=True boundary_ok=False late_settled=False |
| `111-clocked-sine-source` | `FAIL_SIM_CORRECTNESS` | streaming_checker:diff_gain=0.00 |
| `111-clocked-sine-source` | `FAIL_SIM_CORRECTNESS` | streaming_checker:diff_gain=0.00 |
| `111-clocked-sine-source` | `FAIL_SIM_CORRECTNESS` | streaming_checker:diff_gain=0.00 |
| `111-clocked-sine-source` | `FAIL_SIM_CORRECTNESS` | streaming_checker:diff_gain=0.00 |
| `111-clocked-sine-source` | `FAIL_SIM_CORRECTNESS` | streaming_checker:diff_gain=3.85 |
| `112-clocked-sar-comparator` | `FAIL_SIM_CORRECTNESS` | dcmpp@7ns=0.0000 expected=0.9000 tol=0.0800 |
| `112-clocked-sar-comparator` | `FAIL_SIM_CORRECTNESS` | dcmpp@17ns=0.0000 expected=0.9000 tol=0.0800 |
| `112-clocked-sar-comparator` | `FAIL_SIM_CORRECTNESS` | dcmpp@7ns=0.0000 expected=0.9000 tol=0.0800 |
| `112-clocked-sar-comparator` | `FAIL_SIM_CORRECTNESS` | dcmpp@7ns=0.4500 expected=0.9000 tol=0.0800 |
| `112-clocked-sar-comparator` | `FAIL_SIM_CORRECTNESS` | dcmpp@7ns=0.3780 expected=0.9000 tol=0.0800 |
| `113-clocked-dac-restore-4b` | `FAIL_SIM_CORRECTNESS` | vout@6ns=0.0000 expected=-0.7312 tol=0.0200 |
| `113-clocked-dac-restore-4b` | `FAIL_SIM_CORRECTNESS` | vout@6ns=-0.7875 expected=-0.7312 tol=0.0200 |
| `113-clocked-dac-restore-4b` | `FAIL_SIM_CORRECTNESS` | vout@6ns=0.0563 expected=-0.7312 tol=0.0200 |
| `113-clocked-dac-restore-4b` | `FAIL_SIM_CORRECTNESS` | vout@6ns=-0.8156 expected=-0.7312 tol=0.0200 |
| `113-clocked-dac-restore-4b` | `FAIL_SIM_CORRECTNESS` | vout@6ns=-0.3071 expected=-0.7312 tol=0.0200 |
| `114-sample-and-hold-ideal` | `FAIL_SIM_CORRECTNESS` | max_sample_error=0.7562 max_hold_span=0.0000 |
| `114-sample-and-hold-ideal` | `FAIL_SIM_CORRECTNESS` | max_sample_error=0.0480 max_hold_span=0.2880 |
| `114-sample-and-hold-ideal` | `FAIL_SIM_CORRECTNESS` | max_sample_error=0.2350 max_hold_span=0.3802 |
| `114-sample-and-hold-ideal` | `FAIL_SIM_CORRECTNESS` | max_sample_error=0.3787 max_hold_span=0.0000 |
| `114-sample-and-hold-ideal` | `FAIL_SIM_CORRECTNESS` | max_sample_error=0.4391 max_hold_span=0.0000 |
| `115-single-shot-pulse` | `FAIL_SIM_CORRECTNESS` | vout@8ns=0.0000 expected=0.9000 tol=0.0800 |
| `115-single-shot-pulse` | `FAIL_SIM_CORRECTNESS` | vout@14ns=0.0000 expected=0.9000 tol=0.0800 |
| `115-single-shot-pulse` | `FAIL_SIM_CORRECTNESS` | vout@8ns=0.0000 expected=0.9000 tol=0.0800 |
| `115-single-shot-pulse` | `FAIL_SIM_CORRECTNESS` | vout@18ns=0.9000 expected=0.0000 tol=0.0800 |
| `115-single-shot-pulse` | `FAIL_SIM_CORRECTNESS` | vout@8ns=0.3780 expected=0.9000 tol=0.0800 |
| `116-clocked-comparator-reset-low` | `FAIL_SIM_CORRECTNESS` | dcmpp@7ns=0.0000 expected=0.9000 tol=0.0800 |
| `116-clocked-comparator-reset-low` | `FAIL_SIM_CORRECTNESS` | dcmpp@17ns=0.9000 expected=0.0000 tol=0.0800 |
| `116-clocked-comparator-reset-low` | `FAIL_SIM_CORRECTNESS` | dcmpp@7ns=0.0000 expected=0.9000 tol=0.0800 |
| `116-clocked-comparator-reset-low` | `FAIL_SIM_CORRECTNESS` | dcmpn@27ns=0.0000 expected=0.9000 tol=0.0800 |
| `116-clocked-comparator-reset-low` | `FAIL_SIM_CORRECTNESS` | dcmpp@7ns=0.3780 expected=0.9000 tol=0.0800 |
| `117-bipolar-dac-4b-continuous` | `FAIL_SIM_CORRECTNESS` | bipolar_dac_max_err=0.7800 codes=[1, 6, 7, 9, 14] |
| `117-bipolar-dac-4b-continuous` | `FAIL_SIM_CORRECTNESS` | bipolar_dac_max_err=0.8400 codes=[1, 6, 7, 9, 14] |
| `117-bipolar-dac-4b-continuous` | `FAIL_SIM_CORRECTNESS` | bipolar_dac_max_err=0.8400 codes=[1, 6, 7, 9, 14] |
| `117-bipolar-dac-4b-continuous` | `FAIL_SIM_CORRECTNESS` | bipolar_dac_max_err=0.1050 codes=[1, 6, 7, 9, 14] |
| `117-bipolar-dac-4b-continuous` | `FAIL_SIM_CORRECTNESS` | bipolar_dac_max_err=0.4524 codes=[1, 6, 7, 9, 14] |
| `118-clocked-dac-restore-7b` | `FAIL_SIM_CORRECTNESS` | vout@6ns=0.0000 expected=-0.8930 tol=0.0250 |
| `118-clocked-dac-restore-7b` | `FAIL_SIM_CORRECTNESS` | vout@16ns=0.2953 expected=-0.3023 tol=0.0250 |
| `118-clocked-dac-restore-7b` | `FAIL_SIM_CORRECTNESS` | vout@26ns=-0.1477 expected=0.3023 tol=0.0250 |
| `118-clocked-dac-restore-7b` | `FAIL_SIM_CORRECTNESS` | vout@26ns=-0.5977 expected=0.3023 tol=0.0250 |
| `118-clocked-dac-restore-7b` | `FAIL_SIM_CORRECTNESS` | vout@6ns=-0.3750 expected=-0.8930 tol=0.0250 |
| `119-crossing-pulse-detector` | `FAIL_SIM_CORRECTNESS` | sigout@7ns=0.0000 expected=0.9000 tol=0.0800 |
| `119-crossing-pulse-detector` | `FAIL_SIM_CORRECTNESS` | sigout@17ns=0.0000 expected=0.9000 tol=0.0800 |
| `119-crossing-pulse-detector` | `FAIL_SIM_CORRECTNESS` | sigout@7ns=0.0000 expected=0.9000 tol=0.0800 |
| `119-crossing-pulse-detector` | `FAIL_SIM_CORRECTNESS` | sigout@12ns=0.9000 expected=0.0000 tol=0.0800 |
| `119-crossing-pulse-detector` | `FAIL_SIM_CORRECTNESS` | sigout@7ns=0.3780 expected=0.9000 tol=0.0800 |
| `120-not-gate-voltage` | `FAIL_SIM_CORRECTNESS` | vout@2ns=0.0000 expected=0.9000 tol=0.0800 |
| `120-not-gate-voltage` | `FAIL_SIM_CORRECTNESS` | vout@2ns=0.0000 expected=0.9000 tol=0.0800 |
| `120-not-gate-voltage` | `FAIL_SIM_CORRECTNESS` | vout@2ns=0.4500 expected=0.9000 tol=0.0800 |
| `120-not-gate-voltage` | `FAIL_SIM_CORRECTNESS` | vout@7ns=0.9000 expected=0.0000 tol=0.0800 |
| `120-not-gate-voltage` | `FAIL_SIM_CORRECTNESS` | vout@2ns=0.3780 expected=0.9000 tol=0.0800 |
| `121-dff-reset-voltage` | `FAIL_SIM_CORRECTNESS` | vout_q@6ns=0.0000 expected=0.9000 tol=0.0800 |
| `121-dff-reset-voltage` | `FAIL_SIM_CORRECTNESS` | vout_qbar@6ns=0.9000 expected=0.0000 tol=0.0800 |
| `121-dff-reset-voltage` | `FAIL_SIM_CORRECTNESS` | vout_q@29ns=0.9000 expected=0.0000 tol=0.0800 |
| `121-dff-reset-voltage` | `FAIL_SIM_CORRECTNESS` | vout_q@6ns=0.0000 expected=0.9000 tol=0.0800 |
| `121-dff-reset-voltage` | `FAIL_SIM_CORRECTNESS` | vout_q@6ns=0.3780 expected=0.9000 tol=0.0800 |
| `122-offset-search-comparator` | `FAIL_SIM_CORRECTNESS` | diff@7.900ns=0.00000 expected=0.01000 cm@7.900ns=0.00000 expected=0.45000 diff@17.900ns=0.00000 expected=0.02000 cm@17.900ns=0.00000 expected=0.45000 diff@27.900ns=0.00000 expected=0.01500 |
| `122-offset-search-comparator` | `FAIL_SIM_CORRECTNESS` | diff@27.900ns=0.01000 expected=0.01500 diff@37.900ns=0.00000 expected=0.01000 |
| `122-offset-search-comparator` | `FAIL_SIM_CORRECTNESS` | diff@7.900ns=-0.00500 expected=0.01000 diff@17.900ns=-0.01000 expected=0.02000 diff@27.900ns=-0.00750 expected=0.01500 diff@37.900ns=-0.00500 expected=0.01000 diff@47.900ns=-0.00625 expected=0.01250 |
| `122-offset-search-comparator` | `FAIL_SIM_CORRECTNESS` | cm@7.900ns=0.70000 expected=0.45000 cm@17.900ns=0.70000 expected=0.45000 cm@27.900ns=0.70000 expected=0.45000 cm@37.900ns=0.70000 expected=0.45000 cm@47.900ns=0.70000 expected=0.45000 |
| `122-offset-search-comparator` | `FAIL_SIM_CORRECTNESS` | diff@7.900ns=0.00420 expected=0.01000 cm@7.900ns=0.18900 expected=0.45000 diff@17.900ns=0.00840 expected=0.02000 cm@17.900ns=0.18900 expected=0.45000 diff@27.900ns=0.00630 expected=0.01500 |
| `123-start-gated-offset-search` | `FAIL_SIM_CORRECTNESS` | common_mode@8ns=0.00000 expected=0.70000 tol=0.00300 |
| `123-start-gated-offset-search` | `FAIL_SIM_CORRECTNESS` | vinp-vinn@18.5ns=0.00000 expected=0.02000 tol=0.00300 |
| `123-start-gated-offset-search` | `FAIL_SIM_CORRECTNESS` | vinp-vinn@28.5ns=0.00000 expected=0.01000 tol=0.00300 |
| `123-start-gated-offset-search` | `FAIL_SIM_CORRECTNESS` | common_mode@8ns=0.45000 expected=0.70000 tol=0.00300 |
| `123-start-gated-offset-search` | `FAIL_SIM_CORRECTNESS` | vinp-vinn@18.5ns=0.00840 expected=0.02000 tol=0.00300 |
| `124-comp-os-detect` | `FAIL_SIM_CORRECTNESS` | vinp-vinn@8.5ns=0.00000 expected=0.10000 tol=0.00300 |
| `124-comp-os-detect` | `FAIL_SIM_CORRECTNESS` | vinp-vinn@8.5ns=0.05000 expected=0.10000 tol=0.00300 |
| `124-comp-os-detect` | `FAIL_SIM_CORRECTNESS` | vinp-vinn@8.5ns=-0.10000 expected=0.10000 tol=0.00300 |
| `124-comp-os-detect` | `FAIL_SIM_CORRECTNESS` | vinp-vinn@18.5ns=0.00000 expected=0.05000 tol=0.00300 |
| `124-comp-os-detect` | `FAIL_SIM_CORRECTNESS` | vinp-vinn@8.5ns=0.04200 expected=0.10000 tol=0.00300 |
| `125-clocked-dac-4b-binary` | `FAIL_SIM_CORRECTNESS` | vout@6ns=0.0000 expected=-0.8438 tol=0.0250 |
| `125-clocked-dac-4b-binary` | `FAIL_SIM_CORRECTNESS` | vout@6ns=-0.9000 expected=-0.8438 tol=0.0250 |
| `125-clocked-dac-4b-binary` | `FAIL_SIM_CORRECTNESS` | vout@16ns=0.2812 expected=-0.2812 tol=0.0250 |
| `125-clocked-dac-4b-binary` | `FAIL_SIM_CORRECTNESS` | vout@6ns=0.0000 expected=-0.8438 tol=0.0250 |
| `125-clocked-dac-4b-binary` | `FAIL_SIM_CORRECTNESS` | vout@6ns=-0.3544 expected=-0.8438 tol=0.0250 |
| `126-latched-comparator-delay` | `FAIL_SIM_CORRECTNESS` | dout@6ns=0.0000 expected=0.9000 tol=0.0800 |
| `126-latched-comparator-delay` | `FAIL_SIM_CORRECTNESS` | dout@6ns=0.0000 expected=0.9000 tol=0.0800 |
| `126-latched-comparator-delay` | `FAIL_SIM_CORRECTNESS` | dout@6ns=0.4500 expected=0.9000 tol=0.0800 |
| `126-latched-comparator-delay` | `FAIL_SIM_CORRECTNESS` | dout@6ns=0.0000 expected=0.9000 tol=0.0800 |
| `126-latched-comparator-delay` | `FAIL_SIM_CORRECTNESS` | dout@6ns=0.3780 expected=0.9000 tol=0.0800 |
| `127-sar-weighted-sum` | `FAIL_SIM_CORRECTNESS` | vout@2ns=0.0000 expected=-1.0000 tol=0.0250 |
| `127-sar-weighted-sum` | `FAIL_SIM_CORRECTNESS` | vout@12ns=-0.9375 expected=-0.9062 tol=0.0250 |
| `127-sar-weighted-sum` | `FAIL_SIM_CORRECTNESS` | vout@12ns=-0.9531 expected=-0.9062 tol=0.0250 |
| `127-sar-weighted-sum` | `FAIL_SIM_CORRECTNESS` | vout@2ns=0.0000 expected=-1.0000 tol=0.0250 |
| `127-sar-weighted-sum` | `FAIL_SIM_CORRECTNESS` | vout@2ns=-0.4200 expected=-1.0000 tol=0.0250 |
| `128-two-input-and-gate` | `FAIL_SIM_CORRECTNESS` | out@25ns=0.0000 expected=0.9000 tol=0.0800 |
| `128-two-input-and-gate` | `FAIL_SIM_CORRECTNESS` | out@15ns=0.9000 expected=0.0000 tol=0.0800 |
| `128-two-input-and-gate` | `FAIL_SIM_CORRECTNESS` | out@15ns=0.9000 expected=0.0000 tol=0.0800 |
| `128-two-input-and-gate` | `FAIL_SIM_CORRECTNESS` | out@25ns=0.4500 expected=0.9000 tol=0.0800 |
| `128-two-input-and-gate` | `FAIL_SIM_CORRECTNESS` | out@25ns=0.3780 expected=0.9000 tol=0.0800 |
| `129-two-input-xor-gate` | `FAIL_SIM_CORRECTNESS` | out@15ns=0.0000 expected=0.9000 tol=0.0800 |
| `129-two-input-xor-gate` | `FAIL_SIM_CORRECTNESS` | out@25ns=0.9000 expected=0.0000 tol=0.0800 |
| `129-two-input-xor-gate` | `FAIL_SIM_CORRECTNESS` | out@5ns=0.9000 expected=0.0000 tol=0.0800 |
| `129-two-input-xor-gate` | `FAIL_SIM_CORRECTNESS` | out@15ns=0.4500 expected=0.9000 tol=0.0800 |
| `129-two-input-xor-gate` | `FAIL_SIM_CORRECTNESS` | out@15ns=0.3780 expected=0.9000 tol=0.0800 |
| `130-analog-mux-threshold` | `FAIL_SIM_CORRECTNESS` | vout@5ns=0.0000 expected=0.7500 tol=0.0250 |
| `130-analog-mux-threshold` | `FAIL_SIM_CORRECTNESS` | vout@5ns=0.2000 expected=0.7500 tol=0.0250 |
| `130-analog-mux-threshold` | `FAIL_SIM_CORRECTNESS` | vout@35ns=0.5500 expected=0.4500 tol=0.0250 |
| `130-analog-mux-threshold` | `FAIL_SIM_CORRECTNESS` | vout@5ns=0.4750 expected=0.7500 tol=0.0250 |
| `130-analog-mux-threshold` | `FAIL_SIM_CORRECTNESS` | vout@5ns=0.3150 expected=0.7500 tol=0.0250 |
| `131-two-bit-counter-marker` | `FAIL_SIM_CORRECTNESS` | mc@36ns=0.0000 expected=1.0000 tol=0.0800 |
| `131-two-bit-counter-marker` | `FAIL_SIM_CORRECTNESS` | mc@6ns=1.0000 expected=0.0000 tol=0.0800 |
| `131-two-bit-counter-marker` | `FAIL_SIM_CORRECTNESS` | mc@26ns=1.0000 expected=0.0000 tol=0.0800 |
| `131-two-bit-counter-marker` | `FAIL_SIM_CORRECTNESS` | mc@26ns=1.0000 expected=0.0000 tol=0.0800 |
| `131-two-bit-counter-marker` | `FAIL_SIM_CORRECTNESS` | mc@36ns=0.4200 expected=1.0000 tol=0.0800 |
| `132-max-detector-hold` | `FAIL_SIM_CORRECTNESS` | vout@5ns=0.0000 expected=0.2000 tol=0.0250 |
| `132-max-detector-hold` | `FAIL_SIM_CORRECTNESS` | vout@25ns=0.4000 expected=0.7000 tol=0.0250 |
| `132-max-detector-hold` | `FAIL_SIM_CORRECTNESS` | vout@15ns=0.2000 expected=0.7000 tol=0.0250 |
| `132-max-detector-hold` | `FAIL_SIM_CORRECTNESS` | vout@15ns=0.2000 expected=0.7000 tol=0.0250 |
| `132-max-detector-hold` | `FAIL_SIM_CORRECTNESS` | vout@5ns=0.0840 expected=0.2000 tol=0.0250 |
| `133-time-diff-detector` | `FAIL_SIM_CORRECTNESS` | vout@26ns=0.0000 expected=-0.9000 tol=0.0800 |
| `133-time-diff-detector` | `FAIL_SIM_CORRECTNESS` | vout@26ns=0.9000 expected=-0.9000 tol=0.0800 |
| `133-time-diff-detector` | `FAIL_SIM_CORRECTNESS` | vout@26ns=-0.5000 expected=-0.9000 tol=0.0800 |
| `133-time-diff-detector` | `FAIL_SIM_CORRECTNESS` | vout@46ns=-0.9000 expected=0.9000 tol=0.0800 |
| `133-time-diff-detector` | `FAIL_SIM_CORRECTNESS` | vout@26ns=-0.3780 expected=-0.9000 tol=0.0800 |
| `134-differential-buffer` | `FAIL_SIM_CORRECTNESS` | voutp@5ns=0.0000 expected=0.2500 tol=0.0250 |
| `134-differential-buffer` | `FAIL_SIM_CORRECTNESS` | voutp@5ns=0.5500 expected=0.2500 tol=0.0250 |
| `134-differential-buffer` | `FAIL_SIM_CORRECTNESS` | voutp@5ns=0.1250 expected=0.2500 tol=0.0250 |
| `134-differential-buffer` | `FAIL_SIM_CORRECTNESS` | voutp@5ns=0.4000 expected=0.2500 tol=0.0250 |
| `134-differential-buffer` | `FAIL_SIM_CORRECTNESS` | voutp@5ns=0.1050 expected=0.2500 tol=0.0250 |
| `135-two-input-or-gate` | `FAIL_SIM_CORRECTNESS` | out@15ns=0.0000 expected=0.9000 tol=0.0800 |
| `135-two-input-or-gate` | `FAIL_SIM_CORRECTNESS` | out@15ns=0.0000 expected=0.9000 tol=0.0800 |
| `135-two-input-or-gate` | `FAIL_SIM_CORRECTNESS` | out@25ns=0.0000 expected=0.9000 tol=0.0800 |
| `135-two-input-or-gate` | `FAIL_SIM_CORRECTNESS` | out@15ns=0.4500 expected=0.9000 tol=0.0800 |
| `135-two-input-or-gate` | `FAIL_SIM_CORRECTNESS` | out@15ns=0.3780 expected=0.9000 tol=0.0800 |
| `136-sar-cdac-residue` | `FAIL_SIM_CORRECTNESS` | vres@6ns=0.0000 expected=0.2000 tol=0.0250 |
| `136-sar-cdac-residue` | `FAIL_SIM_CORRECTNESS` | vres@12ns=0.2000 expected=0.6500 tol=0.0250 |
| `136-sar-cdac-residue` | `FAIL_SIM_CORRECTNESS` | vres@12ns=1.1000 expected=0.6500 tol=0.0250 |
| `136-sar-cdac-residue` | `FAIL_SIM_CORRECTNESS` | cdac_sequence_unexpected samples=0.2000,0.6500,0.4250,0.3125,0.2562,0.2281,0.2281 |
| `136-sar-cdac-residue` | `FAIL_SIM_CORRECTNESS` | vres@6ns=0.0840 expected=0.2000 tol=0.0250 |
| `137-two-input-nand-gate` | `FAIL_SIM_CORRECTNESS` | out@5ns=0.0000 expected=0.9000 tol=0.0800 |
| `137-two-input-nand-gate` | `FAIL_SIM_CORRECTNESS` | out@5ns=0.0000 expected=0.9000 tol=0.0800 |
| `137-two-input-nand-gate` | `FAIL_SIM_CORRECTNESS` | out@5ns=0.0000 expected=0.9000 tol=0.0800 |
| `137-two-input-nand-gate` | `FAIL_SIM_CORRECTNESS` | out@5ns=0.4500 expected=0.9000 tol=0.0800 |
| `137-two-input-nand-gate` | `FAIL_SIM_CORRECTNESS` | out@5ns=0.3780 expected=0.9000 tol=0.0800 |
| `138-two-input-nor-gate` | `FAIL_SIM_CORRECTNESS` | out@5ns=0.0000 expected=0.9000 tol=0.0800 |
| `138-two-input-nor-gate` | `FAIL_SIM_CORRECTNESS` | out@5ns=0.0000 expected=0.9000 tol=0.0800 |
| `138-two-input-nor-gate` | `FAIL_SIM_CORRECTNESS` | out@5ns=0.0000 expected=0.9000 tol=0.0800 |
| `138-two-input-nor-gate` | `FAIL_SIM_CORRECTNESS` | out@5ns=0.4500 expected=0.9000 tol=0.0800 |
| `138-two-input-nor-gate` | `FAIL_SIM_CORRECTNESS` | out@5ns=0.3780 expected=0.9000 tol=0.0800 |
| `139-three-input-and-gate` | `FAIL_SIM_CORRECTNESS` | vout@35ns=0.0000 expected=0.9000 tol=0.0800 |
| `139-three-input-and-gate` | `FAIL_SIM_CORRECTNESS` | vout@15ns=0.9000 expected=0.0000 tol=0.0800 |
| `139-three-input-and-gate` | `FAIL_SIM_CORRECTNESS` | vout@25ns=0.9000 expected=0.0000 tol=0.0800 |
| `139-three-input-and-gate` | `FAIL_SIM_CORRECTNESS` | vout@35ns=0.4500 expected=0.9000 tol=0.0800 |
| `139-three-input-and-gate` | `FAIL_SIM_CORRECTNESS` | vout@35ns=0.3780 expected=0.9000 tol=0.0800 |
| `140-three-input-or-gate` | `FAIL_SIM_CORRECTNESS` | vout@15ns=0.0000 expected=0.9000 tol=0.0800 |
| `140-three-input-or-gate` | `FAIL_SIM_CORRECTNESS` | vout@15ns=0.0000 expected=0.9000 tol=0.0800 |
| `140-three-input-or-gate` | `FAIL_SIM_CORRECTNESS` | vout@25ns=0.0000 expected=0.9000 tol=0.0800 |
| `140-three-input-or-gate` | `FAIL_SIM_CORRECTNESS` | vout@15ns=0.4500 expected=0.9000 tol=0.0800 |
| `140-three-input-or-gate` | `FAIL_SIM_CORRECTNESS` | vout@15ns=0.3780 expected=0.9000 tol=0.0800 |
| `141-three-input-xor-gate` | `FAIL_SIM_CORRECTNESS` | vout@15ns=0.0000 expected=0.9000 tol=0.0800 |
| `141-three-input-xor-gate` | `FAIL_SIM_CORRECTNESS` | vout@25ns=0.9000 expected=0.0000 tol=0.0800 |
| `141-three-input-xor-gate` | `FAIL_SIM_CORRECTNESS` | vout@5ns=0.9000 expected=0.0000 tol=0.0800 |
| `141-three-input-xor-gate` | `FAIL_SIM_CORRECTNESS` | vout@15ns=0.4500 expected=0.9000 tol=0.0800 |
| `141-three-input-xor-gate` | `FAIL_SIM_CORRECTNESS` | vout@15ns=0.3780 expected=0.9000 tol=0.0800 |
| `142-attenuator-gain` | `FAIL_SIM_CORRECTNESS` | vout@5ns=0.0000 expected=0.1000 tol=0.0150 |
| `142-attenuator-gain` | `FAIL_SIM_CORRECTNESS` | vout@5ns=0.2000 expected=0.1000 tol=0.0150 |
| `142-attenuator-gain` | `FAIL_SIM_CORRECTNESS` | vout@5ns=0.4000 expected=0.1000 tol=0.0150 |
| `142-attenuator-gain` | `FAIL_SIM_CORRECTNESS` | vout@5ns=0.0500 expected=0.1000 tol=0.0150 |
| `142-attenuator-gain` | `FAIL_SIM_CORRECTNESS` | vout@5ns=0.0420 expected=0.1000 tol=0.0150 |
| `143-deadband-window` | `FAIL_SIM_CORRECTNESS` | sigout@5ns=0.0000 expected=-0.3000 tol=0.0150 |
| `143-deadband-window` | `FAIL_SIM_CORRECTNESS` | sigout@5ns=0.0000 expected=-0.3000 tol=0.0150 |
| `143-deadband-window` | `FAIL_SIM_CORRECTNESS` | sigout@5ns=-0.7000 expected=-0.3000 tol=0.0150 |
| `143-deadband-window` | `FAIL_SIM_CORRECTNESS` | sigout@5ns=-0.2000 expected=-0.3000 tol=0.0150 |
| `143-deadband-window` | `FAIL_SIM_CORRECTNESS` | sigout@5ns=-0.1260 expected=-0.3000 tol=0.0150 |
| `144-differential-deadband` | `FAIL_SIM_CORRECTNESS` | sigout@5ns=0.0000 expected=-0.2500 tol=0.0150 |
| `144-differential-deadband` | `FAIL_SIM_CORRECTNESS` | sigout@15ns=0.0000 expected=0.0500 tol=0.0150 |
| `144-differential-deadband` | `FAIL_SIM_CORRECTNESS` | sigout@5ns=-0.6500 expected=-0.2500 tol=0.0150 |
| `144-differential-deadband` | `FAIL_SIM_CORRECTNESS` | sigout@5ns=0.0500 expected=-0.2500 tol=0.0150 |
| `144-differential-deadband` | `FAIL_SIM_CORRECTNESS` | sigout@5ns=-0.1050 expected=-0.2500 tol=0.0150 |
| `145-hard-voltage-clamp` | `FAIL_SIM_CORRECTNESS` | vout@5ns=0.0000 expected=-0.2000 tol=0.0150 |
| `145-hard-voltage-clamp` | `FAIL_SIM_CORRECTNESS` | vout@5ns=-0.5000 expected=-0.2000 tol=0.0150 |
| `145-hard-voltage-clamp` | `FAIL_SIM_CORRECTNESS` | vout@25ns=0.9000 expected=0.6000 tol=0.0150 |
| `145-hard-voltage-clamp` | `FAIL_SIM_CORRECTNESS` | vout@5ns=0.6000 expected=-0.2000 tol=0.0150 |
| `145-hard-voltage-clamp` | `FAIL_SIM_CORRECTNESS` | vout@25ns=0.2520 expected=0.6000 tol=0.0150 |
| `146-smooth-comparator-tanh` | `FAIL_SIM_CORRECTNESS` | checked=1679 max_tanh_error=0.89999 |
| `146-smooth-comparator-tanh` | `FAIL_SIM_CORRECTNESS` | checked=1679 max_tanh_error=0.89999 |
| `146-smooth-comparator-tanh` | `FAIL_SIM_CORRECTNESS` | checked=1679 max_tanh_error=0.13476 |
| `146-smooth-comparator-tanh` | `FAIL_SIM_CORRECTNESS` | checked=1679 max_tanh_error=0.22500 |
| `146-smooth-comparator-tanh` | `FAIL_SIM_CORRECTNESS` | checked=1679 max_tanh_error=0.52200 |
| `147-limiter-rails` | `FAIL_SIM_CORRECTNESS` | vout@5ns=0.0000 expected=0.1000 tol=0.0150 |
| `147-limiter-rails` | `FAIL_SIM_CORRECTNESS` | vout@5ns=0.0000 expected=0.1000 tol=0.0150 |
| `147-limiter-rails` | `FAIL_SIM_CORRECTNESS` | vout@5ns=0.2000 expected=0.1000 tol=0.0150 |
| `147-limiter-rails` | `FAIL_SIM_CORRECTNESS` | vout@5ns=-0.2000 expected=0.1000 tol=0.0150 |
| `147-limiter-rails` | `FAIL_SIM_CORRECTNESS` | vout@25ns=0.2940 expected=0.7000 tol=0.0150 |
| `148-absolute-value` | `FAIL_SIM_CORRECTNESS` | checked=641 max_abs_error=0.75000 |
| `148-absolute-value` | `FAIL_SIM_CORRECTNESS` | checked=641 max_abs_error=1.50000 |
| `148-absolute-value` | `FAIL_SIM_CORRECTNESS` | checked=641 max_abs_error=1.50000 |
| `148-absolute-value` | `FAIL_SIM_CORRECTNESS` | checked=641 max_abs_error=0.37500 |
| `148-absolute-value` | `FAIL_SIM_CORRECTNESS` | checked=641 max_abs_error=0.43500 |
| `149-offset-gain-amplifier` | `FAIL_SIM_CORRECTNESS` | sigout@5ns=0.0000 expected=-0.3000 tol=0.0150 |
| `149-offset-gain-amplifier` | `FAIL_SIM_CORRECTNESS` | sigout@5ns=0.3000 expected=-0.3000 tol=0.0150 |
| `149-offset-gain-amplifier` | `FAIL_SIM_CORRECTNESS` | sigout@5ns=-0.2000 expected=-0.3000 tol=0.0150 |
| `149-offset-gain-amplifier` | `FAIL_SIM_CORRECTNESS` | sigout@5ns=0.9000 expected=-0.3000 tol=0.0150 |
| `149-offset-gain-amplifier` | `FAIL_SIM_CORRECTNESS` | sigout@5ns=-0.1260 expected=-0.3000 tol=0.0150 |
| `150-safe-voltage-divider` | `FAIL_SIM_CORRECTNESS` | sigout@5ns=0.0000 expected=1.0000 tol=0.0300 |
| `150-safe-voltage-divider` | `FAIL_SIM_CORRECTNESS` | sigout@15ns=6.0000 expected=2.4000 tol=0.0300 |
| `150-safe-voltage-divider` | `FAIL_SIM_CORRECTNESS` | sigout@25ns=-1.6000 expected=1.6000 tol=0.0300 |
| `150-safe-voltage-divider` | `FAIL_SIM_CORRECTNESS` | sigout@5ns=0.5000 expected=1.0000 tol=0.0300 |
| `150-safe-voltage-divider` | `FAIL_SIM_CORRECTNESS` | sigout@5ns=0.4200 expected=1.0000 tol=0.0300 |
| `151-polynomial-differential-vcvs` | `FAIL_SIM_CORRECTNESS` | outp@5ns=0.0000 expected=0.3995 tol=0.0250 |
| `151-polynomial-differential-vcvs` | `FAIL_SIM_CORRECTNESS` | outp@5ns=0.2990 expected=0.3995 tol=0.0250 |
| `151-polynomial-differential-vcvs` | `FAIL_SIM_CORRECTNESS` | outp@5ns=0.6005 expected=0.3995 tol=0.0250 |
| `151-polynomial-differential-vcvs` | `FAIL_SIM_CORRECTNESS` | outp@5ns=-0.1005 expected=0.3995 tol=0.0250 |
| `151-polynomial-differential-vcvs` | `FAIL_SIM_CORRECTNESS` | outp@5ns=0.1678 expected=0.3995 tol=0.0250 |
| `152-differential-gain-driver` | `FAIL_SIM_CORRECTNESS` | sigout_p@5ns=0.0000 expected=0.3500 tol=0.0200 |
| `152-differential-gain-driver` | `FAIL_SIM_CORRECTNESS` | sigout_p@5ns=0.2500 expected=0.3500 tol=0.0200 |
| `152-differential-gain-driver` | `FAIL_SIM_CORRECTNESS` | sigout_p@5ns=0.2500 expected=0.3500 tol=0.0200 |
| `152-differential-gain-driver` | `FAIL_SIM_CORRECTNESS` | sigout_p@5ns=0.5500 expected=0.3500 tol=0.0200 |
| `152-differential-gain-driver` | `FAIL_SIM_CORRECTNESS` | sigout_p@5ns=0.4080 expected=0.3500 tol=0.0200 |
| `153-limiting-differential-amplifier` | `FAIL_SIM_CORRECTNESS` | sigout@5ns=0.0000 expected=-0.4000 tol=0.0200 |
| `153-limiting-differential-amplifier` | `FAIL_SIM_CORRECTNESS` | sigout@15ns=0.3500 expected=0.2000 tol=0.0200 |
| `153-limiting-differential-amplifier` | `FAIL_SIM_CORRECTNESS` | sigout@5ns=-0.8500 expected=-0.4000 tol=0.0200 |
| `153-limiting-differential-amplifier` | `FAIL_SIM_CORRECTNESS` | sigout@15ns=-0.0000 expected=0.2000 tol=0.0200 |
| `153-limiting-differential-amplifier` | `FAIL_SIM_CORRECTNESS` | sigout@5ns=-0.1680 expected=-0.4000 tol=0.0200 |
| `154-analog-multiplier` | `FAIL_SIM_CORRECTNESS` | sigout@5ns=0.0000 expected=0.2000 tol=0.0150 |
| `154-analog-multiplier` | `FAIL_SIM_CORRECTNESS` | sigout@5ns=1.4000 expected=0.2000 tol=0.0150 |
| `154-analog-multiplier` | `FAIL_SIM_CORRECTNESS` | sigout@5ns=0.1000 expected=0.2000 tol=0.0150 |
| `154-analog-multiplier` | `FAIL_SIM_CORRECTNESS` | sigout@5ns=0.0800 expected=0.2000 tol=0.0150 |
| `154-analog-multiplier` | `FAIL_SIM_CORRECTNESS` | sigout@5ns=0.0840 expected=0.2000 tol=0.0150 |
| `155-three-way-threshold-mux` | `FAIL_SIM_CORRECTNESS` | sigout@5ns=0.0000 expected=0.1000 tol=0.0200 |
| `155-three-way-threshold-mux` | `FAIL_SIM_CORRECTNESS` | sigout@5ns=0.9000 expected=0.1000 tol=0.0200 |
| `155-three-way-threshold-mux` | `FAIL_SIM_CORRECTNESS` | sigout@5ns=0.5000 expected=0.1000 tol=0.0200 |
| `155-three-way-threshold-mux` | `FAIL_SIM_CORRECTNESS` | sigout@15ns=0.9000 expected=0.5000 tol=0.0200 |
| `155-three-way-threshold-mux` | `FAIL_SIM_CORRECTNESS` | sigout@5ns=0.0420 expected=0.1000 tol=0.0200 |
| `156-differential-amplifier-core` | `FAIL_SIM_CORRECTNESS` | sigout@5ns=0.0000 expected=-0.5000 tol=0.0200 |
| `156-differential-amplifier-core` | `FAIL_SIM_CORRECTNESS` | sigout@5ns=0.4000 expected=-0.5000 tol=0.0200 |
| `156-differential-amplifier-core` | `FAIL_SIM_CORRECTNESS` | sigout@5ns=-0.4000 expected=-0.5000 tol=0.0200 |
| `156-differential-amplifier-core` | `FAIL_SIM_CORRECTNESS` | sigout@5ns=-0.2500 expected=-0.5000 tol=0.0200 |
| `156-differential-amplifier-core` | `FAIL_SIM_CORRECTNESS` | sigout@5ns=-0.2100 expected=-0.5000 tol=0.0200 |
| `157-logarithmic-amplifier` | `FAIL_SIM_CORRECTNESS` | sigout@5ns=0.0000 expected=-2.3026 tol=0.0350 |
| `157-logarithmic-amplifier` | `FAIL_SIM_CORRECTNESS` | sigout@25ns=-2.3026 expected=-0.6931 tol=0.0350 |
| `157-logarithmic-amplifier` | `FAIL_SIM_CORRECTNESS` | simulator_error=math domain error |
| `157-logarithmic-amplifier` | `FAIL_SIM_CORRECTNESS` | sigout@5ns=-1.6094 expected=-2.3026 tol=0.0350 |
| `157-logarithmic-amplifier` | `FAIL_SIM_CORRECTNESS` | sigout@5ns=-0.9671 expected=-2.3026 tol=0.0350 |
| `158-soft-voltage-clamp` | `FAIL_SIM_CORRECTNESS` | vout@5ns=0.0000 expected=-0.1729 tol=0.0250 |
| `158-soft-voltage-clamp` | `FAIL_SIM_CORRECTNESS` | vout@5ns=-0.2000 expected=-0.1729 tol=0.0250 |
| `158-soft-voltage-clamp` | `FAIL_SIM_CORRECTNESS` | vout@5ns=-0.3264 expected=-0.1729 tol=0.0250 |
| `158-soft-voltage-clamp` | `FAIL_SIM_CORRECTNESS` | vout@5ns=-0.0865 expected=-0.1729 tol=0.0250 |
| `158-soft-voltage-clamp` | `FAIL_SIM_CORRECTNESS` | vout@5ns=-0.0726 expected=-0.1729 tol=0.0250 |
| `159-variable-gain-differential-amplifier` | `FAIL_SIM_CORRECTNESS` | sigout@15ns=0.0000 expected=0.4000 tol=0.0250 |
| `159-variable-gain-differential-amplifier` | `FAIL_SIM_CORRECTNESS` | sigout@5ns=-0.2000 expected=0.0000 tol=0.0250 |
| `159-variable-gain-differential-amplifier` | `FAIL_SIM_CORRECTNESS` | sigout@5ns=-0.1800 expected=0.0000 tol=0.0250 |
| `159-variable-gain-differential-amplifier` | `FAIL_SIM_CORRECTNESS` | sigout@25ns=0.9200 expected=0.8000 tol=0.0250 |
| `159-variable-gain-differential-amplifier` | `FAIL_SIM_CORRECTNESS` | sigout@15ns=0.1680 expected=0.4000 tol=0.0250 |
| `160-voltage-controlled-gain-amplifier` | `FAIL_SIM_CORRECTNESS` | vout@5ns=0.0000 expected=0.3125 tol=0.0250 |
| `160-voltage-controlled-gain-amplifier` | `FAIL_SIM_CORRECTNESS` | vout@5ns=0.3500 expected=0.3125 tol=0.0250 |
| `160-voltage-controlled-gain-amplifier` | `FAIL_SIM_CORRECTNESS` | vout@5ns=0.1437 expected=0.3125 tol=0.0250 |
| `160-voltage-controlled-gain-amplifier` | `FAIL_SIM_CORRECTNESS` | vout@25ns=1.5500 expected=0.9000 tol=0.0250 |
| `160-voltage-controlled-gain-amplifier` | `FAIL_SIM_CORRECTNESS` | vout@5ns=0.1313 expected=0.3125 tol=0.0250 |
| `161-ideal-differential-opamp` | `FAIL_SIM_CORRECTNESS` | voutp@5ns=0.0000 expected=0.3000 tol=0.0250 |
| `161-ideal-differential-opamp` | `FAIL_SIM_CORRECTNESS` | voutp@5ns=0.4000 expected=0.3000 tol=0.0250 |
| `161-ideal-differential-opamp` | `FAIL_SIM_CORRECTNESS` | voutp@5ns=0.7000 expected=0.3000 tol=0.0250 |
| `161-ideal-differential-opamp` | `FAIL_SIM_CORRECTNESS` | voutp@5ns=-0.2000 expected=0.3000 tol=0.0250 |
| `161-ideal-differential-opamp` | `FAIL_SIM_CORRECTNESS` | voutp@5ns=0.1260 expected=0.3000 tol=0.0250 |
| `162-half-adder-logic` | `FAIL_SIM_CORRECTNESS` | vout_sum@15ns=0.0000 expected=0.9000 tol=0.0800 |
| `162-half-adder-logic` | `FAIL_SIM_CORRECTNESS` | vout_sum@35ns=0.9000 expected=0.0000 tol=0.0800 |
| `162-half-adder-logic` | `FAIL_SIM_CORRECTNESS` | vout_carry@15ns=0.9000 expected=0.0000 tol=0.0800 |
| `162-half-adder-logic` | `FAIL_SIM_CORRECTNESS` | vout_sum@15ns=0.4500 expected=0.9000 tol=0.0800 |
| `162-half-adder-logic` | `FAIL_SIM_CORRECTNESS` | vout_carry@35ns=0.3780 expected=0.9000 tol=0.0800 |
| `163-full-adder-logic` | `FAIL_SIM_CORRECTNESS` | vout_sum@15ns=0.0000 expected=0.9000 tol=0.0800 |
| `163-full-adder-logic` | `FAIL_SIM_CORRECTNESS` | vout_sum@15ns=0.0000 expected=0.9000 tol=0.0800 |
| `163-full-adder-logic` | `FAIL_SIM_CORRECTNESS` | vout_carry@45ns=0.0000 expected=0.9000 tol=0.0800 |
| `163-full-adder-logic` | `FAIL_SIM_CORRECTNESS` | vout_sum@5ns=0.9000 expected=0.0000 tol=0.0800 |
| `163-full-adder-logic` | `FAIL_SIM_CORRECTNESS` | vout_carry@45ns=0.3780 expected=0.9000 tol=0.0800 |
| `164-half-subtractor-logic` | `FAIL_SIM_CORRECTNESS` | vout_diff@15ns=0.0000 expected=0.9000 tol=0.0800 |
| `164-half-subtractor-logic` | `FAIL_SIM_CORRECTNESS` | vout_borrow@15ns=0.0000 expected=0.9000 tol=0.0800 |
| `164-half-subtractor-logic` | `FAIL_SIM_CORRECTNESS` | vout_diff@15ns=0.0000 expected=0.9000 tol=0.0800 |
| `164-half-subtractor-logic` | `FAIL_SIM_CORRECTNESS` | vout_diff@15ns=0.4500 expected=0.9000 tol=0.0800 |
| `164-half-subtractor-logic` | `FAIL_SIM_CORRECTNESS` | vout_diff@15ns=0.3780 expected=0.9000 tol=0.0800 |
| `165-full-subtractor-logic` | `FAIL_SIM_CORRECTNESS` | vout_diff@15ns=0.0000 expected=0.9000 tol=0.0800 |
| `165-full-subtractor-logic` | `FAIL_SIM_CORRECTNESS` | vout_diff@15ns=0.0000 expected=0.9000 tol=0.0800 |
| `165-full-subtractor-logic` | `FAIL_SIM_CORRECTNESS` | vout_borrow@15ns=0.0000 expected=0.9000 tol=0.0800 |
| `165-full-subtractor-logic` | `FAIL_SIM_CORRECTNESS` | vout_diff@5ns=0.9000 expected=0.0000 tol=0.0800 |
| `165-full-subtractor-logic` | `FAIL_SIM_CORRECTNESS` | vout_diff@15ns=0.3780 expected=0.9000 tol=0.0800 |
| `166-rs-latch-voltage` | `FAIL_SIM_CORRECTNESS` | vout_q@12ns=0.0000 expected=0.9000 tol=0.0800 |
| `166-rs-latch-voltage` | `FAIL_SIM_CORRECTNESS` | vout_q@22ns=0.0000 expected=0.9000 tol=0.0800 |
| `166-rs-latch-voltage` | `FAIL_SIM_CORRECTNESS` | vout_q@12ns=0.0000 expected=0.9000 tol=0.0800 |
| `166-rs-latch-voltage` | `FAIL_SIM_CORRECTNESS` | vout_qbar@5ns=0.0000 expected=0.9000 tol=0.0800 |
| `166-rs-latch-voltage` | `FAIL_SIM_CORRECTNESS` | vout_q@12ns=0.3780 expected=0.9000 tol=0.0800 |
| `167-ideal-adc-4bit-quantizer` | `FAIL_SIM_CORRECTNESS` | adc4_quantizer_max_err=15.0000 codes=[0, 6, 10, 14, 15] |
| `167-ideal-adc-4bit-quantizer` | `FAIL_SIM_CORRECTNESS` | adc4_quantizer_max_err=7.5000 codes=[0, 6, 10, 14, 15] |
| `167-ideal-adc-4bit-quantizer` | `FAIL_SIM_CORRECTNESS` | adc4_quantizer_max_err=6.0000 codes=[0, 6, 10, 14, 15] |
| `167-ideal-adc-4bit-quantizer` | `FAIL_SIM_CORRECTNESS` | adc4_quantizer_max_err=1.0000 codes=[0, 6, 10, 14, 15] |
| `167-ideal-adc-4bit-quantizer` | `FAIL_SIM_CORRECTNESS` | adc4_quantizer_max_err=8.7000 codes=[0, 6, 10, 14, 15] |
| `168-ideal-dac-4bit-differential` | `FAIL_SIM_CORRECTNESS` | differential_dac_max_err=1.0688 max_cm_error=0.6000 codes=[2, 7, 12, 15] |
| `168-ideal-dac-4bit-differential` | `FAIL_SIM_CORRECTNESS` | differential_dac_max_err=0.0646 max_cm_error=0.0000 codes=[2, 7, 12, 15] |
| `168-ideal-dac-4bit-differential` | `FAIL_SIM_CORRECTNESS` | differential_dac_max_err=0.0313 max_cm_error=0.0000 codes=[2, 7, 12, 15] |
| `168-ideal-dac-4bit-differential` | `FAIL_SIM_CORRECTNESS` | differential_dac_max_err=0.9375 max_cm_error=0.0000 codes=[2, 7, 12, 15] |
| `168-ideal-dac-4bit-differential` | `FAIL_SIM_CORRECTNESS` | differential_dac_max_err=0.6199 max_cm_error=0.3480 codes=[2, 7, 12, 15] |
| `169-two-period-sample-delay` | `FAIL_SIM_CORRECTNESS` | aout@14ns=0.0000 expected=0.1000 tol=0.0250 |
| `169-two-period-sample-delay` | `FAIL_SIM_CORRECTNESS` | aout@4ns=0.1000 expected=0.0000 tol=0.0250 |
| `169-two-period-sample-delay` | `FAIL_SIM_CORRECTNESS` | aout@14ns=0.0500 expected=0.1000 tol=0.0250 |
| `169-two-period-sample-delay` | `FAIL_SIM_CORRECTNESS` | aout@4ns=0.5000 expected=0.0000 tol=0.0250 |
| `169-two-period-sample-delay` | `FAIL_SIM_CORRECTNESS` | aout@14ns=0.0420 expected=0.1000 tol=0.0250 |
| `170-clocked-four-input-mux` | `FAIL_SIM_CORRECTNESS` | dout@4ns=0.0000 expected=0.1500 tol=0.0250 |
| `170-clocked-four-input-mux` | `FAIL_SIM_CORRECTNESS` | dout@4ns=0.0000 expected=0.1500 tol=0.0250 |
| `170-clocked-four-input-mux` | `FAIL_SIM_CORRECTNESS` | dout@14ns=0.6500 expected=0.3500 tol=0.0250 |
| `170-clocked-four-input-mux` | `FAIL_SIM_CORRECTNESS` | dout@24ns=0.1500 expected=0.6500 tol=0.0250 |
| `170-clocked-four-input-mux` | `FAIL_SIM_CORRECTNESS` | dout@4ns=0.0630 expected=0.1500 tol=0.0250 |
| `171-divide-by-eight-clock` | `FAIL_SIM_CORRECTNESS` | vout@2ns=0.0000 expected=0.9000 tol=0.0800 |
| `171-divide-by-eight-clock` | `FAIL_SIM_CORRECTNESS` | vout@6ns=0.0000 expected=0.9000 tol=0.0800 |
| `171-divide-by-eight-clock` | `FAIL_SIM_CORRECTNESS` | vout@4ns=0.0000 expected=0.9000 tol=0.0800 |
| `171-divide-by-eight-clock` | `FAIL_SIM_CORRECTNESS` | vout@8ns=0.0000 expected=0.9000 tol=0.0800 |
| `171-divide-by-eight-clock` | `FAIL_SIM_CORRECTNESS` | vout@2ns=0.3780 expected=0.9000 tol=0.0800 |
| `172-flash-thermometer-centered-sum` | `FAIL_SIM_CORRECTNESS` | checked=62 max_error=0.45000 |
| `172-flash-thermometer-centered-sum` | `FAIL_SIM_CORRECTNESS` | checked=62 max_error=0.10000 |
| `172-flash-thermometer-centered-sum` | `FAIL_SIM_CORRECTNESS` | checked=62 max_error=0.05000 |
| `172-flash-thermometer-centered-sum` | `FAIL_SIM_CORRECTNESS` | checked=62 max_error=0.45000 |
| `172-flash-thermometer-centered-sum` | `FAIL_SIM_CORRECTNESS` | checked=62 max_error=0.26100 |
| `173-weighted-sar-decoder-9b` | `FAIL_SIM_CORRECTNESS` | aout7b@5ns=0.0000 expected=-0.4963 tol=0.0100 |
| `173-weighted-sar-decoder-9b` | `FAIL_SIM_CORRECTNESS` | aout7b@5ns=0.0000 expected=-0.4963 tol=0.0100 |
| `173-weighted-sar-decoder-9b` | `FAIL_SIM_CORRECTNESS` | aout7b@5ns=-0.2610 expected=-0.4963 tol=0.0100 |
| `173-weighted-sar-decoder-9b` | `FAIL_SIM_CORRECTNESS` | aout7b@5ns=-0.5273 expected=-0.4963 tol=0.0100 |
| `173-weighted-sar-decoder-9b` | `FAIL_SIM_CORRECTNESS` | aout7b@5ns=-0.2085 expected=-0.4963 tol=0.0100 |
| `174-control-word-encoder-7b` | `FAIL_SIM_CORRECTNESS` | d0@5ns=0.0000 expected=0.9000 tol=0.0800 |
| `174-control-word-encoder-7b` | `FAIL_SIM_CORRECTNESS` | d0@5ns=0.0000 expected=0.9000 tol=0.0800 |
| `174-control-word-encoder-7b` | `FAIL_SIM_CORRECTNESS` | d0@5ns=0.0000 expected=0.9000 tol=0.0800 |
| `174-control-word-encoder-7b` | `FAIL_SIM_CORRECTNESS` | d0@5ns=0.4500 expected=0.9000 tol=0.0800 |
| `174-control-word-encoder-7b` | `FAIL_SIM_CORRECTNESS` | d0@5ns=0.3780 expected=0.9000 tol=0.0800 |
| `175-four-channel-edge-sampler` | `FAIL_SIM_CORRECTNESS` | vout0@4ns=0.0000 expected=0.1000 tol=0.0250 |
| `175-four-channel-edge-sampler` | `FAIL_SIM_CORRECTNESS` | vout0@4ns=0.0500 expected=0.1000 tol=0.0250 |
| `175-four-channel-edge-sampler` | `FAIL_SIM_CORRECTNESS` | vout0@4ns=0.2000 expected=0.1000 tol=0.0250 |
| `175-four-channel-edge-sampler` | `FAIL_SIM_CORRECTNESS` | vout3@4ns=0.0000 expected=0.4000 tol=0.0250 |
| `175-four-channel-edge-sampler` | `FAIL_SIM_CORRECTNESS` | vout0@4ns=0.0420 expected=0.1000 tol=0.0250 |
| `176-dual-modulus-divider-16-17` | `FAIL_SIM_CORRECTNESS` | fout@32ns=0.0000 expected=1.0000 tol=0.0800 |
| `176-dual-modulus-divider-16-17` | `FAIL_SIM_CORRECTNESS` | fout@64ns=1.0000 expected=0.0000 tol=0.0800 |
| `176-dual-modulus-divider-16-17` | `FAIL_SIM_CORRECTNESS` | fout@32ns=0.0000 expected=1.0000 tol=0.0800 |
| `176-dual-modulus-divider-16-17` | `FAIL_SIM_CORRECTNESS` | fout@48ns=0.0000 expected=1.0000 tol=0.0800 |
| `176-dual-modulus-divider-16-17` | `FAIL_SIM_CORRECTNESS` | fout@32ns=0.4200 expected=1.0000 tol=0.0800 |
| `177-sar-5bit-serial-decoder` | `FAIL_SIM_CORRECTNESS` | published=3 max_error=0.50000 |
| `177-sar-5bit-serial-decoder` | `FAIL_SIM_CORRECTNESS` | published=3 max_error=0.02218 |
| `177-sar-5bit-serial-decoder` | `FAIL_SIM_CORRECTNESS` | published=3 max_error=0.29032 |
| `177-sar-5bit-serial-decoder` | `FAIL_SIM_CORRECTNESS` | published=3 max_error=0.50000 |
| `177-sar-5bit-serial-decoder` | `FAIL_SIM_CORRECTNESS` | published=3 max_error=0.29000 |
| `178-cyclic-decoder-12bit` | `FAIL_SIM_CORRECTNESS` | dout@4ns=0.0000 expected=-0.5000 tol=0.0200 |
| `178-cyclic-decoder-12bit` | `FAIL_SIM_CORRECTNESS` | dout@4ns=-0.2500 expected=-0.5000 tol=0.0200 |
| `178-cyclic-decoder-12bit` | `FAIL_SIM_CORRECTNESS` | dout@14ns=0.3332 expected=-0.1667 tol=0.0200 |
| `178-cyclic-decoder-12bit` | `FAIL_SIM_CORRECTNESS` | dout@4ns=0.0000 expected=-0.5000 tol=0.0200 |
| `178-cyclic-decoder-12bit` | `FAIL_SIM_CORRECTNESS` | dout@4ns=-0.2100 expected=-0.5000 tol=0.0200 |
| `179-flash-8level-sum-delay` | `FAIL_SIM_CORRECTNESS` | checked=5 max_sum_error=1.00000 max_delay_error=1.00000 |
| `179-flash-8level-sum-delay` | `FAIL_SIM_CORRECTNESS` | checked=5 max_sum_error=0.25000 max_delay_error=0.25000 |
| `179-flash-8level-sum-delay` | `FAIL_SIM_CORRECTNESS` | checked=5 max_sum_error=0.00000 max_delay_error=0.75000 |
| `179-flash-8level-sum-delay` | `FAIL_SIM_CORRECTNESS` | checked=5 max_sum_error=1.00000 max_delay_error=1.00000 |
| `179-flash-8level-sum-delay` | `FAIL_SIM_CORRECTNESS` | checked=5 max_sum_error=0.58000 max_delay_error=0.58000 |
| `180-flash-sum8-fraction` | `FAIL_SIM_CORRECTNESS` | dout@14ns=0.0000 expected=0.3750 tol=0.0250 |
| `180-flash-sum8-fraction` | `FAIL_SIM_CORRECTNESS` | dout@14ns=0.7500 expected=0.3750 tol=0.0250 |
| `180-flash-sum8-fraction` | `FAIL_SIM_CORRECTNESS` | dout@24ns=0.5000 expected=0.6250 tol=0.0250 |
| `180-flash-sum8-fraction` | `FAIL_SIM_CORRECTNESS` | dout@4ns=0.1000 expected=0.0000 tol=0.0250 |
| `180-flash-sum8-fraction` | `FAIL_SIM_CORRECTNESS` | dout@14ns=0.1575 expected=0.3750 tol=0.0250 |
| `181-two-channel-sample-demux` | `FAIL_SIM_CORRECTNESS` | vout@4ns=0.0000 expected=0.1000 tol=0.0250 |
| `181-two-channel-sample-demux` | `FAIL_SIM_CORRECTNESS` | vout@4ns=0.2000 expected=0.1000 tol=0.0250 |
| `181-two-channel-sample-demux` | `FAIL_SIM_CORRECTNESS` | vout@14ns=0.3000 expected=0.4000 tol=0.0250 |
| `181-two-channel-sample-demux` | `FAIL_SIM_CORRECTNESS` | vout@4ns=0.0500 expected=0.1000 tol=0.0250 |
| `181-two-channel-sample-demux` | `FAIL_SIM_CORRECTNESS` | vout@4ns=0.0420 expected=0.1000 tol=0.0250 |
| `182-differential-dac-calc-6b` | `FAIL_SIM_CORRECTNESS` | voutp@5ns=0.0000 expected=0.5777 tol=0.0250 |
| `182-differential-dac-calc-6b` | `FAIL_SIM_CORRECTNESS` | voutp@5ns=0.9223 expected=0.5777 tol=0.0250 |
| `182-differential-dac-calc-6b` | `FAIL_SIM_CORRECTNESS` | voutp@5ns=0.4340 expected=0.5777 tol=0.0250 |
| `182-differential-dac-calc-6b` | `FAIL_SIM_CORRECTNESS` | voutp@5ns=0.2889 expected=0.5777 tol=0.0250 |
| `182-differential-dac-calc-6b` | `FAIL_SIM_CORRECTNESS` | voutp@5ns=0.2426 expected=0.5777 tol=0.0250 |
| `183-flash-adc-threshold-taps` | `FAIL_SIM_CORRECTNESS` | tap_checks=42 max_error=0.90000 |
| `183-flash-adc-threshold-taps` | `FAIL_SIM_CORRECTNESS` | tap_checks=42 max_error=0.90000 |
| `183-flash-adc-threshold-taps` | `FAIL_SIM_CORRECTNESS` | tap_checks=42 max_error=0.90000 |
| `183-flash-adc-threshold-taps` | `FAIL_SIM_CORRECTNESS` | tap_checks=42 max_error=0.45000 |
| `183-flash-adc-threshold-taps` | `FAIL_SIM_CORRECTNESS` | tap_checks=42 max_error=0.52200 |
| `184-divide-by-two-toggle` | `FAIL_SIM_CORRECTNESS` | clkout@2ns=0.0000 expected=0.9000 tol=0.0800 |
| `184-divide-by-two-toggle` | `FAIL_SIM_CORRECTNESS` | clkout@5ns=0.9000 expected=0.0000 tol=0.0800 |
| `184-divide-by-two-toggle` | `FAIL_SIM_CORRECTNESS` | clkout@2ns=0.0000 expected=0.9000 tol=0.0800 |
| `184-divide-by-two-toggle` | `FAIL_SIM_CORRECTNESS` | clkout@2ns=0.4500 expected=0.9000 tol=0.0800 |
| `184-divide-by-two-toggle` | `FAIL_SIM_CORRECTNESS` | clkout@2ns=0.3780 expected=0.9000 tol=0.0800 |
| `185-dac-5v-weighted-7b` | `FAIL_SIM_CORRECTNESS` | vout@5ns=0.0000 expected=1.0000 tol=0.0400 |
| `185-dac-5v-weighted-7b` | `FAIL_SIM_CORRECTNESS` | vout@5ns=0.5000 expected=1.0000 tol=0.0400 |
| `185-dac-5v-weighted-7b` | `FAIL_SIM_CORRECTNESS` | vout@5ns=0.5000 expected=1.0000 tol=0.0400 |
| `185-dac-5v-weighted-7b` | `FAIL_SIM_CORRECTNESS` | vout@5ns=0.0000 expected=1.0000 tol=0.0400 |
| `185-dac-5v-weighted-7b` | `FAIL_SIM_CORRECTNESS` | vout@5ns=0.4200 expected=1.0000 tol=0.0400 |
| `186-folded-flash-dac-4b` | `FAIL_SIM_CORRECTNESS` | checked=4 max_error=0.81250 |
| `186-folded-flash-dac-4b` | `FAIL_SIM_CORRECTNESS` | checked=5 max_error=0.37500 |
| `186-folded-flash-dac-4b` | `FAIL_SIM_CORRECTNESS` | checked=5 max_error=0.81250 |
| `186-folded-flash-dac-4b` | `FAIL_SIM_CORRECTNESS` | checked=5 max_error=1.12500 |
| `186-folded-flash-dac-4b` | `FAIL_SIM_CORRECTNESS` | checked=5 max_error=0.47125 |
| `187-ref-flash-8level-decoder` | `FAIL_SIM_CORRECTNESS` | checked=5 max_dout_error=0.62500 max_res_error=0.42500 |
| `187-ref-flash-8level-decoder` | `FAIL_SIM_CORRECTNESS` | checked=5 max_dout_error=0.62500 max_res_error=0.00000 |
| `187-ref-flash-8level-decoder` | `FAIL_SIM_CORRECTNESS` | checked=5 max_dout_error=0.00000 max_res_error=0.50000 |
| `187-ref-flash-8level-decoder` | `FAIL_SIM_CORRECTNESS` | checked=5 max_dout_error=0.37500 max_res_error=0.37500 |
| `187-ref-flash-8level-decoder` | `FAIL_SIM_CORRECTNESS` | checked=5 max_dout_error=0.36250 max_res_error=0.00000 |
| `188-ref-flash-15level-decoder` | `FAIL_SIM_CORRECTNESS` | dout@14ns=0.0000 expected=0.3333 tol=0.0250 |
| `188-ref-flash-15level-decoder` | `FAIL_SIM_CORRECTNESS` | dout@14ns=0.6250 expected=0.3333 tol=0.0250 |
| `188-ref-flash-15level-decoder` | `FAIL_SIM_CORRECTNESS` | dout@34ns=0.6667 expected=1.0000 tol=0.0250 |
| `188-ref-flash-15level-decoder` | `FAIL_SIM_CORRECTNESS` | dout@14ns=0.1667 expected=0.3333 tol=0.0250 |
| `188-ref-flash-15level-decoder` | `FAIL_SIM_CORRECTNESS` | dout@14ns=0.1400 expected=0.3333 tol=0.0250 |
| `189-divide-by-8-9-switch` | `FAIL_SIM_CORRECTNESS` | out@2ns=0.0000 expected=1.2000 tol=0.0800 |
| `189-divide-by-8-9-switch` | `FAIL_SIM_CORRECTNESS` | out@2ns=0.6000 expected=1.2000 tol=0.0800 |
| `189-divide-by-8-9-switch` | `FAIL_SIM_CORRECTNESS` | out@2ns=0.0000 expected=1.2000 tol=0.0800 |
| `189-divide-by-8-9-switch` | `FAIL_SIM_CORRECTNESS` | out@28ns=0.0000 expected=1.2000 tol=0.0800 |
| `189-divide-by-8-9-switch` | `FAIL_SIM_CORRECTNESS` | out@2ns=0.5040 expected=1.2000 tol=0.0800 |
| `190-dac-restore-10bit-offset` | `FAIL_SIM_CORRECTNESS` | vout@5ns=0.0000 expected=-0.9554 tol=0.0250 |
| `190-dac-restore-10bit-offset` | `FAIL_SIM_CORRECTNESS` | vout@5ns=-0.8991 expected=-0.9554 tol=0.0250 |
| `190-dac-restore-10bit-offset` | `FAIL_SIM_CORRECTNESS` | vout@15ns=0.2065 expected=0.3190 tol=0.0250 |
| `190-dac-restore-10bit-offset` | `FAIL_SIM_CORRECTNESS` | vout@5ns=-1.0107 expected=-0.9554 tol=0.0250 |
| `190-dac-restore-10bit-offset` | `FAIL_SIM_CORRECTNESS` | vout@5ns=-0.4013 expected=-0.9554 tol=0.0250 |
| `191-dac-8bit-ideal-scalar` | `FAIL_SIM_CORRECTNESS` | vout@15ns=0.0000 expected=0.3320 tol=0.0200 |
| `191-dac-8bit-ideal-scalar` | `FAIL_SIM_CORRECTNESS` | vout@15ns=0.8281 expected=0.3320 tol=0.0200 |
| `191-dac-8bit-ideal-scalar` | `FAIL_SIM_CORRECTNESS` | vout@15ns=0.6641 expected=0.3320 tol=0.0200 |
| `191-dac-8bit-ideal-scalar` | `FAIL_SIM_CORRECTNESS` | vout@15ns=0.1660 expected=0.3320 tol=0.0200 |
| `191-dac-8bit-ideal-scalar` | `FAIL_SIM_CORRECTNESS` | vout@15ns=0.1395 expected=0.3320 tol=0.0200 |
| `192-flash-data-align-pipeline` | `FAIL_SIM_CORRECTNESS` | dout0@26ns=0.0000 expected=1.0000 tol=0.0800 |
| `192-flash-data-align-pipeline` | `FAIL_SIM_CORRECTNESS` | dout0@20ns=1.0000 expected=0.0000 tol=0.0800 |
| `192-flash-data-align-pipeline` | `FAIL_SIM_CORRECTNESS` | dout0@32ns=0.0000 expected=1.0000 tol=0.0800 |
| `192-flash-data-align-pipeline` | `FAIL_SIM_CORRECTNESS` | dout0@32ns=0.0000 expected=1.0000 tol=0.0800 |
| `192-flash-data-align-pipeline` | `FAIL_SIM_CORRECTNESS` | dout0@26ns=0.4200 expected=1.0000 tol=0.0800 |
| `193-cyclic-decoder-10b` | `FAIL_SIM_CORRECTNESS` | published=2 half_weight_seen=True max_error=0.21457 |
| `193-cyclic-decoder-10b` | `FAIL_SIM_CORRECTNESS` | published=2 half_weight_seen=True max_error=0.35728 |
| `193-cyclic-decoder-10b` | `FAIL_SIM_CORRECTNESS` | published=2 half_weight_seen=True max_error=0.28592 |
| `193-cyclic-decoder-10b` | `FAIL_SIM_CORRECTNESS` | published=2 half_weight_seen=True max_error=0.50000 |
| `193-cyclic-decoder-10b` | `FAIL_SIM_CORRECTNESS` | published=2 half_weight_seen=True max_error=0.12445 |
| `194-ideal-adc-out-7bits` | `FAIL_SIM_CORRECTNESS` | dout@15ns=0.0000 expected=0.6641 tol=0.0200 |
| `194-ideal-adc-out-7bits` | `FAIL_SIM_CORRECTNESS` | dout@15ns=0.1641 expected=0.6641 tol=0.0200 |
| `194-ideal-adc-out-7bits` | `FAIL_SIM_CORRECTNESS` | dout@5ns=0.1250 expected=0.0000 tol=0.0200 |
| `194-ideal-adc-out-7bits` | `FAIL_SIM_CORRECTNESS` | dout@15ns=0.3320 expected=0.6641 tol=0.0200 |
| `194-ideal-adc-out-7bits` | `FAIL_SIM_CORRECTNESS` | dout@15ns=0.2789 expected=0.6641 tol=0.0200 |
| `195-va-lx-adc-ideal-4b` | `FAIL_SIM_CORRECTNESS` | va_lx_adc_max_err=1.0000 codes=[0, 7, 10, 15] |
| `195-va-lx-adc-ideal-4b` | `FAIL_SIM_CORRECTNESS` | va_lx_adc_max_err=1.0000 codes=[0, 7, 10, 15] |
| `195-va-lx-adc-ideal-4b` | `FAIL_SIM_CORRECTNESS` | va_lx_adc_max_err=1.0000 codes=[0, 7, 10, 15] |
| `195-va-lx-adc-ideal-4b` | `FAIL_SIM_CORRECTNESS` | va_lx_adc_max_err=1.0000 codes=[0, 7, 10, 15] |
| `195-va-lx-adc-ideal-4b` | `FAIL_SIM_CORRECTNESS` | va_lx_adc_max_err=0.5800 codes=[0, 7, 10, 15] |
| `196-va-lx-dac-ideal-4b` | `FAIL_SIM_CORRECTNESS` | aout@15ns=0.0000 expected=0.5625 tol=0.0300 |
| `196-va-lx-dac-ideal-4b` | `FAIL_SIM_CORRECTNESS` | aout@15ns=0.3125 expected=0.5625 tol=0.0300 |
| `196-va-lx-dac-ideal-4b` | `FAIL_SIM_CORRECTNESS` | aout@25ns=1.1250 expected=1.5750 tol=0.0300 |
| `196-va-lx-dac-ideal-4b` | `FAIL_SIM_CORRECTNESS` | aout@15ns=0.4500 expected=0.5625 tol=0.0300 |
| `196-va-lx-dac-ideal-4b` | `FAIL_SIM_CORRECTNESS` | aout@15ns=0.2362 expected=0.5625 tol=0.0300 |
| `197-l1-dac-4b-bipolar` | `FAIL_SIM_CORRECTNESS` | aout@5ns=0.0000 expected=-1.0000 tol=0.0300 |
| `197-l1-dac-4b-bipolar` | `FAIL_SIM_CORRECTNESS` | aout@5ns=0.0000 expected=-1.0000 tol=0.0300 |
| `197-l1-dac-4b-bipolar` | `FAIL_SIM_CORRECTNESS` | aout@5ns=1.0000 expected=-1.0000 tol=0.0300 |
| `197-l1-dac-4b-bipolar` | `FAIL_SIM_CORRECTNESS` | aout@25ns=0.2500 expected=0.7500 tol=0.0300 |
| `197-l1-dac-4b-bipolar` | `FAIL_SIM_CORRECTNESS` | aout@5ns=-0.4200 expected=-1.0000 tol=0.0300 |
| `198-l2-cdac-4b-residue` | `FAIL_SIM_CORRECTNESS` | vres@2ns=0.0000 expected=0.1000 tol=0.0300 |
| `198-l2-cdac-4b-residue` | `FAIL_SIM_CORRECTNESS` | vres@4ns=0.3500 expected=0.6000 tol=0.0300 |
| `198-l2-cdac-4b-residue` | `FAIL_SIM_CORRECTNESS` | vres@6ns=0.3500 expected=0.8500 tol=0.0300 |
| `198-l2-cdac-4b-residue` | `FAIL_SIM_CORRECTNESS` | vres@8ns=0.8500 expected=0.9750 tol=0.0300 |
| `198-l2-cdac-4b-residue` | `FAIL_SIM_CORRECTNESS` | vres@2ns=0.0420 expected=0.1000 tol=0.0300 |
| `199-ideal-clkmux-8channel` | `FAIL_SIM_CORRECTNESS` | out@2ns=0.0000 expected=0.2000 tol=0.0800 |
| `199-ideal-clkmux-8channel` | `FAIL_SIM_CORRECTNESS` | out@14ns=0.1000 expected=0.8000 tol=0.0800 |
| `199-ideal-clkmux-8channel` | `FAIL_SIM_CORRECTNESS` | out@2ns=0.1000 expected=0.2000 tol=0.0800 |
| `199-ideal-clkmux-8channel` | `FAIL_SIM_CORRECTNESS` | count_x@2ns=0.5000 expected=1.0000 tol=0.0800 |
| `199-ideal-clkmux-8channel` | `FAIL_SIM_CORRECTNESS` | out@2ns=0.0840 expected=0.2000 tol=0.0800 |
| `200-dac-ideal-4b-offset` | `FAIL_SIM_CORRECTNESS` | offset_dac_max_err=0.6609 codes=[2, 7, 12, 15] |
| `200-dac-ideal-4b-offset` | `FAIL_SIM_CORRECTNESS` | offset_dac_max_err=0.2390 codes=[2, 7, 12, 15] |
| `200-dac-ideal-4b-offset` | `FAIL_SIM_CORRECTNESS` | offset_dac_max_err=0.0469 codes=[2, 7, 12, 15] |
| `200-dac-ideal-4b-offset` | `FAIL_SIM_CORRECTNESS` | offset_dac_max_err=0.1969 codes=[2, 7, 12, 15] |
| `200-dac-ideal-4b-offset` | `FAIL_SIM_CORRECTNESS` | offset_dac_max_err=0.3833 codes=[2, 7, 12, 15] |
| `201-linear-pfd-gain` | `FAIL_SIM_CORRECTNESS` | out@5ns=0.0000 expected=0.2030 tol=0.0200 |
| `201-linear-pfd-gain` | `FAIL_SIM_CORRECTNESS` | out@5ns=-0.2030 expected=0.2030 tol=0.0200 |
| `201-linear-pfd-gain` | `FAIL_SIM_CORRECTNESS` | out@5ns=0.1000 expected=0.2030 tol=0.0200 |
| `201-linear-pfd-gain` | `FAIL_SIM_CORRECTNESS` | out@5ns=0.4060 expected=0.2030 tol=0.0200 |
| `201-linear-pfd-gain` | `FAIL_SIM_CORRECTNESS` | out@5ns=0.0853 expected=0.2030 tol=0.0200 |
| `202-l2-cmp-ideal-clocked` | `FAIL_SIM_CORRECTNESS` | dcmpp@1.3ns=0.0000 expected=0.9000 tol=0.0800 |
| `202-l2-cmp-ideal-clocked` | `FAIL_SIM_CORRECTNESS` | dcmpp@1.3ns=0.0000 expected=0.9000 tol=0.0800 |
| `202-l2-cmp-ideal-clocked` | `FAIL_SIM_CORRECTNESS` | dcmpp@12ns=0.0000 expected=0.9000 tol=0.0800 |
| `202-l2-cmp-ideal-clocked` | `FAIL_SIM_CORRECTNESS` | dcmpp@1.3ns=0.4500 expected=0.9000 tol=0.0800 |
| `202-l2-cmp-ideal-clocked` | `FAIL_SIM_CORRECTNESS` | dcmpp@1.3ns=0.3780 expected=0.9000 tol=0.0800 |
| `203-comparator-offset-driver` | `FAIL_SIM_CORRECTNESS` | diff@1.775ns=0.00000 expected=0.10000 cm@1.775ns=0.00000 expected=0.45000 diff@7.775ns=0.00000 expected=0.15000 cm@7.775ns=0.00000 expected=0.45000 diff@13.775ns=0.00000 expected=0.12500 |
| `203-comparator-offset-driver` | `FAIL_SIM_CORRECTNESS` | diff@7.775ns=0.20000 expected=0.15000 diff@13.775ns=0.10000 expected=0.12500 diff@19.775ns=0.20000 expected=0.13750 diff@25.775ns=0.10000 expected=0.13125 diff@31.775ns=0.00000 expected=0.12813 |
| `203-comparator-offset-driver` | `FAIL_SIM_CORRECTNESS` | diff@1.775ns=-0.10000 expected=0.10000 diff@7.775ns=-0.15000 expected=0.15000 diff@13.775ns=-0.12500 expected=0.12500 diff@19.775ns=-0.13750 expected=0.13750 diff@25.775ns=-0.13125 expected=0.13125 |
| `203-comparator-offset-driver` | `FAIL_SIM_CORRECTNESS` | diff@1.775ns=0.20000 expected=0.10000 diff@7.775ns=0.30000 expected=0.15000 diff@13.775ns=0.25000 expected=0.12500 diff@19.775ns=0.27500 expected=0.13750 diff@25.775ns=0.26250 expected=0.13125 |
| `203-comparator-offset-driver` | `FAIL_SIM_CORRECTNESS` | diff@1.775ns=0.04200 expected=0.10000 cm@1.775ns=0.18900 expected=0.45000 diff@7.775ns=0.06300 expected=0.15000 cm@7.775ns=0.18900 expected=0.45000 diff@13.775ns=0.05250 expected=0.12500 |
| `204-pipe-2lane-edge-align` | `FAIL_SIM_CORRECTNESS` | dout_after_din1_edge@2.025ns=0.0000 expected=0.2500 dout_after_din2_edge@2.825ns=0.0000 expected=-0.3000 dout_after_din1_edge@9.025ns=0.0000 expected=0.6500 dout_after_din2_edge@10.225ns=0.0000 expected=0.1500 |
| `204-pipe-2lane-edge-align` | `FAIL_SIM_CORRECTNESS` | dout_after_din1_edge@2.025ns=-0.3000 expected=0.2500 dout_after_din2_edge@2.825ns=0.2500 expected=-0.3000 dout_after_din1_edge@9.025ns=0.1500 expected=0.6500 dout_after_din2_edge@10.225ns=0.6500 expected=0.1500 |
| `204-pipe-2lane-edge-align` | `FAIL_SIM_CORRECTNESS` | dout_after_din2_edge@2.825ns=0.2500 expected=-0.3000 dout_after_din2_edge@10.225ns=0.6500 expected=0.1500 dout_after_din2_edge@17.425ns=-0.1000 expected=0.8500 dout_after_din2_edge@25.525ns=0.4500 expected=-0.0500 |
| `204-pipe-2lane-edge-align` | `FAIL_SIM_CORRECTNESS` | dout_after_din1_edge@2.025ns=0.1250 expected=0.2500 dout_after_din2_edge@2.825ns=-0.1500 expected=-0.3000 dout_after_din1_edge@9.025ns=0.3250 expected=0.6500 dout_after_din2_edge@10.225ns=0.0750 expected=0.1500 |
| `204-pipe-2lane-edge-align` | `FAIL_SIM_CORRECTNESS` | dout_after_din1_edge@2.025ns=0.1050 expected=0.2500 dout_after_din2_edge@2.825ns=-0.1260 expected=-0.3000 dout_after_din1_edge@9.025ns=0.2730 expected=0.6500 dout_after_din2_edge@10.225ns=0.0630 expected=0.1500 |
| `205-dac-serial-accumulator` | `FAIL_SIM_CORRECTNESS` | out@2ns=0.0000 expected=-1.1000 tol=0.0350 |
| `205-dac-serial-accumulator` | `FAIL_SIM_CORRECTNESS` | out@14ns=0.4125 expected=-1.1000 tol=0.0350 |
| `205-dac-serial-accumulator` | `FAIL_SIM_CORRECTNESS` | out@4ns=-0.9625 expected=0.0000 tol=0.0350 |
| `205-dac-serial-accumulator` | `FAIL_SIM_CORRECTNESS` | out@2ns=0.0000 expected=-1.1000 tol=0.0350 |
| `205-dac-serial-accumulator` | `FAIL_SIM_CORRECTNESS` | out@2ns=-0.4620 expected=-1.1000 tol=0.0350 |
| `206-sar-sum-weighted-11b` | `FAIL_SIM_CORRECTNESS` | vout@5ns=0.0000 expected=-1.0000 tol=0.0200 |
| `206-sar-sum-weighted-11b` | `FAIL_SIM_CORRECTNESS` | vout@15ns=1.6289 expected=0.3145 tol=0.0200 |
| `206-sar-sum-weighted-11b` | `FAIL_SIM_CORRECTNESS` | vout@15ns=-0.6230 expected=0.3145 tol=0.0200 |
| `206-sar-sum-weighted-11b` | `FAIL_SIM_CORRECTNESS` | vout@5ns=0.0000 expected=-1.0000 tol=0.0200 |
| `206-sar-sum-weighted-11b` | `FAIL_SIM_CORRECTNESS` | vout@5ns=-0.4200 expected=-1.0000 tol=0.0200 |
| `207-iterative-isar-dac` | `FAIL_SIM_CORRECTNESS` | too_few_effective_updates=0 |
| `207-iterative-isar-dac` | `FAIL_SIM_CORRECTNESS` | wrong_update_direction@1.225ns diff=-0.2000 dcmp=0.000 wrong_update_direction@2.625ns diff=0.1000 dcmp=1.000 wrong_update_direction@4.025ns diff=-0.0500 dcmp=0.000 wrong_update_direction@5.425ns diff=-0.0250 dcmp=0.000 wrong_update_direction@6.825ns diff=0.0125 dcmp=1.000 |
| `207-iterative-isar-dac` | `FAIL_SIM_CORRECTNESS` | bad_halving_ratios=1.000,1.000,1.000,1.000 |
| `207-iterative-isar-dac` | `FAIL_SIM_CORRECTNESS` | bad_halving_ratios=0.250,0.250,0.250,0.250 |
| `207-iterative-isar-dac` | `FAIL_SIM_CORRECTNESS` | wrong_update_direction@1.225ns diff=-0.2000 dcmp=0.000 wrong_update_direction@2.625ns diff=0.1000 dcmp=1.000 wrong_update_direction@4.025ns diff=-0.0500 dcmp=0.000 wrong_update_direction@5.425ns diff=-0.0250 dcmp=0.000 wrong_update_direction@6.825ns diff=0.0125 dcmp=1.000 |
| `208-offset-bisection-driver` | `FAIL_SIM_CORRECTNESS` | diff@2.275ns=0.00000 expected=0.01000 cm@2.275ns=0.00000 expected=0.48000 diff@4.775ns=0.00000 expected=0.02000 cm@4.775ns=0.00000 expected=0.48000 diff@7.275ns=0.00000 expected=0.01500 |
| `208-offset-bisection-driver` | `FAIL_SIM_CORRECTNESS` | diff@7.275ns=0.01000 expected=0.01500 diff@9.775ns=0.00000 expected=0.01000 diff@14.775ns=0.00000 expected=0.01125 |
| `208-offset-bisection-driver` | `FAIL_SIM_CORRECTNESS` | diff@2.275ns=-0.00500 expected=0.01000 diff@4.775ns=-0.01000 expected=0.02000 diff@7.275ns=-0.00750 expected=0.01500 diff@9.775ns=-0.00500 expected=0.01000 diff@12.275ns=-0.00625 expected=0.01250 |
| `208-offset-bisection-driver` | `FAIL_SIM_CORRECTNESS` | diff@2.275ns=0.02000 expected=0.01000 diff@4.775ns=0.04000 expected=0.02000 diff@7.275ns=0.03000 expected=0.01500 diff@9.775ns=0.02000 expected=0.01000 diff@12.275ns=0.02500 expected=0.01250 |
| `208-offset-bisection-driver` | `FAIL_SIM_CORRECTNESS` | diff@2.275ns=0.00420 expected=0.01000 cm@2.275ns=0.20160 expected=0.48000 diff@4.775ns=0.00840 expected=0.02000 cm@4.775ns=0.20160 expected=0.48000 diff@7.275ns=0.00630 expected=0.01500 |
| `209-weighted-decoder-7b5` | `FAIL_SIM_CORRECTNESS` | checked=1974 max_weighted7b5_error=0.49816 worst_code=000000000 |
| `209-weighted-decoder-7b5` | `FAIL_SIM_CORRECTNESS` | checked=1974 max_weighted7b5_error=0.03114 worst_code=000000000 |
| `209-weighted-decoder-7b5` | `FAIL_SIM_CORRECTNESS` | checked=1974 max_weighted7b5_error=0.24908 worst_code=000000000 |
| `209-weighted-decoder-7b5` | `FAIL_SIM_CORRECTNESS` | checked=1974 max_weighted7b5_error=0.99265 worst_code=000000000 |
| `209-weighted-decoder-7b5` | `FAIL_SIM_CORRECTNESS` | checked=1974 max_weighted7b5_error=0.28893 worst_code=000000000 |
| `210-toggle-flip-flop` | `FAIL_SIM_CORRECTNESS` | vout_q@1.3ns=0.0000 expected=0.9000 tol=0.0400 |
| `210-toggle-flip-flop` | `FAIL_SIM_CORRECTNESS` | vout_q@3.3ns=0.9000 expected=0.0000 tol=0.0400 |
| `210-toggle-flip-flop` | `FAIL_SIM_CORRECTNESS` | vout_q@1.3ns=0.0000 expected=0.9000 tol=0.0400 |
| `210-toggle-flip-flop` | `FAIL_SIM_CORRECTNESS` | vout_qbar@0.8ns=0.0000 expected=0.9000 tol=0.0400 |
| `210-toggle-flip-flop` | `FAIL_SIM_CORRECTNESS` | vout_q@1.3ns=0.3780 expected=0.9000 tol=0.0400 |
| `211-sync-8b-dffs-v2` | `FAIL_SIM_CORRECTNESS` | do0@9.7ns=0.0000 expected=1.0000 tol=0.0800 |
| `211-sync-8b-dffs-v2` | `FAIL_SIM_CORRECTNESS` | do8@9.7ns=0.0000 expected=1.0000 tol=0.0800 |
| `211-sync-8b-dffs-v2` | `FAIL_SIM_CORRECTNESS` | do4@9.7ns=0.0000 expected=1.0000 tol=0.0800 |
| `211-sync-8b-dffs-v2` | `FAIL_SIM_CORRECTNESS` | do8@9.7ns=0.0000 expected=1.0000 tol=0.0800 |
| `211-sync-8b-dffs-v2` | `FAIL_SIM_CORRECTNESS` | do0@9.7ns=0.4200 expected=1.0000 tol=0.0800 |
| `212-onehot-progress-encoder` | `FAIL_SIM_CORRECTNESS` | sum@1.3ns=0.0000 expected=1.0000 tol=0.0800 |
| `212-onehot-progress-encoder` | `FAIL_SIM_CORRECTNESS` | sum@0.8ns=1.0000 expected=0.0000 tol=0.0800 |
| `212-onehot-progress-encoder` | `FAIL_SIM_CORRECTNESS` | sum@0.8ns=-1.0000 expected=0.0000 tol=0.0800 |
| `212-onehot-progress-encoder` | `FAIL_SIM_CORRECTNESS` | d4@16.3ns=0.0000 expected=1.0000 tol=0.0800 |
| `212-onehot-progress-encoder` | `FAIL_SIM_CORRECTNESS` | d0@1.3ns=0.4200 expected=1.0000 tol=0.0800 |
| `213-tdc-ideal-edge-delta` | `FAIL_SIM_CORRECTNESS` | vout@3ns=0.0000 expected=-0.3000 tol=0.0250 |
| `213-tdc-ideal-edge-delta` | `FAIL_SIM_CORRECTNESS` | vout@7ns=-0.6000 expected=0.6000 tol=0.0250 |
| `213-tdc-ideal-edge-delta` | `FAIL_SIM_CORRECTNESS` | vout@3ns=-0.6000 expected=-0.3000 tol=0.0250 |
| `213-tdc-ideal-edge-delta` | `FAIL_SIM_CORRECTNESS` | vout@3ns=-0.1500 expected=-0.3000 tol=0.0250 |
| `213-tdc-ideal-edge-delta` | `FAIL_SIM_CORRECTNESS` | vout@3ns=-0.1260 expected=-0.3000 tol=0.0250 |
| `214-foreground-cload-calibrator` | `FAIL_SIM_CORRECTNESS` | cvinp@0.5ns=0.0000 expected=0.8200 tol=0.0800 |
| `214-foreground-cload-calibrator` | `FAIL_SIM_CORRECTNESS` | dcp4@1.7ns=0.0000 expected=1.0000 tol=0.0800 |
| `214-foreground-cload-calibrator` | `FAIL_SIM_CORRECTNESS` | en@11.7ns=1.0000 expected=0.0000 tol=0.0800 |
| `214-foreground-cload-calibrator` | `FAIL_SIM_CORRECTNESS` | cvinp@0.5ns=0.1800 expected=0.8200 tol=0.0800 |
| `214-foreground-cload-calibrator` | `FAIL_SIM_CORRECTNESS` | cvinp@0.5ns=0.3444 expected=0.8200 tol=0.0800 |
| `215-pipe15-data-align` | `FAIL_SIM_CORRECTNESS` | do0@0.610ns=0.000 expected=0.900 delay=0 do1@2.210ns=0.000 expected=0.900 delay=0 do2@2.210ns=0.000 expected=0.900 delay=0 do3@2.210ns=0.000 expected=0.900 delay=1 do6@2.210ns=0.000 expected=0.900 delay=1 do0@3.810ns=0.000 expected=0.900 delay=0 |
| `215-pipe15-data-align` | `FAIL_SIM_CORRECTNESS` | do11@5.410ns=0.900 expected=0.000 delay=4 do14@5.410ns=0.900 expected=0.000 delay=4 do11@7.010ns=0.000 expected=0.900 delay=4 do12@7.010ns=0.900 expected=0.000 delay=4 do14@7.010ns=0.000 expected=0.900 delay=4 do12@8.610ns=0.000 expected=0.900 delay=4 |
| `215-pipe15-data-align` | `FAIL_SIM_CORRECTNESS` | do7@3.810ns=0.000 expected=0.900 delay=2 do8@5.410ns=0.000 expected=0.900 delay=2 do9@5.410ns=0.000 expected=0.900 delay=2 do10@5.410ns=0.000 expected=0.900 delay=2 do7@7.010ns=0.000 expected=0.900 delay=2 do7@10.210ns=0.000 expected=0.900 delay=2 |
| `215-pipe15-data-align` | `FAIL_SIM_CORRECTNESS` | do14@7.010ns=0.000 expected=0.900 delay=4 do14@10.210ns=0.000 expected=0.900 delay=4 |
| `215-pipe15-data-align` | `FAIL_SIM_CORRECTNESS` | do0@0.610ns=0.378 expected=0.900 delay=0 do1@2.210ns=0.378 expected=0.900 delay=0 do2@2.210ns=0.378 expected=0.900 delay=0 do3@2.210ns=0.378 expected=0.900 delay=1 do6@2.210ns=0.378 expected=0.900 delay=1 do0@3.810ns=0.378 expected=0.900 delay=0 |
| `216-clocked-mux4-sampler` | `FAIL_SIM_CORRECTNESS` | dout@1.3ns=0.0000 expected=0.1200 tol=0.0150 |
| `216-clocked-mux4-sampler` | `FAIL_SIM_CORRECTNESS` | dout@1.3ns=0.0000 expected=0.1200 tol=0.0150 |
| `216-clocked-mux4-sampler` | `FAIL_SIM_CORRECTNESS` | dout@1.3ns=0.3400 expected=0.1200 tol=0.0150 |
| `216-clocked-mux4-sampler` | `FAIL_SIM_CORRECTNESS` | dout@1.3ns=0.0600 expected=0.1200 tol=0.0150 |
| `216-clocked-mux4-sampler` | `FAIL_SIM_CORRECTNESS` | dout@1.3ns=0.0504 expected=0.1200 tol=0.0150 |
| `217-dac7-code-generator` | `FAIL_SIM_CORRECTNESS` | din0@1.3ns=0.0000 expected=0.9000 tol=0.0800 |
| `217-dac7-code-generator` | `FAIL_SIM_CORRECTNESS` | din4@8.3ns=0.9000 expected=0.0000 tol=0.0800 |
| `217-dac7-code-generator` | `FAIL_SIM_CORRECTNESS` | din0@1.3ns=0.0000 expected=0.9000 tol=0.0800 |
| `217-dac7-code-generator` | `FAIL_SIM_CORRECTNESS` | din0@1.3ns=0.4500 expected=0.9000 tol=0.0800 |
| `217-dac7-code-generator` | `FAIL_SIM_CORRECTNESS` | din0@1.3ns=0.3780 expected=0.9000 tol=0.0800 |
| `218-foreground-rdac-calibrator` | `FAIL_SIM_CORRECTNESS` | dc6@0.5ns=0.0000 expected=1.0000 tol=0.0800 |
| `218-foreground-rdac-calibrator` | `FAIL_SIM_CORRECTNESS` | dc6@0.5ns=0.0000 expected=1.0000 tol=0.0800 |
| `218-foreground-rdac-calibrator` | `FAIL_SIM_CORRECTNESS` | dc6@11.7ns=0.0000 expected=1.0000 tol=0.0800 |
| `218-foreground-rdac-calibrator` | `FAIL_SIM_CORRECTNESS` | en@13.7ns=1.0000 expected=0.0000 tol=0.0800 |
| `218-foreground-rdac-calibrator` | `FAIL_SIM_CORRECTNESS` | dc6@0.5ns=0.4200 expected=1.0000 tol=0.0800 |
| `219-offset-rdac-search-flow` | `FAIL_SIM_CORRECTNESS` | dc6@0.5ns=0.0000 expected=1.0000 tol=0.0800 |
| `219-offset-rdac-search-flow` | `FAIL_SIM_CORRECTNESS` | vinp@0.5ns=0.0688 expected=0.3344 tol=0.0800 |
| `219-offset-rdac-search-flow` | `FAIL_SIM_CORRECTNESS` | dc6@7.7ns=0.0000 expected=1.0000 tol=0.0800 |
| `219-offset-rdac-search-flow` | `FAIL_SIM_CORRECTNESS` | vrefp@0.5ns=0.6000 expected=0.3344 tol=0.0800 |
| `219-offset-rdac-search-flow` | `FAIL_SIM_CORRECTNESS` | dc6@0.5ns=0.4200 expected=1.0000 tol=0.0800 |
| `220-spi-shift-mux` | `FAIL_SIM_CORRECTNESS` | out7@0.2ns=0.0000 expected=0.9000 tol=0.0800 |
| `220-spi-shift-mux` | `FAIL_SIM_CORRECTNESS` | out7@2.3ns=0.0000 expected=0.9000 tol=0.0800 |
| `220-spi-shift-mux` | `FAIL_SIM_CORRECTNESS` | out7@1.3ns=0.9000 expected=0.0000 tol=0.0800 |
| `220-spi-shift-mux` | `FAIL_SIM_CORRECTNESS` | sdo@0.2ns=0.0000 expected=0.9000 tol=0.0800 |
| `220-spi-shift-mux` | `FAIL_SIM_CORRECTNESS` | out7@0.2ns=0.3780 expected=0.9000 tol=0.0800 |
| `221-dff-set-reset-hold` | `FAIL_SIM_CORRECTNESS` | qp@1.3ns=0.0000 expected=0.9000 tol=0.0800 |
| `221-dff-set-reset-hold` | `FAIL_SIM_CORRECTNESS` | qp@1.3ns=0.4500 expected=0.9000 tol=0.0800 |
| `221-dff-set-reset-hold` | `FAIL_SIM_CORRECTNESS` | qp@6.3ns=0.9000 expected=0.0000 tol=0.0800 |
| `221-dff-set-reset-hold` | `FAIL_SIM_CORRECTNESS` | qp@1.3ns=0.0000 expected=0.9000 tol=0.0800 |
| `221-dff-set-reset-hold` | `FAIL_SIM_CORRECTNESS` | qp@1.3ns=0.3780 expected=0.9000 tol=0.0800 |
| `222-sarfend-logic-4b` | `FAIL_SIM_CORRECTNESS` | clkc@1.8ns=0.0000 expected=1.0000 tol=0.0800 |
| `222-sarfend-logic-4b` | `FAIL_SIM_CORRECTNESS` | dp4@2.4ns=0.0000 expected=1.0000 tol=0.0800 |
| `222-sarfend-logic-4b` | `FAIL_SIM_CORRECTNESS` | clkc@1.8ns=0.5000 expected=1.0000 tol=0.0800 |
| `222-sarfend-logic-4b` | `FAIL_SIM_CORRECTNESS` | dout3@1.2ns=1.0000 expected=0.0000 tol=0.0800 |
| `222-sarfend-logic-4b` | `FAIL_SIM_CORRECTNESS` | clkc@1.8ns=0.4200 expected=1.0000 tol=0.0800 |
| `223-adc-sample-clock-sequencer` | `FAIL_SIM_CORRECTNESS` | rst@0.1ns=0.0000 expected=0.9000 tol=0.0800 |
| `223-adc-sample-clock-sequencer` | `FAIL_SIM_CORRECTNESS` | conv@2.6ns=0.4500 expected=0.9000 tol=0.0800 |
| `223-adc-sample-clock-sequencer` | `FAIL_SIM_CORRECTNESS` | s@0.7ns=0.4500 expected=0.9000 tol=0.0800 |
| `223-adc-sample-clock-sequencer` | `FAIL_SIM_CORRECTNESS` | nc_az@1.45ns=0.0000 expected=0.9000 tol=0.0800 |
| `223-adc-sample-clock-sequencer` | `FAIL_SIM_CORRECTNESS` | nc_az@1.45ns=0.3780 expected=0.9000 tol=0.0800 |
| `224-pipeline-counter-onehot` | `FAIL_SIM_CORRECTNESS` | dout0@0.8ns=0.0000 expected=0.9000 tol=0.0800 |
| `224-pipeline-counter-onehot` | `FAIL_SIM_CORRECTNESS` | dout0@4.8ns=0.0000 expected=0.9000 tol=0.0800 |
| `224-pipeline-counter-onehot` | `FAIL_SIM_CORRECTNESS` | dout0@0.3ns=0.9000 expected=0.0000 tol=0.0800 |
| `224-pipeline-counter-onehot` | `FAIL_SIM_CORRECTNESS` | s5@4.8ns=0.4500 expected=0.9000 tol=0.0800 |
| `224-pipeline-counter-onehot` | `FAIL_SIM_CORRECTNESS` | dout0@0.8ns=0.3780 expected=0.9000 tol=0.0800 |
| `225-cdac-bidirect-residue` | `FAIL_SIM_CORRECTNESS` | initial_vres=0.0000 expected=0.4200 |
| `225-cdac-bidirect-residue` | `FAIL_SIM_CORRECTNESS` | vres_after_dctrl7=-0.1250 expected=0.8750 err=1.0000 |
| `225-cdac-bidirect-residue` | `FAIL_SIM_CORRECTNESS` | vres_after_dctrl6=0.3750 expected=0.6250 err=0.2500 |
| `225-cdac-bidirect-residue` | `FAIL_SIM_CORRECTNESS` | initial_vres=0.2100 expected=0.4200 |
| `225-cdac-bidirect-residue` | `FAIL_SIM_CORRECTNESS` | initial_vres=0.1764 expected=0.4200 |
| `226-pfd-reset-pulse` | `FAIL_SIM_CORRECTNESS` | ub@0.5ns=0.0000 expected=0.9000 tol=0.0800 |
| `226-pfd-reset-pulse` | `FAIL_SIM_CORRECTNESS` | d@3.5ns=0.4500 expected=0.9000 tol=0.0800 |
| `226-pfd-reset-pulse` | `FAIL_SIM_CORRECTNESS` | ub@0.5ns=0.0000 expected=0.9000 tol=0.0800 |
| `226-pfd-reset-pulse` | `FAIL_SIM_CORRECTNESS` | ub@1.9ns=0.0000 expected=0.9000 tol=0.0800 |
| `226-pfd-reset-pulse` | `FAIL_SIM_CORRECTNESS` | ub@0.5ns=0.3780 expected=0.9000 tol=0.0800 |
| `227-trim-ctrl-4bit` | `FAIL_SIM_CORRECTNESS` | dout0@1.5ns=0.0000 expected=0.9000 tol=0.0800 |
| `227-trim-ctrl-4bit` | `FAIL_SIM_CORRECTNESS` | dout1@0.5ns=0.9000 expected=0.0000 tol=0.0800 |
| `227-trim-ctrl-4bit` | `FAIL_SIM_CORRECTNESS` | dout3@0.5ns=0.9000 expected=0.0000 tol=0.0800 |
| `227-trim-ctrl-4bit` | `FAIL_SIM_CORRECTNESS` | dout0@1.5ns=0.4500 expected=0.9000 tol=0.0800 |
| `227-trim-ctrl-4bit` | `FAIL_SIM_CORRECTNESS` | dout0@1.5ns=0.3780 expected=0.9000 tol=0.0800 |
| `228-linearity-rdac-offset-sweep` | `FAIL_SIM_CORRECTNESS` | dc0@0.5ns=0.0000 expected=1.0000 tol=0.0120 |
| `228-linearity-rdac-offset-sweep` | `FAIL_SIM_CORRECTNESS` | vrefp@0.5ns=0.6000 expected=0.3656 tol=0.0120 |
| `228-linearity-rdac-offset-sweep` | `FAIL_SIM_CORRECTNESS` | dc0@5.5ns=1.0000 expected=0.0000 tol=0.0120 |
| `228-linearity-rdac-offset-sweep` | `FAIL_SIM_CORRECTNESS` | vinp@0.5ns=0.1713 expected=0.3856 tol=0.0120 |
| `228-linearity-rdac-offset-sweep` | `FAIL_SIM_CORRECTNESS` | dc0@0.5ns=0.4200 expected=1.0000 tol=0.0120 |
| `229-sar-das-logic-6b` | `FAIL_SIM_CORRECTNESS` | sampling_fall_d1@1.2ns=0.0000 expected=1.1000 tol=0.1300 |
| `229-sar-das-logic-6b` | `FAIL_SIM_CORRECTNESS` | sar_rise_co@1.43ns=1.1000 expected=0.0000 tol=0.1300 |
| `229-sar-das-logic-6b` | `FAIL_SIM_CORRECTNESS` | sampling_fall_d6@1.2ns=0.5500 expected=1.1000 tol=0.1300 |
| `229-sar-das-logic-6b` | `FAIL_SIM_CORRECTNESS` | sar_rise_co@2.48ns=0.5500 expected=1.1000 tol=0.1300 |
| `229-sar-das-logic-6b` | `FAIL_SIM_CORRECTNESS` | sampling_fall_d1@1.2ns=0.4620 expected=1.1000 tol=0.1300 |
| `230-sar-logic-4b-self-timed` | `FAIL_SIM_CORRECTNESS` | reset_dbotp1@0.28ns=0.0000 expected=1.0000 tol=0.1200 |
| `230-sar-logic-4b-self-timed` | `FAIL_SIM_CORRECTNESS` | decision_step4_dout4@1.3ns=0.0000 expected=1.0000 tol=0.1200 |
| `230-sar-logic-4b-self-timed` | `FAIL_SIM_CORRECTNESS` | decision_step3_dout4@1.9ns=0.0000 expected=1.0000 tol=0.1200 |
| `230-sar-logic-4b-self-timed` | `FAIL_SIM_CORRECTNESS` | clkc_start_cmpck@0.95ns=0.5000 expected=1.0000 tol=0.1200 |
| `230-sar-logic-4b-self-timed` | `FAIL_SIM_CORRECTNESS` | reset_dbotp1@0.28ns=0.4200 expected=1.0000 tol=0.1200 |
| `231-pfd-tdomain-reset-window` | `FAIL_SIM_CORRECTNESS` | up@1ns=0.0000 expected=1.0000 tol=0.0900 |
| `231-pfd-tdomain-reset-window` | `FAIL_SIM_CORRECTNESS` | up@3.1ns=0.0000 expected=1.0000 tol=0.0900 |
| `231-pfd-tdomain-reset-window` | `FAIL_SIM_CORRECTNESS` | up@3.1ns=0.0000 expected=1.0000 tol=0.0900 |
| `231-pfd-tdomain-reset-window` | `FAIL_SIM_CORRECTNESS` | up@1ns=0.0000 expected=1.0000 tol=0.0900 |
| `231-pfd-tdomain-reset-window` | `FAIL_SIM_CORRECTNESS` | up@1ns=0.4200 expected=1.0000 tol=0.0900 |
| `232-pipe-adc-gain-control-loop` | `FAIL_SIM_CORRECTNESS` | dout10@0.5ns=0.0000 expected=0.9000 tol=0.0900 |
| `232-pipe-adc-gain-control-loop` | `FAIL_SIM_CORRECTNESS` | ddiff@1.5ns=0.5000 expected=0.8200 tol=0.0900 |
| `232-pipe-adc-gain-control-loop` | `FAIL_SIM_CORRECTNESS` | gctrlcode@1.5ns=0.9000 expected=0.7200 tol=0.0900 |
| `232-pipe-adc-gain-control-loop` | `FAIL_SIM_CORRECTNESS` | gainctrl6@1.5ns=0.4500 expected=0.9000 tol=0.0900 |
| `232-pipe-adc-gain-control-loop` | `FAIL_SIM_CORRECTNESS` | dout10@0.5ns=0.3780 expected=0.9000 tol=0.0900 |
| `233-clock-sample-1600n-sequencer` | `FAIL_SIM_CORRECTNESS` | rst@0.1ns=0.0000 expected=1.1000 tol=0.0900 |
| `233-clock-sample-1600n-sequencer` | `FAIL_SIM_CORRECTNESS` | conv@3.5ns=0.5500 expected=1.1000 tol=0.0900 |
| `233-clock-sample-1600n-sequencer` | `FAIL_SIM_CORRECTNESS` | nc@2.1ns=0.0000 expected=1.1000 tol=0.0900 |
| `233-clock-sample-1600n-sequencer` | `FAIL_SIM_CORRECTNESS` | s@9.4ns=0.0000 expected=1.1000 tol=0.0900 |
| `233-clock-sample-1600n-sequencer` | `FAIL_SIM_CORRECTNESS` | nc@2.1ns=0.4620 expected=1.1000 tol=0.0900 |
| `234-l2-sar-logic-4b` | `FAIL_SIM_CORRECTNESS` | clkc_start_cmpck@0.95ns=0.0000 expected=1.1000 tol=0.1300 |
| `234-l2-sar-logic-4b` | `FAIL_SIM_CORRECTNESS` | decision_step3_do3@1.27ns=0.0000 expected=1.1000 tol=0.1300 |
| `234-l2-sar-logic-4b` | `FAIL_SIM_CORRECTNESS` | decision_step2_do3@1.87ns=0.0000 expected=1.1000 tol=0.1300 |
| `234-l2-sar-logic-4b` | `FAIL_SIM_CORRECTNESS` | clkc_start_cmpck@0.95ns=0.5500 expected=1.1000 tol=0.1300 |
| `234-l2-sar-logic-4b` | `FAIL_SIM_CORRECTNESS` | clkc_start_cmpck@0.95ns=0.4620 expected=1.1000 tol=0.1300 |
| `235-phase-detector-chopper` | `FAIL_SIM_CORRECTNESS` | vif@0.5ns=0.0000 expected=-0.1250 tol=0.0150 |
| `235-phase-detector-chopper` | `FAIL_SIM_CORRECTNESS` | vif@0.5ns=0.1250 expected=-0.1250 tol=0.0150 |
| `235-phase-detector-chopper` | `FAIL_SIM_CORRECTNESS` | vif@0.5ns=-0.1000 expected=-0.1250 tol=0.0150 |
| `235-phase-detector-chopper` | `FAIL_SIM_CORRECTNESS` | vif@0.5ns=0.1250 expected=-0.1250 tol=0.0150 |
| `235-phase-detector-chopper` | `FAIL_SIM_CORRECTNESS` | vif@0.5ns=-0.0525 expected=-0.1250 tol=0.0150 |
| `236-single-adc-7b-weighted` | `FAIL_SIM_CORRECTNESS` | dout@1.5ns=0.0000 expected=0.6641 tol=0.0120 |
| `236-single-adc-7b-weighted` | `FAIL_SIM_CORRECTNESS` | dout@1.5ns=0.1641 expected=0.6641 tol=0.0120 |
| `236-single-adc-7b-weighted` | `FAIL_SIM_CORRECTNESS` | dout@1.5ns=0.3320 expected=0.6641 tol=0.0120 |
| `236-single-adc-7b-weighted` | `FAIL_SIM_CORRECTNESS` | dout@0.5ns=0.1250 expected=0.0000 tol=0.0120 |
| `236-single-adc-7b-weighted` | `FAIL_SIM_CORRECTNESS` | dout@1.5ns=0.2789 expected=0.6641 tol=0.0120 |
| `237-qtz-differential-2level` | `FAIL_SIM_CORRECTNESS` | dout_after_clk=0.0000 expected=-0.5000 err=0.5000 |
| `237-qtz-differential-2level` | `FAIL_SIM_CORRECTNESS` | dout_after_clk=0.5000 expected=-0.5000 err=1.0000 |
| `237-qtz-differential-2level` | `FAIL_SIM_CORRECTNESS` | dout_after_clk=-0.5000 expected=0.5000 err=1.0000 |
| `237-qtz-differential-2level` | `FAIL_SIM_CORRECTNESS` | dout_after_clk=0.0000 expected=-0.5000 err=0.5000 |
| `237-qtz-differential-2level` | `FAIL_SIM_CORRECTNESS` | dout_after_clk=-0.2100 expected=-0.5000 err=0.2900 |
| `238-l2-7b-dac-ready` | `FAIL_SIM_CORRECTNESS` | checked=412 ready_edges=6 max_ready_dac_error=0.90000 |
| `238-l2-7b-dac-ready` | `FAIL_SIM_CORRECTNESS` | checked=413 ready_edges=6 max_ready_dac_error=0.87209 |
| `238-l2-7b-dac-ready` | `FAIL_SIM_CORRECTNESS` | checked=413 ready_edges=6 max_ready_dac_error=0.45000 |
| `238-l2-7b-dac-ready` | `FAIL_SIM_CORRECTNESS` | checked=413 ready_edges=6 max_ready_dac_error=0.90000 |
| `238-l2-7b-dac-ready` | `FAIL_SIM_CORRECTNESS` | checked=413 ready_edges=6 max_ready_dac_error=0.52200 |
| `239-l2-cdac-4b-switch` | `FAIL_SIM_CORRECTNESS` | aout@1.5ns=0.0000 expected=-1.1000 tol=0.0250 |
| `239-l2-cdac-4b-switch` | `FAIL_SIM_CORRECTNESS` | aout@0.5ns=-1.1000 expected=0.0000 tol=0.0250 |
| `239-l2-cdac-4b-switch` | `FAIL_SIM_CORRECTNESS` | aout@2.5ns=0.2750 expected=0.1941 tol=0.0250 |
| `239-l2-cdac-4b-switch` | `FAIL_SIM_CORRECTNESS` | aout@1.5ns=0.0000 expected=-1.1000 tol=0.0250 |
| `239-l2-cdac-4b-switch` | `FAIL_SIM_CORRECTNESS` | aout@1.5ns=-0.4620 expected=-1.1000 tol=0.0250 |
| `240-cdac-monodown-7b` | `FAIL_SIM_CORRECTNESS` | vres@0.5ns=0.0000 expected=0.8000 tol=0.0200 |
| `240-cdac-monodown-7b` | `FAIL_SIM_CORRECTNESS` | vres@1.5ns=0.5500 expected=0.3000 tol=0.0200 |
| `240-cdac-monodown-7b` | `FAIL_SIM_CORRECTNESS` | vres@2.1ns=0.5500 expected=0.0500 tol=0.0200 |
| `240-cdac-monodown-7b` | `FAIL_SIM_CORRECTNESS` | vres@0.5ns=0.4000 expected=0.8000 tol=0.0200 |
| `240-cdac-monodown-7b` | `FAIL_SIM_CORRECTNESS` | vres@0.5ns=0.3360 expected=0.8000 tol=0.0200 |
| `241-cdac-6b-stage1-up` | `FAIL_SIM_CORRECTNESS` | vres@0.5ns=0.0000 expected=0.2000 tol=0.0200 |
| `241-cdac-6b-stage1-up` | `FAIL_SIM_CORRECTNESS` | vres@1.5ns=0.4500 expected=0.7000 tol=0.0200 |
| `241-cdac-6b-stage1-up` | `FAIL_SIM_CORRECTNESS` | vres@2.1ns=0.4500 expected=0.9500 tol=0.0200 |
| `241-cdac-6b-stage1-up` | `FAIL_SIM_CORRECTNESS` | vres@0.5ns=0.1000 expected=0.2000 tol=0.0200 |
| `241-cdac-6b-stage1-up` | `FAIL_SIM_CORRECTNESS` | vres@0.5ns=0.0840 expected=0.2000 tol=0.0200 |
| `242-adc-zoom-timing-sequencer` | `FAIL_SIM_CORRECTNESS` | rst@0.6ns=0.0000 expected=1.1000 tol=0.0900 |
| `242-adc-zoom-timing-sequencer` | `FAIL_SIM_CORRECTNESS` | clk_sar@3.1ns=0.5500 expected=1.1000 tol=0.0900 |
| `242-adc-zoom-timing-sequencer` | `FAIL_SIM_CORRECTNESS` | sar@3.4ns=0.0000 expected=1.1000 tol=0.0900 |
| `242-adc-zoom-timing-sequencer` | `FAIL_SIM_CORRECTNESS` | clk_zoom@9.3ns=0.0000 expected=1.1000 tol=0.0900 |
| `242-adc-zoom-timing-sequencer` | `FAIL_SIM_CORRECTNESS` | intg@8.3ns=0.4620 expected=1.1000 tol=0.0900 |
| `243-l2-sar-logic-7b` | `FAIL_SIM_CORRECTNESS` | cmpck@0.95ns=0.0000 expected=1.1000 tol=0.0900 |
| `243-l2-sar-logic-7b` | `FAIL_SIM_CORRECTNESS` | do6@1.7ns=0.0000 expected=1.1000 tol=0.0900 |
| `243-l2-sar-logic-7b` | `FAIL_SIM_CORRECTNESS` | cmpck@6ns=1.1000 expected=0.0000 tol=0.0900 |
| `243-l2-sar-logic-7b` | `FAIL_SIM_CORRECTNESS` | cmpck@0.95ns=0.5500 expected=1.1000 tol=0.0900 |
| `243-l2-sar-logic-7b` | `FAIL_SIM_CORRECTNESS` | cmpck@0.95ns=0.4620 expected=1.1000 tol=0.0900 |
| `244-l3-sar2-logic-7b` | `FAIL_SIM_CORRECTNESS` | do1=0.0 expected=0.900 do2=0.0 expected=0.900 do5=0.0 expected=0.900 sp1=0.0 expected=0.900 sp2=0.0 expected=0.900 sn3=0.0 expected=0.900 sn4=0.0 expected=0.900 sp5=0.0 expected=0.900 |
| `244-l3-sar2-logic-7b` | `FAIL_SIM_CORRECTNESS` | do0=0.9 expected=0.000 do1=0.0 expected=0.900 do2=0.0 expected=0.900 do3=0.9 expected=0.000 do4=0.9 expected=0.000 do5=0.0 expected=0.900 do6=0.9 expected=0.000 sp1=0.0 expected=0.900 |
| `244-l3-sar2-logic-7b` | `FAIL_SIM_CORRECTNESS` | do1=0.0 expected=0.900 do2=0.0 expected=0.900 do5=0.0 expected=0.900 sp1=0.0 expected=0.900 sp2=0.0 expected=0.900 sn3=0.0 expected=0.900 sn4=0.0 expected=0.900 sp5=0.0 expected=0.900 |
| `244-l3-sar2-logic-7b` | `FAIL_SIM_CORRECTNESS` | cmpck_start=0.45 |
| `244-l3-sar2-logic-7b` | `FAIL_SIM_CORRECTNESS` | do1=0.378 expected=0.900 do2=0.378 expected=0.900 do5=0.378 expected=0.900 cmpck_start=0.378 |
| `245-cdac-8b-monodown` | `FAIL_SIM_CORRECTNESS` | vres_after_sample@0.675ns=0.0000 expected=0.3600 vres_after_dctrl4@1.410ns=0.0000 expected=0.2975 vres_after_dctrl7@2.010ns=0.0000 expected=-0.2025 vres_after_dctrl1@2.610ns=0.0000 expected=-0.2103 vres_after_dctrl6@3.210ns=0.0000 expected=-0.4603 vres_after_sample@6.425ns=0.0000 expected=-0.1200 |
| `245-cdac-8b-monodown` | `FAIL_SIM_CORRECTNESS` | vres_after_dctrl7@2.010ns=0.0475 expected=-0.2025 vres_after_dctrl1@2.610ns=0.0397 expected=-0.2103 vres_after_dctrl6@3.210ns=-0.2103 expected=-0.4603 |
| `245-cdac-8b-monodown` | `FAIL_SIM_CORRECTNESS` | vres_after_dctrl6@3.210ns=0.0397 expected=-0.4603 |
| `245-cdac-8b-monodown` | `FAIL_SIM_CORRECTNESS` | vres_after_sample@0.675ns=0.1800 expected=0.3600 vres_after_dctrl4@1.410ns=0.1487 expected=0.2975 vres_after_dctrl7@2.010ns=-0.1013 expected=-0.2025 vres_after_dctrl1@2.610ns=-0.1052 expected=-0.2103 vres_after_dctrl6@3.210ns=-0.2302 expected=-0.4603 vres_after_sample@6.425ns=-0.0600 expected=-0.1200 |
| `245-cdac-8b-monodown` | `FAIL_SIM_CORRECTNESS` | vres_after_sample@0.675ns=0.1512 expected=0.3600 vres_after_dctrl4@1.410ns=0.1250 expected=0.2975 vres_after_dctrl7@2.010ns=-0.0851 expected=-0.2025 vres_after_dctrl1@2.610ns=-0.0883 expected=-0.2103 vres_after_dctrl6@3.210ns=-0.1933 expected=-0.4603 vres_after_sample@6.425ns=-0.0504 expected=-0.1200 |
| `246-va-dac-6b-se` | `FAIL_SIM_CORRECTNESS` | aout@0.5ns=0.0000 expected=-1.0000 tol=0.0200 |
| `246-va-dac-6b-se` | `FAIL_SIM_CORRECTNESS` | aout@1.5ns=-0.4737 expected=-0.1368 tol=0.0200 |
| `246-va-dac-6b-se` | `FAIL_SIM_CORRECTNESS` | aout@0.5ns=0.0000 expected=-1.0000 tol=0.0200 |
| `246-va-dac-6b-se` | `FAIL_SIM_CORRECTNESS` | aout@0.5ns=-0.5000 expected=-1.0000 tol=0.0200 |
| `246-va-dac-6b-se` | `FAIL_SIM_CORRECTNESS` | aout@0.5ns=-0.4200 expected=-1.0000 tol=0.0200 |
| `247-offset-halving-search` | `FAIL_SIM_CORRECTNESS` | vinp@0.5ns=0.0000 expected=0.4500 tol=0.0100 |
| `247-offset-halving-search` | `FAIL_SIM_CORRECTNESS` | vinp@2ns=0.4500 expected=0.4250 tol=0.0100 |
| `247-offset-halving-search` | `FAIL_SIM_CORRECTNESS` | vinp@1ns=0.5000 expected=0.4000 tol=0.0100 |
| `247-offset-halving-search` | `FAIL_SIM_CORRECTNESS` | vinp@1ns=0.3500 expected=0.4000 tol=0.0100 |
| `247-offset-halving-search` | `FAIL_SIM_CORRECTNESS` | vinp@0.5ns=0.1890 expected=0.4500 tol=0.0100 |
| `248-sar-comparator-reset-high` | `FAIL_SIM_CORRECTNESS` | dcmpp@0.2ns=0.0000 expected=0.9000 tol=0.0700 |
| `248-sar-comparator-reset-high` | `FAIL_SIM_CORRECTNESS` | dcmpp@0.5ns=0.0000 expected=0.9000 tol=0.0700 |
| `248-sar-comparator-reset-high` | `FAIL_SIM_CORRECTNESS` | dcmpp@0.2ns=0.0000 expected=0.9000 tol=0.0700 |
| `248-sar-comparator-reset-high` | `FAIL_SIM_CORRECTNESS` | dcmpp@0.2ns=0.4500 expected=0.9000 tol=0.0700 |
| `248-sar-comparator-reset-high` | `FAIL_SIM_CORRECTNESS` | dcmpp@0.2ns=0.3780 expected=0.9000 tol=0.0700 |
| `249-dac-restore-4bit-clocked` | `FAIL_SIM_CORRECTNESS` | vout@0.5ns=0.0000 expected=-0.8438 tol=0.0120 |
| `249-dac-restore-4bit-clocked` | `FAIL_SIM_CORRECTNESS` | vout@0.5ns=-0.9000 expected=-0.8438 tol=0.0120 |
| `249-dac-restore-4bit-clocked` | `FAIL_SIM_CORRECTNESS` | vout@1.5ns=-0.2400 expected=-0.2812 tol=0.0120 |
| `249-dac-restore-4bit-clocked` | `FAIL_SIM_CORRECTNESS` | vout@0.5ns=0.0563 expected=-0.8438 tol=0.0120 |
| `249-dac-restore-4bit-clocked` | `FAIL_SIM_CORRECTNESS` | vout@0.5ns=-0.3544 expected=-0.8438 tol=0.0120 |
| `250-dac-restore-7bit-clocked` | `FAIL_SIM_CORRECTNESS` | vout@0.5ns=0.0000 expected=-0.8930 tol=0.0120 |
| `250-dac-restore-7bit-clocked` | `FAIL_SIM_CORRECTNESS` | vout@2.5ns=-0.5977 expected=0.3023 tol=0.0120 |
| `250-dac-restore-7bit-clocked` | `FAIL_SIM_CORRECTNESS` | vout@3.5ns=0.9071 expected=0.8930 tol=0.0120 |
| `250-dac-restore-7bit-clocked` | `FAIL_SIM_CORRECTNESS` | vout@0.5ns=0.0070 expected=-0.8930 tol=0.0120 |
| `250-dac-restore-7bit-clocked` | `FAIL_SIM_CORRECTNESS` | vout@0.5ns=-0.3750 expected=-0.8930 tol=0.0120 |
| `251-dac-restore-6bit-1p8` | `FAIL_SIM_CORRECTNESS` | vout@0.5ns=0.0000 expected=-1.7719 tol=0.0200 |
| `251-dac-restore-6bit-1p8` | `FAIL_SIM_CORRECTNESS` | vout@2.5ns=-1.2094 expected=0.5906 tol=0.0200 |
| `251-dac-restore-6bit-1p8` | `FAIL_SIM_CORRECTNESS` | vout@2.5ns=0.6286 expected=0.5906 tol=0.0200 |
| `251-dac-restore-6bit-1p8` | `FAIL_SIM_CORRECTNESS` | vout@0.5ns=0.0281 expected=-1.7719 tol=0.0200 |
| `251-dac-restore-6bit-1p8` | `FAIL_SIM_CORRECTNESS` | vout@0.5ns=-0.7442 expected=-1.7719 tol=0.0200 |
| `252-sample-hold-5v-clock` | `FAIL_SIM_CORRECTNESS` | vout@0.5ns=0.0000 expected=0.1000 tol=0.0200 |
| `252-sample-hold-5v-clock` | `FAIL_SIM_CORRECTNESS` | vout@0.5ns=0.0000 expected=0.1000 tol=0.0200 |
| `252-sample-hold-5v-clock` | `FAIL_SIM_CORRECTNESS` | vout@0.2ns=0.1000 expected=0.0000 tol=0.0200 |
| `252-sample-hold-5v-clock` | `FAIL_SIM_CORRECTNESS` | vout@0.5ns=0.0500 expected=0.1000 tol=0.0200 |
| `252-sample-hold-5v-clock` | `FAIL_SIM_CORRECTNESS` | vout@0.5ns=0.0420 expected=0.1000 tol=0.0200 |
| `253-sum5-signed-sar-weight` | `FAIL_SIM_CORRECTNESS` | out@0.5ns=0.0000 expected=-3.2313 tol=0.0250 |
| `253-sum5-signed-sar-weight` | `FAIL_SIM_CORRECTNESS` | out@0.5ns=-2.1313 expected=-3.2313 tol=0.0250 |
| `253-sum5-signed-sar-weight` | `FAIL_SIM_CORRECTNESS` | out@0.5ns=-1.0656 expected=-3.2313 tol=0.0250 |
| `253-sum5-signed-sar-weight` | `FAIL_SIM_CORRECTNESS` | out@0.5ns=-1.6156 expected=-3.2313 tol=0.0250 |
| `253-sum5-signed-sar-weight` | `FAIL_SIM_CORRECTNESS` | out@0.5ns=-1.3571 expected=-3.2313 tol=0.0250 |
| `254-lt-readout-sar4` | `FAIL_SIM_CORRECTNESS` | vout@1.5ns=0.0000 expected=0.5625 tol=0.0200 |
| `254-lt-readout-sar4` | `FAIL_SIM_CORRECTNESS` | vout@1.5ns=1.3500 expected=0.5625 tol=0.0200 |
| `254-lt-readout-sar4` | `FAIL_SIM_CORRECTNESS` | vout@1.5ns=0.6000 expected=0.5625 tol=0.0200 |
| `254-lt-readout-sar4` | `FAIL_SIM_CORRECTNESS` | vout@1.5ns=0.2812 expected=0.5625 tol=0.0200 |
| `254-lt-readout-sar4` | `FAIL_SIM_CORRECTNESS` | vout@1.5ns=0.2362 expected=0.5625 tol=0.0200 |
| `255-tool-4bit-sar-signed-dac` | `FAIL_SIM_CORRECTNESS` | aout@0.510ns=0.0000 expected=0.5625 bits=1010 aout@1.410ns=0.0000 expected=-1.0125 bits=0011 aout@2.310ns=0.0000 expected=1.0125 bits=1100 aout@3.210ns=0.0000 expected=-0.5625 bits=0101 aout@4.110ns=0.0000 expected=0.3375 bits=1001 |
| `255-tool-4bit-sar-signed-dac` | `FAIL_SIM_CORRECTNESS` | aout@0.510ns=1.1250 expected=0.5625 bits=1010 aout@1.410ns=0.3375 expected=-1.0125 bits=0011 aout@2.310ns=1.3500 expected=1.0125 bits=1100 aout@3.210ns=0.5625 expected=-0.5625 bits=0101 aout@4.110ns=1.0125 expected=0.3375 bits=1001 |
| `255-tool-4bit-sar-signed-dac` | `FAIL_SIM_CORRECTNESS` | aout@0.510ns=0.2812 expected=0.5625 bits=1010 aout@1.410ns=-0.5062 expected=-1.0125 bits=0011 aout@2.310ns=0.5062 expected=1.0125 bits=1100 aout@3.210ns=-0.2812 expected=-0.5625 bits=0101 aout@4.110ns=0.1688 expected=0.3375 bits=1001 |
| `255-tool-4bit-sar-signed-dac` | `FAIL_SIM_CORRECTNESS` | aout@0.510ns=0.0000 expected=0.5625 bits=1010 aout@1.410ns=0.5625 expected=-1.0125 bits=0011 aout@2.310ns=-1.0125 expected=1.0125 bits=1100 aout@3.210ns=1.0125 expected=-0.5625 bits=0101 aout@4.110ns=-0.5625 expected=0.3375 bits=1001 |
| `255-tool-4bit-sar-signed-dac` | `FAIL_SIM_CORRECTNESS` | aout@0.510ns=0.2362 expected=0.5625 bits=1010 aout@1.410ns=-0.4253 expected=-1.0125 bits=0011 aout@2.310ns=0.4253 expected=1.0125 bits=1100 aout@3.210ns=-0.2362 expected=-0.5625 bits=0101 aout@4.110ns=0.1417 expected=0.3375 bits=1001 |
| `256-dac4bit-small-swing` | `FAIL_SIM_CORRECTNESS` | vout@0.5ns=0.0000 expected=-0.0200 tol=0.0015 |
| `256-dac4bit-small-swing` | `FAIL_SIM_CORRECTNESS` | vout@0.5ns=0.0000 expected=-0.0200 tol=0.0015 |
| `256-dac4bit-small-swing` | `FAIL_SIM_CORRECTNESS` | vout@1.5ns=0.0120 expected=-0.0067 tol=0.0015 |
| `256-dac4bit-small-swing` | `FAIL_SIM_CORRECTNESS` | vout@1.5ns=-0.0200 expected=-0.0067 tol=0.0015 |
| `256-dac4bit-small-swing` | `FAIL_SIM_CORRECTNESS` | vout@0.5ns=-0.0084 expected=-0.0200 tol=0.0015 |
| `257-comparator-reset-low-1p8` | `FAIL_SIM_CORRECTNESS` | dcmpp@0.55ns=0.0000 expected=1.8000 tol=0.0800 |
| `257-comparator-reset-low-1p8` | `FAIL_SIM_CORRECTNESS` | dcmpp@0.95ns=1.8000 expected=0.0000 tol=0.0800 |
| `257-comparator-reset-low-1p8` | `FAIL_SIM_CORRECTNESS` | dcmpp@0.55ns=0.0000 expected=1.8000 tol=0.0800 |
| `257-comparator-reset-low-1p8` | `FAIL_SIM_CORRECTNESS` | dcmpp@0.55ns=0.0000 expected=1.8000 tol=0.0800 |
| `257-comparator-reset-low-1p8` | `FAIL_SIM_CORRECTNESS` | dcmpp@0.55ns=0.7560 expected=1.8000 tol=0.0800 |
| `258-lt-read-sar6b-weighted` | `FAIL_SIM_CORRECTNESS` | vout@0.5ns=0.0000 expected=-0.9000 tol=0.0200 |
| `258-lt-read-sar6b-weighted` | `FAIL_SIM_CORRECTNESS` | vout@1.5ns=0.2531 expected=0.2250 tol=0.0200 |
| `258-lt-read-sar6b-weighted` | `FAIL_SIM_CORRECTNESS` | vout@0.5ns=0.0000 expected=-0.9000 tol=0.0200 |
| `258-lt-read-sar6b-weighted` | `FAIL_SIM_CORRECTNESS` | vout@1.5ns=-0.6188 expected=0.2250 tol=0.0200 |
| `258-lt-read-sar6b-weighted` | `FAIL_SIM_CORRECTNESS` | vout@0.5ns=-0.3780 expected=-0.9000 tol=0.0200 |
| `259-lt-read-sar7b-weighted` | `FAIL_SIM_CORRECTNESS` | vout@0.5ns=0.0000 expected=-0.9000 tol=0.0200 |
| `259-lt-read-sar7b-weighted` | `FAIL_SIM_CORRECTNESS` | vout@0.5ns=-0.4500 expected=-0.9000 tol=0.0200 |
| `259-lt-read-sar7b-weighted` | `FAIL_SIM_CORRECTNESS` | vout@0.5ns=-0.4500 expected=-0.9000 tol=0.0200 |
| `259-lt-read-sar7b-weighted` | `FAIL_SIM_CORRECTNESS` | vout@1.5ns=-0.6680 expected=0.2250 tol=0.0200 |
| `259-lt-read-sar7b-weighted` | `FAIL_SIM_CORRECTNESS` | vout@0.5ns=-0.3780 expected=-0.9000 tol=0.0200 |
| `260-dac-serial-16b-nobridge` | `FAIL_SIM_CORRECTNESS` | checked=1010 ready_edges=8 sample_resets=2 max_serial_dac_error=1.10000 |
| `260-dac-serial-16b-nobridge` | `FAIL_SIM_CORRECTNESS` | checked=1010 ready_edges=8 sample_resets=2 max_serial_dac_error=0.97093 |
| `260-dac-serial-16b-nobridge` | `FAIL_SIM_CORRECTNESS` | checked=1040 ready_edges=8 sample_resets=2 max_serial_dac_error=0.97093 |
| `260-dac-serial-16b-nobridge` | `FAIL_SIM_CORRECTNESS` | checked=1010 ready_edges=8 sample_resets=2 max_serial_dac_error=0.48546 |
| `260-dac-serial-16b-nobridge` | `FAIL_SIM_CORRECTNESS` | checked=1010 ready_edges=8 sample_resets=2 max_serial_dac_error=0.63800 |
| `261-sar-13bit-serial-decoder` | `FAIL_SIM_CORRECTNESS` | dout@0.260ns=0.0000 expected=-0.5000 dnum@1.210ns=0.000 expected=1.0 dnum@2.260ns=0.000 expected=1.0 dnum@3.310ns=0.000 expected=1.0 dnum@4.360ns=0.000 expected=2.0 dnum@5.410ns=0.000 expected=3.0 |
| `261-sar-13bit-serial-decoder` | `FAIL_SIM_CORRECTNESS` | dnum@1.210ns=0.000 expected=1.0 dnum@3.310ns=2.000 expected=1.0 dnum@5.410ns=2.000 expected=3.0 dnum@7.510ns=3.000 expected=4.0 dnum@9.610ns=5.000 expected=4.0 dnum@11.710ns=6.000 expected=5.0 |
| `261-sar-13bit-serial-decoder` | `FAIL_SIM_CORRECTNESS` | dnum@13.810ns=6.000 expected=7.0 dout@15.710ns=-0.1986 expected=0.1030 |
| `261-sar-13bit-serial-decoder` | `FAIL_SIM_CORRECTNESS` | dout@0.260ns=0.0000 expected=-0.5000 dout@15.710ns=0.6030 expected=0.1030 |
| `261-sar-13bit-serial-decoder` | `FAIL_SIM_CORRECTNESS` | dout@0.260ns=-0.2100 expected=-0.5000 dnum@1.210ns=0.420 expected=1.0 dnum@2.260ns=0.420 expected=1.0 dnum@3.310ns=0.420 expected=1.0 dnum@4.360ns=0.840 expected=2.0 dnum@5.410ns=1.260 expected=3.0 |
| `262-single-shot-timer-pulse` | `FAIL_SIM_CORRECTNESS` | vout@0.9ns=0.0000 expected=0.9000 tol=0.0800 |
| `262-single-shot-timer-pulse` | `FAIL_SIM_CORRECTNESS` | vout@0.9ns=0.0000 expected=0.9000 tol=0.0800 |
| `262-single-shot-timer-pulse` | `FAIL_SIM_CORRECTNESS` | vout@2.4ns=0.0000 expected=0.9000 tol=0.0800 |
| `262-single-shot-timer-pulse` | `FAIL_SIM_CORRECTNESS` | vout@2.9ns=0.9000 expected=0.0000 tol=0.0800 |
| `262-single-shot-timer-pulse` | `FAIL_SIM_CORRECTNESS` | vout@0.9ns=0.3780 expected=0.9000 tol=0.0800 |
| `263-clocked-comparator-dual-output` | `FAIL_SIM_CORRECTNESS` | decision@0.480ns outp/outn=0.000/0.000 expected=1.000/0.000 decision@2.880ns outp/outn=0.000/0.000 expected=0.000/1.000 |
| `263-clocked-comparator-dual-output` | `FAIL_SIM_CORRECTNESS` | reset@1.180ns outp/outn=1.000/0.000 reset@3.580ns outp/outn=0.000/1.000 |
| `263-clocked-comparator-dual-output` | `FAIL_SIM_CORRECTNESS` | decision@0.480ns outp/outn=0.000/1.000 expected=1.000/0.000 decision@2.880ns outp/outn=1.000/0.000 expected=0.000/1.000 |
| `263-clocked-comparator-dual-output` | `FAIL_SIM_CORRECTNESS` | decision@0.480ns outp/outn=0.000/1.000 expected=1.000/0.000 decision@2.880ns outp/outn=1.000/0.000 expected=0.000/1.000 |
| `263-clocked-comparator-dual-output` | `FAIL_SIM_CORRECTNESS` | decision@0.480ns outp/outn=0.420/0.000 expected=1.000/0.000 decision@2.880ns outp/outn=0.000/0.420 expected=0.000/1.000 |
| `264-dac4bit-bipolar-252m` | `FAIL_SIM_CORRECTNESS` | vout@0.5ns=0.0000 expected=-0.2520 tol=0.0100 |
| `264-dac4bit-bipolar-252m` | `FAIL_SIM_CORRECTNESS` | vout@0.5ns=0.0000 expected=-0.2520 tol=0.0100 |
| `264-dac4bit-bipolar-252m` | `FAIL_SIM_CORRECTNESS` | vout@0.5ns=-0.0200 expected=-0.2520 tol=0.0100 |
| `264-dac4bit-bipolar-252m` | `FAIL_SIM_CORRECTNESS` | vout@1.5ns=0.0168 expected=-0.2184 tol=0.0100 |
| `264-dac4bit-bipolar-252m` | `FAIL_SIM_CORRECTNESS` | vout@0.5ns=-0.1058 expected=-0.2520 tol=0.0100 |
| `265-bin2ther-2b` | `FAIL_SIM_CORRECTNESS` | t0@2.5ns=0.0000 expected=0.9000 tol=0.0500 |
| `265-bin2ther-2b` | `FAIL_SIM_CORRECTNESS` | t0@1.5ns=0.9000 expected=0.0000 tol=0.0500 |
| `265-bin2ther-2b` | `FAIL_SIM_CORRECTNESS` | t0@1.5ns=0.9000 expected=0.0000 tol=0.0500 |
| `265-bin2ther-2b` | `FAIL_SIM_CORRECTNESS` | t0@2.5ns=0.0000 expected=0.9000 tol=0.0500 |
| `265-bin2ther-2b` | `FAIL_SIM_CORRECTNESS` | t0@2.5ns=0.3780 expected=0.9000 tol=0.0500 |
| `266-dff-set-reset` | `FAIL_SIM_CORRECTNESS` | q@1.7ns=0.0000 expected=0.9000 tol=0.0500 |
| `266-dff-set-reset` | `FAIL_SIM_CORRECTNESS` | q@0.7ns=0.9000 expected=0.0000 tol=0.0500 |
| `266-dff-set-reset` | `FAIL_SIM_CORRECTNESS` | q@3.5ns=0.9000 expected=0.0000 tol=0.0500 |
| `266-dff-set-reset` | `FAIL_SIM_CORRECTNESS` | qb@0.7ns=0.0000 expected=0.9000 tol=0.0500 |
| `266-dff-set-reset` | `FAIL_SIM_CORRECTNESS` | q@1.7ns=0.3780 expected=0.9000 tol=0.0500 |
| `267-pfd-up-down-state` | `FAIL_SIM_CORRECTNESS` | up@2.25ns=0.0000 expected=1.2000 tol=0.0800 |
| `267-pfd-up-down-state` | `FAIL_SIM_CORRECTNESS` | up@0.7ns=1.2000 expected=0.0000 tol=0.0800 |
| `267-pfd-up-down-state` | `FAIL_SIM_CORRECTNESS` | up@1.5ns=1.2000 expected=0.0000 tol=0.0800 |
| `267-pfd-up-down-state` | `FAIL_SIM_CORRECTNESS` | up@1.5ns=1.2000 expected=0.0000 tol=0.0800 |
| `267-pfd-up-down-state` | `FAIL_SIM_CORRECTNESS` | up@2.25ns=0.5040 expected=1.2000 tol=0.0800 |
| `268-samplehold-rising-edge` | `FAIL_SIM_CORRECTNESS` | vout@0.8ns=0.0000 expected=1.0000 tol=0.0500 |
| `268-samplehold-rising-edge` | `FAIL_SIM_CORRECTNESS` | vout@0.8ns=0.5000 expected=1.0000 tol=0.0500 |
| `268-samplehold-rising-edge` | `FAIL_SIM_CORRECTNESS` | vout@0.3ns=1.0000 expected=0.0000 tol=0.0500 |
| `268-samplehold-rising-edge` | `FAIL_SIM_CORRECTNESS` | vout@0.8ns=0.0000 expected=1.0000 tol=0.0500 |
| `268-samplehold-rising-edge` | `FAIL_SIM_CORRECTNESS` | vout@0.8ns=0.4200 expected=1.0000 tol=0.0500 |
| `269-trim-ctrl-5bit` | `FAIL_SIM_CORRECTNESS` | dout0@1.2ns=0.0000 expected=0.9000 tol=0.0500 |
| `269-trim-ctrl-5bit` | `FAIL_SIM_CORRECTNESS` | dout0@0.5ns=0.9000 expected=0.0000 tol=0.0500 |
| `269-trim-ctrl-5bit` | `FAIL_SIM_CORRECTNESS` | dout0@2.1ns=0.9000 expected=0.0000 tol=0.0500 |
| `269-trim-ctrl-5bit` | `FAIL_SIM_CORRECTNESS` | dout0@1.2ns=0.0000 expected=0.9000 tol=0.0500 |
| `269-trim-ctrl-5bit` | `FAIL_SIM_CORRECTNESS` | dout0@1.2ns=0.3780 expected=0.9000 tol=0.0500 |
| `270-therm8-to-bin4-count` | `FAIL_SIM_CORRECTNESS` | b0@1.2ns=0.0000 expected=0.9000 tol=0.0500 |
| `270-therm8-to-bin4-count` | `FAIL_SIM_CORRECTNESS` | b0@2.1ns=0.0000 expected=0.9000 tol=0.0500 |
| `270-therm8-to-bin4-count` | `FAIL_SIM_CORRECTNESS` | b0@1.2ns=0.0000 expected=0.9000 tol=0.0500 |
| `270-therm8-to-bin4-count` | `FAIL_SIM_CORRECTNESS` | b0@1.2ns=0.0000 expected=0.9000 tol=0.0500 |
| `270-therm8-to-bin4-count` | `FAIL_SIM_CORRECTNESS` | b0@1.2ns=0.3780 expected=0.9000 tol=0.0500 |
| `271-coarse-qtz-3bit-residue` | `FAIL_SIM_CORRECTNESS` | checked=78 low_clip=True high_clip=True internal=True max_bit_error=1.00000 max_res_error=0.25000 |
| `271-coarse-qtz-3bit-residue` | `FAIL_SIM_CORRECTNESS` | checked=78 low_clip=True high_clip=True internal=True max_bit_error=1.00000 max_res_error=0.25000 |
| `271-coarse-qtz-3bit-residue` | `FAIL_SIM_CORRECTNESS` | checked=78 low_clip=True high_clip=True internal=True max_bit_error=0.00000 max_res_error=0.50000 |
| `271-coarse-qtz-3bit-residue` | `FAIL_SIM_CORRECTNESS` | checked=78 low_clip=True high_clip=True internal=True max_bit_error=0.00000 max_res_error=0.50000 |
| `271-coarse-qtz-3bit-residue` | `FAIL_SIM_CORRECTNESS` | checked=78 low_clip=True high_clip=True internal=True max_bit_error=0.58000 max_res_error=0.00000 |
| `272-rs-phase-detector` | `FAIL_SIM_CORRECTNESS` | up@0.8ns=0.0000 expected=1.2000 tol=0.0800 |
| `272-rs-phase-detector` | `FAIL_SIM_CORRECTNESS` | up@0.8ns=0.0000 expected=1.2000 tol=0.0800 |
| `272-rs-phase-detector` | `FAIL_SIM_CORRECTNESS` | down@0.2ns=0.0000 expected=1.2000 tol=0.0800 |
| `272-rs-phase-detector` | `FAIL_SIM_CORRECTNESS` | up@1.4ns=1.2000 expected=0.0000 tol=0.0800 |
| `272-rs-phase-detector` | `FAIL_SIM_CORRECTNESS` | up@0.8ns=0.5040 expected=1.2000 tol=0.0800 |
| `273-level-shifter-offset` | `FAIL_SIM_CORRECTNESS` | sigout@0.4ns=0.1000 expected=0.4500 tol=0.0200 |
| `273-level-shifter-offset` | `FAIL_SIM_CORRECTNESS` | sigout@0.4ns=0.3000 expected=0.4500 tol=0.0200 |
| `273-level-shifter-offset` | `FAIL_SIM_CORRECTNESS` | sigout@0.4ns=-0.2500 expected=0.4500 tol=0.0200 |
| `273-level-shifter-offset` | `FAIL_SIM_CORRECTNESS` | sigout@0.4ns=0.5500 expected=0.4500 tol=0.0200 |
| `273-level-shifter-offset` | `FAIL_SIM_CORRECTNESS` | sigout@0.4ns=0.1890 expected=0.4500 tol=0.0200 |
| `274-weighted-decoder-6bit` | `FAIL_SIM_CORRECTNESS` | checked=643 max_weighted_error=0.84127 worst_code=110101 |
| `274-weighted-decoder-6bit` | `FAIL_SIM_CORRECTNESS` | checked=643 max_weighted_error=0.81498 worst_code=110101 |
| `274-weighted-decoder-6bit` | `FAIL_SIM_CORRECTNESS` | checked=643 max_weighted_error=0.42063 worst_code=110101 |
| `274-weighted-decoder-6bit` | `FAIL_SIM_CORRECTNESS` | checked=643 max_weighted_error=0.84127 worst_code=110101 |
| `274-weighted-decoder-6bit` | `FAIL_SIM_CORRECTNESS` | checked=643 max_weighted_error=0.48794 worst_code=110101 |
| `275-divide-by-two-toggle` | `FAIL_SIM_CORRECTNESS` | out@0.8ns=0.0000 expected=0.9000 tol=0.0600 |
| `275-divide-by-two-toggle` | `FAIL_SIM_CORRECTNESS` | out@0.8ns=0.0000 expected=0.9000 tol=0.0600 |
| `275-divide-by-two-toggle` | `FAIL_SIM_CORRECTNESS` | out@0.2ns=0.9000 expected=0.0000 tol=0.0600 |
| `275-divide-by-two-toggle` | `FAIL_SIM_CORRECTNESS` | out@1.6ns=0.9000 expected=0.0000 tol=0.0600 |
| `275-divide-by-two-toggle` | `FAIL_SIM_CORRECTNESS` | out@0.8ns=0.3780 expected=0.9000 tol=0.0600 |
| `276-accum3-pulse` | `FAIL_SIM_CORRECTNESS` | out@0.8ns=0.0000 expected=0.9000 tol=0.0600 |
| `276-accum3-pulse` | `FAIL_SIM_CORRECTNESS` | out@0.2ns=0.9000 expected=0.0000 tol=0.0600 |
| `276-accum3-pulse` | `FAIL_SIM_CORRECTNESS` | out@0.8ns=0.0000 expected=0.9000 tol=0.0600 |
| `276-accum3-pulse` | `FAIL_SIM_CORRECTNESS` | out@1.8ns=0.9000 expected=0.0000 tol=0.0600 |
| `276-accum3-pulse` | `FAIL_SIM_CORRECTNESS` | out@0.8ns=0.3780 expected=0.9000 tol=0.0600 |
| `277-xor-phase-detector` | `FAIL_SIM_CORRECTNESS` | up@1.2ns=0.0000 expected=1.2000 tol=0.0600 |
| `277-xor-phase-detector` | `FAIL_SIM_CORRECTNESS` | up@0.4ns=1.2000 expected=0.0000 tol=0.0600 |
| `277-xor-phase-detector` | `FAIL_SIM_CORRECTNESS` | down@0.4ns=0.0000 expected=1.2000 tol=0.0600 |
| `277-xor-phase-detector` | `FAIL_SIM_CORRECTNESS` | up@2ns=1.2000 expected=0.0000 tol=0.0600 |
| `277-xor-phase-detector` | `FAIL_SIM_CORRECTNESS` | up@1.2ns=0.5040 expected=1.2000 tol=0.0600 |
| `278-decision-router-logic` | `FAIL_SIM_CORRECTNESS` | x@1.2ns=0.0000 expected=0.9000 tol=0.0500 |
| `278-decision-router-logic` | `FAIL_SIM_CORRECTNESS` | x@0.4ns=0.9000 expected=0.0000 tol=0.0500 |
| `278-decision-router-logic` | `FAIL_SIM_CORRECTNESS` | dm@2ns=0.9000 expected=0.0000 tol=0.0500 |
| `278-decision-router-logic` | `FAIL_SIM_CORRECTNESS` | y@3.5ns=0.9000 expected=0.0000 tol=0.0500 |
| `278-decision-router-logic` | `FAIL_SIM_CORRECTNESS` | x@1.2ns=0.3780 expected=0.9000 tol=0.0500 |
| `279-safe-analog-divider` | `FAIL_SIM_CORRECTNESS` | sigout@0.4ns=0.0000 expected=0.3000 tol=0.0400 |
| `279-safe-analog-divider` | `FAIL_SIM_CORRECTNESS` | sigout@1.2ns=12.0000 expected=3.0000 tol=0.0400 |
| `279-safe-analog-divider` | `FAIL_SIM_CORRECTNESS` | sigout@2ns=3.0000 expected=-3.0000 tol=0.0400 |
| `279-safe-analog-divider` | `FAIL_SIM_CORRECTNESS` | sigout@0.4ns=0.1500 expected=0.3000 tol=0.0400 |
| `279-safe-analog-divider` | `FAIL_SIM_CORRECTNESS` | sigout@0.4ns=0.1260 expected=0.3000 tol=0.0400 |
| `280-vargain-diffamp-clip` | `FAIL_SIM_CORRECTNESS` | sigout@0.4ns=0.0000 expected=0.3750 tol=0.0400 |
| `280-vargain-diffamp-clip` | `FAIL_SIM_CORRECTNESS` | sigout@0.4ns=0.4500 expected=0.3750 tol=0.0400 |
| `280-vargain-diffamp-clip` | `FAIL_SIM_CORRECTNESS` | sigout@0.4ns=-0.3750 expected=0.3750 tol=0.0400 |
| `280-vargain-diffamp-clip` | `FAIL_SIM_CORRECTNESS` | sigout@1.2ns=1.6500 expected=1.0000 tol=0.0400 |
| `280-vargain-diffamp-clip` | `FAIL_SIM_CORRECTNESS` | sigout@0.4ns=0.1575 expected=0.3750 tol=0.0400 |
| `281-programmable-divider-by-n` | `FAIL_SIM_CORRECTNESS` | out@0.2ns=0.0000 expected=0.9000 tol=0.0600 |
| `281-programmable-divider-by-n` | `FAIL_SIM_CORRECTNESS` | out@1.4ns=0.9000 expected=0.0000 tol=0.0600 |
| `281-programmable-divider-by-n` | `FAIL_SIM_CORRECTNESS` | out@0.6ns=0.9000 expected=0.0000 tol=0.0600 |
| `281-programmable-divider-by-n` | `FAIL_SIM_CORRECTNESS` | out@0.2ns=0.0000 expected=0.9000 tol=0.0600 |
| `281-programmable-divider-by-n` | `FAIL_SIM_CORRECTNESS` | out@0.2ns=0.3780 expected=0.9000 tol=0.0600 |
| `282-pfd-timer-reset` | `FAIL_SIM_CORRECTNESS` | checked=1814 pfd_actions=9 max_pfd_error=0.90000 |
| `282-pfd-timer-reset` | `FAIL_SIM_CORRECTNESS` | checked=1814 pfd_actions=9 max_pfd_error=0.90000 |
| `282-pfd-timer-reset` | `FAIL_SIM_CORRECTNESS` | checked=1814 pfd_actions=9 max_pfd_error=0.90000 |
| `282-pfd-timer-reset` | `FAIL_SIM_CORRECTNESS` | checked=1814 pfd_actions=9 max_pfd_error=0.90000 |
| `282-pfd-timer-reset` | `FAIL_SIM_CORRECTNESS` | checked=1814 pfd_actions=9 max_pfd_error=0.52200 |
| `283-weighted-sar-adc-dac-loop` | `FAIL_SIM_CORRECTNESS` | streaming_checker:public_contract |
| `283-weighted-sar-adc-dac-loop` | `FAIL_SIM_CORRECTNESS` | streaming_checker:public_contract |
| `283-weighted-sar-adc-dac-loop` | `FAIL_SIM_CORRECTNESS` | streaming_checker:public_contract |
| `283-weighted-sar-adc-dac-loop` | `FAIL_SIM_CORRECTNESS` | streaming_checker:public_contract |
| `283-weighted-sar-adc-dac-loop` | `FAIL_SIM_CORRECTNESS` | streaming_checker:public_contract |
| `284-window-comparator-testbench` | `FAIL_SIM_CORRECTNESS` | streaming_checker:out_span_too_small=0.000 |
| `284-window-comparator-testbench` | `FAIL_SIM_CORRECTNESS` | streaming_checker:insufficient_window_samples below=130 above=0 rise=58 fall=57 |
| `284-window-comparator-testbench` | `FAIL_SIM_CORRECTNESS` | streaming_checker:insufficient_window_samples below=37 above=217 rise=45 fall=0 |
| `284-window-comparator-testbench` | `FAIL_SIM_CORRECTNESS` | streaming_checker:insufficient_window_samples below=0 above=145 rise=45 fall=44 |
| `284-window-comparator-testbench` | `FAIL_SIM_CORRECTNESS` | streaming_checker:insufficient_window_samples below=14 above=308 rise=16 fall=0 |
| `285-aperture-delay-sample-hold` | `FAIL_SIM_CORRECTNESS` | aperture_samples=0.100,0.350,0.600,0.250,0.700,0.400,0.800 expected=0.350,0.600,0.250,0.700,0.400,0.800,0.800 mismatches=6 span=0.700 |
| `285-aperture-delay-sample-hold` | `FAIL_SIM_CORRECTNESS` | aperture_samples=0.147,0.252,0.105,0.294,0.168,0.336,0.336 expected=0.350,0.600,0.250,0.700,0.400,0.800,0.800 mismatches=7 span=0.231 |
| `285-aperture-delay-sample-hold` | `FAIL_SIM_CORRECTNESS` | aperture_samples=0.042,0.147,0.252,0.105,0.294,0.168,0.336 expected=0.350,0.600,0.250,0.700,0.400,0.800,0.800 mismatches=6 span=0.294 |
| `285-aperture-delay-sample-hold` | `FAIL_SIM_CORRECTNESS` | aperture_samples=0.147,0.252,0.105,0.294,0.168,0.336,0.336 expected=0.350,0.600,0.250,0.700,0.400,0.800,0.800 mismatches=7 span=0.231 |
| `285-aperture-delay-sample-hold` | `FAIL_SIM_CORRECTNESS` | aperture_samples=0.147,0.252,0.105,0.294,0.168,0.336,0.336 expected=0.350,0.600,0.250,0.700,0.400,0.800,0.800 mismatches=7 span=0.231 |
| `286-first-order-lowpass-bugfix` | `FAIL_SIM_CORRECTNESS` | configured_lowpass_samples=0.136,0.356,0.601,0.740 input_step=True monotonic=True response_fast_enough=False not_instant=True bounded=True checker_config_parameters=first_order_lowpass |
| `286-first-order-lowpass-bugfix` | `FAIL_SIM_CORRECTNESS` | configured_lowpass_samples=0.800,0.800,0.800,0.800 input_step=True monotonic=False response_fast_enough=True not_instant=False bounded=True checker_config_parameters=first_order_lowpass |
| `286-first-order-lowpass-bugfix` | `FAIL_SIM_CORRECTNESS` | configured_lowpass_samples=0.412,0.213,0.115,0.101 input_step=True monotonic=False response_fast_enough=False not_instant=True bounded=True checker_config_parameters=first_order_lowpass |
| `286-first-order-lowpass-bugfix` | `FAIL_SIM_CORRECTNESS` | configured_lowpass_samples=0.299,0.350,0.350,0.350 input_step=True monotonic=False response_fast_enough=False not_instant=True bounded=True checker_config_parameters=first_order_lowpass |
| `286-first-order-lowpass-bugfix` | `FAIL_SIM_CORRECTNESS` | configured_lowpass_samples=0.126,0.260,0.326,0.336 input_step=True monotonic=True response_fast_enough=False not_instant=True bounded=True checker_config_parameters=first_order_lowpass |
| `287-gain-extraction-flow` | `FAIL_SIM_CORRECTNESS` | streaming_checker:diff_gain=1.28 |
| `287-gain-extraction-flow` | `FAIL_SIM_CORRECTNESS` | streaming_checker:diff_gain=2.17 |
| `287-gain-extraction-flow` | `FAIL_SIM_CORRECTNESS` | streaming_checker:diff_gain=2.17 |
| `287-gain-extraction-flow` | `FAIL_SIM_CORRECTNESS` | streaming_checker:diff_gain=2.17 |
| `287-gain-extraction-flow` | `FAIL_SIM_CORRECTNESS` | streaming_checker:diff_gain=2.17 |
| `288-absolute-value` | `FAIL_SIM_CORRECTNESS` | checked=641 max_abs_error=0.95000 |
| `288-absolute-value` | `FAIL_SIM_CORRECTNESS` | checked=641 max_abs_error=1.90000 |
| `288-absolute-value` | `FAIL_SIM_CORRECTNESS` | checked=641 max_abs_error=0.47500 |
| `288-absolute-value` | `FAIL_SIM_CORRECTNESS` | checked=641 max_abs_error=0.25000 |
| `288-absolute-value` | `FAIL_SIM_CORRECTNESS` | checked=641 max_abs_error=0.55100 |
| `289-deadband-voltage` | `FAIL_SIM_CORRECTNESS` | sigout@0.4ns=0.0000 expected=-0.4500 tol=0.0200 |
| `289-deadband-voltage` | `FAIL_SIM_CORRECTNESS` | sigout@0.4ns=-0.7000 expected=-0.4500 tol=0.0200 |
| `289-deadband-voltage` | `FAIL_SIM_CORRECTNESS` | sigout@0.4ns=-0.2000 expected=-0.4500 tol=0.0200 |
| `289-deadband-voltage` | `FAIL_SIM_CORRECTNESS` | sigout@0.4ns=0.4500 expected=-0.4500 tol=0.0200 |
| `289-deadband-voltage` | `FAIL_SIM_CORRECTNESS` | sigout@0.4ns=-0.1890 expected=-0.4500 tol=0.0200 |
| `290-deadband-diffamp` | `FAIL_SIM_CORRECTNESS` | sigout@0.4ns=0.0000 expected=-0.5800 tol=0.0300 |
| `290-deadband-diffamp` | `FAIL_SIM_CORRECTNESS` | sigout@0.4ns=-0.1800 expected=-0.5800 tol=0.0300 |
| `290-deadband-diffamp` | `FAIL_SIM_CORRECTNESS` | sigout@2.8ns=0.8200 expected=1.2200 tol=0.0300 |
| `290-deadband-diffamp` | `FAIL_SIM_CORRECTNESS` | sigout@0.4ns=0.9200 expected=-0.5800 tol=0.0300 |
| `290-deadband-diffamp` | `FAIL_SIM_CORRECTNESS` | sigout@0.4ns=-0.2436 expected=-0.5800 tol=0.0300 |
| `291-limiting-diffamp` | `FAIL_SIM_CORRECTNESS` | sigout@0.4ns=0.0000 expected=-0.7500 tol=0.0300 |
| `291-limiting-diffamp` | `FAIL_SIM_CORRECTNESS` | sigout@0.4ns=-1.2000 expected=-0.7500 tol=0.0300 |
| `291-limiting-diffamp` | `FAIL_SIM_CORRECTNESS` | sigout@0.4ns=-0.6000 expected=-0.7500 tol=0.0300 |
| `291-limiting-diffamp` | `FAIL_SIM_CORRECTNESS` | sigout@0.4ns=0.7500 expected=-0.7500 tol=0.0300 |
| `291-limiting-diffamp` | `FAIL_SIM_CORRECTNESS` | sigout@0.4ns=-0.3150 expected=-0.7500 tol=0.0300 |
| `292-hysteretic-comparator-receiver` | `FAIL_SIM_CORRECTNESS` | missing_rising_edges actual=0 expected=2 |
| `292-hysteretic-comparator-receiver` | `FAIL_SIM_CORRECTNESS` | falling_edge_delay_error got=5.377ns want=6.311ns err=933.9ps |
| `292-hysteretic-comparator-receiver` | `FAIL_SIM_CORRECTNESS` | rising_edge_delay_error got=1.010ns want=1.410ns err=400.0ps |
| `292-hysteretic-comparator-receiver` | `FAIL_SIM_CORRECTNESS` | rising_edge_delay_error got=3.383ns want=1.410ns err=1973.0ps |
| `292-hysteretic-comparator-receiver` | `FAIL_SIM_CORRECTNESS` | missing_rising_edges actual=0 expected=2 |
| `293-flash-folded-dac4` | `FAIL_SIM_CORRECTNESS` | vout@0.4ns=0.0000 expected=0.5000 tol=0.0300 |
| `293-flash-folded-dac4` | `FAIL_SIM_CORRECTNESS` | vout@0.4ns=0.0000 expected=0.5000 tol=0.0300 |
| `293-flash-folded-dac4` | `FAIL_SIM_CORRECTNESS` | vout@0.4ns=0.5333 expected=0.5000 tol=0.0300 |
| `293-flash-folded-dac4` | `FAIL_SIM_CORRECTNESS` | vout@1.2ns=0.7500 expected=0.2500 tol=0.0300 |
| `293-flash-folded-dac4` | `FAIL_SIM_CORRECTNESS` | vout@2ns=0.2625 expected=0.6250 tol=0.0300 |
| `294-subradix-dac10` | `FAIL_SIM_CORRECTNESS` | checked=643 max_weighted_error=0.77973 worst_code=1100111100 |
| `294-subradix-dac10` | `FAIL_SIM_CORRECTNESS` | checked=643 max_weighted_error=0.03181 worst_code=1010001101 |
| `294-subradix-dac10` | `FAIL_SIM_CORRECTNESS` | checked=643 max_weighted_error=0.10195 worst_code=1100111100 |
| `294-subradix-dac10` | `FAIL_SIM_CORRECTNESS` | checked=643 max_weighted_error=0.65529 worst_code=1100111100 |
| `294-subradix-dac10` | `FAIL_SIM_CORRECTNESS` | checked=643 max_weighted_error=0.45224 worst_code=1100111100 |
| `295-clocked-adc3bit` | `FAIL_SIM_CORRECTNESS` | clocked_adc3bit_max_err=0.9000 codes=[0, 1, 4, 7] |
| `295-clocked-adc3bit` | `FAIL_SIM_CORRECTNESS` | clocked_adc3bit_max_err=0.9000 codes=[0, 1, 4, 7] |
| `295-clocked-adc3bit` | `FAIL_SIM_CORRECTNESS` | clocked_adc3bit_max_err=0.9000 codes=[0, 1, 4, 7] |
| `295-clocked-adc3bit` | `FAIL_SIM_CORRECTNESS` | clocked_adc3bit_max_err=0.9000 codes=[0, 1, 4, 7] |
| `295-clocked-adc3bit` | `FAIL_SIM_CORRECTNESS` | clocked_adc3bit_max_err=0.5220 codes=[0, 1, 4, 7] |
| `296-cal4bit-modulo` | `FAIL_SIM_CORRECTNESS` | d0@1.2ns=0.0000 expected=0.9000 tol=0.0600 |
| `296-cal4bit-modulo` | `FAIL_SIM_CORRECTNESS` | d0@0.4ns=0.9000 expected=0.0000 tol=0.0600 |
| `296-cal4bit-modulo` | `FAIL_SIM_CORRECTNESS` | d0@1.2ns=0.0000 expected=0.9000 tol=0.0600 |
| `296-cal4bit-modulo` | `FAIL_SIM_CORRECTNESS` | d0@1.2ns=0.0000 expected=0.9000 tol=0.0600 |
| `296-cal4bit-modulo` | `FAIL_SIM_CORRECTNESS` | d0@1.2ns=0.3780 expected=0.9000 tol=0.0600 |
| `297-mux4-priority` | `FAIL_SIM_CORRECTNESS` | out@0.4ns=0.0000 expected=0.1000 tol=0.0200 |
| `297-mux4-priority` | `FAIL_SIM_CORRECTNESS` | out@1.2ns=-0.2000 expected=0.4000 tol=0.0200 |
| `297-mux4-priority` | `FAIL_SIM_CORRECTNESS` | out@0.4ns=0.8000 expected=0.1000 tol=0.0200 |
| `297-mux4-priority` | `FAIL_SIM_CORRECTNESS` | out@1.2ns=0.1000 expected=0.4000 tol=0.0200 |
| `297-mux4-priority` | `FAIL_SIM_CORRECTNESS` | out@0.4ns=0.0420 expected=0.1000 tol=0.0200 |
| `298-xnor-gate-voltage` | `FAIL_SIM_CORRECTNESS` | vout@0.4ns=0.0000 expected=0.9000 tol=0.0600 |
| `298-xnor-gate-voltage` | `FAIL_SIM_CORRECTNESS` | vout@0.4ns=0.0000 expected=0.9000 tol=0.0600 |
| `298-xnor-gate-voltage` | `FAIL_SIM_CORRECTNESS` | vout@0.4ns=0.0000 expected=0.9000 tol=0.0600 |
| `298-xnor-gate-voltage` | `FAIL_SIM_CORRECTNESS` | vout@2.8ns=0.0000 expected=0.9000 tol=0.0600 |
| `298-xnor-gate-voltage` | `FAIL_SIM_CORRECTNESS` | vout@0.4ns=0.3780 expected=0.9000 tol=0.0600 |
| `299-bipolar-dff-sample` | `FAIL_SIM_CORRECTNESS` | vout_q@0.6ns=0.0000 expected=-1.0000 tol=0.0800 |
| `299-bipolar-dff-sample` | `FAIL_SIM_CORRECTNESS` | vout_qbar@0.6ns=-1.0000 expected=1.0000 tol=0.0800 |
| `299-bipolar-dff-sample` | `FAIL_SIM_CORRECTNESS` | vout_q@0.6ns=1.0000 expected=-1.0000 tol=0.0800 |
| `299-bipolar-dff-sample` | `FAIL_SIM_CORRECTNESS` | vout_q@2.9ns=-1.0000 expected=1.0000 tol=0.0800 |
| `299-bipolar-dff-sample` | `FAIL_SIM_CORRECTNESS` | vout_q@0.6ns=-0.4200 expected=-1.0000 tol=0.0800 |
| `300-pfd-active-low-reset` | `FAIL_SIM_CORRECTNESS` | checked=1614 pfd_actions=9 max_pfd_error=0.90000 |
| `300-pfd-active-low-reset` | `FAIL_SIM_CORRECTNESS` | checked=1614 pfd_actions=9 max_pfd_error=0.90000 |
| `300-pfd-active-low-reset` | `FAIL_SIM_CORRECTNESS` | checked=1614 pfd_actions=9 max_pfd_error=0.90000 |
| `300-pfd-active-low-reset` | `FAIL_SIM_CORRECTNESS` | checked=1614 pfd_actions=9 max_pfd_error=0.90000 |
| `300-pfd-active-low-reset` | `FAIL_SIM_CORRECTNESS` | checked=1614 pfd_actions=9 max_pfd_error=0.52200 |
| `301-function-clamp-window` | `FAIL_SIM_CORRECTNESS` | sample0_out=0.0000_expected=0.1000;sample1_out=0.0000_expected=0.1000;sample2_out=0.0000_expected=0.3700;sample3_out=0.0000_expected=0.4500;sample4_out=0.0000_expected=0.5300;sample5_out=0.0000_expected=0.7800;sample6_out=0.0000_expected=0.8000;sample7_out=0.0000_expected=0.8000 |
| `301-function-clamp-window` | `FAIL_SIM_CORRECTNESS` | sample0_metric=0.0000_expected=0.1111;sample1_metric=0.0000_expected=0.1111;sample2_metric=0.0000_expected=0.4111;sample3_metric=0.0000_expected=0.5000;sample4_metric=0.0000_expected=0.5889;sample5_metric=0.0000_expected=0.8667;sample6_metric=0.0000_expected=0.8889;sample7_metric=0.0000_expected=0.8889 |
| `301-function-clamp-window` | `FAIL_SIM_CORRECTNESS` | sample0_out=0.0000_expected=0.1000;sample0_metric=0.0000_expected=0.1111 |
| `301-function-clamp-window` | `FAIL_SIM_CORRECTNESS` | sample6_out=0.9000_expected=0.8000;sample6_metric=1.0000_expected=0.8889;sample7_out=0.9000_expected=0.8000;sample7_metric=1.0000_expected=0.8889 |
| `301-function-clamp-window` | `FAIL_SIM_CORRECTNESS` | sample2_metric=0.5139_expected=0.4111;sample3_metric=0.6250_expected=0.5000;sample4_metric=0.7361_expected=0.5889;sample5_metric=1.0833_expected=0.8667;sample6_metric=1.1111_expected=0.8889;sample7_metric=1.1111_expected=0.8889 |
| `302-function-deadband-map` | `FAIL_SIM_CORRECTNESS` | sample3_out=0.0000_expected=0.4500;sample4_out=0.0000_expected=0.9000;sample5_out=0.0000_expected=0.9000;sample6_out=0.0000_expected=0.9000;sample7_out=0.0000_expected=0.9000 |
| `302-function-deadband-map` | `FAIL_SIM_CORRECTNESS` | sample0_metric=0.0000_expected=-1.0000;sample1_metric=0.0000_expected=-1.0000;sample2_metric=0.0000_expected=-1.0000;sample4_metric=0.0000_expected=1.0000;sample5_metric=0.0000_expected=1.0000;sample6_metric=0.0000_expected=1.0000;sample7_metric=0.0000_expected=1.0000 |
| `302-function-deadband-map` | `FAIL_SIM_CORRECTNESS` | sample2_out=0.4500_expected=0.0000;sample2_metric=0.0000_expected=-1.0000 |
| `302-function-deadband-map` | `FAIL_SIM_CORRECTNESS` | sample4_out=0.4500_expected=0.9000;sample4_metric=0.0000_expected=1.0000 |
| `302-function-deadband-map` | `FAIL_SIM_CORRECTNESS` | sample0_metric=0.0000_expected=-1.0000;sample1_metric=0.0000_expected=-1.0000;sample2_metric=0.0000_expected=-1.0000;sample3_metric=0.6250_expected=0.0000;sample4_metric=1.2500_expected=1.0000;sample5_metric=1.2500_expected=1.0000;sample6_metric=1.2500_expected=1.0000;sample7_metric=1.2500_expected=1.0000 |
| `303-function-piecewise-gain` | `FAIL_SIM_CORRECTNESS` | sample1_out=0.0000_expected=0.0500;sample2_out=0.0000_expected=0.3700;sample3_out=0.0000_expected=0.4500;sample4_out=0.0000_expected=0.5300;sample5_out=0.0000_expected=0.6825;sample6_out=0.0000_expected=0.6925;sample7_out=0.0000_expected=0.7125 |
| `303-function-piecewise-gain` | `FAIL_SIM_CORRECTNESS` | sample1_metric=0.0000_expected=0.0500;sample2_metric=0.0000_expected=0.3700;sample3_metric=0.0000_expected=0.4500;sample4_metric=0.0000_expected=0.5300;sample5_metric=0.0000_expected=0.6825;sample6_metric=0.0000_expected=0.6925;sample7_metric=0.0000_expected=0.7125 |
| `303-function-piecewise-gain` | `FAIL_SIM_CORRECTNESS` | sample1_out=0.0000_expected=0.0500;sample1_metric=0.0000_expected=0.0500 |
| `303-function-piecewise-gain` | `FAIL_SIM_CORRECTNESS` | sample5_out=0.7150_expected=0.6825;sample5_metric=0.7150_expected=0.6825;sample6_out=0.7350_expected=0.6925;sample6_metric=0.7350_expected=0.6925;sample7_out=0.7750_expected=0.7125;sample7_metric=0.7750_expected=0.7125 |
| `303-function-piecewise-gain` | `FAIL_SIM_CORRECTNESS` | sample2_metric=0.5139_expected=0.3700;sample3_metric=0.6250_expected=0.4500;sample4_metric=0.7361_expected=0.5300;sample5_metric=0.9479_expected=0.6825;sample6_metric=0.9618_expected=0.6925;sample7_metric=0.9896_expected=0.7125 |
| `304-function-code-normalizer` | `FAIL_SIM_CORRECTNESS` | sample1_out=0.0000_expected=0.0600;sample2_out=0.0000_expected=0.3600;sample3_out=0.0000_expected=0.4800;sample4_out=0.0000_expected=0.5400;sample5_out=0.0000_expected=0.7800;sample6_out=0.0000_expected=0.8400;sample7_out=0.0000_expected=0.9000 |
| `304-function-code-normalizer` | `FAIL_SIM_CORRECTNESS` | sample1_metric=0.0000_expected=0.0667;sample2_metric=0.0000_expected=0.4000;sample3_metric=0.0000_expected=0.5333;sample4_metric=0.0000_expected=0.6000;sample5_metric=0.0000_expected=0.8667;sample6_metric=0.0000_expected=0.9333;sample7_metric=0.0000_expected=1.0000 |
| `304-function-code-normalizer` | `FAIL_SIM_CORRECTNESS` | sample3_out=0.4200_expected=0.4800;sample3_metric=0.4667_expected=0.5333;sample4_out=0.4800_expected=0.5400;sample4_metric=0.5333_expected=0.6000;sample6_out=0.7800_expected=0.8400;sample6_metric=0.8667_expected=0.9333 |
| `304-function-code-normalizer` | `FAIL_SIM_CORRECTNESS` | sample7_out=0.8400_expected=0.9000;sample7_metric=0.9333_expected=1.0000 |
| `304-function-code-normalizer` | `FAIL_SIM_CORRECTNESS` | sample2_metric=0.5000_expected=0.4000;sample3_metric=0.6667_expected=0.5333;sample4_metric=0.7500_expected=0.6000;sample5_metric=1.0833_expected=0.8667;sample6_metric=1.1667_expected=0.9333;sample7_metric=1.2500_expected=1.0000 |
| `305-function-soft-threshold` | `FAIL_SIM_CORRECTNESS` | sample2_out=0.0000_expected=0.1958;sample3_out=0.0000_expected=0.4500;sample4_out=0.0000_expected=0.7042;sample5_out=0.0000_expected=0.8960;sample6_out=0.0000_expected=0.8973;sample7_out=0.0000_expected=0.8993 |
| `305-function-soft-threshold` | `FAIL_SIM_CORRECTNESS` | sample2_metric=0.0000_expected=0.1958;sample3_metric=0.0000_expected=0.4500;sample4_metric=0.0000_expected=0.7042;sample5_metric=0.0000_expected=0.8960;sample6_metric=0.0000_expected=0.8973;sample7_metric=0.0000_expected=0.8993 |
| `305-function-soft-threshold` | `FAIL_SIM_CORRECTNESS` | sample2_out=0.2492_expected=0.1958;sample2_metric=0.2492_expected=0.1958;sample4_out=0.6508_expected=0.7042;sample4_metric=0.6508_expected=0.7042 |
| `305-function-soft-threshold` | `FAIL_SIM_CORRECTNESS` | sample2_out=0.1000_expected=0.1958;sample2_metric=0.1000_expected=0.1958;sample3_out=0.2790_expected=0.4500;sample3_metric=0.2790_expected=0.4500;sample4_out=0.5560_expected=0.7042;sample4_metric=0.5560_expected=0.7042 |
| `305-function-soft-threshold` | `FAIL_SIM_CORRECTNESS` | sample2_metric=0.2719_expected=0.1958;sample3_metric=0.6250_expected=0.4500;sample4_metric=0.9781_expected=0.7042;sample5_metric=1.2437_expected=0.8960;sample6_metric=1.2467_expected=0.8973;sample7_metric=1.2491_expected=0.8993 |
| `306-case-mode-gain-selector` | `FAIL_SIM_CORRECTNESS` | out@17ns=0.0000 expected=0.1600 tol=0.0250 |
| `306-case-mode-gain-selector` | `FAIL_SIM_CORRECTNESS` | metric@27ns=0.0000 expected=0.3000 tol=0.0250 |
| `306-case-mode-gain-selector` | `FAIL_SIM_CORRECTNESS` | out@7ns=0.1600 expected=0.0000 tol=0.0250 |
| `306-case-mode-gain-selector` | `FAIL_SIM_CORRECTNESS` | out@27ns=0.1600 expected=0.4000 tol=0.0250 |
| `306-case-mode-gain-selector` | `FAIL_SIM_CORRECTNESS` | out@47ns=0.6400 expected=0.8000 tol=0.0250 |
| `307-case-priority-status-decoder` | `FAIL_SIM_CORRECTNESS` | out@27ns=0.0000 expected=0.3000 tol=0.0250 |
| `307-case-priority-status-decoder` | `FAIL_SIM_CORRECTNESS` | out@17ns=0.0400 expected=0.0000 tol=0.0250 |
| `307-case-priority-status-decoder` | `FAIL_SIM_CORRECTNESS` | out@7ns=0.0400 expected=0.0000 tol=0.0250 |
| `307-case-priority-status-decoder` | `FAIL_SIM_CORRECTNESS` | out@17ns=0.0400 expected=0.0000 tol=0.0250 |
| `307-case-priority-status-decoder` | `FAIL_SIM_CORRECTNESS` | out@17ns=0.0400 expected=0.0000 tol=0.0250 |
| `308-case-quantized-output-level` | `FAIL_SIM_CORRECTNESS` | out@27ns=0.0000 expected=0.3000 tol=0.0250 |
| `308-case-quantized-output-level` | `FAIL_SIM_CORRECTNESS` | out@27ns=0.0600 expected=0.3000 tol=0.0250 |
| `308-case-quantized-output-level` | `FAIL_SIM_CORRECTNESS` | out@27ns=0.0000 expected=0.3000 tol=0.0250 |
| `308-case-quantized-output-level` | `FAIL_SIM_CORRECTNESS` | out@27ns=0.0600 expected=0.3000 tol=0.0250 |
| `308-case-quantized-output-level` | `FAIL_SIM_CORRECTNESS` | out@27ns=0.0600 expected=0.3000 tol=0.0250 |
| `309-case-clocked-range-bucket` | `FAIL_SIM_CORRECTNESS` | out@17ns=0.0000 expected=0.1000 tol=0.0250 |
| `309-case-clocked-range-bucket` | `FAIL_SIM_CORRECTNESS` | out@17ns=0.0400 expected=0.1000 tol=0.0250 |
| `309-case-clocked-range-bucket` | `FAIL_SIM_CORRECTNESS` | out@7ns=0.0400 expected=0.0000 tol=0.0250 |
| `309-case-clocked-range-bucket` | `FAIL_SIM_CORRECTNESS` | out@17ns=0.0400 expected=0.1000 tol=0.0250 |
| `309-case-clocked-range-bucket` | `FAIL_SIM_CORRECTNESS` | out@17ns=0.0400 expected=0.1000 tol=0.0250 |
| `310-case-resettable-state-decoder` | `FAIL_SIM_CORRECTNESS` | out@17ns=0.0000 expected=0.3000 tol=0.0250 |
| `310-case-resettable-state-decoder` | `FAIL_SIM_CORRECTNESS` | out@17ns=0.5000 expected=0.3000 tol=0.0250 |
| `310-case-resettable-state-decoder` | `FAIL_SIM_CORRECTNESS` | out@7ns=0.5000 expected=0.0000 tol=0.0250 |
| `310-case-resettable-state-decoder` | `FAIL_SIM_CORRECTNESS` | out@17ns=0.5000 expected=0.3000 tol=0.0250 |
| `310-case-resettable-state-decoder` | `FAIL_SIM_CORRECTNESS` | out@17ns=0.5000 expected=0.3000 tol=0.0250 |
| `311-for-loop-running-average` | `FAIL_SIM_CORRECTNESS` | out@17ns=0.0000 expected=0.0500 tol=0.0250 |
| `311-for-loop-running-average` | `FAIL_SIM_CORRECTNESS` | out@47ns=0.4000 expected=0.5000 tol=0.0250 |
| `311-for-loop-running-average` | `FAIL_SIM_CORRECTNESS` | out@47ns=0.4000 expected=0.5000 tol=0.0250 |
| `311-for-loop-running-average` | `FAIL_SIM_CORRECTNESS` | out@47ns=0.4000 expected=0.5000 tol=0.0250 |
| `311-for-loop-running-average` | `FAIL_SIM_CORRECTNESS` | out@47ns=0.4000 expected=0.5000 tol=0.0250 |
| `312-for-loop-thermometer-count` | `FAIL_SIM_CORRECTNESS` | out@27ns=0.0000 expected=0.2250 tol=0.0250 |
| `312-for-loop-thermometer-count` | `FAIL_SIM_CORRECTNESS` | out@17ns=0.0300 expected=0.0000 tol=0.0250 |
| `312-for-loop-thermometer-count` | `FAIL_SIM_CORRECTNESS` | out@17ns=0.0300 expected=0.0000 tol=0.0250 |
| `312-for-loop-thermometer-count` | `FAIL_SIM_CORRECTNESS` | out@17ns=0.0300 expected=0.0000 tol=0.0250 |
| `312-for-loop-thermometer-count` | `FAIL_SIM_CORRECTNESS` | out@17ns=0.0300 expected=0.0000 tol=0.0250 |
| `313-for-loop-weighted-accumulator` | `FAIL_SIM_CORRECTNESS` | out@17ns=0.0000 expected=0.0400 tol=0.0350 |
| `313-for-loop-weighted-accumulator` | `FAIL_SIM_CORRECTNESS` | out@27ns=0.0700 expected=0.1100 tol=0.0350 |
| `313-for-loop-weighted-accumulator` | `FAIL_SIM_CORRECTNESS` | out@27ns=0.0700 expected=0.1100 tol=0.0350 |
| `313-for-loop-weighted-accumulator` | `FAIL_SIM_CORRECTNESS` | out@27ns=0.0700 expected=0.1100 tol=0.0350 |
| `313-for-loop-weighted-accumulator` | `FAIL_SIM_CORRECTNESS` | out@27ns=0.0700 expected=0.1100 tol=0.0350 |
| `314-for-loop-windowed-peak` | `FAIL_SIM_CORRECTNESS` | out@17ns=0.0000 expected=0.3000 tol=0.0250 |
| `314-for-loop-windowed-peak` | `FAIL_SIM_CORRECTNESS` | out@7ns=0.0300 expected=0.0000 tol=0.0250 |
| `314-for-loop-windowed-peak` | `FAIL_SIM_CORRECTNESS` | out@7ns=0.0300 expected=0.0000 tol=0.0250 |
| `314-for-loop-windowed-peak` | `FAIL_SIM_CORRECTNESS` | out@7ns=0.0300 expected=0.0000 tol=0.0250 |
| `314-for-loop-windowed-peak` | `FAIL_SIM_CORRECTNESS` | out@7ns=0.0300 expected=0.0000 tol=0.0250 |
| `315-for-loop-code-popcount` | `FAIL_SIM_CORRECTNESS` | out@27ns=0.0000 expected=0.2250 tol=0.0250 |
| `315-for-loop-code-popcount` | `FAIL_SIM_CORRECTNESS` | out@17ns=0.0300 expected=0.0000 tol=0.0250 |
| `315-for-loop-code-popcount` | `FAIL_SIM_CORRECTNESS` | out@17ns=0.0300 expected=0.0000 tol=0.0250 |
| `315-for-loop-code-popcount` | `FAIL_SIM_CORRECTNESS` | out@17ns=0.0300 expected=0.0000 tol=0.0250 |
| `315-for-loop-code-popcount` | `FAIL_SIM_CORRECTNESS` | out@17ns=0.0300 expected=0.0000 tol=0.0250 |
| `316-final-step-edge-counter-file` | `FAIL_SIM_CORRECTNESS` | out@27ns=0.0000 expected=0.2250 tol=0.0250 |
| `316-final-step-edge-counter-file` | `FAIL_SIM_CORRECTNESS` | metric@27ns=0.0000 expected=0.2500 tol=0.0250 |
| `316-final-step-edge-counter-file` | `FAIL_SIM_CORRECTNESS` | out@7ns=0.2250 expected=0.0000 tol=0.0250 |
| `316-final-step-edge-counter-file` | `FAIL_SIM_CORRECTNESS` | out@27ns=0.0000 expected=0.2250 tol=0.0250 |
| `316-final-step-edge-counter-file` | `FAIL_SIM_CORRECTNESS` | out@47ns=0.4000 expected=0.4500 tol=0.0250 |
| `317-final-step-average-metric-file` | `FAIL_SIM_CORRECTNESS` | out@27ns=0.0000 expected=0.2250 tol=0.0250 |
| `317-final-step-average-metric-file` | `FAIL_SIM_CORRECTNESS` | metric@27ns=0.0000 expected=0.2500 tol=0.0250 |
| `317-final-step-average-metric-file` | `FAIL_SIM_CORRECTNESS` | out@7ns=0.9000 expected=0.0000 tol=0.0250 |
| `317-final-step-average-metric-file` | `FAIL_SIM_CORRECTNESS` | out@27ns=0.0000 expected=0.2250 tol=0.0250 |
| `317-final-step-average-metric-file` | `FAIL_SIM_CORRECTNESS` | out@27ns=0.1800 expected=0.2250 tol=0.0250 |
| `318-final-step-max-observer-file` | `FAIL_SIM_CORRECTNESS` | out@27ns=0.0000 expected=0.1800 tol=0.0250 |
| `318-final-step-max-observer-file` | `FAIL_SIM_CORRECTNESS` | metric@27ns=0.0000 expected=0.2000 tol=0.0250 |
| `318-final-step-max-observer-file` | `FAIL_SIM_CORRECTNESS` | out@7ns=0.9000 expected=0.0000 tol=0.0250 |
| `318-final-step-max-observer-file` | `FAIL_SIM_CORRECTNESS` | out@27ns=0.0000 expected=0.1800 tol=0.0250 |
| `318-final-step-max-observer-file` | `FAIL_SIM_CORRECTNESS` | out@27ns=0.1440 expected=0.1800 tol=0.0250 |
| `319-display-strobe-event-logger` | `FAIL_SIM_CORRECTNESS` | out@27ns=0.0000 expected=0.2250 tol=0.0250 |
| `319-display-strobe-event-logger` | `FAIL_SIM_CORRECTNESS` | metric@27ns=0.0000 expected=0.2500 tol=0.0250 |
| `319-display-strobe-event-logger` | `FAIL_SIM_CORRECTNESS` | out@7ns=0.9000 expected=0.0000 tol=0.0250 |
| `319-display-strobe-event-logger` | `FAIL_SIM_CORRECTNESS` | out@27ns=0.0000 expected=0.2250 tol=0.0250 |
| `319-display-strobe-event-logger` | `FAIL_SIM_CORRECTNESS` | out@27ns=0.1800 expected=0.2250 tol=0.0250 |
| `320-file-io-sampled-metric-writer` | `FAIL_SIM_CORRECTNESS` | out@27ns=0.0000 expected=0.1800 tol=0.0250 |
| `320-file-io-sampled-metric-writer` | `FAIL_SIM_CORRECTNESS` | metric@27ns=0.0000 expected=0.2000 tol=0.0250 |
| `320-file-io-sampled-metric-writer` | `FAIL_SIM_CORRECTNESS` | out@7ns=0.9000 expected=0.0000 tol=0.0250 |
| `320-file-io-sampled-metric-writer` | `FAIL_SIM_CORRECTNESS` | out@27ns=0.0000 expected=0.1800 tol=0.0250 |
| `320-file-io-sampled-metric-writer` | `FAIL_SIM_CORRECTNESS` | out=0.000,0.180,0.360,0.720,0.540 metric=0.000,0.200,0.400,0.800,0.600 |
| `321-slew-limited-voltage-follower` | `FAIL_SIM_CORRECTNESS` | out@25.5ns=0.0000 expected=0.4000 tol=0.0900 |
| `321-slew-limited-voltage-follower` | `FAIL_SIM_CORRECTNESS` | metric@25.5ns=0.0000 expected=0.4000 tol=0.0900 |
| `321-slew-limited-voltage-follower` | `FAIL_SIM_CORRECTNESS` | out@7ns=0.9000 expected=0.0000 tol=0.0900 |
| `321-slew-limited-voltage-follower` | `FAIL_SIM_CORRECTNESS` | out@25.5ns=0.0000 expected=0.4000 tol=0.0900 |
| `321-slew-limited-voltage-follower` | `FAIL_SIM_CORRECTNESS` | out@25.5ns=0.2200 expected=0.4000 tol=0.0900 |
| `322-slew-limited-mode-stepper` | `FAIL_SIM_CORRECTNESS` | out@25.5ns=0.0000 expected=0.2000 tol=0.1000 |
| `322-slew-limited-mode-stepper` | `FAIL_SIM_CORRECTNESS` | metric@25.5ns=0.0000 expected=0.2500 tol=0.1000 |
| `322-slew-limited-mode-stepper` | `FAIL_SIM_CORRECTNESS` | out@7ns=0.2000 expected=0.0000 tol=0.1000 |
| `322-slew-limited-mode-stepper` | `FAIL_SIM_CORRECTNESS` | out@25.5ns=0.0000 expected=0.2000 tol=0.1000 |
| `322-slew-limited-mode-stepper` | `FAIL_SIM_CORRECTNESS` | out@45.5ns=0.4400 expected=0.6000 tol=0.1000 |
| `323-slew-output-reset-recovery` | `FAIL_SIM_CORRECTNESS` | out@26.2ns=0.0000 expected=0.8000 tol=0.1000 |
| `323-slew-output-reset-recovery` | `FAIL_SIM_CORRECTNESS` | metric@26.2ns=0.0000 expected=1.0000 tol=0.1000 |
| `323-slew-output-reset-recovery` | `FAIL_SIM_CORRECTNESS` | out@7ns=0.8000 expected=0.0000 tol=0.1000 |
| `323-slew-output-reset-recovery` | `FAIL_SIM_CORRECTNESS` | out@26.2ns=0.0000 expected=0.8000 tol=0.1000 |
| `323-slew-output-reset-recovery` | `FAIL_SIM_CORRECTNESS` | out@26.2ns=0.5000 expected=0.8000 tol=0.1000 |
| `324-slew-limited-envelope` | `FAIL_SIM_CORRECTNESS` | out@26ns=0.0000 expected=0.2000 tol=0.1000 |
| `324-slew-limited-envelope` | `FAIL_SIM_CORRECTNESS` | metric@26ns=0.0000 expected=0.2500 tol=0.1000 |
| `324-slew-limited-envelope` | `FAIL_SIM_CORRECTNESS` | out@7ns=0.8000 expected=0.0000 tol=0.1000 |
| `324-slew-limited-envelope` | `FAIL_SIM_CORRECTNESS` | out@26ns=0.0000 expected=0.2000 tol=0.1000 |
| `324-slew-limited-envelope` | `FAIL_SIM_CORRECTNESS` | out@45.5ns=0.4260 expected=0.6000 tol=0.1000 |
| `325-slew-asymmetric-rise-fall` | `FAIL_SIM_CORRECTNESS` | out@25.5ns=0.0000 expected=0.4000 tol=0.1000 |
| `325-slew-asymmetric-rise-fall` | `FAIL_SIM_CORRECTNESS` | metric@25.5ns=0.0000 expected=0.5000 tol=0.1000 |
| `325-slew-asymmetric-rise-fall` | `FAIL_SIM_CORRECTNESS` | out@7ns=0.8000 expected=0.0000 tol=0.1000 |
| `325-slew-asymmetric-rise-fall` | `FAIL_SIM_CORRECTNESS` | out@25.5ns=0.0000 expected=0.4000 tol=0.1000 |
| `325-slew-asymmetric-rise-fall` | `FAIL_SIM_CORRECTNESS` | out@45.5ns=0.3600 expected=0.7000 tol=0.1000 |
| `326-idtmod-phase-accumulator` | `FAIL_SIM_CORRECTNESS` | out@125ns=0.0000 expected=0.2250 tol=0.0700 |
| `326-idtmod-phase-accumulator` | `FAIL_SIM_CORRECTNESS` | metric@375ns=0.0000 expected=0.9000 tol=0.0700 |
| `326-idtmod-phase-accumulator` | `FAIL_SIM_CORRECTNESS` | out@250ns=0.3374 expected=0.4500 tol=0.0700 |
| `326-idtmod-phase-accumulator` | `FAIL_SIM_CORRECTNESS` | out@520ns=0.9359 expected=0.0360 tol=0.0700 |
| `326-idtmod-phase-accumulator` | `FAIL_SIM_CORRECTNESS` | out@250ns=0.3749 expected=0.4500 tol=0.0700 |
| `327-idtmod-wrapped-ramp-source` | `FAIL_SIM_CORRECTNESS` | out@162ns=0.0000 expected=0.0914 tol=0.0900 |
| `327-idtmod-wrapped-ramp-source` | `FAIL_SIM_CORRECTNESS` | metric@441.106ns=0.0000 expected=0.9000 tol=0.0900 |
| `327-idtmod-wrapped-ramp-source` | `FAIL_SIM_CORRECTNESS` | out@162ns=0.0000 expected=0.0914 tol=0.0900 |
| `327-idtmod-wrapped-ramp-source` | `FAIL_SIM_CORRECTNESS` | metric@441.106ns=0.0000 expected=0.9000 tol=0.0900 |
| `327-idtmod-wrapped-ramp-source` | `FAIL_SIM_CORRECTNESS` | out@413.577ns=0.3615 expected=0.4520 tol=0.0900 |
| `328-idtmod-frequency-control` | `FAIL_SIM_CORRECTNESS` | out@138.6ns=0.0000 expected=0.0936 tol=0.0900 |
| `328-idtmod-frequency-control` | `FAIL_SIM_CORRECTNESS` | metric@693.236ns=0.0000 expected=0.9000 tol=0.0900 |
| `328-idtmod-frequency-control` | `FAIL_SIM_CORRECTNESS` | out@138.6ns=0.0000 expected=0.0936 tol=0.0900 |
| `328-idtmod-frequency-control` | `FAIL_SIM_CORRECTNESS` | out@443.371ns=0.2919 expected=0.3846 tol=0.0900 |
| `328-idtmod-frequency-control` | `FAIL_SIM_CORRECTNESS` | out@494.436ns=0.3664 expected=0.4581 tol=0.0900 |
| `329-idtmod-modulo-phase-marker` | `FAIL_SIM_CORRECTNESS` | out@42ns=0.0000 expected=0.0907 tol=0.0900 |
| `329-idtmod-modulo-phase-marker` | `FAIL_SIM_CORRECTNESS` | metric@0ns=0.0000 expected=0.9000 tol=0.0900 |
| `329-idtmod-modulo-phase-marker` | `FAIL_SIM_CORRECTNESS` | metric@0ns=0.0000 expected=0.9000 tol=0.0900 |
| `329-idtmod-modulo-phase-marker` | `FAIL_SIM_CORRECTNESS` | metric@86.0789ns=0.9000 expected=0.0000 tol=0.0900 |
| `329-idtmod-modulo-phase-marker` | `FAIL_SIM_CORRECTNESS` | out@209.224ns=0.3697 expected=0.4624 tol=0.0900 |
| `330-idtmod-clock-phase-meter` | `FAIL_SIM_CORRECTNESS` | out@123.24ns=0.0000 expected=0.1458 tol=0.0900 |
| `330-idtmod-clock-phase-meter` | `FAIL_SIM_CORRECTNESS` | metric@464.88ns=0.0000 expected=0.9000 tol=0.0900 |
| `330-idtmod-clock-phase-meter` | `FAIL_SIM_CORRECTNESS` | out@123.24ns=0.0000 expected=0.1458 tol=0.0900 |
| `330-idtmod-clock-phase-meter` | `FAIL_SIM_CORRECTNESS` | metric@464.88ns=0.0000 expected=0.9000 tol=0.0900 |
| `330-idtmod-clock-phase-meter` | `FAIL_SIM_CORRECTNESS` | out@464.88ns=0.4807 expected=0.6009 tol=0.0900 |
| `331-above-threshold-latch` | `FAIL_SIM_CORRECTNESS` | out@86.1ns=0.0000 expected=0.9000 tol=0.0800 |
| `331-above-threshold-latch` | `FAIL_SIM_CORRECTNESS` | metric@262.5ns=0.0000 expected=0.9000 tol=0.0800 |
| `331-above-threshold-latch` | `FAIL_SIM_CORRECTNESS` | out@424.2ns=0.9000 expected=0.0000 tol=0.0800 |
| `331-above-threshold-latch` | `FAIL_SIM_CORRECTNESS` | metric@262.5ns=0.0000 expected=0.9000 tol=0.0800 |
| `331-above-threshold-latch` | `FAIL_SIM_CORRECTNESS` | out@83.3ns=0.7200 expected=0.9000 tol=0.0800 |
| `332-above-window-qualifier` | `FAIL_SIM_CORRECTNESS` | out@94.24ns=0.0000 expected=0.9000 tol=0.0800 |
| `332-above-window-qualifier` | `FAIL_SIM_CORRECTNESS` | metric@247ns=0.0000 expected=0.9000 tol=0.0800 |
| `332-above-window-qualifier` | `FAIL_SIM_CORRECTNESS` | out@427.12ns=0.9000 expected=0.0000 tol=0.0800 |
| `332-above-window-qualifier` | `FAIL_SIM_CORRECTNESS` | metric@247ns=0.0000 expected=0.9000 tol=0.0800 |
| `332-above-window-qualifier` | `FAIL_SIM_CORRECTNESS` | out@91.2ns=0.7200 expected=0.9000 tol=0.0800 |
| `333-last-crossing-period-meter` | `FAIL_SIM_CORRECTNESS` | out@261ns=0.0000 expected=0.3815 tol=0.0800 |
| `333-last-crossing-period-meter` | `FAIL_SIM_CORRECTNESS` | metric@261ns=0.0000 expected=0.9000 tol=0.0800 |
| `333-last-crossing-period-meter` | `FAIL_SIM_CORRECTNESS` | out@725.4ns=0.6750 expected=0.0000 tol=0.0800 |
| `333-last-crossing-period-meter` | `FAIL_SIM_CORRECTNESS` | out@261ns=0.5100 expected=0.3815 tol=0.0800 |
| `333-last-crossing-period-meter` | `FAIL_SIM_CORRECTNESS` | out@564.3ns=0.5400 expected=0.6756 tol=0.0800 |
| `334-last-crossing-edge-age` | `FAIL_SIM_CORRECTNESS` | out@156ns=0.0000 expected=0.2100 tol=0.0800 |
| `334-last-crossing-edge-age` | `FAIL_SIM_CORRECTNESS` | metric@100.8ns=0.0000 expected=0.9000 tol=0.0800 |
| `334-last-crossing-edge-age` | `FAIL_SIM_CORRECTNESS` | out@676.8ns=0.5715 expected=0.0000 tol=0.0800 |
| `334-last-crossing-edge-age` | `FAIL_SIM_CORRECTNESS` | out@152.8ns=0.3172 expected=0.2100 tol=0.0800 |
| `334-last-crossing-edge-age` | `FAIL_SIM_CORRECTNESS` | out@252ns=0.4092 expected=0.5100 tol=0.0800 |
| `335-above-resettable-peak-marker` | `FAIL_SIM_CORRECTNESS` | out@82.8ns=0.0000 expected=0.9000 tol=0.0800 |
| `335-above-resettable-peak-marker` | `FAIL_SIM_CORRECTNESS` | metric@104.4ns=0.0000 expected=0.5000 tol=0.0800 |
| `335-above-resettable-peak-marker` | `FAIL_SIM_CORRECTNESS` | out@426.24ns=0.9000 expected=0.0000 tol=0.0800 |
| `335-above-resettable-peak-marker` | `FAIL_SIM_CORRECTNESS` | metric@404.64ns=0.2500 expected=0.8500 tol=0.0800 |
| `335-above-resettable-peak-marker` | `FAIL_SIM_CORRECTNESS` | out@84.96ns=0.7200 expected=0.9000 tol=0.0800 |
| `336-directive-configurable-threshold` | `FAIL_SIM_CORRECTNESS` | out@301.6ns=0.0000 expected=0.9000 tol=0.0800 |
| `336-directive-configurable-threshold` | `FAIL_SIM_CORRECTNESS` | metric@107.25ns=0.0000 expected=0.5000 tol=0.0800 |
| `336-directive-configurable-threshold` | `FAIL_SIM_CORRECTNESS` | out@501.15ns=0.9000 expected=0.0000 tol=0.0800 |
| `336-directive-configurable-threshold` | `FAIL_SIM_CORRECTNESS` | out@100ns=0.9000 expected=0.0000 tol=0.0800 |
| `336-directive-configurable-threshold` | `FAIL_SIM_CORRECTNESS` | out@301.6ns=0.7200 expected=0.9000 tol=0.0800 |
| `337-parameter-range-limited-gain` | `FAIL_SIM_CORRECTNESS` | out@104.65ns=0.0000 expected=0.4375 tol=0.0800 |
| `337-parameter-range-limited-gain` | `FAIL_SIM_CORRECTNESS` | metric@104.65ns=0.0000 expected=0.4375 tol=0.0800 |
| `337-parameter-range-limited-gain` | `FAIL_SIM_CORRECTNESS` | out@500ns=0.8125 expected=0.0000 tol=0.0800 |
| `337-parameter-range-limited-gain` | `FAIL_SIM_CORRECTNESS` | out@104.65ns=0.1875 expected=0.4375 tol=0.0800 |
| `337-parameter-range-limited-gain` | `FAIL_SIM_CORRECTNESS` | out@300.3ns=0.7200 expected=0.9000 tol=0.0800 |
| `338-math-trig-envelope-detector` | `FAIL_SIM_CORRECTNESS` | out@104.65ns=0.0000 expected=0.2477 tol=0.0800 |
| `338-math-trig-envelope-detector` | `FAIL_SIM_CORRECTNESS` | metric@104.65ns=0.0000 expected=0.4977 tol=0.0800 |
| `338-math-trig-envelope-detector` | `FAIL_SIM_CORRECTNESS` | out@500ns=0.4968 expected=0.0000 tol=0.0800 |
| `338-math-trig-envelope-detector` | `FAIL_SIM_CORRECTNESS` | out@104.65ns=0.5969 expected=0.2477 tol=0.0800 |
| `338-math-trig-envelope-detector` | `FAIL_SIM_CORRECTNESS` | out@104.65ns=0.3691 expected=0.2477 tol=0.0800 |
| `339-random-seeded-dither-source` | `FAIL_SIM_CORRECTNESS` | out@104.65ns=0.0000 expected_range=[0.200,0.490] |
| `339-random-seeded-dither-source` | `FAIL_SIM_CORRECTNESS` | mode_high_metric_too_low@104.65ns=0.0000 |
| `339-random-seeded-dither-source` | `FAIL_SIM_CORRECTNESS` | reset_window_nonzero@500ns |
| `339-random-seeded-dither-source` | `FAIL_SIM_CORRECTNESS` | dither_relation_err@104.65ns=0.0500 out=0.2700 vin=0.2200 metric=0.2000 |
| `339-random-seeded-dither-source` | `FAIL_SIM_CORRECTNESS` | dither_relation_err@104.65ns=0.0500 out=0.2700 vin=0.2200 metric=0.2000 |
| `340-bound-step-clock-guard` | `FAIL_SIM_CORRECTNESS` | out@104ns=0.0000 expected=0.2500 tol=0.0800 |
| `340-bound-step-clock-guard` | `FAIL_SIM_CORRECTNESS` | metric@104ns=0.0000 expected=0.8000 tol=0.0800 |
| `340-bound-step-clock-guard` | `FAIL_SIM_CORRECTNESS` | out@500.5ns=0.4200 expected=0.0000 tol=0.0800 |
| `340-bound-step-clock-guard` | `FAIL_SIM_CORRECTNESS` | out@104ns=0.0000 expected=0.2500 tol=0.0800 |
| `340-bound-step-clock-guard` | `FAIL_SIM_CORRECTNESS` | out@104ns=0.1500 expected=0.2500 tol=0.0800 |
| `341-wreal-gain-pass-through` | `FAIL_SIM_CORRECTNESS` | y@200.2ns=0.0000 expected=0.4375 sel=0.9000 tol=0.0800 |
| `341-wreal-gain-pass-through` | `FAIL_SIM_CORRECTNESS` | y@0ns=0.5500 expected=0.0750 sel=0.0000 tol=0.0800 |
| `341-wreal-gain-pass-through` | `FAIL_SIM_CORRECTNESS` | y@200.2ns=0.3375 expected=0.4375 sel=0.9000 tol=0.0800 |
| `341-wreal-gain-pass-through` | `FAIL_SIM_CORRECTNESS` | y@200.2ns=0.0750 expected=0.4375 sel=0.9000 tol=0.0800 |
| `341-wreal-gain-pass-through` | `FAIL_SIM_CORRECTNESS` | y@423.8ns=0.5320 expected=0.6400 sel=0.9000 tol=0.0800 |
| `342-wreal-two-input-summer` | `FAIL_SIM_CORRECTNESS` | y@0ns=0.0000 expected=0.4300 sel=0.0000 tol=0.0800 |
| `342-wreal-two-input-summer` | `FAIL_SIM_CORRECTNESS` | y@0ns=0.5300 expected=0.4300 sel=0.0000 tol=0.0800 |
| `342-wreal-two-input-summer` | `FAIL_SIM_CORRECTNESS` | y@201.5ns=0.4300 expected=0.5300 sel=0.9000 tol=0.0800 |
| `342-wreal-two-input-summer` | `FAIL_SIM_CORRECTNESS` | y@201.5ns=0.4300 expected=0.5300 sel=0.9000 tol=0.0800 |
| `342-wreal-two-input-summer` | `FAIL_SIM_CORRECTNESS` | y@224.25ns=0.6800 expected=0.8000 sel=0.9000 tol=0.0800 |
| `343-wreal-threshold-flag` | `FAIL_SIM_CORRECTNESS` | y@224.25ns=0.0000 expected=0.9000 sel=0.9000 tol=0.0800 |
| `343-wreal-threshold-flag` | `FAIL_SIM_CORRECTNESS` | y@224.25ns=0.0000 expected=0.9000 sel=0.9000 tol=0.0800 |
| `343-wreal-threshold-flag` | `FAIL_SIM_CORRECTNESS` | y@224.25ns=0.0000 expected=0.9000 sel=0.9000 tol=0.0800 |
| `343-wreal-threshold-flag` | `FAIL_SIM_CORRECTNESS` | y@201.5ns=0.9000 expected=0.0000 sel=0.9000 tol=0.0800 |
| `343-wreal-threshold-flag` | `FAIL_SIM_CORRECTNESS` | y@224.25ns=0.6000 expected=0.9000 sel=0.9000 tol=0.0800 |
| `344-wreal-clamped-mux` | `FAIL_SIM_CORRECTNESS` | y@201.5ns=0.0000 expected=0.9000 sel=0.9000 tol=0.0800 |
| `344-wreal-clamped-mux` | `FAIL_SIM_CORRECTNESS` | y@0ns=0.9000 expected=0.0000 sel=0.0000 tol=0.0800 |
| `344-wreal-clamped-mux` | `FAIL_SIM_CORRECTNESS` | y@0ns=-0.1500 expected=0.0000 sel=0.0000 tol=0.0800 |
| `344-wreal-clamped-mux` | `FAIL_SIM_CORRECTNESS` | y@201.5ns=0.0000 expected=0.9000 sel=0.9000 tol=0.0800 |
| `344-wreal-clamped-mux` | `FAIL_SIM_CORRECTNESS` | y@201.5ns=0.6000 expected=0.9000 sel=0.9000 tol=0.0800 |
| `345-wreal-scale-offset` | `FAIL_SIM_CORRECTNESS` | y@0ns=0.0000 expected=0.2500 sel=0.0000 tol=0.0800 |
| `345-wreal-scale-offset` | `FAIL_SIM_CORRECTNESS` | y@0ns=0.4250 expected=0.2500 sel=0.0000 tol=0.0800 |
| `345-wreal-scale-offset` | `FAIL_SIM_CORRECTNESS` | y@201.5ns=0.6250 expected=0.4250 sel=0.9000 tol=0.0800 |
| `345-wreal-scale-offset` | `FAIL_SIM_CORRECTNESS` | y@201.5ns=0.2500 expected=0.4250 sel=0.9000 tol=0.0800 |
| `345-wreal-scale-offset` | `FAIL_SIM_CORRECTNESS` | y@201.5ns=0.2850 expected=0.4250 sel=0.9000 tol=0.0800 |
| `346-logic-assign-inverter` | `FAIL_SIM_CORRECTNESS` | y@0ns=0.0000 expected=1.0000 a=0.0000 b=1.0000 en=1.0000 tol=0.0800 |
| `346-logic-assign-inverter` | `FAIL_SIM_CORRECTNESS` | y@185.9ns=1.0000 expected=0.0000 a=1.0000 b=1.0000 en=1.0000 tol=0.0800 |
| `346-logic-assign-inverter` | `FAIL_SIM_CORRECTNESS` | y@0ns=0.0000 expected=1.0000 a=0.0000 b=1.0000 en=1.0000 tol=0.0800 |
| `346-logic-assign-inverter` | `FAIL_SIM_CORRECTNESS` | y@185.9ns=1.0000 expected=0.0000 a=1.0000 b=1.0000 en=1.0000 tol=0.0800 |
| `346-logic-assign-inverter` | `FAIL_SIM_CORRECTNESS` | y@0ns=0.0000 expected=1.0000 a=0.0000 b=1.0000 en=1.0000 tol=0.0800 |
| `347-logic-assign-and-or` | `FAIL_SIM_CORRECTNESS` | y@263.25ns=0.0000 expected=1.0000 a=1.0000 b=1.0000 en=0.0000 tol=0.0800 |
| `347-logic-assign-and-or` | `FAIL_SIM_CORRECTNESS` | y@263.25ns=0.0000 expected=1.0000 a=1.0000 b=1.0000 en=0.0000 tol=0.0800 |
| `347-logic-assign-and-or` | `FAIL_SIM_CORRECTNESS` | y@424.45ns=0.0000 expected=1.0000 a=0.0000 b=1.0000 en=1.0000 tol=0.0800 |
| `347-logic-assign-and-or` | `FAIL_SIM_CORRECTNESS` | y@162.5ns=1.0000 expected=0.0000 a=1.0000 b=0.0000 en=0.0000 tol=0.0800 |
| `347-logic-assign-and-or` | `FAIL_SIM_CORRECTNESS` | y@0ns=1.0000 expected=0.0000 a=0.0000 b=0.0000 en=0.0000 tol=0.0800 |
| `348-logic-assign-xor-flag` | `FAIL_SIM_CORRECTNESS` | y@0ns=0.0000 expected=1.0000 a=0.0000 b=1.0000 en=1.0000 tol=0.0800 |
| `348-logic-assign-xor-flag` | `FAIL_SIM_CORRECTNESS` | y@0ns=0.0000 expected=1.0000 a=0.0000 b=1.0000 en=1.0000 tol=0.0800 |
| `348-logic-assign-xor-flag` | `FAIL_SIM_CORRECTNESS` | y@461.5ns=1.0000 expected=0.0000 a=0.0000 b=1.0000 en=0.0000 tol=0.0800 |
| `348-logic-assign-xor-flag` | `FAIL_SIM_CORRECTNESS` | y@0ns=0.0000 expected=1.0000 a=0.0000 b=1.0000 en=1.0000 tol=0.0800 |
| `348-logic-assign-xor-flag` | `FAIL_SIM_CORRECTNESS` | y@0ns=0.0000 expected=1.0000 a=0.0000 b=1.0000 en=1.0000 tol=0.0800 |
| `349-logic-assign-priority-mux` | `FAIL_SIM_CORRECTNESS` | y@0ns=0.0000 expected=1.0000 a=0.0000 b=1.0000 en=0.0000 tol=0.0800 |
| `349-logic-assign-priority-mux` | `FAIL_SIM_CORRECTNESS` | y@0ns=0.0000 expected=1.0000 a=0.0000 b=1.0000 en=0.0000 tol=0.0800 |
| `349-logic-assign-priority-mux` | `FAIL_SIM_CORRECTNESS` | y@0ns=0.0000 expected=1.0000 a=0.0000 b=1.0000 en=0.0000 tol=0.0800 |
| `349-logic-assign-priority-mux` | `FAIL_SIM_CORRECTNESS` | y@0ns=0.0000 expected=1.0000 a=0.0000 b=1.0000 en=0.0000 tol=0.0800 |
| `349-logic-assign-priority-mux` | `FAIL_SIM_CORRECTNESS` | y@0ns=0.0000 expected=1.0000 a=0.0000 b=1.0000 en=0.0000 tol=0.0800 |
| `350-logic-assign-reduction` | `FAIL_SIM_CORRECTNESS` | y@0ns=0.0000 expected=1.0000 a=1.0000 b=1.0000 en=1.0000 tol=0.0800 |
| `350-logic-assign-reduction` | `FAIL_SIM_CORRECTNESS` | y@0ns=0.0000 expected=1.0000 a=1.0000 b=1.0000 en=1.0000 tol=0.0800 |
| `350-logic-assign-reduction` | `FAIL_SIM_CORRECTNESS` | y@500.5ns=1.0000 expected=0.0000 a=1.0000 b=1.0000 en=0.0000 tol=0.0800 |
| `350-logic-assign-reduction` | `FAIL_SIM_CORRECTNESS` | y@0ns=0.0000 expected=1.0000 a=1.0000 b=1.0000 en=1.0000 tol=0.0800 |
| `350-logic-assign-reduction` | `FAIL_SIM_CORRECTNESS` | y@362.7ns=1.0000 expected=0.0000 a=1.0000 b=0.0000 en=1.0000 tol=0.0800 |
| `351-always-posedged-dff` | `FAIL_SIM_CORRECTNESS` | q@159.12ns=0.0000 expected=1.0000 edge=posedge tol=0.0800 |
| `351-always-posedged-dff` | `FAIL_SIM_CORRECTNESS` | q@159.12ns=0.0000 expected=1.0000 edge=posedge tol=0.0800 |
| `351-always-posedged-dff` | `FAIL_SIM_CORRECTNESS` | q@59.04ns=1.0000 expected=0.0000 edge=posedge tol=0.0800 |
| `351-always-posedged-dff` | `FAIL_SIM_CORRECTNESS` | q@100ns=1.0000 expected=0.0000 edge=posedge tol=0.0800 |
| `351-always-posedged-dff` | `FAIL_SIM_CORRECTNESS` | q@559.44ns=1.0000 expected=0.0000 edge=posedge tol=0.0800 |
| `352-always-negedge-sampler` | `FAIL_SIM_CORRECTNESS` | q@160ns=0.0000 expected=1.0000 edge=negedge tol=0.0800 |
| `352-always-negedge-sampler` | `FAIL_SIM_CORRECTNESS` | q@160ns=0.0000 expected=1.0000 edge=negedge tol=0.0800 |
| `352-always-negedge-sampler` | `FAIL_SIM_CORRECTNESS` | q@60.0001ns=1.0000 expected=0.0000 edge=negedge tol=0.0800 |
| `352-always-negedge-sampler` | `FAIL_SIM_CORRECTNESS` | q@99.36ns=1.0000 expected=0.0000 edge=negedge tol=0.0800 |
| `352-always-negedge-sampler` | `FAIL_SIM_CORRECTNESS` | q@560ns=1.0000 expected=0.0000 edge=negedge tol=0.0800 |
| `353-always-resettable-toggle` | `FAIL_SIM_CORRECTNESS` | q@50ns=0.0000 expected=1.0000 tol=0.0800 |
| `353-always-resettable-toggle` | `FAIL_SIM_CORRECTNESS` | q@50ns=0.0000 expected=1.0000 tol=0.0800 |
| `353-always-resettable-toggle` | `FAIL_SIM_CORRECTNESS` | q@150ns=1.0000 expected=0.0000 tol=0.0800 |
| `353-always-resettable-toggle` | `FAIL_SIM_CORRECTNESS` | q@50ns=0.0000 expected=1.0000 tol=0.0800 |
| `353-always-resettable-toggle` | `FAIL_SIM_CORRECTNESS` | q@50ns=0.0000 expected=1.0000 tol=0.0800 |
| `354-always-counter-two-bit` | `FAIL_SIM_CORRECTNESS` | q@359.98ns=0.0000 expected=1.0000 count=2 tol=0.0800 |
| `354-always-counter-two-bit` | `FAIL_SIM_CORRECTNESS` | q@159.9ns=1.0000 expected=0.0000 count=1 tol=0.0800 |
| `354-always-counter-two-bit` | `FAIL_SIM_CORRECTNESS` | q@59.86ns=1.0000 expected=0.0000 count=0 tol=0.0800 |
| `354-always-counter-two-bit` | `FAIL_SIM_CORRECTNESS` | q@200.08ns=1.0000 expected=0.0000 count=1 tol=0.0800 |
| `354-always-counter-two-bit` | `FAIL_SIM_CORRECTNESS` | q@0.82ns=1.0000 expected=0.0000 count=0 tol=0.0800 |
| `355-always-enable-hold` | `FAIL_SIM_CORRECTNESS` | q@159.12ns=0.0000 expected=1.0000 edge=posedge tol=0.0800 |
| `355-always-enable-hold` | `FAIL_SIM_CORRECTNESS` | q@159.12ns=0.0000 expected=1.0000 edge=posedge tol=0.0800 |
| `355-always-enable-hold` | `FAIL_SIM_CORRECTNESS` | q@59.04ns=1.0000 expected=0.0000 edge=posedge tol=0.0800 |
| `355-always-enable-hold` | `FAIL_SIM_CORRECTNESS` | q@100ns=1.0000 expected=0.0000 edge=posedge tol=0.0800 |
| `355-always-enable-hold` | `FAIL_SIM_CORRECTNESS` | q@559.44ns=1.0000 expected=0.0000 edge=posedge tol=0.0800 |
| `356-mixed-logic-enable-voltage-driver` | `FAIL_SIM_CORRECTNESS` | vout@0ns=0.0000 expected=0.5500 tol=0.0800 |
| `356-mixed-logic-enable-voltage-driver` | `FAIL_SIM_CORRECTNESS` | vout@0ns=0.0000 expected=0.5500 tol=0.0800 |
| `356-mixed-logic-enable-voltage-driver` | `FAIL_SIM_CORRECTNESS` | vout@230.28ns=0.2500 expected=0.0000 tol=0.0800 |
| `356-mixed-logic-enable-voltage-driver` | `FAIL_SIM_CORRECTNESS` | vout@0ns=0.0000 expected=0.5500 tol=0.0800 |
| `356-mixed-logic-enable-voltage-driver` | `FAIL_SIM_CORRECTNESS` | vout@0ns=0.2750 expected=0.5500 tol=0.0800 |
| `357-mixed-wreal-to-electrical-buffer` | `FAIL_SIM_CORRECTNESS` | vout@0ns=0.0000 expected=0.3000 tol=0.0800 |
| `357-mixed-wreal-to-electrical-buffer` | `FAIL_SIM_CORRECTNESS` | vout@0ns=0.1000 expected=0.3000 tol=0.0800 |
| `357-mixed-wreal-to-electrical-buffer` | `FAIL_SIM_CORRECTNESS` | vout@0ns=0.6500 expected=0.3000 tol=0.0800 |
| `357-mixed-wreal-to-electrical-buffer` | `FAIL_SIM_CORRECTNESS` | vout@0ns=0.0000 expected=0.3000 tol=0.0800 |
| `357-mixed-wreal-to-electrical-buffer` | `FAIL_SIM_CORRECTNESS` | vout@0ns=0.1500 expected=0.3000 tol=0.0800 |
| `358-mixed-electrical-threshold-logic-flag` | `FAIL_SIM_CORRECTNESS` | vout@165.68ns=0.0000 expected=0.9000 tol=0.0800 |
| `358-mixed-electrical-threshold-logic-flag` | `FAIL_SIM_CORRECTNESS` | vout@0ns=0.9000 expected=0.0000 tol=0.0800 |
| `358-mixed-electrical-threshold-logic-flag` | `FAIL_SIM_CORRECTNESS` | vout@0ns=0.9000 expected=0.0000 tol=0.0800 |
| `358-mixed-electrical-threshold-logic-flag` | `FAIL_SIM_CORRECTNESS` | vout@165.68ns=0.0000 expected=0.9000 tol=0.0800 |
| `358-mixed-electrical-threshold-logic-flag` | `FAIL_SIM_CORRECTNESS` | vout@162.64ns=0.4500 expected=0.9000 tol=0.0800 |
| `359-mixed-logic-clocked-voltage-sampler` | `FAIL_SIM_CORRECTNESS` | vout@223.86ns=0.0000 expected=0.7200 sampled=True tol=0.0800 |
| `359-mixed-logic-clocked-voltage-sampler` | `FAIL_SIM_CORRECTNESS` | vout@79.895ns=0.3375 expected=0.0000 sampled=True tol=0.0800 |
| `359-mixed-logic-clocked-voltage-sampler` | `FAIL_SIM_CORRECTNESS` | vout@181.22ns=0.4500 expected=0.0000 sampled=True tol=0.0800 |
| `359-mixed-logic-clocked-voltage-sampler` | `FAIL_SIM_CORRECTNESS` | vout@223.86ns=0.0000 expected=0.7200 sampled=True tol=0.0800 |
| `359-mixed-logic-clocked-voltage-sampler` | `FAIL_SIM_CORRECTNESS` | vout@220.58ns=0.3600 expected=0.7200 sampled=True tol=0.0800 |
| `360-mixed-wreal-logic-select-driver` | `FAIL_SIM_CORRECTNESS` | vout@0ns=0.0000 expected=0.7800 tol=0.0800 |
| `360-mixed-wreal-logic-select-driver` | `FAIL_SIM_CORRECTNESS` | vout@0ns=0.2000 expected=0.7800 tol=0.0800 |
| `360-mixed-wreal-logic-select-driver` | `FAIL_SIM_CORRECTNESS` | vout@0ns=0.0000 expected=0.7800 tol=0.0800 |
| `360-mixed-wreal-logic-select-driver` | `FAIL_SIM_CORRECTNESS` | vout@0ns=0.4900 expected=0.7800 tol=0.0800 |
| `360-mixed-wreal-logic-select-driver` | `FAIL_SIM_CORRECTNESS` | vout@0ns=0.3900 expected=0.7800 tol=0.0800 |
| `361-white-noise-voltage-source` | `FAIL_SIM_CORRECTNESS` | metric@65.52ns=0.0000 expected=0.2500 tol=0.0800 |
| `361-white-noise-voltage-source` | `FAIL_SIM_CORRECTNESS` | metric@63.28ns=0.3500 expected=0.2500 tol=0.0800 |
| `361-white-noise-voltage-source` | `FAIL_SIM_CORRECTNESS` | metric@65.52ns=0.0000 expected=0.2500 tol=0.0800 |
| `361-white-noise-voltage-source` | `FAIL_SIM_CORRECTNESS` | metric@63.28ns=0.4500 expected=0.2500 tol=0.0800 |
| `361-white-noise-voltage-source` | `FAIL_SIM_CORRECTNESS` | metric@63.28ns=0.1250 expected=0.2500 tol=0.0800 |
| `362-white-noise-gated-source` | `FAIL_SIM_CORRECTNESS` | metric@173.6ns=0.0000 expected=0.9000 tol=0.0800 |
| `362-white-noise-gated-source` | `FAIL_SIM_CORRECTNESS` | metric@59.65ns=0.9000 expected=0.0000 tol=0.0800 |
| `362-white-noise-gated-source` | `FAIL_SIM_CORRECTNESS` | metric@173.6ns=0.0000 expected=0.9000 tol=0.0800 |
| `362-white-noise-gated-source` | `FAIL_SIM_CORRECTNESS` | metric@59.65ns=0.2500 expected=0.0000 tol=0.0800 |
| `362-white-noise-gated-source` | `FAIL_SIM_CORRECTNESS` | metric@171.36ns=0.4500 expected=0.9000 tol=0.0800 |
| `363-flicker-noise-voltage-source` | `FAIL_SIM_CORRECTNESS` | metric@65.52ns=0.0000 expected=1.0000 tol=0.0800 |
| `363-flicker-noise-voltage-source` | `FAIL_SIM_CORRECTNESS` | metric@63.28ns=1.2000 expected=1.0000 tol=0.0800 |
| `363-flicker-noise-voltage-source` | `FAIL_SIM_CORRECTNESS` | metric@65.52ns=0.0000 expected=1.0000 tol=0.0800 |
| `363-flicker-noise-voltage-source` | `FAIL_SIM_CORRECTNESS` | metric@63.28ns=0.2500 expected=1.0000 tol=0.0800 |
| `363-flicker-noise-voltage-source` | `FAIL_SIM_CORRECTNESS` | metric@63.28ns=0.5000 expected=1.0000 tol=0.0800 |
| `364-flicker-noise-corner-selector` | `FAIL_SIM_CORRECTNESS` | metric@173.6ns=0.0000 expected=0.9000 tol=0.0800 |
| `364-flicker-noise-corner-selector` | `FAIL_SIM_CORRECTNESS` | metric@59.65ns=0.9000 expected=0.0000 tol=0.0800 |
| `364-flicker-noise-corner-selector` | `FAIL_SIM_CORRECTNESS` | metric@173.6ns=0.0000 expected=0.9000 tol=0.0800 |
| `364-flicker-noise-corner-selector` | `FAIL_SIM_CORRECTNESS` | metric@59.65ns=0.2500 expected=0.0000 tol=0.0800 |
| `364-flicker-noise-corner-selector` | `FAIL_SIM_CORRECTNESS` | metric@171.36ns=0.4500 expected=0.9000 tol=0.0800 |
| `365-noise-table-voltage-shaper` | `FAIL_SIM_CORRECTNESS` | metric@65.52ns=0.0000 expected=0.3500 tol=0.0800 |
| `365-noise-table-voltage-shaper` | `FAIL_SIM_CORRECTNESS` | metric@63.28ns=0.4500 expected=0.3500 tol=0.0800 |
| `365-noise-table-voltage-shaper` | `FAIL_SIM_CORRECTNESS` | metric@65.52ns=0.0000 expected=0.3500 tol=0.0800 |
| `365-noise-table-voltage-shaper` | `FAIL_SIM_CORRECTNESS` | metric@63.28ns=0.2500 expected=0.3500 tol=0.0800 |
| `365-noise-table-voltage-shaper` | `FAIL_SIM_CORRECTNESS` | metric@63.28ns=0.1750 expected=0.3500 tol=0.0800 |
| `366-noise-table-gated-shaper` | `FAIL_SIM_CORRECTNESS` | metric@173.6ns=0.0000 expected=0.9000 tol=0.0800 |
| `366-noise-table-gated-shaper` | `FAIL_SIM_CORRECTNESS` | metric@59.65ns=0.9000 expected=0.0000 tol=0.0800 |
| `366-noise-table-gated-shaper` | `FAIL_SIM_CORRECTNESS` | metric@173.6ns=0.0000 expected=0.9000 tol=0.0800 |
| `366-noise-table-gated-shaper` | `FAIL_SIM_CORRECTNESS` | metric@59.65ns=0.2500 expected=0.0000 tol=0.0800 |
| `366-noise-table-gated-shaper` | `FAIL_SIM_CORRECTNESS` | metric@171.36ns=0.4500 expected=0.9000 tol=0.0800 |
| `367-analysis-dependent-dc-tran-mode` | `FAIL_SIM_CORRECTNESS` | out@0ns=0.0000 expected=0.2500 tol=0.0800 |
| `367-analysis-dependent-dc-tran-mode` | `FAIL_SIM_CORRECTNESS` | out@0ns=0.3500 expected=0.2500 tol=0.0800 |
| `367-analysis-dependent-dc-tran-mode` | `FAIL_SIM_CORRECTNESS` | out@132.72ns=0.2500 expected=0.7200 tol=0.0800 |
| `367-analysis-dependent-dc-tran-mode` | `FAIL_SIM_CORRECTNESS` | metric@63.84ns=0.0000 expected=0.9000 tol=0.0800 |
| `367-analysis-dependent-dc-tran-mode` | `FAIL_SIM_CORRECTNESS` | out@0ns=0.1250 expected=0.2500 tol=0.0800 |
| `368-analysis-dependent-noise-enable` | `FAIL_SIM_CORRECTNESS` | metric@65.52ns=0.0000 expected=0.2500 tol=0.0800 |
| `368-analysis-dependent-noise-enable` | `FAIL_SIM_CORRECTNESS` | metric@63.28ns=0.3500 expected=0.2500 tol=0.0800 |
| `368-analysis-dependent-noise-enable` | `FAIL_SIM_CORRECTNESS` | metric@65.52ns=0.0000 expected=0.2500 tol=0.0800 |
| `368-analysis-dependent-noise-enable` | `FAIL_SIM_CORRECTNESS` | metric@63.28ns=0.7500 expected=0.2500 tol=0.0800 |
| `368-analysis-dependent-noise-enable` | `FAIL_SIM_CORRECTNESS` | metric@63.28ns=0.1250 expected=0.2500 tol=0.0800 |
| `369-ac-stim-small-signal-source` | `FAIL_SIM_CORRECTNESS` | out@0ns=0.0000 expected=0.2500 tol=0.0800 |
| `369-ac-stim-small-signal-source` | `FAIL_SIM_CORRECTNESS` | out@0ns=0.3500 expected=0.2500 tol=0.0800 |
| `369-ac-stim-small-signal-source` | `FAIL_SIM_CORRECTNESS` | out@132.72ns=0.2500 expected=0.7200 tol=0.0800 |
| `369-ac-stim-small-signal-source` | `FAIL_SIM_CORRECTNESS` | metric@63.84ns=0.0000 expected=1.0000 tol=0.0800 |
| `369-ac-stim-small-signal-source` | `FAIL_SIM_CORRECTNESS` | out@0ns=0.1250 expected=0.2500 tol=0.0800 |
| `370-ac-stim-phase-selector` | `FAIL_SIM_CORRECTNESS` | out@0ns=0.0000 expected=0.2500 tol=0.0800 |
| `370-ac-stim-phase-selector` | `FAIL_SIM_CORRECTNESS` | out@0ns=0.3500 expected=0.2500 tol=0.0800 |
| `370-ac-stim-phase-selector` | `FAIL_SIM_CORRECTNESS` | out@134.96ns=0.2500 expected=0.7200 tol=0.0800 |
| `370-ac-stim-phase-selector` | `FAIL_SIM_CORRECTNESS` | metric@61.6ns=0.9000 expected=0.0000 tol=0.0800 |
| `370-ac-stim-phase-selector` | `FAIL_SIM_CORRECTNESS` | out@0ns=0.1250 expected=0.2500 tol=0.0800 |
| `371-combined-white-flicker-noise` | `FAIL_SIM_CORRECTNESS` | metric@65.52ns=0.0000 expected=1.5000 tol=0.0800 |
| `371-combined-white-flicker-noise` | `FAIL_SIM_CORRECTNESS` | metric@63.28ns=1.0000 expected=1.5000 tol=0.0800 |
| `371-combined-white-flicker-noise` | `FAIL_SIM_CORRECTNESS` | metric@65.52ns=0.0000 expected=1.5000 tol=0.0800 |
| `371-combined-white-flicker-noise` | `FAIL_SIM_CORRECTNESS` | metric@63.28ns=0.2500 expected=1.5000 tol=0.0800 |
| `371-combined-white-flicker-noise` | `FAIL_SIM_CORRECTNESS` | metric@63.28ns=0.7500 expected=1.5000 tol=0.0800 |
| `372-analysis-aware-noise-metric` | `FAIL_SIM_CORRECTNESS` | out@0ns=0.0000 expected=0.2500 tol=0.0800 |
| `372-analysis-aware-noise-metric` | `FAIL_SIM_CORRECTNESS` | out@0ns=0.3500 expected=0.2500 tol=0.0800 |
| `372-analysis-aware-noise-metric` | `FAIL_SIM_CORRECTNESS` | metric@61.6ns=0.2500 expected=0.1250 tol=0.0800 |
| `372-analysis-aware-noise-metric` | `FAIL_SIM_CORRECTNESS` | metric@61.6ns=0.2500 expected=0.1250 tol=0.0800 |
| `372-analysis-aware-noise-metric` | `FAIL_SIM_CORRECTNESS` | out@0ns=0.1250 expected=0.2500 tol=0.0800 |
| `373-task-output-limiter` | `FAIL_SIM_CORRECTNESS` | out@150.8ns=0.0000 expected=0.9000 tol=0.0800 |
| `373-task-output-limiter` | `FAIL_SIM_CORRECTNESS` | out@352.56ns=0.0000 expected=0.9000 tol=0.0800 |
| `373-task-output-limiter` | `FAIL_SIM_CORRECTNESS` | out@253.76ns=-0.1000 expected=-0.2000 tol=0.0800 |
| `373-task-output-limiter` | `FAIL_SIM_CORRECTNESS` | metric@50.44ns=0.1250 expected=0.0000 tol=0.0800 |
| `373-task-output-limiter` | `FAIL_SIM_CORRECTNESS` | out@150.8ns=0.4500 expected=0.9000 tol=0.0800 |
| `374-task-dual-output-update` | `FAIL_SIM_CORRECTNESS` | out@52.52ns=0.0000 expected=0.1500 tol=0.0800 |
| `374-task-dual-output-update` | `FAIL_SIM_CORRECTNESS` | out@50.44ns=0.0250 expected=0.1500 tol=0.0800 |
| `374-task-dual-output-update` | `FAIL_SIM_CORRECTNESS` | metric@152.88ns=0.2778 expected=0.6111 tol=0.0800 |
| `374-task-dual-output-update` | `FAIL_SIM_CORRECTNESS` | metric@50.44ns=0.1250 expected=0.0000 tol=0.0800 |
| `374-task-dual-output-update` | `FAIL_SIM_CORRECTNESS` | out@152.88ns=0.2250 expected=0.4500 tol=0.0800 |
| `375-task-event-counter-service` | `FAIL_SIM_CORRECTNESS` | out@150.8ns=0.0000 expected=0.1500 tol=0.0800 |
| `375-task-event-counter-service` | `FAIL_SIM_CORRECTNESS` | out@50.44ns=0.1500 expected=0.0000 tol=0.0800 |
| `375-task-event-counter-service` | `FAIL_SIM_CORRECTNESS` | metric@150.8ns=0.1000 expected=0.2000 tol=0.0800 |
| `375-task-event-counter-service` | `FAIL_SIM_CORRECTNESS` | metric@150.8ns=0.3250 expected=0.2000 tol=0.0800 |
| `375-task-event-counter-service` | `FAIL_SIM_CORRECTNESS` | out@253.76ns=0.2000 expected=0.3000 tol=0.0800 |
| `376-task-reset-sequencer` | `FAIL_SIM_CORRECTNESS` | out@50.44ns=0.0000 expected=0.7500 tol=0.0800 |
| `376-task-reset-sequencer` | `FAIL_SIM_CORRECTNESS` | out@250.64ns=0.9000 expected=0.0000 tol=0.0800 |
| `376-task-reset-sequencer` | `FAIL_SIM_CORRECTNESS` | metric@352.56ns=0.5000 expected=0.2500 tol=0.0800 |
| `376-task-reset-sequencer` | `FAIL_SIM_CORRECTNESS` | metric@50.44ns=0.3750 expected=0.2500 tol=0.0800 |
| `376-task-reset-sequencer` | `FAIL_SIM_CORRECTNESS` | out@50.44ns=0.6500 expected=0.7500 tol=0.0800 |
| `377-task-stateful-threshold-update` | `FAIL_SIM_CORRECTNESS` | out@152.88ns=0.0000 expected=0.9000 tol=0.0800 |
| `377-task-stateful-threshold-update` | `FAIL_SIM_CORRECTNESS` | metric@50.44ns=0.3500 expected=0.4500 tol=0.0800 |
| `377-task-stateful-threshold-update` | `FAIL_SIM_CORRECTNESS` | metric@50.44ns=0.5500 expected=0.4500 tol=0.0800 |
| `377-task-stateful-threshold-update` | `FAIL_SIM_CORRECTNESS` | metric@50.44ns=0.5750 expected=0.4500 tol=0.0800 |
| `377-task-stateful-threshold-update` | `FAIL_SIM_CORRECTNESS` | out@152.88ns=0.4500 expected=0.9000 tol=0.0800 |
| `378-task-metric-normalizer` | `FAIL_SIM_CORRECTNESS` | out@52.52ns=0.0000 expected=0.1000 tol=0.0800 |
| `378-task-metric-normalizer` | `FAIL_SIM_CORRECTNESS` | metric@50.44ns=0.7000 expected=0.3500 tol=0.0800 |
| `378-task-metric-normalizer` | `FAIL_SIM_CORRECTNESS` | metric@50.44ns=0.0000 expected=0.3500 tol=0.0800 |
| `378-task-metric-normalizer` | `FAIL_SIM_CORRECTNESS` | metric@50.44ns=0.4750 expected=0.3500 tol=0.0800 |
| `378-task-metric-normalizer` | `FAIL_SIM_CORRECTNESS` | out@152.88ns=0.2250 expected=0.4500 tol=0.0800 |
| `379-file-fgets-config-loader` | `FAIL_SIM_CORRECTNESS` | metric@0ns=0.0000 expected=0.9000 tol=0.0800 |
| `379-file-fgets-config-loader` | `FAIL_SIM_CORRECTNESS` | metric@0ns=0.4500 expected=0.9000 tol=0.0800 |
| `379-file-fgets-config-loader` | `FAIL_SIM_CORRECTNESS` | out@52.52ns=0.0000 expected=0.9000 tol=0.0800 |
| `379-file-fgets-config-loader` | `FAIL_SIM_CORRECTNESS` | metric@0ns=0.7000 expected=0.9000 tol=0.0800 |
| `379-file-fgets-config-loader` | `FAIL_SIM_CORRECTNESS` | out@50.44ns=0.4500 expected=0.9000 tol=0.0800 |
| `380-file-feof-line-counter` | `FAIL_SIM_CORRECTNESS` | metric@0ns=0.0000 expected=0.9000 tol=0.0800 |
| `380-file-feof-line-counter` | `FAIL_SIM_CORRECTNESS` | metric@0ns=0.4500 expected=0.9000 tol=0.0800 |
| `380-file-feof-line-counter` | `FAIL_SIM_CORRECTNESS` | out@52.52ns=0.0000 expected=0.9000 tol=0.0800 |
| `380-file-feof-line-counter` | `FAIL_SIM_CORRECTNESS` | metric@0ns=0.7000 expected=0.9000 tol=0.0800 |
| `380-file-feof-line-counter` | `FAIL_SIM_CORRECTNESS` | out@50.44ns=0.4500 expected=0.9000 tol=0.0800 |
| `381-file-fseek-offset-reader` | `FAIL_SIM_CORRECTNESS` | metric@0ns=0.0000 expected=0.9000 tol=0.0800 |
| `381-file-fseek-offset-reader` | `FAIL_SIM_CORRECTNESS` | metric@0ns=0.4500 expected=0.9000 tol=0.0800 |
| `381-file-fseek-offset-reader` | `FAIL_SIM_CORRECTNESS` | out@52.52ns=0.0000 expected=0.9000 tol=0.0800 |
| `381-file-fseek-offset-reader` | `FAIL_SIM_CORRECTNESS` | metric@0ns=0.7000 expected=0.9000 tol=0.0800 |
| `381-file-fseek-offset-reader` | `FAIL_SIM_CORRECTNESS` | out@50.44ns=0.4500 expected=0.9000 tol=0.0800 |
| `382-file-ftell-position-meter` | `FAIL_SIM_CORRECTNESS` | metric@0ns=0.0000 expected=0.9000 tol=0.0800 |
| `382-file-ftell-position-meter` | `FAIL_SIM_CORRECTNESS` | metric@0ns=0.4500 expected=0.9000 tol=0.0800 |
| `382-file-ftell-position-meter` | `FAIL_SIM_CORRECTNESS` | out@52.52ns=0.0000 expected=0.9000 tol=0.0800 |
| `382-file-ftell-position-meter` | `FAIL_SIM_CORRECTNESS` | metric@0ns=0.7000 expected=0.9000 tol=0.0800 |
| `382-file-ftell-position-meter` | `FAIL_SIM_CORRECTNESS` | out@50.44ns=0.4500 expected=0.9000 tol=0.0800 |
| `383-file-rewind-second-pass` | `FAIL_SIM_CORRECTNESS` | metric@0ns=0.0000 expected=0.9000 tol=0.0800 |
| `383-file-rewind-second-pass` | `FAIL_SIM_CORRECTNESS` | metric@0ns=0.4500 expected=0.9000 tol=0.0800 |
| `383-file-rewind-second-pass` | `FAIL_SIM_CORRECTNESS` | out@52.52ns=0.0000 expected=0.9000 tol=0.0800 |
| `383-file-rewind-second-pass` | `FAIL_SIM_CORRECTNESS` | metric@0ns=0.7000 expected=0.9000 tol=0.0800 |
| `383-file-rewind-second-pass` | `FAIL_SIM_CORRECTNESS` | out@50.44ns=0.4500 expected=0.9000 tol=0.0800 |
| `384-file-fopen-mode-selector` | `FAIL_SIM_CORRECTNESS` | metric@0ns=0.0000 expected=0.9000 tol=0.0800 |
| `384-file-fopen-mode-selector` | `FAIL_SIM_CORRECTNESS` | metric@0ns=0.0000 expected=0.9000 tol=0.0800 |
| `384-file-fopen-mode-selector` | `FAIL_SIM_CORRECTNESS` | out@52.52ns=0.0000 expected=0.9000 tol=0.0800 |
| `384-file-fopen-mode-selector` | `FAIL_SIM_CORRECTNESS` | metric@0ns=0.7000 expected=0.9000 tol=0.0800 |
| `384-file-fopen-mode-selector` | `FAIL_SIM_CORRECTNESS` | out@50.44ns=0.4500 expected=0.9000 tol=0.0800 |
| `385-table-model-linear-gain` | `FAIL_SIM_CORRECTNESS` | out@152.88ns=0.0000 expected=0.3267 tol=0.0800 |
| `385-table-model-linear-gain` | `FAIL_SIM_CORRECTNESS` | out@251.68ns=0.9000 expected=0.5700 tol=0.0800 |
| `385-table-model-linear-gain` | `FAIL_SIM_CORRECTNESS` | out@50.44ns=0.1556 expected=0.0389 tol=0.0800 |
| `385-table-model-linear-gain` | `FAIL_SIM_CORRECTNESS` | metric@50.44ns=0.1682 expected=0.0432 tol=0.0800 |
| `385-table-model-linear-gain` | `FAIL_SIM_CORRECTNESS` | out@152.88ns=0.1633 expected=0.3267 tol=0.0800 |
| `386-table-model-clamped-transfer` | `FAIL_SIM_CORRECTNESS` | out@150.8ns=0.0000 expected=0.1167 tol=0.0800 |
| `386-table-model-clamped-transfer` | `FAIL_SIM_CORRECTNESS` | out@253.76ns=0.9000 expected=0.6800 tol=0.0800 |
| `386-table-model-clamped-transfer` | `FAIL_SIM_CORRECTNESS` | out@150.8ns=0.2333 expected=0.1167 tol=0.0800 |
| `386-table-model-clamped-transfer` | `FAIL_SIM_CORRECTNESS` | metric@50.44ns=0.1250 expected=0.0000 tol=0.0800 |
| `386-table-model-clamped-transfer` | `FAIL_SIM_CORRECTNESS` | out@253.76ns=0.3400 expected=0.6800 tol=0.0800 |
| `387-table-model-threshold-map` | `FAIL_SIM_CORRECTNESS` | out@150.8ns=0.0000 expected=0.6750 tol=0.0800 |
| `387-table-model-threshold-map` | `FAIL_SIM_CORRECTNESS` | out@150.8ns=0.0000 expected=0.6750 tol=0.0800 |
| `387-table-model-threshold-map` | `FAIL_SIM_CORRECTNESS` | out@50.44ns=0.9000 expected=0.0000 tol=0.0800 |
| `387-table-model-threshold-map` | `FAIL_SIM_CORRECTNESS` | metric@50.44ns=0.1250 expected=0.0000 tol=0.0800 |
| `387-table-model-threshold-map` | `FAIL_SIM_CORRECTNESS` | out@150.8ns=0.3375 expected=0.6750 tol=0.0800 |
| `388-table-model-dac-code-map` | `FAIL_SIM_CORRECTNESS` | out@50.44ns=0.0000 expected=0.1500 tol=0.0800 |
| `388-table-model-dac-code-map` | `FAIL_SIM_CORRECTNESS` | out@152.88ns=0.9000 expected=0.4500 tol=0.0800 |
| `388-table-model-dac-code-map` | `FAIL_SIM_CORRECTNESS` | out@50.44ns=0.3000 expected=0.1500 tol=0.0800 |
| `388-table-model-dac-code-map` | `FAIL_SIM_CORRECTNESS` | metric@50.44ns=0.2917 expected=0.1667 tol=0.0800 |
| `388-table-model-dac-code-map` | `FAIL_SIM_CORRECTNESS` | out@152.88ns=0.2250 expected=0.4500 tol=0.0800 |
| `389-table-model-temperature-profile` | `FAIL_SIM_CORRECTNESS` | out@50.44ns=0.0000 expected=0.6577 tol=0.0800 |
| `389-table-model-temperature-profile` | `FAIL_SIM_CORRECTNESS` | out@152.88ns=0.9000 expected=0.7833 tol=0.0800 |
| `389-table-model-temperature-profile` | `FAIL_SIM_CORRECTNESS` | out@50.44ns=0.8731 expected=0.6577 tol=0.0800 |
| `389-table-model-temperature-profile` | `FAIL_SIM_CORRECTNESS` | metric@50.44ns=0.8558 expected=0.7308 tol=0.0800 |
| `389-table-model-temperature-profile` | `FAIL_SIM_CORRECTNESS` | out@50.44ns=0.3288 expected=0.6577 tol=0.0800 |
| `390-table-model-piecewise-calibrator` | `FAIL_SIM_CORRECTNESS` | out@152.88ns=0.0000 expected=0.2900 tol=0.0800 |
| `390-table-model-piecewise-calibrator` | `FAIL_SIM_CORRECTNESS` | out@251.68ns=0.9000 expected=0.6233 tol=0.0800 |
| `390-table-model-piecewise-calibrator` | `FAIL_SIM_CORRECTNESS` | out@50.44ns=0.2083 expected=0.0417 tol=0.0800 |
| `390-table-model-piecewise-calibrator` | `FAIL_SIM_CORRECTNESS` | metric@50.44ns=0.1713 expected=0.0463 tol=0.0800 |
| `390-table-model-piecewise-calibrator` | `FAIL_SIM_CORRECTNESS` | out@152.88ns=0.1450 expected=0.2900 tol=0.0800 |
| `391-rdist-exponential-jitter` | `FAIL_SIM_CORRECTNESS` | out@50.82ns=0.0000 expected=0.6579 tol=0.0500 |
| `391-rdist-exponential-jitter` | `FAIL_SIM_CORRECTNESS` | out@50.82ns=0.9000 expected=0.6579 tol=0.0500 |
| `391-rdist-exponential-jitter` | `FAIL_SIM_CORRECTNESS` | metric@50.82ns=0.3618 expected=3.7943 tol=0.0500 |
| `391-rdist-exponential-jitter` | `FAIL_SIM_CORRECTNESS` | metric@50.82ns=3.9193 expected=3.7943 tol=0.0500 |
| `391-rdist-exponential-jitter` | `FAIL_SIM_CORRECTNESS` | out@50.82ns=0.3290 expected=0.6579 tol=0.0500 |
| `392-rdist-poisson-count-noise` | `FAIL_SIM_CORRECTNESS` | out@50.82ns=0.0000 expected=0.6500 tol=0.0500 |
| `392-rdist-poisson-count-noise` | `FAIL_SIM_CORRECTNESS` | out@50.82ns=0.9000 expected=0.6500 tol=0.0500 |
| `392-rdist-poisson-count-noise` | `FAIL_SIM_CORRECTNESS` | metric@50.82ns=0.0000 expected=3.0000 tol=0.0500 |
| `392-rdist-poisson-count-noise` | `FAIL_SIM_CORRECTNESS` | metric@50.82ns=3.1250 expected=3.0000 tol=0.0500 |
| `392-rdist-poisson-count-noise` | `FAIL_SIM_CORRECTNESS` | out@50.82ns=0.3250 expected=0.6500 tol=0.0500 |
| `393-rdist-normal-offset-dither` | `FAIL_SIM_CORRECTNESS` | out@50.82ns=0.0000 expected=0.6201 tol=0.0200 |
| `393-rdist-normal-offset-dither` | `FAIL_SIM_CORRECTNESS` | out@50.82ns=0.9000 expected=0.6201 tol=0.0200 |
| `393-rdist-normal-offset-dither` | `FAIL_SIM_CORRECTNESS` | metric@50.82ns=-0.0123 expected=0.0113 tol=0.0080 |
| `393-rdist-normal-offset-dither` | `FAIL_SIM_CORRECTNESS` | metric@50.82ns=0.1363 expected=0.0113 tol=0.0080 |
| `393-rdist-normal-offset-dither` | `FAIL_SIM_CORRECTNESS` | out@50.82ns=0.3101 expected=0.6201 tol=0.0200 |
| `394-rdist-chi-square-energy` | `FAIL_SIM_CORRECTNESS` | out@50.82ns=0.0000 expected=0.6250 tol=0.0300 |
| `394-rdist-chi-square-energy` | `FAIL_SIM_CORRECTNESS` | out@50.82ns=0.9000 expected=0.6250 tol=0.0300 |
| `394-rdist-chi-square-energy` | `FAIL_SIM_CORRECTNESS` | metric@50.82ns=0.1473 expected=0.5044 tol=0.0300 |
| `394-rdist-chi-square-energy` | `FAIL_SIM_CORRECTNESS` | metric@50.82ns=0.6294 expected=0.5044 tol=0.0300 |
| `394-rdist-chi-square-energy` | `FAIL_SIM_CORRECTNESS` | out@50.82ns=0.3125 expected=0.6250 tol=0.0300 |
| `395-rdist-t-tail-dither` | `FAIL_SIM_CORRECTNESS` | out@50.82ns=0.0000 expected=0.6025 tol=0.0300 |
| `395-rdist-t-tail-dither` | `FAIL_SIM_CORRECTNESS` | out@50.82ns=0.9000 expected=0.6025 tol=0.0300 |
| `395-rdist-t-tail-dither` | `FAIL_SIM_CORRECTNESS` | metric@50.82ns=0.0711 expected=-1.7540 tol=0.0300 |
| `395-rdist-t-tail-dither` | `FAIL_SIM_CORRECTNESS` | metric@50.82ns=-1.6290 expected=-1.7540 tol=0.0300 |
| `395-rdist-t-tail-dither` | `FAIL_SIM_CORRECTNESS` | out@50.82ns=0.3012 expected=0.6025 tol=0.0300 |
| `396-rdist-erlang-latency` | `FAIL_SIM_CORRECTNESS` | out@50.82ns=0.0000 expected=0.6309 tol=0.0300 |
| `396-rdist-erlang-latency` | `FAIL_SIM_CORRECTNESS` | out@50.82ns=0.9000 expected=0.6309 tol=0.0300 |
| `396-rdist-erlang-latency` | `FAIL_SIM_CORRECTNESS` | metric@50.82ns=0.7106 expected=1.0851 tol=0.0300 |
| `396-rdist-erlang-latency` | `FAIL_SIM_CORRECTNESS` | metric@50.82ns=1.2101 expected=1.0851 tol=0.0300 |
| `396-rdist-erlang-latency` | `FAIL_SIM_CORRECTNESS` | out@50.82ns=0.3154 expected=0.6309 tol=0.0300 |
| `397-hierarchy-gain-child` | `FAIL_SIM_CORRECTNESS` | out@0ns=-0.5600 expected=0.2000 tol=0.0350 |
| `397-hierarchy-gain-child` | `FAIL_SIM_CORRECTNESS` | metric@49.689ns=0.2250 expected=0.0000 tol=0.0350 |
| `397-hierarchy-gain-child` | `FAIL_SIM_CORRECTNESS` | out@0ns=-0.0700 expected=0.2000 tol=0.0350 |
| `397-hierarchy-gain-child` | `FAIL_SIM_CORRECTNESS` | metric@0ns=0.1250 expected=0.0000 tol=0.0350 |
| `397-hierarchy-gain-child` | `FAIL_SIM_CORRECTNESS` | out@0ns=-0.2800 expected=0.2000 tol=0.0350 |
| `398-hierarchy-two-stage-chain` | `FAIL_SIM_CORRECTNESS` | metric@0ns=0.0000 expected=0.2000 tol=0.0350 |
| `398-hierarchy-two-stage-chain` | `FAIL_SIM_CORRECTNESS` | metric@0ns=0.0000 expected=0.2000 tol=0.0350 |
| `398-hierarchy-two-stage-chain` | `FAIL_SIM_CORRECTNESS` | out@49.2618ns=0.0700 expected=0.1492 tol=0.0350 |
| `398-hierarchy-two-stage-chain` | `FAIL_SIM_CORRECTNESS` | metric@0ns=0.3250 expected=0.2000 tol=0.0350 |
| `398-hierarchy-two-stage-chain` | `FAIL_SIM_CORRECTNESS` | metric@0ns=0.1000 expected=0.2000 tol=0.0350 |
| `399-hierarchy-parameter-override` | `FAIL_SIM_CORRECTNESS` | out@0ns=-1.0500 expected=0.2700 tol=0.0400 |
| `399-hierarchy-parameter-override` | `FAIL_SIM_CORRECTNESS` | metric@99.2ns=0.2801 expected=0.0000 tol=0.0400 |
| `399-hierarchy-parameter-override` | `FAIL_SIM_CORRECTNESS` | out@0ns=-0.1400 expected=0.2700 tol=0.0400 |
| `399-hierarchy-parameter-override` | `FAIL_SIM_CORRECTNESS` | metric@0ns=0.1250 expected=0.0000 tol=0.0400 |
| `399-hierarchy-parameter-override` | `FAIL_SIM_CORRECTNESS` | out@0ns=-0.5250 expected=0.2700 tol=0.0400 |
| `400-hierarchy-named-port-map` | `FAIL_SIM_CORRECTNESS` | out@0ns=-0.5600 expected=0.2000 tol=0.0350 |
| `400-hierarchy-named-port-map` | `FAIL_SIM_CORRECTNESS` | metric@49.689ns=0.2250 expected=0.0000 tol=0.0350 |
| `400-hierarchy-named-port-map` | `FAIL_SIM_CORRECTNESS` | out@0ns=-0.0700 expected=0.2000 tol=0.0350 |
| `400-hierarchy-named-port-map` | `FAIL_SIM_CORRECTNESS` | metric@0ns=0.1250 expected=0.0000 tol=0.0350 |
| `400-hierarchy-named-port-map` | `FAIL_SIM_CORRECTNESS` | out@0ns=-0.2800 expected=0.2000 tol=0.0350 |
| `401-hierarchy-ordered-port-map` | `FAIL_SIM_CORRECTNESS` | metric@0ns=0.0000 expected=0.2000 tol=0.0350 |
| `401-hierarchy-ordered-port-map` | `FAIL_SIM_CORRECTNESS` | metric@0ns=0.0000 expected=0.2000 tol=0.0350 |
| `401-hierarchy-ordered-port-map` | `FAIL_SIM_CORRECTNESS` | out@49.2618ns=0.0700 expected=0.1492 tol=0.0350 |
| `401-hierarchy-ordered-port-map` | `FAIL_SIM_CORRECTNESS` | metric@0ns=0.3250 expected=0.2000 tol=0.0350 |
| `401-hierarchy-ordered-port-map` | `FAIL_SIM_CORRECTNESS` | metric@0ns=0.1000 expected=0.2000 tol=0.0350 |
| `402-hierarchy-shared-threshold-child` | `FAIL_SIM_CORRECTNESS` | out@0ns=-0.9000 expected=0.0000 tol=0.0400 |
| `402-hierarchy-shared-threshold-child` | `FAIL_SIM_CORRECTNESS` | metric@149.533ns=0.6750 expected=0.0000 tol=0.0400 |
| `402-hierarchy-shared-threshold-child` | `FAIL_SIM_CORRECTNESS` | out@0ns=-0.2000 expected=0.0000 tol=0.0400 |
| `402-hierarchy-shared-threshold-child` | `FAIL_SIM_CORRECTNESS` | metric@0ns=0.1250 expected=0.0000 tol=0.0400 |
| `402-hierarchy-shared-threshold-child` | `FAIL_SIM_CORRECTNESS` | out@0ns=-0.4500 expected=0.0000 tol=0.0400 |
| `403-vector-bit-select-flag` | `FAIL_SIM_CORRECTNESS` | out@53.04ns=0.0000 expected=0.9000 tol=0.0500 |
| `403-vector-bit-select-flag` | `FAIL_SIM_CORRECTNESS` | out@53.04ns=0.0000 expected=0.9000 tol=0.0500 |
| `403-vector-bit-select-flag` | `FAIL_SIM_CORRECTNESS` | metric@50.96ns=1.0000 expected=0.0000 tol=0.0500 |
| `403-vector-bit-select-flag` | `FAIL_SIM_CORRECTNESS` | metric@50.96ns=0.1250 expected=0.0000 tol=0.0500 |
| `403-vector-bit-select-flag` | `FAIL_SIM_CORRECTNESS` | out@50.96ns=0.4500 expected=0.9000 tol=0.0500 |
| `404-vector-part-select-window` | `FAIL_SIM_CORRECTNESS` | out@51.66ns=0.0000 expected=0.9000 tol=0.0500 |
| `404-vector-part-select-window` | `FAIL_SIM_CORRECTNESS` | out@51.66ns=0.0000 expected=0.9000 tol=0.0500 |
| `404-vector-part-select-window` | `FAIL_SIM_CORRECTNESS` | metric@51.66ns=5.0000 expected=4.0000 tol=0.0500 |
| `404-vector-part-select-window` | `FAIL_SIM_CORRECTNESS` | metric@51.66ns=4.1250 expected=4.0000 tol=0.0500 |
| `404-vector-part-select-window` | `FAIL_SIM_CORRECTNESS` | out@51.66ns=0.4500 expected=0.9000 tol=0.0500 |
| `405-vector-concat-code-build` | `FAIL_SIM_CORRECTNESS` | out@151.84ns=0.0000 expected=0.9000 tol=0.0500 |
| `405-vector-concat-code-build` | `FAIL_SIM_CORRECTNESS` | out@50.96ns=0.9000 expected=0.0000 tol=0.0500 |
| `405-vector-concat-code-build` | `FAIL_SIM_CORRECTNESS` | out@50.96ns=0.9000 expected=0.0000 tol=0.0500 |
| `405-vector-concat-code-build` | `FAIL_SIM_CORRECTNESS` | metric@50.96ns=8.1250 expected=8.0000 tol=0.0500 |
| `405-vector-concat-code-build` | `FAIL_SIM_CORRECTNESS` | out@151.84ns=0.4500 expected=0.9000 tol=0.0500 |
| `406-vector-replication-mask` | `FAIL_SIM_CORRECTNESS` | out@556.14ns=0.0000 expected=0.9000 tol=0.0500 |
| `406-vector-replication-mask` | `FAIL_SIM_CORRECTNESS` | out@52.7ns=0.9000 expected=0.0000 tol=0.0500 |
| `406-vector-replication-mask` | `FAIL_SIM_CORRECTNESS` | out@151.28ns=0.9000 expected=0.0000 tol=0.0500 |
| `406-vector-replication-mask` | `FAIL_SIM_CORRECTNESS` | metric@52.7ns=10.1250 expected=10.0000 tol=0.0500 |
| `406-vector-replication-mask` | `FAIL_SIM_CORRECTNESS` | out@553.66ns=0.4500 expected=0.9000 tol=0.0500 |
| `407-vector-reduction-parity` | `FAIL_SIM_CORRECTNESS` | out@52.7ns=0.0000 expected=0.9000 tol=0.0500 |
| `407-vector-reduction-parity` | `FAIL_SIM_CORRECTNESS` | out@556.14ns=0.9000 expected=0.0000 tol=0.0500 |
| `407-vector-reduction-parity` | `FAIL_SIM_CORRECTNESS` | out@151.28ns=0.0000 expected=0.9000 tol=0.0500 |
| `407-vector-reduction-parity` | `FAIL_SIM_CORRECTNESS` | metric@52.7ns=1.1250 expected=1.0000 tol=0.0500 |
| `407-vector-reduction-parity` | `FAIL_SIM_CORRECTNESS` | out@52.7ns=0.4500 expected=0.9000 tol=0.0500 |
| `408-vector-shift-and-mask-decoder` | `FAIL_SIM_CORRECTNESS` | out@52.44ns=0.0000 expected=0.9000 tol=0.0500 |
| `408-vector-shift-and-mask-decoder` | `FAIL_SIM_CORRECTNESS` | out@252.08ns=0.9000 expected=0.0000 tol=0.0500 |
| `408-vector-shift-and-mask-decoder` | `FAIL_SIM_CORRECTNESS` | out@153.64ns=0.0000 expected=0.9000 tol=0.0500 |
| `408-vector-shift-and-mask-decoder` | `FAIL_SIM_CORRECTNESS` | metric@52.44ns=2.1250 expected=2.0000 tol=0.0500 |
| `408-vector-shift-and-mask-decoder` | `FAIL_SIM_CORRECTNESS` | out@52.44ns=0.4500 expected=0.9000 tol=0.0500 |
| `409-macro-functionlike-clamp` | `FAIL_SIM_CORRECTNESS` | out@50.44ns=0.0000 expected=0.9000 tol=0.0800 |
| `409-macro-functionlike-clamp` | `FAIL_SIM_CORRECTNESS` | out@50.44ns=0.6000 expected=0.9000 tol=0.0800 |
| `409-macro-functionlike-clamp` | `FAIL_SIM_CORRECTNESS` | metric@50.44ns=0.2500 expected=1.0000 tol=0.0800 |
| `409-macro-functionlike-clamp` | `FAIL_SIM_CORRECTNESS` | metric@50.44ns=1.1250 expected=1.0000 tol=0.0800 |
| `409-macro-functionlike-clamp` | `FAIL_SIM_CORRECTNESS` | out@50.44ns=0.4500 expected=0.9000 tol=0.0800 |
| `410-macro-ifdef-gain-select` | `FAIL_SIM_CORRECTNESS` | out@60ns=0.0000 expected=0.1500 tol=0.0800 |
| `410-macro-ifdef-gain-select` | `FAIL_SIM_CORRECTNESS` | out@160ns=0.9000 expected=0.8000 tol=0.0800 |
| `410-macro-ifdef-gain-select` | `FAIL_SIM_CORRECTNESS` | metric@60ns=0.2500 expected=1.2500 tol=0.0800 |
| `410-macro-ifdef-gain-select` | `FAIL_SIM_CORRECTNESS` | metric@60ns=1.3750 expected=1.2500 tol=0.0800 |
| `410-macro-ifdef-gain-select` | `FAIL_SIM_CORRECTNESS` | out@160ns=0.4000 expected=0.8000 tol=0.0800 |
| `411-escaped-identifier-state` | `FAIL_SIM_CORRECTNESS` | out@50.82ns=0.0000 expected=0.7500 tol=0.0800 |
| `411-escaped-identifier-state` | `FAIL_SIM_CORRECTNESS` | out@50.82ns=0.6000 expected=0.7500 tol=0.0800 |
| `411-escaped-identifier-state` | `FAIL_SIM_CORRECTNESS` | metric@351.12ns=0.2500 expected=0.1000 tol=0.0800 |
| `411-escaped-identifier-state` | `FAIL_SIM_CORRECTNESS` | metric@50.82ns=0.3250 expected=0.2000 tol=0.0800 |
| `411-escaped-identifier-state` | `FAIL_SIM_CORRECTNESS` | out@50.82ns=0.3750 expected=0.7500 tol=0.0800 |
| `412-initial-final-step-lifecycle` | `FAIL_SIM_CORRECTNESS` | out@52.5ns=0.0000 expected=0.6500 tol=0.0800 |
| `412-initial-final-step-lifecycle` | `FAIL_SIM_CORRECTNESS` | out@50.82ns=0.9000 expected=0.6500 tol=0.0800 |
| `412-initial-final-step-lifecycle` | `FAIL_SIM_CORRECTNESS` | metric@50.82ns=0.2500 expected=0.0000 tol=0.0800 |
| `412-initial-final-step-lifecycle` | `FAIL_SIM_CORRECTNESS` | metric@50.82ns=0.1250 expected=0.0000 tol=0.0800 |
| `412-initial-final-step-lifecycle` | `FAIL_SIM_CORRECTNESS` | out@50.82ns=0.3250 expected=0.6500 tol=0.0800 |
| `413-while-loop-array-sum` | `FAIL_SIM_CORRECTNESS` | out@150.36ns=0.0000 expected=0.9000 tol=0.0800 |
| `413-while-loop-array-sum` | `FAIL_SIM_CORRECTNESS` | out@349.5ns=0.2251 expected=0.0000 tol=0.0800 |
| `413-while-loop-array-sum` | `FAIL_SIM_CORRECTNESS` | out@49.5001ns=0.2251 expected=0.0000 tol=0.0800 |
| `413-while-loop-array-sum` | `FAIL_SIM_CORRECTNESS` | metric@50.82ns=3.1250 expected=3.0000 tol=0.0800 |
| `413-while-loop-array-sum` | `FAIL_SIM_CORRECTNESS` | out@150.36ns=0.4500 expected=0.9000 tol=0.0800 |
| `414-parameter-range-real-control` | `FAIL_SIM_CORRECTNESS` | out@50.82ns=0.0000 expected=0.2800 tol=0.0800 |
| `414-parameter-range-real-control` | `FAIL_SIM_CORRECTNESS` | out@150.36ns=0.9000 expected=0.6000 tol=0.0800 |
| `414-parameter-range-real-control` | `FAIL_SIM_CORRECTNESS` | metric@50.82ns=2.0000 expected=1.0000 tol=0.0800 |
| `414-parameter-range-real-control` | `FAIL_SIM_CORRECTNESS` | metric@50.82ns=1.1250 expected=1.0000 tol=0.0800 |
| `414-parameter-range-real-control` | `FAIL_SIM_CORRECTNESS` | out@50.82ns=0.1400 expected=0.2800 tol=0.0800 |
| `415-logic-vector-assign-slice` | `FAIL_SIM_CORRECTNESS` | y@50ns=0.0000 expected=1.0000 tol=0.0800 |
| `415-logic-vector-assign-slice` | `FAIL_SIM_CORRECTNESS` | y@150ns=0.0000 expected=1.0000 tol=0.0800 |
| `415-logic-vector-assign-slice` | `FAIL_SIM_CORRECTNESS` | y@50ns=0.0000 expected=1.0000 tol=0.0800 |
| `415-logic-vector-assign-slice` | `FAIL_SIM_CORRECTNESS` | y@150ns=0.0000 expected=1.0000 tol=0.0800 |
| `415-logic-vector-assign-slice` | `FAIL_SIM_CORRECTNESS` | y@300ns=0.0000 expected=1.0000 tol=0.0800 |
| `416-logic-vector-reduction-flag` | `FAIL_SIM_CORRECTNESS` | valid@50ns=0.0000 expected=1.0000 tol=0.0800 |
| `416-logic-vector-reduction-flag` | `FAIL_SIM_CORRECTNESS` | valid@50ns=0.0000 expected=1.0000 tol=0.0800 |
| `416-logic-vector-reduction-flag` | `FAIL_SIM_CORRECTNESS` | valid@50ns=0.0000 expected=1.0000 tol=0.0800 |
| `416-logic-vector-reduction-flag` | `FAIL_SIM_CORRECTNESS` | valid@250ns=0.0000 expected=1.0000 tol=0.0800 |
| `416-logic-vector-reduction-flag` | `FAIL_SIM_CORRECTNESS` | valid@50ns=0.0000 expected=1.0000 tol=0.0800 |
| `417-always-async-reset-counter` | `FAIL_SIM_CORRECTNESS` | q@100ns=0.0000 expected=1.0000 tol=0.0800 |
| `417-always-async-reset-counter` | `FAIL_SIM_CORRECTNESS` | q@100ns=0.0000 expected=1.0000 tol=0.0800 |
| `417-always-async-reset-counter` | `FAIL_SIM_CORRECTNESS` | q@300ns=1.0000 expected=0.0000 tol=0.0800 |
| `417-always-async-reset-counter` | `FAIL_SIM_CORRECTNESS` | q@100ns=0.0000 expected=1.0000 tol=0.0800 |
| `417-always-async-reset-counter` | `FAIL_SIM_CORRECTNESS` | q@100ns=0.0000 expected=1.0000 tol=0.0800 |
| `418-always-enable-saturating-counter` | `FAIL_SIM_CORRECTNESS` | q0@90ns=0.0000 expected=1.0000 tol=0.0800 |
| `418-always-enable-saturating-counter` | `FAIL_SIM_CORRECTNESS` | q0@200ns=1.0000 expected=0.0000 tol=0.0800 |
| `418-always-enable-saturating-counter` | `FAIL_SIM_CORRECTNESS` | q0@400ns=1.0000 expected=0.0000 tol=0.0800 |
| `418-always-enable-saturating-counter` | `FAIL_SIM_CORRECTNESS` | q0@90ns=0.0000 expected=1.0000 tol=0.0800 |
| `418-always-enable-saturating-counter` | `FAIL_SIM_CORRECTNESS` | q0@90ns=0.0000 expected=1.0000 tol=0.0800 |
| `419-wreal-logic-threshold-bridge` | `FAIL_SIM_CORRECTNESS` | flag@80ns=0.0000 expected=1.0000 tol=0.0800 |
| `419-wreal-logic-threshold-bridge` | `FAIL_SIM_CORRECTNESS` | flag@80ns=0.0000 expected=1.0000 tol=0.0800 |
| `419-wreal-logic-threshold-bridge` | `FAIL_SIM_CORRECTNESS` | flag@0ns=1.0000 expected=0.0000 tol=0.0800 |
| `419-wreal-logic-threshold-bridge` | `FAIL_SIM_CORRECTNESS` | flag@152ns=1.0000 expected=0.0000 tol=0.0800 |
| `419-wreal-logic-threshold-bridge` | `FAIL_SIM_CORRECTNESS` | flag@380ns=1.0000 expected=0.0000 tol=0.0800 |
| `420-mixed-analog-digital-mode-latch` | `FAIL_SIM_CORRECTNESS` | flag@100.1ns=0.0000 expected=1.0000 tol=0.0800 |
| `420-mixed-analog-digital-mode-latch` | `FAIL_SIM_CORRECTNESS` | flag@100.1ns=0.0000 expected=1.0000 tol=0.0800 |
| `420-mixed-analog-digital-mode-latch` | `FAIL_SIM_CORRECTNESS` | flag@199.65ns=1.0000 expected=0.0000 tol=0.0800 |
| `420-mixed-analog-digital-mode-latch` | `FAIL_SIM_CORRECTNESS` | flag@100.1ns=0.0000 expected=1.0000 tol=0.0800 |
| `420-mixed-analog-digital-mode-latch` | `FAIL_SIM_CORRECTNESS` | flag@100.1ns=0.0000 expected=1.0000 tol=0.0800 |
| `421-task-local-variable-transform` | `FAIL_SIM_CORRECTNESS` | out@102.85ns=0.0000 expected=0.9000 tol=0.0800 |
| `421-task-local-variable-transform` | `FAIL_SIM_CORRECTNESS` | out@300.3ns=0.9000 expected=0.6200 tol=0.0800 |
| `421-task-local-variable-transform` | `FAIL_SIM_CORRECTNESS` | metric@400.95ns=0.2500 expected=0.0000 tol=0.0800 |
| `421-task-local-variable-transform` | `FAIL_SIM_CORRECTNESS` | metric@102.85ns=1.1250 expected=1.0000 tol=0.0800 |
| `421-task-local-variable-transform` | `FAIL_SIM_CORRECTNESS` | out@102.85ns=0.4500 expected=0.9000 tol=0.0800 |
| `422-file-fscanf-table-stimulus` | `FAIL_SIM_CORRECTNESS` | out@99.55ns=0.3500 expected=0.7000 tol=0.0800 |
| `422-file-fscanf-table-stimulus` | `FAIL_SIM_CORRECTNESS` | out@99.55ns=0.8000 expected=0.7000 tol=0.0800 |
| `422-file-fscanf-table-stimulus` | `FAIL_SIM_CORRECTNESS` | metric@199.6ns=0.1876 expected=0.0000 tol=0.0800 |
| `422-file-fscanf-table-stimulus` | `FAIL_SIM_CORRECTNESS` | metric@101.7ns=0.1250 expected=0.0000 tol=0.0800 |
| `422-file-fscanf-table-stimulus` | `FAIL_SIM_CORRECTNESS` | out@99.55ns=0.5250 expected=0.7000 tol=0.0800 |
| `423-file-profile-replay-controller` | `FAIL_SIM_CORRECTNESS` | out@200.25ns=0.0000 expected=0.9000 tol=0.0800 |
| `423-file-profile-replay-controller` | `FAIL_SIM_CORRECTNESS` | out@300.6ns=0.9000 expected=0.0000 tol=0.0800 |
| `423-file-profile-replay-controller` | `FAIL_SIM_CORRECTNESS` | metric@400.95ns=0.2500 expected=0.0000 tol=0.0800 |
| `423-file-profile-replay-controller` | `FAIL_SIM_CORRECTNESS` | metric@101.7ns=1.1250 expected=1.0000 tol=0.0800 |
| `423-file-profile-replay-controller` | `FAIL_SIM_CORRECTNESS` | out@200.25ns=0.4500 expected=0.9000 tol=0.0800 |
| `424-file-fscanf-multi-column-profile` | `FAIL_SIM_CORRECTNESS` | out@99.55ns=0.3500 expected=0.7000 tol=0.0800 |
| `424-file-fscanf-multi-column-profile` | `FAIL_SIM_CORRECTNESS` | out@99.55ns=0.8000 expected=0.7000 tol=0.0800 |
| `424-file-fscanf-multi-column-profile` | `FAIL_SIM_CORRECTNESS` | metric@202.05ns=0.2500 expected=0.0000 tol=0.0800 |
| `424-file-fscanf-multi-column-profile` | `FAIL_SIM_CORRECTNESS` | metric@101.7ns=0.6250 expected=0.5000 tol=0.0800 |
| `424-file-fscanf-multi-column-profile` | `FAIL_SIM_CORRECTNESS` | out@99.55ns=0.5250 expected=0.7000 tol=0.0800 |
| `425-string-swrite-label-builder` | `FAIL_SIM_CORRECTNESS` | out@200.25ns=0.0000 expected=0.9000 tol=0.0800 |
| `425-string-swrite-label-builder` | `FAIL_SIM_CORRECTNESS` | out@300.6ns=0.9000 expected=0.0000 tol=0.0800 |
| `425-string-swrite-label-builder` | `FAIL_SIM_CORRECTNESS` | metric@400.95ns=0.2500 expected=0.0000 tol=0.0800 |
| `425-string-swrite-label-builder` | `FAIL_SIM_CORRECTNESS` | metric@101.7ns=0.1250 expected=0.0000 tol=0.0800 |
| `425-string-swrite-label-builder` | `FAIL_SIM_CORRECTNESS` | out@200.25ns=0.4500 expected=0.9000 tol=0.0800 |
| `426-string-sformat-mode-tag` | `FAIL_SIM_CORRECTNESS` | out@200.25ns=0.0000 expected=0.9000 tol=0.0800 |
| `426-string-sformat-mode-tag` | `FAIL_SIM_CORRECTNESS` | out@300.6ns=0.9000 expected=0.0000 tol=0.0800 |
| `426-string-sformat-mode-tag` | `FAIL_SIM_CORRECTNESS` | metric@400.95ns=0.2500 expected=0.0000 tol=0.0800 |
| `426-string-sformat-mode-tag` | `FAIL_SIM_CORRECTNESS` | metric@101.7ns=0.1250 expected=0.0000 tol=0.0800 |
| `426-string-sformat-mode-tag` | `FAIL_SIM_CORRECTNESS` | out@200.25ns=0.4500 expected=0.9000 tol=0.0800 |
| `427-string-formatted-metric-line` | `FAIL_SIM_CORRECTNESS` | out@200.25ns=0.0000 expected=0.9000 tol=0.0800 |
| `427-string-formatted-metric-line` | `FAIL_SIM_CORRECTNESS` | out@300.6ns=0.9000 expected=0.0000 tol=0.0800 |
| `427-string-formatted-metric-line` | `FAIL_SIM_CORRECTNESS` | metric@400.95ns=0.2500 expected=0.0000 tol=0.0800 |
| `427-string-formatted-metric-line` | `FAIL_SIM_CORRECTNESS` | metric@101.7ns=0.1250 expected=0.0000 tol=0.0800 |
| `427-string-formatted-metric-line` | `FAIL_SIM_CORRECTNESS` | out@200.25ns=0.4500 expected=0.9000 tol=0.0800 |
| `428-string-mode-tagged-log` | `FAIL_SIM_CORRECTNESS` | out@200.25ns=0.0000 expected=0.9000 tol=0.0800 |
| `428-string-mode-tagged-log` | `FAIL_SIM_CORRECTNESS` | out@300.6ns=0.9000 expected=0.0000 tol=0.0800 |
| `428-string-mode-tagged-log` | `FAIL_SIM_CORRECTNESS` | metric@400.95ns=0.2500 expected=0.0000 tol=0.0800 |
| `428-string-mode-tagged-log` | `FAIL_SIM_CORRECTNESS` | metric@101.7ns=0.1250 expected=0.0000 tol=0.0800 |
| `428-string-mode-tagged-log` | `FAIL_SIM_CORRECTNESS` | out@200.25ns=0.4500 expected=0.9000 tol=0.0800 |
| `429-string-config-label-select` | `FAIL_SIM_CORRECTNESS` | out@101.7ns=0.0000 expected=0.9000 tol=0.0800 |
| `429-string-config-label-select` | `FAIL_SIM_CORRECTNESS` | out@399.6ns=0.6747 expected=0.0000 tol=0.0800 |
| `429-string-config-label-select` | `FAIL_SIM_CORRECTNESS` | metric@302.4ns=0.2500 expected=0.0000 tol=0.0800 |
| `429-string-config-label-select` | `FAIL_SIM_CORRECTNESS` | metric@101.7ns=10.1250 expected=10.0000 tol=0.0800 |
| `429-string-config-label-select` | `FAIL_SIM_CORRECTNESS` | out@101.7ns=0.4500 expected=0.9000 tol=0.0800 |
| `430-rdist-seed-reproducibility` | `FAIL_SIM_CORRECTNESS` | out@101.7ns=0.0000 expected_near_vin=0.6200 |
| `430-rdist-seed-reproducibility` | `FAIL_SIM_CORRECTNESS` | out@101.7ns=0.9000 expected_near_vin=0.6200 |
| `430-rdist-seed-reproducibility` | `FAIL_SIM_CORRECTNESS` | metric@302.4ns=0.2500 expected=1.0000 tol=0.0800 |
| `430-rdist-seed-reproducibility` | `FAIL_SIM_CORRECTNESS` | metric@101.7ns=1.1250 expected=1.0000 tol=0.0800 |
| `430-rdist-seed-reproducibility` | `FAIL_SIM_CORRECTNESS` | out@101.7ns=0.3150 expected_near_vin=0.6200 |
| `431-hierarchy-support-artifact-staging` | `FAIL_SIM_CORRECTNESS` | metric@100ns=0.0000 expected=0.7125 tol=0.0800 |
| `431-hierarchy-support-artifact-staging` | `FAIL_SIM_CORRECTNESS` | metric@100ns=0.9000 expected=0.7125 tol=0.0800 |
| `431-hierarchy-support-artifact-staging` | `FAIL_SIM_CORRECTNESS` | metric@220ns=0.2500 expected=1.2000 tol=0.0800 |
| `431-hierarchy-support-artifact-staging` | `FAIL_SIM_CORRECTNESS` | metric@100ns=0.8375 expected=0.7125 tol=0.0800 |
| `431-hierarchy-support-artifact-staging` | `FAIL_SIM_CORRECTNESS` | metric@100ns=0.3563 expected=0.7125 tol=0.0800 |
| `432-hierarchy-nested-parameter-chain` | `FAIL_SIM_CORRECTNESS` | metric@80ns=0.0000 expected=0.3600 tol=0.0800 |
| `432-hierarchy-nested-parameter-chain` | `FAIL_SIM_CORRECTNESS` | metric@80ns=0.0000 expected=0.3600 tol=0.0800 |
| `432-hierarchy-nested-parameter-chain` | `FAIL_SIM_CORRECTNESS` | metric@220ns=0.2500 expected=1.4400 tol=0.0800 |
| `432-hierarchy-nested-parameter-chain` | `FAIL_SIM_CORRECTNESS` | metric@80ns=0.4850 expected=0.3600 tol=0.0800 |
| `432-hierarchy-nested-parameter-chain` | `FAIL_SIM_CORRECTNESS` | metric@80ns=0.1800 expected=0.3600 tol=0.0800 |
| `433-preprocessor-ifndef-elsif-undef` | `FAIL_SIM_CORRECTNESS` | out@101.7ns=0.0000 expected=0.1500 tol=0.0800 |
| `433-preprocessor-ifndef-elsif-undef` | `FAIL_SIM_CORRECTNESS` | out@202.05ns=0.9000 expected=0.6150 tol=0.0800 |
| `433-preprocessor-ifndef-elsif-undef` | `FAIL_SIM_CORRECTNESS` | metric@302.4ns=0.2500 expected=0.0000 tol=0.0800 |
| `433-preprocessor-ifndef-elsif-undef` | `FAIL_SIM_CORRECTNESS` | metric@101.7ns=0.8750 expected=0.7500 tol=0.0800 |
| `433-preprocessor-ifndef-elsif-undef` | `FAIL_SIM_CORRECTNESS` | out@202.05ns=0.3075 expected=0.6150 tol=0.0800 |
| `434-repeat-loop-accumulator` | `FAIL_SIM_CORRECTNESS` | out@202.05ns=0.0000 expected=0.9000 tol=0.0800 |
| `434-repeat-loop-accumulator` | `FAIL_SIM_CORRECTNESS` | out@399.6ns=0.6747 expected=0.0000 tol=0.0800 |
| `434-repeat-loop-accumulator` | `FAIL_SIM_CORRECTNESS` | metric@302.4ns=0.2500 expected=0.0000 tol=0.0800 |
| `434-repeat-loop-accumulator` | `FAIL_SIM_CORRECTNESS` | metric@101.7ns=4.1250 expected=4.0000 tol=0.0800 |
| `434-repeat-loop-accumulator` | `FAIL_SIM_CORRECTNESS` | out@202.05ns=0.4500 expected=0.9000 tol=0.0800 |
| `435-ddt-voltage-derivative-source` | `FAIL_SIM_CORRECTNESS` | out_second_sample=0 expected_ddt=8.653e+05 metric_second_sample=0 expected_ddt=8.653e+05 |
| `435-ddt-voltage-derivative-source` | `FAIL_SIM_CORRECTNESS` | out_second_sample=0.9 expected_ddt=8.653e+05 metric_second_sample=0.9 expected_ddt=8.653e+05 |
| `435-ddt-voltage-derivative-source` | `FAIL_SIM_CORRECTNESS` | out_first_sample=1e+05 expected_initial_ddt=0 out_second_sample=9.653e+05 expected_ddt=8.653e+05 metric_first_sample=1e+05 expected_initial_ddt=0 metric_second_sample=9.653e+05 expected_ddt=8.653e+05 |
| `435-ddt-voltage-derivative-source` | `FAIL_SIM_CORRECTNESS` | out_first_sample=0.125 expected_initial_ddt=0 metric_first_sample=0.125 expected_initial_ddt=0 |
| `435-ddt-voltage-derivative-source` | `FAIL_SIM_CORRECTNESS` | out_second_sample=4.326e+05 expected_ddt=8.653e+05 metric_second_sample=4.326e+05 expected_ddt=8.653e+05 |
| `436-idt-voltage-integrator-source` | `FAIL_SIM_CORRECTNESS` | out_second_sample=0 expected_idt=7.5e-08 metric_second_sample=0 expected_idt=7.5e-08 |
| `436-idt-voltage-integrator-source` | `FAIL_SIM_CORRECTNESS` | out_second_sample=0 expected_idt=7.5e-08 metric_second_sample=0 expected_idt=7.5e-08 |
| `436-idt-voltage-integrator-source` | `FAIL_SIM_CORRECTNESS` | out_first_sample=2e-08 expected_initial_idt=0 out_second_sample=9.5e-08 expected_idt=7.5e-08 metric_first_sample=2e-08 expected_initial_idt=0 metric_second_sample=9.5e-08 expected_idt=7.5e-08 |
| `436-idt-voltage-integrator-source` | `FAIL_SIM_CORRECTNESS` | out_first_sample=0.125 expected_initial_idt=0 out_second_sample=0.125 expected_idt=7.5e-08 metric_first_sample=0.125 expected_initial_idt=0 metric_second_sample=0.125 expected_idt=7.5e-08 |
| `436-idt-voltage-integrator-source` | `FAIL_SIM_CORRECTNESS` | out_second_sample=3.75e-08 expected_idt=7.5e-08 metric_second_sample=3.75e-08 expected_idt=7.5e-08 |
| `437-laplace-nd-lowpass-filter` | `FAIL_SIM_CORRECTNESS` | out_first_sample=0 expected_laplace_init=0.8 out_second_sample=0 expected_laplace=0.8 metric_first_sample=0 expected_laplace_init=0.8 metric_second_sample=0 expected_laplace=0.8 |
| `437-laplace-nd-lowpass-filter` | `FAIL_SIM_CORRECTNESS` | out_first_sample=0.9 expected_laplace_init=0.8 out_second_sample=0.9 expected_laplace=0.8 metric_first_sample=0.9 expected_laplace_init=0.8 metric_second_sample=0.9 expected_laplace=0.8 |
| `437-laplace-nd-lowpass-filter` | `FAIL_SIM_CORRECTNESS` | out_first_sample=0.82 expected_laplace_init=0.8 metric_first_sample=0.82 expected_laplace_init=0.8 |
| `437-laplace-nd-lowpass-filter` | `FAIL_SIM_CORRECTNESS` | out_first_sample=0.925 expected_laplace_init=0.8 out_second_sample=0.925 expected_laplace=0.8 metric_first_sample=0.925 expected_laplace_init=0.8 metric_second_sample=0.925 expected_laplace=0.8 |
| `437-laplace-nd-lowpass-filter` | `FAIL_SIM_CORRECTNESS` | out_first_sample=0.4 expected_laplace_init=0.8 out_second_sample=0.4 expected_laplace=0.8 metric_first_sample=0.4 expected_laplace_init=0.8 metric_second_sample=0.4 expected_laplace=0.8 |
| `438-laplace-np-pole-filter` | `FAIL_SIM_CORRECTNESS` | out_first_sample=0 expected_laplace_init=0.6 out_second_sample=0 expected_laplace=0.6 metric_first_sample=0 expected_laplace_init=0.6 metric_second_sample=0 expected_laplace=0.6 |
| `438-laplace-np-pole-filter` | `FAIL_SIM_CORRECTNESS` | out_first_sample=0.9 expected_laplace_init=0.6 out_second_sample=0.9 expected_laplace=0.6 metric_first_sample=0.9 expected_laplace_init=0.6 metric_second_sample=0.9 expected_laplace=0.6 |
| `438-laplace-np-pole-filter` | `FAIL_SIM_CORRECTNESS` | out_first_sample=0.62 expected_laplace_init=0.6 metric_first_sample=0.62 expected_laplace_init=0.6 |
| `438-laplace-np-pole-filter` | `FAIL_SIM_CORRECTNESS` | out_first_sample=0.725 expected_laplace_init=0.6 out_second_sample=0.725 expected_laplace=0.6 metric_first_sample=0.725 expected_laplace_init=0.6 metric_second_sample=0.725 expected_laplace=0.6 |
| `438-laplace-np-pole-filter` | `FAIL_SIM_CORRECTNESS` | out_first_sample=0.3 expected_laplace_init=0.6 out_second_sample=0.3 expected_laplace=0.6 metric_first_sample=0.3 expected_laplace_init=0.6 metric_second_sample=0.3 expected_laplace=0.6 |
| `439-laplace-zd-zero-den-filter` | `FAIL_SIM_CORRECTNESS` | out_first_sample=0 expected_laplace_init=0.75 out_second_sample=0 expected_laplace=0.75 metric_first_sample=0 expected_laplace_init=0.75 metric_second_sample=0 expected_laplace=0.75 |
| `439-laplace-zd-zero-den-filter` | `FAIL_SIM_CORRECTNESS` | out_first_sample=0.9 expected_laplace_init=0.75 out_second_sample=0.9 expected_laplace=0.75 metric_first_sample=0.9 expected_laplace_init=0.75 metric_second_sample=0.9 expected_laplace=0.75 |
| `439-laplace-zd-zero-den-filter` | `FAIL_SIM_CORRECTNESS` | out_first_sample=0.77 expected_laplace_init=0.75 metric_first_sample=0.77 expected_laplace_init=0.75 |
| `439-laplace-zd-zero-den-filter` | `FAIL_SIM_CORRECTNESS` | out_first_sample=0.875 expected_laplace_init=0.75 out_second_sample=0.875 expected_laplace=0.75 metric_first_sample=0.875 expected_laplace_init=0.75 metric_second_sample=0.875 expected_laplace=0.75 |
| `439-laplace-zd-zero-den-filter` | `FAIL_SIM_CORRECTNESS` | out_first_sample=0.375 expected_laplace_init=0.75 out_second_sample=0.375 expected_laplace=0.75 metric_first_sample=0.375 expected_laplace_init=0.75 metric_second_sample=0.375 expected_laplace=0.75 |
| `440-laplace-zp-zero-pole-filter` | `FAIL_SIM_CORRECTNESS` | out_second_sample=0 expected_laplace=1.35e-07 metric_second_sample=0 expected_laplace=1.35e-07 |
| `440-laplace-zp-zero-pole-filter` | `FAIL_SIM_CORRECTNESS` | out_second_sample=0 expected_laplace=1.35e-07 metric_second_sample=0 expected_laplace=1.35e-07 |
| `440-laplace-zp-zero-pole-filter` | `FAIL_SIM_CORRECTNESS` | out_first_sample=0.02 expected_laplace_init=0 out_second_sample=0.02 expected_laplace=1.35e-07 metric_first_sample=0.02 expected_laplace_init=0 metric_second_sample=0.02 expected_laplace=1.35e-07 |
| `440-laplace-zp-zero-pole-filter` | `FAIL_SIM_CORRECTNESS` | out_first_sample=0.125 expected_laplace_init=0 out_second_sample=0.125 expected_laplace=1.35e-07 metric_first_sample=0.125 expected_laplace_init=0 metric_second_sample=0.125 expected_laplace=1.35e-07 |
| `440-laplace-zp-zero-pole-filter` | `FAIL_SIM_CORRECTNESS` | out_second_sample=6.75e-08 expected_laplace=1.35e-07 metric_second_sample=6.75e-08 expected_laplace=1.35e-07 |
| `441-zi-nd-discrete-filter` | `FAIL_SIM_CORRECTNESS` | out_first_sample=0 expected_zi_init=0.7 metric_first_sample=0 expected_zi_init=0.7 |
| `441-zi-nd-discrete-filter` | `FAIL_SIM_CORRECTNESS` | out_first_sample=0.9 expected_zi_init=0.7 metric_first_sample=0.9 expected_zi_init=0.7 |
| `441-zi-nd-discrete-filter` | `FAIL_SIM_CORRECTNESS` | out_first_sample=0.72 expected_zi_init=0.7 out_second_sample=0.02 expected_zi=0 metric_first_sample=0.72 expected_zi_init=0.7 metric_second_sample=0.02 expected_zi=0 |
| `441-zi-nd-discrete-filter` | `FAIL_SIM_CORRECTNESS` | out_first_sample=0.825 expected_zi_init=0.7 out_second_sample=0.125 expected_zi=0 metric_first_sample=0.825 expected_zi_init=0.7 metric_second_sample=0.125 expected_zi=0 |
| `441-zi-nd-discrete-filter` | `FAIL_SIM_CORRECTNESS` | out_first_sample=0.35 expected_zi_init=0.7 metric_first_sample=0.35 expected_zi_init=0.7 |
| `442-zi-np-discrete-filter` | `FAIL_SIM_CORRECTNESS` | out_first_sample=0 expected_zi_init=0.65 out_second_sample=0 expected_zi=-0.35 metric_first_sample=0 expected_zi_init=0.65 metric_second_sample=0 expected_zi=-0.35 |
| `442-zi-np-discrete-filter` | `FAIL_SIM_CORRECTNESS` | out_first_sample=0.9 expected_zi_init=0.65 out_second_sample=0 expected_zi=-0.35 metric_first_sample=0.9 expected_zi_init=0.65 metric_second_sample=0 expected_zi=-0.35 |
| `442-zi-np-discrete-filter` | `FAIL_SIM_CORRECTNESS` | out_first_sample=0.67 expected_zi_init=0.65 out_second_sample=-0.33 expected_zi=-0.35 metric_first_sample=0.67 expected_zi_init=0.65 metric_second_sample=-0.33 expected_zi=-0.35 |
| `442-zi-np-discrete-filter` | `FAIL_SIM_CORRECTNESS` | out_first_sample=0.775 expected_zi_init=0.65 out_second_sample=-0.225 expected_zi=-0.35 metric_first_sample=0.775 expected_zi_init=0.65 metric_second_sample=-0.225 expected_zi=-0.35 |
| `442-zi-np-discrete-filter` | `FAIL_SIM_CORRECTNESS` | out_first_sample=0.325 expected_zi_init=0.65 out_second_sample=-0.175 expected_zi=-0.35 metric_first_sample=0.325 expected_zi_init=0.65 metric_second_sample=-0.175 expected_zi=-0.35 |
| `443-zi-zd-discrete-filter` | `FAIL_SIM_CORRECTNESS` | out_first_sample=0 expected_zi_init=0.55 out_second_sample=0 expected_zi=0.3 metric_first_sample=0 expected_zi_init=0.55 metric_second_sample=0 expected_zi=0.3 |
| `443-zi-zd-discrete-filter` | `FAIL_SIM_CORRECTNESS` | out_first_sample=0 expected_zi_init=0.55 out_second_sample=0 expected_zi=0.3 metric_first_sample=0 expected_zi_init=0.55 metric_second_sample=0 expected_zi=0.3 |
| `443-zi-zd-discrete-filter` | `FAIL_SIM_CORRECTNESS` | out_first_sample=0.57 expected_zi_init=0.55 out_second_sample=0.32 expected_zi=0.3 metric_first_sample=0.57 expected_zi_init=0.55 metric_second_sample=0.32 expected_zi=0.3 |
| `443-zi-zd-discrete-filter` | `FAIL_SIM_CORRECTNESS` | out_first_sample=0.675 expected_zi_init=0.55 out_second_sample=0.425 expected_zi=0.3 metric_first_sample=0.675 expected_zi_init=0.55 metric_second_sample=0.425 expected_zi=0.3 |
| `443-zi-zd-discrete-filter` | `FAIL_SIM_CORRECTNESS` | out_first_sample=0.275 expected_zi_init=0.55 out_second_sample=0.15 expected_zi=0.3 metric_first_sample=0.275 expected_zi_init=0.55 metric_second_sample=0.15 expected_zi=0.3 |
| `444-zi-zp-discrete-filter` | `FAIL_SIM_CORRECTNESS` | out_first_sample=0 expected_zi_init=0.45 metric_first_sample=0 expected_zi_init=0.45 |
| `444-zi-zp-discrete-filter` | `FAIL_SIM_CORRECTNESS` | out_first_sample=0 expected_zi_init=0.45 metric_first_sample=0 expected_zi_init=0.45 |
| `444-zi-zp-discrete-filter` | `FAIL_SIM_CORRECTNESS` | out_first_sample=0.47 expected_zi_init=0.45 out_second_sample=0.02 expected_zi=0 metric_first_sample=0.47 expected_zi_init=0.45 metric_second_sample=0.02 expected_zi=0 |
| `444-zi-zp-discrete-filter` | `FAIL_SIM_CORRECTNESS` | out_first_sample=0.575 expected_zi_init=0.45 out_second_sample=0.125 expected_zi=0 metric_first_sample=0.575 expected_zi_init=0.45 metric_second_sample=0.125 expected_zi=0 |
| `444-zi-zp-discrete-filter` | `FAIL_SIM_CORRECTNESS` | out_first_sample=0.225 expected_zi_init=0.45 metric_first_sample=0.225 expected_zi_init=0.45 |
| `445-limexp-soft-exponential` | `FAIL_SIM_CORRECTNESS` | out@103.5ns=0.0000 expected=0.7788 tol=0.1000 |
| `445-limexp-soft-exponential` | `FAIL_SIM_CORRECTNESS` | out@101.7ns=0.9000 expected=0.7788 tol=0.1000 |
| `445-limexp-soft-exponential` | `FAIL_SIM_CORRECTNESS` | metric@399.65ns=0.2500 expected=0.0000 tol=0.1000 |
| `445-limexp-soft-exponential` | `FAIL_SIM_CORRECTNESS` | out@101.7ns=0.9038 expected=0.7788 tol=0.1000 |
| `445-limexp-soft-exponential` | `FAIL_SIM_CORRECTNESS` | out@101.7ns=0.3894 expected=0.7788 tol=0.1000 |
| `446-fstrobe-file-line-writer` | `FAIL_SIM_CORRECTNESS` | out@202.05ns=0.0000 expected=0.9000 tol=0.0800 |
| `446-fstrobe-file-line-writer` | `FAIL_SIM_CORRECTNESS` | metric@200.25ns=0.9000 expected=1.0000 tol=0.0800 |
| `446-fstrobe-file-line-writer` | `FAIL_SIM_CORRECTNESS` | metric@400.95ns=0.2500 expected=0.0000 tol=0.0800 |
| `446-fstrobe-file-line-writer` | `FAIL_SIM_CORRECTNESS` | out@101.7ns=0.1250 expected=0.0000 tol=0.0800 |
| `446-fstrobe-file-line-writer` | `FAIL_SIM_CORRECTNESS` | out@200.25ns=0.4500 expected=0.9000 tol=0.0800 |
| `447-display-warning-debug-log` | `FAIL_SIM_CORRECTNESS` | out@202.05ns=0.0000 expected=0.9000 tol=0.0800 |
| `447-display-warning-debug-log` | `FAIL_SIM_CORRECTNESS` | metric@200.25ns=0.9000 expected=1.0000 tol=0.0800 |
| `447-display-warning-debug-log` | `FAIL_SIM_CORRECTNESS` | metric@400.95ns=0.2500 expected=0.0000 tol=0.0800 |
| `447-display-warning-debug-log` | `FAIL_SIM_CORRECTNESS` | out@101.7ns=0.1250 expected=0.0000 tol=0.0800 |
| `447-display-warning-debug-log` | `FAIL_SIM_CORRECTNESS` | out@200.25ns=0.4500 expected=0.9000 tol=0.0800 |
| `448-rdist-uniform-seeded-dither` | `FAIL_SIM_CORRECTNESS` | out@103.5ns=0.0000 expected_near_vin=0.6200 |
| `448-rdist-uniform-seeded-dither` | `FAIL_SIM_CORRECTNESS` | out@101.7ns=0.9000 expected_near_vin=0.6200 |
| `448-rdist-uniform-seeded-dither` | `FAIL_SIM_CORRECTNESS` | metric@399.65ns=0.2500 expected_uniform_range |
| `448-rdist-uniform-seeded-dither` | `FAIL_SIM_CORRECTNESS` | out@101.7ns=0.7478 expected_near_vin=0.6200 |
| `448-rdist-uniform-seeded-dither` | `FAIL_SIM_CORRECTNESS` | out@101.7ns=0.3114 expected_near_vin=0.6200 |
| `449-generate-genvar-replicated-stage` | `FAIL_SIM_CORRECTNESS` | y@10ns=0.0000 expected=0.8000 tol=0.0500 |
| `449-generate-genvar-replicated-stage` | `FAIL_SIM_CORRECTNESS` | y@10ns=0.9000 expected=0.8000 tol=0.0500 |
| `449-generate-genvar-replicated-stage` | `FAIL_SIM_CORRECTNESS` | y@10ns=0.8750 expected=0.8000 tol=0.0500 |
| `449-generate-genvar-replicated-stage` | `FAIL_SIM_CORRECTNESS` | y@10ns=0.9250 expected=0.8000 tol=0.0500 |
| `449-generate-genvar-replicated-stage` | `FAIL_SIM_CORRECTNESS` | y@10ns=0.4000 expected=0.8000 tol=0.0500 |
| `450-custom-nature-discipline-voltage` | `FAIL_SIM_CORRECTNESS` | y@0ns=0.0000 expected_a=0.9000 |
| `450-custom-nature-discipline-voltage` | `FAIL_SIM_CORRECTNESS` | y@1.28ns=0.9000 expected_a=0.8488 |
| `450-custom-nature-discipline-voltage` | `FAIL_SIM_CORRECTNESS` | y@11.52ns=0.2500 expected_a=0.4392 |
| `450-custom-nature-discipline-voltage` | `FAIL_SIM_CORRECTNESS` | y@0ns=1.0250 expected_a=0.9000 |
| `450-custom-nature-discipline-voltage` | `FAIL_SIM_CORRECTNESS` | y@0ns=0.4500 expected_a=0.9000 |
| `451-connectmodule-electrical-bridge` | `FAIL_SIM_CORRECTNESS` | y@0ns=0.0000 expected_a=0.6500 |
| `451-connectmodule-electrical-bridge` | `FAIL_SIM_CORRECTNESS` | y@0ns=0.9000 expected_a=0.6500 |
| `451-connectmodule-electrical-bridge` | `FAIL_SIM_CORRECTNESS` | y@8.96ns=0.2500 expected_a=0.4260 |
| `451-connectmodule-electrical-bridge` | `FAIL_SIM_CORRECTNESS` | y@0ns=0.7750 expected_a=0.6500 |
| `451-connectmodule-electrical-bridge` | `FAIL_SIM_CORRECTNESS` | y@0ns=0.3250 expected_a=0.6500 |
| `452-connectrules-electrical-map` | `FAIL_SIM_CORRECTNESS` | y@0ns=0.0000 expected_a=0.4000 |
| `452-connectrules-electrical-map` | `FAIL_SIM_CORRECTNESS` | y@0ns=0.0000 expected_a=0.4000 |
| `452-connectrules-electrical-map` | `FAIL_SIM_CORRECTNESS` | y@0ns=0.2500 expected_a=0.4000 |
| `452-connectrules-electrical-map` | `FAIL_SIM_CORRECTNESS` | y@0ns=0.5250 expected_a=0.4000 |
| `452-connectrules-electrical-map` | `FAIL_SIM_CORRECTNESS` | y@0ns=0.2000 expected_a=0.4000 |
| `453-specify-specparam-delay` | `FAIL_SIM_CORRECTNESS` | missing_certified_rising_path_delay samples=0 |
| `453-specify-specparam-delay` | `FAIL_SIM_CORRECTNESS` | missing_certified_rising_path_delay samples=0 |
| `453-specify-specparam-delay` | `FAIL_SIM_CORRECTNESS` | missing_certified_rising_path_delay samples=0 |
| `453-specify-specparam-delay` | `FAIL_SIM_CORRECTNESS` | missing_certified_rising_path_delay samples=0 |
| `453-specify-specparam-delay` | `FAIL_SIM_CORRECTNESS` | missing_certified_rising_path_delay samples=0 |
| `454-multidimensional-array-state` | `FAIL_SIM_CORRECTNESS` | metric@105.05ns=0.0000 expected=1.0000 tol=0.0800 |
| `454-multidimensional-array-state` | `FAIL_SIM_CORRECTNESS` | metric@102.85ns=0.9000 expected=1.0000 tol=0.0800 |
| `454-multidimensional-array-state` | `FAIL_SIM_CORRECTNESS` | metric@400ns=0.2500 expected=0.0000 tol=0.0800 |
| `454-multidimensional-array-state` | `FAIL_SIM_CORRECTNESS` | out@99.7ns=0.0938 expected=0.0000 tol=0.0800 |
| `454-multidimensional-array-state` | `FAIL_SIM_CORRECTNESS` | metric@102.85ns=0.5000 expected=1.0000 tol=0.0800 |
| `455-packed-logic-bus-slice` | `FAIL_SIM_CORRECTNESS` | y3@50ns=0.0000 expected_a7=1.0000 y1@50ns=0.0000 expected_a1=1.0000 y0@50ns=0.0000 expected_a0=1.0000 y3@90ns=0.0000 expected_a7=1.0000 |
| `455-packed-logic-bus-slice` | `FAIL_SIM_CORRECTNESS` | y3@50ns=0.0000 expected_a7=1.0000 y1@50ns=0.0000 expected_a1=1.0000 y3@90ns=0.0000 expected_a7=1.0000 y2@90ns=0.0000 expected_a6=1.0000 |
| `455-packed-logic-bus-slice` | `FAIL_SIM_CORRECTNESS` | y3@50ns=0.0000 expected_a7=1.0000 y2@90ns=0.0000 expected_a6=1.0000 y3@100ns=1.0000 expected_a7=0.0000 y2@100ns=0.0000 expected_a6=1.0000 |
| `455-packed-logic-bus-slice` | `FAIL_SIM_CORRECTNESS` | y1@50ns=0.0000 expected_a1=1.0000 y1@90ns=0.0000 expected_a1=1.0000 y1@100ns=0.0000 expected_a1=1.0000 y1@150ns=0.0000 expected_a1=1.0000 |
| `455-packed-logic-bus-slice` | `FAIL_SIM_CORRECTNESS` | y3@50ns=0.0000 expected_a7=1.0000 y2@50ns=1.0000 expected_a6=0.0000 y0@50ns=0.0000 expected_a0=1.0000 y2@90ns=0.0000 expected_a6=1.0000 |
| `456-event-or-cross-timer` | `FAIL_SIM_CORRECTNESS` | out@1.342ns=0.0000 expected=0.3500 |
| `456-event-or-cross-timer` | `FAIL_SIM_CORRECTNESS` | out@1.342ns=0.0000 expected=0.3500 |
| `456-event-or-cross-timer` | `FAIL_SIM_CORRECTNESS` | metric@1.342ns=2.0000 expected=1.0000 |
| `456-event-or-cross-timer` | `FAIL_SIM_CORRECTNESS` | out@1.342ns=0.4750 expected=0.3500 |
| `456-event-or-cross-timer` | `FAIL_SIM_CORRECTNESS` | out@1.342ns=0.1750 expected=0.3500 |
| `457-nested-function-pipeline` | `FAIL_SIM_CORRECTNESS` | out@0ns=0.0000 expected=1.5625 |
| `457-nested-function-pipeline` | `FAIL_SIM_CORRECTNESS` | out@0ns=0.9000 expected=1.5625 |
| `457-nested-function-pipeline` | `FAIL_SIM_CORRECTNESS` | out@0ns=1.8125 expected=1.5625 |
| `457-nested-function-pipeline` | `FAIL_SIM_CORRECTNESS` | out@0ns=1.6875 expected=1.5625 |
| `457-nested-function-pipeline` | `FAIL_SIM_CORRECTNESS` | out@0ns=0.7812 expected=1.5625 |
| `458-recursive-function-candidate` | `FAIL_SIM_CORRECTNESS` | hidden_depth4: out@10ns=0.0000 expected=24.0000 |
| `458-recursive-function-candidate` | `FAIL_SIM_CORRECTNESS` | hidden_depth4: out@10ns=0.9000 expected=24.0000 |
| `458-recursive-function-candidate` | `FAIL_SIM_CORRECTNESS` | hidden_depth4: out@10ns=24.2500 expected=24.0000 |
| `458-recursive-function-candidate` | `FAIL_SIM_CORRECTNESS` | hidden_depth4: out@10ns=6.0000 expected=24.0000 |
| `458-recursive-function-candidate` | `FAIL_SIM_CORRECTNESS` | hidden_depth4: out@10ns=12.0000 expected=24.0000 |
| `459-do-while-loop-accumulator` | `FAIL_SIM_CORRECTNESS` | out@32ns=0.0000 expected=0.9000 tol=0.0800 |
| `459-do-while-loop-accumulator` | `FAIL_SIM_CORRECTNESS` | out@12ns=0.9000 expected=0.0000 tol=0.0800 |
| `459-do-while-loop-accumulator` | `FAIL_SIM_CORRECTNESS` | out@12ns=0.9000 expected=0.0000 tol=0.0800 |
| `459-do-while-loop-accumulator` | `FAIL_SIM_CORRECTNESS` | metric@12ns=3.1250 expected=3.0000 tol=0.0800 |
| `459-do-while-loop-accumulator` | `FAIL_SIM_CORRECTNESS` | out@32ns=0.4500 expected=0.9000 tol=0.0800 |
| `460-analog-initial-block-state` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.0000 expected=0.2500 tol=0.0800 |
| `460-analog-initial-block-state` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.5000 expected=0.2500 tol=0.0800 |
| `460-analog-initial-block-state` | `FAIL_SIM_CORRECTNESS` | out@50ns=0.0500 expected=0.4500 tol=0.0800 |
| `460-analog-initial-block-state` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.3750 expected=0.2500 tol=0.0800 |
| `460-analog-initial-block-state` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.1250 expected=0.2500 tol=0.0800 |
| `461-vt-thermal-voltage-source` | `FAIL_SIM_CORRECTNESS` | out@12ns=0.00000 expected=0.02585 tol=0.00400 |
| `461-vt-thermal-voltage-source` | `FAIL_SIM_CORRECTNESS` | out@12ns=0.00000 expected=0.02585 tol=0.00400 |
| `461-vt-thermal-voltage-source` | `FAIL_SIM_CORRECTNESS` | out@32ns=0.03586 expected=0.02585 tol=0.00400 |
| `461-vt-thermal-voltage-source` | `FAIL_SIM_CORRECTNESS` | out@12ns=0.15086 expected=0.02585 tol=0.00400 |
| `461-vt-thermal-voltage-source` | `FAIL_SIM_CORRECTNESS` | out@12ns=0.01293 expected=0.02585 tol=0.00400 |
| `462-vt-temperature-argument` | `FAIL_SIM_CORRECTNESS` | out@12ns=0.00000 expected=0.05170 tol=0.00600 |
| `462-vt-temperature-argument` | `FAIL_SIM_CORRECTNESS` | out@12ns=0.00000 expected=0.05170 tol=0.00600 |
| `462-vt-temperature-argument` | `FAIL_SIM_CORRECTNESS` | out@32ns=0.06170 expected=0.05170 tol=0.00600 |
| `462-vt-temperature-argument` | `FAIL_SIM_CORRECTNESS` | out@12ns=0.17670 expected=0.05170 tol=0.00600 |
| `462-vt-temperature-argument` | `FAIL_SIM_CORRECTNESS` | out@12ns=0.02585 expected=0.05170 tol=0.00600 |
| `463-discontinuity-event-announcement` | `FAIL_SIM_CORRECTNESS` | out@12ns=0.0000 expected=0.9000 tol=0.0800 |
| `463-discontinuity-event-announcement` | `FAIL_SIM_CORRECTNESS` | out@12ns=0.0000 expected=0.9000 tol=0.0800 |
| `463-discontinuity-event-announcement` | `FAIL_SIM_CORRECTNESS` | metric@12ns=1.0000 expected=0.0000 tol=0.0800 |
| `463-discontinuity-event-announcement` | `FAIL_SIM_CORRECTNESS` | out@12ns=1.0250 expected=0.9000 tol=0.0800 |
| `463-discontinuity-event-announcement` | `FAIL_SIM_CORRECTNESS` | out@12ns=0.4500 expected=0.9000 tol=0.0800 |
| `464-param-given-gain-select` | `FAIL_SIM_CORRECTNESS` | out_def@12ns=0.0000 expected=0.6000 out_ovr@12ns=0.0000 expected=0.3000 out_def@52ns=0.0000 expected=0.3000 out_ovr@52ns=0.0000 expected=0.1500 |
| `464-param-given-gain-select` | `FAIL_SIM_CORRECTNESS` | out_def@12ns=0.9000 expected=0.6000 out_ovr@12ns=0.0000 expected=0.3000 out_def@52ns=0.0000 expected=0.3000 out_ovr@52ns=0.0000 expected=0.1500 |
| `464-param-given-gain-select` | `FAIL_SIM_CORRECTNESS` | metric_def@12ns=1.0000 expected=0.0000 metric_ovr@12ns=0.0000 expected=1.0000 metric_def@52ns=1.0000 expected=0.0000 metric_ovr@52ns=0.0000 expected=1.0000 |
| `464-param-given-gain-select` | `FAIL_SIM_CORRECTNESS` | out_def@12ns=0.7250 expected=0.6000 out_ovr@12ns=0.4250 expected=0.3000 out_def@52ns=0.4250 expected=0.3000 out_ovr@52ns=0.2750 expected=0.1500 |
| `464-param-given-gain-select` | `FAIL_SIM_CORRECTNESS` | out_def@12ns=0.3000 expected=0.6000 out_ovr@12ns=0.1500 expected=0.3000 out_def@52ns=0.1500 expected=0.3000 out_ovr@52ns=0.0750 expected=0.1500 |
| `465-port-connected-output-enable` | `FAIL_SIM_CORRECTNESS` | out@12ns=0.0000 expected=0.6000 tol=0.0800 |
| `465-port-connected-output-enable` | `FAIL_SIM_CORRECTNESS` | out@12ns=0.9000 expected=0.6000 tol=0.0800 |
| `465-port-connected-output-enable` | `FAIL_SIM_CORRECTNESS` | metric@12ns=0.0000 expected=1.0000 tol=0.0800 |
| `465-port-connected-output-enable` | `FAIL_SIM_CORRECTNESS` | out@12ns=0.7250 expected=0.6000 tol=0.0800 |
| `465-port-connected-output-enable` | `FAIL_SIM_CORRECTNESS` | out@12ns=0.3000 expected=0.6000 tol=0.0800 |
| `466-temperature-environment-metric` | `FAIL_SIM_CORRECTNESS` | out@12ns=0.0000 expected=1.0005 tol=0.0400 |
| `466-temperature-environment-metric` | `FAIL_SIM_CORRECTNESS` | out@12ns=0.9000 expected=1.0005 tol=0.0400 |
| `466-temperature-environment-metric` | `FAIL_SIM_CORRECTNESS` | metric@12ns=310.1500 expected=300.1500 tol=2.0000 |
| `466-temperature-environment-metric` | `FAIL_SIM_CORRECTNESS` | out@12ns=1.1255 expected=1.0005 tol=0.0400 |
| `466-temperature-environment-metric` | `FAIL_SIM_CORRECTNESS` | out@12ns=0.5002 expected=1.0005 tol=0.0400 |
| `467-simparam-query-tnom` | `FAIL_SIM_CORRECTNESS` | out@12ns=0.0000 expected=0.0900 tol=0.0250 |
| `467-simparam-query-tnom` | `FAIL_SIM_CORRECTNESS` | out@12ns=0.0000 expected=0.0900 tol=0.0250 |
| `467-simparam-query-tnom` | `FAIL_SIM_CORRECTNESS` | metric@12ns=0.1400 expected=0.0900 tol=0.0250 |
| `467-simparam-query-tnom` | `FAIL_SIM_CORRECTNESS` | out@12ns=0.2150 expected=0.0900 tol=0.0250 |
| `467-simparam-query-tnom` | `FAIL_SIM_CORRECTNESS` | out@12ns=0.0450 expected=0.0900 tol=0.0250 |
| `468-branch-declaration-voltage-probe` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.0000 expected=0.1000 tol=0.0350 |
| `468-branch-declaration-voltage-probe` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.0000 expected=0.1000 tol=0.0350 |
| `468-branch-declaration-voltage-probe` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.1500 expected=0.1000 tol=0.0350 |
| `468-branch-declaration-voltage-probe` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.2250 expected=0.1000 tol=0.0350 |
| `468-branch-declaration-voltage-probe` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.0500 expected=0.1000 tol=0.0350 |
| `469-current-contribution-conductance` | `FAIL_SIM_CORRECTNESS` | imon@50ns=5.000e-04 expected=4.000e-04 tol=2.4e-05 imon@90ns=2.000e-04 expected=1.000e-04 tol=1.0e-05 imon@130ns=8.000e-04 expected=5.000e-04 tol=3.0e-05 imon@150ns=5.000e-05 expected=-2.500e-04 tol=1.5e-05 |
| `469-current-contribution-conductance` | `FAIL_SIM_CORRECTNESS` | imon@150ns=0.000e+00 expected=-2.500e-04 tol=1.5e-05 imon@170ns=0.000e+00 expected=-2.500e-04 tol=1.5e-05 |
| `469-current-contribution-conductance` | `FAIL_SIM_CORRECTNESS` | imon@10ns=1.000e-04 expected=0.000e+00 tol=1.0e-05 imon@50ns=5.000e-04 expected=4.000e-04 tol=2.4e-05 imon@90ns=2.000e-04 expected=1.000e-04 tol=1.0e-05 imon@130ns=6.000e-04 expected=5.000e-04 tol=3.0e-05 |
| `469-current-contribution-conductance` | `FAIL_SIM_CORRECTNESS` | imon@50ns=-4.000e-04 expected=4.000e-04 tol=2.4e-05 imon@90ns=-1.000e-04 expected=1.000e-04 tol=1.0e-05 imon@130ns=-5.000e-04 expected=5.000e-04 tol=3.0e-05 imon@150ns=2.500e-04 expected=-2.500e-04 tol=1.5e-05 |
| `469-current-contribution-conductance` | `FAIL_SIM_CORRECTNESS` | imon@50ns=2.000e-04 expected=4.000e-04 tol=2.4e-05 imon@90ns=5.000e-05 expected=1.000e-04 tol=1.0e-05 imon@130ns=2.500e-04 expected=5.000e-04 tol=3.0e-05 imon@150ns=-1.250e-04 expected=-2.500e-04 tol=1.5e-05 |
| `470-branch-current-probe-contribution` | `FAIL_SIM_CORRECTNESS` | out@50ns=0.0000 expected_branch_current=0.5000 out@90ns=0.0000 expected_branch_current=0.2000 |
| `470-branch-current-probe-contribution` | `FAIL_SIM_CORRECTNESS` | out@50ns=0.0000 expected_branch_current=0.5000 out@90ns=0.0000 expected_branch_current=0.2000 |
| `470-branch-current-probe-contribution` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.1250 expected_branch_current=0.0000 out@50ns=0.6250 expected_branch_current=0.5000 out@90ns=0.3250 expected_branch_current=0.2000 |
| `470-branch-current-probe-contribution` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.1250 expected_branch_current=0.0000 out@50ns=0.6250 expected_branch_current=0.5000 out@90ns=0.3250 expected_branch_current=0.2000 |
| `470-branch-current-probe-contribution` | `FAIL_SIM_CORRECTNESS` | out@50ns=0.2500 expected_branch_current=0.5000 out@90ns=0.1000 expected_branch_current=0.2000 |
| `471-indirect-branch-null-balance` | `FAIL_SIM_CORRECTNESS` | out_not_tracking_in@50ns out=0.0000 inp=0.5000 err=0.5000 |
| `471-indirect-branch-null-balance` | `FAIL_SIM_CORRECTNESS` | out_not_tracking_in@10ns out=0.1000 inp=0.0000 err=0.1000 |
| `471-indirect-branch-null-balance` | `FAIL_SIM_CORRECTNESS` | out_not_tracking_in@50ns out=-0.5000 inp=0.5000 err=1.0000 |
| `471-indirect-branch-null-balance` | `FAIL_SIM_CORRECTNESS` | out_not_tracking_in@10ns out=-0.1000 inp=0.0000 err=0.1000 |
| `471-indirect-branch-null-balance` | `FAIL_SIM_CORRECTNESS` | out_not_tracking_in@50ns out=0.2500 inp=0.5000 err=0.2500 |
| `472-indirect-branch-ddt-balance` | `FAIL_SIM_CORRECTNESS` | out_not_integral@50ns out=0.0000e+00 expected=1.4750e-08 err=1.4750e-08 |
| `472-indirect-branch-ddt-balance` | `FAIL_SIM_CORRECTNESS` | out_not_integral@50ns out=1.9750e-08 expected=1.4750e-08 err=5.0000e-09 |
| `472-indirect-branch-ddt-balance` | `FAIL_SIM_CORRECTNESS` | tran.csv missing |
| `472-indirect-branch-ddt-balance` | `FAIL_SIM_CORRECTNESS` | out_not_integral@50ns out=7.3750e-09 expected=1.4750e-08 err=7.3750e-09 |
| `472-indirect-branch-ddt-balance` | `FAIL_SIM_CORRECTNESS` | out_not_integral@50ns out=9.7500e-09 expected=1.4750e-08 err=5.0000e-09 |
| `473-attribute-potential-abstol-probe` | `FAIL_SIM_CORRECTNESS` | out@50ns=0.1000 expected=0.4000 tol=0.0350 |
| `473-attribute-potential-abstol-probe` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.0100 expected=0.1000 tol=0.0350 |
| `473-attribute-potential-abstol-probe` | `FAIL_SIM_CORRECTNESS` | out@10ns=-0.1000 expected=0.1000 tol=0.0350 |
| `473-attribute-potential-abstol-probe` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.1500 expected=0.1000 tol=0.0350 |
| `473-attribute-potential-abstol-probe` | `FAIL_SIM_CORRECTNESS` | out@50ns=0.3200 expected=0.4000 tol=0.0350 |
| `474-generic-potential-access-function` | `FAIL_SIM_CORRECTNESS` | out@50ns=0.0000 expected=0.3000 tol=0.0350 |
| `474-generic-potential-access-function` | `FAIL_SIM_CORRECTNESS` | out@50ns=0.0000 expected=0.3000 tol=0.0350 |
| `474-generic-potential-access-function` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.1000 expected=0.0000 tol=0.0350 |
| `474-generic-potential-access-function` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.0500 expected=0.0000 tol=0.0350 |
| `474-generic-potential-access-function` | `FAIL_SIM_CORRECTNESS` | out@50ns=0.2400 expected=0.3000 tol=0.0350 |
| `475-generic-potential-contribution` | `FAIL_SIM_CORRECTNESS` | out@50ns=0.0000 expected=0.2500 tol=0.0350 |
| `475-generic-potential-contribution` | `FAIL_SIM_CORRECTNESS` | out@50ns=0.0000 expected=0.2500 tol=0.0350 |
| `475-generic-potential-contribution` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.1000 expected=0.0000 tol=0.0350 |
| `475-generic-potential-contribution` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.0500 expected=0.0000 tol=0.0350 |
| `475-generic-potential-contribution` | `FAIL_SIM_CORRECTNESS` | out@50ns=0.2000 expected=0.2500 tol=0.0350 |
| `476-oomr-string-voltage-probe` | `FAIL_SIM_CORRECTNESS` | out@50ns=0.0000 expected=0.2000 tol=0.0350 |
| `476-oomr-string-voltage-probe` | `FAIL_SIM_CORRECTNESS` | out@50ns=0.0000 expected=0.2000 tol=0.0350 |
| `476-oomr-string-voltage-probe` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.1000 expected=0.0000 tol=0.0350 |
| `476-oomr-string-voltage-probe` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.0500 expected=0.0000 tol=0.0350 |
| `476-oomr-string-voltage-probe` | `FAIL_SIM_CORRECTNESS` | out@50ns=0.1600 expected=0.2000 tol=0.0350 |
| `477-analog-node-alias-initial` | `FAIL_SIM_CORRECTNESS` | out@50ns=0.0000 expected=0.2000 tol=0.0350 |
| `477-analog-node-alias-initial` | `FAIL_SIM_CORRECTNESS` | out@50ns=0.0000 expected=0.2000 tol=0.0350 |
| `477-analog-node-alias-initial` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.1000 expected=0.0000 tol=0.0350 |
| `477-analog-node-alias-initial` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.0500 expected=0.0000 tol=0.0350 |
| `477-analog-node-alias-initial` | `FAIL_SIM_CORRECTNESS` | out@50ns=0.1600 expected=0.2000 tol=0.0350 |
| `478-inherited-port-attribute-supply` | `FAIL_SIM_CORRECTNESS` | out@50ns=0.0000 expected=0.2200 tol=0.0350 |
| `478-inherited-port-attribute-supply` | `FAIL_SIM_CORRECTNESS` | out@50ns=0.0000 expected=0.2200 tol=0.0350 |
| `478-inherited-port-attribute-supply` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.1000 expected=0.0000 tol=0.0350 |
| `478-inherited-port-attribute-supply` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.0500 expected=0.0000 tol=0.0350 |
| `478-inherited-port-attribute-supply` | `FAIL_SIM_CORRECTNESS` | out@50ns=0.1760 expected=0.2200 tol=0.0350 |
| `479-inherited-mfactor-parameter` | `FAIL_SIM_CORRECTNESS` | out@50ns=0.0000 expected=0.3000 tol=0.0350 |
| `479-inherited-mfactor-parameter` | `FAIL_SIM_CORRECTNESS` | out@50ns=0.0000 expected=0.3000 tol=0.0350 |
| `479-inherited-mfactor-parameter` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.1000 expected=0.0000 tol=0.0350 |
| `479-inherited-mfactor-parameter` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.0500 expected=0.0000 tol=0.0350 |
| `479-inherited-mfactor-parameter` | `FAIL_SIM_CORRECTNESS` | out@50ns=0.2400 expected=0.3000 tol=0.0350 |
| `480-mfactor-system-function-gain` | `FAIL_SIM_CORRECTNESS` | out@50ns=0.0000 expected=0.3000 tol=0.0350 |
| `480-mfactor-system-function-gain` | `FAIL_SIM_CORRECTNESS` | out@50ns=0.0000 expected=0.3000 tol=0.0350 |
| `480-mfactor-system-function-gain` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.1000 expected=0.0000 tol=0.0350 |
| `480-mfactor-system-function-gain` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.0500 expected=0.0000 tol=0.0350 |
| `480-mfactor-system-function-gain` | `FAIL_SIM_CORRECTNESS` | out@50ns=0.2400 expected=0.3000 tol=0.0350 |
| `481-analog-primitive-resistor-instance` | `FAIL_SIM_CORRECTNESS` | primitive_trace_present rows=1003 p_range=0.6 |
| `481-analog-primitive-resistor-instance` | `FAIL_SIM_CORRECTNESS` | primitive_trace_present rows=1003 p_range=0.6 |
| `481-analog-primitive-resistor-instance` | `FAIL_SIM_CORRECTNESS` | primitive_trace_present rows=1003 p_range=0.6 |
| `481-analog-primitive-resistor-instance` | `FAIL_SIM_CORRECTNESS` | primitive_trace_present rows=1003 p_range=0.6 |
| `481-analog-primitive-resistor-instance` | `FAIL_SIM_CORRECTNESS` | primitive_trace_present rows=1003 p_range=0.6 |
| `482-analog-primitive-isource-instance` | `FAIL_SIM_CORRECTNESS` | primitive_trace_present rows=1001 p_range=0 |
| `482-analog-primitive-isource-instance` | `FAIL_SIM_CORRECTNESS` | primitive_trace_present rows=1001 p_range=0 |
| `482-analog-primitive-isource-instance` | `FAIL_SIM_CORRECTNESS` | primitive_trace_present rows=1001 p_range=0 |
| `482-analog-primitive-isource-instance` | `FAIL_SIM_CORRECTNESS` | primitive_trace_present rows=1001 p_range=0 |
| `482-analog-primitive-isource-instance` | `FAIL_SIM_CORRECTNESS` | primitive_trace_present rows=1001 p_range=0 |
| `483-cds-violation-threshold-assert` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.0000 expected=0.2000 tol=0.0350 |
| `483-cds-violation-threshold-assert` | `FAIL_SIM_CORRECTNESS` | out@50ns=1.0000 expected=0.7500 tol=0.0350 |
| `483-cds-violation-threshold-assert` | `FAIL_SIM_CORRECTNESS` | out@90ns=0.9000 expected=1.0000 tol=0.0350 |
| `483-cds-violation-threshold-assert` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.2500 expected=0.2000 tol=0.0350 |
| `483-cds-violation-threshold-assert` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.1600 expected=0.2000 tol=0.0350 |
| `484-rtoi-conversion-quantizer` | `FAIL_SIM_CORRECTNESS` | out@50ns=0.0000 expected=0.2857 tol=0.0350 |
| `484-rtoi-conversion-quantizer` | `FAIL_SIM_CORRECTNESS` | out@50ns=0.1429 expected=0.2857 tol=0.0350 |
| `484-rtoi-conversion-quantizer` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.1429 expected=0.0000 tol=0.0350 |
| `484-rtoi-conversion-quantizer` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.0500 expected=0.0000 tol=0.0350 |
| `484-rtoi-conversion-quantizer` | `FAIL_SIM_CORRECTNESS` | out@50ns=0.2286 expected=0.2857 tol=0.0350 |
| `485-mc-trial-number-metric` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.0000 expected=0.2500 tol=0.0250 |
| `485-mc-trial-number-metric` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.3500 expected=0.2500 tol=0.0250 |
| `485-mc-trial-number-metric` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.3500 expected=0.2500 tol=0.0250 |
| `485-mc-trial-number-metric` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.3000 expected=0.2500 tol=0.0250 |
| `485-mc-trial-number-metric` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.2000 expected=0.2500 tol=0.0250 |
| `486-rf-source-info-registration` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.0000 expected=0.2000 tol=0.0350 |
| `486-rf-source-info-registration` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.1500 expected=0.2000 tol=0.0350 |
| `486-rf-source-info-registration` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.3000 expected=0.2000 tol=0.0350 |
| `486-rf-source-info-registration` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.2500 expected=0.2000 tol=0.0350 |
| `486-rf-source-info-registration` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.1600 expected=0.2000 tol=0.0350 |
| `487-table-model-2d-array-surface` | `FAIL_SIM_CORRECTNESS` | out@50ns=0.0000 expected=1.0000 tol=0.0500 |
| `487-table-model-2d-array-surface` | `FAIL_SIM_CORRECTNESS` | out@130ns=1.0000 expected=2.0000 tol=0.0500 |
| `487-table-model-2d-array-surface` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.5000 expected=0.0000 tol=0.0500 |
| `487-table-model-2d-array-surface` | `FAIL_SIM_CORRECTNESS` | out@50ns=1.0500 expected=1.0000 tol=0.0500 |
| `487-table-model-2d-array-surface` | `FAIL_SIM_CORRECTNESS` | out@50ns=0.8000 expected=1.0000 tol=0.0500 |
| `488-table-model-string-param-source` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.0000 expected=0.1000 tol=0.0400 |
| `488-table-model-string-param-source` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.0000 expected=0.1000 tol=0.0400 |
| `488-table-model-string-param-source` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.6000 expected=0.1000 tol=0.0400 |
| `488-table-model-string-param-source` | `FAIL_SIM_CORRECTNESS` | out@10ns=0.1500 expected=0.1000 tol=0.0400 |
| `488-table-model-string-param-source` | `FAIL_SIM_CORRECTNESS` | out@50ns=0.4800 expected=0.6000 tol=0.0400 |
| `489-event-nested-or-expression` | `FAIL_SIM_CORRECTNESS` | out@15ns=0.0000 expected=0.1000 tol=0.0350 |
| `489-event-nested-or-expression` | `FAIL_SIM_CORRECTNESS` | out@40ns=0.2000 expected=0.3000 tol=0.0350 |
| `489-event-nested-or-expression` | `FAIL_SIM_CORRECTNESS` | out@15ns=0.2000 expected=0.1000 tol=0.0350 |
| `489-event-nested-or-expression` | `FAIL_SIM_CORRECTNESS` | out@15ns=0.1500 expected=0.1000 tol=0.0350 |
| `489-event-nested-or-expression` | `FAIL_SIM_CORRECTNESS` | out@40ns=0.2400 expected=0.3000 tol=0.0350 |
| `490-event-task-function-state-update` | `FAIL_SIM_CORRECTNESS` | out@20ns=0.0000 expected=0.1500 tol=0.0350 |
| `490-event-task-function-state-update` | `FAIL_SIM_CORRECTNESS` | out@20ns=0.0000 expected=0.1500 tol=0.0350 |
| `490-event-task-function-state-update` | `FAIL_SIM_CORRECTNESS` | out@20ns=0.2000 expected=0.1500 tol=0.0350 |
| `490-event-task-function-state-update` | `FAIL_SIM_CORRECTNESS` | out@20ns=0.2000 expected=0.1500 tol=0.0350 |
| `490-event-task-function-state-update` | `FAIL_SIM_CORRECTNESS` | out@40ns=0.3200 expected=0.4000 tol=0.0350 |
| `491-kcl-capacitor-ddt-current` | `FAIL_SIM_CORRECTNESS` | imon@62ns=0.000e+00 expected=-7.500e-05 tol=7.5e-06 imon@142ns=0.000e+00 expected=-1.250e-04 tol=1.2e-05 imon_range_too_small=1.527e-04 |
| `491-kcl-capacitor-ddt-current` | `FAIL_SIM_CORRECTNESS` | imon@22ns=2.000e-04 expected=1.000e-04 tol=1.0e-05 imon@62ns=-1.500e-04 expected=-7.500e-05 tol=7.5e-06 imon@122ns=3.000e-04 expected=1.500e-04 tol=1.5e-05 imon@142ns=-2.500e-04 expected=-1.250e-04 tol=1.2e-05 |
| `491-kcl-capacitor-ddt-current` | `FAIL_SIM_CORRECTNESS` | imon@22ns=-1.000e-04 expected=1.000e-04 tol=1.0e-05 imon@62ns=7.500e-05 expected=-7.500e-05 tol=7.5e-06 imon@122ns=-1.500e-04 expected=1.500e-04 tol=1.5e-05 imon@142ns=1.250e-04 expected=-1.250e-04 tol=1.2e-05 |
| `491-kcl-capacitor-ddt-current` | `FAIL_SIM_CORRECTNESS` | imon@62ns=-5.000e-05 expected=-7.500e-05 tol=7.5e-06 imon@122ns=1.250e-04 expected=1.500e-04 tol=1.5e-05 imon@142ns=-5.000e-05 expected=-1.250e-04 tol=1.2e-05 imon_range_too_small=1.750e-04 |
| `491-kcl-capacitor-ddt-current` | `FAIL_SIM_CORRECTNESS` | imon@22ns=8.000e-05 expected=1.000e-04 tol=1.0e-05 imon@62ns=-6.000e-05 expected=-7.500e-05 tol=7.5e-06 imon@122ns=1.200e-04 expected=1.500e-04 tol=1.5e-05 imon@142ns=-1.000e-04 expected=-1.250e-04 tol=1.2e-05 |
| `492-kcl-inductor-idt-voltage` | `FAIL_SIM_CORRECTNESS` | p@21ns=0.000e+00 expected=5.000e-25 tol=2.500e-25 p@40ns=0.000e+00 expected=1.950e-23 tol=5.850e-25 p@80ns=0.000e+00 expected=5.950e-23 tol=1.785e-24 p@100ns=0.000e+00 expected=4.050e-23 tol=1.215e-24 |
| `492-kcl-inductor-idt-voltage` | `FAIL_SIM_CORRECTNESS` | p@21ns=1.000e-24 expected=5.000e-25 tol=2.500e-25 p@40ns=3.900e-23 expected=1.950e-23 tol=5.850e-25 p@80ns=1.190e-22 expected=5.950e-23 tol=1.785e-24 p@100ns=8.100e-23 expected=4.050e-23 tol=1.215e-24 |
| `492-kcl-inductor-idt-voltage` | `FAIL_SIM_CORRECTNESS` | p@21ns=-5.000e-25 expected=5.000e-25 tol=2.500e-25 p@40ns=-1.950e-23 expected=1.950e-23 tol=5.850e-25 p@80ns=-5.950e-23 expected=5.950e-23 tol=1.785e-24 p@100ns=-4.050e-23 expected=4.050e-23 tol=1.215e-24 |
| `492-kcl-inductor-idt-voltage` | `FAIL_SIM_CORRECTNESS` | p@21ns=1.000e-10 expected=5.000e-25 tol=2.500e-25 p@40ns=1.000e-10 expected=1.950e-23 tol=5.850e-25 p@80ns=1.000e-10 expected=5.950e-23 tol=1.785e-24 p@100ns=1.000e-10 expected=4.050e-23 tol=1.215e-24 |
| `492-kcl-inductor-idt-voltage` | `FAIL_SIM_CORRECTNESS` | p@40ns=1.560e-23 expected=1.950e-23 tol=5.850e-25 p@80ns=4.760e-23 expected=5.950e-23 tol=1.785e-24 p@100ns=3.240e-23 expected=4.050e-23 tol=1.215e-24 p@120ns=1.640e-23 expected=2.050e-23 tol=6.150e-25 |
| `493-continuous-laplace-nd-filter` | `FAIL_SIM_CORRECTNESS` | out@40ns=0 expected=0.01931 out@75ns=0 expected=0.05304 out@100ns=0 expected=0.05711 out@150ns=0 expected=0.05433 out_range_too_small=0 |
| `493-continuous-laplace-nd-filter` | `FAIL_SIM_CORRECTNESS` | out@40ns=-0.01932 expected=0.01931 out@75ns=-0.05305 expected=0.05304 out@100ns=-0.05711 expected=0.05711 out@150ns=-0.05432 expected=0.05433 |
| `493-continuous-laplace-nd-filter` | `FAIL_SIM_CORRECTNESS` | out@40ns=0.1193 expected=0.01931 out@75ns=0.1531 expected=0.05304 out@100ns=0.1571 expected=0.05711 out@150ns=0.1543 expected=0.05433 |
| `493-continuous-laplace-nd-filter` | `FAIL_SIM_CORRECTNESS` | out@40ns=0.06932 expected=0.01931 out@75ns=0.1031 expected=0.05304 out@100ns=0.1071 expected=0.05711 out@150ns=0.1043 expected=0.05433 |
| `493-continuous-laplace-nd-filter` | `FAIL_SIM_CORRECTNESS` | out@40ns=0.01546 expected=0.01931 out@75ns=0.04244 expected=0.05304 out@100ns=0.04569 expected=0.05711 out@150ns=0.04346 expected=0.05433 |
| `494-continuous-zi-nd-filter` | `FAIL_SIM_CORRECTNESS` | out@30ns=0 expected=0.08 out@40ns=0 expected=0.6 out@50ns=0 expected=1.15 out@70ns=0 expected=1.322 out@100ns=0 expected=0.483 out@120ns=0 expected=0.03019 |
| `494-continuous-zi-nd-filter` | `FAIL_SIM_CORRECTNESS` | out@30ns=-0.08 expected=0.08 out@40ns=-0.6 expected=0.6 out@50ns=-1.15 expected=1.15 out@70ns=-1.322 expected=1.322 out@100ns=-0.483 expected=0.483 out@120ns=-0.03019 expected=0.03019 |
| `494-continuous-zi-nd-filter` | `FAIL_SIM_CORRECTNESS` | out@30ns=0.2081 expected=0.08 out@40ns=0.732 expected=0.6 out@50ns=1.283 expected=1.15 out@70ns=1.455 expected=1.322 out@100ns=0.6163 expected=0.483 out@120ns=0.1635 expected=0.03019 |
| `494-continuous-zi-nd-filter` | `FAIL_SIM_CORRECTNESS` | out@30ns=0.13 expected=0.08 out@40ns=0.65 expected=0.6 out@100ns=0.533 expected=0.483 out@120ns=0.08019 expected=0.03019 out@140ns=0.05189 expected=0.001887 decay_tail_too_large=0.05189 |
| `494-continuous-zi-nd-filter` | `FAIL_SIM_CORRECTNESS` | out@40ns=0.48 expected=0.6 out@50ns=0.92 expected=1.15 out@70ns=1.058 expected=1.322 out@100ns=0.3864 expected=0.483 iir_peak_wrong=1.064 |
| `495-slew-rate-dac4` | `FAIL_SIM_CORRECTNESS` | max_slew_error=0.7333 |
| `495-slew-rate-dac4` | `FAIL_SIM_CORRECTNESS` | max_slew_error=0.7293 |
| `495-slew-rate-dac4` | `FAIL_SIM_CORRECTNESS` | max_endpoint_error=0.0250 |
| `495-slew-rate-dac4` | `FAIL_SIM_CORRECTNESS` | max_slew_error=0.1333 |
| `495-slew-rate-dac4` | `FAIL_SIM_CORRECTNESS` | max_slew_error=0.3658 |
| `496-first-order-sigma-delta-modulator` | `FAIL_SIM_CORRECTNESS` | edge@0.310ns bit=0 expected=1 vin=0.200 edge@3.510ns bit=0 expected=1 vin=0.200 edge@7.510ns bit=0 expected=1 vin=0.200 edge@11.510ns bit=0 expected=1 vin=0.200 edge@15.510ns bit=0 expected=1 vin=0.200 edge@18.710ns bit=0 expected=1 vin=0.600 |
| `496-first-order-sigma-delta-modulator` | `FAIL_SIM_CORRECTNESS` | edge@1.110ns bit=1 expected=0 vin=0.200 edge@1.910ns bit=1 expected=0 vin=0.200 edge@2.710ns bit=1 expected=0 vin=0.200 edge@4.310ns bit=1 expected=0 vin=0.200 edge@5.110ns bit=1 expected=0 vin=0.200 edge@5.910ns bit=1 expected=0 vin=0.200 |
| `496-first-order-sigma-delta-modulator` | `FAIL_SIM_CORRECTNESS` | edge@0.310ns bit=0 expected=1 vin=0.200 edge@3.510ns bit=0 expected=1 vin=0.200 edge@7.510ns bit=0 expected=1 vin=0.200 edge@11.510ns bit=0 expected=1 vin=0.200 edge@15.510ns bit=0 expected=1 vin=0.200 edge@18.710ns bit=0 expected=1 vin=0.600 |
| `496-first-order-sigma-delta-modulator` | `FAIL_SIM_CORRECTNESS` | edge@0.310ns bit=0 expected=1 vin=0.200 edge@1.110ns bit=1 expected=0 vin=0.200 edge@3.510ns bit=0 expected=1 vin=0.200 edge@4.310ns bit=1 expected=0 vin=0.200 edge@7.510ns bit=0 expected=1 vin=0.200 edge@8.310ns bit=1 expected=0 vin=0.200 |
| `496-first-order-sigma-delta-modulator` | `FAIL_SIM_CORRECTNESS` | edge@1.910ns bit=1 expected=0 vin=0.200 edge@5.910ns bit=1 expected=0 vin=0.200 edge@9.910ns bit=1 expected=0 vin=0.200 edge@13.910ns bit=1 expected=0 vin=0.200 edge@17.910ns bit=1 expected=0 vin=0.200 edge@19.510ns bit=1 expected=0 vin=0.600 |
| `497-thermometer-bus-encoder` | `FAIL_SIM_CORRECTNESS` | therm@1.40ns code=1 observed=0 prefix=00000000 therm@3.40ns code=5 observed=0 prefix=00000000 therm@5.40ns code=11 observed=0 prefix=00000000 therm@7.40ns code=15 observed=0 prefix=00000000 therm@9.40ns code=16 observed=0 prefix=00000000 |
| `497-thermometer-bus-encoder` | `FAIL_SIM_CORRECTNESS` | tran.csv missing |
| `497-thermometer-bus-encoder` | `FAIL_SIM_CORRECTNESS` | tran.csv missing |
| `497-thermometer-bus-encoder` | `FAIL_SIM_CORRECTNESS` | tran.csv missing |
| `497-thermometer-bus-encoder` | `FAIL_SIM_CORRECTNESS` | therm@3.40ns code=5 observed=6 prefix=11111100 therm@5.40ns code=11 observed=12 prefix=11111111 therm@7.40ns code=15 observed=16 prefix=11111111 |
| `498-dc-aware-adc3bit` | `FAIL_SIM_CORRECTNESS` | adc3@3.80ns vin=0.190 code=1 obs={'d2': 0, 'd1': 0, 'd0': 0} adc3@5.80ns vin=0.380 code=3 obs={'d2': 0, 'd1': 0, 'd0': 0} adc3@7.80ns vin=0.620 code=4 obs={'d2': 0, 'd1': 0, 'd0': 0} adc3@9.80ns vin=0.870 code=6 obs={'d2': 0, 'd1': 0, 'd0': 0} adc3@11.80ns vin=1.100 code=7 obs={'d2': 0, 'd1': 0, 'd0': 0} |
| `498-dc-aware-adc3bit` | `FAIL_SIM_CORRECTNESS` | adc3@5.80ns vin=0.380 code=3 obs={'d2': 0, 'd1': 1, 'd0': 0} |
| `498-dc-aware-adc3bit` | `FAIL_SIM_CORRECTNESS` | adc3@3.80ns vin=0.190 code=1 obs={'d2': 1, 'd1': 0, 'd0': 0} adc3@5.80ns vin=0.380 code=3 obs={'d2': 1, 'd1': 1, 'd0': 0} adc3@7.80ns vin=0.620 code=4 obs={'d2': 0, 'd1': 0, 'd0': 1} adc3@9.80ns vin=0.870 code=6 obs={'d2': 0, 'd1': 1, 'd0': 1} |
| `498-dc-aware-adc3bit` | `FAIL_SIM_CORRECTNESS` | adc3@11.80ns vin=1.100 code=7 obs={'d2': 0, 'd1': 0, 'd0': 0} |
| `498-dc-aware-adc3bit` | `FAIL_SIM_CORRECTNESS` | adc3@3.80ns vin=0.190 code=1 obs={'d2': 0, 'd1': 1, 'd0': 0} adc3@7.80ns vin=0.620 code=4 obs={'d2': 1, 'd1': 0, 'd0': 1} adc3@9.80ns vin=0.870 code=6 obs={'d2': 1, 'd1': 1, 'd0': 1} |
| `499-latched-bus-dac8` | `FAIL_SIM_CORRECTNESS` | max_latched_dac_edge_err=0.9412 codes=[17, 126, 128, 45, 240] |
| `499-latched-bus-dac8` | `FAIL_SIM_CORRECTNESS` | max_latched_dac_hold_err=0.7647 codes=[17, 126, 128, 45, 240] |
| `499-latched-bus-dac8` | `FAIL_SIM_CORRECTNESS` | max_latched_dac_edge_err=0.7647 codes=[17, 126, 128, 45, 240] |
| `499-latched-bus-dac8` | `FAIL_SIM_CORRECTNESS` | max_latched_dac_edge_err=0.8824 codes=[17, 126, 128, 45, 240] |
| `499-latched-bus-dac8` | `FAIL_SIM_CORRECTNESS` | max_latched_dac_edge_err=0.9486 codes=[17, 126, 128, 45, 240] |
| `500-deterministic-mismatch-dac6` | `FAIL_SIM_CORRECTNESS` | max_mismatch_dac_err=1.0000 codes=[0, 3, 17, 34, 45, 62, 63] |
| `500-deterministic-mismatch-dac6` | `FAIL_SIM_CORRECTNESS` | max_mismatch_dac_err=0.0250 codes=[0, 3, 17, 34, 45, 62, 63] |
| `500-deterministic-mismatch-dac6` | `FAIL_SIM_CORRECTNESS` | max_mismatch_dac_err=0.0515 codes=[0, 3, 17, 34, 45, 62, 63] |
| `500-deterministic-mismatch-dac6` | `FAIL_SIM_CORRECTNESS` | max_mismatch_dac_err=0.7182 codes=[0, 3, 17, 34, 45, 62, 63] |
| `500-deterministic-mismatch-dac6` | `FAIL_SIM_CORRECTNESS` | max_mismatch_dac_err=0.0291 codes=[0, 3, 17, 34, 45, 62, 63] |
| `501-adc-static-linearity-monitor` | `FAIL_SIM_CORRECTNESS` | maxerr_metric_error=2.0000 metrics=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0] |
| `501-adc-static-linearity-monitor` | `FAIL_SIM_CORRECTNESS` | maxerr_not_monotonic=[0.0, 1.0, 0.0, 2.0, 0.0, 0.0] |
| `501-adc-static-linearity-monitor` | `FAIL_SIM_CORRECTNESS` | maxerr_metric_error=3.0000 metrics=[3.0, 3.0, 3.0, 5.0, 5.0, 5.0] |
| `501-adc-static-linearity-monitor` | `FAIL_SIM_CORRECTNESS` | maxerr_metric_error=1.0000 metrics=[1.0, 1.0, 1.0, 2.0, 2.0, 2.0] |
| `501-adc-static-linearity-monitor` | `FAIL_SIM_CORRECTNESS` | maxerr_metric_error=1.0000 metrics=[0.0, 0.0, 1.0, 1.0, 1.0, 1.0] |
