# EVAS/Spectre Mismatch Triage

Generated: 2026-05-30T06:58:18.030902+00:00

This report separates model failures, runner inconclusive rows, and
EVAS/Spectre semantic mismatches. L0 conformance rows are diagnostics
and are not part of the scored vaBench denominator.

## Summary

| Metric | Value |
| --- | ---: |
| total rows | 52 |
| strict dual pass rows | 41 |
| Spectre checker pass rows | 41 |
| EVAS PASS / Spectre FAIL rows | 1 |
| Spectre PASS / EVAS FAIL rows | 0 |
| parity gate rows | 0 |
| incomplete generation rows | 0 |
| runner inconclusive rows | 0 |

## Score Slices

| Slice | Rows | Strict dual pass | Pass rate | Meaning |
| --- | ---: | ---: | ---: | --- |
| `full_strict` | 52 | 41 | 78.85% | All scored rows. Incomplete generation and runner/output inconclusive rows are counted as failures. |
| `valid_candidate` | 52 | 41 | 78.85% | Rows with complete model artifacts and a reliable evaluator judgment. Syntax and behavior failure... |
| `behavior_ready` | 50 | 41 | 82.00% | Rows that reached the functional checker: strict dual pass plus model_behavior failure rows. |

## Difficulty Breakdown

| Difficulty | Rows | Strict dual pass | Strict rate | Valid candidates | Behavior-ready rows | Behavior-ready pass rate | Non-model/inconclusive |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `D1` | 9 | 7 | 77.78% | 9 | 9 | 77.78% | 0 |
| `D2` | 40 | 31 | 77.50% | 40 | 38 | 81.58% | 0 |
| `D3` | 3 | 3 | 100.00% | 3 | 3 | 100.00% | 0 |

## Form Breakdown

| Form | Rows | Strict dual pass | Strict rate | Valid candidates | Behavior-ready rows | Behavior-ready pass rate | Non-model/inconclusive |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bugfix` | 52 | 41 | 78.85% | 52 | 50 | 82.00% | 0 |

## Category Breakdown

| Category | Rows | Strict dual pass | Strict rate | Valid candidates | Behavior-ready rows | Behavior-ready pass rate | Non-model/inconclusive |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseband Signal Conditioning | 7 | 5 | 71.43% | 7 | 6 | 83.33% | 0 |
| Bias Reference and Power Management | 6 | 4 | 66.67% | 6 | 6 | 66.67% | 0 |
| Calibration, DEM, and Control | 6 | 4 | 66.67% | 6 | 6 | 66.67% | 0 |
| Comparator and Decision Circuits | 7 | 6 | 85.71% | 7 | 6 | 100.00% | 0 |
| Data Converter Models | 9 | 7 | 77.78% | 9 | 9 | 77.78% | 0 |
| PLL Clock and Timing Systems | 8 | 8 | 100.00% | 8 | 8 | 100.00% | 0 |
| RF and AFE Behavioral Macromodels | 5 | 3 | 60.00% | 5 | 5 | 60.00% | 0 |
| Sampling and Analog Memory | 4 | 4 | 100.00% | 4 | 4 | 100.00% | 0 |

## Axis Counts

| Axis | Count | Meaning |
| --- | ---: | --- |
| `evas_spectre_mismatch` | 1 | EVAS and Spectre disagree on the same candidate; reduce to L0 conformance. |
| `model_behavior` | 9 | The candidate compiled and ran but failed the functional checker. |
| `model_dut_compile` | 1 | EVAS/static front-end rejected the generated Verilog-A DUT. |
| `pass` | 41 | Strict EVAS+Spectre pass. |

## Failure Families

| Family | Axis | Count | Example | Evidence |
| --- | --- | ---: | --- | --- |
| `strict_dual_pass` | `pass` | 41 | `vbm1_cdac_calibration_bugfix` | {"common_window_s": [0.0, 2.2e-07], "max_abs_v": 6.000013338058885e-06, "max_nrmse": 3.2258637039... |
| `calibration_control_behavior` | `model_behavior` | 2 | `vbm1_element_shuffler_bugfix` | spectre:active_sequence=3,1,2,0,3,1 expected=2,0,3,1,2,0 failures=20ns_active=[3]_expected=2 40ns... |
| `reference_power_behavior` | `model_behavior` | 2 | `vbr1_l1_bandgap_reference_macro_model_bugfix` | spectre:bandgap_brownout_not_reset=0.550 |
| `converter_code_or_transfer_behavior` | `model_behavior` | 2 | `vbr1_l1_capacitive_weighted_sar_feedback_dac_bugfix` | spectre:samples=16 mismatches=15/1 cal_mismatches=0 covered_states=16 diff_span=1.2035 max_diff_e... |
| `rf_afe_macro_behavior` | `model_behavior` | 2 | `vbr1_l1_limiting_amplifier_frontend_bugfix` | FAIL_SIM_CORRECTNESS |
| `restricted_analog_operator_placement` | `model_dut_compile` | 1 | `vbm1_strongarm_comparator_behavior_bugfix` | ERROR (VACOMP-2146): "dut_fixed.va", line 27: Encountered the `cross' |
| `event_or_sampling_semantics` | `evas_spectre_mismatch` | 1 | `vbr1_l1_precision_rectifier_envelope_detector_bugfix` | spectre:rectifier_envelope_hold_missing env=0.586 rect=0.500 metric=0.900 |
| `baseband_dynamic_behavior` | `model_behavior` | 1 | `vbr1_l1_soft_hysteretic_limiter_bugfix` | spectre:soft_limiter_metric_not_stateful high=0.429/1.000 low=0.919/0.000 |

## Mismatch / Conformance Seeds

| Task | Direction/axis | Family | Suggested L0 action | Evidence |
| --- | --- | --- | --- | --- |
| `vbr1_l1_precision_rectifier_envelope_detector_bugfix` | EVAS PASS / Spectre FAIL | `event_or_sampling_semantics` | minimize vbr1_l1_precision_rectifier_envelope_detector into L0 event-sampling conformance | spectre:rectifier_envelope_hold_missing env=0.586 rect=0.500 metric=0.900 |

## Inputs

- `results/vabench-release-v1-baseline-dual-mimo-v2.5-pro-20260530-mimo-bugfix52-no-rootcause-v1-dual-r2-sui`
