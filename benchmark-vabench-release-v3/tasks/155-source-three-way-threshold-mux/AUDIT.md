# Source Three Way Threshold Mux Audit

- Source: `wangx/multiplexer.va`
- Scenario: three-input analog mux selected by a differential threshold window.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable analog samples from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch7-evas/155-source-three-way-threshold-mux`
  - `WORK/source-import-batch7-spectre/155-source-three-way-threshold-mux`
