# Source Bin2ther 2b Audit

- Source: `cuiyl/bin2ther_2b.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: Implement the source 2-bit thermometer encoder. The MSB drives t0 and t1 high together, while the LSB independently drives t2.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch28-evas/265-bin2ther-2b`
  - `WORK/source-import-batch28-spectre/265-bin2ther-2b`
