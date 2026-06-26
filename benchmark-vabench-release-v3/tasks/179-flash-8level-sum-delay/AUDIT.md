# Source Flash 8level Sum Delay Audit

- Source: `zhangm/FLASH_8_LEVEL.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: flash ADC thermometer summation with one-cycle delayed summary.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch12-evas/179-flash-8level-sum-delay`
  - `WORK/source-import-batch12-spectre/179-flash-8level-sum-delay`
