# vaBench Model Baseline Quality Audit

Generated: 2026-05-29T06:20:19.730516+00:00

This report audits benchmark-quality risks exposed by model baselines.
It is diagnostic: flagged rows/categories require human review before metadata changes.

## Model Score Slices

| Model | Slice | Rows | Strict dual pass | Pass rate | Meaning |
| --- | --- | ---: | ---: | ---: | --- |
| deepseek | `full_strict` | 236 | 59 | 25.00% | All scored rows. Incomplete generation and runner/output inconclusive rows are counted as failures. |
| deepseek | `valid_candidate` | 232 | 59 | 25.43% | Rows with complete model artifacts and a reliable evaluator judgment. Syntax and behavior failure... |
| deepseek | `behavior_ready` | 195 | 59 | 30.26% | Rows that reached the functional checker: strict dual pass plus model_behavior failure rows. |
| mimo | `full_strict` | 236 | 51 | 21.61% | All scored rows. Incomplete generation and runner/output inconclusive rows are counted as failures. |
| mimo | `valid_candidate` | 211 | 51 | 24.17% | Rows with complete model artifacts and a reliable evaluator judgment. Syntax and behavior failure... |
| mimo | `behavior_ready` | 164 | 51 | 31.10% | Rows that reached the functional checker: strict dual pass plus model_behavior failure rows. |

## Pass Overlap

| Metric | Value |
| --- | ---: |
| row count | 236 |
| both pass | 36 |
| deepseek only pass | 23 |
| mimo only pass | 15 |
| both fail | 162 |
| missing in one report | 0 |

## Difficulty Calibration Warnings

| Model | D1 rate | D1 rows | D2 rate | D2 rows | D3 rate | D3 rows | Flags | Interpretation |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| deepseek | 58.33% | 24 | 20.56% | 180 | 25.00% | 32 | D3_not_harder_than_D2 | Treat difficulty labels as requiring manual calibration; do not claim calibrated difficulty tiers... |
| mimo | 45.83% | 24 | 17.78% | 180 | 25.00% | 32 | D3_not_harder_than_D2, D1_low_pass_rate | Treat difficulty labels as requiring manual calibration; do not claim calibrated difficulty tiers... |

## Category Risk Audit

| Category | Rows | Both pass | deepseek only | mimo only | Both fail | deepseek rate | mimo rate | Common behavior fail | Artifact/protocol fail | Risk | Action |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| Baseband Signal Conditioning | 30 | 2 | 4 | 1 | 23 | 20.00% | 10.00% | 16 | 7 | `protocol_noise_sensitive` | Separate language/protocol failures from behavior claims and inspect public contracts for missing... |
| Bias Reference and Power Management | 28 | 0 | 4 | 0 | 24 | 14.29% | 0.00% | 12 | 12 | `zero_common_pass` | Manually audit prompts/checkers and category scope before using this as evidence of calibrated di... |
| Calibration, DEM, and Control | 26 | 1 | 0 | 3 | 22 | 3.85% | 15.38% | 13 | 9 | `protocol_noise_sensitive` | Separate language/protocol failures from behavior claims and inspect public contracts for missing... |
| Comparator and Decision Circuits | 30 | 9 | 6 | 0 | 15 | 50.00% | 30.00% | 7 | 8 | `protocol_noise_sensitive` | Separate language/protocol failures from behavior claims and inspect public contracts for missing... |
| Data Converter Models | 44 | 14 | 3 | 4 | 23 | 38.64% | 40.91% | 6 | 17 | `protocol_noise_sensitive` | Separate language/protocol failures from behavior claims and inspect public contracts for missing... |
| PLL Clock and Timing Systems | 36 | 5 | 4 | 4 | 23 | 25.00% | 25.00% | 10 | 13 | `protocol_noise_sensitive` | Separate language/protocol failures from behavior claims and inspect public contracts for missing... |
| RF and AFE Behavioral Macromodels | 24 | 2 | 1 | 1 | 20 | 12.50% | 12.50% | 11 | 9 | `common_hard_category` | Check whether the category is under-scaffolded or genuinely hard; keep as hard coverage only with... |
| Sampling and Analog Memory | 18 | 3 | 1 | 2 | 12 | 22.22% | 27.78% | 7 | 5 | `protocol_noise_sensitive` | Separate language/protocol failures from behavior claims and inspect public contracts for missing... |

