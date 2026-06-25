# Source Two Input XOR Gate Audit

- Source: `tangxy/xor2.va`
- Scenario: voltage-domain exclusive-or logic primitive.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable semantic samples from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch4-evas/129-source-two-input-xor-gate`
  - `WORK/source-import-batch4-spectre/129-source-two-input-xor-gate`
