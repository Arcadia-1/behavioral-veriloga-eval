# Source L2 CDAC 4b Residue Audit

- Source: `wangxy/L2_CDAC_4b_ideal.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: sampled CDAC residue update with three binary control steps.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
