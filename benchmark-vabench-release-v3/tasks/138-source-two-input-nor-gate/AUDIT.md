# Source Two Input NOR Gate Audit

- Source: `tangxy/nor2.va`
- Scenario: voltage-domain two-input NOR logic primitive.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable truth-table samples from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch5-evas/138-source-two-input-nor-gate`
  - `WORK/source-import-batch5-spectre/138-source-two-input-nor-gate`
