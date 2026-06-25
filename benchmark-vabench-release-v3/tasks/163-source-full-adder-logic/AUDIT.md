# Source Full Adder Logic Audit

- Source: `wangx/full_adder.va`
- Scenario: one-bit full adder with carry-in for digital control datapaths.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable truth-table/state samples from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch9-evas/163-source-full-adder-logic`
  - `WORK/source-import-batch9-spectre/163-source-full-adder-logic`
