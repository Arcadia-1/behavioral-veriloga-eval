# Source Clocked Mux4 Sampler Audit

- Source: `zhangm/MUX4T1.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: falling-edge sampled four-input mux used before select changes.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch18-evas/216-clocked-mux4-sampler`
  - `WORK/source-import-batch18-spectre/216-clocked-mux4-sampler`
