# vaBench v3 Score/Support Manifest

Date: 2026-07-06

## Summary

- Total active v3 tasks: **456**
- Numbered active tasks: **451**
- Unnumbered candidates: **5**
- Current scored benchmark tasks: **258**
- Current support tasks: **42**
- Non-scored language-extension tasks: **147**
- Non-scored candidate/provenance tasks: **9**

## Policy

- `source_of_truth`: benchmark-vabench-release-v3/reports/score_support_manifest.json
- `historical_denominators`: v1/v1.1 entry-form score denominators are provenance only and are not used to score the current v3 task tree.
- `scored_benchmark_rule`: Count current v3 tasks 001-300 except measurement/stimulus/testbench utility support categories.
- `support_rule`: Current v3 tasks 001-300 in measurement, stimulus, or testbench utility categories are certified support assets and excluded from the core score.
- `language_extension_rule`: Current numbered tasks above 300 are language/semantics extension rows unless explicitly promoted into a future score policy.
- `candidate_provenance_rule`: Unnumbered candidates and numbered behavior-extension candidates outside 001-300 are preserved as provenance/candidate material and excluded from the current core score.

## Score Roles

| Score role | Tasks | Score status |
| --- | ---: | --- |
| `scored_benchmark` | 258 | Counted in the current v3 core score. |
| `support` | 42 | Certified/reviewed separately; excluded from the core score. |
| `language_extension` | 147 | Non-scored Verilog-A language/semantics extension coverage. |
| `candidate_provenance` | 9 | Non-scored candidate/provenance material pending explicit promotion. |

## Support Tasks

| Task | Category | Level | Title |
| --- | --- | --- | --- |
| `020-thermometer-code-decoder` | `testbench_utility_modules` | `L1` | Thermometer Code Decoder |
| `050-bin-to-thermometer-decoder-8b` | `testbench_utility_modules` | `L1` | Binary To Thermometer Decoder 8b |
| `051-thermometer-to-binary-encoder-8b` | `testbench_utility_modules` | `L1` | Thermometer To Binary Encoder 8b |
| `058-config-latch-32b-clocked` | `testbench_utility_modules` | `L1` | Config Latch 32b Clocked |
| `059-config-latch-128b-static-enable` | `testbench_utility_modules` | `L1` | Config Latch 128b Static Enable |
| `060-config-shift-register-64b` | `testbench_utility_modules` | `L1` | Config Shift Register 64b |
| `061-bus-splitter-256-to-16x16` | `testbench_utility_modules` | `L1` | Bus Splitter 256 To 16x16 |
| `062-bus-combiner-16x16-to-256` | `testbench_utility_modules` | `L1` | Bus Combiner 16x16 To 256 |
| `063-masked-config-update-32b` | `testbench_utility_modules` | `L1` | Masked Config Update 32b |
| `064-edge-interval-tdc-8b` | `testbench_utility_modules` | `L1` | Edge Interval TDC 8b |
| `065-period-meter-16b` | `testbench_utility_modules` | `L1` | Period Meter 16b |
| `066-duty-cycle-meter-8b` | `testbench_utility_modules` | `L1` | Duty Cycle Meter 8b |
| `067-event-counter-windowed-16b` | `testbench_utility_modules` | `L1` | Event Counter Windowed 16b |
| `068-latency-counter-ready-valid-12b` | `testbench_utility_modules` | `L1` | Ready/Valid Latency Counter 12b |
| `069-settling-window-detector` | `testbench_utility_modules` | `L1` | Settling Window Detector |
| `070-active-low-reset-synchronizer` | `testbench_utility_modules` | `L1` | Active Low Reset Synchronizer |
| `071-active-high-reset-synchronizer` | `testbench_utility_modules` | `L1` | Active High Reset Synchronizer |
| `072-enable-gated-clock-pulse` | `testbench_utility_modules` | `L1` | Enable Gated Clock Pulse |
| `073-low-active-enable-decoder-4b` | `testbench_utility_modules` | `L1` | Low Active Enable Decoder 4b |
| `074-configurable-polarity-edge-detector` | `testbench_utility_modules` | `L1` | Configurable Polarity Edge Detector |
| `076-multiphase-clock-generator-4ph` | `testbench_utility_modules` | `L1` | Multiphase Clock Generator 4ph |
| `077-configurable-pulse-train-generator` | `testbench_utility_modules` | `L1` | Configurable Pulse Train Generator |
| `078-staircase-dac-stimulus-8b` | `testbench_utility_modules` | `L1` | Staircase DAC Stimulus 8b |
| `079-jittered-clock-source-deterministic` | `testbench_utility_modules` | `L1` | Deterministic Jittered Clock Source |
| `083-crossing-metric-writer` | `measurement_instrumentation_flows` | `L1` | Crossing Metric Writer |
| `084-peak-detector` | `measurement_instrumentation_flows` | `L1` | Peak Detector |
| `085-burst-clock-source` | `stimulus_source_generators` | `L1` | Burst Clock Source |
| `086-dither-noise-like-deterministic-source` | `stimulus_source_generators` | `L1` | Dither Noise Like Deterministic Source |
| `087-lfsr-prbs-generator` | `stimulus_source_generators` | `L1` | LFSR PRBS Generator |
| `088-ramp-step-source` | `stimulus_source_generators` | `L1` | Ramp Step Source |
| `089-sine-periodic-voltage-source` | `stimulus_source_generators` | `L1` | Sine Periodic Voltage Source |
| `098-edge-crossing-interval-timer` | `measurement_instrumentation_flows` | `L1` | Edge Crossing Interval Timer |
| `099-dither-adder` | `measurement_instrumentation_flows` | `L1` | Dither Adder |
| `100-final-step-file-metric` | `measurement_instrumentation_flows` | `L1` | Final Step File Metric |
| `101-fixed-gain-amplifier` | `measurement_instrumentation_flows` | `L1` | Fixed Gain Amplifier |
| `102-gain-estimator` | `measurement_instrumentation_flows` | `L1` | Gain Estimator |
| `106-programmable-stimulus-sequencer` | `stimulus_source_generators` | `L2` | Programmable Stimulus Sequencer |
| `110-settling-time-measurement` | `measurement_instrumentation_flows` | `L1` | Settling Time Measurement |
| `111-clocked-sine-source` | `measurement_instrumentation_flows` | `L2` | Clocked Sine Source |
| `213-tdc-ideal-edge-delta` | `measurement` | `L1` | TDC Ideal Edge Delta |
| `217-dac7-code-generator` | `stimulus` | `L1` | DAC7 Code Generator |
| `287-gain-extraction-flow` | `measurement_instrumentation_flows` | `L2` | Gain Extraction Flow |

