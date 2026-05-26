# Same-Server EVAS/Spectre Speed

Date: 2026-05-26
Claim allowed: `False`
Reason: Same-server timing is measured directly on one host and the artifact emits checker/waveform Spectre-equivalence gates. Paper-facing speed claims should use only equivalence-gated rows and still need repeated cold/warm runs.

## Scope

- Host: `thu-sui`
- Selected rows: 64
- Jobs: 5
- EVAS modes: `profile_fast_skip_source_error_control, strict_current`
- Spectre modes: `spectre_ax_equalized_precision, spectre_reference_strict_primary`
- Output root: `results/precision-ranking-full-e2e-equalized-20260526`

## Mode Summary

| Backend | Mode | Runs | Sim OK | Behavior PASS | Behavior non-PASS | Total wall s | Mean wall s |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| evas | profile_fast_skip_source_error_control | 64 | 64 | 57 | 7 | 190.458 | 2.976 |
| evas | strict_current | 64 | 64 | 57 | 7 | 525.160 | 8.206 |
| spectre | spectre_ax_equalized_precision | 64 | 64 | 57 | 7 | 66.184 | 1.034 |
| spectre | spectre_reference_strict_primary | 64 | 64 | 57 | 7 | 242.031 | 3.782 |

## Reference Comparison Summary

Each candidate is compared against the same-row strict Spectre reference. The waveform status uses the simulator-equivalence policy from `run_gold_dual_suite.py`.

| Candidate | Runs | Passed | Needs review | Blocked | Worst max abs V | Worst max relative RMS error |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `evas/profile_fast_skip_source_error_control` | 64 | 64 | 0 | 0 | 1 | 0.127836 |
| `evas/strict_current` | 64 | 64 | 0 | 0 | 1 | 0.127836 |
| `spectre/spectre_ax_equalized_precision` | 64 | 64 | 0 | 0 | 1 | 0.122542 |

## Per-Row Reference Comparisons

| Entry | Form | Variant | Candidate | Reference | Behavior OK | Waveform | Max abs V | Max relative RMS error | Signals |
| --- | --- | --- | --- | --- | --- | --- | ---: | ---: | ---: |
| `vbr1_l1_acquisition_limited_sample_and_hold` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 4.95927e-08 | 4.62642e-08 | 5 |
| `vbr1_l1_acquisition_limited_sample_and_hold` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 3.22649e-06 | 2.5478e-07 | 5 |
| `vbr1_l1_acquisition_limited_sample_and_hold` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 6.66134e-15 | 6.75842e-16 | 5 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 4.501e-07 | 2.1234e-08 | 3 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 4.501e-07 | 2.1234e-08 | 3 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 4.455e-05 | 2.10169e-06 | 3 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 1 | 0.0025 | 5 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 1 | 0.0025 | 5 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 5 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `False` | `passed` | 0.0569985 | 0.00630664 | 5 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `False` | `passed` | 0.0569985 | 0.00630664 | 5 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `False` | `passed` | 0.0197224 | 0.00175035 | 5 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 3 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 3 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 3 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 5.54543e-07 | 7.69535e-08 | 5 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0.000487804 | 4.90351e-05 | 5 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 5.43425e-05 | 5.70416e-06 | 5 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `False` | `passed` | 0 | 0 | 5 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `False` | `passed` | 0 | 0 | 5 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `False` | `passed` | 0 | 0 | 5 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `False` | `passed` | 4.00089e-07 | 6.25139e-08 | 5 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `False` | `passed` | 0.000355526 | 3.73012e-05 | 5 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `False` | `passed` | 3.96e-05 | 6.1875e-06 | 5 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 12 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 12 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 12 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 4.99583e-08 | 5.94643e-09 | 5 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 4.99885e-08 | 7.98918e-09 | 5 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 2.22045e-16 | 6.16207e-17 | 5 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 8.95699e-08 | 9.50284e-09 | 3 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 4.93208e-05 | 2.21536e-06 | 3 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 8.86545e-06 | 7.12526e-07 | 3 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 2 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 2 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 2 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0.152904 | 0.00711894 | 5 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0.152904 | 0.00711894 | 5 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0.0233945 | 0.00130555 | 5 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 3 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 3 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 3 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 1.23217e-11 | 1.04606e-12 | 2 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 1.23217e-11 | 1.04606e-12 | 2 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 1.23328e-11 | 1.04681e-12 | 2 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 2 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 2 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 2 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 2.77001e-14 | 4.65686e-15 | 38 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0.00066011 | 6.64217e-05 | 38 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 1.67089e-14 | 2.61237e-15 | 38 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 4 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 4 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 4 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 6 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 6 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 6 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 4.99386e-08 | 3.19388e-08 | 2 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 4.99386e-08 | 3.19388e-08 | 2 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 7.77156e-16 | 7.90649e-17 | 2 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0.231542 | 0.127836 | 4 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0.209265 | 0.127836 | 4 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0.0433608 | 0.00221414 | 4 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 5.00111e-08 | 9.2018e-09 | 5 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 9.01097e-08 | 1.02918e-08 | 5 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 4.95e-06 | 9.10775e-07 | 5 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `False` | `passed` | 1.75788e-07 | 4.5392e-08 | 5 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `False` | `passed` | 0.000117285 | 1.0732e-05 | 5 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `False` | `passed` | 1.40212e-05 | 2.10921e-06 | 5 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 1 | 0.000833333 | 4 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 1 | 0.000833333 | 4 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 4 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 3.90241e-10 | 3.64558e-11 | 3 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0.00713601 | 0.000466392 | 3 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 1.85663e-12 | 1.75325e-13 | 3 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 4 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 4 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 4 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 5.54543e-07 | 7.69535e-08 | 5 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0.000487804 | 4.90351e-05 | 5 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 5.43425e-05 | 5.70416e-06 | 5 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 4 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 4 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 4 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 8.56537e-14 | 5.30325e-15 | 3 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0.0208674 | 0.00137938 | 3 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0.549083 | 0.0395091 | 3 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 4.56907e-08 | 5.34204e-09 | 4 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 4.56907e-08 | 5.46698e-09 | 4 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 9.65894e-15 | 3.13341e-15 | 4 |
| `vbr1_l1_pipeline_adc_stage` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 8.99164e-06 | 1.44249e-06 | 6 |
| `vbr1_l1_pipeline_adc_stage` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 7.3696e-07 | 1.2333e-07 | 6 |
| `vbr1_l1_pipeline_adc_stage` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 2.2275e-05 | 5.05207e-06 | 6 |
| `vbr1_l1_precision_rectifier_envelope_detector` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 1 | 0.00454476 | 6 |
| `vbr1_l1_precision_rectifier_envelope_detector` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 1 | 0.00462411 | 6 |
| `vbr1_l1_precision_rectifier_envelope_detector` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 1 | 0.01 | 6 |
| `vbr1_l1_programmable_gain_amplifier` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 1 | 0.0128087 | 6 |
| `vbr1_l1_programmable_gain_amplifier` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 1 | 0.0126319 | 6 |
| `vbr1_l1_programmable_gain_amplifier` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 1 | 0.0191667 | 6 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0.00105038 | 9.80241e-07 | 6 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0.000295673 | 1.99714e-06 | 6 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0.103929 | 9.3869e-05 | 6 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 1 | 0.127719 | 2 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 1 | 0.127719 | 2 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 1 | 0.122542 | 2 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 1.34615e-14 | 1.06386e-15 | 3 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0.388 | 0.0514651 | 3 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 1.94011e-14 | 1.44192e-15 | 3 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 7.50167e-07 | 6.3615e-08 | 3 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 7.50167e-07 | 6.33999e-08 | 3 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 7.425e-05 | 5.71577e-06 | 3 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 7 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 7 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 7 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0.0949975 | 0.0104149 | 6 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0.0949975 | 0.0104149 | 6 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0.0456999 | 0.00370817 | 6 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 4.99582e-08 | 3.32577e-08 | 3 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 4.99582e-08 | 3.32578e-08 | 3 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 1.06165e-15 | 8.30977e-17 | 3 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 9.22158e-07 | 6.80958e-07 | 1 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 9.22158e-07 | 6.80958e-07 | 1 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0.000202784 | 0.000257532 | 1 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 5.88418e-15 | 3.84554e-15 | 2 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0.015 | 0.00978913 | 2 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 5.66214e-15 | 3.69588e-15 | 2 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `False` | `passed` | 1.75788e-07 | 4.5392e-08 | 5 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `False` | `passed` | 0.000117285 | 1.0732e-05 | 5 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `False` | `passed` | 1.40212e-05 | 2.10921e-06 | 5 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 5 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 5 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 5 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 5.54543e-07 | 7.69535e-08 | 5 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0.000487804 | 4.90351e-05 | 5 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 5.43425e-05 | 5.70416e-06 | 5 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 1 | 0.00166667 | 7 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 1 | 0.00166667 | 7 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 7 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 3 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 3 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 3 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 6.00133e-08 | 3.2282e-08 | 4 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 6.00133e-08 | 3.10475e-08 | 4 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 5.94e-06 | 3.19521e-06 | 4 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0.132996 | 0.0090756 | 16 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0.132996 | 0.0090756 | 16 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0.0231896 | 0.0017511 | 16 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 1.29452e-13 | 6.14446e-15 | 3 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 2.34503e-08 | 6.8241e-10 | 3 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 1.12244e-13 | 5.42041e-15 | 3 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 1 | 0.000833333 | 2 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 1 | 0.000833333 | 2 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 3.33067e-16 | 9.5596e-17 | 2 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | - | - | - |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | - | - | - |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | - | - | - |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `False` | `passed` | 1.75788e-07 | 4.5392e-08 | 5 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `False` | `passed` | 0.000117285 | 1.0732e-05 | 5 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `False` | `passed` | 1.40212e-05 | 2.10921e-06 | 5 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 3 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 3 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0 | 0 | 3 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `False` | `passed` | 5.54543e-07 | 7.69535e-08 | 5 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `False` | `passed` | 0.000487804 | 4.90351e-05 | 5 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `False` | `passed` | 5.43425e-05 | 5.70416e-06 | 5 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 4.97492e-08 | 2.53167e-08 | 3 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 4.97492e-08 | 2.53167e-08 | 3 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 1.0969e-13 | 6.73699e-15 | 3 |
| `vbr1_l2_converter_static_linearity_measurement_flow` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 1.56414e-07 | 2.14744e-08 | 7 |
| `vbr1_l2_converter_static_linearity_measurement_flow` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 2.88536e-05 | 2.82103e-06 | 7 |
| `vbr1_l2_converter_static_linearity_measurement_flow` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 1.32e-05 | 1.93283e-06 | 7 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | - | - | - |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | - | - | - |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | - | - | - |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 4.99583e-08 | 5.94643e-09 | 5 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 4.99885e-08 | 7.98918e-09 | 5 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 2.22045e-16 | 6.16207e-17 | 5 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0.231542 | 0.127836 | 4 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0.209265 | 0.127836 | 4 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0.0433608 | 0.00221414 | 4 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 1.40657e-07 | 1.56285e-08 | 2 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 5.35934e-06 | 2.97928e-07 | 2 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 1.39219e-05 | 1.54687e-06 | 2 |
| `vbr1_l2_pipeline_adc_chain` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 1 | 0.03 | 12 |
| `vbr1_l2_pipeline_adc_chain` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 1 | 0.03 | 12 |
| `vbr1_l2_pipeline_adc_chain` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 1 | 0.03 | 12 |
| `vbr1_l2_programmable_stimulus_sequencer` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0.0672899 | 0.00637048 | 6 |
| `vbr1_l2_programmable_stimulus_sequencer` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0.0672899 | 0.00637005 | 6 |
| `vbr1_l2_programmable_stimulus_sequencer` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 0.304466 | 0.031849 | 6 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `evas/profile_fast_skip_source_error_control` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 5.46989e-07 | 2.16459e-07 | 13 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `evas/strict_current` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 4.52701e-06 | 3.62085e-07 | 13 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `spectre/spectre_ax_equalized_precision` | `spectre/spectre_reference_strict_primary` | `True` | `passed` | 2.29049e-05 | 1.00009e-06 | 13 |

