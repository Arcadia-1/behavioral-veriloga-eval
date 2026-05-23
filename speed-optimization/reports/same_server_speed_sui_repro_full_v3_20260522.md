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
- Output root: `results/same-server-speed-sui-repro-full-v3-20260522`

## Mode Summary

| Backend | Mode | Runs | PASS | Non-PASS | Total wall s | Mean wall s |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| evas | profile_fast_skip_source_error_control | 259 | 235 | 24 | 424.512 | 1.639 |
| evas | strict_current | 259 | 235 | 24 | 1441.278 | 5.565 |
| spectre | ax | 259 | 235 | 24 | 2091.707 | 8.076 |
| spectre | classic | 259 | 235 | 24 | 6456.935 | 24.930 |

## Accuracy Gate Summary

| EVAS mode | Runs | Gate PASS | Gate FAIL | Gate BLOCKED | Gate missing |
| --- | ---: | ---: | ---: | ---: | ---: |
| profile_fast_skip_source_error_control | 259 | 235 | 0 | 24 | 0 |
| strict_current | 259 | 235 | 0 | 24 | 0 |

## Per-Row Accuracy Gates

| Entry | Form | Variant | EVAS mode | Gate | Reasons | Blocked |
| --- | --- | --- | --- | --- | --- | --- |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `strict_current` | `BLOCKED` | - | candidate_no_behavior_checker, spectre_ax_parity:spectre_no_behavior_checker, spectre_classic_parity:spectre_no_behavior_checker |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `BLOCKED` | - | candidate_no_behavior_checker, spectre_ax_parity:spectre_no_behavior_checker, spectre_classic_parity:spectre_no_behavior_checker |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `strict_current` | `BLOCKED` | - | candidate_no_behavior_checker, spectre_ax_parity:spectre_no_behavior_checker, spectre_classic_parity:spectre_no_behavior_checker |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `BLOCKED` | - | candidate_no_behavior_checker, spectre_ax_parity:spectre_no_behavior_checker, spectre_classic_parity:spectre_no_behavior_checker |
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
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `strict_current` | `BLOCKED` | - | candidate_no_behavior_checker, spectre_ax_parity:spectre_no_behavior_checker, spectre_classic_parity:spectre_no_behavior_checker |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `BLOCKED` | - | candidate_no_behavior_checker, spectre_ax_parity:spectre_no_behavior_checker, spectre_classic_parity:spectre_no_behavior_checker |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `strict_current` | `BLOCKED` | - | candidate_no_behavior_checker, spectre_ax_parity:spectre_no_behavior_checker, spectre_classic_parity:spectre_no_behavior_checker |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `BLOCKED` | - | candidate_no_behavior_checker, spectre_ax_parity:spectre_no_behavior_checker, spectre_classic_parity:spectre_no_behavior_checker |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `strict_current` | `BLOCKED` | - | candidate_no_behavior_checker, spectre_ax_parity:spectre_no_behavior_checker, spectre_classic_parity:spectre_no_behavior_checker |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `BLOCKED` | - | candidate_no_behavior_checker, spectre_ax_parity:spectre_no_behavior_checker, spectre_classic_parity:spectre_no_behavior_checker |
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
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `strict_current` | `BLOCKED` | - | candidate_no_behavior_checker, spectre_ax_parity:spectre_no_behavior_checker, spectre_classic_parity:spectre_no_behavior_checker |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `BLOCKED` | - | candidate_no_behavior_checker, spectre_ax_parity:spectre_no_behavior_checker, spectre_classic_parity:spectre_no_behavior_checker |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `strict_current` | `BLOCKED` | - | candidate_no_behavior_checker, spectre_ax_parity:spectre_no_behavior_checker, spectre_classic_parity:spectre_no_behavior_checker |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `BLOCKED` | - | candidate_no_behavior_checker, spectre_ax_parity:spectre_no_behavior_checker, spectre_classic_parity:spectre_no_behavior_checker |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `strict_current` | `BLOCKED` | - | candidate_no_behavior_checker, spectre_ax_parity:spectre_no_behavior_checker, spectre_classic_parity:spectre_no_behavior_checker |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `BLOCKED` | - | candidate_no_behavior_checker, spectre_ax_parity:spectre_no_behavior_checker, spectre_classic_parity:spectre_no_behavior_checker |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `strict_current` | `BLOCKED` | - | candidate_no_behavior_checker, spectre_ax_parity:spectre_no_behavior_checker, spectre_classic_parity:spectre_no_behavior_checker |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `BLOCKED` | - | candidate_no_behavior_checker, spectre_ax_parity:spectre_no_behavior_checker, spectre_classic_parity:spectre_no_behavior_checker |
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
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `strict_current` | `BLOCKED` | - | candidate_no_behavior_checker, spectre_ax_parity:spectre_no_behavior_checker, spectre_classic_parity:spectre_no_behavior_checker |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `BLOCKED` | - | candidate_no_behavior_checker, spectre_ax_parity:spectre_no_behavior_checker, spectre_classic_parity:spectre_no_behavior_checker |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `strict_current` | `BLOCKED` | - | candidate_no_behavior_checker, spectre_ax_parity:spectre_no_behavior_checker, spectre_classic_parity:spectre_no_behavior_checker |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `BLOCKED` | - | candidate_no_behavior_checker, spectre_ax_parity:spectre_no_behavior_checker, spectre_classic_parity:spectre_no_behavior_checker |
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
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `strict_current` | `BLOCKED` | - | candidate_no_behavior_checker, spectre_ax_parity:spectre_no_behavior_checker, spectre_classic_parity:spectre_no_behavior_checker |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `BLOCKED` | - | candidate_no_behavior_checker, spectre_ax_parity:spectre_no_behavior_checker, spectre_classic_parity:spectre_no_behavior_checker |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `strict_current` | `BLOCKED` | - | candidate_no_behavior_checker, spectre_ax_parity:spectre_no_behavior_checker, spectre_classic_parity:spectre_no_behavior_checker |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `BLOCKED` | - | candidate_no_behavior_checker, spectre_ax_parity:spectre_no_behavior_checker, spectre_classic_parity:spectre_no_behavior_checker |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `strict_current` | `BLOCKED` | - | candidate_no_behavior_checker, spectre_ax_parity:spectre_no_behavior_checker, spectre_classic_parity:spectre_no_behavior_checker |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `BLOCKED` | - | candidate_no_behavior_checker, spectre_ax_parity:spectre_no_behavior_checker, spectre_classic_parity:spectre_no_behavior_checker |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `strict_current` | `BLOCKED` | - | candidate_no_behavior_checker, spectre_ax_parity:spectre_no_behavior_checker, spectre_classic_parity:spectre_no_behavior_checker |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `BLOCKED` | - | candidate_no_behavior_checker, spectre_ax_parity:spectre_no_behavior_checker, spectre_classic_parity:spectre_no_behavior_checker |
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
| `vbr1_l2_event_controller` | `tb` | `gold` | `strict_current` | `BLOCKED` | - | candidate_no_behavior_checker, spectre_ax_parity:spectre_no_behavior_checker, spectre_classic_parity:spectre_no_behavior_checker |
| `vbr1_l2_event_controller` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `BLOCKED` | - | candidate_no_behavior_checker, spectre_ax_parity:spectre_no_behavior_checker, spectre_classic_parity:spectre_no_behavior_checker |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `strict_current` | `BLOCKED` | - | candidate_no_behavior_checker, spectre_ax_parity:spectre_no_behavior_checker, spectre_classic_parity:spectre_no_behavior_checker |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `BLOCKED` | - | candidate_no_behavior_checker, spectre_ax_parity:spectre_no_behavior_checker, spectre_classic_parity:spectre_no_behavior_checker |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `strict_current` | `BLOCKED` | - | candidate_no_behavior_checker, spectre_ax_parity:spectre_no_behavior_checker, spectre_classic_parity:spectre_no_behavior_checker |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `BLOCKED` | - | candidate_no_behavior_checker, spectre_ax_parity:spectre_no_behavior_checker, spectre_classic_parity:spectre_no_behavior_checker |
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
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `strict_current` | `BLOCKED` | - | candidate_no_behavior_checker, spectre_ax_parity:spectre_no_behavior_checker, spectre_classic_parity:spectre_no_behavior_checker |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `BLOCKED` | - | candidate_no_behavior_checker, spectre_ax_parity:spectre_no_behavior_checker, spectre_classic_parity:spectre_no_behavior_checker |
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
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `strict_current` | `BLOCKED` | - | candidate_no_behavior_checker, spectre_ax_parity:spectre_no_behavior_checker, spectre_classic_parity:spectre_no_behavior_checker |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `BLOCKED` | - | candidate_no_behavior_checker, spectre_ax_parity:spectre_no_behavior_checker, spectre_classic_parity:spectre_no_behavior_checker |
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
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `strict_current` | `BLOCKED` | - | candidate_no_behavior_checker, spectre_ax_parity:spectre_no_behavior_checker, spectre_classic_parity:spectre_no_behavior_checker |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `BLOCKED` | - | candidate_no_behavior_checker, spectre_ax_parity:spectre_no_behavior_checker, spectre_classic_parity:spectre_no_behavior_checker |
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
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `strict_current` | `BLOCKED` | - | candidate_no_behavior_checker, spectre_ax_parity:spectre_no_behavior_checker, spectre_classic_parity:spectre_no_behavior_checker |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `BLOCKED` | - | candidate_no_behavior_checker, spectre_ax_parity:spectre_no_behavior_checker, spectre_classic_parity:spectre_no_behavior_checker |
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
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `strict_current` | `BLOCKED` | - | candidate_no_behavior_checker, spectre_ax_parity:spectre_no_behavior_checker, spectre_classic_parity:spectre_no_behavior_checker |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `BLOCKED` | - | candidate_no_behavior_checker, spectre_ax_parity:spectre_no_behavior_checker, spectre_classic_parity:spectre_no_behavior_checker |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `strict_current` | `BLOCKED` | - | candidate_no_behavior_checker, spectre_ax_parity:spectre_no_behavior_checker, spectre_classic_parity:spectre_no_behavior_checker |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `BLOCKED` | - | candidate_no_behavior_checker, spectre_ax_parity:spectre_no_behavior_checker, spectre_classic_parity:spectre_no_behavior_checker |
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
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.007 | 1.117 | 6.271 |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.007 | 1.401 | 5.001 |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 26.454 | 1.117 | 23.677 |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `classic` | `strict_current` | 26.454 | 1.401 | 18.881 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.322 | 1.148 | 5.506 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `ax` | `strict_current` | 6.322 | 1.538 | 4.111 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.615 | 1.148 | 24.048 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `classic` | `strict_current` | 27.615 | 1.538 | 17.957 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.253 | 1.187 | 5.267 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `ax` | `strict_current` | 6.253 | 1.298 | 4.818 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.230 | 1.187 | 22.096 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `classic` | `strict_current` | 26.230 | 1.298 | 20.213 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.050 | 1.335 | 6.029 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `ax` | `strict_current` | 8.050 | 1.606 | 5.013 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.560 | 1.335 | 20.640 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `classic` | `strict_current` | 27.560 | 1.606 | 17.162 |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.308 | 0.866 | 8.435 |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.308 | 9.773 | 0.748 |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.075 | 0.866 | 27.788 |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.075 | 9.773 | 2.463 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.911 | 1.423 | 4.856 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `ax` | `strict_current` | 6.911 | 10.843 | 0.637 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.513 | 1.423 | 16.521 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `classic` | `strict_current` | 23.513 | 10.843 | 2.169 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.623 | 1.601 | 4.137 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `ax` | `strict_current` | 6.623 | 1.949 | 3.398 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.163 | 1.601 | 16.965 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `classic` | `strict_current` | 27.163 | 1.949 | 13.936 |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.778 | 0.892 | 7.599 |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `ax` | `strict_current` | 6.778 | 1.002 | 6.767 |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.476 | 0.892 | 30.801 |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `classic` | `strict_current` | 27.476 | 1.002 | 27.428 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 16.788 | 0.834 | 20.123 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `ax` | `strict_current` | 16.788 | 0.828 | 20.285 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 26.696 | 0.834 | 32.000 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `classic` | `strict_current` | 26.696 | 0.828 | 32.256 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 17.887 | 0.836 | 21.406 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `ax` | `strict_current` | 17.887 | 0.859 | 20.815 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.203 | 0.836 | 32.555 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `classic` | `strict_current` | 27.203 | 0.859 | 31.656 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 18.302 | 1.130 | 16.203 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `ax` | `strict_current` | 18.302 | 0.955 | 19.164 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 29.494 | 1.130 | 26.111 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `classic` | `strict_current` | 29.494 | 0.955 | 30.883 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.338 | 0.809 | 7.830 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `ax` | `strict_current` | 6.338 | 0.946 | 6.697 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.210 | 0.809 | 32.383 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `classic` | `strict_current` | 26.210 | 0.946 | 27.695 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.822 | 0.936 | 7.289 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `ax` | `strict_current` | 6.822 | 1.520 | 4.488 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.140 | 0.936 | 27.932 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `classic` | `strict_current` | 26.140 | 1.520 | 17.197 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.976 | 0.994 | 7.019 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `ax` | `strict_current` | 6.976 | 1.486 | 4.694 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.639 | 0.994 | 25.798 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `classic` | `strict_current` | 25.639 | 1.486 | 17.254 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.938 | 0.963 | 7.202 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `ax` | `strict_current` | 6.938 | 1.333 | 5.205 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.565 | 0.963 | 26.537 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `classic` | `strict_current` | 25.565 | 1.333 | 19.177 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.258 | 0.951 | 7.636 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.258 | 1.681 | 4.319 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 27.215 | 0.951 | 28.632 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `classic` | `strict_current` | 27.215 | 1.681 | 16.195 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.804 | 0.920 | 7.395 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `ax` | `strict_current` | 6.804 | 1.639 | 4.150 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.983 | 0.920 | 29.328 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `classic` | `strict_current` | 26.983 | 1.639 | 16.460 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.067 | 0.883 | 8.002 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `ax` | `strict_current` | 7.067 | 1.621 | 4.361 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.787 | 0.883 | 29.197 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `classic` | `strict_current` | 25.787 | 1.621 | 15.912 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.351 | 0.914 | 8.043 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `ax` | `strict_current` | 7.351 | 1.620 | 4.538 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.842 | 0.914 | 29.369 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `classic` | `strict_current` | 26.842 | 1.620 | 16.571 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.573 | 0.997 | 6.594 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.573 | 2.547 | 2.581 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.289 | 0.997 | 24.366 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.289 | 2.547 | 9.538 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.762 | 1.692 | 3.406 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `ax` | `strict_current` | 5.762 | 3.592 | 1.604 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.838 | 1.692 | 14.680 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `classic` | `strict_current` | 24.838 | 3.592 | 6.916 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.033 | 0.839 | 7.191 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `ax` | `strict_current` | 6.033 | 2.808 | 2.149 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.663 | 0.839 | 29.395 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `classic` | `strict_current` | 24.663 | 2.808 | 8.784 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.385 | 0.972 | 6.569 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `ax` | `strict_current` | 6.385 | 2.798 | 2.282 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.131 | 0.972 | 25.853 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `classic` | `strict_current` | 25.131 | 2.798 | 8.982 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.742 | 1.118 | 6.031 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.742 | 1.755 | 3.841 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 26.965 | 1.118 | 24.124 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `classic` | `strict_current` | 26.965 | 1.755 | 15.361 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.180 | 0.880 | 8.159 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `ax` | `strict_current` | 7.180 | 1.552 | 4.627 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.324 | 0.880 | 31.048 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `classic` | `strict_current` | 27.324 | 1.552 | 17.607 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.625 | 0.880 | 7.528 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `ax` | `strict_current` | 6.625 | 1.617 | 4.097 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.876 | 0.880 | 31.673 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `classic` | `strict_current` | 27.876 | 1.617 | 17.237 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.747 | 0.916 | 7.366 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `ax` | `strict_current` | 6.747 | 1.698 | 3.974 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.127 | 0.916 | 29.619 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `classic` | `strict_current` | 27.127 | 1.698 | 15.980 |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.137 | 0.942 | 6.513 |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.137 | 3.325 | 1.846 |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.167 | 0.942 | 25.649 |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.167 | 3.325 | 7.268 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.460 | 1.416 | 4.563 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `ax` | `strict_current` | 6.460 | 3.983 | 1.622 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.177 | 1.416 | 16.371 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `classic` | `strict_current` | 23.177 | 3.983 | 5.819 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.060 | 1.277 | 4.745 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `ax` | `strict_current` | 6.060 | 3.989 | 1.519 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.830 | 1.277 | 18.658 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `classic` | `strict_current` | 23.830 | 3.989 | 5.975 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.595 | 1.383 | 4.045 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `ax` | `strict_current` | 5.595 | 3.905 | 1.433 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.303 | 1.383 | 17.572 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `classic` | `strict_current` | 24.303 | 3.905 | 6.223 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.809 | 0.943 | 7.219 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.809 | 1.711 | 3.980 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 26.268 | 0.943 | 27.852 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `classic` | `strict_current` | 26.268 | 1.711 | 15.355 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.250 | 1.103 | 6.576 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `ax` | `strict_current` | 7.250 | 1.668 | 4.345 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.130 | 1.103 | 23.701 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `classic` | `strict_current` | 26.130 | 1.668 | 15.661 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.275 | 1.033 | 7.042 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `ax` | `strict_current` | 7.275 | 1.702 | 4.274 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.190 | 1.033 | 26.316 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `classic` | `strict_current` | 27.190 | 1.702 | 15.973 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.467 | 0.983 | 6.581 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `ax` | `strict_current` | 6.467 | 1.686 | 3.836 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.193 | 0.983 | 26.654 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `classic` | `strict_current` | 26.193 | 1.686 | 15.537 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 5.906 | 1.212 | 4.872 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 5.906 | 3.135 | 1.884 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.064 | 1.212 | 19.850 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.064 | 3.135 | 7.675 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.318 | 1.167 | 5.412 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `ax` | `strict_current` | 6.318 | 3.229 | 1.957 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.615 | 1.167 | 21.084 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `classic` | `strict_current` | 24.615 | 3.229 | 7.624 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.637 | 1.267 | 5.240 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 6.637 | 3.294 | 2.015 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.405 | 1.267 | 19.268 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 24.405 | 3.294 | 7.410 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.295 | 1.268 | 4.963 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `ax` | `strict_current` | 6.295 | 3.236 | 1.945 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.132 | 1.268 | 19.027 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `classic` | `strict_current` | 24.132 | 3.236 | 7.456 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.181 | 0.983 | 7.304 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.181 | 1.701 | 4.222 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 15.575 | 0.983 | 15.840 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `classic` | `strict_current` | 15.575 | 1.701 | 9.156 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.346 | 0.920 | 7.988 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `ax` | `strict_current` | 7.346 | 1.649 | 4.455 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.628 | 0.920 | 15.906 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `classic` | `strict_current` | 14.628 | 1.649 | 8.872 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.586 | 1.131 | 7.589 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `ax` | `strict_current` | 8.586 | 1.660 | 5.171 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 16.137 | 1.131 | 14.263 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `classic` | `strict_current` | 16.137 | 1.660 | 9.718 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.529 | 0.948 | 7.945 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `ax` | `strict_current` | 7.529 | 1.631 | 4.615 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 16.279 | 0.948 | 17.179 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `classic` | `strict_current` | 16.279 | 1.631 | 9.979 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.989 | 0.960 | 8.323 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `ax` | `strict_current` | 7.989 | 0.985 | 8.112 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 16.366 | 0.960 | 17.051 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `classic` | `strict_current` | 16.366 | 0.985 | 16.618 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.187 | 0.812 | 7.620 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `ax` | `strict_current` | 6.187 | 0.925 | 6.688 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.248 | 0.812 | 18.779 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `classic` | `strict_current` | 15.248 | 0.925 | 16.484 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.745 | 1.407 | 5.503 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `ax` | `strict_current` | 7.745 | 0.813 | 9.521 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.818 | 1.407 | 11.239 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `classic` | `strict_current` | 15.818 | 0.813 | 19.445 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.468 | 0.755 | 8.563 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.468 | 0.990 | 6.535 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.788 | 0.755 | 32.817 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.788 | 0.990 | 25.044 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.593 | 0.760 | 8.676 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `ax` | `strict_current` | 6.593 | 0.835 | 7.898 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.449 | 0.760 | 33.486 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `classic` | `strict_current` | 25.449 | 0.835 | 30.486 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.536 | 0.759 | 9.925 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `ax` | `strict_current` | 7.536 | 0.952 | 7.920 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.539 | 0.759 | 33.635 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `classic` | `strict_current` | 25.539 | 0.952 | 26.840 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.483 | 0.709 | 9.141 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `ax` | `strict_current` | 6.483 | 0.865 | 7.496 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.622 | 0.709 | 34.719 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `classic` | `strict_current` | 24.622 | 0.865 | 28.472 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 18.678 | 0.806 | 23.177 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `ax` | `strict_current` | 18.678 | 0.930 | 20.088 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 28.850 | 0.806 | 35.798 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `classic` | `strict_current` | 28.850 | 0.930 | 31.028 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.828 | 0.868 | 9.018 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `ax` | `strict_current` | 7.828 | 1.100 | 7.118 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 28.529 | 0.868 | 32.863 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `classic` | `strict_current` | 28.529 | 1.100 | 25.940 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.237 | 0.788 | 7.911 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `ax` | `strict_current` | 6.237 | 0.859 | 7.265 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.194 | 0.788 | 31.955 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `classic` | `strict_current` | 25.194 | 0.859 | 29.345 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 15.322 | 0.757 | 20.241 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `ax` | `strict_current` | 15.322 | 0.938 | 16.337 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.420 | 0.757 | 33.581 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `classic` | `strict_current` | 25.420 | 0.938 | 27.105 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.250 | 1.061 | 5.892 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.250 | 5.033 | 1.242 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 26.107 | 1.061 | 24.613 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `classic` | `strict_current` | 26.107 | 5.033 | 5.187 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.002 | 1.051 | 6.660 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `ax` | `strict_current` | 7.002 | 4.809 | 1.456 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.527 | 1.051 | 25.231 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `classic` | `strict_current` | 26.527 | 4.809 | 5.516 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.684 | 1.112 | 6.013 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `ax` | `strict_current` | 6.684 | 4.631 | 1.443 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.305 | 1.112 | 23.664 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `classic` | `strict_current` | 26.305 | 4.631 | 5.680 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.445 | 1.012 | 7.359 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `ax` | `strict_current` | 7.445 | 4.749 | 1.568 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.580 | 1.012 | 25.283 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `classic` | `strict_current` | 25.580 | 4.749 | 5.386 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.071 | 1.608 | 4.398 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.071 | 1.746 | 4.051 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.558 | 1.608 | 15.897 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.558 | 1.746 | 14.641 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.604 | 1.676 | 3.940 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `ax` | `strict_current` | 6.604 | 1.644 | 4.018 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.330 | 1.676 | 15.709 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `classic` | `strict_current` | 26.330 | 1.644 | 16.018 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.141 | 1.596 | 4.474 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `ax` | `strict_current` | 7.141 | 1.800 | 3.968 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.214 | 1.596 | 17.049 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `classic` | `strict_current` | 27.214 | 1.800 | 15.120 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.172 | 1.673 | 4.883 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `ax` | `strict_current` | 8.172 | 1.695 | 4.820 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.052 | 1.673 | 16.165 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `classic` | `strict_current` | 27.052 | 1.695 | 15.956 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.295 | 0.890 | 7.077 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `ax` | `strict_current` | 6.295 | 0.859 | 7.328 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 10.739 | 0.890 | 12.073 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `classic` | `strict_current` | 10.739 | 0.859 | 12.501 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.848 | 0.771 | 8.879 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `ax` | `strict_current` | 6.848 | 0.816 | 8.393 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.736 | 0.771 | 19.104 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `classic` | `strict_current` | 14.736 | 0.816 | 18.058 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.846 | 0.805 | 8.500 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `ax` | `strict_current` | 6.846 | 1.216 | 5.628 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.598 | 0.805 | 16.883 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `classic` | `strict_current` | 13.598 | 1.216 | 11.179 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 8.348 | 0.966 | 8.640 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `ax` | `strict_current` | 8.348 | 2.621 | 3.184 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 46.983 | 0.966 | 48.630 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `classic` | `strict_current` | 46.983 | 2.621 | 17.922 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.279 | 0.904 | 8.050 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `ax` | `strict_current` | 7.279 | 2.597 | 2.803 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 51.115 | 0.904 | 56.530 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `classic` | `strict_current` | 51.115 | 2.597 | 19.685 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.772 | 0.981 | 7.925 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `ax` | `strict_current` | 7.772 | 2.745 | 2.832 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 47.818 | 0.981 | 48.758 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `classic` | `strict_current` | 47.818 | 2.745 | 17.422 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.413 | 0.908 | 8.167 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `ax` | `strict_current` | 7.413 | 2.611 | 2.839 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 49.044 | 0.908 | 54.033 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `classic` | `strict_current` | 49.044 | 2.611 | 18.783 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 16.736 | 0.806 | 20.767 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 16.736 | 0.978 | 17.109 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 27.335 | 0.806 | 33.919 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 27.335 | 0.978 | 27.945 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.455 | 1.384 | 5.386 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `ax` | `strict_current` | 7.455 | 0.970 | 7.683 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 30.103 | 1.384 | 21.749 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `classic` | `strict_current` | 30.103 | 0.970 | 31.024 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.308 | 0.833 | 7.574 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `ax` | `strict_current` | 6.308 | 1.008 | 6.255 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.593 | 0.833 | 30.733 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `classic` | `strict_current` | 25.593 | 1.008 | 25.379 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 16.375 | 0.831 | 19.716 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `ax` | `strict_current` | 16.375 | 0.963 | 16.997 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 28.228 | 0.831 | 33.987 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `classic` | `strict_current` | 28.228 | 0.963 | 29.300 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.211 | 1.340 | 5.383 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `ax` | `strict_current` | 7.211 | 4.563 | 1.580 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.345 | 1.340 | 18.173 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `classic` | `strict_current` | 24.345 | 4.563 | 5.335 |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.233 | 0.787 | 7.917 |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `ax` | `strict_current` | 6.233 | 4.175 | 1.493 |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.053 | 0.787 | 30.550 |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `classic` | `strict_current` | 24.053 | 4.175 | 5.761 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 5.965 | 0.773 | 7.715 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `ax` | `strict_current` | 5.965 | 0.947 | 6.298 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.632 | 0.773 | 33.149 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.632 | 0.947 | 27.064 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.936 | 1.006 | 7.893 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `ax` | `strict_current` | 7.936 | 1.050 | 7.556 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.090 | 1.006 | 25.947 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `classic` | `strict_current` | 26.090 | 1.050 | 24.839 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.676 | 0.801 | 8.336 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `ax` | `strict_current` | 6.676 | 0.953 | 7.008 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.697 | 0.801 | 33.335 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `classic` | `strict_current` | 26.697 | 0.953 | 28.025 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.518 | 0.919 | 7.091 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `ax` | `strict_current` | 6.518 | 0.977 | 6.669 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.164 | 0.919 | 27.377 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `classic` | `strict_current` | 25.164 | 0.977 | 25.747 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.742 | 0.854 | 7.897 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.742 | 0.944 | 7.144 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 26.104 | 0.854 | 30.576 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `classic` | `strict_current` | 26.104 | 0.944 | 27.658 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.591 | 0.685 | 9.625 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `ax` | `strict_current` | 6.591 | 1.034 | 6.375 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.907 | 0.685 | 37.836 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `classic` | `strict_current` | 25.907 | 1.034 | 25.059 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.079 | 0.743 | 9.530 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `ax` | `strict_current` | 7.079 | 0.985 | 7.184 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.669 | 0.743 | 34.555 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `classic` | `strict_current` | 25.669 | 0.985 | 26.049 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.708 | 0.697 | 9.628 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `ax` | `strict_current` | 6.708 | 0.878 | 7.638 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.312 | 0.697 | 36.331 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `classic` | `strict_current` | 25.312 | 0.878 | 28.823 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 16.024 | 1.198 | 13.370 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `ax` | `strict_current` | 16.024 | 1.447 | 11.077 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 15.147 | 1.198 | 12.638 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `classic` | `strict_current` | 15.147 | 1.447 | 10.471 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.796 | 1.094 | 6.214 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `ax` | `strict_current` | 6.796 | 1.034 | 6.574 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.126 | 1.094 | 12.916 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `classic` | `strict_current` | 14.126 | 1.034 | 13.664 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 16.699 | 1.267 | 13.180 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `ax` | `strict_current` | 16.699 | 1.105 | 15.117 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 16.051 | 1.267 | 12.668 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `classic` | `strict_current` | 16.051 | 1.105 | 14.530 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.470 | 1.069 | 6.050 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `ax` | `strict_current` | 6.470 | 1.172 | 5.519 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.178 | 1.069 | 13.259 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `classic` | `strict_current` | 14.178 | 1.172 | 12.094 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.422 | 9.539 | 1.093 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `ax` | `strict_current` | 10.422 | 129.793 | 0.080 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 54.507 | 9.539 | 5.714 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `classic` | `strict_current` | 54.507 | 129.793 | 0.420 |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.841 | 9.911 | 1.094 |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `ax` | `strict_current` | 10.841 | 125.174 | 0.087 |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 52.078 | 9.911 | 5.254 |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `classic` | `strict_current` | 52.078 | 125.174 | 0.416 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 15.339 | 1.303 | 11.768 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `ax` | `strict_current` | 15.339 | 1.765 | 8.689 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 13.844 | 1.303 | 10.621 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `classic` | `strict_current` | 13.844 | 1.765 | 7.842 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 15.695 | 1.192 | 13.162 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `ax` | `strict_current` | 15.695 | 1.615 | 9.721 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.417 | 1.192 | 12.929 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `classic` | `strict_current` | 15.417 | 1.615 | 9.549 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.648 | 1.119 | 6.834 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `ax` | `strict_current` | 7.648 | 1.866 | 4.099 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.640 | 1.119 | 13.975 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `classic` | `strict_current` | 15.640 | 1.866 | 8.382 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.974 | 1.141 | 6.990 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `ax` | `strict_current` | 7.974 | 1.650 | 4.834 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.540 | 1.141 | 13.623 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `classic` | `strict_current` | 15.540 | 1.650 | 9.421 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 8.022 | 0.937 | 8.562 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `ax` | `strict_current` | 8.022 | 1.441 | 5.569 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.970 | 0.937 | 27.716 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.970 | 1.441 | 18.027 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.588 | 0.793 | 8.308 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `ax` | `strict_current` | 6.588 | 1.237 | 5.324 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.293 | 0.793 | 31.896 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `classic` | `strict_current` | 25.293 | 1.237 | 20.441 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.071 | 0.896 | 7.892 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `ax` | `strict_current` | 7.071 | 1.224 | 5.778 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.396 | 0.896 | 28.344 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `classic` | `strict_current` | 25.396 | 1.224 | 20.753 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.384 | 0.811 | 7.874 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `ax` | `strict_current` | 6.384 | 1.323 | 4.827 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.923 | 0.811 | 31.971 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `classic` | `strict_current` | 25.923 | 1.323 | 19.598 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.080 | 1.122 | 6.308 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.080 | 1.354 | 5.230 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.591 | 1.122 | 22.799 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.591 | 1.354 | 18.903 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.362 | 0.958 | 6.641 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `ax` | `strict_current` | 6.362 | 0.998 | 6.376 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.482 | 0.958 | 28.684 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `classic` | `strict_current` | 27.482 | 0.998 | 27.540 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.053 | 1.110 | 6.352 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 7.053 | 1.075 | 6.559 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.297 | 1.110 | 23.683 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 26.297 | 1.075 | 24.453 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.187 | 0.953 | 6.494 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `ax` | `strict_current` | 6.187 | 1.022 | 6.056 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.098 | 0.953 | 28.443 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `classic` | `strict_current` | 27.098 | 1.022 | 26.522 |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.679 | 0.937 | 7.132 |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.679 | 3.913 | 1.707 |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.488 | 0.937 | 26.148 |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.488 | 3.913 | 6.258 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.576 | 1.780 | 3.694 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `ax` | `strict_current` | 6.576 | 4.675 | 1.407 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.871 | 1.780 | 13.411 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `classic` | `strict_current` | 23.871 | 4.675 | 5.106 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.371 | 1.595 | 3.996 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `ax` | `strict_current` | 6.371 | 2.820 | 2.260 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.778 | 1.595 | 15.539 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `classic` | `strict_current` | 24.778 | 2.820 | 8.787 |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.453 | 0.947 | 6.814 |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `ax` | `strict_current` | 6.453 | 2.155 | 2.994 |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.792 | 0.947 | 26.177 |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `classic` | `strict_current` | 24.792 | 2.155 | 11.504 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 16.716 | 1.080 | 15.481 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 16.716 | 1.220 | 13.700 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 26.078 | 1.080 | 24.153 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 26.078 | 1.220 | 21.374 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.462 | 0.775 | 8.334 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `ax` | `strict_current` | 6.462 | 1.156 | 5.588 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.627 | 0.775 | 33.047 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `classic` | `strict_current` | 25.627 | 1.156 | 22.159 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 18.881 | 1.163 | 16.240 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `ax` | `strict_current` | 18.881 | 1.021 | 18.491 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 29.484 | 1.163 | 25.359 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `classic` | `strict_current` | 29.484 | 1.021 | 28.876 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.863 | 0.897 | 7.648 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `ax` | `strict_current` | 6.863 | 1.078 | 6.364 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.448 | 0.897 | 28.357 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `classic` | `strict_current` | 25.448 | 1.078 | 23.596 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.626 | 0.817 | 8.115 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.626 | 1.756 | 3.774 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 26.710 | 0.817 | 32.712 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `classic` | `strict_current` | 26.710 | 1.756 | 15.211 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.915 | 0.872 | 7.934 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `ax` | `strict_current` | 6.915 | 1.576 | 4.387 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.229 | 0.872 | 30.095 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `classic` | `strict_current` | 26.229 | 1.576 | 16.641 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.578 | 0.883 | 8.585 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `ax` | `strict_current` | 7.578 | 1.609 | 4.709 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.925 | 0.883 | 31.635 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `classic` | `strict_current` | 27.925 | 1.609 | 17.353 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.312 | 1.008 | 7.257 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `ax` | `strict_current` | 7.312 | 1.707 | 4.285 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.731 | 1.008 | 26.528 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `classic` | `strict_current` | 26.731 | 1.707 | 15.663 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 16.444 | 1.078 | 15.251 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 16.444 | 1.513 | 10.868 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 15.591 | 1.078 | 14.459 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 15.591 | 1.513 | 10.304 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 16.941 | 1.108 | 15.291 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `ax` | `strict_current` | 16.941 | 1.413 | 11.989 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.334 | 1.108 | 13.841 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `classic` | `strict_current` | 15.334 | 1.413 | 10.852 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.673 | 1.394 | 4.788 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 6.673 | 1.366 | 4.883 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.485 | 1.394 | 10.394 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 14.485 | 1.366 | 10.601 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.554 | 1.118 | 5.864 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `ax` | `strict_current` | 6.554 | 1.356 | 4.835 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.087 | 1.118 | 13.498 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `classic` | `strict_current` | 15.087 | 1.356 | 11.130 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.595 | 0.908 | 7.262 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.595 | 1.176 | 5.610 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.521 | 0.908 | 27.002 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.521 | 1.176 | 20.857 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.537 | 0.899 | 7.274 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `ax` | `strict_current` | 6.537 | 1.072 | 6.096 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.261 | 0.899 | 30.337 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `classic` | `strict_current` | 27.261 | 1.072 | 25.423 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.303 | 0.947 | 6.653 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `ax` | `strict_current` | 6.303 | 1.032 | 6.108 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.679 | 0.947 | 27.103 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `classic` | `strict_current` | 25.679 | 1.032 | 24.885 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.810 | 0.852 | 6.818 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `ax` | `strict_current` | 5.810 | 0.958 | 6.063 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.300 | 0.852 | 29.689 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `classic` | `strict_current` | 25.300 | 0.958 | 26.402 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.072 | 0.879 | 8.043 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.072 | 0.996 | 7.104 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 14.939 | 0.879 | 16.989 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 14.939 | 0.996 | 15.005 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.409 | 0.858 | 7.473 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `ax` | `strict_current` | 6.409 | 1.049 | 6.110 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.307 | 0.858 | 16.682 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `classic` | `strict_current` | 14.307 | 1.049 | 13.639 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.721 | 0.878 | 7.657 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `ax` | `strict_current` | 6.721 | 1.297 | 5.184 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.619 | 0.878 | 16.653 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `classic` | `strict_current` | 14.619 | 1.297 | 11.275 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.916 | 0.833 | 8.302 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `ax` | `strict_current` | 6.916 | 1.105 | 6.258 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 16.138 | 0.833 | 19.372 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `classic` | `strict_current` | 16.138 | 1.105 | 14.603 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 4.845 | 15.953 | 0.304 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `ax` | `strict_current` | 4.845 | 33.966 | 0.143 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 18.539 | 15.953 | 1.162 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `classic` | `strict_current` | 18.539 | 33.966 | 0.546 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 4.417 | 16.232 | 0.272 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `ax` | `strict_current` | 4.417 | 32.917 | 0.134 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 17.049 | 16.232 | 1.050 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `classic` | `strict_current` | 17.049 | 32.917 | 0.518 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 4.870 | 15.971 | 0.305 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `ax` | `strict_current` | 4.870 | 33.013 | 0.148 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 17.278 | 15.971 | 1.082 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `classic` | `strict_current` | 17.278 | 33.013 | 0.523 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.060 | 16.088 | 0.315 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `ax` | `strict_current` | 5.060 | 33.650 | 0.150 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 17.501 | 16.088 | 1.088 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `classic` | `strict_current` | 17.501 | 33.650 | 0.520 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 11.343 | 8.983 | 1.263 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `ax` | `strict_current` | 11.343 | 69.545 | 0.163 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 17.558 | 8.983 | 1.955 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `classic` | `strict_current` | 17.558 | 69.545 | 0.252 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 4.129 | 8.749 | 0.472 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `ax` | `strict_current` | 4.129 | 68.112 | 0.061 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 16.521 | 8.749 | 1.888 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `classic` | `strict_current` | 16.521 | 68.112 | 0.243 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 4.052 | 8.847 | 0.458 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `ax` | `strict_current` | 4.052 | 69.966 | 0.058 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.705 | 8.847 | 1.775 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `classic` | `strict_current` | 15.705 | 69.966 | 0.224 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 11.052 | 8.576 | 1.289 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `ax` | `strict_current` | 11.052 | 66.564 | 0.166 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 17.496 | 8.576 | 2.040 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `classic` | `strict_current` | 17.496 | 66.564 | 0.263 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 8.029 | 0.880 | 9.120 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `ax` | `strict_current` | 8.029 | 1.407 | 5.705 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 14.771 | 0.880 | 16.777 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `classic` | `strict_current` | 14.771 | 1.407 | 10.495 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.286 | 0.836 | 7.523 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `ax` | `strict_current` | 6.286 | 1.182 | 5.320 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.754 | 0.836 | 16.459 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `classic` | `strict_current` | 13.754 | 1.182 | 11.641 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.592 | 0.779 | 8.466 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `ax` | `strict_current` | 6.592 | 1.150 | 5.734 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.757 | 0.779 | 18.951 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `classic` | `strict_current` | 14.757 | 1.150 | 12.836 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.856 | 0.845 | 8.117 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `ax` | `strict_current` | 6.856 | 1.106 | 6.201 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.187 | 0.845 | 17.979 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `classic` | `strict_current` | 15.187 | 1.106 | 13.735 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.015 | 3.222 | 2.177 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.015 | 9.279 | 0.756 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 43.607 | 3.222 | 13.532 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 43.607 | 9.279 | 4.700 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.544 | 2.597 | 2.905 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `ax` | `strict_current` | 7.544 | 9.396 | 0.803 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 41.950 | 2.597 | 16.153 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `classic` | `strict_current` | 41.950 | 9.396 | 4.465 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.911 | 2.198 | 2.690 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 5.911 | 9.456 | 0.625 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 44.390 | 2.198 | 20.197 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 44.390 | 9.456 | 4.695 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.939 | 2.218 | 3.128 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `ax` | `strict_current` | 6.939 | 9.561 | 0.726 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 46.034 | 2.218 | 20.750 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `classic` | `strict_current` | 46.034 | 9.561 | 4.815 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.152 | 0.797 | 7.716 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `ax` | `strict_current` | 6.152 | 0.780 | 7.884 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.498 | 0.797 | 33.236 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `classic` | `strict_current` | 26.498 | 0.780 | 33.960 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.273 | 0.822 | 7.634 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `ax` | `strict_current` | 6.273 | 0.802 | 7.819 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.812 | 0.822 | 28.980 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `classic` | `strict_current` | 23.812 | 0.802 | 29.681 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.457 | 0.819 | 7.880 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `ax` | `strict_current` | 6.457 | 0.806 | 8.008 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.471 | 0.819 | 31.083 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `classic` | `strict_current` | 25.471 | 0.806 | 31.590 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 16.391 | 1.045 | 15.690 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `ax` | `strict_current` | 16.391 | 1.166 | 14.053 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 26.190 | 1.045 | 25.070 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `classic` | `strict_current` | 26.190 | 1.166 | 22.455 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.241 | 1.108 | 6.535 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `ax` | `strict_current` | 7.241 | 1.141 | 6.347 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.913 | 1.108 | 24.290 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `classic` | `strict_current` | 26.913 | 1.141 | 23.592 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.332 | 1.148 | 5.517 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `ax` | `strict_current` | 6.332 | 1.260 | 5.027 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.209 | 1.148 | 21.965 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `classic` | `strict_current` | 25.209 | 1.260 | 20.014 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 16.084 | 1.042 | 15.436 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `ax` | `strict_current` | 16.084 | 1.248 | 12.887 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.422 | 1.042 | 25.357 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `classic` | `strict_current` | 26.422 | 1.248 | 21.169 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.216 | 0.819 | 8.811 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.216 | 0.899 | 8.029 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.926 | 0.819 | 30.435 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.926 | 0.899 | 27.734 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.134 | 0.944 | 9.680 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `ax` | `strict_current` | 9.134 | 1.184 | 7.715 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.083 | 0.944 | 27.643 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `classic` | `strict_current` | 26.083 | 1.184 | 22.031 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.643 | 0.921 | 7.211 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `ax` | `strict_current` | 6.643 | 1.030 | 6.451 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.931 | 0.921 | 28.150 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `classic` | `strict_current` | 25.931 | 1.030 | 25.182 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.398 | 0.838 | 7.634 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `ax` | `strict_current` | 6.398 | 0.990 | 6.464 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.297 | 0.838 | 31.375 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `classic` | `strict_current` | 26.297 | 0.990 | 26.567 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.840 | 1.014 | 6.748 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.840 | 1.072 | 6.382 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 16.018 | 1.014 | 15.802 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `classic` | `strict_current` | 16.018 | 1.072 | 14.945 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.408 | 1.005 | 6.379 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `ax` | `strict_current` | 6.408 | 1.025 | 6.254 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.385 | 1.005 | 14.319 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `classic` | `strict_current` | 14.385 | 1.025 | 14.040 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.221 | 0.832 | 8.684 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `ax` | `strict_current` | 7.221 | 0.969 | 7.449 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.587 | 0.832 | 17.542 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `classic` | `strict_current` | 14.587 | 0.969 | 15.047 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.605 | 0.895 | 7.376 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `ax` | `strict_current` | 6.605 | 0.962 | 6.868 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.916 | 0.895 | 15.540 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `classic` | `strict_current` | 13.916 | 0.962 | 14.471 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 18.846 | 0.915 | 20.601 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `ax` | `strict_current` | 18.846 | 1.502 | 12.545 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 27.080 | 0.915 | 29.602 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `classic` | `strict_current` | 27.080 | 1.502 | 18.027 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.103 | 0.907 | 8.933 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `ax` | `strict_current` | 8.103 | 1.562 | 5.187 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.360 | 0.907 | 30.160 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `classic` | `strict_current` | 27.360 | 1.562 | 17.515 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 16.927 | 0.996 | 16.998 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `ax` | `strict_current` | 16.927 | 1.568 | 10.798 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 29.477 | 0.996 | 29.601 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `classic` | `strict_current` | 29.477 | 1.568 | 18.804 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 19.921 | 1.091 | 18.263 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `ax` | `strict_current` | 19.921 | 1.562 | 12.751 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 28.930 | 1.091 | 26.523 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `classic` | `strict_current` | 28.930 | 1.562 | 18.517 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 15.924 | 0.969 | 16.439 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `ax` | `strict_current` | 15.924 | 0.844 | 18.861 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 15.086 | 0.969 | 15.574 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `classic` | `strict_current` | 15.086 | 0.844 | 17.869 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.021 | 0.793 | 8.859 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `ax` | `strict_current` | 7.021 | 0.945 | 7.429 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.248 | 0.793 | 17.978 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `classic` | `strict_current` | 14.248 | 0.945 | 15.075 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 18.246 | 0.837 | 21.787 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `ax` | `strict_current` | 18.246 | 0.782 | 23.325 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 17.361 | 0.837 | 20.730 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `classic` | `strict_current` | 17.361 | 0.782 | 22.193 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.105 | 0.767 | 10.567 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `ax` | `strict_current` | 8.105 | 0.837 | 9.681 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.477 | 0.767 | 20.178 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `classic` | `strict_current` | 15.477 | 0.837 | 18.486 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.246 | 1.120 | 5.576 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.246 | 2.065 | 3.024 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.027 | 1.120 | 22.344 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.027 | 2.065 | 12.118 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.116 | 1.258 | 4.862 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `ax` | `strict_current` | 6.116 | 2.114 | 2.894 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.733 | 1.258 | 19.662 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `classic` | `strict_current` | 24.733 | 2.114 | 11.702 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.223 | 1.236 | 5.037 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `ax` | `strict_current` | 6.223 | 2.179 | 2.856 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.909 | 1.236 | 20.969 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `classic` | `strict_current` | 25.909 | 2.179 | 11.892 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.200 | 1.162 | 5.336 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `ax` | `strict_current` | 6.200 | 2.168 | 2.860 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.404 | 1.162 | 20.142 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `classic` | `strict_current` | 23.404 | 2.168 | 10.796 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.953 | 1.078 | 5.520 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `ax` | `strict_current` | 5.953 | 1.025 | 5.808 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 30.046 | 1.078 | 27.861 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `classic` | `strict_current` | 30.046 | 1.025 | 29.316 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.390 | 0.980 | 6.518 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `ax` | `strict_current` | 6.390 | 0.968 | 6.598 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.863 | 0.980 | 25.360 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `classic` | `strict_current` | 24.863 | 0.968 | 25.672 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.368 | 0.928 | 6.859 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `ax` | `strict_current` | 6.368 | 0.979 | 6.505 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.313 | 0.928 | 16.494 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `classic` | `strict_current` | 15.313 | 0.979 | 15.643 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.968 | 0.781 | 8.919 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `ax` | `strict_current` | 6.968 | 1.047 | 6.658 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.153 | 0.781 | 18.117 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `classic` | `strict_current` | 14.153 | 1.047 | 13.523 |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.843 | 0.765 | 8.944 |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `ax` | `strict_current` | 6.843 | 0.972 | 7.042 |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.214 | 0.765 | 19.888 |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `classic` | `strict_current` | 15.214 | 0.972 | 15.659 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.911 | 0.916 | 7.545 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.911 | 0.916 | 7.547 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 14.331 | 0.916 | 15.645 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `classic` | `strict_current` | 14.331 | 0.916 | 15.649 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.405 | 0.918 | 8.066 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `ax` | `strict_current` | 7.405 | 0.935 | 7.916 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.850 | 0.918 | 15.086 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `classic` | `strict_current` | 13.850 | 0.935 | 14.807 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.853 | 1.071 | 6.400 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `ax` | `strict_current` | 6.853 | 1.334 | 5.137 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.800 | 1.071 | 13.822 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `classic` | `strict_current` | 14.800 | 1.334 | 11.095 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.564 | 0.923 | 7.111 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `ax` | `strict_current` | 6.564 | 0.978 | 6.714 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.976 | 0.923 | 15.141 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `classic` | `strict_current` | 13.976 | 0.978 | 14.295 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.962 | 0.967 | 7.198 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.962 | 1.347 | 5.170 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.925 | 0.967 | 26.805 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.925 | 1.347 | 19.252 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.355 | 0.774 | 8.208 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `ax` | `strict_current` | 6.355 | 1.303 | 4.877 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.415 | 0.774 | 32.821 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `classic` | `strict_current` | 25.415 | 1.303 | 19.505 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.115 | 1.077 | 6.603 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `ax` | `strict_current` | 7.115 | 1.347 | 5.283 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.819 | 1.077 | 23.964 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `classic` | `strict_current` | 25.819 | 1.347 | 19.171 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.518 | 0.886 | 7.356 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `ax` | `strict_current` | 6.518 | 1.263 | 5.161 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.456 | 0.886 | 28.727 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `classic` | `strict_current` | 25.456 | 1.263 | 20.155 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.035 | 1.917 | 3.670 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.035 | 2.651 | 2.654 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 23.888 | 1.917 | 12.463 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 23.888 | 2.651 | 9.012 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.454 | 1.112 | 5.803 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `ax` | `strict_current` | 6.454 | 2.941 | 2.195 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.867 | 1.112 | 22.357 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `classic` | `strict_current` | 24.867 | 2.941 | 8.456 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.907 | 1.119 | 6.172 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 6.907 | 3.032 | 2.278 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.534 | 1.119 | 22.816 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 25.534 | 3.032 | 8.421 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.509 | 1.363 | 4.776 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `ax` | `strict_current` | 6.509 | 2.886 | 2.255 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.245 | 1.363 | 18.524 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `classic` | `strict_current` | 25.245 | 2.886 | 8.746 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.712 | 1.017 | 6.598 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.712 | 1.555 | 4.315 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 28.288 | 1.017 | 27.805 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `classic` | `strict_current` | 28.288 | 1.555 | 18.186 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.846 | 0.999 | 7.853 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `ax` | `strict_current` | 7.846 | 1.822 | 4.306 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.393 | 0.999 | 27.417 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `classic` | `strict_current` | 27.393 | 1.822 | 15.034 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.737 | 0.852 | 7.909 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `ax` | `strict_current` | 6.737 | 1.607 | 4.192 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.202 | 0.852 | 30.761 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `classic` | `strict_current` | 26.202 | 1.607 | 16.304 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.522 | 0.789 | 9.532 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `ax` | `strict_current` | 7.522 | 1.631 | 4.613 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.454 | 0.789 | 33.520 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `classic` | `strict_current` | 26.454 | 1.631 | 16.223 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 16.461 | 0.871 | 18.904 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `ax` | `strict_current` | 16.461 | 1.036 | 15.896 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 29.097 | 0.871 | 33.415 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `classic` | `strict_current` | 29.097 | 1.036 | 28.099 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.120 | 0.762 | 8.029 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `ax` | `strict_current` | 6.120 | 0.894 | 6.842 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.929 | 0.762 | 36.643 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `classic` | `strict_current` | 27.929 | 0.894 | 31.224 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.106 | 0.818 | 9.910 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `ax` | `strict_current` | 8.106 | 0.873 | 9.286 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.534 | 0.818 | 31.216 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `classic` | `strict_current` | 25.534 | 0.873 | 29.250 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 19.247 | 0.805 | 23.900 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `ax` | `strict_current` | 19.247 | 0.856 | 22.495 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.189 | 0.805 | 33.761 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `classic` | `strict_current` | 27.189 | 0.856 | 31.776 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.011 | 0.742 | 9.449 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.011 | 0.904 | 7.753 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.639 | 0.742 | 33.207 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.639 | 0.904 | 27.247 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.351 | 0.763 | 8.323 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `ax` | `strict_current` | 6.351 | 0.914 | 6.951 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.151 | 0.763 | 32.962 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `classic` | `strict_current` | 25.151 | 0.914 | 27.528 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.562 | 0.784 | 8.373 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 6.562 | 0.811 | 8.094 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.802 | 0.784 | 31.650 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 24.802 | 0.811 | 30.593 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.009 | 0.919 | 7.627 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `ax` | `strict_current` | 7.009 | 0.831 | 8.433 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.703 | 0.919 | 27.969 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `classic` | `strict_current` | 25.703 | 0.831 | 30.926 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 16.724 | 0.879 | 19.034 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `ax` | `strict_current` | 16.724 | 1.316 | 12.706 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 15.204 | 0.879 | 17.304 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `classic` | `strict_current` | 15.204 | 1.316 | 11.551 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 15.589 | 0.919 | 16.957 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `ax` | `strict_current` | 15.589 | 1.268 | 12.291 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.471 | 0.919 | 16.829 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `classic` | `strict_current` | 15.471 | 1.268 | 12.198 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.489 | 0.900 | 7.207 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `ax` | `strict_current` | 6.489 | 1.148 | 5.654 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.163 | 0.900 | 16.840 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `classic` | `strict_current` | 15.163 | 1.148 | 13.211 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.474 | 0.983 | 6.588 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `ax` | `strict_current` | 6.474 | 1.146 | 5.651 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.933 | 0.983 | 14.177 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `classic` | `strict_current` | 13.933 | 1.146 | 12.160 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.019 | 0.872 | 8.052 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.019 | 1.148 | 6.111 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 27.040 | 0.872 | 31.019 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `classic` | `strict_current` | 27.040 | 1.148 | 23.545 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.090 | 0.908 | 7.809 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `ax` | `strict_current` | 7.090 | 0.965 | 7.346 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.639 | 0.908 | 29.339 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `classic` | `strict_current` | 26.639 | 0.965 | 27.601 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.822 | 0.907 | 7.521 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `ax` | `strict_current` | 6.822 | 0.967 | 7.058 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.598 | 0.907 | 30.425 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `classic` | `strict_current` | 27.598 | 0.967 | 28.552 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.901 | 0.930 | 7.423 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `ax` | `strict_current` | 6.901 | 1.044 | 6.612 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.569 | 0.930 | 28.582 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `classic` | `strict_current` | 26.569 | 1.044 | 25.458 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.361 | 1.064 | 6.918 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.361 | 1.187 | 6.203 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.050 | 1.064 | 23.543 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.050 | 1.187 | 21.108 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.390 | 0.969 | 6.592 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `ax` | `strict_current` | 6.390 | 1.171 | 5.458 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.571 | 0.969 | 26.382 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `classic` | `strict_current` | 25.571 | 1.171 | 21.842 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.387 | 0.983 | 7.513 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `ax` | `strict_current` | 7.387 | 1.327 | 5.568 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 29.090 | 0.983 | 29.585 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `classic` | `strict_current` | 29.090 | 1.327 | 21.928 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.143 | 1.025 | 6.972 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `ax` | `strict_current` | 7.143 | 1.023 | 6.984 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.549 | 1.025 | 25.910 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `classic` | `strict_current` | 26.549 | 1.023 | 25.956 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 16.884 | 1.133 | 14.902 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `ax` | `strict_current` | 16.884 | 1.394 | 12.112 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 15.998 | 1.133 | 14.120 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `classic` | `strict_current` | 15.998 | 1.394 | 11.477 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.102 | 1.088 | 6.527 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `ax` | `strict_current` | 7.102 | 1.052 | 6.754 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.552 | 1.088 | 14.292 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `classic` | `strict_current` | 15.552 | 1.052 | 14.789 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.437 | 1.149 | 7.343 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `ax` | `strict_current` | 8.437 | 1.164 | 7.250 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 17.470 | 1.149 | 15.205 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `classic` | `strict_current` | 17.470 | 1.164 | 15.013 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 14.790 | 1.029 | 14.367 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `ax` | `strict_current` | 14.790 | 0.886 | 16.697 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.662 | 1.029 | 13.271 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `classic` | `strict_current` | 13.662 | 0.886 | 15.423 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.063 | 0.911 | 7.754 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.063 | 1.320 | 5.350 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 26.309 | 0.911 | 28.883 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `classic` | `strict_current` | 26.309 | 1.320 | 19.927 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.285 | 0.933 | 6.735 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `ax` | `strict_current` | 6.285 | 1.428 | 4.402 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.596 | 0.933 | 26.359 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `classic` | `strict_current` | 24.596 | 1.428 | 17.226 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.601 | 0.837 | 7.882 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `ax` | `strict_current` | 6.601 | 1.499 | 4.405 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.760 | 0.837 | 30.761 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `classic` | `strict_current` | 25.760 | 1.499 | 17.189 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.595 | 0.955 | 6.907 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `ax` | `strict_current` | 6.595 | 1.368 | 4.821 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.061 | 0.955 | 26.247 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `classic` | `strict_current` | 25.061 | 1.368 | 18.318 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.022 | 1.691 | 3.562 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.022 | 4.082 | 1.475 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.633 | 1.691 | 14.568 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.633 | 4.082 | 6.035 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.688 | 1.733 | 3.860 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `ax` | `strict_current` | 6.688 | 4.266 | 1.568 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.143 | 1.733 | 13.935 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `classic` | `strict_current` | 24.143 | 4.266 | 5.659 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.462 | 1.756 | 3.679 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `ax` | `strict_current` | 6.462 | 4.223 | 1.530 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.853 | 1.756 | 13.581 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `classic` | `strict_current` | 23.853 | 4.223 | 5.649 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.498 | 1.741 | 3.732 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `ax` | `strict_current` | 6.498 | 4.371 | 1.487 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.868 | 1.741 | 14.283 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `classic` | `strict_current` | 24.868 | 4.371 | 5.689 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 15.977 | 0.865 | 18.464 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `ax` | `strict_current` | 15.977 | 1.086 | 14.705 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 26.744 | 0.865 | 30.906 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `classic` | `strict_current` | 26.744 | 1.086 | 24.615 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 17.096 | 0.795 | 21.505 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `ax` | `strict_current` | 17.096 | 1.081 | 15.811 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.578 | 0.795 | 33.433 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `classic` | `strict_current` | 26.578 | 1.081 | 24.581 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.540 | 0.868 | 7.539 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `ax` | `strict_current` | 6.540 | 1.067 | 6.129 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.718 | 0.868 | 27.339 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `classic` | `strict_current` | 23.718 | 1.067 | 22.228 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.350 | 0.754 | 9.753 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `ax` | `strict_current` | 7.350 | 1.048 | 7.011 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.099 | 0.754 | 35.955 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `classic` | `strict_current` | 27.099 | 1.048 | 25.849 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.890 | 1.789 | 3.851 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.890 | 3.219 | 2.140 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.132 | 1.789 | 14.048 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.132 | 3.219 | 7.807 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.002 | 1.719 | 4.074 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `ax` | `strict_current` | 7.002 | 3.094 | 2.263 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.550 | 1.719 | 13.703 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `classic` | `strict_current` | 23.550 | 3.094 | 7.610 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.639 | 1.643 | 4.040 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `ax` | `strict_current` | 6.639 | 3.521 | 1.886 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.331 | 1.643 | 14.806 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `classic` | `strict_current` | 24.331 | 3.521 | 6.911 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.802 | 1.645 | 3.527 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `ax` | `strict_current` | 5.802 | 3.126 | 1.856 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.738 | 1.645 | 15.039 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `classic` | `strict_current` | 24.738 | 3.126 | 7.914 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.158 | 1.310 | 6.229 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `ax` | `strict_current` | 8.158 | 8.594 | 0.949 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 35.119 | 1.310 | 26.817 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `classic` | `strict_current` | 35.119 | 8.594 | 4.086 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.521 | 1.250 | 6.018 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `ax` | `strict_current` | 7.521 | 8.544 | 0.880 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 37.014 | 1.250 | 29.616 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `classic` | `strict_current` | 37.014 | 8.544 | 4.332 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.962 | 0.968 | 7.193 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `ax` | `strict_current` | 6.962 | 1.608 | 4.330 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.858 | 0.968 | 27.749 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `classic` | `strict_current` | 26.858 | 1.608 | 16.704 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.099 | 0.848 | 8.373 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `ax` | `strict_current` | 7.099 | 1.721 | 4.124 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.369 | 0.848 | 31.101 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `classic` | `strict_current` | 26.369 | 1.721 | 15.320 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.955 | 3.293 | 2.112 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `ax` | `strict_current` | 6.955 | 3.502 | 1.986 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.356 | 3.293 | 7.396 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `classic` | `strict_current` | 24.356 | 3.502 | 6.956 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.475 | 1.190 | 5.440 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `ax` | `strict_current` | 6.475 | 1.315 | 4.925 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.708 | 1.190 | 19.917 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `classic` | `strict_current` | 23.708 | 1.315 | 18.030 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.850 | 0.873 | 7.850 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `ax` | `strict_current` | 6.850 | 1.362 | 5.028 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.714 | 0.873 | 28.320 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `classic` | `strict_current` | 24.714 | 1.362 | 18.142 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.448 | 0.846 | 7.624 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `ax` | `strict_current` | 6.448 | 1.295 | 4.980 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.365 | 0.846 | 28.807 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `classic` | `strict_current` | 24.365 | 1.295 | 18.817 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.496 | 1.016 | 6.392 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `ax` | `strict_current` | 6.496 | 1.042 | 6.232 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.280 | 1.016 | 26.844 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `classic` | `strict_current` | 27.280 | 1.042 | 26.171 |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.942 | 0.801 | 8.664 |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `ax` | `strict_current` | 6.942 | 0.925 | 7.505 |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.374 | 0.801 | 32.917 |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `classic` | `strict_current` | 26.374 | 0.925 | 28.515 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.267 | 0.997 | 7.285 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `ax` | `strict_current` | 7.267 | 1.647 | 4.411 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 28.767 | 0.997 | 28.841 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `classic` | `strict_current` | 28.767 | 1.647 | 17.462 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.514 | 0.866 | 7.523 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `ax` | `strict_current` | 6.514 | 1.949 | 3.342 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.166 | 0.866 | 31.373 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `classic` | `strict_current` | 27.166 | 1.949 | 13.938 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.456 | 1.455 | 6.498 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `ax` | `strict_current` | 9.456 | 1.559 | 6.065 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 29.656 | 1.455 | 20.379 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `classic` | `strict_current` | 29.656 | 1.559 | 19.020 |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.744 | 0.810 | 8.331 |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `ax` | `strict_current` | 6.744 | 1.090 | 6.186 |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.230 | 0.810 | 32.400 |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `classic` | `strict_current` | 26.230 | 1.090 | 24.058 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.686 | 11.820 | 0.650 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `ax` | `strict_current` | 7.686 | 12.165 | 0.632 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 43.483 | 11.820 | 3.679 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `classic` | `strict_current` | 43.483 | 12.165 | 3.574 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.855 | 2.669 | 2.569 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `ax` | `strict_current` | 6.855 | 2.883 | 2.378 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 42.333 | 2.669 | 15.863 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `classic` | `strict_current` | 42.333 | 2.883 | 14.685 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.677 | 1.745 | 3.827 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `ax` | `strict_current` | 6.677 | 2.540 | 2.629 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.770 | 1.745 | 15.917 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `classic` | `strict_current` | 27.770 | 2.540 | 10.932 |
| `vbr1_l2_event_controller` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.509 | 0.862 | 8.711 |
| `vbr1_l2_event_controller` | `tb` | `gold` | `ax` | `strict_current` | 7.509 | 1.943 | 3.864 |
| `vbr1_l2_event_controller` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 29.674 | 0.862 | 34.426 |
| `vbr1_l2_event_controller` | `tb` | `gold` | `classic` | `strict_current` | 29.674 | 1.943 | 15.271 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.202 | 1.088 | 6.622 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `ax` | `strict_current` | 7.202 | 1.753 | 4.110 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.590 | 1.088 | 25.365 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `classic` | `strict_current` | 27.590 | 1.753 | 15.743 |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.510 | 0.826 | 7.883 |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `ax` | `strict_current` | 6.510 | 1.446 | 4.502 |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.217 | 0.826 | 32.960 |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `classic` | `strict_current` | 27.217 | 1.446 | 18.824 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 11.087 | 10.054 | 1.103 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `ax` | `strict_current` | 11.087 | 127.027 | 0.087 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 52.028 | 10.054 | 5.175 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `classic` | `strict_current` | 52.028 | 127.027 | 0.410 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.653 | 9.529 | 1.118 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `ax` | `strict_current` | 10.653 | 130.392 | 0.082 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 54.184 | 9.529 | 5.686 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `classic` | `strict_current` | 54.184 | 130.392 | 0.416 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.531 | 1.681 | 3.886 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `ax` | `strict_current` | 6.531 | 2.449 | 2.666 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 28.275 | 1.681 | 16.824 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `classic` | `strict_current` | 28.275 | 2.449 | 11.544 |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.822 | 1.335 | 7.357 |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `ax` | `strict_current` | 9.822 | 1.961 | 5.007 |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.876 | 1.335 | 20.881 |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `classic` | `strict_current` | 27.876 | 1.961 | 14.212 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.599 | 10.330 | 0.736 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `ax` | `strict_current` | 7.599 | 10.366 | 0.733 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.997 | 10.330 | 2.517 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `classic` | `strict_current` | 25.997 | 10.366 | 2.508 |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.050 | 2.331 | 2.595 |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `ax` | `strict_current` | 6.050 | 2.642 | 2.290 |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.967 | 2.331 | 11.139 |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `classic` | `strict_current` | 25.967 | 2.642 | 9.830 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.733 | 1.323 | 5.088 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `ax` | `strict_current` | 6.733 | 2.116 | 3.183 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.099 | 1.323 | 18.966 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `classic` | `strict_current` | 25.099 | 2.116 | 11.864 |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.812 | 0.824 | 8.264 |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `ax` | `strict_current` | 6.812 | 1.687 | 4.038 |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.957 | 0.824 | 29.063 |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `classic` | `strict_current` | 23.957 | 1.687 | 14.203 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.928 | 1.380 | 4.294 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `ax` | `strict_current` | 5.928 | 16.312 | 0.363 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 48.880 | 1.380 | 35.410 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `classic` | `strict_current` | 48.880 | 16.312 | 2.997 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.527 | 1.268 | 5.148 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `ax` | `strict_current` | 6.527 | 16.783 | 0.389 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 44.106 | 1.268 | 34.785 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `classic` | `strict_current` | 44.106 | 16.783 | 2.628 |

