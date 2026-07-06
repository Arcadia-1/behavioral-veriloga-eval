# Source L1 DAC 4b Bipolar Audit

- Source: `wangxy/L1_DAC_4b_ideal.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: ready-triggered four-bit bipolar DAC reconstruction.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