## Spectre Run Settings

This table records the final staged testbench settings used by Spectre. For normalized precision-ranking modes, `tran` and `simulatorOptions` are rewritten before Spectre is launched; speed-baseline modes keep the staged testbench unchanged.

| Entry | Form | Variant | Mode | Normalized | CLI args | tran line | simulatorOptions line | Result root |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `vbr1_l1_acquisition_limited_sample_and_hold` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=90n maxstep=250p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_acquisition_limited_sample_and_hold/e2e/gold/vbr1_l1_acquisition_limited_sample_and_hold_e2e/spectre_ax_equalized_precision` |
| `vbr1_l1_acquisition_limited_sample_and_hold` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=90n maxstep=250p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_acquisition_limited_sample_and_hold/e2e/gold/vbr1_l1_acquisition_limited_sample_and_hold_e2e/spectre_reference_strict_primary` |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=140n maxstep=100p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_aperture_delay_track_and_hold/e2e/gold/vbm1_track_hold_aperture_e2e/spectre_ax_equalized_precision` |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=140n maxstep=100p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_aperture_delay_track_and_hold/e2e/gold/vbm1_track_hold_aperture_e2e/spectre_reference_strict_primary` |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=170n maxstep=0.1n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_bang_bang_phase_detector/e2e/gold/bbpd_data_edge_alignment_smoke/spectre_ax_equalized_precision` |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=170n maxstep=0.1n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_bang_bang_phase_detector/e2e/gold/bbpd_data_edge_alignment_smoke/spectre_reference_strict_primary` |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=165n maxstep=500p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_binary_weighted_voltage_dac/e2e/gold/vbm1_simple_binary_voltage_dac_4b_e2e/spectre_ax_equalized_precision` |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=165n maxstep=500p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_binary_weighted_voltage_dac/e2e/gold/vbm1_simple_binary_voltage_dac_4b_e2e/spectre_reference_strict_primary` |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=3000n maxstep=5n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_burst_clock_source/e2e/gold/clk_burst_gen_smoke/spectre_ax_equalized_precision` |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=3000n maxstep=5n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_burst_clock_source/e2e/gold/clk_burst_gen_smoke/spectre_reference_strict_primary` |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=80n maxstep=0.5n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_calibration_deadband_controller/e2e/gold/vbr1_l1_calibration_deadband_controller_e2e/spectre_ax_equalized_precision` |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=80n maxstep=0.5n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_calibration_deadband_controller/e2e/gold/vbr1_l1_calibration_deadband_controller_e2e/spectre_reference_strict_primary` |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=68n maxstep=20p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_capacitive_weighted_sar_feedback_dac/e2e/gold/vbr1_l1_capacitive_weighted_sar_feedback_dac_e2e/spectre_ax_equalized_precision` |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=68n maxstep=20p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_capacitive_weighted_sar_feedback_dac/e2e/gold/vbr1_l1_capacitive_weighted_sar_feedback_dac_e2e/spectre_reference_strict_primary` |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=80n maxstep=0.5n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_charge_pump_abstraction/e2e/gold/vbr1_l1_charge_pump_abstraction_e2e/spectre_ax_equalized_precision` |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=80n maxstep=0.5n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_charge_pump_abstraction/e2e/gold/vbr1_l1_charge_pump_abstraction_e2e/spectre_reference_strict_primary` |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=80n maxstep=50p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_clock_divider/e2e/gold/vbm1_resettable_counter_divider_e2e/spectre_ax_equalized_precision` |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=80n maxstep=50p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_clock_divider/e2e/gold/vbm1_resettable_counter_divider_e2e/spectre_reference_strict_primary` |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=820n maxstep=2n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_clocked_adc_quantizer/e2e/gold/flash_adc_3b_smoke/spectre_ax_equalized_precision` |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=820n maxstep=2n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_clocked_adc_quantizer/e2e/gold/flash_adc_3b_smoke/spectre_reference_strict_primary` |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=1u maxstep=2n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_clocked_sample_and_hold/e2e/gold/sample_hold_smoke/spectre_ax_equalized_precision` |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=1u maxstep=2n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_clocked_sample_and_hold/e2e/gold/sample_hold_smoke/spectre_reference_strict_primary` |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=90n maxstep=500p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_crossing_metric_writer/e2e/gold/vbm1_file_metric_writer_e2e/spectre_ax_equalized_precision` |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=90n maxstep=500p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_crossing_metric_writer/e2e/gold/vbm1_file_metric_writer_e2e/spectre_reference_strict_primary` |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=80n maxstep=0.5n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_dac_mismatch_unit_weighting_model/e2e/gold/vbr1_l1_dac_mismatch_unit_weighting_model_e2e/spectre_ax_equalized_precision` |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=80n maxstep=0.5n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_dac_mismatch_unit_weighting_model/e2e/gold/vbr1_l1_dac_mismatch_unit_weighting_model_e2e/spectre_reference_strict_primary` |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=140n maxstep=500p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_debounce_latch/e2e/gold/vbm1_debounce_latch_e2e/spectre_ax_equalized_precision` |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=140n maxstep=500p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_debounce_latch/e2e/gold/vbm1_debounce_latch_e2e/spectre_reference_strict_primary` |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=75n maxstep=20p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 temp=27 tnom=27 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_digital_phase_accumulator_with_modulo_wrap/e2e/gold/phase_accumulator_timer_wrap_smoke/spectre_ax_equalized_precision` |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=75n maxstep=20p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 temp=27 tnom=27 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_digital_phase_accumulator_with_modulo_wrap/e2e/gold/phase_accumulator_timer_wrap_smoke/spectre_reference_strict_primary` |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=500n maxstep=1n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_dither_or_noise_like_deterministic_source/e2e/gold/noise_gen_smoke/spectre_ax_equalized_precision` |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=500n maxstep=1n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_dither_or_noise_like_deterministic_source/e2e/gold/noise_gen_smoke/spectre_reference_strict_primary` |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=100n maxstep=2n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_dwa_dem_encoder/e2e/gold/dwa_ptr_gen_smoke/spectre_ax_equalized_precision` |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=100n maxstep=2n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_dwa_dem_encoder/e2e/gold/dwa_ptr_gen_smoke/spectre_reference_strict_primary` |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=12n maxstep=5p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 temp=27 tnom=27 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_edge_interval_timer/e2e/gold/cross_interval_163p333_smoke/spectre_ax_equalized_precision` |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=12n maxstep=5p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 temp=27 tnom=27 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_edge_interval_timer/e2e/gold/cross_interval_163p333_smoke/spectre_reference_strict_primary` |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=130n maxstep=500p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_element_shuffler/e2e/gold/vbm1_element_shuffler_e2e/spectre_ax_equalized_precision` |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=130n maxstep=500p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_element_shuffler/e2e/gold/vbm1_element_shuffler_e2e/spectre_reference_strict_primary` |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=160n maxstep=500p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_first_order_lowpass/e2e/gold/vbm1_first_order_lowpass_e2e/spectre_ax_equalized_precision` |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=160n maxstep=500p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_first_order_lowpass/e2e/gold/vbm1_first_order_lowpass_e2e/spectre_reference_strict_primary` |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=200u maxstep=8n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_gain_estimator/e2e/gold/gain_extraction_smoke/spectre_ax_equalized_precision` |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=200u maxstep=8n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_gain_estimator/e2e/gold/gain_extraction_smoke/spectre_reference_strict_primary` |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=620n maxstep=500p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_gain_trim_controller/e2e/gold/vbm1_gain_trim_controller_e2e/spectre_ax_equalized_precision` |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=620n maxstep=500p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_gain_trim_controller/e2e/gold/vbm1_gain_trim_controller_e2e/spectre_reference_strict_primary` |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=80n maxstep=0.5n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_higher_order_filter/e2e/gold/vbr1_l1_higher_order_filter_e2e/spectre_ax_equalized_precision` |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=80n maxstep=0.5n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_higher_order_filter/e2e/gold/vbr1_l1_higher_order_filter_e2e/spectre_reference_strict_primary` |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=80n maxstep=100p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_hysteresis_comparator/e2e/gold/comparator_hysteresis_smoke/spectre_ax_equalized_precision` |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=80n maxstep=100p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_hysteresis_comparator/e2e/gold/comparator_hysteresis_smoke/spectre_reference_strict_primary` |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=500n maxstep=2n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_lfsr_prbs_generator/e2e/gold/lfsr_smoke/spectre_ax_equalized_precision` |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=500n maxstep=2n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_lfsr_prbs_generator/e2e/gold/lfsr_smoke/spectre_reference_strict_primary` |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=220n maxstep=500p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_lock_detector/e2e/gold/vbm1_lock_detector_e2e/spectre_ax_equalized_precision` |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=220n maxstep=500p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_lock_detector/e2e/gold/vbm1_lock_detector_e2e/spectre_reference_strict_primary` |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=80n maxstep=0.5n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_loop_filter_abstraction/e2e/gold/vbr1_l1_loop_filter_abstraction_e2e/spectre_ax_equalized_precision` |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=80n maxstep=0.5n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_loop_filter_abstraction/e2e/gold/vbr1_l1_loop_filter_abstraction_e2e/spectre_reference_strict_primary` |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=28n maxstep=20p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_offset_comparator/e2e/gold/vbm1_offset_comparator_e2e/spectre_ax_equalized_precision` |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=28n maxstep=20p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_offset_comparator/e2e/gold/vbm1_offset_comparator_e2e/spectre_reference_strict_primary` |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=180n maxstep=500p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_peak_detector/e2e/gold/vbm1_peak_detector_e2e/spectre_ax_equalized_precision` |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=180n maxstep=500p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_peak_detector/e2e/gold/vbm1_peak_detector_e2e/spectre_reference_strict_primary` |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=300n maxstep=10p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 temp=27 tnom=27 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_pfd_up_dn_logic/e2e/gold/vbm1_pfd_reset_race_e2e/spectre_ax_equalized_precision` |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=300n maxstep=10p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 temp=27 tnom=27 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_pfd_up_dn_logic/e2e/gold/vbm1_pfd_reset_race_e2e/spectre_reference_strict_primary` |
| `vbr1_l1_pipeline_adc_stage` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=300n maxstep=500p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_pipeline_adc_stage/e2e/gold/vbr1_l1_pipeline_adc_stage_e2e/spectre_ax_equalized_precision` |
| `vbr1_l1_pipeline_adc_stage` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=300n maxstep=500p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_pipeline_adc_stage/e2e/gold/vbr1_l1_pipeline_adc_stage_e2e/spectre_reference_strict_primary` |
| `vbr1_l1_precision_rectifier_envelope_detector` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=90n maxstep=250p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_precision_rectifier_envelope_detector/e2e/gold/vbr1_l1_precision_rectifier_envelope_detector_e2e/spectre_ax_equalized_precision` |
| `vbr1_l1_precision_rectifier_envelope_detector` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=90n maxstep=250p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_precision_rectifier_envelope_detector/e2e/gold/vbr1_l1_precision_rectifier_envelope_detector_e2e/spectre_reference_strict_primary` |
| `vbr1_l1_programmable_gain_amplifier` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=90n maxstep=250p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_programmable_gain_amplifier/e2e/gold/vbr1_l1_programmable_gain_amplifier_e2e/spectre_ax_equalized_precision` |
| `vbr1_l1_programmable_gain_amplifier` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=90n maxstep=250p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_programmable_gain_amplifier/e2e/gold/vbr1_l1_programmable_gain_amplifier_e2e/spectre_reference_strict_primary` |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=16n maxstep=10p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_propagation_delay_comparator/e2e/gold/cmp_delay_smoke/spectre_ax_equalized_precision` |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=16n maxstep=10p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_propagation_delay_comparator/e2e/gold/cmp_delay_smoke/spectre_reference_strict_primary` |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=34n maxstep=20n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 temp=27 tnom=27 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_ramp_or_step_source/e2e/gold/bound_step_period_guard_smoke/spectre_ax_equalized_precision` |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=34n maxstep=20n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 temp=27 tnom=27 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_ramp_or_step_source/e2e/gold/bound_step_period_guard_smoke/spectre_reference_strict_primary` |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=320n maxstep=500p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_resettable_integrator/e2e/gold/vbm1_resettable_integrator_e2e/spectre_ax_equalized_precision` |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=320n maxstep=500p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_resettable_integrator/e2e/gold/vbm1_resettable_integrator_e2e/spectre_reference_strict_primary` |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=170n maxstep=500p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_sample_and_hold_with_droop_leakage/e2e/gold/vbm1_leaky_hold_e2e/spectre_ax_equalized_precision` |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=170n maxstep=500p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_sample_and_hold_with_droop_leakage/e2e/gold/vbm1_leaky_hold_e2e/spectre_reference_strict_primary` |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=260n maxstep=1n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_sar_logic/e2e/gold/vbm1_sar_logic_4b_e2e/spectre_ax_equalized_precision` |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=260n maxstep=1n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_sar_logic/e2e/gold/vbm1_sar_logic_4b_e2e/spectre_reference_strict_primary` |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=150n maxstep=500p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_segmented_dac/e2e/gold/vbm1_segmented_dac_e2e/spectre_ax_equalized_precision` |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=150n maxstep=500p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_segmented_dac/e2e/gold/vbm1_segmented_dac_e2e/spectre_reference_strict_primary` |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=160n maxstep=500p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_settling_time_detector/e2e/gold/vbm1_settling_time_measurement_tb_e2e/spectre_ax_equalized_precision` |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=160n maxstep=500p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_settling_time_detector/e2e/gold/vbm1_settling_time_measurement_tb_e2e/spectre_reference_strict_primary` |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=500n maxstep=500p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_sine_periodic_voltage_source/e2e/gold/vbr1_l1_sine_periodic_voltage_source_e2e/spectre_ax_equalized_precision` |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=500n maxstep=500p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_sine_periodic_voltage_source/e2e/gold/vbr1_l1_sine_periodic_voltage_source_e2e/spectre_reference_strict_primary` |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=170n maxstep=500p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_slew_rate_limiter/e2e/gold/vbm1_slew_rate_limiter_e2e/spectre_ax_equalized_precision` |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=170n maxstep=500p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_slew_rate_limiter/e2e/gold/vbm1_slew_rate_limiter_e2e/spectre_reference_strict_primary` |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=80n maxstep=0.5n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_soft_hysteretic_limiter/e2e/gold/vbr1_l1_soft_hysteretic_limiter_e2e/spectre_ax_equalized_precision` |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=80n maxstep=0.5n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_soft_hysteretic_limiter/e2e/gold/vbr1_l1_soft_hysteretic_limiter_e2e/spectre_reference_strict_primary` |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=4n maxstep=5p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_strongarm_style_latch_comparator/e2e/gold/vbm1_strongarm_comparator_behavior_e2e/spectre_ax_equalized_precision` |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=4n maxstep=5p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_strongarm_style_latch_comparator/e2e/gold/vbm1_strongarm_comparator_behavior_e2e/spectre_reference_strict_primary` |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=80n maxstep=0.5n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_successive_approximation_calibration_search_fsm/e2e/gold/vbr1_l1_successive_approximation_calibration_search_fsm_e2e/spectre_ax_equalized_precision` |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=80n maxstep=0.5n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_successive_approximation_calibration_search_fsm/e2e/gold/vbr1_l1_successive_approximation_calibration_search_fsm_e2e/spectre_reference_strict_primary` |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=120n maxstep=500p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_thermometer_code_decoder/e2e/gold/vbm1_thermometer_decoder_guarded_e2e/spectre_ax_equalized_precision` |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=120n maxstep=500p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_thermometer_code_decoder/e2e/gold/vbm1_thermometer_decoder_guarded_e2e/spectre_reference_strict_primary` |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=30n maxstep=0.5n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_threshold_comparator/e2e/gold/comparator_smoke/spectre_ax_equalized_precision` |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=30n maxstep=0.5n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_threshold_comparator/e2e/gold/comparator_smoke/spectre_reference_strict_primary` |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=220n maxstep=500p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_trim_calibration_controller/e2e/gold/vbm1_cdac_calibration_e2e/spectre_ax_equalized_precision` |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=220n maxstep=500p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_trim_calibration_controller/e2e/gold/vbm1_cdac_calibration_e2e/spectre_reference_strict_primary` |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=180n maxstep=500p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_unit_element_thermometer_dac/e2e/gold/vbm1_thermometer_dac_15seg_e2e/spectre_ax_equalized_precision` |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=180n maxstep=500p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_unit_element_thermometer_dac/e2e/gold/vbm1_thermometer_dac_15seg_e2e/spectre_reference_strict_primary` |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=180n maxstep=500p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_vco_phase_integrator/e2e/gold/vbm1_vco_phase_integrator_e2e/spectre_ax_equalized_precision` |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=180n maxstep=500p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_vco_phase_integrator/e2e/gold/vbm1_vco_phase_integrator_e2e/spectre_reference_strict_primary` |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=90n maxstep=20p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 temp=27 tnom=27 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_window_comparator_detector/e2e/gold/cross_hysteresis_window_smoke/spectre_ax_equalized_precision` |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=90n maxstep=20p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 temp=27 tnom=27 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l1_window_comparator_detector/e2e/gold/cross_hysteresis_window_smoke/spectre_reference_strict_primary` |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=5u maxstep=5n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l2_adpll_lock_ratio_hop_timer_flow/e2e/gold/adpll_ratio_hop_smoke/spectre_ax_equalized_precision` |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=5u maxstep=5n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l2_adpll_lock_ratio_hop_timer_flow/e2e/gold/adpll_ratio_hop_smoke/spectre_reference_strict_primary` |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=80n maxstep=0.5n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l2_amplifier_filter_chain/e2e/gold/vbr1_l2_amplifier_filter_chain_e2e/spectre_ax_equalized_precision` |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=80n maxstep=0.5n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l2_amplifier_filter_chain/e2e/gold/vbr1_l2_amplifier_filter_chain_e2e/spectre_reference_strict_primary` |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=100n maxstep=100p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l2_comparator_measurement_flow/e2e/gold/comparator_offset_search_smoke/spectre_ax_equalized_precision` |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=100n maxstep=100p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l2_comparator_measurement_flow/e2e/gold/comparator_offset_search_smoke/spectre_reference_strict_primary` |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=80n maxstep=0.5n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l2_complete_calibration_loop/e2e/gold/vbr1_l2_complete_calibration_loop_e2e/spectre_ax_equalized_precision` |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=80n maxstep=0.5n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l2_complete_calibration_loop/e2e/gold/vbr1_l2_complete_calibration_loop_e2e/spectre_reference_strict_primary` |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=170n maxstep=0.1n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l2_converter_front_end/e2e/gold/sample_hold_droop_smoke/spectre_ax_equalized_precision` |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=170n maxstep=0.1n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l2_converter_front_end/e2e/gold/sample_hold_droop_smoke/spectre_reference_strict_primary` |
| `vbr1_l2_converter_static_linearity_measurement_flow` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=96n maxstep=250p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l2_converter_static_linearity_measurement_flow/e2e/gold/vbr1_l2_converter_static_linearity_measurement_flow_e2e/spectre_ax_equalized_precision` |
| `vbr1_l2_converter_static_linearity_measurement_flow` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=96n maxstep=250p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l2_converter_static_linearity_measurement_flow/e2e/gold/vbr1_l2_converter_static_linearity_measurement_flow_e2e/spectre_reference_strict_primary` |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=6u maxstep=5n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow/e2e/gold/cppll_freq_step_reacquire_smoke/spectre_ax_equalized_precision` |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=6u maxstep=5n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow/e2e/gold/cppll_freq_step_reacquire_smoke/spectre_reference_strict_primary` |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=820n maxstep=2n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l2_flash_adc_mini_array/e2e/gold/flash_adc_3b_smoke/spectre_ax_equalized_precision` |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=820n maxstep=2n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l2_flash_adc_mini_array/e2e/gold/flash_adc_3b_smoke/spectre_reference_strict_primary` |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=200u maxstep=8n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l2_gain_extraction_convergence_measurement_flow/e2e/gold/gain_extraction_smoke/spectre_ax_equalized_precision` |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=200u maxstep=8n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l2_gain_extraction_convergence_measurement_flow/e2e/gold/gain_extraction_smoke/spectre_reference_strict_primary` |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=80n maxstep=20p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 temp=27 tnom=27 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l2_measurement_flow/e2e/gold/final_step_file_metric_smoke/spectre_ax_equalized_precision` |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=80n maxstep=20p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 temp=27 tnom=27 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l2_measurement_flow/e2e/gold/final_step_file_metric_smoke/spectre_reference_strict_primary` |
| `vbr1_l2_pipeline_adc_chain` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=170n maxstep=200p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l2_pipeline_adc_chain/e2e/gold/pipeline_adc_chain_e2e/spectre_ax_equalized_precision` |
| `vbr1_l2_pipeline_adc_chain` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=170n maxstep=200p errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l2_pipeline_adc_chain/e2e/gold/pipeline_adc_chain_e2e/spectre_reference_strict_primary` |
| `vbr1_l2_programmable_stimulus_sequencer` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=90n maxstep=0.25n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l2_programmable_stimulus_sequencer/e2e/gold/vbr1_l2_programmable_stimulus_sequencer_e2e/spectre_ax_equalized_precision` |
| `vbr1_l2_programmable_stimulus_sequencer` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=90n maxstep=0.25n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l2_programmable_stimulus_sequencer/e2e/gold/vbr1_l2_programmable_stimulus_sequencer_e2e/spectre_reference_strict_primary` |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `True` | `+preset=ax +mt` | `tran tran stop=10u maxstep=5n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l2_weighted_sar_adc_dac_loop/e2e/gold/sar_adc_dac_weighted_8b_smoke/spectre_ax_equalized_precision` |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `spectre_reference_strict_primary` | `True` | - | `tran tran stop=10u maxstep=5n errpreset=conservative` | `simulatorOptions options reltol=1e-5 vabstol=1e-8 iabstol=1e-12 gmin=1e-12` | `results/precision-ranking-full-e2e-equalized-20260526/spectre/vbr1_l2_weighted_sar_adc_dac_loop/e2e/gold/sar_adc_dac_weighted_8b_smoke/spectre_reference_strict_primary` |

