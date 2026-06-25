# Source Half Subtractor Logic Audit

- Source: `wangx/half_subtractor.va`
- Scenario: one-bit subtractor cell with borrow output.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable truth-table/state samples from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch9-evas/164-source-half-subtractor-logic`
  - `WORK/source-import-batch9-spectre/164-source-half-subtractor-logic`
