# Source Offset Halving Search Audit

- Source: `zhangym/_va_offset.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: comparator-decision offset search driver that halves the search step on each CLK falling edge and drives VINP/VINN symmetrically.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled VINP/VINN values from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch24-evas/247-source-offset-halving-search`
  - `WORK/source-import-batch24-spectre/247-source-offset-halving-search`
