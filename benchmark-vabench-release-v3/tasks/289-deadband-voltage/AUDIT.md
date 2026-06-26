# Source Deadband Voltage Audit

- Source: `wangx/deadband.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: Implement a deadband shaper. OUT is zero within [-0.25 V, +0.25 V], otherwise it reports the excess beyond the nearest threshold.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch32-evas/289-deadband-voltage`
  - `WORK/source-import-batch32-spectre/289-deadband-voltage`
