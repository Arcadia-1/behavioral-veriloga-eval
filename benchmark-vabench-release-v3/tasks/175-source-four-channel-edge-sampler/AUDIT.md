# Source Four Channel Edge Sampler Audit

- Source: `tangxy/SINGLE_EDGE_SAMPLER.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: multi-lane analog sample-and-hold for converter output capture.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch11-evas/175-source-four-channel-edge-sampler`
  - `WORK/source-import-batch11-spectre/175-source-four-channel-edge-sampler`
