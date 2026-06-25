# Source Offset RDAC Search Flow Audit

- Source: `zhaoh/VA_comparator_offset_calib_rdac.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: combined RDAC code search followed by comparator offset bisection and reference stepping.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch19-evas/219-source-offset-rdac-search-flow`
  - `WORK/source-import-batch19-spectre/219-source-offset-rdac-search-flow`
