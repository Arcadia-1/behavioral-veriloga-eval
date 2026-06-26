# Source Smooth Tanh Comparator Audit

- Source: `wangx/comparator.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: Implement a smooth comparator macro. OUT follows tanh(4*(IN-REF-0.05)) and ranges from -1 V to +1 V.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch32-evas/292-source-smooth-tanh-comparator`
  - `WORK/source-import-batch32-spectre/292-source-smooth-tanh-comparator`
