# Source Latched Comparator Delay Audit

- Source: `jielu/L2_comp.va`
- Scenario: single-output latched comparator with supply-referenced output delay.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable semantic samples from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch3-evas/126-latched-comparator-delay`
  - `WORK/source-import-batch3-spectre/126-latched-comparator-delay`
