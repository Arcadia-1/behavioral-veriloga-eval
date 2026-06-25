# Source Limiting Differential Amplifier Audit

- Source: `wangx/limiting_diffamp.va`
- Scenario: gain-limited differential amplifier with asymmetric rails.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable analog samples from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch7-evas/153-source-limiting-differential-amplifier`
  - `WORK/source-import-batch7-spectre/153-source-limiting-differential-amplifier`
