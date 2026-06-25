# Source Comparator Reset Low 1p8 Audit

- Source: `zhangfm/comparator_ideal.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: Implement a 1.8 V clocked comparator. On CMPCK rising, compare VINP/VINN; on CMPCK falling, reset both outputs low.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch26-evas/257-source-comparator-reset-low-1p8`
  - `WORK/source-import-batch26-spectre/257-source-comparator-reset-low-1p8`
