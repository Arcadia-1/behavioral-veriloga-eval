# vaBench Model Baseline Quality Audit

Generated: 2026-05-31T20:08:12.787416+00:00

This report audits benchmark-quality risks exposed by model baselines.
It is diagnostic: flagged rows/categories require human review before metadata changes.

## Model Score Slices

| Model | Slice | Rows | Strict dual pass | Pass rate | Meaning |
| --- | --- | ---: | ---: | ---: | --- |
| mimo-v2.5 | `full_strict` | 236 | 92 | 38.98% | All scored rows. Incomplete generation and runner/output inconclusive rows are counted as failures. |
| mimo-v2.5 | `valid_candidate` | 234 | 92 | 39.32% | Rows with complete model artifacts and a reliable evaluator judgment. Syntax and behavior failure... |
| mimo-v2.5 | `behavior_ready` | 150 | 92 | 61.33% | Rows that reached the functional checker: strict dual pass plus model_behavior failure rows. |
| mimo-v2.5-pro | `full_strict` | 236 | 112 | 47.46% | All scored rows. Incomplete generation and runner/output inconclusive rows are counted as failures. |
| mimo-v2.5-pro | `valid_candidate` | 224 | 112 | 50.00% | Rows with complete model artifacts and a reliable evaluator judgment. Syntax and behavior failure... |
| mimo-v2.5-pro | `behavior_ready` | 190 | 112 | 58.95% | Rows that reached the functional checker: strict dual pass plus model_behavior failure rows. |

## Pass Overlap

| Metric | Value |
| --- | ---: |
| row count | 236 |
| both pass | 76 |
| mimo-v2.5 only pass | 16 |
| mimo-v2.5-pro only pass | 36 |
| both fail | 108 |
| missing in one report | 0 |

## Difficulty Calibration Warnings

| Model | D1 rate | D1 rows | D2 rate | D2 rows | D3 rate | D3 rows | Flags | Interpretation |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| mimo-v2.5 | 69.44% | 36 | 33.12% | 160 | 35.00% | 40 | D3_not_harder_than_D2 | Treat difficulty labels as requiring manual calibration; do not claim calibrated difficulty tiers... |
| mimo-v2.5-pro | 88.89% | 36 | 40.62% | 160 | 37.50% | 40 | none | No monotonicity warning from this model alone. |

## Category Risk Audit

| Category | Rows | Both pass | mimo-v2.5 only | mimo-v2.5-pro only | Both fail | mimo-v2.5 rate | mimo-v2.5-pro rate | Common behavior fail | Artifact/protocol fail | Risk | Action |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| Baseband Signal Conditioning | 30 | 13 | 1 | 4 | 12 | 46.67% | 56.67% | 1 | 11 | `protocol_noise_sensitive` | Separate language/protocol failures from behavior claims and inspect public contracts for missing... |
| Bias Reference and Power Management | 28 | 11 | 4 | 3 | 10 | 53.57% | 50.00% | 3 | 7 | `protocol_noise_sensitive` | Separate language/protocol failures from behavior claims and inspect public contracts for missing... |
| Calibration, DEM, and Control | 26 | 7 | 1 | 0 | 18 | 30.77% | 26.92% | 6 | 12 | `protocol_noise_sensitive` | Separate language/protocol failures from behavior claims and inspect public contracts for missing... |
| Comparator and Decision Circuits | 30 | 13 | 1 | 7 | 9 | 46.67% | 66.67% | 3 | 6 | `protocol_noise_sensitive` | Separate language/protocol failures from behavior claims and inspect public contracts for missing... |
| Data Converter Models | 44 | 12 | 5 | 8 | 19 | 38.64% | 45.45% | 9 | 10 | `protocol_noise_sensitive` | Separate language/protocol failures from behavior claims and inspect public contracts for missing... |
| PLL Clock and Timing Systems | 36 | 10 | 1 | 5 | 20 | 30.56% | 41.67% | 6 | 14 | `protocol_noise_sensitive` | Separate language/protocol failures from behavior claims and inspect public contracts for missing... |
| RF and AFE Behavioral Macromodels | 24 | 7 | 2 | 5 | 10 | 37.50% | 50.00% | 2 | 8 | `protocol_noise_sensitive` | Separate language/protocol failures from behavior claims and inspect public contracts for missing... |
| Sampling and Analog Memory | 18 | 3 | 1 | 4 | 10 | 22.22% | 38.89% | 3 | 7 | `protocol_noise_sensitive` | Separate language/protocol failures from behavior claims and inspect public contracts for missing... |

