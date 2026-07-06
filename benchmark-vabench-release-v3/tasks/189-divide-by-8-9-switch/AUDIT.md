# Source Divide By 8 9 Switch Audit

- Source: `huangsy/DIV8_9.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: control-switched divide-by-8/divide-by-9 clock divider.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
