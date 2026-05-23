# vaBench Same-Server Speed Goal Summary

- Generated: 2026-05-22T16:45:49
- Reports: 1
  - `same_server_speed_ablation_full_goal_20260522`: rows=259 jobs=8 path=`benchmark-vabench-release-v1/reports/same_server_speed_ablation_full_goal_20260522.json`

## Combined Wall-Time Geomean By Mode

| Backend | Mode | Reports | PASS/Runs | Geomean s | Mean s | CV |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| evas | `profile_balanced` | 1 | 259/259 | 1.591 | 1.591 | 0.000 |
| evas | `profile_fast` | 1 | 259/259 | 1.223 | 1.223 | 0.000 |
| evas | `profile_fast_skip_source_error_control` | 1 | 259/259 | 0.968 | 0.968 | 0.000 |
| evas | `skip_source_error_control` | 1 | 258/259 | 1.043 | 1.043 | 0.000 |
| evas | `strict_current` | 1 | 259/259 | 1.770 | 1.770 | 0.000 |
| spectre | `ax` | 1 | 258/259 | 1.284 | 1.284 | 0.000 |
| spectre | `classic` | 1 | 259/259 | 4.323 | 4.323 | 0.000 |

## Combined Accuracy-Gated Speedups

| Spectre | EVAS | N | Geomean x | Mean x | Median x | P10 x | P90 x | Min x | Max x |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `ax` | `profile_balanced` | 258 | 0.804 | 1.259 | 1.003 | 0.166 | 2.556 | 0.027 | 6.260 |
| `ax` | `profile_fast` | 258 | 1.047 | 1.489 | 1.279 | 0.330 | 2.961 | 0.035 | 6.957 |
| `ax` | `profile_fast_skip_source_error_control` | 258 | 1.324 | 1.722 | 1.551 | 0.498 | 2.993 | 0.039 | 6.769 |
| `ax` | `skip_source_error_control` | 257 | 1.227 | 1.660 | 1.534 | 0.430 | 2.894 | 0.025 | 6.961 |
| `ax` | `strict_current` | 258 | 0.723 | 1.184 | 0.943 | 0.151 | 2.508 | 0.011 | 5.919 |
| `classic` | `profile_balanced` | 258 | 2.713 | 3.617 | 3.257 | 0.839 | 6.738 | 0.077 | 9.444 |
| `classic` | `profile_fast` | 258 | 3.531 | 4.402 | 4.478 | 1.719 | 7.307 | 0.088 | 10.70 |
| `classic` | `profile_fast_skip_source_error_control` | 258 | 4.465 | 5.319 | 5.281 | 2.692 | 8.299 | 0.253 | 15.73 |
| `classic` | `skip_source_error_control` | 257 | 4.141 | 5.115 | 5.155 | 1.695 | 8.133 | 0.162 | 12.60 |
| `classic` | `strict_current` | 258 | 2.440 | 3.376 | 3.078 | 0.729 | 6.383 | 0.057 | 9.556 |

## Per-Repeat Accuracy-Gated Speedups

| Report | Spectre | EVAS | N | Geomean x | Median x | P10 x | P90 x |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| `same_server_speed_ablation_full_goal_20260522` | `ax` | `profile_balanced` | 258 | 0.804 | 1.003 | 0.166 | 2.556 |
| `same_server_speed_ablation_full_goal_20260522` | `ax` | `profile_fast` | 258 | 1.047 | 1.279 | 0.330 | 2.961 |
| `same_server_speed_ablation_full_goal_20260522` | `ax` | `profile_fast_skip_source_error_control` | 258 | 1.324 | 1.551 | 0.498 | 2.993 |
| `same_server_speed_ablation_full_goal_20260522` | `ax` | `skip_source_error_control` | 257 | 1.227 | 1.534 | 0.430 | 2.894 |
| `same_server_speed_ablation_full_goal_20260522` | `ax` | `strict_current` | 258 | 0.723 | 0.943 | 0.151 | 2.508 |
| `same_server_speed_ablation_full_goal_20260522` | `classic` | `profile_balanced` | 258 | 2.713 | 3.257 | 0.839 | 6.738 |
| `same_server_speed_ablation_full_goal_20260522` | `classic` | `profile_fast` | 258 | 3.531 | 4.478 | 1.719 | 7.307 |
| `same_server_speed_ablation_full_goal_20260522` | `classic` | `profile_fast_skip_source_error_control` | 258 | 4.465 | 5.281 | 2.692 | 8.299 |
| `same_server_speed_ablation_full_goal_20260522` | `classic` | `skip_source_error_control` | 257 | 4.141 | 5.155 | 1.695 | 8.133 |
| `same_server_speed_ablation_full_goal_20260522` | `classic` | `strict_current` | 258 | 2.440 | 3.078 | 0.729 | 6.383 |

