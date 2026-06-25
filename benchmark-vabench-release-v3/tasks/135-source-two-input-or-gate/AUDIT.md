# Source Two Input OR Gate Audit

- Source: `tangxy/or2.va`
- Scenario: voltage-domain two-input OR logic gate.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable semantic samples from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch4-evas/135-source-two-input-or-gate`
  - `WORK/source-import-batch4-spectre/135-source-two-input-or-gate`
