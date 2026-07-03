# Source Analog Multiplier Audit

- Source: `wangx/multiplier.va`
- Scenario: two-input analog multiplier with scalar gain.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable analog samples from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch7-evas/154-analog-multiplier`
  - `WORK/source-import-batch7-spectre/154-analog-multiplier`
