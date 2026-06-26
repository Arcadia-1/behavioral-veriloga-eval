# Source Flash Sum8 Fraction Audit

- Source: `zhangm/FLASH_SUM8_DELAY.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: clocked flash thermometer density measurement.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch12-evas/180-flash-sum8-fraction`
  - `WORK/source-import-batch12-spectre/180-flash-sum8-fraction`
