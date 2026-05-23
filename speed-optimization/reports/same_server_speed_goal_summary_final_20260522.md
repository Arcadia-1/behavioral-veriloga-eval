# vaBench Same-Server Speed Goal Summary

- Generated: 2026-05-22T18:29:08
- Reports: 4
  - `same_server_speed_cold_r1_goal_20260522`: rows=259 jobs=8 path=`benchmark-vabench-release-v1/reports/same_server_speed_cold_r1_goal_20260522.json`
  - `same_server_speed_repeat_r2_goal_20260522`: rows=259 jobs=8 path=`benchmark-vabench-release-v1/reports/same_server_speed_repeat_r2_goal_20260522.json`
  - `same_server_speed_repeat_r4_goal_20260522`: rows=259 jobs=8 path=`benchmark-vabench-release-v1/reports/same_server_speed_repeat_r4_goal_20260522.json`
  - `same_server_speed_repeat_r5_goal_20260522`: rows=259 jobs=8 path=`benchmark-vabench-release-v1/reports/same_server_speed_repeat_r5_goal_20260522.json`

## Combined Wall-Time Geomean By Mode

| Backend | Mode | Reports | PASS/Runs | Geomean s | Mean s | CV |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| evas | `profile_fast_skip_source_error_control` | 4 | 1036/1036 | 1.150 | 1.155 | 0.101 |
| evas | `strict_current` | 4 | 1036/1036 | 1.871 | 1.875 | 0.074 |
| spectre | `ax` | 4 | 1036/1036 | 8.001 | 8.065 | 0.152 |
| spectre | `classic` | 4 | 1036/1036 | 24.88 | 25.07 | 0.148 |

## Combined Accuracy-Gated Speedups

| Spectre | EVAS | N | Geomean x | Mean x | Median x | P10 x | P90 x | Min x | Max x |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `ax` | `profile_fast_skip_source_error_control` | 1036 | 6.958 | 9.465 | 7.803 | 3.225 | 16.81 | 0.041 | 48.24 |
| `ax` | `strict_current` | 1036 | 4.276 | 6.960 | 5.632 | 1.177 | 14.46 | 0.029 | 41.44 |
| `classic` | `profile_fast_skip_source_error_control` | 1036 | 21.63 | 27.82 | 26.07 | 12.09 | 50.66 | 0.172 | 104.4 |
| `classic` | `strict_current` | 1036 | 13.29 | 19.22 | 17.10 | 4.656 | 37.91 | 0.096 | 67.45 |

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
| `same_server_speed_repeat_r5_goal_20260522` | `ax` | `profile_fast_skip_source_error_control` | 259 | 8.795 | 11.45 | 3.774 | 21.26 |
| `same_server_speed_repeat_r5_goal_20260522` | `ax` | `strict_current` | 259 | 5.453 | 7.352 | 1.808 | 17.34 |
| `same_server_speed_repeat_r5_goal_20260522` | `classic` | `profile_fast_skip_source_error_control` | 259 | 27.22 | 33.91 | 13.84 | 61.25 |
| `same_server_speed_repeat_r5_goal_20260522` | `classic` | `strict_current` | 259 | 16.88 | 23.01 | 6.887 | 48.73 |

## Raw Speedups

| Spectre | EVAS | N | Geomean x | Mean x | Median x |
| --- | --- | ---: | ---: | ---: | ---: |
| `ax` | `profile_fast_skip_source_error_control` | 1036 | 6.958 | 9.465 | 7.803 |
| `ax` | `strict_current` | 1036 | 4.276 | 6.960 | 5.632 |
| `classic` | `profile_fast_skip_source_error_control` | 1036 | 21.63 | 27.82 | 26.07 |
| `classic` | `strict_current` | 1036 | 13.29 | 19.22 | 17.10 |

## EVAS Fast-Skip Versus Strict

Across paired EVAS rows, `strict_current_wall / profile_fast_skip_source_error_control_wall` has geomean 1.627x, median 1.405x, n=1036.

## Waveform Tolerance Sweep