## Spectre-Equivalence Gate Summary

These gates check whether EVAS preserves task behavior and stays within accepted Spectre-equivalent waveform tolerance. They are not a higher-than-Spectre precision target.

| EVAS mode | Runs | Gate PASS | Gate FAIL | Gate BLOCKED | Gate missing |
| --- | ---: | ---: | ---: | ---: | ---: |
| profile_fast_skip_source_error_control | 64 | 57 | 7 | 0 | 0 |
| strict_current | 64 | 57 | 7 | 0 | 0 |

## Per-Row Spectre-Equivalence Gates

| Entry | Form | Variant | EVAS mode | Gate | Reasons | Blocked |
| --- | --- | --- | --- | --- | --- | --- |
| `vbr1_l1_acquisition_limited_sample_and_hold` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_acquisition_limited_sample_and_hold` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `FAIL` | candidate_behavior_check_failed, spectre_spectre_ax_equalized_precision_parity:spectre_behavior_check_failed, spectre_spectre_reference_strict_primary_parity:spectre_behavior_check_failed | - |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `strict_current` | `FAIL` | candidate_behavior_check_failed, spectre_spectre_ax_equalized_precision_parity:spectre_behavior_check_failed, spectre_spectre_reference_strict_primary_parity:spectre_behavior_check_failed | - |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `FAIL` | candidate_behavior_check_failed, spectre_spectre_ax_equalized_precision_parity:spectre_behavior_check_failed, spectre_spectre_reference_strict_primary_parity:spectre_behavior_check_failed | - |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `strict_current` | `FAIL` | candidate_behavior_check_failed, spectre_spectre_ax_equalized_precision_parity:spectre_behavior_check_failed, spectre_spectre_reference_strict_primary_parity:spectre_behavior_check_failed | - |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `FAIL` | candidate_behavior_check_failed, spectre_spectre_ax_equalized_precision_parity:spectre_behavior_check_failed, spectre_spectre_reference_strict_primary_parity:spectre_behavior_check_failed | - |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `strict_current` | `FAIL` | candidate_behavior_check_failed, spectre_spectre_ax_equalized_precision_parity:spectre_behavior_check_failed, spectre_spectre_reference_strict_primary_parity:spectre_behavior_check_failed | - |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `FAIL` | candidate_behavior_check_failed, spectre_spectre_ax_equalized_precision_parity:spectre_behavior_check_failed, spectre_spectre_reference_strict_primary_parity:spectre_behavior_check_failed | - |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `strict_current` | `FAIL` | candidate_behavior_check_failed, spectre_spectre_ax_equalized_precision_parity:spectre_behavior_check_failed, spectre_spectre_reference_strict_primary_parity:spectre_behavior_check_failed | - |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_pipeline_adc_stage` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_pipeline_adc_stage` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_precision_rectifier_envelope_detector` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_precision_rectifier_envelope_detector` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_programmable_gain_amplifier` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_programmable_gain_amplifier` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `FAIL` | candidate_behavior_check_failed, spectre_spectre_ax_equalized_precision_parity:spectre_behavior_check_failed, spectre_spectre_reference_strict_primary_parity:spectre_behavior_check_failed | - |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `strict_current` | `FAIL` | candidate_behavior_check_failed, spectre_spectre_ax_equalized_precision_parity:spectre_behavior_check_failed, spectre_spectre_reference_strict_primary_parity:spectre_behavior_check_failed | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `FAIL` | candidate_behavior_check_failed, spectre_spectre_ax_equalized_precision_parity:spectre_behavior_check_failed, spectre_spectre_reference_strict_primary_parity:spectre_behavior_check_failed | - |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `strict_current` | `FAIL` | candidate_behavior_check_failed, spectre_spectre_ax_equalized_precision_parity:spectre_behavior_check_failed, spectre_spectre_reference_strict_primary_parity:spectre_behavior_check_failed | - |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `FAIL` | candidate_behavior_check_failed, spectre_spectre_ax_equalized_precision_parity:spectre_behavior_check_failed, spectre_spectre_reference_strict_primary_parity:spectre_behavior_check_failed | - |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `strict_current` | `FAIL` | candidate_behavior_check_failed, spectre_spectre_ax_equalized_precision_parity:spectre_behavior_check_failed, spectre_spectre_reference_strict_primary_parity:spectre_behavior_check_failed | - |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_converter_static_linearity_measurement_flow` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_converter_static_linearity_measurement_flow` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_pipeline_adc_chain` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_pipeline_adc_chain` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_programmable_stimulus_sequencer` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_programmable_stimulus_sequencer` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |

## Simulation-Only Speedups

| Entry | Form | Variant | Spectre mode | EVAS mode | Spectre wall s | EVAS wall s | Spectre/EVAS |
| --- | --- | --- | --- | --- | ---: | ---: | ---: |
| `vbr1_l1_acquisition_limited_sample_and_hold` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.975 | 0.583 | 1.673 |
| `vbr1_l1_acquisition_limited_sample_and_hold` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.975 | 1.023 | 0.953 |
| `vbr1_l1_acquisition_limited_sample_and_hold` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.603 | 0.583 | 6.182 |
| `vbr1_l1_acquisition_limited_sample_and_hold` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.603 | 1.023 | 3.522 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 1.167 | 1.588 | 0.735 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 1.167 | 1.940 | 0.601 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.420 | 1.588 | 2.154 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.420 | 1.940 | 1.763 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.882 | 2.735 | 0.323 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.882 | 2.807 | 0.314 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 4.004 | 2.735 | 1.464 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 4.004 | 2.807 | 1.427 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.905 | 0.516 | 1.754 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.905 | 0.484 | 1.870 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.418 | 0.516 | 6.620 |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.418 | 0.484 | 7.059 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.843 | 0.646 | 1.306 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.843 | 0.974 | 0.866 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.602 | 0.646 | 5.579 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.602 | 0.974 | 3.697 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.915 | 0.505 | 1.811 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.915 | 1.186 | 0.771 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.602 | 0.505 | 7.127 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.602 | 1.186 | 3.037 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 1.172 | 2.270 | 0.517 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 1.172 | 4.940 | 0.237 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.289 | 2.270 | 1.449 |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.289 | 4.940 | 0.666 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.958 | 0.682 | 1.404 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.958 | 1.437 | 0.666 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.115 | 0.682 | 4.566 |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.115 | 1.437 | 2.167 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.888 | 1.427 | 0.622 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.888 | 5.125 | 0.173 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.644 | 1.427 | 2.553 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.644 | 5.125 | 0.711 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.904 | 0.595 | 1.518 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.904 | 1.578 | 0.573 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.740 | 0.595 | 6.281 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.740 | 1.578 | 2.370 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.686 | 0.614 | 1.118 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.686 | 1.117 | 0.614 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 2.537 | 0.614 | 4.135 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 2.537 | 1.117 | 2.271 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.797 | 0.470 | 1.694 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.797 | 0.340 | 2.342 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 2.196 | 0.470 | 4.666 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 2.196 | 0.340 | 6.450 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.754 | 0.414 | 1.822 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.754 | 0.543 | 1.390 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.676 | 0.414 | 8.883 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.676 | 0.543 | 6.775 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 1.036 | 0.524 | 1.976 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 1.036 | 0.586 | 1.768 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.697 | 0.524 | 7.051 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.697 | 0.586 | 6.307 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.771 | 1.628 | 0.473 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.771 | 1.794 | 0.429 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.219 | 1.628 | 1.977 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.219 | 1.794 | 1.794 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.729 | 0.370 | 1.969 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.729 | 0.400 | 1.820 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 2.078 | 0.370 | 5.616 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 2.078 | 0.400 | 5.191 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 1.043 | 0.553 | 1.888 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 1.043 | 2.240 | 0.466 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 6.941 | 0.553 | 12.561 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 6.941 | 2.240 | 3.098 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.816 | 1.191 | 0.685 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.816 | 4.517 | 0.181 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.391 | 1.191 | 2.848 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.391 | 4.517 | 0.751 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.813 | 0.662 | 1.228 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.813 | 0.596 | 1.364 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.479 | 0.662 | 5.254 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.479 | 0.596 | 5.837 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.827 | 1.490 | 0.555 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.827 | 1.622 | 0.510 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 2.200 | 1.490 | 1.476 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 2.200 | 1.622 | 1.356 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 4.844 | 9.703 | 0.499 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 4.844 | 133.315 | 0.036 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 13.887 | 9.703 | 1.431 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 13.887 | 133.315 | 0.104 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.771 | 4.208 | 0.183 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.771 | 1.270 | 0.607 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 2.420 | 4.208 | 0.575 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 2.420 | 1.270 | 1.906 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.795 | 0.527 | 1.509 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.795 | 0.855 | 0.930 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.986 | 0.527 | 7.567 |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.986 | 0.855 | 4.664 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 1.114 | 1.113 | 1.001 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 1.114 | 0.608 | 1.831 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 5.023 | 1.113 | 4.512 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 5.023 | 0.608 | 8.258 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 1.003 | 4.172 | 0.240 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 1.003 | 5.370 | 0.187 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.478 | 4.172 | 0.834 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.478 | 5.370 | 0.648 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.763 | 0.704 | 1.083 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.763 | 0.632 | 1.206 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.437 | 0.704 | 4.882 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.437 | 0.632 | 5.435 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.729 | 0.512 | 1.423 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.729 | 1.173 | 0.621 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.291 | 0.512 | 6.427 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.291 | 1.173 | 2.805 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 1.260 | 1.417 | 0.889 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 1.260 | 1.644 | 0.766 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 2.088 | 1.417 | 1.474 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 2.088 | 1.644 | 1.270 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.753 | 0.904 | 0.833 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.753 | 0.578 | 1.302 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 2.210 | 0.904 | 2.444 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 2.210 | 0.578 | 3.821 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.826 | 22.278 | 0.037 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.826 | 73.270 | 0.011 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.965 | 22.278 | 0.178 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.965 | 73.270 | 0.054 |
| `vbr1_l1_pipeline_adc_stage` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.822 | 3.955 | 0.208 |
| `vbr1_l1_pipeline_adc_stage` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.822 | 3.870 | 0.212 |
| `vbr1_l1_pipeline_adc_stage` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.806 | 3.955 | 0.962 |
| `vbr1_l1_pipeline_adc_stage` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.806 | 3.870 | 0.983 |
| `vbr1_l1_precision_rectifier_envelope_detector` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.905 | 1.338 | 0.676 |
| `vbr1_l1_precision_rectifier_envelope_detector` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.905 | 3.999 | 0.226 |
| `vbr1_l1_precision_rectifier_envelope_detector` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.202 | 1.338 | 2.394 |
| `vbr1_l1_precision_rectifier_envelope_detector` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.202 | 3.999 | 0.801 |
| `vbr1_l1_programmable_gain_amplifier` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.798 | 0.664 | 1.201 |
| `vbr1_l1_programmable_gain_amplifier` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.798 | 1.967 | 0.405 |
| `vbr1_l1_programmable_gain_amplifier` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.138 | 0.664 | 4.726 |
| `vbr1_l1_programmable_gain_amplifier` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.138 | 1.967 | 1.595 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.813 | 1.950 | 0.417 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.813 | 9.464 | 0.086 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 5.893 | 1.950 | 3.022 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 5.893 | 9.464 | 0.623 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.613 | 0.394 | 1.556 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.613 | 0.419 | 1.463 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 2.956 | 0.394 | 7.509 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 2.956 | 0.419 | 7.058 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.864 | 1.229 | 0.703 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.864 | 1.107 | 0.780 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.336 | 1.229 | 2.714 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.336 | 1.107 | 3.013 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.689 | 0.620 | 1.113 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.689 | 0.726 | 0.950 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 2.145 | 0.620 | 3.462 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 2.145 | 0.726 | 2.956 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.948 | 0.595 | 1.592 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.948 | 1.046 | 0.906 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.736 | 0.595 | 6.274 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.736 | 1.046 | 3.570 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.671 | 0.463 | 1.449 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.671 | 0.386 | 1.737 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 2.372 | 0.463 | 5.124 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 2.372 | 0.386 | 6.144 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.868 | 0.901 | 0.964 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.868 | 0.791 | 1.097 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.251 | 0.901 | 3.610 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.251 | 0.791 | 4.111 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.824 | 1.278 | 0.644 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.824 | 1.122 | 0.734 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 1.814 | 1.278 | 1.419 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 1.814 | 1.122 | 1.616 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.733 | 0.553 | 1.326 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.733 | 0.530 | 1.384 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 1.982 | 0.553 | 3.585 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 1.982 | 0.530 | 3.741 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.751 | 0.536 | 1.403 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.751 | 0.931 | 0.808 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.335 | 0.536 | 6.225 |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.335 | 0.931 | 3.584 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 1.067 | 0.826 | 1.292 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 1.067 | 2.609 | 0.409 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.244 | 0.826 | 3.925 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.244 | 2.609 | 1.243 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.656 | 0.643 | 1.021 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.656 | 1.149 | 0.572 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.251 | 0.643 | 5.058 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.251 | 1.149 | 2.830 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.934 | 0.692 | 1.349 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.934 | 0.631 | 1.480 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.138 | 0.692 | 4.535 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.138 | 0.631 | 4.974 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 1.058 | 0.992 | 1.067 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 1.058 | 1.009 | 1.049 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.343 | 0.992 | 3.370 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.343 | 1.009 | 3.313 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 1.005 | 1.323 | 0.760 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 1.005 | 1.883 | 0.534 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 1.910 | 1.323 | 1.443 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 1.910 | 1.883 | 1.014 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.816 | 0.886 | 0.920 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.816 | 0.867 | 0.941 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.512 | 0.886 | 3.963 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.512 | 0.867 | 4.052 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 1.279 | 0.827 | 1.546 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 1.279 | 0.967 | 1.323 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.101 | 0.827 | 3.749 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.101 | 0.967 | 3.207 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.704 | 2.178 | 0.323 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.704 | 5.803 | 0.121 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.579 | 2.178 | 1.644 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.579 | 5.803 | 0.617 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 1.069 | 13.625 | 0.078 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 1.069 | 10.891 | 0.098 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.827 | 13.625 | 0.281 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.827 | 10.891 | 0.351 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.745 | 1.165 | 0.639 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.745 | 1.018 | 0.732 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.381 | 1.165 | 2.902 |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.381 | 1.018 | 3.321 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.873 | 1.021 | 0.855 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.873 | 0.800 | 1.092 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.766 | 1.021 | 3.687 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.766 | 0.800 | 4.709 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.748 | 0.712 | 1.050 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.748 | 1.532 | 0.488 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.847 | 0.712 | 5.403 |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.847 | 1.532 | 2.511 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.832 | 2.319 | 0.359 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.832 | 2.406 | 0.346 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.423 | 2.319 | 1.476 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.423 | 2.406 | 1.423 |
| `vbr1_l2_converter_static_linearity_measurement_flow` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.831 | 0.567 | 1.466 |
| `vbr1_l2_converter_static_linearity_measurement_flow` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.831 | 3.076 | 0.270 |
| `vbr1_l2_converter_static_linearity_measurement_flow` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.187 | 0.567 | 5.622 |
| `vbr1_l2_converter_static_linearity_measurement_flow` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.187 | 3.076 | 1.036 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 1.643 | 58.388 | 0.028 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 1.643 | 57.060 | 0.029 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 7.289 | 58.388 | 0.125 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 7.289 | 57.060 | 0.128 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 1.707 | 3.849 | 0.444 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 1.707 | 3.775 | 0.452 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.226 | 3.849 | 0.838 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.226 | 3.775 | 0.855 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 4.729 | 12.828 | 0.369 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 4.729 | 125.939 | 0.038 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 13.132 | 12.828 | 1.024 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 13.132 | 125.939 | 0.104 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 1.135 | 2.973 | 0.382 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 1.135 | 2.452 | 0.463 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.336 | 2.973 | 1.122 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.336 | 2.452 | 1.360 |
| `vbr1_l2_pipeline_adc_chain` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.813 | 1.558 | 0.522 |
| `vbr1_l2_pipeline_adc_chain` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.813 | 2.442 | 0.333 |
| `vbr1_l2_pipeline_adc_chain` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.801 | 1.558 | 2.439 |
| `vbr1_l2_pipeline_adc_chain` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.801 | 2.442 | 1.556 |
| `vbr1_l2_programmable_stimulus_sequencer` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.812 | 2.579 | 0.315 |
| `vbr1_l2_programmable_stimulus_sequencer` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.812 | 3.006 | 0.270 |
| `vbr1_l2_programmable_stimulus_sequencer` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.227 | 2.579 | 1.251 |
| `vbr1_l2_programmable_stimulus_sequencer` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.227 | 3.006 | 1.074 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 1.690 | 1.030 | 1.640 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 1.690 | 15.522 | 0.109 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 7.912 | 1.030 | 7.680 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 7.912 | 15.522 | 0.510 |

## Spectre-Equivalence-Gated Speedups

| Entry | Form | Variant | Spectre mode | EVAS mode | Spectre wall s | EVAS wall s | Spectre/EVAS |
| --- | --- | --- | --- | --- | ---: | ---: | ---: |
| `vbr1_l1_acquisition_limited_sample_and_hold` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.975 | 0.583 | 1.673 |
| `vbr1_l1_acquisition_limited_sample_and_hold` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.975 | 1.023 | 0.953 |
| `vbr1_l1_acquisition_limited_sample_and_hold` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.603 | 0.583 | 6.182 |
| `vbr1_l1_acquisition_limited_sample_and_hold` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.603 | 1.023 | 3.522 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 1.167 | 1.588 | 0.735 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 1.167 | 1.940 | 0.601 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.420 | 1.588 | 2.154 |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.420 | 1.940 | 1.763 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.882 | 2.735 | 0.323 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.882 | 2.807 | 0.314 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 4.004 | 2.735 | 1.464 |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 4.004 | 2.807 | 1.427 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.843 | 0.646 | 1.306 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.843 | 0.974 | 0.866 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.602 | 0.646 | 5.579 |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.602 | 0.974 | 3.697 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.915 | 0.505 | 1.811 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.915 | 1.186 | 0.771 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.602 | 0.505 | 7.127 |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.602 | 1.186 | 3.037 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.888 | 1.427 | 0.622 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.888 | 5.125 | 0.173 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.644 | 1.427 | 2.553 |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.644 | 5.125 | 0.711 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.904 | 0.595 | 1.518 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.904 | 1.578 | 0.573 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.740 | 0.595 | 6.281 |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.740 | 1.578 | 2.370 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.686 | 0.614 | 1.118 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.686 | 1.117 | 0.614 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 2.537 | 0.614 | 4.135 |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 2.537 | 1.117 | 2.271 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.797 | 0.470 | 1.694 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.797 | 0.340 | 2.342 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 2.196 | 0.470 | 4.666 |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 2.196 | 0.340 | 6.450 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.754 | 0.414 | 1.822 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.754 | 0.543 | 1.390 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.676 | 0.414 | 8.883 |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.676 | 0.543 | 6.775 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 1.036 | 0.524 | 1.976 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 1.036 | 0.586 | 1.768 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.697 | 0.524 | 7.051 |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.697 | 0.586 | 6.307 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.771 | 1.628 | 0.473 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.771 | 1.794 | 0.429 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.219 | 1.628 | 1.977 |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.219 | 1.794 | 1.794 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.729 | 0.370 | 1.969 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.729 | 0.400 | 1.820 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 2.078 | 0.370 | 5.616 |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 2.078 | 0.400 | 5.191 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 1.043 | 0.553 | 1.888 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 1.043 | 2.240 | 0.466 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 6.941 | 0.553 | 12.561 |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 6.941 | 2.240 | 3.098 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.816 | 1.191 | 0.685 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.816 | 4.517 | 0.181 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.391 | 1.191 | 2.848 |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.391 | 4.517 | 0.751 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.813 | 0.662 | 1.228 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.813 | 0.596 | 1.364 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.479 | 0.662 | 5.254 |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.479 | 0.596 | 5.837 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.827 | 1.490 | 0.555 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.827 | 1.622 | 0.510 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 2.200 | 1.490 | 1.476 |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 2.200 | 1.622 | 1.356 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 4.844 | 9.703 | 0.499 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 4.844 | 133.315 | 0.036 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 13.887 | 9.703 | 1.431 |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 13.887 | 133.315 | 0.104 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.771 | 4.208 | 0.183 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.771 | 1.270 | 0.607 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 2.420 | 4.208 | 0.575 |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 2.420 | 1.270 | 1.906 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 1.114 | 1.113 | 1.001 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 1.114 | 0.608 | 1.831 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 5.023 | 1.113 | 4.512 |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 5.023 | 0.608 | 8.258 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 1.003 | 4.172 | 0.240 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 1.003 | 5.370 | 0.187 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.478 | 4.172 | 0.834 |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.478 | 5.370 | 0.648 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.763 | 0.704 | 1.083 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.763 | 0.632 | 1.206 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.437 | 0.704 | 4.882 |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.437 | 0.632 | 5.435 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.729 | 0.512 | 1.423 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.729 | 1.173 | 0.621 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.291 | 0.512 | 6.427 |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.291 | 1.173 | 2.805 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 1.260 | 1.417 | 0.889 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 1.260 | 1.644 | 0.766 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 2.088 | 1.417 | 1.474 |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 2.088 | 1.644 | 1.270 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.753 | 0.904 | 0.833 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.753 | 0.578 | 1.302 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 2.210 | 0.904 | 2.444 |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 2.210 | 0.578 | 3.821 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.826 | 22.278 | 0.037 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.826 | 73.270 | 0.011 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.965 | 22.278 | 0.178 |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.965 | 73.270 | 0.054 |
| `vbr1_l1_pipeline_adc_stage` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.822 | 3.955 | 0.208 |
| `vbr1_l1_pipeline_adc_stage` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.822 | 3.870 | 0.212 |
| `vbr1_l1_pipeline_adc_stage` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.806 | 3.955 | 0.962 |
| `vbr1_l1_pipeline_adc_stage` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.806 | 3.870 | 0.983 |
| `vbr1_l1_precision_rectifier_envelope_detector` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.905 | 1.338 | 0.676 |
| `vbr1_l1_precision_rectifier_envelope_detector` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.905 | 3.999 | 0.226 |
| `vbr1_l1_precision_rectifier_envelope_detector` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.202 | 1.338 | 2.394 |
| `vbr1_l1_precision_rectifier_envelope_detector` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.202 | 3.999 | 0.801 |
| `vbr1_l1_programmable_gain_amplifier` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.798 | 0.664 | 1.201 |
| `vbr1_l1_programmable_gain_amplifier` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.798 | 1.967 | 0.405 |
| `vbr1_l1_programmable_gain_amplifier` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.138 | 0.664 | 4.726 |
| `vbr1_l1_programmable_gain_amplifier` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.138 | 1.967 | 1.595 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.813 | 1.950 | 0.417 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.813 | 9.464 | 0.086 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 5.893 | 1.950 | 3.022 |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 5.893 | 9.464 | 0.623 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.613 | 0.394 | 1.556 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.613 | 0.419 | 1.463 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 2.956 | 0.394 | 7.509 |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 2.956 | 0.419 | 7.058 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.864 | 1.229 | 0.703 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.864 | 1.107 | 0.780 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.336 | 1.229 | 2.714 |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.336 | 1.107 | 3.013 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.689 | 0.620 | 1.113 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.689 | 0.726 | 0.950 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 2.145 | 0.620 | 3.462 |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 2.145 | 0.726 | 2.956 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.948 | 0.595 | 1.592 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.948 | 1.046 | 0.906 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.736 | 0.595 | 6.274 |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.736 | 1.046 | 3.570 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.671 | 0.463 | 1.449 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.671 | 0.386 | 1.737 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 2.372 | 0.463 | 5.124 |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 2.372 | 0.386 | 6.144 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.868 | 0.901 | 0.964 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.868 | 0.791 | 1.097 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.251 | 0.901 | 3.610 |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.251 | 0.791 | 4.111 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.824 | 1.278 | 0.644 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.824 | 1.122 | 0.734 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 1.814 | 1.278 | 1.419 |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 1.814 | 1.122 | 1.616 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.733 | 0.553 | 1.326 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.733 | 0.530 | 1.384 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 1.982 | 0.553 | 3.585 |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 1.982 | 0.530 | 3.741 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 1.067 | 0.826 | 1.292 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 1.067 | 2.609 | 0.409 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.244 | 0.826 | 3.925 |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.244 | 2.609 | 1.243 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.656 | 0.643 | 1.021 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.656 | 1.149 | 0.572 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.251 | 0.643 | 5.058 |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.251 | 1.149 | 2.830 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.934 | 0.692 | 1.349 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.934 | 0.631 | 1.480 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.138 | 0.692 | 4.535 |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.138 | 0.631 | 4.974 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 1.058 | 0.992 | 1.067 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 1.058 | 1.009 | 1.049 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.343 | 0.992 | 3.370 |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.343 | 1.009 | 3.313 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 1.005 | 1.323 | 0.760 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 1.005 | 1.883 | 0.534 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 1.910 | 1.323 | 1.443 |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 1.910 | 1.883 | 1.014 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.816 | 0.886 | 0.920 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.816 | 0.867 | 0.941 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.512 | 0.886 | 3.963 |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.512 | 0.867 | 4.052 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 1.279 | 0.827 | 1.546 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 1.279 | 0.967 | 1.323 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.101 | 0.827 | 3.749 |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.101 | 0.967 | 3.207 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.704 | 2.178 | 0.323 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.704 | 5.803 | 0.121 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.579 | 2.178 | 1.644 |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.579 | 5.803 | 0.617 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 1.069 | 13.625 | 0.078 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 1.069 | 10.891 | 0.098 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.827 | 13.625 | 0.281 |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.827 | 10.891 | 0.351 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.873 | 1.021 | 0.855 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.873 | 0.800 | 1.092 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.766 | 1.021 | 3.687 |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.766 | 0.800 | 4.709 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.832 | 2.319 | 0.359 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.832 | 2.406 | 0.346 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.423 | 2.319 | 1.476 |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.423 | 2.406 | 1.423 |
| `vbr1_l2_converter_static_linearity_measurement_flow` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.831 | 0.567 | 1.466 |
| `vbr1_l2_converter_static_linearity_measurement_flow` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.831 | 3.076 | 0.270 |
| `vbr1_l2_converter_static_linearity_measurement_flow` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.187 | 0.567 | 5.622 |
| `vbr1_l2_converter_static_linearity_measurement_flow` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.187 | 3.076 | 1.036 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 1.643 | 58.388 | 0.028 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 1.643 | 57.060 | 0.029 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 7.289 | 58.388 | 0.125 |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 7.289 | 57.060 | 0.128 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 1.707 | 3.849 | 0.444 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 1.707 | 3.775 | 0.452 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.226 | 3.849 | 0.838 |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.226 | 3.775 | 0.855 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 4.729 | 12.828 | 0.369 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 4.729 | 125.939 | 0.038 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 13.132 | 12.828 | 1.024 |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 13.132 | 125.939 | 0.104 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 1.135 | 2.973 | 0.382 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 1.135 | 2.452 | 0.463 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.336 | 2.973 | 1.122 |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.336 | 2.452 | 1.360 |
| `vbr1_l2_pipeline_adc_chain` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.813 | 1.558 | 0.522 |
| `vbr1_l2_pipeline_adc_chain` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.813 | 2.442 | 0.333 |
| `vbr1_l2_pipeline_adc_chain` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.801 | 1.558 | 2.439 |
| `vbr1_l2_pipeline_adc_chain` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.801 | 2.442 | 1.556 |
| `vbr1_l2_programmable_stimulus_sequencer` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 0.812 | 2.579 | 0.315 |
| `vbr1_l2_programmable_stimulus_sequencer` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 0.812 | 3.006 | 0.270 |
| `vbr1_l2_programmable_stimulus_sequencer` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 3.227 | 2.579 | 1.251 |
| `vbr1_l2_programmable_stimulus_sequencer` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 3.227 | 3.006 | 1.074 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `profile_fast_skip_source_error_control` | 1.690 | 1.030 | 1.640 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `spectre_ax_equalized_precision` | `strict_current` | 1.690 | 15.522 | 0.109 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `spectre_reference_strict_primary` | `profile_fast_skip_source_error_control` | 7.912 | 1.030 | 7.680 |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `spectre_reference_strict_primary` | `strict_current` | 7.912 | 15.522 | 0.510 |

## Interpretation Guardrails

- Speedups use `simulation_ok`, so rows without a behavior checker can still contribute timing if the simulator produced waveforms.
- Equivalence-gated speedups require candidate behavior pass, strict-EVAS parity, and parity to every selected Spectre mode.
- `spectre/ax_speed` is the main fast Spectre speed baseline; `spectre/ax` remains a legacy alias for the same command-line preset.
- `spectre/ax_normalized` keeps `+preset=ax +mt` but rewrites the staged testbench to the shared precision settings before launch.
- `spectre/reference_strict_primary` uses the same staged `tran`/`simulatorOptions` settings without runner-added AX preset.
- `spectre/classic` is the stricter non-X reference path; AX/classic waveform differences are expected and should anchor EVAS tolerance rather than imply a single exact waveform truth.
- The waveform gate is an acceptance tolerance for Spectre-equivalent behavioral output, not a requirement that EVAS exceed Spectre precision.
- Cold Spectre runs include AHDL CMI compilation; warm-cache repetitions should be reported separately.
- A `BLOCKED` gate is not evidence of wrong behavior; it means the checker or reference evidence is incomplete.