## Form Audit

| Model | Form | Rows | Strict pass | Strict rate | Behavior-ready rows | Behavior-ready pass rate | Non-model/inconclusive |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| mimo-v2.5 | `bugfix` | 52 | 43 | 82.69% | 50 | 86.00% | 0 |
| mimo-v2.5 | `dut` | 52 | 10 | 19.23% | 19 | 52.63% | 1 |
| mimo-v2.5 | `e2e` | 66 | 8 | 12.12% | 21 | 38.10% | 1 |
| mimo-v2.5 | `tb` | 66 | 31 | 46.97% | 60 | 51.67% | 0 |
| mimo-v2.5-pro | `bugfix` | 52 | 42 | 80.77% | 51 | 82.35% | 1 |
| mimo-v2.5-pro | `dut` | 52 | 19 | 36.54% | 35 | 54.29% | 1 |
| mimo-v2.5-pro | `e2e` | 66 | 16 | 24.24% | 46 | 34.78% | 6 |
| mimo-v2.5-pro | `tb` | 66 | 35 | 53.03% | 58 | 60.34% | 4 |

## Difficulty Relabel Review Candidates

| Task | Difficulty | Form | Category | Reason | mimo-v2.5 family | mimo-v2.5-pro family |
| --- | --- | --- | --- | --- | --- | --- |
| `vbr1_l1_log_rssi_power_detector:tb` | `D3` | `tb` | RF and AFE Behavioral Macromodels | D3 row passed by both baselines; check whether it is truly integration-level or over-labeled. | strict_dual_pass | strict_dual_pass |
| `vbr1_l1_pa_compression_macro:tb` | `D3` | `tb` | RF and AFE Behavioral Macromodels | D3 row passed by both baselines; check whether it is truly integration-level or over-labeled. | strict_dual_pass | strict_dual_pass |
| `vbr1_l1_pipeline_adc_stage:bugfix` | `D3` | `bugfix` | Data Converter Models | D3 row passed by both baselines; check whether it is truly integration-level or over-labeled. | strict_dual_pass | strict_dual_pass |
| `vbr1_l1_thermometer_code_decoder:dut` | `D1` | `dut` | Data Converter Models | D1 row failed by both baselines; check whether the task is under-specified, mislabeled, or genuin... | other_compile_failure | unsupported_event_variable_or_wait |
| `vbr1_l2_amplifier_filter_chain:tb` | `D3` | `tb` | Baseband Signal Conditioning | D3 row passed by both baselines; check whether it is truly integration-level or over-labeled. | strict_dual_pass | strict_dual_pass |
| `vbr1_l2_comparator_measurement_flow:tb` | `D3` | `tb` | Comparator and Decision Circuits | D3 row passed by both baselines; check whether it is truly integration-level or over-labeled. | strict_dual_pass | strict_dual_pass |
| `vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow:tb` | `D3` | `tb` | PLL Clock and Timing Systems | D3 row passed by both baselines; check whether it is truly integration-level or over-labeled. | strict_dual_pass | strict_dual_pass |
| `vbr1_l2_flash_adc_mini_array:tb` | `D3` | `tb` | Data Converter Models | D3 row passed by both baselines; check whether it is truly integration-level or over-labeled. | strict_dual_pass | strict_dual_pass |
| `vbr1_l2_iq_downconversion_chain:tb` | `D3` | `tb` | RF and AFE Behavioral Macromodels | D3 row passed by both baselines; check whether it is truly integration-level or over-labeled. | strict_dual_pass | strict_dual_pass |
| `vbr1_l2_reference_startup_enable_flow:tb` | `D3` | `tb` | Bias Reference and Power Management | D3 row passed by both baselines; check whether it is truly integration-level or over-labeled. | strict_dual_pass | strict_dual_pass |

## Common Failure Examples

