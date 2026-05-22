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
- Output root: `results/same-server-speed-cold-r1-goal-20260522`

## Mode Summary

| Backend | Mode | Runs | PASS | Non-PASS | Total wall s | Mean wall s |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| evas | profile_fast_skip_source_error_control | 259 | 259 | 0 | 507.239 | 1.958 |
| evas | strict_current | 259 | 259 | 0 | 1512.785 | 5.841 |
| spectre | ax | 259 | 259 | 0 | 2035.927 | 7.861 |
| spectre | classic | 259 | 259 | 0 | 6187.572 | 23.890 |

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
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.974 | 1.096 | 6.363 |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.974 | 1.405 | 4.965 |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.726 | 1.096 | 23.469 |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.726 | 1.405 | 18.314 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.075 | 1.099 | 6.437 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `ax` | `strict_current` | 7.075 | 1.446 | 4.892 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.160 | 1.099 | 21.981 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `classic` | `strict_current` | 24.160 | 1.446 | 16.706 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.726 | 1.156 | 4.951 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `ax` | `strict_current` | 5.726 | 1.339 | 4.275 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.547 | 1.156 | 21.225 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `classic` | `strict_current` | 24.547 | 1.339 | 18.327 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.802 | 1.179 | 6.619 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `ax` | `strict_current` | 7.802 | 1.535 | 5.085 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.919 | 1.179 | 21.141 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `classic` | `strict_current` | 24.919 | 1.535 | 16.239 |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.255 | 1.456 | 4.298 |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.255 | 10.932 | 0.572 |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 23.086 | 1.456 | 15.861 |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 23.086 | 10.932 | 2.112 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.468 | 1.489 | 4.343 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `ax` | `strict_current` | 6.468 | 10.720 | 0.603 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 22.851 | 1.489 | 15.344 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `classic` | `strict_current` | 22.851 | 10.720 | 2.132 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.434 | 1.829 | 3.517 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `ax` | `strict_current` | 6.434 | 1.983 | 3.245 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.937 | 1.829 | 13.085 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `classic` | `strict_current` | 23.937 | 1.983 | 12.073 |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.369 | 1.631 | 3.905 |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `ax` | `strict_current` | 6.369 | 1.902 | 3.349 |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.013 | 1.631 | 15.337 |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `classic` | `strict_current` | 25.013 | 1.902 | 13.153 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 17.108 | 0.928 | 18.435 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `ax` | `strict_current` | 17.108 | 1.344 | 12.725 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 27.066 | 0.928 | 29.165 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `classic` | `strict_current` | 27.066 | 1.344 | 20.131 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 15.943 | 0.854 | 18.674 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `ax` | `strict_current` | 15.943 | 0.954 | 16.705 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.620 | 0.854 | 32.352 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `classic` | `strict_current` | 27.620 | 0.954 | 28.939 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 18.676 | 0.761 | 24.545 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `ax` | `strict_current` | 18.676 | 1.030 | 18.127 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 29.079 | 0.761 | 38.216 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `classic` | `strict_current` | 29.079 | 1.030 | 28.223 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.350 | 0.849 | 7.476 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `ax` | `strict_current` | 6.350 | 0.798 | 7.960 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.598 | 0.849 | 30.135 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `classic` | `strict_current` | 25.598 | 0.798 | 32.089 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.268 | 0.965 | 6.498 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `ax` | `strict_current` | 6.268 | 1.344 | 4.665 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.034 | 0.965 | 25.953 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `classic` | `strict_current` | 25.034 | 1.344 | 18.630 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.392 | 1.028 | 6.217 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `ax` | `strict_current` | 6.392 | 1.483 | 4.310 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.713 | 1.028 | 25.011 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `classic` | `strict_current` | 25.713 | 1.483 | 17.339 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.372 | 1.014 | 6.281 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `ax` | `strict_current` | 6.372 | 1.377 | 4.628 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.818 | 1.014 | 27.423 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `classic` | `strict_current` | 27.818 | 1.377 | 20.204 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.515 | 0.831 | 7.841 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.515 | 1.622 | 4.018 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.037 | 0.831 | 30.132 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.037 | 1.622 | 15.438 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.325 | 0.857 | 7.380 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `ax` | `strict_current` | 6.325 | 1.631 | 3.878 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.210 | 0.857 | 29.414 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `classic` | `strict_current` | 25.210 | 1.631 | 15.455 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.396 | 0.927 | 6.903 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `ax` | `strict_current` | 6.396 | 1.576 | 4.058 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.711 | 0.927 | 27.749 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `classic` | `strict_current` | 25.711 | 1.576 | 16.312 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.575 | 0.858 | 7.660 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `ax` | `strict_current` | 6.575 | 1.603 | 4.103 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.338 | 0.858 | 28.352 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `classic` | `strict_current` | 24.338 | 1.603 | 15.186 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.472 | 1.719 | 3.764 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.472 | 3.599 | 1.798 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.290 | 1.719 | 14.128 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.290 | 3.599 | 6.748 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.244 | 1.664 | 3.753 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `ax` | `strict_current` | 6.244 | 3.472 | 1.798 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.555 | 1.664 | 14.156 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `classic` | `strict_current` | 23.555 | 3.472 | 6.784 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.118 | 1.727 | 3.542 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `ax` | `strict_current` | 6.118 | 3.416 | 1.791 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.923 | 1.727 | 13.851 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `classic` | `strict_current` | 23.923 | 3.416 | 7.003 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.494 | 1.798 | 3.611 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `ax` | `strict_current` | 6.494 | 3.446 | 1.885 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.138 | 1.798 | 13.421 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `classic` | `strict_current` | 24.138 | 3.446 | 7.005 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.135 | 0.948 | 6.468 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.135 | 1.645 | 3.731 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.806 | 0.948 | 26.153 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.806 | 1.645 | 15.083 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.990 | 0.816 | 7.343 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `ax` | `strict_current` | 5.990 | 1.567 | 3.822 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.053 | 0.816 | 29.486 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `classic` | `strict_current` | 24.053 | 1.567 | 15.348 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.879 | 0.866 | 7.944 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `ax` | `strict_current` | 6.879 | 1.609 | 4.277 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.498 | 0.866 | 30.600 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `classic` | `strict_current` | 26.498 | 1.609 | 16.474 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.298 | 0.908 | 6.938 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `ax` | `strict_current` | 6.298 | 1.651 | 3.815 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.857 | 0.908 | 26.283 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `classic` | `strict_current` | 23.857 | 1.651 | 14.452 |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.588 | 1.384 | 4.760 |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.588 | 4.028 | 1.636 |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 23.354 | 1.384 | 16.873 |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `classic` | `strict_current` | 23.354 | 4.028 | 5.798 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.602 | 1.413 | 4.673 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `ax` | `strict_current` | 6.602 | 4.048 | 1.631 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.029 | 1.413 | 17.005 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `classic` | `strict_current` | 24.029 | 4.048 | 5.936 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.888 | 1.485 | 3.964 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `ax` | `strict_current` | 5.888 | 4.065 | 1.449 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.660 | 1.485 | 16.602 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `classic` | `strict_current` | 24.660 | 4.065 | 6.067 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.014 | 1.447 | 4.156 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `ax` | `strict_current` | 6.014 | 4.125 | 1.458 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.897 | 1.447 | 17.203 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `classic` | `strict_current` | 24.897 | 4.125 | 6.036 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.145 | 0.985 | 6.238 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.145 | 1.712 | 3.589 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.501 | 0.985 | 24.875 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.501 | 1.712 | 14.312 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.981 | 0.982 | 7.108 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `ax` | `strict_current` | 6.981 | 1.648 | 4.236 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.312 | 0.982 | 24.755 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `classic` | `strict_current` | 24.312 | 1.648 | 14.752 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.999 | 1.072 | 6.531 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `ax` | `strict_current` | 6.999 | 1.677 | 4.172 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.478 | 1.072 | 23.776 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `classic` | `strict_current` | 25.478 | 1.677 | 15.189 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.697 | 0.947 | 7.075 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `ax` | `strict_current` | 6.697 | 1.700 | 3.939 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.526 | 0.947 | 26.966 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `classic` | `strict_current` | 25.526 | 1.700 | 15.015 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.878 | 1.188 | 5.788 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.878 | 3.203 | 2.147 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 23.115 | 1.188 | 19.453 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 23.115 | 3.203 | 7.217 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.379 | 1.288 | 4.952 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `ax` | `strict_current` | 6.379 | 3.274 | 1.948 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.564 | 1.288 | 18.294 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `classic` | `strict_current` | 23.564 | 3.274 | 7.198 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.524 | 1.221 | 5.342 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 6.524 | 3.171 | 2.057 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.953 | 1.221 | 19.612 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 23.953 | 3.171 | 7.554 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.512 | 1.379 | 4.723 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `ax` | `strict_current` | 6.512 | 3.277 | 1.987 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.855 | 1.379 | 17.300 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `classic` | `strict_current` | 23.855 | 3.277 | 7.279 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.625 | 0.935 | 7.088 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.625 | 1.557 | 4.256 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 14.121 | 0.935 | 15.107 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `classic` | `strict_current` | 14.121 | 1.557 | 9.071 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.708 | 0.936 | 7.163 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `ax` | `strict_current` | 6.708 | 1.759 | 3.813 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.976 | 0.936 | 14.924 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `classic` | `strict_current` | 13.976 | 1.759 | 7.943 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.792 | 0.940 | 6.164 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `ax` | `strict_current` | 5.792 | 1.552 | 3.732 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.378 | 0.940 | 14.236 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `classic` | `strict_current` | 13.378 | 1.552 | 8.619 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.720 | 1.181 | 5.689 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `ax` | `strict_current` | 6.720 | 1.560 | 4.307 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.505 | 1.181 | 11.433 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `classic` | `strict_current` | 13.505 | 1.560 | 8.655 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.795 | 0.836 | 9.320 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `ax` | `strict_current` | 7.795 | 1.045 | 7.460 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.674 | 0.836 | 18.741 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `classic` | `strict_current` | 15.674 | 1.045 | 15.001 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.044 | 0.754 | 9.341 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `ax` | `strict_current` | 7.044 | 1.052 | 6.699 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.559 | 0.754 | 20.631 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `classic` | `strict_current` | 15.559 | 1.052 | 14.796 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.827 | 0.952 | 7.174 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `ax` | `strict_current` | 6.827 | 0.867 | 7.877 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.827 | 0.952 | 16.630 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `classic` | `strict_current` | 15.827 | 0.867 | 18.260 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.698 | 0.808 | 8.292 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.698 | 0.816 | 8.205 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.296 | 0.808 | 31.313 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.296 | 0.816 | 30.987 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.711 | 0.767 | 8.748 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `ax` | `strict_current` | 6.711 | 1.022 | 6.564 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.792 | 0.767 | 33.622 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `classic` | `strict_current` | 25.792 | 1.022 | 25.228 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.974 | 0.895 | 8.905 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `ax` | `strict_current` | 7.974 | 0.945 | 8.440 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.099 | 0.895 | 29.146 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `classic` | `strict_current` | 26.099 | 0.945 | 27.622 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.007 | 0.756 | 9.269 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `ax` | `strict_current` | 7.007 | 0.806 | 8.696 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.914 | 0.756 | 32.958 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `classic` | `strict_current` | 24.914 | 0.806 | 30.917 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 19.854 | 0.849 | 23.375 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `ax` | `strict_current` | 19.854 | 1.067 | 18.614 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 28.553 | 0.849 | 33.617 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `classic` | `strict_current` | 28.553 | 1.067 | 26.769 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.870 | 0.886 | 7.756 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `ax` | `strict_current` | 6.870 | 1.019 | 6.740 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 30.621 | 0.886 | 34.573 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `classic` | `strict_current` | 30.621 | 1.019 | 30.041 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.474 | 0.791 | 8.188 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `ax` | `strict_current` | 6.474 | 0.962 | 6.730 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.073 | 0.791 | 31.712 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `classic` | `strict_current` | 25.073 | 0.962 | 26.064 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 15.847 | 0.840 | 18.865 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `ax` | `strict_current` | 15.847 | 1.033 | 15.338 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.120 | 0.840 | 31.093 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `classic` | `strict_current` | 26.120 | 1.033 | 25.281 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.172 | 0.942 | 6.555 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.172 | 4.572 | 1.350 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.046 | 0.942 | 25.539 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.046 | 4.572 | 5.259 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.474 | 1.007 | 6.426 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `ax` | `strict_current` | 6.474 | 4.664 | 1.388 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.441 | 1.007 | 23.268 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `classic` | `strict_current` | 23.441 | 4.664 | 5.026 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.482 | 1.018 | 6.367 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `ax` | `strict_current` | 6.482 | 4.643 | 1.396 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.181 | 1.018 | 24.735 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `classic` | `strict_current` | 25.181 | 4.643 | 5.423 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.523 | 1.022 | 6.383 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `ax` | `strict_current` | 6.523 | 4.592 | 1.421 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.523 | 1.022 | 24.000 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `classic` | `strict_current` | 24.523 | 4.592 | 5.341 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.322 | 1.668 | 3.791 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.322 | 1.737 | 3.641 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.704 | 1.668 | 14.813 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.704 | 1.737 | 14.226 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.183 | 1.640 | 4.379 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `ax` | `strict_current` | 7.183 | 1.651 | 4.351 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.659 | 1.640 | 15.642 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `classic` | `strict_current` | 25.659 | 1.651 | 15.543 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.655 | 1.554 | 4.283 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `ax` | `strict_current` | 6.655 | 1.560 | 4.266 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.729 | 1.554 | 15.915 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `classic` | `strict_current` | 24.729 | 1.560 | 15.850 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.164 | 1.785 | 4.015 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `ax` | `strict_current` | 7.164 | 1.617 | 4.432 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.839 | 1.785 | 13.919 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `classic` | `strict_current` | 24.839 | 1.617 | 15.366 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.980 | 0.802 | 7.459 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `ax` | `strict_current` | 5.980 | 0.897 | 6.664 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 11.632 | 0.802 | 14.509 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `classic` | `strict_current` | 11.632 | 0.897 | 12.962 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.946 | 0.993 | 6.995 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `ax` | `strict_current` | 6.946 | 0.804 | 8.640 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.195 | 0.993 | 14.295 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `classic` | `strict_current` | 14.195 | 0.804 | 17.656 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.622 | 0.874 | 7.577 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `ax` | `strict_current` | 6.622 | 0.837 | 7.907 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.234 | 0.874 | 15.143 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `classic` | `strict_current` | 13.234 | 0.837 | 15.803 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.031 | 0.868 | 8.101 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.031 | 2.589 | 2.715 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 46.073 | 0.868 | 53.090 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `classic` | `strict_current` | 46.073 | 2.589 | 17.794 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.936 | 0.973 | 7.132 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `ax` | `strict_current` | 6.936 | 2.565 | 2.704 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 44.633 | 0.973 | 45.894 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `classic` | `strict_current` | 44.633 | 2.565 | 17.401 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.366 | 0.852 | 8.643 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `ax` | `strict_current` | 7.366 | 2.638 | 2.792 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 45.124 | 0.852 | 52.946 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `classic` | `strict_current` | 45.124 | 2.638 | 17.103 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.123 | 0.888 | 9.144 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `ax` | `strict_current` | 8.123 | 2.542 | 3.196 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 45.649 | 0.888 | 51.388 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `classic` | `strict_current` | 45.649 | 2.542 | 17.960 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 17.071 | 0.888 | 19.218 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 17.071 | 0.949 | 17.986 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 29.637 | 0.888 | 33.365 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 29.637 | 0.949 | 31.226 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 19.918 | 1.255 | 15.876 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `ax` | `strict_current` | 19.918 | 0.853 | 23.344 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 30.136 | 1.255 | 24.020 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `classic` | `strict_current` | 30.136 | 0.853 | 35.320 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.875 | 0.922 | 7.457 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `ax` | `strict_current` | 6.875 | 0.993 | 6.925 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.195 | 0.922 | 27.330 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `classic` | `strict_current` | 25.195 | 0.993 | 25.379 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 18.775 | 0.846 | 22.179 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `ax` | `strict_current` | 18.775 | 1.007 | 18.642 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 29.323 | 0.846 | 34.640 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `classic` | `strict_current` | 29.323 | 1.007 | 29.115 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.374 | 1.347 | 4.732 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `ax` | `strict_current` | 6.374 | 4.633 | 1.376 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.368 | 1.347 | 17.347 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `classic` | `strict_current` | 23.368 | 4.633 | 5.044 |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.823 | 1.475 | 3.947 |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `ax` | `strict_current` | 5.823 | 4.595 | 1.267 |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 22.860 | 1.475 | 15.495 |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `classic` | `strict_current` | 22.860 | 4.595 | 4.975 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.830 | 1.008 | 6.774 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.830 | 1.061 | 6.436 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.882 | 1.008 | 25.671 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.882 | 1.061 | 24.391 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.444 | 0.989 | 7.527 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `ax` | `strict_current` | 7.444 | 1.194 | 6.234 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.453 | 0.989 | 26.748 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `classic` | `strict_current` | 26.453 | 1.194 | 22.154 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.345 | 0.802 | 7.914 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `ax` | `strict_current` | 6.345 | 0.998 | 6.360 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.215 | 0.802 | 31.451 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `classic` | `strict_current` | 25.215 | 0.998 | 25.275 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.432 | 0.779 | 8.261 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `ax` | `strict_current` | 6.432 | 1.176 | 5.472 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.251 | 0.779 | 33.713 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `classic` | `strict_current` | 26.251 | 1.176 | 22.331 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.448 | 0.848 | 7.606 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.448 | 0.969 | 6.651 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.215 | 0.848 | 28.563 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.215 | 0.969 | 24.979 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.946 | 0.882 | 7.879 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `ax` | `strict_current` | 6.946 | 1.075 | 6.462 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.692 | 0.882 | 28.009 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `classic` | `strict_current` | 24.692 | 1.075 | 22.972 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.650 | 0.925 | 7.188 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `ax` | `strict_current` | 6.650 | 1.110 | 5.992 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.287 | 0.925 | 27.332 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `classic` | `strict_current` | 25.287 | 1.110 | 22.784 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.124 | 0.828 | 7.401 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `ax` | `strict_current` | 6.124 | 0.921 | 6.649 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.121 | 0.828 | 29.148 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `classic` | `strict_current` | 24.121 | 0.921 | 26.188 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 14.776 | 1.147 | 12.878 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `ax` | `strict_current` | 14.776 | 1.187 | 12.447 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 13.727 | 1.147 | 11.964 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `classic` | `strict_current` | 13.727 | 1.187 | 11.563 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.511 | 1.094 | 5.952 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `ax` | `strict_current` | 6.511 | 1.153 | 5.648 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.068 | 1.094 | 11.944 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `classic` | `strict_current` | 13.068 | 1.153 | 11.334 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 15.635 | 1.206 | 12.964 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `ax` | `strict_current` | 15.635 | 1.106 | 14.143 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.456 | 1.206 | 11.986 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `classic` | `strict_current` | 14.456 | 1.106 | 13.076 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.536 | 1.019 | 6.414 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `ax` | `strict_current` | 6.536 | 1.271 | 5.142 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.849 | 1.019 | 14.572 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `classic` | `strict_current` | 14.849 | 1.271 | 11.682 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.482 | 9.873 | 1.062 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `ax` | `strict_current` | 10.482 | 127.882 | 0.082 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 48.524 | 9.873 | 4.915 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `classic` | `strict_current` | 48.524 | 127.882 | 0.379 |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.054 | 38.791 | 0.259 |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `ax` | `strict_current` | 10.054 | 149.272 | 0.067 |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 48.478 | 38.791 | 1.250 |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `classic` | `strict_current` | 48.478 | 149.272 | 0.325 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 15.109 | 1.150 | 13.143 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `ax` | `strict_current` | 15.109 | 1.819 | 8.306 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 14.483 | 1.150 | 12.599 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `classic` | `strict_current` | 14.483 | 1.819 | 7.962 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 15.929 | 1.134 | 14.047 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `ax` | `strict_current` | 15.929 | 1.766 | 9.019 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.749 | 1.134 | 12.125 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `classic` | `strict_current` | 13.749 | 1.766 | 7.785 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.519 | 1.080 | 6.038 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `ax` | `strict_current` | 6.519 | 1.696 | 3.845 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.767 | 1.080 | 12.752 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `classic` | `strict_current` | 13.767 | 1.696 | 8.120 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.644 | 1.244 | 5.342 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `ax` | `strict_current` | 6.644 | 1.766 | 3.763 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.591 | 1.244 | 10.928 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `classic` | `strict_current` | 13.591 | 1.766 | 7.697 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.651 | 0.883 | 7.529 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.651 | 1.344 | 4.948 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.382 | 0.883 | 27.604 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.382 | 1.344 | 18.141 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.396 | 0.859 | 7.445 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `ax` | `strict_current` | 6.396 | 1.255 | 5.094 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.341 | 0.859 | 28.334 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `classic` | `strict_current` | 24.341 | 1.255 | 19.388 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.606 | 0.849 | 7.781 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `ax` | `strict_current` | 6.606 | 1.379 | 4.788 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.486 | 0.849 | 28.843 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `classic` | `strict_current` | 24.486 | 1.379 | 17.750 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.683 | 0.883 | 7.572 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `ax` | `strict_current` | 6.683 | 1.414 | 4.727 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.639 | 0.883 | 29.046 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `classic` | `strict_current` | 25.639 | 1.414 | 18.134 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.512 | 1.229 | 6.114 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.512 | 1.312 | 5.724 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.127 | 1.229 | 20.450 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.127 | 1.312 | 19.148 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.685 | 1.047 | 6.386 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `ax` | `strict_current` | 6.685 | 1.046 | 6.392 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.680 | 1.047 | 25.486 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `classic` | `strict_current` | 26.680 | 1.046 | 25.510 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.214 | 0.980 | 7.359 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 7.214 | 1.037 | 6.959 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.503 | 0.980 | 27.036 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 26.503 | 1.037 | 25.564 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.007 | 1.030 | 6.804 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `ax` | `strict_current` | 7.007 | 0.922 | 7.600 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.000 | 1.030 | 25.247 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `classic` | `strict_current` | 26.000 | 0.922 | 28.203 |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 5.969 | 1.825 | 3.271 |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `ax` | `strict_current` | 5.969 | 4.528 | 1.318 |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 23.987 | 1.825 | 13.146 |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `classic` | `strict_current` | 23.987 | 4.528 | 5.298 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.607 | 1.771 | 3.165 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `ax` | `strict_current` | 5.607 | 4.957 | 1.131 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.212 | 1.771 | 13.668 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `classic` | `strict_current` | 24.212 | 4.957 | 4.884 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.956 | 1.769 | 3.933 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `ax` | `strict_current` | 6.956 | 2.928 | 2.376 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.914 | 1.769 | 13.520 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `classic` | `strict_current` | 23.914 | 2.928 | 8.168 |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.400 | 1.670 | 3.832 |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `ax` | `strict_current` | 6.400 | 2.911 | 2.199 |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.341 | 1.670 | 14.573 |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `classic` | `strict_current` | 24.341 | 2.911 | 8.363 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 15.456 | 0.908 | 17.025 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 15.456 | 1.088 | 14.208 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 27.530 | 0.908 | 30.325 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 27.530 | 1.088 | 25.308 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.885 | 0.858 | 8.026 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `ax` | `strict_current` | 6.885 | 1.015 | 6.785 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.735 | 0.858 | 28.832 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `classic` | `strict_current` | 24.735 | 1.015 | 24.376 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 18.483 | 0.909 | 20.330 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `ax` | `strict_current` | 18.483 | 0.907 | 20.371 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 28.771 | 0.909 | 31.647 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `classic` | `strict_current` | 28.771 | 0.907 | 31.710 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.551 | 0.962 | 6.808 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `ax` | `strict_current` | 6.551 | 1.220 | 5.368 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.584 | 0.962 | 25.549 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `classic` | `strict_current` | 24.584 | 1.220 | 20.144 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.208 | 0.827 | 8.720 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.208 | 1.660 | 4.342 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.926 | 0.827 | 30.155 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.926 | 1.660 | 15.016 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.366 | 0.788 | 8.075 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `ax` | `strict_current` | 6.366 | 1.640 | 3.882 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.316 | 0.788 | 29.574 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `classic` | `strict_current` | 23.316 | 1.640 | 14.218 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.606 | 0.868 | 7.607 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `ax` | `strict_current` | 6.606 | 1.671 | 3.953 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.062 | 0.868 | 28.857 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `classic` | `strict_current` | 25.062 | 1.671 | 14.996 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.216 | 0.949 | 6.553 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `ax` | `strict_current` | 6.216 | 1.791 | 3.471 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.666 | 0.949 | 24.947 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `classic` | `strict_current` | 23.666 | 1.791 | 13.216 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 15.619 | 1.199 | 13.031 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 15.619 | 1.423 | 10.976 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 13.315 | 1.199 | 11.109 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 13.315 | 1.423 | 9.356 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 15.125 | 1.141 | 13.251 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `ax` | `strict_current` | 15.125 | 1.302 | 11.621 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.525 | 1.141 | 12.726 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `classic` | `strict_current` | 14.525 | 1.302 | 11.160 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.333 | 1.084 | 5.843 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 6.333 | 1.303 | 4.860 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.195 | 1.084 | 12.172 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 13.195 | 1.303 | 10.125 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.757 | 1.057 | 6.393 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `ax` | `strict_current` | 6.757 | 1.366 | 4.947 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.243 | 1.057 | 13.476 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `classic` | `strict_current` | 14.243 | 1.366 | 10.428 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.274 | 0.862 | 7.281 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.274 | 1.053 | 5.957 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.839 | 0.862 | 28.827 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.839 | 1.053 | 23.585 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.161 | 0.985 | 6.254 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `ax` | `strict_current` | 6.161 | 1.028 | 5.995 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.040 | 0.985 | 26.434 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `classic` | `strict_current` | 26.040 | 1.028 | 25.341 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.292 | 0.907 | 6.941 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `ax` | `strict_current` | 6.292 | 0.960 | 6.553 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.399 | 0.907 | 28.015 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `classic` | `strict_current` | 25.399 | 0.960 | 26.450 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.317 | 0.931 | 6.788 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `ax` | `strict_current` | 6.317 | 1.103 | 5.728 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.756 | 0.931 | 26.603 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `classic` | `strict_current` | 24.756 | 1.103 | 22.447 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.341 | 0.873 | 7.266 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.341 | 1.018 | 6.229 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 14.507 | 0.873 | 16.624 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 14.507 | 1.018 | 14.251 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.049 | 0.824 | 7.344 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `ax` | `strict_current` | 6.049 | 0.992 | 6.100 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.971 | 0.824 | 18.175 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `classic` | `strict_current` | 14.971 | 0.992 | 15.096 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.379 | 0.951 | 6.707 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `ax` | `strict_current` | 6.379 | 1.054 | 6.053 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.969 | 0.951 | 14.687 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `classic` | `strict_current` | 13.969 | 1.054 | 13.255 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.419 | 0.934 | 6.870 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `ax` | `strict_current` | 6.419 | 0.991 | 6.476 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.372 | 0.934 | 16.450 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `classic` | `strict_current` | 15.372 | 0.991 | 15.508 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 4.956 | 15.864 | 0.312 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `ax` | `strict_current` | 4.956 | 33.042 | 0.150 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 17.765 | 15.864 | 1.120 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `classic` | `strict_current` | 17.765 | 33.042 | 0.538 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 4.409 | 16.041 | 0.275 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `ax` | `strict_current` | 4.409 | 33.159 | 0.133 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 17.629 | 16.041 | 1.099 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `classic` | `strict_current` | 17.629 | 33.159 | 0.532 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 4.507 | 16.157 | 0.279 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `ax` | `strict_current` | 4.507 | 33.251 | 0.136 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 18.177 | 16.157 | 1.125 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `classic` | `strict_current` | 18.177 | 33.251 | 0.547 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 4.351 | 15.648 | 0.278 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `ax` | `strict_current` | 4.351 | 33.807 | 0.129 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 17.090 | 15.648 | 1.092 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `classic` | `strict_current` | 17.090 | 33.807 | 0.506 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 11.612 | 11.546 | 1.006 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `ax` | `strict_current` | 11.612 | 67.666 | 0.172 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 17.996 | 11.546 | 1.559 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `classic` | `strict_current` | 17.996 | 67.666 | 0.266 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 4.426 | 8.630 | 0.513 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `ax` | `strict_current` | 4.426 | 66.681 | 0.066 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 17.050 | 8.630 | 1.976 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `classic` | `strict_current` | 17.050 | 66.681 | 0.256 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.099 | 8.458 | 0.603 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `ax` | `strict_current` | 5.099 | 68.518 | 0.074 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 16.136 | 8.458 | 1.908 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `classic` | `strict_current` | 16.136 | 68.518 | 0.236 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.999 | 8.505 | 1.293 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `ax` | `strict_current` | 10.999 | 67.325 | 0.163 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 17.751 | 8.505 | 2.087 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `classic` | `strict_current` | 17.751 | 67.325 | 0.264 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.290 | 0.783 | 9.312 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.290 | 1.368 | 5.327 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 14.100 | 0.783 | 18.012 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `classic` | `strict_current` | 14.100 | 1.368 | 10.304 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.203 | 0.798 | 7.772 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `ax` | `strict_current` | 6.203 | 1.240 | 5.004 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.527 | 0.798 | 16.950 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `classic` | `strict_current` | 13.527 | 1.240 | 10.913 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.386 | 0.867 | 7.362 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `ax` | `strict_current` | 6.386 | 1.137 | 5.616 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.078 | 0.867 | 17.383 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `classic` | `strict_current` | 15.078 | 1.137 | 13.261 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.873 | 0.808 | 8.505 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `ax` | `strict_current` | 6.873 | 1.255 | 5.475 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.508 | 0.808 | 17.953 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `classic` | `strict_current` | 14.508 | 1.255 | 11.557 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.185 | 2.252 | 2.747 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.185 | 9.388 | 0.659 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 37.499 | 2.252 | 16.652 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 37.499 | 9.388 | 3.994 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.725 | 2.135 | 2.682 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `ax` | `strict_current` | 5.725 | 9.095 | 0.629 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 36.247 | 2.135 | 16.980 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `classic` | `strict_current` | 36.247 | 9.095 | 3.985 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.715 | 2.123 | 2.692 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 5.715 | 9.352 | 0.611 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 40.946 | 2.123 | 19.290 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 40.946 | 9.352 | 4.378 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.381 | 2.186 | 2.919 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `ax` | `strict_current` | 6.381 | 9.273 | 0.688 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 42.112 | 2.186 | 19.263 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `classic` | `strict_current` | 42.112 | 9.273 | 4.541 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.301 | 0.748 | 9.767 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `ax` | `strict_current` | 7.301 | 0.914 | 7.987 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.110 | 0.748 | 33.592 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `classic` | `strict_current` | 25.110 | 0.914 | 27.470 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.491 | 0.734 | 8.847 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `ax` | `strict_current` | 6.491 | 0.853 | 7.607 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.788 | 0.734 | 32.423 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `classic` | `strict_current` | 23.788 | 0.853 | 27.877 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.778 | 0.777 | 8.721 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `ax` | `strict_current` | 6.778 | 0.931 | 7.277 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.514 | 0.777 | 34.111 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `classic` | `strict_current` | 26.514 | 0.931 | 28.464 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 16.082 | 1.107 | 14.531 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `ax` | `strict_current` | 16.082 | 1.296 | 12.405 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.617 | 1.107 | 23.146 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.617 | 1.296 | 19.759 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.696 | 1.032 | 6.488 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `ax` | `strict_current` | 6.696 | 1.175 | 5.698 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.414 | 1.032 | 25.594 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `classic` | `strict_current` | 26.414 | 1.175 | 22.476 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.786 | 1.074 | 5.389 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `ax` | `strict_current` | 5.786 | 1.402 | 4.128 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.953 | 1.074 | 22.309 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `classic` | `strict_current` | 23.953 | 1.402 | 17.087 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 16.727 | 1.140 | 14.677 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `ax` | `strict_current` | 16.727 | 1.231 | 13.593 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.779 | 1.140 | 22.620 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `classic` | `strict_current` | 25.779 | 1.231 | 20.949 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.686 | 0.809 | 8.266 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.686 | 1.100 | 6.080 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 26.976 | 0.809 | 33.354 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `classic` | `strict_current` | 26.976 | 1.100 | 24.533 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.817 | 1.062 | 8.303 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `ax` | `strict_current` | 8.817 | 1.236 | 7.132 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.893 | 1.062 | 24.382 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `classic` | `strict_current` | 25.893 | 1.236 | 20.944 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.409 | 0.834 | 7.686 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `ax` | `strict_current` | 6.409 | 0.993 | 6.451 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.782 | 0.834 | 28.521 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `classic` | `strict_current` | 23.782 | 0.993 | 23.939 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.723 | 0.803 | 8.368 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `ax` | `strict_current` | 6.723 | 0.983 | 6.838 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.285 | 0.803 | 30.228 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `classic` | `strict_current` | 24.285 | 0.983 | 24.699 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.092 | 0.936 | 6.505 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.092 | 1.157 | 5.267 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 13.885 | 0.936 | 14.828 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `classic` | `strict_current` | 13.885 | 1.157 | 12.006 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.560 | 0.932 | 7.037 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `ax` | `strict_current` | 6.560 | 1.050 | 6.249 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.200 | 0.932 | 15.232 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `classic` | `strict_current` | 14.200 | 1.050 | 13.527 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.806 | 0.974 | 6.991 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `ax` | `strict_current` | 6.806 | 1.161 | 5.863 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.268 | 0.974 | 14.656 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `classic` | `strict_current` | 14.268 | 1.161 | 12.293 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.894 | 0.899 | 7.671 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `ax` | `strict_current` | 6.894 | 1.148 | 6.005 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.675 | 0.899 | 15.216 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `classic` | `strict_current` | 13.675 | 1.148 | 11.911 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 17.428 | 0.977 | 17.834 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `ax` | `strict_current` | 17.428 | 1.579 | 11.037 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 27.218 | 0.977 | 27.853 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `classic` | `strict_current` | 27.218 | 1.579 | 17.237 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.775 | 0.989 | 6.850 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `ax` | `strict_current` | 6.775 | 1.433 | 4.729 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.253 | 0.989 | 24.523 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `classic` | `strict_current` | 24.253 | 1.433 | 16.929 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 16.663 | 0.941 | 17.703 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `ax` | `strict_current` | 16.663 | 1.717 | 9.702 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.750 | 0.941 | 28.419 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `classic` | `strict_current` | 26.750 | 1.717 | 15.575 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 16.984 | 0.909 | 18.687 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `ax` | `strict_current` | 16.984 | 1.494 | 11.364 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.768 | 0.909 | 30.554 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `classic` | `strict_current` | 27.768 | 1.494 | 18.580 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 13.902 | 0.776 | 17.918 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `ax` | `strict_current` | 13.902 | 0.833 | 16.693 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 13.655 | 0.776 | 17.600 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `classic` | `strict_current` | 13.655 | 0.833 | 16.396 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.874 | 0.962 | 7.147 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `ax` | `strict_current` | 6.874 | 0.987 | 6.961 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.901 | 0.962 | 15.493 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `classic` | `strict_current` | 14.901 | 0.987 | 15.090 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 17.687 | 0.945 | 18.711 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `ax` | `strict_current` | 17.687 | 0.786 | 22.492 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 16.003 | 0.945 | 16.930 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `classic` | `strict_current` | 16.003 | 0.786 | 20.350 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.525 | 0.804 | 9.364 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `ax` | `strict_current` | 7.525 | 0.820 | 9.173 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.755 | 0.804 | 17.115 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `classic` | `strict_current` | 13.755 | 0.820 | 16.766 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 5.962 | 1.267 | 4.707 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `ax` | `strict_current` | 5.962 | 2.155 | 2.766 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.445 | 1.267 | 19.296 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.445 | 2.155 | 11.342 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.998 | 1.388 | 5.043 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `ax` | `strict_current` | 6.998 | 2.114 | 3.310 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.354 | 1.388 | 17.551 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `classic` | `strict_current` | 24.354 | 2.114 | 11.520 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.875 | 1.208 | 5.691 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `ax` | `strict_current` | 6.875 | 2.021 | 3.403 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.926 | 1.208 | 20.631 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `classic` | `strict_current` | 24.926 | 2.021 | 12.335 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.646 | 1.256 | 5.292 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `ax` | `strict_current` | 6.646 | 2.148 | 3.094 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.428 | 1.256 | 19.451 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `classic` | `strict_current` | 24.428 | 2.148 | 11.371 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.514 | 1.033 | 6.309 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `ax` | `strict_current` | 6.514 | 0.982 | 6.636 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 28.533 | 1.033 | 27.633 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `classic` | `strict_current` | 28.533 | 0.982 | 29.067 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.203 | 0.887 | 6.995 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `ax` | `strict_current` | 6.203 | 1.049 | 5.915 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.335 | 0.887 | 28.567 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `classic` | `strict_current` | 25.335 | 1.049 | 24.158 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.652 | 1.006 | 7.609 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `ax` | `strict_current` | 7.652 | 1.009 | 7.581 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.681 | 1.006 | 14.600 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `classic` | `strict_current` | 14.681 | 1.009 | 14.546 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.608 | 0.954 | 6.930 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `ax` | `strict_current` | 6.608 | 1.089 | 6.067 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.501 | 0.954 | 15.208 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `classic` | `strict_current` | 14.501 | 1.089 | 13.314 |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.631 | 0.985 | 6.731 |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `ax` | `strict_current` | 6.631 | 0.989 | 6.707 |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.885 | 0.985 | 14.094 |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `classic` | `strict_current` | 13.885 | 0.989 | 14.043 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.179 | 1.114 | 5.548 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.179 | 1.137 | 5.435 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 14.293 | 1.114 | 12.834 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `classic` | `strict_current` | 14.293 | 1.137 | 12.573 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.886 | 1.025 | 6.718 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `ax` | `strict_current` | 6.886 | 0.927 | 7.429 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.601 | 1.025 | 14.244 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `classic` | `strict_current` | 14.601 | 0.927 | 15.752 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.925 | 1.046 | 6.618 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `ax` | `strict_current` | 6.925 | 1.019 | 6.797 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.271 | 1.046 | 13.638 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `classic` | `strict_current` | 14.271 | 1.019 | 14.006 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.745 | 0.892 | 7.561 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `ax` | `strict_current` | 6.745 | 0.980 | 6.882 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.680 | 0.892 | 15.334 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `classic` | `strict_current` | 13.680 | 0.980 | 13.957 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.723 | 0.948 | 7.091 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.723 | 1.286 | 5.230 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.929 | 0.948 | 26.293 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.929 | 1.286 | 19.391 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.738 | 1.065 | 6.330 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `ax` | `strict_current` | 6.738 | 1.457 | 4.625 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.932 | 1.065 | 23.420 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `classic` | `strict_current` | 24.932 | 1.457 | 17.112 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.309 | 0.802 | 7.866 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `ax` | `strict_current` | 6.309 | 1.430 | 4.414 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.673 | 0.802 | 32.007 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `classic` | `strict_current` | 25.673 | 1.430 | 17.960 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.215 | 0.824 | 7.544 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `ax` | `strict_current` | 6.215 | 1.362 | 4.564 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.290 | 0.824 | 30.700 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `classic` | `strict_current` | 25.290 | 1.362 | 18.571 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.396 | 1.845 | 3.466 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.396 | 2.361 | 2.709 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 23.286 | 1.845 | 12.620 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 23.286 | 2.361 | 9.861 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.754 | 1.156 | 5.842 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `ax` | `strict_current` | 6.754 | 2.839 | 2.379 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.913 | 1.156 | 20.684 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `classic` | `strict_current` | 23.913 | 2.839 | 8.424 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.560 | 1.207 | 5.437 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 6.560 | 2.898 | 2.264 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.466 | 1.207 | 19.447 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 23.466 | 2.898 | 8.097 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.933 | 1.175 | 5.049 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `ax` | `strict_current` | 5.933 | 2.926 | 2.028 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.197 | 1.175 | 20.595 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `classic` | `strict_current` | 24.197 | 2.926 | 8.270 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.969 | 0.868 | 9.177 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.969 | 1.696 | 4.698 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 27.086 | 0.868 | 31.195 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `classic` | `strict_current` | 27.086 | 1.696 | 15.970 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.435 | 0.823 | 7.817 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `ax` | `strict_current` | 6.435 | 1.687 | 3.816 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.112 | 0.823 | 30.505 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `classic` | `strict_current` | 25.112 | 1.687 | 14.890 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.896 | 0.899 | 7.671 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `ax` | `strict_current` | 6.896 | 1.695 | 4.068 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.906 | 0.899 | 27.706 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `classic` | `strict_current` | 24.906 | 1.695 | 14.693 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.514 | 0.896 | 7.272 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `ax` | `strict_current` | 6.514 | 1.645 | 3.961 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.496 | 0.896 | 27.347 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `classic` | `strict_current` | 24.496 | 1.645 | 14.894 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 15.927 | 0.786 | 20.267 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `ax` | `strict_current` | 15.927 | 1.056 | 15.089 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 28.615 | 0.786 | 36.412 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `classic` | `strict_current` | 28.615 | 1.056 | 27.108 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.746 | 0.853 | 7.910 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `ax` | `strict_current` | 6.746 | 0.829 | 8.142 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.710 | 0.853 | 32.491 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `classic` | `strict_current` | 27.710 | 0.829 | 33.444 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.823 | 0.956 | 8.183 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `ax` | `strict_current` | 7.823 | 0.928 | 8.433 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.233 | 0.956 | 26.393 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `classic` | `strict_current` | 25.233 | 0.928 | 27.202 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 17.719 | 0.813 | 21.792 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `ax` | `strict_current` | 17.719 | 0.839 | 21.115 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.711 | 0.813 | 34.079 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `classic` | `strict_current` | 27.711 | 0.839 | 33.021 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.801 | 0.796 | 8.539 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.801 | 1.000 | 6.798 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.384 | 0.796 | 31.871 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.384 | 1.000 | 25.375 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.717 | 0.813 | 8.267 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `ax` | `strict_current` | 6.717 | 1.051 | 6.389 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.040 | 0.813 | 30.818 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `classic` | `strict_current` | 25.040 | 1.051 | 23.819 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.144 | 0.822 | 8.693 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 7.144 | 0.763 | 9.365 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.842 | 0.822 | 31.447 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 25.842 | 0.763 | 33.877 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.259 | 0.881 | 7.103 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `ax` | `strict_current` | 6.259 | 0.865 | 7.235 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.636 | 0.881 | 29.096 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `classic` | `strict_current` | 25.636 | 0.865 | 29.636 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 15.349 | 0.984 | 15.606 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `ax` | `strict_current` | 15.349 | 1.178 | 13.028 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 15.011 | 0.984 | 15.262 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `classic` | `strict_current` | 15.011 | 1.178 | 12.741 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 14.843 | 0.909 | 16.323 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `ax` | `strict_current` | 14.843 | 1.252 | 11.860 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.846 | 0.909 | 15.227 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `classic` | `strict_current` | 13.846 | 1.252 | 11.063 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.628 | 1.136 | 5.833 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `ax` | `strict_current` | 6.628 | 1.300 | 5.100 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.725 | 1.136 | 13.839 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `classic` | `strict_current` | 15.725 | 1.300 | 12.098 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.542 | 0.824 | 7.936 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `ax` | `strict_current` | 6.542 | 1.222 | 5.354 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.585 | 0.824 | 16.479 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `classic` | `strict_current` | 13.585 | 1.222 | 11.117 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.564 | 0.850 | 7.720 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.564 | 1.051 | 6.246 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 27.288 | 0.850 | 32.094 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `classic` | `strict_current` | 27.288 | 1.051 | 25.965 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.480 | 0.887 | 7.307 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `ax` | `strict_current` | 6.480 | 0.931 | 6.962 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.232 | 0.887 | 27.322 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `classic` | `strict_current` | 24.232 | 0.931 | 26.035 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.085 | 0.944 | 6.446 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `ax` | `strict_current` | 6.085 | 1.010 | 6.022 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.584 | 0.944 | 26.044 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `classic` | `strict_current` | 24.584 | 1.010 | 24.331 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.620 | 0.937 | 7.065 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `ax` | `strict_current` | 6.620 | 0.970 | 6.823 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.838 | 0.937 | 26.509 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `classic` | `strict_current` | 24.838 | 0.970 | 25.603 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.910 | 1.088 | 6.352 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.910 | 1.084 | 6.373 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.517 | 1.088 | 22.536 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.517 | 1.084 | 22.611 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.132 | 0.938 | 6.535 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `ax` | `strict_current` | 6.132 | 1.076 | 5.700 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.088 | 0.938 | 25.670 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `classic` | `strict_current` | 24.088 | 1.076 | 22.390 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.548 | 1.191 | 6.335 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `ax` | `strict_current` | 7.548 | 1.262 | 5.983 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 28.118 | 1.191 | 23.599 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `classic` | `strict_current` | 28.118 | 1.262 | 22.287 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.002 | 1.205 | 5.810 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `ax` | `strict_current` | 7.002 | 1.110 | 6.307 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.688 | 1.205 | 20.486 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `classic` | `strict_current` | 24.688 | 1.110 | 22.238 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 16.392 | 1.094 | 14.989 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `ax` | `strict_current` | 16.392 | 1.238 | 13.240 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 15.555 | 1.094 | 14.224 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `classic` | `strict_current` | 15.555 | 1.238 | 12.564 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.952 | 1.091 | 6.375 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `ax` | `strict_current` | 6.952 | 1.145 | 6.074 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.122 | 1.091 | 13.867 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `classic` | `strict_current` | 15.122 | 1.145 | 13.213 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.831 | 1.197 | 6.543 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `ax` | `strict_current` | 7.831 | 0.898 | 8.720 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 16.372 | 1.197 | 13.679 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `classic` | `strict_current` | 16.372 | 0.898 | 18.232 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 14.949 | 1.112 | 13.442 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `ax` | `strict_current` | 14.949 | 0.911 | 16.416 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.699 | 1.112 | 12.318 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `classic` | `strict_current` | 13.699 | 0.911 | 15.043 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.450 | 0.924 | 6.978 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.450 | 1.277 | 5.050 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.206 | 0.924 | 26.188 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.206 | 1.277 | 18.950 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.460 | 0.913 | 7.079 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `ax` | `strict_current` | 6.460 | 1.463 | 4.415 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.681 | 0.913 | 27.045 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `classic` | `strict_current` | 24.681 | 1.463 | 16.868 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.464 | 0.857 | 7.542 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `ax` | `strict_current` | 6.464 | 1.337 | 4.834 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.257 | 0.857 | 29.471 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `classic` | `strict_current` | 25.257 | 1.337 | 18.891 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.282 | 0.848 | 7.410 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `ax` | `strict_current` | 6.282 | 1.321 | 4.756 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.523 | 0.848 | 30.106 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `classic` | `strict_current` | 25.523 | 1.321 | 19.321 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.235 | 1.868 | 3.337 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.235 | 4.280 | 1.457 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 23.879 | 1.868 | 12.781 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 23.879 | 4.280 | 5.580 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.647 | 1.911 | 3.477 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `ax` | `strict_current` | 6.647 | 4.354 | 1.526 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.791 | 1.911 | 12.447 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `classic` | `strict_current` | 23.791 | 4.354 | 5.464 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.561 | 2.058 | 3.188 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `ax` | `strict_current` | 6.561 | 4.391 | 1.494 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.050 | 2.058 | 11.688 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `classic` | `strict_current` | 24.050 | 4.391 | 5.477 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.273 | 1.734 | 3.616 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `ax` | `strict_current` | 6.273 | 4.213 | 1.489 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.820 | 1.734 | 13.734 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `classic` | `strict_current` | 23.820 | 4.213 | 5.653 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 17.369 | 0.877 | 19.797 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `ax` | `strict_current` | 17.369 | 1.085 | 16.007 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 26.436 | 0.877 | 30.131 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `classic` | `strict_current` | 26.436 | 1.085 | 24.362 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 17.296 | 0.962 | 17.975 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `ax` | `strict_current` | 17.296 | 0.935 | 18.499 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.081 | 0.962 | 27.105 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `classic` | `strict_current` | 26.081 | 0.935 | 27.895 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.424 | 0.799 | 8.044 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `ax` | `strict_current` | 6.424 | 1.056 | 6.084 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.081 | 0.799 | 31.406 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `classic` | `strict_current` | 25.081 | 1.056 | 23.754 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.540 | 0.798 | 8.196 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `ax` | `strict_current` | 6.540 | 1.141 | 5.734 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.519 | 0.798 | 31.982 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `classic` | `strict_current` | 25.519 | 1.141 | 22.372 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.576 | 1.686 | 3.900 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.576 | 3.220 | 2.042 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.055 | 1.686 | 14.265 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.055 | 3.220 | 7.469 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.694 | 1.765 | 3.794 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `ax` | `strict_current` | 6.694 | 3.244 | 2.064 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.849 | 1.765 | 13.515 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `classic` | `strict_current` | 23.849 | 3.244 | 7.352 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.566 | 1.782 | 3.685 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `ax` | `strict_current` | 6.566 | 3.056 | 2.148 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.874 | 1.782 | 13.400 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `classic` | `strict_current` | 23.874 | 3.056 | 7.812 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.563 | 1.842 | 3.562 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `ax` | `strict_current` | 6.563 | 3.149 | 2.084 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 22.657 | 1.842 | 12.298 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `classic` | `strict_current` | 22.657 | 3.149 | 7.196 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.113 | 1.305 | 5.450 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `ax` | `strict_current` | 7.113 | 8.562 | 0.831 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.190 | 1.305 | 25.430 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `classic` | `strict_current` | 33.190 | 8.562 | 3.876 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.026 | 1.464 | 4.800 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `ax` | `strict_current` | 7.026 | 8.737 | 0.804 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.183 | 1.464 | 22.670 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `classic` | `strict_current` | 33.183 | 8.737 | 3.798 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.117 | 0.868 | 7.047 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `ax` | `strict_current` | 6.117 | 1.643 | 3.724 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.261 | 0.868 | 27.948 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `classic` | `strict_current` | 24.261 | 1.643 | 14.768 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.954 | 0.976 | 6.102 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `ax` | `strict_current` | 5.954 | 1.750 | 3.402 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.255 | 0.976 | 25.882 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `classic` | `strict_current` | 25.255 | 1.750 | 14.429 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.170 | 3.453 | 1.787 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `ax` | `strict_current` | 6.170 | 3.826 | 1.612 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.548 | 3.453 | 6.820 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `classic` | `strict_current` | 23.548 | 3.826 | 6.154 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.438 | 3.266 | 1.972 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `ax` | `strict_current` | 6.438 | 3.713 | 1.734 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.299 | 3.266 | 7.441 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `classic` | `strict_current` | 24.299 | 3.713 | 6.544 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.678 | 0.901 | 7.415 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `ax` | `strict_current` | 6.678 | 1.265 | 5.281 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.510 | 0.901 | 27.217 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `classic` | `strict_current` | 24.510 | 1.265 | 19.382 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.600 | 0.936 | 7.050 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `ax` | `strict_current` | 6.600 | 1.598 | 4.130 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.011 | 0.936 | 27.782 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `classic` | `strict_current` | 26.011 | 1.598 | 16.275 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.943 | 0.887 | 6.699 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `ax` | `strict_current` | 5.943 | 1.121 | 5.302 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.671 | 0.887 | 28.939 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `classic` | `strict_current` | 25.671 | 1.121 | 22.903 |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.562 | 0.962 | 6.820 |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `ax` | `strict_current` | 6.562 | 1.224 | 5.359 |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.513 | 0.962 | 27.558 |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `classic` | `strict_current` | 26.513 | 1.224 | 21.653 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.542 | 1.002 | 6.532 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `ax` | `strict_current` | 6.542 | 1.789 | 3.658 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.391 | 1.002 | 27.348 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `classic` | `strict_current` | 27.391 | 1.789 | 15.314 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.631 | 0.835 | 7.940 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `ax` | `strict_current` | 6.631 | 1.753 | 3.782 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.624 | 0.835 | 29.482 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `classic` | `strict_current` | 24.624 | 1.753 | 14.043 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.674 | 1.442 | 6.015 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `ax` | `strict_current` | 8.674 | 1.747 | 4.966 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 28.030 | 1.442 | 19.439 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `classic` | `strict_current` | 28.030 | 1.747 | 16.047 |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.781 | 1.355 | 5.006 |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `ax` | `strict_current` | 6.781 | 1.601 | 4.236 |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.295 | 1.355 | 17.936 |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `classic` | `strict_current` | 24.295 | 1.601 | 15.176 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.159 | 12.138 | 0.590 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `ax` | `strict_current` | 7.159 | 11.953 | 0.599 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 38.549 | 12.138 | 3.176 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `classic` | `strict_current` | 38.549 | 11.953 | 3.225 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.858 | 11.944 | 0.574 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `ax` | `strict_current` | 6.858 | 12.207 | 0.562 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 39.227 | 11.944 | 3.284 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `classic` | `strict_current` | 39.227 | 12.207 | 3.213 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.517 | 1.677 | 3.886 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `ax` | `strict_current` | 6.517 | 2.671 | 2.440 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.093 | 1.677 | 14.366 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `classic` | `strict_current` | 24.093 | 2.671 | 9.020 |
| `vbr1_l2_event_controller` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.752 | 1.632 | 4.138 |
| `vbr1_l2_event_controller` | `tb` | `gold` | `ax` | `strict_current` | 6.752 | 2.655 | 2.543 |
| `vbr1_l2_event_controller` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.634 | 1.632 | 15.098 |
| `vbr1_l2_event_controller` | `tb` | `gold` | `classic` | `strict_current` | 24.634 | 2.655 | 9.278 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.178 | 0.989 | 6.246 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `ax` | `strict_current` | 6.178 | 1.597 | 3.868 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.061 | 0.989 | 24.324 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `classic` | `strict_current` | 24.061 | 1.597 | 15.064 |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.557 | 1.075 | 6.102 |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `ax` | `strict_current` | 6.557 | 1.708 | 3.839 |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.404 | 1.075 | 22.710 |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `classic` | `strict_current` | 24.404 | 1.708 | 14.287 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.176 | 9.162 | 1.001 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `ax` | `strict_current` | 9.176 | 127.566 | 0.072 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 45.848 | 9.162 | 5.004 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `classic` | `strict_current` | 45.848 | 127.566 | 0.359 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.238 | 33.015 | 0.310 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `ax` | `strict_current` | 10.238 | 153.387 | 0.067 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 49.841 | 33.015 | 1.510 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `classic` | `strict_current` | 49.841 | 153.387 | 0.325 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.928 | 1.681 | 4.121 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `ax` | `strict_current` | 6.928 | 2.482 | 2.791 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.591 | 1.681 | 14.628 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `classic` | `strict_current` | 24.591 | 2.482 | 9.908 |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.633 | 1.727 | 3.842 |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `ax` | `strict_current` | 6.633 | 2.558 | 2.593 |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.360 | 1.727 | 13.530 |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `classic` | `strict_current` | 23.360 | 2.558 | 9.131 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.764 | 9.757 | 0.693 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `ax` | `strict_current` | 6.764 | 10.336 | 0.654 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 22.022 | 9.757 | 2.257 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `classic` | `strict_current` | 22.022 | 10.336 | 2.131 |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.543 | 10.033 | 0.652 |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `ax` | `strict_current` | 6.543 | 10.221 | 0.640 |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 22.745 | 10.033 | 2.267 |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `classic` | `strict_current` | 22.745 | 10.221 | 2.225 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.402 | 1.179 | 5.429 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `ax` | `strict_current` | 6.402 | 2.220 | 2.884 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.070 | 1.179 | 21.262 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `classic` | `strict_current` | 25.070 | 2.220 | 11.293 |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.442 | 1.227 | 5.249 |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `ax` | `strict_current` | 6.442 | 2.246 | 2.868 |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.542 | 1.227 | 19.999 |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `classic` | `strict_current` | 24.542 | 2.246 | 10.928 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.428 | 1.312 | 4.900 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `ax` | `strict_current` | 6.428 | 16.918 | 0.380 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 45.832 | 1.312 | 34.936 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `classic` | `strict_current` | 45.832 | 16.918 | 2.709 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.121 | 2.580 | 2.372 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `ax` | `strict_current` | 6.121 | 17.108 | 0.358 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 41.845 | 2.580 | 16.219 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `classic` | `strict_current` | 41.845 | 17.108 | 2.446 |

