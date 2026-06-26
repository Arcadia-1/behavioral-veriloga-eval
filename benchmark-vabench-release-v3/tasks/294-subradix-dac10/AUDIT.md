# Source Subradix DAC10 Audit

- Source: `zhangad/dac_10bit_ideal.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: Implement a 10-bit sub-radix weighted DAC using radix 1.8 weights and normalization by 1024.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch32-evas/294-subradix-dac10`
  - `WORK/source-import-batch32-spectre/294-subradix-dac10`
