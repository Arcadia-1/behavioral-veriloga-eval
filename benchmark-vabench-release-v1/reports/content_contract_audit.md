# vaBench Content Contract Audit

Date: 2026-05-26

This report audits benchmark content semantics before model baselines or
paper-facing benchmark claims. EVAS/Spectre certification proves simulator
agreement, but this report asks whether the public task, checker, and gold
source describe the same circuit function.

## Summary

| Metric | Value |
| --- | ---: |
| status | `pass` |
| release entries | 79 |
| release forms | 271 |
| core entries | 66 |
| support entries | 13 |
| content denominator entries | 66 |
| content denominator forms | 236 |
| content-excluded entries | 13 |
| INFO findings | 13 |

## Findings

| Severity | Kind | Entry | Form | Message |
| --- | --- | --- | --- | --- |
| INFO | `content_denominator_excluded_entry` | `vbr1_l1_crossing_metric_writer` | `-` | entry remains in the package as traceable material but is excluded from strong content claims |
| INFO | `content_denominator_excluded_entry` | `vbr1_l1_edge_interval_timer` | `-` | entry remains in the package as traceable material but is excluded from strong content claims |
| INFO | `content_denominator_excluded_entry` | `vbr1_l1_gain_estimator` | `-` | entry remains in the package as traceable material but is excluded from strong content claims |
| INFO | `content_denominator_excluded_entry` | `vbr1_l1_peak_detector` | `-` | entry remains in the package as traceable material but is excluded from strong content claims |
| INFO | `content_denominator_excluded_entry` | `vbr1_l1_settling_time_detector` | `-` | entry remains in the package as traceable material but is excluded from strong content claims |
| INFO | `content_denominator_excluded_entry` | `vbr1_l2_gain_extraction_convergence_measurement_flow` | `-` | entry remains in the package as traceable material but is excluded from strong content claims |
| INFO | `content_denominator_excluded_entry` | `vbr1_l2_measurement_flow` | `-` | entry remains in the package as traceable material but is excluded from strong content claims |
| INFO | `content_denominator_excluded_entry` | `vbr1_l1_burst_clock_source` | `-` | entry remains in the package as traceable material but is excluded from strong content claims |
| INFO | `content_denominator_excluded_entry` | `vbr1_l1_dither_or_noise_like_deterministic_source` | `-` | entry remains in the package as traceable material but is excluded from strong content claims |
| INFO | `content_denominator_excluded_entry` | `vbr1_l1_lfsr_prbs_generator` | `-` | entry remains in the package as traceable material but is excluded from strong content claims |
| INFO | `content_denominator_excluded_entry` | `vbr1_l1_ramp_or_step_source` | `-` | entry remains in the package as traceable material but is excluded from strong content claims |
| INFO | `content_denominator_excluded_entry` | `vbr1_l1_sine_periodic_voltage_source` | `-` | entry remains in the package as traceable material but is excluded from strong content claims |
| INFO | `content_denominator_excluded_entry` | `vbr1_l2_programmable_stimulus_sequencer` | `-` | entry remains in the package as traceable material but is excluded from strong content claims |

## Duplicate L2 Kernel Groups

| Keep candidate | Remove or rewrite candidates | Reason |
| --- | --- | --- |
| none | none | none |

## L2 Review Table

