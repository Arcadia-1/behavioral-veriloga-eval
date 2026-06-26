# Source Three Input XOR Gate Audit

- Source: `wangx/xor3.va`
- Scenario: three-input parity/XOR logic primitive.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable truth-table samples from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch5-evas/141-three-input-xor-gate`
  - `WORK/source-import-batch5-spectre/141-three-input-xor-gate`