## Accuracy-Gated Speedups

| Entry | Form | Variant | Spectre mode | EVAS mode | Spectre wall s | EVAS wall s | Spectre/EVAS |
| --- | --- | --- | --- | --- | ---: | ---: | ---: |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.007 | 1.117 | 6.271 |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.007 | 1.401 | 5.001 |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 26.454 | 1.117 | 23.677 |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `classic` | `strict_current` | 26.454 | 1.401 | 18.881 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.322 | 1.148 | 5.506 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `ax` | `strict_current` | 6.322 | 1.538 | 4.111 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.615 | 1.148 | 24.048 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `classic` | `strict_current` | 27.615 | 1.538 | 17.957 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.253 | 1.187 | 5.267 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `ax` | `strict_current` | 6.253 | 1.298 | 4.818 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.230 | 1.187 | 22.096 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `classic` | `strict_current` | 26.230 | 1.298 | 20.213 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.050 | 1.335 | 6.029 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `ax` | `strict_current` | 8.050 | 1.606 | 5.013 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.560 | 1.335 | 20.640 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `classic` | `strict_current` | 27.560 | 1.606 | 17.162 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.911 | 1.423 | 4.856 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `ax` | `strict_current` | 6.911 | 10.843 | 0.637 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.513 | 1.423 | 16.521 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `classic` | `strict_current` | 23.513 | 10.843 | 2.169 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.623 | 1.601 | 4.137 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `ax` | `strict_current` | 6.623 | 1.949 | 3.398 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.163 | 1.601 | 16.965 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `classic` | `strict_current` | 27.163 | 1.949 | 13.936 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 16.788 | 0.834 | 20.123 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `ax` | `strict_current` | 16.788 | 0.828 | 20.285 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 26.696 | 0.834 | 32.000 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `classic` | `strict_current` | 26.696 | 0.828 | 32.256 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 17.887 | 0.836 | 21.406 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `ax` | `strict_current` | 17.887 | 0.859 | 20.815 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.203 | 0.836 | 32.555 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `classic` | `strict_current` | 27.203 | 0.859 | 31.656 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 18.302 | 1.130 | 16.203 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `ax` | `strict_current` | 18.302 | 0.955 | 19.164 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 29.494 | 1.130 | 26.111 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `classic` | `strict_current` | 29.494 | 0.955 | 30.883 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.338 | 0.809 | 7.830 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `ax` | `strict_current` | 6.338 | 0.946 | 6.697 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.210 | 0.809 | 32.383 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `classic` | `strict_current` | 26.210 | 0.946 | 27.695 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.822 | 0.936 | 7.289 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `ax` | `strict_current` | 6.822 | 1.520 | 4.488 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.140 | 0.936 | 27.932 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `classic` | `strict_current` | 26.140 | 1.520 | 17.197 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.976 | 0.994 | 7.019 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `ax` | `strict_current` | 6.976 | 1.486 | 4.694 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.639 | 0.994 | 25.798 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `classic` | `strict_current` | 25.639 | 1.486 | 17.254 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.938 | 0.963 | 7.202 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `ax` | `strict_current` | 6.938 | 1.333 | 5.205 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.565 | 0.963 | 26.537 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `classic` | `strict_current` | 25.565 | 1.333 | 19.177 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.258 | 0.951 | 7.636 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.258 | 1.681 | 4.319 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 27.215 | 0.951 | 28.632 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `classic` | `strict_current` | 27.215 | 1.681 | 16.195 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.804 | 0.920 | 7.395 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `ax` | `strict_current` | 6.804 | 1.639 | 4.150 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.983 | 0.920 | 29.328 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `classic` | `strict_current` | 26.983 | 1.639 | 16.460 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.067 | 0.883 | 8.002 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `ax` | `strict_current` | 7.067 | 1.621 | 4.361 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.787 | 0.883 | 29.197 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `classic` | `strict_current` | 25.787 | 1.621 | 15.912 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.351 | 0.914 | 8.043 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `ax` | `strict_current` | 7.351 | 1.620 | 4.538 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.842 | 0.914 | 29.369 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `classic` | `strict_current` | 26.842 | 1.620 | 16.571 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.762 | 1.692 | 3.406 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `ax` | `strict_current` | 5.762 | 3.592 | 1.604 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.838 | 1.692 | 14.680 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `classic` | `strict_current` | 24.838 | 3.592 | 6.916 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.742 | 1.118 | 6.031 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.742 | 1.755 | 3.841 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 26.965 | 1.118 | 24.124 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `classic` | `strict_current` | 26.965 | 1.755 | 15.361 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.180 | 0.880 | 8.159 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `ax` | `strict_current` | 7.180 | 1.552 | 4.627 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.324 | 0.880 | 31.048 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `classic` | `strict_current` | 27.324 | 1.552 | 17.607 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.625 | 0.880 | 7.528 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `ax` | `strict_current` | 6.625 | 1.617 | 4.097 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.876 | 0.880 | 31.673 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `classic` | `strict_current` | 27.876 | 1.617 | 17.237 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.747 | 0.916 | 7.366 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `ax` | `strict_current` | 6.747 | 1.698 | 3.974 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.127 | 0.916 | 29.619 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `classic` | `strict_current` | 27.127 | 1.698 | 15.980 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.460 | 1.416 | 4.563 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `ax` | `strict_current` | 6.460 | 3.983 | 1.622 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.177 | 1.416 | 16.371 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `classic` | `strict_current` | 23.177 | 3.983 | 5.819 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.060 | 1.277 | 4.745 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `ax` | `strict_current` | 6.060 | 3.989 | 1.519 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.830 | 1.277 | 18.658 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `classic` | `strict_current` | 23.830 | 3.989 | 5.975 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.595 | 1.383 | 4.045 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `ax` | `strict_current` | 5.595 | 3.905 | 1.433 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.303 | 1.383 | 17.572 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `classic` | `strict_current` | 24.303 | 3.905 | 6.223 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.809 | 0.943 | 7.219 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.809 | 1.711 | 3.980 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 26.268 | 0.943 | 27.852 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `classic` | `strict_current` | 26.268 | 1.711 | 15.355 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.250 | 1.103 | 6.576 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `ax` | `strict_current` | 7.250 | 1.668 | 4.345 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.130 | 1.103 | 23.701 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `classic` | `strict_current` | 26.130 | 1.668 | 15.661 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.275 | 1.033 | 7.042 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `ax` | `strict_current` | 7.275 | 1.702 | 4.274 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.190 | 1.033 | 26.316 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `classic` | `strict_current` | 27.190 | 1.702 | 15.973 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.467 | 0.983 | 6.581 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `ax` | `strict_current` | 6.467 | 1.686 | 3.836 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.193 | 0.983 | 26.654 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `classic` | `strict_current` | 26.193 | 1.686 | 15.537 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 5.906 | 1.212 | 4.872 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 5.906 | 3.135 | 1.884 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.064 | 1.212 | 19.850 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.064 | 3.135 | 7.675 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.318 | 1.167 | 5.412 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `ax` | `strict_current` | 6.318 | 3.229 | 1.957 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.615 | 1.167 | 21.084 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `classic` | `strict_current` | 24.615 | 3.229 | 7.624 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.637 | 1.267 | 5.240 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 6.637 | 3.294 | 2.015 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.405 | 1.267 | 19.268 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 24.405 | 3.294 | 7.410 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.295 | 1.268 | 4.963 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `ax` | `strict_current` | 6.295 | 3.236 | 1.945 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.132 | 1.268 | 19.027 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `classic` | `strict_current` | 24.132 | 3.236 | 7.456 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.181 | 0.983 | 7.304 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.181 | 1.701 | 4.222 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 15.575 | 0.983 | 15.840 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `classic` | `strict_current` | 15.575 | 1.701 | 9.156 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.346 | 0.920 | 7.988 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `ax` | `strict_current` | 7.346 | 1.649 | 4.455 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.628 | 0.920 | 15.906 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `classic` | `strict_current` | 14.628 | 1.649 | 8.872 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.586 | 1.131 | 7.589 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `ax` | `strict_current` | 8.586 | 1.660 | 5.171 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 16.137 | 1.131 | 14.263 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `classic` | `strict_current` | 16.137 | 1.660 | 9.718 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.529 | 0.948 | 7.945 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `ax` | `strict_current` | 7.529 | 1.631 | 4.615 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 16.279 | 0.948 | 17.179 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `classic` | `strict_current` | 16.279 | 1.631 | 9.979 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.989 | 0.960 | 8.323 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `ax` | `strict_current` | 7.989 | 0.985 | 8.112 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 16.366 | 0.960 | 17.051 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `classic` | `strict_current` | 16.366 | 0.985 | 16.618 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.187 | 0.812 | 7.620 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `ax` | `strict_current` | 6.187 | 0.925 | 6.688 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.248 | 0.812 | 18.779 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `classic` | `strict_current` | 15.248 | 0.925 | 16.484 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.745 | 1.407 | 5.503 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `ax` | `strict_current` | 7.745 | 0.813 | 9.521 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.818 | 1.407 | 11.239 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `classic` | `strict_current` | 15.818 | 0.813 | 19.445 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.468 | 0.755 | 8.563 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.468 | 0.990 | 6.535 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.788 | 0.755 | 32.817 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.788 | 0.990 | 25.044 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.593 | 0.760 | 8.676 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `ax` | `strict_current` | 6.593 | 0.835 | 7.898 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.449 | 0.760 | 33.486 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `classic` | `strict_current` | 25.449 | 0.835 | 30.486 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.536 | 0.759 | 9.925 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `ax` | `strict_current` | 7.536 | 0.952 | 7.920 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.539 | 0.759 | 33.635 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `classic` | `strict_current` | 25.539 | 0.952 | 26.840 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.483 | 0.709 | 9.141 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `ax` | `strict_current` | 6.483 | 0.865 | 7.496 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.622 | 0.709 | 34.719 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `classic` | `strict_current` | 24.622 | 0.865 | 28.472 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 18.678 | 0.806 | 23.177 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `ax` | `strict_current` | 18.678 | 0.930 | 20.088 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 28.850 | 0.806 | 35.798 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `classic` | `strict_current` | 28.850 | 0.930 | 31.028 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.828 | 0.868 | 9.018 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `ax` | `strict_current` | 7.828 | 1.100 | 7.118 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 28.529 | 0.868 | 32.863 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `classic` | `strict_current` | 28.529 | 1.100 | 25.940 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.237 | 0.788 | 7.911 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `ax` | `strict_current` | 6.237 | 0.859 | 7.265 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.194 | 0.788 | 31.955 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `classic` | `strict_current` | 25.194 | 0.859 | 29.345 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 15.322 | 0.757 | 20.241 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `ax` | `strict_current` | 15.322 | 0.938 | 16.337 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.420 | 0.757 | 33.581 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `classic` | `strict_current` | 25.420 | 0.938 | 27.105 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.250 | 1.061 | 5.892 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.250 | 5.033 | 1.242 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 26.107 | 1.061 | 24.613 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `classic` | `strict_current` | 26.107 | 5.033 | 5.187 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.002 | 1.051 | 6.660 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `ax` | `strict_current` | 7.002 | 4.809 | 1.456 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.527 | 1.051 | 25.231 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `classic` | `strict_current` | 26.527 | 4.809 | 5.516 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.684 | 1.112 | 6.013 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `ax` | `strict_current` | 6.684 | 4.631 | 1.443 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.305 | 1.112 | 23.664 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `classic` | `strict_current` | 26.305 | 4.631 | 5.680 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.445 | 1.012 | 7.359 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `ax` | `strict_current` | 7.445 | 4.749 | 1.568 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.580 | 1.012 | 25.283 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `classic` | `strict_current` | 25.580 | 4.749 | 5.386 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.071 | 1.608 | 4.398 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.071 | 1.746 | 4.051 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.558 | 1.608 | 15.897 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.558 | 1.746 | 14.641 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.604 | 1.676 | 3.940 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `ax` | `strict_current` | 6.604 | 1.644 | 4.018 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.330 | 1.676 | 15.709 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `classic` | `strict_current` | 26.330 | 1.644 | 16.018 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.141 | 1.596 | 4.474 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `ax` | `strict_current` | 7.141 | 1.800 | 3.968 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.214 | 1.596 | 17.049 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `classic` | `strict_current` | 27.214 | 1.800 | 15.120 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.172 | 1.673 | 4.883 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `ax` | `strict_current` | 8.172 | 1.695 | 4.820 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.052 | 1.673 | 16.165 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `classic` | `strict_current` | 27.052 | 1.695 | 15.956 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.295 | 0.890 | 7.077 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `ax` | `strict_current` | 6.295 | 0.859 | 7.328 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 10.739 | 0.890 | 12.073 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `classic` | `strict_current` | 10.739 | 0.859 | 12.501 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.848 | 0.771 | 8.879 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `ax` | `strict_current` | 6.848 | 0.816 | 8.393 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.736 | 0.771 | 19.104 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `classic` | `strict_current` | 14.736 | 0.816 | 18.058 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.846 | 0.805 | 8.500 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `ax` | `strict_current` | 6.846 | 1.216 | 5.628 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.598 | 0.805 | 16.883 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `classic` | `strict_current` | 13.598 | 1.216 | 11.179 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 8.348 | 0.966 | 8.640 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `ax` | `strict_current` | 8.348 | 2.621 | 3.184 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 46.983 | 0.966 | 48.630 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `classic` | `strict_current` | 46.983 | 2.621 | 17.922 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.279 | 0.904 | 8.050 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `ax` | `strict_current` | 7.279 | 2.597 | 2.803 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 51.115 | 0.904 | 56.530 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `classic` | `strict_current` | 51.115 | 2.597 | 19.685 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.772 | 0.981 | 7.925 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `ax` | `strict_current` | 7.772 | 2.745 | 2.832 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 47.818 | 0.981 | 48.758 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `classic` | `strict_current` | 47.818 | 2.745 | 17.422 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.413 | 0.908 | 8.167 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `ax` | `strict_current` | 7.413 | 2.611 | 2.839 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 49.044 | 0.908 | 54.033 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `classic` | `strict_current` | 49.044 | 2.611 | 18.783 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 16.736 | 0.806 | 20.767 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 16.736 | 0.978 | 17.109 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 27.335 | 0.806 | 33.919 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 27.335 | 0.978 | 27.945 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.455 | 1.384 | 5.386 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `ax` | `strict_current` | 7.455 | 0.970 | 7.683 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 30.103 | 1.384 | 21.749 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `classic` | `strict_current` | 30.103 | 0.970 | 31.024 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.308 | 0.833 | 7.574 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `ax` | `strict_current` | 6.308 | 1.008 | 6.255 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.593 | 0.833 | 30.733 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `classic` | `strict_current` | 25.593 | 1.008 | 25.379 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 16.375 | 0.831 | 19.716 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `ax` | `strict_current` | 16.375 | 0.963 | 16.997 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 28.228 | 0.831 | 33.987 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `classic` | `strict_current` | 28.228 | 0.963 | 29.300 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.211 | 1.340 | 5.383 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `ax` | `strict_current` | 7.211 | 4.563 | 1.580 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.345 | 1.340 | 18.173 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `classic` | `strict_current` | 24.345 | 4.563 | 5.335 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 5.965 | 0.773 | 7.715 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `ax` | `strict_current` | 5.965 | 0.947 | 6.298 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.632 | 0.773 | 33.149 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.632 | 0.947 | 27.064 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.936 | 1.006 | 7.893 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `ax` | `strict_current` | 7.936 | 1.050 | 7.556 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.090 | 1.006 | 25.947 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `classic` | `strict_current` | 26.090 | 1.050 | 24.839 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.676 | 0.801 | 8.336 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `ax` | `strict_current` | 6.676 | 0.953 | 7.008 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.697 | 0.801 | 33.335 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `classic` | `strict_current` | 26.697 | 0.953 | 28.025 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.518 | 0.919 | 7.091 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `ax` | `strict_current` | 6.518 | 0.977 | 6.669 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.164 | 0.919 | 27.377 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `classic` | `strict_current` | 25.164 | 0.977 | 25.747 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.742 | 0.854 | 7.897 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.742 | 0.944 | 7.144 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 26.104 | 0.854 | 30.576 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `classic` | `strict_current` | 26.104 | 0.944 | 27.658 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.591 | 0.685 | 9.625 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `ax` | `strict_current` | 6.591 | 1.034 | 6.375 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.907 | 0.685 | 37.836 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `classic` | `strict_current` | 25.907 | 1.034 | 25.059 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.079 | 0.743 | 9.530 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `ax` | `strict_current` | 7.079 | 0.985 | 7.184 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.669 | 0.743 | 34.555 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `classic` | `strict_current` | 25.669 | 0.985 | 26.049 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.708 | 0.697 | 9.628 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `ax` | `strict_current` | 6.708 | 0.878 | 7.638 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.312 | 0.697 | 36.331 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `classic` | `strict_current` | 25.312 | 0.878 | 28.823 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 16.024 | 1.198 | 13.370 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `ax` | `strict_current` | 16.024 | 1.447 | 11.077 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 15.147 | 1.198 | 12.638 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `classic` | `strict_current` | 15.147 | 1.447 | 10.471 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.796 | 1.094 | 6.214 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `ax` | `strict_current` | 6.796 | 1.034 | 6.574 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.126 | 1.094 | 12.916 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `classic` | `strict_current` | 14.126 | 1.034 | 13.664 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 16.699 | 1.267 | 13.180 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `ax` | `strict_current` | 16.699 | 1.105 | 15.117 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 16.051 | 1.267 | 12.668 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `classic` | `strict_current` | 16.051 | 1.105 | 14.530 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.470 | 1.069 | 6.050 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `ax` | `strict_current` | 6.470 | 1.172 | 5.519 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.178 | 1.069 | 13.259 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `classic` | `strict_current` | 14.178 | 1.172 | 12.094 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 10.422 | 9.539 | 1.093 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `ax` | `strict_current` | 10.422 | 129.793 | 0.080 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 54.507 | 9.539 | 5.714 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `classic` | `strict_current` | 54.507 | 129.793 | 0.420 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 15.339 | 1.303 | 11.768 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `ax` | `strict_current` | 15.339 | 1.765 | 8.689 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 13.844 | 1.303 | 10.621 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `classic` | `strict_current` | 13.844 | 1.765 | 7.842 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 15.695 | 1.192 | 13.162 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `ax` | `strict_current` | 15.695 | 1.615 | 9.721 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.417 | 1.192 | 12.929 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `classic` | `strict_current` | 15.417 | 1.615 | 9.549 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.648 | 1.119 | 6.834 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `ax` | `strict_current` | 7.648 | 1.866 | 4.099 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.640 | 1.119 | 13.975 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `classic` | `strict_current` | 15.640 | 1.866 | 8.382 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.974 | 1.141 | 6.990 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `ax` | `strict_current` | 7.974 | 1.650 | 4.834 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.540 | 1.141 | 13.623 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `classic` | `strict_current` | 15.540 | 1.650 | 9.421 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 8.022 | 0.937 | 8.562 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `ax` | `strict_current` | 8.022 | 1.441 | 5.569 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.970 | 0.937 | 27.716 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.970 | 1.441 | 18.027 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.588 | 0.793 | 8.308 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `ax` | `strict_current` | 6.588 | 1.237 | 5.324 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.293 | 0.793 | 31.896 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `classic` | `strict_current` | 25.293 | 1.237 | 20.441 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.071 | 0.896 | 7.892 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `ax` | `strict_current` | 7.071 | 1.224 | 5.778 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.396 | 0.896 | 28.344 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `classic` | `strict_current` | 25.396 | 1.224 | 20.753 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.384 | 0.811 | 7.874 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `ax` | `strict_current` | 6.384 | 1.323 | 4.827 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.923 | 0.811 | 31.971 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `classic` | `strict_current` | 25.923 | 1.323 | 19.598 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.080 | 1.122 | 6.308 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.080 | 1.354 | 5.230 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.591 | 1.122 | 22.799 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.591 | 1.354 | 18.903 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.362 | 0.958 | 6.641 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `ax` | `strict_current` | 6.362 | 0.998 | 6.376 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.482 | 0.958 | 28.684 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `classic` | `strict_current` | 27.482 | 0.998 | 27.540 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.053 | 1.110 | 6.352 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 7.053 | 1.075 | 6.559 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.297 | 1.110 | 23.683 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 26.297 | 1.075 | 24.453 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.187 | 0.953 | 6.494 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `ax` | `strict_current` | 6.187 | 1.022 | 6.056 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.098 | 0.953 | 28.443 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `classic` | `strict_current` | 27.098 | 1.022 | 26.522 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.576 | 1.780 | 3.694 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `ax` | `strict_current` | 6.576 | 4.675 | 1.407 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.871 | 1.780 | 13.411 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `classic` | `strict_current` | 23.871 | 4.675 | 5.106 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.371 | 1.595 | 3.996 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `ax` | `strict_current` | 6.371 | 2.820 | 2.260 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.778 | 1.595 | 15.539 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `classic` | `strict_current` | 24.778 | 2.820 | 8.787 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 16.716 | 1.080 | 15.481 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 16.716 | 1.220 | 13.700 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 26.078 | 1.080 | 24.153 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 26.078 | 1.220 | 21.374 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.462 | 0.775 | 8.334 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `ax` | `strict_current` | 6.462 | 1.156 | 5.588 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.627 | 0.775 | 33.047 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `classic` | `strict_current` | 25.627 | 1.156 | 22.159 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 18.881 | 1.163 | 16.240 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `ax` | `strict_current` | 18.881 | 1.021 | 18.491 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 29.484 | 1.163 | 25.359 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `classic` | `strict_current` | 29.484 | 1.021 | 28.876 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.863 | 0.897 | 7.648 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `ax` | `strict_current` | 6.863 | 1.078 | 6.364 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.448 | 0.897 | 28.357 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `classic` | `strict_current` | 25.448 | 1.078 | 23.596 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.626 | 0.817 | 8.115 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.626 | 1.756 | 3.774 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 26.710 | 0.817 | 32.712 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `classic` | `strict_current` | 26.710 | 1.756 | 15.211 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.915 | 0.872 | 7.934 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `ax` | `strict_current` | 6.915 | 1.576 | 4.387 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.229 | 0.872 | 30.095 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `classic` | `strict_current` | 26.229 | 1.576 | 16.641 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.578 | 0.883 | 8.585 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `ax` | `strict_current` | 7.578 | 1.609 | 4.709 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.925 | 0.883 | 31.635 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `classic` | `strict_current` | 27.925 | 1.609 | 17.353 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.312 | 1.008 | 7.257 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `ax` | `strict_current` | 7.312 | 1.707 | 4.285 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.731 | 1.008 | 26.528 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `classic` | `strict_current` | 26.731 | 1.707 | 15.663 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 16.444 | 1.078 | 15.251 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 16.444 | 1.513 | 10.868 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 15.591 | 1.078 | 14.459 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 15.591 | 1.513 | 10.304 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 16.941 | 1.108 | 15.291 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `ax` | `strict_current` | 16.941 | 1.413 | 11.989 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.334 | 1.108 | 13.841 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `classic` | `strict_current` | 15.334 | 1.413 | 10.852 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.673 | 1.394 | 4.788 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 6.673 | 1.366 | 4.883 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.485 | 1.394 | 10.394 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 14.485 | 1.366 | 10.601 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.554 | 1.118 | 5.864 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `ax` | `strict_current` | 6.554 | 1.356 | 4.835 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.087 | 1.118 | 13.498 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `classic` | `strict_current` | 15.087 | 1.356 | 11.130 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.595 | 0.908 | 7.262 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.595 | 1.176 | 5.610 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.521 | 0.908 | 27.002 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.521 | 1.176 | 20.857 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.537 | 0.899 | 7.274 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `ax` | `strict_current` | 6.537 | 1.072 | 6.096 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.261 | 0.899 | 30.337 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `classic` | `strict_current` | 27.261 | 1.072 | 25.423 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.303 | 0.947 | 6.653 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `ax` | `strict_current` | 6.303 | 1.032 | 6.108 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.679 | 0.947 | 27.103 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `classic` | `strict_current` | 25.679 | 1.032 | 24.885 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.810 | 0.852 | 6.818 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `ax` | `strict_current` | 5.810 | 0.958 | 6.063 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.300 | 0.852 | 29.689 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `classic` | `strict_current` | 25.300 | 0.958 | 26.402 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.072 | 0.879 | 8.043 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.072 | 0.996 | 7.104 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 14.939 | 0.879 | 16.989 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 14.939 | 0.996 | 15.005 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.409 | 0.858 | 7.473 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `ax` | `strict_current` | 6.409 | 1.049 | 6.110 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.307 | 0.858 | 16.682 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `classic` | `strict_current` | 14.307 | 1.049 | 13.639 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.721 | 0.878 | 7.657 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `ax` | `strict_current` | 6.721 | 1.297 | 5.184 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.619 | 0.878 | 16.653 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `classic` | `strict_current` | 14.619 | 1.297 | 11.275 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.916 | 0.833 | 8.302 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `ax` | `strict_current` | 6.916 | 1.105 | 6.258 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 16.138 | 0.833 | 19.372 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `classic` | `strict_current` | 16.138 | 1.105 | 14.603 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 4.845 | 15.953 | 0.304 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `ax` | `strict_current` | 4.845 | 33.966 | 0.143 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 18.539 | 15.953 | 1.162 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `classic` | `strict_current` | 18.539 | 33.966 | 0.546 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 4.417 | 16.232 | 0.272 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `ax` | `strict_current` | 4.417 | 32.917 | 0.134 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 17.049 | 16.232 | 1.050 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `classic` | `strict_current` | 17.049 | 32.917 | 0.518 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 4.870 | 15.971 | 0.305 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `ax` | `strict_current` | 4.870 | 33.013 | 0.148 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 17.278 | 15.971 | 1.082 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `classic` | `strict_current` | 17.278 | 33.013 | 0.523 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.060 | 16.088 | 0.315 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `ax` | `strict_current` | 5.060 | 33.650 | 0.150 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 17.501 | 16.088 | 1.088 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `classic` | `strict_current` | 17.501 | 33.650 | 0.520 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 11.343 | 8.983 | 1.263 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `ax` | `strict_current` | 11.343 | 69.545 | 0.163 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 17.558 | 8.983 | 1.955 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `classic` | `strict_current` | 17.558 | 69.545 | 0.252 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 4.129 | 8.749 | 0.472 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `ax` | `strict_current` | 4.129 | 68.112 | 0.061 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 16.521 | 8.749 | 1.888 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `classic` | `strict_current` | 16.521 | 68.112 | 0.243 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 4.052 | 8.847 | 0.458 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `ax` | `strict_current` | 4.052 | 69.966 | 0.058 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.705 | 8.847 | 1.775 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `classic` | `strict_current` | 15.705 | 69.966 | 0.224 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 11.052 | 8.576 | 1.289 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `ax` | `strict_current` | 11.052 | 66.564 | 0.166 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 17.496 | 8.576 | 2.040 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `classic` | `strict_current` | 17.496 | 66.564 | 0.263 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 8.029 | 0.880 | 9.120 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `ax` | `strict_current` | 8.029 | 1.407 | 5.705 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 14.771 | 0.880 | 16.777 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `classic` | `strict_current` | 14.771 | 1.407 | 10.495 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.286 | 0.836 | 7.523 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `ax` | `strict_current` | 6.286 | 1.182 | 5.320 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.754 | 0.836 | 16.459 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `classic` | `strict_current` | 13.754 | 1.182 | 11.641 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.592 | 0.779 | 8.466 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `ax` | `strict_current` | 6.592 | 1.150 | 5.734 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.757 | 0.779 | 18.951 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `classic` | `strict_current` | 14.757 | 1.150 | 12.836 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.856 | 0.845 | 8.117 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `ax` | `strict_current` | 6.856 | 1.106 | 6.201 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.187 | 0.845 | 17.979 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `classic` | `strict_current` | 15.187 | 1.106 | 13.735 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.015 | 3.222 | 2.177 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.015 | 9.279 | 0.756 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 43.607 | 3.222 | 13.532 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 43.607 | 9.279 | 4.700 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.544 | 2.597 | 2.905 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `ax` | `strict_current` | 7.544 | 9.396 | 0.803 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 41.950 | 2.597 | 16.153 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `classic` | `strict_current` | 41.950 | 9.396 | 4.465 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.911 | 2.198 | 2.690 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 5.911 | 9.456 | 0.625 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 44.390 | 2.198 | 20.197 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 44.390 | 9.456 | 4.695 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.939 | 2.218 | 3.128 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `ax` | `strict_current` | 6.939 | 9.561 | 0.726 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 46.034 | 2.218 | 20.750 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `classic` | `strict_current` | 46.034 | 9.561 | 4.815 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.152 | 0.797 | 7.716 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `ax` | `strict_current` | 6.152 | 0.780 | 7.884 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.498 | 0.797 | 33.236 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `classic` | `strict_current` | 26.498 | 0.780 | 33.960 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.273 | 0.822 | 7.634 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `ax` | `strict_current` | 6.273 | 0.802 | 7.819 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.812 | 0.822 | 28.980 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `classic` | `strict_current` | 23.812 | 0.802 | 29.681 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.457 | 0.819 | 7.880 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `ax` | `strict_current` | 6.457 | 0.806 | 8.008 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.471 | 0.819 | 31.083 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `classic` | `strict_current` | 25.471 | 0.806 | 31.590 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 16.391 | 1.045 | 15.690 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `ax` | `strict_current` | 16.391 | 1.166 | 14.053 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 26.190 | 1.045 | 25.070 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `classic` | `strict_current` | 26.190 | 1.166 | 22.455 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.241 | 1.108 | 6.535 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `ax` | `strict_current` | 7.241 | 1.141 | 6.347 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.913 | 1.108 | 24.290 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `classic` | `strict_current` | 26.913 | 1.141 | 23.592 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.332 | 1.148 | 5.517 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `ax` | `strict_current` | 6.332 | 1.260 | 5.027 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.209 | 1.148 | 21.965 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `classic` | `strict_current` | 25.209 | 1.260 | 20.014 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 16.084 | 1.042 | 15.436 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `ax` | `strict_current` | 16.084 | 1.248 | 12.887 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.422 | 1.042 | 25.357 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `classic` | `strict_current` | 26.422 | 1.248 | 21.169 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.216 | 0.819 | 8.811 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.216 | 0.899 | 8.029 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.926 | 0.819 | 30.435 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.926 | 0.899 | 27.734 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.134 | 0.944 | 9.680 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `ax` | `strict_current` | 9.134 | 1.184 | 7.715 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.083 | 0.944 | 27.643 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `classic` | `strict_current` | 26.083 | 1.184 | 22.031 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.643 | 0.921 | 7.211 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `ax` | `strict_current` | 6.643 | 1.030 | 6.451 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.931 | 0.921 | 28.150 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `classic` | `strict_current` | 25.931 | 1.030 | 25.182 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.398 | 0.838 | 7.634 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `ax` | `strict_current` | 6.398 | 0.990 | 6.464 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.297 | 0.838 | 31.375 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `classic` | `strict_current` | 26.297 | 0.990 | 26.567 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.840 | 1.014 | 6.748 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.840 | 1.072 | 6.382 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 16.018 | 1.014 | 15.802 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `classic` | `strict_current` | 16.018 | 1.072 | 14.945 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.408 | 1.005 | 6.379 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `ax` | `strict_current` | 6.408 | 1.025 | 6.254 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.385 | 1.005 | 14.319 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `classic` | `strict_current` | 14.385 | 1.025 | 14.040 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.221 | 0.832 | 8.684 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `ax` | `strict_current` | 7.221 | 0.969 | 7.449 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.587 | 0.832 | 17.542 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `classic` | `strict_current` | 14.587 | 0.969 | 15.047 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.605 | 0.895 | 7.376 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `ax` | `strict_current` | 6.605 | 0.962 | 6.868 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.916 | 0.895 | 15.540 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `classic` | `strict_current` | 13.916 | 0.962 | 14.471 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 18.846 | 0.915 | 20.601 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `ax` | `strict_current` | 18.846 | 1.502 | 12.545 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 27.080 | 0.915 | 29.602 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `classic` | `strict_current` | 27.080 | 1.502 | 18.027 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.103 | 0.907 | 8.933 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `ax` | `strict_current` | 8.103 | 1.562 | 5.187 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.360 | 0.907 | 30.160 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `classic` | `strict_current` | 27.360 | 1.562 | 17.515 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 16.927 | 0.996 | 16.998 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `ax` | `strict_current` | 16.927 | 1.568 | 10.798 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 29.477 | 0.996 | 29.601 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `classic` | `strict_current` | 29.477 | 1.568 | 18.804 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 19.921 | 1.091 | 18.263 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `ax` | `strict_current` | 19.921 | 1.562 | 12.751 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 28.930 | 1.091 | 26.523 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `classic` | `strict_current` | 28.930 | 1.562 | 18.517 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 15.924 | 0.969 | 16.439 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `ax` | `strict_current` | 15.924 | 0.844 | 18.861 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 15.086 | 0.969 | 15.574 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `classic` | `strict_current` | 15.086 | 0.844 | 17.869 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.021 | 0.793 | 8.859 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `ax` | `strict_current` | 7.021 | 0.945 | 7.429 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.248 | 0.793 | 17.978 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `classic` | `strict_current` | 14.248 | 0.945 | 15.075 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 18.246 | 0.837 | 21.787 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `ax` | `strict_current` | 18.246 | 0.782 | 23.325 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 17.361 | 0.837 | 20.730 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `classic` | `strict_current` | 17.361 | 0.782 | 22.193 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.105 | 0.767 | 10.567 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `ax` | `strict_current` | 8.105 | 0.837 | 9.681 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.477 | 0.767 | 20.178 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `classic` | `strict_current` | 15.477 | 0.837 | 18.486 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.246 | 1.120 | 5.576 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.246 | 2.065 | 3.024 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.027 | 1.120 | 22.344 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.027 | 2.065 | 12.118 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.116 | 1.258 | 4.862 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `ax` | `strict_current` | 6.116 | 2.114 | 2.894 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.733 | 1.258 | 19.662 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `classic` | `strict_current` | 24.733 | 2.114 | 11.702 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.223 | 1.236 | 5.037 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `ax` | `strict_current` | 6.223 | 2.179 | 2.856 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.909 | 1.236 | 20.969 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `classic` | `strict_current` | 25.909 | 2.179 | 11.892 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.200 | 1.162 | 5.336 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `ax` | `strict_current` | 6.200 | 2.168 | 2.860 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.404 | 1.162 | 20.142 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `classic` | `strict_current` | 23.404 | 2.168 | 10.796 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.953 | 1.078 | 5.520 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `ax` | `strict_current` | 5.953 | 1.025 | 5.808 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 30.046 | 1.078 | 27.861 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `classic` | `strict_current` | 30.046 | 1.025 | 29.316 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.390 | 0.980 | 6.518 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `ax` | `strict_current` | 6.390 | 0.968 | 6.598 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.863 | 0.980 | 25.360 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `classic` | `strict_current` | 24.863 | 0.968 | 25.672 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.368 | 0.928 | 6.859 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `ax` | `strict_current` | 6.368 | 0.979 | 6.505 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.313 | 0.928 | 16.494 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `classic` | `strict_current` | 15.313 | 0.979 | 15.643 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.911 | 0.916 | 7.545 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.911 | 0.916 | 7.547 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 14.331 | 0.916 | 15.645 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `classic` | `strict_current` | 14.331 | 0.916 | 15.649 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.405 | 0.918 | 8.066 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `ax` | `strict_current` | 7.405 | 0.935 | 7.916 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.850 | 0.918 | 15.086 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `classic` | `strict_current` | 13.850 | 0.935 | 14.807 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.853 | 1.071 | 6.400 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `ax` | `strict_current` | 6.853 | 1.334 | 5.137 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 14.800 | 1.071 | 13.822 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `classic` | `strict_current` | 14.800 | 1.334 | 11.095 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.564 | 0.923 | 7.111 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `ax` | `strict_current` | 6.564 | 0.978 | 6.714 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.976 | 0.923 | 15.141 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `classic` | `strict_current` | 13.976 | 0.978 | 14.295 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.962 | 0.967 | 7.198 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.962 | 1.347 | 5.170 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.925 | 0.967 | 26.805 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.925 | 1.347 | 19.252 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.355 | 0.774 | 8.208 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `ax` | `strict_current` | 6.355 | 1.303 | 4.877 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.415 | 0.774 | 32.821 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `classic` | `strict_current` | 25.415 | 1.303 | 19.505 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.115 | 1.077 | 6.603 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `ax` | `strict_current` | 7.115 | 1.347 | 5.283 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.819 | 1.077 | 23.964 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `classic` | `strict_current` | 25.819 | 1.347 | 19.171 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.518 | 0.886 | 7.356 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `ax` | `strict_current` | 6.518 | 1.263 | 5.161 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.456 | 0.886 | 28.727 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `classic` | `strict_current` | 25.456 | 1.263 | 20.155 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.035 | 1.917 | 3.670 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.035 | 2.651 | 2.654 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 23.888 | 1.917 | 12.463 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 23.888 | 2.651 | 9.012 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.454 | 1.112 | 5.803 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `ax` | `strict_current` | 6.454 | 2.941 | 2.195 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.867 | 1.112 | 22.357 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `classic` | `strict_current` | 24.867 | 2.941 | 8.456 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.907 | 1.119 | 6.172 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 6.907 | 3.032 | 2.278 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.534 | 1.119 | 22.816 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 25.534 | 3.032 | 8.421 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.509 | 1.363 | 4.776 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `ax` | `strict_current` | 6.509 | 2.886 | 2.255 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.245 | 1.363 | 18.524 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `classic` | `strict_current` | 25.245 | 2.886 | 8.746 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.712 | 1.017 | 6.598 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.712 | 1.555 | 4.315 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 28.288 | 1.017 | 27.805 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `classic` | `strict_current` | 28.288 | 1.555 | 18.186 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.846 | 0.999 | 7.853 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `ax` | `strict_current` | 7.846 | 1.822 | 4.306 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.393 | 0.999 | 27.417 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `classic` | `strict_current` | 27.393 | 1.822 | 15.034 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.737 | 0.852 | 7.909 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `ax` | `strict_current` | 6.737 | 1.607 | 4.192 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.202 | 0.852 | 30.761 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `classic` | `strict_current` | 26.202 | 1.607 | 16.304 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.522 | 0.789 | 9.532 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `ax` | `strict_current` | 7.522 | 1.631 | 4.613 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.454 | 0.789 | 33.520 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `classic` | `strict_current` | 26.454 | 1.631 | 16.223 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 16.461 | 0.871 | 18.904 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `ax` | `strict_current` | 16.461 | 1.036 | 15.896 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 29.097 | 0.871 | 33.415 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `classic` | `strict_current` | 29.097 | 1.036 | 28.099 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.120 | 0.762 | 8.029 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `ax` | `strict_current` | 6.120 | 0.894 | 6.842 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.929 | 0.762 | 36.643 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `classic` | `strict_current` | 27.929 | 0.894 | 31.224 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.106 | 0.818 | 9.910 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `ax` | `strict_current` | 8.106 | 0.873 | 9.286 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.534 | 0.818 | 31.216 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `classic` | `strict_current` | 25.534 | 0.873 | 29.250 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 19.247 | 0.805 | 23.900 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `ax` | `strict_current` | 19.247 | 0.856 | 22.495 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.189 | 0.805 | 33.761 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `classic` | `strict_current` | 27.189 | 0.856 | 31.776 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.011 | 0.742 | 9.449 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.011 | 0.904 | 7.753 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.639 | 0.742 | 33.207 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.639 | 0.904 | 27.247 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.351 | 0.763 | 8.323 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `ax` | `strict_current` | 6.351 | 0.914 | 6.951 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.151 | 0.763 | 32.962 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `classic` | `strict_current` | 25.151 | 0.914 | 27.528 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.562 | 0.784 | 8.373 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 6.562 | 0.811 | 8.094 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.802 | 0.784 | 31.650 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 24.802 | 0.811 | 30.593 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.009 | 0.919 | 7.627 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `ax` | `strict_current` | 7.009 | 0.831 | 8.433 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.703 | 0.919 | 27.969 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `classic` | `strict_current` | 25.703 | 0.831 | 30.926 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 16.724 | 0.879 | 19.034 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `ax` | `strict_current` | 16.724 | 1.316 | 12.706 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 15.204 | 0.879 | 17.304 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `classic` | `strict_current` | 15.204 | 1.316 | 11.551 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 15.589 | 0.919 | 16.957 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `ax` | `strict_current` | 15.589 | 1.268 | 12.291 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.471 | 0.919 | 16.829 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `classic` | `strict_current` | 15.471 | 1.268 | 12.198 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.489 | 0.900 | 7.207 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `ax` | `strict_current` | 6.489 | 1.148 | 5.654 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.163 | 0.900 | 16.840 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `classic` | `strict_current` | 15.163 | 1.148 | 13.211 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.474 | 0.983 | 6.588 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `ax` | `strict_current` | 6.474 | 1.146 | 5.651 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.933 | 0.983 | 14.177 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `classic` | `strict_current` | 13.933 | 1.146 | 12.160 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.019 | 0.872 | 8.052 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.019 | 1.148 | 6.111 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 27.040 | 0.872 | 31.019 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `classic` | `strict_current` | 27.040 | 1.148 | 23.545 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.090 | 0.908 | 7.809 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `ax` | `strict_current` | 7.090 | 0.965 | 7.346 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.639 | 0.908 | 29.339 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `classic` | `strict_current` | 26.639 | 0.965 | 27.601 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.822 | 0.907 | 7.521 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `ax` | `strict_current` | 6.822 | 0.967 | 7.058 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.598 | 0.907 | 30.425 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `classic` | `strict_current` | 27.598 | 0.967 | 28.552 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.901 | 0.930 | 7.423 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `ax` | `strict_current` | 6.901 | 1.044 | 6.612 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.569 | 0.930 | 28.582 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `classic` | `strict_current` | 26.569 | 1.044 | 25.458 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.361 | 1.064 | 6.918 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.361 | 1.187 | 6.203 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.050 | 1.064 | 23.543 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.050 | 1.187 | 21.108 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.390 | 0.969 | 6.592 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `ax` | `strict_current` | 6.390 | 1.171 | 5.458 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.571 | 0.969 | 26.382 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `classic` | `strict_current` | 25.571 | 1.171 | 21.842 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.387 | 0.983 | 7.513 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `ax` | `strict_current` | 7.387 | 1.327 | 5.568 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 29.090 | 0.983 | 29.585 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `classic` | `strict_current` | 29.090 | 1.327 | 21.928 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.143 | 1.025 | 6.972 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `ax` | `strict_current` | 7.143 | 1.023 | 6.984 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.549 | 1.025 | 25.910 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `classic` | `strict_current` | 26.549 | 1.023 | 25.956 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 16.884 | 1.133 | 14.902 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `ax` | `strict_current` | 16.884 | 1.394 | 12.112 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 15.998 | 1.133 | 14.120 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `classic` | `strict_current` | 15.998 | 1.394 | 11.477 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.102 | 1.088 | 6.527 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `ax` | `strict_current` | 7.102 | 1.052 | 6.754 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 15.552 | 1.088 | 14.292 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `classic` | `strict_current` | 15.552 | 1.052 | 14.789 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.437 | 1.149 | 7.343 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `ax` | `strict_current` | 8.437 | 1.164 | 7.250 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 17.470 | 1.149 | 15.205 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `classic` | `strict_current` | 17.470 | 1.164 | 15.013 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 14.790 | 1.029 | 14.367 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `ax` | `strict_current` | 14.790 | 0.886 | 16.697 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.662 | 1.029 | 13.271 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `classic` | `strict_current` | 13.662 | 0.886 | 15.423 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 7.063 | 0.911 | 7.754 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `ax` | `strict_current` | 7.063 | 1.320 | 5.350 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 26.309 | 0.911 | 28.883 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `classic` | `strict_current` | 26.309 | 1.320 | 19.927 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.285 | 0.933 | 6.735 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `ax` | `strict_current` | 6.285 | 1.428 | 4.402 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.596 | 0.933 | 26.359 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `classic` | `strict_current` | 24.596 | 1.428 | 17.226 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.601 | 0.837 | 7.882 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `ax` | `strict_current` | 6.601 | 1.499 | 4.405 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.760 | 0.837 | 30.761 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `classic` | `strict_current` | 25.760 | 1.499 | 17.189 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.595 | 0.955 | 6.907 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `ax` | `strict_current` | 6.595 | 1.368 | 4.821 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.061 | 0.955 | 26.247 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `classic` | `strict_current` | 25.061 | 1.368 | 18.318 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.022 | 1.691 | 3.562 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.022 | 4.082 | 1.475 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 24.633 | 1.691 | 14.568 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 24.633 | 4.082 | 6.035 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.688 | 1.733 | 3.860 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `ax` | `strict_current` | 6.688 | 4.266 | 1.568 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.143 | 1.733 | 13.935 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `classic` | `strict_current` | 24.143 | 4.266 | 5.659 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.462 | 1.756 | 3.679 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `ax` | `strict_current` | 6.462 | 4.223 | 1.530 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.853 | 1.756 | 13.581 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `classic` | `strict_current` | 23.853 | 4.223 | 5.649 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.498 | 1.741 | 3.732 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `ax` | `strict_current` | 6.498 | 4.371 | 1.487 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.868 | 1.741 | 14.283 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `classic` | `strict_current` | 24.868 | 4.371 | 5.689 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 15.977 | 0.865 | 18.464 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `ax` | `strict_current` | 15.977 | 1.086 | 14.705 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 26.744 | 0.865 | 30.906 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `classic` | `strict_current` | 26.744 | 1.086 | 24.615 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 17.096 | 0.795 | 21.505 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `ax` | `strict_current` | 17.096 | 1.081 | 15.811 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.578 | 0.795 | 33.433 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `classic` | `strict_current` | 26.578 | 1.081 | 24.581 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.540 | 0.868 | 7.539 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `ax` | `strict_current` | 6.540 | 1.067 | 6.129 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.718 | 0.868 | 27.339 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `classic` | `strict_current` | 23.718 | 1.067 | 22.228 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.350 | 0.754 | 9.753 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `ax` | `strict_current` | 7.350 | 1.048 | 7.011 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.099 | 0.754 | 35.955 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `classic` | `strict_current` | 27.099 | 1.048 | 25.849 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 6.890 | 1.789 | 3.851 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 6.890 | 3.219 | 2.140 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 25.132 | 1.789 | 14.048 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 25.132 | 3.219 | 7.807 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.002 | 1.719 | 4.074 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `ax` | `strict_current` | 7.002 | 3.094 | 2.263 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 23.550 | 1.719 | 13.703 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `classic` | `strict_current` | 23.550 | 3.094 | 7.610 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.639 | 1.643 | 4.040 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `ax` | `strict_current` | 6.639 | 3.521 | 1.886 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.331 | 1.643 | 14.806 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `classic` | `strict_current` | 24.331 | 3.521 | 6.911 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.802 | 1.645 | 3.527 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `ax` | `strict_current` | 5.802 | 3.126 | 1.856 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.738 | 1.645 | 15.039 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `classic` | `strict_current` | 24.738 | 3.126 | 7.914 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 8.158 | 1.310 | 6.229 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `ax` | `strict_current` | 8.158 | 8.594 | 0.949 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 35.119 | 1.310 | 26.817 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `classic` | `strict_current` | 35.119 | 8.594 | 4.086 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.962 | 0.968 | 7.193 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `ax` | `strict_current` | 6.962 | 1.608 | 4.330 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.858 | 0.968 | 27.749 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `classic` | `strict_current` | 26.858 | 1.608 | 16.704 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.099 | 0.848 | 8.373 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `ax` | `strict_current` | 7.099 | 1.721 | 4.124 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 26.369 | 0.848 | 31.101 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `classic` | `strict_current` | 26.369 | 1.721 | 15.320 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.955 | 3.293 | 2.112 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `ax` | `strict_current` | 6.955 | 3.502 | 1.986 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.356 | 3.293 | 7.396 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `classic` | `strict_current` | 24.356 | 3.502 | 6.956 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.850 | 0.873 | 7.850 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `ax` | `strict_current` | 6.850 | 1.362 | 5.028 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.714 | 0.873 | 28.320 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `classic` | `strict_current` | 24.714 | 1.362 | 18.142 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.448 | 0.846 | 7.624 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `ax` | `strict_current` | 6.448 | 1.295 | 4.980 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 24.365 | 0.846 | 28.807 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `classic` | `strict_current` | 24.365 | 1.295 | 18.817 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.496 | 1.016 | 6.392 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `ax` | `strict_current` | 6.496 | 1.042 | 6.232 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.280 | 1.016 | 26.844 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `classic` | `strict_current` | 27.280 | 1.042 | 26.171 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.267 | 0.997 | 7.285 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `ax` | `strict_current` | 7.267 | 1.647 | 4.411 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 28.767 | 0.997 | 28.841 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `classic` | `strict_current` | 28.767 | 1.647 | 17.462 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.514 | 0.866 | 7.523 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `ax` | `strict_current` | 6.514 | 1.949 | 3.342 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.166 | 0.866 | 31.373 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `classic` | `strict_current` | 27.166 | 1.949 | 13.938 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 9.456 | 1.455 | 6.498 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `ax` | `strict_current` | 9.456 | 1.559 | 6.065 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 29.656 | 1.455 | 20.379 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `classic` | `strict_current` | 29.656 | 1.559 | 19.020 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.686 | 11.820 | 0.650 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `ax` | `strict_current` | 7.686 | 12.165 | 0.632 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 43.483 | 11.820 | 3.679 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `classic` | `strict_current` | 43.483 | 12.165 | 3.574 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.677 | 1.745 | 3.827 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `ax` | `strict_current` | 6.677 | 2.540 | 2.629 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.770 | 1.745 | 15.917 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `classic` | `strict_current` | 27.770 | 2.540 | 10.932 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.202 | 1.088 | 6.622 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `ax` | `strict_current` | 7.202 | 1.753 | 4.110 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 27.590 | 1.088 | 25.365 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `classic` | `strict_current` | 27.590 | 1.753 | 15.743 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 11.087 | 10.054 | 1.103 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `ax` | `strict_current` | 11.087 | 127.027 | 0.087 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 52.028 | 10.054 | 5.175 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `classic` | `strict_current` | 52.028 | 127.027 | 0.410 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.531 | 1.681 | 3.886 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `ax` | `strict_current` | 6.531 | 2.449 | 2.666 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 28.275 | 1.681 | 16.824 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `classic` | `strict_current` | 28.275 | 2.449 | 11.544 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 7.599 | 10.330 | 0.736 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `ax` | `strict_current` | 7.599 | 10.366 | 0.733 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.997 | 10.330 | 2.517 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `classic` | `strict_current` | 25.997 | 10.366 | 2.508 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 6.733 | 1.323 | 5.088 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `ax` | `strict_current` | 6.733 | 2.116 | 3.183 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 25.099 | 1.323 | 18.966 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `classic` | `strict_current` | 25.099 | 2.116 | 11.864 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.928 | 1.380 | 4.294 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `ax` | `strict_current` | 5.928 | 16.312 | 0.363 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 48.880 | 1.380 | 35.410 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `classic` | `strict_current` | 48.880 | 16.312 | 2.997 |

## Interpretation Guardrails

- Speedups use `simulation_ok`, so rows without a behavior checker can still contribute timing if the simulator produced waveforms.
- Accuracy-gated speedups require candidate behavior pass, strict-EVAS parity, and parity to every selected Spectre mode.
- `spectre/ax` matches the previous bridge default but Spectre X may ignore `errpreset` and `maxstep` from the testbench.
- `spectre/classic` is available to measure the stricter non-X path when requested.
- Cold Spectre runs include AHDL CMI compilation; warm-cache repetitions should be reported separately.
- A `BLOCKED` gate is not evidence of wrong behavior; it means the checker or reference evidence is incomplete.
