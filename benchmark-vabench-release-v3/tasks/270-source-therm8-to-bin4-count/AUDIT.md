# Source Therm8 To Bin4 Count Audit

- Source: `liudongyang/tb_therm8_to_bin4.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: Implement an 8-input thermometer-popcount encoder. Count high thermometer inputs and drive the count as a 4-bit voltage-coded binary value.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch29-evas/270-source-therm8-to-bin4-count`
  - `WORK/source-import-batch29-spectre/270-source-therm8-to-bin4-count`
