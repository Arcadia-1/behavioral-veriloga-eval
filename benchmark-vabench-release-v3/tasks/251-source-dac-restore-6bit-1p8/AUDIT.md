# Source DAC Restore 6bit 1p8 Audit

- Source: `wangxy/L1_DAC_restore_6bit.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: Implement a 1.8 V-threshold clocked 6-bit restore DAC with D1 as MSB and D6 as LSB. The output is `(code + 0.5) * 3.6 / 64 - 1.8`.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch25-evas/251-source-dac-restore-6bit-1p8`
  - `WORK/source-import-batch25-spectre/251-source-dac-restore-6bit-1p8`
