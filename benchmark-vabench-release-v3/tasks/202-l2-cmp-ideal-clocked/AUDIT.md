# Source L2 CMP Ideal Clocked Audit

- Source: `caiyizeng25/L2_CMP_Ideal.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: clocked comparator decision and reset behavior.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch16-evas/202-l2-cmp-ideal-clocked`
  - `WORK/source-import-batch16-spectre/202-l2-cmp-ideal-clocked`
