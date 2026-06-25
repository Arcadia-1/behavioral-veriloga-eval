# Source Max Detector Hold Audit

- Source: `hexy/maxDetector.va`
- Scenario: peak/max voltage detector with monotonic hold output.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable semantic samples from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch4-evas/132-source-max-detector-hold`
  - `WORK/source-import-batch4-spectre/132-source-max-detector-hold`
