# Source Differential Gain Driver Audit

- Source: `wangx/diffdriver.va`
- Scenario: single-ended reference plus symmetric differential output driver.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable analog samples from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch7-evas/152-source-differential-gain-driver`
  - `WORK/source-import-batch7-spectre/152-source-differential-gain-driver`
