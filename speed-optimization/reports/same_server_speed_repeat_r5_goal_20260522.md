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
- Output root: `results/same-server-speed-repeat-r5-goal-20260522`

## Mode Summary

| Backend | Mode | Runs | PASS | Non-PASS | Total wall s | Mean wall s |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| evas | profile_fast_skip_source_error_control | 259 | 259 | 0 | 934.237 | 3.607 |
| evas | strict_current | 259 | 259 | 0 | 2164.696 | 8.358 |
| spectre | ax | 259 | 259 | 0 | 2784.330 | 10.750 |
| spectre | classic | 259 | 259 | 0 | 8597.249 | 33.194 |

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
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.872 | 1.519 | 5.184 |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.872 | 1.097 | 7.175 |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 30.752 | 1.519 | 20.250 |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `classic` | `strict_current` | 30.752 | 1.097 | 28.029 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.463 | 0.916 | 9.236 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `ax` | `strict_current` | 8.463 | 1.288 | 6.573 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.767 | 0.916 | 36.851 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `classic` | `strict_current` | 33.767 | 1.288 | 26.225 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.121 | 0.731 | 11.113 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `ax` | `strict_current` | 8.121 | 1.114 | 7.287 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 31.574 | 0.731 | 43.209 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `classic` | `strict_current` | 31.574 | 1.114 | 28.334 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.481 | 1.078 | 9.720 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `ax` | `strict_current` | 10.481 | 1.173 | 8.934 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.946 | 1.078 | 31.482 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `classic` | `strict_current` | 33.946 | 1.173 | 28.936 |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 9.853 | 1.500 | 6.567 |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 9.853 | 10.180 | 0.968 |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 44.307 | 1.500 | 29.529 |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 44.307 | 10.180 | 4.352 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 13.578 | 1.195 | 11.367 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `ax` | `strict_current` | 13.578 | 10.711 | 1.268 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 41.046 | 1.195 | 34.361 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `classic` | `strict_current` | 41.046 | 10.711 | 3.832 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.444 | 1.910 | 4.421 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `ax` | `strict_current` | 8.444 | 1.543 | 5.472 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.171 | 1.910 | 17.367 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `classic` | `strict_current` | 33.171 | 1.543 | 21.495 |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.653 | 1.428 | 6.759 |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `ax` | `strict_current` | 9.653 | 1.828 | 5.282 |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.741 | 1.428 | 23.626 |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `classic` | `strict_current` | 33.741 | 1.828 | 18.461 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 23.401 | 0.783 | 29.903 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `ax` | `strict_current` | 23.401 | 0.730 | 32.056 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 34.996 | 0.783 | 44.719 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `classic` | `strict_current` | 34.996 | 0.730 | 47.939 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 20.395 | 0.508 | 40.143 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `ax` | `strict_current` | 20.395 | 0.583 | 35.005 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 35.069 | 0.508 | 69.024 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `classic` | `strict_current` | 35.069 | 0.583 | 60.189 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 23.583 | 0.575 | 40.980 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `ax` | `strict_current` | 23.583 | 0.602 | 39.158 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 37.017 | 0.575 | 64.323 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `classic` | `strict_current` | 37.017 | 0.602 | 61.462 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.834 | 0.755 | 13.021 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `ax` | `strict_current` | 9.834 | 0.722 | 13.615 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 34.671 | 0.755 | 45.909 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `classic` | `strict_current` | 34.671 | 0.722 | 48.003 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 11.711 | 0.879 | 13.318 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `ax` | `strict_current` | 11.711 | 1.059 | 11.054 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 41.692 | 0.879 | 47.416 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `classic` | `strict_current` | 41.692 | 1.059 | 39.355 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.323 | 1.123 | 9.191 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `ax` | `strict_current` | 10.323 | 1.267 | 8.146 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 43.619 | 1.123 | 38.832 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `classic` | `strict_current` | 43.619 | 1.267 | 34.420 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.509 | 1.078 | 8.823 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `ax` | `strict_current` | 9.509 | 1.224 | 7.767 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 36.980 | 1.078 | 34.313 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `classic` | `strict_current` | 36.980 | 1.224 | 30.205 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.916 | 0.554 | 14.278 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.916 | 1.350 | 5.862 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 31.451 | 0.554 | 56.727 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `classic` | `strict_current` | 31.451 | 1.350 | 23.291 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.925 | 0.970 | 8.166 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `ax` | `strict_current` | 7.925 | 1.315 | 6.025 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 31.600 | 0.970 | 32.562 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `classic` | `strict_current` | 31.600 | 1.315 | 24.023 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.231 | 1.006 | 8.178 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `ax` | `strict_current` | 8.231 | 1.451 | 5.673 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 32.305 | 1.006 | 32.096 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `classic` | `strict_current` | 32.305 | 1.451 | 22.264 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.241 | 0.587 | 12.336 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `ax` | `strict_current` | 7.241 | 1.384 | 5.231 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 30.452 | 0.587 | 51.876 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `classic` | `strict_current` | 30.452 | 1.384 | 22.000 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 8.307 | 1.565 | 5.308 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `ax` | `strict_current` | 8.307 | 3.260 | 2.548 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 29.370 | 1.565 | 18.766 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `classic` | `strict_current` | 29.370 | 3.260 | 9.010 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.540 | 1.990 | 3.788 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `ax` | `strict_current` | 7.540 | 3.767 | 2.001 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 36.232 | 1.990 | 18.204 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `classic` | `strict_current` | 36.232 | 3.767 | 9.617 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.624 | 2.514 | 3.032 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `ax` | `strict_current` | 7.624 | 3.594 | 2.121 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 30.384 | 2.514 | 12.085 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `classic` | `strict_current` | 30.384 | 3.594 | 8.454 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.173 | 2.070 | 4.431 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `ax` | `strict_current` | 9.173 | 3.691 | 2.485 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 29.177 | 2.070 | 14.094 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `classic` | `strict_current` | 29.177 | 3.691 | 7.904 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 9.178 | 0.732 | 12.534 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `ax` | `strict_current` | 9.178 | 1.387 | 6.615 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 31.510 | 0.732 | 43.032 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `classic` | `strict_current` | 31.510 | 1.387 | 22.711 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.967 | 1.086 | 8.257 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `ax` | `strict_current` | 8.967 | 1.567 | 5.722 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 30.999 | 1.086 | 28.546 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `classic` | `strict_current` | 30.999 | 1.567 | 19.782 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.730 | 0.617 | 12.523 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `ax` | `strict_current` | 7.730 | 1.264 | 6.116 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.114 | 0.617 | 53.645 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `classic` | `strict_current` | 33.114 | 1.264 | 26.196 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.201 | 0.740 | 11.077 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `ax` | `strict_current` | 8.201 | 2.036 | 4.028 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 32.111 | 0.740 | 43.372 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `classic` | `strict_current` | 32.111 | 2.036 | 15.770 |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 8.201 | 1.456 | 5.632 |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `ax` | `strict_current` | 8.201 | 4.987 | 1.645 |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 31.465 | 1.456 | 21.609 |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `classic` | `strict_current` | 31.465 | 4.987 | 6.309 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.546 | 1.120 | 6.739 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `ax` | `strict_current` | 7.546 | 4.455 | 1.694 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 31.939 | 1.120 | 28.521 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `classic` | `strict_current` | 31.939 | 4.455 | 7.170 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.593 | 1.157 | 6.561 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `ax` | `strict_current` | 7.593 | 4.025 | 1.886 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 30.968 | 1.157 | 26.757 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `classic` | `strict_current` | 30.968 | 4.025 | 7.693 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.873 | 1.150 | 7.714 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `ax` | `strict_current` | 8.873 | 3.868 | 2.294 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 32.010 | 1.150 | 27.830 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `classic` | `strict_current` | 32.010 | 3.868 | 8.275 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 8.419 | 0.888 | 9.478 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `ax` | `strict_current` | 8.419 | 1.354 | 6.220 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 31.684 | 0.888 | 35.670 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `classic` | `strict_current` | 31.684 | 1.354 | 23.408 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.760 | 0.689 | 12.721 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `ax` | `strict_current` | 8.760 | 1.455 | 6.021 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.447 | 0.689 | 48.570 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `classic` | `strict_current` | 33.447 | 1.455 | 22.987 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.300 | 0.785 | 10.576 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `ax` | `strict_current` | 8.300 | 1.402 | 5.918 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 31.111 | 0.785 | 39.643 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `classic` | `strict_current` | 31.111 | 1.402 | 22.184 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.983 | 0.749 | 10.652 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `ax` | `strict_current` | 7.983 | 1.425 | 5.604 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 31.708 | 0.749 | 42.310 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `classic` | `strict_current` | 31.708 | 1.425 | 22.258 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 8.259 | 1.001 | 8.253 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 8.259 | 3.295 | 2.506 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 30.237 | 1.001 | 30.217 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 30.237 | 3.295 | 9.176 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.823 | 1.089 | 9.020 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `ax` | `strict_current` | 9.823 | 2.794 | 3.515 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 31.470 | 1.089 | 28.899 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `classic` | `strict_current` | 31.470 | 2.794 | 11.262 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 13.877 | 2.532 | 5.480 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 13.877 | 3.451 | 4.022 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 37.009 | 2.532 | 14.614 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 37.009 | 3.451 | 10.725 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 14.931 | 1.338 | 11.156 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `ax` | `strict_current` | 14.931 | 2.835 | 5.267 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 37.844 | 1.338 | 28.275 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `classic` | `strict_current` | 37.844 | 2.835 | 13.350 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 8.291 | 1.079 | 7.686 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `ax` | `strict_current` | 8.291 | 1.247 | 6.647 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 18.026 | 1.079 | 16.709 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `classic` | `strict_current` | 18.026 | 1.247 | 14.451 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.380 | 0.958 | 8.746 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `ax` | `strict_current` | 8.380 | 1.219 | 6.873 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 17.822 | 0.958 | 18.600 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `classic` | `strict_current` | 17.822 | 1.219 | 14.617 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.693 | 0.749 | 10.270 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `ax` | `strict_current` | 7.693 | 1.282 | 5.999 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 16.694 | 0.749 | 22.287 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `classic` | `strict_current` | 16.694 | 1.282 | 13.018 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.030 | 0.741 | 12.186 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `ax` | `strict_current` | 9.030 | 1.204 | 7.500 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 19.490 | 0.741 | 26.300 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `classic` | `strict_current` | 19.490 | 1.204 | 16.187 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.655 | 0.609 | 15.855 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `ax` | `strict_current` | 9.655 | 0.569 | 16.965 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 20.551 | 0.609 | 33.748 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `classic` | `strict_current` | 20.551 | 0.569 | 36.111 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.450 | 0.542 | 13.752 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `ax` | `strict_current` | 7.450 | 0.506 | 14.728 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 19.123 | 0.542 | 35.297 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `classic` | `strict_current` | 19.123 | 0.506 | 37.802 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.409 | 0.621 | 15.152 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `ax` | `strict_current` | 9.409 | 0.536 | 17.554 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 18.631 | 0.621 | 30.004 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `classic` | `strict_current` | 18.631 | 0.536 | 34.759 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 8.261 | 0.903 | 9.148 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `ax` | `strict_current` | 8.261 | 0.571 | 14.462 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 31.260 | 0.903 | 34.616 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `classic` | `strict_current` | 31.260 | 0.571 | 54.727 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.844 | 0.532 | 14.748 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `ax` | `strict_current` | 7.844 | 0.652 | 12.028 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 31.904 | 0.532 | 59.989 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `classic` | `strict_current` | 31.904 | 0.652 | 48.923 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.909 | 0.414 | 21.530 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `ax` | `strict_current` | 8.909 | 0.573 | 15.546 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 32.601 | 0.414 | 78.786 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `classic` | `strict_current` | 32.601 | 0.573 | 56.888 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.044 | 0.636 | 14.210 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `ax` | `strict_current` | 9.044 | 0.496 | 18.242 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.209 | 0.636 | 52.177 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `classic` | `strict_current` | 33.209 | 0.496 | 66.984 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 22.881 | 0.474 | 48.237 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `ax` | `strict_current` | 22.881 | 0.918 | 24.914 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 33.342 | 0.474 | 70.291 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `classic` | `strict_current` | 33.342 | 0.918 | 36.304 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.038 | 0.672 | 11.964 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `ax` | `strict_current` | 8.038 | 1.102 | 7.296 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 36.953 | 0.672 | 54.998 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `classic` | `strict_current` | 36.953 | 1.102 | 33.539 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.152 | 1.023 | 9.925 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `ax` | `strict_current` | 10.152 | 0.702 | 14.461 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 29.568 | 1.023 | 28.906 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `classic` | `strict_current` | 29.568 | 0.702 | 42.116 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 20.910 | 0.552 | 37.848 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `ax` | `strict_current` | 20.910 | 0.622 | 33.593 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 34.782 | 0.552 | 62.957 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `classic` | `strict_current` | 34.782 | 0.622 | 55.878 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.695 | 0.827 | 9.309 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.695 | 4.491 | 1.714 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 31.055 | 0.827 | 37.566 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `classic` | `strict_current` | 31.055 | 4.491 | 6.916 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.705 | 0.669 | 13.021 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `ax` | `strict_current` | 8.705 | 4.370 | 1.992 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 32.130 | 0.669 | 48.061 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `classic` | `strict_current` | 32.130 | 4.370 | 7.353 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.874 | 0.904 | 8.706 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `ax` | `strict_current` | 7.874 | 4.395 | 1.792 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 31.096 | 0.904 | 34.382 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `classic` | `strict_current` | 31.096 | 4.395 | 7.075 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.071 | 0.647 | 12.473 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `ax` | `strict_current` | 8.071 | 4.323 | 1.867 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 32.158 | 0.647 | 49.694 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `classic` | `strict_current` | 32.158 | 4.323 | 7.439 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 8.460 | 2.406 | 3.516 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `ax` | `strict_current` | 8.460 | 2.743 | 3.084 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 32.125 | 2.406 | 13.352 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `classic` | `strict_current` | 32.125 | 2.743 | 11.711 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.845 | 1.525 | 5.800 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `ax` | `strict_current` | 8.845 | 1.381 | 6.404 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 31.376 | 1.525 | 20.574 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `classic` | `strict_current` | 31.376 | 1.381 | 22.716 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.172 | 1.899 | 5.356 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `ax` | `strict_current` | 10.172 | 1.409 | 7.217 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.340 | 1.899 | 17.556 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `classic` | `strict_current` | 33.340 | 1.409 | 23.655 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.646 | 1.297 | 5.896 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `ax` | `strict_current` | 7.646 | 1.259 | 6.072 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 32.407 | 1.297 | 24.988 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `classic` | `strict_current` | 32.407 | 1.259 | 25.733 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.147 | 0.957 | 8.509 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `ax` | `strict_current` | 8.147 | 0.540 | 15.088 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.294 | 0.957 | 13.885 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `classic` | `strict_current` | 13.294 | 0.540 | 24.622 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.555 | 0.571 | 18.501 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `ax` | `strict_current` | 10.555 | 0.651 | 16.211 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 19.238 | 0.571 | 33.721 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `classic` | `strict_current` | 19.238 | 0.651 | 29.547 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.393 | 0.629 | 13.349 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `ax` | `strict_current` | 8.393 | 0.678 | 12.373 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.609 | 0.629 | 24.826 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `classic` | `strict_current` | 15.609 | 0.678 | 23.011 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 8.148 | 0.575 | 14.182 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `ax` | `strict_current` | 8.148 | 2.247 | 3.625 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 57.486 | 0.575 | 100.062 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `classic` | `strict_current` | 57.486 | 2.247 | 25.579 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.278 | 0.573 | 14.442 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `ax` | `strict_current` | 8.278 | 2.394 | 3.458 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 59.859 | 0.573 | 104.438 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `classic` | `strict_current` | 59.859 | 2.394 | 25.003 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.270 | 0.686 | 12.049 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `ax` | `strict_current` | 8.270 | 2.881 | 2.870 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 52.520 | 0.686 | 76.520 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `classic` | `strict_current` | 52.520 | 2.881 | 18.228 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.751 | 0.652 | 13.424 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `ax` | `strict_current` | 8.751 | 2.374 | 3.687 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 57.247 | 0.652 | 87.815 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `classic` | `strict_current` | 57.247 | 2.374 | 24.118 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 19.411 | 0.626 | 30.986 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 19.411 | 0.814 | 23.859 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 35.524 | 0.626 | 56.706 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 35.524 | 0.814 | 43.663 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.695 | 0.547 | 19.556 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `ax` | `strict_current` | 10.695 | 0.652 | 16.404 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 36.043 | 0.547 | 65.906 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `classic` | `strict_current` | 36.043 | 0.652 | 55.283 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.485 | 0.596 | 14.231 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `ax` | `strict_current` | 8.485 | 0.665 | 12.752 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.834 | 0.596 | 56.747 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `classic` | `strict_current` | 33.834 | 0.665 | 50.847 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 23.891 | 0.721 | 33.122 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `ax` | `strict_current` | 23.891 | 0.734 | 32.537 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 36.137 | 0.721 | 50.100 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `classic` | `strict_current` | 36.137 | 0.734 | 49.214 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.158 | 1.152 | 7.946 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `ax` | `strict_current` | 9.158 | 4.411 | 2.076 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 31.362 | 1.152 | 27.212 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `classic` | `strict_current` | 31.362 | 4.411 | 7.111 |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 15.621 | 2.286 | 6.833 |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `ax` | `strict_current` | 15.621 | 5.506 | 2.837 |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 37.278 | 2.286 | 16.307 |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `classic` | `strict_current` | 37.278 | 5.506 | 6.771 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 8.859 | 0.537 | 16.502 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `ax` | `strict_current` | 8.859 | 0.743 | 11.920 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 35.042 | 0.537 | 65.274 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `classic` | `strict_current` | 35.042 | 0.743 | 47.150 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.825 | 0.577 | 17.029 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `ax` | `strict_current` | 9.825 | 0.703 | 13.969 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 35.451 | 0.577 | 61.441 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `classic` | `strict_current` | 35.451 | 0.703 | 50.400 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.622 | 0.535 | 14.236 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `ax` | `strict_current` | 7.622 | 0.731 | 10.431 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 32.025 | 0.535 | 59.815 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `classic` | `strict_current` | 32.025 | 0.731 | 43.830 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.711 | 0.661 | 13.185 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `ax` | `strict_current` | 8.711 | 0.786 | 11.088 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 35.256 | 0.661 | 53.366 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `classic` | `strict_current` | 35.256 | 0.786 | 44.879 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 9.070 | 0.470 | 19.309 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `ax` | `strict_current` | 9.070 | 0.763 | 11.883 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 33.808 | 0.470 | 71.971 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `classic` | `strict_current` | 33.808 | 0.763 | 44.293 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.002 | 0.535 | 16.817 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `ax` | `strict_current` | 9.002 | 0.574 | 15.686 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 32.509 | 0.535 | 60.731 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `classic` | `strict_current` | 32.509 | 0.574 | 56.646 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.424 | 0.742 | 11.361 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `ax` | `strict_current` | 8.424 | 0.682 | 12.344 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 34.527 | 0.742 | 46.563 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `classic` | `strict_current` | 34.527 | 0.682 | 50.592 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.285 | 0.927 | 8.935 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `ax` | `strict_current` | 8.285 | 0.645 | 12.846 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.331 | 0.927 | 35.947 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `classic` | `strict_current` | 33.331 | 0.645 | 51.679 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 20.571 | 0.821 | 25.064 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `ax` | `strict_current` | 20.571 | 1.421 | 14.475 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 19.540 | 0.821 | 23.808 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `classic` | `strict_current` | 19.540 | 1.421 | 13.749 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.850 | 1.320 | 5.948 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `ax` | `strict_current` | 7.850 | 1.483 | 5.293 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 17.821 | 1.320 | 13.502 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `classic` | `strict_current` | 17.821 | 1.483 | 12.016 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 19.663 | 0.843 | 23.335 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `ax` | `strict_current` | 19.663 | 0.797 | 24.665 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 18.706 | 0.843 | 22.199 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `classic` | `strict_current` | 18.706 | 0.797 | 23.465 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.416 | 1.322 | 6.367 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `ax` | `strict_current` | 8.416 | 1.451 | 5.801 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 17.785 | 1.322 | 13.455 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `classic` | `strict_current` | 17.785 | 1.451 | 12.260 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 11.067 | 9.831 | 1.126 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `ax` | `strict_current` | 11.067 | 128.819 | 0.086 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 50.995 | 9.831 | 5.187 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `classic` | `strict_current` | 50.995 | 128.819 | 0.396 |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.833 | 33.116 | 0.327 |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `ax` | `strict_current` | 10.833 | 149.967 | 0.072 |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 48.727 | 33.116 | 1.471 |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `classic` | `strict_current` | 48.727 | 149.967 | 0.325 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 16.457 | 1.002 | 16.423 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `ax` | `strict_current` | 16.457 | 1.491 | 11.039 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 16.527 | 1.002 | 16.493 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `classic` | `strict_current` | 16.527 | 1.491 | 11.085 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 18.595 | 0.859 | 21.638 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `ax` | `strict_current` | 18.595 | 1.923 | 9.668 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 16.574 | 0.859 | 19.286 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `classic` | `strict_current` | 16.574 | 1.923 | 8.617 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.950 | 0.784 | 10.146 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `ax` | `strict_current` | 7.950 | 1.642 | 4.842 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 18.713 | 0.784 | 23.882 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `classic` | `strict_current` | 18.713 | 1.642 | 11.397 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.806 | 0.829 | 10.617 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `ax` | `strict_current` | 8.806 | 1.509 | 5.836 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 18.689 | 0.829 | 22.534 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `classic` | `strict_current` | 18.689 | 1.509 | 12.386 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.068 | 0.605 | 11.684 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.068 | 1.002 | 7.055 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 33.016 | 0.605 | 54.582 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `classic` | `strict_current` | 33.016 | 1.002 | 32.955 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.389 | 0.633 | 13.249 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `ax` | `strict_current` | 8.389 | 0.986 | 8.504 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 38.133 | 0.633 | 60.224 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `classic` | `strict_current` | 38.133 | 0.986 | 38.657 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 11.801 | 0.557 | 21.192 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `ax` | `strict_current` | 11.801 | 1.566 | 7.534 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 36.775 | 0.557 | 66.037 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `classic` | `strict_current` | 36.775 | 1.566 | 23.476 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.553 | 0.677 | 15.596 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `ax` | `strict_current` | 10.553 | 1.109 | 9.517 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 42.478 | 0.677 | 62.778 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `classic` | `strict_current` | 42.478 | 1.109 | 38.307 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.667 | 0.739 | 10.377 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.667 | 0.823 | 9.320 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 33.507 | 0.739 | 45.349 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 33.507 | 0.823 | 40.729 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.521 | 0.752 | 11.331 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `ax` | `strict_current` | 8.521 | 0.784 | 10.865 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 34.215 | 0.752 | 45.498 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `classic` | `strict_current` | 34.215 | 0.784 | 43.627 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.480 | 0.880 | 10.772 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 9.480 | 0.766 | 12.371 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 34.257 | 0.880 | 38.929 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 34.257 | 0.766 | 44.707 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.598 | 0.716 | 12.000 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `ax` | `strict_current` | 8.598 | 1.063 | 8.088 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 34.669 | 0.716 | 48.387 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `classic` | `strict_current` | 34.669 | 1.063 | 32.612 |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.650 | 1.630 | 4.080 |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.650 | 4.371 | 1.521 |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 29.581 | 1.630 | 18.146 |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `classic` | `strict_current` | 29.581 | 4.371 | 6.767 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 13.211 | 2.207 | 5.986 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `ax` | `strict_current` | 13.211 | 5.610 | 2.355 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 34.192 | 2.207 | 15.493 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `classic` | `strict_current` | 34.192 | 5.610 | 6.095 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.837 | 2.060 | 3.805 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `ax` | `strict_current` | 7.837 | 3.271 | 2.396 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 29.237 | 2.060 | 14.195 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `classic` | `strict_current` | 29.237 | 3.271 | 8.937 |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.831 | 2.106 | 3.719 |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `ax` | `strict_current` | 7.831 | 3.317 | 2.361 |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 28.789 | 2.106 | 13.672 |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `classic` | `strict_current` | 28.789 | 3.317 | 8.680 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 21.853 | 0.662 | 33.011 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 21.853 | 0.745 | 29.346 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 37.128 | 0.662 | 56.084 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 37.128 | 0.745 | 49.856 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.285 | 0.573 | 16.210 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `ax` | `strict_current` | 9.285 | 0.734 | 12.643 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 32.411 | 0.573 | 56.587 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `classic` | `strict_current` | 32.411 | 0.734 | 44.133 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 23.761 | 0.600 | 39.574 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `ax` | `strict_current` | 23.761 | 0.756 | 31.413 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 39.851 | 0.600 | 66.373 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `classic` | `strict_current` | 39.851 | 0.756 | 52.686 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.383 | 0.608 | 13.778 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `ax` | `strict_current` | 8.383 | 0.910 | 9.212 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.218 | 0.608 | 54.595 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `classic` | `strict_current` | 33.218 | 0.910 | 36.505 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.508 | 0.522 | 14.390 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.508 | 1.350 | 5.560 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 31.519 | 0.522 | 60.409 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `classic` | `strict_current` | 31.519 | 1.350 | 23.339 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.461 | 0.607 | 15.575 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `ax` | `strict_current` | 9.461 | 1.473 | 6.425 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 32.104 | 0.607 | 52.848 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `classic` | `strict_current` | 32.104 | 1.473 | 21.802 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.551 | 0.637 | 13.424 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `ax` | `strict_current` | 8.551 | 1.405 | 6.088 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 30.615 | 0.637 | 48.062 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `classic` | `strict_current` | 30.615 | 1.405 | 21.796 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.363 | 0.690 | 12.116 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `ax` | `strict_current` | 8.363 | 1.418 | 5.900 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 32.217 | 0.690 | 46.674 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `classic` | `strict_current` | 32.217 | 1.418 | 22.727 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 19.050 | 1.260 | 15.121 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 19.050 | 1.040 | 18.313 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 18.350 | 1.260 | 14.565 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 18.350 | 1.040 | 17.640 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 18.165 | 1.137 | 15.974 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `ax` | `strict_current` | 18.165 | 1.303 | 13.941 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 17.224 | 1.137 | 15.147 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `classic` | `strict_current` | 17.224 | 1.303 | 13.219 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.808 | 0.834 | 8.159 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 6.808 | 1.075 | 6.335 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 17.046 | 0.834 | 20.428 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 17.046 | 1.075 | 15.860 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.247 | 0.919 | 8.971 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `ax` | `strict_current` | 8.247 | 1.017 | 8.110 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 19.031 | 0.919 | 20.701 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `classic` | `strict_current` | 19.031 | 1.017 | 18.714 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 8.913 | 0.613 | 14.528 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `ax` | `strict_current` | 8.913 | 0.890 | 10.009 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 34.584 | 0.613 | 56.373 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `classic` | `strict_current` | 34.584 | 0.890 | 38.837 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.493 | 0.932 | 8.043 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `ax` | `strict_current` | 7.493 | 0.778 | 9.637 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 35.299 | 0.932 | 37.890 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `classic` | `strict_current` | 35.299 | 0.778 | 45.400 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.987 | 0.698 | 11.447 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `ax` | `strict_current` | 7.987 | 0.782 | 10.208 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 32.630 | 0.698 | 46.765 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `classic` | `strict_current` | 32.630 | 0.782 | 41.705 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.798 | 0.631 | 12.350 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `ax` | `strict_current` | 7.798 | 0.826 | 9.441 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 32.174 | 0.631 | 50.953 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `classic` | `strict_current` | 32.174 | 0.826 | 38.953 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.167 | 0.737 | 9.719 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.167 | 0.852 | 8.408 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 18.975 | 0.737 | 25.731 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 18.975 | 0.852 | 22.260 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.976 | 0.668 | 13.435 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `ax` | `strict_current` | 8.976 | 0.799 | 11.232 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 18.649 | 0.668 | 27.915 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `classic` | `strict_current` | 18.649 | 0.799 | 23.337 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.703 | 0.648 | 13.429 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `ax` | `strict_current` | 8.703 | 0.672 | 12.946 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 18.689 | 0.648 | 28.838 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `classic` | `strict_current` | 18.689 | 0.672 | 27.801 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.001 | 0.968 | 9.294 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `ax` | `strict_current` | 9.001 | 0.723 | 12.455 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 21.901 | 0.968 | 22.614 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `classic` | `strict_current` | 21.901 | 0.723 | 30.306 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 4.284 | 103.312 | 0.041 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `ax` | `strict_current` | 4.284 | 110.725 | 0.039 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 17.751 | 103.312 | 0.172 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `classic` | `strict_current` | 17.751 | 110.725 | 0.160 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.045 | 76.879 | 0.066 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `ax` | `strict_current` | 5.045 | 172.800 | 0.029 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 16.514 | 76.879 | 0.215 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `classic` | `strict_current` | 16.514 | 172.800 | 0.096 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 4.776 | 81.341 | 0.059 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `ax` | `strict_current` | 4.776 | 81.915 | 0.058 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 17.305 | 81.341 | 0.213 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `classic` | `strict_current` | 17.305 | 81.915 | 0.211 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 4.411 | 76.428 | 0.058 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `ax` | `strict_current` | 4.411 | 98.822 | 0.045 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 16.708 | 76.428 | 0.219 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `classic` | `strict_current` | 16.708 | 98.822 | 0.169 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 10.692 | 8.425 | 1.269 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `ax` | `strict_current` | 10.692 | 70.423 | 0.152 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 17.432 | 8.425 | 2.069 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `classic` | `strict_current` | 17.432 | 70.423 | 0.248 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 4.204 | 8.226 | 0.511 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `ax` | `strict_current` | 4.204 | 117.164 | 0.036 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 16.067 | 8.226 | 1.953 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `classic` | `strict_current` | 16.067 | 117.164 | 0.137 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 4.381 | 9.300 | 0.471 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `ax` | `strict_current` | 4.381 | 122.388 | 0.036 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 16.012 | 9.300 | 1.722 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `classic` | `strict_current` | 16.012 | 122.388 | 0.131 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.385 | 8.350 | 1.244 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `ax` | `strict_current` | 10.385 | 93.241 | 0.111 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 17.925 | 8.350 | 2.147 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `classic` | `strict_current` | 17.925 | 93.241 | 0.192 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 9.957 | 0.697 | 14.283 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `ax` | `strict_current` | 9.957 | 1.722 | 5.781 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 19.344 | 0.697 | 27.746 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `classic` | `strict_current` | 19.344 | 1.722 | 11.231 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.690 | 0.762 | 11.407 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `ax` | `strict_current` | 8.690 | 1.182 | 7.352 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 19.263 | 0.762 | 25.285 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `classic` | `strict_current` | 19.263 | 1.182 | 16.297 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.499 | 0.457 | 16.421 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `ax` | `strict_current` | 7.499 | 0.943 | 7.951 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 20.271 | 0.457 | 44.390 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `classic` | `strict_current` | 20.271 | 0.943 | 21.495 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.110 | 0.806 | 11.308 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `ax` | `strict_current` | 9.110 | 0.817 | 11.149 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 19.458 | 0.806 | 24.153 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `classic` | `strict_current` | 19.458 | 0.817 | 23.815 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 26.003 | 2.337 | 11.127 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 26.003 | 9.875 | 2.633 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 146.062 | 2.337 | 62.500 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 146.062 | 9.875 | 14.791 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 23.216 | 5.781 | 4.016 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `ax` | `strict_current` | 23.216 | 12.086 | 1.921 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 152.460 | 5.781 | 26.375 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `classic` | `strict_current` | 152.460 | 12.086 | 12.615 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 25.010 | 3.958 | 6.319 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 25.010 | 9.049 | 2.764 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 142.085 | 3.958 | 35.901 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 142.085 | 9.049 | 15.702 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 31.959 | 3.200 | 9.987 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `ax` | `strict_current` | 31.959 | 10.434 | 3.063 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 140.301 | 3.200 | 43.844 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `classic` | `strict_current` | 140.301 | 10.434 | 13.447 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.332 | 0.589 | 15.852 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `ax` | `strict_current` | 9.332 | 0.546 | 17.092 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 35.299 | 0.589 | 59.959 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `classic` | `strict_current` | 35.299 | 0.546 | 64.647 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.480 | 0.480 | 21.814 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `ax` | `strict_current` | 10.480 | 0.568 | 18.464 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 30.740 | 0.480 | 63.989 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `classic` | `strict_current` | 30.740 | 0.568 | 54.161 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.536 | 0.692 | 13.779 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `ax` | `strict_current` | 9.536 | 0.524 | 18.210 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 35.319 | 0.692 | 51.034 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `classic` | `strict_current` | 35.319 | 0.524 | 67.447 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 21.867 | 1.340 | 16.316 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `ax` | `strict_current` | 21.867 | 1.465 | 14.929 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 35.814 | 1.340 | 26.722 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `classic` | `strict_current` | 35.814 | 1.465 | 24.450 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.761 | 1.086 | 8.070 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `ax` | `strict_current` | 8.761 | 0.897 | 9.770 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 35.285 | 1.086 | 32.503 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `classic` | `strict_current` | 35.285 | 0.897 | 39.352 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.008 | 0.839 | 10.739 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `ax` | `strict_current` | 9.008 | 0.910 | 9.903 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.419 | 0.839 | 39.844 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `classic` | `strict_current` | 33.419 | 0.910 | 36.742 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 21.585 | 0.803 | 26.885 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `ax` | `strict_current` | 21.585 | 0.859 | 25.124 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 34.095 | 0.803 | 42.467 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `classic` | `strict_current` | 34.095 | 0.859 | 39.685 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 11.713 | 0.823 | 14.229 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `ax` | `strict_current` | 11.713 | 0.789 | 14.845 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 36.483 | 0.823 | 44.319 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `classic` | `strict_current` | 36.483 | 0.789 | 46.237 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.483 | 0.624 | 16.808 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `ax` | `strict_current` | 10.483 | 0.750 | 13.983 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 35.454 | 0.624 | 56.848 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `classic` | `strict_current` | 35.454 | 0.750 | 47.291 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.522 | 0.645 | 13.213 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `ax` | `strict_current` | 8.522 | 0.928 | 9.184 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 32.685 | 0.645 | 50.672 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `classic` | `strict_current` | 32.685 | 0.928 | 35.223 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.937 | 0.633 | 14.111 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `ax` | `strict_current` | 8.937 | 0.964 | 9.273 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 32.601 | 0.633 | 51.477 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `classic` | `strict_current` | 32.601 | 0.964 | 33.828 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 9.039 | 0.958 | 9.435 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `ax` | `strict_current` | 9.039 | 1.022 | 8.847 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 19.664 | 0.958 | 20.526 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `classic` | `strict_current` | 19.664 | 1.022 | 19.247 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.152 | 0.622 | 14.713 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `ax` | `strict_current` | 9.152 | 0.903 | 10.137 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 19.004 | 0.622 | 30.552 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `classic` | `strict_current` | 19.004 | 0.903 | 21.050 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.006 | 0.579 | 13.824 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `ax` | `strict_current` | 8.006 | 0.829 | 9.662 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 17.434 | 0.579 | 30.103 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `classic` | `strict_current` | 17.434 | 0.829 | 21.040 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.937 | 0.650 | 13.741 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `ax` | `strict_current` | 8.937 | 0.854 | 10.466 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 18.356 | 0.650 | 28.223 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `classic` | `strict_current` | 18.356 | 0.854 | 21.497 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 20.258 | 0.650 | 31.148 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `ax` | `strict_current` | 20.258 | 1.169 | 17.328 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 33.637 | 0.650 | 51.719 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `classic` | `strict_current` | 33.637 | 1.169 | 28.772 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.620 | 0.675 | 15.722 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `ax` | `strict_current` | 10.620 | 1.431 | 7.424 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.149 | 0.675 | 49.074 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `classic` | `strict_current` | 33.149 | 1.431 | 23.172 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 22.892 | 0.836 | 27.399 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `ax` | `strict_current` | 22.892 | 1.501 | 15.253 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 35.800 | 0.836 | 42.848 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `classic` | `strict_current` | 35.800 | 1.501 | 23.853 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 21.210 | 0.847 | 25.041 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `ax` | `strict_current` | 21.210 | 1.301 | 16.297 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.877 | 0.847 | 39.997 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `classic` | `strict_current` | 33.877 | 1.301 | 26.031 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 16.832 | 0.634 | 26.531 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `ax` | `strict_current` | 16.832 | 0.567 | 29.661 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 15.530 | 0.634 | 24.479 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `classic` | `strict_current` | 15.530 | 0.567 | 27.367 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.969 | 0.918 | 10.864 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `ax` | `strict_current` | 9.969 | 0.912 | 10.935 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 20.661 | 0.918 | 22.517 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `classic` | `strict_current` | 20.661 | 0.912 | 22.665 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 21.591 | 0.635 | 34.007 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `ax` | `strict_current` | 21.591 | 0.559 | 38.657 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 20.181 | 0.635 | 31.786 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `classic` | `strict_current` | 20.181 | 0.559 | 36.133 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.030 | 0.488 | 18.510 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `ax` | `strict_current` | 9.030 | 0.612 | 14.746 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 17.031 | 0.488 | 34.913 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `classic` | `strict_current` | 17.031 | 0.612 | 27.813 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.584 | 1.187 | 6.390 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.584 | 2.140 | 3.544 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 31.904 | 1.187 | 26.884 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `classic` | `strict_current` | 31.904 | 2.140 | 14.911 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.583 | 1.560 | 6.782 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `ax` | `strict_current` | 10.583 | 1.953 | 5.418 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 34.512 | 1.560 | 22.117 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `classic` | `strict_current` | 34.512 | 1.953 | 17.668 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.658 | 0.980 | 7.812 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `ax` | `strict_current` | 7.658 | 1.926 | 3.976 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.016 | 0.980 | 33.682 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `classic` | `strict_current` | 33.016 | 1.926 | 17.144 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.274 | 1.229 | 6.731 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `ax` | `strict_current` | 8.274 | 2.076 | 3.985 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 32.062 | 1.229 | 26.082 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `classic` | `strict_current` | 32.062 | 2.076 | 15.442 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.633 | 0.640 | 15.058 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `ax` | `strict_current` | 9.633 | 0.707 | 13.626 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 39.165 | 0.640 | 61.221 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `classic` | `strict_current` | 39.165 | 0.707 | 55.400 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.715 | 0.813 | 11.949 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `ax` | `strict_current` | 9.715 | 1.405 | 6.916 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.879 | 0.813 | 41.671 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `classic` | `strict_current` | 33.879 | 1.405 | 24.118 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.130 | 0.939 | 9.719 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `ax` | `strict_current` | 9.130 | 1.218 | 7.494 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.907 | 0.939 | 16.932 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `classic` | `strict_current` | 15.907 | 1.218 | 13.056 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.897 | 0.744 | 11.954 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `ax` | `strict_current` | 8.897 | 0.734 | 12.114 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 18.650 | 0.744 | 25.057 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `classic` | `strict_current` | 18.650 | 0.734 | 25.393 |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.773 | 0.756 | 10.277 |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `ax` | `strict_current` | 7.773 | 0.753 | 10.326 |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.288 | 0.756 | 20.214 |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `classic` | `strict_current` | 15.288 | 0.753 | 20.310 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 9.183 | 0.969 | 9.481 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `ax` | `strict_current` | 9.183 | 1.349 | 6.807 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 18.879 | 0.969 | 19.492 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `classic` | `strict_current` | 18.879 | 1.349 | 13.993 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.242 | 0.663 | 15.437 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `ax` | `strict_current` | 10.242 | 0.623 | 16.437 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 19.813 | 0.663 | 29.864 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `classic` | `strict_current` | 19.813 | 0.623 | 31.797 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.809 | 0.688 | 11.348 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `ax` | `strict_current` | 7.809 | 0.681 | 11.463 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.087 | 0.688 | 21.925 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `classic` | `strict_current` | 15.087 | 0.681 | 22.146 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.183 | 0.637 | 12.850 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `ax` | `strict_current` | 8.183 | 0.812 | 10.081 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 18.862 | 0.637 | 29.620 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `classic` | `strict_current` | 18.862 | 0.812 | 23.237 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 11.407 | 0.979 | 11.652 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `ax` | `strict_current` | 11.407 | 1.481 | 7.704 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 37.172 | 0.979 | 37.968 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `classic` | `strict_current` | 37.172 | 1.481 | 25.104 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 11.423 | 0.685 | 16.685 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `ax` | `strict_current` | 11.423 | 1.105 | 10.337 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 42.016 | 0.685 | 61.371 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `classic` | `strict_current` | 42.016 | 1.105 | 38.021 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 12.224 | 1.215 | 10.057 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `ax` | `strict_current` | 12.224 | 1.378 | 8.868 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 40.408 | 1.215 | 33.245 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `classic` | `strict_current` | 40.408 | 1.378 | 29.316 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 11.158 | 0.666 | 16.766 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `ax` | `strict_current` | 11.158 | 1.263 | 8.837 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 37.069 | 0.666 | 55.698 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `classic` | `strict_current` | 37.069 | 1.263 | 29.359 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 8.436 | 3.122 | 2.702 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 8.436 | 3.365 | 2.507 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 27.304 | 3.122 | 8.745 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 27.304 | 3.365 | 8.114 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.430 | 0.850 | 8.738 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `ax` | `strict_current` | 7.430 | 2.773 | 2.679 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 29.447 | 0.850 | 34.628 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `classic` | `strict_current` | 29.447 | 2.773 | 10.618 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 34.405 | 1.416 | 24.304 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 34.405 | 3.137 | 10.969 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 55.546 | 1.416 | 39.238 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 55.546 | 3.137 | 17.709 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.700 | 0.886 | 8.691 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `ax` | `strict_current` | 7.700 | 2.844 | 2.707 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 29.620 | 0.886 | 33.433 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `classic` | `strict_current` | 29.620 | 2.844 | 10.413 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 8.616 | 0.564 | 15.270 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `ax` | `strict_current` | 8.616 | 1.517 | 5.681 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 34.024 | 0.564 | 60.301 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `classic` | `strict_current` | 34.024 | 1.517 | 22.433 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.843 | 0.613 | 11.165 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `ax` | `strict_current` | 6.843 | 1.293 | 5.292 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 31.573 | 0.613 | 51.513 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `classic` | `strict_current` | 31.573 | 1.293 | 24.414 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.313 | 0.561 | 14.810 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `ax` | `strict_current` | 8.313 | 1.841 | 4.514 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 31.152 | 0.561 | 55.501 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `classic` | `strict_current` | 31.152 | 1.841 | 16.918 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.952 | 0.594 | 13.391 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `ax` | `strict_current` | 7.952 | 1.272 | 6.252 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 31.055 | 0.594 | 52.297 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `classic` | `strict_current` | 31.055 | 1.272 | 24.415 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 22.811 | 0.631 | 36.151 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `ax` | `strict_current` | 22.811 | 0.699 | 32.618 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 39.307 | 0.631 | 62.293 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `classic` | `strict_current` | 39.307 | 0.699 | 56.206 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.510 | 0.532 | 14.116 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `ax` | `strict_current` | 7.510 | 0.777 | 9.669 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 34.319 | 0.532 | 64.512 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `classic` | `strict_current` | 34.319 | 0.777 | 44.188 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.253 | 0.456 | 22.488 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `ax` | `strict_current` | 10.253 | 0.527 | 19.466 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 29.041 | 0.456 | 63.695 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `classic` | `strict_current` | 29.041 | 0.527 | 55.133 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 25.706 | 0.798 | 32.220 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `ax` | `strict_current` | 25.706 | 0.620 | 41.443 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 38.373 | 0.798 | 48.097 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `classic` | `strict_current` | 38.373 | 0.620 | 61.866 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 8.307 | 0.834 | 9.965 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 8.307 | 0.578 | 14.371 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 32.743 | 0.834 | 39.276 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 32.743 | 0.578 | 56.644 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.357 | 0.577 | 14.471 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `ax` | `strict_current` | 8.357 | 0.788 | 10.605 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.282 | 0.577 | 57.631 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `classic` | `strict_current` | 33.282 | 0.788 | 42.236 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.152 | 0.531 | 15.354 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 8.152 | 0.560 | 14.554 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.220 | 0.531 | 62.571 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 33.220 | 0.560 | 59.309 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.780 | 0.631 | 13.917 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `ax` | `strict_current` | 8.780 | 0.583 | 15.060 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 34.986 | 0.631 | 55.457 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `classic` | `strict_current` | 34.986 | 0.583 | 60.009 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 20.285 | 1.143 | 17.751 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `ax` | `strict_current` | 20.285 | 0.989 | 20.508 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 19.406 | 1.143 | 16.981 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `classic` | `strict_current` | 19.406 | 0.989 | 19.619 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 19.571 | 0.961 | 20.369 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `ax` | `strict_current` | 19.571 | 1.124 | 17.409 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 18.800 | 0.961 | 19.566 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `classic` | `strict_current` | 18.800 | 1.124 | 16.723 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.620 | 0.839 | 10.269 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `ax` | `strict_current` | 8.620 | 1.105 | 7.800 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 20.289 | 0.839 | 24.170 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `classic` | `strict_current` | 20.289 | 1.105 | 18.359 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.090 | 0.590 | 12.021 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `ax` | `strict_current` | 7.090 | 0.863 | 8.218 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 22.396 | 0.590 | 37.973 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `classic` | `strict_current` | 22.396 | 0.863 | 25.961 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.165 | 0.616 | 11.629 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.165 | 0.679 | 10.550 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 32.317 | 0.616 | 52.456 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `classic` | `strict_current` | 32.317 | 0.679 | 47.589 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.695 | 0.651 | 11.825 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `ax` | `strict_current` | 7.695 | 0.695 | 11.071 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 32.942 | 0.651 | 50.625 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `classic` | `strict_current` | 32.942 | 0.695 | 47.396 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.530 | 0.713 | 13.366 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `ax` | `strict_current` | 9.530 | 0.655 | 14.552 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 31.885 | 0.713 | 44.718 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `classic` | `strict_current` | 31.885 | 0.655 | 48.687 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.521 | 0.664 | 14.341 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `ax` | `strict_current` | 9.521 | 0.810 | 11.757 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 31.509 | 0.664 | 47.462 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `classic` | `strict_current` | 31.509 | 0.810 | 38.908 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 9.126 | 0.793 | 11.514 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `ax` | `strict_current` | 9.126 | 1.572 | 5.806 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 34.961 | 0.793 | 44.108 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `classic` | `strict_current` | 34.961 | 1.572 | 22.241 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.302 | 0.871 | 9.534 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `ax` | `strict_current` | 8.302 | 1.169 | 7.102 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.314 | 0.871 | 38.260 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `classic` | `strict_current` | 33.314 | 1.169 | 28.500 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.277 | 0.851 | 12.077 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `ax` | `strict_current` | 10.277 | 1.208 | 8.505 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 39.985 | 0.851 | 46.989 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `classic` | `strict_current` | 39.985 | 1.208 | 33.091 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.974 | 0.694 | 11.487 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `ax` | `strict_current` | 7.974 | 0.737 | 10.825 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 34.146 | 0.694 | 49.189 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `classic` | `strict_current` | 34.146 | 0.737 | 46.357 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 22.285 | 0.998 | 22.329 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `ax` | `strict_current` | 22.285 | 0.905 | 24.617 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 22.641 | 0.998 | 22.686 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `classic` | `strict_current` | 22.641 | 0.905 | 25.011 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.076 | 0.799 | 12.618 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `ax` | `strict_current` | 10.076 | 0.787 | 12.801 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 20.467 | 0.799 | 25.631 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `classic` | `strict_current` | 20.467 | 0.787 | 26.003 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.240 | 1.037 | 7.946 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `ax` | `strict_current` | 8.240 | 1.029 | 8.009 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 21.295 | 1.037 | 20.534 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `classic` | `strict_current` | 21.295 | 1.029 | 20.697 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 18.635 | 0.931 | 20.027 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `ax` | `strict_current` | 18.635 | 1.193 | 15.616 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 17.075 | 0.931 | 18.350 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `classic` | `strict_current` | 17.075 | 1.193 | 14.308 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 10.588 | 0.829 | 12.769 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `ax` | `strict_current` | 10.588 | 1.304 | 8.118 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 41.387 | 0.829 | 49.915 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `classic` | `strict_current` | 41.387 | 1.304 | 31.733 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.642 | 1.107 | 9.617 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `ax` | `strict_current` | 10.642 | 1.461 | 7.283 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 37.521 | 1.107 | 33.906 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `classic` | `strict_current` | 37.521 | 1.461 | 25.678 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 11.793 | 0.688 | 17.152 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `ax` | `strict_current` | 11.793 | 1.162 | 10.150 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 42.297 | 0.688 | 61.516 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `classic` | `strict_current` | 42.297 | 1.162 | 36.403 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.365 | 0.723 | 14.342 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `ax` | `strict_current` | 10.365 | 1.450 | 7.150 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 39.551 | 0.723 | 54.726 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `classic` | `strict_current` | 39.551 | 1.450 | 27.283 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 8.149 | 1.881 | 4.333 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 8.149 | 4.078 | 1.998 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 31.573 | 1.881 | 16.788 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 31.573 | 4.078 | 7.742 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.356 | 1.757 | 4.755 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `ax` | `strict_current` | 8.356 | 3.872 | 2.158 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 29.594 | 1.757 | 16.842 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `classic` | `strict_current` | 29.594 | 3.872 | 7.642 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.387 | 1.545 | 6.074 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `ax` | `strict_current` | 9.387 | 3.971 | 2.364 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 31.788 | 1.545 | 20.569 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `classic` | `strict_current` | 31.788 | 3.971 | 8.005 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.064 | 1.408 | 5.728 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `ax` | `strict_current` | 8.064 | 4.021 | 2.005 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 30.391 | 1.408 | 21.589 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `classic` | `strict_current` | 30.391 | 4.021 | 7.558 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 20.928 | 0.633 | 33.038 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `ax` | `strict_current` | 20.928 | 0.715 | 29.274 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 33.659 | 0.633 | 53.134 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `classic` | `strict_current` | 33.659 | 0.715 | 47.081 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 22.225 | 1.126 | 19.731 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `ax` | `strict_current` | 22.225 | 1.167 | 19.044 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 35.656 | 1.126 | 31.655 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `classic` | `strict_current` | 35.656 | 1.167 | 30.552 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.181 | 0.552 | 14.832 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `ax` | `strict_current` | 8.181 | 0.872 | 9.379 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 34.874 | 0.552 | 63.229 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `classic` | `strict_current` | 34.874 | 0.872 | 39.983 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.912 | 0.673 | 16.221 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `ax` | `strict_current` | 10.912 | 1.001 | 10.900 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 34.076 | 0.673 | 50.656 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `classic` | `strict_current` | 34.076 | 1.001 | 34.039 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 8.139 | 1.964 | 4.144 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 8.139 | 3.297 | 2.468 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 31.085 | 1.964 | 15.827 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 31.085 | 3.297 | 9.428 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.001 | 3.302 | 2.423 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `ax` | `strict_current` | 8.001 | 4.047 | 1.977 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 28.850 | 3.302 | 8.737 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `classic` | `strict_current` | 28.850 | 4.047 | 7.128 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.453 | 2.323 | 3.208 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `ax` | `strict_current` | 7.453 | 4.113 | 1.812 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.095 | 2.323 | 14.246 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `classic` | `strict_current` | 33.095 | 4.113 | 8.047 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.542 | 1.460 | 5.165 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `ax` | `strict_current` | 7.542 | 2.944 | 2.562 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 38.063 | 1.460 | 26.065 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `classic` | `strict_current` | 38.063 | 2.944 | 12.931 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 33.661 | 1.699 | 19.808 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `ax` | `strict_current` | 33.661 | 9.063 | 3.714 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 91.299 | 1.699 | 53.726 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `classic` | `strict_current` | 91.299 | 9.063 | 10.073 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 29.873 | 3.128 | 9.549 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `ax` | `strict_current` | 29.873 | 11.479 | 2.602 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 106.013 | 3.128 | 33.887 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `classic` | `strict_current` | 106.013 | 11.479 | 9.235 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.298 | 1.095 | 7.575 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `ax` | `strict_current` | 8.298 | 1.403 | 5.913 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 32.774 | 1.095 | 29.920 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `classic` | `strict_current` | 32.774 | 1.403 | 23.354 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.461 | 0.558 | 15.153 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `ax` | `strict_current` | 8.461 | 1.488 | 5.684 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 31.910 | 0.558 | 57.148 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `classic` | `strict_current` | 31.910 | 1.488 | 21.439 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.302 | 5.878 | 1.582 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `ax` | `strict_current` | 9.302 | 4.003 | 2.324 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.276 | 5.878 | 4.470 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `classic` | `strict_current` | 26.276 | 4.003 | 6.564 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.947 | 8.877 | 1.008 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `ax` | `strict_current` | 8.947 | 9.903 | 0.903 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.266 | 8.877 | 3.071 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `classic` | `strict_current` | 27.266 | 9.903 | 2.753 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.883 | 0.578 | 15.377 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `ax` | `strict_current` | 8.883 | 1.271 | 6.990 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 36.586 | 0.578 | 63.334 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `classic` | `strict_current` | 36.586 | 1.271 | 28.792 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.292 | 0.689 | 14.948 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `ax` | `strict_current` | 10.292 | 1.369 | 7.516 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 36.732 | 0.689 | 53.346 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `classic` | `strict_current` | 36.732 | 1.369 | 26.823 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.305 | 0.828 | 10.036 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `ax` | `strict_current` | 8.305 | 0.782 | 10.619 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 34.561 | 0.828 | 41.761 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `classic` | `strict_current` | 34.561 | 0.782 | 44.187 |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.032 | 0.750 | 12.037 |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `ax` | `strict_current` | 9.032 | 0.757 | 11.925 |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 35.821 | 0.750 | 47.739 |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `classic` | `strict_current` | 35.821 | 0.757 | 47.295 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.550 | 0.674 | 12.680 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `ax` | `strict_current` | 8.550 | 1.383 | 6.181 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.037 | 0.674 | 48.998 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `classic` | `strict_current` | 33.037 | 1.383 | 23.886 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.087 | 0.607 | 14.975 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `ax` | `strict_current` | 9.087 | 1.405 | 6.469 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 31.077 | 0.607 | 51.213 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `classic` | `strict_current` | 31.077 | 1.405 | 22.123 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 11.289 | 1.146 | 9.846 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `ax` | `strict_current` | 11.289 | 1.455 | 7.757 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 36.686 | 1.146 | 31.998 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `classic` | `strict_current` | 36.686 | 1.455 | 25.207 |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.759 | 1.110 | 7.888 |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `ax` | `strict_current` | 8.759 | 1.711 | 5.118 |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 32.808 | 1.110 | 29.545 |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `classic` | `strict_current` | 32.808 | 1.711 | 19.170 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.641 | 96.532 | 0.079 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `ax` | `strict_current` | 7.641 | 97.329 | 0.079 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.018 | 96.532 | 0.342 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `classic` | `strict_current` | 33.018 | 97.329 | 0.339 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.990 | 54.861 | 0.146 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `ax` | `strict_current` | 7.990 | 46.755 | 0.171 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 35.193 | 54.861 | 0.641 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `classic` | `strict_current` | 35.193 | 46.755 | 0.753 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 11.327 | 1.423 | 7.961 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `ax` | `strict_current` | 11.327 | 2.382 | 4.756 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 32.393 | 1.423 | 22.766 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `classic` | `strict_current` | 32.393 | 2.382 | 13.601 |
| `vbr1_l2_event_controller` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.529 | 2.008 | 4.247 |
| `vbr1_l2_event_controller` | `tb` | `gold` | `ax` | `strict_current` | 8.529 | 2.425 | 3.517 |
| `vbr1_l2_event_controller` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 35.444 | 2.008 | 17.648 |
| `vbr1_l2_event_controller` | `tb` | `gold` | `classic` | `strict_current` | 35.444 | 2.425 | 14.614 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.793 | 0.851 | 10.338 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `ax` | `strict_current` | 8.793 | 1.622 | 5.421 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 32.152 | 0.851 | 37.802 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `classic` | `strict_current` | 32.152 | 1.622 | 19.822 |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.014 | 0.687 | 11.673 |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `ax` | `strict_current` | 8.014 | 1.477 | 5.426 |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 32.438 | 0.687 | 47.246 |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `classic` | `strict_current` | 32.438 | 1.477 | 21.961 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.729 | 9.362 | 1.039 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `ax` | `strict_current` | 9.729 | 128.097 | 0.076 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 45.237 | 9.362 | 4.832 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `classic` | `strict_current` | 45.237 | 128.097 | 0.353 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 11.051 | 33.137 | 0.333 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `ax` | `strict_current` | 11.051 | 153.491 | 0.072 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 49.652 | 33.137 | 1.498 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `classic` | `strict_current` | 49.652 | 153.491 | 0.323 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.960 | 1.338 | 5.200 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `ax` | `strict_current` | 6.960 | 2.110 | 3.298 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 35.376 | 1.338 | 26.433 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `classic` | `strict_current` | 35.376 | 2.110 | 16.763 |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.625 | 1.347 | 6.403 |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `ax` | `strict_current` | 8.625 | 2.129 | 4.051 |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 31.153 | 1.347 | 23.127 |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `classic` | `strict_current` | 31.153 | 2.129 | 14.633 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.579 | 25.062 | 0.223 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `ax` | `strict_current` | 5.579 | 25.028 | 0.223 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 75.773 | 25.062 | 3.023 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `classic` | `strict_current` | 75.773 | 25.028 | 3.028 |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.642 | 37.297 | 0.151 |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `ax` | `strict_current` | 5.642 | 75.211 | 0.075 |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 18.828 | 37.297 | 0.505 |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `classic` | `strict_current` | 18.828 | 75.211 | 0.250 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.859 | 1.241 | 7.137 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `ax` | `strict_current` | 8.859 | 1.831 | 4.838 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.766 | 1.241 | 27.204 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `classic` | `strict_current` | 33.766 | 1.831 | 18.441 |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.652 | 0.935 | 8.182 |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `ax` | `strict_current` | 7.652 | 1.869 | 4.095 |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 31.186 | 0.935 | 33.345 |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `classic` | `strict_current` | 31.186 | 1.869 | 16.688 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.106 | 1.722 | 3.546 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `ax` | `strict_current` | 6.106 | 17.412 | 0.351 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 40.718 | 1.722 | 23.648 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `classic` | `strict_current` | 40.718 | 17.412 | 2.339 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.024 | 7.606 | 0.792 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `ax` | `strict_current` | 6.024 | 25.830 | 0.233 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 40.533 | 7.606 | 5.329 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `classic` | `strict_current` | 40.533 | 25.830 | 1.569 |

