# Source SAR Sum Weighted 11b Audit

- Source: `liudongyang/TB_SAR_SUM.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: nonbinary 11-bit SAR weighted code compression.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch16-evas/206-source-sar-sum-weighted-11b`
  - `WORK/source-import-batch16-spectre/206-source-sar-sum-weighted-11b`
