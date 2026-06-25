# Source Ideal Differential Opamp Audit

- Source: `taoy/OPAMP.va`
- Scenario: ideal differential output opamp centered around common-mode.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable analog samples from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch8-evas/161-source-ideal-differential-opamp`
  - `WORK/source-import-batch8-spectre/161-source-ideal-differential-opamp`
