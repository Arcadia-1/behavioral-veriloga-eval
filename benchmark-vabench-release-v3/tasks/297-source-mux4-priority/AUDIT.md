# Source Mux4 Priority Audit

- Source: `zhaoty/MUX4.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: Implement a four-channel analog mux. A 2-bit select chooses IN0, IN1, IN2, or IN3 and forwards that voltage to OUT.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch32-evas/297-source-mux4-priority`
  - `WORK/source-import-batch32-spectre/297-source-mux4-priority`
