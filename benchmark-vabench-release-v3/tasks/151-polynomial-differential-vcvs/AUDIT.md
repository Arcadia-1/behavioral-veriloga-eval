# Source Polynomial Differential VCVS Audit

- Source: `cuiyl/LI_VCVS_NLIN.va`
- Scenario: nonlinear differential voltage-controlled voltage source.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable analog samples from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch7-evas/151-polynomial-differential-vcvs`
  - `WORK/source-import-batch7-spectre/151-polynomial-differential-vcvs`
