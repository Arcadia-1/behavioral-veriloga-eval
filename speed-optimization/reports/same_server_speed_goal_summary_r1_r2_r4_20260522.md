# vaBench Same-Server Speed Goal Summary

- Generated: 2026-05-22T17:03:39
- Reports: 3
  - `same_server_speed_cold_r1_goal_20260522`: rows=259 jobs=8 path=`benchmark-vabench-release-v1/reports/same_server_speed_cold_r1_goal_20260522.json`
  - `same_server_speed_repeat_r2_goal_20260522`: rows=259 jobs=8 path=`benchmark-vabench-release-v1/reports/same_server_speed_repeat_r2_goal_20260522.json`
  - `same_server_speed_repeat_r4_goal_20260522`: rows=259 jobs=8 path=`benchmark-vabench-release-v1/reports/same_server_speed_repeat_r4_goal_20260522.json`

## Combined Wall-Time Geomean By Mode

| Backend | Mode | Reports | PASS/Runs | Geomean s | Mean s | CV |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| evas | `profile_fast_skip_source_error_control` | 3 | 777/777 | 1.159 | 1.165 | 0.121 |
| evas | `strict_current` | 3 | 777/777 | 1.891 | 1.896 | 0.086 |
| spectre | `ax` | 3 | 777/777 | 7.457 | 7.459 | 0.027 |
| spectre | `classic` | 3 | 777/777 | 23.22 | 23.22 | 0.025 |

## Combined Accuracy-Gated Speedups

| Spectre | EVAS | N | Geomean x | Mean x | Median x | P10 x | P90 x | Min x | Max x |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `ax` | `profile_fast_skip_source_error_control` | 777 | 6.435 | 8.536 | 7.318 | 3.127 | 15.47 | 0.045 | 37.44 |
| `ax` | `strict_current` | 777 | 3.943 | 6.242 | 5.177 | 0.828 | 13.26 | 0.039 | 31.46 |
| `classic` | `profile_fast_skip_source_error_control` | 777 | 20.04 | 25.05 | 24.47 | 11.94 | 45.04 | 0.174 | 86.96 |
| `classic` | `strict_current` | 777 | 12.28 | 17.23 | 15.80 | 4.498 | 30.63 | 0.144 | 57.38 |

## Per-Repeat Accuracy-Gated Speedups

| Report | Spectre | EVAS | N | Geomean x | Median x | P10 x | P90 x |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| `same_server_speed_cold_r1_goal_20260522` | `ax` | `profile_fast_skip_source_error_control` | 259 | 5.928 | 6.820 | 3.324 | 13.29 |
| `same_server_speed_cold_r1_goal_20260522` | `ax` | `strict_current` | 259 | 3.714 | 4.834 | 1.071 | 11.10 |
| `same_server_speed_cold_r1_goal_20260522` | `classic` | `profile_fast_skip_source_error_control` | 259 | 18.38 | 21.26 | 12.16 | 31.66 |
| `same_server_speed_cold_r1_goal_20260522` | `classic` | `strict_current` | 259 | 11.52 | 15.01 | 4.815 | 26.09 |
| `same_server_speed_repeat_r2_goal_20260522` | `ax` | `profile_fast_skip_source_error_control` | 259 | 5.860 | 6.883 | 3.312 | 13.35 |
| `same_server_speed_repeat_r2_goal_20260522` | `ax` | `strict_current` | 259 | 3.670 | 4.681 | 1.125 | 10.75 |
| `same_server_speed_repeat_r2_goal_20260522` | `classic` | `profile_fast_skip_source_error_control` | 259 | 18.34 | 21.55 | 11.95 | 31.68 |
| `same_server_speed_repeat_r2_goal_20260522` | `classic` | `strict_current` | 259 | 11.48 | 14.66 | 4.738 | 27.05 |
| `same_server_speed_repeat_r4_goal_20260522` | `ax` | `profile_fast_skip_source_error_control` | 259 | 7.670 | 10.71 | 2.879 | 19.65 |
| `same_server_speed_repeat_r4_goal_20260522` | `ax` | `strict_current` | 259 | 4.499 | 6.448 | 0.781 | 14.94 |
| `same_server_speed_repeat_r4_goal_20260522` | `classic` | `profile_fast_skip_source_error_control` | 259 | 23.85 | 32.46 | 10.15 | 52.60 |
| `same_server_speed_repeat_r4_goal_20260522` | `classic` | `strict_current` | 259 | 13.99 | 19.57 | 4.377 | 43.49 |

