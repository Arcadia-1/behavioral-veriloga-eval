# Source Differential Deadband Audit

- Source: `wangx/deadband_diffamp.va`
- Scenario: differential deadband amplifier with leakage bias.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable analog samples from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch6-evas/144-source-differential-deadband`
  - `WORK/source-import-batch6-spectre/144-source-differential-deadband`
