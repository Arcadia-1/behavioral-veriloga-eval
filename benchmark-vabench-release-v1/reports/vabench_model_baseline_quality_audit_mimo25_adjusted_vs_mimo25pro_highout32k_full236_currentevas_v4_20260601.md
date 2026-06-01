# vaBench Model Baseline Quality Audit

Generated: 2026-05-31T17:39:48.680040+00:00

This report audits benchmark-quality risks exposed by model baselines.
It is diagnostic: flagged rows/categories require human review before metadata changes.

## Model Score Slices

| Model | Slice | Rows | Strict dual pass | Pass rate | Meaning |
| --- | --- | ---: | ---: | ---: | --- |
| mimo-v2.5-adjusted | `full_strict` | 236 | 85 | 36.02% | All scored rows. Incomplete generation and runner/output inconclusive rows are counted as failures. |
| mimo-v2.5-adjusted | `valid_candidate` | 234 | 85 | 36.32% | Rows with complete model artifacts and a reliable evaluator judgment. Syntax and behavior failure... |
| mimo-v2.5-adjusted | `behavior_ready` | 153 | 85 | 55.56% | Rows that reached the functional checker: strict dual pass plus model_behavior failure rows. |
| mimo-v2.5-pro-highout32k | `full_strict` | 236 | 113 | 47.88% | All scored rows. Incomplete generation and runner/output inconclusive rows are counted as failures. |
| mimo-v2.5-pro-highout32k | `valid_candidate` | 225 | 113 | 50.22% | Rows with complete model artifacts and a reliable evaluator judgment. Syntax and behavior failure... |
| mimo-v2.5-pro-highout32k | `behavior_ready` | 191 | 113 | 59.16% | Rows that reached the functional checker: strict dual pass plus model_behavior failure rows. |

## Pass Overlap

| Metric | Value |
| --- | ---: |
| row count | 236 |
| both pass | 74 |
| mimo-v2.5-adjusted only pass | 11 |
| mimo-v2.5-pro-highout32k only pass | 39 |
| both fail | 112 |
| missing in one report | 0 |

## Difficulty Calibration Warnings

| Model | D1 rate | D1 rows | D2 rate | D2 rows | D3 rate | D3 rows | Flags | Interpretation |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| mimo-v2.5-adjusted | 61.11% | 36 | 30.00% | 160 | 37.50% | 40 | D3_not_harder_than_D2 | Treat difficulty labels as requiring manual calibration; do not claim calibrated difficulty tiers... |
| mimo-v2.5-pro-highout32k | 91.67% | 36 | 40.62% | 160 | 37.50% | 40 | none | No monotonicity warning from this model alone. |

## Category Risk Audit

| Category | Rows | Both pass | mimo-v2.5-adjusted only | mimo-v2.5-pro-highout32k only | Both fail | mimo-v2.5-adjusted rate | mimo-v2.5-pro-highout32k rate | Common behavior fail | Artifact/protocol fail | Risk | Action |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| Baseband Signal Conditioning | 30 | 11 | 0 | 7 | 12 | 36.67% | 60.00% | 3 | 9 | `protocol_noise_sensitive` | Separate language/protocol failures from behavior claims and inspect public contracts for missing... |
| Bias Reference and Power Management | 28 | 8 | 1 | 6 | 13 | 32.14% | 50.00% | 5 | 8 | `protocol_noise_sensitive` | Separate language/protocol failures from behavior claims and inspect public contracts for missing... |
| Calibration, DEM, and Control | 26 | 4 | 1 | 3 | 18 | 19.23% | 26.92% | 8 | 10 | `protocol_noise_sensitive` | Separate language/protocol failures from behavior claims and inspect public contracts for missing... |
| Comparator and Decision Circuits | 30 | 14 | 2 | 6 | 8 | 53.33% | 66.67% | 3 | 5 | `balanced` | Keep as normal benchmark coverage; inspect row-level failures only if paper wording overclaims. |
| Data Converter Models | 44 | 16 | 3 | 4 | 21 | 43.18% | 45.45% | 8 | 13 | `protocol_noise_sensitive` | Separate language/protocol failures from behavior claims and inspect public contracts for missing... |
| PLL Clock and Timing Systems | 36 | 9 | 1 | 6 | 20 | 27.78% | 41.67% | 7 | 13 | `protocol_noise_sensitive` | Separate language/protocol failures from behavior claims and inspect public contracts for missing... |
| RF and AFE Behavioral Macromodels | 24 | 8 | 2 | 4 | 10 | 41.67% | 50.00% | 4 | 6 | `protocol_noise_sensitive` | Separate language/protocol failures from behavior claims and inspect public contracts for missing... |
| Sampling and Analog Memory | 18 | 4 | 1 | 3 | 10 | 27.78% | 38.89% | 5 | 5 | `protocol_noise_sensitive` | Separate language/protocol failures from behavior claims and inspect public contracts for missing... |

