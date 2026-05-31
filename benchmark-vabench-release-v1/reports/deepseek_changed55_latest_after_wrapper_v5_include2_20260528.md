# DeepSeek Changed55 Latest After Wrapper-v5 Include Rerun

Generated: `2026-05-28T08:33:42.040555+00:00`

55 rows selected from wrapper-v4 changed rerun, with the two wrapper-v4 include-ambiguity rows replaced by wrapper-v5 rerun results

## Pass Rate

| Slice | Pass | Total | Pass rate |
| --- | ---: | ---: | ---: |
| changed55 latest | 7 | 55 | 12.7% |

## Status Counts

| Status | Count |
| --- | ---: |
| `FAIL_SIM_CORRECTNESS` | 39 |
| `PASS` | 7 |
| `FAIL_DUT_COMPILE` | 8 |
| `FAIL_TB_COMPILE` | 1 |

## Failure Status Counts

| Failure status | Count |
| --- | ---: |
| `FAIL_SIM_CORRECTNESS` | 39 |
| `FAIL_DUT_COMPILE` | 8 |
| `FAIL_TB_COMPILE` | 1 |

## Failure Root Families

| Root family | Count |
| --- | ---: |
| Behavior: output stuck or reset/hold state wrong | 7 |
| Behavior: analog transfer/reference macro wrong | 12 |
| Behavior: missing/incorrect event timing or stimulus coverage | 7 |
| Behavior: wrong decision/code sequence | 6 |
| Verilog-A subset: local declaration inside analog/procedural block | 7 |
| Behavior: calibration/control algorithm wrong | 5 |
| Behavior: sample/hold droop or hold-window behavior wrong | 2 |
| Spectre TB syntax: malformed instance/source line | 1 |
| Verilog-A subset: transition() used inside conditional/event block | 1 |

## By Form

| Form | Pass | Total | Pass rate |
| --- | ---: | ---: | ---: |
| `bugfix` | 1 | 11 | 9.1% |
| `dut` | 0 | 4 | 0.0% |
| `e2e` | 2 | 27 | 7.4% |
| `tb` | 4 | 13 | 30.8% |

## Wrapper-v5 Replacement Rows

| Release task id | Status | Root family | Evidence |
| --- | --- | --- | --- |
| `vbr1_l1_lna_gain_compression_macro:e2e` | `FAIL_SIM_CORRECTNESS` | Behavior: analog transfer/reference macro wrong | lna_small_signal_gain_missing vin=0.473 out=0.450 |
| `vbr1_l1_programmable_gain_amplifier:e2e` | `FAIL_SIM_CORRECTNESS` | Behavior: analog transfer/reference macro wrong | pga_unclamped_range=(0.000,1.500) |
