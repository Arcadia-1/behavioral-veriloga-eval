# vaBench Model Baseline Quality Audit

Generated: 2026-05-29T07:35:45.341517+00:00

This report audits benchmark-quality risks exposed by model baselines.
It is diagnostic: flagged rows/categories require human review before metadata changes.

## Model Score Slices

| Model | Slice | Rows | Strict dual pass | Pass rate | Meaning |
| --- | --- | ---: | ---: | ---: | --- |
| deepseek | `full_strict` | 236 | 66 | 27.97% | All scored rows. Incomplete generation and runner/output inconclusive rows are counted as failures. |
| deepseek | `valid_candidate` | 222 | 66 | 29.73% | Rows with complete model artifacts and a reliable evaluator judgment. Syntax and behavior failure... |
| deepseek | `behavior_ready` | 187 | 66 | 35.29% | Rows that reached the functional checker: strict dual pass plus model_behavior failure rows. |
| mimo | `full_strict` | 236 | 55 | 23.31% | All scored rows. Incomplete generation and runner/output inconclusive rows are counted as failures. |
| mimo | `valid_candidate` | 206 | 55 | 26.70% | Rows with complete model artifacts and a reliable evaluator judgment. Syntax and behavior failure... |
| mimo | `behavior_ready` | 155 | 55 | 35.48% | Rows that reached the functional checker: strict dual pass plus model_behavior failure rows. |

## Pass Overlap

| Metric | Value |
| --- | ---: |
| row count | 236 |
| both pass | 40 |
| deepseek only pass | 26 |
| mimo only pass | 15 |
| both fail | 155 |
| missing in one report | 0 |

## Difficulty Calibration Warnings

| Model | D1 rate | D1 rows | D2 rate | D2 rows | D3 rate | D3 rows | Flags | Interpretation |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| deepseek | 52.78% | 36 | 24.38% | 160 | 20.00% | 40 | none | No monotonicity warning from this model alone. |
| mimo | 36.11% | 36 | 21.25% | 160 | 20.00% | 40 | D1_low_pass_rate | Treat difficulty labels as requiring manual calibration; do not claim calibrated difficulty tiers... |

## Category Risk Audit

| Category | Rows | Both pass | deepseek only | mimo only | Both fail | deepseek rate | mimo rate | Common behavior fail | Artifact/protocol fail | Risk | Action |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| Baseband Signal Conditioning | 30 | 2 | 4 | 1 | 23 | 20.00% | 10.00% | 16 | 7 | `protocol_noise_sensitive` | Separate language/protocol failures from behavior claims and inspect public contracts for missing... |
| Bias Reference and Power Management | 28 | 5 | 4 | 1 | 18 | 32.14% | 21.43% | 7 | 10 | `protocol_noise_sensitive` | Separate language/protocol failures from behavior claims and inspect public contracts for missing... |
| Calibration, DEM, and Control | 26 | 1 | 0 | 3 | 22 | 3.85% | 15.38% | 13 | 9 | `protocol_noise_sensitive` | Separate language/protocol failures from behavior claims and inspect public contracts for missing... |
| Comparator and Decision Circuits | 30 | 9 | 6 | 0 | 15 | 50.00% | 30.00% | 7 | 8 | `protocol_noise_sensitive` | Separate language/protocol failures from behavior claims and inspect public contracts for missing... |
| Data Converter Models | 44 | 14 | 3 | 4 | 23 | 38.64% | 40.91% | 6 | 17 | `protocol_noise_sensitive` | Separate language/protocol failures from behavior claims and inspect public contracts for missing... |
| PLL Clock and Timing Systems | 36 | 5 | 4 | 4 | 23 | 25.00% | 25.00% | 10 | 13 | `protocol_noise_sensitive` | Separate language/protocol failures from behavior claims and inspect public contracts for missing... |
| RF and AFE Behavioral Macromodels | 24 | 1 | 4 | 0 | 19 | 20.83% | 4.17% | 5 | 12 | `protocol_noise_sensitive` | Separate language/protocol failures from behavior claims and inspect public contracts for missing... |
| Sampling and Analog Memory | 18 | 3 | 1 | 2 | 12 | 22.22% | 27.78% | 7 | 5 | `protocol_noise_sensitive` | Separate language/protocol failures from behavior claims and inspect public contracts for missing... |

## Form Audit

| Model | Form | Rows | Strict pass | Strict rate | Behavior-ready rows | Behavior-ready pass rate | Non-model/inconclusive |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| deepseek | `bugfix` | 52 | 18 | 34.62% | 41 | 43.90% | 3 |
| deepseek | `dut` | 52 | 23 | 44.23% | 40 | 57.50% | 2 |
| deepseek | `e2e` | 66 | 10 | 15.15% | 42 | 23.81% | 8 |
| deepseek | `tb` | 66 | 15 | 22.73% | 64 | 23.44% | 1 |
| mimo | `bugfix` | 52 | 14 | 26.92% | 31 | 45.16% | 4 |
| mimo | `dut` | 52 | 16 | 30.77% | 30 | 53.33% | 2 |
| mimo | `e2e` | 66 | 7 | 10.61% | 36 | 19.44% | 20 |
| mimo | `tb` | 66 | 18 | 27.27% | 58 | 31.03% | 4 |

