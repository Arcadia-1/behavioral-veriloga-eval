# Source Clocked Four Input Mux Audit

- Source: `zhangm/MUX4T1.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: clocked analog mux sampling for switched-cap/control flows.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch10-evas/170-source-clocked-four-input-mux`
  - `WORK/source-import-batch10-spectre/170-source-clocked-four-input-mux`
