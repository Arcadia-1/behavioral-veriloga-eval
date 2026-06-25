# Source Comparator Offset Detect Audit

- Source: `guoxy/ideal_COMP_OS_DETECT.va`
- Scenario: successive-approximation comparator offset detector outputs.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable semantic samples from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch3-evas/124-source-comp-os-detect`
  - `WORK/source-import-batch3-spectre/124-source-comp-os-detect`