## Raw Speedups

| Spectre | EVAS | N | Geomean x | Mean x | Median x |
| --- | --- | ---: | ---: | ---: | ---: |
| `ax` | `profile_fast_skip_source_error_control` | 777 | 6.435 | 8.536 | 7.318 |
| `ax` | `strict_current` | 777 | 3.943 | 6.242 | 5.177 |
| `classic` | `profile_fast_skip_source_error_control` | 777 | 20.04 | 25.05 | 24.47 |
| `classic` | `strict_current` | 777 | 12.28 | 17.23 | 15.80 |

## EVAS Fast-Skip Versus Strict

Across paired EVAS rows, `strict_current_wall / profile_fast_skip_source_error_control_wall` has geomean 1.632x, median 1.404x, n=777.

## Waveform Tolerance Sweep

This sweep reuses saved waveform parity metrics for `profile_fast_skip_source_error_control`; task-specific semantic comparators are counted as non-waveform rows and are not threshold-scanned.

| Target | Waveform Rows | Non-Waveform Rows | Current PASS | P95<=0.05 Max<=0.10 | P95<=0.10 Max<=0.15 | P95<=0.14 Max<=0.22 | P95<=0.20 Max<=0.30 | Worst P95 | Worst Max | Worst Abs V |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `spectre_ax` | 753 | 24 | 753 | 729 | 741 | 753 | 753 | 0.128 | 0.128 | 1.000 |
| `spectre_classic` | 753 | 24 | 753 | 732 | 732 | 753 | 753 | 0.130 | 0.130 | 1.000 |
| `strict_evas` | 753 | 24 | 753 | 741 | 753 | 753 | 753 | 0.051 | 0.051 | 0.934 |

## Non-PASS Rows

No non-PASS rows in the included reports.

## Outliers

### Smallest Spectre-AX / Fast-Skip Speedups

| Report | Entry | Form | Task | Value | EVAS s | Spectre s | EVAS steps | Spectre steps |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| `same_server_speed_repeat_r4_goal_20260522` | `vbr1_l1_pfd_small_phase_error_response` | `tb` | `vbr1_l1_pfd_small_phase_error_response_tb` | 0.045 | 98.87 | 4.437 | 60058 | 435 |
| `same_server_speed_repeat_r4_goal_20260522` | `vbr1_l1_pfd_small_phase_error_response` | `dut` | `vbm1_pfd_small_phase_error_response_dut` | 0.046 | 102.6 | 4.751 | 60058 | 435 |
| `same_server_speed_repeat_r4_goal_20260522` | `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `pfd_small_phase_response_smoke` | 0.051 | 97.91 | 5.042 | 60058 | 435 |
| `same_server_speed_repeat_r4_goal_20260522` | `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `vbr1_l1_pfd_small_phase_error_response_bugfix` | 0.055 | 93.99 | 5.165 | 60058 | 435 |
| `same_server_speed_repeat_r4_goal_20260522` | `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow_tb` | 0.096 | 66.78 | 6.412 | 41900 | 34050 |
| `same_server_speed_repeat_r4_goal_20260522` | `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `cppll_freq_step_reacquire_smoke` | 0.097 | 71.77 | 6.964 | 41900 | 34050 |
| `same_server_speed_repeat_r4_goal_20260522` | `vbr1_l2_pll_timing_slice` | `tb` | `vbr1_l2_pll_timing_slice_tb` | 0.107 | 50.41 | 5.414 | 35275 | 28069 |
| `same_server_speed_repeat_r4_goal_20260522` | `vbr1_l2_pll_timing_slice` | `e2e` | `cppll_tracking_smoke` | 0.134 | 41.95 | 5.601 | 35275 | 28069 |
| `same_server_speed_repeat_r4_goal_20260522` | `vbr1_l1_pfd_up_dn_logic` | `dut` | `vbm1_pfd_reset_race_dut` | 0.227 | 19.72 | 4.469 | 30058 | 453 |
| `same_server_speed_cold_r1_goal_20260522` | `vbr1_l1_gain_estimator` | `tb` | `vbr1_l1_gain_estimator_tb` | 0.259 | 38.79 | 10.05 | 110493 | 150146 |

### Largest Spectre-AX / Fast-Skip Speedups

| Report | Entry | Form | Task | Value | EVAS s | Spectre s | EVAS steps | Spectre steps |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| `same_server_speed_repeat_r4_goal_20260522` | `vbr1_l1_thermometer_code_decoder` | `bugfix` | `vbm1_thermometer_decoder_guarded_bugfix` | 37.44 | 0.515 | 19.30 | 253 | 105 |
| `same_server_speed_repeat_r4_goal_20260522` | `vbr1_l1_debounce_latch` | `tb` | `vbm1_debounce_latch_tb` | 34.69 | 0.488 | 16.92 | 283 | 113 |
| `same_server_speed_repeat_r4_goal_20260522` | `vbr1_l1_edge_detector` | `tb` | `vbm1_edge_detector_tb` | 34.36 | 0.556 | 19.09 | 413 | 129 |
| `same_server_speed_repeat_r4_goal_20260522` | `vbr1_l1_windowed_dem_pointer` | `dut` | `vbm1_barrel_pointer_window_dut` | 33.85 | 0.530 | 17.93 | 316 | 128 |
| `same_server_speed_repeat_r4_goal_20260522` | `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `vbm1_simple_binary_voltage_dac_4b_e2e` | 33.81 | 0.548 | 18.52 | 351 | 156 |
| `same_server_speed_repeat_r4_goal_20260522` | `vbr1_l1_debounce_latch` | `bugfix` | `vbm1_debounce_latch_bugfix` | 33.72 | 0.550 | 18.53 | 283 | 113 |
| `same_server_speed_repeat_r4_goal_20260522` | `vbr1_l1_thermometer_code_decoder` | `tb` | `vbm1_thermometer_decoder_guarded_tb` | 32.50 | 0.620 | 20.16 | 253 | 105 |
| `same_server_speed_repeat_r4_goal_20260522` | `vbr1_l1_lock_detector` | `e2e` | `vbm1_lock_detector_e2e` | 31.78 | 0.576 | 18.31 | 480 | 250 |
| `same_server_speed_repeat_r4_goal_20260522` | `vbr1_l1_segmented_dac` | `e2e` | `vbm1_segmented_dac_e2e` | 31.63 | 0.579 | 18.32 | 312 | 103 |
| `same_server_speed_repeat_r4_goal_20260522` | `vbr1_l1_windowed_dem_pointer` | `bugfix` | `vbm1_barrel_pointer_window_bugfix` | 30.92 | 0.551 | 17.03 | 316 | 128 |

