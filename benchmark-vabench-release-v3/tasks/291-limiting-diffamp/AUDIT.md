# Source Limiting Diffamp Audit

- Source: `wangx/limiting_diffamp.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: Implement a differential amplifier with hard output limits. OUT is 4*(INP-INN) clipped to +/-0.75 V.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch32-evas/291-limiting-diffamp`
  - `WORK/source-import-batch32-spectre/291-limiting-diffamp`
