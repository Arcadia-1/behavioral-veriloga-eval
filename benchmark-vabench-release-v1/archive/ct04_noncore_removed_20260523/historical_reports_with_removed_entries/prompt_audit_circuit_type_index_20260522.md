# Prompt Audit Circuit Type Index

Date: 2026-05-22

Scope: `benchmark-vabench-release-v1` prompt audit by circuit type. These IDs are stable audit labels for reviewing public prompts against the intended voltage-domain behavioral circuit function.

## Circuit Type IDs

| Type ID | Circuit Type | L1 | L2 | Audit Focus |
| --- | --- | ---: | ---: | --- |
| `CT01` | Data Converter Models | 8 | 3 | code mapping, quantization, reconstruction, monotonicity, rail saturation |
| `CT02` | PLL, Clock, and Timing Systems | 10 | 3 | edge timing, phase/frequency relation, lock/reacquire behavior, timer semantics |
| `CT03` | Baseband Signal Conditioning | 9 | 1 | gain/filter/limit dynamics, settling, bounded voltage-domain behavior |
| `CT04` | Calibration, DEM, and Control | 8 | 1 | state-machine/control loop behavior, trim direction, convergence, element selection |
| `CT05` | Comparator and Decision Circuits | 7 | 1 | threshold/offset/hysteresis decisions, clocked decisions, output polarity |
| `CT06` | Digital and Event-Driven Logic | 6 | 2 | event ordering, edge detection, pulse/frame timing, digital state progression |
| `CT07` | Measurement Instrumentation Flows | 5 | 2 | metric extraction, final-step/file outputs, edge/settling/gain measurement contracts |
| `CT08` | Sampling and Analog Memory | 3 | 1 | track/hold windows, aperture delay, droop/leakage, sampled memory behavior |
| `SUP01` | Stimulus and Source Generators | 4 | 1 | source waveform shape, clock bursts, deterministic noise/dither, sweep coverage |

## Detailed Entries

### `CT01` Data Converter Models

| Level | Entry | Base Function |
| --- | --- | --- |
| L1 | `vbr1_l1_binary_weighted_voltage_dac` | Simple 4-bit binary-coded DAC |
| L1 | `vbr1_l1_capacitive_weighted_sar_feedback_dac` | Capacitive/weighted SAR feedback DAC |
| L1 | `vbr1_l1_clocked_adc_quantizer` | Clocked ADC quantizer |
| L1 | `vbr1_l1_dac_mismatch_unit_weighting_model` | DAC mismatch/unit-weighting model |
| L1 | `vbr1_l1_sar_logic` | SAR logic |
| L1 | `vbr1_l1_segmented_dac` | Segmented DAC |
| L1 | `vbr1_l1_thermometer_code_decoder` | Thermometer-code decoder |
| L1 | `vbr1_l1_unit_element_thermometer_dac` | Unit-element thermometer DAC |
| L2 | `vbr1_l2_adc_dac_reconstruction_chain` | ADC/DAC reconstruction chain |
| L2 | `vbr1_l2_flash_adc_mini_array` | Flash ADC mini-array |
| L2 | `vbr1_l2_weighted_sar_adc_dac_loop` | Weighted SAR ADC/DAC loop |

### `CT02` PLL, Clock, and Timing Systems

| Level | Entry | Base Function |
| --- | --- | --- |
| L1 | `vbr1_l1_bang_bang_phase_detector` | Bang-bang phase detector |
| L1 | `vbr1_l1_charge_pump_abstraction` | Voltage-domain charge-pump control abstraction |
| L1 | `vbr1_l1_clock_divider` | Clock divider |
| L1 | `vbr1_l1_digital_phase_accumulator_with_modulo_wrap` | Digital phase accumulator with modulo wrap |
| L1 | `vbr1_l1_lock_detector` | Lock detector |
| L1 | `vbr1_l1_loop_filter_abstraction` | Sampled loop-filter abstraction |
| L1 | `vbr1_l1_pfd_small_phase_error_response` | PFD small phase-error response |
| L1 | `vbr1_l1_pfd_up_dn_logic` | PFD UP/DN logic |
| L1 | `vbr1_l1_vco_phase_integrator` | VCO phase integrator |
| L1 | `vbr1_l1_xor_phase_detector` | XOR phase detector |
| L2 | `vbr1_l2_adpll_lock_ratio_hop_timer_flow` | ADPLL lock/ratio-hop/timer flow |
| L2 | `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow` | CPPLL tracking and frequency-step reacquire flow |
| L2 | `vbr1_l2_pll_timing_slice` | PLL timing slice |

### `CT03` Baseband Signal Conditioning

| Level | Entry | Base Function |
| --- | --- | --- |
| L1 | `vbr1_l1_differential_output_driver` | Differential output driver |
| L1 | `vbr1_l1_first_order_lowpass` | First-order lowpass |
| L1 | `vbr1_l1_higher_order_filter` | Higher-order filter |
| L1 | `vbr1_l1_precision_rectifier` | Precision rectifier |
| L1 | `vbr1_l1_resettable_integrator` | Resettable integrator |
| L1 | `vbr1_l1_slew_rate_limiter` | Slew-rate limiter |
| L1 | `vbr1_l1_soft_hysteretic_limiter` | Soft/hysteretic limiter |
| L1 | `vbr1_l1_voltage_clamp_or_limiter` | Voltage clamp or limiter |
| L1 | `vbr1_l1_voltage_gain_amplifier` | Voltage gain amplifier |
| L2 | `vbr1_l2_amplifier_filter_chain` | Amplifier/filter chain |