### Slowest Fast-Skip Cases

| Report | Entry | Form | Task | Value | EVAS s | Spectre s | EVAS steps | Spectre steps |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| `same_server_speed_repeat_r4_goal_20260522` | `vbr1_l1_pfd_small_phase_error_response` | `dut` | `vbm1_pfd_small_phase_error_response_dut` | 102.6 | 102.6 | - | 60058 | - |
| `same_server_speed_repeat_r4_goal_20260522` | `vbr1_l1_pfd_small_phase_error_response` | `tb` | `vbr1_l1_pfd_small_phase_error_response_tb` | 98.87 | 98.87 | - | 60058 | - |
| `same_server_speed_repeat_r4_goal_20260522` | `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `pfd_small_phase_response_smoke` | 97.91 | 97.91 | - | 60058 | - |
| `same_server_speed_repeat_r4_goal_20260522` | `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `vbr1_l1_pfd_small_phase_error_response_bugfix` | 93.99 | 93.99 | - | 60058 | - |
| `same_server_speed_repeat_r4_goal_20260522` | `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `cppll_freq_step_reacquire_smoke` | 71.77 | 71.77 | - | 41900 | - |
| `same_server_speed_repeat_r4_goal_20260522` | `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow_tb` | 66.78 | 66.78 | - | 41900 | - |
| `same_server_speed_repeat_r4_goal_20260522` | `vbr1_l2_pll_timing_slice` | `tb` | `vbr1_l2_pll_timing_slice_tb` | 50.41 | 50.41 | - | 35275 | - |
| `same_server_speed_repeat_r4_goal_20260522` | `vbr1_l2_pll_timing_slice` | `e2e` | `cppll_tracking_smoke` | 41.95 | 41.95 | - | 35275 | - |
| `same_server_speed_cold_r1_goal_20260522` | `vbr1_l1_gain_estimator` | `tb` | `vbr1_l1_gain_estimator_tb` | 38.79 | 38.79 | - | 110493 | - |
| `same_server_speed_repeat_r4_goal_20260522` | `vbr1_l1_gain_estimator` | `tb` | `vbr1_l1_gain_estimator_tb` | 33.69 | 33.69 | - | 110493 | - |
