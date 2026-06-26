# Source Deadband Window Audit

- Source: `wangx/deadband.va`
- Scenario: windowed deadband error extraction around zero.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable analog samples from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch6-evas/143-deadband-window`
  - `WORK/source-import-batch6-spectre/143-deadband-window`
