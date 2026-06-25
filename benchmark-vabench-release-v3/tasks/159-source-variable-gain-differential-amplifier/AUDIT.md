# Source Variable Gain Differential Amplifier Audit

- Source: `wangx/vargain_diffamp.va`
- Scenario: differential amplifier controlled by a differential gain input.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable analog samples from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch8-evas/159-source-variable-gain-differential-amplifier`
  - `WORK/source-import-batch8-spectre/159-source-variable-gain-differential-amplifier`
