# Source Smooth Comparator Tanh Audit

- Source: `chenr/comparator_ideal.va`
- Scenario: continuous tanh comparator macro model.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable analog samples from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch6-evas/146-source-smooth-comparator-tanh`
  - `WORK/source-import-batch6-spectre/146-source-smooth-comparator-tanh`
