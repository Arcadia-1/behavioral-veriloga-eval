# EVAS/Spectre Mismatch Triage

Generated: 2026-05-31T17:39:40.841105+00:00

This report separates model failures, runner inconclusive rows, and
EVAS/Spectre semantic mismatches. L0 conformance rows are diagnostics
and are not part of the scored vaBench denominator.

## Summary

| Metric | Value |
| --- | ---: |
| total rows | 236 |
| strict dual pass rows | 113 |
| Spectre checker pass rows | 113 |
| EVAS PASS / Spectre FAIL rows | 0 |
| Spectre PASS / EVAS FAIL rows | 0 |
| parity gate rows | 0 |
| incomplete generation rows | 8 |
| runner inconclusive rows | 3 |

## Score Slices

| Slice | Rows | Strict dual pass | Pass rate | Meaning |
| --- | ---: | ---: | ---: | --- |
| `full_strict` | 236 | 113 | 47.88% | All scored rows. Incomplete generation and runner/output inconclusive rows are counted as failures. |
| `valid_candidate` | 225 | 113 | 50.22% | Rows with complete model artifacts and a reliable evaluator judgment. Syntax and behavior failure... |
| `behavior_ready` | 191 | 113 | 59.16% | Rows that reached the functional checker: strict dual pass plus model_behavior failure rows. |

## Difficulty Breakdown

| Difficulty | Rows | Strict dual pass | Strict rate | Valid candidates | Behavior-ready rows | Behavior-ready pass rate | Non-model/inconclusive |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `D1` | 36 | 33 | 91.67% | 36 | 33 | 100.00% | 0 |
| `D2` | 160 | 65 | 40.62% | 155 | 131 | 49.62% | 5 |
| `D3` | 40 | 15 | 37.50% | 34 | 27 | 55.56% | 6 |

## Form Breakdown

