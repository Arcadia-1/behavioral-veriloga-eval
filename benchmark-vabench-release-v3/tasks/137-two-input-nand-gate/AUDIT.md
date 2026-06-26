# Source Two Input NAND Gate Audit

- Source: `tangxy/nand2.va`
- Scenario: voltage-domain two-input NAND logic primitive.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable truth-table samples from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch5-evas/137-two-input-nand-gate`
  - `WORK/source-import-batch5-spectre/137-two-input-nand-gate`
