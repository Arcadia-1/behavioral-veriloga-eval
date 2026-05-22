# Same-Server EVAS/Spectre Speed

Date: 2026-05-22
Claim allowed: `False`
Reason: Same-server timing is measured directly on one host and the artifact emits checker/waveform accuracy gates. Paper-facing speed claims should use only accuracy-gated rows and still need repeated cold/warm runs.

## Scope

- Host: `thu-sui`
- Selected rows: 259
- Jobs: 8
- EVAS modes: `strict_current, profile_balanced, profile_fast, skip_source_error_control, profile_fast_skip_source_error_control`
- Spectre modes: `ax, classic`
- Output root: `results/same-server-speed-ablation-full-goal-20260522`

## Mode Summary

| Backend | Mode | Runs | PASS | Non-PASS | Total wall s | Mean wall s |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| evas | profile_balanced | 259 | 259 | 0 | 1205.029 | 4.653 |
| evas | profile_fast | 259 | 259 | 0 | 920.351 | 3.553 |
| evas | profile_fast_skip_source_error_control | 259 | 259 | 0 | 435.375 | 1.681 |
| evas | skip_source_error_control | 259 | 258 | 1 | 519.416 | 2.005 |
| evas | strict_current | 259 | 259 | 0 | 1479.601 | 5.713 |
| spectre | ax | 259 | 258 | 1 | 375.031 | 1.448 |
| spectre | classic | 259 | 259 | 0 | 1170.224 | 4.518 |

## Accuracy Gate Summary

| EVAS mode | Runs | Gate PASS | Gate FAIL | Gate BLOCKED | Gate missing |
| --- | ---: | ---: | ---: | ---: | ---: |
| profile_balanced | 259 | 258 | 1 | 0 | 0 |
| profile_fast | 259 | 258 | 1 | 0 | 0 |
| profile_fast_skip_source_error_control | 259 | 258 | 1 | 0 | 0 |
| skip_source_error_control | 259 | 257 | 2 | 0 | 0 |
| strict_current | 259 | 258 | 1 | 0 | 0 |

## Per-Row Accuracy Gates

