# Source Differential Amplifier Core Audit

- Source: `wangx/diffamp.va`
- Scenario: single-ended output differential amplifier primitive.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable analog samples from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch8-evas/156-differential-amplifier-core`
  - `WORK/source-import-batch8-spectre/156-differential-amplifier-core`
