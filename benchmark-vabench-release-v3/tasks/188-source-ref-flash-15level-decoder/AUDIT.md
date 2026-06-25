# Source Ref Flash 15level Decoder Audit

- Source: `zhangm/tb_REF_FLASH_15L_DECODER.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: 15-level flash thermometer count normalization.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch13-evas/188-source-ref-flash-15level-decoder`
  - `WORK/source-import-batch13-spectre/188-source-ref-flash-15level-decoder`