This sweep reuses saved waveform parity metrics for `profile_fast_skip_source_error_control`; task-specific semantic comparators are counted as non-waveform rows and are not threshold-scanned.

| Target | Waveform Rows | Non-Waveform Rows | Current PASS | P95<=0.05 Max<=0.10 | P95<=0.10 Max<=0.15 | P95<=0.14 Max<=0.22 | P95<=0.20 Max<=0.30 | Worst P95 | Worst Max | Worst Abs V |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `spectre_ax` | 1004 | 32 | 1004 | 972 | 988 | 1004 | 1004 | 0.128 | 0.128 | 1.000 |
| `spectre_classic` | 1004 | 32 | 1004 | 976 | 976 | 1004 | 1004 | 0.130 | 0.130 | 1.000 |
| `strict_evas` | 1004 | 32 | 1004 | 988 | 1004 | 1004 | 1004 | 0.051 | 0.051 | 0.934 |

## Non-PASS Rows

No non-PASS rows in the included reports.

## Outliers

### Smallest Spectre-AX / Fast-Skip Speedups

| Report | Entry | Form | Task | Value | EVAS s | Spectre s | EVAS steps | Spectre steps |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| `same_server_speed_repeat_r5_goal_20260522` | `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `vbr1_l1_pfd_small_phase_error_response_bugfix` | 0.041 | 103.3 | 4.284 | 60058 | 435 |
| `same_server_speed_repeat_r4_goal_20260522` | `vbr1_l1_pfd_small_phase_error_response` | `tb` | `vbr1_l1_pfd_small_phase_error_response_tb` | 0.045 | 98.87 | 4.437 | 60058 | 435 |
| `same_server_speed_repeat_r4_goal_20260522` | `vbr1_l1_pfd_small_phase_error_response` | `dut` | `vbm1_pfd_small_phase_error_response_dut` | 0.046 | 102.6 | 4.751 | 60058 | 435 |
| `same_server_speed_repeat_r4_goal_20260522` | `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `pfd_small_phase_response_smoke` | 0.051 | 97.91 | 5.042 | 60058 | 435 |
| `same_server_speed_repeat_r4_goal_20260522` | `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `vbr1_l1_pfd_small_phase_error_response_bugfix` | 0.055 | 93.99 | 5.165 | 60058 | 435 |
| `same_server_speed_repeat_r5_goal_20260522` | `vbr1_l1_pfd_small_phase_error_response` | `tb` | `vbr1_l1_pfd_small_phase_error_response_tb` | 0.058 | 76.43 | 4.411 | 60058 | 435 |
| `same_server_speed_repeat_r5_goal_20260522` | `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `pfd_small_phase_response_smoke` | 0.059 | 81.34 | 4.776 | 60058 | 435 |
| `same_server_speed_repeat_r5_goal_20260522` | `vbr1_l1_pfd_small_phase_error_response` | `dut` | `vbm1_pfd_small_phase_error_response_dut` | 0.066 | 76.88 | 5.045 | 60058 | 435 |
| `same_server_speed_repeat_r5_goal_20260522` | `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `cppll_freq_step_reacquire_smoke` | 0.079 | 96.53 | 7.641 | 41900 | 34050 |
| `same_server_speed_repeat_r4_goal_20260522` | `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow_tb` | 0.096 | 66.78 | 6.412 | 41900 | 34050 |

### Largest Spectre-AX / Fast-Skip Speedups

| Report | Entry | Form | Task | Value | EVAS s | Spectre s | EVAS steps | Spectre steps |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| `same_server_speed_repeat_r5_goal_20260522` | `vbr1_l1_debounce_latch` | `bugfix` | `vbm1_debounce_latch_bugfix` | 48.24 | 0.474 | 22.88 | 283 | 113 |
| `same_server_speed_repeat_r5_goal_20260522` | `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `vbm1_simple_binary_voltage_dac_4b_e2e` | 40.98 | 0.575 | 23.58 | 351 | 156 |
| `same_server_speed_repeat_r5_goal_20260522` | `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `vbm1_simple_binary_voltage_dac_4b_dut` | 40.14 | 0.508 | 20.40 | 351 | 156 |
| `same_server_speed_repeat_r5_goal_20260522` | `vbr1_l1_lock_detector` | `e2e` | `vbm1_lock_detector_e2e` | 39.57 | 0.600 | 23.76 | 480 | 250 |
| `same_server_speed_repeat_r5_goal_20260522` | `vbr1_l1_debounce_latch` | `tb` | `vbm1_debounce_latch_tb` | 37.85 | 0.552 | 20.91 | 283 | 113 |
| `same_server_speed_repeat_r4_goal_20260522` | `vbr1_l1_thermometer_code_decoder` | `bugfix` | `vbm1_thermometer_decoder_guarded_bugfix` | 37.44 | 0.515 | 19.30 | 253 | 105 |
| `same_server_speed_repeat_r5_goal_20260522` | `vbr1_l1_thermometer_code_decoder` | `bugfix` | `vbm1_thermometer_decoder_guarded_bugfix` | 36.15 | 0.631 | 22.81 | 253 | 105 |
| `same_server_speed_repeat_r4_goal_20260522` | `vbr1_l1_debounce_latch` | `tb` | `vbm1_debounce_latch_tb` | 34.69 | 0.488 | 16.92 | 283 | 113 |
| `same_server_speed_repeat_r4_goal_20260522` | `vbr1_l1_edge_detector` | `tb` | `vbm1_edge_detector_tb` | 34.36 | 0.556 | 19.09 | 413 | 129 |
| `same_server_speed_repeat_r5_goal_20260522` | `vbr1_l1_segmented_dac` | `e2e` | `vbm1_segmented_dac_e2e` | 34.01 | 0.635 | 21.59 | 312 | 103 |

### Slowest Fast-Skip Cases

| Report | Entry | Form | Task | Value | EVAS s | Spectre s | EVAS steps | Spectre steps |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| `same_server_speed_repeat_r5_goal_20260522` | `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `vbr1_l1_pfd_small_phase_error_response_bugfix` | 103.3 | 103.3 | - | 60058 | - |
| `same_server_speed_repeat_r4_goal_20260522` | `vbr1_l1_pfd_small_phase_error_response` | `dut` | `vbm1_pfd_small_phase_error_response_dut` | 102.6 | 102.6 | - | 60058 | - |
| `same_server_speed_repeat_r4_goal_20260522` | `vbr1_l1_pfd_small_phase_error_response` | `tb` | `vbr1_l1_pfd_small_phase_error_response_tb` | 98.87 | 98.87 | - | 60058 | - |
| `same_server_speed_repeat_r4_goal_20260522` | `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `pfd_small_phase_response_smoke` | 97.91 | 97.91 | - | 60058 | - |
| `same_server_speed_repeat_r5_goal_20260522` | `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `cppll_freq_step_reacquire_smoke` | 96.53 | 96.53 | - | 41900 | - |
| `same_server_speed_repeat_r4_goal_20260522` | `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `vbr1_l1_pfd_small_phase_error_response_bugfix` | 93.99 | 93.99 | - | 60058 | - |
| `same_server_speed_repeat_r5_goal_20260522` | `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `pfd_small_phase_response_smoke` | 81.34 | 81.34 | - | 60058 | - |
| `same_server_speed_repeat_r5_goal_20260522` | `vbr1_l1_pfd_small_phase_error_response` | `dut` | `vbm1_pfd_small_phase_error_response_dut` | 76.88 | 76.88 | - | 60058 | - |
| `same_server_speed_repeat_r5_goal_20260522` | `vbr1_l1_pfd_small_phase_error_response` | `tb` | `vbr1_l1_pfd_small_phase_error_response_tb` | 76.43 | 76.43 | - | 60058 | - |
| `same_server_speed_repeat_r4_goal_20260522` | `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `cppll_freq_step_reacquire_smoke` | 71.77 | 71.77 | - | 41900 | - |