## Accuracy-Gated Speedups

| Entry | Form | Variant | Spectre mode | EVAS mode | Spectre wall s | EVAS wall s | Spectre/EVAS |
| --- | --- | --- | --- | --- | ---: | ---: | ---: |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.974 | 1.096 | 6.363 |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.974 | 1.405 | 4.965 |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.726 | 1.096 | 23.469 |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.726 | 1.405 | 18.314 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.075 | 1.099 | 6.437 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `ax` | `strict_current` | 7.075 | 1.446 | 4.892 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.160 | 1.099 | 21.981 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `classic` | `strict_current` | 24.160 | 1.446 | 16.706 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.726 | 1.156 | 4.951 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `ax` | `strict_current` | 5.726 | 1.339 | 4.275 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.547 | 1.156 | 21.225 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `classic` | `strict_current` | 24.547 | 1.339 | 18.327 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.802 | 1.179 | 6.619 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `ax` | `strict_current` | 7.802 | 1.535 | 5.085 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.919 | 1.179 | 21.141 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `classic` | `strict_current` | 24.919 | 1.535 | 16.239 |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.255 | 1.456 | 4.298 |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.255 | 10.932 | 0.572 |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 23.086 | 1.456 | 15.861 |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 23.086 | 10.932 | 2.112 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.468 | 1.489 | 4.343 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `ax` | `strict_current` | 6.468 | 10.720 | 0.603 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 22.851 | 1.489 | 15.344 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `classic` | `strict_current` | 22.851 | 10.720 | 2.132 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.434 | 1.829 | 3.517 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `ax` | `strict_current` | 6.434 | 1.983 | 3.245 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.937 | 1.829 | 13.085 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `classic` | `strict_current` | 23.937 | 1.983 | 12.073 |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.369 | 1.631 | 3.905 |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `ax` | `strict_current` | 6.369 | 1.902 | 3.349 |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.013 | 1.631 | 15.337 |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `classic` | `strict_current` | 25.013 | 1.902 | 13.153 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 17.108 | 0.928 | 18.435 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `ax` | `strict_current` | 17.108 | 1.344 | 12.725 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 27.066 | 0.928 | 29.165 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `classic` | `strict_current` | 27.066 | 1.344 | 20.131 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 15.943 | 0.854 | 18.674 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `ax` | `strict_current` | 15.943 | 0.954 | 16.705 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.620 | 0.854 | 32.352 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `classic` | `strict_current` | 27.620 | 0.954 | 28.939 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 18.676 | 0.761 | 24.545 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `ax` | `strict_current` | 18.676 | 1.030 | 18.127 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 29.079 | 0.761 | 38.216 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `classic` | `strict_current` | 29.079 | 1.030 | 28.223 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.350 | 0.849 | 7.476 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `ax` | `strict_current` | 6.350 | 0.798 | 7.960 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.598 | 0.849 | 30.135 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `classic` | `strict_current` | 25.598 | 0.798 | 32.089 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.268 | 0.965 | 6.498 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `ax` | `strict_current` | 6.268 | 1.344 | 4.665 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.034 | 0.965 | 25.953 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `classic` | `strict_current` | 25.034 | 1.344 | 18.630 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.392 | 1.028 | 6.217 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `ax` | `strict_current` | 6.392 | 1.483 | 4.310 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.713 | 1.028 | 25.011 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `classic` | `strict_current` | 25.713 | 1.483 | 17.339 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.372 | 1.014 | 6.281 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `ax` | `strict_current` | 6.372 | 1.377 | 4.628 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.818 | 1.014 | 27.423 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `classic` | `strict_current` | 27.818 | 1.377 | 20.204 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.515 | 0.831 | 7.841 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.515 | 1.622 | 4.018 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.037 | 0.831 | 30.132 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.037 | 1.622 | 15.438 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.325 | 0.857 | 7.380 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `ax` | `strict_current` | 6.325 | 1.631 | 3.878 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.210 | 0.857 | 29.414 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `classic` | `strict_current` | 25.210 | 1.631 | 15.455 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.396 | 0.927 | 6.903 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `ax` | `strict_current` | 6.396 | 1.576 | 4.058 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.711 | 0.927 | 27.749 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `classic` | `strict_current` | 25.711 | 1.576 | 16.312 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.575 | 0.858 | 7.660 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `ax` | `strict_current` | 6.575 | 1.603 | 4.103 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.338 | 0.858 | 28.352 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `classic` | `strict_current` | 24.338 | 1.603 | 15.186 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.472 | 1.719 | 3.764 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.472 | 3.599 | 1.798 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.290 | 1.719 | 14.128 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.290 | 3.599 | 6.748 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.244 | 1.664 | 3.753 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `ax` | `strict_current` | 6.244 | 3.472 | 1.798 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.555 | 1.664 | 14.156 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `classic` | `strict_current` | 23.555 | 3.472 | 6.784 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.118 | 1.727 | 3.542 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `ax` | `strict_current` | 6.118 | 3.416 | 1.791 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.923 | 1.727 | 13.851 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `classic` | `strict_current` | 23.923 | 3.416 | 7.003 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.494 | 1.798 | 3.611 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `ax` | `strict_current` | 6.494 | 3.446 | 1.885 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.138 | 1.798 | 13.421 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `classic` | `strict_current` | 24.138 | 3.446 | 7.005 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.135 | 0.948 | 6.468 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.135 | 1.645 | 3.731 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.806 | 0.948 | 26.153 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.806 | 1.645 | 15.083 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.990 | 0.816 | 7.343 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `ax` | `strict_current` | 5.990 | 1.567 | 3.822 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.053 | 0.816 | 29.486 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `classic` | `strict_current` | 24.053 | 1.567 | 15.348 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.879 | 0.866 | 7.944 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `ax` | `strict_current` | 6.879 | 1.609 | 4.277 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.498 | 0.866 | 30.600 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `classic` | `strict_current` | 26.498 | 1.609 | 16.474 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.298 | 0.908 | 6.938 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `ax` | `strict_current` | 6.298 | 1.651 | 3.815 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.857 | 0.908 | 26.283 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `classic` | `strict_current` | 23.857 | 1.651 | 14.452 |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.588 | 1.384 | 4.760 |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.588 | 4.028 | 1.636 |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 23.354 | 1.384 | 16.873 |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `classic` | `strict_current` | 23.354 | 4.028 | 5.798 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.602 | 1.413 | 4.673 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `ax` | `strict_current` | 6.602 | 4.048 | 1.631 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.029 | 1.413 | 17.005 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `classic` | `strict_current` | 24.029 | 4.048 | 5.936 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.888 | 1.485 | 3.964 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `ax` | `strict_current` | 5.888 | 4.065 | 1.449 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.660 | 1.485 | 16.602 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `classic` | `strict_current` | 24.660 | 4.065 | 6.067 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.014 | 1.447 | 4.156 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `ax` | `strict_current` | 6.014 | 4.125 | 1.458 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.897 | 1.447 | 17.203 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `classic` | `strict_current` | 24.897 | 4.125 | 6.036 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.145 | 0.985 | 6.238 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.145 | 1.712 | 3.589 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.501 | 0.985 | 24.875 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.501 | 1.712 | 14.312 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.981 | 0.982 | 7.108 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `ax` | `strict_current` | 6.981 | 1.648 | 4.236 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.312 | 0.982 | 24.755 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `classic` | `strict_current` | 24.312 | 1.648 | 14.752 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.999 | 1.072 | 6.531 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `ax` | `strict_current` | 6.999 | 1.677 | 4.172 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.478 | 1.072 | 23.776 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `classic` | `strict_current` | 25.478 | 1.677 | 15.189 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.697 | 0.947 | 7.075 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `ax` | `strict_current` | 6.697 | 1.700 | 3.939 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.526 | 0.947 | 26.966 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `classic` | `strict_current` | 25.526 | 1.700 | 15.015 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.878 | 1.188 | 5.788 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.878 | 3.203 | 2.147 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 23.115 | 1.188 | 19.453 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 23.115 | 3.203 | 7.217 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.379 | 1.288 | 4.952 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `ax` | `strict_current` | 6.379 | 3.274 | 1.948 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.564 | 1.288 | 18.294 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `classic` | `strict_current` | 23.564 | 3.274 | 7.198 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.524 | 1.221 | 5.342 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 6.524 | 3.171 | 2.057 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.953 | 1.221 | 19.612 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 23.953 | 3.171 | 7.554 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.512 | 1.379 | 4.723 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `ax` | `strict_current` | 6.512 | 3.277 | 1.987 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.855 | 1.379 | 17.300 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `classic` | `strict_current` | 23.855 | 3.277 | 7.279 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.625 | 0.935 | 7.088 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.625 | 1.557 | 4.256 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 14.121 | 0.935 | 15.107 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `classic` | `strict_current` | 14.121 | 1.557 | 9.071 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.708 | 0.936 | 7.163 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `ax` | `strict_current` | 6.708 | 1.759 | 3.813 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.976 | 0.936 | 14.924 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `classic` | `strict_current` | 13.976 | 1.759 | 7.943 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.792 | 0.940 | 6.164 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `ax` | `strict_current` | 5.792 | 1.552 | 3.732 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.378 | 0.940 | 14.236 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `classic` | `strict_current` | 13.378 | 1.552 | 8.619 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.720 | 1.181 | 5.689 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `ax` | `strict_current` | 6.720 | 1.560 | 4.307 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.505 | 1.181 | 11.433 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `classic` | `strict_current` | 13.505 | 1.560 | 8.655 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.795 | 0.836 | 9.320 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `ax` | `strict_current` | 7.795 | 1.045 | 7.460 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.674 | 0.836 | 18.741 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `classic` | `strict_current` | 15.674 | 1.045 | 15.001 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.044 | 0.754 | 9.341 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `ax` | `strict_current` | 7.044 | 1.052 | 6.699 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.559 | 0.754 | 20.631 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `classic` | `strict_current` | 15.559 | 1.052 | 14.796 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.827 | 0.952 | 7.174 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `ax` | `strict_current` | 6.827 | 0.867 | 7.877 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.827 | 0.952 | 16.630 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `classic` | `strict_current` | 15.827 | 0.867 | 18.260 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.698 | 0.808 | 8.292 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.698 | 0.816 | 8.205 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.296 | 0.808 | 31.313 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.296 | 0.816 | 30.987 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.711 | 0.767 | 8.748 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `ax` | `strict_current` | 6.711 | 1.022 | 6.564 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.792 | 0.767 | 33.622 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `classic` | `strict_current` | 25.792 | 1.022 | 25.228 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.974 | 0.895 | 8.905 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `ax` | `strict_current` | 7.974 | 0.945 | 8.440 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.099 | 0.895 | 29.146 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `classic` | `strict_current` | 26.099 | 0.945 | 27.622 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.007 | 0.756 | 9.269 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `ax` | `strict_current` | 7.007 | 0.806 | 8.696 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.914 | 0.756 | 32.958 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `classic` | `strict_current` | 24.914 | 0.806 | 30.917 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 19.854 | 0.849 | 23.375 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `ax` | `strict_current` | 19.854 | 1.067 | 18.614 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 28.553 | 0.849 | 33.617 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `classic` | `strict_current` | 28.553 | 1.067 | 26.769 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.870 | 0.886 | 7.756 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `ax` | `strict_current` | 6.870 | 1.019 | 6.740 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 30.621 | 0.886 | 34.573 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `classic` | `strict_current` | 30.621 | 1.019 | 30.041 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.474 | 0.791 | 8.188 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `ax` | `strict_current` | 6.474 | 0.962 | 6.730 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.073 | 0.791 | 31.712 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `classic` | `strict_current` | 25.073 | 0.962 | 26.064 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 15.847 | 0.840 | 18.865 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `ax` | `strict_current` | 15.847 | 1.033 | 15.338 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.120 | 0.840 | 31.093 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `classic` | `strict_current` | 26.120 | 1.033 | 25.281 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.172 | 0.942 | 6.555 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.172 | 4.572 | 1.350 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.046 | 0.942 | 25.539 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.046 | 4.572 | 5.259 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.474 | 1.007 | 6.426 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `ax` | `strict_current` | 6.474 | 4.664 | 1.388 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.441 | 1.007 | 23.268 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `classic` | `strict_current` | 23.441 | 4.664 | 5.026 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.482 | 1.018 | 6.367 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `ax` | `strict_current` | 6.482 | 4.643 | 1.396 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.181 | 1.018 | 24.735 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `classic` | `strict_current` | 25.181 | 4.643 | 5.423 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.523 | 1.022 | 6.383 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `ax` | `strict_current` | 6.523 | 4.592 | 1.421 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.523 | 1.022 | 24.000 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `classic` | `strict_current` | 24.523 | 4.592 | 5.341 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.322 | 1.668 | 3.791 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.322 | 1.737 | 3.641 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.704 | 1.668 | 14.813 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.704 | 1.737 | 14.226 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.183 | 1.640 | 4.379 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `ax` | `strict_current` | 7.183 | 1.651 | 4.351 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.659 | 1.640 | 15.642 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `classic` | `strict_current` | 25.659 | 1.651 | 15.543 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.655 | 1.554 | 4.283 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `ax` | `strict_current` | 6.655 | 1.560 | 4.266 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.729 | 1.554 | 15.915 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `classic` | `strict_current` | 24.729 | 1.560 | 15.850 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.164 | 1.785 | 4.015 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `ax` | `strict_current` | 7.164 | 1.617 | 4.432 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.839 | 1.785 | 13.919 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `classic` | `strict_current` | 24.839 | 1.617 | 15.366 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.980 | 0.802 | 7.459 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `ax` | `strict_current` | 5.980 | 0.897 | 6.664 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 11.632 | 0.802 | 14.509 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `classic` | `strict_current` | 11.632 | 0.897 | 12.962 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.946 | 0.993 | 6.995 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `ax` | `strict_current` | 6.946 | 0.804 | 8.640 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.195 | 0.993 | 14.295 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `classic` | `strict_current` | 14.195 | 0.804 | 17.656 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.622 | 0.874 | 7.577 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `ax` | `strict_current` | 6.622 | 0.837 | 7.907 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.234 | 0.874 | 15.143 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `classic` | `strict_current` | 13.234 | 0.837 | 15.803 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.031 | 0.868 | 8.101 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.031 | 2.589 | 2.715 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 46.073 | 0.868 | 53.090 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `classic` | `strict_current` | 46.073 | 2.589 | 17.794 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.936 | 0.973 | 7.132 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `ax` | `strict_current` | 6.936 | 2.565 | 2.704 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 44.633 | 0.973 | 45.894 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `classic` | `strict_current` | 44.633 | 2.565 | 17.401 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.366 | 0.852 | 8.643 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `ax` | `strict_current` | 7.366 | 2.638 | 2.792 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 45.124 | 0.852 | 52.946 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `classic` | `strict_current` | 45.124 | 2.638 | 17.103 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.123 | 0.888 | 9.144 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `ax` | `strict_current` | 8.123 | 2.542 | 3.196 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 45.649 | 0.888 | 51.388 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `classic` | `strict_current` | 45.649 | 2.542 | 17.960 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 17.071 | 0.888 | 19.218 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 17.071 | 0.949 | 17.986 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 29.637 | 0.888 | 33.365 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 29.637 | 0.949 | 31.226 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 19.918 | 1.255 | 15.876 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `ax` | `strict_current` | 19.918 | 0.853 | 23.344 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 30.136 | 1.255 | 24.020 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `classic` | `strict_current` | 30.136 | 0.853 | 35.320 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.875 | 0.922 | 7.457 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `ax` | `strict_current` | 6.875 | 0.993 | 6.925 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.195 | 0.922 | 27.330 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `classic` | `strict_current` | 25.195 | 0.993 | 25.379 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 18.775 | 0.846 | 22.179 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `ax` | `strict_current` | 18.775 | 1.007 | 18.642 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 29.323 | 0.846 | 34.640 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `classic` | `strict_current` | 29.323 | 1.007 | 29.115 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.374 | 1.347 | 4.732 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `ax` | `strict_current` | 6.374 | 4.633 | 1.376 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.368 | 1.347 | 17.347 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `classic` | `strict_current` | 23.368 | 4.633 | 5.044 |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.823 | 1.475 | 3.947 |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `ax` | `strict_current` | 5.823 | 4.595 | 1.267 |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 22.860 | 1.475 | 15.495 |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `classic` | `strict_current` | 22.860 | 4.595 | 4.975 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.830 | 1.008 | 6.774 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.830 | 1.061 | 6.436 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.882 | 1.008 | 25.671 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.882 | 1.061 | 24.391 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.444 | 0.989 | 7.527 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `ax` | `strict_current` | 7.444 | 1.194 | 6.234 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.453 | 0.989 | 26.748 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `classic` | `strict_current` | 26.453 | 1.194 | 22.154 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.345 | 0.802 | 7.914 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `ax` | `strict_current` | 6.345 | 0.998 | 6.360 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.215 | 0.802 | 31.451 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `classic` | `strict_current` | 25.215 | 0.998 | 25.275 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.432 | 0.779 | 8.261 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `ax` | `strict_current` | 6.432 | 1.176 | 5.472 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.251 | 0.779 | 33.713 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `classic` | `strict_current` | 26.251 | 1.176 | 22.331 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.448 | 0.848 | 7.606 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.448 | 0.969 | 6.651 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.215 | 0.848 | 28.563 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.215 | 0.969 | 24.979 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.946 | 0.882 | 7.879 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `ax` | `strict_current` | 6.946 | 1.075 | 6.462 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.692 | 0.882 | 28.009 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `classic` | `strict_current` | 24.692 | 1.075 | 22.972 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.650 | 0.925 | 7.188 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `ax` | `strict_current` | 6.650 | 1.110 | 5.992 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.287 | 0.925 | 27.332 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `classic` | `strict_current` | 25.287 | 1.110 | 22.784 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.124 | 0.828 | 7.401 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `ax` | `strict_current` | 6.124 | 0.921 | 6.649 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.121 | 0.828 | 29.148 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `classic` | `strict_current` | 24.121 | 0.921 | 26.188 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 14.776 | 1.147 | 12.878 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `ax` | `strict_current` | 14.776 | 1.187 | 12.447 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 13.727 | 1.147 | 11.964 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `classic` | `strict_current` | 13.727 | 1.187 | 11.563 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.511 | 1.094 | 5.952 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `ax` | `strict_current` | 6.511 | 1.153 | 5.648 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.068 | 1.094 | 11.944 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `classic` | `strict_current` | 13.068 | 1.153 | 11.334 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 15.635 | 1.206 | 12.964 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `ax` | `strict_current` | 15.635 | 1.106 | 14.143 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.456 | 1.206 | 11.986 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `classic` | `strict_current` | 14.456 | 1.106 | 13.076 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.536 | 1.019 | 6.414 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `ax` | `strict_current` | 6.536 | 1.271 | 5.142 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.849 | 1.019 | 14.572 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `classic` | `strict_current` | 14.849 | 1.271 | 11.682 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.482 | 9.873 | 1.062 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `ax` | `strict_current` | 10.482 | 127.882 | 0.082 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 48.524 | 9.873 | 4.915 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `classic` | `strict_current` | 48.524 | 127.882 | 0.379 |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.054 | 38.791 | 0.259 |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `ax` | `strict_current` | 10.054 | 149.272 | 0.067 |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 48.478 | 38.791 | 1.250 |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `classic` | `strict_current` | 48.478 | 149.272 | 0.325 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 15.109 | 1.150 | 13.143 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `ax` | `strict_current` | 15.109 | 1.819 | 8.306 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 14.483 | 1.150 | 12.599 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `classic` | `strict_current` | 14.483 | 1.819 | 7.962 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 15.929 | 1.134 | 14.047 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `ax` | `strict_current` | 15.929 | 1.766 | 9.019 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.749 | 1.134 | 12.125 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `classic` | `strict_current` | 13.749 | 1.766 | 7.785 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.519 | 1.080 | 6.038 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `ax` | `strict_current` | 6.519 | 1.696 | 3.845 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.767 | 1.080 | 12.752 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `classic` | `strict_current` | 13.767 | 1.696 | 8.120 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.644 | 1.244 | 5.342 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `ax` | `strict_current` | 6.644 | 1.766 | 3.763 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.591 | 1.244 | 10.928 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `classic` | `strict_current` | 13.591 | 1.766 | 7.697 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.651 | 0.883 | 7.529 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.651 | 1.344 | 4.948 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.382 | 0.883 | 27.604 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.382 | 1.344 | 18.141 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.396 | 0.859 | 7.445 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `ax` | `strict_current` | 6.396 | 1.255 | 5.094 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.341 | 0.859 | 28.334 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `classic` | `strict_current` | 24.341 | 1.255 | 19.388 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.606 | 0.849 | 7.781 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `ax` | `strict_current` | 6.606 | 1.379 | 4.788 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.486 | 0.849 | 28.843 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `classic` | `strict_current` | 24.486 | 1.379 | 17.750 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.683 | 0.883 | 7.572 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `ax` | `strict_current` | 6.683 | 1.414 | 4.727 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.639 | 0.883 | 29.046 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `classic` | `strict_current` | 25.639 | 1.414 | 18.134 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.512 | 1.229 | 6.114 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.512 | 1.312 | 5.724 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.127 | 1.229 | 20.450 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.127 | 1.312 | 19.148 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.685 | 1.047 | 6.386 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `ax` | `strict_current` | 6.685 | 1.046 | 6.392 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.680 | 1.047 | 25.486 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `classic` | `strict_current` | 26.680 | 1.046 | 25.510 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.214 | 0.980 | 7.359 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 7.214 | 1.037 | 6.959 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.503 | 0.980 | 27.036 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 26.503 | 1.037 | 25.564 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.007 | 1.030 | 6.804 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `ax` | `strict_current` | 7.007 | 0.922 | 7.600 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.000 | 1.030 | 25.247 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `classic` | `strict_current` | 26.000 | 0.922 | 28.203 |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 5.969 | 1.825 | 3.271 |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `ax` | `strict_current` | 5.969 | 4.528 | 1.318 |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 23.987 | 1.825 | 13.146 |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `classic` | `strict_current` | 23.987 | 4.528 | 5.298 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.607 | 1.771 | 3.165 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `ax` | `strict_current` | 5.607 | 4.957 | 1.131 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.212 | 1.771 | 13.668 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `classic` | `strict_current` | 24.212 | 4.957 | 4.884 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.956 | 1.769 | 3.933 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `ax` | `strict_current` | 6.956 | 2.928 | 2.376 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.914 | 1.769 | 13.520 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `classic` | `strict_current` | 23.914 | 2.928 | 8.168 |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.400 | 1.670 | 3.832 |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `ax` | `strict_current` | 6.400 | 2.911 | 2.199 |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.341 | 1.670 | 14.573 |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `classic` | `strict_current` | 24.341 | 2.911 | 8.363 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 15.456 | 0.908 | 17.025 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 15.456 | 1.088 | 14.208 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 27.530 | 0.908 | 30.325 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 27.530 | 1.088 | 25.308 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.885 | 0.858 | 8.026 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `ax` | `strict_current` | 6.885 | 1.015 | 6.785 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.735 | 0.858 | 28.832 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `classic` | `strict_current` | 24.735 | 1.015 | 24.376 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 18.483 | 0.909 | 20.330 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `ax` | `strict_current` | 18.483 | 0.907 | 20.371 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 28.771 | 0.909 | 31.647 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `classic` | `strict_current` | 28.771 | 0.907 | 31.710 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.551 | 0.962 | 6.808 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `ax` | `strict_current` | 6.551 | 1.220 | 5.368 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.584 | 0.962 | 25.549 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `classic` | `strict_current` | 24.584 | 1.220 | 20.144 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.208 | 0.827 | 8.720 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.208 | 1.660 | 4.342 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.926 | 0.827 | 30.155 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.926 | 1.660 | 15.016 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.366 | 0.788 | 8.075 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `ax` | `strict_current` | 6.366 | 1.640 | 3.882 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.316 | 0.788 | 29.574 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `classic` | `strict_current` | 23.316 | 1.640 | 14.218 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.606 | 0.868 | 7.607 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `ax` | `strict_current` | 6.606 | 1.671 | 3.953 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.062 | 0.868 | 28.857 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `classic` | `strict_current` | 25.062 | 1.671 | 14.996 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.216 | 0.949 | 6.553 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `ax` | `strict_current` | 6.216 | 1.791 | 3.471 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.666 | 0.949 | 24.947 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `classic` | `strict_current` | 23.666 | 1.791 | 13.216 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 15.619 | 1.199 | 13.031 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 15.619 | 1.423 | 10.976 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 13.315 | 1.199 | 11.109 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 13.315 | 1.423 | 9.356 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 15.125 | 1.141 | 13.251 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `ax` | `strict_current` | 15.125 | 1.302 | 11.621 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.525 | 1.141 | 12.726 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `classic` | `strict_current` | 14.525 | 1.302 | 11.160 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.333 | 1.084 | 5.843 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 6.333 | 1.303 | 4.860 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.195 | 1.084 | 12.172 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 13.195 | 1.303 | 10.125 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.757 | 1.057 | 6.393 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `ax` | `strict_current` | 6.757 | 1.366 | 4.947 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.243 | 1.057 | 13.476 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `classic` | `strict_current` | 14.243 | 1.366 | 10.428 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.274 | 0.862 | 7.281 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.274 | 1.053 | 5.957 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.839 | 0.862 | 28.827 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.839 | 1.053 | 23.585 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.161 | 0.985 | 6.254 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `ax` | `strict_current` | 6.161 | 1.028 | 5.995 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.040 | 0.985 | 26.434 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `classic` | `strict_current` | 26.040 | 1.028 | 25.341 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.292 | 0.907 | 6.941 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `ax` | `strict_current` | 6.292 | 0.960 | 6.553 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.399 | 0.907 | 28.015 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `classic` | `strict_current` | 25.399 | 0.960 | 26.450 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.317 | 0.931 | 6.788 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `ax` | `strict_current` | 6.317 | 1.103 | 5.728 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.756 | 0.931 | 26.603 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `classic` | `strict_current` | 24.756 | 1.103 | 22.447 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.341 | 0.873 | 7.266 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.341 | 1.018 | 6.229 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 14.507 | 0.873 | 16.624 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 14.507 | 1.018 | 14.251 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.049 | 0.824 | 7.344 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `ax` | `strict_current` | 6.049 | 0.992 | 6.100 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.971 | 0.824 | 18.175 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `classic` | `strict_current` | 14.971 | 0.992 | 15.096 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.379 | 0.951 | 6.707 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `ax` | `strict_current` | 6.379 | 1.054 | 6.053 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.969 | 0.951 | 14.687 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `classic` | `strict_current` | 13.969 | 1.054 | 13.255 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.419 | 0.934 | 6.870 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `ax` | `strict_current` | 6.419 | 0.991 | 6.476 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.372 | 0.934 | 16.450 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `classic` | `strict_current` | 15.372 | 0.991 | 15.508 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 4.956 | 15.864 | 0.312 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `ax` | `strict_current` | 4.956 | 33.042 | 0.150 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 17.765 | 15.864 | 1.120 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `classic` | `strict_current` | 17.765 | 33.042 | 0.538 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 4.409 | 16.041 | 0.275 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `ax` | `strict_current` | 4.409 | 33.159 | 0.133 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 17.629 | 16.041 | 1.099 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `classic` | `strict_current` | 17.629 | 33.159 | 0.532 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 4.507 | 16.157 | 0.279 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `ax` | `strict_current` | 4.507 | 33.251 | 0.136 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 18.177 | 16.157 | 1.125 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `classic` | `strict_current` | 18.177 | 33.251 | 0.547 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 4.351 | 15.648 | 0.278 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `ax` | `strict_current` | 4.351 | 33.807 | 0.129 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 17.090 | 15.648 | 1.092 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `classic` | `strict_current` | 17.090 | 33.807 | 0.506 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 11.612 | 11.546 | 1.006 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `ax` | `strict_current` | 11.612 | 67.666 | 0.172 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 17.996 | 11.546 | 1.559 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `classic` | `strict_current` | 17.996 | 67.666 | 0.266 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 4.426 | 8.630 | 0.513 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `ax` | `strict_current` | 4.426 | 66.681 | 0.066 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 17.050 | 8.630 | 1.976 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `classic` | `strict_current` | 17.050 | 66.681 | 0.256 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.099 | 8.458 | 0.603 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `ax` | `strict_current` | 5.099 | 68.518 | 0.074 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 16.136 | 8.458 | 1.908 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `classic` | `strict_current` | 16.136 | 68.518 | 0.236 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.999 | 8.505 | 1.293 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `ax` | `strict_current` | 10.999 | 67.325 | 0.163 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 17.751 | 8.505 | 2.087 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `classic` | `strict_current` | 17.751 | 67.325 | 0.264 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.290 | 0.783 | 9.312 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.290 | 1.368 | 5.327 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 14.100 | 0.783 | 18.012 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `classic` | `strict_current` | 14.100 | 1.368 | 10.304 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.203 | 0.798 | 7.772 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `ax` | `strict_current` | 6.203 | 1.240 | 5.004 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.527 | 0.798 | 16.950 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `classic` | `strict_current` | 13.527 | 1.240 | 10.913 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.386 | 0.867 | 7.362 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `ax` | `strict_current` | 6.386 | 1.137 | 5.616 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.078 | 0.867 | 17.383 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `classic` | `strict_current` | 15.078 | 1.137 | 13.261 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.873 | 0.808 | 8.505 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `ax` | `strict_current` | 6.873 | 1.255 | 5.475 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.508 | 0.808 | 17.953 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `classic` | `strict_current` | 14.508 | 1.255 | 11.557 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.185 | 2.252 | 2.747 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.185 | 9.388 | 0.659 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 37.499 | 2.252 | 16.652 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 37.499 | 9.388 | 3.994 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.725 | 2.135 | 2.682 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `ax` | `strict_current` | 5.725 | 9.095 | 0.629 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 36.247 | 2.135 | 16.980 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `classic` | `strict_current` | 36.247 | 9.095 | 3.985 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.715 | 2.123 | 2.692 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 5.715 | 9.352 | 0.611 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 40.946 | 2.123 | 19.290 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 40.946 | 9.352 | 4.378 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.381 | 2.186 | 2.919 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `ax` | `strict_current` | 6.381 | 9.273 | 0.688 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 42.112 | 2.186 | 19.263 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `classic` | `strict_current` | 42.112 | 9.273 | 4.541 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.301 | 0.748 | 9.767 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `ax` | `strict_current` | 7.301 | 0.914 | 7.987 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.110 | 0.748 | 33.592 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `classic` | `strict_current` | 25.110 | 0.914 | 27.470 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.491 | 0.734 | 8.847 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `ax` | `strict_current` | 6.491 | 0.853 | 7.607 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.788 | 0.734 | 32.423 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `classic` | `strict_current` | 23.788 | 0.853 | 27.877 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.778 | 0.777 | 8.721 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `ax` | `strict_current` | 6.778 | 0.931 | 7.277 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.514 | 0.777 | 34.111 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `classic` | `strict_current` | 26.514 | 0.931 | 28.464 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 16.082 | 1.107 | 14.531 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `ax` | `strict_current` | 16.082 | 1.296 | 12.405 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.617 | 1.107 | 23.146 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.617 | 1.296 | 19.759 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.696 | 1.032 | 6.488 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `ax` | `strict_current` | 6.696 | 1.175 | 5.698 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.414 | 1.032 | 25.594 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `classic` | `strict_current` | 26.414 | 1.175 | 22.476 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.786 | 1.074 | 5.389 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `ax` | `strict_current` | 5.786 | 1.402 | 4.128 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.953 | 1.074 | 22.309 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `classic` | `strict_current` | 23.953 | 1.402 | 17.087 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 16.727 | 1.140 | 14.677 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `ax` | `strict_current` | 16.727 | 1.231 | 13.593 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.779 | 1.140 | 22.620 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `classic` | `strict_current` | 25.779 | 1.231 | 20.949 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.686 | 0.809 | 8.266 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.686 | 1.100 | 6.080 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 26.976 | 0.809 | 33.354 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `classic` | `strict_current` | 26.976 | 1.100 | 24.533 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.817 | 1.062 | 8.303 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `ax` | `strict_current` | 8.817 | 1.236 | 7.132 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.893 | 1.062 | 24.382 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `classic` | `strict_current` | 25.893 | 1.236 | 20.944 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.409 | 0.834 | 7.686 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `ax` | `strict_current` | 6.409 | 0.993 | 6.451 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.782 | 0.834 | 28.521 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `classic` | `strict_current` | 23.782 | 0.993 | 23.939 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.723 | 0.803 | 8.368 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `ax` | `strict_current` | 6.723 | 0.983 | 6.838 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.285 | 0.803 | 30.228 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `classic` | `strict_current` | 24.285 | 0.983 | 24.699 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.092 | 0.936 | 6.505 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.092 | 1.157 | 5.267 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 13.885 | 0.936 | 14.828 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `classic` | `strict_current` | 13.885 | 1.157 | 12.006 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.560 | 0.932 | 7.037 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `ax` | `strict_current` | 6.560 | 1.050 | 6.249 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.200 | 0.932 | 15.232 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `classic` | `strict_current` | 14.200 | 1.050 | 13.527 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.806 | 0.974 | 6.991 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `ax` | `strict_current` | 6.806 | 1.161 | 5.863 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.268 | 0.974 | 14.656 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `classic` | `strict_current` | 14.268 | 1.161 | 12.293 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.894 | 0.899 | 7.671 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `ax` | `strict_current` | 6.894 | 1.148 | 6.005 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.675 | 0.899 | 15.216 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `classic` | `strict_current` | 13.675 | 1.148 | 11.911 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 17.428 | 0.977 | 17.834 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `ax` | `strict_current` | 17.428 | 1.579 | 11.037 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 27.218 | 0.977 | 27.853 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `classic` | `strict_current` | 27.218 | 1.579 | 17.237 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.775 | 0.989 | 6.850 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `ax` | `strict_current` | 6.775 | 1.433 | 4.729 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.253 | 0.989 | 24.523 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `classic` | `strict_current` | 24.253 | 1.433 | 16.929 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 16.663 | 0.941 | 17.703 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `ax` | `strict_current` | 16.663 | 1.717 | 9.702 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.750 | 0.941 | 28.419 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `classic` | `strict_current` | 26.750 | 1.717 | 15.575 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 16.984 | 0.909 | 18.687 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `ax` | `strict_current` | 16.984 | 1.494 | 11.364 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.768 | 0.909 | 30.554 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `classic` | `strict_current` | 27.768 | 1.494 | 18.580 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 13.902 | 0.776 | 17.918 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `ax` | `strict_current` | 13.902 | 0.833 | 16.693 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 13.655 | 0.776 | 17.600 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `classic` | `strict_current` | 13.655 | 0.833 | 16.396 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.874 | 0.962 | 7.147 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `ax` | `strict_current` | 6.874 | 0.987 | 6.961 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.901 | 0.962 | 15.493 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `classic` | `strict_current` | 14.901 | 0.987 | 15.090 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 17.687 | 0.945 | 18.711 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `ax` | `strict_current` | 17.687 | 0.786 | 22.492 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 16.003 | 0.945 | 16.930 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `classic` | `strict_current` | 16.003 | 0.786 | 20.350 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.525 | 0.804 | 9.364 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `ax` | `strict_current` | 7.525 | 0.820 | 9.173 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.755 | 0.804 | 17.115 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `classic` | `strict_current` | 13.755 | 0.820 | 16.766 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 5.962 | 1.267 | 4.707 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `ax` | `strict_current` | 5.962 | 2.155 | 2.766 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.445 | 1.267 | 19.296 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.445 | 2.155 | 11.342 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.998 | 1.388 | 5.043 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `ax` | `strict_current` | 6.998 | 2.114 | 3.310 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.354 | 1.388 | 17.551 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `classic` | `strict_current` | 24.354 | 2.114 | 11.520 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.875 | 1.208 | 5.691 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `ax` | `strict_current` | 6.875 | 2.021 | 3.403 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.926 | 1.208 | 20.631 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `classic` | `strict_current` | 24.926 | 2.021 | 12.335 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.646 | 1.256 | 5.292 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `ax` | `strict_current` | 6.646 | 2.148 | 3.094 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.428 | 1.256 | 19.451 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `classic` | `strict_current` | 24.428 | 2.148 | 11.371 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.514 | 1.033 | 6.309 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `ax` | `strict_current` | 6.514 | 0.982 | 6.636 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 28.533 | 1.033 | 27.633 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `classic` | `strict_current` | 28.533 | 0.982 | 29.067 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.203 | 0.887 | 6.995 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `ax` | `strict_current` | 6.203 | 1.049 | 5.915 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.335 | 0.887 | 28.567 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `classic` | `strict_current` | 25.335 | 1.049 | 24.158 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.652 | 1.006 | 7.609 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `ax` | `strict_current` | 7.652 | 1.009 | 7.581 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.681 | 1.006 | 14.600 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `classic` | `strict_current` | 14.681 | 1.009 | 14.546 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.608 | 0.954 | 6.930 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `ax` | `strict_current` | 6.608 | 1.089 | 6.067 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.501 | 0.954 | 15.208 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `classic` | `strict_current` | 14.501 | 1.089 | 13.314 |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.631 | 0.985 | 6.731 |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `ax` | `strict_current` | 6.631 | 0.989 | 6.707 |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.885 | 0.985 | 14.094 |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `classic` | `strict_current` | 13.885 | 0.989 | 14.043 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.179 | 1.114 | 5.548 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.179 | 1.137 | 5.435 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 14.293 | 1.114 | 12.834 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `classic` | `strict_current` | 14.293 | 1.137 | 12.573 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.886 | 1.025 | 6.718 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `ax` | `strict_current` | 6.886 | 0.927 | 7.429 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.601 | 1.025 | 14.244 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `classic` | `strict_current` | 14.601 | 0.927 | 15.752 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.925 | 1.046 | 6.618 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `ax` | `strict_current` | 6.925 | 1.019 | 6.797 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.271 | 1.046 | 13.638 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `classic` | `strict_current` | 14.271 | 1.019 | 14.006 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.745 | 0.892 | 7.561 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `ax` | `strict_current` | 6.745 | 0.980 | 6.882 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.680 | 0.892 | 15.334 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `classic` | `strict_current` | 13.680 | 0.980 | 13.957 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.723 | 0.948 | 7.091 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.723 | 1.286 | 5.230 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.929 | 0.948 | 26.293 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.929 | 1.286 | 19.391 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.738 | 1.065 | 6.330 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `ax` | `strict_current` | 6.738 | 1.457 | 4.625 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.932 | 1.065 | 23.420 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `classic` | `strict_current` | 24.932 | 1.457 | 17.112 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.309 | 0.802 | 7.866 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `ax` | `strict_current` | 6.309 | 1.430 | 4.414 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.673 | 0.802 | 32.007 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `classic` | `strict_current` | 25.673 | 1.430 | 17.960 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.215 | 0.824 | 7.544 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `ax` | `strict_current` | 6.215 | 1.362 | 4.564 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.290 | 0.824 | 30.700 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `classic` | `strict_current` | 25.290 | 1.362 | 18.571 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.396 | 1.845 | 3.466 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.396 | 2.361 | 2.709 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 23.286 | 1.845 | 12.620 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 23.286 | 2.361 | 9.861 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.754 | 1.156 | 5.842 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `ax` | `strict_current` | 6.754 | 2.839 | 2.379 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.913 | 1.156 | 20.684 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `classic` | `strict_current` | 23.913 | 2.839 | 8.424 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.560 | 1.207 | 5.437 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 6.560 | 2.898 | 2.264 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.466 | 1.207 | 19.447 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 23.466 | 2.898 | 8.097 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.933 | 1.175 | 5.049 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `ax` | `strict_current` | 5.933 | 2.926 | 2.028 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.197 | 1.175 | 20.595 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `classic` | `strict_current` | 24.197 | 2.926 | 8.270 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.969 | 0.868 | 9.177 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.969 | 1.696 | 4.698 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 27.086 | 0.868 | 31.195 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `classic` | `strict_current` | 27.086 | 1.696 | 15.970 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.435 | 0.823 | 7.817 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `ax` | `strict_current` | 6.435 | 1.687 | 3.816 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.112 | 0.823 | 30.505 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `classic` | `strict_current` | 25.112 | 1.687 | 14.890 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.896 | 0.899 | 7.671 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `ax` | `strict_current` | 6.896 | 1.695 | 4.068 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.906 | 0.899 | 27.706 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `classic` | `strict_current` | 24.906 | 1.695 | 14.693 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.514 | 0.896 | 7.272 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `ax` | `strict_current` | 6.514 | 1.645 | 3.961 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.496 | 0.896 | 27.347 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `classic` | `strict_current` | 24.496 | 1.645 | 14.894 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 15.927 | 0.786 | 20.267 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `ax` | `strict_current` | 15.927 | 1.056 | 15.089 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 28.615 | 0.786 | 36.412 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `classic` | `strict_current` | 28.615 | 1.056 | 27.108 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.746 | 0.853 | 7.910 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `ax` | `strict_current` | 6.746 | 0.829 | 8.142 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.710 | 0.853 | 32.491 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `classic` | `strict_current` | 27.710 | 0.829 | 33.444 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.823 | 0.956 | 8.183 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `ax` | `strict_current` | 7.823 | 0.928 | 8.433 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.233 | 0.956 | 26.393 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `classic` | `strict_current` | 25.233 | 0.928 | 27.202 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 17.719 | 0.813 | 21.792 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `ax` | `strict_current` | 17.719 | 0.839 | 21.115 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.711 | 0.813 | 34.079 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `classic` | `strict_current` | 27.711 | 0.839 | 33.021 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.801 | 0.796 | 8.539 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.801 | 1.000 | 6.798 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.384 | 0.796 | 31.871 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.384 | 1.000 | 25.375 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.717 | 0.813 | 8.267 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `ax` | `strict_current` | 6.717 | 1.051 | 6.389 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.040 | 0.813 | 30.818 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `classic` | `strict_current` | 25.040 | 1.051 | 23.819 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.144 | 0.822 | 8.693 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 7.144 | 0.763 | 9.365 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.842 | 0.822 | 31.447 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 25.842 | 0.763 | 33.877 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.259 | 0.881 | 7.103 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `ax` | `strict_current` | 6.259 | 0.865 | 7.235 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.636 | 0.881 | 29.096 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `classic` | `strict_current` | 25.636 | 0.865 | 29.636 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 15.349 | 0.984 | 15.606 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `ax` | `strict_current` | 15.349 | 1.178 | 13.028 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 15.011 | 0.984 | 15.262 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `classic` | `strict_current` | 15.011 | 1.178 | 12.741 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 14.843 | 0.909 | 16.323 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `ax` | `strict_current` | 14.843 | 1.252 | 11.860 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.846 | 0.909 | 15.227 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `classic` | `strict_current` | 13.846 | 1.252 | 11.063 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.628 | 1.136 | 5.833 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `ax` | `strict_current` | 6.628 | 1.300 | 5.100 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.725 | 1.136 | 13.839 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `classic` | `strict_current` | 15.725 | 1.300 | 12.098 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.542 | 0.824 | 7.936 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `ax` | `strict_current` | 6.542 | 1.222 | 5.354 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.585 | 0.824 | 16.479 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `classic` | `strict_current` | 13.585 | 1.222 | 11.117 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.564 | 0.850 | 7.720 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.564 | 1.051 | 6.246 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 27.288 | 0.850 | 32.094 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `classic` | `strict_current` | 27.288 | 1.051 | 25.965 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.480 | 0.887 | 7.307 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `ax` | `strict_current` | 6.480 | 0.931 | 6.962 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.232 | 0.887 | 27.322 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `classic` | `strict_current` | 24.232 | 0.931 | 26.035 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.085 | 0.944 | 6.446 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `ax` | `strict_current` | 6.085 | 1.010 | 6.022 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.584 | 0.944 | 26.044 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `classic` | `strict_current` | 24.584 | 1.010 | 24.331 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.620 | 0.937 | 7.065 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `ax` | `strict_current` | 6.620 | 0.970 | 6.823 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.838 | 0.937 | 26.509 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `classic` | `strict_current` | 24.838 | 0.970 | 25.603 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.910 | 1.088 | 6.352 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.910 | 1.084 | 6.373 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.517 | 1.088 | 22.536 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.517 | 1.084 | 22.611 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.132 | 0.938 | 6.535 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `ax` | `strict_current` | 6.132 | 1.076 | 5.700 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.088 | 0.938 | 25.670 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `classic` | `strict_current` | 24.088 | 1.076 | 22.390 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.548 | 1.191 | 6.335 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `ax` | `strict_current` | 7.548 | 1.262 | 5.983 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 28.118 | 1.191 | 23.599 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `classic` | `strict_current` | 28.118 | 1.262 | 22.287 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.002 | 1.205 | 5.810 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `ax` | `strict_current` | 7.002 | 1.110 | 6.307 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.688 | 1.205 | 20.486 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `classic` | `strict_current` | 24.688 | 1.110 | 22.238 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 16.392 | 1.094 | 14.989 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `ax` | `strict_current` | 16.392 | 1.238 | 13.240 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 15.555 | 1.094 | 14.224 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `classic` | `strict_current` | 15.555 | 1.238 | 12.564 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.952 | 1.091 | 6.375 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `ax` | `strict_current` | 6.952 | 1.145 | 6.074 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.122 | 1.091 | 13.867 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `classic` | `strict_current` | 15.122 | 1.145 | 13.213 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.831 | 1.197 | 6.543 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `ax` | `strict_current` | 7.831 | 0.898 | 8.720 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 16.372 | 1.197 | 13.679 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `classic` | `strict_current` | 16.372 | 0.898 | 18.232 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 14.949 | 1.112 | 13.442 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `ax` | `strict_current` | 14.949 | 0.911 | 16.416 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.699 | 1.112 | 12.318 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `classic` | `strict_current` | 13.699 | 0.911 | 15.043 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.450 | 0.924 | 6.978 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.450 | 1.277 | 5.050 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.206 | 0.924 | 26.188 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.206 | 1.277 | 18.950 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.460 | 0.913 | 7.079 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `ax` | `strict_current` | 6.460 | 1.463 | 4.415 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.681 | 0.913 | 27.045 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `classic` | `strict_current` | 24.681 | 1.463 | 16.868 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.464 | 0.857 | 7.542 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `ax` | `strict_current` | 6.464 | 1.337 | 4.834 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.257 | 0.857 | 29.471 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `classic` | `strict_current` | 25.257 | 1.337 | 18.891 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.282 | 0.848 | 7.410 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `ax` | `strict_current` | 6.282 | 1.321 | 4.756 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.523 | 0.848 | 30.106 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `classic` | `strict_current` | 25.523 | 1.321 | 19.321 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.235 | 1.868 | 3.337 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.235 | 4.280 | 1.457 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 23.879 | 1.868 | 12.781 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 23.879 | 4.280 | 5.580 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.647 | 1.911 | 3.477 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `ax` | `strict_current` | 6.647 | 4.354 | 1.526 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.791 | 1.911 | 12.447 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `classic` | `strict_current` | 23.791 | 4.354 | 5.464 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.561 | 2.058 | 3.188 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `ax` | `strict_current` | 6.561 | 4.391 | 1.494 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.050 | 2.058 | 11.688 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `classic` | `strict_current` | 24.050 | 4.391 | 5.477 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.273 | 1.734 | 3.616 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `ax` | `strict_current` | 6.273 | 4.213 | 1.489 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.820 | 1.734 | 13.734 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `classic` | `strict_current` | 23.820 | 4.213 | 5.653 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 17.369 | 0.877 | 19.797 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `ax` | `strict_current` | 17.369 | 1.085 | 16.007 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 26.436 | 0.877 | 30.131 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `classic` | `strict_current` | 26.436 | 1.085 | 24.362 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 17.296 | 0.962 | 17.975 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `ax` | `strict_current` | 17.296 | 0.935 | 18.499 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.081 | 0.962 | 27.105 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `classic` | `strict_current` | 26.081 | 0.935 | 27.895 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.424 | 0.799 | 8.044 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `ax` | `strict_current` | 6.424 | 1.056 | 6.084 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.081 | 0.799 | 31.406 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `classic` | `strict_current` | 25.081 | 1.056 | 23.754 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.540 | 0.798 | 8.196 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `ax` | `strict_current` | 6.540 | 1.141 | 5.734 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.519 | 0.798 | 31.982 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `classic` | `strict_current` | 25.519 | 1.141 | 22.372 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.576 | 1.686 | 3.900 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.576 | 3.220 | 2.042 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.055 | 1.686 | 14.265 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.055 | 3.220 | 7.469 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.694 | 1.765 | 3.794 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `ax` | `strict_current` | 6.694 | 3.244 | 2.064 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.849 | 1.765 | 13.515 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `classic` | `strict_current` | 23.849 | 3.244 | 7.352 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.566 | 1.782 | 3.685 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `ax` | `strict_current` | 6.566 | 3.056 | 2.148 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.874 | 1.782 | 13.400 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `classic` | `strict_current` | 23.874 | 3.056 | 7.812 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.563 | 1.842 | 3.562 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `ax` | `strict_current` | 6.563 | 3.149 | 2.084 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 22.657 | 1.842 | 12.298 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `classic` | `strict_current` | 22.657 | 3.149 | 7.196 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.113 | 1.305 | 5.450 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `ax` | `strict_current` | 7.113 | 8.562 | 0.831 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.190 | 1.305 | 25.430 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `classic` | `strict_current` | 33.190 | 8.562 | 3.876 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.026 | 1.464 | 4.800 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `ax` | `strict_current` | 7.026 | 8.737 | 0.804 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 33.183 | 1.464 | 22.670 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `classic` | `strict_current` | 33.183 | 8.737 | 3.798 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.117 | 0.868 | 7.047 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `ax` | `strict_current` | 6.117 | 1.643 | 3.724 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.261 | 0.868 | 27.948 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `classic` | `strict_current` | 24.261 | 1.643 | 14.768 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.954 | 0.976 | 6.102 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `ax` | `strict_current` | 5.954 | 1.750 | 3.402 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.255 | 0.976 | 25.882 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `classic` | `strict_current` | 25.255 | 1.750 | 14.429 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.170 | 3.453 | 1.787 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `ax` | `strict_current` | 6.170 | 3.826 | 1.612 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.548 | 3.453 | 6.820 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `classic` | `strict_current` | 23.548 | 3.826 | 6.154 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.438 | 3.266 | 1.972 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `ax` | `strict_current` | 6.438 | 3.713 | 1.734 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.299 | 3.266 | 7.441 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `classic` | `strict_current` | 24.299 | 3.713 | 6.544 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.678 | 0.901 | 7.415 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `ax` | `strict_current` | 6.678 | 1.265 | 5.281 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.510 | 0.901 | 27.217 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `classic` | `strict_current` | 24.510 | 1.265 | 19.382 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.600 | 0.936 | 7.050 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `ax` | `strict_current` | 6.600 | 1.598 | 4.130 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.011 | 0.936 | 27.782 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `classic` | `strict_current` | 26.011 | 1.598 | 16.275 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.943 | 0.887 | 6.699 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `ax` | `strict_current` | 5.943 | 1.121 | 5.302 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.671 | 0.887 | 28.939 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `classic` | `strict_current` | 25.671 | 1.121 | 22.903 |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.562 | 0.962 | 6.820 |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `ax` | `strict_current` | 6.562 | 1.224 | 5.359 |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.513 | 0.962 | 27.558 |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `classic` | `strict_current` | 26.513 | 1.224 | 21.653 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.542 | 1.002 | 6.532 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `ax` | `strict_current` | 6.542 | 1.789 | 3.658 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.391 | 1.002 | 27.348 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `classic` | `strict_current` | 27.391 | 1.789 | 15.314 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.631 | 0.835 | 7.940 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `ax` | `strict_current` | 6.631 | 1.753 | 3.782 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.624 | 0.835 | 29.482 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `classic` | `strict_current` | 24.624 | 1.753 | 14.043 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.674 | 1.442 | 6.015 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `ax` | `strict_current` | 8.674 | 1.747 | 4.966 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 28.030 | 1.442 | 19.439 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `classic` | `strict_current` | 28.030 | 1.747 | 16.047 |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.781 | 1.355 | 5.006 |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `ax` | `strict_current` | 6.781 | 1.601 | 4.236 |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.295 | 1.355 | 17.936 |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `classic` | `strict_current` | 24.295 | 1.601 | 15.176 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.159 | 12.138 | 0.590 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `ax` | `strict_current` | 7.159 | 11.953 | 0.599 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 38.549 | 12.138 | 3.176 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `classic` | `strict_current` | 38.549 | 11.953 | 3.225 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.858 | 11.944 | 0.574 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `ax` | `strict_current` | 6.858 | 12.207 | 0.562 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 39.227 | 11.944 | 3.284 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `classic` | `strict_current` | 39.227 | 12.207 | 3.213 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.517 | 1.677 | 3.886 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `ax` | `strict_current` | 6.517 | 2.671 | 2.440 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.093 | 1.677 | 14.366 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `classic` | `strict_current` | 24.093 | 2.671 | 9.020 |
| `vbr1_l2_event_controller` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.752 | 1.632 | 4.138 |
| `vbr1_l2_event_controller` | `tb` | `gold` | `ax` | `strict_current` | 6.752 | 2.655 | 2.543 |
| `vbr1_l2_event_controller` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.634 | 1.632 | 15.098 |
| `vbr1_l2_event_controller` | `tb` | `gold` | `classic` | `strict_current` | 24.634 | 2.655 | 9.278 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.178 | 0.989 | 6.246 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `ax` | `strict_current` | 6.178 | 1.597 | 3.868 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.061 | 0.989 | 24.324 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `classic` | `strict_current` | 24.061 | 1.597 | 15.064 |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.557 | 1.075 | 6.102 |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `ax` | `strict_current` | 6.557 | 1.708 | 3.839 |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.404 | 1.075 | 22.710 |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `classic` | `strict_current` | 24.404 | 1.708 | 14.287 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.176 | 9.162 | 1.001 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `ax` | `strict_current` | 9.176 | 127.566 | 0.072 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 45.848 | 9.162 | 5.004 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `classic` | `strict_current` | 45.848 | 127.566 | 0.359 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.238 | 33.015 | 0.310 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `ax` | `strict_current` | 10.238 | 153.387 | 0.067 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 49.841 | 33.015 | 1.510 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `classic` | `strict_current` | 49.841 | 153.387 | 0.325 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.928 | 1.681 | 4.121 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `ax` | `strict_current` | 6.928 | 2.482 | 2.791 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.591 | 1.681 | 14.628 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `classic` | `strict_current` | 24.591 | 2.482 | 9.908 |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.633 | 1.727 | 3.842 |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `ax` | `strict_current` | 6.633 | 2.558 | 2.593 |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.360 | 1.727 | 13.530 |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `classic` | `strict_current` | 23.360 | 2.558 | 9.131 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.764 | 9.757 | 0.693 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `ax` | `strict_current` | 6.764 | 10.336 | 0.654 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 22.022 | 9.757 | 2.257 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `classic` | `strict_current` | 22.022 | 10.336 | 2.131 |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.543 | 10.033 | 0.652 |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `ax` | `strict_current` | 6.543 | 10.221 | 0.640 |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 22.745 | 10.033 | 2.267 |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `classic` | `strict_current` | 22.745 | 10.221 | 2.225 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.402 | 1.179 | 5.429 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `ax` | `strict_current` | 6.402 | 2.220 | 2.884 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.070 | 1.179 | 21.262 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `classic` | `strict_current` | 25.070 | 2.220 | 11.293 |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.442 | 1.227 | 5.249 |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `ax` | `strict_current` | 6.442 | 2.246 | 2.868 |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.542 | 1.227 | 19.999 |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `classic` | `strict_current` | 24.542 | 2.246 | 10.928 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.428 | 1.312 | 4.900 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `ax` | `strict_current` | 6.428 | 16.918 | 0.380 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 45.832 | 1.312 | 34.936 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `classic` | `strict_current` | 45.832 | 16.918 | 2.709 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.121 | 2.580 | 2.372 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `ax` | `strict_current` | 6.121 | 17.108 | 0.358 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 41.845 | 2.580 | 16.219 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `classic` | `strict_current` | 41.845 | 17.108 | 2.446 |

## Interpretation Guardrails

- Speedups use `simulation_ok`, so rows without a behavior checker can still contribute timing if the simulator produced waveforms.
- Accuracy-gated speedups require candidate behavior pass, strict-EVAS parity, and parity to every selected Spectre mode.
- `spectre/ax` matches the previous bridge default but Spectre X may ignore `errpreset` and `maxstep` from the testbench.
- `spectre/classic` is available to measure the stricter non-X path when requested.
- Cold Spectre runs include AHDL CMI compilation; warm-cache repetitions should be reported separately.
- A `BLOCKED` gate is not evidence of wrong behavior; it means the checker or reference evidence is incomplete.
