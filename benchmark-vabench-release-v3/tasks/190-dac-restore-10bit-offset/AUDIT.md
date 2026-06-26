# Source DAC Restore 10bit Offset Audit

- Source: `wangxy/DAC_restore_10bit.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: clocked 10-bit offset DAC reconstruction with source-specific weighting.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch14-evas/190-dac-restore-10bit-offset`
  - `WORK/source-import-batch14-spectre/190-dac-restore-10bit-offset`
