# vaBench Same-Server Speed Goal Summary

- Generated: 2026-05-22T16:47:26
- Reports: 3
  - `same_server_speed_cold_r1_goal_20260522`: rows=259 jobs=8 path=`benchmark-vabench-release-v1/reports/same_server_speed_cold_r1_goal_20260522.json`
  - `same_server_speed_repeat_r2_goal_20260522`: rows=259 jobs=8 path=`benchmark-vabench-release-v1/reports/same_server_speed_repeat_r2_goal_20260522.json`
  - `same_server_speed_repeat_r3_goal_20260522`: rows=259 jobs=8 path=`benchmark-vabench-release-v1/reports/same_server_speed_repeat_r3_goal_20260522.json`

## Combined Wall-Time Geomean By Mode

| Backend | Mode | Reports | PASS/Runs | Geomean s | Mean s | CV |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| evas | `profile_fast_skip_source_error_control` | 3 | 776/777 | 1.248 | 1.248 | 0.003 |
| evas | `strict_current` | 3 | 777/777 | 1.988 | 1.988 | 0.001 |
| spectre | `ax` | 3 | 777/777 | 7.336 | 7.337 | 0.007 |
| spectre | `classic` | 3 | 777/777 | 22.89 | 22.89 | 0.002 |

## Combined Accuracy-Gated Speedups

| Spectre | EVAS | N | Geomean x | Mean x | Median x | P10 x | P90 x | Min x | Max x |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `ax` | `profile_fast_skip_source_error_control` | 776 | 5.875 | 7.250 | 6.813 | 3.234 | 13.57 | 0.259 | 26.97 |
| `ax` | `strict_current` | 777 | 3.690 | 5.470 | 4.762 | 1.020 | 10.71 | 0.064 | 24.49 |
| `classic` | `profile_fast_skip_source_error_control` | 776 | 18.33 | 21.38 | 21.42 | 12.04 | 31.38 | 1.029 | 56.95 |
| `classic` | `strict_current` | 777 | 11.51 | 15.16 | 14.71 | 4.598 | 26.78 | 0.228 | 35.94 |

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
| `same_server_speed_repeat_r3_goal_20260522` | `ax` | `profile_fast_skip_source_error_control` | 258 | 5.837 | 6.773 | 3.229 | 13.63 |
| `same_server_speed_repeat_r3_goal_20260522` | `ax` | `strict_current` | 259 | 3.685 | 4.787 | 1.149 | 9.963 |
| `same_server_speed_repeat_r3_goal_20260522` | `classic` | `profile_fast_skip_source_error_control` | 258 | 18.26 | 21.32 | 12.04 | 30.72 |
| `same_server_speed_repeat_r3_goal_20260522` | `classic` | `strict_current` | 259 | 11.53 | 14.43 | 4.609 | 26.93 |

## Raw Speedups

| Spectre | EVAS | N | Geomean x | Mean x | Median x |
| --- | --- | ---: | ---: | ---: | ---: |
| `ax` | `profile_fast_skip_source_error_control` | 777 | 5.876 | 7.250 | 6.817 |
| `ax` | `strict_current` | 777 | 3.690 | 5.470 | 4.762 |
| `classic` | `profile_fast_skip_source_error_control` | 777 | 18.34 | 21.38 | 21.44 |
| `classic` | `strict_current` | 777 | 11.51 | 15.16 | 14.71 |

## EVAS Fast-Skip Versus Strict

Across paired EVAS rows, `strict_current_wall / profile_fast_skip_source_error_control_wall` has geomean 1.592x, median 1.375x, n=776.

## Waveform Tolerance Sweep

This sweep reuses saved waveform parity metrics for `profile_fast_skip_source_error_control`; task-specific semantic comparators are counted as non-waveform rows and are not threshold-scanned.

