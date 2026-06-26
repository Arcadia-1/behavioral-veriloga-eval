# Source Flash Data Align Pipeline Audit

- Source: `zhangm/FLASH_DATA_ALIGN_V2.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: flash thermometer count alignment through a four-cycle pipeline.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch14-evas/192-flash-data-align-pipeline`
  - `WORK/source-import-batch14-spectre/192-flash-data-align-pipeline`