## Raw Speedups

| Spectre | EVAS | N | Geomean x | Mean x | Median x |
| --- | --- | ---: | ---: | ---: | ---: |
| `ax` | `profile_balanced` | 259 | 0.807 | 1.261 | 1.005 |
| `ax` | `profile_fast` | 259 | 1.049 | 1.490 | 1.281 |
| `ax` | `profile_fast_skip_source_error_control` | 259 | 1.326 | 1.723 | 1.551 |
| `ax` | `skip_source_error_control` | 259 | 1.231 | 1.661 | 1.534 |
| `ax` | `strict_current` | 259 | 0.725 | 1.185 | 0.944 |
| `classic` | `profile_balanced` | 259 | 2.717 | 3.619 | 3.269 |
| `classic` | `profile_fast` | 259 | 3.534 | 4.402 | 4.467 |
| `classic` | `profile_fast_skip_source_error_control` | 259 | 4.466 | 5.317 | 5.257 |
| `classic` | `skip_source_error_control` | 259 | 4.145 | 5.111 | 5.131 |
| `classic` | `strict_current` | 259 | 2.443 | 3.375 | 3.098 |

## EVAS Fast-Skip Versus Strict

Across paired EVAS rows, `strict_current_wall / profile_fast_skip_source_error_control_wall` has geomean 1.828x, median 1.547x, n=259.

## Waveform Tolerance Sweep

This sweep reuses saved waveform parity metrics for `profile_fast_skip_source_error_control`; task-specific semantic comparators are counted as non-waveform rows and are not threshold-scanned.

| Target | Waveform Rows | Non-Waveform Rows | Current PASS | P95<=0.05 Max<=0.10 | P95<=0.10 Max<=0.15 | P95<=0.14 Max<=0.22 | P95<=0.20 Max<=0.30 | Worst P95 | Worst Max | Worst Abs V |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `spectre_ax` | 250 | 9 | 250 | 242 | 246 | 250 | 250 | 0.128 | 0.128 | 1.000 |
| `spectre_classic` | 251 | 8 | 251 | 244 | 244 | 251 | 251 | 0.130 | 0.130 | 1.000 |
| `strict_evas` | 251 | 8 | 251 | 247 | 251 | 251 | 251 | 0.051 | 0.051 | 0.934 |

## Non-PASS Rows

| Report | Entry | Form | Backend | Mode | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `same_server_speed_ablation_full_goal_20260522` | `vbr1_l1_peak_detector` | `e2e` | spectre | `ax` | PASS | behavior_eval_timeout>60s |
| `same_server_speed_ablation_full_goal_20260522` | `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | evas | `skip_source_error_control` | FAIL_SIM_CORRECTNESS | returncode=0; behavior_eval_timeout>60s |

## Outliers

### Smallest Spectre-AX / Fast-Skip Speedups

| Report | Entry | Form | Task | Value |
| --- | --- | --- | --- | ---: |
| `same_server_speed_ablation_full_goal_20260522` | `vbr1_l1_pfd_small_phase_error_response` | `dut` | `vbm1_pfd_small_phase_error_response_dut` | 0.039 |
| `same_server_speed_ablation_full_goal_20260522` | `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `pfd_small_phase_response_smoke` | 0.049 |
| `same_server_speed_ablation_full_goal_20260522` | `vbr1_l1_pfd_small_phase_error_response` | `tb` | `vbr1_l1_pfd_small_phase_error_response_tb` | 0.050 |
| `same_server_speed_ablation_full_goal_20260522` | `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `vbr1_l1_pfd_small_phase_error_response_bugfix` | 0.057 |
| `same_server_speed_ablation_full_goal_20260522` | `vbr1_l1_pfd_up_dn_logic` | `e2e` | `vbm1_pfd_reset_race_e2e` | 0.087 |
| `same_server_speed_ablation_full_goal_20260522` | `vbr1_l1_pfd_up_dn_logic` | `dut` | `vbm1_pfd_reset_race_dut` | 0.102 |
| `same_server_speed_ablation_full_goal_20260522` | `vbr1_l2_pll_timing_slice` | `e2e` | `cppll_tracking_smoke` | 0.113 |
| `same_server_speed_ablation_full_goal_20260522` | `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `cppll_freq_step_reacquire_smoke` | 0.137 |
| `same_server_speed_ablation_full_goal_20260522` | `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow_tb` | 0.142 |
| `same_server_speed_ablation_full_goal_20260522` | `vbr1_l1_gain_estimator` | `tb` | `vbr1_l1_gain_estimator_tb` | 0.146 |

