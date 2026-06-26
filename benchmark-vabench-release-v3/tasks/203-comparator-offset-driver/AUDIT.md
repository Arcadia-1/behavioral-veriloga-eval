# Source Comparator Offset Driver Audit

- Source: `wangxy/L2_comparator_4b_offset.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: successive-approximation comparator-offset stimulus driver.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch16-evas/203-comparator-offset-driver`
  - `WORK/source-import-batch16-spectre/203-comparator-offset-driver`
