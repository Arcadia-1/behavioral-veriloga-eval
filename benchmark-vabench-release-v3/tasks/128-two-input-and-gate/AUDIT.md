# Source Two Input AND Gate Audit

- Source: `tangxy/and2.va`
- Scenario: voltage-domain two-input logic gate with thresholded inputs.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable semantic samples from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch4-evas/128-two-input-and-gate`
  - `WORK/source-import-batch4-spectre/128-two-input-and-gate`
