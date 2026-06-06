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
- EVAS modes: `strict_current, profile_fast_skip_source_error_control, profile_fast_rust_55, profile_fast_evas2`
- Spectre modes: ``
- Output root: `results/full-release-evas-py-rust-after-fixes-20260606`

## EVAS Mode Specs

| Mode | Phase | Default-off | Simulator options |
| --- | --- | --- | --- |
| `strict_current` | `P1` | `False` | - |
| `profile_fast_skip_source_error_control` | `P3` | `True` | `evas_profile=fast evas_skip_source_error_control=yes` |
| `profile_fast_rust_55` | `P11` | `True` | `evas_profile=fast evas_skip_source_error_control=yes evas_rust_full_model_fastpath=true evas_rust_required=true` |
| `profile_fast_evas2` | `EVAS2` | `True` | `evas_profile=fast evas_skip_source_error_control=yes evas_engine=evas2` |

## Mode Summary

| Backend | Mode | Runs | Sim OK | Behavior PASS | Behavior non-PASS | Total wall s | Mean wall s |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| evas | profile_fast_evas2 | 271 | 266 | 266 | 5 | 60.426 | 0.223 |
| evas | profile_fast_rust_55 | 271 | 271 | 271 | 0 | 60.426 | 0.223 |
| evas | profile_fast_skip_source_error_control | 271 | 271 | 271 | 0 | 98.839 | 0.365 |
| evas | strict_current | 271 | 271 | 271 | 0 | 597.444 | 2.205 |

## Checker Policy Summary

Behavior checkers are shared by EVAS and Spectre through the same checker id. `streaming_validated` means the checker uses a parity-validated streaming implementation; `row_based` means the legacy row-list implementation was used.

| Backend | Mode | Checker implementation | Rows |
| --- | --- | --- | ---: |
| evas | profile_fast_evas2 | `custom_noise` | 1 |
| evas | profile_fast_evas2 | `row_based` | 240 |
| evas | profile_fast_evas2 | `streaming_validated` | 30 |
| evas | profile_fast_rust_55 | `custom_noise` | 1 |
| evas | profile_fast_rust_55 | `row_based` | 240 |
| evas | profile_fast_rust_55 | `streaming_validated` | 30 |
| evas | profile_fast_skip_source_error_control | `custom_noise` | 1 |
| evas | profile_fast_skip_source_error_control | `row_based` | 240 |
| evas | profile_fast_skip_source_error_control | `streaming_validated` | 30 |
| evas | strict_current | `custom_noise` | 1 |
| evas | strict_current | `row_based` | 240 |
| evas | strict_current | `streaming_validated` | 30 |

## Spectre-Equivalence Gate Summary

These gates check whether EVAS preserves task behavior and stays within accepted Spectre-equivalent waveform tolerance. They are not a higher-than-Spectre precision target.

| EVAS mode | Runs | Gate PASS | Gate FAIL | Gate BLOCKED | Gate missing |
| --- | ---: | ---: | ---: | ---: | ---: |
| profile_fast_evas2 | 271 | 266 | 5 | 0 | 0 |
| profile_fast_rust_55 | 271 | 271 | 0 | 0 | 0 |
| profile_fast_skip_source_error_control | 271 | 271 | 0 | 0 | 0 |
| strict_current | 271 | 271 | 0 | 0 | 0 |

## Per-Row Spectre-Equivalence Gates

