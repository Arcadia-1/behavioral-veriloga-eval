# Source DAC 5V Weighted 7b Audit

- Source: `zhangm/DAC_5V.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: clocked 7-bit single-ended weighted DAC reconstruction.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
