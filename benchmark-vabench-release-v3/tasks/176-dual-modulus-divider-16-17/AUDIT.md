# Source Dual Modulus Divider 16 17 Audit

- Source: `zengsy/DIV_16_17_VA.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: dual-modulus PLL divider control primitive.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
