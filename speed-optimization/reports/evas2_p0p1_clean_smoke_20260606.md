# EVAS/Spectre Speed

Date: 2026-06-06
Claim allowed: `False`
Reason: Same-server timing is measured directly on one host and the artifact emits checker/waveform Spectre-equivalence gates. Paper-facing speed claims should use only equivalence-gated rows and still need repeated cold/warm runs.

## Scope

- Host: `BucketsrandeMacBook-Air.local`
- Spectre backend: `local`
- SUI host: `-`
- SUI work root: `-`
- Cadence cshrc: `-`
- Selected rows: 271
- Jobs: 1
- EVAS modes: `profile_fast_evas2`
- Spectre modes: ``
- Output root: `results/evas2-p0p1-clean-smoke-20260606`

## EVAS Mode Specs

| Mode | Phase | Default-off | Simulator options |
| --- | --- | --- | --- |
| `profile_fast_evas2` | `EVAS2` | `True` | `evas_profile=fast evas_skip_source_error_control=yes evas_engine=evas2` |

## Mode Summary

| Backend | Mode | Runs | Sim OK | Behavior PASS | Behavior non-PASS | Total wall s | Mean wall s |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| evas | profile_fast_evas2 | 271 | 271 | 271 | 0 | 225.978 | 0.834 |

## Checker Policy Summary

Behavior checkers are shared by EVAS and Spectre through the same checker id. `streaming_validated` means the checker uses a parity-validated streaming implementation; `row_based` means the legacy row-list implementation was used.

| Backend | Mode | Checker implementation | Rows |
| --- | --- | --- | ---: |
| evas | profile_fast_evas2 | `custom_noise` | 1 |
| evas | profile_fast_evas2 | `row_based` | 232 |
| evas | profile_fast_evas2 | `streaming_validated` | 38 |

## Spectre-Equivalence Gate Summary

These gates check whether EVAS preserves task behavior and stays within accepted Spectre-equivalent waveform tolerance. They are not a higher-than-Spectre precision target.

| EVAS mode | Runs | Gate PASS | Gate FAIL | Gate BLOCKED | Gate missing |
| --- | ---: | ---: | ---: | ---: | ---: |
| profile_fast_evas2 | 271 | 0 | 0 | 271 | 0 |

## Per-Row Spectre-Equivalence Gates

| Entry | Form | Variant | EVAS mode | Gate | Reasons | Blocked |
| --- | --- | --- | --- | --- | --- | --- |
| `vbr1_l1_acquisition_limited_sample_and_hold` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_acquisition_limited_sample_and_hold` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_acquisition_limited_sample_and_hold` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_acquisition_limited_sample_and_hold` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_bandgap_reference_macro_model` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_bandgap_reference_macro_model` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_bandgap_reference_macro_model` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_bandgap_reference_macro_model` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_bias_voltage_generator_with_enable_trim` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_bias_voltage_generator_with_enable_trim` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_bias_voltage_generator_with_enable_trim` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_bias_voltage_generator_with_enable_trim` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_clock_divider` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_debounce_latch` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_element_shuffler` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_higher_order_filter` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_ldo_regulator_macro_model` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_ldo_regulator_macro_model` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_ldo_regulator_macro_model` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_ldo_regulator_macro_model` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_limiting_amplifier_frontend` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_limiting_amplifier_frontend` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_limiting_amplifier_frontend` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_limiting_amplifier_frontend` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_lna_gain_compression_macro` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_lna_gain_compression_macro` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_lna_gain_compression_macro` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_lna_gain_compression_macro` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_lock_detector` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_log_rssi_power_detector` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_log_rssi_power_detector` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_log_rssi_power_detector` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_log_rssi_power_detector` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_offset_comparator` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_pa_compression_macro` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_pa_compression_macro` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_pa_compression_macro` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_pa_compression_macro` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_peak_detector` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_pipeline_adc_stage` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_pipeline_adc_stage` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_pipeline_adc_stage` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_pipeline_adc_stage` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_power_on_reset_detector` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_power_on_reset_detector` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_power_on_reset_detector` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_power_on_reset_detector` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_precision_rectifier_envelope_detector` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_precision_rectifier_envelope_detector` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_precision_rectifier_envelope_detector` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_precision_rectifier_envelope_detector` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_programmable_gain_amplifier` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_programmable_gain_amplifier` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_programmable_gain_amplifier` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_programmable_gain_amplifier` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_ptat_ctat_reference_generator` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_ptat_ctat_reference_generator` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_ptat_ctat_reference_generator` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_ptat_ctat_reference_generator` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_resettable_integrator` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_rf_mixer_downconverter_macro` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_rf_mixer_downconverter_macro` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_rf_mixer_downconverter_macro` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_rf_mixer_downconverter_macro` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_sar_logic` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_segmented_dac` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_threshold_comparator` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_uvlo_brownout_detector` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_uvlo_brownout_detector` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_uvlo_brownout_detector` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_uvlo_brownout_detector` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l2_agc_receiver_leveling_loop` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l2_agc_receiver_leveling_loop` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l2_converter_static_linearity_measurement_flow` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l2_converter_static_linearity_measurement_flow` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l2_iq_downconversion_chain` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l2_iq_downconversion_chain` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l2_ldo_load_step_recovery_flow` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l2_ldo_load_step_recovery_flow` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l2_pipeline_adc_chain` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l2_pipeline_adc_chain` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l2_programmable_stimulus_sequencer` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l2_programmable_stimulus_sequencer` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l2_reference_startup_enable_flow` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l2_reference_startup_enable_flow` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `profile_fast_evas2` | `BLOCKED` | - | reference_parity:missing strict_current EVAS or Spectre strict reference |

