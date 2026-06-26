# Source Two Channel Sample Demux Audit

- Source: `zhangm/TI_2C_DEMUX_VA.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: time-interleaved two-channel analog sample selection.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch12-evas/181-two-channel-sample-demux`
  - `WORK/source-import-batch12-spectre/181-two-channel-sample-demux`
