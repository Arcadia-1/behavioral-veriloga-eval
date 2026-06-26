# Source Divide By Two Toggle Audit

- Source: `taoy/v_DIVIDER_2.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: basic divide-by-two clock/control primitive.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch12-evas/184-divide-by-two-toggle`
  - `WORK/source-import-batch12-spectre/184-divide-by-two-toggle`
