# EVAS/Spectre Mismatch Triage

Generated: 2026-05-31T08:38:18.031905+00:00

This report separates model failures, runner inconclusive rows, and
EVAS/Spectre semantic mismatches. L0 conformance rows are diagnostics
and are not part of the scored vaBench denominator.

## Summary

| Metric | Value |
| --- | ---: |
| total rows | 11 |
| strict dual pass rows | 2 |
| Spectre checker pass rows | 4 |
| EVAS PASS / Spectre FAIL rows | 0 |
| Spectre PASS / EVAS FAIL rows | 0 |
| parity gate rows | 2 |
| incomplete generation rows | 0 |
| runner inconclusive rows | 0 |

## Score Slices

| Slice | Rows | Strict dual pass | Pass rate | Meaning |
| --- | ---: | ---: | ---: | --- |
| `full_strict` | 11 | 2 | 18.18% | All scored rows. Incomplete generation and runner/output inconclusive rows are counted as failures. |
| `valid_candidate` | 11 | 2 | 18.18% | Rows with complete model artifacts and a reliable evaluator judgment. Syntax and behavior failure... |
| `behavior_ready` | 4 | 2 | 50.00% | Rows that reached the functional checker: strict dual pass plus model_behavior failure rows. |

## Difficulty Breakdown

| Difficulty | Rows | Strict dual pass | Strict rate | Valid candidates | Behavior-ready rows | Behavior-ready pass rate | Non-model/inconclusive |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `D1` | 2 | 0 | 0.00% | 2 | 0 | 0.00% | 0 |
| `D2` | 8 | 2 | 25.00% | 8 | 3 | 66.67% | 0 |
| `D3` | 1 | 0 | 0.00% | 1 | 1 | 0.00% | 0 |

## Form Breakdown

| Form | Rows | Strict dual pass | Strict rate | Valid candidates | Behavior-ready rows | Behavior-ready pass rate | Non-model/inconclusive |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bugfix` | 2 | 0 | 0.00% | 2 | 1 | 0.00% | 0 |
| `dut` | 4 | 1 | 25.00% | 4 | 1 | 100.00% | 0 |
| `e2e` | 1 | 0 | 0.00% | 1 | 0 | 0.00% | 0 |
| `tb` | 4 | 1 | 25.00% | 4 | 2 | 50.00% | 0 |

## Category Breakdown

| Category | Rows | Strict dual pass | Strict rate | Valid candidates | Behavior-ready rows | Behavior-ready pass rate | Non-model/inconclusive |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseband Signal Conditioning | 1 | 0 | 0.00% | 1 | 1 | 0.00% | 0 |
| Bias Reference and Power Management | 3 | 1 | 33.33% | 3 | 1 | 100.00% | 0 |
| Calibration, DEM, and Control | 1 | 0 | 0.00% | 1 | 0 | 0.00% | 0 |
| Comparator and Decision Circuits | 1 | 0 | 0.00% | 1 | 0 | 0.00% | 0 |
| PLL Clock and Timing Systems | 2 | 0 | 0.00% | 2 | 0 | 0.00% | 0 |
| RF and AFE Behavioral Macromodels | 2 | 1 | 50.00% | 2 | 2 | 50.00% | 0 |
| Sampling and Analog Memory | 1 | 0 | 0.00% | 1 | 0 | 0.00% | 0 |

## Axis Counts

| Axis | Count | Meaning |
| --- | ---: | --- |
| `model_behavior` | 2 | The candidate compiled and ran but failed the functional checker. |
| `model_dut_compile` | 5 | EVAS/static front-end rejected the generated Verilog-A DUT. |
| `parity` | 2 | Both sides may pass behavior, but waveform parity needs a conformance/checker-window audit. |
| `pass` | 2 | Strict EVAS+Spectre pass. |

## Failure Families

| Family | Axis | Count | Example | Evidence |
| --- | --- | ---: | --- | --- |
| `other_compile_failure` | `model_dut_compile` | 4 | `vbm1_offset_comparator_e2e` | ERROR (VACOMP-2259): "initial_step<<--? begin" |
| `waveform_parity_gate` | `parity` | 2 | `vbm1_vco_phase_integrator_tb` | {"common_window_s": [0.0, 1.8e-07], "max_abs_v": 1.0, "max_nrmse": 0.3312767732565065, "max_relat... |
| `strict_dual_pass` | `pass` | 2 | `vbr1_l1_bandgap_reference_macro_model_dut` | {"common_window_s": [0.0, 8e-08], "max_abs_v": 1.0, "max_nrmse": 0.09916666666666667, "max_relati... |
| `unsupported_event_variable_or_wait` | `model_dut_compile` | 1 | `vbr1_l1_successive_approximation_calibration_search_fsm_dut` | ERROR (VACOMP-2177): "parameter real initial_step<<--? = 0.45;" |
| `rf_afe_macro_behavior` | `model_behavior` | 1 | `vbr1_l1_log_rssi_power_detector_tb` | spectre:rssi_not_monotonic_loglike small/mid/high=0.120/0.714/0.720 |
| `baseband_dynamic_behavior` | `model_behavior` | 1 | `vbr1_l1_precision_rectifier_envelope_detector_bugfix` | spectre:rectifier_envelope_hold_missing env=0.586 rect=0.500 metric=0.900 |

## Mismatch / Conformance Seeds

| Task | Direction/axis | Family | Suggested L0 action | Evidence |
| --- | --- | --- | --- | --- |
| `vbm1_vco_phase_integrator_tb` | parity | `waveform_parity_gate` | minimize vbr1_l1_vco_phase_integrator into L0 waveform/checker-window conformance | {"common_window_s": [0.0, 1.8e-07], "max_abs_v": 1.0, "max_nrmse": 0.3312767732565065, "max_relat... |
| `vbr1_l1_ptat_ctat_reference_generator_tb` | parity | `waveform_parity_gate` | minimize vbr1_l1_ptat_ctat_reference_generator into L0 waveform/checker-window conformance | {"common_window_s": [0.0, 8e-08], "max_abs_v": 1.0, "max_nrmse": 0.3308238846211788, "max_relativ... |

## Inputs

- `results/vabench-release-v1-baseline-dual-mimo-v2.5-20260531-mimo25-mismatch7-suiwei-nested-v3-dual`
- `results/vabench-release-v1-baseline-dual-mimo-v2.5-pro-20260531-mimo25pro-mismatch3-suiwei-nested-v1-dual`
- `results/vabench-release-v1-baseline-dual-mimo-v2.5-pro-20260531-mimo25pro-bugfix-mismatch1-transition-fix-v1-dual`
