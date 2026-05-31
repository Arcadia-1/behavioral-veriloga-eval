# DeepSeek Full236 Latest Overlay After Wrapper-v5 Include Rerun + EVAS Core Fix

Generated: `2026-05-28T15:00:08.641549+00:00`

Full 236-row overlay: base full attribution with the 55 old wrapper-gap rows replaced by changed55 latest results, including wrapper-v5 rerun for the two include-ambiguity rows. This version also overlays the two Spectre-pass/EVAS-parity-debt rows after the EVAS core semantics fix, reclassifies fixed-budget `finish_reason=length` empty generations as `model_incomplete_generation`, and replaces the clock-divider DUT runner-review row with the stagingfix-r2 result.

## Headline

| Metric | Count | Rate |
| --- | ---: | ---: |
| Spectre final pass | 59/236 | 25.0% |
| Strict EVAS/Spectre dual pass | 59/236 | 25.0% |
| Direct model failures | 177/236 | 75.0% |
| Model incomplete generations | 4/236 | 1.7% |
| Runner/evaluator inconclusive | 0/236 | 0.0% |
| EVAS core parity debt, Spectre-pass rows | 0/236 | 0.0% |

## Score With Runner/Evaluator Rows Excluded

| Metric | Count | Denominator | Rate |
| --- | ---: | ---: | ---: |
| Spectre final pass | 59 | 236 | 25.0% |
| Strict dual pass | 59 | 236 | 25.0% |

## Evaluator Status Counts

| Status | Count |
| --- | ---: |
| `PASS` | 59 |
| `FAIL_SIM_CORRECTNESS` | 146 |
| `FAIL_DUT_COMPILE` | 24 |
| `FAIL_TB_COMPILE` | 3 |
| `INCOMPLETE` | 4 |

## Primary Attribution Counts

| Attribution | Count |
| --- | ---: |
| `pass` | 59 |
| `model_behavior_failure` | 146 |
| `model_veriloga_subset_failure` | 27 |
| `model_incomplete_generation` | 4 |

## Failure Groups

| Failure group | Count |
| --- | ---: |
| `model_functional_behavior_failure` | 146 |
| `model_veriloga_or_spectre_subset_failure` | 27 |
| `model_incomplete_generation` | 4 |

## Root Cause Families For Non-Dual-Pass Rows

| Root cause family | Count |
| --- | ---: |
| `behavior_checker_mismatch` | 107 |
| `veriloga_spectre_subset_violation` | 18 |
| `Behavior: output stuck or reset/hold state wrong` | 7 |
| `Verilog-A subset: local declaration inside analog/procedural block` | 7 |
| `Behavior: analog transfer/reference macro wrong` | 12 |
| `Verilog-A subset: transition() used inside conditional/event block` | 1 |
| `Behavior: calibration/control algorithm wrong` | 5 |
| `Behavior: missing/incorrect event timing or stimulus coverage` | 7 |
| `Behavior: wrong decision/code sequence` | 6 |
| `Spectre TB syntax: malformed instance/source line` | 1 |
| `model_output_budget_exhausted` | 4 |
| `Behavior: sample/hold droop or hold-window behavior wrong` | 2 |

## By Form

| Form | Spectre pass | Dual pass | Total | Spectre rate | Dual rate |
| --- | ---: | ---: | ---: | ---: | ---: |
| `bugfix` | 13 | 13 | 52 | 25.0% | 25.0% |
| `dut` | 19 | 19 | 52 | 36.5% | 36.5% |
| `e2e` | 10 | 10 | 66 | 15.2% | 15.2% |
| `tb` | 17 | 17 | 66 | 25.8% | 25.8% |

## By Category

| Category | Spectre pass | Dual pass | Total | Spectre rate | Dual rate |
| --- | ---: | ---: | ---: | ---: | ---: |
| Baseband Signal Conditioning | 6 | 6 | 30 | 20.0% | 20.0% |
| Bias Reference and Power Management | 4 | 4 | 28 | 14.3% | 14.3% |
| Calibration, DEM, and Control | 1 | 1 | 26 | 3.8% | 3.8% |
| Comparator and Decision Circuits | 15 | 15 | 30 | 50.0% | 50.0% |
| Data Converter Models | 17 | 17 | 44 | 38.6% | 38.6% |
| PLL Clock and Timing Systems | 9 | 9 | 36 | 25.0% | 25.0% |
| RF and AFE Behavioral Macromodels | 3 | 3 | 24 | 12.5% | 12.5% |
| Sampling and Analog Memory | 4 | 4 | 18 | 22.2% | 22.2% |
