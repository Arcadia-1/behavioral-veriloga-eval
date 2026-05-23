# vaBench Content Contract Audit

Date: 2026-05-23

This report audits benchmark content semantics before model baselines or
paper-facing benchmark claims. EVAS/Spectre certification proves simulator
agreement, but this report asks whether the public task, checker, and gold
source describe the same circuit function.

## Summary

| Metric | Value |
| --- | ---: |
| status | `pass` |
| release entries | 73 |
| release forms | 249 |
| content denominator entries | 73 |
| content denominator forms | 249 |
| content-excluded entries | 0 |

## Findings

| Severity | Kind | Entry | Form | Message |
| --- | --- | --- | --- | --- |
| none | none | none | none | none |

## Duplicate L2 Kernel Groups

| Keep candidate | Remove or rewrite candidates | Reason |
| --- | --- | --- |
| none | none | none |

## L2 Review Table

| Entry | Content denominator | Category | Function | Gold modules | sim_correct checks |
| --- | --- | --- | --- | --- | --- |
| `vbr1_l2_adc_dac_reconstruction_chain` | `True` | Data Converters | ADC/DAC reconstruction chain | `adc_ideal_4b, adc_ideal_4b, dac_ideal_4b, dac_ideal_4b` | adc_covers_full_code_range<br>dac_output_in_range<br>quantization_error_within_one_lsb |
| `vbr1_l2_flash_adc_mini_array` | `True` | Data Converters | Flash ADC mini-array | `flash_adc_3b` | all_8_flash_codes_present<br>comparator_threshold_ladder_matches_vin_bins<br>comparator_outputs_form_thermometer_prefix<br>binary_code_matches_comparator_count |
| `vbr1_l2_pipeline_adc_chain` | `True` | Data Converters | Pipeline ADC chain | `pipeline_adc_chain_4b` | all_16_pipeline_codes_present<br>stage1_residue_matches_coarse_decision<br>stage2_residue_matches_backend_decision<br>final_code_matches_stage_concatenation<br>final_code_monotonic_with_vin |
| `vbr1_l2_weighted_sar_adc_dac_loop` | `True` | Data Converters | Weighted SAR ADC/DAC loop | `dac_weighted_8b, sar_adc_weighted_8b, sh_ideal` | sar_adc_code_range_sufficient<br>sar_adc_unique_code_count<br>dac_output_in_range |
| `vbr1_l2_comparator_measurement_flow` | `True` | Comparators and Decision Circuits | Single-ramp comparator offset measurement flow | `comparator_offset_search_ref` | comparator_output_low_before_trip<br>comparator_output_high_after_trip<br>measurement_valid_latches_after_trip<br>trip_voltage_near_inn_plus_offset<br>offset_estimate_near_static_offset<br>measurement_outputs_hold_after_valid |
| `vbr1_l2_converter_front_end` | `True` | Sample, Hold, and Analog Memory | Converter front-end | `sample_hold_droop_ref` | aperture_delayed_sample_tracks_vin<br>hold_windows_show_bounded_droop<br>coarse_decision_matches_held_sample<br>valid_pulses_mark_completed_samples |
| `vbr1_l2_amplifier_filter_chain` | `True` | Analog Behavioral Signal Conditioning | Amplifier/filter chain | `amplifier_filter_chain` | amplifier_target_metric<br>filtered_output_lags_target<br>bounded_chain_response |
| `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | `True` | PLL / Clock / Event Timing | ADPLL lock/ratio-hop/timer flow | `adpll_ratio_hop_ref` | adpll_ratio_hop_pre_ratio<br>adpll_ratio_hop_post_ratio<br>adpll_ratio_hop_lock_reacquired |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | `True` | PLL / Clock / Event Timing | CPPLL tracking and frequency-step reacquire flow | `cppll_timer_ref, ref_step_clk` | cppll_reacquires_after_reference_step<br>late_window_tracks_new_reference<br>vctrl_stays_bounded |
| `vbr1_l2_pll_timing_slice` | `True` | PLL / Clock / Event Timing | PLL timing slice | `cppll_timer_ref` | cppll_tracks_reference_frequency<br>vctrl_stays_bounded |
| `vbr1_l2_event_controller` | `True` | Digital and Event-Driven Logic | Event controller | `simultaneous_event_order_ref` | ref_edges_align_with_absolute_timer_grid<br>plateau_levels_encode_cross_after_timer_order<br>simultaneous_event_order |
| `vbr1_l2_serializer_frame_alignment_flow` | `True` | Digital and Event-Driven Logic | Serializer frame-alignment flow | `serializer_frame_alignment_ref` | frame_pulse_present_for_each_loaded_word<br>serialized_bits_match_word0xA5_then_0x3C<br>frame_pulse_width_is_single_bit_window |
| `vbr1_l2_complete_calibration_loop` | `True` | Calibration, DEM, and Control | Complete calibration loop | `complete_calibration_loop` | error_drives_trim<br>actuator_moves_opposite_error<br>loop_converges_toward_target |
| `vbr1_l2_gain_extraction_convergence_measurement_flow` | `True` | Measurement and Testbench Instrumentation | Gain extraction/convergence measurement flow | `dither_adder, gain_amp_fixed, lfsr, vin_src` | gain_amplification_present<br>differential_gain_above_threshold |
| `vbr1_l2_measurement_flow` | `True` | Measurement and Testbench Instrumentation | Measurement flow | `final_step_file_metric_ref` | ref_edges_counted_on_expected_grid<br>metric_out_normalizes_final_edge_count<br>final_step_writes_candidate_metric_file |
| `vbr1_l2_adc_dac_source_sweep_flow` | `True` | Stimulus and Sources | ADC/DAC source sweep flow | `adc_dac_source_sweep_flow` | code_monotonic_with_input<br>reconstruction_follows_code<br>saturation_at_rails |

## Code Excerpts for Manual Judgment

No excerpts were needed.
## Recommended Policy

- Do not retain exact duplicate L2 kernels in the clean release package; rewrite them before re-admission.
- Keep score disabled; allow only unweighted pass-rate reporting after content review.
- For shallow companion checkers, either add function-level behavior checks or mark the companion as auxiliary outside the strong benchmark claim.
- Treat REVIEW_REQUIRED findings as human semantic review queue, not simulator failures.
