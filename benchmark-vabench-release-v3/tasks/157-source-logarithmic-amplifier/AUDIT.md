# Source Logarithmic Amplifier Audit

- Source: `wangx/log_amp.va`
- Scenario: bounded logarithmic measurement of an offset signal.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable analog samples from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch8-evas/157-source-logarithmic-amplifier`
  - `WORK/source-import-batch8-spectre/157-source-logarithmic-amplifier`