### `CT04` Calibration, DEM, and Control

| Level | Entry | Base Function |
| --- | --- | --- |
| L1 | `vbr1_l1_calibration_deadband_controller` | Calibration deadband controller |
| L1 | `vbr1_l1_dwa_dem_encoder` | DWA/DEM encoder |
| L1 | `vbr1_l1_element_shuffler` | Element shuffler |
| L1 | `vbr1_l1_gain_trim_controller` | Gain trim controller |
| L1 | `vbr1_l1_rotating_dem_selector` | Rotating DEM selector |
| L1 | `vbr1_l1_successive_approximation_calibration_search_fsm` | Successive-approximation calibration/search FSM |
| L1 | `vbr1_l1_trim_calibration_controller` | Trim-voltage generator |
| L1 | `vbr1_l1_windowed_dem_pointer` | Windowed DEM pointer |
| L2 | `vbr1_l2_complete_calibration_loop` | Complete calibration loop |

### `CT05` Comparator and Decision Circuits

| Level | Entry | Base Function |
| --- | --- | --- |
| L1 | `vbr1_l1_clocked_comparator` | Clocked comparator |
| L1 | `vbr1_l1_hysteresis_comparator` | Hysteresis comparator |
| L1 | `vbr1_l1_offset_comparator` | Offset comparator |
| L1 | `vbr1_l1_propagation_delay_comparator` | Propagation-delay comparator |
| L1 | `vbr1_l1_strongarm_style_latch_comparator` | StrongARM-style latch comparator |
| L1 | `vbr1_l1_threshold_comparator` | Threshold comparator |
| L1 | `vbr1_l1_window_comparator_detector` | Window comparator/detector |
| L2 | `vbr1_l2_comparator_measurement_flow` | Single-ramp comparator offset measurement flow |

### `CT06` Digital and Event-Driven Logic

| Level | Entry | Base Function |
| --- | --- | --- |
| L1 | `vbr1_l1_debounce_latch` | Debounce latch |
| L1 | `vbr1_l1_edge_detector` | Edge detector |
| L1 | `vbr1_l1_event_pulse_stretcher` | Retriggerable one-shot pulse stretcher |
| L1 | `vbr1_l1_lfsr_prbs_generator` | LFSR/PRBS generator |
| L1 | `vbr1_l1_one_shot_timer` | One-shot timer |
| L1 | `vbr1_l1_serializer_frame_aligner` | Serializer/frame aligner |
| L2 | `vbr1_l2_event_controller` | Event controller |
| L2 | `vbr1_l2_serializer_frame_alignment_flow` | Serializer frame-alignment flow |

### `CT07` Measurement Instrumentation Flows

| Level | Entry | Base Function |
| --- | --- | --- |
| L1 | `vbr1_l1_crossing_metric_writer` | Crossing metric writer |
| L1 | `vbr1_l1_edge_interval_timer` | Edge interval timer |
| L1 | `vbr1_l1_gain_estimator` | Gain estimator |
| L1 | `vbr1_l1_peak_detector` | Peak detector |
| L1 | `vbr1_l1_settling_time_detector` | Settling response measurement helper |
| L2 | `vbr1_l2_gain_extraction_convergence_measurement_flow` | Gain extraction/convergence measurement flow |
| L2 | `vbr1_l2_measurement_flow` | Measurement flow |

### `CT08` Sampling and Analog Memory

| Level | Entry | Base Function |
| --- | --- | --- |
| L1 | `vbr1_l1_aperture_delay_track_and_hold` | Aperture-delay track-and-hold |
| L1 | `vbr1_l1_clocked_sample_and_hold` | Clocked sample-and-hold |
| L1 | `vbr1_l1_sample_and_hold_with_droop_leakage` | Sample-and-hold with droop/leakage |
| L2 | `vbr1_l2_converter_front_end` | Converter front-end |

### `SUP01` Stimulus and Source Generators

| Level | Entry | Base Function |
| --- | --- | --- |
| L1 | `vbr1_l1_burst_clock_source` | Burst clock source |
| L1 | `vbr1_l1_dither_or_noise_like_deterministic_source` | Dither or noise-like deterministic source |
| L1 | `vbr1_l1_ramp_or_step_source` | Periodic phase-ramp guard source |
| L1 | `vbr1_l1_sine_periodic_voltage_source` | Sine/periodic voltage source |
| L2 | `vbr1_l2_adc_dac_source_sweep_flow` | ADC/DAC source sweep flow |

## Suggested Review Order

Start with the two recently tightened groups:

1. `CT06` Digital and Event-Driven Logic: inspect `vbr1_l2_event_controller` first.
2. `CT07` Measurement Instrumentation Flows: inspect `vbr1_l2_measurement_flow` first.
3. Then continue with `CT01`, `CT02`, and `CT03`, because they carry the strongest circuit-facing benchmark claims.
