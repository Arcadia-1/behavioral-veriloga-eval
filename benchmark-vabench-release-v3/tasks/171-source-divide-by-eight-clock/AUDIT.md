# Source Divide By Eight Clock Audit

- Source: `huangsy/DIV8.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: frequency division for clock/control behavioral models.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch10-evas/171-source-divide-by-eight-clock`
  - `WORK/source-import-batch10-spectre/171-source-divide-by-eight-clock`
