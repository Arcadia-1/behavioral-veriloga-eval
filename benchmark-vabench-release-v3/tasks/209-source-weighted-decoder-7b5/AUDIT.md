# Source Weighted Decoder 7b5 Audit

- Source: `shigao/V_DECODER_7B5.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: weighted SAR decoder producing 7-bit, 7.5-bit, and 8-bit normalized analog estimates.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch17-evas/209-source-weighted-decoder-7b5`
  - `WORK/source-import-batch17-spectre/209-source-weighted-decoder-7b5`
