# Main120 C Maintained EVAS + Spectre Audit - 2026-05-09

Condition: `C compile-loop`, model `mimo-v2.5-pro`, reasoning disabled, generation `max_tokens=4096`, generation workers `8`. Spectre audit used bridge profile `jin`, `spectre` mode, `max_workers=2`, `--resume`.

## Main Table

| row | PASS | dut_compile | tb_compile | sim_correct | FAIL_DUT_COMPILE | FAIL_TB_COMPILE | FAIL_SIM_CORRECTNESS |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| D EVAS parityfix/spliced | 21/120 | 92/120 | 96/120 | 21/120 | 28 | 17 | 54 |
| D Spectre | 21/120 | 76/120 | 76/120 | 21/120 | 32 | 12 | 55 |
| C EVAS maintained | 24/120 | 105/120 | 106/120 | 24/120 | 15 | 13 | 68 |
| C Spectre | 24/120 | 92/120 | 92/120 | 24/120 | 19 | 9 | 68 |

## C EVAS/Spectre Agreement

- PASS mismatch: `0/120`.
- Raw status-label mismatch: `4/120`.
- Status-label mismatch tasks:
  - `vbm1_debounce_latch_e2e`: EVAS `FAIL_TB_COMPILE` vs Spectre `FAIL_DUT_COMPILE`
  - `vbm1_offset_comparator_e2e`: EVAS `FAIL_TB_COMPILE` vs Spectre `FAIL_DUT_COMPILE`
  - `vbm1_one_shot_timer_e2e`: EVAS `FAIL_TB_COMPILE` vs Spectre `FAIL_DUT_COMPILE`
  - `vbm1_voltage_clamp_dut`: EVAS `FAIL_TB_COMPILE` vs Spectre `FAIL_DUT_COMPILE`

## D -> C Spectre Delta

- PASS delta: `+3` (`21/120` -> `24/120`).
- New Spectre PASS tasks: `3`.
  - `vbm1_sar_logic_4b_e2e`: D `FAIL_DUT_COMPILE` -> C `PASS`
  - `vbm1_strongarm_comparator_behavior_dut`: D `FAIL_DUT_COMPILE` -> C `PASS`
  - `vbm1_voltage_clamp_tb`: D `FAIL_TB_COMPILE` -> C `PASS`
- Lost Spectre PASS tasks: `0`.

## Interpretation

- Maintained EVAS replay and full Spectre audit agree on C PASS: `24/120`.
- C improves Spectre PASS from `21/120` to `24/120`, with no lost PASS tasks.
- C improves compile closure substantially, but most rescued compile failures become behavior failures; C remains a compile-closure method rather than a behavior-repair method.
