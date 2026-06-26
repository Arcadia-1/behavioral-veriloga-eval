# Source Absolute Value Audit

- Source: `wangx/absolute_value.va`
- Scenario: absolute-value signal conditioning for bipolar behavioral voltages.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable analog samples from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch7-evas/148-absolute-value`
  - `WORK/source-import-batch7-spectre/148-absolute-value`
