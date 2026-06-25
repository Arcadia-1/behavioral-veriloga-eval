# Source Linear PFD Gain Audit

- Source: `zhangz/PFD_20201101.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: deterministic linear PFD gain macro without stochastic noise terms.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch15-evas/201-source-linear-pfd-gain`
  - `WORK/source-import-batch15-spectre/201-source-linear-pfd-gain`
