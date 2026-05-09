# Main120 CTX1 Compact Diagnostics Comparison - 2026-05-09

CTX1 repeats the T1 10-task residual compile slice with `--compile-compact-diagnostics`.

## Slice Result

| row | PASS | compile OK | compile fail | behavior fail | DUT compile fail | TB compile fail |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| T1 EVAS | 0/10 | 8/10 | 2/10 | 8/10 | 2 | 0 |
| CTX1 EVAS | 0/10 | 8/10 | 2/10 | 8/10 | 2 | 0 |
| T1 Spectre | 1/10 | 7/10 | 3/10 | 6/10 | 2 | 1 |
| CTX1 Spectre | 1/10 | 7/10 | 3/10 | 6/10 | 2 | 1 |

## Cost

| row | api calls | input tokens | output tokens | total tokens | avg tokens/task | api elapsed s | avg api s/task |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| T1 | 28 | 102426 | 9979 | 112405 | 11240.5 | 214.088 | 21.409 |
| CTX1 | 34 | 120719 | 13495 | 134214 | 13421.4 | 365.749 | 36.575 |

## Per Task

| task | T1 rounds | CTX1 rounds | T1 tokens | CTX1 tokens | T1 Spectre | CTX1 Spectre |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| `vbm1_debounce_latch_e2e` | 1 | 2 | 9194 | 16992 | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |
| `vbm1_debounce_latch_tb` | 1 | 2 | 7206 | 14274 | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |
| `vbm1_edge_detector_e2e` | 2 | 2 | 16479 | 16358 | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |
| `vbm1_edge_detector_tb` | 2 | 2 | 14557 | 14454 | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |
| `vbm1_lock_detector_tb` | 2 | 2 | 14293 | 13785 | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |
| `vbm1_offset_comparator_e2e` | 1 | 1 | 8141 | 7867 | FAIL_TB_COMPILE | FAIL_TB_COMPILE |
| `vbm1_one_shot_timer_e2e` | 2 | 3 | 18473 | 26910 | FAIL_SIM_CORRECTNESS | FAIL_SIM_CORRECTNESS |
| `vbm1_resettable_integrator_bugfix` | 1 | 1 | 6984 | 6902 | FAIL_DUT_COMPILE | FAIL_DUT_COMPILE |
| `vbm1_vco_phase_integrator_bugfix` | 1 | 1 | 8018 | 7840 | FAIL_DUT_COMPILE | FAIL_DUT_COMPILE |
| `vbm1_voltage_clamp_dut` | 1 | 1 | 9060 | 8832 | PASS | PASS |

## Interpretation

- CTX1 compact diagnostics preserved the final EVAS/Spectre outcome on this 10-task slice: same Spectre PASS 1/10 and same compile fail 3/10 as T1.
- This first compact mode did not reduce total token cost. Total tokens increased from 112405 to 134214 because some tasks required extra rounds after raw validator notes were removed.
- For tasks with the same number of rounds, compact mode usually saved a small amount of tokens, but the savings were too small to offset extra rounds.
- Conclusion: dropping only verbose Validator notes is not a sufficient CTX1 strategy. Next CTX should use structured note compression/trace cards rather than deleting raw notes.

## Next CTX Direction

- Replace raw-note deletion with structured note compression: keep all distinct failure atoms but remove duplicated prose/log boilerplate.
- Add R0 trace cards for similar failure families so the model receives compressed but actionable repair memory.
- Measure per-round prompt tokens separately from total task tokens to distinguish true prompt compression from extra-round effects.
