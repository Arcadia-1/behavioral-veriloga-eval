# Source L2 CDAC 4b Switch Audit

- Source: `yueyh/L2_CDAC_4bit_swi.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: ready-clocked 4-bit switched-CDAC output estimator with first-sample discard.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch23-evas/239-l2-cdac-4b-switch`
  - `WORK/source-import-batch23-spectre/239-l2-cdac-4b-switch`
