# Source Safe Analog Divider Audit

- Source: `wangx/divider.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: Implement a guarded voltage divider. OUT equals NUM/DEN, except small-magnitude denominators are clamped to +/-0.2 V with the original sign.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch31-evas/279-source-safe-analog-divider`
  - `WORK/source-import-batch31-spectre/279-source-safe-analog-divider`
