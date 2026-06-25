# Source Cyclic Decoder 12bit Audit

- Source: `zhangm/ADC12bit_decoder.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: cyclic ADC bit-vector reconstruction into normalized analog code.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch11-evas/178-source-cyclic-decoder-12bit`
  - `WORK/source-import-batch11-spectre/178-source-cyclic-decoder-12bit`
