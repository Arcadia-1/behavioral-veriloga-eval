# Source Hard Voltage Clamp Audit

- Source: `wangx/hard_voltage_clamp.va`
- Scenario: hard-limited voltage clamp for behavioral signal conditioning.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable analog samples from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch6-evas/145-hard-voltage-clamp`
  - `WORK/source-import-batch6-spectre/145-hard-voltage-clamp`