| Target | Waveform Rows | Non-Waveform Rows | Current PASS | P95<=0.05 Max<=0.10 | P95<=0.10 Max<=0.15 | P95<=0.14 Max<=0.22 | P95<=0.20 Max<=0.30 | Worst P95 | Worst Max | Worst Abs V |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `spectre_ax` | 753 | 24 | 753 | 729 | 741 | 753 | 753 | 0.128 | 0.128 | 1.000 |
| `spectre_classic` | 753 | 24 | 753 | 732 | 732 | 753 | 753 | 0.130 | 0.130 | 1.000 |
| `strict_evas` | 753 | 24 | 753 | 741 | 753 | 753 | 753 | 0.051 | 0.051 | 0.934 |

## Non-PASS Rows

| Report | Entry | Form | Backend | Mode | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `same_server_speed_repeat_r3_goal_20260522` | `vbr1_l1_calibration_deadband_controller` | `tb` | evas | `profile_fast_skip_source_error_control` | FAIL_SIM_CORRECTNESS | returncode=0; behavior_eval_timeout>60s |

## Outliers

### Smallest Spectre-AX / Fast-Skip Speedups

| Report | Entry | Form | Task | Value | EVAS s | Spectre s | EVAS steps | Spectre steps |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| `same_server_speed_cold_r1_goal_20260522` | `vbr1_l1_gain_estimator` | `tb` | `vbr1_l1_gain_estimator_tb` | 0.259 | 38.79 | 10.05 | 110493 | 150146 |
| `same_server_speed_repeat_r2_goal_20260522` | `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `vbr1_l1_pfd_small_phase_error_response_bugfix` | 0.259 | 16.04 | 4.160 | 60058 | 435 |
| `same_server_speed_repeat_r2_goal_20260522` | `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `pfd_small_phase_response_smoke` | 0.262 | 16.18 | 4.242 | 60058 | 435 |
| `same_server_speed_cold_r1_goal_20260522` | `vbr1_l1_pfd_small_phase_error_response` | `dut` | `vbm1_pfd_small_phase_error_response_dut` | 0.275 | 16.04 | 4.409 | 60058 | 435 |
| `same_server_speed_cold_r1_goal_20260522` | `vbr1_l1_pfd_small_phase_error_response` | `tb` | `vbr1_l1_pfd_small_phase_error_response_tb` | 0.278 | 15.65 | 4.351 | 60058 | 435 |
| `same_server_speed_cold_r1_goal_20260522` | `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `pfd_small_phase_response_smoke` | 0.279 | 16.16 | 4.507 | 60058 | 435 |
| `same_server_speed_repeat_r2_goal_20260522` | `vbr1_l1_pfd_small_phase_error_response` | `dut` | `vbm1_pfd_small_phase_error_response_dut` | 0.284 | 15.77 | 4.477 | 60058 | 435 |
| `same_server_speed_repeat_r3_goal_20260522` | `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `vbr1_l1_pfd_small_phase_error_response_bugfix` | 0.289 | 16.06 | 4.646 | 60058 | 435 |
| `same_server_speed_repeat_r3_goal_20260522` | `vbr1_l1_pfd_small_phase_error_response` | `dut` | `vbm1_pfd_small_phase_error_response_dut` | 0.290 | 15.83 | 4.593 | 60058 | 435 |
| `same_server_speed_repeat_r3_goal_20260522` | `vbr1_l1_pfd_small_phase_error_response` | `tb` | `vbr1_l1_pfd_small_phase_error_response_tb` | 0.291 | 15.82 | 4.599 | 60058 | 435 |

### Largest Spectre-AX / Fast-Skip Speedups

