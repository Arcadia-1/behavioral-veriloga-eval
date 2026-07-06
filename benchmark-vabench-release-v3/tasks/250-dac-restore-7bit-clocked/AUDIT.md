# Source DAC Restore 7bit Clocked Audit

- Source: `wangxy/DAC_restore_7bit.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: Implement a clocked 7-bit restore DAC. On CLK rising, decode D6..D0 and output `(code + 0.5) * 1.8 / 128 - 0.9`.
- Import status: certified only after visible compile, EVAS/Spectre semantic checks, parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
