# Source DAC Restore 4bit Clocked Audit

- Source: `wangxy/DAC_restore_4bit.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: Implement a clocked 4-bit restore DAC. On CLK rising, decode D3..D0 as a binary word and output the centered bin voltage `(code + 0.5) * 1.8 / 16 - 0.9`.
- Import status: certified only after visible compile, EVAS/Spectre semantic checks, parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
