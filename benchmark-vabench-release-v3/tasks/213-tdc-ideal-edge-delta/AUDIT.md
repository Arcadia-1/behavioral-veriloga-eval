# Source TDC Ideal Edge Delta Audit

- Source: `zhangm/TDC_IDEAL.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: time-to-digital edge interval measurement between two threshold crossings.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch18-evas/213-tdc-ideal-edge-delta`
  - `WORK/source-import-batch18-spectre/213-tdc-ideal-edge-delta`
