# Source Attenuator Gain Audit

- Source: `wangx/attenuator.va`
- Scenario: decibel-configured voltage attenuation primitive.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable analog samples from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch6-evas/142-attenuator-gain`
  - `WORK/source-import-batch6-spectre/142-attenuator-gain`
