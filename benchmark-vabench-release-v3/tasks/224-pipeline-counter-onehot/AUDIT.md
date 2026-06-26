# Source Pipeline Counter Onehot Audit

- Source: `caiyizeng25/V_counter.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: falling-edge modulo-six pipeline counter with one-hot phase and binary count outputs.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch20-evas/224-pipeline-counter-onehot`
  - `WORK/source-import-batch20-spectre/224-pipeline-counter-onehot`
