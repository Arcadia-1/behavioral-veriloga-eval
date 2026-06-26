# Source Decision Router Logic Audit

- Source: `wangx/digital_logic1.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: Implement a five-output decision router. The two decision inputs and a valid flag drive x, y, z, dm, and dl using the source-derived truth table.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch31-evas/278-source-decision-router-logic`
  - `WORK/source-import-batch31-spectre/278-source-decision-router-logic`
