# Source Weighted SAR Decoder 9b Audit

- Source: `shigao/V_DECODER_2B.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: weighted SAR code reconstruction across 7-bit, 7.5-bit, and 8-bit views.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch11-evas/173-source-weighted-sar-decoder-9b`
  - `WORK/source-import-batch11-spectre/173-source-weighted-sar-decoder-9b`