| Entry | Form | Variant | EVAS mode | Gate | Reasons | Blocked |
| --- | --- | --- | --- | --- | --- | --- |
| `vbr1_l1_acquisition_limited_sample_and_hold` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_acquisition_limited_sample_and_hold` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_acquisition_limited_sample_and_hold` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_acquisition_limited_sample_and_hold` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_acquisition_limited_sample_and_hold` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_acquisition_limited_sample_and_hold` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_acquisition_limited_sample_and_hold` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_acquisition_limited_sample_and_hold` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_acquisition_limited_sample_and_hold` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_acquisition_limited_sample_and_hold` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_acquisition_limited_sample_and_hold` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_acquisition_limited_sample_and_hold` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_acquisition_limited_sample_and_hold` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_acquisition_limited_sample_and_hold` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_acquisition_limited_sample_and_hold` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_acquisition_limited_sample_and_hold` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_aperture_delay_track_and_hold` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_aperture_delay_track_and_hold` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_aperture_delay_track_and_hold` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_aperture_delay_track_and_hold` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_bandgap_reference_macro_model` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_bandgap_reference_macro_model` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_bandgap_reference_macro_model` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_bandgap_reference_macro_model` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_bandgap_reference_macro_model` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_bandgap_reference_macro_model` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_bandgap_reference_macro_model` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_bandgap_reference_macro_model` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_bandgap_reference_macro_model` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_bandgap_reference_macro_model` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_bandgap_reference_macro_model` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_bandgap_reference_macro_model` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_bandgap_reference_macro_model` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_bandgap_reference_macro_model` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_bandgap_reference_macro_model` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_bandgap_reference_macro_model` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_bang_bang_phase_detector` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_bang_bang_phase_detector` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_bang_bang_phase_detector` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_bang_bang_phase_detector` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_bias_voltage_generator_with_enable_trim` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_bias_voltage_generator_with_enable_trim` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_bias_voltage_generator_with_enable_trim` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_bias_voltage_generator_with_enable_trim` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_bias_voltage_generator_with_enable_trim` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_bias_voltage_generator_with_enable_trim` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_bias_voltage_generator_with_enable_trim` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_bias_voltage_generator_with_enable_trim` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_bias_voltage_generator_with_enable_trim` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_bias_voltage_generator_with_enable_trim` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_bias_voltage_generator_with_enable_trim` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_bias_voltage_generator_with_enable_trim` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_bias_voltage_generator_with_enable_trim` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_bias_voltage_generator_with_enable_trim` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_bias_voltage_generator_with_enable_trim` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_bias_voltage_generator_with_enable_trim` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_binary_weighted_voltage_dac` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_binary_weighted_voltage_dac` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_binary_weighted_voltage_dac` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_binary_weighted_voltage_dac` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_burst_clock_source` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_burst_clock_source` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_burst_clock_source` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_calibration_deadband_controller` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_calibration_deadband_controller` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_calibration_deadband_controller` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_calibration_deadband_controller` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_capacitive_weighted_sar_feedback_dac` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_charge_pump_abstraction` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_charge_pump_abstraction` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_charge_pump_abstraction` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_charge_pump_abstraction` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_clock_divider` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_clock_divider` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clock_divider` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_clock_divider` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_clock_divider` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_clock_divider` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_clock_divider` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_clocked_adc_quantizer` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_clocked_adc_quantizer` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_clocked_adc_quantizer` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_clocked_adc_quantizer` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_clocked_sample_and_hold` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_clocked_sample_and_hold` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_clocked_sample_and_hold` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_clocked_sample_and_hold` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_crossing_metric_writer` | `dut` | `gold` | `profile_fast_evas2` | `FAIL` | candidate_simulation_not_ok, candidate_behavior_check_failed | reference_parity:missing csv |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_crossing_metric_writer` | `e2e` | `gold` | `profile_fast_evas2` | `FAIL` | candidate_simulation_not_ok, candidate_behavior_check_failed | reference_parity:missing csv |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_crossing_metric_writer` | `tb` | `gold` | `profile_fast_evas2` | `FAIL` | candidate_simulation_not_ok, candidate_behavior_check_failed | reference_parity:missing csv |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_dac_mismatch_unit_weighting_model` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_debounce_latch` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_debounce_latch` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_debounce_latch` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_debounce_latch` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_debounce_latch` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_debounce_latch` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_debounce_latch` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_dither_or_noise_like_deterministic_source` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_dwa_dem_encoder` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_dwa_dem_encoder` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_dwa_dem_encoder` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_dwa_dem_encoder` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_edge_interval_timer` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_edge_interval_timer` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_element_shuffler` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_element_shuffler` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_element_shuffler` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_element_shuffler` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_element_shuffler` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_element_shuffler` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_element_shuffler` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_first_order_lowpass` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_first_order_lowpass` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_first_order_lowpass` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_first_order_lowpass` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_gain_estimator` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_gain_estimator` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_gain_trim_controller` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_gain_trim_controller` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_gain_trim_controller` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_gain_trim_controller` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_higher_order_filter` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_higher_order_filter` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_higher_order_filter` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_higher_order_filter` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_higher_order_filter` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_higher_order_filter` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_higher_order_filter` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_hysteresis_comparator` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_hysteresis_comparator` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_hysteresis_comparator` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_hysteresis_comparator` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_ldo_regulator_macro_model` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_ldo_regulator_macro_model` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_ldo_regulator_macro_model` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_ldo_regulator_macro_model` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_ldo_regulator_macro_model` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_ldo_regulator_macro_model` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_ldo_regulator_macro_model` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_ldo_regulator_macro_model` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_ldo_regulator_macro_model` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_ldo_regulator_macro_model` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_ldo_regulator_macro_model` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_ldo_regulator_macro_model` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_ldo_regulator_macro_model` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_ldo_regulator_macro_model` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_ldo_regulator_macro_model` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_ldo_regulator_macro_model` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_lfsr_prbs_generator` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_lfsr_prbs_generator` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_lfsr_prbs_generator` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_lfsr_prbs_generator` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_limiting_amplifier_frontend` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_limiting_amplifier_frontend` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_limiting_amplifier_frontend` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_limiting_amplifier_frontend` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_limiting_amplifier_frontend` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_limiting_amplifier_frontend` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_limiting_amplifier_frontend` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_limiting_amplifier_frontend` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_limiting_amplifier_frontend` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_limiting_amplifier_frontend` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_limiting_amplifier_frontend` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_limiting_amplifier_frontend` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_limiting_amplifier_frontend` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_limiting_amplifier_frontend` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_limiting_amplifier_frontend` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_limiting_amplifier_frontend` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_lna_gain_compression_macro` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_lna_gain_compression_macro` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_lna_gain_compression_macro` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_lna_gain_compression_macro` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_lna_gain_compression_macro` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_lna_gain_compression_macro` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_lna_gain_compression_macro` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_lna_gain_compression_macro` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_lna_gain_compression_macro` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_lna_gain_compression_macro` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_lna_gain_compression_macro` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_lna_gain_compression_macro` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_lna_gain_compression_macro` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_lna_gain_compression_macro` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_lna_gain_compression_macro` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_lna_gain_compression_macro` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_lock_detector` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_lock_detector` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_lock_detector` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_lock_detector` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_lock_detector` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_lock_detector` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_lock_detector` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_log_rssi_power_detector` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_log_rssi_power_detector` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_log_rssi_power_detector` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_log_rssi_power_detector` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_log_rssi_power_detector` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_log_rssi_power_detector` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_log_rssi_power_detector` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_log_rssi_power_detector` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_log_rssi_power_detector` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_log_rssi_power_detector` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_log_rssi_power_detector` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_log_rssi_power_detector` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_log_rssi_power_detector` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_log_rssi_power_detector` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_log_rssi_power_detector` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_log_rssi_power_detector` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_loop_filter_abstraction` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_loop_filter_abstraction` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_loop_filter_abstraction` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_loop_filter_abstraction` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_offset_comparator` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_offset_comparator` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_offset_comparator` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_offset_comparator` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_offset_comparator` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_offset_comparator` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_offset_comparator` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_pa_compression_macro` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_pa_compression_macro` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_pa_compression_macro` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_pa_compression_macro` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_pa_compression_macro` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_pa_compression_macro` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_pa_compression_macro` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_pa_compression_macro` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_pa_compression_macro` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_pa_compression_macro` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_pa_compression_macro` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_pa_compression_macro` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_pa_compression_macro` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_pa_compression_macro` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_pa_compression_macro` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_pa_compression_macro` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_peak_detector` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_peak_detector` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_peak_detector` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_peak_detector` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_peak_detector` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_peak_detector` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_peak_detector` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_pfd_up_dn_logic` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_pfd_up_dn_logic` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_pfd_up_dn_logic` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_pfd_up_dn_logic` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_pipeline_adc_stage` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_pipeline_adc_stage` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_pipeline_adc_stage` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_pipeline_adc_stage` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_pipeline_adc_stage` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_pipeline_adc_stage` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_pipeline_adc_stage` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_pipeline_adc_stage` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_pipeline_adc_stage` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_pipeline_adc_stage` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_pipeline_adc_stage` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_pipeline_adc_stage` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_pipeline_adc_stage` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_pipeline_adc_stage` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_pipeline_adc_stage` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_pipeline_adc_stage` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_power_on_reset_detector` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_power_on_reset_detector` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_power_on_reset_detector` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_power_on_reset_detector` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_power_on_reset_detector` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_power_on_reset_detector` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_power_on_reset_detector` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_power_on_reset_detector` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_power_on_reset_detector` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_power_on_reset_detector` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_power_on_reset_detector` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_power_on_reset_detector` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_power_on_reset_detector` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_power_on_reset_detector` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_power_on_reset_detector` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_power_on_reset_detector` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_precision_rectifier_envelope_detector` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_precision_rectifier_envelope_detector` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_precision_rectifier_envelope_detector` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_precision_rectifier_envelope_detector` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_precision_rectifier_envelope_detector` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_precision_rectifier_envelope_detector` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_precision_rectifier_envelope_detector` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_precision_rectifier_envelope_detector` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_precision_rectifier_envelope_detector` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_precision_rectifier_envelope_detector` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_precision_rectifier_envelope_detector` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_precision_rectifier_envelope_detector` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_precision_rectifier_envelope_detector` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_precision_rectifier_envelope_detector` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_precision_rectifier_envelope_detector` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_precision_rectifier_envelope_detector` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_programmable_gain_amplifier` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_programmable_gain_amplifier` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_programmable_gain_amplifier` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_programmable_gain_amplifier` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_programmable_gain_amplifier` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_programmable_gain_amplifier` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_programmable_gain_amplifier` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_programmable_gain_amplifier` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_programmable_gain_amplifier` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_programmable_gain_amplifier` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_programmable_gain_amplifier` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_programmable_gain_amplifier` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_programmable_gain_amplifier` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_programmable_gain_amplifier` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_programmable_gain_amplifier` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_programmable_gain_amplifier` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_propagation_delay_comparator` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_propagation_delay_comparator` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_propagation_delay_comparator` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_propagation_delay_comparator` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_ptat_ctat_reference_generator` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_ptat_ctat_reference_generator` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_ptat_ctat_reference_generator` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_ptat_ctat_reference_generator` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_ptat_ctat_reference_generator` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_ptat_ctat_reference_generator` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_ptat_ctat_reference_generator` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_ptat_ctat_reference_generator` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_ptat_ctat_reference_generator` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_ptat_ctat_reference_generator` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_ptat_ctat_reference_generator` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_ptat_ctat_reference_generator` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_ptat_ctat_reference_generator` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_ptat_ctat_reference_generator` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_ptat_ctat_reference_generator` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_ptat_ctat_reference_generator` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_ramp_or_step_source` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_ramp_or_step_source` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_ramp_or_step_source` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_resettable_integrator` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_resettable_integrator` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_resettable_integrator` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_resettable_integrator` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_resettable_integrator` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_resettable_integrator` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_resettable_integrator` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_rf_mixer_downconverter_macro` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_rf_mixer_downconverter_macro` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_rf_mixer_downconverter_macro` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_rf_mixer_downconverter_macro` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_rf_mixer_downconverter_macro` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_rf_mixer_downconverter_macro` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_rf_mixer_downconverter_macro` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_rf_mixer_downconverter_macro` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_rf_mixer_downconverter_macro` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_rf_mixer_downconverter_macro` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_rf_mixer_downconverter_macro` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_rf_mixer_downconverter_macro` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_rf_mixer_downconverter_macro` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_rf_mixer_downconverter_macro` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_rf_mixer_downconverter_macro` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_rf_mixer_downconverter_macro` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_sample_and_hold_with_droop_leakage` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_sar_logic` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_sar_logic` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_sar_logic` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_sar_logic` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_sar_logic` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_sar_logic` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_sar_logic` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_segmented_dac` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_segmented_dac` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_segmented_dac` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_segmented_dac` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_segmented_dac` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_segmented_dac` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_segmented_dac` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_settling_time_detector` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_settling_time_detector` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_sine_periodic_voltage_source` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_sine_periodic_voltage_source` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_sine_periodic_voltage_source` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_slew_rate_limiter` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_slew_rate_limiter` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_slew_rate_limiter` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_slew_rate_limiter` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_soft_hysteretic_limiter` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_soft_hysteretic_limiter` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_soft_hysteretic_limiter` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_soft_hysteretic_limiter` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_strongarm_style_latch_comparator` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_successive_approximation_calibration_search_fsm` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_thermometer_code_decoder` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_thermometer_code_decoder` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_thermometer_code_decoder` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_thermometer_code_decoder` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_threshold_comparator` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_threshold_comparator` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_threshold_comparator` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_threshold_comparator` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_threshold_comparator` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_threshold_comparator` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_threshold_comparator` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_trim_calibration_controller` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_trim_calibration_controller` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_trim_calibration_controller` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_trim_calibration_controller` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_unit_element_thermometer_dac` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_unit_element_thermometer_dac` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_unit_element_thermometer_dac` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_unit_element_thermometer_dac` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_uvlo_brownout_detector` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_uvlo_brownout_detector` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_uvlo_brownout_detector` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_uvlo_brownout_detector` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_uvlo_brownout_detector` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_uvlo_brownout_detector` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_uvlo_brownout_detector` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_uvlo_brownout_detector` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_uvlo_brownout_detector` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_uvlo_brownout_detector` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_uvlo_brownout_detector` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_uvlo_brownout_detector` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_uvlo_brownout_detector` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_uvlo_brownout_detector` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_uvlo_brownout_detector` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_uvlo_brownout_detector` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_vco_phase_integrator` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_vco_phase_integrator` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_vco_phase_integrator` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_vco_phase_integrator` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_window_comparator_detector` | `bugfix` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_window_comparator_detector` | `dut` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_window_comparator_detector` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l1_window_comparator_detector` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l2_agc_receiver_leveling_loop` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_agc_receiver_leveling_loop` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_agc_receiver_leveling_loop` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l2_agc_receiver_leveling_loop` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l2_agc_receiver_leveling_loop` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_agc_receiver_leveling_loop` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_agc_receiver_leveling_loop` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l2_agc_receiver_leveling_loop` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l2_amplifier_filter_chain` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l2_amplifier_filter_chain` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l2_comparator_measurement_flow` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l2_comparator_measurement_flow` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l2_complete_calibration_loop` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l2_complete_calibration_loop` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l2_converter_front_end` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l2_converter_front_end` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l2_converter_static_linearity_measurement_flow` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_converter_static_linearity_measurement_flow` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_converter_static_linearity_measurement_flow` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l2_converter_static_linearity_measurement_flow` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l2_converter_static_linearity_measurement_flow` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_converter_static_linearity_measurement_flow` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_converter_static_linearity_measurement_flow` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l2_converter_static_linearity_measurement_flow` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l2_flash_adc_mini_array` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l2_flash_adc_mini_array` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l2_iq_downconversion_chain` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_iq_downconversion_chain` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_iq_downconversion_chain` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l2_iq_downconversion_chain` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l2_iq_downconversion_chain` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_iq_downconversion_chain` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_iq_downconversion_chain` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l2_iq_downconversion_chain` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l2_ldo_load_step_recovery_flow` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_ldo_load_step_recovery_flow` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_ldo_load_step_recovery_flow` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l2_ldo_load_step_recovery_flow` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l2_ldo_load_step_recovery_flow` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_ldo_load_step_recovery_flow` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_ldo_load_step_recovery_flow` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l2_ldo_load_step_recovery_flow` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l2_measurement_flow` | `e2e` | `gold` | `profile_fast_evas2` | `FAIL` | candidate_simulation_not_ok, candidate_behavior_check_failed | reference_parity:missing csv |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l2_measurement_flow` | `tb` | `gold` | `profile_fast_evas2` | `FAIL` | candidate_simulation_not_ok, candidate_behavior_check_failed | reference_parity:missing csv |
| `vbr1_l2_pipeline_adc_chain` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_pipeline_adc_chain` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_pipeline_adc_chain` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l2_pipeline_adc_chain` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l2_pipeline_adc_chain` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_pipeline_adc_chain` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_pipeline_adc_chain` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l2_pipeline_adc_chain` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l2_programmable_stimulus_sequencer` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_programmable_stimulus_sequencer` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_programmable_stimulus_sequencer` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l2_programmable_stimulus_sequencer` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l2_programmable_stimulus_sequencer` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_programmable_stimulus_sequencer` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_programmable_stimulus_sequencer` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l2_programmable_stimulus_sequencer` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l2_reference_startup_enable_flow` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_reference_startup_enable_flow` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_reference_startup_enable_flow` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l2_reference_startup_enable_flow` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l2_reference_startup_enable_flow` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_reference_startup_enable_flow` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_reference_startup_enable_flow` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l2_reference_startup_enable_flow` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `e2e` | `gold` | `profile_fast_evas2` | `PASS` | - | - |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `strict_current` | `PASS` | - | - |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `profile_fast_skip_source_error_control` | `PASS` | - | - |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `profile_fast_rust_55` | `PASS` | - | - |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `tb` | `gold` | `profile_fast_evas2` | `PASS` | - | - |

## E2E Wall-Time Speedups

The primary `wall_time_s` now uses the same evaluator E2E boundary for both EVAS and Spectre: fixture materialization/staging, simulator subprocess, conversion/parsing, checker, and validation. Use `simulator_subprocess_wall_s` or `timing_split` for simulator-only analysis.

| Entry | Form | Variant | Spectre mode | EVAS mode | Spectre wall s | EVAS wall s | Spectre/EVAS |
| --- | --- | --- | --- | --- | ---: | ---: | ---: |

## Timing Split Totals

These totals explain what is inside the unified E2E wall time. EVAS `run_case_*` fields come from `simulate_evas.run_case`; Spectre fields come from the direct Spectre runner.

| Backend | Mode | Field | Total s | Mean s |
| --- | --- | --- | ---: | ---: |
| evas | profile_fast_evas2 | `evaluator_e2e_wall_s` | 60.425742 | 0.222973 |
| evas | profile_fast_evas2 | `fixture_materialize_s` | 2.075648 | 0.007659 |
| evas | profile_fast_evas2 | `run_case_behavior_checker_s` | 48.788345 | 0.183415 |
| evas | profile_fast_evas2 | `run_case_copy_inputs_s` | 0.470801 | 0.001737 |
| evas | profile_fast_evas2 | `run_case_evas_reported_total_elapsed_s` | 3.300000 | 0.012406 |
| evas | profile_fast_evas2 | `run_case_evas_reported_tran_elapsed_s` | 2.725900 | 0.010248 |
| evas | profile_fast_evas2 | `run_case_evas_runner_csv_write_s` | 1.347043 | 0.005064 |
| evas | profile_fast_evas2 | `run_case_evas_runner_derive_bus_signals_s` | 0.005905 | 0.000022 |
| evas | profile_fast_evas2 | `run_case_evas_subprocess_unattributed_s` | 5.152590 | 0.020945 |
| evas | profile_fast_evas2 | `run_case_evas_subprocess_wall_s` | 7.899667 | 0.029150 |
| evas | profile_fast_evas2 | `run_case_metric_cleanup_s` | 0.001719 | 0.000006 |
| evas | profile_fast_evas2 | `run_case_outer_wall_s` | 58.330389 | 0.215241 |
| evas | profile_fast_evas2 | `run_case_output_setup_s` | 0.118495 | 0.000437 |
| evas | profile_fast_evas2 | `run_case_preflight_s` | 0.142159 | 0.000525 |
| evas | profile_fast_evas2 | `run_case_required_trace_signal_count` | 172.000000 | 5.931034 |
| evas | profile_fast_evas2 | `run_case_run_case_wall_s` | 58.326658 | 0.215228 |
| evas | profile_fast_evas2 | `run_case_side_output_validation_s` | 0.000835 | 0.000003 |
| evas | profile_fast_evas2 | `run_case_temp_cleanup_s` | 0.223118 | 0.000823 |
| evas | profile_fast_evas2 | `run_case_tempdir_create_s` | 0.080627 | 0.000298 |
| evas | profile_fast_rust_55 | `evaluator_e2e_wall_s` | 60.425852 | 0.222974 |
| evas | profile_fast_rust_55 | `fixture_materialize_s` | 1.884411 | 0.006954 |
| evas | profile_fast_rust_55 | `run_case_behavior_checker_s` | 49.116438 | 0.181241 |
| evas | profile_fast_rust_55 | `run_case_copy_inputs_s` | 0.432468 | 0.001596 |
| evas | profile_fast_rust_55 | `run_case_evas_reported_total_elapsed_s` | 3.300000 | 0.012177 |
| evas | profile_fast_rust_55 | `run_case_evas_reported_tran_elapsed_s` | 2.867800 | 0.010582 |
| evas | profile_fast_rust_55 | `run_case_evas_runner_csv_write_s` | 1.288153 | 0.004753 |
| evas | profile_fast_rust_55 | `run_case_evas_runner_derive_bus_signals_s` | 0.005761 | 0.000021 |
| evas | profile_fast_rust_55 | `run_case_evas_subprocess_unattributed_s` | 5.145244 | 0.020581 |
| evas | profile_fast_rust_55 | `run_case_evas_subprocess_wall_s` | 7.806147 | 0.028805 |
| evas | profile_fast_rust_55 | `run_case_metric_cleanup_s` | 0.001383 | 0.000005 |
| evas | profile_fast_rust_55 | `run_case_outer_wall_s` | 58.522906 | 0.215952 |
| evas | profile_fast_rust_55 | `run_case_output_setup_s` | 0.094055 | 0.000347 |
| evas | profile_fast_rust_55 | `run_case_preflight_s` | 0.120568 | 0.000445 |
| evas | profile_fast_rust_55 | `run_case_required_trace_signal_count` | 172.000000 | 5.931034 |
| evas | profile_fast_rust_55 | `run_case_run_case_wall_s` | 58.519269 | 0.215938 |
| evas | profile_fast_rust_55 | `run_case_side_output_validation_s` | 0.005141 | 0.000019 |
| evas | profile_fast_rust_55 | `run_case_temp_cleanup_s` | 0.290688 | 0.001073 |
| evas | profile_fast_rust_55 | `run_case_tempdir_create_s` | 0.069771 | 0.000257 |
| evas | profile_fast_skip_source_error_control | `evaluator_e2e_wall_s` | 98.839202 | 0.364720 |
| evas | profile_fast_skip_source_error_control | `fixture_materialize_s` | 1.938255 | 0.007152 |
| evas | profile_fast_skip_source_error_control | `run_case_behavior_checker_s` | 54.072872 | 0.199531 |
| evas | profile_fast_skip_source_error_control | `run_case_copy_inputs_s` | 0.436794 | 0.001612 |
| evas | profile_fast_skip_source_error_control | `run_case_evas_reported_total_elapsed_s` | 36.800000 | 0.135793 |
| evas | profile_fast_skip_source_error_control | `run_case_evas_reported_tran_elapsed_s` | 36.135200 | 0.133340 |
| evas | profile_fast_skip_source_error_control | `run_case_evas_runner_csv_write_s` | 1.429600 | 0.005275 |
| evas | profile_fast_skip_source_error_control | `run_case_evas_runner_derive_bus_signals_s` | 0.007058 | 0.000026 |
| evas | profile_fast_skip_source_error_control | `run_case_evas_subprocess_unattributed_s` | 6.033412 | 0.027932 |
| evas | profile_fast_skip_source_error_control | `run_case_evas_subprocess_wall_s` | 41.305155 | 0.152418 |
| evas | profile_fast_skip_source_error_control | `run_case_metric_cleanup_s` | 0.001234 | 0.000005 |
| evas | profile_fast_skip_source_error_control | `run_case_outer_wall_s` | 96.882375 | 0.357500 |
| evas | profile_fast_skip_source_error_control | `run_case_output_setup_s` | 0.088711 | 0.000327 |
| evas | profile_fast_skip_source_error_control | `run_case_preflight_s` | 0.116286 | 0.000429 |
| evas | profile_fast_skip_source_error_control | `run_case_required_trace_signal_count` | 172.000000 | 5.931034 |
| evas | profile_fast_skip_source_error_control | `run_case_run_case_wall_s` | 96.878897 | 0.357487 |
| evas | profile_fast_skip_source_error_control | `run_case_side_output_validation_s` | 0.004765 | 0.000018 |
| evas | profile_fast_skip_source_error_control | `run_case_temp_cleanup_s` | 0.221745 | 0.000818 |
| evas | profile_fast_skip_source_error_control | `run_case_tempdir_create_s` | 0.069209 | 0.000255 |
| evas | strict_current | `evaluator_e2e_wall_s` | 597.443547 | 2.204589 |
| evas | strict_current | `fixture_materialize_s` | 2.510464 | 0.009264 |
| evas | strict_current | `run_case_behavior_checker_s` | 51.804352 | 0.191160 |
| evas | strict_current | `run_case_copy_inputs_s` | 0.480392 | 0.001773 |
| evas | strict_current | `run_case_evas_reported_total_elapsed_s` | 539.300000 | 1.990037 |
| evas | strict_current | `run_case_evas_reported_tran_elapsed_s` | 535.216800 | 1.974970 |
| evas | strict_current | `run_case_evas_runner_csv_write_s` | 1.393332 | 0.005141 |
| evas | strict_current | `run_case_evas_runner_derive_bus_signals_s` | 0.007981 | 0.000029 |
| evas | strict_current | `run_case_evas_subprocess_unattributed_s` | 4.639366 | 0.031137 |
| evas | strict_current | `run_case_evas_subprocess_wall_s` | 541.312833 | 1.997464 |
| evas | strict_current | `run_case_metric_cleanup_s` | 0.001335 | 0.000005 |
| evas | strict_current | `run_case_outer_wall_s` | 594.910437 | 2.195241 |
| evas | strict_current | `run_case_output_setup_s` | 0.258378 | 0.000953 |
| evas | strict_current | `run_case_preflight_s` | 0.139547 | 0.000515 |
| evas | strict_current | `run_case_required_trace_signal_count` | 172.000000 | 5.931034 |
| evas | strict_current | `run_case_run_case_wall_s` | 594.906056 | 2.195225 |
| evas | strict_current | `run_case_side_output_validation_s` | 0.005346 | 0.000020 |
| evas | strict_current | `run_case_temp_cleanup_s` | 0.236357 | 0.000872 |
| evas | strict_current | `run_case_tempdir_create_s` | 0.083923 | 0.000310 |

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