## E2E Wall-Time Speedups

The primary `wall_time_s` now uses the same evaluator E2E boundary for both EVAS and Spectre: fixture materialization/staging, simulator subprocess, conversion/parsing, checker, and validation. Use `simulator_subprocess_wall_s` or `timing_split` for simulator-only analysis.

| Entry | Form | Variant | Spectre mode | EVAS mode | Spectre wall s | EVAS wall s | Spectre/EVAS |
| --- | --- | --- | --- | --- | ---: | ---: | ---: |

## Timing Split Totals

These totals explain what is inside the unified E2E wall time. EVAS `run_case_*` fields come from `simulate_evas.run_case`; Spectre fields come from the direct Spectre runner.

| Backend | Mode | Field | Total s | Mean s |
| --- | --- | --- | ---: | ---: |
| evas | profile_fast_evas2 | `evaluator_e2e_wall_s` | 225.978234 | 0.833868 |
| evas | profile_fast_evas2 | `fixture_materialize_s` | 4.398577 | 0.016231 |
| evas | profile_fast_evas2 | `run_case_behavior_checker_s` | 54.433744 | 0.200863 |
| evas | profile_fast_evas2 | `run_case_copy_inputs_s` | 0.784744 | 0.002896 |
| evas | profile_fast_evas2 | `run_case_evas_reported_total_elapsed_s` | 5.900000 | 0.021771 |
| evas | profile_fast_evas2 | `run_case_evas_reported_tran_elapsed_s` | 4.187300 | 0.015451 |
| evas | profile_fast_evas2 | `run_case_evas_runner_csv_write_s` | 1.976157 | 0.007292 |
| evas | profile_fast_evas2 | `run_case_evas_runner_derive_bus_signals_s` | 0.055099 | 0.000203 |
| evas | profile_fast_evas2 | `run_case_evas_subprocess_unattributed_s` | 156.983681 | 0.579276 |
| evas | profile_fast_evas2 | `run_case_evas_subprocess_wall_s` | 162.883681 | 0.601047 |
| evas | profile_fast_evas2 | `run_case_metric_cleanup_s` | 0.002139 | 0.000008 |
| evas | profile_fast_evas2 | `run_case_outer_wall_s` | 221.541219 | 0.817495 |
| evas | profile_fast_evas2 | `run_case_output_setup_s` | 0.378865 | 0.001398 |
| evas | profile_fast_evas2 | `run_case_preflight_s` | 0.186212 | 0.000687 |
| evas | profile_fast_evas2 | `run_case_required_trace_signal_count` | 1359.000000 | 5.502024 |
| evas | profile_fast_evas2 | `run_case_run_case_wall_s` | 221.518210 | 0.817410 |
| evas | profile_fast_evas2 | `run_case_side_output_validation_s` | 0.016200 | 0.000060 |
| evas | profile_fast_evas2 | `run_case_temp_cleanup_s` | 0.362648 | 0.001338 |
| evas | profile_fast_evas2 | `run_case_tempdir_create_s` | 0.126057 | 0.000465 |

## Spectre-Equivalence-Gated Speedups

| Entry | Form | Variant | Spectre mode | EVAS mode | Spectre wall s | EVAS wall s | Spectre/EVAS |
| --- | --- | --- | --- | --- | ---: | ---: | ---: |

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