## Form Audit

| Model | Form | Rows | Strict pass | Strict rate | Behavior-ready rows | Behavior-ready pass rate | Non-model/inconclusive |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| deepseek | `bugfix` | 52 | 13 | 25.00% | 41 | 31.71% | 2 |
| deepseek | `dut` | 52 | 19 | 36.54% | 42 | 45.24% | 0 |
| deepseek | `e2e` | 66 | 10 | 15.15% | 46 | 21.74% | 2 |
| deepseek | `tb` | 66 | 17 | 25.76% | 66 | 25.76% | 0 |
| mimo | `bugfix` | 52 | 12 | 23.08% | 33 | 36.36% | 2 |
| mimo | `dut` | 52 | 15 | 28.85% | 33 | 45.45% | 3 |
| mimo | `e2e` | 66 | 6 | 9.09% | 38 | 15.79% | 18 |
| mimo | `tb` | 66 | 18 | 27.27% | 60 | 30.00% | 2 |

## Difficulty Relabel Review Candidates

| Task | Difficulty | Form | Category | Reason | deepseek family | mimo family |
| --- | --- | --- | --- | --- | --- | --- |
| `vbr1_l1_binary_weighted_voltage_dac:e2e` | `D1` | `e2e` | Data Converter Models | D1 row failed by both baselines; check whether the task is under-specified, mislabeled, or genuin... | spectre_tb_source_or_waveform_reject | converter_code_or_transfer_behavior |
| `vbr1_l1_first_order_lowpass:e2e` | `D1` | `e2e` | Baseband Signal Conditioning | D1 row failed by both baselines; check whether the task is under-specified, mislabeled, or genuin... | baseband_dynamic_behavior | baseband_dynamic_behavior |
| `vbr1_l1_first_order_lowpass:tb` | `D1` | `tb` | Baseband Signal Conditioning | D1 row failed by both baselines; check whether the task is under-specified, mislabeled, or genuin... | baseband_dynamic_behavior | baseband_dynamic_behavior |
| `vbr1_l1_offset_comparator:bugfix` | `D1` | `bugfix` | Comparator and Decision Circuits | D1 row failed by both baselines; check whether the task is under-specified, mislabeled, or genuin... | decision_threshold_behavior | decision_threshold_behavior |
| `vbr1_l1_offset_comparator:dut` | `D1` | `dut` | Comparator and Decision Circuits | D1 row failed by both baselines; check whether the task is under-specified, mislabeled, or genuin... | decision_threshold_behavior | decision_threshold_behavior |
| `vbr1_l1_offset_comparator:e2e` | `D1` | `e2e` | Comparator and Decision Circuits | D1 row failed by both baselines; check whether the task is under-specified, mislabeled, or genuin... | decision_threshold_behavior | decision_threshold_behavior |
| `vbr1_l1_offset_comparator:tb` | `D1` | `tb` | Comparator and Decision Circuits | D1 row failed by both baselines; check whether the task is under-specified, mislabeled, or genuin... | decision_threshold_behavior | decision_threshold_behavior |
| `vbr1_l1_pipeline_adc_stage:e2e` | `D3` | `e2e` | Data Converter Models | D3 row passed by both baselines; check whether it is truly integration-level or over-labeled. | strict_dual_pass | strict_dual_pass |
| `vbr1_l1_pipeline_adc_stage:tb` | `D3` | `tb` | Data Converter Models | D3 row passed by both baselines; check whether it is truly integration-level or over-labeled. | strict_dual_pass | strict_dual_pass |
| `vbr1_l1_thermometer_code_decoder:e2e` | `D1` | `e2e` | Data Converter Models | D1 row failed by both baselines; check whether the task is under-specified, mislabeled, or genuin... | spectre_tb_source_or_waveform_reject | digital_verilog_in_veriloga |
| `vbr1_l1_thermometer_code_decoder:tb` | `D1` | `tb` | Data Converter Models | D1 row failed by both baselines; check whether the task is under-specified, mislabeled, or genuin... | converter_code_or_transfer_behavior | converter_code_or_transfer_behavior |
| `vbr1_l1_unit_element_thermometer_dac:tb` | `D1` | `tb` | Data Converter Models | D1 row failed by both baselines; check whether the task is under-specified, mislabeled, or genuin... | converter_code_or_transfer_behavior | converter_code_or_transfer_behavior |
| `vbr1_l2_amplifier_filter_chain:e2e` | `D3` | `e2e` | Baseband Signal Conditioning | D3 row passed by both baselines; check whether it is truly integration-level or over-labeled. | strict_dual_pass | strict_dual_pass |
| `vbr1_l2_comparator_measurement_flow:tb` | `D3` | `tb` | Comparator and Decision Circuits | D3 row passed by both baselines; check whether it is truly integration-level or over-labeled. | strict_dual_pass | strict_dual_pass |
| `vbr1_l2_converter_static_linearity_measurement_flow:tb` | `D3` | `tb` | Data Converter Models | D3 row passed by both baselines; check whether it is truly integration-level or over-labeled. | strict_dual_pass | strict_dual_pass |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow:tb` | `D3` | `tb` | PLL Clock and Timing Systems | D3 row passed by both baselines; check whether it is truly integration-level or over-labeled. | strict_dual_pass | strict_dual_pass |

## Common Failure Examples

| Task | Difficulty | Form | Category | deepseek axis/family | mimo axis/family | deepseek evidence | mimo evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `vbr1_l1_first_order_lowpass:e2e` | `D1` | `e2e` | Baseband Signal Conditioning | model_behavior/baseband_dynamic_behavior | model_behavior/baseband_dynamic_behavior | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_first_order_lowpass:tb` | `D1` | `tb` | Baseband Signal Conditioning | model_behavior/baseband_dynamic_behavior | model_behavior/baseband_dynamic_behavior | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_higher_order_filter:bugfix` | `D2` | `bugfix` | Baseband Signal Conditioning | model_dut_compile/veriloga_embedded_declaration | model_behavior/baseband_dynamic_behavior | ERROR (VACOMP-1917): "higher_order_filter.va", line 24: Encountered an | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_higher_order_filter:dut` | `D2` | `dut` | Baseband Signal Conditioning | model_behavior/baseband_dynamic_behavior | model_dut_compile/guarded_transition_contribution | FAIL_SIM_CORRECTNESS | ERROR (VACOMP-2143): "higher_order_filter.va", line 32: Encountered the |
| `vbr1_l1_higher_order_filter:e2e` | `D2` | `e2e` | Baseband Signal Conditioning | model_behavior/baseband_dynamic_behavior | model_behavior/baseband_dynamic_behavior | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_higher_order_filter:tb` | `D2` | `tb` | Baseband Signal Conditioning | model_behavior/baseband_dynamic_behavior | model_behavior/baseband_dynamic_behavior | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_precision_rectifier_envelope_detector:bugfix` | `D2` | `bugfix` | Baseband Signal Conditioning | model_dut_compile/veriloga_embedded_declaration | model_behavior/baseband_dynamic_behavior | ERROR (VACOMP-1917): "precision_rectifier_envelope_detector.va", line 34: | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_precision_rectifier_envelope_detector:e2e` | `D2` | `e2e` | Baseband Signal Conditioning | model_dut_compile/veriloga_embedded_declaration | model_behavior/baseband_dynamic_behavior | ERROR (VACOMP-1917): "precision_rectifier_envelope_detector.va", line 33: | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_precision_rectifier_envelope_detector:tb` | `D2` | `tb` | Baseband Signal Conditioning | model_behavior/baseband_dynamic_behavior | model_behavior/baseband_dynamic_behavior | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_programmable_gain_amplifier:bugfix` | `D2` | `bugfix` | Baseband Signal Conditioning | model_behavior/baseband_dynamic_behavior | model_dut_compile/guarded_transition_contribution | FAIL_SIM_CORRECTNESS | ERROR (VACOMP-2143): "programmable_gain_amplifier.va", line 55: Encountered |
| `vbr1_l1_programmable_gain_amplifier:dut` | `D2` | `dut` | Baseband Signal Conditioning | model_behavior/baseband_dynamic_behavior | model_behavior/baseband_dynamic_behavior | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_programmable_gain_amplifier:e2e` | `D2` | `e2e` | Baseband Signal Conditioning | model_behavior/baseband_dynamic_behavior | model_behavior/baseband_dynamic_behavior | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_programmable_gain_amplifier:tb` | `D2` | `tb` | Baseband Signal Conditioning | model_behavior/baseband_dynamic_behavior | model_behavior/baseband_dynamic_behavior | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_resettable_integrator:bugfix` | `D2` | `bugfix` | Baseband Signal Conditioning | model_behavior/baseband_dynamic_behavior | model_behavior/baseband_dynamic_behavior | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_resettable_integrator:dut` | `D2` | `dut` | Baseband Signal Conditioning | model_behavior/baseband_dynamic_behavior | model_behavior/baseband_dynamic_behavior | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_resettable_integrator:e2e` | `D2` | `e2e` | Baseband Signal Conditioning | model_behavior/baseband_dynamic_behavior | model_behavior/baseband_dynamic_behavior | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_resettable_integrator:tb` | `D2` | `tb` | Baseband Signal Conditioning | model_behavior/baseband_dynamic_behavior | model_behavior/baseband_dynamic_behavior | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_slew_rate_limiter:bugfix` | `D2` | `bugfix` | Baseband Signal Conditioning | model_behavior/baseband_dynamic_behavior | model_behavior/baseband_dynamic_behavior | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_slew_rate_limiter:e2e` | `D2` | `e2e` | Baseband Signal Conditioning | model_behavior/baseband_dynamic_behavior | model_dut_compile/guarded_transition_contribution | FAIL_SIM_CORRECTNESS | ERROR (VACOMP-2143): "slew_rate_limiter.va", line 15: Encountered the |
| `vbr1_l1_slew_rate_limiter:tb` | `D2` | `tb` | Baseband Signal Conditioning | model_behavior/baseband_dynamic_behavior | model_behavior/baseband_dynamic_behavior | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_soft_hysteretic_limiter:bugfix` | `D2` | `bugfix` | Baseband Signal Conditioning | model_behavior/baseband_dynamic_behavior | model_behavior/baseband_dynamic_behavior | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_soft_hysteretic_limiter:e2e` | `D2` | `e2e` | Baseband Signal Conditioning | model_dut_compile/guarded_transition_contribution | model_behavior/baseband_dynamic_behavior | ERROR (VACOMP-2146): "soft_hysteretic_limiter.va", line 35: Encountered the | FAIL_SIM_CORRECTNESS |
| `vbr1_l2_amplifier_filter_chain:tb` | `D3` | `tb` | Baseband Signal Conditioning | model_behavior/baseband_dynamic_behavior | model_behavior/baseband_dynamic_behavior | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_bandgap_reference_macro_model:bugfix` | `D2` | `bugfix` | Bias Reference and Power Management | model_dut_compile/veriloga_embedded_declaration | model_behavior/reference_power_behavior | ERROR (VACOMP-1917): "bandgap_reference_macro_model.va", line 57: | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_bandgap_reference_macro_model:e2e` | `D2` | `e2e` | Bias Reference and Power Management | model_behavior/reference_power_behavior | model_spectre_elab_or_topology/spectre_elaboration_parameter_or_topology_reject | FAIL_SIM_CORRECTNESS | (0) falls below lower bound in from range limit (0). |
| `vbr1_l1_bandgap_reference_macro_model:tb` | `D2` | `tb` | Bias Reference and Power Management | model_behavior/reference_power_behavior | model_behavior/reference_power_behavior | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_bias_voltage_generator_with_enable_trim:bugfix` | `D2` | `bugfix` | Bias Reference and Power Management | model_behavior/reference_power_behavior | model_behavior/reference_power_behavior | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_bias_voltage_generator_with_enable_trim:dut` | `D2` | `dut` | Bias Reference and Power Management | model_behavior/reference_power_behavior | model_behavior/reference_power_behavior | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_bias_voltage_generator_with_enable_trim:e2e` | `D2` | `e2e` | Bias Reference and Power Management | model_dut_compile/other_compile_failure | model_behavior/reference_power_behavior | tran.csv missing | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_bias_voltage_generator_with_enable_trim:tb` | `D2` | `tb` | Bias Reference and Power Management | model_behavior/reference_power_behavior | model_dut_compile/spectre_testbench_syntax | FAIL_SIM_CORRECTNESS | tran.csv missing |
| `vbr1_l1_ldo_regulator_macro_model:bugfix` | `D2` | `bugfix` | Bias Reference and Power Management | model_behavior/reference_power_behavior | model_dut_compile/veriloga_embedded_declaration | FAIL_SIM_CORRECTNESS | ERROR (VACOMP-1917): "ldo_regulator_macro_model.va", line 32: Encountered |
| `vbr1_l1_ldo_regulator_macro_model:dut` | `D2` | `dut` | Bias Reference and Power Management | model_behavior/reference_power_behavior | model_behavior/reference_power_behavior | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_ldo_regulator_macro_model:e2e` | `D2` | `e2e` | Bias Reference and Power Management | model_behavior/reference_power_behavior | model_behavior/reference_power_behavior | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_power_on_reset_detector:bugfix` | `D2` | `bugfix` | Bias Reference and Power Management | model_behavior/reference_power_behavior | model_dut_compile/unsupported_event_variable_or_wait | FAIL_SIM_CORRECTNESS | ERROR (VACOMP-2259): "event start_delay,<<--? release_reset, brownout;" |
| `vbr1_l1_power_on_reset_detector:dut` | `D2` | `dut` | Bias Reference and Power Management | model_behavior/reference_power_behavior | model_dut_compile/guarded_transition_contribution | FAIL_SIM_CORRECTNESS | ERROR (VACOMP-2143): "power_on_reset_detector.va", line 53: Encountered the |
| `vbr1_l1_power_on_reset_detector:e2e` | `D2` | `e2e` | Bias Reference and Power Management | model_behavior/reference_power_behavior | model_behavior/reference_power_behavior | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_power_on_reset_detector:tb` | `D2` | `tb` | Bias Reference and Power Management | model_behavior/reference_power_behavior | model_behavior/reference_power_behavior | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_ptat_ctat_reference_generator:bugfix` | `D2` | `bugfix` | Bias Reference and Power Management | model_dut_compile/unsupported_event_variable_or_wait | model_behavior/reference_power_behavior | tran.csv missing | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_ptat_ctat_reference_generator:dut` | `D2` | `dut` | Bias Reference and Power Management | model_behavior/reference_power_behavior | model_dut_compile/veriloga_embedded_declaration | FAIL_SIM_CORRECTNESS | ERROR (VACOMP-1917): "ptat_ctat_reference_generator.va", line 43: |
| `vbr1_l1_ptat_ctat_reference_generator:e2e` | `D2` | `e2e` | Bias Reference and Power Management | model_behavior/reference_power_behavior | model_spectre_ahdl_compile/spectre_ahdl_syntax_scope_or_operator_reject | FAIL_SIM_CORRECTNESS | ERROR (VACOMP-2259): "metric_voltage;<<--? " |

## Recommended Next Actions

- Report full_strict, valid_candidate, and behavior_ready rates separately in model-baseline discussion.
- Treat D1/D2/D3 as design-intent labels until manual calibration resolves flagged anomalies.
- Audit zero-common-pass and common-hard categories before claiming calibrated benchmark difficulty.
- Keep incomplete generation and runner/output inconclusive rows outside circuit-behavior error analysis, while still reporting them under fixed-budget model baselines.
