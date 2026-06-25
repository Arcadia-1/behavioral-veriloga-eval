# Source Level Shifter Offset Audit

- Source: `hexy/level_shifter.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: Implement a voltage-domain level shifter. OUT must equal IN plus a fixed 350 mV offset across the transient.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch30-evas/273-source-level-shifter-offset`
  - `WORK/source-import-batch30-spectre/273-source-level-shifter-offset`