| Entry | Form | Variant | EVAS mode | Gate | Reasons | Blocked |
| --- | --- | --- | --- | --- | --- | --- |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_event_controller` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_event_controller` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l2_event_controller` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l2_event_controller` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_event_controller` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `strict_current` | `FAIL` | spectre_ax_parity:spectre_behavior_check_failed | - |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `profile_balanced` | `FAIL` | spectre_ax_parity:spectre_behavior_check_failed | - |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `profile_fast` | `FAIL` | spectre_ax_parity:spectre_behavior_check_failed | - |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `skip_source_error_control` | `FAIL` | spectre_ax_parity:spectre_behavior_check_failed | - |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `FAIL` | spectre_ax_parity:spectre_behavior_check_failed | - |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `skip_source_error_control` | `FAIL` | candidate_behavior_check_failed | - |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `profile_balanced` | `PASS` | - | - |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `profile_fast` | `PASS` | - | - |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |

## Simulation-Only Speedups

| Entry | Form | Variant | Spectre mode | EVAS mode | Spectre wall s | EVAS wall s | Spectre/EVAS |
| --- | --- | --- | --- | --- | ---: | ---: | ---: |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.113 | 1.181 | 0.942 |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.113 | 0.968 | 1.150 |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.113 | 0.757 | 1.470 |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.113 | 0.799 | 1.392 |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.113 | 1.040 | 1.070 |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.632 | 1.181 | 3.923 |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.632 | 0.968 | 4.787 |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.632 | 0.757 | 6.117 |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.632 | 0.799 | 5.795 |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.632 | 1.040 | 4.456 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `ax` | `profile_balanced` | 0.928 | 1.160 | 0.800 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `ax` | `profile_fast` | 0.928 | 0.882 | 1.052 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.928 | 1.065 | 0.872 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `ax` | `skip_source_error_control` | 0.928 | 0.823 | 1.128 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `ax` | `strict_current` | 0.928 | 1.219 | 0.762 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `classic` | `profile_balanced` | 4.221 | 1.160 | 3.638 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `classic` | `profile_fast` | 4.221 | 0.882 | 4.785 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.221 | 1.065 | 3.964 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `classic` | `skip_source_error_control` | 4.221 | 0.823 | 5.131 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `classic` | `strict_current` | 4.221 | 1.219 | 3.463 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.141 | 1.173 | 0.973 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `ax` | `profile_fast` | 1.141 | 0.957 | 1.191 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.141 | 0.821 | 1.389 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.141 | 0.904 | 1.262 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `ax` | `strict_current` | 1.141 | 1.239 | 0.920 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.606 | 1.173 | 3.927 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `classic` | `profile_fast` | 4.606 | 0.957 | 4.811 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.606 | 0.821 | 5.607 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.606 | 0.904 | 5.097 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `classic` | `strict_current` | 4.606 | 1.239 | 3.716 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `ax` | `profile_balanced` | 1.216 | 1.181 | 1.029 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `ax` | `profile_fast` | 1.216 | 1.067 | 1.139 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.216 | 1.006 | 1.209 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.216 | 0.896 | 1.358 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `ax` | `strict_current` | 1.216 | 1.324 | 0.918 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `classic` | `profile_balanced` | 4.702 | 1.181 | 3.980 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `classic` | `profile_fast` | 4.702 | 1.067 | 4.406 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.702 | 1.006 | 4.675 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.702 | 0.896 | 5.250 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `classic` | `strict_current` | 4.702 | 1.324 | 3.550 |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.380 | 10.800 | 0.128 |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.380 | 5.790 | 0.238 |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.380 | 1.125 | 1.227 |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.380 | 1.242 | 1.111 |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.380 | 10.551 | 0.131 |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 3.725 | 10.800 | 0.345 |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `classic` | `profile_fast` | 3.725 | 5.790 | 0.643 |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 3.725 | 1.125 | 3.312 |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 3.725 | 1.242 | 2.999 |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 3.725 | 10.551 | 0.353 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `ax` | `profile_balanced` | 0.792 | 10.647 | 0.074 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `ax` | `profile_fast` | 0.792 | 5.606 | 0.141 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.792 | 1.057 | 0.749 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `ax` | `skip_source_error_control` | 0.792 | 1.157 | 0.684 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `ax` | `strict_current` | 0.792 | 10.733 | 0.074 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `classic` | `profile_balanced` | 3.652 | 10.647 | 0.343 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `classic` | `profile_fast` | 3.652 | 5.606 | 0.652 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.652 | 1.057 | 3.456 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `classic` | `skip_source_error_control` | 3.652 | 1.157 | 3.158 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `classic` | `strict_current` | 3.652 | 10.733 | 0.340 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.022 | 1.626 | 0.629 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `ax` | `profile_fast` | 1.022 | 1.550 | 0.660 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.022 | 1.516 | 0.674 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.022 | 1.371 | 0.746 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `ax` | `strict_current` | 1.022 | 1.658 | 0.617 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.136 | 1.626 | 2.544 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `classic` | `profile_fast` | 4.136 | 1.550 | 2.669 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.136 | 1.516 | 2.729 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.136 | 1.371 | 3.018 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `classic` | `strict_current` | 4.136 | 1.658 | 2.495 |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `ax` | `profile_balanced` | 1.085 | 1.783 | 0.609 |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `ax` | `profile_fast` | 1.085 | 1.488 | 0.729 |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.085 | 1.539 | 0.705 |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.085 | 1.458 | 0.744 |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `ax` | `strict_current` | 1.085 | 1.792 | 0.606 |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `classic` | `profile_balanced` | 4.459 | 1.783 | 2.501 |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `classic` | `profile_fast` | 4.459 | 1.488 | 2.997 |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.459 | 1.539 | 2.897 |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.459 | 1.458 | 3.059 |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `classic` | `strict_current` | 4.459 | 1.792 | 2.488 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 3.309 | 0.722 | 4.582 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `ax` | `profile_fast` | 3.309 | 0.709 | 4.667 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 3.309 | 0.691 | 4.788 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 3.309 | 0.719 | 4.604 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `ax` | `strict_current` | 3.309 | 0.782 | 4.229 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 5.395 | 0.722 | 7.469 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `classic` | `profile_fast` | 5.395 | 0.709 | 7.609 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 5.395 | 0.691 | 7.805 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 5.395 | 0.719 | 7.506 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `classic` | `strict_current` | 5.395 | 0.782 | 6.895 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `ax` | `profile_balanced` | 3.687 | 0.700 | 5.269 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `ax` | `profile_fast` | 3.687 | 0.679 | 5.433 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 3.687 | 0.604 | 6.108 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `ax` | `skip_source_error_control` | 3.687 | 0.924 | 3.990 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `ax` | `strict_current` | 3.687 | 0.695 | 5.304 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `classic` | `profile_balanced` | 5.298 | 0.700 | 7.570 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `classic` | `profile_fast` | 5.298 | 0.679 | 7.806 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.298 | 0.604 | 8.775 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `classic` | `skip_source_error_control` | 5.298 | 0.924 | 5.733 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `classic` | `strict_current` | 5.298 | 0.695 | 7.620 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.294 | 0.860 | 1.504 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `ax` | `profile_fast` | 1.294 | 0.726 | 1.783 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.294 | 0.594 | 2.179 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.294 | 0.661 | 1.959 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `ax` | `strict_current` | 1.294 | 0.820 | 1.579 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.979 | 0.860 | 5.786 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `classic` | `profile_fast` | 4.979 | 0.726 | 6.862 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.979 | 0.594 | 8.383 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.979 | 0.661 | 7.537 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `classic` | `strict_current` | 4.979 | 0.820 | 6.076 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `ax` | `profile_balanced` | 1.209 | 0.788 | 1.533 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `ax` | `profile_fast` | 1.209 | 0.805 | 1.502 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.209 | 0.683 | 1.770 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.209 | 0.688 | 1.756 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `ax` | `strict_current` | 1.209 | 0.904 | 1.336 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `classic` | `profile_balanced` | 4.827 | 0.788 | 6.122 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `classic` | `profile_fast` | 4.827 | 0.805 | 5.998 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.827 | 0.683 | 7.069 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.827 | 0.688 | 7.012 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `classic` | `strict_current` | 4.827 | 0.904 | 5.337 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `ax` | `profile_balanced` | 1.516 | 1.189 | 1.276 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `ax` | `profile_fast` | 1.516 | 0.774 | 1.959 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.516 | 0.858 | 1.767 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.516 | 0.865 | 1.754 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `ax` | `strict_current` | 1.516 | 1.203 | 1.260 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `classic` | `profile_balanced` | 5.392 | 1.189 | 4.536 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `classic` | `profile_fast` | 5.392 | 0.774 | 6.965 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.392 | 0.858 | 6.283 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `classic` | `skip_source_error_control` | 5.392 | 0.865 | 6.237 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `classic` | `strict_current` | 5.392 | 1.203 | 4.480 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `ax` | `profile_balanced` | 0.882 | 1.156 | 0.763 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `ax` | `profile_fast` | 0.882 | 0.753 | 1.172 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.882 | 0.800 | 1.103 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 0.882 | 0.668 | 1.322 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `ax` | `strict_current` | 0.882 | 1.168 | 0.755 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.538 | 1.156 | 3.925 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `classic` | `profile_fast` | 4.538 | 0.753 | 6.030 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.538 | 0.800 | 5.673 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.538 | 0.668 | 6.798 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `classic` | `strict_current` | 4.538 | 1.168 | 3.885 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `ax` | `profile_balanced` | 0.886 | 1.172 | 0.756 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `ax` | `profile_fast` | 0.886 | 0.668 | 1.326 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.886 | 0.794 | 1.116 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `ax` | `skip_source_error_control` | 0.886 | 0.821 | 1.079 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `ax` | `strict_current` | 0.886 | 1.182 | 0.750 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `classic` | `profile_balanced` | 4.276 | 1.172 | 3.649 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `classic` | `profile_fast` | 4.276 | 0.668 | 6.402 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.276 | 0.794 | 5.388 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.276 | 0.821 | 5.208 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `classic` | `strict_current` | 4.276 | 1.182 | 3.619 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 0.912 | 1.542 | 0.591 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `ax` | `profile_fast` | 0.912 | 1.119 | 0.815 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 0.912 | 0.541 | 1.687 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 0.912 | 0.632 | 1.443 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `ax` | `strict_current` | 0.912 | 1.671 | 0.546 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.485 | 1.542 | 2.908 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.485 | 1.119 | 4.009 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.485 | 0.541 | 8.296 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.485 | 0.632 | 7.097 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.485 | 1.671 | 2.684 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `ax` | `profile_balanced` | 0.992 | 1.445 | 0.687 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `ax` | `profile_fast` | 0.992 | 0.955 | 1.039 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.992 | 0.662 | 1.499 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `ax` | `skip_source_error_control` | 0.992 | 0.525 | 1.890 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `ax` | `strict_current` | 0.992 | 1.569 | 0.633 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `classic` | `profile_balanced` | 4.378 | 1.445 | 3.030 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `classic` | `profile_fast` | 4.378 | 0.955 | 4.583 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.378 | 0.662 | 6.612 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `classic` | `skip_source_error_control` | 4.378 | 0.525 | 8.339 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `classic` | `strict_current` | 4.378 | 1.569 | 2.791 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.274 | 1.602 | 0.795 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `ax` | `profile_fast` | 1.274 | 0.998 | 1.276 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.274 | 0.586 | 2.173 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.274 | 0.605 | 2.105 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `ax` | `strict_current` | 1.274 | 1.706 | 0.747 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.942 | 1.602 | 3.084 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `classic` | `profile_fast` | 4.942 | 0.998 | 4.952 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.942 | 0.586 | 8.432 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.942 | 0.605 | 8.167 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `classic` | `strict_current` | 4.942 | 1.706 | 2.897 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `ax` | `profile_balanced` | 0.939 | 1.470 | 0.639 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `ax` | `profile_fast` | 0.939 | 0.973 | 0.965 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.939 | 0.605 | 1.551 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `ax` | `skip_source_error_control` | 0.939 | 0.534 | 1.760 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `ax` | `strict_current` | 0.939 | 1.439 | 0.652 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `classic` | `profile_balanced` | 4.109 | 1.470 | 2.795 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `classic` | `profile_fast` | 4.109 | 0.973 | 4.224 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.109 | 0.605 | 6.790 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.109 | 0.534 | 7.702 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `classic` | `strict_current` | 4.109 | 1.439 | 2.856 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 0.887 | 3.447 | 0.257 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `ax` | `profile_fast` | 0.887 | 2.168 | 0.409 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 0.887 | 1.445 | 0.614 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 0.887 | 1.428 | 0.621 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `ax` | `strict_current` | 0.887 | 3.584 | 0.247 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.033 | 3.447 | 1.170 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.033 | 2.168 | 1.860 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.033 | 1.445 | 2.791 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.033 | 1.428 | 2.825 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.033 | 3.584 | 1.125 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `ax` | `profile_balanced` | 0.674 | 3.535 | 0.191 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `ax` | `profile_fast` | 0.674 | 1.978 | 0.341 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.674 | 1.358 | 0.496 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `ax` | `skip_source_error_control` | 0.674 | 1.405 | 0.480 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `ax` | `strict_current` | 0.674 | 3.570 | 0.189 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `classic` | `profile_balanced` | 3.919 | 3.535 | 1.109 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `classic` | `profile_fast` | 3.919 | 1.978 | 1.981 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.919 | 1.358 | 2.886 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `classic` | `skip_source_error_control` | 3.919 | 1.405 | 2.790 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `classic` | `strict_current` | 3.919 | 3.570 | 1.098 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.511 | 3.566 | 0.424 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `ax` | `profile_fast` | 1.511 | 1.998 | 0.756 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.511 | 1.503 | 1.005 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.511 | 1.417 | 1.067 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `ax` | `strict_current` | 1.511 | 3.468 | 0.436 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `classic` | `profile_balanced` | 3.914 | 3.566 | 1.098 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `classic` | `profile_fast` | 3.914 | 1.998 | 1.959 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.914 | 1.503 | 2.604 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 3.914 | 1.417 | 2.763 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `classic` | `strict_current` | 3.914 | 3.468 | 1.129 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `ax` | `profile_balanced` | 0.658 | 3.351 | 0.196 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `ax` | `profile_fast` | 0.658 | 2.004 | 0.328 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.658 | 1.529 | 0.430 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `ax` | `skip_source_error_control` | 0.658 | 1.536 | 0.428 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `ax` | `strict_current` | 0.658 | 3.555 | 0.185 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `classic` | `profile_balanced` | 4.466 | 3.351 | 1.333 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `classic` | `profile_fast` | 4.466 | 2.004 | 2.229 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.466 | 1.529 | 2.922 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.466 | 1.536 | 2.907 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `classic` | `strict_current` | 4.466 | 3.555 | 1.256 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 0.927 | 1.548 | 0.599 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `ax` | `profile_fast` | 0.927 | 0.971 | 0.954 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 0.927 | 0.740 | 1.253 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 0.927 | 0.609 | 1.523 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `ax` | `strict_current` | 0.927 | 1.489 | 0.622 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.202 | 1.548 | 2.715 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.202 | 0.971 | 4.327 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.202 | 0.740 | 5.680 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.202 | 0.609 | 6.902 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.202 | 1.489 | 2.821 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `ax` | `profile_balanced` | 1.038 | 1.473 | 0.705 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `ax` | `profile_fast` | 1.038 | 0.919 | 1.129 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.038 | 0.747 | 1.390 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.038 | 0.540 | 1.921 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `ax` | `strict_current` | 1.038 | 1.584 | 0.655 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `classic` | `profile_balanced` | 4.149 | 1.473 | 2.818 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `classic` | `profile_fast` | 4.149 | 0.919 | 4.515 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.149 | 0.747 | 5.557 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `classic` | `skip_source_error_control` | 4.149 | 0.540 | 7.683 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `classic` | `strict_current` | 4.149 | 1.584 | 2.620 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `ax` | `profile_balanced` | 0.909 | 1.349 | 0.674 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `ax` | `profile_fast` | 0.909 | 0.975 | 0.932 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.909 | 0.629 | 1.445 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 0.909 | 0.548 | 1.659 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `ax` | `strict_current` | 0.909 | 1.416 | 0.642 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.011 | 1.349 | 2.974 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `classic` | `profile_fast` | 4.011 | 0.975 | 4.116 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.011 | 0.629 | 6.379 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.011 | 0.548 | 7.324 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `classic` | `strict_current` | 4.011 | 1.416 | 2.834 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `ax` | `profile_balanced` | 1.220 | 1.462 | 0.834 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `ax` | `profile_fast` | 1.220 | 0.956 | 1.277 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.220 | 0.733 | 1.665 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.220 | 0.598 | 2.042 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `ax` | `strict_current` | 1.220 | 1.507 | 0.810 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `classic` | `profile_balanced` | 4.239 | 1.462 | 2.899 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `classic` | `profile_fast` | 4.239 | 0.956 | 4.435 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.239 | 0.733 | 5.786 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.239 | 0.598 | 7.093 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `classic` | `strict_current` | 4.239 | 1.507 | 2.813 |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.117 | 4.015 | 0.278 |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.117 | 2.256 | 0.495 |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.117 | 1.144 | 0.977 |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.117 | 1.124 | 0.994 |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.117 | 4.079 | 0.274 |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.458 | 4.015 | 1.110 |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.458 | 2.256 | 1.976 |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.458 | 1.144 | 3.899 |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.458 | 1.124 | 3.968 |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.458 | 4.079 | 1.093 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `ax` | `profile_balanced` | 0.865 | 3.826 | 0.226 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `ax` | `profile_fast` | 0.865 | 2.346 | 0.369 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.865 | 1.053 | 0.822 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `ax` | `skip_source_error_control` | 0.865 | 1.115 | 0.776 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `ax` | `strict_current` | 0.865 | 3.917 | 0.221 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `classic` | `profile_balanced` | 3.963 | 3.826 | 1.036 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `classic` | `profile_fast` | 3.963 | 2.346 | 1.689 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.963 | 1.053 | 3.765 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `classic` | `skip_source_error_control` | 3.963 | 1.115 | 3.554 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `classic` | `strict_current` | 3.963 | 3.917 | 1.012 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.438 | 3.879 | 0.371 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `ax` | `profile_fast` | 1.438 | 2.382 | 0.604 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.438 | 1.125 | 1.279 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.438 | 1.169 | 1.230 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `ax` | `strict_current` | 1.438 | 3.955 | 0.364 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.287 | 3.879 | 1.105 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `classic` | `profile_fast` | 4.287 | 2.382 | 1.800 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.287 | 1.125 | 3.811 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.287 | 1.169 | 3.666 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `classic` | `strict_current` | 4.287 | 3.955 | 1.084 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `ax` | `profile_balanced` | 1.294 | 4.116 | 0.315 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `ax` | `profile_fast` | 1.294 | 2.281 | 0.567 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.294 | 1.054 | 1.228 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.294 | 1.145 | 1.130 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `ax` | `strict_current` | 1.294 | 4.000 | 0.324 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `classic` | `profile_balanced` | 3.923 | 4.116 | 0.953 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `classic` | `profile_fast` | 3.923 | 2.281 | 1.720 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.923 | 1.054 | 3.721 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `classic` | `skip_source_error_control` | 3.923 | 1.145 | 3.425 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `classic` | `strict_current` | 3.923 | 4.000 | 0.981 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.240 | 1.545 | 0.802 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.240 | 0.907 | 1.367 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.240 | 0.759 | 1.633 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.240 | 0.712 | 1.742 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.240 | 1.519 | 0.816 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.705 | 1.545 | 3.046 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.705 | 0.907 | 5.188 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.705 | 0.759 | 6.199 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.705 | 0.712 | 6.610 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.705 | 1.519 | 3.098 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `ax` | `profile_balanced` | 1.224 | 1.533 | 0.798 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `ax` | `profile_fast` | 1.224 | 0.938 | 1.305 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.224 | 0.825 | 1.484 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.224 | 0.780 | 1.568 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `ax` | `strict_current` | 1.224 | 1.581 | 0.774 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `classic` | `profile_balanced` | 4.392 | 1.533 | 2.866 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `classic` | `profile_fast` | 4.392 | 0.938 | 4.683 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.392 | 0.825 | 5.326 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `classic` | `skip_source_error_control` | 4.392 | 0.780 | 5.628 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `classic` | `strict_current` | 4.392 | 1.581 | 2.779 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.129 | 1.523 | 0.741 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `ax` | `profile_fast` | 1.129 | 1.011 | 1.116 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.129 | 0.843 | 1.340 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.129 | 0.671 | 1.683 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `ax` | `strict_current` | 1.129 | 1.574 | 0.717 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.566 | 1.523 | 2.998 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `classic` | `profile_fast` | 4.566 | 1.011 | 4.516 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.566 | 0.843 | 5.419 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.566 | 0.671 | 6.807 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `classic` | `strict_current` | 4.566 | 1.574 | 2.901 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `ax` | `profile_balanced` | 1.073 | 1.595 | 0.673 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `ax` | `profile_fast` | 1.073 | 0.941 | 1.141 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.073 | 0.664 | 1.618 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.073 | 0.709 | 1.513 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `ax` | `strict_current` | 1.073 | 1.598 | 0.672 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `classic` | `profile_balanced` | 4.778 | 1.595 | 2.997 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `classic` | `profile_fast` | 4.778 | 0.941 | 5.078 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.778 | 0.664 | 7.201 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.778 | 0.709 | 6.737 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `classic` | `strict_current` | 4.778 | 1.598 | 2.991 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 0.932 | 3.248 | 0.287 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast` | 0.932 | 1.401 | 0.665 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 0.932 | 0.896 | 1.040 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 0.932 | 1.938 | 0.481 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 0.932 | 3.300 | 0.282 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 3.799 | 3.248 | 1.170 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast` | 3.799 | 1.401 | 2.711 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 3.799 | 0.896 | 4.238 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 3.799 | 1.938 | 1.960 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 3.799 | 3.300 | 1.151 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `ax` | `profile_balanced` | 1.306 | 3.272 | 0.399 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `ax` | `profile_fast` | 1.306 | 1.450 | 0.901 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.306 | 0.885 | 1.477 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.306 | 2.083 | 0.627 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `ax` | `strict_current` | 1.306 | 3.278 | 0.399 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `classic` | `profile_balanced` | 4.432 | 3.272 | 1.355 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `classic` | `profile_fast` | 4.432 | 1.450 | 3.056 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.432 | 0.885 | 5.009 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `classic` | `skip_source_error_control` | 4.432 | 2.083 | 2.128 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `classic` | `strict_current` | 4.432 | 3.278 | 1.352 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `ax` | `profile_balanced` | 0.750 | 3.047 | 0.246 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `ax` | `profile_fast` | 0.750 | 1.435 | 0.522 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.750 | 0.870 | 0.862 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 0.750 | 1.981 | 0.378 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 0.750 | 3.176 | 0.236 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `classic` | `profile_balanced` | 3.665 | 3.047 | 1.203 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `classic` | `profile_fast` | 3.665 | 1.435 | 2.553 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.665 | 0.870 | 4.214 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 3.665 | 1.981 | 1.850 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 3.665 | 3.176 | 1.154 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `ax` | `profile_balanced` | 0.983 | 3.048 | 0.322 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `ax` | `profile_fast` | 0.983 | 1.381 | 0.712 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.983 | 0.861 | 1.142 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `ax` | `skip_source_error_control` | 0.983 | 1.916 | 0.513 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `ax` | `strict_current` | 0.983 | 3.024 | 0.325 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `classic` | `profile_balanced` | 4.050 | 3.048 | 1.329 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `classic` | `profile_fast` | 4.050 | 1.381 | 2.933 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.050 | 0.861 | 4.706 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.050 | 1.916 | 2.114 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `classic` | `strict_current` | 4.050 | 3.024 | 1.340 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.289 | 1.287 | 1.001 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.289 | 0.897 | 1.437 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.289 | 0.685 | 1.882 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.289 | 0.739 | 1.745 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.289 | 1.272 | 1.013 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 2.653 | 1.287 | 2.061 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `classic` | `profile_fast` | 2.653 | 0.897 | 2.957 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 2.653 | 0.685 | 3.874 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 2.653 | 0.739 | 3.592 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `classic` | `strict_current` | 2.653 | 1.272 | 2.085 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `ax` | `profile_balanced` | 1.689 | 1.232 | 1.371 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `ax` | `profile_fast` | 1.689 | 0.744 | 2.272 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.689 | 0.847 | 1.994 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.689 | 0.789 | 2.140 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `ax` | `strict_current` | 1.689 | 1.274 | 1.325 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `classic` | `profile_balanced` | 3.561 | 1.232 | 2.890 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `classic` | `profile_fast` | 3.561 | 0.744 | 4.789 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.561 | 0.847 | 4.203 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `classic` | `skip_source_error_control` | 3.561 | 0.789 | 4.512 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `classic` | `strict_current` | 3.561 | 1.274 | 2.794 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `ax` | `profile_balanced` | 0.742 | 1.357 | 0.547 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `ax` | `profile_fast` | 0.742 | 0.916 | 0.810 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.742 | 0.718 | 1.033 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 0.742 | 0.717 | 1.035 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `ax` | `strict_current` | 0.742 | 1.428 | 0.519 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `classic` | `profile_balanced` | 2.354 | 1.357 | 1.735 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `classic` | `profile_fast` | 2.354 | 0.916 | 2.570 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.354 | 0.718 | 3.277 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 2.354 | 0.717 | 3.284 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `classic` | `strict_current` | 2.354 | 1.428 | 1.648 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `ax` | `profile_balanced` | 0.930 | 1.282 | 0.725 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `ax` | `profile_fast` | 0.930 | 0.735 | 1.265 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.930 | 0.601 | 1.546 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `ax` | `skip_source_error_control` | 0.930 | 0.754 | 1.233 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `ax` | `strict_current` | 0.930 | 1.465 | 0.634 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `classic` | `profile_balanced` | 2.466 | 1.282 | 1.924 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `classic` | `profile_fast` | 2.466 | 0.735 | 3.356 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.466 | 0.601 | 4.100 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `classic` | `skip_source_error_control` | 2.466 | 0.754 | 3.270 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `classic` | `strict_current` | 2.466 | 1.465 | 1.683 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `ax` | `profile_balanced` | 1.352 | 0.683 | 1.980 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `ax` | `profile_fast` | 1.352 | 0.777 | 1.740 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.352 | 0.506 | 2.675 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.352 | 0.793 | 1.705 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `ax` | `strict_current` | 1.352 | 0.790 | 1.711 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `classic` | `profile_balanced` | 3.038 | 0.683 | 4.448 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `classic` | `profile_fast` | 3.038 | 0.777 | 3.908 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.038 | 0.506 | 6.009 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `classic` | `skip_source_error_control` | 3.038 | 0.793 | 3.829 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `classic` | `strict_current` | 3.038 | 0.790 | 3.844 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.456 | 0.666 | 2.187 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `ax` | `profile_fast` | 1.456 | 0.582 | 2.501 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.456 | 0.722 | 2.016 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.456 | 0.644 | 2.262 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `ax` | `strict_current` | 1.456 | 0.848 | 1.717 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `classic` | `profile_balanced` | 3.452 | 0.666 | 5.184 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `classic` | `profile_fast` | 3.452 | 0.582 | 5.928 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.452 | 0.722 | 4.779 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 3.452 | 0.644 | 5.363 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `classic` | `strict_current` | 3.452 | 0.848 | 4.070 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `ax` | `profile_balanced` | 1.291 | 0.682 | 1.894 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `ax` | `profile_fast` | 1.291 | 0.576 | 2.243 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.291 | 0.580 | 2.225 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.291 | 0.540 | 2.393 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `ax` | `strict_current` | 1.291 | 0.778 | 1.660 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `classic` | `profile_balanced` | 3.278 | 0.682 | 4.808 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `classic` | `profile_fast` | 3.278 | 0.576 | 5.694 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.278 | 0.580 | 5.650 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `classic` | `skip_source_error_control` | 3.278 | 0.540 | 6.075 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `classic` | `strict_current` | 3.278 | 0.778 | 4.214 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.490 | 0.590 | 2.525 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.490 | 0.577 | 2.583 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.490 | 0.540 | 2.757 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.490 | 0.557 | 2.674 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.490 | 0.568 | 2.624 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.654 | 0.590 | 7.884 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.654 | 0.577 | 8.065 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.654 | 0.540 | 8.611 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.654 | 0.557 | 8.352 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.654 | 0.568 | 8.193 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `ax` | `profile_balanced` | 1.311 | 0.783 | 1.675 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `ax` | `profile_fast` | 1.311 | 0.661 | 1.983 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.311 | 0.651 | 2.014 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.311 | 0.669 | 1.961 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `ax` | `strict_current` | 1.311 | 0.812 | 1.614 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `classic` | `profile_balanced` | 4.804 | 0.783 | 6.135 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `classic` | `profile_fast` | 4.804 | 0.661 | 7.265 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.804 | 0.651 | 7.379 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `classic` | `skip_source_error_control` | 4.804 | 0.669 | 7.184 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `classic` | `strict_current` | 4.804 | 0.812 | 5.915 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.504 | 0.599 | 2.510 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `ax` | `profile_fast` | 1.504 | 0.821 | 1.831 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.504 | 0.673 | 2.233 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.504 | 0.615 | 2.445 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `ax` | `strict_current` | 1.504 | 0.600 | 2.507 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `classic` | `profile_balanced` | 5.477 | 0.599 | 9.143 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `classic` | `profile_fast` | 5.477 | 0.821 | 6.668 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.477 | 0.673 | 8.135 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 5.477 | 0.615 | 8.906 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `classic` | `strict_current` | 5.477 | 0.600 | 9.131 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `ax` | `profile_balanced` | 0.996 | 0.544 | 1.829 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `ax` | `profile_fast` | 0.996 | 0.600 | 1.659 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.996 | 0.533 | 1.869 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `ax` | `skip_source_error_control` | 0.996 | 0.617 | 1.614 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `ax` | `strict_current` | 0.996 | 0.635 | 1.567 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `classic` | `profile_balanced` | 4.753 | 0.544 | 8.735 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `classic` | `profile_fast` | 4.753 | 0.600 | 7.921 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.753 | 0.533 | 8.923 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.753 | 0.617 | 7.704 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `classic` | `strict_current` | 4.753 | 0.635 | 7.482 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 4.157 | 1.094 | 3.802 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `ax` | `profile_fast` | 4.157 | 1.029 | 4.042 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 4.157 | 0.686 | 6.056 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 4.157 | 0.758 | 5.483 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `ax` | `strict_current` | 4.157 | 1.205 | 3.449 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 5.535 | 1.094 | 5.061 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `classic` | `profile_fast` | 5.535 | 1.029 | 5.381 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 5.535 | 0.686 | 8.062 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 5.535 | 0.758 | 7.300 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `classic` | `strict_current` | 5.535 | 1.205 | 4.591 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `ax` | `profile_balanced` | 1.154 | 0.780 | 1.479 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `ax` | `profile_fast` | 1.154 | 0.632 | 1.825 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.154 | 0.711 | 1.623 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.154 | 0.538 | 2.143 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `ax` | `strict_current` | 1.154 | 0.987 | 1.169 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `classic` | `profile_balanced` | 5.921 | 0.780 | 7.587 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `classic` | `profile_fast` | 5.921 | 0.632 | 9.363 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.921 | 0.711 | 8.330 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `classic` | `skip_source_error_control` | 5.921 | 0.538 | 10.999 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `classic` | `strict_current` | 5.921 | 0.987 | 6.000 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.079 | 0.767 | 1.408 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `ax` | `profile_fast` | 1.079 | 0.663 | 1.628 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.079 | 0.632 | 1.707 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.079 | 0.523 | 2.062 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `ax` | `strict_current` | 1.079 | 0.836 | 1.291 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.867 | 0.767 | 6.347 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `classic` | `profile_fast` | 4.867 | 0.663 | 7.339 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.867 | 0.632 | 7.698 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.867 | 0.523 | 9.298 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `classic` | `strict_current` | 4.867 | 0.836 | 5.821 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `ax` | `profile_balanced` | 1.194 | 0.879 | 1.358 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `ax` | `profile_fast` | 1.194 | 0.770 | 1.550 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.194 | 0.627 | 1.904 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.194 | 0.655 | 1.824 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `ax` | `strict_current` | 1.194 | 0.942 | 1.267 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `classic` | `profile_balanced` | 4.876 | 0.879 | 5.546 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `classic` | `profile_fast` | 4.876 | 0.770 | 6.330 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.876 | 0.627 | 7.776 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.876 | 0.655 | 7.446 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `classic` | `strict_current` | 4.876 | 0.942 | 5.174 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.188 | 1.261 | 0.942 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.188 | 0.934 | 1.272 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.188 | 0.759 | 1.565 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.188 | 0.752 | 1.579 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.188 | 4.813 | 0.247 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.450 | 1.261 | 3.530 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.450 | 0.934 | 4.765 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.450 | 0.759 | 5.865 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.450 | 0.752 | 5.915 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.450 | 4.813 | 0.925 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `ax` | `profile_balanced` | 1.281 | 1.374 | 0.932 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `ax` | `profile_fast` | 1.281 | 1.048 | 1.222 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.281 | 0.777 | 1.648 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.281 | 0.826 | 1.552 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `ax` | `strict_current` | 1.281 | 4.745 | 0.270 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `classic` | `profile_balanced` | 4.950 | 1.374 | 3.603 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `classic` | `profile_fast` | 4.950 | 1.048 | 4.723 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.950 | 0.777 | 6.369 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `classic` | `skip_source_error_control` | 4.950 | 0.826 | 5.996 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `classic` | `strict_current` | 4.950 | 4.745 | 1.043 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.397 | 1.249 | 1.119 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `ax` | `profile_fast` | 1.397 | 0.846 | 1.652 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.397 | 0.775 | 1.802 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.397 | 0.759 | 1.842 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `ax` | `strict_current` | 1.397 | 4.760 | 0.294 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.888 | 1.249 | 3.914 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `classic` | `profile_fast` | 4.888 | 0.846 | 5.778 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.888 | 0.775 | 6.303 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.888 | 0.759 | 6.441 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `classic` | `strict_current` | 4.888 | 4.760 | 1.027 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `ax` | `profile_balanced` | 1.372 | 1.376 | 0.997 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `ax` | `profile_fast` | 1.372 | 0.929 | 1.477 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.372 | 0.770 | 1.781 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.372 | 0.898 | 1.527 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `ax` | `strict_current` | 1.372 | 4.873 | 0.281 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `classic` | `profile_balanced` | 5.128 | 1.376 | 3.726 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `classic` | `profile_fast` | 5.128 | 0.929 | 5.521 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.128 | 0.770 | 6.661 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `classic` | `skip_source_error_control` | 5.128 | 0.898 | 5.710 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `classic` | `strict_current` | 5.128 | 4.873 | 1.052 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.149 | 1.519 | 0.756 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.149 | 1.472 | 0.781 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.149 | 1.387 | 0.828 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.149 | 1.419 | 0.810 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.149 | 1.478 | 0.777 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.303 | 1.519 | 2.833 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.303 | 1.472 | 2.923 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.303 | 1.387 | 3.102 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.303 | 1.419 | 3.032 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.303 | 1.478 | 2.911 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `ax` | `profile_balanced` | 0.929 | 1.548 | 0.600 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `ax` | `profile_fast` | 0.929 | 1.584 | 0.586 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.929 | 1.253 | 0.741 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `ax` | `skip_source_error_control` | 0.929 | 1.360 | 0.683 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `ax` | `strict_current` | 0.929 | 1.571 | 0.591 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `classic` | `profile_balanced` | 4.206 | 1.548 | 2.716 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `classic` | `profile_fast` | 4.206 | 1.584 | 2.655 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.206 | 1.253 | 3.356 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `classic` | `skip_source_error_control` | 4.206 | 1.360 | 3.093 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `classic` | `strict_current` | 4.206 | 1.571 | 2.676 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `ax` | `profile_balanced` | 0.912 | 1.512 | 0.603 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `ax` | `profile_fast` | 0.912 | 1.459 | 0.625 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.912 | 1.307 | 0.698 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 0.912 | 1.437 | 0.635 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `ax` | `strict_current` | 0.912 | 1.596 | 0.572 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.374 | 1.512 | 2.892 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `classic` | `profile_fast` | 4.374 | 1.459 | 2.997 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.374 | 1.307 | 3.347 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.374 | 1.437 | 3.044 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `classic` | `strict_current` | 4.374 | 1.596 | 2.740 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `ax` | `profile_balanced` | 1.137 | 1.543 | 0.737 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `ax` | `profile_fast` | 1.137 | 1.552 | 0.732 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.137 | 1.284 | 0.885 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.137 | 1.311 | 0.867 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `ax` | `strict_current` | 1.137 | 1.688 | 0.674 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `classic` | `profile_balanced` | 4.396 | 1.543 | 2.848 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `classic` | `profile_fast` | 4.396 | 1.552 | 2.832 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.396 | 1.284 | 3.423 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.396 | 1.311 | 3.352 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `classic` | `strict_current` | 4.396 | 1.688 | 2.605 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `ax` | `profile_balanced` | 1.041 | 0.980 | 1.062 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `ax` | `profile_fast` | 1.041 | 0.662 | 1.572 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.041 | 0.646 | 1.611 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.041 | 0.633 | 1.644 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `ax` | `strict_current` | 1.041 | 1.000 | 1.041 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `classic` | `profile_balanced` | 2.488 | 0.980 | 2.539 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `classic` | `profile_fast` | 2.488 | 0.662 | 3.756 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.488 | 0.646 | 3.849 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `classic` | `skip_source_error_control` | 2.488 | 0.633 | 3.929 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `classic` | `strict_current` | 2.488 | 1.000 | 2.487 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.671 | 0.571 | 2.929 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `ax` | `profile_fast` | 1.671 | 0.549 | 3.046 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.671 | 0.608 | 2.749 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.671 | 0.652 | 2.562 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `ax` | `strict_current` | 1.671 | 0.521 | 3.206 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `classic` | `profile_balanced` | 3.837 | 0.571 | 6.724 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `classic` | `profile_fast` | 3.837 | 0.549 | 6.993 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.837 | 0.608 | 6.311 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 3.837 | 0.652 | 5.883 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `classic` | `strict_current` | 3.837 | 0.521 | 7.362 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `ax` | `profile_balanced` | 1.231 | 0.691 | 1.781 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `ax` | `profile_fast` | 1.231 | 0.722 | 1.704 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.231 | 0.667 | 1.846 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.231 | 0.754 | 1.632 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `ax` | `strict_current` | 1.231 | 0.810 | 1.520 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `classic` | `profile_balanced` | 3.010 | 0.691 | 4.357 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `classic` | `profile_fast` | 3.010 | 0.722 | 4.168 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.010 | 0.667 | 4.514 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `classic` | `skip_source_error_control` | 3.010 | 0.754 | 3.992 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `classic` | `strict_current` | 3.010 | 0.810 | 3.718 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.216 | 2.654 | 0.458 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.216 | 1.597 | 0.761 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.216 | 0.535 | 2.273 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.216 | 0.739 | 1.645 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.216 | 2.611 | 0.466 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 8.410 | 2.654 | 3.169 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `classic` | `profile_fast` | 8.410 | 1.597 | 5.265 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 8.410 | 0.535 | 15.727 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 8.410 | 0.739 | 11.379 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `classic` | `strict_current` | 8.410 | 2.611 | 3.221 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `ax` | `profile_balanced` | 1.171 | 2.563 | 0.457 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `ax` | `profile_fast` | 1.171 | 1.563 | 0.750 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.171 | 0.576 | 2.032 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.171 | 0.657 | 1.784 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `ax` | `strict_current` | 1.171 | 2.470 | 0.474 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `classic` | `profile_balanced` | 8.274 | 2.563 | 3.229 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `classic` | `profile_fast` | 8.274 | 1.563 | 5.295 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 8.274 | 0.576 | 14.356 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `classic` | `skip_source_error_control` | 8.274 | 0.657 | 12.601 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `classic` | `strict_current` | 8.274 | 2.470 | 3.350 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `ax` | `profile_balanced` | 0.810 | 2.526 | 0.321 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `ax` | `profile_fast` | 0.810 | 1.514 | 0.535 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.810 | 0.592 | 1.367 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 0.810 | 0.729 | 1.110 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `ax` | `strict_current` | 0.810 | 2.583 | 0.313 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `classic` | `profile_balanced` | 8.328 | 2.526 | 3.297 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `classic` | `profile_fast` | 8.328 | 1.514 | 5.500 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 8.328 | 0.592 | 14.060 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 8.328 | 0.729 | 11.419 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `classic` | `strict_current` | 8.328 | 2.583 | 3.224 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `ax` | `profile_balanced` | 1.048 | 2.493 | 0.420 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `ax` | `profile_fast` | 1.048 | 1.559 | 0.672 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.048 | 0.632 | 1.660 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.048 | 0.668 | 1.569 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `ax` | `strict_current` | 1.048 | 2.564 | 0.409 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `classic` | `profile_balanced` | 8.356 | 2.493 | 3.351 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `classic` | `profile_fast` | 8.356 | 1.559 | 5.358 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 8.356 | 0.632 | 13.230 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `classic` | `skip_source_error_control` | 8.356 | 0.668 | 12.505 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `classic` | `strict_current` | 8.356 | 2.564 | 3.259 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 3.598 | 0.934 | 3.852 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `ax` | `profile_fast` | 3.598 | 0.674 | 5.336 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 3.598 | 0.696 | 5.166 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 3.598 | 0.696 | 5.168 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 3.598 | 0.944 | 3.812 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 5.065 | 0.934 | 5.423 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `classic` | `profile_fast` | 5.065 | 0.674 | 7.512 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 5.065 | 0.696 | 7.273 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 5.065 | 0.696 | 7.277 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 5.065 | 0.944 | 5.367 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `ax` | `profile_balanced` | 4.267 | 0.794 | 5.376 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `ax` | `profile_fast` | 4.267 | 0.823 | 5.186 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 4.267 | 0.662 | 6.445 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `ax` | `skip_source_error_control` | 4.267 | 0.715 | 5.965 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `ax` | `strict_current` | 4.267 | 0.839 | 5.088 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `classic` | `profile_balanced` | 5.375 | 0.794 | 6.771 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `classic` | `profile_fast` | 5.375 | 0.823 | 6.533 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.375 | 0.662 | 8.119 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `classic` | `skip_source_error_control` | 5.375 | 0.715 | 7.513 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `classic` | `strict_current` | 5.375 | 0.839 | 6.409 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.480 | 0.678 | 2.182 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `ax` | `profile_fast` | 1.480 | 0.572 | 2.587 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.480 | 0.624 | 2.370 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.480 | 0.840 | 1.761 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `ax` | `strict_current` | 1.480 | 0.742 | 1.995 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `classic` | `profile_balanced` | 5.434 | 0.678 | 8.012 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `classic` | `profile_fast` | 5.434 | 0.572 | 9.498 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.434 | 0.624 | 8.703 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 5.434 | 0.840 | 6.466 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `classic` | `strict_current` | 5.434 | 0.742 | 7.326 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `ax` | `profile_balanced` | 3.851 | 0.942 | 4.087 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `ax` | `profile_fast` | 3.851 | 0.715 | 5.385 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 3.851 | 0.656 | 5.871 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `ax` | `skip_source_error_control` | 3.851 | 0.759 | 5.075 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `ax` | `strict_current` | 3.851 | 1.000 | 3.851 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `classic` | `profile_balanced` | 5.515 | 0.942 | 5.853 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `classic` | `profile_fast` | 5.515 | 0.715 | 7.713 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.515 | 0.656 | 8.408 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `classic` | `skip_source_error_control` | 5.515 | 0.759 | 7.269 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `classic` | `strict_current` | 5.515 | 1.000 | 5.516 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `ax` | `profile_balanced` | 0.870 | 1.426 | 0.610 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `ax` | `profile_fast` | 0.870 | 1.110 | 0.784 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.870 | 1.027 | 0.847 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 0.870 | 1.169 | 0.744 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `ax` | `strict_current` | 0.870 | 4.645 | 0.187 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `classic` | `profile_balanced` | 3.761 | 1.426 | 2.637 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `classic` | `profile_fast` | 3.761 | 1.110 | 3.389 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.761 | 1.027 | 3.662 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 3.761 | 1.169 | 3.218 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `classic` | `strict_current` | 3.761 | 4.645 | 0.810 |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `ax` | `profile_balanced` | 0.723 | 1.375 | 0.526 |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `ax` | `profile_fast` | 0.723 | 1.098 | 0.658 |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.723 | 1.016 | 0.711 |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `ax` | `skip_source_error_control` | 0.723 | 0.963 | 0.750 |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `ax` | `strict_current` | 0.723 | 4.572 | 0.158 |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `classic` | `profile_balanced` | 3.377 | 1.375 | 2.456 |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `classic` | `profile_fast` | 3.377 | 1.098 | 3.076 |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.377 | 1.016 | 3.324 |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `classic` | `skip_source_error_control` | 3.377 | 0.963 | 3.507 |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `classic` | `strict_current` | 3.377 | 4.572 | 0.739 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.176 | 0.867 | 1.357 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.176 | 0.825 | 1.426 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.176 | 0.746 | 1.577 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.176 | 0.803 | 1.465 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.176 | 0.892 | 1.319 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.681 | 0.867 | 5.402 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.681 | 0.825 | 5.675 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.681 | 0.746 | 6.275 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.681 | 0.803 | 5.830 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.681 | 0.892 | 5.249 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `ax` | `profile_balanced` | 1.163 | 0.736 | 1.581 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `ax` | `profile_fast` | 1.163 | 0.582 | 1.997 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.163 | 0.651 | 1.787 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.163 | 0.605 | 1.922 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `ax` | `strict_current` | 1.163 | 0.763 | 1.523 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `classic` | `profile_balanced` | 4.864 | 0.736 | 6.611 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `classic` | `profile_fast` | 4.864 | 0.582 | 8.351 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.864 | 0.651 | 7.473 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `classic` | `skip_source_error_control` | 4.864 | 0.605 | 8.038 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `classic` | `strict_current` | 4.864 | 0.763 | 6.372 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `ax` | `profile_balanced` | 0.974 | 0.806 | 1.208 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `ax` | `profile_fast` | 0.974 | 0.784 | 1.243 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.974 | 0.781 | 1.247 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 0.974 | 0.762 | 1.278 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `ax` | `strict_current` | 0.974 | 0.821 | 1.186 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.627 | 0.806 | 5.738 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `classic` | `profile_fast` | 4.627 | 0.784 | 5.905 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.627 | 0.781 | 5.922 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.627 | 0.762 | 6.072 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `classic` | `strict_current` | 4.627 | 0.821 | 5.634 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `ax` | `profile_balanced` | 1.044 | 0.679 | 1.538 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `ax` | `profile_fast` | 1.044 | 0.642 | 1.626 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.044 | 0.633 | 1.650 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.044 | 0.629 | 1.660 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `ax` | `strict_current` | 1.044 | 0.822 | 1.270 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `classic` | `profile_balanced` | 4.801 | 0.679 | 7.073 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `classic` | `profile_fast` | 4.801 | 0.642 | 7.481 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.801 | 0.633 | 7.588 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.801 | 0.629 | 7.638 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `classic` | `strict_current` | 4.801 | 0.822 | 5.840 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.089 | 0.903 | 1.205 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.089 | 0.780 | 1.396 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.089 | 0.614 | 1.773 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.089 | 0.614 | 1.772 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.089 | 1.008 | 1.080 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.697 | 0.903 | 5.201 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.697 | 0.780 | 6.023 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.697 | 0.614 | 7.652 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.697 | 0.614 | 7.647 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.697 | 1.008 | 4.661 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `ax` | `profile_balanced` | 0.946 | 0.684 | 1.382 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `ax` | `profile_fast` | 0.946 | 0.711 | 1.330 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.946 | 0.651 | 1.451 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `ax` | `skip_source_error_control` | 0.946 | 0.636 | 1.486 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `ax` | `strict_current` | 0.946 | 0.777 | 1.216 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `classic` | `profile_balanced` | 4.769 | 0.684 | 6.972 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `classic` | `profile_fast` | 4.769 | 0.711 | 6.708 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.769 | 0.651 | 7.320 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `classic` | `skip_source_error_control` | 4.769 | 0.636 | 7.496 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `classic` | `strict_current` | 4.769 | 0.777 | 6.134 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.646 | 0.733 | 2.244 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `ax` | `profile_fast` | 1.646 | 0.681 | 2.415 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.646 | 0.565 | 2.912 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.646 | 0.645 | 2.551 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `ax` | `strict_current` | 1.646 | 0.756 | 2.176 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `classic` | `profile_balanced` | 5.230 | 0.733 | 7.134 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `classic` | `profile_fast` | 5.230 | 0.681 | 7.675 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.230 | 0.565 | 9.257 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 5.230 | 0.645 | 8.110 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `classic` | `strict_current` | 5.230 | 0.756 | 6.916 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `ax` | `profile_balanced` | 1.040 | 0.816 | 1.276 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `ax` | `profile_fast` | 1.040 | 0.658 | 1.581 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.040 | 0.564 | 1.845 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.040 | 0.607 | 1.714 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `ax` | `strict_current` | 1.040 | 0.981 | 1.060 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `classic` | `profile_balanced` | 4.595 | 0.816 | 5.635 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `classic` | `profile_fast` | 4.595 | 0.658 | 6.983 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.595 | 0.564 | 8.151 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.595 | 0.607 | 7.570 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `classic` | `strict_current` | 4.595 | 0.981 | 4.683 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 2.925 | 0.972 | 3.009 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `ax` | `profile_fast` | 2.925 | 0.988 | 2.960 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 2.925 | 0.957 | 3.056 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 2.925 | 0.946 | 3.092 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `ax` | `strict_current` | 2.925 | 1.077 | 2.717 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 2.837 | 0.972 | 2.918 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `classic` | `profile_fast` | 2.837 | 0.988 | 2.871 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 2.837 | 0.957 | 2.964 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 2.837 | 0.946 | 2.999 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `classic` | `strict_current` | 2.837 | 1.077 | 2.635 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `ax` | `profile_balanced` | 0.913 | 0.859 | 1.063 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `ax` | `profile_fast` | 0.913 | 0.919 | 0.993 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.913 | 0.772 | 1.183 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `ax` | `skip_source_error_control` | 0.913 | 0.821 | 1.113 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `ax` | `strict_current` | 0.913 | 0.837 | 1.091 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `classic` | `profile_balanced` | 2.277 | 0.859 | 2.649 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `classic` | `profile_fast` | 2.277 | 0.919 | 2.476 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.277 | 0.772 | 2.949 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `classic` | `skip_source_error_control` | 2.277 | 0.821 | 2.774 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `classic` | `strict_current` | 2.277 | 0.837 | 2.719 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `ax` | `profile_balanced` | 3.089 | 0.952 | 3.246 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `ax` | `profile_fast` | 3.089 | 0.893 | 3.460 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 3.089 | 0.812 | 3.803 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 3.089 | 0.893 | 3.460 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `ax` | `strict_current` | 3.089 | 0.796 | 3.879 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `classic` | `profile_balanced` | 2.789 | 0.952 | 2.931 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `classic` | `profile_fast` | 2.789 | 0.893 | 3.124 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.789 | 0.812 | 3.434 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 2.789 | 0.893 | 3.124 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `classic` | `strict_current` | 2.789 | 0.796 | 3.502 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `ax` | `profile_balanced` | 0.914 | 0.902 | 1.013 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `ax` | `profile_fast` | 0.914 | 0.890 | 1.026 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.914 | 0.740 | 1.235 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `ax` | `skip_source_error_control` | 0.914 | 0.890 | 1.027 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `ax` | `strict_current` | 0.914 | 1.004 | 0.910 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `classic` | `profile_balanced` | 2.345 | 0.902 | 2.600 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `classic` | `profile_fast` | 2.345 | 0.890 | 2.634 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.345 | 0.740 | 3.168 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `classic` | `skip_source_error_control` | 2.345 | 0.890 | 2.636 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `classic` | `strict_current` | 2.345 | 1.004 | 2.336 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `ax` | `profile_balanced` | 5.736 | 126.899 | 0.045 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `ax` | `profile_fast` | 5.736 | 107.294 | 0.053 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.736 | 11.311 | 0.507 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 5.736 | 11.323 | 0.507 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `ax` | `strict_current` | 5.736 | 128.977 | 0.044 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `classic` | `profile_balanced` | 13.116 | 126.899 | 0.103 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `classic` | `profile_fast` | 13.116 | 107.294 | 0.122 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.116 | 11.311 | 1.160 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 13.116 | 11.323 | 1.158 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `classic` | `strict_current` | 13.116 | 128.977 | 0.102 |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `ax` | `profile_balanced` | 4.784 | 151.214 | 0.032 |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `ax` | `profile_fast` | 4.784 | 132.261 | 0.036 |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 4.784 | 32.723 | 0.146 |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `ax` | `skip_source_error_control` | 4.784 | 34.644 | 0.138 |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `ax` | `strict_current` | 4.784 | 154.555 | 0.031 |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `classic` | `profile_balanced` | 11.678 | 151.214 | 0.077 |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `classic` | `profile_fast` | 11.678 | 132.261 | 0.088 |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 11.678 | 32.723 | 0.357 |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `classic` | `skip_source_error_control` | 11.678 | 34.644 | 0.337 |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `classic` | `strict_current` | 11.678 | 154.555 | 0.076 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 2.402 | 1.528 | 1.572 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `ax` | `profile_fast` | 2.402 | 1.062 | 2.262 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 2.402 | 0.874 | 2.749 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 2.402 | 0.868 | 2.769 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `ax` | `strict_current` | 2.402 | 1.514 | 1.586 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 2.365 | 1.528 | 1.547 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `classic` | `profile_fast` | 2.365 | 1.062 | 2.226 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 2.365 | 0.874 | 2.707 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 2.365 | 0.868 | 2.726 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `classic` | `strict_current` | 2.365 | 1.514 | 1.562 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `ax` | `profile_balanced` | 2.595 | 1.386 | 1.872 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `ax` | `profile_fast` | 2.595 | 0.959 | 2.705 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 2.595 | 0.947 | 2.740 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `ax` | `skip_source_error_control` | 2.595 | 0.811 | 3.200 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `ax` | `strict_current` | 2.595 | 1.453 | 1.786 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `classic` | `profile_balanced` | 2.565 | 1.386 | 1.850 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `classic` | `profile_fast` | 2.565 | 0.959 | 2.674 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.565 | 0.947 | 2.709 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `classic` | `skip_source_error_control` | 2.565 | 0.811 | 3.163 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `classic` | `strict_current` | 2.565 | 1.453 | 1.766 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.493 | 1.410 | 1.058 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `ax` | `profile_fast` | 1.493 | 1.109 | 1.346 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.493 | 0.902 | 1.655 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.493 | 0.913 | 1.636 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `ax` | `strict_current` | 1.493 | 1.497 | 0.997 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `classic` | `profile_balanced` | 2.919 | 1.410 | 2.069 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `classic` | `profile_fast` | 2.919 | 1.109 | 2.632 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.919 | 0.902 | 3.237 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 2.919 | 0.913 | 3.198 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `classic` | `strict_current` | 2.919 | 1.497 | 1.950 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `ax` | `profile_balanced` | 0.913 | 1.450 | 0.630 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `ax` | `profile_fast` | 0.913 | 0.993 | 0.919 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.913 | 0.891 | 1.025 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `ax` | `skip_source_error_control` | 0.913 | 0.890 | 1.026 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `ax` | `strict_current` | 0.913 | 1.538 | 0.594 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `classic` | `profile_balanced` | 2.527 | 1.450 | 1.744 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `classic` | `profile_fast` | 2.527 | 0.993 | 2.545 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.527 | 0.891 | 2.838 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `classic` | `skip_source_error_control` | 2.527 | 0.890 | 2.840 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `classic` | `strict_current` | 2.527 | 1.538 | 1.643 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.304 | 1.192 | 1.094 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.304 | 0.873 | 1.494 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.304 | 0.597 | 2.185 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.304 | 0.610 | 2.137 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.304 | 1.366 | 0.954 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.770 | 1.192 | 4.001 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.770 | 0.873 | 5.465 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.770 | 0.597 | 7.995 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.770 | 0.610 | 7.817 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.770 | 1.366 | 3.492 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `ax` | `profile_balanced` | 1.091 | 1.284 | 0.849 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `ax` | `profile_fast` | 1.091 | 0.957 | 1.140 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.091 | 0.624 | 1.749 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.091 | 0.715 | 1.526 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `ax` | `strict_current` | 1.091 | 1.319 | 0.827 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `classic` | `profile_balanced` | 5.418 | 1.284 | 4.218 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `classic` | `profile_fast` | 5.418 | 0.957 | 5.660 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.418 | 0.624 | 8.683 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `classic` | `skip_source_error_control` | 5.418 | 0.715 | 7.579 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `classic` | `strict_current` | 5.418 | 1.319 | 4.108 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.087 | 1.119 | 0.971 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `ax` | `profile_fast` | 1.087 | 0.814 | 1.335 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.087 | 0.669 | 1.625 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.087 | 0.635 | 1.711 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `ax` | `strict_current` | 1.087 | 1.260 | 0.863 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `classic` | `profile_balanced` | 5.069 | 1.119 | 4.529 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `classic` | `profile_fast` | 5.069 | 0.814 | 6.226 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.069 | 0.669 | 7.579 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 5.069 | 0.635 | 7.981 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `classic` | `strict_current` | 5.069 | 1.260 | 4.024 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `ax` | `profile_balanced` | 0.969 | 1.357 | 0.714 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `ax` | `profile_fast` | 0.969 | 0.895 | 1.083 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.969 | 0.594 | 1.633 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `ax` | `skip_source_error_control` | 0.969 | 0.659 | 1.471 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `ax` | `strict_current` | 0.969 | 1.399 | 0.693 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `classic` | `profile_balanced` | 4.158 | 1.357 | 3.064 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `classic` | `profile_fast` | 4.158 | 0.895 | 4.649 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.158 | 0.594 | 7.005 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.158 | 0.659 | 6.311 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `classic` | `strict_current` | 4.158 | 1.399 | 2.972 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.107 | 0.910 | 1.216 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.107 | 0.794 | 1.395 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.107 | 0.852 | 1.299 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.107 | 0.747 | 1.482 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.107 | 1.143 | 0.969 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.738 | 0.910 | 5.205 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.738 | 0.794 | 5.968 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.738 | 0.852 | 5.560 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.738 | 0.747 | 6.341 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.738 | 1.143 | 4.145 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `ax` | `profile_balanced` | 1.458 | 0.822 | 1.775 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `ax` | `profile_fast` | 1.458 | 0.901 | 1.618 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.458 | 0.967 | 1.507 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.458 | 0.990 | 1.473 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `ax` | `strict_current` | 1.458 | 0.874 | 1.668 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `classic` | `profile_balanced` | 5.006 | 0.822 | 6.093 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `classic` | `profile_fast` | 5.006 | 0.901 | 5.554 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.006 | 0.967 | 5.175 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `classic` | `skip_source_error_control` | 5.006 | 0.990 | 5.057 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `classic` | `strict_current` | 5.006 | 0.874 | 5.726 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.113 | 0.824 | 1.352 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `ax` | `profile_fast` | 1.113 | 0.815 | 1.366 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.113 | 0.847 | 1.313 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.113 | 0.883 | 1.261 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 1.113 | 0.891 | 1.249 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `classic` | `profile_balanced` | 5.325 | 0.824 | 6.466 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `classic` | `profile_fast` | 5.325 | 0.815 | 6.534 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.325 | 0.847 | 6.284 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 5.325 | 0.883 | 6.031 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 5.325 | 0.891 | 5.975 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `ax` | `profile_balanced` | 1.098 | 0.860 | 1.276 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `ax` | `profile_fast` | 1.098 | 0.802 | 1.369 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.098 | 0.688 | 1.597 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.098 | 0.803 | 1.367 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `ax` | `strict_current` | 1.098 | 1.003 | 1.095 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `classic` | `profile_balanced` | 4.896 | 0.860 | 5.690 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `classic` | `profile_fast` | 4.896 | 0.802 | 6.107 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.896 | 0.688 | 7.121 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.896 | 0.803 | 6.096 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `classic` | `strict_current` | 4.896 | 1.003 | 4.883 |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 0.843 | 4.787 | 0.176 |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `ax` | `profile_fast` | 0.843 | 2.250 | 0.375 |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 0.843 | 1.642 | 0.513 |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 0.843 | 1.663 | 0.507 |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `ax` | `strict_current` | 0.843 | 4.556 | 0.185 |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.209 | 4.787 | 0.879 |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.209 | 2.250 | 1.871 |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.209 | 1.642 | 2.563 |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.209 | 1.663 | 2.531 |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.209 | 4.556 | 0.924 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `ax` | `profile_balanced` | 1.056 | 4.568 | 0.231 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `ax` | `profile_fast` | 1.056 | 2.153 | 0.491 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.056 | 1.470 | 0.719 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.056 | 1.507 | 0.701 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `ax` | `strict_current` | 1.056 | 4.619 | 0.229 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `classic` | `profile_balanced` | 4.077 | 4.568 | 0.893 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `classic` | `profile_fast` | 4.077 | 2.153 | 1.894 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.077 | 1.470 | 2.774 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `classic` | `skip_source_error_control` | 4.077 | 1.507 | 2.706 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `classic` | `strict_current` | 4.077 | 4.619 | 0.883 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.350 | 2.679 | 0.504 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `ax` | `profile_fast` | 1.350 | 2.712 | 0.498 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.350 | 1.388 | 0.973 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.350 | 1.390 | 0.972 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `ax` | `strict_current` | 1.350 | 2.709 | 0.498 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `classic` | `profile_balanced` | 3.884 | 2.679 | 1.450 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `classic` | `profile_fast` | 3.884 | 2.712 | 1.432 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.884 | 1.388 | 2.797 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 3.884 | 1.390 | 2.794 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `classic` | `strict_current` | 3.884 | 2.709 | 1.434 |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `ax` | `profile_balanced` | 0.859 | 2.743 | 0.313 |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `ax` | `profile_fast` | 0.859 | 2.654 | 0.324 |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.859 | 1.359 | 0.632 |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `ax` | `skip_source_error_control` | 0.859 | 1.655 | 0.519 |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `ax` | `strict_current` | 0.859 | 2.719 | 0.316 |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `classic` | `profile_balanced` | 3.887 | 2.743 | 1.417 |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `classic` | `profile_fast` | 3.887 | 2.654 | 1.464 |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.887 | 1.359 | 2.860 |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `classic` | `skip_source_error_control` | 3.887 | 1.655 | 2.348 |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `classic` | `strict_current` | 3.887 | 2.719 | 1.429 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 3.094 | 0.875 | 3.536 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `ax` | `profile_fast` | 3.094 | 0.708 | 4.371 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 3.094 | 0.862 | 3.590 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 3.094 | 0.669 | 4.621 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 3.094 | 0.870 | 3.557 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.349 | 0.875 | 4.971 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.349 | 0.708 | 6.145 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.349 | 0.862 | 5.047 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.349 | 0.669 | 6.497 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.349 | 0.870 | 5.000 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `ax` | `profile_balanced` | 1.283 | 0.835 | 1.536 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `ax` | `profile_fast` | 1.283 | 0.803 | 1.598 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.283 | 0.665 | 1.930 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.283 | 0.773 | 1.660 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `ax` | `strict_current` | 1.283 | 0.877 | 1.463 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `classic` | `profile_balanced` | 5.012 | 0.835 | 6.000 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `classic` | `profile_fast` | 5.012 | 0.803 | 6.242 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.012 | 0.665 | 7.539 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `classic` | `skip_source_error_control` | 5.012 | 0.773 | 6.485 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `classic` | `strict_current` | 5.012 | 0.877 | 5.715 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `ax` | `profile_balanced` | 3.476 | 0.884 | 3.932 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `ax` | `profile_fast` | 3.476 | 0.677 | 5.132 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 3.476 | 0.625 | 5.562 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 3.476 | 0.629 | 5.522 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `ax` | `strict_current` | 3.476 | 0.766 | 4.537 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.940 | 0.884 | 5.587 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `classic` | `profile_fast` | 4.940 | 0.677 | 7.294 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.940 | 0.625 | 7.905 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.940 | 0.629 | 7.847 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `classic` | `strict_current` | 4.940 | 0.766 | 6.448 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `ax` | `profile_balanced` | 1.261 | 0.867 | 1.454 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `ax` | `profile_fast` | 1.261 | 0.812 | 1.553 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.261 | 0.788 | 1.601 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.261 | 0.819 | 1.540 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `ax` | `strict_current` | 1.261 | 0.879 | 1.434 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `classic` | `profile_balanced` | 5.110 | 0.867 | 5.891 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `classic` | `profile_fast` | 5.110 | 0.812 | 6.295 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.110 | 0.788 | 6.488 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `classic` | `skip_source_error_control` | 5.110 | 0.819 | 6.239 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `classic` | `strict_current` | 5.110 | 0.879 | 5.810 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 0.835 | 1.514 | 0.552 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `ax` | `profile_fast` | 0.835 | 1.014 | 0.824 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 0.835 | 0.580 | 1.440 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 0.835 | 0.588 | 1.420 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `ax` | `strict_current` | 0.835 | 1.541 | 0.542 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.250 | 1.514 | 2.807 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.250 | 1.014 | 4.193 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.250 | 0.580 | 7.326 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.250 | 0.588 | 7.223 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.250 | 1.541 | 2.758 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `ax` | `profile_balanced` | 0.910 | 1.351 | 0.674 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `ax` | `profile_fast` | 0.910 | 0.972 | 0.937 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.910 | 0.560 | 1.625 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `ax` | `skip_source_error_control` | 0.910 | 0.573 | 1.589 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `ax` | `strict_current` | 0.910 | 1.389 | 0.655 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `classic` | `profile_balanced` | 5.051 | 1.351 | 3.739 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `classic` | `profile_fast` | 5.051 | 0.972 | 5.199 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.051 | 0.560 | 9.023 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `classic` | `skip_source_error_control` | 5.051 | 0.573 | 8.820 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `classic` | `strict_current` | 5.051 | 1.389 | 3.635 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.184 | 1.499 | 0.790 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `ax` | `profile_fast` | 1.184 | 0.927 | 1.277 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.184 | 0.763 | 1.551 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.184 | 0.685 | 1.729 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `ax` | `strict_current` | 1.184 | 1.537 | 0.771 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.635 | 1.499 | 3.091 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `classic` | `profile_fast` | 4.635 | 0.927 | 4.998 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.635 | 0.763 | 6.071 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.635 | 0.685 | 6.769 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `classic` | `strict_current` | 4.635 | 1.537 | 3.016 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `ax` | `profile_balanced` | 0.883 | 1.615 | 0.547 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `ax` | `profile_fast` | 0.883 | 1.052 | 0.839 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.883 | 0.543 | 1.626 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `ax` | `skip_source_error_control` | 0.883 | 0.634 | 1.392 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `ax` | `strict_current` | 0.883 | 1.570 | 0.562 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `classic` | `profile_balanced` | 4.803 | 1.615 | 2.974 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `classic` | `profile_fast` | 4.803 | 1.052 | 4.565 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.803 | 0.543 | 8.846 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.803 | 0.634 | 7.576 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `classic` | `strict_current` | 4.803 | 1.570 | 3.059 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 3.436 | 0.943 | 3.644 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast` | 3.436 | 1.066 | 3.222 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 3.436 | 0.891 | 3.854 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 3.436 | 0.985 | 3.489 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 3.436 | 1.012 | 3.396 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 3.295 | 0.943 | 3.494 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast` | 3.295 | 1.066 | 3.090 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 3.295 | 0.891 | 3.696 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 3.295 | 0.985 | 3.346 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 3.295 | 1.012 | 3.257 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `ax` | `profile_balanced` | 2.599 | 1.021 | 2.546 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `ax` | `profile_fast` | 2.599 | 0.968 | 2.686 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 2.599 | 0.876 | 2.966 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `ax` | `skip_source_error_control` | 2.599 | 0.828 | 3.140 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `ax` | `strict_current` | 2.599 | 1.117 | 2.326 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `classic` | `profile_balanced` | 2.592 | 1.021 | 2.540 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `classic` | `profile_fast` | 2.592 | 0.968 | 2.679 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.592 | 0.876 | 2.959 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `classic` | `skip_source_error_control` | 2.592 | 0.828 | 3.132 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `classic` | `strict_current` | 2.592 | 1.117 | 2.320 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `ax` | `profile_balanced` | 0.869 | 1.206 | 0.721 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `ax` | `profile_fast` | 0.869 | 1.152 | 0.755 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.869 | 0.974 | 0.892 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 0.869 | 0.993 | 0.875 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 0.869 | 1.387 | 0.627 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `classic` | `profile_balanced` | 2.812 | 1.206 | 2.331 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `classic` | `profile_fast` | 2.812 | 1.152 | 2.441 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.812 | 0.974 | 2.887 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 2.812 | 0.993 | 2.830 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 2.812 | 1.387 | 2.027 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `ax` | `profile_balanced` | 1.399 | 0.990 | 1.413 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `ax` | `profile_fast` | 1.399 | 1.069 | 1.309 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.399 | 0.963 | 1.453 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.399 | 0.946 | 1.478 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `ax` | `strict_current` | 1.399 | 1.079 | 1.297 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `classic` | `profile_balanced` | 3.213 | 0.990 | 3.244 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `classic` | `profile_fast` | 3.213 | 1.069 | 3.006 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.213 | 0.963 | 3.337 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `classic` | `skip_source_error_control` | 3.213 | 0.946 | 3.395 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `classic` | `strict_current` | 3.213 | 1.079 | 2.978 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.357 | 0.868 | 1.564 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.357 | 0.771 | 1.761 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.357 | 0.738 | 1.839 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.357 | 0.678 | 2.002 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.357 | 0.911 | 1.490 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.887 | 0.868 | 5.632 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.887 | 0.771 | 6.341 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.887 | 0.738 | 6.624 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.887 | 0.678 | 7.211 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.887 | 0.911 | 5.365 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `ax` | `profile_balanced` | 1.457 | 0.718 | 2.030 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `ax` | `profile_fast` | 1.457 | 0.632 | 2.306 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.457 | 0.788 | 1.849 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.457 | 0.606 | 2.404 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `ax` | `strict_current` | 1.457 | 0.842 | 1.731 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `classic` | `profile_balanced` | 5.920 | 0.718 | 8.250 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `classic` | `profile_fast` | 5.920 | 0.632 | 9.373 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.920 | 0.788 | 7.512 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `classic` | `skip_source_error_control` | 5.920 | 0.606 | 9.769 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `classic` | `strict_current` | 5.920 | 0.842 | 7.033 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.447 | 0.845 | 1.712 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `ax` | `profile_fast` | 1.447 | 0.750 | 1.930 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.447 | 0.712 | 2.033 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.447 | 0.704 | 2.056 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `ax` | `strict_current` | 1.447 | 0.809 | 1.788 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `classic` | `profile_balanced` | 5.382 | 0.845 | 6.368 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `classic` | `profile_fast` | 5.382 | 0.750 | 7.180 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.382 | 0.712 | 7.563 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 5.382 | 0.704 | 7.648 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `classic` | `strict_current` | 5.382 | 0.809 | 6.653 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `ax` | `profile_balanced` | 0.888 | 0.731 | 1.214 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `ax` | `profile_fast` | 0.888 | 0.683 | 1.300 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.888 | 0.648 | 1.369 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `ax` | `skip_source_error_control` | 0.888 | 0.569 | 1.559 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `ax` | `strict_current` | 0.888 | 0.917 | 0.968 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `classic` | `profile_balanced` | 4.393 | 0.731 | 6.006 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `classic` | `profile_fast` | 4.393 | 0.683 | 6.431 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.393 | 0.648 | 6.775 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.393 | 0.569 | 7.715 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `classic` | `strict_current` | 4.393 | 0.917 | 4.791 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 0.893 | 0.777 | 1.150 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `ax` | `profile_fast` | 0.893 | 0.642 | 1.390 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 0.893 | 0.701 | 1.273 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 0.893 | 0.646 | 1.383 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 0.893 | 0.771 | 1.158 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 2.721 | 0.777 | 3.504 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `classic` | `profile_fast` | 2.721 | 0.642 | 4.237 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 2.721 | 0.701 | 3.880 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 2.721 | 0.646 | 4.215 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 2.721 | 0.771 | 3.531 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `ax` | `profile_balanced` | 0.952 | 0.852 | 1.118 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `ax` | `profile_fast` | 0.952 | 0.671 | 1.420 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.952 | 0.649 | 1.466 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `ax` | `skip_source_error_control` | 0.952 | 0.651 | 1.462 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `ax` | `strict_current` | 0.952 | 0.865 | 1.101 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `classic` | `profile_balanced` | 2.735 | 0.852 | 3.212 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `classic` | `profile_fast` | 2.735 | 0.671 | 4.079 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.735 | 0.649 | 4.212 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `classic` | `skip_source_error_control` | 2.735 | 0.651 | 4.200 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `classic` | `strict_current` | 2.735 | 0.865 | 3.161 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.414 | 0.797 | 1.774 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `ax` | `profile_fast` | 1.414 | 0.714 | 1.979 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.414 | 0.662 | 2.134 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.414 | 0.623 | 2.269 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `ax` | `strict_current` | 1.414 | 0.980 | 1.443 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `classic` | `profile_balanced` | 3.151 | 0.797 | 3.956 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `classic` | `profile_fast` | 3.151 | 0.714 | 4.412 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.151 | 0.662 | 4.757 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 3.151 | 0.623 | 5.057 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `classic` | `strict_current` | 3.151 | 0.980 | 3.217 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `ax` | `profile_balanced` | 1.153 | 0.806 | 1.431 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `ax` | `profile_fast` | 1.153 | 0.729 | 1.583 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.153 | 0.675 | 1.708 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.153 | 0.641 | 1.799 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `ax` | `strict_current` | 1.153 | 0.905 | 1.274 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `classic` | `profile_balanced` | 2.946 | 0.806 | 3.656 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `classic` | `profile_fast` | 2.946 | 0.729 | 4.044 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.946 | 0.675 | 4.364 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `classic` | `skip_source_error_control` | 2.946 | 0.641 | 4.596 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `classic` | `strict_current` | 2.946 | 0.905 | 3.254 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 0.907 | 21.950 | 0.041 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `ax` | `profile_fast` | 0.907 | 17.204 | 0.053 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 0.907 | 15.787 | 0.057 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 0.907 | 24.569 | 0.037 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `ax` | `strict_current` | 0.907 | 32.764 | 0.028 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 3.988 | 21.950 | 0.182 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `classic` | `profile_fast` | 3.988 | 17.204 | 0.232 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 3.988 | 15.787 | 0.253 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 3.988 | 24.569 | 0.162 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `classic` | `strict_current` | 3.988 | 32.764 | 0.122 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `ax` | `profile_balanced` | 0.605 | 22.400 | 0.027 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `ax` | `profile_fast` | 0.605 | 17.252 | 0.035 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.605 | 15.603 | 0.039 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `ax` | `skip_source_error_control` | 0.605 | 23.802 | 0.025 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `ax` | `strict_current` | 0.605 | 33.563 | 0.018 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `classic` | `profile_balanced` | 3.941 | 22.400 | 0.176 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `classic` | `profile_fast` | 3.941 | 17.252 | 0.228 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.941 | 15.603 | 0.253 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `classic` | `skip_source_error_control` | 3.941 | 23.802 | 0.166 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `classic` | `strict_current` | 3.941 | 33.563 | 0.117 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `ax` | `profile_balanced` | 0.767 | 21.916 | 0.035 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `ax` | `profile_fast` | 0.767 | 17.373 | 0.044 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.767 | 15.749 | 0.049 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 0.767 | 24.088 | 0.032 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `ax` | `strict_current` | 0.767 | 33.284 | 0.023 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.019 | 21.916 | 0.183 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `classic` | `profile_fast` | 4.019 | 17.373 | 0.231 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.019 | 15.749 | 0.255 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.019 | 24.088 | 0.167 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `classic` | `strict_current` | 4.019 | 33.284 | 0.121 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `ax` | `profile_balanced` | 0.801 | 21.908 | 0.037 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `ax` | `profile_fast` | 0.801 | 17.081 | 0.047 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.801 | 15.871 | 0.050 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `ax` | `skip_source_error_control` | 0.801 | 23.451 | 0.034 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `ax` | `strict_current` | 0.801 | 32.865 | 0.024 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `classic` | `profile_balanced` | 4.106 | 21.908 | 0.187 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `classic` | `profile_fast` | 4.106 | 17.081 | 0.240 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.106 | 15.871 | 0.259 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.106 | 23.451 | 0.175 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `classic` | `strict_current` | 4.106 | 32.865 | 0.125 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 2.618 | 21.786 | 0.120 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `ax` | `profile_fast` | 2.618 | 10.967 | 0.239 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 2.618 | 8.191 | 0.320 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 2.618 | 12.189 | 0.215 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `ax` | `strict_current` | 2.618 | 66.053 | 0.040 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.102 | 21.786 | 0.188 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.102 | 10.967 | 0.374 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.102 | 8.191 | 0.501 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.102 | 12.189 | 0.337 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.102 | 66.053 | 0.062 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `ax` | `profile_balanced` | 0.851 | 22.339 | 0.038 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `ax` | `profile_fast` | 0.851 | 11.369 | 0.075 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.851 | 8.340 | 0.102 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `ax` | `skip_source_error_control` | 0.851 | 12.604 | 0.068 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `ax` | `strict_current` | 0.851 | 67.892 | 0.013 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `classic` | `profile_balanced` | 3.894 | 22.339 | 0.174 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `classic` | `profile_fast` | 3.894 | 11.369 | 0.343 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.894 | 8.340 | 0.467 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `classic` | `skip_source_error_control` | 3.894 | 12.604 | 0.309 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `classic` | `strict_current` | 3.894 | 67.892 | 0.057 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `ax` | `profile_balanced` | 0.727 | 22.283 | 0.033 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `ax` | `profile_fast` | 0.727 | 11.137 | 0.065 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.727 | 8.358 | 0.087 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 0.727 | 12.437 | 0.058 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `ax` | `strict_current` | 0.727 | 67.125 | 0.011 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `classic` | `profile_balanced` | 3.798 | 22.283 | 0.170 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `classic` | `profile_fast` | 3.798 | 11.137 | 0.341 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.798 | 8.358 | 0.454 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 3.798 | 12.437 | 0.305 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `classic` | `strict_current` | 3.798 | 67.125 | 0.057 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `ax` | `profile_balanced` | 2.187 | 21.714 | 0.101 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `ax` | `profile_fast` | 2.187 | 11.223 | 0.195 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 2.187 | 8.401 | 0.260 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `ax` | `skip_source_error_control` | 2.187 | 12.287 | 0.178 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `ax` | `strict_current` | 2.187 | 69.158 | 0.032 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `classic` | `profile_balanced` | 4.086 | 21.714 | 0.188 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `classic` | `profile_fast` | 4.086 | 11.223 | 0.364 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.086 | 8.401 | 0.486 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.086 | 12.287 | 0.333 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `classic` | `strict_current` | 4.086 | 69.158 | 0.059 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.145 | 1.220 | 0.939 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.145 | 0.733 | 1.563 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.145 | 0.567 | 2.021 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.145 | 0.576 | 1.989 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.145 | 1.277 | 0.897 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 2.601 | 1.220 | 2.133 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `classic` | `profile_fast` | 2.601 | 0.733 | 3.549 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 2.601 | 0.567 | 4.590 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 2.601 | 0.576 | 4.516 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `classic` | `strict_current` | 2.601 | 1.277 | 2.037 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `ax` | `profile_balanced` | 0.923 | 0.914 | 1.011 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `ax` | `profile_fast` | 0.923 | 0.721 | 1.281 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.923 | 0.587 | 1.572 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `ax` | `skip_source_error_control` | 0.923 | 0.523 | 1.766 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `ax` | `strict_current` | 0.923 | 0.948 | 0.975 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `classic` | `profile_balanced` | 2.534 | 0.914 | 2.773 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `classic` | `profile_fast` | 2.534 | 0.721 | 3.515 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.534 | 0.587 | 4.313 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `classic` | `skip_source_error_control` | 2.534 | 0.523 | 4.846 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `classic` | `strict_current` | 2.534 | 0.948 | 2.674 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.063 | 1.035 | 1.027 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `ax` | `profile_fast` | 1.063 | 0.628 | 1.693 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.063 | 0.620 | 1.713 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.063 | 0.602 | 1.766 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `ax` | `strict_current` | 1.063 | 1.236 | 0.860 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `classic` | `profile_balanced` | 2.561 | 1.035 | 2.475 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `classic` | `profile_fast` | 2.561 | 0.628 | 4.080 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.561 | 0.620 | 4.128 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 2.561 | 0.602 | 4.256 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `classic` | `strict_current` | 2.561 | 1.236 | 2.072 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `ax` | `profile_balanced` | 1.600 | 0.893 | 1.792 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `ax` | `profile_fast` | 1.600 | 0.737 | 2.170 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.600 | 0.657 | 2.434 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.600 | 0.656 | 2.439 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `ax` | `strict_current` | 1.600 | 0.873 | 1.832 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `classic` | `profile_balanced` | 3.425 | 0.893 | 3.836 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `classic` | `profile_fast` | 3.425 | 0.737 | 4.645 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.425 | 0.657 | 5.210 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `classic` | `skip_source_error_control` | 3.425 | 0.656 | 5.220 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `classic` | `strict_current` | 3.425 | 0.873 | 3.921 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 0.776 | 9.300 | 0.083 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast` | 0.776 | 3.199 | 0.243 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 0.776 | 1.932 | 0.401 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 0.776 | 4.541 | 0.171 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 0.776 | 9.411 | 0.082 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 6.175 | 9.300 | 0.664 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast` | 6.175 | 3.199 | 1.931 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 6.175 | 1.932 | 3.195 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 6.175 | 4.541 | 1.360 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 6.175 | 9.411 | 0.656 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `ax` | `profile_balanced` | 0.910 | 9.472 | 0.096 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `ax` | `profile_fast` | 0.910 | 3.154 | 0.289 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.910 | 1.882 | 0.484 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `ax` | `skip_source_error_control` | 0.910 | 4.651 | 0.196 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `ax` | `strict_current` | 0.910 | 9.266 | 0.098 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `classic` | `profile_balanced` | 5.472 | 9.472 | 0.578 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `classic` | `profile_fast` | 5.472 | 3.154 | 1.735 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.472 | 1.882 | 2.908 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `classic` | `skip_source_error_control` | 5.472 | 4.651 | 1.177 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `classic` | `strict_current` | 5.472 | 9.266 | 0.591 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `ax` | `profile_balanced` | 0.877 | 9.272 | 0.095 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `ax` | `profile_fast` | 0.877 | 3.090 | 0.284 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.877 | 1.788 | 0.490 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 0.877 | 4.512 | 0.194 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 0.877 | 9.127 | 0.096 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `classic` | `profile_balanced` | 6.452 | 9.272 | 0.696 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `classic` | `profile_fast` | 6.452 | 3.090 | 2.088 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 6.452 | 1.788 | 3.608 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 6.452 | 4.512 | 1.430 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 6.452 | 9.127 | 0.707 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `ax` | `profile_balanced` | 1.026 | 9.608 | 0.107 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `ax` | `profile_fast` | 1.026 | 3.102 | 0.331 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.026 | 1.907 | 0.538 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.026 | 4.493 | 0.228 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `ax` | `strict_current` | 1.026 | 9.655 | 0.106 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `classic` | `profile_balanced` | 6.573 | 9.608 | 0.684 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `classic` | `profile_fast` | 6.573 | 3.102 | 2.119 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 6.573 | 1.907 | 3.446 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `classic` | `skip_source_error_control` | 6.573 | 4.493 | 1.463 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `classic` | `strict_current` | 6.573 | 9.655 | 0.681 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `ax` | `profile_balanced` | 1.657 | 0.565 | 2.934 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `ax` | `profile_fast` | 1.657 | 0.588 | 2.819 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.657 | 0.579 | 2.862 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.657 | 0.595 | 2.784 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `ax` | `strict_current` | 1.657 | 0.772 | 2.145 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `classic` | `profile_balanced` | 5.333 | 0.565 | 9.444 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `classic` | `profile_fast` | 5.333 | 0.588 | 9.077 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.333 | 0.579 | 9.212 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `classic` | `skip_source_error_control` | 5.333 | 0.595 | 8.961 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `classic` | `strict_current` | 5.333 | 0.772 | 6.904 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.679 | 0.618 | 2.718 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `ax` | `profile_fast` | 1.679 | 0.578 | 2.903 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.679 | 0.598 | 2.808 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.679 | 0.663 | 2.533 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `ax` | `strict_current` | 1.679 | 0.680 | 2.470 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `classic` | `profile_balanced` | 5.413 | 0.618 | 8.766 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `classic` | `profile_fast` | 5.413 | 0.578 | 9.362 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.413 | 0.598 | 9.053 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 5.413 | 0.663 | 8.168 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `classic` | `strict_current` | 5.413 | 0.680 | 7.964 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `ax` | `profile_balanced` | 1.476 | 0.672 | 2.195 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `ax` | `profile_fast` | 1.476 | 0.594 | 2.486 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.476 | 0.679 | 2.173 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.476 | 0.564 | 2.615 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `ax` | `strict_current` | 1.476 | 0.638 | 2.314 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `classic` | `profile_balanced` | 5.575 | 0.672 | 8.292 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `classic` | `profile_fast` | 5.575 | 0.594 | 9.390 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.575 | 0.679 | 8.209 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `classic` | `skip_source_error_control` | 5.575 | 0.564 | 9.881 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `classic` | `strict_current` | 5.575 | 0.638 | 8.743 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 3.517 | 0.892 | 3.944 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `ax` | `profile_fast` | 3.517 | 0.846 | 4.156 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 3.517 | 1.031 | 3.410 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 3.517 | 0.824 | 4.268 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `ax` | `strict_current` | 3.517 | 1.056 | 3.330 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.870 | 0.892 | 5.461 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.870 | 0.846 | 5.755 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.870 | 1.031 | 4.722 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.870 | 0.824 | 5.910 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.870 | 1.056 | 4.612 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `ax` | `profile_balanced` | 1.011 | 1.096 | 0.922 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `ax` | `profile_fast` | 1.011 | 0.929 | 1.088 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.011 | 0.904 | 1.118 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.011 | 0.826 | 1.225 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `ax` | `strict_current` | 1.011 | 1.123 | 0.900 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `classic` | `profile_balanced` | 4.730 | 1.096 | 4.315 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `classic` | `profile_fast` | 4.730 | 0.929 | 5.092 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.730 | 0.904 | 5.229 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `classic` | `skip_source_error_control` | 4.730 | 0.826 | 5.729 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `classic` | `strict_current` | 4.730 | 1.123 | 4.213 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.298 | 1.068 | 1.216 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `ax` | `profile_fast` | 1.298 | 1.030 | 1.260 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.298 | 0.925 | 1.403 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.298 | 0.898 | 1.446 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `ax` | `strict_current` | 1.298 | 1.081 | 1.201 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.627 | 1.068 | 4.334 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `classic` | `profile_fast` | 4.627 | 1.030 | 4.490 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.627 | 0.925 | 5.003 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.627 | 0.898 | 5.155 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `classic` | `strict_current` | 4.627 | 1.081 | 4.281 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `ax` | `profile_balanced` | 3.661 | 1.084 | 3.377 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `ax` | `profile_fast` | 3.661 | 0.901 | 4.062 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 3.661 | 0.960 | 3.815 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `ax` | `skip_source_error_control` | 3.661 | 0.936 | 3.913 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `ax` | `strict_current` | 3.661 | 1.170 | 3.130 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `classic` | `profile_balanced` | 4.861 | 1.084 | 4.484 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `classic` | `profile_fast` | 4.861 | 0.901 | 5.393 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.861 | 0.960 | 5.066 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.861 | 0.936 | 5.195 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `classic` | `strict_current` | 4.861 | 1.170 | 4.155 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.111 | 0.885 | 1.254 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.111 | 0.744 | 1.493 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.111 | 0.606 | 1.831 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.111 | 0.655 | 1.695 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.111 | 0.941 | 1.180 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.619 | 0.885 | 5.218 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.619 | 0.744 | 6.209 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.619 | 0.606 | 7.617 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.619 | 0.655 | 7.050 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.619 | 0.941 | 4.908 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `ax` | `profile_balanced` | 1.190 | 0.868 | 1.371 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `ax` | `profile_fast` | 1.190 | 0.659 | 1.807 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.190 | 0.683 | 1.742 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.190 | 0.748 | 1.591 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `ax` | `strict_current` | 1.190 | 0.950 | 1.253 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `classic` | `profile_balanced` | 4.939 | 0.868 | 5.691 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `classic` | `profile_fast` | 4.939 | 0.659 | 7.500 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.939 | 0.683 | 7.228 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `classic` | `skip_source_error_control` | 4.939 | 0.748 | 6.604 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `classic` | `strict_current` | 4.939 | 0.950 | 5.201 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `ax` | `profile_balanced` | 0.779 | 0.813 | 0.957 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `ax` | `profile_fast` | 0.779 | 0.718 | 1.084 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.779 | 0.599 | 1.300 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 0.779 | 0.628 | 1.241 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `ax` | `strict_current` | 0.779 | 0.827 | 0.942 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.299 | 0.813 | 5.285 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `classic` | `profile_fast` | 4.299 | 0.718 | 5.985 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.299 | 0.599 | 7.178 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.299 | 0.628 | 6.850 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `classic` | `strict_current` | 4.299 | 0.827 | 5.199 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `ax` | `profile_balanced` | 0.974 | 0.754 | 1.291 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `ax` | `profile_fast` | 0.974 | 0.617 | 1.577 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.974 | 0.648 | 1.503 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `ax` | `skip_source_error_control` | 0.974 | 0.586 | 1.663 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `ax` | `strict_current` | 0.974 | 0.774 | 1.259 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `classic` | `profile_balanced` | 4.455 | 0.754 | 5.907 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `classic` | `profile_fast` | 4.455 | 0.617 | 7.215 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.455 | 0.648 | 6.875 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.455 | 0.586 | 7.606 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `classic` | `strict_current` | 4.455 | 0.774 | 5.757 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.019 | 0.942 | 1.081 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.019 | 0.646 | 1.576 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.019 | 0.677 | 1.504 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.019 | 0.618 | 1.647 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.019 | 0.941 | 1.082 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 2.471 | 0.942 | 2.622 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `classic` | `profile_fast` | 2.471 | 0.646 | 3.823 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 2.471 | 0.677 | 3.649 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 2.471 | 0.618 | 3.996 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `classic` | `strict_current` | 2.471 | 0.941 | 2.625 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `ax` | `profile_balanced` | 1.107 | 0.776 | 1.426 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `ax` | `profile_fast` | 1.107 | 0.745 | 1.485 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.107 | 0.815 | 1.358 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.107 | 0.615 | 1.798 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `ax` | `strict_current` | 1.107 | 0.809 | 1.367 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `classic` | `profile_balanced` | 3.138 | 0.776 | 4.043 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `classic` | `profile_fast` | 3.138 | 0.745 | 4.211 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.138 | 0.815 | 3.849 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `classic` | `skip_source_error_control` | 3.138 | 0.615 | 5.099 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `classic` | `strict_current` | 3.138 | 0.809 | 3.877 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.300 | 0.887 | 1.466 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `ax` | `profile_fast` | 1.300 | 0.767 | 1.694 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.300 | 0.589 | 2.207 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.300 | 0.790 | 1.646 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `ax` | `strict_current` | 1.300 | 0.995 | 1.306 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `classic` | `profile_balanced` | 2.623 | 0.887 | 2.958 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `classic` | `profile_fast` | 2.623 | 0.767 | 3.420 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.623 | 0.589 | 4.455 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 2.623 | 0.790 | 3.322 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `classic` | `strict_current` | 2.623 | 0.995 | 2.636 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `ax` | `profile_balanced` | 1.013 | 0.999 | 1.014 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `ax` | `profile_fast` | 1.013 | 0.738 | 1.372 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.013 | 0.694 | 1.459 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.013 | 0.768 | 1.319 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `ax` | `strict_current` | 1.013 | 1.017 | 0.996 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `classic` | `profile_balanced` | 3.167 | 0.999 | 3.170 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `classic` | `profile_fast` | 3.167 | 0.738 | 4.291 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.167 | 0.694 | 4.563 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `classic` | `skip_source_error_control` | 3.167 | 0.768 | 4.126 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `classic` | `strict_current` | 3.167 | 1.017 | 3.114 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 3.122 | 1.383 | 2.257 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `ax` | `profile_fast` | 3.122 | 0.883 | 3.535 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 3.122 | 0.861 | 3.627 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 3.122 | 1.253 | 2.492 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `ax` | `strict_current` | 3.122 | 1.359 | 2.297 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.699 | 1.383 | 3.397 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.699 | 0.883 | 5.320 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.699 | 0.861 | 5.459 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.699 | 1.253 | 3.751 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.699 | 1.359 | 3.458 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `ax` | `profile_balanced` | 0.893 | 1.360 | 0.657 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `ax` | `profile_fast` | 0.893 | 0.929 | 0.962 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.893 | 0.790 | 1.131 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `ax` | `skip_source_error_control` | 0.893 | 1.245 | 0.718 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `ax` | `strict_current` | 0.893 | 1.310 | 0.682 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `classic` | `profile_balanced` | 4.507 | 1.360 | 3.314 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `classic` | `profile_fast` | 4.507 | 0.929 | 4.853 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.507 | 0.790 | 5.704 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `classic` | `skip_source_error_control` | 4.507 | 1.245 | 3.622 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `classic` | `strict_current` | 4.507 | 1.310 | 3.442 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `ax` | `profile_balanced` | 3.002 | 1.305 | 2.301 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `ax` | `profile_fast` | 3.002 | 0.805 | 3.728 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 3.002 | 0.954 | 3.147 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 3.002 | 1.110 | 2.704 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `ax` | `strict_current` | 3.002 | 1.351 | 2.222 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.527 | 1.305 | 3.470 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `classic` | `profile_fast` | 4.527 | 0.805 | 5.623 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.527 | 0.954 | 4.746 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.527 | 1.110 | 4.079 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `classic` | `strict_current` | 4.527 | 1.351 | 3.351 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `ax` | `profile_balanced` | 3.304 | 1.282 | 2.578 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `ax` | `profile_fast` | 3.304 | 0.904 | 3.656 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 3.304 | 0.702 | 4.705 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `ax` | `skip_source_error_control` | 3.304 | 1.115 | 2.964 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `ax` | `strict_current` | 3.304 | 1.316 | 2.511 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `classic` | `profile_balanced` | 4.588 | 1.282 | 3.580 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `classic` | `profile_fast` | 4.588 | 0.904 | 5.077 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.588 | 0.702 | 6.534 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.588 | 1.115 | 4.117 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `classic` | `strict_current` | 4.588 | 1.316 | 3.487 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 3.616 | 0.613 | 5.900 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `ax` | `profile_fast` | 3.616 | 0.696 | 5.196 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 3.616 | 0.680 | 5.315 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 3.616 | 0.625 | 5.789 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `ax` | `strict_current` | 3.616 | 0.611 | 5.914 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 3.617 | 0.613 | 5.900 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `classic` | `profile_fast` | 3.617 | 0.696 | 5.197 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 3.617 | 0.680 | 5.316 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 3.617 | 0.625 | 5.790 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `classic` | `strict_current` | 3.617 | 0.611 | 5.915 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `ax` | `profile_balanced` | 0.956 | 0.680 | 1.405 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `ax` | `profile_fast` | 0.956 | 0.646 | 1.480 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.956 | 0.683 | 1.399 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `ax` | `skip_source_error_control` | 0.956 | 0.623 | 1.534 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `ax` | `strict_current` | 0.956 | 0.713 | 1.341 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `classic` | `profile_balanced` | 3.026 | 0.680 | 4.448 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `classic` | `profile_fast` | 3.026 | 0.646 | 4.686 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.026 | 0.683 | 4.429 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `classic` | `skip_source_error_control` | 3.026 | 0.623 | 4.857 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `classic` | `strict_current` | 3.026 | 0.713 | 4.245 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `ax` | `profile_balanced` | 3.397 | 0.641 | 5.303 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `ax` | `profile_fast` | 3.397 | 0.626 | 5.423 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 3.397 | 0.747 | 4.548 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 3.397 | 0.635 | 5.351 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `ax` | `strict_current` | 3.397 | 0.687 | 4.945 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `classic` | `profile_balanced` | 3.306 | 0.641 | 5.161 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `classic` | `profile_fast` | 3.306 | 0.626 | 5.278 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.306 | 0.747 | 4.426 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 3.306 | 0.635 | 5.208 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `classic` | `strict_current` | 3.306 | 0.687 | 4.813 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `ax` | `profile_balanced` | 1.053 | 0.694 | 1.518 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `ax` | `profile_fast` | 1.053 | 0.776 | 1.357 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.053 | 0.626 | 1.681 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.053 | 0.695 | 1.515 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `ax` | `strict_current` | 1.053 | 0.786 | 1.340 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `classic` | `profile_balanced` | 3.424 | 0.694 | 4.936 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `classic` | `profile_fast` | 3.424 | 0.776 | 4.412 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.424 | 0.626 | 5.467 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `classic` | `skip_source_error_control` | 3.424 | 0.695 | 4.927 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `classic` | `strict_current` | 3.424 | 0.786 | 4.356 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.363 | 2.009 | 0.679 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.363 | 1.310 | 1.041 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.363 | 0.900 | 1.515 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.363 | 1.033 | 1.319 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.363 | 2.074 | 0.657 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.805 | 2.009 | 2.392 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.805 | 1.310 | 3.667 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.805 | 0.900 | 5.338 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.805 | 1.033 | 4.650 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.805 | 2.074 | 2.317 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `ax` | `profile_balanced` | 0.922 | 1.979 | 0.466 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `ax` | `profile_fast` | 0.922 | 1.208 | 0.764 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.922 | 0.970 | 0.951 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `ax` | `skip_source_error_control` | 0.922 | 0.994 | 0.928 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `ax` | `strict_current` | 0.922 | 1.949 | 0.473 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `classic` | `profile_balanced` | 4.613 | 1.979 | 2.331 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `classic` | `profile_fast` | 4.613 | 1.208 | 3.818 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.613 | 0.970 | 4.756 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `classic` | `skip_source_error_control` | 4.613 | 0.994 | 4.643 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `classic` | `strict_current` | 4.613 | 1.949 | 2.367 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `ax` | `profile_balanced` | 0.852 | 1.884 | 0.452 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `ax` | `profile_fast` | 0.852 | 1.230 | 0.692 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.852 | 0.890 | 0.957 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 0.852 | 0.916 | 0.930 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `ax` | `strict_current` | 0.852 | 1.930 | 0.441 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.646 | 1.884 | 2.465 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `classic` | `profile_fast` | 4.646 | 1.230 | 3.776 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.646 | 0.890 | 5.220 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.646 | 0.916 | 5.074 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `classic` | `strict_current` | 4.646 | 1.930 | 2.407 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `ax` | `profile_balanced` | 0.949 | 2.130 | 0.445 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `ax` | `profile_fast` | 0.949 | 1.213 | 0.782 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.949 | 0.901 | 1.052 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `ax` | `skip_source_error_control` | 0.949 | 0.997 | 0.952 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `ax` | `strict_current` | 0.949 | 2.200 | 0.431 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `classic` | `profile_balanced` | 4.664 | 2.130 | 2.190 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `classic` | `profile_fast` | 4.664 | 1.213 | 3.844 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.664 | 0.901 | 5.174 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.664 | 0.997 | 4.678 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `classic` | `strict_current` | 4.664 | 2.200 | 2.119 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.338 | 0.903 | 1.481 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `ax` | `profile_fast` | 1.338 | 1.072 | 1.248 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.338 | 0.781 | 1.713 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.338 | 0.807 | 1.657 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `ax` | `strict_current` | 1.338 | 1.024 | 1.306 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `classic` | `profile_balanced` | 5.312 | 0.903 | 5.882 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `classic` | `profile_fast` | 5.312 | 1.072 | 4.953 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.312 | 0.781 | 6.800 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 5.312 | 0.807 | 6.579 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `classic` | `strict_current` | 5.312 | 1.024 | 5.186 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `ax` | `profile_balanced` | 1.114 | 0.988 | 1.127 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `ax` | `profile_fast` | 1.114 | 0.681 | 1.635 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.114 | 0.716 | 1.556 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.114 | 0.685 | 1.626 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `ax` | `strict_current` | 1.114 | 0.821 | 1.356 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `classic` | `profile_balanced` | 4.599 | 0.988 | 4.653 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `classic` | `profile_fast` | 4.599 | 0.681 | 6.752 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.599 | 0.716 | 6.425 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.599 | 0.685 | 6.715 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `classic` | `strict_current` | 4.599 | 0.821 | 5.600 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `ax` | `profile_balanced` | 1.110 | 0.852 | 1.303 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `ax` | `profile_fast` | 1.110 | 0.907 | 1.224 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.110 | 0.696 | 1.596 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.110 | 0.719 | 1.544 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `ax` | `strict_current` | 1.110 | 0.946 | 1.174 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `classic` | `profile_balanced` | 2.589 | 0.852 | 3.038 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `classic` | `profile_fast` | 2.589 | 0.907 | 2.854 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.589 | 0.696 | 3.721 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `classic` | `skip_source_error_control` | 2.589 | 0.719 | 3.600 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `classic` | `strict_current` | 2.589 | 0.946 | 2.738 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.198 | 0.877 | 1.366 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `ax` | `profile_fast` | 1.198 | 0.811 | 1.478 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.198 | 0.737 | 1.627 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.198 | 0.711 | 1.686 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `ax` | `strict_current` | 1.198 | 0.928 | 1.292 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `classic` | `profile_balanced` | 2.336 | 0.877 | 2.663 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `classic` | `profile_fast` | 2.336 | 0.811 | 2.882 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.336 | 0.737 | 3.172 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 2.336 | 0.711 | 3.288 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `classic` | `strict_current` | 2.336 | 0.928 | 2.519 |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `ax` | `profile_balanced` | 1.014 | 0.818 | 1.241 |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `ax` | `profile_fast` | 1.014 | 0.781 | 1.300 |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.014 | 0.892 | 1.138 |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.014 | 0.856 | 1.186 |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `ax` | `strict_current` | 1.014 | 0.951 | 1.067 |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `classic` | `profile_balanced` | 2.700 | 0.818 | 3.302 |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `classic` | `profile_fast` | 2.700 | 0.781 | 3.459 |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.700 | 0.892 | 3.028 |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `classic` | `skip_source_error_control` | 2.700 | 0.856 | 3.156 |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `classic` | `strict_current` | 2.700 | 0.951 | 2.838 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.286 | 0.840 | 1.531 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.286 | 0.739 | 1.739 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.286 | 0.717 | 1.793 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.286 | 0.738 | 1.743 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.286 | 0.793 | 1.622 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 2.988 | 0.840 | 3.557 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `classic` | `profile_fast` | 2.988 | 0.739 | 4.041 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 2.988 | 0.717 | 4.167 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 2.988 | 0.738 | 4.050 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `classic` | `strict_current` | 2.988 | 0.793 | 3.769 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `ax` | `profile_balanced` | 1.259 | 0.659 | 1.910 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `ax` | `profile_fast` | 1.259 | 0.589 | 2.136 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.259 | 0.682 | 1.845 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.259 | 0.705 | 1.784 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `ax` | `strict_current` | 1.259 | 0.698 | 1.804 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `classic` | `profile_balanced` | 2.881 | 0.659 | 4.372 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `classic` | `profile_fast` | 2.881 | 0.589 | 4.889 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.881 | 0.682 | 4.223 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `classic` | `skip_source_error_control` | 2.881 | 0.705 | 4.084 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `classic` | `strict_current` | 2.881 | 0.698 | 4.128 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.071 | 0.776 | 1.379 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `ax` | `profile_fast` | 1.071 | 0.743 | 1.442 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.071 | 0.780 | 1.372 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.071 | 0.698 | 1.535 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `ax` | `strict_current` | 1.071 | 0.803 | 1.333 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `classic` | `profile_balanced` | 3.124 | 0.776 | 4.024 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `classic` | `profile_fast` | 3.124 | 0.743 | 4.207 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.124 | 0.780 | 4.005 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 3.124 | 0.698 | 4.478 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `classic` | `strict_current` | 3.124 | 0.803 | 3.888 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `ax` | `profile_balanced` | 1.008 | 0.697 | 1.446 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `ax` | `profile_fast` | 1.008 | 0.709 | 1.422 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.008 | 0.805 | 1.251 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.008 | 0.779 | 1.294 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `ax` | `strict_current` | 1.008 | 0.792 | 1.272 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `classic` | `profile_balanced` | 2.776 | 0.697 | 3.982 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `classic` | `profile_fast` | 2.776 | 0.709 | 3.918 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.776 | 0.805 | 3.447 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `classic` | `skip_source_error_control` | 2.776 | 0.779 | 3.565 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `classic` | `strict_current` | 2.776 | 0.792 | 3.503 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.085 | 1.287 | 0.843 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.085 | 0.916 | 1.184 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.085 | 0.765 | 1.418 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.085 | 0.654 | 1.658 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.085 | 1.345 | 0.807 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.503 | 1.287 | 3.500 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.503 | 0.916 | 4.916 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.503 | 0.765 | 5.885 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.503 | 0.654 | 6.883 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.503 | 1.345 | 3.349 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `ax` | `profile_balanced` | 1.179 | 1.054 | 1.118 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `ax` | `profile_fast` | 1.179 | 0.831 | 1.419 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.179 | 0.881 | 1.338 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.179 | 0.645 | 1.826 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `ax` | `strict_current` | 1.179 | 1.169 | 1.008 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `classic` | `profile_balanced` | 4.672 | 1.054 | 4.432 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `classic` | `profile_fast` | 4.672 | 0.831 | 5.624 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.672 | 0.881 | 5.306 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `classic` | `skip_source_error_control` | 4.672 | 0.645 | 7.239 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `classic` | `strict_current` | 4.672 | 1.169 | 3.996 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.120 | 1.300 | 0.861 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `ax` | `profile_fast` | 1.120 | 1.006 | 1.113 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.120 | 0.644 | 1.738 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.120 | 0.825 | 1.358 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `ax` | `strict_current` | 1.120 | 1.187 | 0.944 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.701 | 1.300 | 3.615 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `classic` | `profile_fast` | 4.701 | 1.006 | 4.672 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.701 | 0.644 | 7.298 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.701 | 0.825 | 5.701 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `classic` | `strict_current` | 4.701 | 1.187 | 3.962 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `ax` | `profile_balanced` | 1.408 | 1.217 | 1.158 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `ax` | `profile_fast` | 1.408 | 0.966 | 1.458 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.408 | 0.585 | 2.409 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.408 | 0.628 | 2.243 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `ax` | `strict_current` | 1.408 | 1.136 | 1.239 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `classic` | `profile_balanced` | 5.244 | 1.217 | 4.310 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `classic` | `profile_fast` | 5.244 | 0.966 | 5.430 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.244 | 0.585 | 8.969 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `classic` | `skip_source_error_control` | 5.244 | 0.628 | 8.350 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `classic` | `strict_current` | 5.244 | 1.136 | 4.614 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.268 | 2.111 | 0.601 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.268 | 1.678 | 0.755 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.268 | 1.494 | 0.849 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.268 | 1.490 | 0.851 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.268 | 2.110 | 0.601 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.267 | 2.111 | 2.022 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.267 | 1.678 | 2.542 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.267 | 1.494 | 2.857 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.267 | 1.490 | 2.864 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.267 | 2.110 | 2.023 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `ax` | `profile_balanced` | 1.141 | 2.664 | 0.428 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `ax` | `profile_fast` | 1.141 | 1.271 | 0.898 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.141 | 0.835 | 1.366 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.141 | 1.822 | 0.626 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `ax` | `strict_current` | 1.141 | 2.838 | 0.402 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `classic` | `profile_balanced` | 4.101 | 2.664 | 1.539 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `classic` | `profile_fast` | 4.101 | 1.271 | 3.227 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.101 | 0.835 | 4.911 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `classic` | `skip_source_error_control` | 4.101 | 1.822 | 2.251 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `classic` | `strict_current` | 4.101 | 2.838 | 1.445 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `ax` | `profile_balanced` | 0.720 | 2.759 | 0.261 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `ax` | `profile_fast` | 0.720 | 1.299 | 0.554 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.720 | 0.841 | 0.856 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 0.720 | 1.721 | 0.418 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 0.720 | 2.710 | 0.266 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `classic` | `profile_balanced` | 3.395 | 2.759 | 1.230 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `classic` | `profile_fast` | 3.395 | 1.299 | 2.613 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.395 | 0.841 | 4.039 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 3.395 | 1.721 | 1.973 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 3.395 | 2.710 | 1.253 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `ax` | `profile_balanced` | 1.035 | 2.764 | 0.375 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `ax` | `profile_fast` | 1.035 | 1.410 | 0.735 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.035 | 0.939 | 1.103 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.035 | 1.731 | 0.598 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `ax` | `strict_current` | 1.035 | 2.849 | 0.363 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `classic` | `profile_balanced` | 3.860 | 2.764 | 1.396 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `classic` | `profile_fast` | 3.860 | 1.410 | 2.738 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.860 | 0.939 | 4.110 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `classic` | `skip_source_error_control` | 3.860 | 1.731 | 2.230 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `classic` | `strict_current` | 3.860 | 2.849 | 1.355 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.328 | 1.522 | 0.872 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.328 | 1.004 | 1.322 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.328 | 0.624 | 2.128 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.328 | 0.590 | 2.249 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.328 | 1.532 | 0.866 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.984 | 1.522 | 3.275 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.984 | 1.004 | 4.963 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.984 | 0.624 | 7.989 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.984 | 0.590 | 8.441 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.984 | 1.532 | 3.252 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `ax` | `profile_balanced` | 1.226 | 1.473 | 0.832 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `ax` | `profile_fast` | 1.226 | 1.122 | 1.092 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.226 | 0.613 | 1.998 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.226 | 0.658 | 1.864 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `ax` | `strict_current` | 1.226 | 1.516 | 0.808 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `classic` | `profile_balanced` | 4.518 | 1.473 | 3.068 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `classic` | `profile_fast` | 4.518 | 1.122 | 4.026 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.518 | 0.613 | 7.366 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `classic` | `skip_source_error_control` | 4.518 | 0.658 | 6.870 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `classic` | `strict_current` | 4.518 | 1.516 | 2.980 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.449 | 1.454 | 0.996 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `ax` | `profile_fast` | 1.449 | 0.931 | 1.557 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.449 | 0.671 | 2.158 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.449 | 0.618 | 2.343 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `ax` | `strict_current` | 1.449 | 1.506 | 0.962 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.756 | 1.454 | 3.270 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `classic` | `profile_fast` | 4.756 | 0.931 | 5.109 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.756 | 0.671 | 7.084 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.756 | 0.618 | 7.692 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `classic` | `strict_current` | 4.756 | 1.506 | 3.158 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `ax` | `profile_balanced` | 0.894 | 1.478 | 0.605 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `ax` | `profile_fast` | 0.894 | 0.971 | 0.920 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.894 | 0.715 | 1.249 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `ax` | `skip_source_error_control` | 0.894 | 0.527 | 1.695 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `ax` | `strict_current` | 0.894 | 1.519 | 0.589 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `classic` | `profile_balanced` | 4.294 | 1.478 | 2.906 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `classic` | `profile_fast` | 4.294 | 0.971 | 4.420 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.294 | 0.715 | 6.002 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.294 | 0.527 | 8.143 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `classic` | `strict_current` | 4.294 | 1.519 | 2.828 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 3.640 | 0.630 | 5.772 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `ax` | `profile_fast` | 3.640 | 0.661 | 5.507 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 3.640 | 0.738 | 4.933 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 3.640 | 0.595 | 6.113 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `ax` | `strict_current` | 3.640 | 0.763 | 4.769 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 5.441 | 0.630 | 8.630 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `classic` | `profile_fast` | 5.441 | 0.661 | 8.232 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 5.441 | 0.738 | 7.375 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 5.441 | 0.595 | 9.139 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `classic` | `strict_current` | 5.441 | 0.763 | 7.130 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `ax` | `profile_balanced` | 0.988 | 0.705 | 1.402 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `ax` | `profile_fast` | 0.988 | 0.704 | 1.404 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.988 | 0.627 | 1.575 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `ax` | `skip_source_error_control` | 0.988 | 0.668 | 1.479 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `ax` | `strict_current` | 0.988 | 0.830 | 1.190 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `classic` | `profile_balanced` | 4.973 | 0.705 | 7.057 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `classic` | `profile_fast` | 4.973 | 0.704 | 7.066 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.973 | 0.627 | 7.931 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `classic` | `skip_source_error_control` | 4.973 | 0.668 | 7.444 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `classic` | `strict_current` | 4.973 | 0.830 | 5.990 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.241 | 0.808 | 1.537 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `ax` | `profile_fast` | 1.241 | 0.692 | 1.794 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.241 | 0.670 | 1.852 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.241 | 0.658 | 1.886 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `ax` | `strict_current` | 1.241 | 0.562 | 2.207 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `classic` | `profile_balanced` | 5.374 | 0.808 | 6.654 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `classic` | `profile_fast` | 5.374 | 0.692 | 7.767 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.374 | 0.670 | 8.019 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 5.374 | 0.658 | 8.167 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `classic` | `strict_current` | 5.374 | 0.562 | 9.556 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `ax` | `profile_balanced` | 3.763 | 0.601 | 6.260 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `ax` | `profile_fast` | 3.763 | 0.541 | 6.957 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 3.763 | 0.600 | 6.272 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `ax` | `skip_source_error_control` | 3.763 | 0.541 | 6.961 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `ax` | `strict_current` | 3.763 | 0.636 | 5.919 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `classic` | `profile_balanced` | 4.984 | 0.601 | 8.291 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `classic` | `profile_fast` | 4.984 | 0.541 | 9.215 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.984 | 0.600 | 8.307 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.984 | 0.541 | 9.220 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `classic` | `strict_current` | 4.984 | 0.636 | 7.839 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.157 | 0.721 | 1.605 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.157 | 0.853 | 1.357 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.157 | 0.576 | 2.008 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.157 | 0.807 | 1.433 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.157 | 0.736 | 1.573 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 5.383 | 0.721 | 7.467 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast` | 5.383 | 0.853 | 6.311 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 5.383 | 0.576 | 9.340 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 5.383 | 0.807 | 6.668 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 5.383 | 0.736 | 7.318 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `ax` | `profile_balanced` | 0.958 | 0.741 | 1.291 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `ax` | `profile_fast` | 0.958 | 0.526 | 1.820 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.958 | 0.610 | 1.570 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `ax` | `skip_source_error_control` | 0.958 | 0.644 | 1.488 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `ax` | `strict_current` | 0.958 | 0.707 | 1.355 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `classic` | `profile_balanced` | 5.628 | 0.741 | 7.591 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `classic` | `profile_fast` | 5.628 | 0.526 | 10.699 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.628 | 0.610 | 9.227 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `classic` | `skip_source_error_control` | 5.628 | 0.644 | 8.743 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `classic` | `strict_current` | 5.628 | 0.707 | 7.965 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.133 | 0.623 | 1.817 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `ax` | `profile_fast` | 1.133 | 0.632 | 1.791 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.133 | 0.575 | 1.969 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.133 | 0.639 | 1.772 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 1.133 | 0.697 | 1.626 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `classic` | `profile_balanced` | 5.195 | 0.623 | 8.335 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `classic` | `profile_fast` | 5.195 | 0.632 | 8.214 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.195 | 0.575 | 9.030 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 5.195 | 0.639 | 8.126 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 5.195 | 0.697 | 7.458 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `ax` | `profile_balanced` | 1.679 | 0.726 | 2.313 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `ax` | `profile_fast` | 1.679 | 0.751 | 2.235 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.679 | 0.666 | 2.522 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.679 | 0.646 | 2.600 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `ax` | `strict_current` | 1.679 | 0.670 | 2.507 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `classic` | `profile_balanced` | 5.734 | 0.726 | 7.899 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `classic` | `profile_fast` | 5.734 | 0.751 | 7.633 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.734 | 0.666 | 8.610 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `classic` | `skip_source_error_control` | 5.734 | 0.646 | 8.878 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `classic` | `strict_current` | 5.734 | 0.670 | 8.560 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 2.900 | 0.972 | 2.984 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `ax` | `profile_fast` | 2.900 | 0.830 | 3.496 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 2.900 | 0.562 | 5.161 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 2.900 | 0.760 | 3.817 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `ax` | `strict_current` | 2.900 | 1.000 | 2.901 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 2.954 | 0.972 | 3.040 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `classic` | `profile_fast` | 2.954 | 0.830 | 3.561 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 2.954 | 0.562 | 5.257 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 2.954 | 0.760 | 3.888 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `classic` | `strict_current` | 2.954 | 1.000 | 2.955 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `ax` | `profile_balanced` | 3.095 | 1.252 | 2.471 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `ax` | `profile_fast` | 3.095 | 0.778 | 3.979 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 3.095 | 0.681 | 4.547 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `ax` | `skip_source_error_control` | 3.095 | 0.777 | 3.984 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `ax` | `strict_current` | 3.095 | 1.184 | 2.615 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `classic` | `profile_balanced` | 3.087 | 1.252 | 2.465 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `classic` | `profile_fast` | 3.087 | 0.778 | 3.969 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.087 | 0.681 | 4.536 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `classic` | `skip_source_error_control` | 3.087 | 0.777 | 3.974 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `classic` | `strict_current` | 3.087 | 1.184 | 2.608 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.734 | 0.845 | 2.052 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `ax` | `profile_fast` | 1.734 | 0.727 | 2.387 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.734 | 0.747 | 2.322 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.734 | 0.658 | 2.635 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `ax` | `strict_current` | 1.734 | 0.943 | 1.839 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `classic` | `profile_balanced` | 2.679 | 0.845 | 3.170 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `classic` | `profile_fast` | 2.679 | 0.727 | 3.687 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.679 | 0.747 | 3.586 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 2.679 | 0.658 | 4.070 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `classic` | `strict_current` | 2.679 | 0.943 | 2.840 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `ax` | `profile_balanced` | 1.121 | 1.129 | 0.993 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `ax` | `profile_fast` | 1.121 | 0.762 | 1.472 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.121 | 0.659 | 1.702 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.121 | 0.636 | 1.763 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `ax` | `strict_current` | 1.121 | 1.019 | 1.100 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `classic` | `profile_balanced` | 2.730 | 1.129 | 2.419 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `classic` | `profile_fast` | 2.730 | 0.762 | 3.584 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.730 | 0.659 | 4.145 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `classic` | `skip_source_error_control` | 2.730 | 0.636 | 4.293 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `classic` | `strict_current` | 2.730 | 1.019 | 2.679 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 0.988 | 0.825 | 1.197 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `ax` | `profile_fast` | 0.988 | 0.783 | 1.261 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 0.988 | 0.899 | 1.099 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 0.988 | 0.770 | 1.282 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `ax` | `strict_current` | 0.988 | 0.872 | 1.132 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 5.495 | 0.825 | 6.660 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `classic` | `profile_fast` | 5.495 | 0.783 | 7.018 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 5.495 | 0.899 | 6.113 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 5.495 | 0.770 | 7.136 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `classic` | `strict_current` | 5.495 | 0.872 | 6.299 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `ax` | `profile_balanced` | 0.941 | 0.691 | 1.363 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `ax` | `profile_fast` | 0.941 | 0.636 | 1.480 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.941 | 0.659 | 1.428 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `ax` | `skip_source_error_control` | 0.941 | 0.636 | 1.480 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `ax` | `strict_current` | 0.941 | 0.751 | 1.253 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `classic` | `profile_balanced` | 4.293 | 0.691 | 6.214 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `classic` | `profile_fast` | 4.293 | 0.636 | 6.749 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.293 | 0.659 | 6.513 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `classic` | `skip_source_error_control` | 4.293 | 0.636 | 6.747 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `classic` | `strict_current` | 4.293 | 0.751 | 5.713 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.437 | 0.712 | 2.018 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `ax` | `profile_fast` | 1.437 | 0.736 | 1.953 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.437 | 0.661 | 2.173 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.437 | 0.839 | 1.713 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `ax` | `strict_current` | 1.437 | 0.734 | 1.959 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.873 | 0.712 | 6.841 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `classic` | `profile_fast` | 4.873 | 0.736 | 6.620 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.873 | 0.661 | 7.366 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.873 | 0.839 | 5.806 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `classic` | `strict_current` | 4.873 | 0.734 | 6.642 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `ax` | `profile_balanced` | 1.448 | 0.650 | 2.228 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `ax` | `profile_fast` | 1.448 | 0.627 | 2.307 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.448 | 0.721 | 2.007 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.448 | 0.684 | 2.115 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `ax` | `strict_current` | 1.448 | 0.699 | 2.072 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `classic` | `profile_balanced` | 5.290 | 0.650 | 8.141 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `classic` | `profile_fast` | 5.290 | 0.627 | 8.431 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.290 | 0.721 | 7.334 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `classic` | `skip_source_error_control` | 5.290 | 0.684 | 7.729 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `classic` | `strict_current` | 5.290 | 0.699 | 7.570 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.138 | 0.861 | 1.322 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.138 | 0.935 | 1.218 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.138 | 0.876 | 1.299 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.138 | 0.888 | 1.282 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.138 | 0.848 | 1.343 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.771 | 0.861 | 5.541 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.771 | 0.935 | 5.105 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.771 | 0.876 | 5.444 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.771 | 0.888 | 5.375 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.771 | 0.848 | 5.629 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `ax` | `profile_balanced` | 1.395 | 0.896 | 1.557 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `ax` | `profile_fast` | 1.395 | 0.863 | 1.617 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.395 | 0.831 | 1.679 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.395 | 0.838 | 1.665 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `ax` | `strict_current` | 1.395 | 0.950 | 1.469 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `classic` | `profile_balanced` | 4.796 | 0.896 | 5.355 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `classic` | `profile_fast` | 4.796 | 0.863 | 5.559 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.796 | 0.831 | 5.773 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `classic` | `skip_source_error_control` | 4.796 | 0.838 | 5.725 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `classic` | `strict_current` | 4.796 | 0.950 | 5.049 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.093 | 0.985 | 1.109 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `ax` | `profile_fast` | 1.093 | 0.843 | 1.296 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.093 | 0.787 | 1.388 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.093 | 0.780 | 1.401 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `ax` | `strict_current` | 1.093 | 1.018 | 1.073 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.918 | 0.985 | 4.992 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `classic` | `profile_fast` | 4.918 | 0.843 | 5.835 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.918 | 0.787 | 6.249 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.918 | 0.780 | 6.307 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `classic` | `strict_current` | 4.918 | 1.018 | 4.832 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `ax` | `profile_balanced` | 0.979 | 0.818 | 1.197 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `ax` | `profile_fast` | 0.979 | 0.806 | 1.215 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.979 | 0.807 | 1.214 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `ax` | `skip_source_error_control` | 0.979 | 0.840 | 1.166 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `ax` | `strict_current` | 0.979 | 0.933 | 1.049 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `classic` | `profile_balanced` | 3.906 | 0.818 | 4.775 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `classic` | `profile_fast` | 3.906 | 0.806 | 4.845 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.906 | 0.807 | 4.842 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `classic` | `skip_source_error_control` | 3.906 | 0.840 | 4.649 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `classic` | `strict_current` | 3.906 | 0.933 | 4.184 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 2.668 | 0.935 | 2.854 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `ax` | `profile_fast` | 2.668 | 0.900 | 2.964 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 2.668 | 0.839 | 3.181 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 2.668 | 0.915 | 2.916 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `ax` | `strict_current` | 2.668 | 0.886 | 3.011 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 2.429 | 0.935 | 2.598 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `classic` | `profile_fast` | 2.429 | 0.900 | 2.698 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 2.429 | 0.839 | 2.896 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 2.429 | 0.915 | 2.654 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `classic` | `strict_current` | 2.429 | 0.886 | 2.741 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `ax` | `profile_balanced` | 2.722 | 0.695 | 3.917 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `ax` | `profile_fast` | 2.722 | 0.865 | 3.149 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 2.722 | 0.849 | 3.206 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `ax` | `skip_source_error_control` | 2.722 | 0.945 | 2.880 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `ax` | `strict_current` | 2.722 | 0.860 | 3.166 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `classic` | `profile_balanced` | 2.589 | 0.695 | 3.725 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `classic` | `profile_fast` | 2.589 | 0.865 | 2.994 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.589 | 0.849 | 3.048 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `classic` | `skip_source_error_control` | 2.589 | 0.945 | 2.738 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `classic` | `strict_current` | 2.589 | 0.860 | 3.011 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.135 | 0.819 | 1.386 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `ax` | `profile_fast` | 1.135 | 0.881 | 1.289 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.135 | 0.881 | 1.289 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.135 | 1.033 | 1.099 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `ax` | `strict_current` | 1.135 | 0.838 | 1.355 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `classic` | `profile_balanced` | 2.965 | 0.819 | 3.621 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `classic` | `profile_fast` | 2.965 | 0.881 | 3.367 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.965 | 0.881 | 3.367 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 2.965 | 1.033 | 2.871 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `classic` | `strict_current` | 2.965 | 0.838 | 3.539 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `ax` | `profile_balanced` | 1.600 | 1.061 | 1.508 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `ax` | `profile_fast` | 1.600 | 0.951 | 1.683 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.600 | 0.872 | 1.834 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.600 | 1.029 | 1.555 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `ax` | `strict_current` | 1.600 | 1.057 | 1.513 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `classic` | `profile_balanced` | 3.009 | 1.061 | 2.836 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `classic` | `profile_fast` | 3.009 | 0.951 | 3.165 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.009 | 0.872 | 3.449 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `classic` | `skip_source_error_control` | 3.009 | 1.029 | 2.924 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `classic` | `strict_current` | 3.009 | 1.057 | 2.845 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.035 | 1.122 | 0.922 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.035 | 0.921 | 1.124 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.035 | 0.593 | 1.744 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.035 | 0.719 | 1.440 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.035 | 1.373 | 0.754 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.693 | 1.122 | 4.182 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.693 | 0.921 | 5.097 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.693 | 0.593 | 7.908 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.693 | 0.719 | 6.530 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.693 | 1.373 | 3.419 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `ax` | `profile_balanced` | 1.364 | 1.207 | 1.129 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `ax` | `profile_fast` | 1.364 | 0.845 | 1.613 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.364 | 0.698 | 1.955 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.364 | 0.702 | 1.943 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `ax` | `strict_current` | 1.364 | 1.218 | 1.120 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `classic` | `profile_balanced` | 5.023 | 1.207 | 4.160 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `classic` | `profile_fast` | 5.023 | 0.845 | 5.942 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.023 | 0.698 | 7.201 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `classic` | `skip_source_error_control` | 5.023 | 0.702 | 7.156 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `classic` | `strict_current` | 5.023 | 1.218 | 4.124 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.198 | 1.042 | 1.149 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `ax` | `profile_fast` | 1.198 | 0.855 | 1.401 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.198 | 0.674 | 1.777 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.198 | 0.626 | 1.912 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `ax` | `strict_current` | 1.198 | 1.264 | 0.948 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.919 | 1.042 | 4.719 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `classic` | `profile_fast` | 4.919 | 0.855 | 5.755 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.919 | 0.674 | 7.297 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.919 | 0.626 | 7.853 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `classic` | `strict_current` | 4.919 | 1.264 | 3.893 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `ax` | `profile_balanced` | 1.702 | 1.168 | 1.457 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `ax` | `profile_fast` | 1.702 | 0.819 | 2.078 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.702 | 0.691 | 2.463 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.702 | 0.569 | 2.993 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `ax` | `strict_current` | 1.702 | 1.279 | 1.331 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `classic` | `profile_balanced` | 5.603 | 1.168 | 4.796 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `classic` | `profile_fast` | 5.603 | 0.819 | 6.837 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.603 | 0.691 | 8.107 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `classic` | `skip_source_error_control` | 5.603 | 0.569 | 9.849 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `classic` | `strict_current` | 5.603 | 1.279 | 4.381 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 0.712 | 1.962 | 0.363 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `ax` | `profile_fast` | 0.712 | 1.618 | 0.440 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 0.712 | 1.625 | 0.438 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 0.712 | 1.448 | 0.491 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 0.712 | 4.213 | 0.169 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 3.781 | 1.962 | 1.927 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `classic` | `profile_fast` | 3.781 | 1.618 | 2.336 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 3.781 | 1.625 | 2.326 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 3.781 | 1.448 | 2.610 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 3.781 | 4.213 | 0.897 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `ax` | `profile_balanced` | 0.768 | 1.977 | 0.388 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `ax` | `profile_fast` | 0.768 | 1.653 | 0.464 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.768 | 1.528 | 0.503 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `ax` | `skip_source_error_control` | 0.768 | 1.445 | 0.531 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `ax` | `strict_current` | 0.768 | 4.108 | 0.187 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `classic` | `profile_balanced` | 3.645 | 1.977 | 1.844 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `classic` | `profile_fast` | 3.645 | 1.653 | 2.205 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.645 | 1.528 | 2.385 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `classic` | `skip_source_error_control` | 3.645 | 1.445 | 2.522 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `classic` | `strict_current` | 3.645 | 4.108 | 0.887 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `ax` | `profile_balanced` | 0.781 | 1.996 | 0.391 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `ax` | `profile_fast` | 0.781 | 1.740 | 0.449 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.781 | 1.563 | 0.499 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 0.781 | 1.581 | 0.494 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `ax` | `strict_current` | 0.781 | 4.234 | 0.184 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `classic` | `profile_balanced` | 3.792 | 1.996 | 1.900 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `classic` | `profile_fast` | 3.792 | 1.740 | 2.180 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.792 | 1.563 | 2.426 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 3.792 | 1.581 | 2.399 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `classic` | `strict_current` | 3.792 | 4.234 | 0.896 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `ax` | `profile_balanced` | 0.835 | 1.952 | 0.428 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `ax` | `profile_fast` | 0.835 | 1.639 | 0.510 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.835 | 1.443 | 0.579 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `ax` | `skip_source_error_control` | 0.835 | 1.530 | 0.546 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `ax` | `strict_current` | 0.835 | 4.167 | 0.200 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `classic` | `profile_balanced` | 3.848 | 1.952 | 1.972 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `classic` | `profile_fast` | 3.848 | 1.639 | 2.348 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.848 | 1.443 | 2.667 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `classic` | `skip_source_error_control` | 3.848 | 1.530 | 2.515 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `classic` | `strict_current` | 3.848 | 4.167 | 0.923 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 4.121 | 0.770 | 5.353 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `ax` | `profile_fast` | 4.121 | 0.846 | 4.872 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 4.121 | 0.609 | 6.769 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 4.121 | 0.687 | 6.000 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `ax` | `strict_current` | 4.121 | 0.768 | 5.363 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 5.062 | 0.770 | 6.575 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `classic` | `profile_fast` | 5.062 | 0.846 | 5.985 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 5.062 | 0.609 | 8.315 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 5.062 | 0.687 | 7.370 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `classic` | `strict_current` | 5.062 | 0.768 | 6.588 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `ax` | `profile_balanced` | 3.881 | 0.957 | 4.054 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `ax` | `profile_fast` | 3.881 | 0.810 | 4.794 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 3.881 | 0.716 | 5.419 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `ax` | `skip_source_error_control` | 3.881 | 0.792 | 4.902 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `ax` | `strict_current` | 3.881 | 0.957 | 4.054 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `classic` | `profile_balanced` | 5.214 | 0.957 | 5.446 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `classic` | `profile_fast` | 5.214 | 0.810 | 6.440 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.214 | 0.716 | 7.279 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `classic` | `skip_source_error_control` | 5.214 | 0.792 | 6.585 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `classic` | `strict_current` | 5.214 | 0.957 | 5.446 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.075 | 0.876 | 1.227 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `ax` | `profile_fast` | 1.075 | 0.646 | 1.663 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.075 | 0.665 | 1.615 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.075 | 0.610 | 1.763 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `ax` | `strict_current` | 1.075 | 0.874 | 1.230 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.750 | 0.876 | 5.422 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `classic` | `profile_fast` | 4.750 | 0.646 | 7.352 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.750 | 0.665 | 7.138 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.750 | 0.610 | 7.792 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `classic` | `strict_current` | 4.750 | 0.874 | 5.437 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `ax` | `profile_balanced` | 1.481 | 0.761 | 1.947 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `ax` | `profile_fast` | 1.481 | 0.652 | 2.271 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.481 | 0.683 | 2.168 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.481 | 0.747 | 1.983 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `ax` | `strict_current` | 1.481 | 0.842 | 1.759 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `classic` | `profile_balanced` | 5.165 | 0.761 | 6.790 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `classic` | `profile_fast` | 5.165 | 0.652 | 7.918 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.165 | 0.683 | 7.560 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `classic` | `skip_source_error_control` | 5.165 | 0.747 | 6.915 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `classic` | `strict_current` | 5.165 | 0.842 | 6.133 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 0.857 | 2.762 | 0.310 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `ax` | `profile_fast` | 0.857 | 1.640 | 0.523 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 0.857 | 1.483 | 0.578 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 0.857 | 2.768 | 0.310 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 0.857 | 3.042 | 0.282 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.006 | 2.762 | 1.450 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.006 | 1.640 | 2.443 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.006 | 1.483 | 2.701 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.006 | 2.768 | 1.447 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.006 | 3.042 | 1.317 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `ax` | `profile_balanced` | 1.226 | 2.766 | 0.443 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `ax` | `profile_fast` | 1.226 | 1.724 | 0.711 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.226 | 1.372 | 0.893 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.226 | 2.826 | 0.434 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `ax` | `strict_current` | 1.226 | 2.958 | 0.415 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `classic` | `profile_balanced` | 4.047 | 2.766 | 1.463 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `classic` | `profile_fast` | 4.047 | 1.724 | 2.347 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.047 | 1.372 | 2.949 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `classic` | `skip_source_error_control` | 4.047 | 2.826 | 1.432 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `classic` | `strict_current` | 4.047 | 2.958 | 1.368 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `ax` | `profile_balanced` | 0.755 | 2.789 | 0.271 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `ax` | `profile_fast` | 0.755 | 1.667 | 0.453 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.755 | 1.346 | 0.561 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 0.755 | 2.834 | 0.266 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `ax` | `strict_current` | 0.755 | 2.997 | 0.252 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `classic` | `profile_balanced` | 3.698 | 2.789 | 1.326 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `classic` | `profile_fast` | 3.698 | 1.667 | 2.218 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.698 | 1.346 | 2.747 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 3.698 | 2.834 | 1.305 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `classic` | `strict_current` | 3.698 | 2.997 | 1.234 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `ax` | `profile_balanced` | 1.113 | 2.855 | 0.390 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `ax` | `profile_fast` | 1.113 | 1.667 | 0.668 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.113 | 1.436 | 0.775 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.113 | 2.963 | 0.376 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `ax` | `strict_current` | 1.113 | 3.104 | 0.359 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `classic` | `profile_balanced` | 4.042 | 2.855 | 1.416 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `classic` | `profile_fast` | 4.042 | 1.667 | 2.424 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.042 | 1.436 | 2.814 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.042 | 2.963 | 1.364 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `classic` | `strict_current` | 4.042 | 3.104 | 1.302 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `ax` | `profile_balanced` | 0.906 | 8.839 | 0.103 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `ax` | `profile_fast` | 0.906 | 2.926 | 0.310 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.906 | 0.985 | 0.920 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 0.906 | 1.244 | 0.729 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `ax` | `strict_current` | 0.906 | 9.002 | 0.101 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `classic` | `profile_balanced` | 5.531 | 8.839 | 0.626 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `classic` | `profile_fast` | 5.531 | 2.926 | 1.890 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.531 | 0.985 | 5.618 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 5.531 | 1.244 | 4.447 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `classic` | `strict_current` | 5.531 | 9.002 | 0.614 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `ax` | `profile_balanced` | 1.042 | 8.669 | 0.120 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `ax` | `profile_fast` | 1.042 | 2.967 | 0.351 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.042 | 0.934 | 1.116 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.042 | 1.290 | 0.808 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `ax` | `strict_current` | 1.042 | 8.708 | 0.120 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `classic` | `profile_balanced` | 5.095 | 8.669 | 0.588 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `classic` | `profile_fast` | 5.095 | 2.967 | 1.717 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.095 | 0.934 | 5.456 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `classic` | `skip_source_error_control` | 5.095 | 1.290 | 3.951 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `classic` | `strict_current` | 5.095 | 8.708 | 0.585 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `ax` | `profile_balanced` | 0.984 | 1.652 | 0.596 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `ax` | `profile_fast` | 0.984 | 0.954 | 1.032 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.984 | 0.597 | 1.649 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 0.984 | 0.652 | 1.510 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `ax` | `strict_current` | 0.984 | 1.621 | 0.607 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.286 | 1.652 | 2.594 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `classic` | `profile_fast` | 4.286 | 0.954 | 4.493 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.286 | 0.597 | 7.180 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.286 | 0.652 | 6.575 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `classic` | `strict_current` | 4.286 | 1.621 | 2.644 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `ax` | `profile_balanced` | 1.316 | 1.464 | 0.899 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `ax` | `profile_fast` | 1.316 | 0.926 | 1.421 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.316 | 0.588 | 2.240 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.316 | 0.632 | 2.082 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `ax` | `strict_current` | 1.316 | 1.479 | 0.890 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `classic` | `profile_balanced` | 4.679 | 1.464 | 3.196 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `classic` | `profile_fast` | 4.679 | 0.926 | 5.050 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.679 | 0.588 | 7.961 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.679 | 0.632 | 7.402 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `classic` | `strict_current` | 4.679 | 1.479 | 3.164 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.431 | 3.316 | 0.432 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `ax` | `profile_fast` | 1.431 | 3.331 | 0.430 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.431 | 3.239 | 0.442 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.431 | 3.151 | 0.454 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `ax` | `strict_current` | 1.431 | 3.368 | 0.425 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.499 | 3.316 | 1.357 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `classic` | `profile_fast` | 4.499 | 3.331 | 1.351 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.499 | 3.239 | 1.389 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.499 | 3.151 | 1.428 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `classic` | `strict_current` | 4.499 | 3.368 | 1.336 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `ax` | `profile_balanced` | 1.247 | 3.310 | 0.377 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `ax` | `profile_fast` | 1.247 | 3.221 | 0.387 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.247 | 3.168 | 0.394 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.247 | 3.160 | 0.394 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `ax` | `strict_current` | 1.247 | 3.464 | 0.360 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `classic` | `profile_balanced` | 4.348 | 3.310 | 1.314 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `classic` | `profile_fast` | 4.348 | 3.221 | 1.350 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.348 | 3.168 | 1.373 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.348 | 3.160 | 1.376 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `classic` | `strict_current` | 4.348 | 3.464 | 1.255 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.550 | 1.265 | 1.225 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `ax` | `profile_fast` | 1.550 | 1.039 | 1.492 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.550 | 0.739 | 2.097 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.550 | 0.885 | 1.751 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `ax` | `strict_current` | 1.550 | 1.202 | 1.289 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `classic` | `profile_balanced` | 5.583 | 1.265 | 4.413 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `classic` | `profile_fast` | 5.583 | 1.039 | 5.376 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.583 | 0.739 | 7.553 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 5.583 | 0.885 | 6.305 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `classic` | `strict_current` | 5.583 | 1.202 | 4.644 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `ax` | `profile_balanced` | 1.077 | 1.071 | 1.005 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `ax` | `profile_fast` | 1.077 | 0.870 | 1.238 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.077 | 0.614 | 1.753 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.077 | 0.554 | 1.943 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `ax` | `strict_current` | 1.077 | 1.320 | 0.816 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `classic` | `profile_balanced` | 4.613 | 1.071 | 4.306 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `classic` | `profile_fast` | 4.613 | 0.870 | 5.304 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.613 | 0.614 | 7.509 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.613 | 0.554 | 8.323 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `classic` | `strict_current` | 4.613 | 1.320 | 3.495 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.245 | 1.044 | 1.193 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `ax` | `profile_fast` | 1.245 | 0.899 | 1.386 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.245 | 0.774 | 1.609 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.245 | 0.733 | 1.699 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `ax` | `strict_current` | 1.245 | 1.050 | 1.186 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `classic` | `profile_balanced` | 5.251 | 1.044 | 5.030 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `classic` | `profile_fast` | 5.251 | 0.899 | 5.843 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.251 | 0.774 | 6.782 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 5.251 | 0.733 | 7.162 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `classic` | `strict_current` | 5.251 | 1.050 | 5.002 |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `ax` | `profile_balanced` | 1.489 | 0.782 | 1.904 |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `ax` | `profile_fast` | 1.489 | 0.832 | 1.790 |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.489 | 0.799 | 1.865 |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.489 | 0.787 | 1.893 |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `ax` | `strict_current` | 1.489 | 0.807 | 1.846 |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `classic` | `profile_balanced` | 5.356 | 0.782 | 6.845 |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `classic` | `profile_fast` | 5.356 | 0.832 | 6.437 |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.356 | 0.799 | 6.706 |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `classic` | `skip_source_error_control` | 5.356 | 0.787 | 6.808 |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `classic` | `strict_current` | 5.356 | 0.807 | 6.639 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.241 | 1.380 | 0.899 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `ax` | `profile_fast` | 1.241 | 0.872 | 1.423 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.241 | 0.621 | 1.998 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.241 | 0.669 | 1.855 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `ax` | `strict_current` | 1.241 | 1.621 | 0.765 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.512 | 1.380 | 3.269 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `classic` | `profile_fast` | 4.512 | 0.872 | 5.176 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.512 | 0.621 | 7.265 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.512 | 0.669 | 6.748 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `classic` | `strict_current` | 4.512 | 1.621 | 2.784 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `ax` | `profile_balanced` | 1.101 | 1.364 | 0.807 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `ax` | `profile_fast` | 1.101 | 1.007 | 1.094 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.101 | 0.705 | 1.563 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.101 | 0.620 | 1.776 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `ax` | `strict_current` | 1.101 | 1.418 | 0.777 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `classic` | `profile_balanced` | 4.496 | 1.364 | 3.297 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `classic` | `profile_fast` | 4.496 | 1.007 | 4.467 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.496 | 0.705 | 6.381 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.496 | 0.620 | 7.250 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `classic` | `strict_current` | 4.496 | 1.418 | 3.172 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.485 | 1.354 | 1.097 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `ax` | `profile_fast` | 1.485 | 1.278 | 1.162 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.485 | 1.231 | 1.206 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.485 | 1.068 | 1.391 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `ax` | `strict_current` | 1.485 | 1.444 | 1.028 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `classic` | `profile_balanced` | 5.047 | 1.354 | 3.727 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `classic` | `profile_fast` | 5.047 | 1.278 | 3.950 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.047 | 1.231 | 4.100 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 5.047 | 1.068 | 4.728 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `classic` | `strict_current` | 5.047 | 1.444 | 3.495 |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `ax` | `profile_balanced` | 1.126 | 1.385 | 0.813 |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `ax` | `profile_fast` | 1.126 | 1.287 | 0.875 |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.126 | 1.128 | 0.998 |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.126 | 1.193 | 0.943 |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `ax` | `strict_current` | 1.126 | 1.446 | 0.778 |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `classic` | `profile_balanced` | 5.005 | 1.385 | 3.614 |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `classic` | `profile_fast` | 5.005 | 1.287 | 3.890 |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.005 | 1.128 | 4.439 |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `classic` | `skip_source_error_control` | 5.005 | 1.193 | 4.196 |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `classic` | `strict_current` | 5.005 | 1.446 | 3.461 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.562 | 11.561 | 0.135 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `ax` | `profile_fast` | 1.562 | 11.265 | 0.139 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.562 | 11.426 | 0.137 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.562 | 11.510 | 0.136 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `ax` | `strict_current` | 1.562 | 11.654 | 0.134 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `classic` | `profile_balanced` | 7.638 | 11.561 | 0.661 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `classic` | `profile_fast` | 7.638 | 11.265 | 0.678 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 7.638 | 11.426 | 0.668 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 7.638 | 11.510 | 0.664 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `classic` | `strict_current` | 7.638 | 11.654 | 0.655 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `ax` | `profile_balanced` | 1.634 | 11.429 | 0.143 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `ax` | `profile_fast` | 1.634 | 11.563 | 0.141 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.634 | 11.528 | 0.142 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.634 | 11.698 | 0.140 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `ax` | `strict_current` | 1.634 | 12.077 | 0.135 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `classic` | `profile_balanced` | 8.501 | 11.429 | 0.744 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `classic` | `profile_fast` | 8.501 | 11.563 | 0.735 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 8.501 | 11.528 | 0.737 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `classic` | `skip_source_error_control` | 8.501 | 11.698 | 0.727 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `classic` | `strict_current` | 8.501 | 12.077 | 0.704 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `ax` | `profile_balanced` | 0.717 | 1.980 | 0.362 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `ax` | `profile_fast` | 0.717 | 1.614 | 0.444 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.717 | 1.484 | 0.483 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 0.717 | 1.418 | 0.506 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `ax` | `strict_current` | 0.717 | 2.552 | 0.281 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `classic` | `profile_balanced` | 3.759 | 1.980 | 1.898 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `classic` | `profile_fast` | 3.759 | 1.614 | 2.329 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.759 | 1.484 | 2.532 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 3.759 | 1.418 | 2.651 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `classic` | `strict_current` | 3.759 | 2.552 | 1.473 |
| `vbr1_l2_event_controller` | `tb` | `gold` | `ax` | `profile_balanced` | 1.241 | 1.888 | 0.657 |
| `vbr1_l2_event_controller` | `tb` | `gold` | `ax` | `profile_fast` | 1.241 | 1.646 | 0.754 |
| `vbr1_l2_event_controller` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.241 | 1.345 | 0.922 |
| `vbr1_l2_event_controller` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.241 | 1.650 | 0.752 |
| `vbr1_l2_event_controller` | `tb` | `gold` | `ax` | `strict_current` | 1.241 | 2.412 | 0.514 |
| `vbr1_l2_event_controller` | `tb` | `gold` | `classic` | `profile_balanced` | 4.147 | 1.888 | 2.197 |
| `vbr1_l2_event_controller` | `tb` | `gold` | `classic` | `profile_fast` | 4.147 | 1.646 | 2.519 |
| `vbr1_l2_event_controller` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.147 | 1.345 | 3.083 |
| `vbr1_l2_event_controller` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.147 | 1.650 | 2.513 |
| `vbr1_l2_event_controller` | `tb` | `gold` | `classic` | `strict_current` | 4.147 | 2.412 | 1.719 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `ax` | `profile_balanced` | 0.954 | 1.601 | 0.596 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `ax` | `profile_fast` | 0.954 | 0.912 | 1.045 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.954 | 0.724 | 1.317 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 0.954 | 0.725 | 1.315 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `ax` | `strict_current` | 0.954 | 1.632 | 0.584 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.347 | 1.601 | 2.715 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `classic` | `profile_fast` | 4.347 | 0.912 | 4.764 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.347 | 0.724 | 6.003 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.347 | 0.725 | 5.992 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `classic` | `strict_current` | 4.347 | 1.632 | 2.663 |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `ax` | `profile_balanced` | 1.077 | 1.480 | 0.728 |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `ax` | `profile_fast` | 1.077 | 0.975 | 1.105 |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.077 | 0.774 | 1.392 |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.077 | 0.766 | 1.407 |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `ax` | `strict_current` | 1.077 | 1.602 | 0.673 |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `classic` | `profile_balanced` | 4.797 | 1.480 | 3.241 |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `classic` | `profile_fast` | 4.797 | 0.975 | 4.920 |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.797 | 0.774 | 6.198 |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.797 | 0.766 | 6.266 |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `classic` | `strict_current` | 4.797 | 1.602 | 2.995 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `ax` | `profile_balanced` | 4.305 | 126.930 | 0.034 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `ax` | `profile_fast` | 4.305 | 108.032 | 0.040 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 4.305 | 8.947 | 0.481 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 4.305 | 10.863 | 0.396 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `ax` | `strict_current` | 4.305 | 126.150 | 0.034 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `classic` | `profile_balanced` | 11.788 | 126.930 | 0.093 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `classic` | `profile_fast` | 11.788 | 108.032 | 0.109 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 11.788 | 8.947 | 1.318 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 11.788 | 10.863 | 1.085 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `classic` | `strict_current` | 11.788 | 126.150 | 0.093 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `ax` | `profile_balanced` | 5.743 | 150.482 | 0.038 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `ax` | `profile_fast` | 5.743 | 130.434 | 0.044 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.743 | 32.383 | 0.177 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `ax` | `skip_source_error_control` | 5.743 | 34.954 | 0.164 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `ax` | `strict_current` | 5.743 | 150.862 | 0.038 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `classic` | `profile_balanced` | 12.627 | 150.482 | 0.084 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `classic` | `profile_fast` | 12.627 | 130.434 | 0.097 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 12.627 | 32.383 | 0.390 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `classic` | `skip_source_error_control` | 12.627 | 34.954 | 0.361 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `classic` | `strict_current` | 12.627 | 150.862 | 0.084 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.391 | 1.818 | 0.765 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `ax` | `profile_fast` | 1.391 | 1.561 | 0.891 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.391 | 1.386 | 1.004 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.391 | 1.476 | 0.942 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `ax` | `strict_current` | 1.391 | 2.244 | 0.620 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.268 | 1.818 | 2.348 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `classic` | `profile_fast` | 4.268 | 1.561 | 2.734 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.268 | 1.386 | 3.080 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.268 | 1.476 | 2.890 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `classic` | `strict_current` | 4.268 | 2.244 | 1.901 |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `ax` | `profile_balanced` | 0.641 | 1.823 | 0.352 |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `ax` | `profile_fast` | 0.641 | 1.672 | 0.384 |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.641 | 1.400 | 0.458 |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `ax` | `skip_source_error_control` | 0.641 | 1.488 | 0.431 |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `ax` | `strict_current` | 0.641 | 2.309 | 0.278 |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `classic` | `profile_balanced` | 3.741 | 1.823 | 2.052 |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `classic` | `profile_fast` | 3.741 | 1.672 | 2.238 |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.741 | 1.400 | 2.672 |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `classic` | `skip_source_error_control` | 3.741 | 1.488 | 2.513 |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `classic` | `strict_current` | 3.741 | 2.309 | 1.620 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.104 | 10.760 | 0.103 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `ax` | `profile_fast` | 1.104 | 10.591 | 0.104 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.104 | 9.768 | 0.113 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.104 | 10.193 | 0.108 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `ax` | `strict_current` | 1.104 | 10.757 | 0.103 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.351 | 10.760 | 0.404 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `classic` | `profile_fast` | 4.351 | 10.591 | 0.411 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.351 | 9.768 | 0.445 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.351 | 10.193 | 0.427 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `classic` | `strict_current` | 4.351 | 10.757 | 0.404 |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `ax` | `profile_balanced` | 1.391 | 10.425 | 0.133 |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `ax` | `profile_fast` | 1.391 | 10.067 | 0.138 |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.391 | 9.432 | 0.147 |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.391 | 9.880 | 0.141 |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `ax` | `strict_current` | 1.391 | 10.290 | 0.135 |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `classic` | `profile_balanced` | 4.451 | 10.425 | 0.427 |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `classic` | `profile_fast` | 4.451 | 10.067 | 0.442 |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.451 | 9.432 | 0.472 |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.451 | 9.880 | 0.450 |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `classic` | `strict_current` | 4.451 | 10.290 | 0.433 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `ax` | `profile_balanced` | 0.946 | 2.019 | 0.469 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `ax` | `profile_fast` | 0.946 | 1.189 | 0.796 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.946 | 1.011 | 0.936 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 0.946 | 1.015 | 0.932 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `ax` | `strict_current` | 0.946 | 2.103 | 0.450 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.176 | 2.019 | 2.068 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `classic` | `profile_fast` | 4.176 | 1.189 | 3.512 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.176 | 1.011 | 4.130 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.176 | 1.015 | 4.114 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `classic` | `strict_current` | 4.176 | 2.103 | 1.986 |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `ax` | `profile_balanced` | 0.890 | 1.948 | 0.457 |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `ax` | `profile_fast` | 0.890 | 1.297 | 0.686 |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.890 | 0.882 | 1.009 |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `ax` | `skip_source_error_control` | 0.890 | 0.986 | 0.903 |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `ax` | `strict_current` | 0.890 | 2.047 | 0.435 |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `classic` | `profile_balanced` | 4.599 | 1.948 | 2.361 |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `classic` | `profile_fast` | 4.599 | 1.297 | 3.547 |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.599 | 0.882 | 5.216 |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.599 | 0.986 | 4.665 |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `classic` | `strict_current` | 4.599 | 2.047 | 2.246 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.183 | 15.724 | 0.075 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `ax` | `profile_fast` | 1.183 | 7.865 | 0.150 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.183 | 1.006 | 1.176 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.183 | 1.031 | 1.147 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `ax` | `strict_current` | 1.183 | 16.093 | 0.073 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `classic` | `profile_balanced` | 8.683 | 15.724 | 0.552 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `classic` | `profile_fast` | 8.683 | 7.865 | 1.104 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 8.683 | 1.006 | 8.633 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 8.683 | 1.031 | 8.422 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `classic` | `strict_current` | 8.683 | 16.093 | 0.540 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `ax` | `profile_balanced` | 1.212 | 17.479 | 0.069 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `ax` | `profile_fast` | 1.212 | 8.913 | 0.136 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.212 | 2.470 | 0.491 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.212 | 2.359 | 0.514 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `ax` | `strict_current` | 1.212 | 17.465 | 0.069 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `classic` | `profile_balanced` | 7.767 | 17.479 | 0.444 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `classic` | `profile_fast` | 7.767 | 8.913 | 0.871 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 7.767 | 2.470 | 3.145 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `classic` | `skip_source_error_control` | 7.767 | 2.359 | 3.292 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `classic` | `strict_current` | 7.767 | 17.465 | 0.445 |

