# Source Soft Voltage Clamp Audit

- Source: `wangx/soft_voltage_clamp.va`
- Scenario: smooth exponential voltage limiting near clamp rails.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable analog samples from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch8-evas/158-source-soft-voltage-clamp`
  - `WORK/source-import-batch8-spectre/158-source-soft-voltage-clamp`
