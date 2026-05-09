# Main120 Compile Strategy Matrix - MiMo-V2.5-Pro - 2026-05-09

Model setting for generation/repair rows: `mimo-v2.5-pro`, reasoning disabled, `max_tokens=4096`. Spectre audits use bridge profile `jin`, `spectre` mode, `max_workers=2`.

## Unified EVAS/Spectre Table

| row | PASS | compile OK | compile fail | behavior fail | DUT compile fail | TB compile fail | EVAS/Spectre PASS mismatch |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| A EVAS | 18/120 | 59/120 | 61/120 | 41/120 | 33 | 28 | 2 |
| A Spectre | 20/120 | 48/120 | 72/120 | 28/120 | 46 | 26 |  |
| D EVAS | 21/120 | 75/120 | 45/120 | 54/120 | 28 | 17 | 0 |
| D Spectre | 21/120 | 76/120 | 44/120 | 55/120 | 32 | 12 |  |
| C EVAS | 24/120 | 92/120 | 28/120 | 68/120 | 15 | 13 | 0 |
| C Spectre | 24/120 | 92/120 | 28/120 | 68/120 | 19 | 9 |  |
| S1 EVAS | 27/120 | 109/120 | 11/120 | 82/120 | 3 | 8 | 1 |
| S1 Spectre | 28/120 | 108/120 | 12/120 | 80/120 | 6 | 6 |  |
| S2 EVAS | 28/120 | 111/120 | 9/120 | 83/120 | 3 | 6 | 1 |
| S2 Spectre | 29/120 | 110/120 | 10/120 | 81/120 | 6 | 4 |  |

## Spectre Main Rows

| row | PASS | compile OK | compile fail | behavior fail | DUT compile fail | TB compile fail | delta vs D | delta vs C |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| A Spectre | 20/120 | 48/120 | 72/120 | 28/120 | 46 | 26 | -1 | -4 |
| D Spectre | 21/120 | 76/120 | 44/120 | 55/120 | 32 | 12 | +0 | -3 |
| C Spectre | 24/120 | 92/120 | 28/120 | 68/120 | 19 | 9 | +3 | +0 |
| S1 Spectre | 28/120 | 108/120 | 12/120 | 80/120 | 6 | 6 | +7 | +4 |
| S2 Spectre | 29/120 | 110/120 | 10/120 | 81/120 | 6 | 4 | +8 | +5 |

## Key Deltas
- `D_to_C_spectre_delta`: net `+3`, new PASS `3`, lost PASS `0`.
  - new: `vbm1_sar_logic_4b_e2e`, `vbm1_strongarm_comparator_behavior_dut`, `vbm1_voltage_clamp_tb`
- `C_to_S1_spectre_delta`: net `+4`, new PASS `5`, lost PASS `1`.
  - new: `vbm1_barrel_pointer_window_dut`, `vbm1_debounce_latch_bugfix`, `vbm1_precision_rectifier_bugfix`, `vbm1_precision_rectifier_dut`, `vbm1_sar_logic_4b_tb`
  - lost: `vbm1_voltage_clamp_tb`
- `C_to_S2_spectre_delta`: net `+5`, new PASS `5`, lost PASS `0`.
  - new: `vbm1_barrel_pointer_window_dut`, `vbm1_debounce_latch_bugfix`, `vbm1_precision_rectifier_bugfix`, `vbm1_precision_rectifier_dut`, `vbm1_sar_logic_4b_tb`
- `D_to_S1_spectre_delta`: net `+7`, new PASS `7`, lost PASS `0`.
  - new: `vbm1_barrel_pointer_window_dut`, `vbm1_debounce_latch_bugfix`, `vbm1_precision_rectifier_bugfix`, `vbm1_precision_rectifier_dut`, `vbm1_sar_logic_4b_e2e`, `vbm1_sar_logic_4b_tb`, `vbm1_strongarm_comparator_behavior_dut`
- `D_to_S2_spectre_delta`: net `+8`, new PASS `8`, lost PASS `0`.
  - new: `vbm1_barrel_pointer_window_dut`, `vbm1_debounce_latch_bugfix`, `vbm1_precision_rectifier_bugfix`, `vbm1_precision_rectifier_dut`, `vbm1_sar_logic_4b_e2e`, `vbm1_sar_logic_4b_tb`, `vbm1_strongarm_comparator_behavior_dut`, `vbm1_voltage_clamp_tb`
- `S1_to_S2_spectre_delta`: net `+1`, new PASS `1`, lost PASS `0`.
  - new: `vbm1_voltage_clamp_tb`

## Cost / Runtime Notes

- C LLM repair calls: `47`; input/output/reasoning tokens: `145542` / `23046` / `0`; API elapsed `439.928`s.
- S1 LLM repair calls: `47`; input/output/reasoning tokens: `155887` / `21212` / `0`; API elapsed `349.901`s.
- S2 selected compile-fail tasks: `28`; tasks with accepted local skill actions: `19`; accepted actions `19`; no LLM calls.

## Interpretation

- C establishes compile-loop as useful: Spectre PASS `21/120 -> 24/120`.
- S1 compile-skill prompt improves further to Spectre `28/120`, mainly by reducing compile failures to `12/120`.
- S2 deterministic accept/reject reaches Spectre `29/120`, one PASS above S1, with lower LLM cost because it does not call the model.
- Report overall compile fail before DUT/TB attribution, because EVAS and Spectre may disagree on attribution even when PASS/overall compile outcome is aligned.