| Form | Rows | Strict dual pass | Strict rate | Valid candidates | Behavior-ready rows | Behavior-ready pass rate | Non-model/inconclusive |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bugfix` | 52 | 42 | 80.77% | 51 | 51 | 82.35% | 1 |
| `dut` | 52 | 20 | 38.46% | 52 | 36 | 55.56% | 0 |
| `e2e` | 66 | 16 | 24.24% | 60 | 46 | 34.78% | 6 |
| `tb` | 66 | 35 | 53.03% | 62 | 58 | 60.34% | 4 |

## Category Breakdown

| Category | Rows | Strict dual pass | Strict rate | Valid candidates | Behavior-ready rows | Behavior-ready pass rate | Non-model/inconclusive |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseband Signal Conditioning | 30 | 18 | 60.00% | 30 | 23 | 78.26% | 0 |
| Bias Reference and Power Management | 28 | 14 | 50.00% | 27 | 25 | 56.00% | 1 |
| Calibration, DEM, and Control | 26 | 7 | 26.92% | 24 | 22 | 31.82% | 2 |
| Comparator and Decision Circuits | 30 | 20 | 66.67% | 29 | 26 | 76.92% | 1 |
| Data Converter Models | 44 | 20 | 45.45% | 43 | 35 | 57.14% | 1 |
| PLL Clock and Timing Systems | 36 | 15 | 41.67% | 31 | 26 | 57.69% | 5 |
| RF and AFE Behavioral Macromodels | 24 | 12 | 50.00% | 23 | 20 | 60.00% | 1 |
| Sampling and Analog Memory | 18 | 7 | 38.89% | 18 | 14 | 50.00% | 0 |

## Axis Counts

| Axis | Count | Meaning |
| --- | ---: | --- |
| `generation` | 8 | The model did not produce a complete usable artifact. |
| `model_behavior` | 78 | The candidate compiled and ran but failed the functional checker. |
| `model_dut_compile` | 27 | EVAS/static front-end rejected the generated Verilog-A DUT. |
| `model_spectre_ahdl_compile` | 2 | Spectre final judge rejected generated Verilog-A syntax/scope/operator usage. |
| `model_spectre_elab_or_topology` | 1 | Spectre final judge rejected parameter binding, range, or topology. |
| `model_spectre_tb_source` | 2 | Spectre final judge rejected generated testbench source/waveform syntax. |
| `model_tb_compile` | 2 | EVAS/static front-end rejected the generated Spectre testbench. |
| `pass` | 113 | Strict EVAS+Spectre pass. |
| `runner` | 3 | Evaluation infrastructure, staging, or external backend did not produce a reliable judgment. |

## Failure Families

| Family | Axis | Count | Example | Evidence |
| --- | --- | ---: | --- | --- |
| `strict_dual_pass` | `pass` | 113 | `cdac_cal` | {"common_window_s": [0.0, 6.8e-08], "max_abs_v": 7.538062663736689e-06, "max_nrmse": 1.5137141323... |
| `calibration_control_behavior` | `model_behavior` | 15 | `vbm1_cdac_calibration_e2e` | FAIL_SIM_CORRECTNESS |
| `converter_code_or_transfer_behavior` | `model_behavior` | 15 | `vbm1_sar_logic_4b_dut` | FAIL_SIM_CORRECTNESS |
| `timing_or_pll_behavior` | `model_behavior` | 11 | `bbpd` | FAIL_SIM_CORRECTNESS |
| `reference_power_behavior` | `model_behavior` | 11 | `vbr1_l1_bandgap_reference_macro_model_bugfix` | spectre:bandgap_brownout_not_reset=0.550 |
| `incomplete_generation` | `generation` | 8 | `adpll_ratio_hop_smoke` | no_code_extracted |
| `guarded_transition_contribution` | `model_dut_compile` | 8 | `phase_accumulator_timer_wrap_smoke` | ERROR (VACOMP-2143): "phase_accumulator_timer_wrap_ref.va", line 34: |
| `rf_afe_macro_behavior` | `model_behavior` | 8 | `vbr1_l1_lna_gain_compression_macro_tb` | FAIL_SIM_CORRECTNESS |
| `veriloga_embedded_declaration` | `model_dut_compile` | 7 | `vbm1_slew_rate_limiter_dut` | ERROR (VACOMP-1917): "slew_rate_limiter.va", line 15: Encountered an |
| `sample_hold_memory_behavior` | `model_behavior` | 7 | `vbr1_l1_acquisition_limited_sample_and_hold_bugfix` | FAIL_SIM_CORRECTNESS |
| `decision_threshold_behavior` | `model_behavior` | 6 | `comparator_hysteresis_smoke` | FAIL_SIM_CORRECTNESS |
| `spectre_testbench_syntax` | `model_dut_compile` | 5 | `vbm1_debounce_latch_e2e` | ERROR (SFE-874): "vbm1_debounce_latch_e2e__tb_debounce_latch_ref.scs" 7: |
| `baseband_dynamic_behavior` | `model_behavior` | 5 | `vbm1_resettable_integrator_dut` | FAIL_SIM_CORRECTNESS |
| `other_compile_failure` | `model_dut_compile` | 4 | `flash_adc_3b_smoke` | tran.csv missing |
| `unsupported_event_variable_or_wait` | `model_dut_compile` | 3 | `vbm1_thermometer_decoder_guarded_dut` | ERROR (VACOMP-2259): "task compute_targets;<<--? " |
| `spectre_run_inconclusive` | `runner` | 3 | `vbr1_l2_agc_receiver_leveling_loop_tb` | ERROR (CMI-2116): XDUT: Too few terminals given (5 < 7). |
| `spectre_tb_source_or_waveform_reject` | `model_spectre_tb_source` | 2 | `sar_adc_dac_weighted_8b_smoke` | ERROR (CMI-2194): Vvin: Waveform type must be specified if any waveform |
| `spectre_ahdl_syntax_scope_or_operator_reject` | `model_spectre_ahdl_compile` | 2 | `vbr1_l1_ldo_regulator_macro_model_dut` | ERROR (VACOMP-2212): "ldo_regulator_macro_model.va", line 53: Encountered |
| `unsupported_event_loop_form` | `model_dut_compile` | 1 | `vbm1_lock_detector_dut` | ERROR (VACOMP-2212): "disable lock_detector<<--? ; // reset handled |
| `restricted_analog_operator_placement` | `model_dut_compile` | 1 | `vbr1_l1_programmable_gain_amplifier_dut` | ERROR (VACOMP-2146): "programmable_gain_amplifier.va", line 39: Encountered |
| `spectre_elaboration_parameter_or_topology_reject` | `model_spectre_elab_or_topology` | 1 | `vbr1_l2_weighted_sar_adc_dac_loop_tb` | ERROR (SFE-1997): |

## Mismatch / Conformance Seeds

No EVAS/Spectre mismatch rows were found in the selected inputs.

## Inputs

- `results/vabench-release-v1-baseline-dual-mimo-v2.5-pro-20260601-full236-highout32k-currentevas-v4-dual`
