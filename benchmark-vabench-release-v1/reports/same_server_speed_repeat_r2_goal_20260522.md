# Same-Server EVAS/Spectre Speed

Date: 2026-05-22
Claim allowed: `False`
Reason: Same-server timing is measured directly on one host and the artifact emits checker/waveform accuracy gates. Paper-facing speed claims should use only accuracy-gated rows and still need repeated cold/warm runs.

## Scope

- Host: `thu-sui`
- Selected rows: 259
- Jobs: 8
- EVAS modes: `strict_current, profile_fast_skip_source_error_control`
- Spectre modes: `ax, classic`
- Output root: `results/same-server-speed-repeat-r2-goal-20260522`

## Mode Summary

| Backend | Mode | Runs | PASS | Non-PASS | Total wall s | Mean wall s |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| evas | profile_fast_skip_source_error_control | 259 | 259 | 0 | 500.582 | 1.933 |
| evas | strict_current | 259 | 259 | 0 | 1523.088 | 5.881 |
| spectre | ax | 259 | 259 | 0 | 2007.435 | 7.751 |
| spectre | classic | 259 | 259 | 0 | 6161.326 | 23.789 |

## Accuracy Gate Summary

| EVAS mode | Runs | Gate PASS | Gate FAIL | Gate BLOCKED | Gate missing |
| --- | ---: | ---: | ---: | ---: | ---: |
| profile_fast_skip_source_error_control | 259 | 259 | 0 | 0 | 0 |
| strict_current | 259 | 259 | 0 | 0 | 0 |

## Per-Row Accuracy Gates

| Entry | Form | Variant | EVAS mode | Gate | Reasons | Blocked |
| --- | --- | --- | --- | --- | --- | --- |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_event_controller` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_event_controller` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |

## Simulation-Only Speedups

