# Source Absolute Value Audit

- Source: `wangx/absolute_value.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: Implement an absolute-value voltage primitive. OUT must track abs(IN) for positive and negative inputs.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch32-evas/288-absolute-value`
  - `WORK/source-import-batch32-spectre/288-absolute-value`
