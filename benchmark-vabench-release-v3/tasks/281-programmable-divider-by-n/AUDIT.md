# Source Programmable Divider By N Audit

- Source: `zhangm/divider.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: Implement a programmable clock divider. The output is high only when the internal edge counter is zero; with DIVCTRL=3 it asserts every third rising edge.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch31-evas/281-programmable-divider-by-n`
  - `WORK/source-import-batch31-spectre/281-programmable-divider-by-n`