| Task | Difficulty | Form | Category | mimo-v2.5 axis/family | mimo-v2.5-pro axis/family | mimo-v2.5 evidence | mimo-v2.5-pro evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `vbr1_l1_higher_order_filter:dut` | `D2` | `dut` | Baseband Signal Conditioning | model_dut_compile/veriloga_embedded_declaration | model_behavior/baseband_dynamic_behavior | ERROR (VACOMP-1917): "higher_order_filter.va", line 48: Encountered an | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_higher_order_filter:e2e` | `D2` | `e2e` | Baseband Signal Conditioning | model_dut_compile/veriloga_embedded_declaration | model_dut_compile/guarded_transition_contribution | ERROR (VACOMP-1917): "higher_order_filter.va", line 36: Encountered an | ERROR (VACOMP-2143): "higher_order_filter.va", line 18: Encountered the |
| `vbr1_l1_precision_rectifier_envelope_detector:dut` | `D2` | `dut` | Baseband Signal Conditioning | model_behavior/baseband_dynamic_behavior | model_dut_compile/veriloga_embedded_declaration | spectre:rectifier_negative_half_not_rectified=0.183 | ERROR (VACOMP-1917): "precision_rectifier_envelope_detector.va", line 26: |
| `vbr1_l1_precision_rectifier_envelope_detector:e2e` | `D2` | `e2e` | Baseband Signal Conditioning | model_spectre_ahdl_compile/spectre_ahdl_syntax_scope_or_operator_reject | model_behavior/baseband_dynamic_behavior | ERROR (VACOMP-2212): "env_target = env_r * exp(-(abstime /<<--? | spectre:rectifier_positive_half_not_rectified=0.447 |
| `vbr1_l1_programmable_gain_amplifier:dut` | `D2` | `dut` | Baseband Signal Conditioning | model_behavior/baseband_dynamic_behavior | model_dut_compile/restricted_analog_operator_placement | FAIL_SIM_CORRECTNESS | ERROR (VACOMP-2146): "programmable_gain_amplifier.va", line 39: Encountered |
| `vbr1_l1_resettable_integrator:dut` | `D2` | `dut` | Baseband Signal Conditioning | model_spectre_elab_or_topology/spectre_elaboration_parameter_or_topology_reject | model_behavior/baseband_dynamic_behavior | below lower bound in from range limit (0). | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_resettable_integrator:e2e` | `D2` | `e2e` | Baseband Signal Conditioning | model_behavior/baseband_dynamic_behavior | model_dut_compile/guarded_transition_contribution | FAIL_SIM_CORRECTNESS | ERROR (VACOMP-2143): "resettable_integrator.va", line 14: Encountered the |
| `vbr1_l1_slew_rate_limiter:dut` | `D2` | `dut` | Baseband Signal Conditioning | model_dut_compile/veriloga_embedded_declaration | model_dut_compile/veriloga_embedded_declaration | ERROR (VACOMP-2143): "slew_rate_limiter.va", line 18: Encountered the | ERROR (VACOMP-1917): "slew_rate_limiter.va", line 15: Encountered an |
| `vbr1_l1_slew_rate_limiter:e2e` | `D2` | `e2e` | Baseband Signal Conditioning | model_dut_compile/veriloga_embedded_declaration | model_behavior/baseband_dynamic_behavior | ERROR (VACOMP-2143): "slew_rate_limiter.va", line 11: Encountered the | spectre:slew_samples=0.450,0.150,0.000,0.000,0.000 input_sequence=False rising_limited=False high... |
| `vbr1_l1_soft_hysteretic_limiter:bugfix` | `D2` | `bugfix` | Baseband Signal Conditioning | model_behavior/baseband_dynamic_behavior | model_behavior/baseband_dynamic_behavior | FAIL_SIM_CORRECTNESS | spectre:soft_limiter_metric_not_stateful high=0.526/0.450 low=0.376/0.483 |
| `vbr1_l1_soft_hysteretic_limiter:dut` | `D2` | `dut` | Baseband Signal Conditioning | model_spectre_ahdl_compile/spectre_ahdl_syntax_scope_or_operator_reject | model_dut_compile/guarded_transition_contribution | ERROR (VACOMP-1552): "@(cross(rst - 0.45,<<--? +1) or cross(rst - 0.45, | ERROR (VACOMP-2143): "soft_hysteretic_limiter.va", line 68: Encountered the |
| `vbr1_l1_soft_hysteretic_limiter:e2e` | `D2` | `e2e` | Baseband Signal Conditioning | model_behavior/baseband_dynamic_behavior | model_spectre_ahdl_compile/spectre_ahdl_syntax_scope_or_operator_reject | FAIL_SIM_CORRECTNESS | ERROR (SFE-23): |
| `vbr1_l1_bandgap_reference_macro_model:e2e` | `D2` | `e2e` | Bias Reference and Power Management | model_spectre_ahdl_compile/spectre_ahdl_syntax_scope_or_operator_reject | model_behavior/reference_power_behavior | ERROR (VACOMP-1552): "@(cross(vin - vreset_low,<<--? +1)) begin" | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_bandgap_reference_macro_model:tb` | `D2` | `tb` | Bias Reference and Power Management | model_behavior/reference_power_behavior | model_behavior/reference_power_behavior | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_ldo_regulator_macro_model:dut` | `D2` | `dut` | Bias Reference and Power Management | model_dut_compile/veriloga_embedded_declaration | model_spectre_ahdl_compile/spectre_ahdl_syntax_scope_or_operator_reject | ERROR (VACOMP-1917): "ldo_regulator_macro_model.va", line 40: Encountered | ERROR (VACOMP-2212): "ldo_regulator_macro_model.va", line 53: Encountered |
| `vbr1_l1_ldo_regulator_macro_model:e2e` | `D2` | `e2e` | Bias Reference and Power Management | model_behavior/reference_power_behavior | model_behavior/reference_power_behavior | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_power_on_reset_detector:dut` | `D2` | `dut` | Bias Reference and Power Management | model_dut_compile/other_compile_failure | model_behavior/reference_power_behavior | ERROR (VACOMP-2259): "initial<<--? begin" | spectre:por_initial_not_asserted=0.000 |
| `vbr1_l1_power_on_reset_detector:e2e` | `D2` | `e2e` | Bias Reference and Power Management | model_spectre_ahdl_compile/spectre_ahdl_syntax_scope_or_operator_reject | model_behavior/reference_power_behavior | ERROR (VACOMP-2259): "parameter real vth = 0.62 from [0.0:0.1:<<--? 1.0];" | spectre:por_not_released=1.000 |
| `vbr1_l1_ptat_ctat_reference_generator:dut` | `D2` | `dut` | Bias Reference and Power Management | model_dut_compile/guarded_transition_contribution | model_dut_compile/veriloga_embedded_declaration | ERROR (VACOMP-2157): "ptat_ctat_reference_generator.va", line 31: | ERROR (VACOMP-2143): "ptat_ctat_reference_generator.va", line 26: |
| `vbr1_l1_ptat_ctat_reference_generator:e2e` | `D2` | `e2e` | Bias Reference and Power Management | model_spectre_ahdl_compile/spectre_ahdl_syntax_scope_or_operator_reject | model_behavior/reference_power_behavior | ERROR (VACOMP-1552): "@(cross(rst - 0.45,<<--? 1)) begin" | FAIL_SIM_CORRECTNESS |
| `vbr1_l2_ldo_load_step_recovery_flow:e2e` | `D3` | `e2e` | Bias Reference and Power Management | model_dut_compile/guarded_transition_contribution | model_behavior/reference_power_behavior | ERROR (VACOMP-1552): "@(cross(rst - 0.5,<<--? +1)) begin" | FAIL_SIM_CORRECTNESS |
| `vbr1_l2_reference_startup_enable_flow:e2e` | `D3` | `e2e` | Bias Reference and Power Management | model_behavior/reference_power_behavior | model_behavior/reference_power_behavior | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_calibration_deadband_controller:dut` | `D2` | `dut` | Calibration, DEM, and Control | model_behavior/calibration_control_behavior | model_dut_compile/veriloga_embedded_declaration | spectre:trim_direction_mismatches=2/24 | ERROR (VACOMP-1917): "calibration_deadband_controller.va", line 40: |
| `vbr1_l1_calibration_deadband_controller:e2e` | `D2` | `e2e` | Calibration, DEM, and Control | model_dut_compile/other_compile_failure | model_behavior/calibration_control_behavior | ERROR (VACOMP-2259): "parameter real deadband = 0.01 from (0,<<--? inf);" | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_dwa_dem_encoder:dut` | `D2` | `dut` | Calibration, DEM, and Control | model_tb_compile/unsupported_event_variable_or_wait | model_tb_compile/guarded_transition_contribution | ERROR (VACOMP-2157): "v2b_4b.va", line 36: Encountered a contribution | ERROR (VACOMP-2143): "v2b_4b.va", line 40: Encountered the `transition' |
| `vbr1_l1_dwa_dem_encoder:e2e` | `D2` | `e2e` | Calibration, DEM, and Control | model_dut_compile/other_compile_failure | generation/incomplete_generation | ERROR (VACOMP-1194): "dwa_ptr_gen.va", line 59: Access function has more | no_code_extracted |
| `vbr1_l1_dwa_dem_encoder:tb` | `D2` | `tb` | Calibration, DEM, and Control | model_behavior/calibration_control_behavior | model_behavior/calibration_control_behavior | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_element_shuffler:bugfix` | `D2` | `bugfix` | Calibration, DEM, and Control | model_behavior/calibration_control_behavior | model_behavior/calibration_control_behavior | spectre:active_sequence=2,0,2,0,2,0 expected=2,0,3,1,2,0 failures=60ns_active=[2]_expected=3 80ns... | spectre:active_sequence=2,0,2,0,2,0 expected=2,0,3,1,2,0 failures=60ns_active=[2]_expected=3 80ns... |
| `vbr1_l1_element_shuffler:dut` | `D2` | `dut` | Calibration, DEM, and Control | model_dut_compile/unsupported_event_variable_or_wait | model_behavior/calibration_control_behavior | ERROR (VACOMP-1552): "@(rst_n == 0)<<--? begin" | spectre:active_sequence=1,2,3,0,1,2 expected=2,0,3,1,2,0 failures=20ns_active=[1]_expected=2 40ns... |
| `vbr1_l1_element_shuffler:e2e` | `D2` | `e2e` | Calibration, DEM, and Control | model_dut_compile/guarded_transition_contribution | model_behavior/calibration_control_behavior | ERROR (VACOMP-2157): "element_shuffler.va", line 23: Encountered a | spectre:active_sequence=-,2,0,3,1,2 expected=2,0,3,1,2,0 failures=20ns_active=[]_expected=2 40ns_... |
| `vbr1_l1_element_shuffler:tb` | `D2` | `tb` | Calibration, DEM, and Control | model_behavior/calibration_control_behavior | model_behavior/calibration_control_behavior | spectre:active_sequence=1,2,0,3,1,2 expected=2,0,3,1,2,0 failures=20ns_active=[1]_expected=2 40ns... | spectre:active_sequence=1,2,0,3,1,2 expected=2,0,3,1,2,0 failures=20ns_active=[1]_expected=2 40ns... |
| `vbr1_l1_gain_trim_controller:e2e` | `D2` | `e2e` | Calibration, DEM, and Control | model_dut_compile/guarded_transition_contribution | model_behavior/calibration_control_behavior | ERROR (VACOMP-2143): "gain_trim_controller.va", line 33: Encountered the | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_gain_trim_controller:tb` | `D2` | `tb` | Calibration, DEM, and Control | model_dut_compile/spectre_testbench_syntax | model_behavior/calibration_control_behavior | tran.csv missing | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_successive_approximation_calibration_search_fsm:dut` | `D2` | `dut` | Calibration, DEM, and Control | model_behavior/calibration_control_behavior | model_behavior/calibration_control_behavior | spectre:sar_cal_direction_mismatches=3/6 | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_successive_approximation_calibration_search_fsm:e2e` | `D2` | `e2e` | Calibration, DEM, and Control | model_dut_compile/unsupported_event_variable_or_wait | model_behavior/calibration_control_behavior | ERROR (VACOMP-2177): "parameter real initial_step<<--? = 0.225;" | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_successive_approximation_calibration_search_fsm:tb` | `D2` | `tb` | Calibration, DEM, and Control | model_behavior/calibration_control_behavior | model_behavior/calibration_control_behavior | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_trim_calibration_controller:e2e` | `D2` | `e2e` | Calibration, DEM, and Control | model_dut_compile/guarded_transition_contribution | model_behavior/calibration_control_behavior | ERROR (VACOMP-2146): "cdac_calibration.va", line 13: Encountered the | FAIL_SIM_CORRECTNESS |
| `vbr1_l1_trim_calibration_controller:tb` | `D2` | `tb` | Calibration, DEM, and Control | model_behavior/calibration_control_behavior | model_behavior/calibration_control_behavior | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |
| `vbr1_l2_complete_calibration_loop:e2e` | `D3` | `e2e` | Calibration, DEM, and Control | generation/incomplete_generation | model_behavior/calibration_control_behavior | no_code_extracted | FAIL_SIM_CORRECTNESS |
| `vbr1_l2_complete_calibration_loop:tb` | `D3` | `tb` | Calibration, DEM, and Control | model_behavior/calibration_control_behavior | runner/spectre_run_inconclusive | FAIL_SIM_CORRECTNESS | ERROR (CMI-2116): XDUT: Too few terminals given (5 < 7). |

## Recommended Next Actions

- Report full_strict, valid_candidate, and behavior_ready rates separately in model-baseline discussion.
- Treat D1/D2/D3 as design-intent labels until manual calibration resolves flagged anomalies.
- Audit zero-common-pass and common-hard categories before claiming calibrated benchmark difficulty.
- Keep incomplete generation and runner/output inconclusive rows outside circuit-behavior error analysis, while still reporting them under fixed-budget model baselines.
