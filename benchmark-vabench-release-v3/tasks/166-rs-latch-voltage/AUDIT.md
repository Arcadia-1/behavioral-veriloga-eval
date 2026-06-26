# Source RS Latch Voltage Audit

- Source: `wangx/rs_ff.va`
- Scenario: set/reset state latch for voltage-domain digital control.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable truth-table/state samples from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch9-evas/166-rs-latch-voltage`
  - `WORK/source-import-batch9-spectre/166-rs-latch-voltage`