### Largest Spectre-AX / Fast-Skip Speedups

| Report | Entry | Form | Task | Value |
| --- | --- | --- | --- | ---: |
| `same_server_speed_ablation_full_goal_20260522` | `vbr1_l1_windowed_dem_pointer` | `bugfix` | `vbm1_barrel_pointer_window_bugfix` | 6.769 |
| `same_server_speed_ablation_full_goal_20260522` | `vbr1_l1_edge_detector` | `dut` | `vbm1_edge_detector_dut` | 6.445 |
| `same_server_speed_ablation_full_goal_20260522` | `vbr1_l1_thermometer_code_decoder` | `tb` | `vbm1_thermometer_decoder_guarded_tb` | 6.272 |
| `same_server_speed_ablation_full_goal_20260522` | `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `vbm1_simple_binary_voltage_dac_4b_dut` | 6.108 |
| `same_server_speed_ablation_full_goal_20260522` | `vbr1_l1_debounce_latch` | `bugfix` | `vbm1_debounce_latch_bugfix` | 6.056 |
| `same_server_speed_ablation_full_goal_20260522` | `vbr1_l1_edge_detector` | `tb` | `vbm1_edge_detector_tb` | 5.871 |
| `same_server_speed_ablation_full_goal_20260522` | `vbr1_l1_lock_detector` | `e2e` | `vbm1_lock_detector_e2e` | 5.562 |
| `same_server_speed_ablation_full_goal_20260522` | `vbr1_l1_windowed_dem_pointer` | `dut` | `vbm1_barrel_pointer_window_dut` | 5.419 |
| `same_server_speed_ablation_full_goal_20260522` | `vbr1_l1_segmented_dac` | `bugfix` | `vbm1_segmented_dac_bugfix` | 5.315 |
| `same_server_speed_ablation_full_goal_20260522` | `vbr1_l1_edge_detector` | `bugfix` | `vbm1_edge_detector_bugfix` | 5.166 |

### Slowest Fast-Skip Cases

| Report | Entry | Form | Task | Value |
| --- | --- | --- | --- | ---: |
| `same_server_speed_ablation_full_goal_20260522` | `vbr1_l1_gain_estimator` | `tb` | `vbr1_l1_gain_estimator_tb` | 32.72 |
| `same_server_speed_ablation_full_goal_20260522` | `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `vbr1_l2_gain_extraction_convergence_measurement_flow_tb` | 32.38 |
| `same_server_speed_ablation_full_goal_20260522` | `vbr1_l1_pfd_small_phase_error_response` | `tb` | `vbr1_l1_pfd_small_phase_error_response_tb` | 15.87 |
| `same_server_speed_ablation_full_goal_20260522` | `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `vbr1_l1_pfd_small_phase_error_response_bugfix` | 15.79 |
| `same_server_speed_ablation_full_goal_20260522` | `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `pfd_small_phase_response_smoke` | 15.75 |
| `same_server_speed_ablation_full_goal_20260522` | `vbr1_l1_pfd_small_phase_error_response` | `dut` | `vbm1_pfd_small_phase_error_response_dut` | 15.60 |
| `same_server_speed_ablation_full_goal_20260522` | `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow_tb` | 11.53 |
| `same_server_speed_ablation_full_goal_20260522` | `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `cppll_freq_step_reacquire_smoke` | 11.43 |
| `same_server_speed_ablation_full_goal_20260522` | `vbr1_l1_gain_estimator` | `e2e` | `gain_extraction_smoke` | 11.31 |
| `same_server_speed_ablation_full_goal_20260522` | `vbr1_l2_pll_timing_slice` | `e2e` | `cppll_tracking_smoke` | 9.768 |