| Report | Entry | Form | Task | Value | EVAS s | Spectre s | EVAS steps | Spectre steps |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| `same_server_speed_repeat_r3_goal_20260522` | `vbr1_l1_thermometer_code_decoder` | `tb` | `vbm1_thermometer_decoder_guarded_tb` | 26.97 | 0.718 | 19.36 | 253 | 105 |
| `same_server_speed_cold_r1_goal_20260522` | `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `vbm1_simple_binary_voltage_dac_4b_e2e` | 24.54 | 0.761 | 18.68 | 351 | 156 |
| `same_server_speed_cold_r1_goal_20260522` | `vbr1_l1_debounce_latch` | `bugfix` | `vbm1_debounce_latch_bugfix` | 23.38 | 0.849 | 19.85 | 283 | 113 |
| `same_server_speed_repeat_r2_goal_20260522` | `vbr1_l1_thermometer_code_decoder` | `tb` | `vbm1_thermometer_decoder_guarded_tb` | 23.27 | 0.824 | 19.18 | 253 | 105 |
| `same_server_speed_repeat_r2_goal_20260522` | `vbr1_l1_debounce_latch` | `bugfix` | `vbm1_debounce_latch_bugfix` | 22.83 | 0.767 | 17.52 | 283 | 113 |
| `same_server_speed_repeat_r3_goal_20260522` | `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `vbm1_simple_binary_voltage_dac_4b_e2e` | 22.36 | 0.846 | 18.91 | 351 | 156 |
| `same_server_speed_cold_r1_goal_20260522` | `vbr1_l1_edge_detector` | `tb` | `vbm1_edge_detector_tb` | 22.18 | 0.846 | 18.77 | 413 | 129 |
| `same_server_speed_repeat_r3_goal_20260522` | `vbr1_l1_segmented_dac` | `e2e` | `vbm1_segmented_dac_e2e` | 22.03 | 0.870 | 19.17 | 312 | 103 |
| `same_server_speed_cold_r1_goal_20260522` | `vbr1_l1_thermometer_code_decoder` | `tb` | `vbm1_thermometer_decoder_guarded_tb` | 21.79 | 0.813 | 17.72 | 253 | 105 |
| `same_server_speed_repeat_r2_goal_20260522` | `vbr1_l1_lock_detector` | `e2e` | `vbm1_lock_detector_e2e` | 20.63 | 0.895 | 18.46 | 480 | 250 |

### Slowest Fast-Skip Cases

| Report | Entry | Form | Task | Value | EVAS s | Spectre s | EVAS steps | Spectre steps |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| `same_server_speed_cold_r1_goal_20260522` | `vbr1_l1_gain_estimator` | `tb` | `vbr1_l1_gain_estimator_tb` | 38.79 | 38.79 | - | 110493 | - |
| `same_server_speed_repeat_r3_goal_20260522` | `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `vbr1_l2_gain_extraction_convergence_measurement_flow_tb` | 33.50 | 33.50 | - | 110493 | - |
| `same_server_speed_repeat_r2_goal_20260522` | `vbr1_l1_gain_estimator` | `tb` | `vbr1_l1_gain_estimator_tb` | 33.27 | 33.27 | - | 110493 | - |
| `same_server_speed_cold_r1_goal_20260522` | `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `vbr1_l2_gain_extraction_convergence_measurement_flow_tb` | 33.02 | 33.02 | - | 110493 | - |
| `same_server_speed_repeat_r2_goal_20260522` | `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `vbr1_l2_gain_extraction_convergence_measurement_flow_tb` | 32.70 | 32.70 | - | 110493 | - |
| `same_server_speed_repeat_r3_goal_20260522` | `vbr1_l1_gain_estimator` | `tb` | `vbr1_l1_gain_estimator_tb` | 32.34 | 32.34 | - | 110493 | - |
| `same_server_speed_repeat_r3_goal_20260522` | `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `pfd_small_phase_response_smoke` | 16.26 | 16.26 | - | 60058 | - |
| `same_server_speed_repeat_r2_goal_20260522` | `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `pfd_small_phase_response_smoke` | 16.18 | 16.18 | - | 60058 | - |
| `same_server_speed_cold_r1_goal_20260522` | `vbr1_l1_pfd_small_phase_error_response` | `e2e` | `pfd_small_phase_response_smoke` | 16.16 | 16.16 | - | 60058 | - |
| `same_server_speed_repeat_r3_goal_20260522` | `vbr1_l1_pfd_small_phase_error_response` | `bugfix` | `vbr1_l1_pfd_small_phase_error_response_bugfix` | 16.06 | 16.06 | - | 60058 | - |
