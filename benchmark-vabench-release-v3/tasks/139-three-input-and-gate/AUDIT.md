# Source Three Input AND Gate Audit

- Source: `wangx/and3.va`
- Scenario: three-input logic gate for voltage-domain behavioral control.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable truth-table samples from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch5-evas/139-three-input-and-gate`
  - `WORK/source-import-batch5-spectre/139-three-input-and-gate`
