# Over-Five Mutation Semantic Review

These proposals are not final assignments. Review whether the selected five retain the strongest distinct
fault meanings and whether the Bugfix seed is a representative single semantic fault.

| Family | Count | Bugfix seed | Proposed T | Excluded |
|---|---:|---|---|---|
| 001 | 6 | neg_001_swap_outputs | neg_001_swap_outputs, neg_003_never_clears_on_clock, neg_004_both_outputs_on_direction, neg_006_weak_high_level, neg_005_retimed_ignored | neg_002_ignore_falling_data_edges |
| 002 | 6 | neg_001_ignore_calibration | neg_001_ignore_calibration, neg_002_reversed_polarity, neg_005_common_mode_error, neg_006_asynchronous_code_update, neg_003_bit_weight_swap | neg_004_calibration_scale_16 |
| 003 | 7 | neg_004_middle_code_wrong | neg_004_middle_code_wrong, neg_001_threshold_too_wide, neg_006_live_vin_on_phi2, neg_007_missing_residue_clamp, neg_002_upper_decision_msb_stuck_low | neg_003_residue_feedback_sign_swapped, neg_005_residue_gain_low |
| 004 | 6 | neg_002_inverted_error_direction | neg_002_inverted_error_direction, neg_005_missing_lower_clamp, neg_004_wrong_reset_level, neg_006_asynchronous_error_update, neg_001_stuck_midscale | neg_003_wrong_step_size |
| 005 | 7 | neg_002_immediate_set_on_rise | neg_002_immediate_set_on_rise, neg_004_reset_does_not_cancel_timer, neg_007_missing_fall_clear, neg_001_no_final_sig_recheck, neg_005_never_qualifies_high | neg_003_arms_while_reset_low, neg_006_spurious_timer_glitch |
| 006 | 7 | neg_003_monotonic_output_order | neg_003_monotonic_output_order, neg_005_out0_stuck_high, neg_006_weak_high_level, neg_007_wrong_reset_state, neg_001_stuck_initial_state | neg_002_skip_every_other_state, neg_004_forces_state_three |
| 007 | 7 | neg_001_too_slow_alpha | neg_001_too_slow_alpha, neg_003_inverted_input, neg_005_stuck_zero, neg_006_wrong_initial_state, neg_002_passthrough_timer | neg_004_output_clamped, neg_007_wrong_update_period |
| 008 | 6 | neg_002_inverted_direction | neg_002_inverted_direction, neg_005_missing_deadband_hold, neg_004_wrong_reset_level, neg_006_missing_control_clamp, neg_001_stuck_midscale | neg_003_wrong_step_size |
| 010 | 6 | neg_001_zero_offset | neg_001_zero_offset, neg_006_fixed_clock_midpoint, neg_003_falling_edge, neg_002_large_offset, neg_004_async_response | neg_005_weak_high |
| 011 | 6 | neg_001_swapped_outputs | neg_001_swapped_outputs, neg_005_div_lead_clear_leaves_up, neg_006_fixed_nominal_rails, neg_002_missing_ref_lead_clear, neg_003_div_falling_edge | neg_004_dn_channel_missing |
| 012 | 6 | neg_001_ratio_decode_bit_drop | neg_001_ratio_decode_bit_drop, neg_005_output_stuck_high_after_start, neg_004_lock_never_asserts, neg_006_reset_ignored, neg_002_off_by_one_divide_ratio | neg_003_ratio_bit_order_reversed |
| 013 | 6 | neg_001_gain_low | neg_001_gain_low, neg_003_integral_sign_reversed, neg_004_reset_ignored, neg_002_timer_too_slow, neg_006_nonzero_output_baseline | neg_005_output_half_scale |
| 016 | 7 | neg_002_passthrough_update | neg_002_passthrough_update, neg_001_stuck_zero, neg_006_wrong_initial_state, neg_007_wrong_update_period, neg_003_inverted_slew_direction | neg_004_step_too_small, neg_005_missing_fall_branch |
| 019 | 6 | neg_001_missing_phase_increment | neg_001_missing_phase_increment, neg_004_missing_phase_wrap, neg_002_phase_increment_too_small, neg_003_wrong_timer_period, neg_005_wrap_does_not_toggle_clock | neg_006_control_direction_inverted |
| 031 | 7 | neg_001_linear_gain_error | neg_001_linear_gain_error, neg_005_metric_stuck_low, neg_007_output_clamp_missing, neg_004_reset_ignored, neg_006_asynchronous_tracking | neg_002_positive_limit_slope, neg_003_negative_limit_slope |
| 032 | 7 | neg_001_reduced_small_signal_gain | neg_001_reduced_small_signal_gain, neg_004_compression_metric_stuck_low, neg_005_output_clamp_bypass, neg_007_reset_ignored, neg_006_asynchronous_input_tracking | neg_002_positive_compression_bypass, neg_003_negative_compression_bypass |
| 035 | 7 | neg_003_inverted_drive | neg_003_inverted_drive, neg_006_output_clamp_bypass, neg_004_reset_ignored, neg_007_asynchronous_tracking, neg_002_compression_bypass | neg_001_wrong_gain, neg_005_metric_stuck_linear |
| 038 | 7 | neg_002_inverted_gain_select | neg_002_inverted_gain_select, neg_005_clip_metric_stuck_low, neg_007_output_clamp_bypass, neg_006_reset_ignored, neg_003_fixed_unity_gain | neg_001_zero_gain, neg_004_fixed_high_gain |
| 048 | 6 | neg_001_off_by_one_count | neg_001_off_by_one_count, neg_005_reversed_bit_order, neg_006_weak_high_level, neg_003_enable_ignored, neg_004_missing_top_cell | neg_002_reversed_thermometer_bus |
| 061 | 6 | neg_001_zero | neg_001_zero, neg_003_no_clear, neg_004_no_done, neg_006_swapped_count0_count1, neg_002_count_all | neg_005_off_by_one |
| 063 | 6 | neg_001_zero | neg_001_zero, neg_003_wide_tol, neg_004_no_reset, neg_005_wrong_code, neg_006_reversed_code_bits | neg_002_no_hold |
| 067 | 7 | neg_001_force_zero | neg_001_force_zero, neg_003_reversed_observed_bits, neg_004_rounds_ideal_code, neg_006_signed_error_only, neg_007_half_scale_metric | neg_002_instantaneous_error_only, neg_005_wrong_code_span |
| 069 | 7 | neg_001_zero | neg_001_zero, neg_003_wrong_period, neg_004_no_done, neg_005_extra_pulse, neg_006_zero_code_width_not_minimum | neg_002_ignore_width, neg_007_output_levels_low |
| 070 | 7 | neg_001_zero | neg_001_zero, neg_004_unbounded, neg_005_ignore_seed, neg_006_nonrepeating_sequence, neg_007_weak_high | neg_002_no_jitter, neg_003_too_slow |
| 073 | 6 | neg_001_zero | neg_001_zero, neg_003_event_edge_wrong, neg_004_reset_polarity_wrong, neg_005_metric_scale_low, neg_006_nonmonotonic_upper_trim | neg_002_threshold_shifted |
| 075 | 7 | neg_001_zero | neg_001_zero, neg_003_event_edge_wrong, neg_004_reset_polarity_wrong, neg_006_monotonic_notch, neg_007_no_transition_smoothing | neg_002_threshold_shifted, neg_005_metric_scale_low |
| 076 | 7 | neg_001_zero | neg_001_zero, neg_004_wrong_div4, neg_005_metric_scale_low, neg_006_reset_ignored, neg_007_frame_start_offset | neg_002_pass_all_cycles, neg_003_one_cycle_burst |
| 078 | 6 | neg_001_zero | neg_001_zero, neg_005_metric_scale_low, neg_003_ignore_enable, neg_006_shift_sequence_wrong, neg_002_wrong_taps | neg_004_wrong_serial_bit |
| 092 | 5 | neg_002_unity_gain | neg_002_unity_gain, neg_005_metric_scale_low, neg_001_zero, neg_003_inverted_polarity, neg_004_ignores_gain_parameter | none |
| 098 | 5 | neg_002_no_frequency_step | neg_002_no_frequency_step, neg_005_bad_duty_cycle, neg_003_wrong_post_period, neg_001_zero, neg_004_late_switch | none |
| 105 | 6 | neg_001_zero | neg_001_zero, neg_003_falling_edge_trigger, neg_004_stuck_high_after_first, neg_005_metric_scale_low, neg_006_no_output_delay | neg_002_short_pulse |
| 108 | 6 | neg_001_zero | neg_001_zero, neg_003_short_pulse, neg_004_no_delay, neg_005_metric_scale_low, neg_006_no_output_delay | neg_002_rising_only |
| 218 | 6 | neg_002_no_falling_reset | neg_002_no_falling_reset, neg_001_zero, neg_005_metric_scale_low, neg_006_equal_input_bias, neg_004_swapped_outputs | neg_003_inverted_compare |
| 343 | 6 | neg_001_stage1_threshold_shift | neg_001_stage1_threshold_shift, neg_005_valid_stuck_low, neg_006_reset_state_not_cleared, neg_003_stage2_threshold_shift, neg_004_coarse_alignment_weight | neg_002_residue_gain_low |
| 346 | 7 | neg_001_count_by_two | neg_001_count_by_two, neg_003_valid_stuck_low, neg_004_early_overflow, neg_006_reset_clear_ignored, neg_007_restart_clear_ignored | neg_002_stop_off_by_one, neg_005_encoder_lsb_swapped |
| 380 | 6 | neg_002_envelope_dbg_stuck | neg_002_envelope_dbg_stuck, neg_001_no_modulation, neg_003_valid_stuck_low, neg_004_missing_clear, neg_006_output_not_clamped | neg_005_carrier_inverted |
| 386 | 6 | neg_002_gain_metric_wrong | neg_002_gain_metric_wrong, neg_001_no_compression, neg_004_flag_stuck_low, neg_005_missing_clear, neg_006_output_not_clamped | neg_003_phase_metric_stuck |
| 398 | 6 | neg_001_stage1_wrong | neg_001_stage1_wrong, neg_003_settled_stuck_high, neg_004_missing_clear, neg_005_clamp_flag_stuck_low, neg_006_asynchronous_update | neg_002_no_slew_limit |

Detailed fault classes, trigger conditions, properties, and legacy profiles are retained in
`OVERFIVE_REVIEW.json`.
