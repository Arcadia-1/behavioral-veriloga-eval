# Source Ref Flash 8level Decoder Audit

- Source: `zhangm/tb_REF_FLASH_8L_DEC.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: 8-level flash thermometer count and residue calculation.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch13-evas/187-source-ref-flash-8level-decoder`
  - `WORK/source-import-batch13-spectre/187-source-ref-flash-8level-decoder`