## Form Audit

| Model | Form | Rows | Strict pass | Strict rate | Behavior-ready rows | Behavior-ready pass rate | Non-model/inconclusive |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| mimo-v2.5-adjusted | `bugfix` | 52 | 37 | 71.15% | 48 | 77.08% | 1 |
| mimo-v2.5-adjusted | `dut` | 52 | 12 | 23.08% | 18 | 66.67% | 1 |
| mimo-v2.5-adjusted | `e2e` | 66 | 3 | 4.55% | 29 | 10.34% | 0 |
| mimo-v2.5-adjusted | `tb` | 66 | 33 | 50.00% | 58 | 56.90% | 0 |
| mimo-v2.5-pro-highout32k | `bugfix` | 52 | 42 | 80.77% | 51 | 82.35% | 1 |
| mimo-v2.5-pro-highout32k | `dut` | 52 | 20 | 38.46% | 36 | 55.56% | 0 |
| mimo-v2.5-pro-highout32k | `e2e` | 66 | 16 | 24.24% | 46 | 34.78% | 6 |
| mimo-v2.5-pro-highout32k | `tb` | 66 | 35 | 53.03% | 58 | 60.34% | 4 |

## Difficulty Relabel Review Candidates

| Task | Difficulty | Form | Category | Reason | mimo-v2.5-adjusted family | mimo-v2.5-pro-highout32k family |
| --- | --- | --- | --- | --- | --- | --- |
| `vbr1_l1_log_rssi_power_detector:bugfix` | `D3` | `bugfix` | RF and AFE Behavioral Macromodels | D3 row passed by both baselines; check whether it is truly integration-level or over-labeled. | strict_dual_pass | strict_dual_pass |
| `vbr1_l1_log_rssi_power_detector:tb` | `D3` | `tb` | RF and AFE Behavioral Macromodels | D3 row passed by both baselines; check whether it is truly integration-level or over-labeled. | strict_dual_pass | strict_dual_pass |
| `vbr1_l1_pa_compression_macro:tb` | `D3` | `tb` | RF and AFE Behavioral Macromodels | D3 row passed by both baselines; check whether it is truly integration-level or over-labeled. | strict_dual_pass | strict_dual_pass |
| `vbr1_l1_pipeline_adc_stage:bugfix` | `D3` | `bugfix` | Data Converter Models | D3 row passed by both baselines; check whether it is truly integration-level or over-labeled. | strict_dual_pass | strict_dual_pass |
| `vbr1_l1_unit_element_thermometer_dac:e2e` | `D1` | `e2e` | Data Converter Models | D1 row failed by both baselines; check whether the task is under-specified, mislabeled, or genuin... | converter_code_or_transfer_behavior | spectre_testbench_syntax |
| `vbr1_l2_amplifier_filter_chain:tb` | `D3` | `tb` | Baseband Signal Conditioning | D3 row passed by both baselines; check whether it is truly integration-level or over-labeled. | strict_dual_pass | strict_dual_pass |
| `vbr1_l2_comparator_measurement_flow:e2e` | `D3` | `e2e` | Comparator and Decision Circuits | D3 row passed by both baselines; check whether it is truly integration-level or over-labeled. | strict_dual_pass | strict_dual_pass |
| `vbr1_l2_comparator_measurement_flow:tb` | `D3` | `tb` | Comparator and Decision Circuits | D3 row passed by both baselines; check whether it is truly integration-level or over-labeled. | strict_dual_pass | strict_dual_pass |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow:tb` | `D3` | `tb` | PLL Clock and Timing Systems | D3 row passed by both baselines; check whether it is truly integration-level or over-labeled. | strict_dual_pass | strict_dual_pass |
| `vbr1_l2_flash_adc_mini_array:tb` | `D3` | `tb` | Data Converter Models | D3 row passed by both baselines; check whether it is truly integration-level or over-labeled. | strict_dual_pass | strict_dual_pass |
| `vbr1_l2_iq_downconversion_chain:tb` | `D3` | `tb` | RF and AFE Behavioral Macromodels | D3 row passed by both baselines; check whether it is truly integration-level or over-labeled. | strict_dual_pass | strict_dual_pass |
| `vbr1_l2_reference_startup_enable_flow:tb` | `D3` | `tb` | Bias Reference and Power Management | D3 row passed by both baselines; check whether it is truly integration-level or over-labeled. | strict_dual_pass | strict_dual_pass |

## Common Failure Examples

| Task | Difficulty | Form | Category | mimo-v2.5-adjusted axis/family | mimo-v2.5-pro-highout32k axis/family | mimo-v2.5-adjusted evidence | mimo-v2.5-pro-highout32k evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `vbr1_l1_higher_order_filter:dut` | `D2` | `dut` | Baseband Signal Conditioning | model_behavior/baseband_dynamic_behavior | model_behavior/baseband_dynamic_behavior | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_higher_order_filter:e2e` | `D2` | `e2e` | Baseband Signal Conditioning | model_spectre_elab_or_topology/spectre_elaboration_parameter_or_topology_reject | model_dut_compile/guarded_transition_contribution | spectre_failed rc=1 | ERROR (VACOMP-2143): "higher_order_filter.va", line 18: Encountered the |
| `vbr1_l1_precision_rectifier_envelope_detector:dut` | `D2` | `dut` | Baseband Signal Conditioning | model_dut_compile/guarded_transition_contribution | model_dut_compile/veriloga_embedded_declaration | ERROR (VACOMP-2259): "env_val = env_val - ((env_val - rect_val) * $realtime | ERROR (VACOMP-1917): "precision_rectifier_envelope_detector.va", line 26: |
| `vbr1_l1_precision_rectifier_envelope_detector:e2e` | `D2` | `e2e` | Baseband Signal Conditioning | model_behavior/baseband_dynamic_behavior | model_behavior/baseband_dynamic_behavior | FAIL_SIM_CORRECTNESS | spectre:rectifier_positive_half_not_rectified=0.447 |
| `vbr1_l1_programmable_gain_amplifier:dut` | `D2` | `dut` | Baseband Signal Conditioning | model_spectre_ahdl_compile/spectre_ahdl_syntax_scope_or_operator_reject | model_dut_compile/restricted_analog_operator_placement | ERROR (VACOMP-2259): "parameter real vcm = 0.5 from (0:0.001:<<--? 1.0);" | ERROR (VACOMP-2146): "programmable_gain_amplifier.va", line 39: Encountered |
| `vbr1_l1_resettable_integrator:dut` | `D2` | `dut` | Baseband Signal Conditioning | model_dut_compile/guarded_transition_contribution | model_behavior/baseband_dynamic_behavior | ERROR (VACOMP-2143): "resettable_integrator.va", line 23: Encountered the | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_resettable_integrator:e2e` | `D2` | `e2e` | Baseband Signal Conditioning | model_dut_compile/guarded_transition_contribution | model_dut_compile/guarded_transition_contribution | ERROR (VACOMP-2143): "resettable_integrator.va", line 41: Encountered the | ERROR (VACOMP-2143): "resettable_integrator.va", line 14: Encountered the |
| `vbr1_l1_slew_rate_limiter:dut` | `D2` | `dut` | Baseband Signal Conditioning | model_dut_compile/veriloga_embedded_declaration | model_dut_compile/veriloga_embedded_declaration | ERROR (VACOMP-1917): "slew_rate_limiter.va", line 23: Encountered an | ERROR (VACOMP-1917): "slew_rate_limiter.va", line 15: Encountered an |
| `vbr1_l1_slew_rate_limiter:e2e` | `D2` | `e2e` | Baseband Signal Conditioning | model_dut_compile/guarded_transition_contribution | model_behavior/baseband_dynamic_behavior | ERROR (VACOMP-2143): "slew_rate_limiter.va", line 29: Encountered the | spectre:slew_samples=0.450,0.150,0.000,0.000,0.000 input_sequence=False rising_limited=False high... |
| `vbr1_l1_soft_hysteretic_limiter:bugfix` | `D2` | `bugfix` | Baseband Signal Conditioning | model_behavior/baseband_dynamic_behavior | model_behavior/baseband_dynamic_behavior | spectre:soft_limiter_metric_not_stateful high=0.000/0.000 low=0.000/0.000 | spectre:soft_limiter_metric_not_stateful high=0.526/0.450 low=0.376/0.483 |
| `vbr1_l1_soft_hysteretic_limiter:dut` | `D2` | `dut` | Baseband Signal Conditioning | model_dut_compile/other_compile_failure | model_dut_compile/guarded_transition_contribution | ERROR (VACOMP-1552): "soft_hysteretic_limiter.va", line 34: Encountered | ERROR (VACOMP-2143): "soft_hysteretic_limiter.va", line 68: Encountered the |
| `vbr1_l1_soft_hysteretic_limiter:e2e` | `D2` | `e2e` | Baseband Signal Conditioning | model_behavior/baseband_dynamic_behavior | model_spectre_ahdl_compile/spectre_ahdl_syntax_scope_or_operator_reject | FAIL_SIM_CORRECTNESS | ERROR (SFE-23): |
| `vbr1_l1_bandgap_reference_macro_model:bugfix` | `D2` | `bugfix` | Bias Reference and Power Management | model_behavior/reference_power_behavior | model_behavior/reference_power_behavior | spectre:bandgap_brownout_not_reset=0.550 | spectre:bandgap_brownout_not_reset=0.550 |
| `vbr1_l1_bandgap_reference_macro_model:dut` | `D2` | `dut` | Bias Reference and Power Management | model_spectre_ahdl_compile/spectre_ahdl_syntax_scope_or_operator_reject | model_behavior/reference_power_behavior | ERROR (VACOMP-2259): "task update_state;<<--? " | spectre:bandgap_brownout_not_reset=0.550 |
| `vbr1_l1_bandgap_reference_macro_model:e2e` | `D2` | `e2e` | Bias Reference and Power Management | model_spectre_ahdl_compile/spectre_ahdl_syntax_scope_or_operator_reject | model_behavior/reference_power_behavior | ERROR (VACOMP-1552): "@(cross(rst - v_threshold)<<--? ) begin" | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_bandgap_reference_macro_model:tb` | `D2` | `tb` | Bias Reference and Power Management | model_behavior/reference_power_behavior | model_behavior/reference_power_behavior | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_ldo_regulator_macro_model:bugfix` | `D2` | `bugfix` | Bias Reference and Power Management | model_behavior/reference_power_behavior | model_behavior/reference_power_behavior | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_ldo_regulator_macro_model:dut` | `D2` | `dut` | Bias Reference and Power Management | model_dut_compile/other_compile_failure | model_spectre_ahdl_compile/spectre_ahdl_syntax_scope_or_operator_reject | ERROR (VACOMP-2259): "parameter real nominal_voltage = 0.6 from (0.0,<<--? | ERROR (VACOMP-2212): "ldo_regulator_macro_model.va", line 53: Encountered |
| `vbr1_l1_ldo_regulator_macro_model:e2e` | `D2` | `e2e` | Bias Reference and Power Management | model_behavior/reference_power_behavior | model_behavior/reference_power_behavior | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_power_on_reset_detector:dut` | `D2` | `dut` | Bias Reference and Power Management | model_dut_compile/unsupported_event_variable_or_wait | model_behavior/reference_power_behavior | ERROR (VACOMP-2259): "initial<<--? step begin" | spectre:por_initial_not_asserted=0.000 |
| `vbr1_l1_power_on_reset_detector:e2e` | `D2` | `e2e` | Bias Reference and Power Management | model_spectre_ahdl_compile/spectre_ahdl_syntax_scope_or_operator_reject | model_behavior/reference_power_behavior | ERROR (VACOMP-1552): "@(cross(rst - threshold)<<--? ) begin" | spectre:por_not_released=1.000 |
| `vbr1_l1_ptat_ctat_reference_generator:dut` | `D2` | `dut` | Bias Reference and Power Management | model_dut_compile/unsupported_event_variable_or_wait | model_dut_compile/veriloga_embedded_declaration | ERROR (VACOMP-1743): "ptat_ctat_reference_generator.va", line 12: | ERROR (VACOMP-2143): "ptat_ctat_reference_generator.va", line 26: |
| `vbr1_l1_ptat_ctat_reference_generator:e2e` | `D2` | `e2e` | Bias Reference and Power Management | model_behavior/reference_power_behavior | model_behavior/reference_power_behavior | spectre:ptat_metric_not_monotonic cold=0.000 hot=0.000 | FAIL_SIM_CORRECTNESS |
| `vbr1_l2_ldo_load_step_recovery_flow:e2e` | `D3` | `e2e` | Bias Reference and Power Management | model_spectre_ahdl_compile/spectre_ahdl_syntax_scope_or_operator_reject | model_behavior/reference_power_behavior | ERROR (VACOMP-1552): "@(cross(rst - 0.5,<<--? 1)) begin" | FAIL_SIM_CORRECTNESS |
| `vbr1_l2_reference_startup_enable_flow:e2e` | `D3` | `e2e` | Bias Reference and Power Management | model_dut_compile/veriloga_embedded_declaration | model_behavior/reference_power_behavior | ERROR (VACOMP-1917): "reference_startup_enable_flow.va", line 91: | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_calibration_deadband_controller:dut` | `D2` | `dut` | Calibration, DEM, and Control | model_dut_compile/veriloga_embedded_declaration | model_dut_compile/veriloga_embedded_declaration | ERROR (VACOMP-1917): "calibration_deadband_controller.va", line 31: | ERROR (VACOMP-1917): "calibration_deadband_controller.va", line 40: |
| `vbr1_l1_calibration_deadband_controller:e2e` | `D2` | `e2e` | Calibration, DEM, and Control | model_dut_compile/veriloga_embedded_declaration | model_behavior/calibration_control_behavior | ERROR (VACOMP-1917): "calibration_deadband_controller.va", line 36: | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_dwa_dem_encoder:dut` | `D2` | `dut` | Calibration, DEM, and Control | model_tb_compile/unsupported_event_variable_or_wait | model_tb_compile/guarded_transition_contribution | ERROR (VACOMP-2157): "v2b_4b.va", line 46: Encountered a contribution | ERROR (VACOMP-2143): "v2b_4b.va", line 40: Encountered the `transition' |
| `vbr1_l1_dwa_dem_encoder:e2e` | `D2` | `e2e` | Calibration, DEM, and Control | model_tb_compile/guarded_transition_contribution | generation/incomplete_generation | ERROR (VACOMP-1192): "V(cell_en_o[i])<<--? <+ transition(0, 0, 1n, 1n);" | no_code_extracted |
| `vbr1_l1_dwa_dem_encoder:tb` | `D2` | `tb` | Calibration, DEM, and Control | model_behavior/calibration_control_behavior | model_behavior/calibration_control_behavior | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_element_shuffler:bugfix` | `D2` | `bugfix` | Calibration, DEM, and Control | model_behavior/calibration_control_behavior | model_behavior/calibration_control_behavior | spectre:active_sequence=0,3,1,2,0,3 expected=2,0,3,1,2,0 failures=20ns_active=[0]_expected=2 40ns... | spectre:active_sequence=2,0,2,0,2,0 expected=2,0,3,1,2,0 failures=60ns_active=[2]_expected=3 80ns... |
| `vbr1_l1_element_shuffler:dut` | `D2` | `dut` | Calibration, DEM, and Control | model_dut_compile/unsupported_event_variable_or_wait | model_behavior/calibration_control_behavior | ERROR (VACOMP-2259): "out out0<<--? , out1, out2, out3;" | spectre:active_sequence=1,2,3,0,1,2 expected=2,0,3,1,2,0 failures=20ns_active=[1]_expected=2 40ns... |
| `vbr1_l1_element_shuffler:e2e` | `D2` | `e2e` | Calibration, DEM, and Control | model_spectre_ahdl_compile/spectre_ahdl_syntax_scope_or_operator_reject | model_behavior/calibration_control_behavior | ERROR (VACOMP-2259): "initial<<--? state = 0;" | spectre:active_sequence=-,2,0,3,1,2 expected=2,0,3,1,2,0 failures=20ns_active=[]_expected=2 40ns_... |
| `vbr1_l1_element_shuffler:tb` | `D2` | `tb` | Calibration, DEM, and Control | model_behavior/calibration_control_behavior | model_behavior/calibration_control_behavior | spectre:active_sequence=1,1,1,1,1,1 expected=2,0,3,1,2,0 failures=20ns_active=[1]_expected=2 40ns... | spectre:active_sequence=1,2,0,3,1,2 expected=2,0,3,1,2,0 failures=20ns_active=[1]_expected=2 40ns... |
| `vbr1_l1_gain_trim_controller:e2e` | `D2` | `e2e` | Calibration, DEM, and Control | model_behavior/calibration_control_behavior | model_behavior/calibration_control_behavior | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_gain_trim_controller:tb` | `D2` | `tb` | Calibration, DEM, and Control | model_behavior/calibration_control_behavior | model_behavior/calibration_control_behavior | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_successive_approximation_calibration_search_fsm:dut` | `D2` | `dut` | Calibration, DEM, and Control | model_dut_compile/unsupported_event_variable_or_wait | model_behavior/calibration_control_behavior | ERROR (VACOMP-2177): "parameter real initial_step<<--? = 0.45;" | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_successive_approximation_calibration_search_fsm:e2e` | `D2` | `e2e` | Calibration, DEM, and Control | model_spectre_ahdl_compile/spectre_ahdl_syntax_scope_or_operator_reject | model_behavior/calibration_control_behavior | ERROR (VACOMP-2177): "parameter real initial_step<<--? = full_scale / | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_successive_approximation_calibration_search_fsm:tb` | `D2` | `tb` | Calibration, DEM, and Control | model_behavior/calibration_control_behavior | model_behavior/calibration_control_behavior | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_trim_calibration_controller:e2e` | `D2` | `e2e` | Calibration, DEM, and Control | model_behavior/calibration_control_behavior | model_behavior/calibration_control_behavior | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |

## Recommended Next Actions

- Report full_strict, valid_candidate, and behavior_ready rates separately in model-baseline discussion.
- Treat D1/D2/D3 as design-intent labels until manual calibration resolves flagged anomalies.
- Audit zero-common-pass and common-hard categories before claiming calibrated benchmark difficulty.
- Keep incomplete generation and runner/output inconclusive rows outside circuit-behavior error analysis, while still reporting them under fixed-budget model baselines.
