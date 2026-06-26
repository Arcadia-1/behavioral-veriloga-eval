# Source SARFEND Logic 4b Audit

- Source: `guoxue25/SARFEND_LOGIC_FT_4B.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: four-bit SAR front-end logic that resets DAC trials, consumes comparator decisions, and publishes the previous-cycle decision word.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch19-evas/222-sarfend-logic-4b`
  - `WORK/source-import-batch19-spectre/222-sarfend-logic-4b`
