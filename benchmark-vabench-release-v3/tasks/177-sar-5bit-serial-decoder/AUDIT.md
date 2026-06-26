# Source SAR 5bit Serial Decoder Audit

- Source: `zhangm/SAR_5bit_decoder.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: serial SAR decision accumulation and normalized code reporting.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch11-evas/177-sar-5bit-serial-decoder`
  - `WORK/source-import-batch11-spectre/177-sar-5bit-serial-decoder`
