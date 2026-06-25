# Source Analog Mux Threshold Audit

- Source: `wangx/analog_mux.va`
- Scenario: threshold-controlled two-input analog multiplexer.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable semantic samples from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch4-evas/130-source-analog-mux-threshold`
  - `WORK/source-import-batch4-spectre/130-source-analog-mux-threshold`
