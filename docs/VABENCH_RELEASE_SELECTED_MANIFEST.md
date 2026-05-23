# vaBench Release Selected Manifest

Date: 2026-05-15

This manifest records selected L1/L2 release entries created by the
long-run materializer. Rows without release-ready source tasks are kept
as explicit pending package entries rather than hidden missing work.

## Summary

| Metric | Count |
| --- | ---: |
| selected entries | 46 |
| entries with copied or designed source assets | 46 |
| entries pending source design | 0 |

## Rows

| Entry | Forms | Missing forms | Source paths | Notes |
| --- | --- | --- | --- | --- |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix|dut|e2e|tb` | `` | `tasks/spec-to-va/voltage/dac/vbm1_thermometer_dac_15seg_dut|tasks/tb-generation/voltage/dac/vbm1_thermometer_dac_15seg_tb|tasks/bugfix/voltage/dac/vbm1_thermometer_dac_15seg_bugfix|tasks/end-to-end/voltage/dac/vbm1_thermometer_dac_15seg_e2e` | selected source copied; release checks normalized when needed; dual evidence pending rerun |
| `vbr1_l1_clocked_adc_quantizer` | `dut|tb|bugfix|e2e` | `` | `tasks/end-to-end/voltage/flash_adc_3b_smoke` | selected source copied; release checks normalized when needed; dual evidence pending rerun; companion forms generated from existing release gold; true-bugfix companion generated from existing release gold |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut|tb|bugfix|e2e` | `` | `tasks/spec-to-va/voltage/dac/cdac_cal` | selected source copied; release checks normalized when needed; dual evidence pending rerun; companion forms generated from existing release gold; true-bugfix companion generated from existing release gold |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut|tb|bugfix|e2e` | `` | `designed_release_spec:vbr1_l1_dac_mismatch_unit_weighting_model` | designed release source generated; dual evidence pending rerun |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb|e2e` | `` | `tasks/end-to-end/voltage/adc_dac_ideal_4b_smoke` | selected source copied; release checks normalized when needed; dual evidence pending rerun; companion forms generated from existing release gold |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb|e2e` | `` | `tasks/end-to-end/voltage/sar_adc_dac_weighted_8b_smoke` | selected source copied; release checks normalized when needed; dual evidence pending rerun; companion forms generated from existing release gold |
| `vbr1_l2_flash_adc_mini_array` | `tb|e2e` | `` | `tasks/end-to-end/voltage/flash_adc_3b_smoke` | selected source copied; release checks normalized when needed; dual evidence pending rerun; companion forms generated from existing release gold |
| `vbr1_l1_threshold_comparator` | `dut|tb|bugfix|e2e` | `` | `tasks/end-to-end/voltage/comparator_smoke` | selected source copied; release checks normalized when needed; dual evidence pending rerun; companion forms generated from existing release gold; true-bugfix companion generated from existing release gold |
| `vbr1_l1_propagation_delay_comparator` | `dut|tb|bugfix|e2e` | `` | `tasks/end-to-end/voltage/cmp_delay_smoke` | selected source copied; release checks normalized when needed; dual evidence pending rerun; companion forms generated from existing release gold; true-bugfix companion generated from existing release gold |
| `vbr1_l1_hysteresis_comparator` | `dut|tb|bugfix|e2e` | `` | `tasks/end-to-end/voltage/comparator_hysteresis_smoke` | selected source copied; release checks normalized when needed; dual evidence pending rerun; companion forms generated from existing release gold; true-bugfix companion generated from existing release gold |
| `vbr1_l1_window_comparator_detector` | `dut|tb|bugfix|e2e` | `` | `manual_release_spec:vbr1_l1_window_comparator_detector` | manual release spec corrected to true window semantics; fresh dual evidence pending rerun; companion forms generated from existing release gold; true-bugfix companion generated from existing release gold |
| `vbr1_l2_comparator_measurement_flow` | `tb|e2e` | `` | `tasks/end-to-end/voltage/comparator_measurement_flow_smoke` | selected source copied; release checks normalized when needed; dual evidence pending rerun; companion forms generated from existing release gold |
| `vbr1_l1_pfd_small_phase_error_response` | `dut|tb|bugfix|e2e` | `` | `tasks/spec-to-va/voltage/pll-clock/vbm1_pfd_small_phase_error_response_dut|tasks/end-to-end/voltage/pfd_small_phase_response_smoke` | selected source copied; release checks normalized when needed; dual evidence pending rerun; companion forms generated from existing release gold; true-bugfix companion generated from existing release gold |
| `vbr1_l1_xor_phase_detector` | `dut|tb|bugfix|e2e` | `` | `tasks/end-to-end/voltage/xor_pd_smoke` | selected source copied; release checks normalized when needed; dual evidence pending rerun; companion forms generated from existing release gold; true-bugfix companion generated from existing release gold |
| `vbr1_l1_bang_bang_phase_detector` | `dut|tb|bugfix|e2e` | `` | `tasks/spec-to-va/voltage/pll-clock/bbpd|tasks/end-to-end/voltage/bbpd_data_edge_alignment_smoke` | selected source copied; release checks normalized when needed; dual evidence pending rerun; companion forms generated from existing release gold; true-bugfix companion generated from existing release gold |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut|tb|bugfix|e2e` | `` | `tasks/end-to-end/voltage/phase_accumulator_timer_wrap_smoke` | selected source copied; release checks normalized when needed; dual evidence pending rerun; companion forms generated from existing release gold; true-bugfix companion generated from existing release gold |
| `vbr1_l1_charge_pump_abstraction` | `dut|tb|bugfix|e2e` | `` | `designed_release_spec:vbr1_l1_charge_pump_abstraction` | designed release source generated; dual evidence pending rerun |
| `vbr1_l1_loop_filter_abstraction` | `dut|tb|bugfix|e2e` | `` | `designed_release_spec:vbr1_l1_loop_filter_abstraction` | designed release source generated; dual evidence pending rerun |
| `vbr1_l2_pll_timing_slice` | `tb|e2e` | `` | `tasks/end-to-end/voltage/cppll_tracking_smoke` | selected source copied; release checks normalized when needed; dual evidence pending rerun; companion forms generated from existing release gold |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb|e2e` | `` | `tasks/end-to-end/voltage/adpll_ratio_hop_smoke` | selected source copied; release checks normalized when needed; dual evidence pending rerun; companion forms generated from existing release gold |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb|e2e` | `` | `tasks/end-to-end/voltage/cppll_freq_step_reacquire_smoke` | selected source copied; release checks normalized when needed; dual evidence pending rerun; companion forms generated from existing release gold |
| `vbr1_l1_dwa_dem_encoder` | `dut|tb|bugfix|e2e` | `` | `tasks/end-to-end/voltage/dwa_ptr_gen_smoke` | selected source copied; release checks normalized when needed; dual evidence pending rerun; companion forms generated from existing release gold; true-bugfix companion generated from existing release gold |
| `vbr1_l1_calibration_deadband_controller` | `dut|tb|bugfix|e2e` | `` | `designed_release_spec:vbr1_l1_calibration_deadband_controller` | designed release source generated; dual evidence pending rerun |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut|tb|bugfix|e2e` | `` | `designed_release_spec:vbr1_l1_successive_approximation_calibration_search_fsm` | designed release source generated; dual evidence pending rerun |
| `vbr1_l2_complete_calibration_loop` | `e2e|tb` | `` | `designed_release_spec:vbr1_l2_complete_calibration_loop` | designed release source generated; dual evidence pending rerun |
| `vbr1_l1_lfsr_prbs_generator` | `dut|tb|bugfix|e2e` | `` | `tasks/spec-to-va/voltage/digital-logic/prbs7|tasks/end-to-end/voltage/lfsr_smoke` | selected source copied; release checks normalized when needed; dual evidence pending rerun; companion forms generated from existing release gold; true-bugfix companion generated from existing release gold |
| `vbr1_l1_serializer_frame_aligner` | `dut|tb|bugfix|e2e` | `` | `tasks/end-to-end/voltage/serializer_frame_alignment_smoke` | selected source copied; release checks normalized when needed; dual evidence pending rerun; companion forms generated from existing release gold; true-bugfix companion generated from existing release gold |
| `vbr1_l1_event_pulse_stretcher` | `dut|tb|bugfix|e2e` | `` | `designed_release_spec:vbr1_l1_event_pulse_stretcher` | designed release source generated; dual evidence pending rerun |
| `vbr1_l2_event_controller` | `tb|e2e` | `` | `tasks/end-to-end/voltage/simultaneous_event_order_smoke` | selected source copied; release checks normalized when needed; dual evidence pending rerun; companion forms generated from existing release gold |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb|e2e` | `` | `tasks/end-to-end/voltage/serializer_frame_alignment_smoke` | selected source copied; release checks normalized when needed; dual evidence pending rerun; companion forms generated from existing release gold |
| `vbr1_l1_gain_estimator` | `tb|e2e` | `` | `tasks/end-to-end/voltage/gain_extraction_smoke` | selected source copied; release checks normalized when needed; dual evidence pending rerun; companion forms generated from existing release gold |
| `vbr1_l1_edge_interval_timer` | `tb|e2e` | `` | `tasks/end-to-end/voltage/cross_interval_163p333_smoke` | selected source copied; release checks normalized when needed; dual evidence pending rerun; companion forms generated from existing release gold |
| `vbr1_l2_measurement_flow` | `tb|e2e` | `` | `tasks/end-to-end/voltage/final_step_file_metric_smoke` | selected source copied; release checks normalized when needed; dual evidence pending rerun; companion forms generated from existing release gold |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb|e2e` | `` | `tasks/end-to-end/voltage/gain_extraction_smoke` | selected source copied; release checks normalized when needed; dual evidence pending rerun; companion forms generated from existing release gold |
| `vbr1_l1_ramp_or_step_source` | `dut|tb|e2e` | `` | `tasks/end-to-end/voltage/bound_step_period_guard_smoke` | selected source copied; release checks normalized when needed; dual evidence pending rerun; companion forms generated from existing release gold |
| `vbr1_l1_burst_clock_source` | `dut|tb|e2e` | `` | `tasks/end-to-end/voltage/clk_burst_gen_smoke` | selected source copied; release checks normalized when needed; dual evidence pending rerun; companion forms generated from existing release gold |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut|tb|e2e` | `` | `tasks/end-to-end/voltage/noise_gen_smoke` | selected source copied; release checks normalized when needed; dual evidence pending rerun; companion forms generated from existing release gold |
| `vbr1_l1_sine_periodic_voltage_source` | `dut|tb|e2e` | `` | `tasks/spec-to-va/voltage/signal-source/multitone` | selected source copied; release checks normalized when needed; dual evidence pending rerun; companion forms generated from existing release gold |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e|tb` | `` | `designed_release_spec:vbr1_l2_adc_dac_source_sweep_flow` | designed release source generated; dual evidence pending rerun |
| `vbr1_l1_soft_hysteretic_limiter` | `dut|tb|bugfix|e2e` | `` | `designed_release_spec:vbr1_l1_soft_hysteretic_limiter` | designed release source generated; dual evidence pending rerun |
| `vbr1_l1_voltage_gain_amplifier` | `dut|tb|bugfix|e2e` | `` | `designed_release_spec:vbr1_l1_voltage_gain_amplifier` | designed release source generated; dual evidence pending rerun |
| `vbr1_l1_higher_order_filter` | `dut|tb|bugfix|e2e` | `` | `designed_release_spec:vbr1_l1_higher_order_filter` | designed release source generated; dual evidence pending rerun |
| `vbr1_l2_amplifier_filter_chain` | `e2e|tb` | `` | `designed_release_spec:vbr1_l2_amplifier_filter_chain` | designed release source generated; dual evidence pending rerun |
| `vbr1_l1_clocked_sample_and_hold` | `dut|tb|bugfix|e2e` | `` | `tasks/end-to-end/voltage/sample_hold_smoke` | selected source copied; release checks normalized when needed; dual evidence pending rerun; companion forms generated from existing release gold; true-bugfix companion generated from existing release gold |
| `vbr1_l2_converter_front_end` | `tb|e2e` | `` | `tasks/end-to-end/voltage/sample_hold_droop_smoke` | selected source copied; release checks normalized when needed; dual evidence pending rerun; companion forms generated from existing release gold |
