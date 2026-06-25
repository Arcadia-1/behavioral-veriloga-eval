# Source Onehot Progress Encoder Audit

- Source: `zhaoh/VA_encoder_test.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: clocked one-hot progress marker with a scalar count output.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch17-evas/212-source-onehot-progress-encoder`
  - `WORK/source-import-batch17-spectre/212-source-onehot-progress-encoder`
