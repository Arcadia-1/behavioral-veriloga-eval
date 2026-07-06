# Source Linear PFD Gain Audit

- Source: `zhangz/PFD_20201101.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: deterministic linear PFD gain macro without stochastic noise terms.
- Import status: certified only after visible compile, EVAS/Spectre semantic checks and parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