## Accuracy-Gated Speedups

| Entry | Form | Variant | Spectre mode | EVAS mode | Spectre wall s | EVAS wall s | Spectre/EVAS |
| --- | --- | --- | --- | --- | ---: | ---: | ---: |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.872 | 1.519 | 5.184 |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.872 | 1.097 | 7.175 |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 30.752 | 1.519 | 20.250 |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `classic` | `strict_current` | 30.752 | 1.097 | 28.029 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.463 | 0.916 | 9.236 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `ax` | `strict_current` | 8.463 | 1.288 | 6.573 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.767 | 0.916 | 36.851 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `classic` | `strict_current` | 33.767 | 1.288 | 26.225 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.121 | 0.731 | 11.113 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `ax` | `strict_current` | 8.121 | 1.114 | 7.287 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 31.574 | 0.731 | 43.209 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `classic` | `strict_current` | 31.574 | 1.114 | 28.334 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.481 | 1.078 | 9.720 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `ax` | `strict_current` | 10.481 | 1.173 | 8.934 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.946 | 1.078 | 31.482 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `classic` | `strict_current` | 33.946 | 1.173 | 28.936 |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 9.853 | 1.500 | 6.567 |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 9.853 | 10.180 | 0.968 |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 44.307 | 1.500 | 29.529 |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 44.307 | 10.180 | 4.352 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 13.578 | 1.195 | 11.367 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `ax` | `strict_current` | 13.578 | 10.711 | 1.268 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 41.046 | 1.195 | 34.361 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `classic` | `strict_current` | 41.046 | 10.711 | 3.832 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.444 | 1.910 | 4.421 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `ax` | `strict_current` | 8.444 | 1.543 | 5.472 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.171 | 1.910 | 17.367 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `classic` | `strict_current` | 33.171 | 1.543 | 21.495 |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.653 | 1.428 | 6.759 |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `ax` | `strict_current` | 9.653 | 1.828 | 5.282 |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.741 | 1.428 | 23.626 |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `classic` | `strict_current` | 33.741 | 1.828 | 18.461 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 23.401 | 0.783 | 29.903 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `ax` | `strict_current` | 23.401 | 0.730 | 32.056 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 34.996 | 0.783 | 44.719 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `classic` | `strict_current` | 34.996 | 0.730 | 47.939 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 20.395 | 0.508 | 40.143 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `ax` | `strict_current` | 20.395 | 0.583 | 35.005 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 35.069 | 0.508 | 69.024 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `classic` | `strict_current` | 35.069 | 0.583 | 60.189 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 23.583 | 0.575 | 40.980 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `ax` | `strict_current` | 23.583 | 0.602 | 39.158 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 37.017 | 0.575 | 64.323 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `classic` | `strict_current` | 37.017 | 0.602 | 61.462 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.834 | 0.755 | 13.021 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `ax` | `strict_current` | 9.834 | 0.722 | 13.615 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 34.671 | 0.755 | 45.909 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `classic` | `strict_current` | 34.671 | 0.722 | 48.003 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 11.711 | 0.879 | 13.318 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `ax` | `strict_current` | 11.711 | 1.059 | 11.054 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 41.692 | 0.879 | 47.416 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `classic` | `strict_current` | 41.692 | 1.059 | 39.355 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.323 | 1.123 | 9.191 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `ax` | `strict_current` | 10.323 | 1.267 | 8.146 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 43.619 | 1.123 | 38.832 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `classic` | `strict_current` | 43.619 | 1.267 | 34.420 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.509 | 1.078 | 8.823 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `ax` | `strict_current` | 9.509 | 1.224 | 7.767 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 36.980 | 1.078 | 34.313 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `classic` | `strict_current` | 36.980 | 1.224 | 30.205 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.916 | 0.554 | 14.278 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.916 | 1.350 | 5.862 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 31.451 | 0.554 | 56.727 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `classic` | `strict_current` | 31.451 | 1.350 | 23.291 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.925 | 0.970 | 8.166 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `ax` | `strict_current` | 7.925 | 1.315 | 6.025 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 31.600 | 0.970 | 32.562 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `classic` | `strict_current` | 31.600 | 1.315 | 24.023 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.231 | 1.006 | 8.178 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `ax` | `strict_current` | 8.231 | 1.451 | 5.673 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 32.305 | 1.006 | 32.096 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `classic` | `strict_current` | 32.305 | 1.451 | 22.264 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.241 | 0.587 | 12.336 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `ax` | `strict_current` | 7.241 | 1.384 | 5.231 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 30.452 | 0.587 | 51.876 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `classic` | `strict_current` | 30.452 | 1.384 | 22.000 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 8.307 | 1.565 | 5.308 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `ax` | `strict_current` | 8.307 | 3.260 | 2.548 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 29.370 | 1.565 | 18.766 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `classic` | `strict_current` | 29.370 | 3.260 | 9.010 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.540 | 1.990 | 3.788 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `ax` | `strict_current` | 7.540 | 3.767 | 2.001 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 36.232 | 1.990 | 18.204 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `classic` | `strict_current` | 36.232 | 3.767 | 9.617 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.624 | 2.514 | 3.032 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `ax` | `strict_current` | 7.624 | 3.594 | 2.121 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 30.384 | 2.514 | 12.085 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `classic` | `strict_current` | 30.384 | 3.594 | 8.454 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.173 | 2.070 | 4.431 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `ax` | `strict_current` | 9.173 | 3.691 | 2.485 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 29.177 | 2.070 | 14.094 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `classic` | `strict_current` | 29.177 | 3.691 | 7.904 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 9.178 | 0.732 | 12.534 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `ax` | `strict_current` | 9.178 | 1.387 | 6.615 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 31.510 | 0.732 | 43.032 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `classic` | `strict_current` | 31.510 | 1.387 | 22.711 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.967 | 1.086 | 8.257 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `ax` | `strict_current` | 8.967 | 1.567 | 5.722 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 30.999 | 1.086 | 28.546 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `classic` | `strict_current` | 30.999 | 1.567 | 19.782 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.730 | 0.617 | 12.523 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `ax` | `strict_current` | 7.730 | 1.264 | 6.116 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.114 | 0.617 | 53.645 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `classic` | `strict_current` | 33.114 | 1.264 | 26.196 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.201 | 0.740 | 11.077 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `ax` | `strict_current` | 8.201 | 2.036 | 4.028 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 32.111 | 0.740 | 43.372 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `classic` | `strict_current` | 32.111 | 2.036 | 15.770 |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 8.201 | 1.456 | 5.632 |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `ax` | `strict_current` | 8.201 | 4.987 | 1.645 |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 31.465 | 1.456 | 21.609 |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `classic` | `strict_current` | 31.465 | 4.987 | 6.309 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.546 | 1.120 | 6.739 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `ax` | `strict_current` | 7.546 | 4.455 | 1.694 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 31.939 | 1.120 | 28.521 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `classic` | `strict_current` | 31.939 | 4.455 | 7.170 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.593 | 1.157 | 6.561 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `ax` | `strict_current` | 7.593 | 4.025 | 1.886 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 30.968 | 1.157 | 26.757 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `classic` | `strict_current` | 30.968 | 4.025 | 7.693 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.873 | 1.150 | 7.714 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `ax` | `strict_current` | 8.873 | 3.868 | 2.294 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 32.010 | 1.150 | 27.830 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `classic` | `strict_current` | 32.010 | 3.868 | 8.275 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 8.419 | 0.888 | 9.478 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `ax` | `strict_current` | 8.419 | 1.354 | 6.220 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 31.684 | 0.888 | 35.670 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `classic` | `strict_current` | 31.684 | 1.354 | 23.408 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.760 | 0.689 | 12.721 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `ax` | `strict_current` | 8.760 | 1.455 | 6.021 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.447 | 0.689 | 48.570 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `classic` | `strict_current` | 33.447 | 1.455 | 22.987 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.300 | 0.785 | 10.576 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `ax` | `strict_current` | 8.300 | 1.402 | 5.918 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 31.111 | 0.785 | 39.643 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `classic` | `strict_current` | 31.111 | 1.402 | 22.184 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.983 | 0.749 | 10.652 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `ax` | `strict_current` | 7.983 | 1.425 | 5.604 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 31.708 | 0.749 | 42.310 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `classic` | `strict_current` | 31.708 | 1.425 | 22.258 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 8.259 | 1.001 | 8.253 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 8.259 | 3.295 | 2.506 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 30.237 | 1.001 | 30.217 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 30.237 | 3.295 | 9.176 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.823 | 1.089 | 9.020 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `ax` | `strict_current` | 9.823 | 2.794 | 3.515 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 31.470 | 1.089 | 28.899 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `classic` | `strict_current` | 31.470 | 2.794 | 11.262 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 13.877 | 2.532 | 5.480 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 13.877 | 3.451 | 4.022 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 37.009 | 2.532 | 14.614 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 37.009 | 3.451 | 10.725 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 14.931 | 1.338 | 11.156 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `ax` | `strict_current` | 14.931 | 2.835 | 5.267 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 37.844 | 1.338 | 28.275 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `classic` | `strict_current` | 37.844 | 2.835 | 13.350 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 8.291 | 1.079 | 7.686 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `ax` | `strict_current` | 8.291 | 1.247 | 6.647 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 18.026 | 1.079 | 16.709 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `classic` | `strict_current` | 18.026 | 1.247 | 14.451 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.380 | 0.958 | 8.746 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `ax` | `strict_current` | 8.380 | 1.219 | 6.873 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 17.822 | 0.958 | 18.600 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `classic` | `strict_current` | 17.822 | 1.219 | 14.617 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.693 | 0.749 | 10.270 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `ax` | `strict_current` | 7.693 | 1.282 | 5.999 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 16.694 | 0.749 | 22.287 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `classic` | `strict_current` | 16.694 | 1.282 | 13.018 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.030 | 0.741 | 12.186 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `ax` | `strict_current` | 9.030 | 1.204 | 7.500 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 19.490 | 0.741 | 26.300 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `classic` | `strict_current` | 19.490 | 1.204 | 16.187 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.655 | 0.609 | 15.855 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `ax` | `strict_current` | 9.655 | 0.569 | 16.965 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 20.551 | 0.609 | 33.748 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `classic` | `strict_current` | 20.551 | 0.569 | 36.111 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.450 | 0.542 | 13.752 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `ax` | `strict_current` | 7.450 | 0.506 | 14.728 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 19.123 | 0.542 | 35.297 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `classic` | `strict_current` | 19.123 | 0.506 | 37.802 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.409 | 0.621 | 15.152 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `ax` | `strict_current` | 9.409 | 0.536 | 17.554 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 18.631 | 0.621 | 30.004 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `classic` | `strict_current` | 18.631 | 0.536 | 34.759 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 8.261 | 0.903 | 9.148 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `ax` | `strict_current` | 8.261 | 0.571 | 14.462 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 31.260 | 0.903 | 34.616 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `classic` | `strict_current` | 31.260 | 0.571 | 54.727 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.844 | 0.532 | 14.748 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `ax` | `strict_current` | 7.844 | 0.652 | 12.028 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 31.904 | 0.532 | 59.989 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `classic` | `strict_current` | 31.904 | 0.652 | 48.923 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.909 | 0.414 | 21.530 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `ax` | `strict_current` | 8.909 | 0.573 | 15.546 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 32.601 | 0.414 | 78.786 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `classic` | `strict_current` | 32.601 | 0.573 | 56.888 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.044 | 0.636 | 14.210 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `ax` | `strict_current` | 9.044 | 0.496 | 18.242 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.209 | 0.636 | 52.177 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `classic` | `strict_current` | 33.209 | 0.496 | 66.984 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 22.881 | 0.474 | 48.237 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `ax` | `strict_current` | 22.881 | 0.918 | 24.914 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 33.342 | 0.474 | 70.291 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `classic` | `strict_current` | 33.342 | 0.918 | 36.304 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.038 | 0.672 | 11.964 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `ax` | `strict_current` | 8.038 | 1.102 | 7.296 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 36.953 | 0.672 | 54.998 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `classic` | `strict_current` | 36.953 | 1.102 | 33.539 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.152 | 1.023 | 9.925 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `ax` | `strict_current` | 10.152 | 0.702 | 14.461 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 29.568 | 1.023 | 28.906 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `classic` | `strict_current` | 29.568 | 0.702 | 42.116 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 20.910 | 0.552 | 37.848 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `ax` | `strict_current` | 20.910 | 0.622 | 33.593 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 34.782 | 0.552 | 62.957 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `classic` | `strict_current` | 34.782 | 0.622 | 55.878 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.695 | 0.827 | 9.309 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.695 | 4.491 | 1.714 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 31.055 | 0.827 | 37.566 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `classic` | `strict_current` | 31.055 | 4.491 | 6.916 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.705 | 0.669 | 13.021 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `ax` | `strict_current` | 8.705 | 4.370 | 1.992 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 32.130 | 0.669 | 48.061 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `classic` | `strict_current` | 32.130 | 4.370 | 7.353 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.874 | 0.904 | 8.706 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `ax` | `strict_current` | 7.874 | 4.395 | 1.792 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 31.096 | 0.904 | 34.382 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `classic` | `strict_current` | 31.096 | 4.395 | 7.075 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.071 | 0.647 | 12.473 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `ax` | `strict_current` | 8.071 | 4.323 | 1.867 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 32.158 | 0.647 | 49.694 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `classic` | `strict_current` | 32.158 | 4.323 | 7.439 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 8.460 | 2.406 | 3.516 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `ax` | `strict_current` | 8.460 | 2.743 | 3.084 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 32.125 | 2.406 | 13.352 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `classic` | `strict_current` | 32.125 | 2.743 | 11.711 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.845 | 1.525 | 5.800 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `ax` | `strict_current` | 8.845 | 1.381 | 6.404 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 31.376 | 1.525 | 20.574 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `classic` | `strict_current` | 31.376 | 1.381 | 22.716 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.172 | 1.899 | 5.356 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `ax` | `strict_current` | 10.172 | 1.409 | 7.217 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.340 | 1.899 | 17.556 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `classic` | `strict_current` | 33.340 | 1.409 | 23.655 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.646 | 1.297 | 5.896 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `ax` | `strict_current` | 7.646 | 1.259 | 6.072 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 32.407 | 1.297 | 24.988 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `classic` | `strict_current` | 32.407 | 1.259 | 25.733 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.147 | 0.957 | 8.509 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `ax` | `strict_current` | 8.147 | 0.540 | 15.088 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.294 | 0.957 | 13.885 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `classic` | `strict_current` | 13.294 | 0.540 | 24.622 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.555 | 0.571 | 18.501 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `ax` | `strict_current` | 10.555 | 0.651 | 16.211 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 19.238 | 0.571 | 33.721 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `classic` | `strict_current` | 19.238 | 0.651 | 29.547 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.393 | 0.629 | 13.349 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `ax` | `strict_current` | 8.393 | 0.678 | 12.373 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.609 | 0.629 | 24.826 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `classic` | `strict_current` | 15.609 | 0.678 | 23.011 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 8.148 | 0.575 | 14.182 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `ax` | `strict_current` | 8.148 | 2.247 | 3.625 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 57.486 | 0.575 | 100.062 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `classic` | `strict_current` | 57.486 | 2.247 | 25.579 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.278 | 0.573 | 14.442 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `ax` | `strict_current` | 8.278 | 2.394 | 3.458 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 59.859 | 0.573 | 104.438 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `classic` | `strict_current` | 59.859 | 2.394 | 25.003 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.270 | 0.686 | 12.049 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `ax` | `strict_current` | 8.270 | 2.881 | 2.870 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 52.520 | 0.686 | 76.520 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `classic` | `strict_current` | 52.520 | 2.881 | 18.228 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.751 | 0.652 | 13.424 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `ax` | `strict_current` | 8.751 | 2.374 | 3.687 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 57.247 | 0.652 | 87.815 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `classic` | `strict_current` | 57.247 | 2.374 | 24.118 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 19.411 | 0.626 | 30.986 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 19.411 | 0.814 | 23.859 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 35.524 | 0.626 | 56.706 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 35.524 | 0.814 | 43.663 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.695 | 0.547 | 19.556 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `ax` | `strict_current` | 10.695 | 0.652 | 16.404 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 36.043 | 0.547 | 65.906 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `classic` | `strict_current` | 36.043 | 0.652 | 55.283 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.485 | 0.596 | 14.231 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `ax` | `strict_current` | 8.485 | 0.665 | 12.752 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.834 | 0.596 | 56.747 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `classic` | `strict_current` | 33.834 | 0.665 | 50.847 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 23.891 | 0.721 | 33.122 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `ax` | `strict_current` | 23.891 | 0.734 | 32.537 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 36.137 | 0.721 | 50.100 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `classic` | `strict_current` | 36.137 | 0.734 | 49.214 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.158 | 1.152 | 7.946 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `ax` | `strict_current` | 9.158 | 4.411 | 2.076 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 31.362 | 1.152 | 27.212 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `classic` | `strict_current` | 31.362 | 4.411 | 7.111 |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 15.621 | 2.286 | 6.833 |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `ax` | `strict_current` | 15.621 | 5.506 | 2.837 |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 37.278 | 2.286 | 16.307 |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `classic` | `strict_current` | 37.278 | 5.506 | 6.771 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 8.859 | 0.537 | 16.502 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `ax` | `strict_current` | 8.859 | 0.743 | 11.920 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 35.042 | 0.537 | 65.274 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `classic` | `strict_current` | 35.042 | 0.743 | 47.150 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.825 | 0.577 | 17.029 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `ax` | `strict_current` | 9.825 | 0.703 | 13.969 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 35.451 | 0.577 | 61.441 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `classic` | `strict_current` | 35.451 | 0.703 | 50.400 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.622 | 0.535 | 14.236 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `ax` | `strict_current` | 7.622 | 0.731 | 10.431 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 32.025 | 0.535 | 59.815 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `classic` | `strict_current` | 32.025 | 0.731 | 43.830 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.711 | 0.661 | 13.185 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `ax` | `strict_current` | 8.711 | 0.786 | 11.088 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 35.256 | 0.661 | 53.366 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `classic` | `strict_current` | 35.256 | 0.786 | 44.879 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 9.070 | 0.470 | 19.309 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `ax` | `strict_current` | 9.070 | 0.763 | 11.883 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 33.808 | 0.470 | 71.971 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `classic` | `strict_current` | 33.808 | 0.763 | 44.293 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.002 | 0.535 | 16.817 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `ax` | `strict_current` | 9.002 | 0.574 | 15.686 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 32.509 | 0.535 | 60.731 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `classic` | `strict_current` | 32.509 | 0.574 | 56.646 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.424 | 0.742 | 11.361 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `ax` | `strict_current` | 8.424 | 0.682 | 12.344 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 34.527 | 0.742 | 46.563 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `classic` | `strict_current` | 34.527 | 0.682 | 50.592 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.285 | 0.927 | 8.935 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `ax` | `strict_current` | 8.285 | 0.645 | 12.846 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.331 | 0.927 | 35.947 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `classic` | `strict_current` | 33.331 | 0.645 | 51.679 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 20.571 | 0.821 | 25.064 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `ax` | `strict_current` | 20.571 | 1.421 | 14.475 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 19.540 | 0.821 | 23.808 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `classic` | `strict_current` | 19.540 | 1.421 | 13.749 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.850 | 1.320 | 5.948 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `ax` | `strict_current` | 7.850 | 1.483 | 5.293 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 17.821 | 1.320 | 13.502 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `classic` | `strict_current` | 17.821 | 1.483 | 12.016 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 19.663 | 0.843 | 23.335 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `ax` | `strict_current` | 19.663 | 0.797 | 24.665 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 18.706 | 0.843 | 22.199 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `classic` | `strict_current` | 18.706 | 0.797 | 23.465 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.416 | 1.322 | 6.367 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `ax` | `strict_current` | 8.416 | 1.451 | 5.801 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 17.785 | 1.322 | 13.455 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `classic` | `strict_current` | 17.785 | 1.451 | 12.260 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 11.067 | 9.831 | 1.126 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `ax` | `strict_current` | 11.067 | 128.819 | 0.086 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 50.995 | 9.831 | 5.187 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `classic` | `strict_current` | 50.995 | 128.819 | 0.396 |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.833 | 33.116 | 0.327 |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `ax` | `strict_current` | 10.833 | 149.967 | 0.072 |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 48.727 | 33.116 | 1.471 |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `classic` | `strict_current` | 48.727 | 149.967 | 0.325 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 16.457 | 1.002 | 16.423 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `ax` | `strict_current` | 16.457 | 1.491 | 11.039 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 16.527 | 1.002 | 16.493 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `classic` | `strict_current` | 16.527 | 1.491 | 11.085 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 18.595 | 0.859 | 21.638 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `ax` | `strict_current` | 18.595 | 1.923 | 9.668 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 16.574 | 0.859 | 19.286 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `classic` | `strict_current` | 16.574 | 1.923 | 8.617 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.950 | 0.784 | 10.146 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `ax` | `strict_current` | 7.950 | 1.642 | 4.842 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 18.713 | 0.784 | 23.882 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `classic` | `strict_current` | 18.713 | 1.642 | 11.397 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.806 | 0.829 | 10.617 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `ax` | `strict_current` | 8.806 | 1.509 | 5.836 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 18.689 | 0.829 | 22.534 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `classic` | `strict_current` | 18.689 | 1.509 | 12.386 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.068 | 0.605 | 11.684 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.068 | 1.002 | 7.055 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 33.016 | 0.605 | 54.582 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `classic` | `strict_current` | 33.016 | 1.002 | 32.955 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.389 | 0.633 | 13.249 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `ax` | `strict_current` | 8.389 | 0.986 | 8.504 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 38.133 | 0.633 | 60.224 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `classic` | `strict_current` | 38.133 | 0.986 | 38.657 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 11.801 | 0.557 | 21.192 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `ax` | `strict_current` | 11.801 | 1.566 | 7.534 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 36.775 | 0.557 | 66.037 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `classic` | `strict_current` | 36.775 | 1.566 | 23.476 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.553 | 0.677 | 15.596 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `ax` | `strict_current` | 10.553 | 1.109 | 9.517 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 42.478 | 0.677 | 62.778 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `classic` | `strict_current` | 42.478 | 1.109 | 38.307 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.667 | 0.739 | 10.377 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.667 | 0.823 | 9.320 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 33.507 | 0.739 | 45.349 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 33.507 | 0.823 | 40.729 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.521 | 0.752 | 11.331 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `ax` | `strict_current` | 8.521 | 0.784 | 10.865 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 34.215 | 0.752 | 45.498 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `classic` | `strict_current` | 34.215 | 0.784 | 43.627 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.480 | 0.880 | 10.772 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 9.480 | 0.766 | 12.371 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 34.257 | 0.880 | 38.929 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 34.257 | 0.766 | 44.707 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.598 | 0.716 | 12.000 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `ax` | `strict_current` | 8.598 | 1.063 | 8.088 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 34.669 | 0.716 | 48.387 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `classic` | `strict_current` | 34.669 | 1.063 | 32.612 |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.650 | 1.630 | 4.080 |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.650 | 4.371 | 1.521 |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 29.581 | 1.630 | 18.146 |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `classic` | `strict_current` | 29.581 | 4.371 | 6.767 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 13.211 | 2.207 | 5.986 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `ax` | `strict_current` | 13.211 | 5.610 | 2.355 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 34.192 | 2.207 | 15.493 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `classic` | `strict_current` | 34.192 | 5.610 | 6.095 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.837 | 2.060 | 3.805 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `ax` | `strict_current` | 7.837 | 3.271 | 2.396 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 29.237 | 2.060 | 14.195 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `classic` | `strict_current` | 29.237 | 3.271 | 8.937 |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.831 | 2.106 | 3.719 |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `ax` | `strict_current` | 7.831 | 3.317 | 2.361 |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 28.789 | 2.106 | 13.672 |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `classic` | `strict_current` | 28.789 | 3.317 | 8.680 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 21.853 | 0.662 | 33.011 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 21.853 | 0.745 | 29.346 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 37.128 | 0.662 | 56.084 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 37.128 | 0.745 | 49.856 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.285 | 0.573 | 16.210 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `ax` | `strict_current` | 9.285 | 0.734 | 12.643 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 32.411 | 0.573 | 56.587 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `classic` | `strict_current` | 32.411 | 0.734 | 44.133 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 23.761 | 0.600 | 39.574 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `ax` | `strict_current` | 23.761 | 0.756 | 31.413 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 39.851 | 0.600 | 66.373 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `classic` | `strict_current` | 39.851 | 0.756 | 52.686 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.383 | 0.608 | 13.778 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `ax` | `strict_current` | 8.383 | 0.910 | 9.212 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.218 | 0.608 | 54.595 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `classic` | `strict_current` | 33.218 | 0.910 | 36.505 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.508 | 0.522 | 14.390 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.508 | 1.350 | 5.560 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 31.519 | 0.522 | 60.409 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `classic` | `strict_current` | 31.519 | 1.350 | 23.339 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.461 | 0.607 | 15.575 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `ax` | `strict_current` | 9.461 | 1.473 | 6.425 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 32.104 | 0.607 | 52.848 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `classic` | `strict_current` | 32.104 | 1.473 | 21.802 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.551 | 0.637 | 13.424 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `ax` | `strict_current` | 8.551 | 1.405 | 6.088 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 30.615 | 0.637 | 48.062 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `classic` | `strict_current` | 30.615 | 1.405 | 21.796 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.363 | 0.690 | 12.116 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `ax` | `strict_current` | 8.363 | 1.418 | 5.900 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 32.217 | 0.690 | 46.674 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `classic` | `strict_current` | 32.217 | 1.418 | 22.727 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 19.050 | 1.260 | 15.121 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 19.050 | 1.040 | 18.313 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 18.350 | 1.260 | 14.565 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 18.350 | 1.040 | 17.640 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 18.165 | 1.137 | 15.974 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `ax` | `strict_current` | 18.165 | 1.303 | 13.941 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 17.224 | 1.137 | 15.147 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `classic` | `strict_current` | 17.224 | 1.303 | 13.219 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.808 | 0.834 | 8.159 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 6.808 | 1.075 | 6.335 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 17.046 | 0.834 | 20.428 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 17.046 | 1.075 | 15.860 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.247 | 0.919 | 8.971 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `ax` | `strict_current` | 8.247 | 1.017 | 8.110 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 19.031 | 0.919 | 20.701 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `classic` | `strict_current` | 19.031 | 1.017 | 18.714 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 8.913 | 0.613 | 14.528 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `ax` | `strict_current` | 8.913 | 0.890 | 10.009 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 34.584 | 0.613 | 56.373 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `classic` | `strict_current` | 34.584 | 0.890 | 38.837 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.493 | 0.932 | 8.043 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `ax` | `strict_current` | 7.493 | 0.778 | 9.637 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 35.299 | 0.932 | 37.890 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `classic` | `strict_current` | 35.299 | 0.778 | 45.400 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.987 | 0.698 | 11.447 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `ax` | `strict_current` | 7.987 | 0.782 | 10.208 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 32.630 | 0.698 | 46.765 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `classic` | `strict_current` | 32.630 | 0.782 | 41.705 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.798 | 0.631 | 12.350 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `ax` | `strict_current` | 7.798 | 0.826 | 9.441 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 32.174 | 0.631 | 50.953 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `classic` | `strict_current` | 32.174 | 0.826 | 38.953 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.167 | 0.737 | 9.719 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.167 | 0.852 | 8.408 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 18.975 | 0.737 | 25.731 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 18.975 | 0.852 | 22.260 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.976 | 0.668 | 13.435 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `ax` | `strict_current` | 8.976 | 0.799 | 11.232 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 18.649 | 0.668 | 27.915 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `classic` | `strict_current` | 18.649 | 0.799 | 23.337 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.703 | 0.648 | 13.429 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `ax` | `strict_current` | 8.703 | 0.672 | 12.946 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 18.689 | 0.648 | 28.838 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `classic` | `strict_current` | 18.689 | 0.672 | 27.801 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.001 | 0.968 | 9.294 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `ax` | `strict_current` | 9.001 | 0.723 | 12.455 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 21.901 | 0.968 | 22.614 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `classic` | `strict_current` | 21.901 | 0.723 | 30.306 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 4.284 | 103.312 | 0.041 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `ax` | `strict_current` | 4.284 | 110.725 | 0.039 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 17.751 | 103.312 | 0.172 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `classic` | `strict_current` | 17.751 | 110.725 | 0.160 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.045 | 76.879 | 0.066 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `ax` | `strict_current` | 5.045 | 172.800 | 0.029 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 16.514 | 76.879 | 0.215 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `classic` | `strict_current` | 16.514 | 172.800 | 0.096 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 4.776 | 81.341 | 0.059 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `ax` | `strict_current` | 4.776 | 81.915 | 0.058 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 17.305 | 81.341 | 0.213 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `classic` | `strict_current` | 17.305 | 81.915 | 0.211 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 4.411 | 76.428 | 0.058 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `ax` | `strict_current` | 4.411 | 98.822 | 0.045 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 16.708 | 76.428 | 0.219 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `classic` | `strict_current` | 16.708 | 98.822 | 0.169 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 10.692 | 8.425 | 1.269 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `ax` | `strict_current` | 10.692 | 70.423 | 0.152 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 17.432 | 8.425 | 2.069 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `classic` | `strict_current` | 17.432 | 70.423 | 0.248 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 4.204 | 8.226 | 0.511 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `ax` | `strict_current` | 4.204 | 117.164 | 0.036 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 16.067 | 8.226 | 1.953 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `classic` | `strict_current` | 16.067 | 117.164 | 0.137 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 4.381 | 9.300 | 0.471 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `ax` | `strict_current` | 4.381 | 122.388 | 0.036 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 16.012 | 9.300 | 1.722 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `classic` | `strict_current` | 16.012 | 122.388 | 0.131 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.385 | 8.350 | 1.244 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `ax` | `strict_current` | 10.385 | 93.241 | 0.111 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 17.925 | 8.350 | 2.147 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `classic` | `strict_current` | 17.925 | 93.241 | 0.192 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 9.957 | 0.697 | 14.283 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `ax` | `strict_current` | 9.957 | 1.722 | 5.781 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 19.344 | 0.697 | 27.746 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `classic` | `strict_current` | 19.344 | 1.722 | 11.231 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.690 | 0.762 | 11.407 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `ax` | `strict_current` | 8.690 | 1.182 | 7.352 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 19.263 | 0.762 | 25.285 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `classic` | `strict_current` | 19.263 | 1.182 | 16.297 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.499 | 0.457 | 16.421 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `ax` | `strict_current` | 7.499 | 0.943 | 7.951 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 20.271 | 0.457 | 44.390 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `classic` | `strict_current` | 20.271 | 0.943 | 21.495 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.110 | 0.806 | 11.308 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `ax` | `strict_current` | 9.110 | 0.817 | 11.149 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 19.458 | 0.806 | 24.153 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `classic` | `strict_current` | 19.458 | 0.817 | 23.815 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 26.003 | 2.337 | 11.127 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 26.003 | 9.875 | 2.633 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 146.062 | 2.337 | 62.500 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 146.062 | 9.875 | 14.791 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 23.216 | 5.781 | 4.016 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `ax` | `strict_current` | 23.216 | 12.086 | 1.921 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 152.460 | 5.781 | 26.375 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `classic` | `strict_current` | 152.460 | 12.086 | 12.615 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 25.010 | 3.958 | 6.319 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 25.010 | 9.049 | 2.764 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 142.085 | 3.958 | 35.901 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 142.085 | 9.049 | 15.702 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 31.959 | 3.200 | 9.987 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `ax` | `strict_current` | 31.959 | 10.434 | 3.063 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 140.301 | 3.200 | 43.844 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `classic` | `strict_current` | 140.301 | 10.434 | 13.447 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.332 | 0.589 | 15.852 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `ax` | `strict_current` | 9.332 | 0.546 | 17.092 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 35.299 | 0.589 | 59.959 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `classic` | `strict_current` | 35.299 | 0.546 | 64.647 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.480 | 0.480 | 21.814 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `ax` | `strict_current` | 10.480 | 0.568 | 18.464 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 30.740 | 0.480 | 63.989 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `classic` | `strict_current` | 30.740 | 0.568 | 54.161 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.536 | 0.692 | 13.779 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `ax` | `strict_current` | 9.536 | 0.524 | 18.210 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 35.319 | 0.692 | 51.034 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `classic` | `strict_current` | 35.319 | 0.524 | 67.447 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 21.867 | 1.340 | 16.316 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `ax` | `strict_current` | 21.867 | 1.465 | 14.929 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 35.814 | 1.340 | 26.722 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `classic` | `strict_current` | 35.814 | 1.465 | 24.450 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.761 | 1.086 | 8.070 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `ax` | `strict_current` | 8.761 | 0.897 | 9.770 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 35.285 | 1.086 | 32.503 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `classic` | `strict_current` | 35.285 | 0.897 | 39.352 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.008 | 0.839 | 10.739 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `ax` | `strict_current` | 9.008 | 0.910 | 9.903 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.419 | 0.839 | 39.844 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `classic` | `strict_current` | 33.419 | 0.910 | 36.742 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 21.585 | 0.803 | 26.885 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `ax` | `strict_current` | 21.585 | 0.859 | 25.124 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 34.095 | 0.803 | 42.467 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `classic` | `strict_current` | 34.095 | 0.859 | 39.685 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 11.713 | 0.823 | 14.229 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `ax` | `strict_current` | 11.713 | 0.789 | 14.845 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 36.483 | 0.823 | 44.319 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `classic` | `strict_current` | 36.483 | 0.789 | 46.237 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.483 | 0.624 | 16.808 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `ax` | `strict_current` | 10.483 | 0.750 | 13.983 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 35.454 | 0.624 | 56.848 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `classic` | `strict_current` | 35.454 | 0.750 | 47.291 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.522 | 0.645 | 13.213 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `ax` | `strict_current` | 8.522 | 0.928 | 9.184 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 32.685 | 0.645 | 50.672 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `classic` | `strict_current` | 32.685 | 0.928 | 35.223 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.937 | 0.633 | 14.111 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `ax` | `strict_current` | 8.937 | 0.964 | 9.273 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 32.601 | 0.633 | 51.477 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `classic` | `strict_current` | 32.601 | 0.964 | 33.828 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 9.039 | 0.958 | 9.435 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `ax` | `strict_current` | 9.039 | 1.022 | 8.847 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 19.664 | 0.958 | 20.526 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `classic` | `strict_current` | 19.664 | 1.022 | 19.247 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.152 | 0.622 | 14.713 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `ax` | `strict_current` | 9.152 | 0.903 | 10.137 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 19.004 | 0.622 | 30.552 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `classic` | `strict_current` | 19.004 | 0.903 | 21.050 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.006 | 0.579 | 13.824 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `ax` | `strict_current` | 8.006 | 0.829 | 9.662 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 17.434 | 0.579 | 30.103 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `classic` | `strict_current` | 17.434 | 0.829 | 21.040 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.937 | 0.650 | 13.741 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `ax` | `strict_current` | 8.937 | 0.854 | 10.466 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 18.356 | 0.650 | 28.223 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `classic` | `strict_current` | 18.356 | 0.854 | 21.497 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 20.258 | 0.650 | 31.148 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `ax` | `strict_current` | 20.258 | 1.169 | 17.328 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 33.637 | 0.650 | 51.719 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `classic` | `strict_current` | 33.637 | 1.169 | 28.772 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.620 | 0.675 | 15.722 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `ax` | `strict_current` | 10.620 | 1.431 | 7.424 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.149 | 0.675 | 49.074 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `classic` | `strict_current` | 33.149 | 1.431 | 23.172 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 22.892 | 0.836 | 27.399 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `ax` | `strict_current` | 22.892 | 1.501 | 15.253 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 35.800 | 0.836 | 42.848 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `classic` | `strict_current` | 35.800 | 1.501 | 23.853 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 21.210 | 0.847 | 25.041 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `ax` | `strict_current` | 21.210 | 1.301 | 16.297 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.877 | 0.847 | 39.997 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `classic` | `strict_current` | 33.877 | 1.301 | 26.031 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 16.832 | 0.634 | 26.531 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `ax` | `strict_current` | 16.832 | 0.567 | 29.661 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 15.530 | 0.634 | 24.479 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `classic` | `strict_current` | 15.530 | 0.567 | 27.367 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.969 | 0.918 | 10.864 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `ax` | `strict_current` | 9.969 | 0.912 | 10.935 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 20.661 | 0.918 | 22.517 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `classic` | `strict_current` | 20.661 | 0.912 | 22.665 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 21.591 | 0.635 | 34.007 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `ax` | `strict_current` | 21.591 | 0.559 | 38.657 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 20.181 | 0.635 | 31.786 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `classic` | `strict_current` | 20.181 | 0.559 | 36.133 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.030 | 0.488 | 18.510 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `ax` | `strict_current` | 9.030 | 0.612 | 14.746 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 17.031 | 0.488 | 34.913 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `classic` | `strict_current` | 17.031 | 0.612 | 27.813 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.584 | 1.187 | 6.390 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.584 | 2.140 | 3.544 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 31.904 | 1.187 | 26.884 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `classic` | `strict_current` | 31.904 | 2.140 | 14.911 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.583 | 1.560 | 6.782 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `ax` | `strict_current` | 10.583 | 1.953 | 5.418 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 34.512 | 1.560 | 22.117 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `classic` | `strict_current` | 34.512 | 1.953 | 17.668 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.658 | 0.980 | 7.812 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `ax` | `strict_current` | 7.658 | 1.926 | 3.976 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.016 | 0.980 | 33.682 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `classic` | `strict_current` | 33.016 | 1.926 | 17.144 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.274 | 1.229 | 6.731 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `ax` | `strict_current` | 8.274 | 2.076 | 3.985 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 32.062 | 1.229 | 26.082 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `classic` | `strict_current` | 32.062 | 2.076 | 15.442 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.633 | 0.640 | 15.058 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `ax` | `strict_current` | 9.633 | 0.707 | 13.626 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 39.165 | 0.640 | 61.221 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `classic` | `strict_current` | 39.165 | 0.707 | 55.400 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.715 | 0.813 | 11.949 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `ax` | `strict_current` | 9.715 | 1.405 | 6.916 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.879 | 0.813 | 41.671 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `classic` | `strict_current` | 33.879 | 1.405 | 24.118 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.130 | 0.939 | 9.719 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `ax` | `strict_current` | 9.130 | 1.218 | 7.494 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.907 | 0.939 | 16.932 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `classic` | `strict_current` | 15.907 | 1.218 | 13.056 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.897 | 0.744 | 11.954 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `ax` | `strict_current` | 8.897 | 0.734 | 12.114 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 18.650 | 0.744 | 25.057 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `classic` | `strict_current` | 18.650 | 0.734 | 25.393 |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.773 | 0.756 | 10.277 |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `ax` | `strict_current` | 7.773 | 0.753 | 10.326 |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.288 | 0.756 | 20.214 |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `classic` | `strict_current` | 15.288 | 0.753 | 20.310 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 9.183 | 0.969 | 9.481 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `ax` | `strict_current` | 9.183 | 1.349 | 6.807 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 18.879 | 0.969 | 19.492 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `classic` | `strict_current` | 18.879 | 1.349 | 13.993 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.242 | 0.663 | 15.437 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `ax` | `strict_current` | 10.242 | 0.623 | 16.437 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 19.813 | 0.663 | 29.864 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `classic` | `strict_current` | 19.813 | 0.623 | 31.797 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.809 | 0.688 | 11.348 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `ax` | `strict_current` | 7.809 | 0.681 | 11.463 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.087 | 0.688 | 21.925 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `classic` | `strict_current` | 15.087 | 0.681 | 22.146 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.183 | 0.637 | 12.850 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `ax` | `strict_current` | 8.183 | 0.812 | 10.081 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 18.862 | 0.637 | 29.620 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `classic` | `strict_current` | 18.862 | 0.812 | 23.237 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 11.407 | 0.979 | 11.652 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `ax` | `strict_current` | 11.407 | 1.481 | 7.704 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 37.172 | 0.979 | 37.968 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `classic` | `strict_current` | 37.172 | 1.481 | 25.104 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 11.423 | 0.685 | 16.685 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `ax` | `strict_current` | 11.423 | 1.105 | 10.337 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 42.016 | 0.685 | 61.371 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `classic` | `strict_current` | 42.016 | 1.105 | 38.021 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 12.224 | 1.215 | 10.057 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `ax` | `strict_current` | 12.224 | 1.378 | 8.868 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 40.408 | 1.215 | 33.245 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `classic` | `strict_current` | 40.408 | 1.378 | 29.316 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 11.158 | 0.666 | 16.766 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `ax` | `strict_current` | 11.158 | 1.263 | 8.837 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 37.069 | 0.666 | 55.698 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `classic` | `strict_current` | 37.069 | 1.263 | 29.359 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 8.436 | 3.122 | 2.702 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 8.436 | 3.365 | 2.507 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 27.304 | 3.122 | 8.745 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 27.304 | 3.365 | 8.114 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.430 | 0.850 | 8.738 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `ax` | `strict_current` | 7.430 | 2.773 | 2.679 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 29.447 | 0.850 | 34.628 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `classic` | `strict_current` | 29.447 | 2.773 | 10.618 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 34.405 | 1.416 | 24.304 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 34.405 | 3.137 | 10.969 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 55.546 | 1.416 | 39.238 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 55.546 | 3.137 | 17.709 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.700 | 0.886 | 8.691 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `ax` | `strict_current` | 7.700 | 2.844 | 2.707 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 29.620 | 0.886 | 33.433 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `classic` | `strict_current` | 29.620 | 2.844 | 10.413 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 8.616 | 0.564 | 15.270 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `ax` | `strict_current` | 8.616 | 1.517 | 5.681 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 34.024 | 0.564 | 60.301 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `classic` | `strict_current` | 34.024 | 1.517 | 22.433 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.843 | 0.613 | 11.165 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `ax` | `strict_current` | 6.843 | 1.293 | 5.292 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 31.573 | 0.613 | 51.513 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `classic` | `strict_current` | 31.573 | 1.293 | 24.414 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.313 | 0.561 | 14.810 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `ax` | `strict_current` | 8.313 | 1.841 | 4.514 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 31.152 | 0.561 | 55.501 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `classic` | `strict_current` | 31.152 | 1.841 | 16.918 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.952 | 0.594 | 13.391 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `ax` | `strict_current` | 7.952 | 1.272 | 6.252 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 31.055 | 0.594 | 52.297 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `classic` | `strict_current` | 31.055 | 1.272 | 24.415 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 22.811 | 0.631 | 36.151 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `ax` | `strict_current` | 22.811 | 0.699 | 32.618 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 39.307 | 0.631 | 62.293 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `classic` | `strict_current` | 39.307 | 0.699 | 56.206 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.510 | 0.532 | 14.116 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `ax` | `strict_current` | 7.510 | 0.777 | 9.669 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 34.319 | 0.532 | 64.512 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `classic` | `strict_current` | 34.319 | 0.777 | 44.188 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.253 | 0.456 | 22.488 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `ax` | `strict_current` | 10.253 | 0.527 | 19.466 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 29.041 | 0.456 | 63.695 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `classic` | `strict_current` | 29.041 | 0.527 | 55.133 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 25.706 | 0.798 | 32.220 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `ax` | `strict_current` | 25.706 | 0.620 | 41.443 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 38.373 | 0.798 | 48.097 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `classic` | `strict_current` | 38.373 | 0.620 | 61.866 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 8.307 | 0.834 | 9.965 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 8.307 | 0.578 | 14.371 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 32.743 | 0.834 | 39.276 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 32.743 | 0.578 | 56.644 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.357 | 0.577 | 14.471 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `ax` | `strict_current` | 8.357 | 0.788 | 10.605 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.282 | 0.577 | 57.631 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `classic` | `strict_current` | 33.282 | 0.788 | 42.236 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.152 | 0.531 | 15.354 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 8.152 | 0.560 | 14.554 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.220 | 0.531 | 62.571 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 33.220 | 0.560 | 59.309 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.780 | 0.631 | 13.917 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `ax` | `strict_current` | 8.780 | 0.583 | 15.060 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 34.986 | 0.631 | 55.457 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `classic` | `strict_current` | 34.986 | 0.583 | 60.009 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 20.285 | 1.143 | 17.751 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `ax` | `strict_current` | 20.285 | 0.989 | 20.508 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 19.406 | 1.143 | 16.981 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `classic` | `strict_current` | 19.406 | 0.989 | 19.619 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 19.571 | 0.961 | 20.369 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `ax` | `strict_current` | 19.571 | 1.124 | 17.409 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 18.800 | 0.961 | 19.566 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `classic` | `strict_current` | 18.800 | 1.124 | 16.723 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.620 | 0.839 | 10.269 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `ax` | `strict_current` | 8.620 | 1.105 | 7.800 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 20.289 | 0.839 | 24.170 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `classic` | `strict_current` | 20.289 | 1.105 | 18.359 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.090 | 0.590 | 12.021 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `ax` | `strict_current` | 7.090 | 0.863 | 8.218 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 22.396 | 0.590 | 37.973 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `classic` | `strict_current` | 22.396 | 0.863 | 25.961 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.165 | 0.616 | 11.629 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.165 | 0.679 | 10.550 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 32.317 | 0.616 | 52.456 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `classic` | `strict_current` | 32.317 | 0.679 | 47.589 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.695 | 0.651 | 11.825 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `ax` | `strict_current` | 7.695 | 0.695 | 11.071 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 32.942 | 0.651 | 50.625 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `classic` | `strict_current` | 32.942 | 0.695 | 47.396 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.530 | 0.713 | 13.366 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `ax` | `strict_current` | 9.530 | 0.655 | 14.552 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 31.885 | 0.713 | 44.718 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `classic` | `strict_current` | 31.885 | 0.655 | 48.687 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.521 | 0.664 | 14.341 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `ax` | `strict_current` | 9.521 | 0.810 | 11.757 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 31.509 | 0.664 | 47.462 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `classic` | `strict_current` | 31.509 | 0.810 | 38.908 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 9.126 | 0.793 | 11.514 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `ax` | `strict_current` | 9.126 | 1.572 | 5.806 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 34.961 | 0.793 | 44.108 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `classic` | `strict_current` | 34.961 | 1.572 | 22.241 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.302 | 0.871 | 9.534 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `ax` | `strict_current` | 8.302 | 1.169 | 7.102 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.314 | 0.871 | 38.260 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `classic` | `strict_current` | 33.314 | 1.169 | 28.500 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.277 | 0.851 | 12.077 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `ax` | `strict_current` | 10.277 | 1.208 | 8.505 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 39.985 | 0.851 | 46.989 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `classic` | `strict_current` | 39.985 | 1.208 | 33.091 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.974 | 0.694 | 11.487 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `ax` | `strict_current` | 7.974 | 0.737 | 10.825 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 34.146 | 0.694 | 49.189 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `classic` | `strict_current` | 34.146 | 0.737 | 46.357 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 22.285 | 0.998 | 22.329 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `ax` | `strict_current` | 22.285 | 0.905 | 24.617 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 22.641 | 0.998 | 22.686 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `classic` | `strict_current` | 22.641 | 0.905 | 25.011 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.076 | 0.799 | 12.618 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `ax` | `strict_current` | 10.076 | 0.787 | 12.801 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 20.467 | 0.799 | 25.631 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `classic` | `strict_current` | 20.467 | 0.787 | 26.003 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.240 | 1.037 | 7.946 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `ax` | `strict_current` | 8.240 | 1.029 | 8.009 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 21.295 | 1.037 | 20.534 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `classic` | `strict_current` | 21.295 | 1.029 | 20.697 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 18.635 | 0.931 | 20.027 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `ax` | `strict_current` | 18.635 | 1.193 | 15.616 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 17.075 | 0.931 | 18.350 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `classic` | `strict_current` | 17.075 | 1.193 | 14.308 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 10.588 | 0.829 | 12.769 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `ax` | `strict_current` | 10.588 | 1.304 | 8.118 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 41.387 | 0.829 | 49.915 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `classic` | `strict_current` | 41.387 | 1.304 | 31.733 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.642 | 1.107 | 9.617 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `ax` | `strict_current` | 10.642 | 1.461 | 7.283 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 37.521 | 1.107 | 33.906 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `classic` | `strict_current` | 37.521 | 1.461 | 25.678 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 11.793 | 0.688 | 17.152 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `ax` | `strict_current` | 11.793 | 1.162 | 10.150 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 42.297 | 0.688 | 61.516 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `classic` | `strict_current` | 42.297 | 1.162 | 36.403 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.365 | 0.723 | 14.342 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `ax` | `strict_current` | 10.365 | 1.450 | 7.150 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 39.551 | 0.723 | 54.726 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `classic` | `strict_current` | 39.551 | 1.450 | 27.283 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 8.149 | 1.881 | 4.333 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 8.149 | 4.078 | 1.998 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 31.573 | 1.881 | 16.788 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 31.573 | 4.078 | 7.742 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.356 | 1.757 | 4.755 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `ax` | `strict_current` | 8.356 | 3.872 | 2.158 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 29.594 | 1.757 | 16.842 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `classic` | `strict_current` | 29.594 | 3.872 | 7.642 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.387 | 1.545 | 6.074 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `ax` | `strict_current` | 9.387 | 3.971 | 2.364 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 31.788 | 1.545 | 20.569 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `classic` | `strict_current` | 31.788 | 3.971 | 8.005 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.064 | 1.408 | 5.728 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `ax` | `strict_current` | 8.064 | 4.021 | 2.005 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 30.391 | 1.408 | 21.589 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `classic` | `strict_current` | 30.391 | 4.021 | 7.558 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 20.928 | 0.633 | 33.038 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `ax` | `strict_current` | 20.928 | 0.715 | 29.274 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 33.659 | 0.633 | 53.134 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `classic` | `strict_current` | 33.659 | 0.715 | 47.081 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 22.225 | 1.126 | 19.731 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `ax` | `strict_current` | 22.225 | 1.167 | 19.044 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 35.656 | 1.126 | 31.655 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `classic` | `strict_current` | 35.656 | 1.167 | 30.552 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.181 | 0.552 | 14.832 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `ax` | `strict_current` | 8.181 | 0.872 | 9.379 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 34.874 | 0.552 | 63.229 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `classic` | `strict_current` | 34.874 | 0.872 | 39.983 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.912 | 0.673 | 16.221 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `ax` | `strict_current` | 10.912 | 1.001 | 10.900 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 34.076 | 0.673 | 50.656 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `classic` | `strict_current` | 34.076 | 1.001 | 34.039 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 8.139 | 1.964 | 4.144 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 8.139 | 3.297 | 2.468 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 31.085 | 1.964 | 15.827 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 31.085 | 3.297 | 9.428 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.001 | 3.302 | 2.423 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `ax` | `strict_current` | 8.001 | 4.047 | 1.977 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 28.850 | 3.302 | 8.737 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `classic` | `strict_current` | 28.850 | 4.047 | 7.128 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.453 | 2.323 | 3.208 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `ax` | `strict_current` | 7.453 | 4.113 | 1.812 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.095 | 2.323 | 14.246 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `classic` | `strict_current` | 33.095 | 4.113 | 8.047 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.542 | 1.460 | 5.165 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `ax` | `strict_current` | 7.542 | 2.944 | 2.562 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 38.063 | 1.460 | 26.065 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `classic` | `strict_current` | 38.063 | 2.944 | 12.931 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 33.661 | 1.699 | 19.808 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `ax` | `strict_current` | 33.661 | 9.063 | 3.714 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 91.299 | 1.699 | 53.726 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `classic` | `strict_current` | 91.299 | 9.063 | 10.073 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 29.873 | 3.128 | 9.549 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `ax` | `strict_current` | 29.873 | 11.479 | 2.602 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 106.013 | 3.128 | 33.887 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `classic` | `strict_current` | 106.013 | 11.479 | 9.235 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.298 | 1.095 | 7.575 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `ax` | `strict_current` | 8.298 | 1.403 | 5.913 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 32.774 | 1.095 | 29.920 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `classic` | `strict_current` | 32.774 | 1.403 | 23.354 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.461 | 0.558 | 15.153 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `ax` | `strict_current` | 8.461 | 1.488 | 5.684 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 31.910 | 0.558 | 57.148 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `classic` | `strict_current` | 31.910 | 1.488 | 21.439 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.302 | 5.878 | 1.582 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `ax` | `strict_current` | 9.302 | 4.003 | 2.324 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.276 | 5.878 | 4.470 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `classic` | `strict_current` | 26.276 | 4.003 | 6.564 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.947 | 8.877 | 1.008 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `ax` | `strict_current` | 8.947 | 9.903 | 0.903 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.266 | 8.877 | 3.071 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `classic` | `strict_current` | 27.266 | 9.903 | 2.753 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.883 | 0.578 | 15.377 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `ax` | `strict_current` | 8.883 | 1.271 | 6.990 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 36.586 | 0.578 | 63.334 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `classic` | `strict_current` | 36.586 | 1.271 | 28.792 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.292 | 0.689 | 14.948 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `ax` | `strict_current` | 10.292 | 1.369 | 7.516 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 36.732 | 0.689 | 53.346 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `classic` | `strict_current` | 36.732 | 1.369 | 26.823 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.305 | 0.828 | 10.036 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `ax` | `strict_current` | 8.305 | 0.782 | 10.619 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 34.561 | 0.828 | 41.761 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `classic` | `strict_current` | 34.561 | 0.782 | 44.187 |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.032 | 0.750 | 12.037 |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `ax` | `strict_current` | 9.032 | 0.757 | 11.925 |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 35.821 | 0.750 | 47.739 |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `classic` | `strict_current` | 35.821 | 0.757 | 47.295 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.550 | 0.674 | 12.680 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `ax` | `strict_current` | 8.550 | 1.383 | 6.181 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.037 | 0.674 | 48.998 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `classic` | `strict_current` | 33.037 | 1.383 | 23.886 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.087 | 0.607 | 14.975 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `ax` | `strict_current` | 9.087 | 1.405 | 6.469 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 31.077 | 0.607 | 51.213 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `classic` | `strict_current` | 31.077 | 1.405 | 22.123 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 11.289 | 1.146 | 9.846 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `ax` | `strict_current` | 11.289 | 1.455 | 7.757 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 36.686 | 1.146 | 31.998 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `classic` | `strict_current` | 36.686 | 1.455 | 25.207 |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.759 | 1.110 | 7.888 |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `ax` | `strict_current` | 8.759 | 1.711 | 5.118 |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 32.808 | 1.110 | 29.545 |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `classic` | `strict_current` | 32.808 | 1.711 | 19.170 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.641 | 96.532 | 0.079 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `ax` | `strict_current` | 7.641 | 97.329 | 0.079 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.018 | 96.532 | 0.342 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `classic` | `strict_current` | 33.018 | 97.329 | 0.339 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.990 | 54.861 | 0.146 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `ax` | `strict_current` | 7.990 | 46.755 | 0.171 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 35.193 | 54.861 | 0.641 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `classic` | `strict_current` | 35.193 | 46.755 | 0.753 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 11.327 | 1.423 | 7.961 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `ax` | `strict_current` | 11.327 | 2.382 | 4.756 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 32.393 | 1.423 | 22.766 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `classic` | `strict_current` | 32.393 | 2.382 | 13.601 |
| `vbr1_l2_event_controller` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.529 | 2.008 | 4.247 |
| `vbr1_l2_event_controller` | `tb` | `gold` | `ax` | `strict_current` | 8.529 | 2.425 | 3.517 |
| `vbr1_l2_event_controller` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 35.444 | 2.008 | 17.648 |
| `vbr1_l2_event_controller` | `tb` | `gold` | `classic` | `strict_current` | 35.444 | 2.425 | 14.614 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.793 | 0.851 | 10.338 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `ax` | `strict_current` | 8.793 | 1.622 | 5.421 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 32.152 | 0.851 | 37.802 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `classic` | `strict_current` | 32.152 | 1.622 | 19.822 |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.014 | 0.687 | 11.673 |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `ax` | `strict_current` | 8.014 | 1.477 | 5.426 |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 32.438 | 0.687 | 47.246 |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `classic` | `strict_current` | 32.438 | 1.477 | 21.961 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.729 | 9.362 | 1.039 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `ax` | `strict_current` | 9.729 | 128.097 | 0.076 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 45.237 | 9.362 | 4.832 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `classic` | `strict_current` | 45.237 | 128.097 | 0.353 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 11.051 | 33.137 | 0.333 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `ax` | `strict_current` | 11.051 | 153.491 | 0.072 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 49.652 | 33.137 | 1.498 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `classic` | `strict_current` | 49.652 | 153.491 | 0.323 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.960 | 1.338 | 5.200 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `ax` | `strict_current` | 6.960 | 2.110 | 3.298 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 35.376 | 1.338 | 26.433 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `classic` | `strict_current` | 35.376 | 2.110 | 16.763 |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.625 | 1.347 | 6.403 |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `ax` | `strict_current` | 8.625 | 2.129 | 4.051 |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 31.153 | 1.347 | 23.127 |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `classic` | `strict_current` | 31.153 | 2.129 | 14.633 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.579 | 25.062 | 0.223 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `ax` | `strict_current` | 5.579 | 25.028 | 0.223 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 75.773 | 25.062 | 3.023 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `classic` | `strict_current` | 75.773 | 25.028 | 3.028 |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.642 | 37.297 | 0.151 |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `ax` | `strict_current` | 5.642 | 75.211 | 0.075 |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 18.828 | 37.297 | 0.505 |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `classic` | `strict_current` | 18.828 | 75.211 | 0.250 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.859 | 1.241 | 7.137 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `ax` | `strict_current` | 8.859 | 1.831 | 4.838 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.766 | 1.241 | 27.204 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `classic` | `strict_current` | 33.766 | 1.831 | 18.441 |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.652 | 0.935 | 8.182 |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `ax` | `strict_current` | 7.652 | 1.869 | 4.095 |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 31.186 | 0.935 | 33.345 |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `classic` | `strict_current` | 31.186 | 1.869 | 16.688 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.106 | 1.722 | 3.546 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `ax` | `strict_current` | 6.106 | 17.412 | 0.351 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 40.718 | 1.722 | 23.648 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `classic` | `strict_current` | 40.718 | 17.412 | 2.339 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.024 | 7.606 | 0.792 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `ax` | `strict_current` | 6.024 | 25.830 | 0.233 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 40.533 | 7.606 | 5.329 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `classic` | `strict_current` | 40.533 | 25.830 | 1.569 |

## Interpretation Guardrails

- Speedups use `simulation_ok`, so rows without a behavior checker can still contribute timing if the simulator produced waveforms.
- Accuracy-gated speedups require candidate behavior pass, strict-EVAS parity, and parity to every selected Spectre mode.
- `spectre/ax` matches the previous bridge default but Spectre X may ignore `errpreset` and `maxstep` from the testbench.
- `spectre/classic` is available to measure the stricter non-X path when requested.
- Cold Spectre runs include AHDL CMI compilation; warm-cache repetitions should be reported separately.
- A `BLOCKED` gate is not evidence of wrong behavior; it means the checker or reference evidence is incomplete.
