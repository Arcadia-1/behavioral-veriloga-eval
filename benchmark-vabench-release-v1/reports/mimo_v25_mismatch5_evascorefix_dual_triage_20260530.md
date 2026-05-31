# EVAS/Spectre Mismatch Triage

Generated: 2026-05-30T08:16:41.687418+00:00

This report separates model failures, runner inconclusive rows, and
EVAS/Spectre semantic mismatches. L0 conformance rows are diagnostics
and are not part of the scored vaBench denominator.

## Summary

| Metric | Value |
| --- | ---: |
| total rows | 5 |
| strict dual pass rows | 0 |
| Spectre checker pass rows | 0 |
| EVAS PASS / Spectre FAIL rows | 0 |
| Spectre PASS / EVAS FAIL rows | 0 |
| parity gate rows | 0 |
| incomplete generation rows | 0 |
| runner inconclusive rows | 5 |

## Score Slices

| Slice | Rows | Strict dual pass | Pass rate | Meaning |
| --- | ---: | ---: | ---: | --- |
| `full_strict` | 5 | 0 | 0.00% | All scored rows. Incomplete generation and runner/output inconclusive rows are counted as failures. |
| `valid_candidate` | 0 | 0 | 0.00% | Rows with complete model artifacts and a reliable evaluator judgment. Syntax and behavior failure... |
| `behavior_ready` | 0 | 0 | 0.00% | Rows that reached the functional checker: strict dual pass plus model_behavior failure rows. |

## Difficulty Breakdown

| Difficulty | Rows | Strict dual pass | Strict rate | Valid candidates | Behavior-ready rows | Behavior-ready pass rate | Non-model/inconclusive |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `D1` | 2 | 0 | 0.00% | 0 | 0 | 0.00% | 2 |
| `D2` | 3 | 0 | 0.00% | 0 | 0 | 0.00% | 3 |

## Form Breakdown

| Form | Rows | Strict dual pass | Strict rate | Valid candidates | Behavior-ready rows | Behavior-ready pass rate | Non-model/inconclusive |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `bugfix` | 1 | 0 | 0.00% | 0 | 0 | 0.00% | 1 |
| `dut` | 3 | 0 | 0.00% | 0 | 0 | 0.00% | 3 |
| `e2e` | 1 | 0 | 0.00% | 0 | 0 | 0.00% | 1 |

## Category Breakdown

| Category | Rows | Strict dual pass | Strict rate | Valid candidates | Behavior-ready rows | Behavior-ready pass rate | Non-model/inconclusive |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Bias Reference and Power Management | 1 | 0 | 0.00% | 0 | 0 | 0.00% | 1 |
| Calibration, DEM, and Control | 1 | 0 | 0.00% | 0 | 0 | 0.00% | 1 |
| Comparator and Decision Circuits | 1 | 0 | 0.00% | 0 | 0 | 0.00% | 1 |
| PLL Clock and Timing Systems | 1 | 0 | 0.00% | 0 | 0 | 0.00% | 1 |
| Sampling and Analog Memory | 1 | 0 | 0.00% | 0 | 0 | 0.00% | 1 |

## Axis Counts

| Axis | Count | Meaning |
| --- | ---: | --- |
| `runner` | 5 | Evaluation infrastructure, staging, or external backend did not produce a reliable judgment. |

## Failure Families

| Family | Axis | Count | Example | Evidence |
| --- | --- | ---: | --- | --- |
| `spectre_license_or_backend_unavailable` | `runner` | 5 | `vbm1_offset_comparator_e2e` | tran.csv missing |

## Mismatch / Conformance Seeds

No EVAS/Spectre mismatch rows were found in the selected inputs.

## Inputs

- `results/vabench-release-v1-baseline-dual-mimo-v2.5-20260530-mimo25-mismatch5-evascorefix-dual`
