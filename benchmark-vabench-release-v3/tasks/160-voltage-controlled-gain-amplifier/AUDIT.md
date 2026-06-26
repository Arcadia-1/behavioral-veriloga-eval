# Source Voltage Controlled Gain Amplifier Audit

- Source: `wangx/vc_vg_diffamp.va`
- Scenario: voltage-controlled differential gain block with output rails.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable analog samples from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch8-evas/160-voltage-controlled-gain-amplifier`
  - `WORK/source-import-batch8-spectre/160-voltage-controlled-gain-amplifier`
