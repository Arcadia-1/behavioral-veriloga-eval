# Source Three Input OR Gate Audit

- Source: `wangx/or3.va`
- Scenario: three-input OR logic primitive for voltage-domain control.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable truth-table samples from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch5-evas/140-source-three-input-or-gate`
  - `WORK/source-import-batch5-spectre/140-source-three-input-or-gate`