| Entry | Form | Variant | Spectre mode | EVAS mode | Spectre wall s | EVAS wall s | Spectre/EVAS |
| --- | --- | --- | --- | --- | ---: | ---: | ---: |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.307 | 1.310 | 4.813 |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.307 | 1.240 | 5.087 |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.133 | 1.310 | 19.180 |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.133 | 1.240 | 20.270 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.667 | 1.114 | 5.983 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `ax` | `strict_current` | 6.667 | 1.376 | 4.844 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.695 | 1.114 | 22.163 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `classic` | `strict_current` | 24.695 | 1.376 | 17.945 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.141 | 1.253 | 4.902 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `ax` | `strict_current` | 6.141 | 1.312 | 4.681 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.441 | 1.253 | 19.509 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `classic` | `strict_current` | 24.441 | 1.312 | 18.632 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.850 | 1.195 | 6.567 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `ax` | `strict_current` | 7.850 | 1.749 | 4.489 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.201 | 1.195 | 22.754 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `classic` | `strict_current` | 27.201 | 1.749 | 15.552 |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.249 | 1.627 | 3.841 |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.249 | 10.404 | 0.601 |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 23.138 | 1.627 | 14.223 |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 23.138 | 10.404 | 2.224 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.467 | 1.424 | 4.542 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `ax` | `strict_current` | 6.467 | 10.449 | 0.619 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 22.285 | 1.424 | 15.653 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `classic` | `strict_current` | 22.285 | 10.449 | 2.133 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.259 | 1.648 | 3.797 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `ax` | `strict_current` | 6.259 | 1.989 | 3.146 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.520 | 1.648 | 14.875 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `classic` | `strict_current` | 24.520 | 1.989 | 12.326 |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.056 | 1.829 | 3.858 |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `ax` | `strict_current` | 7.056 | 1.951 | 3.616 |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.567 | 1.829 | 13.432 |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `classic` | `strict_current` | 24.567 | 1.951 | 12.590 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 16.484 | 1.034 | 15.944 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `ax` | `strict_current` | 16.484 | 1.182 | 13.946 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 27.733 | 1.034 | 26.825 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `classic` | `strict_current` | 27.733 | 1.182 | 23.464 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 17.526 | 1.068 | 16.410 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `ax` | `strict_current` | 17.526 | 0.908 | 19.300 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.738 | 1.068 | 25.971 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `classic` | `strict_current` | 27.738 | 0.908 | 30.546 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 18.523 | 0.994 | 18.633 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `ax` | `strict_current` | 18.523 | 1.036 | 17.881 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 29.571 | 0.994 | 29.746 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `classic` | `strict_current` | 29.571 | 1.036 | 28.546 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.717 | 0.836 | 8.031 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `ax` | `strict_current` | 6.717 | 0.999 | 6.721 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.577 | 0.836 | 30.580 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `classic` | `strict_current` | 25.577 | 0.999 | 25.593 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.221 | 0.917 | 6.786 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `ax` | `strict_current` | 6.221 | 1.378 | 4.514 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.159 | 0.917 | 27.444 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `classic` | `strict_current` | 25.159 | 1.378 | 18.257 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.692 | 1.024 | 6.537 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `ax` | `strict_current` | 6.692 | 1.360 | 4.921 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.215 | 1.024 | 24.629 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `classic` | `strict_current` | 25.215 | 1.360 | 18.542 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.535 | 0.953 | 6.859 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `ax` | `strict_current` | 6.535 | 1.487 | 4.396 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.087 | 0.953 | 27.379 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `classic` | `strict_current` | 26.087 | 1.487 | 17.548 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.642 | 0.877 | 7.577 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.642 | 1.781 | 3.728 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.709 | 0.877 | 29.330 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.709 | 1.781 | 14.431 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.505 | 0.874 | 7.447 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `ax` | `strict_current` | 6.505 | 1.629 | 3.993 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.216 | 0.874 | 28.868 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `classic` | `strict_current` | 25.216 | 1.629 | 15.478 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.609 | 0.800 | 8.266 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `ax` | `strict_current` | 6.609 | 1.687 | 3.918 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.210 | 0.800 | 31.532 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `classic` | `strict_current` | 25.210 | 1.687 | 14.947 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.456 | 0.888 | 7.270 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `ax` | `strict_current` | 6.456 | 1.717 | 3.760 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.849 | 0.888 | 26.855 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `classic` | `strict_current` | 23.849 | 1.717 | 13.889 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.389 | 1.776 | 3.598 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.389 | 3.510 | 1.820 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.235 | 1.776 | 13.646 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.235 | 3.510 | 6.904 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.740 | 1.781 | 3.222 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `ax` | `strict_current` | 5.740 | 3.488 | 1.646 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.075 | 1.781 | 13.515 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `classic` | `strict_current` | 24.075 | 3.488 | 6.903 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.120 | 1.739 | 3.519 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `ax` | `strict_current` | 6.120 | 3.500 | 1.748 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.029 | 1.739 | 13.818 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `classic` | `strict_current` | 24.029 | 3.500 | 6.866 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.276 | 1.812 | 3.464 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `ax` | `strict_current` | 6.276 | 3.509 | 1.789 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.940 | 1.812 | 13.212 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `classic` | `strict_current` | 23.940 | 3.509 | 6.822 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.815 | 0.934 | 7.293 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.815 | 1.748 | 3.900 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.200 | 0.934 | 25.897 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.200 | 1.748 | 13.848 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.250 | 0.859 | 7.276 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `ax` | `strict_current` | 6.250 | 1.618 | 3.864 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.100 | 0.859 | 29.218 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `classic` | `strict_current` | 25.100 | 1.618 | 15.517 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.356 | 0.772 | 8.233 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `ax` | `strict_current` | 6.356 | 1.710 | 3.718 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.524 | 0.772 | 34.357 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `classic` | `strict_current` | 26.524 | 1.710 | 15.513 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.327 | 0.877 | 7.213 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `ax` | `strict_current` | 6.327 | 1.599 | 3.956 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.156 | 0.877 | 28.682 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `classic` | `strict_current` | 25.156 | 1.599 | 15.730 |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.443 | 1.433 | 4.496 |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.443 | 4.071 | 1.583 |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 23.160 | 1.433 | 16.161 |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `classic` | `strict_current` | 23.160 | 4.071 | 5.689 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.396 | 1.474 | 4.338 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `ax` | `strict_current` | 6.396 | 4.045 | 1.581 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.199 | 1.474 | 16.413 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `classic` | `strict_current` | 24.199 | 4.045 | 5.983 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.578 | 1.815 | 3.625 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `ax` | `strict_current` | 6.578 | 4.274 | 1.539 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.260 | 1.815 | 13.368 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `classic` | `strict_current` | 24.260 | 4.274 | 5.676 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.833 | 1.609 | 3.624 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `ax` | `strict_current` | 5.833 | 4.156 | 1.403 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.361 | 1.609 | 14.516 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `classic` | `strict_current` | 23.361 | 4.156 | 5.621 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.469 | 1.002 | 6.458 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.469 | 1.639 | 3.948 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.244 | 1.002 | 25.199 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.244 | 1.639 | 15.404 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.577 | 0.879 | 7.483 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `ax` | `strict_current` | 6.577 | 1.625 | 4.047 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.831 | 0.879 | 28.248 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `classic` | `strict_current` | 24.831 | 1.625 | 15.278 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.322 | 1.006 | 6.287 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `ax` | `strict_current` | 6.322 | 1.641 | 3.853 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.760 | 1.006 | 24.622 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `classic` | `strict_current` | 24.760 | 1.641 | 15.090 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.682 | 0.936 | 7.142 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `ax` | `strict_current` | 6.682 | 1.727 | 3.869 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.316 | 0.936 | 27.059 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `classic` | `strict_current` | 25.316 | 1.727 | 14.659 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 5.900 | 1.179 | 5.006 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 5.900 | 3.237 | 1.823 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 23.960 | 1.179 | 20.328 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 23.960 | 3.237 | 7.402 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.490 | 1.118 | 5.806 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `ax` | `strict_current` | 6.490 | 3.209 | 2.022 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.923 | 1.118 | 21.405 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `classic` | `strict_current` | 23.923 | 3.209 | 7.456 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.195 | 1.212 | 5.112 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 6.195 | 3.128 | 1.981 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.546 | 1.212 | 19.430 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 23.546 | 3.128 | 7.528 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.638 | 1.284 | 4.391 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `ax` | `strict_current` | 5.638 | 3.100 | 1.819 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.260 | 1.284 | 18.113 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `classic` | `strict_current` | 23.260 | 3.100 | 7.502 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.979 | 0.993 | 7.026 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.979 | 1.584 | 4.406 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 14.603 | 0.993 | 14.701 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `classic` | `strict_current` | 14.603 | 1.584 | 9.220 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.520 | 0.839 | 7.769 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `ax` | `strict_current` | 6.520 | 1.463 | 4.456 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.871 | 0.839 | 16.529 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `classic` | `strict_current` | 13.871 | 1.463 | 9.481 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.279 | 0.887 | 7.080 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `ax` | `strict_current` | 6.279 | 1.561 | 4.022 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.232 | 0.887 | 14.919 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `classic` | `strict_current` | 13.232 | 1.561 | 8.476 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.629 | 0.963 | 6.883 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `ax` | `strict_current` | 6.629 | 1.515 | 4.375 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.149 | 0.963 | 13.653 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `classic` | `strict_current` | 13.149 | 1.515 | 8.678 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.619 | 1.050 | 8.210 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `ax` | `strict_current` | 8.619 | 0.806 | 10.697 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 16.250 | 1.050 | 15.480 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `classic` | `strict_current` | 16.250 | 0.806 | 20.169 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.284 | 0.770 | 8.163 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `ax` | `strict_current` | 6.284 | 0.865 | 7.268 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.366 | 0.770 | 18.662 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `classic` | `strict_current` | 14.366 | 0.865 | 16.616 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.960 | 0.793 | 8.778 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `ax` | `strict_current` | 6.960 | 0.873 | 7.970 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.092 | 0.793 | 19.035 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `classic` | `strict_current` | 15.092 | 0.873 | 17.283 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.154 | 0.783 | 7.862 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.154 | 0.766 | 8.036 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 26.217 | 0.783 | 33.491 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `classic` | `strict_current` | 26.217 | 0.766 | 34.234 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.369 | 0.752 | 8.475 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `ax` | `strict_current` | 6.369 | 0.812 | 7.840 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.495 | 0.752 | 35.256 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `classic` | `strict_current` | 26.495 | 0.812 | 32.612 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.392 | 0.824 | 8.976 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `ax` | `strict_current` | 7.392 | 0.862 | 8.575 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.395 | 0.824 | 32.052 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `classic` | `strict_current` | 26.395 | 0.862 | 30.620 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.977 | 0.769 | 9.075 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `ax` | `strict_current` | 6.977 | 0.936 | 7.452 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.352 | 0.769 | 34.277 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `classic` | `strict_current` | 26.352 | 0.936 | 28.144 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 17.520 | 0.767 | 22.828 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `ax` | `strict_current` | 17.520 | 0.992 | 17.654 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 27.652 | 0.767 | 36.030 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `classic` | `strict_current` | 27.652 | 0.992 | 27.864 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.205 | 0.877 | 7.075 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `ax` | `strict_current` | 6.205 | 1.018 | 6.096 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.620 | 0.877 | 31.489 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `classic` | `strict_current` | 27.620 | 1.018 | 27.132 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.474 | 1.003 | 6.457 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `ax` | `strict_current` | 6.474 | 0.997 | 6.490 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.530 | 1.003 | 24.466 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `classic` | `strict_current` | 24.530 | 0.997 | 24.592 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 15.523 | 0.764 | 20.328 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `ax` | `strict_current` | 15.523 | 0.951 | 16.318 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.389 | 0.764 | 33.248 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `classic` | `strict_current` | 25.389 | 0.951 | 26.690 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 5.779 | 0.965 | 5.989 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `ax` | `strict_current` | 5.779 | 4.626 | 1.249 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.686 | 0.965 | 25.584 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.686 | 4.626 | 5.337 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.554 | 1.052 | 6.229 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `ax` | `strict_current` | 6.554 | 4.806 | 1.364 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.274 | 1.052 | 23.068 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `classic` | `strict_current` | 24.274 | 4.806 | 5.051 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.961 | 1.122 | 5.312 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `ax` | `strict_current` | 5.961 | 4.526 | 1.317 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.612 | 1.122 | 21.932 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `classic` | `strict_current` | 24.612 | 4.526 | 5.438 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.263 | 1.074 | 5.832 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `ax` | `strict_current` | 6.263 | 4.671 | 1.341 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.005 | 1.074 | 22.354 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `classic` | `strict_current` | 24.005 | 4.671 | 5.139 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.198 | 1.624 | 3.816 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.198 | 1.843 | 3.363 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.289 | 1.624 | 15.570 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.289 | 1.843 | 13.722 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.658 | 1.685 | 3.952 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `ax` | `strict_current` | 6.658 | 1.739 | 3.829 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.390 | 1.685 | 14.479 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `classic` | `strict_current` | 24.390 | 1.739 | 14.028 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.400 | 1.492 | 4.289 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `ax` | `strict_current` | 6.400 | 1.660 | 3.855 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.665 | 1.492 | 16.529 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `classic` | `strict_current` | 24.665 | 1.660 | 14.854 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.281 | 1.699 | 4.284 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `ax` | `strict_current` | 7.281 | 1.571 | 4.635 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.919 | 1.699 | 14.663 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `classic` | `strict_current` | 24.919 | 1.571 | 15.862 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.359 | 0.848 | 7.498 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `ax` | `strict_current` | 6.359 | 0.899 | 7.073 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 10.743 | 0.848 | 12.668 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `classic` | `strict_current` | 10.743 | 0.899 | 11.950 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.204 | 0.889 | 6.981 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `ax` | `strict_current` | 6.204 | 0.761 | 8.155 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.064 | 0.889 | 15.824 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `classic` | `strict_current` | 14.064 | 0.761 | 18.486 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.342 | 0.884 | 7.171 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `ax` | `strict_current` | 6.342 | 0.857 | 7.401 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 12.538 | 0.884 | 14.176 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `classic` | `strict_current` | 12.538 | 0.857 | 14.633 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.591 | 0.816 | 8.077 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.591 | 2.811 | 2.344 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 45.582 | 0.816 | 55.859 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `classic` | `strict_current` | 45.582 | 2.811 | 16.213 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.847 | 0.865 | 7.912 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `ax` | `strict_current` | 6.847 | 2.667 | 2.567 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 45.947 | 0.865 | 53.091 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `classic` | `strict_current` | 45.947 | 2.667 | 17.225 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.504 | 0.940 | 7.985 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `ax` | `strict_current` | 7.504 | 2.651 | 2.830 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 45.508 | 0.940 | 48.421 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `classic` | `strict_current` | 45.508 | 2.651 | 17.164 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.087 | 0.796 | 8.903 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `ax` | `strict_current` | 7.087 | 2.640 | 2.685 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 45.335 | 0.796 | 56.951 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `classic` | `strict_current` | 45.335 | 2.640 | 17.174 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 16.186 | 1.048 | 15.446 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 16.186 | 0.980 | 16.517 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 26.623 | 1.048 | 25.406 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 26.623 | 0.980 | 27.167 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.408 | 0.959 | 7.722 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `ax` | `strict_current` | 7.408 | 0.952 | 7.780 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.467 | 0.959 | 28.631 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `classic` | `strict_current` | 27.467 | 0.952 | 28.846 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.019 | 0.905 | 7.758 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `ax` | `strict_current` | 7.019 | 1.035 | 6.781 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.905 | 0.905 | 27.528 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `classic` | `strict_current` | 24.905 | 1.035 | 24.060 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 17.693 | 0.974 | 18.169 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `ax` | `strict_current` | 17.693 | 1.096 | 16.142 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.886 | 0.974 | 28.635 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `classic` | `strict_current` | 27.886 | 1.096 | 25.441 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.253 | 1.388 | 4.505 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `ax` | `strict_current` | 6.253 | 4.662 | 1.341 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.609 | 1.388 | 17.731 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `classic` | `strict_current` | 24.609 | 4.662 | 5.279 |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.002 | 1.262 | 4.756 |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `ax` | `strict_current` | 6.002 | 4.594 | 1.307 |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 22.147 | 1.262 | 17.547 |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `classic` | `strict_current` | 22.147 | 4.594 | 4.821 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.137 | 0.788 | 7.785 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.137 | 1.102 | 5.568 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.578 | 0.788 | 32.449 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.578 | 1.102 | 23.210 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.358 | 0.980 | 7.510 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `ax` | `strict_current` | 7.358 | 1.277 | 5.762 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.937 | 0.980 | 26.470 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `classic` | `strict_current` | 25.937 | 1.277 | 20.308 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.026 | 0.792 | 7.608 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `ax` | `strict_current` | 6.026 | 1.022 | 5.895 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.712 | 0.792 | 31.200 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `classic` | `strict_current` | 24.712 | 1.022 | 24.174 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.166 | 0.805 | 8.901 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `ax` | `strict_current` | 7.166 | 1.008 | 7.109 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.956 | 0.805 | 32.241 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `classic` | `strict_current` | 25.956 | 1.008 | 25.749 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.815 | 0.774 | 8.809 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.815 | 0.881 | 7.740 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.785 | 0.774 | 32.035 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.785 | 0.881 | 28.147 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.044 | 0.737 | 8.202 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `ax` | `strict_current` | 6.044 | 0.931 | 6.493 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.321 | 0.737 | 34.365 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `classic` | `strict_current` | 25.321 | 0.931 | 27.203 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.752 | 0.803 | 8.407 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `ax` | `strict_current` | 6.752 | 0.934 | 7.226 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.430 | 0.803 | 30.420 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `classic` | `strict_current` | 24.430 | 0.934 | 26.146 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.559 | 0.917 | 7.149 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `ax` | `strict_current` | 6.559 | 1.008 | 6.505 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.739 | 0.917 | 28.057 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `classic` | `strict_current` | 25.739 | 1.008 | 25.529 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 15.361 | 1.017 | 15.105 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `ax` | `strict_current` | 15.361 | 1.072 | 14.328 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 13.815 | 1.017 | 13.585 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `classic` | `strict_current` | 13.815 | 1.072 | 12.886 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.442 | 1.161 | 5.550 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `ax` | `strict_current` | 6.442 | 1.154 | 5.583 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.089 | 1.161 | 11.276 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `classic` | `strict_current` | 13.089 | 1.154 | 11.342 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 16.258 | 1.122 | 14.489 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `ax` | `strict_current` | 16.258 | 1.165 | 13.958 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.581 | 1.122 | 12.994 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `classic` | `strict_current` | 14.581 | 1.165 | 12.518 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.997 | 1.184 | 5.908 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `ax` | `strict_current` | 6.997 | 1.087 | 6.437 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.126 | 1.184 | 11.927 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `classic` | `strict_current` | 14.126 | 1.087 | 12.995 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.748 | 9.561 | 1.124 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `ax` | `strict_current` | 10.748 | 131.563 | 0.082 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 49.707 | 9.561 | 5.199 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `classic` | `strict_current` | 49.707 | 131.563 | 0.378 |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.892 | 33.266 | 0.327 |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `ax` | `strict_current` | 10.892 | 152.925 | 0.071 |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 47.749 | 33.266 | 1.435 |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `classic` | `strict_current` | 47.749 | 152.925 | 0.312 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 14.865 | 1.173 | 12.675 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `ax` | `strict_current` | 14.865 | 1.759 | 8.451 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 13.691 | 1.173 | 11.674 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `classic` | `strict_current` | 13.691 | 1.759 | 7.783 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 14.929 | 1.131 | 13.197 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `ax` | `strict_current` | 14.929 | 1.625 | 9.185 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.883 | 1.131 | 13.156 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `classic` | `strict_current` | 14.883 | 1.625 | 9.156 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.321 | 1.110 | 5.693 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `ax` | `strict_current` | 6.321 | 1.612 | 3.921 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.806 | 1.110 | 12.435 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `classic` | `strict_current` | 13.806 | 1.612 | 8.565 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.106 | 1.138 | 6.244 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `ax` | `strict_current` | 7.106 | 1.641 | 4.330 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.268 | 1.138 | 11.658 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `classic` | `strict_current` | 13.268 | 1.641 | 8.086 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.992 | 1.035 | 6.756 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.992 | 1.302 | 5.369 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.109 | 1.035 | 24.261 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.109 | 1.302 | 19.281 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.459 | 0.883 | 7.318 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `ax` | `strict_current` | 6.459 | 1.338 | 4.828 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.462 | 0.883 | 27.717 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `classic` | `strict_current` | 24.462 | 1.338 | 18.287 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.356 | 0.970 | 6.553 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `ax` | `strict_current` | 6.356 | 1.361 | 4.668 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.181 | 0.970 | 25.962 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `classic` | `strict_current` | 25.181 | 1.361 | 18.496 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.343 | 0.855 | 7.419 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `ax` | `strict_current` | 6.343 | 1.394 | 4.551 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.105 | 0.855 | 29.362 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `classic` | `strict_current` | 25.105 | 1.394 | 18.011 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.192 | 0.976 | 7.367 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.192 | 1.366 | 5.265 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.620 | 0.976 | 26.242 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.620 | 1.366 | 18.753 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.496 | 1.214 | 5.352 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `ax` | `strict_current` | 6.496 | 1.115 | 5.825 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.289 | 1.214 | 21.658 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `classic` | `strict_current` | 26.289 | 1.115 | 23.574 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.864 | 1.079 | 6.359 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 6.864 | 1.233 | 5.567 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.259 | 1.079 | 23.401 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 25.259 | 1.233 | 20.488 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.334 | 0.974 | 6.504 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `ax` | `strict_current` | 6.334 | 1.121 | 5.650 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.902 | 0.974 | 26.598 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `classic` | `strict_current` | 25.902 | 1.121 | 23.105 |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.734 | 1.780 | 3.784 |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.734 | 4.602 | 1.463 |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 23.797 | 1.780 | 13.371 |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `classic` | `strict_current` | 23.797 | 4.602 | 5.171 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.660 | 1.843 | 3.070 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `ax` | `strict_current` | 5.660 | 4.735 | 1.195 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.334 | 1.843 | 12.658 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `classic` | `strict_current` | 23.334 | 4.735 | 4.928 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.567 | 1.748 | 3.757 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `ax` | `strict_current` | 6.567 | 2.969 | 2.212 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.949 | 1.748 | 13.702 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `classic` | `strict_current` | 23.949 | 2.969 | 8.066 |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.457 | 1.796 | 3.595 |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `ax` | `strict_current` | 6.457 | 2.878 | 2.243 |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.098 | 1.796 | 12.861 |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `classic` | `strict_current` | 23.098 | 2.878 | 8.026 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 17.157 | 0.865 | 19.834 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 17.157 | 1.057 | 16.227 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 27.291 | 0.865 | 31.549 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 27.291 | 1.057 | 25.812 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.817 | 0.879 | 7.754 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `ax` | `strict_current` | 6.817 | 1.012 | 6.736 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.191 | 0.879 | 27.515 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `classic` | `strict_current` | 24.191 | 1.012 | 23.904 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 18.461 | 0.895 | 20.628 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `ax` | `strict_current` | 18.461 | 1.096 | 16.840 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 29.124 | 0.895 | 32.543 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `classic` | `strict_current` | 29.124 | 1.096 | 26.567 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.870 | 0.951 | 7.221 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `ax` | `strict_current` | 6.870 | 1.000 | 6.873 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.232 | 0.951 | 25.469 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `classic` | `strict_current` | 24.232 | 1.000 | 24.241 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.505 | 0.839 | 7.749 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.505 | 1.667 | 3.902 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.229 | 0.839 | 28.865 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.229 | 1.667 | 14.535 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.852 | 0.810 | 8.457 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `ax` | `strict_current` | 6.852 | 1.666 | 4.113 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.125 | 0.810 | 31.009 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `classic` | `strict_current` | 25.125 | 1.666 | 15.081 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.747 | 1.045 | 6.458 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `ax` | `strict_current` | 6.747 | 1.797 | 3.755 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.337 | 1.045 | 23.293 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `classic` | `strict_current` | 24.337 | 1.797 | 13.544 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.417 | 0.869 | 7.388 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `ax` | `strict_current` | 6.417 | 1.751 | 3.665 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.442 | 0.869 | 28.139 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `classic` | `strict_current` | 24.442 | 1.751 | 13.960 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 14.905 | 1.159 | 12.861 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 14.905 | 1.351 | 11.035 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 13.446 | 1.159 | 11.602 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 13.446 | 1.351 | 9.955 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 16.020 | 1.146 | 13.980 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `ax` | `strict_current` | 16.020 | 1.363 | 11.754 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.571 | 1.146 | 12.716 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `classic` | `strict_current` | 14.571 | 1.363 | 10.691 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.870 | 1.139 | 5.152 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 5.870 | 1.308 | 4.489 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.625 | 1.139 | 11.960 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 13.625 | 1.308 | 10.420 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.015 | 1.178 | 5.955 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `ax` | `strict_current` | 7.015 | 1.344 | 5.219 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.839 | 1.178 | 12.598 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `classic` | `strict_current` | 14.839 | 1.344 | 11.041 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.809 | 0.880 | 7.735 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.809 | 1.134 | 6.005 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.299 | 0.880 | 28.738 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.299 | 1.134 | 22.310 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.564 | 0.932 | 7.042 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `ax` | `strict_current` | 6.564 | 1.142 | 5.747 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.789 | 0.932 | 28.742 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `classic` | `strict_current` | 26.789 | 1.142 | 23.455 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.797 | 0.854 | 7.954 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `ax` | `strict_current` | 6.797 | 0.990 | 6.867 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.110 | 0.854 | 28.216 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `classic` | `strict_current` | 24.110 | 0.990 | 24.360 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.355 | 0.849 | 7.481 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `ax` | `strict_current` | 6.355 | 1.154 | 5.508 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.732 | 0.849 | 29.116 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `classic` | `strict_current` | 24.732 | 1.154 | 21.434 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.171 | 0.963 | 6.408 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.171 | 1.088 | 5.669 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 14.052 | 0.963 | 14.592 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 14.052 | 1.088 | 12.910 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.343 | 0.982 | 6.458 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `ax` | `strict_current` | 6.343 | 1.122 | 5.651 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.030 | 0.982 | 14.284 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `classic` | `strict_current` | 14.030 | 1.122 | 12.499 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.521 | 0.898 | 7.258 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `ax` | `strict_current` | 6.521 | 1.104 | 5.908 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.195 | 0.898 | 15.799 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `classic` | `strict_current` | 14.195 | 1.104 | 12.861 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.519 | 0.875 | 7.453 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `ax` | `strict_current` | 6.519 | 1.092 | 5.971 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.511 | 0.875 | 17.732 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `classic` | `strict_current` | 15.511 | 1.092 | 14.206 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 4.160 | 16.043 | 0.259 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `ax` | `strict_current` | 4.160 | 32.846 | 0.127 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 17.129 | 16.043 | 1.068 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `classic` | `strict_current` | 17.129 | 32.846 | 0.521 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 4.477 | 15.773 | 0.284 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `ax` | `strict_current` | 4.477 | 33.215 | 0.135 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 16.576 | 15.773 | 1.051 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `classic` | `strict_current` | 16.576 | 33.215 | 0.499 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 4.242 | 16.176 | 0.262 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `ax` | `strict_current` | 4.242 | 34.066 | 0.125 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 17.487 | 16.176 | 1.081 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `classic` | `strict_current` | 17.487 | 34.066 | 0.513 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 4.717 | 15.979 | 0.295 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `ax` | `strict_current` | 4.717 | 33.741 | 0.140 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 16.437 | 15.979 | 1.029 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `classic` | `strict_current` | 16.437 | 33.741 | 0.487 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 11.659 | 8.738 | 1.334 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `ax` | `strict_current` | 11.659 | 67.461 | 0.173 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 17.969 | 8.738 | 2.056 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `classic` | `strict_current` | 17.969 | 67.461 | 0.266 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 4.540 | 8.461 | 0.537 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `ax` | `strict_current` | 4.540 | 67.624 | 0.067 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 16.504 | 8.461 | 1.951 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `classic` | `strict_current` | 16.504 | 67.624 | 0.244 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 4.540 | 8.473 | 0.536 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `ax` | `strict_current` | 4.540 | 69.275 | 0.066 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 16.921 | 8.473 | 1.997 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `classic` | `strict_current` | 16.921 | 69.275 | 0.244 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 11.302 | 8.504 | 1.329 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `ax` | `strict_current` | 11.302 | 69.511 | 0.163 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 17.297 | 8.504 | 2.034 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `classic` | `strict_current` | 17.297 | 69.511 | 0.249 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.628 | 0.798 | 9.562 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.628 | 1.145 | 6.662 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 14.734 | 0.798 | 18.469 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `classic` | `strict_current` | 14.734 | 1.145 | 12.868 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.286 | 0.974 | 6.453 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `ax` | `strict_current` | 6.286 | 1.362 | 4.616 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.865 | 0.974 | 15.260 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `classic` | `strict_current` | 14.865 | 1.362 | 10.916 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.644 | 1.092 | 6.085 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `ax` | `strict_current` | 6.644 | 1.337 | 4.969 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.408 | 1.092 | 14.112 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `classic` | `strict_current` | 15.408 | 1.337 | 11.522 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.408 | 0.827 | 7.750 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `ax` | `strict_current` | 6.408 | 1.153 | 5.560 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.523 | 0.827 | 17.564 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `classic` | `strict_current` | 14.523 | 1.153 | 12.600 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.067 | 2.092 | 2.900 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.067 | 9.251 | 0.656 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 37.128 | 2.092 | 17.746 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 37.128 | 9.251 | 4.013 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.779 | 3.184 | 1.815 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `ax` | `strict_current` | 5.779 | 9.413 | 0.614 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 35.039 | 3.184 | 11.005 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `classic` | `strict_current` | 35.039 | 9.413 | 3.722 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.792 | 2.175 | 2.663 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 5.792 | 9.517 | 0.609 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 40.046 | 2.175 | 18.412 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 40.046 | 9.517 | 4.208 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.217 | 2.202 | 2.824 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `ax` | `strict_current` | 6.217 | 9.348 | 0.665 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 41.152 | 2.202 | 18.691 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `classic` | `strict_current` | 41.152 | 9.348 | 4.402 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.263 | 0.737 | 8.497 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `ax` | `strict_current` | 6.263 | 0.797 | 7.859 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.701 | 0.737 | 34.868 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `classic` | `strict_current` | 25.701 | 0.797 | 32.252 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.337 | 0.743 | 8.526 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `ax` | `strict_current` | 6.337 | 1.038 | 6.107 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 22.586 | 0.743 | 30.388 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `classic` | `strict_current` | 22.586 | 1.038 | 21.768 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.662 | 0.854 | 7.798 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `ax` | `strict_current` | 6.662 | 0.795 | 8.380 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.148 | 0.854 | 29.437 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `classic` | `strict_current` | 25.148 | 0.795 | 31.633 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 16.566 | 1.037 | 15.974 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `ax` | `strict_current` | 16.566 | 1.176 | 14.091 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 26.888 | 1.037 | 25.928 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `classic` | `strict_current` | 26.888 | 1.176 | 22.871 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.768 | 1.133 | 5.974 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `ax` | `strict_current` | 6.768 | 1.144 | 5.916 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.596 | 1.133 | 22.592 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `classic` | `strict_current` | 25.596 | 1.144 | 22.371 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.318 | 1.151 | 5.491 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `ax` | `strict_current` | 6.318 | 1.294 | 4.881 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.556 | 1.151 | 21.344 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `classic` | `strict_current` | 24.556 | 1.294 | 18.970 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 16.962 | 1.045 | 16.228 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `ax` | `strict_current` | 16.962 | 1.192 | 14.234 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.101 | 1.045 | 24.014 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `classic` | `strict_current` | 25.101 | 1.192 | 21.064 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.639 | 0.848 | 7.829 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.639 | 0.972 | 6.832 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 26.798 | 0.848 | 31.601 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `classic` | `strict_current` | 26.798 | 0.972 | 27.579 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.768 | 0.915 | 9.581 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `ax` | `strict_current` | 8.768 | 1.049 | 8.358 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.784 | 0.915 | 29.266 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `classic` | `strict_current` | 26.784 | 1.049 | 25.532 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.144 | 0.778 | 7.900 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `ax` | `strict_current` | 6.144 | 1.202 | 5.109 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.876 | 0.778 | 31.986 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `classic` | `strict_current` | 24.876 | 1.202 | 20.688 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.806 | 0.835 | 8.153 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `ax` | `strict_current` | 6.806 | 1.114 | 6.111 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.405 | 0.835 | 29.234 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `classic` | `strict_current` | 24.405 | 1.114 | 21.913 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.067 | 1.033 | 5.872 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.067 | 1.098 | 5.525 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 14.744 | 1.033 | 14.269 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `classic` | `strict_current` | 14.744 | 1.098 | 13.428 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.692 | 1.041 | 6.429 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `ax` | `strict_current` | 6.692 | 1.047 | 6.390 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.595 | 1.041 | 14.021 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `classic` | `strict_current` | 14.595 | 1.047 | 13.936 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.585 | 0.991 | 6.642 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `ax` | `strict_current` | 6.585 | 1.080 | 6.097 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.789 | 0.991 | 13.908 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `classic` | `strict_current` | 13.789 | 1.080 | 12.767 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.576 | 0.843 | 7.799 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `ax` | `strict_current` | 6.576 | 1.116 | 5.894 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.835 | 0.843 | 16.408 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `classic` | `strict_current` | 13.835 | 1.116 | 12.399 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 17.094 | 0.928 | 18.422 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `ax` | `strict_current` | 17.094 | 1.563 | 10.936 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 26.677 | 0.928 | 28.748 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `classic` | `strict_current` | 26.677 | 1.563 | 17.067 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.448 | 0.977 | 6.598 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `ax` | `strict_current` | 6.448 | 1.490 | 4.328 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.670 | 0.977 | 25.241 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `classic` | `strict_current` | 24.670 | 1.490 | 16.557 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 14.610 | 1.006 | 14.526 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `ax` | `strict_current` | 14.610 | 1.502 | 9.728 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.959 | 1.006 | 25.811 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `classic` | `strict_current` | 25.959 | 1.502 | 17.285 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 16.262 | 0.920 | 17.673 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `ax` | `strict_current` | 16.262 | 1.640 | 9.916 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.141 | 0.920 | 28.409 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `classic` | `strict_current` | 26.141 | 1.640 | 15.940 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 14.678 | 0.833 | 17.614 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `ax` | `strict_current` | 14.678 | 1.075 | 13.649 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 14.101 | 0.833 | 16.922 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `classic` | `strict_current` | 14.101 | 1.075 | 13.113 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.126 | 0.776 | 9.179 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `ax` | `strict_current` | 7.126 | 0.948 | 7.518 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.694 | 0.776 | 18.928 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `classic` | `strict_current` | 14.694 | 0.948 | 15.503 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 16.656 | 0.912 | 18.260 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `ax` | `strict_current` | 16.656 | 0.823 | 20.229 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 17.338 | 0.912 | 19.008 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `classic` | `strict_current` | 17.338 | 0.823 | 21.058 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.854 | 0.787 | 8.712 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `ax` | `strict_current` | 6.854 | 0.877 | 7.815 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.505 | 0.787 | 18.436 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `classic` | `strict_current` | 14.505 | 0.877 | 16.538 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.264 | 1.155 | 5.424 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.264 | 2.272 | 2.757 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 23.984 | 1.155 | 20.766 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `classic` | `strict_current` | 23.984 | 2.272 | 10.554 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.570 | 1.204 | 5.457 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `ax` | `strict_current` | 6.570 | 2.107 | 3.118 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.135 | 1.204 | 20.047 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `classic` | `strict_current` | 24.135 | 2.107 | 11.453 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.690 | 1.202 | 5.568 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `ax` | `strict_current` | 6.690 | 2.257 | 2.964 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.505 | 1.202 | 21.226 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `classic` | `strict_current` | 25.505 | 2.257 | 11.300 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.296 | 1.230 | 5.117 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `ax` | `strict_current` | 6.296 | 2.092 | 3.009 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.251 | 1.230 | 19.711 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `classic` | `strict_current` | 24.251 | 2.092 | 11.591 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.575 | 1.078 | 6.099 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `ax` | `strict_current` | 6.575 | 0.975 | 6.745 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 29.498 | 1.078 | 27.364 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `classic` | `strict_current` | 29.498 | 0.975 | 30.261 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.180 | 1.021 | 6.054 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `ax` | `strict_current` | 6.180 | 0.954 | 6.475 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.205 | 1.021 | 24.693 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `classic` | `strict_current` | 25.205 | 0.954 | 26.408 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.985 | 1.037 | 6.739 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `ax` | `strict_current` | 6.985 | 0.889 | 7.856 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.966 | 1.037 | 13.474 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `classic` | `strict_current` | 13.966 | 0.889 | 15.708 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.571 | 1.065 | 6.167 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `ax` | `strict_current` | 6.571 | 1.013 | 6.485 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.685 | 1.065 | 13.783 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `classic` | `strict_current` | 14.685 | 1.013 | 14.494 |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.426 | 1.090 | 5.897 |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `ax` | `strict_current` | 6.426 | 1.000 | 6.427 |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.190 | 1.090 | 12.103 |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `classic` | `strict_current` | 13.190 | 1.000 | 13.190 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.929 | 1.042 | 6.648 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.929 | 0.999 | 6.934 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 14.088 | 1.042 | 13.516 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `classic` | `strict_current` | 14.088 | 0.999 | 14.098 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.688 | 0.916 | 8.389 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `ax` | `strict_current` | 7.688 | 0.944 | 8.141 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.604 | 0.916 | 14.844 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `classic` | `strict_current` | 13.604 | 0.944 | 14.406 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.815 | 0.984 | 6.924 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `ax` | `strict_current` | 6.815 | 1.241 | 5.492 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.735 | 0.984 | 13.956 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `classic` | `strict_current` | 13.735 | 1.241 | 11.070 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.985 | 0.914 | 7.641 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `ax` | `strict_current` | 6.985 | 0.910 | 7.672 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.076 | 0.914 | 16.492 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `classic` | `strict_current` | 15.076 | 0.910 | 16.560 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.794 | 0.862 | 7.883 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.794 | 1.470 | 4.622 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.919 | 0.862 | 28.913 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.919 | 1.470 | 16.952 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.630 | 0.882 | 7.521 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `ax` | `strict_current` | 6.630 | 1.439 | 4.607 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.810 | 0.882 | 28.145 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `classic` | `strict_current` | 24.810 | 1.439 | 17.239 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.521 | 0.898 | 7.262 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `ax` | `strict_current` | 6.521 | 1.353 | 4.821 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.361 | 0.898 | 27.132 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `classic` | `strict_current` | 24.361 | 1.353 | 18.011 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.322 | 0.903 | 7.003 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `ax` | `strict_current` | 6.322 | 1.487 | 4.250 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.072 | 0.903 | 27.773 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `classic` | `strict_current` | 25.072 | 1.487 | 16.856 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.683 | 1.781 | 3.753 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.683 | 2.315 | 2.887 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 22.296 | 1.781 | 12.522 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 22.296 | 2.315 | 9.632 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.162 | 1.102 | 6.499 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `ax` | `strict_current` | 7.162 | 3.030 | 2.364 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.747 | 1.102 | 21.550 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `classic` | `strict_current` | 23.747 | 3.030 | 7.839 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.818 | 1.334 | 5.113 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 6.818 | 3.110 | 2.192 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.553 | 1.334 | 17.663 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 23.553 | 3.110 | 7.574 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.251 | 1.155 | 5.412 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `ax` | `strict_current` | 6.251 | 2.889 | 2.164 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 22.204 | 1.155 | 19.222 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `classic` | `strict_current` | 22.204 | 2.889 | 7.685 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.674 | 0.910 | 7.335 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.674 | 1.602 | 4.167 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 27.324 | 0.910 | 30.028 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `classic` | `strict_current` | 27.324 | 1.602 | 17.061 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.795 | 0.905 | 7.510 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `ax` | `strict_current` | 6.795 | 1.656 | 4.102 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.118 | 0.905 | 27.757 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `classic` | `strict_current` | 25.118 | 1.656 | 15.164 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.426 | 0.974 | 7.622 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `ax` | `strict_current` | 7.426 | 1.660 | 4.474 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.757 | 0.974 | 25.411 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `classic` | `strict_current` | 24.757 | 1.660 | 14.916 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.011 | 0.804 | 8.718 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `ax` | `strict_current` | 7.011 | 1.659 | 4.227 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.403 | 0.804 | 30.344 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `classic` | `strict_current` | 24.403 | 1.659 | 14.713 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 16.149 | 0.808 | 19.993 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `ax` | `strict_current` | 16.149 | 0.869 | 18.581 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 28.967 | 0.808 | 35.861 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `classic` | `strict_current` | 28.967 | 0.869 | 33.327 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.772 | 0.745 | 9.084 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `ax` | `strict_current` | 6.772 | 0.851 | 7.955 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 28.214 | 0.745 | 37.847 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `classic` | `strict_current` | 28.214 | 0.851 | 33.144 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.166 | 0.860 | 9.490 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `ax` | `strict_current` | 8.166 | 0.841 | 9.704 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.260 | 0.860 | 30.520 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `classic` | `strict_current` | 26.260 | 0.841 | 31.209 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 19.177 | 0.824 | 23.269 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `ax` | `strict_current` | 19.177 | 0.998 | 19.216 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 28.477 | 0.824 | 34.553 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `classic` | `strict_current` | 28.477 | 0.998 | 28.535 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.028 | 0.788 | 8.916 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.028 | 0.808 | 8.698 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.424 | 0.788 | 30.985 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.424 | 0.808 | 30.228 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.677 | 0.784 | 8.520 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `ax` | `strict_current` | 6.677 | 0.979 | 6.823 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.592 | 0.784 | 33.934 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `classic` | `strict_current` | 26.592 | 0.979 | 27.174 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.345 | 0.742 | 9.896 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 7.345 | 0.887 | 8.283 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.472 | 0.742 | 34.319 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 25.472 | 0.887 | 28.726 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.764 | 0.750 | 9.017 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `ax` | `strict_current` | 6.764 | 0.882 | 7.668 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.118 | 0.750 | 34.817 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `classic` | `strict_current` | 26.118 | 0.882 | 29.609 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 15.056 | 0.853 | 17.641 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `ax` | `strict_current` | 15.056 | 1.192 | 12.633 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 14.552 | 0.853 | 17.050 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `classic` | `strict_current` | 14.552 | 1.192 | 12.210 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 15.221 | 0.911 | 16.717 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `ax` | `strict_current` | 15.221 | 1.274 | 11.950 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.334 | 0.911 | 15.743 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `classic` | `strict_current` | 14.334 | 1.274 | 11.254 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.184 | 0.887 | 6.973 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `ax` | `strict_current` | 6.184 | 1.209 | 5.114 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.446 | 0.887 | 17.416 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `classic` | `strict_current` | 15.446 | 1.209 | 12.773 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.846 | 0.873 | 7.842 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `ax` | `strict_current` | 6.846 | 1.282 | 5.342 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.858 | 0.873 | 15.874 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `classic` | `strict_current` | 13.858 | 1.282 | 10.813 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.260 | 0.882 | 7.095 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.260 | 0.960 | 6.521 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 27.556 | 0.882 | 31.232 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `classic` | `strict_current` | 27.556 | 0.960 | 28.709 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.147 | 0.877 | 7.011 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `ax` | `strict_current` | 6.147 | 0.914 | 6.724 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.490 | 0.877 | 27.931 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `classic` | `strict_current` | 24.490 | 0.914 | 26.788 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.956 | 0.909 | 6.550 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `ax` | `strict_current` | 5.956 | 0.947 | 6.289 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.620 | 0.909 | 28.174 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `classic` | `strict_current` | 25.620 | 0.947 | 27.051 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.586 | 0.844 | 7.807 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `ax` | `strict_current` | 6.586 | 0.991 | 6.644 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.536 | 0.844 | 30.270 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `classic` | `strict_current` | 25.536 | 0.991 | 25.762 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.580 | 1.045 | 6.298 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.580 | 1.051 | 6.263 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.504 | 1.045 | 24.412 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.504 | 1.051 | 24.277 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.009 | 1.048 | 5.735 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `ax` | `strict_current` | 6.009 | 1.110 | 5.413 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.360 | 1.048 | 24.200 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `classic` | `strict_current` | 25.360 | 1.110 | 22.844 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.887 | 1.267 | 6.225 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `ax` | `strict_current` | 7.887 | 1.374 | 5.742 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 28.399 | 1.267 | 22.415 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `classic` | `strict_current` | 28.399 | 1.374 | 20.675 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.291 | 1.117 | 6.525 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `ax` | `strict_current` | 7.291 | 1.095 | 6.659 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.109 | 1.117 | 23.366 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `classic` | `strict_current` | 26.109 | 1.095 | 23.844 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 17.778 | 1.232 | 14.431 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `ax` | `strict_current` | 17.778 | 1.163 | 15.286 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 15.652 | 1.232 | 12.705 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `classic` | `strict_current` | 15.652 | 1.163 | 13.457 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.540 | 1.277 | 5.121 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `ax` | `strict_current` | 6.540 | 0.974 | 6.712 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.533 | 1.277 | 12.162 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `classic` | `strict_current` | 15.533 | 0.974 | 15.942 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.505 | 1.052 | 7.135 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `ax` | `strict_current` | 7.505 | 1.078 | 6.960 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.933 | 1.052 | 15.147 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `classic` | `strict_current` | 15.933 | 1.078 | 14.776 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 14.823 | 1.213 | 12.220 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `ax` | `strict_current` | 14.823 | 1.074 | 13.802 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.192 | 1.213 | 11.699 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `classic` | `strict_current` | 14.192 | 1.074 | 13.213 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.322 | 0.828 | 7.633 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.322 | 1.340 | 4.719 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.406 | 0.828 | 30.675 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.406 | 1.340 | 18.966 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.126 | 0.813 | 8.760 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `ax` | `strict_current` | 7.126 | 1.318 | 5.407 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.367 | 0.813 | 29.955 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `classic` | `strict_current` | 24.367 | 1.318 | 18.489 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.417 | 0.805 | 7.967 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `ax` | `strict_current` | 6.417 | 1.462 | 4.390 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.797 | 0.805 | 30.786 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `classic` | `strict_current` | 24.797 | 1.462 | 16.963 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.973 | 0.982 | 7.102 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `ax` | `strict_current` | 6.973 | 1.424 | 4.897 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.453 | 0.982 | 25.923 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `classic` | `strict_current` | 25.453 | 1.424 | 17.874 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 5.901 | 1.771 | 3.333 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 5.901 | 4.302 | 1.372 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.465 | 1.771 | 13.817 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.465 | 4.302 | 5.687 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.203 | 1.787 | 3.471 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `ax` | `strict_current` | 6.203 | 4.362 | 1.422 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.481 | 1.787 | 13.140 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `classic` | `strict_current` | 23.481 | 4.362 | 5.383 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.198 | 1.807 | 3.430 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `ax` | `strict_current` | 6.198 | 4.218 | 1.470 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.420 | 1.807 | 12.961 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `classic` | `strict_current` | 23.420 | 4.218 | 5.553 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.520 | 1.929 | 3.380 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `ax` | `strict_current` | 6.520 | 4.272 | 1.526 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.528 | 1.929 | 12.196 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `classic` | `strict_current` | 23.528 | 4.272 | 5.507 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 15.946 | 0.892 | 17.884 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `ax` | `strict_current` | 15.946 | 1.109 | 14.379 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 26.381 | 0.892 | 29.587 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `classic` | `strict_current` | 26.381 | 1.109 | 23.788 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 16.362 | 0.833 | 19.644 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `ax` | `strict_current` | 16.362 | 1.001 | 16.348 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.080 | 0.833 | 32.511 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `classic` | `strict_current` | 27.080 | 1.001 | 27.057 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.149 | 0.869 | 7.077 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `ax` | `strict_current` | 6.149 | 0.998 | 6.159 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.184 | 0.869 | 27.834 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `classic` | `strict_current` | 24.184 | 0.998 | 24.222 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.706 | 0.780 | 8.599 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `ax` | `strict_current` | 6.706 | 1.217 | 5.509 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.500 | 0.780 | 32.700 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `classic` | `strict_current` | 25.500 | 1.217 | 20.950 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.327 | 1.755 | 3.604 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.327 | 3.324 | 1.903 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 23.654 | 1.755 | 13.475 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 23.654 | 3.324 | 7.115 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.432 | 1.723 | 3.734 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `ax` | `strict_current` | 6.432 | 3.156 | 2.038 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 22.927 | 1.723 | 13.310 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `classic` | `strict_current` | 22.927 | 3.156 | 7.265 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.631 | 2.055 | 3.227 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `ax` | `strict_current` | 6.631 | 2.957 | 2.243 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 22.628 | 2.055 | 11.011 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `classic` | `strict_current` | 22.628 | 2.957 | 7.653 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.648 | 1.662 | 3.399 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `ax` | `strict_current` | 5.648 | 3.259 | 1.733 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 22.764 | 1.662 | 13.700 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `classic` | `strict_current` | 22.764 | 3.259 | 6.985 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.333 | 1.341 | 5.468 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `ax` | `strict_current` | 7.333 | 8.686 | 0.844 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.021 | 1.341 | 24.622 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `classic` | `strict_current` | 33.021 | 8.686 | 3.802 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.747 | 1.473 | 4.581 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `ax` | `strict_current` | 6.747 | 8.784 | 0.768 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 31.572 | 1.473 | 21.437 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `classic` | `strict_current` | 31.572 | 8.784 | 3.594 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.198 | 0.944 | 6.563 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `ax` | `strict_current` | 6.198 | 1.720 | 3.603 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.023 | 0.944 | 25.437 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `classic` | `strict_current` | 24.023 | 1.720 | 13.966 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.170 | 0.883 | 6.984 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `ax` | `strict_current` | 6.170 | 1.765 | 3.495 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.927 | 0.883 | 27.084 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `classic` | `strict_current` | 23.927 | 1.765 | 13.556 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.036 | 3.410 | 1.770 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `ax` | `strict_current` | 6.036 | 3.565 | 1.693 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.693 | 3.410 | 6.948 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `classic` | `strict_current` | 23.693 | 3.565 | 6.645 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.085 | 3.291 | 1.849 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `ax` | `strict_current` | 6.085 | 3.478 | 1.750 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.359 | 3.291 | 7.098 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `classic` | `strict_current` | 23.359 | 3.478 | 6.717 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.360 | 0.844 | 7.539 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `ax` | `strict_current` | 6.360 | 1.372 | 4.634 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.180 | 0.844 | 29.849 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `classic` | `strict_current` | 25.180 | 1.372 | 18.349 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.197 | 0.805 | 7.697 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `ax` | `strict_current` | 6.197 | 1.301 | 4.762 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.349 | 0.805 | 30.245 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `classic` | `strict_current` | 24.349 | 1.301 | 18.712 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.700 | 1.153 | 5.813 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `ax` | `strict_current` | 6.700 | 1.160 | 5.776 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.954 | 1.153 | 23.386 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `classic` | `strict_current` | 26.954 | 1.160 | 23.235 |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.956 | 1.142 | 5.217 |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `ax` | `strict_current` | 5.956 | 1.044 | 5.703 |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.999 | 1.142 | 22.773 |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `classic` | `strict_current` | 25.999 | 1.044 | 24.896 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.276 | 0.880 | 7.136 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `ax` | `strict_current` | 6.276 | 1.590 | 3.948 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.052 | 0.880 | 30.757 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `classic` | `strict_current` | 27.052 | 1.590 | 17.015 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.509 | 0.847 | 7.684 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `ax` | `strict_current` | 6.509 | 1.908 | 3.411 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.498 | 0.847 | 30.101 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `classic` | `strict_current` | 25.498 | 1.908 | 13.361 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.603 | 1.694 | 4.489 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `ax` | `strict_current` | 7.603 | 1.889 | 4.024 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.489 | 1.694 | 15.641 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `classic` | `strict_current` | 26.489 | 1.889 | 14.021 |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.327 | 1.303 | 4.857 |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `ax` | `strict_current` | 6.327 | 1.523 | 4.154 |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.930 | 1.303 | 18.368 |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `classic` | `strict_current` | 23.930 | 1.523 | 15.711 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.504 | 11.978 | 0.543 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `ax` | `strict_current` | 6.504 | 11.934 | 0.545 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 37.547 | 11.978 | 3.135 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `classic` | `strict_current` | 37.547 | 11.934 | 3.146 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.694 | 12.187 | 0.549 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `ax` | `strict_current` | 6.694 | 12.549 | 0.533 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 37.168 | 12.187 | 3.050 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `classic` | `strict_current` | 37.168 | 12.549 | 2.962 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.347 | 1.551 | 4.092 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `ax` | `strict_current` | 6.347 | 2.648 | 2.397 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.909 | 1.551 | 16.058 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `classic` | `strict_current` | 24.909 | 2.648 | 9.407 |
| `vbr1_l2_event_controller` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.795 | 1.676 | 4.055 |
| `vbr1_l2_event_controller` | `tb` | `gold` | `ax` | `strict_current` | 6.795 | 2.675 | 2.541 |
| `vbr1_l2_event_controller` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.755 | 1.676 | 14.773 |
| `vbr1_l2_event_controller` | `tb` | `gold` | `classic` | `strict_current` | 24.755 | 2.675 | 9.255 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.509 | 0.890 | 6.192 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `ax` | `strict_current` | 5.509 | 1.751 | 3.146 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.830 | 0.890 | 27.912 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `classic` | `strict_current` | 24.830 | 1.751 | 14.183 |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.455 | 0.996 | 6.483 |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `ax` | `strict_current` | 6.455 | 1.589 | 4.064 |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.646 | 0.996 | 24.752 |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `classic` | `strict_current` | 24.646 | 1.589 | 15.515 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.055 | 9.460 | 1.063 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `ax` | `strict_current` | 10.055 | 125.358 | 0.080 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 44.051 | 9.460 | 4.657 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `classic` | `strict_current` | 44.051 | 125.358 | 0.351 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.738 | 32.699 | 0.328 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `ax` | `strict_current` | 10.738 | 153.215 | 0.070 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 48.801 | 32.699 | 1.492 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `classic` | `strict_current` | 48.801 | 153.215 | 0.319 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.496 | 1.676 | 3.875 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `ax` | `strict_current` | 6.496 | 2.498 | 2.601 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.178 | 1.676 | 15.617 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `classic` | `strict_current` | 26.178 | 2.498 | 10.481 |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.577 | 1.685 | 3.904 |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `ax` | `strict_current` | 6.577 | 2.608 | 2.522 |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.130 | 1.685 | 14.322 |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `classic` | `strict_current` | 24.130 | 2.608 | 9.253 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.181 | 10.313 | 0.599 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `ax` | `strict_current` | 6.181 | 10.523 | 0.587 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 21.078 | 10.313 | 2.044 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `classic` | `strict_current` | 21.078 | 10.523 | 2.003 |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.673 | 10.148 | 0.559 |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `ax` | `strict_current` | 5.673 | 10.517 | 0.539 |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 21.603 | 10.148 | 2.129 |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `classic` | `strict_current` | 21.603 | 10.517 | 2.054 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.418 | 1.178 | 5.447 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `ax` | `strict_current` | 6.418 | 2.066 | 3.106 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.057 | 1.178 | 21.268 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `classic` | `strict_current` | 25.057 | 2.066 | 12.128 |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.446 | 1.252 | 5.148 |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `ax` | `strict_current` | 6.446 | 2.078 | 3.102 |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.155 | 1.252 | 19.291 |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `classic` | `strict_current` | 24.155 | 2.078 | 11.625 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.631 | 1.443 | 4.596 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `ax` | `strict_current` | 6.631 | 17.134 | 0.387 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 43.836 | 1.443 | 30.382 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `classic` | `strict_current` | 43.836 | 17.134 | 2.558 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.288 | 2.594 | 2.424 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `ax` | `strict_current` | 6.288 | 17.381 | 0.362 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 40.734 | 2.594 | 15.705 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `classic` | `strict_current` | 40.734 | 17.381 | 2.344 |

