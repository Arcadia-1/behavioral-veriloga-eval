# Source Time Diff Detector Audit

- Source: `yangqihan/ideal_TIME_DIFF_DETECTOR.va`
- Scenario: edge timing difference converted to a bounded voltage.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable semantic samples from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch4-evas/133-source-time-diff-detector`
  - `WORK/source-import-batch4-spectre/133-source-time-diff-detector`
