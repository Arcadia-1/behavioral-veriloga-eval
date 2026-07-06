# Source PFD Tdomain Reset Window Audit

- Source: `zhangsh/PFD.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: time-domain phase-frequency detector with overlap hide-state and finite reset pulse window.
- Import status: certified only after visible compile, EVAS/Spectre semantic checks and parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