## Accuracy-Gated Speedups

| Entry | Form | Variant | Spectre mode | EVAS mode | Spectre wall s | EVAS wall s | Spectre/EVAS |
| --- | --- | --- | --- | --- | ---: | ---: | ---: |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.307 | 1.310 | 4.813 |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.307 | 1.240 | 5.087 |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.133 | 1.310 | 19.180 |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.133 | 1.240 | 20.270 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.667 | 1.114 | 5.983 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `ax` | `strict_current` | 6.667 | 1.376 | 4.844 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.695 | 1.114 | 22.163 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `classic` | `strict_current` | 24.695 | 1.376 | 17.945 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.141 | 1.253 | 4.902 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `ax` | `strict_current` | 6.141 | 1.312 | 4.681 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.441 | 1.253 | 19.509 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `classic` | `strict_current` | 24.441 | 1.312 | 18.632 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.850 | 1.195 | 6.567 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `ax` | `strict_current` | 7.850 | 1.749 | 4.489 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.201 | 1.195 | 22.754 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `classic` | `strict_current` | 27.201 | 1.749 | 15.552 |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.249 | 1.627 | 3.841 |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.249 | 10.404 | 0.601 |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 23.138 | 1.627 | 14.223 |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 23.138 | 10.404 | 2.224 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.467 | 1.424 | 4.542 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `ax` | `strict_current` | 6.467 | 10.449 | 0.619 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 22.285 | 1.424 | 15.653 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `classic` | `strict_current` | 22.285 | 10.449 | 2.133 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.259 | 1.648 | 3.797 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `ax` | `strict_current` | 6.259 | 1.989 | 3.146 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.520 | 1.648 | 14.875 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `classic` | `strict_current` | 24.520 | 1.989 | 12.326 |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.056 | 1.829 | 3.858 |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `ax` | `strict_current` | 7.056 | 1.951 | 3.616 |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.567 | 1.829 | 13.432 |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `classic` | `strict_current` | 24.567 | 1.951 | 12.590 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 16.484 | 1.034 | 15.944 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `ax` | `strict_current` | 16.484 | 1.182 | 13.946 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 27.733 | 1.034 | 26.825 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `classic` | `strict_current` | 27.733 | 1.182 | 23.464 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 17.526 | 1.068 | 16.410 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `ax` | `strict_current` | 17.526 | 0.908 | 19.300 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.738 | 1.068 | 25.971 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `classic` | `strict_current` | 27.738 | 0.908 | 30.546 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 18.523 | 0.994 | 18.633 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `ax` | `strict_current` | 18.523 | 1.036 | 17.881 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 29.571 | 0.994 | 29.746 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `classic` | `strict_current` | 29.571 | 1.036 | 28.546 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.717 | 0.836 | 8.031 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `ax` | `strict_current` | 6.717 | 0.999 | 6.721 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.577 | 0.836 | 30.580 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `classic` | `strict_current` | 25.577 | 0.999 | 25.593 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.221 | 0.917 | 6.786 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `ax` | `strict_current` | 6.221 | 1.378 | 4.514 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.159 | 0.917 | 27.444 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `classic` | `strict_current` | 25.159 | 1.378 | 18.257 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.692 | 1.024 | 6.537 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `ax` | `strict_current` | 6.692 | 1.360 | 4.921 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.215 | 1.024 | 24.629 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `classic` | `strict_current` | 25.215 | 1.360 | 18.542 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.535 | 0.953 | 6.859 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `ax` | `strict_current` | 6.535 | 1.487 | 4.396 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.087 | 0.953 | 27.379 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `classic` | `strict_current` | 26.087 | 1.487 | 17.548 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.642 | 0.877 | 7.577 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.642 | 1.781 | 3.728 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.709 | 0.877 | 29.330 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.709 | 1.781 | 14.431 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.505 | 0.874 | 7.447 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `ax` | `strict_current` | 6.505 | 1.629 | 3.993 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.216 | 0.874 | 28.868 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `classic` | `strict_current` | 25.216 | 1.629 | 15.478 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.609 | 0.800 | 8.266 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `ax` | `strict_current` | 6.609 | 1.687 | 3.918 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.210 | 0.800 | 31.532 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `classic` | `strict_current` | 25.210 | 1.687 | 14.947 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.456 | 0.888 | 7.270 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `ax` | `strict_current` | 6.456 | 1.717 | 3.760 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.849 | 0.888 | 26.855 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `classic` | `strict_current` | 23.849 | 1.717 | 13.889 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.389 | 1.776 | 3.598 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.389 | 3.510 | 1.820 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.235 | 1.776 | 13.646 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.235 | 3.510 | 6.904 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.740 | 1.781 | 3.222 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `ax` | `strict_current` | 5.740 | 3.488 | 1.646 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.075 | 1.781 | 13.515 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `classic` | `strict_current` | 24.075 | 3.488 | 6.903 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.120 | 1.739 | 3.519 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `ax` | `strict_current` | 6.120 | 3.500 | 1.748 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.029 | 1.739 | 13.818 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `classic` | `strict_current` | 24.029 | 3.500 | 6.866 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.276 | 1.812 | 3.464 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `ax` | `strict_current` | 6.276 | 3.509 | 1.789 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.940 | 1.812 | 13.212 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `classic` | `strict_current` | 23.940 | 3.509 | 6.822 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.815 | 0.934 | 7.293 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.815 | 1.748 | 3.900 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.200 | 0.934 | 25.897 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.200 | 1.748 | 13.848 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.250 | 0.859 | 7.276 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `ax` | `strict_current` | 6.250 | 1.618 | 3.864 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.100 | 0.859 | 29.218 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `classic` | `strict_current` | 25.100 | 1.618 | 15.517 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.356 | 0.772 | 8.233 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `ax` | `strict_current` | 6.356 | 1.710 | 3.718 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.524 | 0.772 | 34.357 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `classic` | `strict_current` | 26.524 | 1.710 | 15.513 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.327 | 0.877 | 7.213 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `ax` | `strict_current` | 6.327 | 1.599 | 3.956 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.156 | 0.877 | 28.682 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `classic` | `strict_current` | 25.156 | 1.599 | 15.730 |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.443 | 1.433 | 4.496 |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.443 | 4.071 | 1.583 |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 23.160 | 1.433 | 16.161 |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `classic` | `strict_current` | 23.160 | 4.071 | 5.689 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.396 | 1.474 | 4.338 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `ax` | `strict_current` | 6.396 | 4.045 | 1.581 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.199 | 1.474 | 16.413 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `classic` | `strict_current` | 24.199 | 4.045 | 5.983 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.578 | 1.815 | 3.625 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `ax` | `strict_current` | 6.578 | 4.274 | 1.539 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.260 | 1.815 | 13.368 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `classic` | `strict_current` | 24.260 | 4.274 | 5.676 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.833 | 1.609 | 3.624 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `ax` | `strict_current` | 5.833 | 4.156 | 1.403 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.361 | 1.609 | 14.516 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `classic` | `strict_current` | 23.361 | 4.156 | 5.621 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.469 | 1.002 | 6.458 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.469 | 1.639 | 3.948 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.244 | 1.002 | 25.199 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.244 | 1.639 | 15.404 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.577 | 0.879 | 7.483 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `ax` | `strict_current` | 6.577 | 1.625 | 4.047 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.831 | 0.879 | 28.248 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `classic` | `strict_current` | 24.831 | 1.625 | 15.278 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.322 | 1.006 | 6.287 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `ax` | `strict_current` | 6.322 | 1.641 | 3.853 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.760 | 1.006 | 24.622 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `classic` | `strict_current` | 24.760 | 1.641 | 15.090 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.682 | 0.936 | 7.142 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `ax` | `strict_current` | 6.682 | 1.727 | 3.869 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.316 | 0.936 | 27.059 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `classic` | `strict_current` | 25.316 | 1.727 | 14.659 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 5.900 | 1.179 | 5.006 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 5.900 | 3.237 | 1.823 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 23.960 | 1.179 | 20.328 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 23.960 | 3.237 | 7.402 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.490 | 1.118 | 5.806 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `ax` | `strict_current` | 6.490 | 3.209 | 2.022 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.923 | 1.118 | 21.405 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `classic` | `strict_current` | 23.923 | 3.209 | 7.456 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.195 | 1.212 | 5.112 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 6.195 | 3.128 | 1.981 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.546 | 1.212 | 19.430 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 23.546 | 3.128 | 7.528 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.638 | 1.284 | 4.391 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `ax` | `strict_current` | 5.638 | 3.100 | 1.819 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.260 | 1.284 | 18.113 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `classic` | `strict_current` | 23.260 | 3.100 | 7.502 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.979 | 0.993 | 7.026 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.979 | 1.584 | 4.406 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 14.603 | 0.993 | 14.701 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `classic` | `strict_current` | 14.603 | 1.584 | 9.220 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.520 | 0.839 | 7.769 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `ax` | `strict_current` | 6.520 | 1.463 | 4.456 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.871 | 0.839 | 16.529 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `classic` | `strict_current` | 13.871 | 1.463 | 9.481 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.279 | 0.887 | 7.080 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `ax` | `strict_current` | 6.279 | 1.561 | 4.022 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.232 | 0.887 | 14.919 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `classic` | `strict_current` | 13.232 | 1.561 | 8.476 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.629 | 0.963 | 6.883 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `ax` | `strict_current` | 6.629 | 1.515 | 4.375 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.149 | 0.963 | 13.653 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `classic` | `strict_current` | 13.149 | 1.515 | 8.678 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.619 | 1.050 | 8.210 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `ax` | `strict_current` | 8.619 | 0.806 | 10.697 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 16.250 | 1.050 | 15.480 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `classic` | `strict_current` | 16.250 | 0.806 | 20.169 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.284 | 0.770 | 8.163 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `ax` | `strict_current` | 6.284 | 0.865 | 7.268 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.366 | 0.770 | 18.662 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `classic` | `strict_current` | 14.366 | 0.865 | 16.616 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.960 | 0.793 | 8.778 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `ax` | `strict_current` | 6.960 | 0.873 | 7.970 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.092 | 0.793 | 19.035 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `classic` | `strict_current` | 15.092 | 0.873 | 17.283 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.154 | 0.783 | 7.862 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.154 | 0.766 | 8.036 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 26.217 | 0.783 | 33.491 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `classic` | `strict_current` | 26.217 | 0.766 | 34.234 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.369 | 0.752 | 8.475 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `ax` | `strict_current` | 6.369 | 0.812 | 7.840 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.495 | 0.752 | 35.256 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `classic` | `strict_current` | 26.495 | 0.812 | 32.612 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.392 | 0.824 | 8.976 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `ax` | `strict_current` | 7.392 | 0.862 | 8.575 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.395 | 0.824 | 32.052 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `classic` | `strict_current` | 26.395 | 0.862 | 30.620 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.977 | 0.769 | 9.075 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `ax` | `strict_current` | 6.977 | 0.936 | 7.452 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.352 | 0.769 | 34.277 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `classic` | `strict_current` | 26.352 | 0.936 | 28.144 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 17.520 | 0.767 | 22.828 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `ax` | `strict_current` | 17.520 | 0.992 | 17.654 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 27.652 | 0.767 | 36.030 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `classic` | `strict_current` | 27.652 | 0.992 | 27.864 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.205 | 0.877 | 7.075 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `ax` | `strict_current` | 6.205 | 1.018 | 6.096 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.620 | 0.877 | 31.489 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `classic` | `strict_current` | 27.620 | 1.018 | 27.132 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.474 | 1.003 | 6.457 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `ax` | `strict_current` | 6.474 | 0.997 | 6.490 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.530 | 1.003 | 24.466 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `classic` | `strict_current` | 24.530 | 0.997 | 24.592 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 15.523 | 0.764 | 20.328 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `ax` | `strict_current` | 15.523 | 0.951 | 16.318 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.389 | 0.764 | 33.248 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `classic` | `strict_current` | 25.389 | 0.951 | 26.690 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 5.779 | 0.965 | 5.989 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `ax` | `strict_current` | 5.779 | 4.626 | 1.249 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.686 | 0.965 | 25.584 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.686 | 4.626 | 5.337 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.554 | 1.052 | 6.229 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `ax` | `strict_current` | 6.554 | 4.806 | 1.364 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.274 | 1.052 | 23.068 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `classic` | `strict_current` | 24.274 | 4.806 | 5.051 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.961 | 1.122 | 5.312 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `ax` | `strict_current` | 5.961 | 4.526 | 1.317 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.612 | 1.122 | 21.932 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `classic` | `strict_current` | 24.612 | 4.526 | 5.438 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.263 | 1.074 | 5.832 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `ax` | `strict_current` | 6.263 | 4.671 | 1.341 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.005 | 1.074 | 22.354 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `classic` | `strict_current` | 24.005 | 4.671 | 5.139 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.198 | 1.624 | 3.816 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.198 | 1.843 | 3.363 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.289 | 1.624 | 15.570 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.289 | 1.843 | 13.722 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.658 | 1.685 | 3.952 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `ax` | `strict_current` | 6.658 | 1.739 | 3.829 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.390 | 1.685 | 14.479 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `classic` | `strict_current` | 24.390 | 1.739 | 14.028 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.400 | 1.492 | 4.289 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `ax` | `strict_current` | 6.400 | 1.660 | 3.855 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.665 | 1.492 | 16.529 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `classic` | `strict_current` | 24.665 | 1.660 | 14.854 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.281 | 1.699 | 4.284 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `ax` | `strict_current` | 7.281 | 1.571 | 4.635 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.919 | 1.699 | 14.663 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `classic` | `strict_current` | 24.919 | 1.571 | 15.862 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.359 | 0.848 | 7.498 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `ax` | `strict_current` | 6.359 | 0.899 | 7.073 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 10.743 | 0.848 | 12.668 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `classic` | `strict_current` | 10.743 | 0.899 | 11.950 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.204 | 0.889 | 6.981 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `ax` | `strict_current` | 6.204 | 0.761 | 8.155 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.064 | 0.889 | 15.824 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `classic` | `strict_current` | 14.064 | 0.761 | 18.486 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.342 | 0.884 | 7.171 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `ax` | `strict_current` | 6.342 | 0.857 | 7.401 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 12.538 | 0.884 | 14.176 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `classic` | `strict_current` | 12.538 | 0.857 | 14.633 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.591 | 0.816 | 8.077 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.591 | 2.811 | 2.344 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 45.582 | 0.816 | 55.859 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `classic` | `strict_current` | 45.582 | 2.811 | 16.213 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.847 | 0.865 | 7.912 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `ax` | `strict_current` | 6.847 | 2.667 | 2.567 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 45.947 | 0.865 | 53.091 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `classic` | `strict_current` | 45.947 | 2.667 | 17.225 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.504 | 0.940 | 7.985 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `ax` | `strict_current` | 7.504 | 2.651 | 2.830 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 45.508 | 0.940 | 48.421 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `classic` | `strict_current` | 45.508 | 2.651 | 17.164 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.087 | 0.796 | 8.903 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `ax` | `strict_current` | 7.087 | 2.640 | 2.685 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 45.335 | 0.796 | 56.951 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `classic` | `strict_current` | 45.335 | 2.640 | 17.174 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 16.186 | 1.048 | 15.446 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 16.186 | 0.980 | 16.517 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 26.623 | 1.048 | 25.406 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 26.623 | 0.980 | 27.167 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.408 | 0.959 | 7.722 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `ax` | `strict_current` | 7.408 | 0.952 | 7.780 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.467 | 0.959 | 28.631 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `classic` | `strict_current` | 27.467 | 0.952 | 28.846 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.019 | 0.905 | 7.758 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `ax` | `strict_current` | 7.019 | 1.035 | 6.781 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.905 | 0.905 | 27.528 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `classic` | `strict_current` | 24.905 | 1.035 | 24.060 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 17.693 | 0.974 | 18.169 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `ax` | `strict_current` | 17.693 | 1.096 | 16.142 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.886 | 0.974 | 28.635 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `classic` | `strict_current` | 27.886 | 1.096 | 25.441 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.253 | 1.388 | 4.505 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `ax` | `strict_current` | 6.253 | 4.662 | 1.341 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.609 | 1.388 | 17.731 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `classic` | `strict_current` | 24.609 | 4.662 | 5.279 |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.002 | 1.262 | 4.756 |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `ax` | `strict_current` | 6.002 | 4.594 | 1.307 |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 22.147 | 1.262 | 17.547 |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `classic` | `strict_current` | 22.147 | 4.594 | 4.821 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.137 | 0.788 | 7.785 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.137 | 1.102 | 5.568 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.578 | 0.788 | 32.449 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.578 | 1.102 | 23.210 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.358 | 0.980 | 7.510 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `ax` | `strict_current` | 7.358 | 1.277 | 5.762 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.937 | 0.980 | 26.470 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `classic` | `strict_current` | 25.937 | 1.277 | 20.308 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.026 | 0.792 | 7.608 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `ax` | `strict_current` | 6.026 | 1.022 | 5.895 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.712 | 0.792 | 31.200 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `classic` | `strict_current` | 24.712 | 1.022 | 24.174 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.166 | 0.805 | 8.901 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `ax` | `strict_current` | 7.166 | 1.008 | 7.109 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.956 | 0.805 | 32.241 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `classic` | `strict_current` | 25.956 | 1.008 | 25.749 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.815 | 0.774 | 8.809 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.815 | 0.881 | 7.740 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.785 | 0.774 | 32.035 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.785 | 0.881 | 28.147 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.044 | 0.737 | 8.202 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `ax` | `strict_current` | 6.044 | 0.931 | 6.493 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.321 | 0.737 | 34.365 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `classic` | `strict_current` | 25.321 | 0.931 | 27.203 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.752 | 0.803 | 8.407 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `ax` | `strict_current` | 6.752 | 0.934 | 7.226 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.430 | 0.803 | 30.420 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `classic` | `strict_current` | 24.430 | 0.934 | 26.146 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.559 | 0.917 | 7.149 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `ax` | `strict_current` | 6.559 | 1.008 | 6.505 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.739 | 0.917 | 28.057 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `classic` | `strict_current` | 25.739 | 1.008 | 25.529 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 15.361 | 1.017 | 15.105 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `ax` | `strict_current` | 15.361 | 1.072 | 14.328 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 13.815 | 1.017 | 13.585 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `classic` | `strict_current` | 13.815 | 1.072 | 12.886 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.442 | 1.161 | 5.550 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `ax` | `strict_current` | 6.442 | 1.154 | 5.583 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.089 | 1.161 | 11.276 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `classic` | `strict_current` | 13.089 | 1.154 | 11.342 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 16.258 | 1.122 | 14.489 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `ax` | `strict_current` | 16.258 | 1.165 | 13.958 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.581 | 1.122 | 12.994 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `classic` | `strict_current` | 14.581 | 1.165 | 12.518 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.997 | 1.184 | 5.908 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `ax` | `strict_current` | 6.997 | 1.087 | 6.437 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.126 | 1.184 | 11.927 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `classic` | `strict_current` | 14.126 | 1.087 | 12.995 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.748 | 9.561 | 1.124 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `ax` | `strict_current` | 10.748 | 131.563 | 0.082 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 49.707 | 9.561 | 5.199 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `classic` | `strict_current` | 49.707 | 131.563 | 0.378 |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.892 | 33.266 | 0.327 |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `ax` | `strict_current` | 10.892 | 152.925 | 0.071 |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 47.749 | 33.266 | 1.435 |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `classic` | `strict_current` | 47.749 | 152.925 | 0.312 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 14.865 | 1.173 | 12.675 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `ax` | `strict_current` | 14.865 | 1.759 | 8.451 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 13.691 | 1.173 | 11.674 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `classic` | `strict_current` | 13.691 | 1.759 | 7.783 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 14.929 | 1.131 | 13.197 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `ax` | `strict_current` | 14.929 | 1.625 | 9.185 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.883 | 1.131 | 13.156 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `classic` | `strict_current` | 14.883 | 1.625 | 9.156 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.321 | 1.110 | 5.693 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `ax` | `strict_current` | 6.321 | 1.612 | 3.921 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.806 | 1.110 | 12.435 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `classic` | `strict_current` | 13.806 | 1.612 | 8.565 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.106 | 1.138 | 6.244 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `ax` | `strict_current` | 7.106 | 1.641 | 4.330 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.268 | 1.138 | 11.658 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `classic` | `strict_current` | 13.268 | 1.641 | 8.086 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.992 | 1.035 | 6.756 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.992 | 1.302 | 5.369 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.109 | 1.035 | 24.261 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.109 | 1.302 | 19.281 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.459 | 0.883 | 7.318 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `ax` | `strict_current` | 6.459 | 1.338 | 4.828 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.462 | 0.883 | 27.717 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `classic` | `strict_current` | 24.462 | 1.338 | 18.287 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.356 | 0.970 | 6.553 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `ax` | `strict_current` | 6.356 | 1.361 | 4.668 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.181 | 0.970 | 25.962 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `classic` | `strict_current` | 25.181 | 1.361 | 18.496 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.343 | 0.855 | 7.419 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `ax` | `strict_current` | 6.343 | 1.394 | 4.551 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.105 | 0.855 | 29.362 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `classic` | `strict_current` | 25.105 | 1.394 | 18.011 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.192 | 0.976 | 7.367 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.192 | 1.366 | 5.265 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.620 | 0.976 | 26.242 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.620 | 1.366 | 18.753 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.496 | 1.214 | 5.352 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `ax` | `strict_current` | 6.496 | 1.115 | 5.825 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.289 | 1.214 | 21.658 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `classic` | `strict_current` | 26.289 | 1.115 | 23.574 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.864 | 1.079 | 6.359 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 6.864 | 1.233 | 5.567 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.259 | 1.079 | 23.401 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 25.259 | 1.233 | 20.488 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.334 | 0.974 | 6.504 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `ax` | `strict_current` | 6.334 | 1.121 | 5.650 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.902 | 0.974 | 26.598 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `classic` | `strict_current` | 25.902 | 1.121 | 23.105 |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.734 | 1.780 | 3.784 |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.734 | 4.602 | 1.463 |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 23.797 | 1.780 | 13.371 |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `classic` | `strict_current` | 23.797 | 4.602 | 5.171 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.660 | 1.843 | 3.070 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `ax` | `strict_current` | 5.660 | 4.735 | 1.195 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.334 | 1.843 | 12.658 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `classic` | `strict_current` | 23.334 | 4.735 | 4.928 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.567 | 1.748 | 3.757 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `ax` | `strict_current` | 6.567 | 2.969 | 2.212 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.949 | 1.748 | 13.702 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `classic` | `strict_current` | 23.949 | 2.969 | 8.066 |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.457 | 1.796 | 3.595 |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `ax` | `strict_current` | 6.457 | 2.878 | 2.243 |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.098 | 1.796 | 12.861 |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `classic` | `strict_current` | 23.098 | 2.878 | 8.026 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 17.157 | 0.865 | 19.834 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 17.157 | 1.057 | 16.227 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 27.291 | 0.865 | 31.549 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 27.291 | 1.057 | 25.812 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.817 | 0.879 | 7.754 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `ax` | `strict_current` | 6.817 | 1.012 | 6.736 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.191 | 0.879 | 27.515 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `classic` | `strict_current` | 24.191 | 1.012 | 23.904 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 18.461 | 0.895 | 20.628 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `ax` | `strict_current` | 18.461 | 1.096 | 16.840 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 29.124 | 0.895 | 32.543 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `classic` | `strict_current` | 29.124 | 1.096 | 26.567 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.870 | 0.951 | 7.221 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `ax` | `strict_current` | 6.870 | 1.000 | 6.873 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.232 | 0.951 | 25.469 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `classic` | `strict_current` | 24.232 | 1.000 | 24.241 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.505 | 0.839 | 7.749 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.505 | 1.667 | 3.902 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.229 | 0.839 | 28.865 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.229 | 1.667 | 14.535 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.852 | 0.810 | 8.457 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `ax` | `strict_current` | 6.852 | 1.666 | 4.113 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.125 | 0.810 | 31.009 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `classic` | `strict_current` | 25.125 | 1.666 | 15.081 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.747 | 1.045 | 6.458 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `ax` | `strict_current` | 6.747 | 1.797 | 3.755 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.337 | 1.045 | 23.293 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `classic` | `strict_current` | 24.337 | 1.797 | 13.544 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.417 | 0.869 | 7.388 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `ax` | `strict_current` | 6.417 | 1.751 | 3.665 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.442 | 0.869 | 28.139 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `classic` | `strict_current` | 24.442 | 1.751 | 13.960 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 14.905 | 1.159 | 12.861 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 14.905 | 1.351 | 11.035 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 13.446 | 1.159 | 11.602 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 13.446 | 1.351 | 9.955 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 16.020 | 1.146 | 13.980 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `ax` | `strict_current` | 16.020 | 1.363 | 11.754 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.571 | 1.146 | 12.716 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `classic` | `strict_current` | 14.571 | 1.363 | 10.691 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.870 | 1.139 | 5.152 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 5.870 | 1.308 | 4.489 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.625 | 1.139 | 11.960 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 13.625 | 1.308 | 10.420 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.015 | 1.178 | 5.955 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `ax` | `strict_current` | 7.015 | 1.344 | 5.219 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.839 | 1.178 | 12.598 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `classic` | `strict_current` | 14.839 | 1.344 | 11.041 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.809 | 0.880 | 7.735 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.809 | 1.134 | 6.005 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.299 | 0.880 | 28.738 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.299 | 1.134 | 22.310 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.564 | 0.932 | 7.042 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `ax` | `strict_current` | 6.564 | 1.142 | 5.747 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.789 | 0.932 | 28.742 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `classic` | `strict_current` | 26.789 | 1.142 | 23.455 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.797 | 0.854 | 7.954 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `ax` | `strict_current` | 6.797 | 0.990 | 6.867 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.110 | 0.854 | 28.216 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `classic` | `strict_current` | 24.110 | 0.990 | 24.360 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.355 | 0.849 | 7.481 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `ax` | `strict_current` | 6.355 | 1.154 | 5.508 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.732 | 0.849 | 29.116 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `classic` | `strict_current` | 24.732 | 1.154 | 21.434 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.171 | 0.963 | 6.408 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.171 | 1.088 | 5.669 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 14.052 | 0.963 | 14.592 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 14.052 | 1.088 | 12.910 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.343 | 0.982 | 6.458 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `ax` | `strict_current` | 6.343 | 1.122 | 5.651 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.030 | 0.982 | 14.284 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `classic` | `strict_current` | 14.030 | 1.122 | 12.499 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.521 | 0.898 | 7.258 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `ax` | `strict_current` | 6.521 | 1.104 | 5.908 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.195 | 0.898 | 15.799 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `classic` | `strict_current` | 14.195 | 1.104 | 12.861 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.519 | 0.875 | 7.453 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `ax` | `strict_current` | 6.519 | 1.092 | 5.971 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.511 | 0.875 | 17.732 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `classic` | `strict_current` | 15.511 | 1.092 | 14.206 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 4.160 | 16.043 | 0.259 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `ax` | `strict_current` | 4.160 | 32.846 | 0.127 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 17.129 | 16.043 | 1.068 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `classic` | `strict_current` | 17.129 | 32.846 | 0.521 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 4.477 | 15.773 | 0.284 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `ax` | `strict_current` | 4.477 | 33.215 | 0.135 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 16.576 | 15.773 | 1.051 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `classic` | `strict_current` | 16.576 | 33.215 | 0.499 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 4.242 | 16.176 | 0.262 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `ax` | `strict_current` | 4.242 | 34.066 | 0.125 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 17.487 | 16.176 | 1.081 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `classic` | `strict_current` | 17.487 | 34.066 | 0.513 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 4.717 | 15.979 | 0.295 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `ax` | `strict_current` | 4.717 | 33.741 | 0.140 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 16.437 | 15.979 | 1.029 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `classic` | `strict_current` | 16.437 | 33.741 | 0.487 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 11.659 | 8.738 | 1.334 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `ax` | `strict_current` | 11.659 | 67.461 | 0.173 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 17.969 | 8.738 | 2.056 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `classic` | `strict_current` | 17.969 | 67.461 | 0.266 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 4.540 | 8.461 | 0.537 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `ax` | `strict_current` | 4.540 | 67.624 | 0.067 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 16.504 | 8.461 | 1.951 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `classic` | `strict_current` | 16.504 | 67.624 | 0.244 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 4.540 | 8.473 | 0.536 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `ax` | `strict_current` | 4.540 | 69.275 | 0.066 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 16.921 | 8.473 | 1.997 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `classic` | `strict_current` | 16.921 | 69.275 | 0.244 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 11.302 | 8.504 | 1.329 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `ax` | `strict_current` | 11.302 | 69.511 | 0.163 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 17.297 | 8.504 | 2.034 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `classic` | `strict_current` | 17.297 | 69.511 | 0.249 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.628 | 0.798 | 9.562 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.628 | 1.145 | 6.662 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 14.734 | 0.798 | 18.469 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `classic` | `strict_current` | 14.734 | 1.145 | 12.868 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.286 | 0.974 | 6.453 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `ax` | `strict_current` | 6.286 | 1.362 | 4.616 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.865 | 0.974 | 15.260 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `classic` | `strict_current` | 14.865 | 1.362 | 10.916 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.644 | 1.092 | 6.085 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `ax` | `strict_current` | 6.644 | 1.337 | 4.969 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.408 | 1.092 | 14.112 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `classic` | `strict_current` | 15.408 | 1.337 | 11.522 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.408 | 0.827 | 7.750 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `ax` | `strict_current` | 6.408 | 1.153 | 5.560 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.523 | 0.827 | 17.564 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `classic` | `strict_current` | 14.523 | 1.153 | 12.600 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.067 | 2.092 | 2.900 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.067 | 9.251 | 0.656 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 37.128 | 2.092 | 17.746 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 37.128 | 9.251 | 4.013 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.779 | 3.184 | 1.815 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `ax` | `strict_current` | 5.779 | 9.413 | 0.614 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 35.039 | 3.184 | 11.005 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `classic` | `strict_current` | 35.039 | 9.413 | 3.722 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.792 | 2.175 | 2.663 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 5.792 | 9.517 | 0.609 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 40.046 | 2.175 | 18.412 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 40.046 | 9.517 | 4.208 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.217 | 2.202 | 2.824 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `ax` | `strict_current` | 6.217 | 9.348 | 0.665 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 41.152 | 2.202 | 18.691 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `classic` | `strict_current` | 41.152 | 9.348 | 4.402 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.263 | 0.737 | 8.497 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `ax` | `strict_current` | 6.263 | 0.797 | 7.859 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.701 | 0.737 | 34.868 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `classic` | `strict_current` | 25.701 | 0.797 | 32.252 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.337 | 0.743 | 8.526 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `ax` | `strict_current` | 6.337 | 1.038 | 6.107 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 22.586 | 0.743 | 30.388 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `classic` | `strict_current` | 22.586 | 1.038 | 21.768 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.662 | 0.854 | 7.798 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `ax` | `strict_current` | 6.662 | 0.795 | 8.380 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.148 | 0.854 | 29.437 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `classic` | `strict_current` | 25.148 | 0.795 | 31.633 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 16.566 | 1.037 | 15.974 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `ax` | `strict_current` | 16.566 | 1.176 | 14.091 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 26.888 | 1.037 | 25.928 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `classic` | `strict_current` | 26.888 | 1.176 | 22.871 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.768 | 1.133 | 5.974 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `ax` | `strict_current` | 6.768 | 1.144 | 5.916 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.596 | 1.133 | 22.592 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `classic` | `strict_current` | 25.596 | 1.144 | 22.371 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.318 | 1.151 | 5.491 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `ax` | `strict_current` | 6.318 | 1.294 | 4.881 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.556 | 1.151 | 21.344 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `classic` | `strict_current` | 24.556 | 1.294 | 18.970 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 16.962 | 1.045 | 16.228 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `ax` | `strict_current` | 16.962 | 1.192 | 14.234 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.101 | 1.045 | 24.014 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `classic` | `strict_current` | 25.101 | 1.192 | 21.064 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.639 | 0.848 | 7.829 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.639 | 0.972 | 6.832 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 26.798 | 0.848 | 31.601 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `classic` | `strict_current` | 26.798 | 0.972 | 27.579 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.768 | 0.915 | 9.581 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `ax` | `strict_current` | 8.768 | 1.049 | 8.358 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.784 | 0.915 | 29.266 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `classic` | `strict_current` | 26.784 | 1.049 | 25.532 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.144 | 0.778 | 7.900 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `ax` | `strict_current` | 6.144 | 1.202 | 5.109 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.876 | 0.778 | 31.986 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `classic` | `strict_current` | 24.876 | 1.202 | 20.688 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.806 | 0.835 | 8.153 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `ax` | `strict_current` | 6.806 | 1.114 | 6.111 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.405 | 0.835 | 29.234 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `classic` | `strict_current` | 24.405 | 1.114 | 21.913 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.067 | 1.033 | 5.872 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.067 | 1.098 | 5.525 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 14.744 | 1.033 | 14.269 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `classic` | `strict_current` | 14.744 | 1.098 | 13.428 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.692 | 1.041 | 6.429 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `ax` | `strict_current` | 6.692 | 1.047 | 6.390 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.595 | 1.041 | 14.021 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `classic` | `strict_current` | 14.595 | 1.047 | 13.936 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.585 | 0.991 | 6.642 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `ax` | `strict_current` | 6.585 | 1.080 | 6.097 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.789 | 0.991 | 13.908 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `classic` | `strict_current` | 13.789 | 1.080 | 12.767 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.576 | 0.843 | 7.799 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `ax` | `strict_current` | 6.576 | 1.116 | 5.894 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.835 | 0.843 | 16.408 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `classic` | `strict_current` | 13.835 | 1.116 | 12.399 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 17.094 | 0.928 | 18.422 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `ax` | `strict_current` | 17.094 | 1.563 | 10.936 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 26.677 | 0.928 | 28.748 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `classic` | `strict_current` | 26.677 | 1.563 | 17.067 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.448 | 0.977 | 6.598 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `ax` | `strict_current` | 6.448 | 1.490 | 4.328 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.670 | 0.977 | 25.241 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `classic` | `strict_current` | 24.670 | 1.490 | 16.557 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 14.610 | 1.006 | 14.526 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `ax` | `strict_current` | 14.610 | 1.502 | 9.728 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.959 | 1.006 | 25.811 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `classic` | `strict_current` | 25.959 | 1.502 | 17.285 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 16.262 | 0.920 | 17.673 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `ax` | `strict_current` | 16.262 | 1.640 | 9.916 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.141 | 0.920 | 28.409 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `classic` | `strict_current` | 26.141 | 1.640 | 15.940 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 14.678 | 0.833 | 17.614 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `ax` | `strict_current` | 14.678 | 1.075 | 13.649 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 14.101 | 0.833 | 16.922 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `classic` | `strict_current` | 14.101 | 1.075 | 13.113 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.126 | 0.776 | 9.179 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `ax` | `strict_current` | 7.126 | 0.948 | 7.518 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.694 | 0.776 | 18.928 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `classic` | `strict_current` | 14.694 | 0.948 | 15.503 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 16.656 | 0.912 | 18.260 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `ax` | `strict_current` | 16.656 | 0.823 | 20.229 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 17.338 | 0.912 | 19.008 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `classic` | `strict_current` | 17.338 | 0.823 | 21.058 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.854 | 0.787 | 8.712 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `ax` | `strict_current` | 6.854 | 0.877 | 7.815 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.505 | 0.787 | 18.436 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `classic` | `strict_current` | 14.505 | 0.877 | 16.538 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.264 | 1.155 | 5.424 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.264 | 2.272 | 2.757 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 23.984 | 1.155 | 20.766 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `classic` | `strict_current` | 23.984 | 2.272 | 10.554 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.570 | 1.204 | 5.457 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `ax` | `strict_current` | 6.570 | 2.107 | 3.118 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.135 | 1.204 | 20.047 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `classic` | `strict_current` | 24.135 | 2.107 | 11.453 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.690 | 1.202 | 5.568 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `ax` | `strict_current` | 6.690 | 2.257 | 2.964 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.505 | 1.202 | 21.226 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `classic` | `strict_current` | 25.505 | 2.257 | 11.300 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.296 | 1.230 | 5.117 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `ax` | `strict_current` | 6.296 | 2.092 | 3.009 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.251 | 1.230 | 19.711 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `classic` | `strict_current` | 24.251 | 2.092 | 11.591 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.575 | 1.078 | 6.099 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `ax` | `strict_current` | 6.575 | 0.975 | 6.745 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 29.498 | 1.078 | 27.364 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `classic` | `strict_current` | 29.498 | 0.975 | 30.261 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.180 | 1.021 | 6.054 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `ax` | `strict_current` | 6.180 | 0.954 | 6.475 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.205 | 1.021 | 24.693 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `classic` | `strict_current` | 25.205 | 0.954 | 26.408 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.985 | 1.037 | 6.739 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `ax` | `strict_current` | 6.985 | 0.889 | 7.856 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.966 | 1.037 | 13.474 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `classic` | `strict_current` | 13.966 | 0.889 | 15.708 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.571 | 1.065 | 6.167 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `ax` | `strict_current` | 6.571 | 1.013 | 6.485 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.685 | 1.065 | 13.783 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `classic` | `strict_current` | 14.685 | 1.013 | 14.494 |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.426 | 1.090 | 5.897 |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `ax` | `strict_current` | 6.426 | 1.000 | 6.427 |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.190 | 1.090 | 12.103 |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `classic` | `strict_current` | 13.190 | 1.000 | 13.190 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.929 | 1.042 | 6.648 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.929 | 0.999 | 6.934 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 14.088 | 1.042 | 13.516 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `classic` | `strict_current` | 14.088 | 0.999 | 14.098 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.688 | 0.916 | 8.389 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `ax` | `strict_current` | 7.688 | 0.944 | 8.141 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.604 | 0.916 | 14.844 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `classic` | `strict_current` | 13.604 | 0.944 | 14.406 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.815 | 0.984 | 6.924 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `ax` | `strict_current` | 6.815 | 1.241 | 5.492 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.735 | 0.984 | 13.956 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `classic` | `strict_current` | 13.735 | 1.241 | 11.070 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.985 | 0.914 | 7.641 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `ax` | `strict_current` | 6.985 | 0.910 | 7.672 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.076 | 0.914 | 16.492 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `classic` | `strict_current` | 15.076 | 0.910 | 16.560 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.794 | 0.862 | 7.883 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.794 | 1.470 | 4.622 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.919 | 0.862 | 28.913 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.919 | 1.470 | 16.952 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.630 | 0.882 | 7.521 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `ax` | `strict_current` | 6.630 | 1.439 | 4.607 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.810 | 0.882 | 28.145 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `classic` | `strict_current` | 24.810 | 1.439 | 17.239 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.521 | 0.898 | 7.262 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `ax` | `strict_current` | 6.521 | 1.353 | 4.821 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.361 | 0.898 | 27.132 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `classic` | `strict_current` | 24.361 | 1.353 | 18.011 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.322 | 0.903 | 7.003 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `ax` | `strict_current` | 6.322 | 1.487 | 4.250 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.072 | 0.903 | 27.773 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `classic` | `strict_current` | 25.072 | 1.487 | 16.856 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.683 | 1.781 | 3.753 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.683 | 2.315 | 2.887 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 22.296 | 1.781 | 12.522 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 22.296 | 2.315 | 9.632 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.162 | 1.102 | 6.499 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `ax` | `strict_current` | 7.162 | 3.030 | 2.364 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.747 | 1.102 | 21.550 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `classic` | `strict_current` | 23.747 | 3.030 | 7.839 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.818 | 1.334 | 5.113 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 6.818 | 3.110 | 2.192 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.553 | 1.334 | 17.663 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 23.553 | 3.110 | 7.574 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.251 | 1.155 | 5.412 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `ax` | `strict_current` | 6.251 | 2.889 | 2.164 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 22.204 | 1.155 | 19.222 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `classic` | `strict_current` | 22.204 | 2.889 | 7.685 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.674 | 0.910 | 7.335 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.674 | 1.602 | 4.167 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 27.324 | 0.910 | 30.028 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `classic` | `strict_current` | 27.324 | 1.602 | 17.061 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.795 | 0.905 | 7.510 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `ax` | `strict_current` | 6.795 | 1.656 | 4.102 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.118 | 0.905 | 27.757 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `classic` | `strict_current` | 25.118 | 1.656 | 15.164 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.426 | 0.974 | 7.622 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `ax` | `strict_current` | 7.426 | 1.660 | 4.474 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.757 | 0.974 | 25.411 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `classic` | `strict_current` | 24.757 | 1.660 | 14.916 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.011 | 0.804 | 8.718 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `ax` | `strict_current` | 7.011 | 1.659 | 4.227 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.403 | 0.804 | 30.344 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `classic` | `strict_current` | 24.403 | 1.659 | 14.713 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 16.149 | 0.808 | 19.993 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `ax` | `strict_current` | 16.149 | 0.869 | 18.581 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 28.967 | 0.808 | 35.861 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `classic` | `strict_current` | 28.967 | 0.869 | 33.327 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.772 | 0.745 | 9.084 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `ax` | `strict_current` | 6.772 | 0.851 | 7.955 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 28.214 | 0.745 | 37.847 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `classic` | `strict_current` | 28.214 | 0.851 | 33.144 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.166 | 0.860 | 9.490 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `ax` | `strict_current` | 8.166 | 0.841 | 9.704 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.260 | 0.860 | 30.520 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `classic` | `strict_current` | 26.260 | 0.841 | 31.209 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 19.177 | 0.824 | 23.269 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `ax` | `strict_current` | 19.177 | 0.998 | 19.216 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 28.477 | 0.824 | 34.553 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `classic` | `strict_current` | 28.477 | 0.998 | 28.535 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.028 | 0.788 | 8.916 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.028 | 0.808 | 8.698 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.424 | 0.788 | 30.985 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.424 | 0.808 | 30.228 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.677 | 0.784 | 8.520 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `ax` | `strict_current` | 6.677 | 0.979 | 6.823 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.592 | 0.784 | 33.934 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `classic` | `strict_current` | 26.592 | 0.979 | 27.174 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.345 | 0.742 | 9.896 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 7.345 | 0.887 | 8.283 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.472 | 0.742 | 34.319 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 25.472 | 0.887 | 28.726 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.764 | 0.750 | 9.017 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `ax` | `strict_current` | 6.764 | 0.882 | 7.668 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.118 | 0.750 | 34.817 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `classic` | `strict_current` | 26.118 | 0.882 | 29.609 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 15.056 | 0.853 | 17.641 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `ax` | `strict_current` | 15.056 | 1.192 | 12.633 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 14.552 | 0.853 | 17.050 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `classic` | `strict_current` | 14.552 | 1.192 | 12.210 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 15.221 | 0.911 | 16.717 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `ax` | `strict_current` | 15.221 | 1.274 | 11.950 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.334 | 0.911 | 15.743 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `classic` | `strict_current` | 14.334 | 1.274 | 11.254 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.184 | 0.887 | 6.973 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `ax` | `strict_current` | 6.184 | 1.209 | 5.114 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.446 | 0.887 | 17.416 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `classic` | `strict_current` | 15.446 | 1.209 | 12.773 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.846 | 0.873 | 7.842 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `ax` | `strict_current` | 6.846 | 1.282 | 5.342 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.858 | 0.873 | 15.874 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `classic` | `strict_current` | 13.858 | 1.282 | 10.813 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.260 | 0.882 | 7.095 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.260 | 0.960 | 6.521 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 27.556 | 0.882 | 31.232 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `classic` | `strict_current` | 27.556 | 0.960 | 28.709 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.147 | 0.877 | 7.011 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `ax` | `strict_current` | 6.147 | 0.914 | 6.724 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.490 | 0.877 | 27.931 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `classic` | `strict_current` | 24.490 | 0.914 | 26.788 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.956 | 0.909 | 6.550 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `ax` | `strict_current` | 5.956 | 0.947 | 6.289 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.620 | 0.909 | 28.174 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `classic` | `strict_current` | 25.620 | 0.947 | 27.051 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.586 | 0.844 | 7.807 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `ax` | `strict_current` | 6.586 | 0.991 | 6.644 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.536 | 0.844 | 30.270 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `classic` | `strict_current` | 25.536 | 0.991 | 25.762 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.580 | 1.045 | 6.298 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.580 | 1.051 | 6.263 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.504 | 1.045 | 24.412 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.504 | 1.051 | 24.277 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.009 | 1.048 | 5.735 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `ax` | `strict_current` | 6.009 | 1.110 | 5.413 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.360 | 1.048 | 24.200 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `classic` | `strict_current` | 25.360 | 1.110 | 22.844 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.887 | 1.267 | 6.225 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `ax` | `strict_current` | 7.887 | 1.374 | 5.742 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 28.399 | 1.267 | 22.415 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `classic` | `strict_current` | 28.399 | 1.374 | 20.675 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.291 | 1.117 | 6.525 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `ax` | `strict_current` | 7.291 | 1.095 | 6.659 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.109 | 1.117 | 23.366 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `classic` | `strict_current` | 26.109 | 1.095 | 23.844 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 17.778 | 1.232 | 14.431 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `ax` | `strict_current` | 17.778 | 1.163 | 15.286 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 15.652 | 1.232 | 12.705 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `classic` | `strict_current` | 15.652 | 1.163 | 13.457 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.540 | 1.277 | 5.121 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `ax` | `strict_current` | 6.540 | 0.974 | 6.712 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.533 | 1.277 | 12.162 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `classic` | `strict_current` | 15.533 | 0.974 | 15.942 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.505 | 1.052 | 7.135 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `ax` | `strict_current` | 7.505 | 1.078 | 6.960 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.933 | 1.052 | 15.147 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `classic` | `strict_current` | 15.933 | 1.078 | 14.776 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 14.823 | 1.213 | 12.220 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `ax` | `strict_current` | 14.823 | 1.074 | 13.802 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.192 | 1.213 | 11.699 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `classic` | `strict_current` | 14.192 | 1.074 | 13.213 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.322 | 0.828 | 7.633 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.322 | 1.340 | 4.719 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.406 | 0.828 | 30.675 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.406 | 1.340 | 18.966 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.126 | 0.813 | 8.760 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `ax` | `strict_current` | 7.126 | 1.318 | 5.407 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.367 | 0.813 | 29.955 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `classic` | `strict_current` | 24.367 | 1.318 | 18.489 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.417 | 0.805 | 7.967 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `ax` | `strict_current` | 6.417 | 1.462 | 4.390 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.797 | 0.805 | 30.786 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `classic` | `strict_current` | 24.797 | 1.462 | 16.963 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.973 | 0.982 | 7.102 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `ax` | `strict_current` | 6.973 | 1.424 | 4.897 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.453 | 0.982 | 25.923 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `classic` | `strict_current` | 25.453 | 1.424 | 17.874 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 5.901 | 1.771 | 3.333 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 5.901 | 4.302 | 1.372 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.465 | 1.771 | 13.817 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.465 | 4.302 | 5.687 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.203 | 1.787 | 3.471 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `ax` | `strict_current` | 6.203 | 4.362 | 1.422 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.481 | 1.787 | 13.140 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `classic` | `strict_current` | 23.481 | 4.362 | 5.383 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.198 | 1.807 | 3.430 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `ax` | `strict_current` | 6.198 | 4.218 | 1.470 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.420 | 1.807 | 12.961 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `classic` | `strict_current` | 23.420 | 4.218 | 5.553 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.520 | 1.929 | 3.380 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `ax` | `strict_current` | 6.520 | 4.272 | 1.526 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.528 | 1.929 | 12.196 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `classic` | `strict_current` | 23.528 | 4.272 | 5.507 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 15.946 | 0.892 | 17.884 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `ax` | `strict_current` | 15.946 | 1.109 | 14.379 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 26.381 | 0.892 | 29.587 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `classic` | `strict_current` | 26.381 | 1.109 | 23.788 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 16.362 | 0.833 | 19.644 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `ax` | `strict_current` | 16.362 | 1.001 | 16.348 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.080 | 0.833 | 32.511 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `classic` | `strict_current` | 27.080 | 1.001 | 27.057 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.149 | 0.869 | 7.077 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `ax` | `strict_current` | 6.149 | 0.998 | 6.159 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.184 | 0.869 | 27.834 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `classic` | `strict_current` | 24.184 | 0.998 | 24.222 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.706 | 0.780 | 8.599 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `ax` | `strict_current` | 6.706 | 1.217 | 5.509 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.500 | 0.780 | 32.700 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `classic` | `strict_current` | 25.500 | 1.217 | 20.950 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.327 | 1.755 | 3.604 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.327 | 3.324 | 1.903 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 23.654 | 1.755 | 13.475 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 23.654 | 3.324 | 7.115 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.432 | 1.723 | 3.734 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `ax` | `strict_current` | 6.432 | 3.156 | 2.038 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 22.927 | 1.723 | 13.310 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `classic` | `strict_current` | 22.927 | 3.156 | 7.265 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.631 | 2.055 | 3.227 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `ax` | `strict_current` | 6.631 | 2.957 | 2.243 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 22.628 | 2.055 | 11.011 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `classic` | `strict_current` | 22.628 | 2.957 | 7.653 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.648 | 1.662 | 3.399 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `ax` | `strict_current` | 5.648 | 3.259 | 1.733 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 22.764 | 1.662 | 13.700 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `classic` | `strict_current` | 22.764 | 3.259 | 6.985 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.333 | 1.341 | 5.468 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `ax` | `strict_current` | 7.333 | 8.686 | 0.844 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.021 | 1.341 | 24.622 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `classic` | `strict_current` | 33.021 | 8.686 | 3.802 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.747 | 1.473 | 4.581 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `ax` | `strict_current` | 6.747 | 8.784 | 0.768 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 31.572 | 1.473 | 21.437 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `classic` | `strict_current` | 31.572 | 8.784 | 3.594 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.198 | 0.944 | 6.563 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `ax` | `strict_current` | 6.198 | 1.720 | 3.603 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.023 | 0.944 | 25.437 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `classic` | `strict_current` | 24.023 | 1.720 | 13.966 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.170 | 0.883 | 6.984 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `ax` | `strict_current` | 6.170 | 1.765 | 3.495 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.927 | 0.883 | 27.084 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `classic` | `strict_current` | 23.927 | 1.765 | 13.556 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.036 | 3.410 | 1.770 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `ax` | `strict_current` | 6.036 | 3.565 | 1.693 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.693 | 3.410 | 6.948 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `classic` | `strict_current` | 23.693 | 3.565 | 6.645 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.085 | 3.291 | 1.849 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `ax` | `strict_current` | 6.085 | 3.478 | 1.750 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.359 | 3.291 | 7.098 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `classic` | `strict_current` | 23.359 | 3.478 | 6.717 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.360 | 0.844 | 7.539 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `ax` | `strict_current` | 6.360 | 1.372 | 4.634 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.180 | 0.844 | 29.849 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `classic` | `strict_current` | 25.180 | 1.372 | 18.349 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.197 | 0.805 | 7.697 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `ax` | `strict_current` | 6.197 | 1.301 | 4.762 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.349 | 0.805 | 30.245 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `classic` | `strict_current` | 24.349 | 1.301 | 18.712 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.700 | 1.153 | 5.813 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `ax` | `strict_current` | 6.700 | 1.160 | 5.776 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.954 | 1.153 | 23.386 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `classic` | `strict_current` | 26.954 | 1.160 | 23.235 |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.956 | 1.142 | 5.217 |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `ax` | `strict_current` | 5.956 | 1.044 | 5.703 |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.999 | 1.142 | 22.773 |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `classic` | `strict_current` | 25.999 | 1.044 | 24.896 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.276 | 0.880 | 7.136 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `ax` | `strict_current` | 6.276 | 1.590 | 3.948 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.052 | 0.880 | 30.757 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `classic` | `strict_current` | 27.052 | 1.590 | 17.015 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.509 | 0.847 | 7.684 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `ax` | `strict_current` | 6.509 | 1.908 | 3.411 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.498 | 0.847 | 30.101 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `classic` | `strict_current` | 25.498 | 1.908 | 13.361 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.603 | 1.694 | 4.489 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `ax` | `strict_current` | 7.603 | 1.889 | 4.024 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.489 | 1.694 | 15.641 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `classic` | `strict_current` | 26.489 | 1.889 | 14.021 |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.327 | 1.303 | 4.857 |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `ax` | `strict_current` | 6.327 | 1.523 | 4.154 |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.930 | 1.303 | 18.368 |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `classic` | `strict_current` | 23.930 | 1.523 | 15.711 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.504 | 11.978 | 0.543 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `ax` | `strict_current` | 6.504 | 11.934 | 0.545 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 37.547 | 11.978 | 3.135 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `classic` | `strict_current` | 37.547 | 11.934 | 3.146 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.694 | 12.187 | 0.549 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `ax` | `strict_current` | 6.694 | 12.549 | 0.533 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 37.168 | 12.187 | 3.050 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `classic` | `strict_current` | 37.168 | 12.549 | 2.962 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.347 | 1.551 | 4.092 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `ax` | `strict_current` | 6.347 | 2.648 | 2.397 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.909 | 1.551 | 16.058 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `classic` | `strict_current` | 24.909 | 2.648 | 9.407 |
| `vbr1_l2_event_controller` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.795 | 1.676 | 4.055 |
| `vbr1_l2_event_controller` | `tb` | `gold` | `ax` | `strict_current` | 6.795 | 2.675 | 2.541 |
| `vbr1_l2_event_controller` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.755 | 1.676 | 14.773 |
| `vbr1_l2_event_controller` | `tb` | `gold` | `classic` | `strict_current` | 24.755 | 2.675 | 9.255 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.509 | 0.890 | 6.192 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `ax` | `strict_current` | 5.509 | 1.751 | 3.146 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.830 | 0.890 | 27.912 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `classic` | `strict_current` | 24.830 | 1.751 | 14.183 |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.455 | 0.996 | 6.483 |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `ax` | `strict_current` | 6.455 | 1.589 | 4.064 |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.646 | 0.996 | 24.752 |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `classic` | `strict_current` | 24.646 | 1.589 | 15.515 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.055 | 9.460 | 1.063 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `ax` | `strict_current` | 10.055 | 125.358 | 0.080 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 44.051 | 9.460 | 4.657 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `classic` | `strict_current` | 44.051 | 125.358 | 0.351 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.738 | 32.699 | 0.328 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `ax` | `strict_current` | 10.738 | 153.215 | 0.070 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 48.801 | 32.699 | 1.492 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `classic` | `strict_current` | 48.801 | 153.215 | 0.319 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.496 | 1.676 | 3.875 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `ax` | `strict_current` | 6.496 | 2.498 | 2.601 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.178 | 1.676 | 15.617 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `classic` | `strict_current` | 26.178 | 2.498 | 10.481 |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.577 | 1.685 | 3.904 |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `ax` | `strict_current` | 6.577 | 2.608 | 2.522 |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.130 | 1.685 | 14.322 |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `classic` | `strict_current` | 24.130 | 2.608 | 9.253 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.181 | 10.313 | 0.599 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `ax` | `strict_current` | 6.181 | 10.523 | 0.587 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 21.078 | 10.313 | 2.044 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `classic` | `strict_current` | 21.078 | 10.523 | 2.003 |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.673 | 10.148 | 0.559 |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `ax` | `strict_current` | 5.673 | 10.517 | 0.539 |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 21.603 | 10.148 | 2.129 |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `classic` | `strict_current` | 21.603 | 10.517 | 2.054 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.418 | 1.178 | 5.447 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `ax` | `strict_current` | 6.418 | 2.066 | 3.106 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.057 | 1.178 | 21.268 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `classic` | `strict_current` | 25.057 | 2.066 | 12.128 |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.446 | 1.252 | 5.148 |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `ax` | `strict_current` | 6.446 | 2.078 | 3.102 |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.155 | 1.252 | 19.291 |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `classic` | `strict_current` | 24.155 | 2.078 | 11.625 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.631 | 1.443 | 4.596 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `ax` | `strict_current` | 6.631 | 17.134 | 0.387 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 43.836 | 1.443 | 30.382 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `classic` | `strict_current` | 43.836 | 17.134 | 2.558 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.288 | 2.594 | 2.424 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `ax` | `strict_current` | 6.288 | 17.381 | 0.362 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 40.734 | 2.594 | 15.705 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `classic` | `strict_current` | 40.734 | 17.381 | 2.344 |

## Interpretation Guardrails

- Speedups use `simulation_ok`, so rows without a behavior checker can still contribute timing if the simulator produced waveforms.
- Accuracy-gated speedups require candidate behavior pass, strict-EVAS parity, and parity to every selected Spectre mode.
- `spectre/ax` matches the previous bridge default but Spectre X may ignore `errpreset` and `maxstep` from the testbench.
- `spectre/classic` is available to measure the stricter non-X path when requested.
- Cold Spectre runs include AHDL CMI compilation; warm-cache repetitions should be reported separately.
- A `BLOCKED` gate is not evidence of wrong behavior; it means the checker or reference evidence is incomplete.
