# DeepSeek Full236 Latest Overlay After Wrapper-v5 Include Rerun

Generated: `2026-05-28T08:39:32.983850+00:00`

Full 236-row overlay: base full attribution with the 55 old wrapper-gap rows replaced by changed55 latest results, including wrapper-v5 rerun for the two include-ambiguity rows.

## Headline

| Metric | Count | Rate |
| --- | ---: | ---: |
| Spectre final pass | 59/236 | 25.0% |
| Strict EVAS/Spectre dual pass | 57/236 | 24.2% |
| Direct model failures | 172/236 | 72.9% |
| Runner/evaluator inconclusive | 5/236 | 2.1% |
| EVAS core parity debt, Spectre-pass rows | 2/236 | 0.8% |

## Score With Runner/Evaluator Rows Excluded

| Metric | Count | Denominator | Rate |
| --- | ---: | ---: | ---: |
| Spectre final pass | 59 | 231 | 25.5% |
| Strict dual pass | 57 | 231 | 24.7% |

## Evas/Runner Status Counts

| Status | Count |
| --- | ---: |
| `PASS` | 59 |
| `FAIL_SIM_CORRECTNESS` | 146 |
| `FAIL_DUT_COMPILE` | 24 |
| `FAIL_TB_COMPILE` | 3 |
| `FAIL_INFRA` | 4 |

## Primary Attribution Counts

| Attribution | Count |
| --- | ---: |
| `pass` | 57 |
| `model_behavior_failure` | 145 |
| `model_veriloga_subset_failure` | 27 |
| `evas_core_parity_debt` | 2 |
| `runner_infra_extraction` | 4 |
| `evaluator_runner_review` | 1 |

## Failure Groups

| Failure group | Count |
| --- | ---: |
| `model_functional_behavior_failure` | 145 |
| `model_veriloga_or_spectre_subset_failure` | 27 |
| `evas_core_parity_debt_spectre_pass` | 2 |
| `runner_or_api_infrastructure` | 4 |
| `evaluator_or_runner_review` | 1 |

## Root Cause Families For Non-Dual-Pass Rows

| Root cause family | Count |
| --- | ---: |
| behavior_checker_mismatch | 106 |
| veriloga_spectre_subset_violation | 18 |
| Behavior: output stuck or reset/hold state wrong | 7 |
| Verilog-A subset: local declaration inside analog/procedural block | 7 |
| Behavior: analog transfer/reference macro wrong | 12 |
| Verilog-A subset: transition() used inside conditional/event block | 1 |
| Behavior: calibration/control algorithm wrong | 5 |
| Behavior: missing/incorrect event timing or stimulus coverage | 7 |
| Behavior: wrong decision/code sequence | 6 |
| evas_spectre_semantics | 2 |
| Spectre TB syntax: malformed instance/source line | 1 |
| runner_or_api_artifact | 4 |
| simulation_output_missing | 1 |
| Behavior: sample/hold droop or hold-window behavior wrong | 2 |

## By Form

| Form | Spectre pass | Dual pass | Total | Spectre rate | Dual rate |
| --- | ---: | ---: | ---: | ---: | ---: |
| `bugfix` | 13 | 13 | 52 | 25.0% | 25.0% |
| `dut` | 19 | 17 | 52 | 36.5% | 32.7% |
| `e2e` | 10 | 10 | 66 | 15.2% | 15.2% |
| `tb` | 17 | 17 | 66 | 25.8% | 25.8% |

## By Category

| Category | Spectre pass | Dual pass | Total | Spectre rate |
| --- | ---: | ---: | ---: | ---: |
| Baseband Signal Conditioning | 6 | 6 | 30 | 20.0% |
| Bias Reference and Power Management | 4 | 4 | 28 | 14.3% |
| Calibration, DEM, and Control | 1 | 1 | 26 | 3.8% |
| Comparator and Decision Circuits | 15 | 15 | 30 | 50.0% |
| Data Converter Models | 17 | 16 | 44 | 38.6% |
| PLL Clock and Timing Systems | 9 | 8 | 36 | 25.0% |
| RF and AFE Behavioral Macromodels | 3 | 3 | 24 | 12.5% |
| Sampling and Analog Memory | 4 | 4 | 18 | 22.2% |
