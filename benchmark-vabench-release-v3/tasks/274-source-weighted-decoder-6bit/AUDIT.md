# Source Weighted Decoder 6bit Audit

- Source: `lis/DEC_6bit.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: Implement a six-input weighted decoder. Inputs vd1..vd6 have weights 32,16,8,4,2,1 and VOUT equals VREF times the weighted sum divided by 32.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch30-evas/274-source-weighted-decoder-6bit`
  - `WORK/source-import-batch30-spectre/274-source-weighted-decoder-6bit`
