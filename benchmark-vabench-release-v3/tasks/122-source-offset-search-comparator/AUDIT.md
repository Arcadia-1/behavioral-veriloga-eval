# Source Offset Search Comparator Audit

- Source: `caiyizeng25/V_comp_offset.va`
- Scenario: binary-search style comparator-offset stimulus generator.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable semantic samples from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch3-evas/122-source-offset-search-comparator`
  - `WORK/source-import-batch3-spectre/122-source-offset-search-comparator`
