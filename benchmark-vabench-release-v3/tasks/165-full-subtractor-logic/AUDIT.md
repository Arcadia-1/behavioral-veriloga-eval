# Source Full Subtractor Logic Audit

- Source: `wangx/full_subtractor.va`
- Scenario: one-bit full subtractor with borrow-in for digital datapaths.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable truth-table/state samples from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch9-evas/165-full-subtractor-logic`
  - `WORK/source-import-batch9-spectre/165-full-subtractor-logic`
