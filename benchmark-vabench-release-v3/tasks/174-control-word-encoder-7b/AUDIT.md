# Source Control Word Encoder 7b Audit

- Source: `shigao/V_ENCODER_7B.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: deterministic control-word voltage source for converter trim/configuration.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch11-evas/174-control-word-encoder-7b`
  - `WORK/source-import-batch11-spectre/174-control-word-encoder-7b`