| Entry | Content denominator | Category | Function | Gold modules | sim_correct checks |
| --- | --- | --- | --- | --- | --- |
| `vbr1_l2_converter_static_linearity_measurement_flow` | `True` | Data Converter Models | Converter static linearity measurement flow | `converter_static_linearity_measurement_flow` | ramp_code_coverage<br>monotonic_reconstruction<br>nonuniform_dnl_metric<br>inl_metric_matches_reconstruction_error<br>dnl_metric_matches_step_error |
| `vbr1_l2_flash_adc_mini_array` | `True` | Data Converter Models | Flash ADC mini-array | `flash_adc_3b` | all_8_flash_codes_present<br>comparator_threshold_ladder_matches_vin_bins<br>comparator_outputs_form_thermometer_prefix<br>binary_code_matches_comparator_count |
| `vbr1_l2_pipeline_adc_chain` | `True` | Data Converter Models | Pipeline ADC residue chain | `pipeline_adc_chain_4b` | all_16_pipeline_codes_present<br>stage1_residue_matches_coarse_decision<br>stage2_residue_matches_backend_decision<br>final_code_matches_stage_concatenation<br>final_code_monotonic_with_vin |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `True` | Data Converter Models | Weighted SAR ADC/DAC loop | `dac_weighted_8b, sar_adc_weighted_8b, sh_ideal` | sar_adc_code_range_sufficient<br>sar_adc_unique_code_count<br>sar_code_matches_sampled_input<br>dac_output_matches_weighted_code<br>code_monotonic_with_sampled_input<br>dac_output_in_range |
| `vbr1_l2_comparator_measurement_flow` | `True` | Comparator and Decision Circuits | Single-ramp comparator offset measurement flow | `comparator_offset_search_ref` | comparator_output_low_before_trip<br>comparator_output_high_after_trip<br>outp_first_trip_near_static_offset<br>measurement_valid_latches_after_trip<br>valid_first_assertion_near_trip<br>trip_voltage_near_inn_plus_offset<br>offset_estimate_near_static_offset<br>measurement_outputs_hold_after_valid |
| `vbr1_l2_converter_front_end` | `True` | Sampling and Analog Memory | Converter front-end | `sample_hold_droop_ref` | aperture_delayed_sample_tracks_vin<br>hold_windows_show_bounded_droop<br>coarse_decision_matches_held_sample<br>valid_pulses_mark_completed_samples |
| `vbr1_l2_amplifier_filter_chain` | `True` | Baseband Signal Conditioning | Amplifier/filter chain | `amplifier_filter_chain` | amplified_input<br>filtered_output_lags_input<br>metric_tracks_settling |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `True` | PLL Clock and Timing Systems | ADPLL lock/ratio-hop/timer flow | `adpll_ratio_hop_ref` | adpll_ratio_hop_pre_ratio<br>adpll_ratio_hop_post_ratio<br>adpll_ratio_hop_lock_reacquired |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `True` | PLL Clock and Timing Systems | CPPLL tracking and frequency-step reacquire flow | `cppll_timer_ref, ref_step_clk` | cppll_reacquires_after_reference_step<br>late_window_tracks_new_reference<br>vctrl_stays_bounded |
| `vbr1_l2_complete_calibration_loop` | `True` | Calibration, DEM, and Control | Complete calibration loop | `complete_calibration_loop` | raw_error_is_corrected<br>bounded_negative_feedback_response<br>metric_tracks_convergence |
| `vbr1_l2_ldo_load_step_recovery_flow` | `True` | Bias Reference and Power Management | LDO load-step recovery flow | `ldo_load_step_recovery_flow` | load_step_transient_droop_visible<br>closed_loop_recovery_after_step<br>metric_marks_recovered_regulation |
| `vbr1_l2_reference_startup_enable_flow` | `True` | Bias Reference and Power Management | Reference startup/enable flow | `reference_startup_enable_flow` | pre_enable_reference_is_held_low<br>enabled_reference_startup_settles<br>supply_dip_resets_valid_status |
| `vbr1_l2_agc_receiver_leveling_loop` | `True` | RF and AFE Behavioral Macromodels | AGC receiver leveling loop | `agc_receiver_leveling_loop` | agc_reduces_gain_on_large_input<br>leveled_output_amplitude<br>lock_metric_after_settling |
| `vbr1_l2_iq_downconversion_chain` | `True` | RF and AFE Behavioral Macromodels | I/Q downconversion chain | `iq_downconversion_chain` | quadrature_iq_phase_sequence<br>i_and_q_outputs_are_distinct<br>common_mode_hold_when_input_centered |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `False` | Measurement Instrumentation Flows | Dithered differential gain extraction flow | `dither_adder, gain_amp_fixed, lfsr, vin_src` | gain_amplification_present<br>differential_gain_above_threshold |
| `vbr1_l2_measurement_flow` | `False` | Measurement Instrumentation Flows | Measurement flow | `final_step_file_metric_ref` | ref_edges_counted_on_expected_grid<br>metric_out_normalizes_final_edge_count<br>final_step_writes_candidate_metric_file |
| `vbr1_l2_programmable_stimulus_sequencer` | `False` | Stimulus and Source Generators | Programmable stimulus sequencer | `programmable_stimulus_sequencer` | ramp_segment_monotonic<br>swept_chirp_segment_frequency_increases<br>burst_prbs_gate_schedule<br>mode_switch_continuity |

## Code Excerpts for Manual Judgment

No excerpts were needed.
## Recommended Policy

- Do not retain exact duplicate L2 kernels in the clean release package; rewrite them before re-admission.
- Keep score disabled; allow only unweighted pass-rate reporting after content review.
- For shallow companion checkers, either add function-level behavior checks or mark the companion as auxiliary outside the strong benchmark claim.
- Treat REVIEW_REQUIRED findings as human semantic review queue, not simulator failures.