## Category Counts By Score Role

### `candidate_provenance`

| Category | Tasks |
| --- | ---: |
| `bias_reference_power_management` | 5 |
| `pll_clock_timing` | 3 |
| `pll_clock_timing_systems` | 1 |

### `language_extension`

| Category | Tasks |
| --- | ---: |
| `veriloga_access_function_semantics` | 2 |
| `veriloga_alias_semantics` | 1 |
| `veriloga_analog_initial_semantics` | 1 |
| `veriloga_analog_primitive_semantics` | 2 |
| `veriloga_assert_semantics` | 1 |
| `veriloga_attribute_semantics` | 1 |
| `veriloga_branch_semantics` | 1 |
| `veriloga_continuous_time_semantics` | 2 |
| `veriloga_conversion_semantics` | 1 |
| `veriloga_dynamic_operator_semantics` | 2 |
| `veriloga_environment_function_semantics` | 6 |
| `veriloga_event_semantics` | 2 |
| `veriloga_file_read_semantics` | 9 |
| `veriloga_function_semantics` | 1 |
| `veriloga_hierarchy_semantics` | 8 |
| `veriloga_indirect_branch_semantics` | 2 |
| `veriloga_inherited_port_semantics` | 1 |
| `veriloga_integer_control_semantics` | 2 |
| `veriloga_kcl_contribution_semantics` | 4 |
| `veriloga_language_semantics` | 40 |
| `veriloga_laplace_filter_semantics` | 4 |
| `veriloga_math_function_semantics` | 1 |
| `veriloga_mfactor_semantics` | 2 |
| `veriloga_monte_carlo_semantics` | 1 |
| `veriloga_noise_analysis_semantics` | 12 |
| `veriloga_oomr_semantics` | 1 |
| `veriloga_preprocessor_control_semantics` | 7 |
| `veriloga_random_distribution_semantics` | 6 |
| `veriloga_rf_source_semantics` | 1 |
| `veriloga_simulator_control_semantics` | 1 |
| `veriloga_string_format_semantics` | 5 |
| `veriloga_system_output_semantics` | 2 |
| `veriloga_table_model_semantics` | 8 |
| `veriloga_vector_operator_semantics` | 2 |
| `veriloga_z_domain_filter_semantics` | 4 |
| `verilogams_discipline_semantics` | 1 |

### `scored_benchmark`

| Category | Tasks |
| --- | ---: |
| `analog_primitive` | 3 |
| `baseband_signal_conditioning` | 12 |
| `bias_reference_power_management` | 8 |
| `calibration` | 7 |
| `calibration_control` | 7 |
| `calibration_dem_control` | 1 |
| `clock_timing` | 16 |
| `clocking` | 2 |
| `comparator` | 10 |
| `comparator_decision` | 8 |
| `comparator_decision_circuits` | 1 |
| `data_converter` | 89 |
| `data_converter_models` | 2 |
| `digital_logic` | 19 |
| `filter_amp` | 1 |
| `logic` | 8 |
| `mixed_signal` | 32 |
| `pll_clock_timing` | 8 |
| `pll_clock_timing_systems` | 4 |
| `rf_afe_behavioral_macromodels` | 7 |
| `sampling_analog_memory` | 6 |
| `sampling_memory` | 1 |
| `signal_processing` | 1 |
| `timing` | 3 |
| `timing_primitive` | 2 |

### `support`

| Category | Tasks |
| --- | ---: |
| `measurement` | 1 |
| `measurement_instrumentation_flows` | 10 |
| `stimulus` | 1 |
| `stimulus_source_generators` | 6 |
| `testbench_utility_modules` | 24 |