## Accuracy-Gated Speedups

| Entry | Form | Variant | Spectre mode | EVAS mode | Spectre wall s | EVAS wall s | Spectre/EVAS |
| --- | --- | --- | --- | --- | ---: | ---: | ---: |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.113 | 1.181 | 0.942 |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.113 | 0.968 | 1.150 |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.113 | 0.757 | 1.470 |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.113 | 0.799 | 1.392 |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.113 | 1.040 | 1.070 |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.632 | 1.181 | 3.923 |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.632 | 0.968 | 4.787 |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.632 | 0.757 | 6.117 |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.632 | 0.799 | 5.795 |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.632 | 1.040 | 4.456 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `ax` | `profile_balanced` | 0.928 | 1.160 | 0.800 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `ax` | `profile_fast` | 0.928 | 0.882 | 1.052 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.928 | 1.065 | 0.872 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `ax` | `skip_source_error_control` | 0.928 | 0.823 | 1.128 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `ax` | `strict_current` | 0.928 | 1.219 | 0.762 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `classic` | `profile_balanced` | 4.221 | 1.160 | 3.638 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `classic` | `profile_fast` | 4.221 | 0.882 | 4.785 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.221 | 1.065 | 3.964 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `classic` | `skip_source_error_control` | 4.221 | 0.823 | 5.131 |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `classic` | `strict_current` | 4.221 | 1.219 | 3.463 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.141 | 1.173 | 0.973 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `ax` | `profile_fast` | 1.141 | 0.957 | 1.191 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.141 | 0.821 | 1.389 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.141 | 0.904 | 1.262 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `ax` | `strict_current` | 1.141 | 1.239 | 0.920 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.606 | 1.173 | 3.927 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `classic` | `profile_fast` | 4.606 | 0.957 | 4.811 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.606 | 0.821 | 5.607 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.606 | 0.904 | 5.097 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `classic` | `strict_current` | 4.606 | 1.239 | 3.716 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `ax` | `profile_balanced` | 1.216 | 1.181 | 1.029 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `ax` | `profile_fast` | 1.216 | 1.067 | 1.139 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.216 | 1.006 | 1.209 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.216 | 0.896 | 1.358 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `ax` | `strict_current` | 1.216 | 1.324 | 0.918 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `classic` | `profile_balanced` | 4.702 | 1.181 | 3.980 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `classic` | `profile_fast` | 4.702 | 1.067 | 4.406 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.702 | 1.006 | 4.675 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.702 | 0.896 | 5.250 |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `classic` | `strict_current` | 4.702 | 1.324 | 3.550 |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.380 | 10.800 | 0.128 |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.380 | 5.790 | 0.238 |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.380 | 1.125 | 1.227 |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.380 | 1.242 | 1.111 |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.380 | 10.551 | 0.131 |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 3.725 | 10.800 | 0.345 |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `classic` | `profile_fast` | 3.725 | 5.790 | 0.643 |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 3.725 | 1.125 | 3.312 |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 3.725 | 1.242 | 2.999 |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 3.725 | 10.551 | 0.353 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `ax` | `profile_balanced` | 0.792 | 10.647 | 0.074 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `ax` | `profile_fast` | 0.792 | 5.606 | 0.141 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.792 | 1.057 | 0.749 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `ax` | `skip_source_error_control` | 0.792 | 1.157 | 0.684 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `ax` | `strict_current` | 0.792 | 10.733 | 0.074 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `classic` | `profile_balanced` | 3.652 | 10.647 | 0.343 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `classic` | `profile_fast` | 3.652 | 5.606 | 0.652 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.652 | 1.057 | 3.456 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `classic` | `skip_source_error_control` | 3.652 | 1.157 | 3.158 |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `classic` | `strict_current` | 3.652 | 10.733 | 0.340 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.022 | 1.626 | 0.629 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `ax` | `profile_fast` | 1.022 | 1.550 | 0.660 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.022 | 1.516 | 0.674 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.022 | 1.371 | 0.746 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `ax` | `strict_current` | 1.022 | 1.658 | 0.617 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.136 | 1.626 | 2.544 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `classic` | `profile_fast` | 4.136 | 1.550 | 2.669 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.136 | 1.516 | 2.729 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.136 | 1.371 | 3.018 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `classic` | `strict_current` | 4.136 | 1.658 | 2.495 |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `ax` | `profile_balanced` | 1.085 | 1.783 | 0.609 |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `ax` | `profile_fast` | 1.085 | 1.488 | 0.729 |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.085 | 1.539 | 0.705 |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.085 | 1.458 | 0.744 |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `ax` | `strict_current` | 1.085 | 1.792 | 0.606 |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `classic` | `profile_balanced` | 4.459 | 1.783 | 2.501 |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `classic` | `profile_fast` | 4.459 | 1.488 | 2.997 |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.459 | 1.539 | 2.897 |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.459 | 1.458 | 3.059 |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `classic` | `strict_current` | 4.459 | 1.792 | 2.488 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 3.309 | 0.722 | 4.582 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `ax` | `profile_fast` | 3.309 | 0.709 | 4.667 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 3.309 | 0.691 | 4.788 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 3.309 | 0.719 | 4.604 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `ax` | `strict_current` | 3.309 | 0.782 | 4.229 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 5.395 | 0.722 | 7.469 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `classic` | `profile_fast` | 5.395 | 0.709 | 7.609 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 5.395 | 0.691 | 7.805 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 5.395 | 0.719 | 7.506 |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `fixed` | `classic` | `strict_current` | 5.395 | 0.782 | 6.895 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `ax` | `profile_balanced` | 3.687 | 0.700 | 5.269 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `ax` | `profile_fast` | 3.687 | 0.679 | 5.433 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 3.687 | 0.604 | 6.108 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `ax` | `skip_source_error_control` | 3.687 | 0.924 | 3.990 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `ax` | `strict_current` | 3.687 | 0.695 | 5.304 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `classic` | `profile_balanced` | 5.298 | 0.700 | 7.570 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `classic` | `profile_fast` | 5.298 | 0.679 | 7.806 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.298 | 0.604 | 8.775 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `classic` | `skip_source_error_control` | 5.298 | 0.924 | 5.733 |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `classic` | `strict_current` | 5.298 | 0.695 | 7.620 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.294 | 0.860 | 1.504 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `ax` | `profile_fast` | 1.294 | 0.726 | 1.783 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.294 | 0.594 | 2.179 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.294 | 0.661 | 1.959 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `ax` | `strict_current` | 1.294 | 0.820 | 1.579 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.979 | 0.860 | 5.786 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `classic` | `profile_fast` | 4.979 | 0.726 | 6.862 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.979 | 0.594 | 8.383 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.979 | 0.661 | 7.537 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `classic` | `strict_current` | 4.979 | 0.820 | 6.076 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `ax` | `profile_balanced` | 1.209 | 0.788 | 1.533 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `ax` | `profile_fast` | 1.209 | 0.805 | 1.502 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.209 | 0.683 | 1.770 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.209 | 0.688 | 1.756 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `ax` | `strict_current` | 1.209 | 0.904 | 1.336 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `classic` | `profile_balanced` | 4.827 | 0.788 | 6.122 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `classic` | `profile_fast` | 4.827 | 0.805 | 5.998 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.827 | 0.683 | 7.069 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.827 | 0.688 | 7.012 |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `classic` | `strict_current` | 4.827 | 0.904 | 5.337 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `ax` | `profile_balanced` | 1.516 | 1.189 | 1.276 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `ax` | `profile_fast` | 1.516 | 0.774 | 1.959 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.516 | 0.858 | 1.767 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.516 | 0.865 | 1.754 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `ax` | `strict_current` | 1.516 | 1.203 | 1.260 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `classic` | `profile_balanced` | 5.392 | 1.189 | 4.536 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `classic` | `profile_fast` | 5.392 | 0.774 | 6.965 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.392 | 0.858 | 6.283 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `classic` | `skip_source_error_control` | 5.392 | 0.865 | 6.237 |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `classic` | `strict_current` | 5.392 | 1.203 | 4.480 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `ax` | `profile_balanced` | 0.882 | 1.156 | 0.763 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `ax` | `profile_fast` | 0.882 | 0.753 | 1.172 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.882 | 0.800 | 1.103 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 0.882 | 0.668 | 1.322 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `ax` | `strict_current` | 0.882 | 1.168 | 0.755 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.538 | 1.156 | 3.925 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `classic` | `profile_fast` | 4.538 | 0.753 | 6.030 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.538 | 0.800 | 5.673 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.538 | 0.668 | 6.798 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `classic` | `strict_current` | 4.538 | 1.168 | 3.885 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `ax` | `profile_balanced` | 0.886 | 1.172 | 0.756 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `ax` | `profile_fast` | 0.886 | 0.668 | 1.326 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.886 | 0.794 | 1.116 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `ax` | `skip_source_error_control` | 0.886 | 0.821 | 1.079 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `ax` | `strict_current` | 0.886 | 1.182 | 0.750 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `classic` | `profile_balanced` | 4.276 | 1.172 | 3.649 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `classic` | `profile_fast` | 4.276 | 0.668 | 6.402 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.276 | 0.794 | 5.388 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.276 | 0.821 | 5.208 |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `classic` | `strict_current` | 4.276 | 1.182 | 3.619 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 0.912 | 1.542 | 0.591 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `ax` | `profile_fast` | 0.912 | 1.119 | 0.815 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 0.912 | 0.541 | 1.687 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 0.912 | 0.632 | 1.443 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `ax` | `strict_current` | 0.912 | 1.671 | 0.546 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.485 | 1.542 | 2.908 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.485 | 1.119 | 4.009 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.485 | 0.541 | 8.296 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.485 | 0.632 | 7.097 |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.485 | 1.671 | 2.684 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `ax` | `profile_balanced` | 0.992 | 1.445 | 0.687 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `ax` | `profile_fast` | 0.992 | 0.955 | 1.039 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.992 | 0.662 | 1.499 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `ax` | `skip_source_error_control` | 0.992 | 0.525 | 1.890 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `ax` | `strict_current` | 0.992 | 1.569 | 0.633 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `classic` | `profile_balanced` | 4.378 | 1.445 | 3.030 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `classic` | `profile_fast` | 4.378 | 0.955 | 4.583 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.378 | 0.662 | 6.612 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `classic` | `skip_source_error_control` | 4.378 | 0.525 | 8.339 |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `classic` | `strict_current` | 4.378 | 1.569 | 2.791 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.274 | 1.602 | 0.795 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `ax` | `profile_fast` | 1.274 | 0.998 | 1.276 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.274 | 0.586 | 2.173 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.274 | 0.605 | 2.105 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `ax` | `strict_current` | 1.274 | 1.706 | 0.747 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.942 | 1.602 | 3.084 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `classic` | `profile_fast` | 4.942 | 0.998 | 4.952 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.942 | 0.586 | 8.432 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.942 | 0.605 | 8.167 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `classic` | `strict_current` | 4.942 | 1.706 | 2.897 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `ax` | `profile_balanced` | 0.939 | 1.470 | 0.639 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `ax` | `profile_fast` | 0.939 | 0.973 | 0.965 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.939 | 0.605 | 1.551 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `ax` | `skip_source_error_control` | 0.939 | 0.534 | 1.760 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `ax` | `strict_current` | 0.939 | 1.439 | 0.652 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `classic` | `profile_balanced` | 4.109 | 1.470 | 2.795 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `classic` | `profile_fast` | 4.109 | 0.973 | 4.224 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.109 | 0.605 | 6.790 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.109 | 0.534 | 7.702 |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `classic` | `strict_current` | 4.109 | 1.439 | 2.856 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 0.887 | 3.447 | 0.257 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `ax` | `profile_fast` | 0.887 | 2.168 | 0.409 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 0.887 | 1.445 | 0.614 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 0.887 | 1.428 | 0.621 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `ax` | `strict_current` | 0.887 | 3.584 | 0.247 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.033 | 3.447 | 1.170 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.033 | 2.168 | 1.860 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.033 | 1.445 | 2.791 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.033 | 1.428 | 2.825 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.033 | 3.584 | 1.125 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `ax` | `profile_balanced` | 0.674 | 3.535 | 0.191 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `ax` | `profile_fast` | 0.674 | 1.978 | 0.341 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.674 | 1.358 | 0.496 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `ax` | `skip_source_error_control` | 0.674 | 1.405 | 0.480 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `ax` | `strict_current` | 0.674 | 3.570 | 0.189 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `classic` | `profile_balanced` | 3.919 | 3.535 | 1.109 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `classic` | `profile_fast` | 3.919 | 1.978 | 1.981 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.919 | 1.358 | 2.886 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `classic` | `skip_source_error_control` | 3.919 | 1.405 | 2.790 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `classic` | `strict_current` | 3.919 | 3.570 | 1.098 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.511 | 3.566 | 0.424 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `ax` | `profile_fast` | 1.511 | 1.998 | 0.756 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.511 | 1.503 | 1.005 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.511 | 1.417 | 1.067 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `ax` | `strict_current` | 1.511 | 3.468 | 0.436 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `classic` | `profile_balanced` | 3.914 | 3.566 | 1.098 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `classic` | `profile_fast` | 3.914 | 1.998 | 1.959 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.914 | 1.503 | 2.604 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 3.914 | 1.417 | 2.763 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `classic` | `strict_current` | 3.914 | 3.468 | 1.129 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `ax` | `profile_balanced` | 0.658 | 3.351 | 0.196 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `ax` | `profile_fast` | 0.658 | 2.004 | 0.328 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.658 | 1.529 | 0.430 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `ax` | `skip_source_error_control` | 0.658 | 1.536 | 0.428 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `ax` | `strict_current` | 0.658 | 3.555 | 0.185 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `classic` | `profile_balanced` | 4.466 | 3.351 | 1.333 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `classic` | `profile_fast` | 4.466 | 2.004 | 2.229 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.466 | 1.529 | 2.922 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.466 | 1.536 | 2.907 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `classic` | `strict_current` | 4.466 | 3.555 | 1.256 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 0.927 | 1.548 | 0.599 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `ax` | `profile_fast` | 0.927 | 0.971 | 0.954 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 0.927 | 0.740 | 1.253 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 0.927 | 0.609 | 1.523 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `ax` | `strict_current` | 0.927 | 1.489 | 0.622 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.202 | 1.548 | 2.715 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.202 | 0.971 | 4.327 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.202 | 0.740 | 5.680 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.202 | 0.609 | 6.902 |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.202 | 1.489 | 2.821 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `ax` | `profile_balanced` | 1.038 | 1.473 | 0.705 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `ax` | `profile_fast` | 1.038 | 0.919 | 1.129 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.038 | 0.747 | 1.390 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.038 | 0.540 | 1.921 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `ax` | `strict_current` | 1.038 | 1.584 | 0.655 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `classic` | `profile_balanced` | 4.149 | 1.473 | 2.818 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `classic` | `profile_fast` | 4.149 | 0.919 | 4.515 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.149 | 0.747 | 5.557 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `classic` | `skip_source_error_control` | 4.149 | 0.540 | 7.683 |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `classic` | `strict_current` | 4.149 | 1.584 | 2.620 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `ax` | `profile_balanced` | 0.909 | 1.349 | 0.674 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `ax` | `profile_fast` | 0.909 | 0.975 | 0.932 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.909 | 0.629 | 1.445 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 0.909 | 0.548 | 1.659 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `ax` | `strict_current` | 0.909 | 1.416 | 0.642 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.011 | 1.349 | 2.974 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `classic` | `profile_fast` | 4.011 | 0.975 | 4.116 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.011 | 0.629 | 6.379 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.011 | 0.548 | 7.324 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `classic` | `strict_current` | 4.011 | 1.416 | 2.834 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `ax` | `profile_balanced` | 1.220 | 1.462 | 0.834 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `ax` | `profile_fast` | 1.220 | 0.956 | 1.277 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.220 | 0.733 | 1.665 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.220 | 0.598 | 2.042 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `ax` | `strict_current` | 1.220 | 1.507 | 0.810 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `classic` | `profile_balanced` | 4.239 | 1.462 | 2.899 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `classic` | `profile_fast` | 4.239 | 0.956 | 4.435 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.239 | 0.733 | 5.786 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.239 | 0.598 | 7.093 |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `classic` | `strict_current` | 4.239 | 1.507 | 2.813 |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.117 | 4.015 | 0.278 |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.117 | 2.256 | 0.495 |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.117 | 1.144 | 0.977 |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.117 | 1.124 | 0.994 |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.117 | 4.079 | 0.274 |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.458 | 4.015 | 1.110 |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.458 | 2.256 | 1.976 |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.458 | 1.144 | 3.899 |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.458 | 1.124 | 3.968 |
| `vbr1_l1_clock_divider` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.458 | 4.079 | 1.093 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `ax` | `profile_balanced` | 0.865 | 3.826 | 0.226 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `ax` | `profile_fast` | 0.865 | 2.346 | 0.369 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.865 | 1.053 | 0.822 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `ax` | `skip_source_error_control` | 0.865 | 1.115 | 0.776 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `ax` | `strict_current` | 0.865 | 3.917 | 0.221 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `classic` | `profile_balanced` | 3.963 | 3.826 | 1.036 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `classic` | `profile_fast` | 3.963 | 2.346 | 1.689 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.963 | 1.053 | 3.765 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `classic` | `skip_source_error_control` | 3.963 | 1.115 | 3.554 |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `classic` | `strict_current` | 3.963 | 3.917 | 1.012 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.438 | 3.879 | 0.371 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `ax` | `profile_fast` | 1.438 | 2.382 | 0.604 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.438 | 1.125 | 1.279 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.438 | 1.169 | 1.230 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `ax` | `strict_current` | 1.438 | 3.955 | 0.364 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.287 | 3.879 | 1.105 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `classic` | `profile_fast` | 4.287 | 2.382 | 1.800 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.287 | 1.125 | 3.811 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.287 | 1.169 | 3.666 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `classic` | `strict_current` | 4.287 | 3.955 | 1.084 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `ax` | `profile_balanced` | 1.294 | 4.116 | 0.315 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `ax` | `profile_fast` | 1.294 | 2.281 | 0.567 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.294 | 1.054 | 1.228 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.294 | 1.145 | 1.130 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `ax` | `strict_current` | 1.294 | 4.000 | 0.324 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `classic` | `profile_balanced` | 3.923 | 4.116 | 0.953 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `classic` | `profile_fast` | 3.923 | 2.281 | 1.720 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.923 | 1.054 | 3.721 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `classic` | `skip_source_error_control` | 3.923 | 1.145 | 3.425 |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `classic` | `strict_current` | 3.923 | 4.000 | 0.981 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.240 | 1.545 | 0.802 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.240 | 0.907 | 1.367 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.240 | 0.759 | 1.633 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.240 | 0.712 | 1.742 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.240 | 1.519 | 0.816 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.705 | 1.545 | 3.046 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.705 | 0.907 | 5.188 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.705 | 0.759 | 6.199 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.705 | 0.712 | 6.610 |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.705 | 1.519 | 3.098 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `ax` | `profile_balanced` | 1.224 | 1.533 | 0.798 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `ax` | `profile_fast` | 1.224 | 0.938 | 1.305 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.224 | 0.825 | 1.484 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.224 | 0.780 | 1.568 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `ax` | `strict_current` | 1.224 | 1.581 | 0.774 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `classic` | `profile_balanced` | 4.392 | 1.533 | 2.866 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `classic` | `profile_fast` | 4.392 | 0.938 | 4.683 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.392 | 0.825 | 5.326 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `classic` | `skip_source_error_control` | 4.392 | 0.780 | 5.628 |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `classic` | `strict_current` | 4.392 | 1.581 | 2.779 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.129 | 1.523 | 0.741 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `ax` | `profile_fast` | 1.129 | 1.011 | 1.116 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.129 | 0.843 | 1.340 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.129 | 0.671 | 1.683 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `ax` | `strict_current` | 1.129 | 1.574 | 0.717 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.566 | 1.523 | 2.998 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `classic` | `profile_fast` | 4.566 | 1.011 | 4.516 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.566 | 0.843 | 5.419 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.566 | 0.671 | 6.807 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `classic` | `strict_current` | 4.566 | 1.574 | 2.901 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `ax` | `profile_balanced` | 1.073 | 1.595 | 0.673 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `ax` | `profile_fast` | 1.073 | 0.941 | 1.141 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.073 | 0.664 | 1.618 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.073 | 0.709 | 1.513 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `ax` | `strict_current` | 1.073 | 1.598 | 0.672 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `classic` | `profile_balanced` | 4.778 | 1.595 | 2.997 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `classic` | `profile_fast` | 4.778 | 0.941 | 5.078 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.778 | 0.664 | 7.201 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.778 | 0.709 | 6.737 |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `classic` | `strict_current` | 4.778 | 1.598 | 2.991 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 0.932 | 3.248 | 0.287 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast` | 0.932 | 1.401 | 0.665 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 0.932 | 0.896 | 1.040 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 0.932 | 1.938 | 0.481 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 0.932 | 3.300 | 0.282 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 3.799 | 3.248 | 1.170 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast` | 3.799 | 1.401 | 2.711 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 3.799 | 0.896 | 4.238 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 3.799 | 1.938 | 1.960 |
| `vbr1_l1_clocked_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 3.799 | 3.300 | 1.151 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `ax` | `profile_balanced` | 1.306 | 3.272 | 0.399 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `ax` | `profile_fast` | 1.306 | 1.450 | 0.901 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.306 | 0.885 | 1.477 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.306 | 2.083 | 0.627 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `ax` | `strict_current` | 1.306 | 3.278 | 0.399 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `classic` | `profile_balanced` | 4.432 | 3.272 | 1.355 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `classic` | `profile_fast` | 4.432 | 1.450 | 3.056 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.432 | 0.885 | 5.009 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `classic` | `skip_source_error_control` | 4.432 | 2.083 | 2.128 |
| `vbr1_l1_clocked_comparator` | `dut` | `gold` | `classic` | `strict_current` | 4.432 | 3.278 | 1.352 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `ax` | `profile_balanced` | 0.750 | 3.047 | 0.246 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `ax` | `profile_fast` | 0.750 | 1.435 | 0.522 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.750 | 0.870 | 0.862 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 0.750 | 1.981 | 0.378 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 0.750 | 3.176 | 0.236 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `classic` | `profile_balanced` | 3.665 | 3.047 | 1.203 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `classic` | `profile_fast` | 3.665 | 1.435 | 2.553 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.665 | 0.870 | 4.214 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 3.665 | 1.981 | 1.850 |
| `vbr1_l1_clocked_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 3.665 | 3.176 | 1.154 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `ax` | `profile_balanced` | 0.983 | 3.048 | 0.322 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `ax` | `profile_fast` | 0.983 | 1.381 | 0.712 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.983 | 0.861 | 1.142 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `ax` | `skip_source_error_control` | 0.983 | 1.916 | 0.513 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `ax` | `strict_current` | 0.983 | 3.024 | 0.325 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `classic` | `profile_balanced` | 4.050 | 3.048 | 1.329 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `classic` | `profile_fast` | 4.050 | 1.381 | 2.933 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.050 | 0.861 | 4.706 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.050 | 1.916 | 2.114 |
| `vbr1_l1_clocked_comparator` | `tb` | `gold` | `classic` | `strict_current` | 4.050 | 3.024 | 1.340 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.289 | 1.287 | 1.001 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.289 | 0.897 | 1.437 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.289 | 0.685 | 1.882 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.289 | 0.739 | 1.745 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.289 | 1.272 | 1.013 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 2.653 | 1.287 | 2.061 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `classic` | `profile_fast` | 2.653 | 0.897 | 2.957 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 2.653 | 0.685 | 3.874 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 2.653 | 0.739 | 3.592 |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `fixed` | `classic` | `strict_current` | 2.653 | 1.272 | 2.085 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `ax` | `profile_balanced` | 1.689 | 1.232 | 1.371 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `ax` | `profile_fast` | 1.689 | 0.744 | 2.272 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.689 | 0.847 | 1.994 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.689 | 0.789 | 2.140 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `ax` | `strict_current` | 1.689 | 1.274 | 1.325 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `classic` | `profile_balanced` | 3.561 | 1.232 | 2.890 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `classic` | `profile_fast` | 3.561 | 0.744 | 4.789 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.561 | 0.847 | 4.203 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `classic` | `skip_source_error_control` | 3.561 | 0.789 | 4.512 |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `classic` | `strict_current` | 3.561 | 1.274 | 2.794 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `ax` | `profile_balanced` | 0.742 | 1.357 | 0.547 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `ax` | `profile_fast` | 0.742 | 0.916 | 0.810 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.742 | 0.718 | 1.033 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 0.742 | 0.717 | 1.035 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `ax` | `strict_current` | 0.742 | 1.428 | 0.519 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `classic` | `profile_balanced` | 2.354 | 1.357 | 1.735 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `classic` | `profile_fast` | 2.354 | 0.916 | 2.570 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.354 | 0.718 | 3.277 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 2.354 | 0.717 | 3.284 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `classic` | `strict_current` | 2.354 | 1.428 | 1.648 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `ax` | `profile_balanced` | 0.930 | 1.282 | 0.725 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `ax` | `profile_fast` | 0.930 | 0.735 | 1.265 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.930 | 0.601 | 1.546 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `ax` | `skip_source_error_control` | 0.930 | 0.754 | 1.233 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `ax` | `strict_current` | 0.930 | 1.465 | 0.634 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `classic` | `profile_balanced` | 2.466 | 1.282 | 1.924 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `classic` | `profile_fast` | 2.466 | 0.735 | 3.356 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.466 | 0.601 | 4.100 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `classic` | `skip_source_error_control` | 2.466 | 0.754 | 3.270 |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `classic` | `strict_current` | 2.466 | 1.465 | 1.683 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `ax` | `profile_balanced` | 1.352 | 0.683 | 1.980 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `ax` | `profile_fast` | 1.352 | 0.777 | 1.740 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.352 | 0.506 | 2.675 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.352 | 0.793 | 1.705 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `ax` | `strict_current` | 1.352 | 0.790 | 1.711 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `classic` | `profile_balanced` | 3.038 | 0.683 | 4.448 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `classic` | `profile_fast` | 3.038 | 0.777 | 3.908 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.038 | 0.506 | 6.009 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `classic` | `skip_source_error_control` | 3.038 | 0.793 | 3.829 |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `classic` | `strict_current` | 3.038 | 0.790 | 3.844 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.456 | 0.666 | 2.187 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `ax` | `profile_fast` | 1.456 | 0.582 | 2.501 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.456 | 0.722 | 2.016 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.456 | 0.644 | 2.262 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `ax` | `strict_current` | 1.456 | 0.848 | 1.717 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `classic` | `profile_balanced` | 3.452 | 0.666 | 5.184 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `classic` | `profile_fast` | 3.452 | 0.582 | 5.928 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.452 | 0.722 | 4.779 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 3.452 | 0.644 | 5.363 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `classic` | `strict_current` | 3.452 | 0.848 | 4.070 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `ax` | `profile_balanced` | 1.291 | 0.682 | 1.894 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `ax` | `profile_fast` | 1.291 | 0.576 | 2.243 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.291 | 0.580 | 2.225 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.291 | 0.540 | 2.393 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `ax` | `strict_current` | 1.291 | 0.778 | 1.660 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `classic` | `profile_balanced` | 3.278 | 0.682 | 4.808 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `classic` | `profile_fast` | 3.278 | 0.576 | 5.694 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.278 | 0.580 | 5.650 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `classic` | `skip_source_error_control` | 3.278 | 0.540 | 6.075 |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `classic` | `strict_current` | 3.278 | 0.778 | 4.214 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.490 | 0.590 | 2.525 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.490 | 0.577 | 2.583 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.490 | 0.540 | 2.757 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.490 | 0.557 | 2.674 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.490 | 0.568 | 2.624 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.654 | 0.590 | 7.884 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.654 | 0.577 | 8.065 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.654 | 0.540 | 8.611 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.654 | 0.557 | 8.352 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.654 | 0.568 | 8.193 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `ax` | `profile_balanced` | 1.311 | 0.783 | 1.675 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `ax` | `profile_fast` | 1.311 | 0.661 | 1.983 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.311 | 0.651 | 2.014 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.311 | 0.669 | 1.961 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `ax` | `strict_current` | 1.311 | 0.812 | 1.614 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `classic` | `profile_balanced` | 4.804 | 0.783 | 6.135 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `classic` | `profile_fast` | 4.804 | 0.661 | 7.265 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.804 | 0.651 | 7.379 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `classic` | `skip_source_error_control` | 4.804 | 0.669 | 7.184 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `classic` | `strict_current` | 4.804 | 0.812 | 5.915 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.504 | 0.599 | 2.510 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `ax` | `profile_fast` | 1.504 | 0.821 | 1.831 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.504 | 0.673 | 2.233 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.504 | 0.615 | 2.445 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `ax` | `strict_current` | 1.504 | 0.600 | 2.507 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `classic` | `profile_balanced` | 5.477 | 0.599 | 9.143 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `classic` | `profile_fast` | 5.477 | 0.821 | 6.668 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.477 | 0.673 | 8.135 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 5.477 | 0.615 | 8.906 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `classic` | `strict_current` | 5.477 | 0.600 | 9.131 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `ax` | `profile_balanced` | 0.996 | 0.544 | 1.829 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `ax` | `profile_fast` | 0.996 | 0.600 | 1.659 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.996 | 0.533 | 1.869 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `ax` | `skip_source_error_control` | 0.996 | 0.617 | 1.614 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `ax` | `strict_current` | 0.996 | 0.635 | 1.567 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `classic` | `profile_balanced` | 4.753 | 0.544 | 8.735 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `classic` | `profile_fast` | 4.753 | 0.600 | 7.921 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.753 | 0.533 | 8.923 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.753 | 0.617 | 7.704 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `classic` | `strict_current` | 4.753 | 0.635 | 7.482 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 4.157 | 1.094 | 3.802 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `ax` | `profile_fast` | 4.157 | 1.029 | 4.042 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 4.157 | 0.686 | 6.056 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 4.157 | 0.758 | 5.483 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `ax` | `strict_current` | 4.157 | 1.205 | 3.449 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 5.535 | 1.094 | 5.061 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `classic` | `profile_fast` | 5.535 | 1.029 | 5.381 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 5.535 | 0.686 | 8.062 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 5.535 | 0.758 | 7.300 |
| `vbr1_l1_debounce_latch` | `bugfix` | `fixed` | `classic` | `strict_current` | 5.535 | 1.205 | 4.591 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `ax` | `profile_balanced` | 1.154 | 0.780 | 1.479 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `ax` | `profile_fast` | 1.154 | 0.632 | 1.825 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.154 | 0.711 | 1.623 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.154 | 0.538 | 2.143 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `ax` | `strict_current` | 1.154 | 0.987 | 1.169 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `classic` | `profile_balanced` | 5.921 | 0.780 | 7.587 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `classic` | `profile_fast` | 5.921 | 0.632 | 9.363 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.921 | 0.711 | 8.330 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `classic` | `skip_source_error_control` | 5.921 | 0.538 | 10.999 |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `classic` | `strict_current` | 5.921 | 0.987 | 6.000 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.079 | 0.767 | 1.408 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `ax` | `profile_fast` | 1.079 | 0.663 | 1.628 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.079 | 0.632 | 1.707 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.079 | 0.523 | 2.062 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `ax` | `strict_current` | 1.079 | 0.836 | 1.291 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.867 | 0.767 | 6.347 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `classic` | `profile_fast` | 4.867 | 0.663 | 7.339 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.867 | 0.632 | 7.698 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.867 | 0.523 | 9.298 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `classic` | `strict_current` | 4.867 | 0.836 | 5.821 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `ax` | `profile_balanced` | 1.194 | 0.879 | 1.358 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `ax` | `profile_fast` | 1.194 | 0.770 | 1.550 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.194 | 0.627 | 1.904 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.194 | 0.655 | 1.824 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `ax` | `strict_current` | 1.194 | 0.942 | 1.267 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `classic` | `profile_balanced` | 4.876 | 0.879 | 5.546 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `classic` | `profile_fast` | 4.876 | 0.770 | 6.330 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.876 | 0.627 | 7.776 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.876 | 0.655 | 7.446 |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `classic` | `strict_current` | 4.876 | 0.942 | 5.174 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.188 | 1.261 | 0.942 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.188 | 0.934 | 1.272 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.188 | 0.759 | 1.565 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.188 | 0.752 | 1.579 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.188 | 4.813 | 0.247 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.450 | 1.261 | 3.530 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.450 | 0.934 | 4.765 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.450 | 0.759 | 5.865 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.450 | 0.752 | 5.915 |
| `vbr1_l1_differential_output_driver` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.450 | 4.813 | 0.925 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `ax` | `profile_balanced` | 1.281 | 1.374 | 0.932 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `ax` | `profile_fast` | 1.281 | 1.048 | 1.222 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.281 | 0.777 | 1.648 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.281 | 0.826 | 1.552 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `ax` | `strict_current` | 1.281 | 4.745 | 0.270 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `classic` | `profile_balanced` | 4.950 | 1.374 | 3.603 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `classic` | `profile_fast` | 4.950 | 1.048 | 4.723 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.950 | 0.777 | 6.369 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `classic` | `skip_source_error_control` | 4.950 | 0.826 | 5.996 |
| `vbr1_l1_differential_output_driver` | `dut` | `gold` | `classic` | `strict_current` | 4.950 | 4.745 | 1.043 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.397 | 1.249 | 1.119 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `ax` | `profile_fast` | 1.397 | 0.846 | 1.652 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.397 | 0.775 | 1.802 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.397 | 0.759 | 1.842 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `ax` | `strict_current` | 1.397 | 4.760 | 0.294 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.888 | 1.249 | 3.914 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `classic` | `profile_fast` | 4.888 | 0.846 | 5.778 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.888 | 0.775 | 6.303 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.888 | 0.759 | 6.441 |
| `vbr1_l1_differential_output_driver` | `e2e` | `gold` | `classic` | `strict_current` | 4.888 | 4.760 | 1.027 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `ax` | `profile_balanced` | 1.372 | 1.376 | 0.997 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `ax` | `profile_fast` | 1.372 | 0.929 | 1.477 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.372 | 0.770 | 1.781 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.372 | 0.898 | 1.527 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `ax` | `strict_current` | 1.372 | 4.873 | 0.281 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `classic` | `profile_balanced` | 5.128 | 1.376 | 3.726 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `classic` | `profile_fast` | 5.128 | 0.929 | 5.521 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.128 | 0.770 | 6.661 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `classic` | `skip_source_error_control` | 5.128 | 0.898 | 5.710 |
| `vbr1_l1_differential_output_driver` | `tb` | `gold` | `classic` | `strict_current` | 5.128 | 4.873 | 1.052 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.149 | 1.519 | 0.756 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.149 | 1.472 | 0.781 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.149 | 1.387 | 0.828 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.149 | 1.419 | 0.810 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.149 | 1.478 | 0.777 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.303 | 1.519 | 2.833 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.303 | 1.472 | 2.923 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.303 | 1.387 | 3.102 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.303 | 1.419 | 3.032 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.303 | 1.478 | 2.911 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `ax` | `profile_balanced` | 0.929 | 1.548 | 0.600 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `ax` | `profile_fast` | 0.929 | 1.584 | 0.586 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.929 | 1.253 | 0.741 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `ax` | `skip_source_error_control` | 0.929 | 1.360 | 0.683 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `ax` | `strict_current` | 0.929 | 1.571 | 0.591 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `classic` | `profile_balanced` | 4.206 | 1.548 | 2.716 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `classic` | `profile_fast` | 4.206 | 1.584 | 2.655 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.206 | 1.253 | 3.356 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `classic` | `skip_source_error_control` | 4.206 | 1.360 | 3.093 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `classic` | `strict_current` | 4.206 | 1.571 | 2.676 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `ax` | `profile_balanced` | 0.912 | 1.512 | 0.603 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `ax` | `profile_fast` | 0.912 | 1.459 | 0.625 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.912 | 1.307 | 0.698 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 0.912 | 1.437 | 0.635 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `ax` | `strict_current` | 0.912 | 1.596 | 0.572 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.374 | 1.512 | 2.892 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `classic` | `profile_fast` | 4.374 | 1.459 | 2.997 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.374 | 1.307 | 3.347 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.374 | 1.437 | 3.044 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `classic` | `strict_current` | 4.374 | 1.596 | 2.740 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `ax` | `profile_balanced` | 1.137 | 1.543 | 0.737 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `ax` | `profile_fast` | 1.137 | 1.552 | 0.732 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.137 | 1.284 | 0.885 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.137 | 1.311 | 0.867 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `ax` | `strict_current` | 1.137 | 1.688 | 0.674 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `classic` | `profile_balanced` | 4.396 | 1.543 | 2.848 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `classic` | `profile_fast` | 4.396 | 1.552 | 2.832 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.396 | 1.284 | 3.423 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.396 | 1.311 | 3.352 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `classic` | `strict_current` | 4.396 | 1.688 | 2.605 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `ax` | `profile_balanced` | 1.041 | 0.980 | 1.062 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `ax` | `profile_fast` | 1.041 | 0.662 | 1.572 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.041 | 0.646 | 1.611 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.041 | 0.633 | 1.644 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `ax` | `strict_current` | 1.041 | 1.000 | 1.041 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `classic` | `profile_balanced` | 2.488 | 0.980 | 2.539 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `classic` | `profile_fast` | 2.488 | 0.662 | 3.756 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.488 | 0.646 | 3.849 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `classic` | `skip_source_error_control` | 2.488 | 0.633 | 3.929 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `classic` | `strict_current` | 2.488 | 1.000 | 2.487 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.671 | 0.571 | 2.929 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `ax` | `profile_fast` | 1.671 | 0.549 | 3.046 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.671 | 0.608 | 2.749 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.671 | 0.652 | 2.562 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `ax` | `strict_current` | 1.671 | 0.521 | 3.206 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `classic` | `profile_balanced` | 3.837 | 0.571 | 6.724 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `classic` | `profile_fast` | 3.837 | 0.549 | 6.993 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.837 | 0.608 | 6.311 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 3.837 | 0.652 | 5.883 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `classic` | `strict_current` | 3.837 | 0.521 | 7.362 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `ax` | `profile_balanced` | 1.231 | 0.691 | 1.781 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `ax` | `profile_fast` | 1.231 | 0.722 | 1.704 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.231 | 0.667 | 1.846 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.231 | 0.754 | 1.632 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `ax` | `strict_current` | 1.231 | 0.810 | 1.520 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `classic` | `profile_balanced` | 3.010 | 0.691 | 4.357 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `classic` | `profile_fast` | 3.010 | 0.722 | 4.168 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.010 | 0.667 | 4.514 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `classic` | `skip_source_error_control` | 3.010 | 0.754 | 3.992 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `classic` | `strict_current` | 3.010 | 0.810 | 3.718 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.216 | 2.654 | 0.458 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.216 | 1.597 | 0.761 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.216 | 0.535 | 2.273 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.216 | 0.739 | 1.645 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.216 | 2.611 | 0.466 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 8.410 | 2.654 | 3.169 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `classic` | `profile_fast` | 8.410 | 1.597 | 5.265 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 8.410 | 0.535 | 15.727 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 8.410 | 0.739 | 11.379 |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `fixed` | `classic` | `strict_current` | 8.410 | 2.611 | 3.221 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `ax` | `profile_balanced` | 1.171 | 2.563 | 0.457 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `ax` | `profile_fast` | 1.171 | 1.563 | 0.750 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.171 | 0.576 | 2.032 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.171 | 0.657 | 1.784 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `ax` | `strict_current` | 1.171 | 2.470 | 0.474 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `classic` | `profile_balanced` | 8.274 | 2.563 | 3.229 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `classic` | `profile_fast` | 8.274 | 1.563 | 5.295 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 8.274 | 0.576 | 14.356 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `classic` | `skip_source_error_control` | 8.274 | 0.657 | 12.601 |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `classic` | `strict_current` | 8.274 | 2.470 | 3.350 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `ax` | `profile_balanced` | 0.810 | 2.526 | 0.321 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `ax` | `profile_fast` | 0.810 | 1.514 | 0.535 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.810 | 0.592 | 1.367 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 0.810 | 0.729 | 1.110 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `ax` | `strict_current` | 0.810 | 2.583 | 0.313 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `classic` | `profile_balanced` | 8.328 | 2.526 | 3.297 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `classic` | `profile_fast` | 8.328 | 1.514 | 5.500 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 8.328 | 0.592 | 14.060 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 8.328 | 0.729 | 11.419 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `classic` | `strict_current` | 8.328 | 2.583 | 3.224 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `ax` | `profile_balanced` | 1.048 | 2.493 | 0.420 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `ax` | `profile_fast` | 1.048 | 1.559 | 0.672 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.048 | 0.632 | 1.660 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.048 | 0.668 | 1.569 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `ax` | `strict_current` | 1.048 | 2.564 | 0.409 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `classic` | `profile_balanced` | 8.356 | 2.493 | 3.351 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `classic` | `profile_fast` | 8.356 | 1.559 | 5.358 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 8.356 | 0.632 | 13.230 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `classic` | `skip_source_error_control` | 8.356 | 0.668 | 12.505 |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `classic` | `strict_current` | 8.356 | 2.564 | 3.259 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 3.598 | 0.934 | 3.852 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `ax` | `profile_fast` | 3.598 | 0.674 | 5.336 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 3.598 | 0.696 | 5.166 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 3.598 | 0.696 | 5.168 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 3.598 | 0.944 | 3.812 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 5.065 | 0.934 | 5.423 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `classic` | `profile_fast` | 5.065 | 0.674 | 7.512 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 5.065 | 0.696 | 7.273 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 5.065 | 0.696 | 7.277 |
| `vbr1_l1_edge_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 5.065 | 0.944 | 5.367 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `ax` | `profile_balanced` | 4.267 | 0.794 | 5.376 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `ax` | `profile_fast` | 4.267 | 0.823 | 5.186 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 4.267 | 0.662 | 6.445 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `ax` | `skip_source_error_control` | 4.267 | 0.715 | 5.965 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `ax` | `strict_current` | 4.267 | 0.839 | 5.088 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `classic` | `profile_balanced` | 5.375 | 0.794 | 6.771 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `classic` | `profile_fast` | 5.375 | 0.823 | 6.533 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.375 | 0.662 | 8.119 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `classic` | `skip_source_error_control` | 5.375 | 0.715 | 7.513 |
| `vbr1_l1_edge_detector` | `dut` | `gold` | `classic` | `strict_current` | 5.375 | 0.839 | 6.409 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.480 | 0.678 | 2.182 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `ax` | `profile_fast` | 1.480 | 0.572 | 2.587 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.480 | 0.624 | 2.370 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.480 | 0.840 | 1.761 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `ax` | `strict_current` | 1.480 | 0.742 | 1.995 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `classic` | `profile_balanced` | 5.434 | 0.678 | 8.012 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `classic` | `profile_fast` | 5.434 | 0.572 | 9.498 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.434 | 0.624 | 8.703 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 5.434 | 0.840 | 6.466 |
| `vbr1_l1_edge_detector` | `e2e` | `gold` | `classic` | `strict_current` | 5.434 | 0.742 | 7.326 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `ax` | `profile_balanced` | 3.851 | 0.942 | 4.087 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `ax` | `profile_fast` | 3.851 | 0.715 | 5.385 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 3.851 | 0.656 | 5.871 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `ax` | `skip_source_error_control` | 3.851 | 0.759 | 5.075 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `ax` | `strict_current` | 3.851 | 1.000 | 3.851 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `classic` | `profile_balanced` | 5.515 | 0.942 | 5.853 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `classic` | `profile_fast` | 5.515 | 0.715 | 7.713 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.515 | 0.656 | 8.408 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `classic` | `skip_source_error_control` | 5.515 | 0.759 | 7.269 |
| `vbr1_l1_edge_detector` | `tb` | `gold` | `classic` | `strict_current` | 5.515 | 1.000 | 5.516 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `ax` | `profile_balanced` | 0.870 | 1.426 | 0.610 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `ax` | `profile_fast` | 0.870 | 1.110 | 0.784 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.870 | 1.027 | 0.847 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 0.870 | 1.169 | 0.744 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `ax` | `strict_current` | 0.870 | 4.645 | 0.187 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `classic` | `profile_balanced` | 3.761 | 1.426 | 2.637 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `classic` | `profile_fast` | 3.761 | 1.110 | 3.389 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.761 | 1.027 | 3.662 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 3.761 | 1.169 | 3.218 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `classic` | `strict_current` | 3.761 | 4.645 | 0.810 |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `ax` | `profile_balanced` | 0.723 | 1.375 | 0.526 |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `ax` | `profile_fast` | 0.723 | 1.098 | 0.658 |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.723 | 1.016 | 0.711 |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `ax` | `skip_source_error_control` | 0.723 | 0.963 | 0.750 |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `ax` | `strict_current` | 0.723 | 4.572 | 0.158 |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `classic` | `profile_balanced` | 3.377 | 1.375 | 2.456 |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `classic` | `profile_fast` | 3.377 | 1.098 | 3.076 |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.377 | 1.016 | 3.324 |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `classic` | `skip_source_error_control` | 3.377 | 0.963 | 3.507 |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `classic` | `strict_current` | 3.377 | 4.572 | 0.739 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.176 | 0.867 | 1.357 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.176 | 0.825 | 1.426 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.176 | 0.746 | 1.577 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.176 | 0.803 | 1.465 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.176 | 0.892 | 1.319 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.681 | 0.867 | 5.402 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.681 | 0.825 | 5.675 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.681 | 0.746 | 6.275 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.681 | 0.803 | 5.830 |
| `vbr1_l1_element_shuffler` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.681 | 0.892 | 5.249 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `ax` | `profile_balanced` | 1.163 | 0.736 | 1.581 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `ax` | `profile_fast` | 1.163 | 0.582 | 1.997 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.163 | 0.651 | 1.787 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.163 | 0.605 | 1.922 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `ax` | `strict_current` | 1.163 | 0.763 | 1.523 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `classic` | `profile_balanced` | 4.864 | 0.736 | 6.611 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `classic` | `profile_fast` | 4.864 | 0.582 | 8.351 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.864 | 0.651 | 7.473 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `classic` | `skip_source_error_control` | 4.864 | 0.605 | 8.038 |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `classic` | `strict_current` | 4.864 | 0.763 | 6.372 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `ax` | `profile_balanced` | 0.974 | 0.806 | 1.208 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `ax` | `profile_fast` | 0.974 | 0.784 | 1.243 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.974 | 0.781 | 1.247 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 0.974 | 0.762 | 1.278 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `ax` | `strict_current` | 0.974 | 0.821 | 1.186 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.627 | 0.806 | 5.738 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `classic` | `profile_fast` | 4.627 | 0.784 | 5.905 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.627 | 0.781 | 5.922 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.627 | 0.762 | 6.072 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `classic` | `strict_current` | 4.627 | 0.821 | 5.634 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `ax` | `profile_balanced` | 1.044 | 0.679 | 1.538 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `ax` | `profile_fast` | 1.044 | 0.642 | 1.626 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.044 | 0.633 | 1.650 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.044 | 0.629 | 1.660 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `ax` | `strict_current` | 1.044 | 0.822 | 1.270 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `classic` | `profile_balanced` | 4.801 | 0.679 | 7.073 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `classic` | `profile_fast` | 4.801 | 0.642 | 7.481 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.801 | 0.633 | 7.588 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.801 | 0.629 | 7.638 |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `classic` | `strict_current` | 4.801 | 0.822 | 5.840 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.089 | 0.903 | 1.205 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.089 | 0.780 | 1.396 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.089 | 0.614 | 1.773 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.089 | 0.614 | 1.772 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.089 | 1.008 | 1.080 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.697 | 0.903 | 5.201 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.697 | 0.780 | 6.023 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.697 | 0.614 | 7.652 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.697 | 0.614 | 7.647 |
| `vbr1_l1_event_pulse_stretcher` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.697 | 1.008 | 4.661 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `ax` | `profile_balanced` | 0.946 | 0.684 | 1.382 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `ax` | `profile_fast` | 0.946 | 0.711 | 1.330 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.946 | 0.651 | 1.451 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `ax` | `skip_source_error_control` | 0.946 | 0.636 | 1.486 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `ax` | `strict_current` | 0.946 | 0.777 | 1.216 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `classic` | `profile_balanced` | 4.769 | 0.684 | 6.972 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `classic` | `profile_fast` | 4.769 | 0.711 | 6.708 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.769 | 0.651 | 7.320 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `classic` | `skip_source_error_control` | 4.769 | 0.636 | 7.496 |
| `vbr1_l1_event_pulse_stretcher` | `dut` | `gold` | `classic` | `strict_current` | 4.769 | 0.777 | 6.134 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.646 | 0.733 | 2.244 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `ax` | `profile_fast` | 1.646 | 0.681 | 2.415 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.646 | 0.565 | 2.912 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.646 | 0.645 | 2.551 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `ax` | `strict_current` | 1.646 | 0.756 | 2.176 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `classic` | `profile_balanced` | 5.230 | 0.733 | 7.134 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `classic` | `profile_fast` | 5.230 | 0.681 | 7.675 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.230 | 0.565 | 9.257 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 5.230 | 0.645 | 8.110 |
| `vbr1_l1_event_pulse_stretcher` | `e2e` | `gold` | `classic` | `strict_current` | 5.230 | 0.756 | 6.916 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `ax` | `profile_balanced` | 1.040 | 0.816 | 1.276 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `ax` | `profile_fast` | 1.040 | 0.658 | 1.581 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.040 | 0.564 | 1.845 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.040 | 0.607 | 1.714 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `ax` | `strict_current` | 1.040 | 0.981 | 1.060 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `classic` | `profile_balanced` | 4.595 | 0.816 | 5.635 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `classic` | `profile_fast` | 4.595 | 0.658 | 6.983 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.595 | 0.564 | 8.151 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.595 | 0.607 | 7.570 |
| `vbr1_l1_event_pulse_stretcher` | `tb` | `gold` | `classic` | `strict_current` | 4.595 | 0.981 | 4.683 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 2.925 | 0.972 | 3.009 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `ax` | `profile_fast` | 2.925 | 0.988 | 2.960 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 2.925 | 0.957 | 3.056 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 2.925 | 0.946 | 3.092 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `ax` | `strict_current` | 2.925 | 1.077 | 2.717 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 2.837 | 0.972 | 2.918 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `classic` | `profile_fast` | 2.837 | 0.988 | 2.871 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 2.837 | 0.957 | 2.964 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 2.837 | 0.946 | 2.999 |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `fixed` | `classic` | `strict_current` | 2.837 | 1.077 | 2.635 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `ax` | `profile_balanced` | 0.913 | 0.859 | 1.063 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `ax` | `profile_fast` | 0.913 | 0.919 | 0.993 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.913 | 0.772 | 1.183 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `ax` | `skip_source_error_control` | 0.913 | 0.821 | 1.113 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `ax` | `strict_current` | 0.913 | 0.837 | 1.091 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `classic` | `profile_balanced` | 2.277 | 0.859 | 2.649 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `classic` | `profile_fast` | 2.277 | 0.919 | 2.476 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.277 | 0.772 | 2.949 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `classic` | `skip_source_error_control` | 2.277 | 0.821 | 2.774 |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `classic` | `strict_current` | 2.277 | 0.837 | 2.719 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `ax` | `profile_balanced` | 3.089 | 0.952 | 3.246 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `ax` | `profile_fast` | 3.089 | 0.893 | 3.460 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 3.089 | 0.812 | 3.803 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 3.089 | 0.893 | 3.460 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `ax` | `strict_current` | 3.089 | 0.796 | 3.879 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `classic` | `profile_balanced` | 2.789 | 0.952 | 2.931 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `classic` | `profile_fast` | 2.789 | 0.893 | 3.124 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.789 | 0.812 | 3.434 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 2.789 | 0.893 | 3.124 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `classic` | `strict_current` | 2.789 | 0.796 | 3.502 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `ax` | `profile_balanced` | 0.914 | 0.902 | 1.013 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `ax` | `profile_fast` | 0.914 | 0.890 | 1.026 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.914 | 0.740 | 1.235 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `ax` | `skip_source_error_control` | 0.914 | 0.890 | 1.027 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `ax` | `strict_current` | 0.914 | 1.004 | 0.910 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `classic` | `profile_balanced` | 2.345 | 0.902 | 2.600 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `classic` | `profile_fast` | 2.345 | 0.890 | 2.634 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.345 | 0.740 | 3.168 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `classic` | `skip_source_error_control` | 2.345 | 0.890 | 2.636 |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `classic` | `strict_current` | 2.345 | 1.004 | 2.336 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `ax` | `profile_balanced` | 5.736 | 126.899 | 0.045 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `ax` | `profile_fast` | 5.736 | 107.294 | 0.053 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.736 | 11.311 | 0.507 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 5.736 | 11.323 | 0.507 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `ax` | `strict_current` | 5.736 | 128.977 | 0.044 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `classic` | `profile_balanced` | 13.116 | 126.899 | 0.103 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `classic` | `profile_fast` | 13.116 | 107.294 | 0.122 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 13.116 | 11.311 | 1.160 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 13.116 | 11.323 | 1.158 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `classic` | `strict_current` | 13.116 | 128.977 | 0.102 |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `ax` | `profile_balanced` | 4.784 | 151.214 | 0.032 |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `ax` | `profile_fast` | 4.784 | 132.261 | 0.036 |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 4.784 | 32.723 | 0.146 |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `ax` | `skip_source_error_control` | 4.784 | 34.644 | 0.138 |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `ax` | `strict_current` | 4.784 | 154.555 | 0.031 |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `classic` | `profile_balanced` | 11.678 | 151.214 | 0.077 |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `classic` | `profile_fast` | 11.678 | 132.261 | 0.088 |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 11.678 | 32.723 | 0.357 |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `classic` | `skip_source_error_control` | 11.678 | 34.644 | 0.337 |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `classic` | `strict_current` | 11.678 | 154.555 | 0.076 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 2.402 | 1.528 | 1.572 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `ax` | `profile_fast` | 2.402 | 1.062 | 2.262 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 2.402 | 0.874 | 2.749 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 2.402 | 0.868 | 2.769 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `ax` | `strict_current` | 2.402 | 1.514 | 1.586 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 2.365 | 1.528 | 1.547 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `classic` | `profile_fast` | 2.365 | 1.062 | 2.226 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 2.365 | 0.874 | 2.707 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 2.365 | 0.868 | 2.726 |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `fixed` | `classic` | `strict_current` | 2.365 | 1.514 | 1.562 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `ax` | `profile_balanced` | 2.595 | 1.386 | 1.872 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `ax` | `profile_fast` | 2.595 | 0.959 | 2.705 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 2.595 | 0.947 | 2.740 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `ax` | `skip_source_error_control` | 2.595 | 0.811 | 3.200 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `ax` | `strict_current` | 2.595 | 1.453 | 1.786 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `classic` | `profile_balanced` | 2.565 | 1.386 | 1.850 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `classic` | `profile_fast` | 2.565 | 0.959 | 2.674 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.565 | 0.947 | 2.709 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `classic` | `skip_source_error_control` | 2.565 | 0.811 | 3.163 |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `classic` | `strict_current` | 2.565 | 1.453 | 1.766 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.493 | 1.410 | 1.058 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `ax` | `profile_fast` | 1.493 | 1.109 | 1.346 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.493 | 0.902 | 1.655 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.493 | 0.913 | 1.636 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `ax` | `strict_current` | 1.493 | 1.497 | 0.997 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `classic` | `profile_balanced` | 2.919 | 1.410 | 2.069 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `classic` | `profile_fast` | 2.919 | 1.109 | 2.632 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.919 | 0.902 | 3.237 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 2.919 | 0.913 | 3.198 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `classic` | `strict_current` | 2.919 | 1.497 | 1.950 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `ax` | `profile_balanced` | 0.913 | 1.450 | 0.630 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `ax` | `profile_fast` | 0.913 | 0.993 | 0.919 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.913 | 0.891 | 1.025 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `ax` | `skip_source_error_control` | 0.913 | 0.890 | 1.026 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `ax` | `strict_current` | 0.913 | 1.538 | 0.594 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `classic` | `profile_balanced` | 2.527 | 1.450 | 1.744 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `classic` | `profile_fast` | 2.527 | 0.993 | 2.545 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.527 | 0.891 | 2.838 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `classic` | `skip_source_error_control` | 2.527 | 0.890 | 2.840 |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `classic` | `strict_current` | 2.527 | 1.538 | 1.643 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.304 | 1.192 | 1.094 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.304 | 0.873 | 1.494 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.304 | 0.597 | 2.185 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.304 | 0.610 | 2.137 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.304 | 1.366 | 0.954 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.770 | 1.192 | 4.001 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.770 | 0.873 | 5.465 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.770 | 0.597 | 7.995 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.770 | 0.610 | 7.817 |
| `vbr1_l1_higher_order_filter` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.770 | 1.366 | 3.492 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `ax` | `profile_balanced` | 1.091 | 1.284 | 0.849 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `ax` | `profile_fast` | 1.091 | 0.957 | 1.140 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.091 | 0.624 | 1.749 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.091 | 0.715 | 1.526 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `ax` | `strict_current` | 1.091 | 1.319 | 0.827 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `classic` | `profile_balanced` | 5.418 | 1.284 | 4.218 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `classic` | `profile_fast` | 5.418 | 0.957 | 5.660 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.418 | 0.624 | 8.683 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `classic` | `skip_source_error_control` | 5.418 | 0.715 | 7.579 |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `classic` | `strict_current` | 5.418 | 1.319 | 4.108 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.087 | 1.119 | 0.971 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `ax` | `profile_fast` | 1.087 | 0.814 | 1.335 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.087 | 0.669 | 1.625 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.087 | 0.635 | 1.711 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `ax` | `strict_current` | 1.087 | 1.260 | 0.863 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `classic` | `profile_balanced` | 5.069 | 1.119 | 4.529 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `classic` | `profile_fast` | 5.069 | 0.814 | 6.226 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.069 | 0.669 | 7.579 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 5.069 | 0.635 | 7.981 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `classic` | `strict_current` | 5.069 | 1.260 | 4.024 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `ax` | `profile_balanced` | 0.969 | 1.357 | 0.714 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `ax` | `profile_fast` | 0.969 | 0.895 | 1.083 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.969 | 0.594 | 1.633 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `ax` | `skip_source_error_control` | 0.969 | 0.659 | 1.471 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `ax` | `strict_current` | 0.969 | 1.399 | 0.693 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `classic` | `profile_balanced` | 4.158 | 1.357 | 3.064 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `classic` | `profile_fast` | 4.158 | 0.895 | 4.649 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.158 | 0.594 | 7.005 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.158 | 0.659 | 6.311 |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `classic` | `strict_current` | 4.158 | 1.399 | 2.972 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.107 | 0.910 | 1.216 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.107 | 0.794 | 1.395 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.107 | 0.852 | 1.299 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.107 | 0.747 | 1.482 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.107 | 1.143 | 0.969 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.738 | 0.910 | 5.205 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.738 | 0.794 | 5.968 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.738 | 0.852 | 5.560 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.738 | 0.747 | 6.341 |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.738 | 1.143 | 4.145 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `ax` | `profile_balanced` | 1.458 | 0.822 | 1.775 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `ax` | `profile_fast` | 1.458 | 0.901 | 1.618 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.458 | 0.967 | 1.507 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.458 | 0.990 | 1.473 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `ax` | `strict_current` | 1.458 | 0.874 | 1.668 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `classic` | `profile_balanced` | 5.006 | 0.822 | 6.093 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `classic` | `profile_fast` | 5.006 | 0.901 | 5.554 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.006 | 0.967 | 5.175 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `classic` | `skip_source_error_control` | 5.006 | 0.990 | 5.057 |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `classic` | `strict_current` | 5.006 | 0.874 | 5.726 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.113 | 0.824 | 1.352 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `ax` | `profile_fast` | 1.113 | 0.815 | 1.366 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.113 | 0.847 | 1.313 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.113 | 0.883 | 1.261 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 1.113 | 0.891 | 1.249 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `classic` | `profile_balanced` | 5.325 | 0.824 | 6.466 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `classic` | `profile_fast` | 5.325 | 0.815 | 6.534 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.325 | 0.847 | 6.284 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 5.325 | 0.883 | 6.031 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 5.325 | 0.891 | 5.975 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `ax` | `profile_balanced` | 1.098 | 0.860 | 1.276 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `ax` | `profile_fast` | 1.098 | 0.802 | 1.369 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.098 | 0.688 | 1.597 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.098 | 0.803 | 1.367 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `ax` | `strict_current` | 1.098 | 1.003 | 1.095 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `classic` | `profile_balanced` | 4.896 | 0.860 | 5.690 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `classic` | `profile_fast` | 4.896 | 0.802 | 6.107 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.896 | 0.688 | 7.121 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.896 | 0.803 | 6.096 |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `classic` | `strict_current` | 4.896 | 1.003 | 4.883 |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 0.843 | 4.787 | 0.176 |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `ax` | `profile_fast` | 0.843 | 2.250 | 0.375 |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 0.843 | 1.642 | 0.513 |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 0.843 | 1.663 | 0.507 |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `ax` | `strict_current` | 0.843 | 4.556 | 0.185 |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.209 | 4.787 | 0.879 |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.209 | 2.250 | 1.871 |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.209 | 1.642 | 2.563 |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.209 | 1.663 | 2.531 |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.209 | 4.556 | 0.924 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `ax` | `profile_balanced` | 1.056 | 4.568 | 0.231 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `ax` | `profile_fast` | 1.056 | 2.153 | 0.491 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.056 | 1.470 | 0.719 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.056 | 1.507 | 0.701 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `ax` | `strict_current` | 1.056 | 4.619 | 0.229 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `classic` | `profile_balanced` | 4.077 | 4.568 | 0.893 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `classic` | `profile_fast` | 4.077 | 2.153 | 1.894 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.077 | 1.470 | 2.774 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `classic` | `skip_source_error_control` | 4.077 | 1.507 | 2.706 |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `classic` | `strict_current` | 4.077 | 4.619 | 0.883 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.350 | 2.679 | 0.504 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `ax` | `profile_fast` | 1.350 | 2.712 | 0.498 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.350 | 1.388 | 0.973 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.350 | 1.390 | 0.972 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `ax` | `strict_current` | 1.350 | 2.709 | 0.498 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `classic` | `profile_balanced` | 3.884 | 2.679 | 1.450 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `classic` | `profile_fast` | 3.884 | 2.712 | 1.432 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.884 | 1.388 | 2.797 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 3.884 | 1.390 | 2.794 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `classic` | `strict_current` | 3.884 | 2.709 | 1.434 |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `ax` | `profile_balanced` | 0.859 | 2.743 | 0.313 |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `ax` | `profile_fast` | 0.859 | 2.654 | 0.324 |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.859 | 1.359 | 0.632 |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `ax` | `skip_source_error_control` | 0.859 | 1.655 | 0.519 |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `ax` | `strict_current` | 0.859 | 2.719 | 0.316 |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `classic` | `profile_balanced` | 3.887 | 2.743 | 1.417 |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `classic` | `profile_fast` | 3.887 | 2.654 | 1.464 |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.887 | 1.359 | 2.860 |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `classic` | `skip_source_error_control` | 3.887 | 1.655 | 2.348 |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `classic` | `strict_current` | 3.887 | 2.719 | 1.429 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 3.094 | 0.875 | 3.536 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `ax` | `profile_fast` | 3.094 | 0.708 | 4.371 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 3.094 | 0.862 | 3.590 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 3.094 | 0.669 | 4.621 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 3.094 | 0.870 | 3.557 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.349 | 0.875 | 4.971 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.349 | 0.708 | 6.145 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.349 | 0.862 | 5.047 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.349 | 0.669 | 6.497 |
| `vbr1_l1_lock_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.349 | 0.870 | 5.000 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `ax` | `profile_balanced` | 1.283 | 0.835 | 1.536 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `ax` | `profile_fast` | 1.283 | 0.803 | 1.598 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.283 | 0.665 | 1.930 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.283 | 0.773 | 1.660 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `ax` | `strict_current` | 1.283 | 0.877 | 1.463 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `classic` | `profile_balanced` | 5.012 | 0.835 | 6.000 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `classic` | `profile_fast` | 5.012 | 0.803 | 6.242 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.012 | 0.665 | 7.539 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `classic` | `skip_source_error_control` | 5.012 | 0.773 | 6.485 |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `classic` | `strict_current` | 5.012 | 0.877 | 5.715 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `ax` | `profile_balanced` | 3.476 | 0.884 | 3.932 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `ax` | `profile_fast` | 3.476 | 0.677 | 5.132 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 3.476 | 0.625 | 5.562 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 3.476 | 0.629 | 5.522 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `ax` | `strict_current` | 3.476 | 0.766 | 4.537 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.940 | 0.884 | 5.587 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `classic` | `profile_fast` | 4.940 | 0.677 | 7.294 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.940 | 0.625 | 7.905 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.940 | 0.629 | 7.847 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `classic` | `strict_current` | 4.940 | 0.766 | 6.448 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `ax` | `profile_balanced` | 1.261 | 0.867 | 1.454 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `ax` | `profile_fast` | 1.261 | 0.812 | 1.553 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.261 | 0.788 | 1.601 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.261 | 0.819 | 1.540 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `ax` | `strict_current` | 1.261 | 0.879 | 1.434 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `classic` | `profile_balanced` | 5.110 | 0.867 | 5.891 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `classic` | `profile_fast` | 5.110 | 0.812 | 6.295 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.110 | 0.788 | 6.488 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `classic` | `skip_source_error_control` | 5.110 | 0.819 | 6.239 |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `classic` | `strict_current` | 5.110 | 0.879 | 5.810 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 0.835 | 1.514 | 0.552 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `ax` | `profile_fast` | 0.835 | 1.014 | 0.824 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 0.835 | 0.580 | 1.440 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 0.835 | 0.588 | 1.420 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `ax` | `strict_current` | 0.835 | 1.541 | 0.542 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.250 | 1.514 | 2.807 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.250 | 1.014 | 4.193 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.250 | 0.580 | 7.326 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.250 | 0.588 | 7.223 |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.250 | 1.541 | 2.758 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `ax` | `profile_balanced` | 0.910 | 1.351 | 0.674 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `ax` | `profile_fast` | 0.910 | 0.972 | 0.937 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.910 | 0.560 | 1.625 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `ax` | `skip_source_error_control` | 0.910 | 0.573 | 1.589 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `ax` | `strict_current` | 0.910 | 1.389 | 0.655 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `classic` | `profile_balanced` | 5.051 | 1.351 | 3.739 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `classic` | `profile_fast` | 5.051 | 0.972 | 5.199 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.051 | 0.560 | 9.023 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `classic` | `skip_source_error_control` | 5.051 | 0.573 | 8.820 |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `classic` | `strict_current` | 5.051 | 1.389 | 3.635 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.184 | 1.499 | 0.790 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `ax` | `profile_fast` | 1.184 | 0.927 | 1.277 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.184 | 0.763 | 1.551 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.184 | 0.685 | 1.729 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `ax` | `strict_current` | 1.184 | 1.537 | 0.771 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.635 | 1.499 | 3.091 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `classic` | `profile_fast` | 4.635 | 0.927 | 4.998 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.635 | 0.763 | 6.071 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.635 | 0.685 | 6.769 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `classic` | `strict_current` | 4.635 | 1.537 | 3.016 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `ax` | `profile_balanced` | 0.883 | 1.615 | 0.547 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `ax` | `profile_fast` | 0.883 | 1.052 | 0.839 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.883 | 0.543 | 1.626 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `ax` | `skip_source_error_control` | 0.883 | 0.634 | 1.392 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `ax` | `strict_current` | 0.883 | 1.570 | 0.562 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `classic` | `profile_balanced` | 4.803 | 1.615 | 2.974 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `classic` | `profile_fast` | 4.803 | 1.052 | 4.565 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.803 | 0.543 | 8.846 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.803 | 0.634 | 7.576 |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `classic` | `strict_current` | 4.803 | 1.570 | 3.059 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 3.436 | 0.943 | 3.644 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast` | 3.436 | 1.066 | 3.222 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 3.436 | 0.891 | 3.854 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 3.436 | 0.985 | 3.489 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 3.436 | 1.012 | 3.396 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 3.295 | 0.943 | 3.494 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast` | 3.295 | 1.066 | 3.090 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 3.295 | 0.891 | 3.696 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 3.295 | 0.985 | 3.346 |
| `vbr1_l1_offset_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 3.295 | 1.012 | 3.257 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `ax` | `profile_balanced` | 2.599 | 1.021 | 2.546 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `ax` | `profile_fast` | 2.599 | 0.968 | 2.686 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 2.599 | 0.876 | 2.966 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `ax` | `skip_source_error_control` | 2.599 | 0.828 | 3.140 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `ax` | `strict_current` | 2.599 | 1.117 | 2.326 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `classic` | `profile_balanced` | 2.592 | 1.021 | 2.540 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `classic` | `profile_fast` | 2.592 | 0.968 | 2.679 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.592 | 0.876 | 2.959 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `classic` | `skip_source_error_control` | 2.592 | 0.828 | 3.132 |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `classic` | `strict_current` | 2.592 | 1.117 | 2.320 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `ax` | `profile_balanced` | 0.869 | 1.206 | 0.721 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `ax` | `profile_fast` | 0.869 | 1.152 | 0.755 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.869 | 0.974 | 0.892 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 0.869 | 0.993 | 0.875 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 0.869 | 1.387 | 0.627 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `classic` | `profile_balanced` | 2.812 | 1.206 | 2.331 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `classic` | `profile_fast` | 2.812 | 1.152 | 2.441 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.812 | 0.974 | 2.887 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 2.812 | 0.993 | 2.830 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 2.812 | 1.387 | 2.027 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `ax` | `profile_balanced` | 1.399 | 0.990 | 1.413 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `ax` | `profile_fast` | 1.399 | 1.069 | 1.309 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.399 | 0.963 | 1.453 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.399 | 0.946 | 1.478 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `ax` | `strict_current` | 1.399 | 1.079 | 1.297 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `classic` | `profile_balanced` | 3.213 | 0.990 | 3.244 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `classic` | `profile_fast` | 3.213 | 1.069 | 3.006 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.213 | 0.963 | 3.337 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `classic` | `skip_source_error_control` | 3.213 | 0.946 | 3.395 |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `classic` | `strict_current` | 3.213 | 1.079 | 2.978 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.357 | 0.868 | 1.564 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.357 | 0.771 | 1.761 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.357 | 0.738 | 1.839 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.357 | 0.678 | 2.002 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.357 | 0.911 | 1.490 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.887 | 0.868 | 5.632 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.887 | 0.771 | 6.341 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.887 | 0.738 | 6.624 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.887 | 0.678 | 7.211 |
| `vbr1_l1_one_shot_timer` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.887 | 0.911 | 5.365 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `ax` | `profile_balanced` | 1.457 | 0.718 | 2.030 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `ax` | `profile_fast` | 1.457 | 0.632 | 2.306 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.457 | 0.788 | 1.849 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.457 | 0.606 | 2.404 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `ax` | `strict_current` | 1.457 | 0.842 | 1.731 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `classic` | `profile_balanced` | 5.920 | 0.718 | 8.250 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `classic` | `profile_fast` | 5.920 | 0.632 | 9.373 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.920 | 0.788 | 7.512 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `classic` | `skip_source_error_control` | 5.920 | 0.606 | 9.769 |
| `vbr1_l1_one_shot_timer` | `dut` | `gold` | `classic` | `strict_current` | 5.920 | 0.842 | 7.033 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.447 | 0.845 | 1.712 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `ax` | `profile_fast` | 1.447 | 0.750 | 1.930 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.447 | 0.712 | 2.033 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.447 | 0.704 | 2.056 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `ax` | `strict_current` | 1.447 | 0.809 | 1.788 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `classic` | `profile_balanced` | 5.382 | 0.845 | 6.368 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `classic` | `profile_fast` | 5.382 | 0.750 | 7.180 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.382 | 0.712 | 7.563 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 5.382 | 0.704 | 7.648 |
| `vbr1_l1_one_shot_timer` | `e2e` | `gold` | `classic` | `strict_current` | 5.382 | 0.809 | 6.653 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `ax` | `profile_balanced` | 0.888 | 0.731 | 1.214 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `ax` | `profile_fast` | 0.888 | 0.683 | 1.300 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.888 | 0.648 | 1.369 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `ax` | `skip_source_error_control` | 0.888 | 0.569 | 1.559 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `ax` | `strict_current` | 0.888 | 0.917 | 0.968 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `classic` | `profile_balanced` | 4.393 | 0.731 | 6.006 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `classic` | `profile_fast` | 4.393 | 0.683 | 6.431 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.393 | 0.648 | 6.775 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.393 | 0.569 | 7.715 |
| `vbr1_l1_one_shot_timer` | `tb` | `gold` | `classic` | `strict_current` | 4.393 | 0.917 | 4.791 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 0.893 | 0.777 | 1.150 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `ax` | `profile_fast` | 0.893 | 0.642 | 1.390 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 0.893 | 0.701 | 1.273 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 0.893 | 0.646 | 1.383 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 0.893 | 0.771 | 1.158 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 2.721 | 0.777 | 3.504 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `classic` | `profile_fast` | 2.721 | 0.642 | 4.237 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 2.721 | 0.701 | 3.880 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 2.721 | 0.646 | 4.215 |
| `vbr1_l1_peak_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 2.721 | 0.771 | 3.531 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `ax` | `profile_balanced` | 0.952 | 0.852 | 1.118 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `ax` | `profile_fast` | 0.952 | 0.671 | 1.420 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.952 | 0.649 | 1.466 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `ax` | `skip_source_error_control` | 0.952 | 0.651 | 1.462 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `ax` | `strict_current` | 0.952 | 0.865 | 1.101 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `classic` | `profile_balanced` | 2.735 | 0.852 | 3.212 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `classic` | `profile_fast` | 2.735 | 0.671 | 4.079 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.735 | 0.649 | 4.212 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `classic` | `skip_source_error_control` | 2.735 | 0.651 | 4.200 |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `classic` | `strict_current` | 2.735 | 0.865 | 3.161 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `ax` | `profile_balanced` | 1.153 | 0.806 | 1.431 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `ax` | `profile_fast` | 1.153 | 0.729 | 1.583 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.153 | 0.675 | 1.708 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.153 | 0.641 | 1.799 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `ax` | `strict_current` | 1.153 | 0.905 | 1.274 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `classic` | `profile_balanced` | 2.946 | 0.806 | 3.656 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `classic` | `profile_fast` | 2.946 | 0.729 | 4.044 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.946 | 0.675 | 4.364 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `classic` | `skip_source_error_control` | 2.946 | 0.641 | 4.596 |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `classic` | `strict_current` | 2.946 | 0.905 | 3.254 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 0.907 | 21.950 | 0.041 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `ax` | `profile_fast` | 0.907 | 17.204 | 0.053 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 0.907 | 15.787 | 0.057 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 0.907 | 24.569 | 0.037 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `ax` | `strict_current` | 0.907 | 32.764 | 0.028 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 3.988 | 21.950 | 0.182 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `classic` | `profile_fast` | 3.988 | 17.204 | 0.232 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 3.988 | 15.787 | 0.253 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 3.988 | 24.569 | 0.162 |
| `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `fixed` | `classic` | `strict_current` | 3.988 | 32.764 | 0.122 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `ax` | `profile_balanced` | 0.605 | 22.400 | 0.027 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `ax` | `profile_fast` | 0.605 | 17.252 | 0.035 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.605 | 15.603 | 0.039 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `ax` | `skip_source_error_control` | 0.605 | 23.802 | 0.025 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `ax` | `strict_current` | 0.605 | 33.563 | 0.018 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `classic` | `profile_balanced` | 3.941 | 22.400 | 0.176 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `classic` | `profile_fast` | 3.941 | 17.252 | 0.228 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.941 | 15.603 | 0.253 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `classic` | `skip_source_error_control` | 3.941 | 23.802 | 0.166 |
| `vbr1_l1_pfd_small_phase_error_response` | `dut` | `gold` | `classic` | `strict_current` | 3.941 | 33.563 | 0.117 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `ax` | `profile_balanced` | 0.767 | 21.916 | 0.035 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `ax` | `profile_fast` | 0.767 | 17.373 | 0.044 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.767 | 15.749 | 0.049 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 0.767 | 24.088 | 0.032 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `ax` | `strict_current` | 0.767 | 33.284 | 0.023 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.019 | 21.916 | 0.183 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `classic` | `profile_fast` | 4.019 | 17.373 | 0.231 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.019 | 15.749 | 0.255 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.019 | 24.088 | 0.167 |
| `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `gold` | `classic` | `strict_current` | 4.019 | 33.284 | 0.121 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `ax` | `profile_balanced` | 0.801 | 21.908 | 0.037 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `ax` | `profile_fast` | 0.801 | 17.081 | 0.047 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.801 | 15.871 | 0.050 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `ax` | `skip_source_error_control` | 0.801 | 23.451 | 0.034 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `ax` | `strict_current` | 0.801 | 32.865 | 0.024 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `classic` | `profile_balanced` | 4.106 | 21.908 | 0.187 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `classic` | `profile_fast` | 4.106 | 17.081 | 0.240 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.106 | 15.871 | 0.259 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.106 | 23.451 | 0.175 |
| `vbr1_l1_pfd_small_phase_error_response` | `tb` | `gold` | `classic` | `strict_current` | 4.106 | 32.865 | 0.125 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 2.618 | 21.786 | 0.120 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `ax` | `profile_fast` | 2.618 | 10.967 | 0.239 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 2.618 | 8.191 | 0.320 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 2.618 | 12.189 | 0.215 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `ax` | `strict_current` | 2.618 | 66.053 | 0.040 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.102 | 21.786 | 0.188 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.102 | 10.967 | 0.374 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.102 | 8.191 | 0.501 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.102 | 12.189 | 0.337 |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.102 | 66.053 | 0.062 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `ax` | `profile_balanced` | 0.851 | 22.339 | 0.038 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `ax` | `profile_fast` | 0.851 | 11.369 | 0.075 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.851 | 8.340 | 0.102 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `ax` | `skip_source_error_control` | 0.851 | 12.604 | 0.068 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `ax` | `strict_current` | 0.851 | 67.892 | 0.013 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `classic` | `profile_balanced` | 3.894 | 22.339 | 0.174 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `classic` | `profile_fast` | 3.894 | 11.369 | 0.343 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.894 | 8.340 | 0.467 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `classic` | `skip_source_error_control` | 3.894 | 12.604 | 0.309 |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `classic` | `strict_current` | 3.894 | 67.892 | 0.057 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `ax` | `profile_balanced` | 0.727 | 22.283 | 0.033 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `ax` | `profile_fast` | 0.727 | 11.137 | 0.065 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.727 | 8.358 | 0.087 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 0.727 | 12.437 | 0.058 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `ax` | `strict_current` | 0.727 | 67.125 | 0.011 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `classic` | `profile_balanced` | 3.798 | 22.283 | 0.170 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `classic` | `profile_fast` | 3.798 | 11.137 | 0.341 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.798 | 8.358 | 0.454 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 3.798 | 12.437 | 0.305 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `classic` | `strict_current` | 3.798 | 67.125 | 0.057 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `ax` | `profile_balanced` | 2.187 | 21.714 | 0.101 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `ax` | `profile_fast` | 2.187 | 11.223 | 0.195 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 2.187 | 8.401 | 0.260 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `ax` | `skip_source_error_control` | 2.187 | 12.287 | 0.178 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `ax` | `strict_current` | 2.187 | 69.158 | 0.032 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `classic` | `profile_balanced` | 4.086 | 21.714 | 0.188 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `classic` | `profile_fast` | 4.086 | 11.223 | 0.364 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.086 | 8.401 | 0.486 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.086 | 12.287 | 0.333 |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `classic` | `strict_current` | 4.086 | 69.158 | 0.059 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.145 | 1.220 | 0.939 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.145 | 0.733 | 1.563 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.145 | 0.567 | 2.021 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.145 | 0.576 | 1.989 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.145 | 1.277 | 0.897 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 2.601 | 1.220 | 2.133 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `classic` | `profile_fast` | 2.601 | 0.733 | 3.549 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 2.601 | 0.567 | 4.590 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 2.601 | 0.576 | 4.516 |
| `vbr1_l1_precision_rectifier` | `bugfix` | `fixed` | `classic` | `strict_current` | 2.601 | 1.277 | 2.037 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `ax` | `profile_balanced` | 0.923 | 0.914 | 1.011 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `ax` | `profile_fast` | 0.923 | 0.721 | 1.281 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.923 | 0.587 | 1.572 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `ax` | `skip_source_error_control` | 0.923 | 0.523 | 1.766 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `ax` | `strict_current` | 0.923 | 0.948 | 0.975 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `classic` | `profile_balanced` | 2.534 | 0.914 | 2.773 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `classic` | `profile_fast` | 2.534 | 0.721 | 3.515 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.534 | 0.587 | 4.313 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `classic` | `skip_source_error_control` | 2.534 | 0.523 | 4.846 |
| `vbr1_l1_precision_rectifier` | `dut` | `gold` | `classic` | `strict_current` | 2.534 | 0.948 | 2.674 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.063 | 1.035 | 1.027 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `ax` | `profile_fast` | 1.063 | 0.628 | 1.693 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.063 | 0.620 | 1.713 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.063 | 0.602 | 1.766 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `ax` | `strict_current` | 1.063 | 1.236 | 0.860 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `classic` | `profile_balanced` | 2.561 | 1.035 | 2.475 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `classic` | `profile_fast` | 2.561 | 0.628 | 4.080 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.561 | 0.620 | 4.128 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 2.561 | 0.602 | 4.256 |
| `vbr1_l1_precision_rectifier` | `e2e` | `gold` | `classic` | `strict_current` | 2.561 | 1.236 | 2.072 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `ax` | `profile_balanced` | 1.600 | 0.893 | 1.792 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `ax` | `profile_fast` | 1.600 | 0.737 | 2.170 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.600 | 0.657 | 2.434 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.600 | 0.656 | 2.439 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `ax` | `strict_current` | 1.600 | 0.873 | 1.832 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `classic` | `profile_balanced` | 3.425 | 0.893 | 3.836 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `classic` | `profile_fast` | 3.425 | 0.737 | 4.645 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.425 | 0.657 | 5.210 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `classic` | `skip_source_error_control` | 3.425 | 0.656 | 5.220 |
| `vbr1_l1_precision_rectifier` | `tb` | `gold` | `classic` | `strict_current` | 3.425 | 0.873 | 3.921 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 0.776 | 9.300 | 0.083 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast` | 0.776 | 3.199 | 0.243 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 0.776 | 1.932 | 0.401 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 0.776 | 4.541 | 0.171 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 0.776 | 9.411 | 0.082 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 6.175 | 9.300 | 0.664 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast` | 6.175 | 3.199 | 1.931 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 6.175 | 1.932 | 3.195 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 6.175 | 4.541 | 1.360 |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 6.175 | 9.411 | 0.656 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `ax` | `profile_balanced` | 0.910 | 9.472 | 0.096 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `ax` | `profile_fast` | 0.910 | 3.154 | 0.289 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.910 | 1.882 | 0.484 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `ax` | `skip_source_error_control` | 0.910 | 4.651 | 0.196 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `ax` | `strict_current` | 0.910 | 9.266 | 0.098 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `classic` | `profile_balanced` | 5.472 | 9.472 | 0.578 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `classic` | `profile_fast` | 5.472 | 3.154 | 1.735 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.472 | 1.882 | 2.908 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `classic` | `skip_source_error_control` | 5.472 | 4.651 | 1.177 |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `classic` | `strict_current` | 5.472 | 9.266 | 0.591 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `ax` | `profile_balanced` | 0.877 | 9.272 | 0.095 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `ax` | `profile_fast` | 0.877 | 3.090 | 0.284 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.877 | 1.788 | 0.490 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 0.877 | 4.512 | 0.194 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 0.877 | 9.127 | 0.096 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `classic` | `profile_balanced` | 6.452 | 9.272 | 0.696 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `classic` | `profile_fast` | 6.452 | 3.090 | 2.088 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 6.452 | 1.788 | 3.608 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 6.452 | 4.512 | 1.430 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 6.452 | 9.127 | 0.707 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `ax` | `profile_balanced` | 1.026 | 9.608 | 0.107 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `ax` | `profile_fast` | 1.026 | 3.102 | 0.331 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.026 | 1.907 | 0.538 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.026 | 4.493 | 0.228 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `ax` | `strict_current` | 1.026 | 9.655 | 0.106 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `classic` | `profile_balanced` | 6.573 | 9.608 | 0.684 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `classic` | `profile_fast` | 6.573 | 3.102 | 2.119 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 6.573 | 1.907 | 3.446 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `classic` | `skip_source_error_control` | 6.573 | 4.493 | 1.463 |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `classic` | `strict_current` | 6.573 | 9.655 | 0.681 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `ax` | `profile_balanced` | 1.657 | 0.565 | 2.934 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `ax` | `profile_fast` | 1.657 | 0.588 | 2.819 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.657 | 0.579 | 2.862 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.657 | 0.595 | 2.784 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `ax` | `strict_current` | 1.657 | 0.772 | 2.145 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `classic` | `profile_balanced` | 5.333 | 0.565 | 9.444 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `classic` | `profile_fast` | 5.333 | 0.588 | 9.077 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.333 | 0.579 | 9.212 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `classic` | `skip_source_error_control` | 5.333 | 0.595 | 8.961 |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `classic` | `strict_current` | 5.333 | 0.772 | 6.904 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.679 | 0.618 | 2.718 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `ax` | `profile_fast` | 1.679 | 0.578 | 2.903 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.679 | 0.598 | 2.808 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.679 | 0.663 | 2.533 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `ax` | `strict_current` | 1.679 | 0.680 | 2.470 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `classic` | `profile_balanced` | 5.413 | 0.618 | 8.766 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `classic` | `profile_fast` | 5.413 | 0.578 | 9.362 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.413 | 0.598 | 9.053 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 5.413 | 0.663 | 8.168 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `classic` | `strict_current` | 5.413 | 0.680 | 7.964 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `ax` | `profile_balanced` | 1.476 | 0.672 | 2.195 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `ax` | `profile_fast` | 1.476 | 0.594 | 2.486 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.476 | 0.679 | 2.173 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.476 | 0.564 | 2.615 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `ax` | `strict_current` | 1.476 | 0.638 | 2.314 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `classic` | `profile_balanced` | 5.575 | 0.672 | 8.292 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `classic` | `profile_fast` | 5.575 | 0.594 | 9.390 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.575 | 0.679 | 8.209 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `classic` | `skip_source_error_control` | 5.575 | 0.564 | 9.881 |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `classic` | `strict_current` | 5.575 | 0.638 | 8.743 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 3.517 | 0.892 | 3.944 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `ax` | `profile_fast` | 3.517 | 0.846 | 4.156 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 3.517 | 1.031 | 3.410 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 3.517 | 0.824 | 4.268 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `ax` | `strict_current` | 3.517 | 1.056 | 3.330 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.870 | 0.892 | 5.461 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.870 | 0.846 | 5.755 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.870 | 1.031 | 4.722 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.870 | 0.824 | 5.910 |
| `vbr1_l1_resettable_integrator` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.870 | 1.056 | 4.612 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `ax` | `profile_balanced` | 1.011 | 1.096 | 0.922 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `ax` | `profile_fast` | 1.011 | 0.929 | 1.088 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.011 | 0.904 | 1.118 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.011 | 0.826 | 1.225 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `ax` | `strict_current` | 1.011 | 1.123 | 0.900 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `classic` | `profile_balanced` | 4.730 | 1.096 | 4.315 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `classic` | `profile_fast` | 4.730 | 0.929 | 5.092 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.730 | 0.904 | 5.229 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `classic` | `skip_source_error_control` | 4.730 | 0.826 | 5.729 |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `classic` | `strict_current` | 4.730 | 1.123 | 4.213 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.298 | 1.068 | 1.216 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `ax` | `profile_fast` | 1.298 | 1.030 | 1.260 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.298 | 0.925 | 1.403 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.298 | 0.898 | 1.446 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `ax` | `strict_current` | 1.298 | 1.081 | 1.201 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.627 | 1.068 | 4.334 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `classic` | `profile_fast` | 4.627 | 1.030 | 4.490 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.627 | 0.925 | 5.003 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.627 | 0.898 | 5.155 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `classic` | `strict_current` | 4.627 | 1.081 | 4.281 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `ax` | `profile_balanced` | 3.661 | 1.084 | 3.377 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `ax` | `profile_fast` | 3.661 | 0.901 | 4.062 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 3.661 | 0.960 | 3.815 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `ax` | `skip_source_error_control` | 3.661 | 0.936 | 3.913 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `ax` | `strict_current` | 3.661 | 1.170 | 3.130 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `classic` | `profile_balanced` | 4.861 | 1.084 | 4.484 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `classic` | `profile_fast` | 4.861 | 0.901 | 5.393 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.861 | 0.960 | 5.066 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.861 | 0.936 | 5.195 |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `classic` | `strict_current` | 4.861 | 1.170 | 4.155 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.111 | 0.885 | 1.254 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.111 | 0.744 | 1.493 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.111 | 0.606 | 1.831 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.111 | 0.655 | 1.695 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.111 | 0.941 | 1.180 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.619 | 0.885 | 5.218 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.619 | 0.744 | 6.209 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.619 | 0.606 | 7.617 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.619 | 0.655 | 7.050 |
| `vbr1_l1_rotating_dem_selector` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.619 | 0.941 | 4.908 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `ax` | `profile_balanced` | 1.190 | 0.868 | 1.371 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `ax` | `profile_fast` | 1.190 | 0.659 | 1.807 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.190 | 0.683 | 1.742 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.190 | 0.748 | 1.591 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `ax` | `strict_current` | 1.190 | 0.950 | 1.253 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `classic` | `profile_balanced` | 4.939 | 0.868 | 5.691 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `classic` | `profile_fast` | 4.939 | 0.659 | 7.500 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.939 | 0.683 | 7.228 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `classic` | `skip_source_error_control` | 4.939 | 0.748 | 6.604 |
| `vbr1_l1_rotating_dem_selector` | `dut` | `gold` | `classic` | `strict_current` | 4.939 | 0.950 | 5.201 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `ax` | `profile_balanced` | 0.779 | 0.813 | 0.957 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `ax` | `profile_fast` | 0.779 | 0.718 | 1.084 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.779 | 0.599 | 1.300 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 0.779 | 0.628 | 1.241 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `ax` | `strict_current` | 0.779 | 0.827 | 0.942 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.299 | 0.813 | 5.285 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `classic` | `profile_fast` | 4.299 | 0.718 | 5.985 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.299 | 0.599 | 7.178 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.299 | 0.628 | 6.850 |
| `vbr1_l1_rotating_dem_selector` | `e2e` | `gold` | `classic` | `strict_current` | 4.299 | 0.827 | 5.199 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `ax` | `profile_balanced` | 0.974 | 0.754 | 1.291 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `ax` | `profile_fast` | 0.974 | 0.617 | 1.577 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.974 | 0.648 | 1.503 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `ax` | `skip_source_error_control` | 0.974 | 0.586 | 1.663 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `ax` | `strict_current` | 0.974 | 0.774 | 1.259 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `classic` | `profile_balanced` | 4.455 | 0.754 | 5.907 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `classic` | `profile_fast` | 4.455 | 0.617 | 7.215 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.455 | 0.648 | 6.875 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.455 | 0.586 | 7.606 |
| `vbr1_l1_rotating_dem_selector` | `tb` | `gold` | `classic` | `strict_current` | 4.455 | 0.774 | 5.757 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.019 | 0.942 | 1.081 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.019 | 0.646 | 1.576 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.019 | 0.677 | 1.504 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.019 | 0.618 | 1.647 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.019 | 0.941 | 1.082 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 2.471 | 0.942 | 2.622 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `classic` | `profile_fast` | 2.471 | 0.646 | 3.823 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 2.471 | 0.677 | 3.649 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 2.471 | 0.618 | 3.996 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `fixed` | `classic` | `strict_current` | 2.471 | 0.941 | 2.625 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `ax` | `profile_balanced` | 1.107 | 0.776 | 1.426 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `ax` | `profile_fast` | 1.107 | 0.745 | 1.485 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.107 | 0.815 | 1.358 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.107 | 0.615 | 1.798 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `ax` | `strict_current` | 1.107 | 0.809 | 1.367 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `classic` | `profile_balanced` | 3.138 | 0.776 | 4.043 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `classic` | `profile_fast` | 3.138 | 0.745 | 4.211 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.138 | 0.815 | 3.849 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `classic` | `skip_source_error_control` | 3.138 | 0.615 | 5.099 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `classic` | `strict_current` | 3.138 | 0.809 | 3.877 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.300 | 0.887 | 1.466 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `ax` | `profile_fast` | 1.300 | 0.767 | 1.694 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.300 | 0.589 | 2.207 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.300 | 0.790 | 1.646 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `ax` | `strict_current` | 1.300 | 0.995 | 1.306 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `classic` | `profile_balanced` | 2.623 | 0.887 | 2.958 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `classic` | `profile_fast` | 2.623 | 0.767 | 3.420 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.623 | 0.589 | 4.455 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 2.623 | 0.790 | 3.322 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `classic` | `strict_current` | 2.623 | 0.995 | 2.636 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `ax` | `profile_balanced` | 1.013 | 0.999 | 1.014 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `ax` | `profile_fast` | 1.013 | 0.738 | 1.372 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.013 | 0.694 | 1.459 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `ax` | `strict_current` | 1.013 | 1.017 | 0.996 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `classic` | `profile_balanced` | 3.167 | 0.999 | 3.170 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `classic` | `profile_fast` | 3.167 | 0.738 | 4.291 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.167 | 0.694 | 4.563 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `classic` | `strict_current` | 3.167 | 1.017 | 3.114 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 3.122 | 1.383 | 2.257 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `ax` | `profile_fast` | 3.122 | 0.883 | 3.535 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 3.122 | 0.861 | 3.627 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 3.122 | 1.253 | 2.492 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `ax` | `strict_current` | 3.122 | 1.359 | 2.297 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.699 | 1.383 | 3.397 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.699 | 0.883 | 5.320 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.699 | 0.861 | 5.459 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.699 | 1.253 | 3.751 |
| `vbr1_l1_sar_logic` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.699 | 1.359 | 3.458 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `ax` | `profile_balanced` | 0.893 | 1.360 | 0.657 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `ax` | `profile_fast` | 0.893 | 0.929 | 0.962 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.893 | 0.790 | 1.131 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `ax` | `skip_source_error_control` | 0.893 | 1.245 | 0.718 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `ax` | `strict_current` | 0.893 | 1.310 | 0.682 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `classic` | `profile_balanced` | 4.507 | 1.360 | 3.314 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `classic` | `profile_fast` | 4.507 | 0.929 | 4.853 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.507 | 0.790 | 5.704 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `classic` | `skip_source_error_control` | 4.507 | 1.245 | 3.622 |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `classic` | `strict_current` | 4.507 | 1.310 | 3.442 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `ax` | `profile_balanced` | 3.002 | 1.305 | 2.301 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `ax` | `profile_fast` | 3.002 | 0.805 | 3.728 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 3.002 | 0.954 | 3.147 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 3.002 | 1.110 | 2.704 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `ax` | `strict_current` | 3.002 | 1.351 | 2.222 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.527 | 1.305 | 3.470 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `classic` | `profile_fast` | 4.527 | 0.805 | 5.623 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.527 | 0.954 | 4.746 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.527 | 1.110 | 4.079 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `classic` | `strict_current` | 4.527 | 1.351 | 3.351 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `ax` | `profile_balanced` | 3.304 | 1.282 | 2.578 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `ax` | `profile_fast` | 3.304 | 0.904 | 3.656 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 3.304 | 0.702 | 4.705 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `ax` | `skip_source_error_control` | 3.304 | 1.115 | 2.964 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `ax` | `strict_current` | 3.304 | 1.316 | 2.511 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `classic` | `profile_balanced` | 4.588 | 1.282 | 3.580 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `classic` | `profile_fast` | 4.588 | 0.904 | 5.077 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.588 | 0.702 | 6.534 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.588 | 1.115 | 4.117 |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `classic` | `strict_current` | 4.588 | 1.316 | 3.487 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 3.616 | 0.613 | 5.900 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `ax` | `profile_fast` | 3.616 | 0.696 | 5.196 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 3.616 | 0.680 | 5.315 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 3.616 | 0.625 | 5.789 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `ax` | `strict_current` | 3.616 | 0.611 | 5.914 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 3.617 | 0.613 | 5.900 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `classic` | `profile_fast` | 3.617 | 0.696 | 5.197 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 3.617 | 0.680 | 5.316 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 3.617 | 0.625 | 5.790 |
| `vbr1_l1_segmented_dac` | `bugfix` | `fixed` | `classic` | `strict_current` | 3.617 | 0.611 | 5.915 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `ax` | `profile_balanced` | 0.956 | 0.680 | 1.405 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `ax` | `profile_fast` | 0.956 | 0.646 | 1.480 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.956 | 0.683 | 1.399 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `ax` | `skip_source_error_control` | 0.956 | 0.623 | 1.534 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `ax` | `strict_current` | 0.956 | 0.713 | 1.341 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `classic` | `profile_balanced` | 3.026 | 0.680 | 4.448 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `classic` | `profile_fast` | 3.026 | 0.646 | 4.686 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.026 | 0.683 | 4.429 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `classic` | `skip_source_error_control` | 3.026 | 0.623 | 4.857 |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `classic` | `strict_current` | 3.026 | 0.713 | 4.245 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `ax` | `profile_balanced` | 3.397 | 0.641 | 5.303 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `ax` | `profile_fast` | 3.397 | 0.626 | 5.423 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 3.397 | 0.747 | 4.548 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 3.397 | 0.635 | 5.351 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `ax` | `strict_current` | 3.397 | 0.687 | 4.945 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `classic` | `profile_balanced` | 3.306 | 0.641 | 5.161 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `classic` | `profile_fast` | 3.306 | 0.626 | 5.278 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.306 | 0.747 | 4.426 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 3.306 | 0.635 | 5.208 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `classic` | `strict_current` | 3.306 | 0.687 | 4.813 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `ax` | `profile_balanced` | 1.053 | 0.694 | 1.518 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `ax` | `profile_fast` | 1.053 | 0.776 | 1.357 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.053 | 0.626 | 1.681 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.053 | 0.695 | 1.515 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `ax` | `strict_current` | 1.053 | 0.786 | 1.340 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `classic` | `profile_balanced` | 3.424 | 0.694 | 4.936 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `classic` | `profile_fast` | 3.424 | 0.776 | 4.412 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.424 | 0.626 | 5.467 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `classic` | `skip_source_error_control` | 3.424 | 0.695 | 4.927 |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `classic` | `strict_current` | 3.424 | 0.786 | 4.356 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.363 | 2.009 | 0.679 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.363 | 1.310 | 1.041 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.363 | 0.900 | 1.515 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.363 | 1.033 | 1.319 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.363 | 2.074 | 0.657 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.805 | 2.009 | 2.392 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.805 | 1.310 | 3.667 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.805 | 0.900 | 5.338 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.805 | 1.033 | 4.650 |
| `vbr1_l1_serializer_frame_aligner` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.805 | 2.074 | 2.317 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `ax` | `profile_balanced` | 0.922 | 1.979 | 0.466 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `ax` | `profile_fast` | 0.922 | 1.208 | 0.764 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.922 | 0.970 | 0.951 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `ax` | `skip_source_error_control` | 0.922 | 0.994 | 0.928 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `ax` | `strict_current` | 0.922 | 1.949 | 0.473 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `classic` | `profile_balanced` | 4.613 | 1.979 | 2.331 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `classic` | `profile_fast` | 4.613 | 1.208 | 3.818 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.613 | 0.970 | 4.756 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `classic` | `skip_source_error_control` | 4.613 | 0.994 | 4.643 |
| `vbr1_l1_serializer_frame_aligner` | `dut` | `gold` | `classic` | `strict_current` | 4.613 | 1.949 | 2.367 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `ax` | `profile_balanced` | 0.852 | 1.884 | 0.452 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `ax` | `profile_fast` | 0.852 | 1.230 | 0.692 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.852 | 0.890 | 0.957 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 0.852 | 0.916 | 0.930 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `ax` | `strict_current` | 0.852 | 1.930 | 0.441 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.646 | 1.884 | 2.465 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `classic` | `profile_fast` | 4.646 | 1.230 | 3.776 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.646 | 0.890 | 5.220 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.646 | 0.916 | 5.074 |
| `vbr1_l1_serializer_frame_aligner` | `e2e` | `gold` | `classic` | `strict_current` | 4.646 | 1.930 | 2.407 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `ax` | `profile_balanced` | 0.949 | 2.130 | 0.445 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `ax` | `profile_fast` | 0.949 | 1.213 | 0.782 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.949 | 0.901 | 1.052 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `ax` | `skip_source_error_control` | 0.949 | 0.997 | 0.952 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `ax` | `strict_current` | 0.949 | 2.200 | 0.431 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `classic` | `profile_balanced` | 4.664 | 2.130 | 2.190 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `classic` | `profile_fast` | 4.664 | 1.213 | 3.844 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.664 | 0.901 | 5.174 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.664 | 0.997 | 4.678 |
| `vbr1_l1_serializer_frame_aligner` | `tb` | `gold` | `classic` | `strict_current` | 4.664 | 2.200 | 2.119 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.338 | 0.903 | 1.481 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `ax` | `profile_fast` | 1.338 | 1.072 | 1.248 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.338 | 0.781 | 1.713 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.338 | 0.807 | 1.657 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `ax` | `strict_current` | 1.338 | 1.024 | 1.306 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `classic` | `profile_balanced` | 5.312 | 0.903 | 5.882 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `classic` | `profile_fast` | 5.312 | 1.072 | 4.953 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.312 | 0.781 | 6.800 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 5.312 | 0.807 | 6.579 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `classic` | `strict_current` | 5.312 | 1.024 | 5.186 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `ax` | `profile_balanced` | 1.114 | 0.988 | 1.127 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `ax` | `profile_fast` | 1.114 | 0.681 | 1.635 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.114 | 0.716 | 1.556 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.114 | 0.685 | 1.626 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `ax` | `strict_current` | 1.114 | 0.821 | 1.356 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `classic` | `profile_balanced` | 4.599 | 0.988 | 4.653 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `classic` | `profile_fast` | 4.599 | 0.681 | 6.752 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.599 | 0.716 | 6.425 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.599 | 0.685 | 6.715 |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `classic` | `strict_current` | 4.599 | 0.821 | 5.600 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `ax` | `profile_balanced` | 1.110 | 0.852 | 1.303 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `ax` | `profile_fast` | 1.110 | 0.907 | 1.224 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.110 | 0.696 | 1.596 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.110 | 0.719 | 1.544 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `ax` | `strict_current` | 1.110 | 0.946 | 1.174 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `classic` | `profile_balanced` | 2.589 | 0.852 | 3.038 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `classic` | `profile_fast` | 2.589 | 0.907 | 2.854 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.589 | 0.696 | 3.721 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `classic` | `skip_source_error_control` | 2.589 | 0.719 | 3.600 |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `classic` | `strict_current` | 2.589 | 0.946 | 2.738 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.198 | 0.877 | 1.366 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `ax` | `profile_fast` | 1.198 | 0.811 | 1.478 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.198 | 0.737 | 1.627 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.198 | 0.711 | 1.686 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `ax` | `strict_current` | 1.198 | 0.928 | 1.292 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `classic` | `profile_balanced` | 2.336 | 0.877 | 2.663 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `classic` | `profile_fast` | 2.336 | 0.811 | 2.882 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.336 | 0.737 | 3.172 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 2.336 | 0.711 | 3.288 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `classic` | `strict_current` | 2.336 | 0.928 | 2.519 |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `ax` | `profile_balanced` | 1.014 | 0.818 | 1.241 |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `ax` | `profile_fast` | 1.014 | 0.781 | 1.300 |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.014 | 0.892 | 1.138 |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.014 | 0.856 | 1.186 |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `ax` | `strict_current` | 1.014 | 0.951 | 1.067 |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `classic` | `profile_balanced` | 2.700 | 0.818 | 3.302 |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `classic` | `profile_fast` | 2.700 | 0.781 | 3.459 |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.700 | 0.892 | 3.028 |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `classic` | `skip_source_error_control` | 2.700 | 0.856 | 3.156 |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `classic` | `strict_current` | 2.700 | 0.951 | 2.838 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.286 | 0.840 | 1.531 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.286 | 0.739 | 1.739 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.286 | 0.717 | 1.793 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.286 | 0.738 | 1.743 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.286 | 0.793 | 1.622 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 2.988 | 0.840 | 3.557 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `classic` | `profile_fast` | 2.988 | 0.739 | 4.041 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 2.988 | 0.717 | 4.167 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 2.988 | 0.738 | 4.050 |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `fixed` | `classic` | `strict_current` | 2.988 | 0.793 | 3.769 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `ax` | `profile_balanced` | 1.259 | 0.659 | 1.910 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `ax` | `profile_fast` | 1.259 | 0.589 | 2.136 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.259 | 0.682 | 1.845 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.259 | 0.705 | 1.784 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `ax` | `strict_current` | 1.259 | 0.698 | 1.804 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `classic` | `profile_balanced` | 2.881 | 0.659 | 4.372 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `classic` | `profile_fast` | 2.881 | 0.589 | 4.889 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.881 | 0.682 | 4.223 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `classic` | `skip_source_error_control` | 2.881 | 0.705 | 4.084 |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `classic` | `strict_current` | 2.881 | 0.698 | 4.128 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.071 | 0.776 | 1.379 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `ax` | `profile_fast` | 1.071 | 0.743 | 1.442 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.071 | 0.780 | 1.372 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.071 | 0.698 | 1.535 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `ax` | `strict_current` | 1.071 | 0.803 | 1.333 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `classic` | `profile_balanced` | 3.124 | 0.776 | 4.024 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `classic` | `profile_fast` | 3.124 | 0.743 | 4.207 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.124 | 0.780 | 4.005 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 3.124 | 0.698 | 4.478 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `classic` | `strict_current` | 3.124 | 0.803 | 3.888 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `ax` | `profile_balanced` | 1.008 | 0.697 | 1.446 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `ax` | `profile_fast` | 1.008 | 0.709 | 1.422 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.008 | 0.805 | 1.251 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.008 | 0.779 | 1.294 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `ax` | `strict_current` | 1.008 | 0.792 | 1.272 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `classic` | `profile_balanced` | 2.776 | 0.697 | 3.982 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `classic` | `profile_fast` | 2.776 | 0.709 | 3.918 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.776 | 0.805 | 3.447 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `classic` | `skip_source_error_control` | 2.776 | 0.779 | 3.565 |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `classic` | `strict_current` | 2.776 | 0.792 | 3.503 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.085 | 1.287 | 0.843 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.085 | 0.916 | 1.184 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.085 | 0.765 | 1.418 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.085 | 0.654 | 1.658 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.085 | 1.345 | 0.807 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.503 | 1.287 | 3.500 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.503 | 0.916 | 4.916 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.503 | 0.765 | 5.885 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.503 | 0.654 | 6.883 |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.503 | 1.345 | 3.349 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `ax` | `profile_balanced` | 1.179 | 1.054 | 1.118 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `ax` | `profile_fast` | 1.179 | 0.831 | 1.419 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.179 | 0.881 | 1.338 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.179 | 0.645 | 1.826 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `ax` | `strict_current` | 1.179 | 1.169 | 1.008 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `classic` | `profile_balanced` | 4.672 | 1.054 | 4.432 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `classic` | `profile_fast` | 4.672 | 0.831 | 5.624 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.672 | 0.881 | 5.306 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `classic` | `skip_source_error_control` | 4.672 | 0.645 | 7.239 |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `classic` | `strict_current` | 4.672 | 1.169 | 3.996 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.120 | 1.300 | 0.861 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `ax` | `profile_fast` | 1.120 | 1.006 | 1.113 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.120 | 0.644 | 1.738 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.120 | 0.825 | 1.358 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `ax` | `strict_current` | 1.120 | 1.187 | 0.944 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.701 | 1.300 | 3.615 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `classic` | `profile_fast` | 4.701 | 1.006 | 4.672 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.701 | 0.644 | 7.298 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.701 | 0.825 | 5.701 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `classic` | `strict_current` | 4.701 | 1.187 | 3.962 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `ax` | `profile_balanced` | 1.408 | 1.217 | 1.158 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `ax` | `profile_fast` | 1.408 | 0.966 | 1.458 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.408 | 0.585 | 2.409 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.408 | 0.628 | 2.243 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `ax` | `strict_current` | 1.408 | 1.136 | 1.239 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `classic` | `profile_balanced` | 5.244 | 1.217 | 4.310 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `classic` | `profile_fast` | 5.244 | 0.966 | 5.430 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.244 | 0.585 | 8.969 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `classic` | `skip_source_error_control` | 5.244 | 0.628 | 8.350 |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `classic` | `strict_current` | 5.244 | 1.136 | 4.614 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.268 | 2.111 | 0.601 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.268 | 1.678 | 0.755 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.268 | 1.494 | 0.849 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.268 | 1.490 | 0.851 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.268 | 2.110 | 0.601 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.267 | 2.111 | 2.022 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.267 | 1.678 | 2.542 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.267 | 1.494 | 2.857 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.267 | 1.490 | 2.864 |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.267 | 2.110 | 2.023 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `ax` | `profile_balanced` | 1.141 | 2.664 | 0.428 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `ax` | `profile_fast` | 1.141 | 1.271 | 0.898 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.141 | 0.835 | 1.366 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.141 | 1.822 | 0.626 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `ax` | `strict_current` | 1.141 | 2.838 | 0.402 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `classic` | `profile_balanced` | 4.101 | 2.664 | 1.539 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `classic` | `profile_fast` | 4.101 | 1.271 | 3.227 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.101 | 0.835 | 4.911 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `classic` | `skip_source_error_control` | 4.101 | 1.822 | 2.251 |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `classic` | `strict_current` | 4.101 | 2.838 | 1.445 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `ax` | `profile_balanced` | 0.720 | 2.759 | 0.261 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `ax` | `profile_fast` | 0.720 | 1.299 | 0.554 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.720 | 0.841 | 0.856 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 0.720 | 1.721 | 0.418 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 0.720 | 2.710 | 0.266 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `classic` | `profile_balanced` | 3.395 | 2.759 | 1.230 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `classic` | `profile_fast` | 3.395 | 1.299 | 2.613 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.395 | 0.841 | 4.039 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 3.395 | 1.721 | 1.973 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 3.395 | 2.710 | 1.253 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `ax` | `profile_balanced` | 1.035 | 2.764 | 0.375 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `ax` | `profile_fast` | 1.035 | 1.410 | 0.735 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.035 | 0.939 | 1.103 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.035 | 1.731 | 0.598 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `ax` | `strict_current` | 1.035 | 2.849 | 0.363 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `classic` | `profile_balanced` | 3.860 | 2.764 | 1.396 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `classic` | `profile_fast` | 3.860 | 1.410 | 2.738 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.860 | 0.939 | 4.110 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `classic` | `skip_source_error_control` | 3.860 | 1.731 | 2.230 |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `classic` | `strict_current` | 3.860 | 2.849 | 1.355 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.328 | 1.522 | 0.872 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.328 | 1.004 | 1.322 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.328 | 0.624 | 2.128 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.328 | 0.590 | 2.249 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.328 | 1.532 | 0.866 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.984 | 1.522 | 3.275 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.984 | 1.004 | 4.963 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.984 | 0.624 | 7.989 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.984 | 0.590 | 8.441 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.984 | 1.532 | 3.252 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `ax` | `profile_balanced` | 1.226 | 1.473 | 0.832 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `ax` | `profile_fast` | 1.226 | 1.122 | 1.092 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.226 | 0.613 | 1.998 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.226 | 0.658 | 1.864 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `ax` | `strict_current` | 1.226 | 1.516 | 0.808 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `classic` | `profile_balanced` | 4.518 | 1.473 | 3.068 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `classic` | `profile_fast` | 4.518 | 1.122 | 4.026 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.518 | 0.613 | 7.366 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `classic` | `skip_source_error_control` | 4.518 | 0.658 | 6.870 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `classic` | `strict_current` | 4.518 | 1.516 | 2.980 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.449 | 1.454 | 0.996 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `ax` | `profile_fast` | 1.449 | 0.931 | 1.557 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.449 | 0.671 | 2.158 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.449 | 0.618 | 2.343 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `ax` | `strict_current` | 1.449 | 1.506 | 0.962 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.756 | 1.454 | 3.270 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `classic` | `profile_fast` | 4.756 | 0.931 | 5.109 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.756 | 0.671 | 7.084 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.756 | 0.618 | 7.692 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `classic` | `strict_current` | 4.756 | 1.506 | 3.158 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `ax` | `profile_balanced` | 0.894 | 1.478 | 0.605 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `ax` | `profile_fast` | 0.894 | 0.971 | 0.920 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.894 | 0.715 | 1.249 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `ax` | `skip_source_error_control` | 0.894 | 0.527 | 1.695 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `ax` | `strict_current` | 0.894 | 1.519 | 0.589 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `classic` | `profile_balanced` | 4.294 | 1.478 | 2.906 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `classic` | `profile_fast` | 4.294 | 0.971 | 4.420 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.294 | 0.715 | 6.002 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.294 | 0.527 | 8.143 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `classic` | `strict_current` | 4.294 | 1.519 | 2.828 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 3.640 | 0.630 | 5.772 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `ax` | `profile_fast` | 3.640 | 0.661 | 5.507 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 3.640 | 0.738 | 4.933 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 3.640 | 0.595 | 6.113 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `ax` | `strict_current` | 3.640 | 0.763 | 4.769 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 5.441 | 0.630 | 8.630 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `classic` | `profile_fast` | 5.441 | 0.661 | 8.232 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 5.441 | 0.738 | 7.375 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 5.441 | 0.595 | 9.139 |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `fixed` | `classic` | `strict_current` | 5.441 | 0.763 | 7.130 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `ax` | `profile_balanced` | 0.988 | 0.705 | 1.402 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `ax` | `profile_fast` | 0.988 | 0.704 | 1.404 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.988 | 0.627 | 1.575 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `ax` | `skip_source_error_control` | 0.988 | 0.668 | 1.479 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `ax` | `strict_current` | 0.988 | 0.830 | 1.190 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `classic` | `profile_balanced` | 4.973 | 0.705 | 7.057 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `classic` | `profile_fast` | 4.973 | 0.704 | 7.066 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.973 | 0.627 | 7.931 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `classic` | `skip_source_error_control` | 4.973 | 0.668 | 7.444 |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `classic` | `strict_current` | 4.973 | 0.830 | 5.990 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.241 | 0.808 | 1.537 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `ax` | `profile_fast` | 1.241 | 0.692 | 1.794 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.241 | 0.670 | 1.852 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.241 | 0.658 | 1.886 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `ax` | `strict_current` | 1.241 | 0.562 | 2.207 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `classic` | `profile_balanced` | 5.374 | 0.808 | 6.654 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `classic` | `profile_fast` | 5.374 | 0.692 | 7.767 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.374 | 0.670 | 8.019 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 5.374 | 0.658 | 8.167 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `classic` | `strict_current` | 5.374 | 0.562 | 9.556 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `ax` | `profile_balanced` | 3.763 | 0.601 | 6.260 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `ax` | `profile_fast` | 3.763 | 0.541 | 6.957 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 3.763 | 0.600 | 6.272 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `ax` | `skip_source_error_control` | 3.763 | 0.541 | 6.961 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `ax` | `strict_current` | 3.763 | 0.636 | 5.919 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `classic` | `profile_balanced` | 4.984 | 0.601 | 8.291 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `classic` | `profile_fast` | 4.984 | 0.541 | 9.215 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.984 | 0.600 | 8.307 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.984 | 0.541 | 9.220 |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `classic` | `strict_current` | 4.984 | 0.636 | 7.839 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.157 | 0.721 | 1.605 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.157 | 0.853 | 1.357 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.157 | 0.576 | 2.008 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.157 | 0.807 | 1.433 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.157 | 0.736 | 1.573 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 5.383 | 0.721 | 7.467 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast` | 5.383 | 0.853 | 6.311 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 5.383 | 0.576 | 9.340 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 5.383 | 0.807 | 6.668 |
| `vbr1_l1_threshold_comparator` | `bugfix` | `fixed` | `classic` | `strict_current` | 5.383 | 0.736 | 7.318 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `ax` | `profile_balanced` | 0.958 | 0.741 | 1.291 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `ax` | `profile_fast` | 0.958 | 0.526 | 1.820 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.958 | 0.610 | 1.570 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `ax` | `skip_source_error_control` | 0.958 | 0.644 | 1.488 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `ax` | `strict_current` | 0.958 | 0.707 | 1.355 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `classic` | `profile_balanced` | 5.628 | 0.741 | 7.591 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `classic` | `profile_fast` | 5.628 | 0.526 | 10.699 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.628 | 0.610 | 9.227 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `classic` | `skip_source_error_control` | 5.628 | 0.644 | 8.743 |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `classic` | `strict_current` | 5.628 | 0.707 | 7.965 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.133 | 0.623 | 1.817 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `ax` | `profile_fast` | 1.133 | 0.632 | 1.791 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.133 | 0.575 | 1.969 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.133 | 0.639 | 1.772 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `ax` | `strict_current` | 1.133 | 0.697 | 1.626 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `classic` | `profile_balanced` | 5.195 | 0.623 | 8.335 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `classic` | `profile_fast` | 5.195 | 0.632 | 8.214 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.195 | 0.575 | 9.030 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 5.195 | 0.639 | 8.126 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `classic` | `strict_current` | 5.195 | 0.697 | 7.458 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `ax` | `profile_balanced` | 1.679 | 0.726 | 2.313 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `ax` | `profile_fast` | 1.679 | 0.751 | 2.235 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.679 | 0.666 | 2.522 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.679 | 0.646 | 2.600 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `ax` | `strict_current` | 1.679 | 0.670 | 2.507 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `classic` | `profile_balanced` | 5.734 | 0.726 | 7.899 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `classic` | `profile_fast` | 5.734 | 0.751 | 7.633 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.734 | 0.666 | 8.610 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `classic` | `skip_source_error_control` | 5.734 | 0.646 | 8.878 |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `classic` | `strict_current` | 5.734 | 0.670 | 8.560 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 2.900 | 0.972 | 2.984 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `ax` | `profile_fast` | 2.900 | 0.830 | 3.496 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 2.900 | 0.562 | 5.161 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 2.900 | 0.760 | 3.817 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `ax` | `strict_current` | 2.900 | 1.000 | 2.901 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 2.954 | 0.972 | 3.040 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `classic` | `profile_fast` | 2.954 | 0.830 | 3.561 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 2.954 | 0.562 | 5.257 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 2.954 | 0.760 | 3.888 |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `fixed` | `classic` | `strict_current` | 2.954 | 1.000 | 2.955 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `ax` | `profile_balanced` | 3.095 | 1.252 | 2.471 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `ax` | `profile_fast` | 3.095 | 0.778 | 3.979 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 3.095 | 0.681 | 4.547 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `ax` | `skip_source_error_control` | 3.095 | 0.777 | 3.984 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `ax` | `strict_current` | 3.095 | 1.184 | 2.615 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `classic` | `profile_balanced` | 3.087 | 1.252 | 2.465 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `classic` | `profile_fast` | 3.087 | 0.778 | 3.969 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.087 | 0.681 | 4.536 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `classic` | `skip_source_error_control` | 3.087 | 0.777 | 3.974 |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `classic` | `strict_current` | 3.087 | 1.184 | 2.608 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.734 | 0.845 | 2.052 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `ax` | `profile_fast` | 1.734 | 0.727 | 2.387 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.734 | 0.747 | 2.322 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.734 | 0.658 | 2.635 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `ax` | `strict_current` | 1.734 | 0.943 | 1.839 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `classic` | `profile_balanced` | 2.679 | 0.845 | 3.170 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `classic` | `profile_fast` | 2.679 | 0.727 | 3.687 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.679 | 0.747 | 3.586 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 2.679 | 0.658 | 4.070 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `classic` | `strict_current` | 2.679 | 0.943 | 2.840 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `ax` | `profile_balanced` | 1.121 | 1.129 | 0.993 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `ax` | `profile_fast` | 1.121 | 0.762 | 1.472 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.121 | 0.659 | 1.702 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.121 | 0.636 | 1.763 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `ax` | `strict_current` | 1.121 | 1.019 | 1.100 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `classic` | `profile_balanced` | 2.730 | 1.129 | 2.419 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `classic` | `profile_fast` | 2.730 | 0.762 | 3.584 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.730 | 0.659 | 4.145 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `classic` | `skip_source_error_control` | 2.730 | 0.636 | 4.293 |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `classic` | `strict_current` | 2.730 | 1.019 | 2.679 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 0.988 | 0.825 | 1.197 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `ax` | `profile_fast` | 0.988 | 0.783 | 1.261 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 0.988 | 0.899 | 1.099 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 0.988 | 0.770 | 1.282 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `ax` | `strict_current` | 0.988 | 0.872 | 1.132 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 5.495 | 0.825 | 6.660 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `classic` | `profile_fast` | 5.495 | 0.783 | 7.018 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 5.495 | 0.899 | 6.113 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 5.495 | 0.770 | 7.136 |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `fixed` | `classic` | `strict_current` | 5.495 | 0.872 | 6.299 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `ax` | `profile_balanced` | 0.941 | 0.691 | 1.363 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `ax` | `profile_fast` | 0.941 | 0.636 | 1.480 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.941 | 0.659 | 1.428 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `ax` | `skip_source_error_control` | 0.941 | 0.636 | 1.480 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `ax` | `strict_current` | 0.941 | 0.751 | 1.253 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `classic` | `profile_balanced` | 4.293 | 0.691 | 6.214 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `classic` | `profile_fast` | 4.293 | 0.636 | 6.749 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.293 | 0.659 | 6.513 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `classic` | `skip_source_error_control` | 4.293 | 0.636 | 6.747 |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `classic` | `strict_current` | 4.293 | 0.751 | 5.713 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.437 | 0.712 | 2.018 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `ax` | `profile_fast` | 1.437 | 0.736 | 1.953 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.437 | 0.661 | 2.173 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.437 | 0.839 | 1.713 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `ax` | `strict_current` | 1.437 | 0.734 | 1.959 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.873 | 0.712 | 6.841 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `classic` | `profile_fast` | 4.873 | 0.736 | 6.620 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.873 | 0.661 | 7.366 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.873 | 0.839 | 5.806 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `classic` | `strict_current` | 4.873 | 0.734 | 6.642 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `ax` | `profile_balanced` | 1.448 | 0.650 | 2.228 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `ax` | `profile_fast` | 1.448 | 0.627 | 2.307 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.448 | 0.721 | 2.007 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.448 | 0.684 | 2.115 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `ax` | `strict_current` | 1.448 | 0.699 | 2.072 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `classic` | `profile_balanced` | 5.290 | 0.650 | 8.141 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `classic` | `profile_fast` | 5.290 | 0.627 | 8.431 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.290 | 0.721 | 7.334 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `classic` | `skip_source_error_control` | 5.290 | 0.684 | 7.729 |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `classic` | `strict_current` | 5.290 | 0.699 | 7.570 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.138 | 0.861 | 1.322 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.138 | 0.935 | 1.218 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.138 | 0.876 | 1.299 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.138 | 0.888 | 1.282 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.138 | 0.848 | 1.343 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.771 | 0.861 | 5.541 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.771 | 0.935 | 5.105 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.771 | 0.876 | 5.444 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.771 | 0.888 | 5.375 |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.771 | 0.848 | 5.629 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `ax` | `profile_balanced` | 1.395 | 0.896 | 1.557 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `ax` | `profile_fast` | 1.395 | 0.863 | 1.617 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.395 | 0.831 | 1.679 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.395 | 0.838 | 1.665 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `ax` | `strict_current` | 1.395 | 0.950 | 1.469 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `classic` | `profile_balanced` | 4.796 | 0.896 | 5.355 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `classic` | `profile_fast` | 4.796 | 0.863 | 5.559 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.796 | 0.831 | 5.773 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `classic` | `skip_source_error_control` | 4.796 | 0.838 | 5.725 |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `classic` | `strict_current` | 4.796 | 0.950 | 5.049 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.093 | 0.985 | 1.109 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `ax` | `profile_fast` | 1.093 | 0.843 | 1.296 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.093 | 0.787 | 1.388 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.093 | 0.780 | 1.401 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `ax` | `strict_current` | 1.093 | 1.018 | 1.073 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.918 | 0.985 | 4.992 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `classic` | `profile_fast` | 4.918 | 0.843 | 5.835 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.918 | 0.787 | 6.249 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.918 | 0.780 | 6.307 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `classic` | `strict_current` | 4.918 | 1.018 | 4.832 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `ax` | `profile_balanced` | 0.979 | 0.818 | 1.197 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `ax` | `profile_fast` | 0.979 | 0.806 | 1.215 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.979 | 0.807 | 1.214 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `ax` | `skip_source_error_control` | 0.979 | 0.840 | 1.166 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `ax` | `strict_current` | 0.979 | 0.933 | 1.049 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `classic` | `profile_balanced` | 3.906 | 0.818 | 4.775 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `classic` | `profile_fast` | 3.906 | 0.806 | 4.845 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.906 | 0.807 | 4.842 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `classic` | `skip_source_error_control` | 3.906 | 0.840 | 4.649 |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `classic` | `strict_current` | 3.906 | 0.933 | 4.184 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 2.668 | 0.935 | 2.854 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `ax` | `profile_fast` | 2.668 | 0.900 | 2.964 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 2.668 | 0.839 | 3.181 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 2.668 | 0.915 | 2.916 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `ax` | `strict_current` | 2.668 | 0.886 | 3.011 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 2.429 | 0.935 | 2.598 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `classic` | `profile_fast` | 2.429 | 0.900 | 2.698 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 2.429 | 0.839 | 2.896 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 2.429 | 0.915 | 2.654 |
| `vbr1_l1_voltage_clamp_or_limiter` | `bugfix` | `fixed` | `classic` | `strict_current` | 2.429 | 0.886 | 2.741 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `ax` | `profile_balanced` | 2.722 | 0.695 | 3.917 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `ax` | `profile_fast` | 2.722 | 0.865 | 3.149 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 2.722 | 0.849 | 3.206 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `ax` | `skip_source_error_control` | 2.722 | 0.945 | 2.880 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `ax` | `strict_current` | 2.722 | 0.860 | 3.166 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `classic` | `profile_balanced` | 2.589 | 0.695 | 3.725 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `classic` | `profile_fast` | 2.589 | 0.865 | 2.994 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.589 | 0.849 | 3.048 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `classic` | `skip_source_error_control` | 2.589 | 0.945 | 2.738 |
| `vbr1_l1_voltage_clamp_or_limiter` | `dut` | `gold` | `classic` | `strict_current` | 2.589 | 0.860 | 3.011 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.135 | 0.819 | 1.386 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `ax` | `profile_fast` | 1.135 | 0.881 | 1.289 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.135 | 0.881 | 1.289 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.135 | 1.033 | 1.099 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `ax` | `strict_current` | 1.135 | 0.838 | 1.355 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `classic` | `profile_balanced` | 2.965 | 0.819 | 3.621 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `classic` | `profile_fast` | 2.965 | 0.881 | 3.367 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 2.965 | 0.881 | 3.367 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 2.965 | 1.033 | 2.871 |
| `vbr1_l1_voltage_clamp_or_limiter` | `e2e` | `gold` | `classic` | `strict_current` | 2.965 | 0.838 | 3.539 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `ax` | `profile_balanced` | 1.600 | 1.061 | 1.508 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `ax` | `profile_fast` | 1.600 | 0.951 | 1.683 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.600 | 0.872 | 1.834 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.600 | 1.029 | 1.555 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `ax` | `strict_current` | 1.600 | 1.057 | 1.513 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `classic` | `profile_balanced` | 3.009 | 1.061 | 2.836 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `classic` | `profile_fast` | 3.009 | 0.951 | 3.165 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.009 | 0.872 | 3.449 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `classic` | `skip_source_error_control` | 3.009 | 1.029 | 2.924 |
| `vbr1_l1_voltage_clamp_or_limiter` | `tb` | `gold` | `classic` | `strict_current` | 3.009 | 1.057 | 2.845 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 1.035 | 1.122 | 0.922 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `ax` | `profile_fast` | 1.035 | 0.921 | 1.124 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 1.035 | 0.593 | 1.744 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 1.035 | 0.719 | 1.440 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `ax` | `strict_current` | 1.035 | 1.373 | 0.754 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.693 | 1.122 | 4.182 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.693 | 0.921 | 5.097 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.693 | 0.593 | 7.908 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.693 | 0.719 | 6.530 |
| `vbr1_l1_voltage_gain_amplifier` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.693 | 1.373 | 3.419 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `ax` | `profile_balanced` | 1.364 | 1.207 | 1.129 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `ax` | `profile_fast` | 1.364 | 0.845 | 1.613 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.364 | 0.698 | 1.955 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.364 | 0.702 | 1.943 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `ax` | `strict_current` | 1.364 | 1.218 | 1.120 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `classic` | `profile_balanced` | 5.023 | 1.207 | 4.160 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `classic` | `profile_fast` | 5.023 | 0.845 | 5.942 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.023 | 0.698 | 7.201 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `classic` | `skip_source_error_control` | 5.023 | 0.702 | 7.156 |
| `vbr1_l1_voltage_gain_amplifier` | `dut` | `gold` | `classic` | `strict_current` | 5.023 | 1.218 | 4.124 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.198 | 1.042 | 1.149 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `ax` | `profile_fast` | 1.198 | 0.855 | 1.401 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.198 | 0.674 | 1.777 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.198 | 0.626 | 1.912 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `ax` | `strict_current` | 1.198 | 1.264 | 0.948 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.919 | 1.042 | 4.719 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `classic` | `profile_fast` | 4.919 | 0.855 | 5.755 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.919 | 0.674 | 7.297 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.919 | 0.626 | 7.853 |
| `vbr1_l1_voltage_gain_amplifier` | `e2e` | `gold` | `classic` | `strict_current` | 4.919 | 1.264 | 3.893 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `ax` | `profile_balanced` | 1.702 | 1.168 | 1.457 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `ax` | `profile_fast` | 1.702 | 0.819 | 2.078 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.702 | 0.691 | 2.463 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.702 | 0.569 | 2.993 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `ax` | `strict_current` | 1.702 | 1.279 | 1.331 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `classic` | `profile_balanced` | 5.603 | 1.168 | 4.796 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `classic` | `profile_fast` | 5.603 | 0.819 | 6.837 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.603 | 0.691 | 8.107 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `classic` | `skip_source_error_control` | 5.603 | 0.569 | 9.849 |
| `vbr1_l1_voltage_gain_amplifier` | `tb` | `gold` | `classic` | `strict_current` | 5.603 | 1.279 | 4.381 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 0.712 | 1.962 | 0.363 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `ax` | `profile_fast` | 0.712 | 1.618 | 0.440 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 0.712 | 1.625 | 0.438 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 0.712 | 1.448 | 0.491 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 0.712 | 4.213 | 0.169 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 3.781 | 1.962 | 1.927 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `classic` | `profile_fast` | 3.781 | 1.618 | 2.336 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 3.781 | 1.625 | 2.326 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 3.781 | 1.448 | 2.610 |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 3.781 | 4.213 | 0.897 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `ax` | `profile_balanced` | 0.768 | 1.977 | 0.388 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `ax` | `profile_fast` | 0.768 | 1.653 | 0.464 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.768 | 1.528 | 0.503 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `ax` | `skip_source_error_control` | 0.768 | 1.445 | 0.531 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `ax` | `strict_current` | 0.768 | 4.108 | 0.187 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `classic` | `profile_balanced` | 3.645 | 1.977 | 1.844 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `classic` | `profile_fast` | 3.645 | 1.653 | 2.205 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.645 | 1.528 | 2.385 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `classic` | `skip_source_error_control` | 3.645 | 1.445 | 2.522 |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `classic` | `strict_current` | 3.645 | 4.108 | 0.887 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `ax` | `profile_balanced` | 0.781 | 1.996 | 0.391 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `ax` | `profile_fast` | 0.781 | 1.740 | 0.449 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.781 | 1.563 | 0.499 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 0.781 | 1.581 | 0.494 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `ax` | `strict_current` | 0.781 | 4.234 | 0.184 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `classic` | `profile_balanced` | 3.792 | 1.996 | 1.900 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `classic` | `profile_fast` | 3.792 | 1.740 | 2.180 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.792 | 1.563 | 2.426 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 3.792 | 1.581 | 2.399 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `classic` | `strict_current` | 3.792 | 4.234 | 0.896 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `ax` | `profile_balanced` | 0.835 | 1.952 | 0.428 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `ax` | `profile_fast` | 0.835 | 1.639 | 0.510 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.835 | 1.443 | 0.579 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `ax` | `skip_source_error_control` | 0.835 | 1.530 | 0.546 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `ax` | `strict_current` | 0.835 | 4.167 | 0.200 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `classic` | `profile_balanced` | 3.848 | 1.952 | 1.972 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `classic` | `profile_fast` | 3.848 | 1.639 | 2.348 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.848 | 1.443 | 2.667 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `classic` | `skip_source_error_control` | 3.848 | 1.530 | 2.515 |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `classic` | `strict_current` | 3.848 | 4.167 | 0.923 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 4.121 | 0.770 | 5.353 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `ax` | `profile_fast` | 4.121 | 0.846 | 4.872 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 4.121 | 0.609 | 6.769 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 4.121 | 0.687 | 6.000 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `ax` | `strict_current` | 4.121 | 0.768 | 5.363 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 5.062 | 0.770 | 6.575 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `classic` | `profile_fast` | 5.062 | 0.846 | 5.985 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 5.062 | 0.609 | 8.315 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 5.062 | 0.687 | 7.370 |
| `vbr1_l1_windowed_dem_pointer` | `bugfix` | `fixed` | `classic` | `strict_current` | 5.062 | 0.768 | 6.588 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `ax` | `profile_balanced` | 3.881 | 0.957 | 4.054 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `ax` | `profile_fast` | 3.881 | 0.810 | 4.794 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 3.881 | 0.716 | 5.419 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `ax` | `skip_source_error_control` | 3.881 | 0.792 | 4.902 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `ax` | `strict_current` | 3.881 | 0.957 | 4.054 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `classic` | `profile_balanced` | 5.214 | 0.957 | 5.446 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `classic` | `profile_fast` | 5.214 | 0.810 | 6.440 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.214 | 0.716 | 7.279 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `classic` | `skip_source_error_control` | 5.214 | 0.792 | 6.585 |
| `vbr1_l1_windowed_dem_pointer` | `dut` | `gold` | `classic` | `strict_current` | 5.214 | 0.957 | 5.446 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.075 | 0.876 | 1.227 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `ax` | `profile_fast` | 1.075 | 0.646 | 1.663 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.075 | 0.665 | 1.615 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.075 | 0.610 | 1.763 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `ax` | `strict_current` | 1.075 | 0.874 | 1.230 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.750 | 0.876 | 5.422 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `classic` | `profile_fast` | 4.750 | 0.646 | 7.352 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.750 | 0.665 | 7.138 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.750 | 0.610 | 7.792 |
| `vbr1_l1_windowed_dem_pointer` | `e2e` | `gold` | `classic` | `strict_current` | 4.750 | 0.874 | 5.437 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `ax` | `profile_balanced` | 1.481 | 0.761 | 1.947 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `ax` | `profile_fast` | 1.481 | 0.652 | 2.271 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.481 | 0.683 | 2.168 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.481 | 0.747 | 1.983 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `ax` | `strict_current` | 1.481 | 0.842 | 1.759 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `classic` | `profile_balanced` | 5.165 | 0.761 | 6.790 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `classic` | `profile_fast` | 5.165 | 0.652 | 7.918 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.165 | 0.683 | 7.560 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `classic` | `skip_source_error_control` | 5.165 | 0.747 | 6.915 |
| `vbr1_l1_windowed_dem_pointer` | `tb` | `gold` | `classic` | `strict_current` | 5.165 | 0.842 | 6.133 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `ax` | `profile_balanced` | 0.857 | 2.762 | 0.310 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `ax` | `profile_fast` | 0.857 | 1.640 | 0.523 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `ax` | `profile_fast_skip_source_error_control` | 0.857 | 1.483 | 0.578 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `ax` | `skip_source_error_control` | 0.857 | 2.768 | 0.310 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `ax` | `strict_current` | 0.857 | 3.042 | 0.282 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `classic` | `profile_balanced` | 4.006 | 2.762 | 1.450 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `classic` | `profile_fast` | 4.006 | 1.640 | 2.443 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `classic` | `profile_fast_skip_source_error_control` | 4.006 | 1.483 | 2.701 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `classic` | `skip_source_error_control` | 4.006 | 2.768 | 1.447 |
| `vbr1_l1_xor_phase_detector` | `bugfix` | `fixed` | `classic` | `strict_current` | 4.006 | 3.042 | 1.317 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `ax` | `profile_balanced` | 1.226 | 2.766 | 0.443 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `ax` | `profile_fast` | 1.226 | 1.724 | 0.711 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.226 | 1.372 | 0.893 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `ax` | `skip_source_error_control` | 1.226 | 2.826 | 0.434 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `ax` | `strict_current` | 1.226 | 2.958 | 0.415 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `classic` | `profile_balanced` | 4.047 | 2.766 | 1.463 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `classic` | `profile_fast` | 4.047 | 1.724 | 2.347 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.047 | 1.372 | 2.949 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `classic` | `skip_source_error_control` | 4.047 | 2.826 | 1.432 |
| `vbr1_l1_xor_phase_detector` | `dut` | `gold` | `classic` | `strict_current` | 4.047 | 2.958 | 1.368 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `ax` | `profile_balanced` | 0.755 | 2.789 | 0.271 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `ax` | `profile_fast` | 0.755 | 1.667 | 0.453 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.755 | 1.346 | 0.561 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 0.755 | 2.834 | 0.266 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `ax` | `strict_current` | 0.755 | 2.997 | 0.252 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `classic` | `profile_balanced` | 3.698 | 2.789 | 1.326 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `classic` | `profile_fast` | 3.698 | 1.667 | 2.218 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.698 | 1.346 | 2.747 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 3.698 | 2.834 | 1.305 |
| `vbr1_l1_xor_phase_detector` | `e2e` | `gold` | `classic` | `strict_current` | 3.698 | 2.997 | 1.234 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `ax` | `profile_balanced` | 1.113 | 2.855 | 0.390 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `ax` | `profile_fast` | 1.113 | 1.667 | 0.668 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.113 | 1.436 | 0.775 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.113 | 2.963 | 0.376 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `ax` | `strict_current` | 1.113 | 3.104 | 0.359 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `classic` | `profile_balanced` | 4.042 | 2.855 | 1.416 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `classic` | `profile_fast` | 4.042 | 1.667 | 2.424 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.042 | 1.436 | 2.814 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.042 | 2.963 | 1.364 |
| `vbr1_l1_xor_phase_detector` | `tb` | `gold` | `classic` | `strict_current` | 4.042 | 3.104 | 1.302 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `ax` | `profile_balanced` | 0.906 | 8.839 | 0.103 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `ax` | `profile_fast` | 0.906 | 2.926 | 0.310 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.906 | 0.985 | 0.920 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 0.906 | 1.244 | 0.729 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `ax` | `strict_current` | 0.906 | 9.002 | 0.101 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `classic` | `profile_balanced` | 5.531 | 8.839 | 0.626 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `classic` | `profile_fast` | 5.531 | 2.926 | 1.890 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.531 | 0.985 | 5.618 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 5.531 | 1.244 | 4.447 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `e2e` | `gold` | `classic` | `strict_current` | 5.531 | 9.002 | 0.614 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `ax` | `profile_balanced` | 1.042 | 8.669 | 0.120 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `ax` | `profile_fast` | 1.042 | 2.967 | 0.351 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.042 | 0.934 | 1.116 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.042 | 1.290 | 0.808 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `ax` | `strict_current` | 1.042 | 8.708 | 0.120 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `classic` | `profile_balanced` | 5.095 | 8.669 | 0.588 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `classic` | `profile_fast` | 5.095 | 2.967 | 1.717 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.095 | 0.934 | 5.456 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `classic` | `skip_source_error_control` | 5.095 | 1.290 | 3.951 |
| `vbr1_l2_adc_dac_reconstruction_chain` | `tb` | `gold` | `classic` | `strict_current` | 5.095 | 8.708 | 0.585 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `ax` | `profile_balanced` | 0.984 | 1.652 | 0.596 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `ax` | `profile_fast` | 0.984 | 0.954 | 1.032 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.984 | 0.597 | 1.649 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 0.984 | 0.652 | 1.510 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `ax` | `strict_current` | 0.984 | 1.621 | 0.607 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.286 | 1.652 | 2.594 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `classic` | `profile_fast` | 4.286 | 0.954 | 4.493 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.286 | 0.597 | 7.180 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.286 | 0.652 | 6.575 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `e2e` | `gold` | `classic` | `strict_current` | 4.286 | 1.621 | 2.644 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `ax` | `profile_balanced` | 1.316 | 1.464 | 0.899 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `ax` | `profile_fast` | 1.316 | 0.926 | 1.421 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.316 | 0.588 | 2.240 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.316 | 0.632 | 2.082 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `ax` | `strict_current` | 1.316 | 1.479 | 0.890 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `classic` | `profile_balanced` | 4.679 | 1.464 | 3.196 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `classic` | `profile_fast` | 4.679 | 0.926 | 5.050 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.679 | 0.588 | 7.961 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.679 | 0.632 | 7.402 |
| `vbr1_l2_adc_dac_source_sweep_flow` | `tb` | `gold` | `classic` | `strict_current` | 4.679 | 1.479 | 3.164 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.431 | 3.316 | 0.432 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `ax` | `profile_fast` | 1.431 | 3.331 | 0.430 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.431 | 3.239 | 0.442 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.431 | 3.151 | 0.454 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `ax` | `strict_current` | 1.431 | 3.368 | 0.425 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.499 | 3.316 | 1.357 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `classic` | `profile_fast` | 4.499 | 3.331 | 1.351 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.499 | 3.239 | 1.389 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.499 | 3.151 | 1.428 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `classic` | `strict_current` | 4.499 | 3.368 | 1.336 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `ax` | `profile_balanced` | 1.247 | 3.310 | 0.377 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `ax` | `profile_fast` | 1.247 | 3.221 | 0.387 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.247 | 3.168 | 0.394 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.247 | 3.160 | 0.394 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `ax` | `strict_current` | 1.247 | 3.464 | 0.360 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `classic` | `profile_balanced` | 4.348 | 3.310 | 1.314 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `classic` | `profile_fast` | 4.348 | 3.221 | 1.350 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.348 | 3.168 | 1.373 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.348 | 3.160 | 1.376 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `classic` | `strict_current` | 4.348 | 3.464 | 1.255 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.550 | 1.265 | 1.225 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `ax` | `profile_fast` | 1.550 | 1.039 | 1.492 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.550 | 0.739 | 2.097 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.550 | 0.885 | 1.751 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `ax` | `strict_current` | 1.550 | 1.202 | 1.289 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `classic` | `profile_balanced` | 5.583 | 1.265 | 4.413 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `classic` | `profile_fast` | 5.583 | 1.039 | 5.376 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.583 | 0.739 | 7.553 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 5.583 | 0.885 | 6.305 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `classic` | `strict_current` | 5.583 | 1.202 | 4.644 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `ax` | `profile_balanced` | 1.077 | 1.071 | 1.005 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `ax` | `profile_fast` | 1.077 | 0.870 | 1.238 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.077 | 0.614 | 1.753 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.077 | 0.554 | 1.943 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `ax` | `strict_current` | 1.077 | 1.320 | 0.816 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `classic` | `profile_balanced` | 4.613 | 1.071 | 4.306 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `classic` | `profile_fast` | 4.613 | 0.870 | 5.304 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.613 | 0.614 | 7.509 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.613 | 0.554 | 8.323 |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `classic` | `strict_current` | 4.613 | 1.320 | 3.495 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.245 | 1.044 | 1.193 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `ax` | `profile_fast` | 1.245 | 0.899 | 1.386 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.245 | 0.774 | 1.609 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.245 | 0.733 | 1.699 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `ax` | `strict_current` | 1.245 | 1.050 | 1.186 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `classic` | `profile_balanced` | 5.251 | 1.044 | 5.030 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `classic` | `profile_fast` | 5.251 | 0.899 | 5.843 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.251 | 0.774 | 6.782 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 5.251 | 0.733 | 7.162 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `classic` | `strict_current` | 5.251 | 1.050 | 5.002 |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `ax` | `profile_balanced` | 1.489 | 0.782 | 1.904 |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `ax` | `profile_fast` | 1.489 | 0.832 | 1.790 |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.489 | 0.799 | 1.865 |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.489 | 0.787 | 1.893 |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `ax` | `strict_current` | 1.489 | 0.807 | 1.846 |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `classic` | `profile_balanced` | 5.356 | 0.782 | 6.845 |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `classic` | `profile_fast` | 5.356 | 0.832 | 6.437 |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.356 | 0.799 | 6.706 |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `classic` | `skip_source_error_control` | 5.356 | 0.787 | 6.808 |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `classic` | `strict_current` | 5.356 | 0.807 | 6.639 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.241 | 1.380 | 0.899 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `ax` | `profile_fast` | 1.241 | 0.872 | 1.423 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.241 | 0.621 | 1.998 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.241 | 0.669 | 1.855 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `ax` | `strict_current` | 1.241 | 1.621 | 0.765 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.512 | 1.380 | 3.269 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `classic` | `profile_fast` | 4.512 | 0.872 | 5.176 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.512 | 0.621 | 7.265 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.512 | 0.669 | 6.748 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `classic` | `strict_current` | 4.512 | 1.621 | 2.784 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `ax` | `profile_balanced` | 1.101 | 1.364 | 0.807 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `ax` | `profile_fast` | 1.101 | 1.007 | 1.094 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.101 | 0.705 | 1.563 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.101 | 0.620 | 1.776 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `ax` | `strict_current` | 1.101 | 1.418 | 0.777 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `classic` | `profile_balanced` | 4.496 | 1.364 | 3.297 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `classic` | `profile_fast` | 4.496 | 1.007 | 4.467 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.496 | 0.705 | 6.381 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.496 | 0.620 | 7.250 |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `classic` | `strict_current` | 4.496 | 1.418 | 3.172 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.485 | 1.354 | 1.097 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `ax` | `profile_fast` | 1.485 | 1.278 | 1.162 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.485 | 1.231 | 1.206 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.485 | 1.068 | 1.391 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `ax` | `strict_current` | 1.485 | 1.444 | 1.028 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `classic` | `profile_balanced` | 5.047 | 1.354 | 3.727 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `classic` | `profile_fast` | 5.047 | 1.278 | 3.950 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.047 | 1.231 | 4.100 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 5.047 | 1.068 | 4.728 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `classic` | `strict_current` | 5.047 | 1.444 | 3.495 |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `ax` | `profile_balanced` | 1.126 | 1.385 | 0.813 |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `ax` | `profile_fast` | 1.126 | 1.287 | 0.875 |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.126 | 1.128 | 0.998 |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.126 | 1.193 | 0.943 |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `ax` | `strict_current` | 1.126 | 1.446 | 0.778 |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `classic` | `profile_balanced` | 5.005 | 1.385 | 3.614 |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `classic` | `profile_fast` | 5.005 | 1.287 | 3.890 |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 5.005 | 1.128 | 4.439 |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `classic` | `skip_source_error_control` | 5.005 | 1.193 | 4.196 |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `classic` | `strict_current` | 5.005 | 1.446 | 3.461 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.562 | 11.561 | 0.135 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `ax` | `profile_fast` | 1.562 | 11.265 | 0.139 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.562 | 11.426 | 0.137 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.562 | 11.510 | 0.136 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `ax` | `strict_current` | 1.562 | 11.654 | 0.134 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `classic` | `profile_balanced` | 7.638 | 11.561 | 0.661 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `classic` | `profile_fast` | 7.638 | 11.265 | 0.678 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 7.638 | 11.426 | 0.668 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 7.638 | 11.510 | 0.664 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `classic` | `strict_current` | 7.638 | 11.654 | 0.655 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `ax` | `profile_balanced` | 1.634 | 11.429 | 0.143 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `ax` | `profile_fast` | 1.634 | 11.563 | 0.141 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.634 | 11.528 | 0.142 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.634 | 11.698 | 0.140 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `ax` | `strict_current` | 1.634 | 12.077 | 0.135 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `classic` | `profile_balanced` | 8.501 | 11.429 | 0.744 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `classic` | `profile_fast` | 8.501 | 11.563 | 0.735 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 8.501 | 11.528 | 0.737 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `classic` | `skip_source_error_control` | 8.501 | 11.698 | 0.727 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `classic` | `strict_current` | 8.501 | 12.077 | 0.704 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `ax` | `profile_balanced` | 0.717 | 1.980 | 0.362 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `ax` | `profile_fast` | 0.717 | 1.614 | 0.444 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.717 | 1.484 | 0.483 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 0.717 | 1.418 | 0.506 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `ax` | `strict_current` | 0.717 | 2.552 | 0.281 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `classic` | `profile_balanced` | 3.759 | 1.980 | 1.898 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `classic` | `profile_fast` | 3.759 | 1.614 | 2.329 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.759 | 1.484 | 2.532 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 3.759 | 1.418 | 2.651 |
| `vbr1_l2_event_controller` | `e2e` | `gold` | `classic` | `strict_current` | 3.759 | 2.552 | 1.473 |
| `vbr1_l2_event_controller` | `tb` | `gold` | `ax` | `profile_balanced` | 1.241 | 1.888 | 0.657 |
| `vbr1_l2_event_controller` | `tb` | `gold` | `ax` | `profile_fast` | 1.241 | 1.646 | 0.754 |
| `vbr1_l2_event_controller` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.241 | 1.345 | 0.922 |
| `vbr1_l2_event_controller` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.241 | 1.650 | 0.752 |
| `vbr1_l2_event_controller` | `tb` | `gold` | `ax` | `strict_current` | 1.241 | 2.412 | 0.514 |
| `vbr1_l2_event_controller` | `tb` | `gold` | `classic` | `profile_balanced` | 4.147 | 1.888 | 2.197 |
| `vbr1_l2_event_controller` | `tb` | `gold` | `classic` | `profile_fast` | 4.147 | 1.646 | 2.519 |
| `vbr1_l2_event_controller` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.147 | 1.345 | 3.083 |
| `vbr1_l2_event_controller` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.147 | 1.650 | 2.513 |
| `vbr1_l2_event_controller` | `tb` | `gold` | `classic` | `strict_current` | 4.147 | 2.412 | 1.719 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `ax` | `profile_balanced` | 0.954 | 1.601 | 0.596 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `ax` | `profile_fast` | 0.954 | 0.912 | 1.045 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.954 | 0.724 | 1.317 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 0.954 | 0.725 | 1.315 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `ax` | `strict_current` | 0.954 | 1.632 | 0.584 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.347 | 1.601 | 2.715 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `classic` | `profile_fast` | 4.347 | 0.912 | 4.764 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.347 | 0.724 | 6.003 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.347 | 0.725 | 5.992 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `classic` | `strict_current` | 4.347 | 1.632 | 2.663 |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `ax` | `profile_balanced` | 1.077 | 1.480 | 0.728 |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `ax` | `profile_fast` | 1.077 | 0.975 | 1.105 |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.077 | 0.774 | 1.392 |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.077 | 0.766 | 1.407 |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `ax` | `strict_current` | 1.077 | 1.602 | 0.673 |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `classic` | `profile_balanced` | 4.797 | 1.480 | 3.241 |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `classic` | `profile_fast` | 4.797 | 0.975 | 4.920 |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.797 | 0.774 | 6.198 |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.797 | 0.766 | 6.266 |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `classic` | `strict_current` | 4.797 | 1.602 | 2.995 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `ax` | `profile_balanced` | 4.305 | 126.930 | 0.034 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `ax` | `profile_fast` | 4.305 | 108.032 | 0.040 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 4.305 | 8.947 | 0.481 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 4.305 | 10.863 | 0.396 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `ax` | `strict_current` | 4.305 | 126.150 | 0.034 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `classic` | `profile_balanced` | 11.788 | 126.930 | 0.093 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `classic` | `profile_fast` | 11.788 | 108.032 | 0.109 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 11.788 | 8.947 | 1.318 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 11.788 | 10.863 | 1.085 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `classic` | `strict_current` | 11.788 | 126.150 | 0.093 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `ax` | `profile_balanced` | 5.743 | 150.482 | 0.038 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `ax` | `profile_fast` | 5.743 | 130.434 | 0.044 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 5.743 | 32.383 | 0.177 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `ax` | `skip_source_error_control` | 5.743 | 34.954 | 0.164 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `ax` | `strict_current` | 5.743 | 150.862 | 0.038 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `classic` | `profile_balanced` | 12.627 | 150.482 | 0.084 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `classic` | `profile_fast` | 12.627 | 130.434 | 0.097 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 12.627 | 32.383 | 0.390 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `classic` | `skip_source_error_control` | 12.627 | 34.954 | 0.361 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `classic` | `strict_current` | 12.627 | 150.862 | 0.084 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.391 | 1.818 | 0.765 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `ax` | `profile_fast` | 1.391 | 1.561 | 0.891 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.391 | 1.386 | 1.004 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.391 | 1.476 | 0.942 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `ax` | `strict_current` | 1.391 | 2.244 | 0.620 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.268 | 1.818 | 2.348 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `classic` | `profile_fast` | 4.268 | 1.561 | 2.734 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.268 | 1.386 | 3.080 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.268 | 1.476 | 2.890 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `classic` | `strict_current` | 4.268 | 2.244 | 1.901 |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `ax` | `profile_balanced` | 0.641 | 1.823 | 0.352 |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `ax` | `profile_fast` | 0.641 | 1.672 | 0.384 |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.641 | 1.400 | 0.458 |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `ax` | `skip_source_error_control` | 0.641 | 1.488 | 0.431 |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `ax` | `strict_current` | 0.641 | 2.309 | 0.278 |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `classic` | `profile_balanced` | 3.741 | 1.823 | 2.052 |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `classic` | `profile_fast` | 3.741 | 1.672 | 2.238 |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 3.741 | 1.400 | 2.672 |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `classic` | `skip_source_error_control` | 3.741 | 1.488 | 2.513 |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `classic` | `strict_current` | 3.741 | 2.309 | 1.620 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.104 | 10.760 | 0.103 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `ax` | `profile_fast` | 1.104 | 10.591 | 0.104 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.104 | 9.768 | 0.113 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.104 | 10.193 | 0.108 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `ax` | `strict_current` | 1.104 | 10.757 | 0.103 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.351 | 10.760 | 0.404 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `classic` | `profile_fast` | 4.351 | 10.591 | 0.411 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.351 | 9.768 | 0.445 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.351 | 10.193 | 0.427 |
| `vbr1_l2_pll_timing_slice` | `e2e` | `gold` | `classic` | `strict_current` | 4.351 | 10.757 | 0.404 |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `ax` | `profile_balanced` | 1.391 | 10.425 | 0.133 |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `ax` | `profile_fast` | 1.391 | 10.067 | 0.138 |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.391 | 9.432 | 0.147 |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.391 | 9.880 | 0.141 |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `ax` | `strict_current` | 1.391 | 10.290 | 0.135 |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `classic` | `profile_balanced` | 4.451 | 10.425 | 0.427 |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `classic` | `profile_fast` | 4.451 | 10.067 | 0.442 |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.451 | 9.432 | 0.472 |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.451 | 9.880 | 0.450 |
| `vbr1_l2_pll_timing_slice` | `tb` | `gold` | `classic` | `strict_current` | 4.451 | 10.290 | 0.433 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `ax` | `profile_balanced` | 0.946 | 2.019 | 0.469 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `ax` | `profile_fast` | 0.946 | 1.189 | 0.796 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.946 | 1.011 | 0.936 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 0.946 | 1.015 | 0.932 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `ax` | `strict_current` | 0.946 | 2.103 | 0.450 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `classic` | `profile_balanced` | 4.176 | 2.019 | 2.068 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `classic` | `profile_fast` | 4.176 | 1.189 | 3.512 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.176 | 1.011 | 4.130 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 4.176 | 1.015 | 4.114 |
| `vbr1_l2_serializer_frame_alignment_flow` | `e2e` | `gold` | `classic` | `strict_current` | 4.176 | 2.103 | 1.986 |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `ax` | `profile_balanced` | 0.890 | 1.948 | 0.457 |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `ax` | `profile_fast` | 0.890 | 1.297 | 0.686 |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 0.890 | 0.882 | 1.009 |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `ax` | `skip_source_error_control` | 0.890 | 0.986 | 0.903 |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `ax` | `strict_current` | 0.890 | 2.047 | 0.435 |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `classic` | `profile_balanced` | 4.599 | 1.948 | 2.361 |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `classic` | `profile_fast` | 4.599 | 1.297 | 3.547 |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 4.599 | 0.882 | 5.216 |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `classic` | `skip_source_error_control` | 4.599 | 0.986 | 4.665 |
| `vbr1_l2_serializer_frame_alignment_flow` | `tb` | `gold` | `classic` | `strict_current` | 4.599 | 2.047 | 2.246 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `ax` | `profile_balanced` | 1.183 | 15.724 | 0.075 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `ax` | `profile_fast` | 1.183 | 7.865 | 0.150 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.183 | 1.006 | 1.176 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `ax` | `skip_source_error_control` | 1.183 | 1.031 | 1.147 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `ax` | `strict_current` | 1.183 | 16.093 | 0.073 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `classic` | `profile_balanced` | 8.683 | 15.724 | 0.552 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `classic` | `profile_fast` | 8.683 | 7.865 | 1.104 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 8.683 | 1.006 | 8.633 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `classic` | `skip_source_error_control` | 8.683 | 1.031 | 8.422 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `classic` | `strict_current` | 8.683 | 16.093 | 0.540 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `ax` | `profile_balanced` | 1.212 | 17.479 | 0.069 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `ax` | `profile_fast` | 1.212 | 8.913 | 0.136 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `ax` | `profile_fast_skip_source_error_control` | 1.212 | 2.470 | 0.491 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `ax` | `skip_source_error_control` | 1.212 | 2.359 | 0.514 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `ax` | `strict_current` | 1.212 | 17.465 | 0.069 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `classic` | `profile_balanced` | 7.767 | 17.479 | 0.444 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `classic` | `profile_fast` | 7.767 | 8.913 | 0.871 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `classic` | `profile_fast_skip_source_error_control` | 7.767 | 2.470 | 3.145 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `classic` | `skip_source_error_control` | 7.767 | 2.359 | 3.292 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `classic` | `strict_current` | 7.767 | 17.465 | 0.445 |

## Interpretation Guardrails

- Speedups use `simulation_ok`, so rows without a behavior checker can still contribute timing if the simulator produced waveforms.
- Accuracy-gated speedups require candidate behavior pass, strict-EVAS parity, and parity to every selected Spectre mode.
- `spectre/ax` matches the previous bridge default but Spectre X may ignore `errpreset` and `maxstep` from the testbench.
- `spectre/classic` is available to measure the stricter non-X path when requested.
- Cold Spectre runs include AHDL CMI compilation; warm-cache repetitions should be reported separately.
- A `BLOCKED` gate is not evidence of wrong behavior; it means the checker or reference evidence is incomplete.
