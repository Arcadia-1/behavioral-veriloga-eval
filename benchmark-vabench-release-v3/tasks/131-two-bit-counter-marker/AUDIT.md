# Source Two Bit Counter Marker Audit

- Source: `zengsy/Counter_2b_VA.va`
- Scenario: one-cycle marker emitted every fourth clock edge.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable semantic samples from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch4-evas/131-two-bit-counter-marker`
  - `WORK/source-import-batch4-spectre/131-two-bit-counter-marker`
