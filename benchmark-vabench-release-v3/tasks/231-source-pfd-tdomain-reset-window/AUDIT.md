# Source PFD Tdomain Reset Window Audit

- Source: `zhangsh/PFD.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: time-domain phase-frequency detector with overlap hide-state and finite reset pulse window.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch21-evas/231-source-pfd-tdomain-reset-window`
  - `WORK/source-import-batch21-spectre/231-source-pfd-tdomain-reset-window`
