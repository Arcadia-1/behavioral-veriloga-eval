# Source L2 CDAC 4b Switch Audit

- Source: `yueyh/L2_CDAC_4bit_swi.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: ready-clocked 4-bit switched-CDAC output estimator with first-sample discard.
- Import status: certified only after visible compile, EVAS/Spectre semantic checks and parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
