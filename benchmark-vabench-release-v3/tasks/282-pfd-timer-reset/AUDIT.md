# Source PFD Timer Reset Audit

- Source: `zhangz/L2_PFD.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: Implement a phase-frequency detector with delayed reset. A rising A edge asserts active-low UB; a rising B edge asserts D; when both have occurred, both reset after 100 ps.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch31-evas/282-pfd-timer-reset`
  - `WORK/source-import-batch31-spectre/282-pfd-timer-reset`
