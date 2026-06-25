# Source Trim Ctrl 5bit Audit

- Source: `guoxy/ideal_TRIM_CTRL_5BITS.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: Implement a scalar-to-5-bit trim control encoder. Round AIN to an integer code and drive DOUT0..DOUT4 as voltage-coded binary bits.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch29-evas/269-source-trim-ctrl-5bit`
  - `WORK/source-import-batch29-spectre/269-source-trim-ctrl-5bit`