## Difficulty Relabel Review Candidates

| Task | Difficulty | Form | Category | Reason | deepseek family | mimo family |
| --- | --- | --- | --- | --- | --- | --- |
| `vbr1_l1_bias_voltage_generator_with_enable_trim:dut` | `D1` | `dut` | Bias Reference and Power Management | D1 row failed by both baselines; check whether the task is under-specified, mislabeled, or genuin... | spectre_pass_evas_fail_behavior | reference_power_behavior |
| `vbr1_l1_bias_voltage_generator_with_enable_trim:e2e` | `D1` | `e2e` | Bias Reference and Power Management | D1 row failed by both baselines; check whether the task is under-specified, mislabeled, or genuin... | reference_power_behavior | incomplete_generation |
| `vbr1_l1_bias_voltage_generator_with_enable_trim:tb` | `D1` | `tb` | Bias Reference and Power Management | D1 row failed by both baselines; check whether the task is under-specified, mislabeled, or genuin... | reference_power_behavior | reference_power_behavior |
| `vbr1_l1_binary_weighted_voltage_dac:e2e` | `D1` | `e2e` | Data Converter Models | D1 row failed by both baselines; check whether the task is under-specified, mislabeled, or genuin... | spectre_tb_source_or_waveform_reject | converter_code_or_transfer_behavior |
| `vbr1_l1_first_order_lowpass:e2e` | `D1` | `e2e` | Baseband Signal Conditioning | D1 row failed by both baselines; check whether the task is under-specified, mislabeled, or genuin... | baseband_dynamic_behavior | baseband_dynamic_behavior |
| `vbr1_l1_first_order_lowpass:tb` | `D1` | `tb` | Baseband Signal Conditioning | D1 row failed by both baselines; check whether the task is under-specified, mislabeled, or genuin... | baseband_dynamic_behavior | baseband_dynamic_behavior |
| `vbr1_l1_limiting_amplifier_frontend:e2e` | `D1` | `e2e` | RF and AFE Behavioral Macromodels | D1 row failed by both baselines; check whether the task is under-specified, mislabeled, or genuin... | incomplete_generation | rf_afe_macro_behavior |
| `vbr1_l1_limiting_amplifier_frontend:tb` | `D1` | `tb` | RF and AFE Behavioral Macromodels | D1 row failed by both baselines; check whether the task is under-specified, mislabeled, or genuin... | rf_afe_macro_behavior | rf_afe_macro_behavior |
| `vbr1_l1_offset_comparator:bugfix` | `D1` | `bugfix` | Comparator and Decision Circuits | D1 row failed by both baselines; check whether the task is under-specified, mislabeled, or genuin... | decision_threshold_behavior | decision_threshold_behavior |
| `vbr1_l1_offset_comparator:dut` | `D1` | `dut` | Comparator and Decision Circuits | D1 row failed by both baselines; check whether the task is under-specified, mislabeled, or genuin... | decision_threshold_behavior | decision_threshold_behavior |
| `vbr1_l1_offset_comparator:e2e` | `D1` | `e2e` | Comparator and Decision Circuits | D1 row failed by both baselines; check whether the task is under-specified, mislabeled, or genuin... | decision_threshold_behavior | decision_threshold_behavior |
| `vbr1_l1_offset_comparator:tb` | `D1` | `tb` | Comparator and Decision Circuits | D1 row failed by both baselines; check whether the task is under-specified, mislabeled, or genuin... | decision_threshold_behavior | decision_threshold_behavior |
| `vbr1_l1_pipeline_adc_stage:e2e` | `D3` | `e2e` | Data Converter Models | D3 row passed by both baselines; check whether it is truly integration-level or over-labeled. | strict_dual_pass | strict_dual_pass |
| `vbr1_l1_pipeline_adc_stage:tb` | `D3` | `tb` | Data Converter Models | D3 row passed by both baselines; check whether it is truly integration-level or over-labeled. | strict_dual_pass | strict_dual_pass |
| `vbr1_l1_thermometer_code_decoder:e2e` | `D1` | `e2e` | Data Converter Models | D1 row failed by both baselines; check whether the task is under-specified, mislabeled, or genuin... | spectre_tb_source_or_waveform_reject | digital_verilog_in_veriloga |
| `vbr1_l1_thermometer_code_decoder:tb` | `D1` | `tb` | Data Converter Models | D1 row failed by both baselines; check whether the task is under-specified, mislabeled, or genuin... | converter_code_or_transfer_behavior | converter_code_or_transfer_behavior |
| `vbr1_l1_unit_element_thermometer_dac:tb` | `D1` | `tb` | Data Converter Models | D1 row failed by both baselines; check whether the task is under-specified, mislabeled, or genuin... | converter_code_or_transfer_behavior | converter_code_or_transfer_behavior |
| `vbr1_l1_uvlo_brownout_detector:e2e` | `D1` | `e2e` | Bias Reference and Power Management | D1 row failed by both baselines; check whether the task is under-specified, mislabeled, or genuin... | reference_power_behavior | incomplete_generation |
| `vbr1_l1_uvlo_brownout_detector:tb` | `D1` | `tb` | Bias Reference and Power Management | D1 row failed by both baselines; check whether the task is under-specified, mislabeled, or genuin... | reference_power_behavior | reference_power_behavior |
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
| `vbr1_l1_bias_voltage_generator_with_enable_trim:dut` | `D1` | `dut` | Bias Reference and Power Management | evas_spectre_mismatch/spectre_pass_evas_fail_behavior | model_behavior/reference_power_behavior | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_bias_voltage_generator_with_enable_trim:e2e` | `D1` | `e2e` | Bias Reference and Power Management | model_behavior/reference_power_behavior | generation/incomplete_generation | FAIL_SIM_CORRECTNESS | no_code_extracted |
| `vbr1_l1_bias_voltage_generator_with_enable_trim:tb` | `D1` | `tb` | Bias Reference and Power Management | model_behavior/reference_power_behavior | model_behavior/reference_power_behavior | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_uvlo_brownout_detector:e2e` | `D1` | `e2e` | Bias Reference and Power Management | model_behavior/reference_power_behavior | generation/incomplete_generation | spectre:uvlo_hysteresis_hold_failed good=0.898 hold=0.000 | no_code_extracted |
| `vbr1_l1_uvlo_brownout_detector:tb` | `D1` | `tb` | Bias Reference and Power Management | model_behavior/reference_power_behavior | model_behavior/reference_power_behavior | spectre:uvlo_brownout_or_lower_hold_failed brownout=0.000 hold=0.524 | spectre:uvlo_hysteresis_hold_failed good=0.693 hold=0.596 |
| `vbr1_l1_bandgap_reference_macro_model:e2e` | `D2` | `e2e` | Bias Reference and Power Management | generation/incomplete_generation | model_behavior/reference_power_behavior | no_code_extracted | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_bandgap_reference_macro_model:tb` | `D2` | `tb` | Bias Reference and Power Management | model_behavior/reference_power_behavior | runner/spectre_run_inconclusive | FAIL_SIM_CORRECTNESS | spectre:tran_spectre.csv missing or run failed |
| `vbr1_l1_ldo_regulator_macro_model:bugfix` | `D2` | `bugfix` | Bias Reference and Power Management | model_behavior/reference_power_behavior | runner/spectre_run_inconclusive | FAIL_SIM_CORRECTNESS | spectre:tran_spectre.csv missing or run failed |
| `vbr1_l1_ldo_regulator_macro_model:dut` | `D2` | `dut` | Bias Reference and Power Management | model_behavior/reference_power_behavior | model_behavior/reference_power_behavior | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_ldo_regulator_macro_model:e2e` | `D2` | `e2e` | Bias Reference and Power Management | model_dut_compile/veriloga_embedded_declaration | model_behavior/reference_power_behavior | ERROR (VACOMP-1917): "ldo_regulator_macro_model.va", line 53: Encountered | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_ldo_regulator_macro_model:tb` | `D2` | `tb` | Bias Reference and Power Management | model_behavior/reference_power_behavior | model_behavior/reference_power_behavior | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_power_on_reset_detector:dut` | `D2` | `dut` | Bias Reference and Power Management | model_behavior/reference_power_behavior | model_dut_compile/guarded_transition_contribution | FAIL_SIM_CORRECTNESS | ERROR (VACOMP-2143): "power_on_reset_detector.va", line 52: Encountered the |
| `vbr1_l1_power_on_reset_detector:e2e` | `D2` | `e2e` | Bias Reference and Power Management | generation/incomplete_generation | model_behavior/reference_power_behavior | no_code_extracted | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_power_on_reset_detector:tb` | `D2` | `tb` | Bias Reference and Power Management | model_behavior/reference_power_behavior | model_behavior/reference_power_behavior | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |
| `vbr1_l2_ldo_load_step_recovery_flow:e2e` | `D3` | `e2e` | Bias Reference and Power Management | generation/incomplete_generation | model_spectre_ahdl_compile/spectre_ahdl_syntax_scope_or_operator_reject | no_code_extracted | FATAL (ASL-4201): "ldo_load_step_recovery_flow.va" 41: XDUT: Illegal value |
| `vbr1_l2_ldo_load_step_recovery_flow:tb` | `D3` | `tb` | Bias Reference and Power Management | model_behavior/reference_power_behavior | model_behavior/reference_power_behavior | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |
| `vbr1_l2_reference_startup_enable_flow:e2e` | `D3` | `e2e` | Bias Reference and Power Management | generation/incomplete_generation | generation/incomplete_generation | no_code_extracted | no_code_extracted |

## Recommended Next Actions

- Report full_strict, valid_candidate, and behavior_ready rates separately in model-baseline discussion.
- Treat D1/D2/D3 as design-intent labels until manual calibration resolves flagged anomalies.
- Audit zero-common-pass and common-hard categories before claiming calibrated benchmark difficulty.
- Keep incomplete generation and runner/output inconclusive rows outside circuit-behavior error analysis, while still reporting them under fixed-budget model baselines.
