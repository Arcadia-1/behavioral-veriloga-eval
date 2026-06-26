# Source Samplehold Rising Edge Audit

- Source: `hexy/samplehold.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: Implement a rising-edge sample-and-hold. Each control rising edge captures IN and holds that voltage on OUT until the next capture.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch29-evas/268-samplehold-rising-edge`
  - `WORK/source-import-batch29-spectre/268-samplehold-rising-edge`
