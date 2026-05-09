# Main120 C Compile-Loop Delta - 2026-05-09

Model: `mimo-v2.5-pro`; reasoning: `mimo_thinking:disabled`.

## Summary

| row | PASS | dut_compile | tb_compile | sim_correct | FAIL_DUT_COMPILE | FAIL_TB_COMPILE | FAIL_SIM_CORRECTNESS |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| D | 21/120 | 92/120 | 96/120 | 21/120 | 28 | 17 | 54 |
| C | 21/120 | 105/120 | 106/120 | 21/120 | 15 | 13 | 71 |

## Cost

- Repair calls: `47`
- Input/output/reasoning tokens: `145542` / `23046` / `0`
- Cached input tokens: `19968`
- API elapsed total: `439.928s`

## Interpretation

- Compile/interface closure improved on `17` tasks.
- PASS did not improve over D because repaired tasks mostly moved from compile/interface failure to behavior failure.
- This supports C as a compile-closure baseline, not a behavior-repair method.

