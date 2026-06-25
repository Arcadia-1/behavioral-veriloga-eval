# Source Offset Bisection Driver Audit

- Source: `hexy/COMP_OS_TEST.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: comparator offset bisection stimulus that moves differential inputs around a common-mode center.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch17-evas/208-source-offset-bisection-driver`
  - `WORK/source-import-batch17-spectre/208-source-offset-bisection-driver`
