# Model Failure Attribution and Benchmark-Design Audit - 2026-05-29

Scope: current prompt-change full overlay plus the five-row EVAS/Spectre rulefix overlay. This is not a fresh 236-form full rerun.

## Claim Policy

- Count `model_behavior_failure` and `model_syntax_or_protocol_failure` as model-capability failures, with syntax/protocol reported separately from circuit behavior.
- Report `incomplete_generation_fixed_budget`, `runner_or_output_inconclusive`, and evaluator parity debt separately; do not use them as direct circuit-behavior capability evidence.
- Treat `prompt_contract_review`, `checker_design_review`, and `benchmark_design_review` as review flags, not automatic benchmark defects.

## Exclusive Model Summary

| model | total | pass | model_behavior_failure | model_syntax_or_protocol_failure | incomplete_generation_fixed_budget | runner_or_output_inconclusive | evaluator_parity_debt | model_claim_failures | not_direct_model_capability |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| deepseek | 236 | 68 | 121 | 33 | 14 | 0 | 0 | 154 | 14 |
| mimo | 236 | 57 | 101 | 48 | 23 | 7 | 0 | 149 | 30 |

## Cross-Model Review Counts

| rows | both_pass | deepseek_only_pass | mimo_only_pass | both_fail | both_fail_same_axis | both_fail_same_family | common_behavior_failure | common_artifact_or_protocol_failure | prompt_contract_review_rows | checker_design_review_rows | benchmark_design_review_rows |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 236 | 42 | 26 | 15 | 153 | 80 | 76 | 72 | 24 | 96 | 1 | 40 |

## Category Review

| category | rows | both_pass | both_fail | common_behavior_failure | prompt_contract_review | benchmark_design_review |
| --- | --- | --- | --- | --- | --- | --- |
| Baseband Signal Conditioning | 30 | 2 | 23 | 16 | 10 | 16 |
| Bias Reference and Power Management | 28 | 6 | 17 | 7 | 11 | 9 |
| Calibration, DEM, and Control | 26 | 1 | 22 | 13 | 10 | 0 |
| Comparator and Decision Circuits | 30 | 9 | 15 | 7 | 12 | 4 |
| Data Converter Models | 44 | 14 | 23 | 6 | 18 | 4 |
| PLL Clock and Timing Systems | 36 | 5 | 23 | 10 | 15 | 0 |
| RF and AFE Behavioral Macromodels | 24 | 2 | 18 | 6 | 15 | 7 |
| Sampling and Analog Memory | 18 | 3 | 12 | 7 | 5 | 0 |

## Highest-Priority Manual Review Queue

