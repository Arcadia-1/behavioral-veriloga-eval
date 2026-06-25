# Source PFD Reset Pulse Audit

- Source: `zhangym/L2_PFD.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: phase-frequency detector latch with delayed mutual reset after both reference and feedback edges arrive.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch20-evas/226-source-pfd-reset-pulse`
  - `WORK/source-import-batch20-spectre/226-source-pfd-reset-pulse`
