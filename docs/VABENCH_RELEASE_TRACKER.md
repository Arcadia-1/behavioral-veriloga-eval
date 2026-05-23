# vaBench Release Tracker

Date: 2026-05-17

This tracker is generated from `docs/VABENCH_RELEASE_TAXONOMY.md`.
It is the execution queue for the long-run vaBench release goal.

## Count Summary

| Status | Count |
| --- | ---: |
| current_l1_seed | 27 |
| current_l1_seed_with_review | 1 |
| selected_l1_addition | 32 |
| selected_l2_target | 15 |
| total | 75 |

## Certification Rule

A row enters the scored benchmark only after `certification_status=certified`
and after prompt, metadata, checks, gold assets, static checks, EVAS,
and Spectre are all marked complete/pass.

## Tracker Rows

| Entry | Level | Category | Function | Package status | Certification |
| --- | --- | --- | --- | --- | --- |
| vbr1_l1_binary_weighted_voltage_dac | L1 | Data Converters | Simple 4-bit binary-coded DAC | current_l1_seed | not_certified |
| vbr1_l1_unit_element_thermometer_dac | L1 | Data Converters | Unit-element thermometer DAC | selected_l1_addition | not_certified |
| vbr1_l1_segmented_dac | L1 | Data Converters | Segmented DAC | current_l1_seed | not_certified |
| vbr1_l1_thermometer_code_decoder | L1 | Data Converters | Thermometer-code decoder | current_l1_seed | not_certified |
| vbr1_l1_clocked_adc_quantizer | L1 | Data Converters | Clocked ADC quantizer | selected_l1_addition | not_certified |
| vbr1_l1_capacitive_weighted_sar_feedback_dac | L1 | Data Converters | Capacitive/weighted SAR feedback DAC | selected_l1_addition | not_certified |
| vbr1_l1_dac_mismatch_unit_weighting_model | L1 | Data Converters | DAC mismatch/unit-weighting model | selected_l1_addition | not_certified |
| vbr1_l1_sar_logic | L1 | Data Converters | SAR logic | current_l1_seed | not_certified |
| vbr1_l1_pipeline_adc_stage | L1 | Data Converters | Pipeline ADC MDAC stage | selected_l1_addition | not_certified |
| vbr1_l2_adc_dac_reconstruction_chain | L2 | Data Converters | ADC/DAC reconstruction chain | selected_l2_target | not_certified |
| vbr1_l2_weighted_sar_adc_dac_loop | L2 | Data Converters | Weighted SAR ADC/DAC loop | selected_l2_target | not_certified |
| vbr1_l2_flash_adc_mini_array | L2 | Data Converters | Flash ADC mini-array | selected_l2_target | not_certified |
| vbr1_l2_pipeline_adc_chain | L2 | Data Converters | Pipeline ADC chain | selected_l2_target | not_certified |
| vbr1_l1_threshold_comparator | L1 | Comparators and Decision Circuits | Threshold comparator | selected_l1_addition | not_certified |
| vbr1_l1_propagation_delay_comparator | L1 | Comparators and Decision Circuits | Propagation-delay comparator | selected_l1_addition | not_certified |
| vbr1_l1_hysteresis_comparator | L1 | Comparators and Decision Circuits | Hysteresis comparator | selected_l1_addition | not_certified |
| vbr1_l1_window_comparator_detector | L1 | Comparators and Decision Circuits | Window comparator/detector | selected_l1_addition | not_certified |
| vbr1_l1_offset_comparator | L1 | Comparators and Decision Circuits | Offset comparator | current_l1_seed | not_certified |
| vbr1_l1_strongarm_style_latch_comparator | L1 | Comparators and Decision Circuits | StrongARM-style latch comparator | current_l1_seed | not_certified |
| vbr1_l2_comparator_measurement_flow | L2 | Comparators and Decision Circuits | Single-ramp comparator offset measurement flow | selected_l2_target | not_certified |
| vbr1_l1_vco_phase_integrator | L1 | PLL / Clock / Event Timing | VCO phase integrator | current_l1_seed | not_certified |
| vbr1_l1_pfd_up_dn_logic | L1 | PLL / Clock / Event Timing | PFD UP/DN logic | current_l1_seed | not_certified |
| vbr1_l1_pfd_small_phase_error_response | L1 | PLL / Clock / Event Timing | PFD small phase-error response | selected_l1_addition | not_certified |
| vbr1_l1_xor_phase_detector | L1 | PLL / Clock / Event Timing | XOR phase detector | selected_l1_addition | not_certified |
| vbr1_l1_bang_bang_phase_detector | L1 | PLL / Clock / Event Timing | Bang-bang phase detector | selected_l1_addition | not_certified |
| vbr1_l1_digital_phase_accumulator_with_modulo_wrap | L1 | PLL / Clock / Event Timing | Digital phase accumulator with modulo wrap | selected_l1_addition | not_certified |
| vbr1_l1_clock_divider | L1 | PLL / Clock / Event Timing | Clock divider | current_l1_seed | not_certified |
| vbr1_l1_lock_detector | L1 | PLL / Clock / Event Timing | Lock detector | current_l1_seed | not_certified |
| vbr1_l1_charge_pump_abstraction | L1 | PLL / Clock / Event Timing | Voltage-domain charge-pump control abstraction | selected_l1_addition | not_certified |
| vbr1_l1_loop_filter_abstraction | L1 | PLL / Clock / Event Timing | Sampled loop-filter abstraction | selected_l1_addition | not_certified |
| vbr1_l2_pll_timing_slice | L2 | PLL / Clock / Event Timing | PLL timing slice | selected_l2_target | not_certified |
| vbr1_l2_adpll_lock_ratio_hop_timer_flow | L2 | PLL / Clock / Event Timing | ADPLL lock/ratio-hop/timer flow | selected_l2_target | not_certified |
| vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow | L2 | PLL / Clock / Event Timing | CPPLL tracking and frequency-step reacquire flow | selected_l2_target | not_certified |
| vbr1_l1_trim_calibration_controller | L1 | Calibration, DEM, and Control | Trim-voltage generator | current_l1_seed | not_certified |
| vbr1_l1_gain_trim_controller | L1 | Calibration, DEM, and Control | Gain trim controller | current_l1_seed | not_certified |
| vbr1_l1_rotating_dem_selector | L1 | Calibration, DEM, and Control | Rotating DEM selector | current_l1_seed | not_certified |
| vbr1_l1_windowed_dem_pointer | L1 | Calibration, DEM, and Control | Windowed DEM pointer | current_l1_seed | not_certified |
| vbr1_l1_dwa_dem_encoder | L1 | Calibration, DEM, and Control | DWA/DEM encoder | selected_l1_addition | not_certified |
| vbr1_l1_calibration_deadband_controller | L1 | Calibration, DEM, and Control | Calibration deadband controller | selected_l1_addition | not_certified |
| vbr1_l1_successive_approximation_calibration_search_fsm | L1 | Calibration, DEM, and Control | Successive-approximation calibration/search FSM | selected_l1_addition | not_certified |
| vbr1_l1_element_shuffler | L1 | Calibration, DEM, and Control | Element shuffler | current_l1_seed | not_certified |
| vbr1_l2_complete_calibration_loop | L2 | Calibration, DEM, and Control | Complete calibration loop | selected_l2_target | not_certified |
| vbr1_l1_edge_detector | L1 | Digital and Event-Driven Logic | Edge detector | current_l1_seed | not_certified |
| vbr1_l1_debounce_latch | L1 | Digital and Event-Driven Logic | Debounce latch | current_l1_seed | not_certified |
| vbr1_l1_one_shot_timer | L1 | Digital and Event-Driven Logic | One-shot timer | current_l1_seed | not_certified |
| vbr1_l1_lfsr_prbs_generator | L1 | Digital and Event-Driven Logic | LFSR/PRBS generator | selected_l1_addition | not_certified |
| vbr1_l1_serializer_frame_aligner | L1 | Digital and Event-Driven Logic | Serializer/frame aligner | selected_l1_addition | not_certified |
| vbr1_l1_event_pulse_stretcher | L1 | Digital and Event-Driven Logic | Retriggerable one-shot pulse stretcher | selected_l1_addition | not_certified |
| vbr1_l2_event_controller | L2 | Digital and Event-Driven Logic | Event controller | selected_l2_target | not_certified |
| vbr1_l2_serializer_frame_alignment_flow | L2 | Digital and Event-Driven Logic | Serializer frame-alignment flow | selected_l2_target | not_certified |
| vbr1_l1_crossing_metric_writer | L1 | Measurement and Testbench Instrumentation | Crossing metric writer | current_l1_seed | not_certified |
| vbr1_l1_settling_time_detector | L1 | Measurement and Testbench Instrumentation | Settling response measurement helper | current_l1_seed | not_certified |
| vbr1_l1_peak_detector | L1 | Measurement and Testbench Instrumentation | Peak detector | current_l1_seed | not_certified |
| vbr1_l1_gain_estimator | L1 | Measurement and Testbench Instrumentation | Gain estimator | selected_l1_addition | not_certified |
| vbr1_l1_edge_interval_timer | L1 | Measurement and Testbench Instrumentation | Edge interval timer | selected_l1_addition | not_certified |
| vbr1_l2_measurement_flow | L2 | Measurement and Testbench Instrumentation | Measurement flow | selected_l2_target | not_certified |
| vbr1_l2_gain_extraction_convergence_measurement_flow | L2 | Measurement and Testbench Instrumentation | Gain extraction/convergence measurement flow | selected_l2_target | not_certified |
| vbr1_l1_ramp_or_step_source | L1 | Stimulus and Sources | Periodic phase-ramp guard source | selected_l1_addition | not_certified |
| vbr1_l1_burst_clock_source | L1 | Stimulus and Sources | Burst clock source | selected_l1_addition | not_certified |
| vbr1_l1_dither_or_noise_like_deterministic_source | L1 | Stimulus and Sources | Dither or noise-like deterministic source | selected_l1_addition | not_certified |
| vbr1_l1_sine_periodic_voltage_source | L1 | Stimulus and Sources | Sine/periodic voltage source | selected_l1_addition | not_certified |
| vbr1_l2_adc_dac_source_sweep_flow | L2 | Stimulus and Sources | ADC/DAC source sweep flow | selected_l2_target | not_certified |
| vbr1_l1_first_order_lowpass | L1 | Analog Behavioral Signal Conditioning | First-order lowpass | current_l1_seed | not_certified |
| vbr1_l1_resettable_integrator | L1 | Analog Behavioral Signal Conditioning | Resettable integrator | current_l1_seed | not_certified |
| vbr1_l1_soft_hysteretic_limiter | L1 | Analog Behavioral Signal Conditioning | Soft/hysteretic limiter | selected_l1_addition | not_certified |
| vbr1_l1_voltage_gain_amplifier | L1 | Analog Behavioral Signal Conditioning | Voltage gain amplifier | selected_l1_addition | not_certified |
| vbr1_l1_higher_order_filter | L1 | Analog Behavioral Signal Conditioning | Higher-order filter | selected_l1_addition | not_certified |
| vbr1_l1_slew_rate_limiter | L1 | Analog Behavioral Signal Conditioning | Slew-rate limiter | current_l1_seed | not_certified |
| vbr1_l2_amplifier_filter_chain | L2 | Analog Behavioral Signal Conditioning | Amplifier/filter chain | selected_l2_target | not_certified |
| vbr1_l1_aperture_delay_track_and_hold | L1 | Sample, Hold, and Analog Memory | Aperture-delay track-and-hold | current_l1_seed | not_certified |
| vbr1_l1_sample_and_hold_with_droop_leakage | L1 | Sample, Hold, and Analog Memory | Sample-and-hold with droop/leakage | current_l1_seed_with_review | not_certified |
| vbr1_l1_clocked_sample_and_hold | L1 | Sample, Hold, and Analog Memory | Clocked sample-and-hold | selected_l1_addition | not_certified |
| vbr1_l2_converter_front_end | L2 | Sample, Hold, and Analog Memory | Converter front-end | selected_l2_target | not_certified |