| release_task_id | category | difficulty | form | overlap | deepseek_bucket | mimo_bucket | deepseek_family | mimo_family | prompt_contract_review | checker_design_review | benchmark_design_review |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| vbr1_l1_acquisition_limited_sample_and_hold:dut | Sampling and Analog Memory | D2 | dut | both_fail | model_behavior_failure | model_syntax_or_protocol_failure | sample_hold_memory_behavior | veriloga_embedded_declaration | True | False | False |
| vbr1_l1_aperture_delay_track_and_hold:bugfix | Sampling and Analog Memory | D2 | bugfix | both_fail | model_behavior_failure | model_syntax_or_protocol_failure | sample_hold_memory_behavior | unsupported_event_variable_or_wait | True | False | False |
| vbr1_l1_aperture_delay_track_and_hold:dut | Sampling and Analog Memory | D2 | dut | both_fail | model_behavior_failure | model_syntax_or_protocol_failure | sample_hold_memory_behavior | unsupported_event_variable_or_wait | True | False | False |
| vbr1_l1_aperture_delay_track_and_hold:e2e | Sampling and Analog Memory | D2 | e2e | both_fail | model_behavior_failure | incomplete_generation_fixed_budget | sample_hold_memory_behavior | incomplete_generation | True | False | False |
| vbr1_l1_bandgap_reference_macro_model:e2e | Bias Reference and Power Management | D2 | e2e | both_fail | incomplete_generation_fixed_budget | model_behavior_failure | incomplete_generation | reference_power_behavior | True | False | False |
| vbr1_l1_bang_bang_phase_detector:bugfix | PLL Clock and Timing Systems | D2 | bugfix | both_fail | incomplete_generation_fixed_budget | model_syntax_or_protocol_failure | incomplete_generation | spectre_elaboration_parameter_or_topology_reject | True | False | False |
| vbr1_l1_bang_bang_phase_detector:dut | PLL Clock and Timing Systems | D2 | dut | both_fail | model_syntax_or_protocol_failure | model_behavior_failure | unsupported_event_variable_or_wait | timing_or_pll_behavior | True | False | False |
| vbr1_l1_bias_voltage_generator_with_enable_trim:e2e | Bias Reference and Power Management | D1 | e2e | both_fail | model_behavior_failure | incomplete_generation_fixed_budget | reference_power_behavior | incomplete_generation | True | False | True |
| vbr1_l1_bias_voltage_generator_with_enable_trim:tb | Bias Reference and Power Management | D1 | tb | both_fail | model_behavior_failure | model_behavior_failure | reference_power_behavior | reference_power_behavior | False | False | True |
| vbr1_l1_binary_weighted_voltage_dac:e2e | Data Converter Models | D1 | e2e | both_fail | model_syntax_or_protocol_failure | model_behavior_failure | spectre_tb_source_or_waveform_reject | converter_code_or_transfer_behavior | True | False | True |
| vbr1_l1_calibration_deadband_controller:bugfix | Calibration, DEM, and Control | D2 | bugfix | both_fail | model_syntax_or_protocol_failure | model_behavior_failure | veriloga_embedded_declaration | calibration_control_behavior | True | False | False |
| vbr1_l1_calibration_deadband_controller:dut | Calibration, DEM, and Control | D2 | dut | both_fail | model_behavior_failure | model_syntax_or_protocol_failure | calibration_control_behavior | veriloga_embedded_declaration | True | False | False |
| vbr1_l1_capacitive_weighted_sar_feedback_dac:bugfix | Data Converter Models | D2 | bugfix | both_fail | model_behavior_failure | model_syntax_or_protocol_failure | converter_code_or_transfer_behavior | guarded_transition_contribution | True | False | False |
| vbr1_l1_capacitive_weighted_sar_feedback_dac:tb | Data Converter Models | D2 | tb | both_fail | model_behavior_failure | incomplete_generation_fixed_budget | converter_code_or_transfer_behavior | incomplete_generation | True | False | False |
| vbr1_l1_clock_divider:bugfix | PLL Clock and Timing Systems | D2 | bugfix | both_fail | incomplete_generation_fixed_budget | incomplete_generation_fixed_budget | incomplete_generation | incomplete_generation | True | False | False |
| vbr1_l1_clock_divider:dut | PLL Clock and Timing Systems | D2 | dut | both_fail | incomplete_generation_fixed_budget | model_syntax_or_protocol_failure | incomplete_generation | guarded_transition_contribution | True | False | False |
| vbr1_l1_clocked_adc_quantizer:e2e | Data Converter Models | D2 | e2e | both_fail | model_behavior_failure | model_syntax_or_protocol_failure | converter_code_or_transfer_behavior | guarded_transition_contribution | True | False | False |
| vbr1_l1_dac_mismatch_unit_weighting_model:bugfix | Data Converter Models | D2 | bugfix | both_fail | model_syntax_or_protocol_failure | incomplete_generation_fixed_budget | veriloga_embedded_declaration | incomplete_generation | True | False | False |
| vbr1_l1_dac_mismatch_unit_weighting_model:dut | Data Converter Models | D2 | dut | both_fail | model_behavior_failure | model_syntax_or_protocol_failure | converter_code_or_transfer_behavior | guarded_transition_contribution | True | False | False |
| vbr1_l1_debounce_latch:e2e | Comparator and Decision Circuits | D2 | e2e | both_fail | model_syntax_or_protocol_failure | model_syntax_or_protocol_failure | unsupported_event_loop_form | unsupported_event_variable_or_wait | True | False | False |
| vbr1_l1_dwa_dem_encoder:bugfix | Calibration, DEM, and Control | D2 | bugfix | both_fail | model_syntax_or_protocol_failure | model_syntax_or_protocol_failure | guarded_transition_contribution | veriloga_embedded_declaration | True | False | False |
| vbr1_l1_dwa_dem_encoder:dut | Calibration, DEM, and Control | D2 | dut | both_fail | model_behavior_failure | incomplete_generation_fixed_budget | calibration_control_behavior | incomplete_generation | True | False | False |
| vbr1_l1_dwa_dem_encoder:e2e | Calibration, DEM, and Control | D2 | e2e | both_fail | model_syntax_or_protocol_failure | incomplete_generation_fixed_budget | veriloga_embedded_declaration | incomplete_generation | True | False | False |
| vbr1_l1_element_shuffler:bugfix | Calibration, DEM, and Control | D2 | bugfix | both_fail | model_behavior_failure | model_syntax_or_protocol_failure | calibration_control_behavior | guarded_transition_contribution | True | False | False |
| vbr1_l1_first_order_lowpass:e2e | Baseband Signal Conditioning | D1 | e2e | both_fail | model_behavior_failure | model_behavior_failure | baseband_dynamic_behavior | baseband_dynamic_behavior | False | False | True |
| vbr1_l1_first_order_lowpass:tb | Baseband Signal Conditioning | D1 | tb | both_fail | model_behavior_failure | model_behavior_failure | baseband_dynamic_behavior | baseband_dynamic_behavior | False | False | True |
| vbr1_l1_higher_order_filter:bugfix | Baseband Signal Conditioning | D2 | bugfix | both_fail | model_syntax_or_protocol_failure | model_behavior_failure | veriloga_embedded_declaration | baseband_dynamic_behavior | True | False | False |
| vbr1_l1_higher_order_filter:dut | Baseband Signal Conditioning | D2 | dut | both_fail | model_behavior_failure | model_syntax_or_protocol_failure | baseband_dynamic_behavior | guarded_transition_contribution | True | False | False |
| vbr1_l1_higher_order_filter:e2e | Baseband Signal Conditioning | D2 | e2e | both_fail | model_behavior_failure | model_behavior_failure | baseband_dynamic_behavior | baseband_dynamic_behavior | False | False | True |
| vbr1_l1_higher_order_filter:tb | Baseband Signal Conditioning | D2 | tb | both_fail | model_behavior_failure | model_behavior_failure | baseband_dynamic_behavior | baseband_dynamic_behavior | False | False | True |

## Interpretation

- The dominant shared signal is still real model weakness on behavioral circuit semantics: many rows compile and simulate but fail functional checkers.
- The benchmark is not yet clean enough to convert every non-pass into a model-ability claim: fixed-budget incomplete generations, runner/output inconclusive rows, syntax-contract failures, and D1/common-hard rows need separate reporting or manual review.
- Current EVAS/Spectre mismatch debt is zero after the rulefix overlay, so remaining parity failures should not be cited unless a fresh rerun reintroduces them.
