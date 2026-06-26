# Source SAR 13bit Serial Decoder Audit

- Source: `zhangm/SAR_13bit_decoder.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: Implement a 13-bit serial SAR decoder. CLKS rising publishes the previous accumulated result and resets the accumulator; READY rising consumes DIN into the current bit weight and counts high decisions.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch27-evas/261-sar-13bit-serial-decoder`
  - `WORK/source-import-batch27-spectre/261-sar-13bit-serial-decoder`
