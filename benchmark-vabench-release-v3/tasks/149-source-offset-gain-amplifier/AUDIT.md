# Source Offset Gain Amplifier Audit

- Source: `wangx/amp.va`
- Scenario: linear amplifier with input offset subtraction.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable analog samples from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch7-evas/149-source-offset-gain-amplifier`
  - `WORK/source-import-batch7-spectre/149-source-offset-gain-amplifier`
